"""取出 PDF 圖中內嵌的照片與文字標籤，供 TikZ 重排（SKILL.md 4.6、4.7）。

用法：python extract_figure_assets.py <圖.pdf> --out figures/assets/
輸出到 <out>/<圖名>/：
  img<N>.<ext>   內嵌圖片的原始位元組（JPEG 保持原檔，不重新壓縮）
  layout.json    頁面大小（pt）、每張圖片的位置與原始像素、每個文字標籤的位置與字級、向量繪圖數
  preview.png    舊圖上標出每張圖片的編號與框，用來對照 layout.json
pdflatex 用 \\includegraphics 放入 JPEG 時直接嵌入原檔，所以像素不變。
"""
import argparse, json, pathlib, sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("--out", required=True)
a = ap.parse_args()
doc = pymupdf.open(a.pdf)
page = doc[0]
out = pathlib.Path(a.out) / pathlib.Path(a.pdf).stem
out.mkdir(parents=True, exist_ok=True)

images, seen = [], {}
for info in page.get_image_info(xrefs=True):
    x = info["xref"]
    if not x:
        continue
    if x not in seen:
        d = doc.extract_image(x)
        f = out / f"img{len(seen)}.{d['ext']}"
        f.write_bytes(d["image"])
        if d.get("smask"):  # 透明遮罩另外存，重排時需要
            m = doc.extract_image(d["smask"])
            (out / f"img{len(seen)}_mask.{m['ext']}").write_bytes(m["image"])
        seen[x] = f.name
    b = info["bbox"]
    images.append({"file": seen[x], "bbox_pt": [round(v, 2) for v in b],
                   "px": [info["width"], info["height"]],
                   "dpi": round(info["width"] / max((b[2] - b[0]) / 72, 1e-6))})

texts = [{"text": s["text"], "bbox_pt": [round(v, 2) for v in s["bbox"]], "size": round(s["size"], 1),
          "font": s["font"], "color": "#%06x" % s["color"]}
         for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]

lay = {"pdf": a.pdf, "page_pt": [page.rect.width, page.rect.height], "images": images,
       "texts": texts, "vector_drawings": len(page.get_drawings())}
(out / "layout.json").write_text(json.dumps(lay, ensure_ascii=False, indent=1), encoding="utf-8")

sh = page.new_shape()
for i, im in enumerate(images):
    sh.draw_rect(im["bbox_pt"])
sh.finish(color=(1, 0, 1), width=0.8)
sh.commit()
for i, im in enumerate(images):
    page.insert_text((im["bbox_pt"][0] + 2, im["bbox_pt"][1] + 9), str(i), fontsize=8, color=(1, 0, 1))
page.get_pixmap(dpi=200).save(out / "preview.png")

print(f"{len(images)} 個圖片位置（{len(seen)} 個不同檔案）、{len(texts)} 個文字標籤、{lay['vector_drawings']} 個向量繪圖 → {out}")
sys.exit(0 if images else 2)
