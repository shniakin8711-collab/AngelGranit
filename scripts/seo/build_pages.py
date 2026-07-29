# -*- coding: utf-8 -*-
"""Generate 50 SEO pages, hub, and sitemap for AngelGranit GitHub Pages."""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

from pages_data import BASE, CATEGORIES, PAGES, PHONE, PHONE_TEL, ADDRESS, AGENT
from build_content import REVIEWS, build_faq, build_sections

ROOT = Path(__file__).resolve().parents[2]
SEO_DIR = ROOT / "seo"
ASSETS_FROM_PAGE = "../assets"
HOME_FROM_PAGE = "../../"
TODAY = date.today().isoformat()

PAGE_BY_SLUG = {p["slug"]: p for p in PAGES}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def word_count(text: str) -> int:
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


def abs_url(slug: str | None = None) -> str:
    if slug is None:
        return f"{BASE}/seo/"
    return f"{BASE}/seo/{slug}/"


def related_cards(page) -> str:
    items = []
    for slug in page.get("related_slugs", []):
        other = PAGE_BY_SLUG.get(slug)
        if not other:
            continue
        items.append(
            f'<a href="../{esc(slug)}/"><strong>{esc(other["h1"][:70])}</strong>'
            f'<span>{esc(other["lead"][:110])}…</span></a>'
        )
    return "\n".join(items)


def article_html(page) -> str:
    parts = []
    for sec in build_sections(page):
        parts.append(f'<h2>{esc(sec["h2"])}</h2>')
        for p in sec["paragraphs"]:
            parts.append(f"<p>{esc(p)}</p>")
    return "\n".join(parts)


def faq_html(page) -> str:
    blocks = []
    for item in build_faq(page):
        blocks.append(
            "<details><summary>{q}</summary><p>{a}</p></details>".format(
                q=esc(item["q"]), a=esc(item["a"])
            )
        )
    return "\n".join(blocks)


def reviews_html() -> str:
    blocks = []
    for r in REVIEWS:
        blocks.append(
            f'<figure class="review"><p>«{esc(r["text"])}»</p>'
            f'<footer>— {esc(r["name"])}</footer></figure>'
        )
    return "\n".join(blocks)


def schema_json(page) -> str:
    page_url = abs_url(page["slug"])
    faq = build_faq(page)
    cat_name = CATEGORIES.get(page["category"], "Раздел")
    graph = [
        {
            "@type": "WebPage",
            "@id": page_url + "#webpage",
            "url": page_url,
            "name": page["title"],
            "description": page["description"],
            "isPartOf": {"@id": BASE + "/#website"},
            "about": {"@id": BASE + "/#business"},
            "inLanguage": "ru-KZ",
        },
        {
            "@type": "FuneralHome",
            "@id": BASE + "/#business",
            "name": "AngelGranit",
            "image": BASE + "/images/hero-angelgranit.png",
            "telephone": PHONE_TEL,
            "url": BASE + "/",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": ADDRESS,
                "addressLocality": "Алматы",
                "addressCountry": "KZ",
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": 43.289921,
                "longitude": 76.961065,
            },
            "openingHours": "Mo-Su 00:00-24:00",
            "priceRange": "₸₸₸",
        },
        {
            "@type": "Service",
            "@id": page_url + "#service",
            "name": page["service_name"],
            "description": page["description"],
            "provider": {"@id": BASE + "/#business"},
            "areaServed": {"@type": "City", "name": "Алматы"},
            "url": page_url,
        },
        {
            "@type": "BreadcrumbList",
            "@id": page_url + "#breadcrumb",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": BASE + "/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "SEO-материалы",
                    "item": abs_url(),
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": cat_name,
                    "item": abs_url() + "#" + page["category"],
                },
                {
                    "@type": "ListItem",
                    "position": 4,
                    "name": page["h1"],
                    "item": page_url,
                },
            ],
        },
        {
            "@type": "FAQPage",
            "@id": page_url + "#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
                }
                for f in faq
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)


def ensure_meta(page):
    title = page["title"].strip()
    if len(title) > 60:
        title = title[:57].rstrip() + "…"
    desc = page["description"].strip()
    if len(desc) < 150:
        pad = f" AngelGranit, агент {AGENT}, {ADDRESS}, тел. {PHONE}."
        desc = (desc.rstrip(".") + "." + pad).strip()
    if len(desc) > 160:
        desc = desc[:157].rstrip() + "…"
    return title, desc


