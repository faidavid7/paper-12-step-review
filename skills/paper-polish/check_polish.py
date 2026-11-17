"""paper-polish 交付前檢查。

用法：python check_polish.py --frozen frozen.json --tex main.tex [sec/*.tex ...] --pdf main.pdf
      [--log main.log] [--changelog paper-polish_zh.md] [--figures figures/] [--venue-pages 9]
      [--orig-tex 原始的 main.tex sec/*.tex]
"""
import argparse, csv, json, re, subprocess, sys, tempfile, pathlib, pymupdf

sys.stdout.reconfigure(encoding="utf-8")  # Windows 主控台預設 cp950 會印成亂碼

ap = argparse.ArgumentParser()
ap.add_argument("--frozen", required=True)
ap.add_argument("--tex", required=True, nargs="+")
ap.add_argument("--pdf", required=True)
ap.add_argument("--log")
ap.add_argument("--changelog")
ap.add_argument("--figures")
ap.add_argument("--venue-pages", type=int)
ap.add_argument("--body-end", help="正文結束的標題（不計入頁數的段落），例如 LLM Usage Statement")
ap.add_argument("--orig-tex", nargs="+", help="原始的 .tex，用來找出沒有重畫的圖")
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

# 1b. 凍結清單要完整：原稿有表格、公式時，frozen.json 也要有；claim 至少要有貢獻列表
src = tex
if a.orig_tex:
    src = "\n".join(strip_comments(pathlib.Path(p).read_text(encoding="utf-8")) for p in a.orig_tex)
if re.search(r"\\begin\{tabular", src) and not frozen.get("tables"):
    errs.append("frozen.json 沒有 tables，但原稿有表格。請抽出每個表格的所有儲存格")
if re.search(r"\\begin\{(equation|align|gather|multline)", src) and not frozen.get("equations"):
    errs.append("frozen.json 沒有 equations，但原稿有公式。請抽出每個公式")
if not frozen.get("claims"):
    errs.append("frozen.json 沒有 claims。請至少抽出摘要、貢獻列表與結論中的 claim 原句")

# 2. 修改紀錄：每列 C 編號都要標使用者是否同意
if a.changelog:
    for line in log_md.splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and re.fullmatch(r"C\d+", cells[0]):
            if not re.search(r"^(是|yes|使用者未同意|待確認)$", cells[-1], re.I):
                errs.append(f"{cells[0]}：最後一欄沒有標「是」「使用者未同意」或「待確認」")
else:
    errs.append("沒有給 --changelog，無法檢查修改紀錄")

# 3. PDF：頁數、字型
doc = pymupdf.open(a.pdf)
# CVPR／ICCV review 模式會在標題前後加行號，例如 References 後面接 533
END = "References|Bibliography|參考文獻" + (f"|{re.escape(a.body_end)}" if a.body_end else "")
REF = r"\s*(\d+\s*)?(" + END + r")(\s+\d+)?\s*"
if a.venue_pages:
    ref = next((p for p in doc for b in p.get_text("blocks")
                if re.fullmatch(REF, b[4])), None)
    if ref is None:
        errs.append("找不到 References 標題，無法判斷正文頁數，請人工確認")
    else:
        y = min(b[1] for b in ref.get_text("blocks") if re.fullmatch(REF, b[4]))
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
        if f.name.startswith("compare_") or f.is_dir():
            continue  # 改前改後的對照圖、data/、visual/
        if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
            if f.stem not in {x.stem for x in pathlib.Path(a.figures).glob("*.pdf")}:
                errs.append(f"{f.name}：點陣圖，沒有對應的向量 PDF（定性結果的圖片請在 spec.md 註明）")
        elif f.suffix.lower() == ".pdf":
            p = pymupdf.open(f)[0]
            if not p.get_drawings() and not p.get_text().strip():
                errs.append(f"{f.name}：只有點陣圖，不是向量 PDF")

# 4b. spec.md：沒有重畫的圖要寫原因
def spec_rows(path):
    rows, head = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            head = None
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if head is None:
            head = cells
        elif not all(set(c) <= set("-: ") for c in cells):
            rows.append(dict(zip(head, cells)))
    return rows


HERE = pathlib.Path(__file__).resolve().parent
INC = r"\\includegraphics(?:\[[^\]]*\])?\{([^}#]+)\}"  # 跳過巨集定義中的 #1


