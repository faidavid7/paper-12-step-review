"""從向量 PDF 數據圖抽出數值（SKILL.md 4.3）。

用法：python extract_vector_plot.py <圖.pdf> --out figures/data/
輸出：
  <圖名>_report.json  座標軸對應、每個驗證項目、每組資料的摘要
  <圖名>.csv          每組資料換算後的數值；長條給四邊（x_left、x_right、y_top、y_bottom）。
                    只有一軸有數字刻度時，另一軸是類別軸，輸出 PDF 座標（y 向下）
  <圖名>_overlay.png  舊圖上疊畫抽出的點（洋紅色），用來目視確認位置
不是數據圖（例如方法圖）時，report 的 axes 為空，exit code 為 2。
"""
import argparse, csv, json, math, pathlib, re, sys
from collections import defaultdict
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("--out", required=True)
ap.add_argument("--page", type=int, default=0)
a = ap.parse_args()
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
stem = pathlib.Path(a.pdf).stem
page = pymupdf.open(a.pdf)[a.page]
TOL = 0.005  # 刻度換算誤差上限：軸範圍的 0.5%

# ---------- 數字刻度標籤 ----------
NUM = re.compile(r"^[−\-–]?\d+(\.\d+)?([eE][−\-]?\d+)?\s?(%|×|x|/|k|M)?$")  # 允許單位：1×、2/T 的「2/」、50%


def num(t):
    t = re.sub(r"\s?(%|×|x|/|k|M)$", "", t.strip().replace("−", "-").replace("–", "-"))
    return float(t)


spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
         for s in l["spans"] if s["text"].strip()]
# matplotlib 的 10^k 會拆成「10」與上標「k」兩個 span，合併成一個值
labels, used = [], set()
for i, s in enumerate(spans):
    t = s["text"].strip()
    if i in used or not NUM.match(t):
        continue
    x0, y0, x1, y1 = s["bbox"]
    if t == "10":
        for j, u in enumerate(spans):
            ut = u["text"].strip()
            if j != i and j not in used and NUM.match(ut) and u["size"] < s["size"] * 0.9 \
                    and abs(u["bbox"][0] - x1) < 2 and u["bbox"][3] < y1:
                used.add(j)
                labels.append({"v": 10 ** num(ut), "bbox": (x0, y0, max(x1, u["bbox"][2]), y1), "log10": True})
                break
        else:
            labels.append({"v": 10.0, "bbox": s["bbox"]})
        continue
    labels.append({"v": num(t), "bbox": s["bbox"]})

# ---------- 繪圖指令 ----------
draws = page.get_drawings()
segs = []  # 短的水平或垂直線段，可能是刻度線
for d in draws:
    for it in d["items"]:
        if it[0] == "l":
            p, q = it[1], it[2]
            if abs(p.y - q.y) < 0.01 and 0.5 < abs(p.x - q.x) < 8:
                segs.append(("h", (p.x + q.x) / 2, p.y, min(p.x, q.x), max(p.x, q.x)))
            if abs(p.x - q.x) < 0.01 and 0.5 < abs(p.y - q.y) < 8:
                segs.append(("v", p.x, (p.y + q.y) / 2, min(p.y, q.y), max(p.y, q.y)))


def fit(pos, val):
    """線性或 log 對應：val = f(pos)。回傳 (kind, slope, icpt, 最大誤差比例)。"""
    best = None
    for kind in ("linear", "log"):
        if kind == "log" and min(val) <= 0:
            continue
        y = [math.log10(v) if kind == "log" else v for v in val]
        n = len(pos); mx = sum(pos) / n; my = sum(y) / n
        sxx = sum((p - mx) ** 2 for p in pos)
        if sxx == 0:
            continue
        k = sum((p - mx) * (v - my) for p, v in zip(pos, y)) / sxx
        b = my - k * mx
        rng = (max(y) - min(y)) or 1
        err = max(abs(k * p + b - v) for p, v in zip(pos, y)) / rng
        if best is None or err < best[3]:
            best = (kind, k, b, err)
    return best


def group(items, key, tol):
    gs = []
    for it in sorted(items, key=key):
        if gs and abs(key(it) - key(gs[-1][-1])) < tol:
            gs[-1].append(it)
        else:
            gs.append([it])
    return gs


