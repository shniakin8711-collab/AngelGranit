# -*- coding: utf-8 -*-
"""Inject homepage SEO updates and generate pillar pages."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
ARTICLE = Path(__file__).with_name("home_seo_article.html")

META_DESC = (
    "Ритуальные услуги в Алматы круглосуточно. "
    "Организация похорон, катафалк, памятники, оформление документов, перевозка. "
    "Помощь семье 24/7 — AngelGranit."
)

CSS_BLOCK = """
    .seo-longform {
      padding: 4.5rem 0 3rem;
      border-top: 1px solid rgba(212, 175, 87, 0.18);
      background:
        radial-gradient(ellipse 70% 50% at 10% 0%, rgba(212, 175, 87, 0.07), transparent 55%),
        linear-gradient(180deg, rgba(8, 8, 8, 0.4), transparent 40%);
    }
    .seo-longform__body {
      max-width: 46rem;
      color: rgba(245, 240, 230, 0.86);
      font-size: 1.02rem;
      line-height: 1.75;
    }
    .seo-longform__body h3 {
      margin: 2rem 0 0.75rem;
      font-family: Cinzel, Georgia, serif;
      font-size: clamp(1.15rem, 2vw, 1.45rem);
      color: #d4af57;
      font-weight: 600;
    }
    .seo-longform__body p,
    .seo-longform__body li { margin: 0 0 1rem; }
    .seo-longform__body a {
      color: #e8d5a3;
      text-decoration: underline;
      text-underline-offset: 0.18em;
    }
    .seo-longform__body ol { padding-left: 1.25rem; margin: 0 0 1.25rem; }
    .seo-longform__links {
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      margin-top: 2rem;
      max-width: 52rem;
    }
    .seo-longform__links a {
      display: inline-block;
      padding: 0.45rem 0.8rem;
      border: 1px solid rgba(212, 175, 87, 0.35);
      color: #f5f0e6;
      text-decoration: none;
      font-size: 0.9rem;
    }
    .seo-longform__links a:hover {
      border-color: #d4af57;
      color: #d4af57;
    }
    .hero h1.hero__title {
      margin: 0 0 0.85rem;
      font-family: Cinzel, Georgia, serif;
      font-size: clamp(1.55rem, 3.6vw, 2.55rem);
      line-height: 1.15;
      letter-spacing: 0.02em;
      color: #f7efd8;
      text-shadow: 0 2px 18px rgba(0, 0, 0, 0.45);
      font-weight: 600;
    }
"""


def patch_index() -> None:
    html = INDEX.read_text(encoding="utf-8")

    html = re.sub(
        r'<meta name="description" content="[^"]*" />',
        f'<meta name="description" content="{META_DESC}" />',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*" />',
        f'<meta property="og:description" content="{META_DESC}" />',
        html,
        count=1,
    )

    # Schema: FuneralHome -> LocalBusiness + FuneralHome, add Organization, strengthen keywords
    html = html.replace(
        '"@type": "FuneralHome",\n        "@id": "https://shniakin8711-collab.github.io/AngelGranit/#business",',
        '"@type": ["LocalBusiness", "FuneralHome"],\n        "@id": "https://shniakin8711-collab.github.io/AngelGranit/#business",',
        1,
    )
    if '"@type": "Organization"' not in html:
        org = """      {
        "@type": "Organization",
        "@id": "https://shniakin8711-collab.github.io/AngelGranit/#organization",
        "name": "AngelGranit",
        "url": "https://shniakin8711-collab.github.io/AngelGranit/",
        "logo": "https://shniakin8711-collab.github.io/AngelGranit/images/hero-angelgranit.png",
        "telephone": "+77010567667",
        "sameAs": [
          "https://www.youtube.com/@Blackurbanfpv",
          "https://www.youtube.com/@AngelGranit"
        ]
      },
