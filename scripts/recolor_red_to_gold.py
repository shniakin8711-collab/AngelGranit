# -*- coding: utf-8 -*-
"""Recolor saturated red brand accents to gold. Skips skin-like tones."""
from pathlib import Path
from PIL import Image
import colorsys
import shutil

ROOT = Path("images")
BACKUP = Path("images/_backup_red")

TARGETS = [
    "banner-ritual-services.png",
    "share-repost.png",
    "showcase-hearse.png",
    "price-list.png",
    "price-list-2.png",
    "catalog/banner-ritual.png",
]

# Gold hue ~43° in HSV (0..1)
GOLD_H = 0.118
GOLD_S_BOOST = 1.05
GOLD_V_BOOST = 1.08


def is_brand_red(r, g, b, a):
    if a < 30:
        return False
    # Skip near-grays
    mx, mn = max(r, g, b), min(r, g, b)
    if mx < 55 or (mx - mn) < 28:
        return False
    # Skin / warm neutrals: R high but G close to R
    if r > 90 and g > 55 and abs(r - g) < 55 and b < g + 15 and (r - b) < 90:
        # likely skin/wood — only treat if very saturated pure red
        if g > r * 0.55:
            return False
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    # Pure brand red: hue near 0, decent saturation
    hue_red = h <= 0.045 or h >= 0.955
    if hue_red and s >= 0.42 and v >= 0.18:
        return True
    # Chromatic red without relying only on hue (dark reds)
    if r >= 80 and r > g * 1.45 and r > b * 1.35 and (r - g) >= 35 and s >= 0.38:
        return True
    # Mid red accents used in UI text
    if r >= 140 and g < 90 and b < 90 and (r - g) >= 50:
        return True
    return False


def to_gold(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    s = min(1.0, max(0.35, s * GOLD_S_BOOST))
    v = min(1.0, v * GOLD_V_BOOST)
    # Prefer readable gold, not muddy brown
    if v < 0.35:
        v = min(1.0, v + 0.12)
    if s < 0.45:
        s = 0.55
    nr, ng, nb = colorsys.hsv_to_rgb(GOLD_H, s, v)
    return int(nr * 255), int(ng * 255), int(nb * 255)


def recolor(path: Path):
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    changed = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if is_brand_red(r, g, b, a):
                nr, ng, nb = to_gold(r, g, b)
                px[x, y] = (nr, ng, nb, a)
                changed += 1
    return im, changed, w * h


def main():
    BACKUP.mkdir(parents=True, exist_ok=True)
    for rel in TARGETS:
        src = ROOT / rel
        if not src.exists():
            print("skip missing", rel)
            continue
        bak = BACKUP / rel.replace("/", "__")
        if not bak.exists():
            shutil.copy2(src, bak)
        im, changed, total = recolor(src)
        im.save(src, optimize=True)
        pct = 100.0 * changed / total if total else 0
        print(f"{pct:5.1f}% pixels -> gold  {rel}  ({changed})")


if __name__ == "__main__":
    main()
