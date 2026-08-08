# -*- coding: utf-8 -*-
"""Generate /uslugi/ hub and unique service pages."""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

from services_data import ADDRESS, AGENT, BASE, PHONE, PHONE_TEL, SERVICES
from seo_head import icon_links, social_meta

ROOT = Path(__file__).resolve().parents[2]
USLUGI = ROOT / "uslugi"
TODAY = date.today().isoformat()


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def ensure_desc(desc: str) -> str:
    desc = desc.strip()
    extras = [
        f" AngelGranit, {ADDRESS}, {PHONE}.",
        " Помощь 24/7.",
        " Звоните сейчас.",
    ]
    i = 0
    while len(desc) < 150 and i < len(extras):
        desc = (desc.rstrip(".") + "." + extras[i]).strip()
        i += 1
    while len(desc) < 150:
        desc = (desc.rstrip(".") + ". Алматы.").strip()
    if len(desc) > 160:
        cut = desc[:160]
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        desc = cut.rstrip(".,;:") + "."
        if len(desc) < 150:
            desc = (desc.rstrip(".") + " Алматы.").strip()[:160]
    return desc


def related_for(slug: str, n: int = 6) -> list[dict]:
    others = [s for s in SERVICES if s["slug"] != slug]
    idx = next(i for i, s in enumerate(SERVICES) if s["slug"] == slug)
    rotated = others[idx:] + others[:idx]
    return rotated[:n]


def related_articles_html(service_slug: str, n: int = 6) -> str:
    idx_path = Path(__file__).with_name("articles_index.json")
    if not idx_path.exists():
        return '<p class="lead"><a href="../../stati/">Смотреть раздел статей</a></p>'
    data = json.loads(idx_path.read_text(encoding="utf-8"))
    matched = [a for a in data if service_slug in a.get("services", [])]
    if not matched:
        matched = data[:n]
    matched = matched[:n]
    return "\n".join(
        f'<a href="../../stati/{html.escape(a["slug"])}/"><strong>{html.escape(a["question"])}?</strong><span>Статья</span></a>'
        for a in matched
    )


def nav_html(depth: int = 1) -> str:
    prefix = "../" * depth
    home = prefix if depth else "./"
    items = "\n".join(
        f'          <a href="{prefix}uslugi/{esc(s["slug"])}/">{esc(s["h1"].replace(" в Алматы", "").replace(" на могилу", "").strip())}</a>'
        for s in SERVICES
    )
    return f"""  <header class="site-nav" data-site-nav>
    <a class="site-nav__brand" href="{home}"><strong>AngelGranit</strong><span>AG</span></a>
    <button class="site-nav__toggle" type="button" data-nav-toggle aria-expanded="false">Меню</button>
    <ul class="site-nav__menu">
      <li class="site-nav__item" data-dropdown>
        <button type="button" aria-expanded="false">Услуги</button>
        <div class="site-nav__dropdown">
          <a href="{prefix}uslugi/">Все услуги</a>
{items}
        </div>
      </li>
      <li class="site-nav__item" data-dropdown>
        <button type="button" aria-expanded="false">Статьи</button>
        <div class="site-nav__dropdown">
          <a href="{prefix}stati/">Все статьи</a>
          <a href="{prefix}stati/pervye-shagi/">Первые шаги</a>
          <a href="{prefix}stati/organizaciya-pohoron/">Организация похорон</a>
          <a href="{prefix}stati/dokumenty/">Документы</a>
          <a href="{prefix}stati/transport/">Катафалк и перевозка</a>
          <a href="{prefix}stati/prinadlezhnosti/">Принадлежности</a>
          <a href="{prefix}stati/pamyatniki/">Памятники</a>
          <a href="{prefix}stati/granit-i-gravirovka/">Гранит и гравировка</a>
          <a href="{prefix}stati/blagoustrojstvo/">Благоустройство</a>
          <a href="{prefix}stati/tradicii/">Традиции</a>
          <a href="{prefix}stati/ceny-i-byudzhet/">Цены и бюджет</a>
        </div>
      </li>
      <li class="site-nav__item" data-dropdown>
        <button type="button" aria-expanded="false">Районы</button>
        <div class="site-nav__dropdown">
          <a href="{prefix}rajony/">Все районы Алматы</a>
          <a href="{prefix}rajony/zhetysuskij/">Жетысуский</a>
          <a href="{prefix}rajony/almalinskij/">Алмалинский</a>
          <a href="{prefix}rajony/auezovskij/">Ауэзовский</a>
          <a href="{prefix}rajony/bostandykskij/">Бостандыкский</a>
          <a href="{prefix}naselennye-punkty/">Населённые пункты</a>
          <a href="{prefix}naselennye-punkty/kaskelen/">Каскелен</a>
          <a href="{prefix}naselennye-punkty/talgar/">Талгар</a>
        </div>
      </li>
      <li><a href="{home}#packages">Цены</a></li>
      <li><a href="{home}#works">Наши работы</a></li>
      <li><a href="{prefix}kontakty/">Контакты</a></li>
    </ul>
    <a class="site-nav__call" href="tel:{PHONE_TEL}">Позвонить 24/7</a>
  </header>"""