def find_fig(name, roots):
    """依 LaTeX 的規則找圖檔：可以省略副檔名。"""
    for r in roots:
        for ext in ("", ".pdf", ".png", ".jpg", ".jpeg"):
            f = r / (name + ext)
            if f.is_file():
                return f
    return None


def extract(pdf, out):
    """對圖執行 extract_vector_plot.py，回傳 report；不是數據圖時回傳 None。"""
    subprocess.run([sys.executable, "-I", str(HERE / "extract_vector_plot.py"), str(pdf), "--out", str(out)],
                   capture_output=True)
    rp = pathlib.Path(out) / f"{pathlib.Path(pdf).stem}_report.json"
    return json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else None


def data_points(pdf, out, skip=()):
    """extract 輸出的資料點（折線頂點與 marker），依 panel 分組；不含白色與無色的組（遮罩、圖例底），
    也不含 spec.md「資料組對應」欄標為非資料的組（skip）。"""
    f = pathlib.Path(out) / f"{pathlib.Path(pdf).stem}.csv"
    pts = {}
    if not f.exists():
        return pts
    with open(f, encoding="utf-8") as fh:
        next(fh)
        for row in csv.DictReader(fh):
            if row["kind"] not in ("line", "marker"):
                continue
            if row["stroke"] in ("#ffffff", "none") and row["fill"] in ("#ffffff", "none"):
                continue
            if row["series"] in skip:
                continue
            p = int(row["series"][1:].split("_")[0])
            pts.setdefault(p, []).append((float(row["x"]), float(row["y"])))
    # 類別軸輸出的是 PDF 座標，新舊圖版面不同：依各自的範圍正規化到 0–1 再比對
    rp = pathlib.Path(out) / f"{pathlib.Path(pdf).stem}_report.json"
    rep = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {"axis_checks": []}
    for c in rep["axis_checks"]:
        if c.get("scale") == "category" and c["panel"] in pts:
            k = 0 if c["axis"] == "x" else 1
            v = [q[k] for q in pts[c["panel"]]]
            lo, hi = min(v), max(v)
            pts[c["panel"]] = [tuple((q[i] - lo) / ((hi - lo) or 1) if i == k else q[i] for i in (0, 1))
                               for q in pts[c["panel"]]]
    return pts


def words(pdf):
    """圖中的文字標籤（不含純數字），用來檢查新圖有沒有漏掉舊圖的標籤。"""
    import unicodedata
    ws = set()
    for w in pymupdf.open(pdf)[0].get_text("words"):
        t = unicodedata.normalize("NFKC", w[4]).strip(".,:;()[]{}").lower()
        if re.fullmatch(r"[^\W\d_]{2,}(-[^\W\d_]+)*", t):  # 只比對一般單字；數學式碎片（括號、組合符號、數字）不算
            ws.add(t)
    return ws


def is_raster(f):
    if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
        return True
    return f.suffix.lower() == ".pdf" and bool(pymupdf.open(f)[0].get_images())


