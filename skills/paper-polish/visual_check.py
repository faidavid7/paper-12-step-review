"""圖的目視檢查用圖（SKILL.md 4.10 第 1、3 點）。

用法：python visual_check.py <新圖.pdf> [<舊圖.pdf 或 .png>] --out figures/visual/
輸出 <圖名>_check.png：一列依序是 實際大小（200 dpi）、灰階、deuteranopia 模擬；有舊圖時第二列放舊圖。
用 Read 打開這張 png 逐項看，結果寫進修改紀錄的「目視檢查結果」。
"""
import argparse, pathlib, sys
import numpy as np
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("new")
ap.add_argument("old", nargs="?")
ap.add_argument("--out", required=True)
a = ap.parse_args()
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)

# Machado et al. 2009，deuteranopia，severity 1.0（線性 RGB）
DEUT = np.array([[0.367322, 0.860646, -0.227968],
                 [0.280085, 0.672501, 0.047413],
                 [-0.011820, 0.042940, 0.968881]])


def load(path):
    path = str(path)
    if path.lower().endswith(".pdf"):
        pix = pymupdf.open(path)[0].get_pixmap(dpi=200, alpha=False)
    else:
        pix = pymupdf.Pixmap(path)
        if pix.alpha or pix.n != 3:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix, 0)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3).astype(float) / 255


def lin(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def row(img):
    g = (0.2126 * lin(img[..., 0]) + 0.7152 * lin(img[..., 1]) + 0.0722 * lin(img[..., 2]))
    gray = np.repeat(srgb(g)[..., None], 3, axis=2)
    deut = srgb(lin(img) @ DEUT.T)
    gap = np.ones((img.shape[0], 20, 3))
    return np.concatenate([img, gap, gray, gap, deut], axis=1)


rows = [row(load(a.new))]
if a.old:
    rows.append(row(load(a.old)))
w = max(r.shape[1] for r in rows)
rows = [np.pad(r, ((0, 20), (0, w - r.shape[1]), (0, 0)), constant_values=1) for r in rows]
img = (np.concatenate(rows, axis=0) * 255).astype(np.uint8)
dst = out / f"{pathlib.Path(a.new).stem}_check.png"
pymupdf.Pixmap(pymupdf.csRGB, img.shape[1], img.shape[0], img.tobytes(), False).save(dst)
print(dst)