def render_page(page) -> tuple[str, int]:
    cat = CATEGORIES.get(page["category"], "Раздел")
    title, desc = ensure_meta(page)
    article = article_html(page)
    body_words = word_count(article + page["lead"] + page["h1"])

    html_out = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <meta name="googlebot" content="index, follow" />
  <link rel="canonical" href="{abs_url(page['slug'])}" />
  <meta name="author" content="AngelGranit · {AGENT}" />
  <meta name="geo.region" content="KZ-ALA" />
  <meta name="geo.placename" content="Алматы" />
  <meta name="theme-color" content="#d4af57" />

  <meta property="og:type" content="article" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:site_name" content="AngelGranit — ритуальные услуги Алматы" />
  <meta property="og:url" content="{abs_url(page['slug'])}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:image" content="{BASE}/images/hero-angelgranit.png" />
  <meta property="og:image:alt" content="{esc(page['h1'])}" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{BASE}/images/hero-angelgranit.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" href="{ASSETS_FROM_PAGE}/seo.css" as="style" />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{ASSETS_FROM_PAGE}/seo.css" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23050505'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-family='Georgia,serif' font-size='12' font-weight='700' fill='%23d4af57'%3EAG%3C/text%3E%3C/svg%3E" type="image/svg+xml" />

  <script type="application/ld+json">
{schema_json(page)}
  </script>
