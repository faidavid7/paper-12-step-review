"""paper-polish 交付前檢查。

用法：python check_polish.py --frozen frozen.json --tex main.tex [sec/*.tex ...] --pdf main.pdf
      [--log main.log] [--changelog paper-polish_zh.md] [--figures figures/] [--venue-pages 9]
"""
import argparse, json, re, sys, pathlib, pymupdf

sys.stdout.reconfigure(encoding="utf-8")  # Windows 主控台預設 cp950 會印成亂碼

ap = argparse.ArgumentParser()
ap.add_argument("--frozen", required=True)
ap.add_argument("--tex", required=True, nargs="+")
ap.add_argument("--pdf", required=True)
ap.add_argument("--log")
ap.add_argument("--changelog")
ap.add_argument("--figures")
ap.add_argument("--venue-pages", type=int)
a = ap.parse_args()
errs = []


def strip_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)


def ws(s):
    return re.sub(r"\s+", "", s)


def eq_norm(s):
    return ws(re.sub(r"\\nonumber|\\notag|\\\\|&", "", s))


tex = "\n".join(strip_comments(pathlib.Path(p).read_text(encoding="utf-8")) for p in a.tex)
tex_ws, tex_eq = ws(tex), eq_norm(tex)
frozen = json.load(open(a.frozen, encoding="utf-8"))
log_md = pathlib.Path(a.changelog).read_text(encoding="utf-8") if a.changelog else ""

# 1. 凍結清單：數字、表格儲存格、公式、claim
for n in frozen.get("numbers", []):
    v = re.escape(n["value"])
    if not re.search(rf"(?<![\d.]){v}(?![\d])", tex):
        errs.append(f"數字 {n['value']} 不見了（原句：{n.get('sentence', '')[:60]}）")
for t in frozen.get("tables", []):
    for c in t.get("cells", []):
        if ws(c) and ws(c) not in tex_ws:
            errs.append(f"{t.get('label', '表格')} 的儲存格 {c!r} 不見了")
for e in frozen.get("equations", []):
    if eq_norm(e["body"]) not in tex_eq:
        errs.append(f"公式 {e.get('label', e['body'][:30])} 的內容改變了")
for c in frozen.get("claims", []):
    if ws(c["sentence"]) not in tex_ws and ws(c["sentence"]) not in ws(log_md):
        errs.append(f"{c.get('where', '')} 的 claim 被改了，但修改紀錄沒有記錄原句：{c['sentence'][:60]}")

# 2. 修改紀錄：每列 C 編號都要標使用者是否同意
if a.changelog:
    for line in log_md.splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and re.fullmatch(r"C\d+", cells[0]):
            if not re.search(r"^(是|yes|使用者未同意)$", cells[-1], re.I):
                errs.append(f"{cells[0]}：最後一欄沒有標「是」或「使用者未同意」")
else:
    errs.append("沒有給 --changelog，無法檢查修改紀錄")

# 3. PDF：頁數、字型
doc = pymupdf.open(a.pdf)
if a.venue_pages:
    ref = next((p for p in doc for b in p.get_text("blocks")
                if re.fullmatch(r"\s*(\d+\s*)?(References|Bibliography|參考文獻)\s*", b[4])), None)
    if ref is None:
        errs.append("找不到 References 標題，無法判斷正文頁數，請人工確認")
    else:
        y = next(b[1] for b in ref.get_text("blocks")
                 if re.fullmatch(r"\s*(\d+\s*)?(References|Bibliography|參考文獻)\s*", b[4]))
        body = ref.number + (1 if y > ref.rect.height * 0.15 else 0)
        if body > a.venue_pages:
            errs.append(f"正文約 {body} 頁，超過上限 {a.venue_pages} 頁")
bad_fonts = set()
for p in doc:
    for f in p.get_fonts():
        if f[2] == "Type3" or f[1] == "n/a":
            bad_fonts.add(f"{f[3]}（{'Type 3' if f[2] == 'Type3' else '未嵌入'}）")
if bad_fonts:
    errs.append(f"PDF 字型問題：{sorted(bad_fonts)}")

# 4. figures/ 中的圖要是向量 PDF
if a.figures:
    for f in sorted(pathlib.Path(a.figures).iterdir()):
        if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            if f.stem not in {x.stem for x in pathlib.Path(a.figures).glob("*.pdf")}:
                errs.append(f"{f.name}：點陣圖，沒有對應的向量 PDF（定性結果的圖片請在 spec.md 註明）")
        elif f.suffix.lower() == ".pdf":
            p = pymupdf.open(f)[0]
            if not p.get_drawings() and not p.get_text().strip():
                errs.append(f"{f.name}：只有點陣圖，不是向量 PDF")

# 5. 編譯：未定義的參照與引用
if a.log:
    lg = pathlib.Path(a.log).read_text(encoding="utf-8", errors="ignore")
    undef = sorted(set(re.findall(r"(?:Reference|Citation) `([^']+)' on page \d+ undefined", lg)))
    errs += [f"未定義的參照或引用：{m}" for m in undef]
    if "There were undefined references" in lg and not undef:
        errs.append("log 顯示有未定義的參照")
else:
    errs.append("沒有給 --log，無法檢查編譯結果")

# 6. 每張圖都被引用、編號連續
labels = re.findall(r"\\begin\{figure\*?\}.*?\\label\{([^}]+)\}.*?\\end\{figure\*?\}", tex, re.S)
for lb in labels:
    if not re.search(r"\\(?:[cC]?ref|autoref|subref)\{[^}]*\b" + re.escape(lb) + r"\b", tex):
        errs.append(f"{lb}：內文沒有引用這張圖")
nums = sorted({int(m) for p in doc for m in re.findall(r"^\s*(?:Figure|Fig\.)\s*(\d+)\s*[:.]", p.get_text(), re.M)})
if nums and nums != list(range(1, nums[-1] + 1)):
    errs.append(f"圖的編號不連續：{nums}")

print("\n".join(errs) if errs else "全部通過")
print(f"共 {len(errs)} 項錯誤")
sys.exit(1 if errs else 0)
