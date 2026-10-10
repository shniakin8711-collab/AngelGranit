# -*- coding: utf-8 -*-
"""Point /seo/ritualnye-uslugi-*-rajon/ to canonical /rajony/{slug}/ (AI.md hierarchy)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://angelgranit.com"

DISTRICT_SLUGS = (
    "auezovskij",
    "almalinskij",
    "bostandykskij",
    "medeuskij",
    "nauryzbajskij",
    "turksibskij",
    "zhetysuskij",
    "alatauskij",
)

CANON_NOTE = (
    '<p class="hero__lead">Каноническая локальная страница: '
    '<a href="../../rajony/{slug}/">/rajony/{slug}/</a> '
    "(индекс Google). Этот URL — развёрнутый SEO-гид.</p>"
)


def patch_canonical(html: str, canon: str) -> str:
    html = re.sub(
        r'<link rel="canonical" href="[^"]*"\s*/?>',
        f'<link rel="canonical" href="{canon}" />',
        html,
        count=1,
    )
    if re.search(r'<meta property="og:url"', html):
        html = re.sub(
            r'<meta property="og:url" content="[^"]*"\s*/?>',
            f'<meta property="og:url" content="{canon}" />',
            html,
            count=1,
        )
    return html


def patch_json_ld_urls(html: str, canon: str, seo_slug: str) -> str:
    """Align WebPage + Service url with rajony canonical."""
    html = re.sub(
        r'("@type":\s*"WebPage"[\s\S]*?"url":\s*")https://angelgranit\.com/seo/ritualnye-uslugi-[^"]+(")',
        rf"\1{canon}\2",
        html,
        count=1,
    )
    seo_url = f"{BASE}/seo/{seo_slug}/"
    html = re.sub(
        rf'("@type":\s*"Service"[\s\S]*?"url":\s*"){re.escape(seo_url)}(")',
        rf"\1{canon}\2",
        html,
        count=1,
    )
    return html


def inject_rajony_note(html: str, district: str) -> str:
    note = CANON_NOTE.format(slug=district)
    if f"/rajony/{district}/" in html and "Каноническая локальная страница" in html:
        return html
    marker = '<p class="hero__lead">'
    idx = html.find(marker)
    if idx == -1:
        return html
    end = html.find("</p>", idx)
    if end == -1:
        return html
    insert_at = end + len("</p>")
    return html[:insert_at] + "\n        " + note + html[insert_at:]


def main() -> None:
    for slug in DISTRICT_SLUGS:
        seo_slug = f"ritualnye-uslugi-{slug}-rajon"
        path = ROOT / "seo" / seo_slug / "index.html"
        if not path.exists():
            print("skip missing", seo_slug)
            continue
        canon = f"{BASE}/rajony/{slug}/"
        html = path.read_text(encoding="utf-8")
        html = patch_canonical(html, canon)
        html = patch_json_ld_urls(html, canon, seo_slug)
        html = inject_rajony_note(html, slug)
        path.write_text(html, encoding="utf-8", newline="\n")
        print("OK", seo_slug, "->", canon)


if __name__ == "__main__":
    main()
