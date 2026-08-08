# -*- coding: utf-8 -*-
"""Generate unique semantic-gap landing pages at site root (and nested NP pages)."""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

from missing_pages_data import ADDRESS, AGENT, MISSING_PAGES, PHONE
from seo_head import icon_links, social_meta

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://shniakin8711-collab.github.io/AngelGranit"
PHONE_TEL = "+77010567667"
TODAY = date.today().isoformat()
IMG_BASE = f"{BASE}/images/seo"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def ensure_desc(desc: str) -> str:
    desc = re.sub(r"\s+", " ", desc.strip())
    if len(desc) < 120 and PHONE not in desc:
        desc = f"{desc.rstrip('.')} Спросите агента {AGENT}: {PHONE}."
    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0].rstrip(".,;:") + "."
    return desc


def depth_of(slug: str, page: dict) -> int:
    if "depth" in page:
        return int(page["depth"])
    return slug.count("/") + 1


def prefix(depth: int) -> str:
    return "../" * depth


def nav_html(depth: int) -> str:
    p = prefix(depth)
    return f"""  <header class="site-nav" data-site-nav>
    <a class="site-nav__brand" href="{p}"><strong>AngelGranit</strong><span>AG</span></a>
    <button class="site-nav__toggle" type="button" data-nav-toggle aria-expanded="false">Меню</button>
    <ul class="site-nav__menu">
      <li><a href="{p}uslugi/">Услуги</a></li>
      <li><a href="{p}stati/">Статьи</a></li>
      <li><a href="{p}#works">Работы</a></li>
      <li><a href="{p}kontakty/">Контакты</a></li>
    </ul>
    <a class="site-nav__call" href="tel:{PHONE_TEL}">Позвонить 24/7</a>
  </header>"""


def render_page(page: dict) -> str:
    slug = page["slug"]
    depth = depth_of(slug, page)
    pfx = prefix(depth)
    title = page["title"]
    desc = ensure_desc(page["description"])
    url = f"{BASE}/{slug.strip('/')}/"
    img_file = page["image"]
    img = f"{IMG_BASE}/{img_file}"
    img_rel = f"{pfx}images/seo/{img_file}"

    sections_html = []
    for h2, paras in page["sections"]:
        sections_html.append(f"<h2>{esc(h2)}</h2>")
        for para in paras:
            sections_html.append(f"<p>{esc(para)}</p>")
        # one H3 inside first section block for structure variety
    # Add H3 under last section programmatically unique
    if page["sections"]:
        sections_html.append(f"<h3>{esc('Как связаться с AngelGranit')}</h3>")
        sections_html.append(
            f"<p>Агент {esc(AGENT)} на связи круглосуточно: "
            f'<a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>, офис {esc(ADDRESS)}. '
            f"Напишите в WhatsApp — ответим по шагам без навязанных опций.</p>"
        )

    faq_html = "\n".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>"
        for q, a in page["faq"]
    )

    svc_html = "\n".join(
        f'<a href="{pfx}{esc(href)}"><strong>{esc(label)}</strong><span>Смотреть</span></a>'
        for href, label in page["services"]
    )
    art_html = "\n".join(
        f'<a href="{pfx}{esc(href)}"><strong>{esc(label)}</strong><span>Читать</span></a>'
        for href, label in page["articles"]
    )

    schema_type = page.get("kind", "Service")
    main_entity = {
        "@type": schema_type,
        "name": page["h1"],
        "description": desc,
        "url": url,
        "provider": {"@id": f"{BASE}/#business"},
    }
    if schema_type == "Service":
        main_entity["areaServed"] = {"@type": "City", "name": "Алматы"}
    else:
        main_entity = {
            "@type": "Article",
            "headline": page["h1"],
            "description": desc,
            "dateModified": TODAY,
            "author": {"@id": f"{BASE}/#organization"},
            "publisher": {"@id": f"{BASE}/#organization"},
            "mainEntityOfPage": url,
            "image": img,
        }

    crumbs = [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Услуги и темы", "item": f"{BASE}/temy/"},
        {"@type": "ListItem", "position": 3, "name": page["crumb"], "item": url},
    ]

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE}/#organization",
                "name": "AngelGranit",
                "url": f"{BASE}/",
                "telephone": PHONE_TEL,
            },
            {
                "@type": ["LocalBusiness", "FuneralHome"],
                "@id": f"{BASE}/#business",
                "name": "AngelGranit",
                "telephone": PHONE_TEL,
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": ADDRESS,
                    "addressLocality": "Алматы",
                    "addressCountry": "KZ",
                },
            },
            {
                "@type": "WebPage",
                "@id": url + "#webpage",
                "url": url,
                "name": title,
                "description": desc,
                "primaryImageOfPage": {"@type": "ImageObject", "url": img},
                "about": main_entity if schema_type == "Service" else {"@id": url + "#article"},
            },
            {**main_entity, "@id": url + ("#service" if schema_type == "Service" else "#article")},
            {"@type": "BreadcrumbList", "itemListElement": crumbs},
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in page["faq"]
                ],
            },
        ],
    }

    bc_html = f"""      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="{pfx}">Главная</a></li>
          <li><a href="{pfx}temy/">Темы</a></li>
          <li aria-current="page">{esc(page["crumb"])}</li>
        </ol>
      </nav>"""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="canonical" href="{url}" />
{icon_links(pfx)}
{social_meta(title=esc(title), desc=esc(desc), url=url, image=img)}
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{pfx}seo/assets/seo.css" />
  <link rel="stylesheet" href="{pfx}assets/site/nav.css" />
  <link rel="stylesheet" href="{pfx}assets/site/page.css" />
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{nav_html(depth)}
  <main class="page-main">
    <div class="page-wrap">
{bc_html}
      <header class="page-hero">
        <h1>{esc(page["h1"])}</h1>
        <p class="lead">{esc(page["lead"])}</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn-site btn-site--ghost" href="{pfx}kontakty/">Контакты и адрес</a>
        </div>
      </header>
      <figure class="page-figure">
        <img src="{img_rel}" alt="{esc(page["h1"])}" width="1600" height="900" loading="eager" decoding="async" fetchpriority="high" />
      </figure>
      <article class="page-article">
{chr(10).join(sections_html)}
        <p><strong>Основной запрос страницы:</strong> «{esc(page["focus"])}». Если нужна другая услуга — выберите в блоках ниже или позвоните.</p>
      </article>
      <section class="page-faq" id="faq">
        <h2>Частые вопросы</h2>
{faq_html}
      </section>
      <section>
        <h2>Похожие услуги</h2>
        <div class="related-grid">{svc_html}</div>
      </section>
      <section>
        <h2>Похожие статьи и материалы</h2>
        <div class="related-grid">{art_html}</div>
      </section>
      <section>
        <h2>Контакты</h2>
        <p>AngelGranit · агент {esc(AGENT)} · {esc(ADDRESS)}, Алматы</p>
        <p>Телефон: <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a> · WhatsApp 24/7</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn-site btn-site--ghost" href="{pfx}">На главную</a>
        </div>
      </section>
    </div>
  </main>
  <footer class="page-footer">
    <strong>AngelGranit</strong>
    {esc(AGENT)} · {esc(ADDRESS)} · <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
  </footer>
  <script src="{pfx}assets/site/nav.js" defer></script>