if a.figures:
    figdir = pathlib.Path(a.figures)
    spec = figdir / "spec.md"
    orig_roots = [pathlib.Path(p).resolve().parent for p in (a.orig_tex or [])]
    new_roots = [pathlib.Path(p).resolve().parent for p in a.tex] + [figdir.resolve()]
    if not spec.exists():
        errs.append("figures/spec.md 不存在")
    else:
        rows = [r for r in spec_rows(spec) if "處理方式" in r]
        if not rows:
            errs.append("spec.md 沒有含「處理方式」欄的表格")
        for r in rows:
            fid, how, why = r.get("圖號", "?"), r["處理方式"], r.get("原因", "").strip(" -—")
            olds = re.findall(r"[\w./-]+\.(?:pdf|png|jpe?g)", r.get("原圖檔", ""))
            if re.search(r"只改 ?caption|保留", how):
                m = re.match(r"`?(點陣圖|抽取未通過|重畫後較差)[：:]", why)
                if not m:
                    errs.append(f"spec.md {fid}：處理方式是「{how}」，原因要以「點陣圖：」「抽取未通過：」或「重畫後較差：」開頭")
                    continue
                for o in olds:
                    st = pathlib.Path(o).stem
                    fo = find_fig(o, orig_roots) if orig_roots else None
                    if fo and fo.suffix.lower() == ".pdf" and is_raster(fo) and m.group(1) != "重畫後較差":
                        errs.append(f"spec.md {fid}：{o} 是內嵌圖片的 PDF，圖片可以用 extract_figure_assets.py 取出重排（4.7），"
                                    "只能用「重畫後較差：」保留")
                    if m.group(1) == "抽取未通過":
                        if not (figdir / "data" / f"{st}_report.json").exists():
                            errs.append(f"spec.md {fid}：原因是抽取未通過，但沒有 figures/data/{st}_report.json")
                        # 不信任 report 檔：checker 自己對原圖重跑抽取
                        if fo and fo.suffix.lower() == ".pdf":
                            with tempfile.TemporaryDirectory() as td:
                                rr = extract(fo, td)
                            if rr is None or rr["panels"] == 0:
                                errs.append(f"spec.md {fid}：{o} 沒有數字座標軸，「抽取未通過」不適用。"
                                            "方法圖依 4.6 用 TikZ 重畫；軌跡等沒有刻度的數據圖依 4.3 步驟 3 重播繪圖指令")
                            elif rr["tick_check_pass"]:
                                errs.append(f"spec.md {fid}：checker 重跑 extract_vector_plot.py，{o} 的刻度檢查通過，請重畫")
                    if m.group(1) == "重畫後較差" and not list(figdir.glob(f"compare_{st}.*")):
                        errs.append(f"spec.md {fid}：原因是重畫後較差，但沒有 figures/compare_{st}.png")
                    if m.group(1) == "點陣圖" and orig_roots:
                        f = find_fig(o, orig_roots) or find_fig(pathlib.Path(o).name, orig_roots)
                        if f and f.suffix.lower() == ".pdf":
                            errs.append(f"spec.md {fid}：原因是點陣圖，但 {o} 是 PDF。內嵌圖片可以用 extract_figure_assets.py 取出，"
                                        "請依 4.6／4.7 重排；重排後較差時改用「重畫後較差：」")
            # 每份重畫版（包括判定較差而沒採用的）都要完整：舊圖的文字標籤都在新圖中
            news_all = re.findall(r"[\w./-]+\.pdf", r.get("新圖檔", ""))
            if re.search(r"重畫|重排", how) or (m := re.match(r"`?重畫後較差", why)):
                if re.match(r"`?重畫後較差", why) and not news_all:
                    errs.append(f"spec.md {fid}：原因是重畫後較差，但「新圖檔」欄沒有列出重畫版")
                for o, n in zip(olds, news_all):
                    fo = find_fig(o, orig_roots) if orig_roots else None
                    fn = find_fig(n, new_roots) or find_fig(pathlib.Path(n).name, new_roots)
                    if fo and fn and fo.suffix.lower() == ".pdf":
                        # 相鄰標籤可能被合成一個字（例如 leanbroom）：在新圖的全文中找得到就不算缺
                        import unicodedata
                        full = re.sub(r"\s", "", unicodedata.normalize("NFKC", pymupdf.open(fn)[0].get_text()).lower())
                        miss = sorted(w for w in words(fo) - words(fn) if w not in full)
                        if miss:
                            errs.append(f"spec.md {fid}：重畫版 {n} 少了舊圖的文字標籤 {miss[:12]}。"
                                        "重畫版要先完整，才能拿來比較好壞")
            # 重畫的數據圖：新圖的資料不少於舊圖；判定較差的重畫版也要檢查
            if ("數據圖" in how or re.match(r"`?重畫後較差", why)) and orig_roots:
                news = re.findall(r"[\w./-]+\.pdf", r.get("新圖檔", ""))
                for o, n in zip(olds, news):
                    fo, fn = find_fig(o, orig_roots), find_fig(n, new_roots) or find_fig(pathlib.Path(n).name, new_roots)
                    if not (fo and fn and fo.suffix == ".pdf"):
                        continue
                    with tempfile.TemporaryDirectory() as td:
                        ro, rn = extract(fo, pathlib.Path(td) / "o"), extract(fn, pathlib.Path(td) / "n")
                        # 「資料組對應」欄中，含「非資料」的片段列出的組（例如 p0_g5）不列入比對
                        segs = re.split(r"[；;。]", r.get("資料組對應", ""))
                        skip = {g for sg in segs if "非資料" in sg for g in re.findall(r"p\d+_g\d+", sg)}
                        po, pn_ = data_points(fo, pathlib.Path(td) / "o", skip), data_points(fn, pathlib.Path(td) / "n")
                    if not (ro and rn and ro["series"]):
                        continue
                    co = {(c["panel"], c["axis"]): c for c in ro["axis_checks"] if "span_pt" in c}
                    for c in rn["axis_checks"]:
                        if "span_pt" not in c:
                            continue
                        oc = co.get((c["panel"], c["axis"]))
                        # 刻度太密：超過 7 個，且比舊圖多（序列編號 1–10 這類舊圖本來就有的刻度不算）
                        if len(c["ticks"]) > 7 and not (oc and len(c["ticks"]) <= len(oc["ticks"])):
                            errs.append(f"spec.md {fid}：新圖 {n} panel {c['panel']} 的 {c['axis']} 軸有 {len(c['ticks'])} 個刻度，超過 4–6 個")
                        # 資料區不能縮小：新圖的軸長不小於舊圖的 85%
                        if oc and oc["span_pt"] > 0 and c["span_pt"] < 0.85 * oc["span_pt"] and rn["panels"] == ro["panels"]:
                            errs.append(f"spec.md {fid}：新圖 {n} panel {c['panel']} 的 {c['axis']} 軸長 {c['span_pt']} pt，"
                                        f"小於舊圖的 {oc['span_pt']} pt 的 85%。資料區被壓縮，請調整版面（例如圖例改成直接標籤）")
                    # 資料完整：舊圖的每個資料點，在新圖同一 panel 都有位置相近的點（軸範圍的 1.5% 內）
                    if ro["tick_check_pass"] and rn["tick_check_pass"] and ro["panels"] == rn["panels"]:
                        for p in sorted(po):
                            O, N = po[p], pn_.get(p, [])
                            if not N:
                                errs.append(f"spec.md {fid}：新圖 {n} 沒有 panel {p} 的資料")
                                continue
                            xs = [x for x, _ in O]; ys = [y for _, y in O]
                            sx = (max(xs) - min(xs)) or 1; sy = (max(ys) - min(ys)) or 1
                            lost = sum(min(((x - u) / sx) ** 2 + ((y - v) / sy) ** 2 for u, v in N) > 0.015 ** 2 for x, y in O)
                            if lost > 0.05 * len(O):
                                errs.append(f"spec.md {fid}：舊圖 {o} panel {p} 有 {lost}/{len(O)} 個資料點在新圖 {n} 找不到。"
                                            "請確認沒有漏畫或畫錯資料（淡色曲線、參考線、次要 baseline）")
        if a.orig_tex:
            orig = "\n".join(strip_comments(pathlib.Path(p).read_text(encoding="utf-8")) for p in a.orig_tex)
            kept = set(re.findall(INC, orig)) & set(re.findall(INC, tex))
            for g in sorted(kept):
                stem = pathlib.Path(g).stem
                if not [r for r in rows if stem in r.get("原圖檔", "")]:
                    errs.append(f"{g}：仍使用原圖，但 spec.md 的「原圖檔」欄沒有這個檔案")

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