def render_service(page: dict) -> str:
    title = page["title"]
    desc = ensure_desc(page["description"])
    url = f"{BASE}/uslugi/{page['slug']}/"
    related = related_for(page["slug"])
    img = f"{BASE}/images/seo/{page['image']}"
    img_rel = f"../../images/seo/{page['image']}"

    sections_html = []
    for h2, paras in page["sections"]:
        sections_html.append(f"<h2>{esc(h2)}</h2>")
        for p in paras:
            sections_html.append(f"<p>{esc(p)}</p>")
    article = "\n".join(sections_html)

    faq_html = "\n".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in page["faq"]
    )
    rel_html = "\n".join(
        f'<a href="../{esc(r["slug"])}/"><strong>{esc(r["h1"])}</strong><span>{esc(r["lead"][:120])}…</span></a>'
        for r in related
    )
    articles_html = related_articles_html(page["slug"])

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE}/#organization",
                "name": "AngelGranit",
                "url": f"{BASE}/",
                "logo": f"{BASE}/assets/icons/icon-512.png",
                "telephone": PHONE_TEL,
            },
            {
                "@type": "WebSite",
                "@id": f"{BASE}/#website",
                "url": f"{BASE}/",
                "name": "AngelGranit",
                "publisher": {"@id": f"{BASE}/#organization"},
            },
            {
                "@type": ["LocalBusiness", "FuneralHome"],
                "@id": f"{BASE}/#business",
                "name": "AngelGranit",
                "url": f"{BASE}/",
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
                "isPartOf": {"@id": f"{BASE}/#website"},
                "primaryImageOfPage": {"@type": "ImageObject", "url": img},
            },
            {
                "@type": "Service",
                "name": page["h1"],
                "description": desc,
                "provider": {"@id": f"{BASE}/#business"},
                "areaServed": {"@type": "City", "name": "Алматы"},
                "url": url,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Услуги", "item": f"{BASE}/uslugi/"},
                    {"@type": "ListItem", "position": 3, "name": page["h1"], "item": url},
                ],
            },
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

    img_webp = img_rel.replace(".png", ".webp").replace(".jpg", ".webp").replace(".jpeg", ".webp")
    if not img_webp.endswith(".webp"):
        img_webp = img_rel.rsplit(".", 1)[0] + ".webp" if "." in img_rel else img_rel

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="canonical" href="{url}" />
{icon_links("../../")}
{social_meta(title=esc(title), desc=esc(desc), url=url, image=img)}
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../seo/assets/seo.css" />
  <link rel="stylesheet" href="../../assets/site/nav.css" />
  <link rel="stylesheet" href="../../assets/site/page.css" />
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{nav_html(2)}
  <main class="page-main">
    <div class="page-wrap">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../../">Главная</a></li>
          <li><a href="../">Услуги</a></li>
          <li aria-current="page">{esc(page["h1"])}</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>{esc(page["h1"])}</h1>
        <p class="lead">{esc(page["lead"])}</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn-site btn-site--ghost" href="{esc(page["seo_link"])}">{esc(page["seo_label"])}</a>
        </div>
      </header>
      <figure class="page-figure">
        <picture>
          <source srcset="{img_webp}" type="image/webp" />
          <img src="{img_rel}" alt="{esc(page["h1"])}" title="{esc(page["h1"])} — AngelGranit" width="1600" height="900" loading="eager" decoding="async" fetchpriority="high" />
        </picture>
      </figure>
      <article class="page-article">
{article}
        <p>Нужна помощь по запросу «{esc(page["focus"])}»? Агент {esc(AGENT)} на связи 24/7: <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>, офис {esc(ADDRESS)}.</p>
      </article>
      <section class="page-faq" id="faq">
        <h2>Частые вопросы</h2>
{faq_html}
      </section>
      <section>
        <h2>Связанные услуги</h2>
        <div class="related-grid">
{rel_html}
        </div>
      </section>
      <section>
        <h2>Полезные статьи</h2>
        <div class="related-grid">
{articles_html}
        </div>
      </section>
      <div class="page-cta" style="margin-top:2rem">
        <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить</a>
        <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">Написать в WhatsApp</a>
        <a class="btn-site btn-site--ghost" href="../">Все услуги</a>
      </div>
    </div>
  </main>
  <footer class="page-footer">
    <strong>AngelGranit</strong>
    Ритуальные услуги Алматы · {esc(AGENT)} · {esc(ADDRESS)} · <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
    <ul class="page-footer-links">
      <li><a href="../../">Главная</a></li>
      <li><a href="../">Услуги</a></li>
      <li><a href="../../seo/">Справочник</a></li>
      <li><a href="../../kontakty/">Контакты</a></li>
    </ul>
  </footer>
  <script src="../../assets/site/nav.js" defer></script>
