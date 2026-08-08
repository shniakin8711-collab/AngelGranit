# -*- coding: utf-8 -*-
"""Patch static seo/pillar pages: favicon, manifest, OG webp."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

OLD_ICON = re.compile(
    r"<link rel=\"icon\" href=\"data:image/svg\+xml,[^\"]+\" type=\"image/svg\+xml\"\s*/?>"
)
OG_PNG = "images/hero-angelgranit.png"
OG_WEBP = "images/hero-angelgranit.webp"


def depth_prefix(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth


def icons(prefix: str) -> str:
    return (
        f'<link rel="icon" href="{prefix}assets/icons/favicon.svg" type="image/svg+xml" />\n'
        f'  <link rel="icon" href="{prefix}assets/icons/favicon-32.png" type="image/png" sizes="32x32" />\n'
        f'  <link rel="apple-touch-icon" href="{prefix}assets/icons/apple-touch-icon.png" />\n'
        f'  <link rel="manifest" href="{prefix}site.webmanifest" />'
    )


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    prefix = depth_prefix(path)
    if OLD_ICON.search(text):
        text = OLD_ICON.sub(icons(prefix), text, count=1)
    elif 'assets/icons/favicon.svg' not in text and "</head>" in text:
        text = text.replace("</head>", f"  {icons(prefix)}\n</head>", 1)
    text = text.replace(OG_PNG, OG_WEBP)
    if 'name="twitter:image"' not in text and 'property="og:image"' in text:
        # add twitter if missing
        text = re.sub(
            r'(<meta property="og:image"[^>]*>)',
            r'\1\n  <meta name="twitter:card" content="summary_large_image" />\n  <meta name="twitter:image" content="https://shniakin8711-collab.github.io/AngelGranit/images/hero-angelgranit.webp" />',
            text,
            count=1,
        )
    if text != orig:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    n = 0
    for folder in ["seo"]:
        d = ROOT / folder
        if d.exists():
            for p in d.rglob("index.html"):
                if patch(p):
                    n += 1
                    print("patched", p.relative_to(ROOT))
    for p in ROOT.iterdir():
        if p.is_dir() and (p / "index.html").exists() and (
            p.name.endswith("-almaty") or p.name in {"ritualnye-uslugi-almaty"}
        ):
            if patch(p / "index.html"):
                n += 1
                print("patched", p.name)
    print("done", n)


if __name__ == "__main__":
    main()
