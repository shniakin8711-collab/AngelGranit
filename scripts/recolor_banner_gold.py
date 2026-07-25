# -*- coding: utf-8 -*-
"""Aggressive red→gold recolor for ritual services banner."""
from pathlib import Path
from PIL import Image
import colorsys

SRC = Path("images/banner-ritual-services.png")
OUT = SRC
GOLD_H = 0.12


def is_red(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    if mx < 35:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    # Already gold
    if 0.07 <= h <= 0.20 and s >= 0.25 and g >= r * 0.55:
        return False
    # Skip near-white / gray text
    if s < 0.12 and v > 0.55:
        return False
    # Bright UI red (icons, 24/7, phone)
    if r >= 100 and g < 95 and b < 95 and r > g + 35 and r > b + 35:
        return True
    # Darker red glows / borders
    if r >= 55 and g <= r * 0.75 and b <= r * 0.75 and (r - g) >= 20 and (r - b) >= 20:
        if s >= 0.25 or (r - g) >= 30:
            return True
    # Hue-based red
    if (h <= 0.055 or h >= 0.93) and s >= 0.30 and v >= 0.15:
        return True
    return False


def to_gold(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    # Bright accents → bright gold; dark → deeper gold
    s = min(1.0, max(0.55, s * 1.1))
    v = min(1.0, max(0.42, v * 1.35 if v < 0.55 else v * 1.12))
    nr, ng, nb = colorsys.hsv_to_rgb(GOLD_H, s, v)
    return int(nr * 255), int(ng * 255), int(nb * 255)


def main():
    im = Image.open(SRC).convert("RGBA")
    px = im.load()
    w, h = im.size
    n = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 10:
                continue
            if is_red(r, g, b):
                nr, ng, nb = to_gold(r, g, b)
                px[x, y] = (nr, ng, nb, a)
                n += 1
    # Save as optimized PNG
    rgb = Image.new("RGB", im.size, (0, 0, 0))
    rgb.paste(im, mask=im.split()[3])
    rgb.save(OUT, format="PNG", optimize=True)
    print(f"recolored {n} pixels ({100*n/(w*h):.1f}%) -> {OUT} size={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
