# -*- coding: utf-8 -*-
"""Finalize duplicate SEO mirrors: unique titles + noindex optional + sitemap."""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://angelgranit.com"


def unique_mirror_titles() -> int:
    n = 0
    seo = ROOT / "seo"
    for child in seo.iterdir():
        if not child.is_dir() or not (child / "index.html").exists():
            continue
        p = child / "index.html"
        html = p.read_text(encoding="utf-8")
        m = re.search(r'rel="canonical" href="([^"]+)"', html)
        if not m:
            continue
        self_url = f"{BASE}/seo/{child.name}/"
        can = m.group(1)
        if can.rstrip("/") == self_url.rstrip("/"):
            continue  # already self-canonical unique page
        # mirror: unique title + robots index,follow still ok with canonical
        tm = re.search(r"<title>(.*?)</title>", html, re.S)
        if not tm:
            continue
        title = re.sub(r"\s+", " ", tm.group(1)).strip()
        if "справочник" not in title.lower() and "гид" not in title.lower():
            # strip trailing brand then re-add marker
            core = re.sub(r"\s*\|\s*AngelGranit\s*$", "", title).strip()
            new_title = f"{core} — справочник | AngelGranit"
            html2 = html.replace(f"<title>{tm.group(1)}</title>", f"<title>{new_title}</title>", 1)
            html2 = re.sub(
                r'(property="og:title" content=")[^"]*(")',
                rf"\1{new_title}\2",
                html2,
                count=1,
            )
            html2 = re.sub(
                r'(name="twitter:title" content=")[^"]*(")',
                rf"\1{new_title}\2",
                html2,
                count=1,
            )
            if html2 != html:
                p.write_text(html2, encoding="utf-8", newline="\n")
                n += 1
                print("title", child.name)
    return n


def fix_seo_hub_meta() -> None:
    p = ROOT / "seo" / "index.html"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    t = re.sub(
        r'<meta name="description" content="[^"]*" />',
        '<meta name="description" content="Справочник AngelGranit: ритуальные услуги Алматы, памятники, катафалк, документы, районы города и ответы на частые вопросы семей." />',
        t,
        count=1,
    )
    t = re.sub(
        r"<title>.*?</title>",
        "<title>Справочник ритуальных услуг и памятников Алматы | AngelGranit</title>",
        t,
        count=1,
        flags=re.S,
    )
    p.write_text(t, encoding="utf-8", newline="\n")


def fix_seo_kontakty_title() -> None:
    p = ROOT / "seo" / "kontakty" / "index.html"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    t = re.sub(
        r"<title>.*?</title>",
        "<title>Контакты AngelGranit в Алматы | Ритуальные услуги 24/7</title>",
        t,
        count=1,
        flags=re.S,
    )
    p.write_text(t, encoding="utf-8", newline="\n")


def rebuild_sitemap() -> int:
    today = date.today().isoformat()
    urls: list[tuple[str, str]] = [(f"{BASE}/", "1.0")]
    for folder, pr in [
        ("uslugi", "0.95"),
        ("stati", "0.9"),
        ("rajony", "0.85"),
        ("naselennye-punkty", "0.8"),
        ("kontakty", "0.9"),
    ]:
        d = ROOT / folder
        if (d / "index.html").exists():
            urls.append((f"{BASE}/{folder}/", pr))
        if d.exists():
            for child in sorted(d.iterdir()):
                if child.is_dir() and (child / "index.html").exists():
                    urls.append((f"{BASE}/{folder}/{child.name}/", "0.75" if folder == "stati" else pr))

    for p in ROOT.iterdir():
        if p.is_dir() and (p / "index.html").exists() and (
            p.name.endswith("-almaty") or p.name == "ritualnye-uslugi-almaty"
        ):
            urls.append((f"{BASE}/{p.name}/", "0.85"))

    seo = ROOT / "seo"
    if (seo / "index.html").exists():
        urls.append((f"{BASE}/seo/", "0.7"))
    if seo.exists():
        for child in sorted(seo.iterdir()):
            if not child.is_dir() or not (child / "index.html").exists():
                continue
            html = (child / "index.html").read_text(encoding="utf-8", errors="replace")
            m = re.search(r'rel="canonical" href="([^"]+)"', html)
            self_url = f"{BASE}/seo/{child.name}/"
            if not m:
                continue
            if m.group(1).rstrip("/") == self_url.rstrip("/"):
                urls.append((self_url, "0.7"))

    seen = set()
    out = []
    for loc, pr in urls:
        if loc not in seen:
            seen.add(loc)
            out.append((loc, pr))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, pr in out:
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{today}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{pr}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return len(out)


def main() -> None:
    print("mirrors titled", unique_mirror_titles())
    fix_seo_hub_meta()
    fix_seo_kontakty_title()
    print("sitemap", rebuild_sitemap())


if __name__ == "__main__":
    main()