axes = []
# x 軸：同一高度（底邊對齊）、至少 3 個標籤
def split_row(g):
    """同一高度的標籤可能屬於多個 panel：數值不再遞增，或間距變成 2 倍以上時切開。"""
    g = sorted(g, key=lambda l: l["bbox"][0])
    cx = [(l["bbox"][0] + l["bbox"][2]) / 2 for l in g]
    parts, cur, sign, gap = [], [g[0]], 0, 0
    for i in range(1, len(g)):
        d = (g[i]["v"] > g[i - 1]["v"]) - (g[i]["v"] < g[i - 1]["v"])  # 座標軸可以反向，只看方向是否改變
        step = cx[i] - cx[i - 1]
        if d == 0 or (sign and d != sign) or (gap and step > 2 * gap):
            parts.append(cur); cur, d, step = [], 0, 0
        cur.append(g[i]); sign, gap = d, step
    return parts + [cur]


for g in [p for g0 in group(labels, lambda l: l["bbox"][3], 1.5) for p in split_row(g0)]:
    if len(g) < 3 or len({round(l["bbox"][0]) for l in g}) < len(g):
        continue
    pos, src = [], "tick"
    for l in g:
        cx = (l["bbox"][0] + l["bbox"][2]) / 2
        tk = [s for s in segs if s[0] == "v" and abs(s[1] - cx) < 3 and 0 <= l["bbox"][1] - s[4] < 6]
        if tk:
            pos.append(min(tk, key=lambda s: abs(s[1] - cx))[1])
        else:
            pos.append(cx); src = "label-center"
    axes.append({"dir": "x", "labels": g, "pos": pos, "src": src})
# y 軸：右緣對齊、至少 3 個標籤
for g in group(labels, lambda l: l["bbox"][2], 1.5):
    if len(g) < 3 or len({round(l["bbox"][1]) for l in g}) < len(g):
        continue
    pos, src = [], "tick"
    for l in g:
        cy = (l["bbox"][1] + l["bbox"][3]) / 2
        tk = [s for s in segs if s[0] == "h" and abs(s[2] - cy) < 3 and 0 <= s[3] - l["bbox"][2] < 6]
        if tk:
            pos.append(min(tk, key=lambda s: abs(s[2] - cy))[2])
        else:
            pos.append(cy); src = "label-center"
    axes.append({"dir": "y", "labels": g, "pos": pos, "src": src})

for ax in axes:
    vals = [l["v"] for l in ax["labels"]]
    ax["kind"], ax["k"], ax["b"], ax["err"] = fit(ax["pos"], vals)
    # 順序軸：刻度等距，但數值不是線性也不是 log（例如 0, 0.02, 0.05, 0.1, 0.2 等距排列）
    ps = sorted(ax["pos"])
    gaps = [b - a for a, b in zip(ps, ps[1:])]
    if ax["err"] > TOL and gaps and max(gaps) - min(gaps) < 0.01 * (ps[-1] - ps[0]):
        ax["kind"], ax["err"] = "ordinal", 0.0
        ax["table"] = sorted(zip(ax["pos"], vals))
    ax["values"] = vals
    ax["lo"], ax["hi"] = min(ax["pos"]), max(ax["pos"])

# ---------- 配對成 panel：y 軸在 x 軸左上方 ----------
xs = sorted((x for x in axes if x["dir"] == "x"), key=lambda x: x["lo"])
ys = [y for y in axes if y["dir"] == "y"]
panels = []
for i, x in enumerate(xs):
    xtop = min(l["bbox"][1] for l in x["labels"])
    # 左邊最近、且在 x 軸標籤上方的 y 軸；沒有緊鄰的 y 軸時沿用左邊 panel 的 y 軸（sharey）
    cand = [y for y in ys if max(l["bbox"][2] for l in y["labels"]) < x["lo"] + 2 and y["hi"] < xtop + 2]
    if not cand:
        continue
    y = max(cand, key=lambda y: max(l["bbox"][2] for l in y["labels"]))
    yr = max(l["bbox"][2] for l in y["labels"])
    # 左右相鄰的 panel：同一高度的 x 軸（上方的第二 x 軸不算）
    row = [o for o in xs if abs(min(l["bbox"][1] for l in o["labels"]) - xtop) < 3]
    prev = [o for o in row if o["hi"] < x["lo"]]
    nxt = [o for o in row if o["lo"] > x["hi"]]
    pv = max(prev, key=lambda o: o["hi"]) if prev else None
    left = (pv["hi"] + x["lo"]) / 2 if pv and pv["hi"] > yr else yr
    right = (x["hi"] + min(o["lo"] for o in nxt)) / 2 if nxt else page.rect.x1
    panels.append({"x": x, "y": y, "box": (left, max(0, y["lo"] - 10), right, xtop)})


