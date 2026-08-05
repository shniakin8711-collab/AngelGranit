# -*- coding: utf-8 -*-
"""Convert generated SEO PNGs to optimized WebP 1600x900+."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ASSETS = Path(r"C:\Users\РС\.cursor\projects\c-Users-OneDrive-Desktop\assets")
OUT = Path(__file__).resolve().parents[2] / "images" / "seo"
OUT.mkdir(parents=True, exist_ok=True)

FILES = [
    "ritualnye-uslugi-almaty",
    "organizaciya-pohoron-almaty",
    "ritualny-agent-konsultaciya",
    "katafalk-almaty",
    "granitnye-pamyatniki-almaty",
    "memorialny-kompleks-almaty",
    "ustanovka-pamyatnika-almaty",
    "cvety-vozle-pamyatnika",
    "alleya-kladbishcha",
    "granitnaya-masterskaya",
    "hudozhestvennaya-gravirovka",
    "memorialny-kompleks-chernyj-granit",
    "pamyatnik-s-blagoustrojstvom",
    "granitnyj-stol-lavochka",
    "vaza-iz-granita",
    "oformlenie-mesta-zahoroneniya",
    "professionalnaya-ustanovka-kompleksa",
    "semejnyj-memorial",
    "naturalnyj-granit-krupnym-planom",
    "ritualnye-prinadlezhnosti-almaty",
]

TARGET_W, TARGET_H = 1600, 900


def convert(name: str) -> None:
    src = ASSETS / f"{name}.png"
    if not src.exists():
        raise FileNotFoundError(src)
    img = Image.open(src).convert("RGB")
    w, h = img.size
    # Upscale if needed to meet 1600x900
    scale = max(TARGET_W / w, TARGET_H / h, 1.0)
    if scale > 1.0:
        img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        w, h = img.size
    # Center-crop to 16:9 if needed, keeping at least 1600x900
    target_ratio = TARGET_W / TARGET_H
    ratio = w / h
    if abs(ratio - target_ratio) > 0.02:
        if ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
        w, h = img.size
    if w < TARGET_W or h < TARGET_H:
        img = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        w, h = TARGET_W, TARGET_H
    out = OUT / f"{name}.webp"
    img.save(out, "WEBP", quality=82, method=6)
    size_kb = out.stat().st_size / 1024
    print(f"OK {name}.webp {w}x{h} {size_kb:.0f}KB")


def main() -> None:
    for name in FILES:
        convert(name)
    print("done", len(FILES))


if __name__ == "__main__":
    main()
