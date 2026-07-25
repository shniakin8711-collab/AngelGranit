# -*- coding: utf-8 -*-
"""Scan PNGs for red-ish pixels and report candidates for gold recolor."""
from pathlib import Path
from PIL import Image
import colorsys

ROOT = Path("images")
FILES = [
    "banner-ritual-services.png",
    "service-funeral.png",
    "showcase-monument.png",
    "showcase-hearse.png",
    "package-minimal.png",
    "package-hall.png",
    "package-standard.png",
    "package-elite.png",
    "price-list.png",
    "price-list-2.png",
    "share-repost.png",
    "qr-share.png",
    "catalog/banner-ritual.png",
    "hero-angelgranit.png",
]

def red_ratio(path: Path, sample=4):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    px = im.load()
    red = tot = 0
    for y in range(0, h, sample):
        for x in range(0, w, sample):
            r, g, b, a = px[x, y]
            if a < 40:
                continue
            tot += 1
            mx = max(r, g, b)
            mn = min(r, g, b)
            if mx < 40:
                continue
            # red-ish: high R, low G/B relative
            if r > 90 and r > g * 1.35 and r > b * 1.25 and (r - g) > 25:
                red += 1
            else:
                # HSV hue near red
                hsv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                hue, sat, val = hsv
                if sat > 0.35 and val > 0.2 and (hue < 0.05 or hue > 0.92):
                    red += 1
    return red, tot, (100.0 * red / tot if tot else 0), w, h

for rel in FILES:
    p = ROOT / rel
    if not p.exists():
        print("MISSING", rel)
        continue
    red, tot, pct, w, h = red_ratio(p)
    mark = "***" if pct > 1.5 else "   "
    print(f"{mark} {pct:5.1f}% red  {w}x{h}  {rel}")