# 只有一軸有數字刻度時（例如水平長條圖的 y 軸是方法名稱），另一軸當類別軸：輸出 PDF 座標，用來排序與對應標籤
used_x = {id(p["x"]) for p in panels}
used_y = {id(p["y"]) for p in panels}


def cat(lo, hi):
    return {"dir": "?", "kind": "category", "k": 1.0, "b": 0.0, "err": 0.0, "src": "none",
            "values": [], "lo": lo, "hi": hi, "labels": []}


paired = list(panels)
secondary = []


def overlaps(a0, a1, b0, b1):
    return min(a1, b1) - max(a0, b0) > 0.3 * min(a1 - a0, b1 - b0)


for x in xs:
    if id(x) in used_x or x["src"] != "tick":  # 沒有刻度線的孤立數字列（例如欄標題）不是座標軸
        continue
    # 第二 x 軸：位在已配對 panel 的上方、水平範圍重疊
    if any(overlaps(x["lo"], x["hi"], p["box"][0], p["box"][2]) and max(l["bbox"][3] for l in x["labels"]) <= p["box"][1] + 12
           for p in paired):
        secondary.append({"axis": "x", "ticks": [l["v"] for l in x["labels"]]})
        continue
    xtop = min(l["bbox"][1] for l in x["labels"])
    above = [min(l["bbox"][1] for l in o["labels"]) for o in xs if min(l["bbox"][1] for l in o["labels"]) < xtop - 5]
    y0 = max(above) if above else 0
    panels.append({"x": x, "y": dict(cat(y0, xtop), dir="y"), "box": (0, y0, page.rect.x1, xtop)})
for y in ys:
    if id(y) in used_y or y["src"] != "tick":
        continue
    # 第二 y 軸：位在已配對 panel 的右側、垂直範圍重疊
    if any(overlaps(y["lo"], y["hi"], p["box"][1], p["box"][3]) and min(l["bbox"][0] for l in y["labels"]) >= p["x"]["hi"] - 2
           for p in paired):
        secondary.append({"axis": "y", "ticks": [l["v"] for l in y["labels"]]})
        continue
    yr = max(l["bbox"][2] for l in y["labels"])
    right = [min(l["bbox"][0] for l in o["labels"]) for o in ys if min(l["bbox"][0] for l in o["labels"]) > yr + 5]
    x1 = min(right) if right else page.rect.x1
    pad = (y["hi"] - y["lo"]) * 0.15
    panels.append({"x": dict(cat(yr, x1), dir="x"), "y": y, "box": (yr, max(0, y["lo"] - pad), x1, y["hi"] + pad)})


def to_val(ax, p):
    if ax["kind"] == "ordinal":  # 刻度之間線性內插；資料點通常剛好落在刻度上
        t = ax["table"]
        for (p0, v0), (p1, v1) in zip(t, t[1:]):
            if p <= p1 or (p1, v1) == t[-1]:
                return v0 + (v1 - v0) * (p - p0) / (p1 - p0)
    v = ax["k"] * p + ax["b"]
    return 10 ** v if ax["kind"] == "log" else v


def rgb(c):
    return "none" if c is None else "#%02x%02x%02x" % tuple(round(v * 255) for v in c[:3])


# ---------- 抽資料 ----------
rows, series = [], []
for pi, pn in enumerate(panels):
    X0, Y0, X1, Y1 = pn["box"]
    groups = defaultdict(list)
    for d in draws:
        r = d["rect"]
        if r.x1 < X0 or r.x0 > X1 or r.y1 < Y0 or r.y0 > Y1:
            continue
        if r.width < 0.01 and r.height < 0.01:
            continue
        key = (rgb(d.get("color")), rgb(d.get("fill")), round(d.get("width") or 0, 2))
        if r.width < 8 and r.height < 8 and d.get("fill") is not None and len(d["items"]) > 1:
            groups[key + ("marker",)].append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
        elif all(it[0] == "re" for it in d["items"]) and d.get("fill") is not None:
            for it in d["items"]:
                q = it[1]
                groups[key + ("bar",)].append(((q.x0 + q.x1) / 2, q.y0, q.x0, q.x1, q.y1))
        else:
            pts = []
            for it in d["items"]:
                if it[0] == "l":
                    for p in (it[1], it[2]):
                        if not pts or (abs(pts[-1][0] - p.x) > 1e-3 or abs(pts[-1][1] - p.y) > 1e-3):
                            pts.append((p.x, p.y))
            # 去掉格線、刻度與座標軸（剛好兩點的水平或垂直線）
            if len(pts) == 2 and (abs(pts[0][0] - pts[1][0]) < 0.01 or abs(pts[0][1] - pts[1][1]) < 0.01):
                continue
            if len(pts) >= 2:
                groups[key + ("line",)].append(pts)
    for gi, (key, items) in enumerate(sorted(groups.items())):
        kind = key[3]
        sid = f"p{pi}_g{gi}"
        n = 0
        if kind == "line":
            for li, pts in enumerate(items):
                for px, py in pts:
                    rows.append([sid, kind, key[0], key[1], key[2], li, to_val(pn["x"], px), to_val(pn["y"], py), "", "", "", ""])
                    n += 1
        elif kind == "marker":
            for px, py in items:
                rows.append([sid, kind, key[0], key[1], key[2], 0, to_val(pn["x"], px), to_val(pn["y"], py), "", "", "", ""])
                n += 1
        else:
            for cx, top, x0, x1, bot in items:
                rows.append([sid, kind, key[0], key[1], key[2], 0, to_val(pn["x"], cx), to_val(pn["y"], (top + bot) / 2),
                             to_val(pn["x"], x0), to_val(pn["x"], x1), to_val(pn["y"], top), to_val(pn["y"], bot)])
                n += 1
        series.append({"id": sid, "panel": pi, "kind": kind, "stroke": key[0], "fill": key[1], "width": key[2], "n": n})

