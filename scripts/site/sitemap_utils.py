# -*- coding: utf-8 -*-
"""Shared sitemap rebuild: indexable HTML only (AngelGranit GitHub Pages)."""
from __future__ import annotations

import re
from datetime import date, datetime
from html import unescape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://angelgranit.com"
SKIP_DIRS = {".git", ".idea", "scripts", "node_modules", "__pycache__", "assets"}

# Short GEO answers and thin locality pages are noindex — never list in sitemap.
SITEMAP_SKIP_PREFIXES = ("geo/",)

THIN_LOCATION_WORDS = 600


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE}/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-10]}"
    if rel == "404.html":
        return f"{BASE}/404.html"
    return f"{BASE}/{rel}"


def get_meta(html: str, name: str) -> str | None:
    m = re.search(rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"', html, re.I)
    return unescape(m.group(1)) if m else None


def get_canonical(html: str) -> str | None:
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.I)
    return unescape(m.group(1).strip()) if m else None


def main_unique_words(html: str) -> int:
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.I | re.S)
    body = m.group(1) if m else html
    text = re.sub(r"<script[\s\S]*?</script>", " ", body, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split()) if text else 0


def file_lastmod(path: Path) -> str:
    try:
        ts = path.stat().st_mtime
        return datetime.fromtimestamp(ts).date().isoformat()
    except OSError:
        return date.today().isoformat()


def should_include_in_sitemap(path: Path, html: str) -> bool:
    if path.name != "index.html":
        return False
    if path.name == "404.html" or path.name == "404.html":
        return False
    rel = path.relative_to(ROOT).as_posix()
    if rel == "404.html":
        return False
    rel_dir = path.parent.relative_to(ROOT).as_posix()
    if rel_dir == ".":
        pass
    elif any(rel_dir == p.rstrip("/") or rel_dir.startswith(p) for p in SITEMAP_SKIP_PREFIXES):
        return False

    robots = (get_meta(html, "robots") or "").lower()
    if "noindex" in robots:
        return False

    if rel_dir.startswith("naselennye-punkty/") and rel_dir != "naselennye-punkty":
        if main_unique_words(html) < THIN_LOCATION_WORDS:
            return False

    return True


def priority_for_url(loc: str) -> float:
    high = {
        f"{BASE}/": 1.0,
        f"{BASE}/uslugi/": 0.95,
        f"{BASE}/ceny/": 0.9,
        f"{BASE}/nashi-raboty/": 0.9,
        f"{BASE}/stati/": 0.9,
        f"{BASE}/kontakty/": 0.9,
        f"{BASE}/faq/": 0.85,
        f"{BASE}/otzyvy/": 0.85,
        f"{BASE}/o-kompanii/": 0.85,
        f"{BASE}/klastery/": 0.8,
        f"{BASE}/temy/": 0.8,
    }
    if loc in high:
        return high[loc]
    if "/uslugi/" in loc or "/stati/" in loc:
        pri = 0.7
    else:
        pri = 0.65
    if any(x in loc for x in ("-almaty", "/rajony/", "/naselennye-punkty/")):
        pri = max(pri, 0.75)
    return pri


def collect_index_html_pages() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("index.html"):
        if any(x in SKIP_DIRS for x in p.parts):
            continue
        out.append(p)
    return sorted(out, key=lambda p: str(p))


def rebuild_sitemap(*, dry_run: bool = False) -> int:
    urls: list[tuple[str, float, str]] = []
    seen: set[str] = set()

    for path in collect_index_html_pages():
        if path.name == "404.html":
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        if not should_include_in_sitemap(path, html):
            continue

        self_url = page_url(path)
        rel = path.parent.relative_to(ROOT).as_posix()
        canon = get_canonical(html) or self_url

        if rel.startswith("seo/") and rel != "seo":
            if canon.rstrip("/") != self_url.rstrip("/"):
                continue

        loc = canon if canon.endswith("/") or canon == f"{BASE}/" else canon + "/"

        if loc in seen:
            continue
        seen.add(loc)
        urls.append((loc, priority_for_url(loc), file_lastmod(path)))

    urls.sort(key=lambda x: (0 if x[0] == f"{BASE}/" else 1, x[0]))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pri, lastmod in urls:
        lines += [
            "  <url>",
            f"    <loc>{xml_escape(loc)}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{pri:.2f}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    lines.append("")

    text = "\n".join(lines)
    if not dry_run:
        out_path = ROOT / "sitemap.xml"
        tmp = out_path.with_suffix(".xml.tmp")
        tmp.write_text(text, encoding="utf-8", newline="\n")
        tmp.replace(out_path)
    return len(urls)


if __name__ == "__main__":
    n = rebuild_sitemap()
    print(f"sitemap.xml: {n} indexable URLs")