</head>
<body>
  <header class="nav">
    <a class="nav__brand" href="{HOME_FROM_PAGE}"><strong>AngelGranit</strong><span>AG</span></a>
    <div class="nav__actions">
      <a class="btn btn--ghost" href="{HOME_FROM_PAGE}">На главную</a>
      <a class="btn btn--gold" href="tel:{PHONE_TEL}">Позвонить</a>
      <a class="btn btn--wa" href="#" data-wa-default target="_blank" rel="noopener noreferrer">WhatsApp</a>
    </div>
  </header>

  <main>
    <div class="wrap">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="{HOME_FROM_PAGE}">Главная</a></li>
          <li><a href="../">SEO-материалы</a></li>
          <li><a href="../#{esc(page['category'])}">{esc(cat)}</a></li>
          <li aria-current="page">{esc(page['h1'][:48])}</li>
        </ol>
      </nav>

      <header class="hero">
        <p class="hero__kicker">{esc(cat)} · Алматы · 24/7</p>
        <h1>{esc(page['h1'])}</h1>
        <p class="hero__lead">{esc(page['lead'])}</p>
        <div class="hero__cta">
          <a class="btn btn--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn btn--wa" href="#" data-wa-default target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn btn--ghost" href="#lead">Оставить заявку</a>
        </div>
        <figure class="hero__media">
          <img
            src="{HOME_FROM_PAGE}images/hero-angelgranit.png"
            alt="{esc(page['h1'])} — AngelGranit, ритуальные услуги и памятники в Алматы"
            width="1024"
            height="408"
            decoding="async"
            fetchpriority="high"
          />
        </figure>
      </header>

      <article class="article">
{article}
      </article>

      <div class="cta-bar">
        <p><strong>Нужна помощь сейчас?</strong> Агент {AGENT} на связи 24/7 — {esc(PHONE)}, офис {esc(ADDRESS)}.</p>
        <a class="btn btn--gold" href="tel:{PHONE_TEL}">Звонок</a>
        <a class="btn btn--wa" href="#" data-wa-default target="_blank" rel="noopener noreferrer">WhatsApp</a>
      </div>
    </div>

    <section class="section-block" id="faq">
      <div class="wrap">
        <h2>Частые вопросы</h2>
        <p class="lead">Краткие ответы по теме страницы. Если вашего вопроса нет — напишите в WhatsApp.</p>
        <div class="faq">
{faq_html(page)}
        </div>
      </div>
    </section>

    <section class="section-block" id="reviews">
      <div class="wrap">
        <h2>Отзывы семей</h2>
        <p class="lead">Примеры обратной связи о сопровождении AngelGranit в Алматы.</p>
        <div class="reviews">
{reviews_html()}
        </div>
      </div>
    </section>

    <section class="section-block" id="related">
      <div class="wrap">
        <h2>Похожие материалы и услуги</h2>
        <p class="lead">Внутренние ссылки помогут найти смежные темы без возврата в поиск.</p>
        <div class="related">
{related_cards(page)}
        </div>
      </div>
    </section>

    <section class="section-block" id="lead">
      <div class="wrap wrap--wide" style="display:grid;gap:1.25rem;">
        <div class="form-card">
          <h2>Заявка в WhatsApp</h2>
          <p class="lead">Опишите задачу — откроется чат с готовым текстом для агента Александра.</p>
          <form id="seo-lead-form">
            <div class="form-grid form-grid--2">
              <label>Имя<input name="name" autocomplete="name" required placeholder="Как к вам обращаться" /></label>
              <label>Телефон<input name="phone" type="tel" autocomplete="tel" required placeholder="+7 …" /></label>
            </div>
            <div class="form-grid" style="margin-top:0.75rem;">
              <label>Услуга
                <select name="service">
                  <option>{esc(page['service_name'])}</option>
                  <option>Организация похорон</option>
                  <option>Катафалк</option>
                  <option>Памятник из гранита</option>
                  <option>Благоустройство</option>
                  <option>Другое</option>
                </select>
              </label>
              <label>Сообщение<textarea name="message" placeholder="Кратко опишите ситуацию или вопрос"></textarea></label>
            </div>
            <div class="form-actions">
              <button class="btn btn--wa" type="submit">Отправить в WhatsApp</button>
              <a class="btn btn--gold" href="tel:{PHONE_TEL}">Позвонить</a>
            </div>
          </form>
        </div>

        <div class="map-card">
          <h2>Карта — офис AngelGranit</h2>
          <p class="lead">{esc(ADDRESS)}, Жетысуский район, Алматы</p>
          <button type="button" class="btn btn--ghost" id="seo-map-load">Показать карту Google</button>
          <div class="map-frame" id="seo-map" data-lat="43.289921" data-lng="76.961065">
            <div class="map-placeholder">Карта загрузится автоматически при прокрутке или по кнопке — так страница открывается быстрее.</div>
          </div>
          <p style="margin-top:0.75rem;font-size:0.9rem;color:var(--muted);">
            Также на <a href="https://2gis.kz/almaty/geo/9430047375176085" target="_blank" rel="noopener noreferrer">2ГИС</a>
            · <a href="{HOME_FROM_PAGE}#contact">контакты на главной</a>
          </p>
        </div>

        <div class="media-card">
          <h2>Видео YouTube · Angel Granit</h2>
          <p class="lead">Ролик и канал BLACK HEARSE FPV — примеры катафалка и атмосферы сервиса.</p>
          <div class="form-actions">
            <a class="btn btn--gold" href="https://www.youtube.com/watch?v=sryWmrJC0z4" target="_blank" rel="noopener noreferrer">Смотреть видео</a>
            <a class="btn btn--ghost" href="https://www.youtube.com/@Blackhearsefpv" target="_blank" rel="noopener noreferrer">Канал YouTube</a>
            <a class="btn btn--ghost" href="{HOME_FROM_PAGE}#youtube">Блок на главной</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <strong>AngelGranit</strong>
    Ритуальные услуги · памятники · Алматы<br />
    {AGENT} · {esc(ADDRESS)} · <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
    <ul class="footer-links">
      <li><a href="{HOME_FROM_PAGE}">Главная</a></li>
      <li><a href="../">Все SEO-страницы</a></li>
      <li><a href="../kontakty/">Контакты</a></li>
      <li><a href="../faq/">FAQ</a></li>
      <li><a href="https://www.youtube.com/@Blackhearsefpv" target="_blank" rel="noopener noreferrer">YouTube</a></li>
    </ul>
  </footer>

  <div class="sticky-cta" aria-label="Быстрые действия">
    <a class="btn btn--gold" href="tel:{PHONE_TEL}" aria-label="Позвонить">☎</a>
    <a class="btn btn--wa" href="#" data-wa-default target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">WA</a>
  </div>

  <script src="{ASSETS_FROM_PAGE}/seo.js" defer></script>
