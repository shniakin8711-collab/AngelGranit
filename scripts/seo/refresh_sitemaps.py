# -*- coding: utf-8 -*-
"""Refresh sitemaps for Google Search Console indexing."""
from __future__ import annotations

from datetime import date
from pathlib import Path

BASE = "https://angelgranit.com"
TODAY = date.today().isoformat()
ROOT = Path(__file__).resolve().parents[2]

PRIORITY = [
    ("/", "1.0"),
    ("/ritualnye-uslugi-almaty/", "1.0"),
    ("/organizaciya-pohoron-almaty/", "0.95"),
    ("/ritualny-agent-almaty/", "0.95"),
    ("/katafalk-almaty/", "0.9"),
    ("/ritualnye-prinadlezhnosti-almaty/", "0.9"),
    ("/pamyatniki-almaty/", "0.85"),
    ("/granitnye-pamyatniki-almaty/", "0.85"),
    ("/memorialnye-kompleksy-almaty/", "0.85"),
    ("/seo/", "0.7"),
    ("/seo/kontakty/", "0.7"),
    ("/seo/faq/", "0.7"),
]


def write_urlset(path: Path, urls: list[tuple[str, str]]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pr in urls:
        lines += [
            "  <url>",
            f"    <loc>{BASE}{loc}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            "    <changefreq>daily</changefreq>",
            f"    <priority>{pr}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    write_urlset(ROOT / "sitemap-priority.xml", PRIORITY)

    # Full sitemap: priority first, then all seo pages
    urls = list(PRIORITY)
    seo_dir = ROOT / "seo"
    seen = {BASE + loc for loc, _ in urls}
    if seo_dir.exists():
        for p in sorted(seo_dir.iterdir()):
            if p.is_dir() and (p / "index.html").exists() and p.name != "assets":
                loc = f"{BASE}/seo/{p.name}/"
                if loc not in seen:
                    urls.append((f"/seo/{p.name}/", "0.65"))
                    seen.add(loc)
    write_urlset(ROOT / "sitemap.xml", urls)

    # sitemap index
    index = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{BASE}/sitemap-priority.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>
  <sitemap>
    <loc>{BASE}/sitemap.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>
</sitemapindex>
"""
    (ROOT / "sitemap-index.xml").write_text(index, encoding="utf-8", newline="\n")
    print("sitemaps updated", TODAY, "urls", len(urls))


if __name__ == "__main__":
    main()
