# -*- coding: utf-8 -*-
"""Fix audit findings: seo_links, SEO titles/OG, a11y helpers, sitemap cleanup."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://shniakin8711-collab.github.io/AngelGranit"


def fix_services_data() -> int:
    path = ROOT / "scripts" / "site" / "services_data.py"
    text = path.read_text(encoding="utf-8")
    # from /uslugi/slug/ need ../../ not ../
    new, n = re.subn(
        r'"seo_link": "\.\./',
        '"seo_link": "../../',
        text,
    )
    if n:
        path.write_text(new, encoding="utf-8", newline="\n")
    return n


def preferred_canonical_map() -> dict[str, str]:
    """Map /seo/* paths that should canonicalize to root pillars."""
    mapping = {
        "ritualnye-uslugi-almaty": f"{BASE}/ritualnye-uslugi-almaty/",
        "organizaciya-pohoron-almaty": f"{BASE}/organizaciya-pohoron-almaty/",
        "katafalk-almaty": f"{BASE}/katafalk-almaty/",
        "ritualny-agent-almaty": f"{BASE}/ritualny-agent-almaty/",
        "ritualnye-prinadlezhnosti-almaty": f"{BASE}/ritualnye-prinadlezhnosti-almaty/",
        "pamyatniki-almaty": f"{BASE}/pamyatniki-almaty/",
        "granitnye-pamyatniki-almaty": f"{BASE}/granitnye-pamyatniki-almaty/",
        "memorialnye-kompleksy-almaty": f"{BASE}/memorialnye-kompleksy-almaty/",
    }
    return mapping


def fix_seo_pages() -> list[str]:
    fixed = []
    seo = ROOT / "seo"
    pref = preferred_canonical_map()
    for p in seo.rglob("index.html"):
        rel = p.relative_to(seo).as_posix()
        slug = "" if rel == "index.html" else rel.split("/")[0]
        text = p.read_text(encoding="utf-8")
        orig = text
        self_url = f"{BASE}/seo/" if not slug else f"{BASE}/seo/{slug}/"

        # Titles too short: ensure brand + Almaty
        m = re.search(r"<title>(.*?)</title>", text, re.S)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
            if "AngelGranit" not in title:
                title = f"{title} | AngelGranit"
            if "Алматы" not in title and slug not in {"faq", "kontakty", "index"}:
                # keep reasonable length
                if len(title) < 45:
                    title = title.replace(" | AngelGranit", " в Алматы | AngelGranit")
            if title != m.group(1).strip():
                text = text.replace(f"<title>{m.group(1)}</title>", f"<title>{title}</title>", 1)
                # sync og/twitter title if identical short
                text = re.sub(
                    r'(property="og:title" content=")[^"]*(")',
                    rf'\1{title}\2',
                    text,
                    count=1,
                )
                text = re.sub(
                    r'(name="twitter:title" content=")[^"]*(")',
                    rf'\1{title}\2',
                    text,
                    count=1,
                )

        # Align og:url with canonical (preferred or self)
        can_m = re.search(r'rel="canonical" href="([^"]+)"', text)
        canonical = can_m.group(1) if can_m else self_url
        if slug in pref:
            canonical = pref[slug]
            text = re.sub(
                r'rel="canonical" href="[^"]+"',
                f'rel="canonical" href="{canonical}"',
                text,
                count=1,
            )
        text = re.sub(
            r'property="og:url" content="[^"]+"',
            f'property="og:url" content="{canonical}"',
            text,
            count=1,
        )

        # Expand thin descriptions slightly when truncated with ellipsis junk
        text = text.replace("AngelGranit, агент…", "AngelGranit.")
        text = text.replace("AngelGranit, агент…", "AngelGranit.")

        if text != orig:
            p.write_text(text, encoding="utf-8", newline="\n")
            fixed.append(str(p.relative_to(ROOT)))
    return fixed


def fix_404() -> None:
    p = ROOT / "404.html"
    text = p.read_text(encoding="utf-8")
    text = re.sub(
        r'<meta name="description" content="[^"]*" />',
        '<meta name="description" content="Страница не найдена. Откройте ритуальные услуги AngelGranit в Алматы, каталог услуг, статьи или позвоните агенту Александру 24/7." />',
        text,
        count=1,
    )
    p.write_text(text, encoding="utf-8", newline="\n")


def fix_homepage_a11y() -> list[str]:
    p = ROOT / "index.html"
    text = p.read_text(encoding="utf-8")
    changes = []
    orig = text

    if 'id="skip-to-content"' not in text:
        text = text.replace(
            "<body>",
            '<body>\n  <a class="skip-link" id="skip-to-content" href="#top">Перейти к содержанию</a>',
            1,
        )
        # CSS for skip link near start of style if not present
        if ".skip-link" not in text:
            text = text.replace(
                "  <style>",
                """  <style>
    .skip-link {
      position: absolute;
      left: -999px;
      top: 0.75rem;
      z-index: 10000;
      padding: 0.65rem 1rem;
      background: var(--red-bright, #d4af57);
      color: #050505;
      font-weight: 700;
      text-decoration: none;
      border-radius: 4px;
    }
    .skip-link:focus {
      left: 0.75rem;
      outline: 2px solid #fff;
      outline-offset: 2px;
    }
""",
                1,
            )
        changes.append("skip-link")

    if 'aria-label="Главная навигация"' not in text:
        text = text.replace(
            '<header class="nav site-nav" id="site-nav" data-site-nav>',
            '<header class="nav site-nav" id="site-nav" data-site-nav role="banner">\n    <nav aria-label="Главная навигация">',
            1,
        )
        # close nav before end of header - find nav__call and after it close
        if "</nav>" not in text[text.find('id="site-nav"'):text.find('id="site-nav"') + 2500]:
            text = text.replace(
                '    <a class="nav__call" href="tel:+77010567667">Позвонить 24/7</a>\n  </header>',
                '    <a class="nav__call" href="tel:+77010567667">Позвонить 24/7</a>\n    </nav>\n  </header>',
                1,
            )
            changes.append("nav-landmark")

    # lightbox image dimensions
    if 'id="cat-lightbox-img" src="" alt=""' in text:
        text = text.replace(
            '<img id="cat-lightbox-img" src="" alt="" />',
            '<img id="cat-lightbox-img" src="" alt="" width="900" height="1200" decoding="async" />',
            1,
        )
        changes.append("lightbox-dims")

    # dialog modality
    text = text.replace(
        'id="cat-lightbox" aria-hidden="true" role="dialog" aria-label="Просмотр фото"',
        'id="cat-lightbox" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Просмотр фото"',
        1,
    )
    text = text.replace(
        'id="ai-chat" role="dialog" aria-label="Помощник по ритуальным услугам" aria-hidden="true"',
        'id="ai-chat" role="dialog" aria-modal="true" aria-label="Помощник по ритуальным услугам" aria-hidden="true"',
        1,
    )
    if "aria-modal" in text and "aria-modal" not in orig:
        changes.append("aria-modal")

    # focus-visible for interactive
    if "a:focus-visible" not in text:
        text = text.replace(
            "    *, *::before, *::after { box-sizing: border-box; }",
            """    *, *::before, *::after { box-sizing: border-box; }
    a:focus-visible, button:focus-visible, summary:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible {
      outline: 2px solid var(--red-bright, #d4af57);
      outline-offset: 2px;
    }""",
            1,
        )
        changes.append("focus-visible")

    if text != orig:
        p.write_text(text, encoding="utf-8", newline="\n")
    return changes


def rebuild_sitemap_prefer_canonical() -> int:
    """Drop /seo/* URLs that canonicalize away from themselves to reduce duplicate crawl."""
    from datetime import date

    today = date.today().isoformat()
    # collect preferred set via optimize collector + exclude seo clones with external canonical
    urls = []
    # home
    urls.append((f"{BASE}/", "1.0"))
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

    # keep unique seo articles that canonicalize to themselves
    seo = ROOT / "seo"
    if seo.exists():
        if (seo / "index.html").exists():
            urls.append((f"{BASE}/seo/", "0.7"))
        for child in sorted(seo.iterdir()):
            if not child.is_dir() or not (child / "index.html").exists():
                continue
            html = (child / "index.html").read_text(encoding="utf-8", errors="replace")
            m = re.search(r'rel="canonical" href="([^"]+)"', html)
            self_url = f"{BASE}/seo/{child.name}/"
            if m and m.group(1).rstrip("/") == self_url.rstrip("/"):
                urls.append((self_url, "0.7"))
            # else skip duplicate-target SEO mirrors from sitemap

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
    n = fix_services_data()
    print("seo_link fixes", n)
    seo_fixed = fix_seo_pages()
    print("seo pages patched", len(seo_fixed))
    fix_404()
    print("404 description updated")
    a11y = fix_homepage_a11y()
    print("homepage a11y", a11y)
    count = rebuild_sitemap_prefer_canonical()
    print("sitemap urls", count)


if __name__ == "__main__":
    main()