</body>
</html>
"""
    return html_out, body_words


def render_hub() -> str:
    by_cat = {}
    for p in PAGES:
        by_cat.setdefault(p["category"], []).append(p)

    sections = []
    for cat_id, cat_name in CATEGORIES.items():
        pages = by_cat.get(cat_id, [])
        if not pages:
            continue
        cards = []
        for p in pages:
            cards.append(
                f'<a class="hub-card" href="./{esc(p["slug"])}/" id="{esc(p["slug"])}">'
                f'<strong>{esc(p["title"])}</strong>'
                f'<span>{esc(p["lead"][:140])}…</span></a>'
            )
        sections.append(
            f'<h2 class="hub-cat" id="{esc(cat_id)}">{esc(cat_name)}</h2>'
            f'<div class="hub-grid">{"".join(cards)}</div>'
        )

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SEO-материалы AngelGranit Алматы</title>
  <meta name="description" content="Справочник AngelGranit: ритуальные услуги, памятники, благоустройство, гайды и районы Алматы. 50 полезных страниц." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{abs_url()}" />
  <meta property="og:title" content="SEO-материалы AngelGranit Алматы" />
  <meta property="og:description" content="Ритуальные услуги, памятники и справочник по Алматы — AngelGranit." />
  <meta property="og:url" content="{abs_url()}" />
  <meta property="og:image" content="{BASE}/images/hero-angelgranit.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preload" href="./assets/seo.css" as="style" />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="./assets/seo.css" />
</head>
<body>
  <header class="nav">
    <a class="nav__brand" href="../"><strong>AngelGranit</strong><span>AG</span></a>
    <div class="nav__actions">
      <a class="btn btn--ghost" href="../">На главную</a>
      <a class="btn btn--gold" href="tel:{PHONE_TEL}">Позвонить</a>
      <a class="btn btn--wa" href="https://wa.me/77010567667" target="_blank" rel="noopener noreferrer">WhatsApp</a>
    </div>
  </header>
  <main class="wrap wrap--wide">
    <header class="hero">
      <p class="hero__kicker">Справочник · 50 страниц</p>
      <h1>Полезные материалы AngelGranit</h1>
      <p class="hero__lead">Ритуальные услуги, памятники, благоустройство могил, пошаговые гайды и страницы по районам Алматы. Белый SEO-контент для семей, которым нужна ясность.</p>
      <div class="hero__cta">
        <a class="btn btn--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
        <a class="btn btn--ghost" href="../">Вернуться на главную</a>
      </div>
    </header>
    {''.join(sections)}
  </main>
  <footer class="footer">
    <strong>AngelGranit</strong>
    {AGENT} · {esc(ADDRESS)} · <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
  </footer>
</body>
</html>
"""


def write_sitemap() -> None:
    urls = [
        (f"{BASE}/", "1.0", "weekly"),
        (abs_url(), "0.9", "weekly"),
    ]
    for p in PAGES:
        priority = "0.8"
        if p["slug"] in ("ritualnye-uslugi-almaty", "granitnye-pamyatniki", "katafalk-almaty", "kontakty", "faq"):
            priority = "0.9"
        urls.append((abs_url(p["slug"]), priority, "monthly"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, priority, freq in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    assert len(PAGES) == 50, len(PAGES)
    SEO_DIR.mkdir(parents=True, exist_ok=True)
    (SEO_DIR / "assets").mkdir(parents=True, exist_ok=True)

    low = []
    for page in PAGES:
        out_dir = SEO_DIR / page["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        html_out, words = render_page(page)
        (out_dir / "index.html").write_text(html_out, encoding="utf-8")
        status = "OK" if words >= 1200 else "LOW"
        if words < 1200:
            low.append((page["slug"], words))
        print(f"[{status}] {page['slug']}: {words} words, title={len(page['title'])} desc={len(page['description'])}")

    (SEO_DIR / "index.html").write_text(render_hub(), encoding="utf-8")
    write_sitemap()
    print(f"Hub + sitemap written. Pages: {len(PAGES)}")
    if low:
        print("WARNING low word count:")
        for slug, w in low:
            print(f"  - {slug}: {w}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
