# -*- coding: utf-8 -*-
"""Apply noindex rules for thin GEO / locality pages, then rebuild sitemap."""
from __future__ import annotations

import re
from pathlib import Path

from sitemap_utils import (
    ROOT,
    SKIP_DIRS,
    THIN_LOCATION_WORDS,
    main_unique_words,
    rebuild_sitemap,
)

ROBOTS_NOINDEX = (
    "noindex, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
)
ROBOTS_INDEX = (
    "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
)


def set_robots(html: str, content: str) -> str:
    if re.search(r'<meta\s+name="robots"', html, re.I):
        return re.sub(
            r'(<meta\s+name="robots"\s+content=")[^"]*(")',
            rf"\1{content}\2",
            html,
            count=1,
            flags=re.I,
        )
    insert = f'  <meta name="robots" content="{content}" />\n'
    m = re.search(r"<meta\s+charset", html, re.I)
    if m:
        pos = html.find(">", m.start()) + 1
        return html[:pos] + "\n" + insert + html[pos:]
    return insert + html


def patch_file(path: Path, *, noindex: bool) -> bool:
    html = path.read_text(encoding="utf-8")
    want = ROBOTS_NOINDEX if noindex else ROBOTS_INDEX
    cur = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', html, re.I)
    if cur and cur.group(1).strip() == want:
        return False
    new = set_robots(html, want)
    if new != html:
        path.write_text(new, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed = 0

    for p in ROOT.rglob("index.html"):
        if any(x in SKIP_DIRS for x in p.parts):
            continue
        rel = p.parent.relative_to(ROOT).as_posix()
        if rel == "geo" or rel.startswith("geo/"):
            if patch_file(p, noindex=True):
                changed += 1
            continue
        if rel.startswith("naselennye-punkty/") and rel != "naselennye-punkty":
            html = p.read_text(encoding="utf-8")
            thin = main_unique_words(html) < THIN_LOCATION_WORDS
            if patch_file(p, noindex=thin):
                changed += 1

    n = rebuild_sitemap()
    print(f"robots patched on {changed} pages; sitemap: {n} URLs")


if __name__ == "__main__":
    main()
