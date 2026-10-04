# -*- coding: utf-8 -*-
"""Quick post-build check: sample sitemap URLs vs local HTML (robots/canonical)."""
from __future__ import annotations

import random
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://angelgranit.com"


def url_to_path(loc: str) -> Path | None:
    if not loc.startswith(BASE):
        return None
    path = urlparse(loc).path
    if path == "/":
        return ROOT / "index.html"
    return ROOT / path.strip("/") / "index.html"


def main() -> int:
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    bad = []
    for loc in random.sample(urls, min(10, len(urls))):
        p = url_to_path(loc)
        if not p or not p.is_file():
            bad.append(f"missing file: {loc}")
            continue
        html = p.read_text(encoding="utf-8", errors="replace")
        robots = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', html, re.I)
        if robots and "noindex" in robots.group(1).lower():
            bad.append(f"noindex in sitemap: {loc}")
        canon = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
        if canon:
            cval = canon.group(1).strip()
            if cval.rstrip("/") != loc.rstrip("/"):
                bad.append(f"canonical mismatch {loc} -> {cval}")
    junk = re.search(r"(AI\.md|llms\.txt|/geo/)", sm)
    if junk:
        bad.append("sitemap contains excluded paths")
    if bad:
        print("FAIL:")
        for b in bad:
            print(" ", b)
        return 1
    print(f"OK: {len(urls)} URLs in sitemap; sample of 10 passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
