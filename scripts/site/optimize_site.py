# -*- coding: utf-8 -*-
"""Site-wide SEO/perf helpers: WebP conversion, sitemap rebuild, favicons."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://shniakin8711-collab.github.io/AngelGranit"
TODAY = date.today().isoformat()

# Homepage-critical assets to convert (keep originals)
CONVERT = [
    "images/hero-angelgranit.png",
    "images/service-funeral.png",
    "images/showcase-monument.png",
    "images/showcase-hearse.png",
    "images/package-minimal.png",
    "images/package-hall.png",
    "images/package-standard.png",
    "images/package-elite.png",
    "images/banner-ritual-services.png",
    "images/banner-ritual-ad.png",
    "images/share-repost.png",
    "images/catalog/banner-ritual.png",
]


def _to_webp(src: Path, max_w: int = 1200, quality: int = 78) -> None:
    out = src.with_suffix(".webp")
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGB", img.size, (7, 7, 8))
        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        img = bg
    else:
        img = img.convert("RGB")
    w, h = img.size
    if w > max_w:
        nh = int(h * (max_w / w))
        img = img.resize((max_w, nh), Image.Resampling.LANCZOS)
    img.save(out, "WEBP", quality=quality, method=6)
    print("webp", out.relative_to(ROOT), f"{out.stat().st_size/1024:.0f}KB")


def convert_webp() -> None:
    for rel in CONVERT:
        src = ROOT / rel
        if not src.exists():
            print("skip missing", rel)
            continue
        max_w = 1600 if "hero" in rel or "banner" in rel else 1200
        _to_webp(src, max_w=max_w)

    catalog = ROOT / "images" / "catalog"
    if catalog.exists():
        for src in catalog.rglob("*"):
            if src.suffix.lower() in {".png", ".jpg", ".jpeg"} and src.is_file():
                max_w = 900 if "monuments" in str(src) else 1000
                _to_webp(src, max_w=max_w, quality=76)


def make_favicons() -> None:
    icons = ROOT / "assets" / "icons"
    icons.mkdir(parents=True, exist_ok=True)

    def draw_ag(size: int) -> Image.Image:
        im = Image.new("RGB", (size, size), "#050505")
        dr = ImageDraw.Draw(im)
        # gold frame
        m = max(2, size // 16)
        dr.rectangle([m, m, size - m - 1, size - m - 1], outline="#d4af57", width=max(1, size // 32))
        try:
            font = ImageFont.truetype("arial.ttf", size=int(size * 0.42))
        except Exception:
            font = ImageFont.load_default()
        text = "AG"
        bbox = dr.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        dr.text(((size - tw) / 2, (size - th) / 2 - size * 0.04), text, fill="#d4af57", font=font)
        return im

    for size, name in [(16, "favicon-16.png"), (32, "favicon-32.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
        draw_ag(size).save(icons / name, "PNG", optimize=True)

    (icons / "favicon.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" fill="#050505"/>
  <rect x="2" y="2" width="28" height="28" fill="none" stroke="#d4af57" stroke-width="1.5"/>
  <text x="16" y="22" text-anchor="middle" font-family="Georgia,serif" font-size="12" font-weight="700" fill="#d4af57">AG</text>
</svg>
""",
        encoding="utf-8",
        newline="\n",
    )
    print("favicons ok")


def collect_urls() -> list[tuple[str, str]]:
    urls: list[tuple[str, str]] = [(f"{BASE}/", "1.0")]
    roots = [
        ("uslugi", "0.95"),
        ("stati", "0.9"),
        ("rajony", "0.85"),
        ("naselennye-punkty", "0.8"),
        ("kontakty", "0.9"),
        ("seo", "0.7"),
    ]
    # pillars at root
    for p in ROOT.iterdir():
        if p.is_dir() and (p / "index.html").exists() and p.name not in {
            "uslugi", "stati", "rajony", "naselennye-punkty", "kontakty", "seo",
            "assets", "images", "scripts", ".git", ".idea", ".github"
        }:
            if p.name.endswith("-almaty") or p.name in {"ritualnye-uslugi-almaty"}:
                urls.append((f"{BASE}/{p.name}/", "0.85"))

    for folder, pr in roots:
        d = ROOT / folder
        if not d.exists():
            continue
        if (d / "index.html").exists():
            urls.append((f"{BASE}/{folder}/", pr))
        for child in sorted(d.iterdir()):
            if child.is_dir() and (child / "index.html").exists() and child.name != "assets":
                # skip nested seo/assets
                if folder == "seo" and child.name == "assets":
                    continue
                urls.append((f"{BASE}/{folder}/{child.name}/", "0.75" if folder == "stati" else pr))

    # dedupe preserve order
    seen = set()
    out = []
    for loc, pr in urls:
        if loc not in seen:
            seen.add(loc)
            out.append((loc, pr))
    return out


def write_sitemap() -> None:
    urls = collect_urls()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pr in urls:
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{pr}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("sitemap urls", len(urls))


def main() -> None:
    convert_webp()
    make_favicons()
    write_sitemap()


if __name__ == "__main__":
    main()