"""
        html = html.replace(
            '    "@graph": [\n      {\n        "@type": "WebSite",',
            '    "@graph": [\n' + org + '      {\n        "@type": "WebSite",',
            1,
        )
        html = html.replace(
            '"publisher": { "@id": "https://shniakin8711-collab.github.io/AngelGranit/#business" }',
            '"publisher": { "@id": "https://shniakin8711-collab.github.io/AngelGranit/#organization" }',
            1,
        )

    html = html.replace(
        '"description": "Ритуальные услуги Алматы, памятники из гранита, катафалк Алматы 24/7",\n'
        '        "inLanguage": ["ru-KZ", "kk-KZ"],\n'
        '        "keywords": "ритуальные услуги алматы, памятники алматы, катафалк алматы",',
        '"description": "Ритуальные услуги Алматы 24/7: организация похорон, катафалк, памятники",\n'
        '        "inLanguage": ["ru-KZ", "kk-KZ"],\n'
        '        "keywords": "ритуальные услуги алматы, организация похорон алматы, похоронное бюро алматы",',
        1,
    )

    # CSS
    if ".seo-longform" not in html:
        html = html.replace("    .seo-hub {", CSS_BLOCK + "\n    .seo-hub {", 1)

    # Hero H1 + content (keep visual design; make H1 visible but matching style)
    old_hero = """  <section class="hero" id="top" aria-label="AngelGranit — православные памятники">
    <div class="hero__media">
      <img src="images/hero-angelgranit.png" alt="AngelGranit — православные памятники по всем канонам. Алматы, +7 701 056 7667" width="1024" height="408" decoding="async" fetchpriority="high" />
    </div>
    <div class="hero__veil" aria-hidden="true"></div>
    <div class="hero__content">
      <h1 class="visually-hidden">AngelGranit — православные памятники и ритуальные услуги в Алматы</h1>
      <p class="hero__lead">Православные памятники и ритуальные услуги в Алматы — память, достойная вечности.</p>
      <div class="hero__actions">
        <a class="btn btn--red" href="tel:+77010567667">Позвонить 24/7</a>
        <a class="btn btn--ghost" id="link-wa-hero" href="#" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <a class="btn btn--ghost" href="#monuments">Памятники</a>
        <a class="btn btn--ghost" href="#packages">Ритуал</a>
        <a class="btn btn--ghost" href="#youtube">Видео</a>
      </div>
    </div>
  </section>"""

    new_hero = """  <section class="hero" id="top" aria-label="Ритуальные услуги в Алматы — AngelGranit">
    <div class="hero__media">
      <img src="images/hero-angelgranit.png" alt="Ритуальные услуги Алматы 24/7 — организация похорон AngelGranit" width="1024" height="408" decoding="async" fetchpriority="high" />
    </div>
    <div class="hero__veil" aria-hidden="true"></div>
    <div class="hero__content">
      <h1 class="hero__title">Ритуальные услуги в Алматы</h1>
      <p class="hero__lead">Организация похорон, катафалк, памятники и помощь семье круглосуточно — AngelGranit.</p>
      <div class="hero__actions">
        <a class="btn btn--red" href="tel:+77010567667">Позвонить 24/7</a>
        <a class="btn btn--ghost" id="link-wa-hero" href="#" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <a class="btn btn--ghost" href="#packages">Ритуал</a>
        <a class="btn btn--ghost" href="#seo-ritualnye-uslugi">Подробнее</a>
        <a class="btn btn--ghost" href="#monuments">Памятники</a>
      </div>
    </div>
  </section>"""

    if old_hero in html:
        html = html.replace(old_hero, new_hero, 1)
    else:
        html = re.sub(
            r'<h1 class="visually-hidden">[^<]*</h1>',
            '<h1 class="hero__title">Ритуальные услуги в Алматы</h1>',
            html,
            count=1,
        )

    html = html.replace(
        '<span>направление: <strong>памятники · ритуал</strong></span>',
        '<span>направление: <strong>ритуальные услуги · Алматы</strong></span>',
        1,
    )

    # Image alts emphasizing ritual services
    replacements = [
        (
            'alt="Ритуальные услуги AngelGranit"',
            'alt="Ритуальные услуги Алматы — организация похорон AngelGranit"',
        ),
        (
            'alt="Гранитные памятники AngelGranit"',
            'alt="Гранитные памятники Алматы как часть ритуальных услуг AngelGranit"',
        ),
        (
            'alt="Чёрный катафалк"',
            'alt="Катафалк Алматы — ритуальный транспорт AngelGranit"',
        ),
        (
            'alt="Памятник из чёрного гранита"',
            'alt="Памятники Алматы из гранита — AngelGranit"',
        ),
        (
            'alt="Минимальный комплекс — 150 000 ₸"',
            'alt="Ритуальные услуги Алматы — минимальный комплекс 150 000 ₸"',
        ),
        (
            'alt="Прощальный зал — 150 000 ₸"',
            'alt="Организация похорон Алматы — прощальный зал 150 000 ₸"',
        ),
        (
            'alt="Стандарт комплекс — 400 000 ₸"',
            'alt="Похоронное бюро Алматы — стандарт комплекс 400 000 ₸"',
        ),
        (
            'alt="Комплекс элит — 800 000 ₸"',
            'alt="Ритуальные услуги Алматы — комплекс элит 800 000 ₸"',
        ),
    ]
    for a, b in replacements:
        html = html.replace(a, b)

    # Fix missing width/height on funeral service image if needed
    html = html.replace(
        '<img src="images/service-funeral.png" alt="Ритуальные услуги Алматы — организация похорон AngelGranit" loading="lazy" decoding="async" />',
        '<img src="images/service-funeral.png" alt="Ритуальные услуги Алматы — организация похорон AngelGranit" width="1200" height="800" loading="lazy" decoding="async" />',
        1,
    )

    # Hub links to root pillars
    old_hub = """      <div class="seo-hub__grid reveal">
        <a href="seo/ritualnye-uslugi-almaty/"><strong>Ритуальные услуги</strong><span>Организация похорон 24/7 в Алматы</span></a>
        <a href="seo/organizaciya-pohoron-almaty/"><strong>Организация похорон</strong><span>Пошаговый план под ключ</span></a>
        <a href="seo/katafalk-almaty/"><strong>Катафалк Алматы</strong><span>Ритуальный транспорт и маршруты</span></a>
        <a href="seo/granitnye-pamyatniki/"><strong>Гранитные памятники</strong><span>Изготовление и установка</span></a>
        <a href="seo/chto-delat-esli-umer-chelovek/"><strong>Если умер человек</strong><span>Памятка первых действий</span></a>
        <a href="seo/stoimost-pohoron/"><strong>Стоимость похорон</strong><span>Из чего складывается смета</span></a>
        <a href="seo/ritualnye-uslugi-zhetysuskij-rajon/"><strong>Жетысуский район</strong><span>Выезд агента и локальная помощь</span></a>
        <a href="seo/faq/"><strong>FAQ</strong><span>Частые вопросы о услугах и ценах</span></a>
      </div>
      <div class="seo-hub__more reveal">
        <a class="btn btn--red" href="seo/">Все 50 материалов</a>
        <a class="btn btn--ghost" href="seo/kontakty/">Контакты</a>
      </div>"""

    new_hub = """      <div class="seo-hub__grid reveal">
        <a href="ritualnye-uslugi-almaty/"><strong>Ритуальные услуги</strong><span>Главный раздел · Алматы 24/7</span></a>
        <a href="organizaciya-pohoron-almaty/"><strong>Организация похорон</strong><span>Пошаговый план под ключ</span></a>
        <a href="katafalk-almaty/"><strong>Катафалк Алматы</strong><span>Ритуальный транспорт</span></a>
        <a href="ritualny-agent-almaty/"><strong>Ритуальный агент</strong><span>Выезд и координация 24/7</span></a>
        <a href="ritualnye-prinadlezhnosti-almaty/"><strong>Принадлежности</strong><span>Гробы, венки, кресты</span></a>
        <a href="pamyatniki-almaty/"><strong>Памятники</strong><span>Заказ и установка</span></a>
        <a href="granitnye-pamyatniki-almaty/"><strong>Гранитные памятники</strong><span>Изготовление и монтаж</span></a>
        <a href="memorialnye-kompleksy-almaty/"><strong>Мемориальные комплексы</strong><span>Проект под ключ</span></a>
      </div>
      <div class="seo-hub__more reveal">
        <a class="btn btn--red" href="ritualnye-uslugi-almaty/">Ритуальные услуги Алматы</a>
        <a class="btn btn--ghost" href="seo/">Справочник 50 материалов</a>
        <a class="btn btn--ghost" href="seo/kontakty/">Контакты</a>
      </div>"""

    if old_hub in html:
        html = html.replace(old_hub, new_hub, 1)

    html = html.replace(
        "Православные памятники · ритуальные услуги · Алматы<br />",
        "Ритуальные услуги Алматы · памятники · катафалк<br />",
        1,
    )
    html = html.replace(
        '<a href="seo/">Справочник SEO-страниц</a> · <a href="seo/faq/">FAQ</a> · <a href="sitemap.xml">Sitemap</a>',
        '<a href="ritualnye-uslugi-almaty/">Ритуальные услуги</a> · <a href="seo/">Справочник</a> · <a href="seo/faq/">FAQ</a> · <a href="sitemap.xml">Sitemap</a>',
        1,
    )

    # Inject long SEO article before seo-hub
    article = ARTICLE.read_text(encoding="utf-8").strip()
    if 'id="seo-ritualnye-uslugi"' in html:
        html = re.sub(
            r'<section class="seo-longform" id="seo-ritualnye-uslugi"[\s\S]*?</section>\s*',
            article + "\n\n  ",
            html,
            count=1,
        )
    else:
        html = html.replace(
            '  <section class="seo-hub" id="seo-guides"',
            article + "\n\n  <section class=\"seo-hub\" id=\"seo-guides\"",
            1,
        )

    # Nav link to ritual services
    if 'href="ritualnye-uslugi-almaty/"' not in html.split("</header>", 1)[0]:
        html = html.replace(
            '<a href="seo/">справочник</a>',
            '<a href="ritualnye-uslugi-almaty/">ритуал</a>\n      <a href="seo/">справочник</a>',
            1,
        )

    INDEX.write_text(html, encoding="utf-8", newline="\n")
    plain = re.sub(r"<[^>]+>", " ", article)
    words = len(re.findall(r"\w+", plain, flags=re.UNICODE))
    print(f"index patched; meta desc={len(META_DESC)}; article words~={words}")


def patch_robots() -> None:
    text = """User-agent: *
Allow: /
Allow: /seo/
Allow: /ritualnye-uslugi-almaty/
Allow: /organizaciya-pohoron-almaty/
Allow: /katafalk-almaty/
Allow: /pamyatniki-almaty/
Allow: /granitnye-pamyatniki-almaty/
Allow: /memorialnye-kompleksy-almaty/
Allow: /ritualny-agent-almaty/
Allow: /ritualnye-prinadlezhnosti-almaty/

Sitemap: https://shniakin8711-collab.github.io/AngelGranit/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(text, encoding="utf-8", newline="\n")
    print("robots.txt updated")


def main() -> None:
    assert 150 <= len(META_DESC) <= 160, len(META_DESC)
    patch_index()
    patch_robots()
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("build_pillars.py"))], cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(r.returncode)
    print("done")


if __name__ == "__main__":
    main()
