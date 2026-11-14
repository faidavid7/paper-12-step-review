import re, pymupdf

def norm(s):
    s = re.sub(r"(?<![\w.])\d{1,3}(?![\w.])", " ", s)   # 去掉行號這類獨立的 1–3 位數字
    return re.sub(r"[\s\-‐‑–]", "", s).lower()

def find_sentence(page, sentence):
    """回傳整句每一行的矩形。能處理跨行、連字號斷行、行號。找不到回傳 None。"""
    words = page.get_text("words")
    buf, owner = "", []
    for i, w in enumerate(words):
        n = norm(w[4])
        buf += n
        owner += [i] * len(n)
    target = norm(sentence)
    k = buf.find(target)
    if not target or k < 0:
        return None
    idx = sorted(set(owner[k:k + len(target)]))
    lines = {}
    for i in idx:
        key = (words[i][5], words[i][6])          # (block, line)
        r = pymupdf.Rect(words[i][:4])
        lines[key] = lines[key] | r if key in lines else r
    return list(lines.values())

def marked_text(page, annot):
    v = annot.vertices or []
    rects = [pymupdf.Quad(v[i:i+4]).rect for i in range(0, len(v), 4)]
    out = []
    for r in rects:
        ws = [w for w in page.get_text("words")
              if r.contains(pymupdf.Point((w[0]+w[2])/2, (w[1]+w[3])/2))]
        out += [w[4] for w in sorted(ws, key=lambda w: w[0])]
    return " ".join(out)

def mark(page, sentence, color, title, lines, kind="highlight", pdf_time=None):
    rects = find_sentence(page, sentence)
    if rects is None:
        return None
    f = page.add_highlight_annot if kind == "highlight" else page.add_underline_annot
    a = f(quads=[r.quad for r in rects])
    a.set_colors(stroke=color)
    a.set_info(title=title, content="\n".join(lines))
    if pdf_time:
        a.set_info(creationDate=pdf_time, modDate=pdf_time)
    a.update()
    return a

def figure_rect(page, n):
    """依 caption「Figure n:」往上找圖形範圍。找不到回傳 None，改用目視判斷。"""
    cap = None
    for b in page.get_text("blocks"):
        if re.match(rf"\s*(Figure|Fig\.)\s*{n}\s*[:.]", b[4]):
            cap = pymupdf.Rect(b[:4]); break
    if cap is None:
        return None
    g = [r for r in page.cluster_drawings()] + [pymupdf.Rect(i["bbox"]) for i in page.get_image_info()]
    g = [r for r in g if r.y0 < cap.y0 - 5 and r.y1 <= cap.y1 and r.x1 > cap.x0 - 20 and r.x0 < cap.x1 + 20 and r.height > 3]
    if not g:
        return None
    g = [pymupdf.Rect(r.x0, r.y0, r.x1, min(r.y1, cap.y0)) for r in g]
    g.sort(key=lambda r: -r.y1)
    u = pymupdf.Rect(g[0])
    if cap.y0 - u.y1 > 60:
        return None
    changed = True
    while changed:
        changed = False
        for r in g:
            if not u.contains(r) and r.y1 >= u.y0 - 15:
                u |= r; changed = True
    u.y1 = min(u.y1, cap.y0)
    # 納入圖內文字（座標軸、標籤）
    for b in page.get_text("blocks"):
        br = pymupdf.Rect(b[:4])
        if br.intersects(u) and br.y1 <= cap.y0 + 1:
            u |= br
    return u + (-3, -3, 3, 3)
