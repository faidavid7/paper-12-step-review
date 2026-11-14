"""交付前檢查。用法：python check_review.py --pdf X_annotated.pdf [--md X.md] [--issues issues.json]"""
import argparse, json, re, sys, collections, pymupdf
from annotate_tools import norm, marked_text

ap = argparse.ArgumentParser()
ap.add_argument("--pdf", required=True); ap.add_argument("--md"); ap.add_argument("--issues")
a = ap.parse_args()
doc = pymupdf.open(a.pdf)
errs = []
ID = re.compile(r"\b([PR]\d+-?[A-Z]?\d*)\b")
TIME = re.compile(r"20\d\d-\d\d-\d\d \d\d:\d\d")
FRONT = ["整體判斷", "定位", "論文類型", "Fatal", "方法與實驗", "呈現", "合規"]
FRONT_EN = ["overall", "position", "paper type", "fatal", "method", "presentation", "compliance"]

# 1. 總評頁與圖例頁
front = doc[0].get_text().lower()
if not (all(k.lower() in front for k in FRONT) or all(k in front for k in FRONT_EN)):
    miss = [k for k in FRONT if k.lower() not in front]
    errs.append(f"總評頁缺少項目：{miss}")
if "#ffeb3b" not in doc[-1].get_text().lower():
    errs.append("最後一頁不是顏色圖例")

def caption_near(page, r):
    best = None
    for b in page.get_text("blocks"):
        m = re.match(r"\s*(Figure|Fig\.)\s*(\d+)\s*[:.]", b[4])
        if m:
            d = abs(b[1] - r.y1) if b[1] >= r.y0 - 5 else 1e9
            if best is None or d < best[0]:
                best = (d, f"Fig.{m.group(2)}")
    return best[1] if best else f"未知圖(p{page.number+1})"

# 2. 逐則檢查註解
issues = json.load(open(a.issues, encoding="utf-8")) if a.issues else None
sent = {}
if issues:
    for it in issues.get("issues", []) + issues.get("reading_guide", []):
        if it.get("sentence"):
            sent[it["id"]] = it["sentence"]
marked = collections.defaultdict(str)
fig_contents = collections.defaultdict(list)
fig_seen = set()
pdf_ids = set()
for pno in range(1, len(doc) - 1):
    page = doc[pno]
    hl = []
    for an in page.annots():
        t, title, content = an.type[1], an.info["title"], an.info["content"]
        if not TIME.search(title):
            errs.append(f"p{pno+1} {title[:20]}：標題沒有標註時間")
        lines = [l for l in content.split("\n") if l.strip()]
        if "（續）" not in title and (len(lines) < 2 or any(len(l.split("：", 1)[-1].strip()) < 5 for l in lines)):
            errs.append(f"p{pno+1} {title[:20]}：內容少於兩行，或有欄位只寫關鍵字")
        m = re.match(r"\s*(Fig\.\s*\d+)", title)
        is_fig = t == "Square" and (m or "區塊切分" in content or "Blocks" in content)
        if is_fig and "(" not in title.split("｜")[0]:
            key = m.group(1).replace(" ", "") if m else caption_near(page, an.rect)
            fig_seen.add(key)
            fig_contents[content].append(f"p{pno+1} {key}")
            r = an.rect
            draws = [d["rect"] for d in page.get_drawings()] + [pymupdf.Rect(i["bbox"]) for i in page.get_image_info()]
            if r.height < 60 or not any(r.intersects(d) for d in draws):
                errs.append(f"p{pno+1} {key}：框太小或框內沒有圖形（h={r.height:.0f}），可能框到 caption")
            continue
        for i in ID.findall(title.split("｜")[0]):
            pdf_ids.add(i)
        if t in ("Highlight", "Underline"):
            txt = marked_text(page, an)
            for i in ID.findall(title.split("｜")[0]):
                marked[i] += txt
            hl.append((t, title, [pymupdf.Quad(an.vertices[j:j+4]).rect for j in range(0, len(an.vertices), 4)]))
    for x in range(len(hl)):
        for y in range(x + 1, len(hl)):
            if hl[x][0] != hl[y][0]:
                continue  # 底線與螢光可以並存
            if any(r1.intersects(r2) and (r1 & r2).get_area() > 4 for r1 in hl[x][2] for r2 in hl[y][2]):
                errs.append(f"p{pno+1}：{hl[x][1][:12]} 與 {hl[y][1][:12]} 重疊，請合併成一則")

for c, where in fig_contents.items():
    if len(where) > 1:
        errs.append(f"圖註解內容完全相同（套版）：{where}")

# 3. 每張圖都要有圖註解
figs = set()
for pno in range(1, len(doc) - 1):
    for b in doc[pno].get_text("blocks"):
        m = re.match(r"\s*(Figure|Fig\.)\s*(\d+)\s*[:.]", b[4])
        if m:
            figs.add(f"Fig.{m.group(2)}")
if figs - fig_seen:
    errs.append(f"以下圖沒有圖註解：{sorted(figs - fig_seen, key=lambda s: int(s[4:]))}")

# 4. 整句涵蓋與標過頭
for i, s in sent.items():
    if i not in marked:
        continue
    ms, ss = norm(marked[i]), norm(s)
    if ss not in ms:
        errs.append(f"{i}：沒有涵蓋整句")
    elif len(ms) > len(ss) * 1.15 + 20:
        errs.append(f"{i}：標記超出原句")

# 5. md、issues.json、PDF 的編號一致
if issues:
    ids = {it["id"] for it in issues["issues"]}
    located = {it["id"] for it in issues["issues"] if it.get("page") and it.get("kind") != "figure"}
    for it in issues["issues"]:
        if it.get("kind") == "figure" and it.get("figure", "").replace(" ", "") not in fig_seen:
            errs.append(f"{it['id']}：{it.get('figure')} 沒有圖註解")
    if located - pdf_ids:
        errs.append(f"issues.json 有、PDF 沒標：{sorted(located - pdf_ids)}")
    if (pdf_ids - ids) - {r["id"] for r in issues.get("reading_guide", [])}:
        errs.append(f"PDF 有、issues.json 沒有：{sorted(pdf_ids - ids)}")
    if a.md:
        md_ids = set(re.findall(r"\bP\d+-\d+\b", open(a.md, encoding="utf-8").read()))
        if ids ^ md_ids:
            errs.append(f"md 與 issues.json 編號不一致：只在 md {sorted(md_ids - ids)}；只在 json {sorted(ids - md_ids)}")

print("\n".join(errs) if errs else "全部通過")
print(f"共 {len(errs)} 項錯誤")
sys.exit(1 if errs else 0)