# ---------- 報告 ----------
checks = []
for i, pn in enumerate(panels):
    for d in ("x", "y"):
        ax = pn[d]
        if ax["kind"] == "category":
            checks.append({"panel": i, "axis": d, "scale": "category", "note": "沒有數字刻度，輸出 PDF 座標", "pass": True})
            continue
        checks.append({"panel": i, "axis": d, "scale": ax["kind"], "tick_from": ax["src"],
                       "ticks": ax["values"], "span_pt": round(ax["hi"] - ax["lo"], 2),
                       "max_err_frac": round(ax["err"], 6),
                       "pass": ax["err"] <= TOL})
ok = bool(panels) and all(c["pass"] for c in checks) and bool(series)
rep = {"pdf": str(a.pdf), "panels": len(panels), "axis_checks": checks, "secondary_axes": secondary, "series": series,
       "tick_check_pass": ok,
       "still_required": ["疊圖檢查：看 overlay.png，洋紅點要落在舊圖的資料上",
                          "交叉核對：圖中數值同時出現在表格或內文時要相同",
                          "數量檢查：每組資料的點數與舊圖相同",
                          "辨識每組資料：依顏色與圖例對應方法名稱；去掉圖例樣本、框線等非資料的組"]}
(out / f"{stem}_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
with open(out / f"{stem}.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    f.write(f"# source={a.pdf}; 座標由 PDF 繪圖指令依刻度對應換算（extract_vector_plot.py）\n")
    w.writerow(["series", "kind", "stroke", "fill", "width", "segment", "x", "y", "x_left", "x_right", "y_top", "y_bottom"])
    w.writerows(rows)

# 疊圖：把抽到的點畫回舊圖
shape = page.new_shape()
for s in rows:
    pn = panels[int(s[0][1:].split("_")[0])]
    def back(ax, v):
        if ax["kind"] == "ordinal":
            t = ax["table"]
            for (p0, v0), (p1, v1) in zip(t, t[1:]):
                if v <= v1 or (p1, v1) == t[-1]:
                    return p0 + (p1 - p0) * (v - v0) / ((v1 - v0) or 1)
        v = math.log10(v) if ax["kind"] == "log" else v
        return (v - ax["b"]) / ax["k"]
    shape.draw_circle((back(pn["x"], s[6]), back(pn["y"], s[7])), 0.8)
shape.finish(color=(1, 0, 1), fill=(1, 0, 1), width=0)
shape.commit()
page.get_pixmap(dpi=300).save(out / f"{stem}_overlay.png")

print(f"panels={len(panels)} series={len(series)} 刻度檢查={'通過' if ok else '未通過'}")
for sx in secondary:
    print(f"  第二 {sx['axis']} 軸（不算 panel，重畫時保留）：{sx['ticks']}")
for c in checks:
    if c["scale"] == "category":
        print(f"  panel {c['panel']} {c['axis']}: 類別軸（輸出 PDF 座標，依位置對應標籤文字）")
    else:
        print(f"  panel {c['panel']} {c['axis']}: {c['scale']}，刻度來源 {c['tick_from']}，誤差 {c['max_err_frac']:.4%}")
for s in series:
    print(f"  {s['id']} {s['kind']} stroke={s['stroke']} fill={s['fill']} n={s['n']}")
sys.exit(0 if ok else (2 if not panels else 1))
