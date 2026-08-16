# -*- coding: utf-8 -*-
"""Cut angels from black studio shots, soften edges, save PNG+WebP."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageFilter

SRC = Path(r"C:\Users\РС\.cursor\projects\c-Users-OneDrive-Desktop\assets")
DST = Path(__file__).resolve().parents[2] / "images" / "angels"

THRESHOLD = 28
FEATHER = 2.4


def flood_background_mask(im: Image.Image) -> Image.Image:
    arr = np.array(im.convert("RGBA"))
    rgb = arr[:, :, :3].astype(np.int16)
    lum = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    is_bg = (lum <= THRESHOLD) & (chroma < 18)
    h, w = is_bg.shape
    visited = np.zeros((h, w), dtype=bool)
    stack = []
    for x in range(w):
        if is_bg[0, x]:
            stack.append((0, x))
        if is_bg[h - 1, x]:
            stack.append((h - 1, x))
    for y in range(h):
        if is_bg[y, 0]:
            stack.append((y, 0))
        if is_bg[y, w - 1]:
            stack.append((y, w - 1))
    while stack:
        y, x = stack.pop()
        if y < 0 or y >= h or x < 0 or x >= w or visited[y, x] or not is_bg[y, x]:
            continue
        visited[y, x] = True
        stack.extend(((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)))
    alpha = np.where(visited, 0, 255).astype(np.uint8)
    mask = Image.fromarray(alpha, mode="L")
    return mask.filter(ImageFilter.GaussianBlur(FEATHER))


def warm_ivory(im: Image.Image) -> Image.Image:
    r, g, b, a = im.split()
    r = r.point(lambda v: min(255, int(v * 0.98 + 6)))
    g = g.point(lambda v: min(255, int(v * 0.96 + 3)))
    b = b.point(lambda v: min(255, int(v * 0.90)))
    return Image.merge("RGBA", (r, g, b, a))


def process(src: Path, stem: str) -> None:
    im = Image.open(src).convert("RGBA")
    mask = flood_background_mask(im)
    r, g, b, a = im.split()
    a = ImageChops.darker(a, mask)
    out = warm_ivory(Image.merge("RGBA", (r, g, b, a)))
    bbox = out.getbbox()
    if bbox:
        pad = 40
        x0, y0, x1, y1 = bbox
        x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
        x1, y1 = min(out.width, x1 + pad), min(out.height, y1 + pad)
        out = out.crop((x0, y0, x1, y1))
    r, g, b, a = out.split()
    a = a.filter(ImageFilter.GaussianBlur(1.1))
    out = Image.merge("RGBA", (r, g, b, a))
    DST.mkdir(parents=True, exist_ok=True)
    out.save(DST / f"{stem}.png", "PNG", optimize=True)
    out.save(DST / f"{stem}.webp", "WEBP", quality=88, method=6)
    print(stem, out.size)


if __name__ == "__main__":
    process(SRC / "angel-tender-left.png", "angel-clean-left")
    process(SRC / "angel-tender-right.png", "angel-clean-right")