</body>
</html>
"""


def render_hub() -> str:
    cards = "\n".join(
        f'<a class="hub-card" href="{esc(s["slug"])}/"><strong>{esc(s["h1"])}</strong><span>{esc(s["lead"][:140])}…</span></a>'
        for s in SERVICES
    )
    title = "Услуги AngelGranit в Алматы | Ритуал, памятники, катафалк"
    desc = ensure_desc(
        "Все услуги AngelGranit в Алматы: ритуальные услуги, похороны, катафалк, памятники, благоустройство. 24/7."
    )
    url = f"{BASE}/uslugi/"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": title,
                "description": desc,
                "url": url,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Услуги", "item": url},
                ],
            },
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
{icon_links("../")}
{social_meta(title=esc(title), desc=esc(desc), url=url, image=f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp")}
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../seo/assets/seo.css" />
  <link rel="stylesheet" href="../assets/site/nav.css" />
  <link rel="stylesheet" href="../assets/site/page.css" />
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{nav_html(1)}
  <main class="page-main">
    <div class="page-wrap--wide">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../">Главная</a></li>
          <li aria-current="page">Услуги</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>Услуги AngelGranit в Алматы</h1>
        <p class="lead">Ритуальные услуги, организация похорон, катафалк, памятники и благоустройство — выберите направление.</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
        </div>
      </header>
      <div class="hub-grid">
{cards}
      </div>
    </div>
  </main>
  <footer class="page-footer">
    <strong>AngelGranit</strong>
    {esc(AGENT)} · {esc(ADDRESS)} · <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
  </footer>
  <script src="../assets/site/nav.js" defer></script>
</body>
</html>
"""


def render_kontakty() -> str:
    title = "Контакты AngelGranit в Алматы | Ритуальные услуги 24/7"
    desc = ensure_desc(
        f"Контакты AngelGranit: ритуальные услуги Алматы 24/7. Агент {AGENT}, {PHONE}, {ADDRESS}."
    )
    url = f"{BASE}/kontakty/"
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
{icon_links("../")}
{social_meta(title=esc(title), desc=esc(desc), url=url, image=f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp")}
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../seo/assets/seo.css" />
  <link rel="stylesheet" href="../assets/site/nav.css" />
  <link rel="stylesheet" href="../assets/site/page.css" />
</head>
<body>
{nav_html(1)}
  <main class="page-main">
    <div class="page-wrap">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../">Главная</a></li>
          <li aria-current="page">Контакты</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>Контакты AngelGranit</h1>
        <p class="lead">Ритуальные услуги в Алматы 24/7. Агент {esc(AGENT)}.</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
        </div>
      </header>
      <article class="page-article">
        <h2>Адрес и связь</h2>
        <p>Офис: <a href="https://2gis.kz/almaty/geo/9430047375176085" target="_blank" rel="noopener noreferrer">{esc(ADDRESS)}</a>, Жетысуский район, Алматы.</p>
        <p>Телефон: <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a></p>
        <p>Режим: круглосуточно, без выходных.</p>
        <h2>Как быстро получить помощь</h2>
        <p>Позвоните или напишите в WhatsApp — агент подскажет следующие шаги по организации похорон, катафалку или памятнику.</p>
      </article>
      <div class="page-cta">
        <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить</a>
        <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <a class="btn-site btn-site--ghost" href="../uslugi/">Смотреть услуги</a>
      </div>
    </div>
  </main>
  <footer class="page-footer"><strong>AngelGranit</strong>{esc(ADDRESS)} · {esc(PHONE)}</footer>
  <script src="../assets/site/nav.js" defer></script>
</body>
</html>
"""


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    extra = [(f"{BASE}/uslugi/", "0.95"), (f"{BASE}/kontakty/", "0.9")]
    for s in SERVICES:
        extra.append((f"{BASE}/uslugi/{s['slug']}/", "0.9"))

    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'

    # remove old uslugi/kontakty entries then inject after first url block end
    text = re.sub(
        r"\s*<url>\s*<loc>https://shniakin8711-collab\.github\.io/AngelGranit/(?:uslugi(?:/[^<]*)?|kontakty)/</loc>[\s\S]*?</url>",
        "",
        text,
    )

    blocks = []
    for loc, pr in extra:
        blocks.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            f"    <priority>{pr}</priority>\n"
            "  </url>"
        )
    injection = "\n".join(blocks) + "\n"
    if "</urlset>" in text:
        text = text.replace("</urlset>", injection + "</urlset>")
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    USLUGI.mkdir(parents=True, exist_ok=True)
    (USLUGI / "index.html").write_text(render_hub(), encoding="utf-8", newline="\n")
    for page in SERVICES:
        out = USLUGI / page["slug"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(render_service(page), encoding="utf-8", newline="\n")
        print("OK", page["slug"], "desc", len(ensure_desc(page["description"])), "faq", len(page["faq"]))
    kontakty = ROOT / "kontakty"
    kontakty.mkdir(parents=True, exist_ok=True)
    (kontakty / "index.html").write_text(render_kontakty(), encoding="utf-8", newline="\n")
    # sitemap is rebuilt by optimize_site / fix_audit_issues
    print("pages", len(SERVICES), "+ hub + kontakty")


if __name__ == "__main__":
    main()
