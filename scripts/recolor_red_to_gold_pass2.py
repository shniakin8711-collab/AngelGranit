# -*- coding: utf-8 -*-
"""Second pass: convert remaining dark maroon / red glows to gold."""
from pathlib import Path
from PIL import Image
import colorsys

ROOT = Path("images")
TARGETS = [
    "banner-ritual-services.png",
    "price-list.png",
    "price-list-2.png",
    "showcase-hearse.png",
    "catalog/banner-ritual.png",
]

GOLD_H = 0.118


def is_remaining_red(r, g, b, a):
    if a < 20:
        return False
    mx, mn = max(r, g, b), min(r, g, b)
    if mx < 28:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    # Already gold-ish — skip
    if 0.08 <= h <= 0.18 and s >= 0.25:
        return False
    # Skin / warm lamp — skip
    if r > 90 and g > 60 and abs(r - g) < 50 and b > 40 and s < 0.45:
        return False
    # Dark maroon bars / accents
    if r >= 40 and g <= r * 0.72 and b <= r * 0.72 and (r - g) >= 18 and (r - b) >= 18:
        if s >= 0.22 or (r - g) >= 28:
            return True
    # Red hue leftover
    if (h <= 0.06 or h >= 0.94) and s >= 0.28 and v >= 0.12:
        return True
    # Soft red glows (corners): reddish tint over dark
    if r >= 50 and g < 45 and b < 45 and r > g + 20:
        return True
    return False


def to_gold(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    # Map dark maroons to richer gold
    s = min(1.0, max(0.42, s * 1.15))
    v = min(1.0, max(0.28, v * 1.25))
    nr, ng, nb = colorsys.hsv_to_rgb(GOLD_H, s, v)
    return int(nr * 255), int(ng * 255), int(nb * 255)


def main():
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        im = Image.open(path).convert("RGBA")
        px = im.load()
        w, h = im.size
        n = 0
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if is_remaining_red(r, g, b, a):
                    nr, ng, nb = to_gold(r, g, b)
                    px[x, y] = (nr, ng, nb, a)
                    n += 1
        im.save(path, optimize=True)
        print(f"{100*n/(w*h):5.1f}%  {rel}  ({n})")


if __name__ == "__main__":
    main()