# 改前計畫與改後驗收：每處修改（C 編號、重畫或重排的圖）在 plan.md 都有一列
if a.changelog:
    plan = pathlib.Path(a.changelog).parent / "plan.md"
    need = set(re.findall(r"^\|\s*(C\d+)\s*\|", log_md, re.M))
    if a.figures and (pathlib.Path(a.figures) / "spec.md").exists():
        need |= {r["圖號"] for r in spec_rows(pathlib.Path(a.figures) / "spec.md")
                 if "圖號" in r and re.search(r"重畫|重排", r.get("處理方式", ""))}
    if not plan.exists():
        if need:
            errs.append("plan.md 不存在。每處修改前，先在 plan.md 寫為什麼改、怎麼改、預期結果、驗收方法")
    else:
        prow = {r.get("編號", ""): r for r in spec_rows(plan)}
        for k in sorted(need):
            r = prow.get(k)
            if not r:
                errs.append(f"plan.md 沒有 {k} 的計畫列")
                continue
            for col in ("為什麼改", "怎麼改", "預期結果", "驗收方法", "證據"):
                if not r.get(col, "").strip("-— "):
                    errs.append(f"plan.md {k}：「{col}」欄是空的")
            if r.get("驗收結果", "") not in ("達成", "已還原"):
                errs.append(f"plan.md {k}：驗收結果是「{r.get('驗收結果', '')}」。未達成預期時，修到達成，或還原修改並寫「已還原」")

print("\n".join(errs) if errs else "全部通過")
print(f"共 {len(errs)} 項錯誤")
sys.exit(1 if errs else 0)