</body>
</html>
"""


def render_hub(pages: list[dict]) -> str:
    cards = "\n".join(
        f'<a class="hub-card" href="../{esc(p["slug"].strip("/"))}/"><strong>{esc(p["h1"])}</strong><span>{esc(p["focus"])}</span></a>'
        for p in pages
        if not p["slug"].startswith("naselennye-punkty/")
    )
    # nested separately
    nested = [p for p in pages if p["slug"].startswith("naselennye-punkty/")]
    nest_cards = "\n".join(
        f'<a class="hub-card" href="../{esc(p["slug"].strip("/"))}/"><strong>{esc(p["h1"])}</strong><span>{esc(p["focus"])}</span></a>'
        for p in nested
    )
    title = "Новые темы и посадочные страницы | AngelGranit"
    desc = ensure_desc(
        "Каталог тематических страниц AngelGranit по ритуальным услугам Алматы: Груз 200, цены, конфессии, зал, поминки, кладбища."
    )
    url = f"{BASE}/temy/"
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow" />
{icon_links("../")}
{social_meta(title=esc(title), desc=esc(desc), url=url, image=f"{IMG_BASE}/ritualnye-uslugi-almaty.webp")}
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Manrope:wght@400;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../seo/assets/seo.css" />
  <link rel="stylesheet" href="../assets/site/nav.css" />
  <link rel="stylesheet" href="../assets/site/page.css" />
</head>
<body>
{nav_html(1)}
  <main class="page-main">
    <div class="page-wrap--wide">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../">Главная</a></li>
          <li aria-current="page">Темы</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>Тематические страницы</h1>
        <p class="lead">Каждая страница отвечает на один основной поисковый запрос — без дублей существующих разделов.</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn-site btn-site--ghost" href="../uslugi/">Все услуги</a>
        </div>
      </header>
      <h2 style="color:#d4af57;font-family:Cinzel,Georgia,serif">Основные темы</h2>
      <div class="hub-grid">{cards}</div>
      <h2 style="color:#d4af57;font-family:Cinzel,Georgia,serif;margin-top:2rem">Каскелен</h2>
      <div class="hub-grid">{nest_cards}</div>
    </div>
  </main>
  <footer class="page-footer"><strong>AngelGranit</strong> {esc(PHONE)}</footer>
  <script src="../assets/site/nav.js" defer></script>
</body>
</html>
"""


def inject_sitemap(pages: list[dict]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8") if path.exists() else (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'
    )
    blocks = []
    for page in pages:
        loc = f"{BASE}/{page['slug'].strip('/')}/"
        if f"<loc>{loc}</loc>" in text:
            continue
        blocks.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            "    <priority>0.85</priority>\n"
            "  </url>"
        )
    hub = f"{BASE}/temy/"
    if f"<loc>{hub}</loc>" not in text:
        blocks.insert(
            0,
            "  <url>\n"
            f"    <loc>{hub}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            "    <priority>0.8</priority>\n"
            "  </url>",
        )
    if blocks and "</urlset>" in text:
        text = text.replace("</urlset>", "\n".join(blocks) + "\n</urlset>")
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    # uniqueness check
    focuses = [p["focus"] for p in MISSING_PAGES]
    slugs = [p["slug"] for p in MISSING_PAGES]
    assert len(focuses) == len(set(focuses)), "duplicate focus"
    assert len(slugs) == len(set(slugs)), "duplicate slug"

    for page in MISSING_PAGES:
        out_dir = ROOT / page["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(render_page(page), encoding="utf-8", newline="\n")
        print("OK", page["slug"])

    hub = ROOT / "temy"
    hub.mkdir(parents=True, exist_ok=True)
    (hub / "index.html").write_text(render_hub(MISSING_PAGES), encoding="utf-8", newline="\n")
    inject_sitemap(MISSING_PAGES)
    print("pages", len(MISSING_PAGES), "+ /temy/")


if __name__ == "__main__":
    main()
