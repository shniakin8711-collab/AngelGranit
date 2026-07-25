# -*- coding: utf-8 -*-
"""Replace Black Hearse brand text with Angel Granit via surgical overlay + use generated assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import shutil

ROOT = Path(".")
ASSETS = Path(r"C:\Users\РС\.cursor\projects\c-Users-OneDrive-Desktop-AngelGranit-temp\assets")
BACKUP = Path("images/_backup_red")
BACKUP.mkdir(parents=True, exist_ok=True)


def find_font(size):
    candidates = [
        r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\timesbd.ttf",
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\georgiab.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for c in candidates:
        p = Path(c)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def patch_title(path: Path, cover_box, text="ANGEL GRANIT", fill=(245, 242, 234), font_size=54):
    """cover_box = (left, top, right, bottom)"""
    im = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(im)
    # sample background near cover for fill color
    l, t, r, b = cover_box
    samples = []
    for y in range(max(0, t - 4), max(1, t)):
        for x in range(l, min(r, im.width)):
            samples.append(im.getpixel((x, y)))
    if samples:
        bg = tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
    else:
        bg = (20, 20, 22)
    # soft cover
    overlay = Image.new("RGB", im.size, bg)
    mask = Image.new("L", im.size, 0)
    md = ImageDraw.Draw(mask)
    md.rectangle(cover_box, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    im = Image.composite(overlay, im, mask)
    draw = ImageDraw.Draw(im)
    font = find_font(font_size)
    # measure text
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx = (l + r) // 2
    cy = (t + b) // 2
    x = cx - tw // 2
    y = cy - th // 2
    draw.text((x, y), text, font=font, fill=fill)
    return im


def use_generated(src_name, dest_rel, size):
    src = ASSETS / src_name
    dest = Path("images") / dest_rel
    if not src.exists():
        print("missing generated", src)
        return False
    bak = BACKUP / (dest_rel.replace("/", "__") + ".prebrand")
    if dest.exists() and not bak.exists():
        shutil.copy2(dest, bak)
    im = Image.open(src).convert("RGB")
    if im.size != size:
        im = im.resize(size, Image.Resampling.LANCZOS)
    im.save(dest, format="PNG", optimize=True)
    print("wrote", dest, im.size, dest.stat().st_size)
    return True


def main():
    # Prefer generated full rebrands (already say ANGEL GRANIT)
    use_generated("price-list-angelgranit.png", "price-list.png", (1024, 1536))
    use_generated("price-list-2-angelgranit.png", "price-list-2.png", (1024, 1536))
    use_generated("share-repost-angelgranit.png", "share-repost.png", (1024, 1536))

    # Surgical fallback / extra polish if any leftover on banner etc — skip packages (no brand text)

if __name__ == "__main__":
    main()
