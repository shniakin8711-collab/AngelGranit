# -*- coding: utf-8 -*-
"""
Build multipage architecture pages from the AngelGranit plan:
  ceny/, nashi-raboty/, otzyvy/, faq/, uslugi/ritualny-agent/,
  stati/{5 key articles}/
Uses existing design tokens via assets/site/*.css — no redesign.
"""
from __future__ import annotations

import json
import re
from datetime import date
from html import escape
from pathlib import Path

from seo_head import icon_links, social_meta

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://shniakin8711-collab.github.io/AngelGranit"
PHONE = "+7 701 056 7667"
PHONE_TEL = "+77010567667"
ADDRESS = "ул. Осетинская, 5а"
AGENT = "Александр"
TODAY = date.today().isoformat()
IMG = f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp"


def nav_html(depth: int) -> str:
    p = "../" * depth
    return f"""  <header class="site-nav" data-site-nav>
    <a class="site-nav__brand" href="{p}"><strong>AngelGranit</strong><span>AG</span></a>
    <button class="site-nav__toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav-menu">Меню</button>
    <ul class="site-nav__menu" id="site-nav-menu">
      <li class="site-nav__item" data-dropdown>
        <button type="button" aria-expanded="false">Услуги</button>
        <div class="site-nav__dropdown">
          <a href="{p}uslugi/">Все услуги</a>
          <a href="{p}uslugi/ritualnye-uslugi/">Ритуальные услуги</a>
          <a href="{p}uslugi/organizaciya-pohoron/">Организация похорон</a>
          <a href="{p}uslugi/katafalk/">Катафалк</a>
          <a href="{p}uslugi/ritualny-agent/">Ритуальный агент</a>
          <a href="{p}uslugi/ritualnye-prinadlezhnosti/">Принадлежности</a>
          <a href="{p}uslugi/pamyatniki/">Памятники</a>
          <a href="{p}uslugi/granitnye-pamyatniki/">Гранитные памятники</a>
          <a href="{p}uslugi/memorialnye-kompleksy/">Мемориальные комплексы</a>
        </div>
      </li>
      <li><a href="{p}ceny/">Цены</a></li>
      <li><a href="{p}nashi-raboty/">Наши работы</a></li>
      <li class="site-nav__item" data-dropdown>
        <button type="button" aria-expanded="false">Статьи</button>
        <div class="site-nav__dropdown">
          <a href="{p}stati/">Все статьи</a>
          <a href="{p}stati/chto-delat-esli-umer-chelovek/">Что делать если умер человек</a>
          <a href="{p}stati/kak-organizovat-pohorony/">Как организовать похороны</a>
          <a href="{p}stati/dokumenty-posle-smerti/">Документы после смерти</a>
          <a href="{p}stati/stoimost-pohoron/">Стоимость похорон</a>
          <a href="{p}stati/kogda-ustanavlivat-pamyatnik/">Когда устанавливать памятник</a>
        </div>
      </li>
      <li><a href="{p}otzyvy/">Отзывы</a></li>
      <li><a href="{p}faq/">FAQ</a></li>
      <li><a href="{p}kontakty/">Контакты</a></li>
    </ul>
    <a class="site-nav__call" href="tel:{PHONE_TEL}">Позвонить 24/7</a>
  </header>"""


def footer_html(depth: int) -> str:
    p = "../" * depth
    return f"""  <footer class="page-footer">
    <strong>AngelGranit</strong>
    {AGENT} · {ADDRESS} · <a href="tel:{PHONE_TEL}">{PHONE}</a>
    <ul class="page-footer-links">
      <li><a href="{p}">Главная</a></li>
      <li><a href="{p}uslugi/">Услуги</a></li>
      <li><a href="{p}ceny/">Цены</a></li>
      <li><a href="{p}nashi-raboty/">Работы</a></li>
      <li><a href="{p}stati/">Статьи</a></li>
      <li><a href="{p}otzyvy/">Отзывы</a></li>
      <li><a href="{p}faq/">FAQ</a></li>
      <li><a href="{p}kontakty/">Контакты</a></li>
    </ul>
  </footer>
  <script src="{p}assets/site/nav.js" defer></script>"""


def page_shell(
    *,
    depth: int,
    title: str,
    desc: str,
    canonical: str,
    h1: str,
    lead: str,
    breadcrumbs: list[tuple[str, str]],
    body: str,
    schema: dict | list,
    og_type: str = "website",
    image: str = IMG,
) -> str:
    p = "../" * depth
    crumbs = []
    for href, label in breadcrumbs:
        if href:
            crumbs.append(f'<li><a href="{escape(href)}">{escape(label)}</a></li>')
        else:
            crumbs.append(f'<li aria-current="page">{escape(label)}</li>')
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="canonical" href="{canonical}" />
{icon_links(p)}
{social_meta(title=title, desc=desc, url=canonical, image=image, og_type=og_type)}
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{p}seo/assets/seo.css" />
  <link rel="stylesheet" href="{p}assets/site/nav.css" />
  <link rel="stylesheet" href="{p}assets/site/page.css" />
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>
  <a class="skip-link" href="#main-content">Перейти к содержанию</a>
{nav_html(depth)}
  <main id="main-content" class="page-main">
    <div class="page-wrap--wide">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          {''.join(crumbs)}
        </ol>
      </nav>
      <header class="page-hero">
        <h1>{escape(h1)}</h1>
        <p class="lead">{escape(lead)}</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {PHONE}</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn-site btn-site--ghost" href="{p}kontakty/">Контакты</a>
        </div>
      </header>
{body}
    </div>
  </main>
{footer_html(depth)}
</body>
</html>
"""


def breadcrumb_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (url, name) in enumerate(items)
        ],
    }


def org_graph() -> list[dict]:
    return [
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
            "openingHours": "Mo-Su 00:00-24:00",
        },
    ]


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8", newline="\n")
    print("wrote", path.relative_to(ROOT))


# ── pages ────────────────────────────────────────────────────────────────────

def build_ceny() -> None:
    url = f"{BASE}/ceny/"
    body = f"""
      <article class="page-article">
        <h2>Пакеты ритуальных услуг</h2>
        <p>Ниже — ориентиры стоимости комплексов AngelGranit в Алматы. Точная смета зависит от района, маршрута и состава. Актуальные карточки пакетов также на <a href="../#packages">главной</a>.</p>
        <div class="hub-grid">
          <a class="hub-card" href="../#packages"><strong>Минимальный — от 150 000 ₸</strong><span>Базовый набор для спокойной организации без лишнего.</span></a>
          <a class="hub-card" href="../#packages"><strong>Прощальный зал — от 150 000 ₸</strong><span>Организация прощания в зале с координацией.</span></a>
          <a class="hub-card" href="../#packages"><strong>Стандарт — 400 000 ₸</strong><span>Расширенный комплекс: транспорт, принадлежности, сопровождение.</span></a>
          <a class="hub-card" href="../#packages"><strong>Элит — 800 000 ₸</strong><span>Полный сценарий с повышенным уровнем оформления.</span></a>
        </div>
        <h2>Как понять бюджет</h2>
        <p>Обязательное: документы, транспорт, подготовка. Желательное: зал, расширенное оформление, памятник позже. Можно начать с минимума и добавить опции.</p>
        <p>Считайте смету в <a href="../#calc">калькуляторе</a> на главной или позвоните агенту {AGENT}: {PHONE}.</p>
        <h2>Связанные страницы</h2>
        <div class="related-grid">
          <a href="../uslugi/ritualnye-uslugi/"><strong>Ритуальные услуги</strong><span>Каталог</span></a>
          <a href="../uslugi/pohorony-pod-klyuch/"><strong>Похороны под ключ</strong><span>Услуга</span></a>
          <a href="../stati/stoimost-pohoron/"><strong>Стоимость похорон</strong><span>Статья</span></a>
          <a href="../tseny-ritualnyh-uslug-almaty/"><strong>Цены — подробный гид</strong><span>Pillar</span></a>
        </div>
      </article>
"""
    schema = {
        "@context": "https://schema.org",
        "@graph": org_graph()
        + [
            {
                "@type": "WebPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": "Цены на ритуальные услуги в Алматы",
                "description": "Ориентиры пакетов AngelGranit: от 150 000 ₸.",
            },
            breadcrumb_schema([(f"{BASE}/", "Главная"), (url, "Цены")]),
        ],
    }
    write(
        ROOT / "ceny" / "index.html",
        page_shell(
            depth=1,
            title="Цены на ритуальные услуги в Алматы | AngelGranit",
            desc="Цены ритуальных услуг Алматы: пакеты от 150 000 ₸, стандарт 400 000 ₸, элит 800 000 ₸. Смета 24/7 — AngelGranit.",
            canonical=url,
            h1="Цены на ритуальные услуги в Алматы",
            lead="Прозрачные ориентиры по пакетам. Точную смету озвучим по составу — без навязанных опций.",
            breadcrumbs=[("../", "Главная"), ("", "Цены")],
            body=body,
            schema=schema,
            image=f"{BASE}/images/package-standard.webp",
        ),
    )


def build_nashi_raboty() -> None:
    url = f"{BASE}/nashi-raboty/"
    imgs = [
        ("showcase-monument.webp", "Гранитный памятник — работа AngelGranit", "../uslugi/granitnye-pamyatniki/"),
        ("showcase-hearse.webp", "Катафалк AngelGranit", "../uslugi/katafalk/"),
        ("seo/memorialny-kompleks-chernyj-granit.webp", "Мемориальный комплекс", "../uslugi/memorialnye-kompleksy/"),
        ("seo/hudozhestvennaya-gravirovka.webp", "Художественная гравировка", "../uslugi/gravirovka/"),
        ("seo/pamyatnik-s-blagoustrojstvom.webp", "Памятник с благоустройством", "../uslugi/blagoustrojstvo-mogil/"),
        ("seo/granitnaya-masterskaya.webp", "Гранитная мастерская", "../#production"),
    ]
    cards = []
    for src, alt, href in imgs:
        cards.append(
            f'<a class="hub-card" href="{href}"><img src="../images/{src}" alt="{escape(alt)}" width="800" height="600" loading="lazy" decoding="async" style="width:100%;height:auto;border-radius:4px;margin-bottom:0.65rem" /><strong>{escape(alt)}</strong><span>Смотреть услугу</span></a>'
        )
    body = f"""
      <article class="page-article">
        <h2>Примеры работ</h2>
        <p>Фрагменты реальных проектов: памятники, транспорт, комплексы и производство. Полная лента также на <a href="../#works">главной</a>.</p>
        <div class="hub-grid">{''.join(cards)}</div>
        <h2>Производство</h2>
        <p>Камень обрабатываем с контролем макета и монтажа. Подробнее о цикле — в блоке <a href="../#production">производство</a> и на страницах <a href="../uslugi/pamyatniki/">памятников</a>.</p>
      </article>
"""
    schema = {
        "@context": "https://schema.org",
        "@graph": org_graph()
        + [
            {"@type": "CollectionPage", "url": url, "name": "Наши работы AngelGranit"},
            breadcrumb_schema([(f"{BASE}/", "Главная"), (url, "Наши работы")]),
        ],
    }
    write(
        ROOT / "nashi-raboty" / "index.html",
        page_shell(
            depth=1,
            title="Наши работы — памятники и ритуальные услуги Алматы | AngelGranit",
            desc="Галерея работ AngelGranit в Алматы: гранитные памятники, катафалк, мемориальные комплексы и благоустройство. Примеры на сайте.",
            canonical=url,
            h1="Наши работы",
            lead="Памятники, транспорт и комплексы — чтобы было проще понять уровень исполнения до звонка.",
            breadcrumbs=[("../", "Главная"), ("", "Наши работы")],
            body=body,
            schema=schema,
            image=f"{BASE}/images/showcase-monument.webp",
        ),
    )


def build_otzyvy() -> None:
    url = f"{BASE}/otzyvy/"
    reviews = [
        ("Елена", "Алмалинский район", "Ночью приняли звонок, спокойно объяснили порядок действий и прислали катафалк вовремя. Без лишней суеты и навязанных услуг."),
        ("Марат", "Бостандыкский район", "Заказывали гранитный памятник и гравировку. Эскиз согласовали быстро, установка на кладбище прошла аккуратно."),
        ("Семья Н.", "Каскелен", "Нужен был только транспорт и документы. Всё прозрачно по цене, агент на связи до самого захоронения."),
        ("Айгуль", "Ауэзовский район", "Помогли организовать прощание под ключ. Один координатор — меньше хаоса для семьи."),
        ("Игорь", "Медеуский район", "Отдельно заказали венки и катафалк. Подача вовремя, маршрут согласовали заранее."),
    ]
    cards = "\n".join(
        f'<article class="hub-card"><strong>{escape(name)}</strong><span>{escape(place)}</span><p style="margin:0.75rem 0 0;color:#ece8e0;line-height:1.65">{escape(text)}</p></article>'
        for name, place, text in reviews
    )
    body = f"""
      <article class="page-article">
        <h2>Отзывы семей</h2>
        <p>Мы публикуем короткие отзывы о реальных обращениях. Больше историй — в блоке <a href="../#reviews">отзывов на главной</a>.</p>
        <div class="hub-grid">{cards}</div>
        <h2>Хотите оставить отзыв?</h2>
        <p>Напишите в WhatsApp или позвоните {PHONE}. Агент {AGENT} поможет и с организацией, и с памятником.</p>
        <div class="related-grid">
          <a href="../uslugi/ritualnye-uslugi/"><strong>Ритуальные услуги</strong><span>Услуги</span></a>
          <a href="../nashi-raboty/"><strong>Наши работы</strong><span>Галерея</span></a>
          <a href="../kontakty/"><strong>Контакты</strong><span>Связаться</span></a>
        </div>
      </article>
"""
    review_entities = [
        {
            "@type": "Review",
            "author": {"@type": "Person", "name": name},
            "reviewBody": text,
            "itemReviewed": {"@id": f"{BASE}/#business"},
        }
        for name, _place, text in reviews[:3]
    ]
    schema = {
        "@context": "https://schema.org",
        "@graph": org_graph()
        + [
            {"@type": "WebPage", "url": url, "name": "Отзывы AngelGranit"},
            breadcrumb_schema([(f"{BASE}/", "Главная"), (url, "Отзывы")]),
        ]
        + review_entities,
    }
    write(
        ROOT / "otzyvy" / "index.html",
        page_shell(
            depth=1,
            title="Отзывы о ритуальных услугах AngelGranit в Алматы",
            desc="Отзывы семей о ритуальных услугах и памятниках AngelGranit в Алматы. Реальные обращения, катафалк, памятники, организация 24/7.",
            canonical=url,
            h1="Отзывы",
            lead="Слова семей, которым мы помогли организовать прощание и оформить место памяти.",
            breadcrumbs=[("../", "Главная"), ("", "Отзывы")],
            body=body,
            schema=schema,
        ),
    )


def build_faq() -> None:
    url = f"{BASE}/faq/"
    faqs = [
        ("Как быстро вы приезжаете в Алматы?", f"Агент и транспорт выезжают круглосуточно. Ориентир по району уточним при звонке {PHONE}."),
        ("Сколько стоят ритуальные услуги?", "Минимальный комплекс от 150 000 ₸, стандарт — 400 000 ₸, элит — 800 000 ₸. Смотрите страницу цен."),
        ("Можно заказать только катафалк или памятник?", "Да. Полный пакет не обязателен — заказывайте только нужные позиции."),
        ("Работаете ли ночью и в праздники?", "Да, AngelGranit принимает заявки 24/7."),
        ("Где ваш офис?", f"Офис: {ADDRESS}, Алматы. Возможен выезд агента."),
        ("Как вызвать ритуального агента?", f"Позвоните {PHONE} или напишите в WhatsApp — агент {AGENT} даст порядок действий."),
        ("Помогаете с документами?", "Да, подскажем последовательность и что подготовить. См. статьи о документах."),
        ("Делаете ли памятники после похорон?", "Да, гранитные памятники и комплексы можно заказать отдельно позже."),
        ("Ездите ли в область?", "Да, по согласованию: Каскелен, Талгар и другие населённые пункты."),
        ("Какие гарантии на памятник?", "Условия по камню и монтажу фиксируем при заказе — обсудим на консультации."),
        ("Можно ли получить смету в WhatsApp?", "Да, пришлём понятный список позиций без давления."),
        ("Где смотреть работы?", "На странице «Наши работы» и в блоке работ на главной."),
    ]
    details = "\n".join(
        f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faqs
    )
    body = f"""
      <section class="page-faq" id="faq">
        <h2>Ответы на частые вопросы</h2>
        {details}
      </section>
      <div class="related-grid" style="margin-top:1.5rem">
        <a href="../ceny/"><strong>Цены</strong><span>Пакеты</span></a>
        <a href="../uslugi/"><strong>Услуги</strong><span>Каталог</span></a>
        <a href="../stati/"><strong>Статьи</strong><span>Инструкции</span></a>
        <a href="../kontakty/"><strong>Контакты</strong><span>Связаться</span></a>
      </div>
"""
    schema = {
        "@context": "https://schema.org",
        "@graph": org_graph()
        + [
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ]},
            breadcrumb_schema([(f"{BASE}/", "Главная"), (url, "FAQ")]),
        ],
    }
    write(
        ROOT / "faq" / "index.html",
        page_shell(
            depth=1,
            title="FAQ — частые вопросы о ритуальных услугах Алматы | AngelGranit",
            desc="FAQ AngelGranit: цены, катафалк, памятники, выезд 24/7, документы. Короткие ответы для семей в Алматы.",
            canonical=url,
            h1="Частые вопросы",
            lead="Короткие ответы без воды. Если ситуации нет в списке — позвоните, разберём по шагам.",
            breadcrumbs=[("../", "Главная"), ("", "FAQ")],
            body=body,
            schema=schema,
        ),
    )


def build_ritualny_agent() -> None:
    url = f"{BASE}/uslugi/ritualny-agent/"
    body = f"""
      <figure class="page-figure">
        <img src="../../images/seo/ritualny-agent-konsultaciya.webp" alt="Ритуальный агент AngelGranit — консультация" width="1200" height="800" loading="lazy" decoding="async" />
      </figure>
      <article class="page-article">
        <h2>Когда нужен ритуальный агент</h2>
        <p>Ритуальный агент нужен, когда семье требуется спокойный порядок действий: кого вызвать, какие документы собрать, как согласовать транспорт и прощание.</p>
        <p>Агент {AGENT} принимает звонки 24/7 по Алматы и области. Не «приходите завтра», а конкретные шаги в ближайшие часы.</p>
        <h2>Что делает агент</h2>
        <p>Уточняет обстоятельства, составляет понятный план, помогает с логистикой и сметой. Можно заказать полное сопровождение или только консультацию и отдельные услуги.</p>
        <h2>Подробный гид</h2>
        <p>Развёрнутый материал: <a href="../../ritualny-agent-almaty/">ритуальный агент Алматы</a>. Также смотрите <a href="../ritualnye-uslugi/">ритуальные услуги</a> и <a href="../organizaciya-pohoron/">организацию похорон</a>.</p>
      </article>
      <section class="page-faq">
        <h2>FAQ</h2>
        <details><summary>Как быстро связаться с агентом?</summary><p>Позвоните {PHONE} или напишите в WhatsApp — отвечаем круглосуточно.</p></details>
        <details><summary>Нужно ли приезжать в офис?</summary><p>Не обязательно. Многие вопросы решаются удалённо.</p></details>
        <details><summary>Можно ли только консультацию?</summary><p>Да. Полный пакет услуг не обязателен.</p></details>
      </section>
"""
    schema = {
        "@context": "https://schema.org",
        "@graph": org_graph()
        + [
            {
                "@type": "Service",
                "name": "Ритуальный агент в Алматы",
                "provider": {"@id": f"{BASE}/#business"},
                "areaServed": {"@type": "City", "name": "Алматы"},
                "url": url,
            },
            breadcrumb_schema([
                (f"{BASE}/", "Главная"),
                (f"{BASE}/uslugi/", "Услуги"),
                (url, "Ритуальный агент"),
            ]),
        ],
    }
    write(
        ROOT / "uslugi" / "ritualny-agent" / "index.html",
        page_shell(
            depth=2,
            title="Ритуальный агент в Алматы 24/7 | AngelGranit",
            desc="Вызов ритуального агента в Алматы круглосуточно. Агент Александр: план, документы, транспорт. Телефон +7 701 056 7667.",
            canonical=url,
            h1="Ритуальный агент в Алматы",
            lead="Один звонок — понятный порядок действий без давления и лишних опций.",
            breadcrumbs=[("../../", "Главная"), ("../", "Услуги"), ("", "Ритуальный агент")],
            body=body,
            schema=schema,
            image=f"{BASE}/images/seo/ritualny-agent-konsultaciya.webp",
        ),
    )


ARTICLES = [
    {
        "slug": "chto-delat-esli-umer-chelovek",
        "title": "Что делать если умер человек в Алматы | AngelGranit",
        "h1": "Что делать, если умер человек в Алматы",
        "desc": "Что делать, если умер человек в Алматы: первые часы, врачи, документы, морг, звонок агенту. Спокойная памятка AngelGranit 24/7.",
        "seo_old": "../seo/chto-delat-esli-umer-chelovek/",
        "sections": [
            ("Первые действия", [
                "Сохраняйте спокойствие и обеспечьте безопасность места. Если смерть дома и обстоятельства неясны — вызовите скорую и при необходимости полицию.",
                "Не перемещайте тело до указаний специалистов. Зафиксируйте время и контакты тех, кто рядом.",
            ]),
            ("Документы и морг", [
                "Далее оформляются медицинские документы и перевод в морг. Список бумаг зависит от места смерти — дома, в больнице или в другом городе.",
                "Агент поможет выстроить порядок, чтобы не ездить по кругу и не терять время.",
            ]),
            ("Когда звонить AngelGranit", [
                f"Позвоните {PHONE} в любой час: агент {AGENT} объяснит следующие шаги и что можно отложить.",
                "Параллельно можно открыть раздел статей «Первые шаги» и страницу ритуальных услуг.",
            ]),
        ],
    },
    {
        "slug": "kak-organizovat-pohorony",
        "title": "Как организовать похороны в Алматы | AngelGranit",
        "h1": "Как организовать похороны в Алматы",
        "desc": "Как организовать похороны в Алматы по шагам: дата, документы, транспорт, зал, кладбище. План от AngelGranit без хаоса.",
        "seo_old": "../seo/kak-organizovat-pohorony/",
        "sections": [
            ("Пошаговый план", [
                "Определите дату и формат прощания, круг участников и маршрут. Затем согласуйте транспорт и место церемонии.",
                "Параллельно решите вопрос принадлежностей и, при необходимости, зала или храма.",
            ]),
            ("Кто координирует", [
                "Один координатор снижает хаос. Ритуальный агент держит тайминг: подача катафалка, зал, кладбище.",
            ]),
            ("Бюджет", [
                "Сначала обязательное, затем желательное. Ориентиры пакетов — на странице цен; точную смету дадим по составу.",
            ]),
        ],
    },
    {
        "slug": "dokumenty-posle-smerti",
        "title": "Документы после смерти в Алматы | AngelGranit",
        "h1": "Документы после смерти в Алматы",
        "desc": "Документы после смерти в Алматы: свидетельство, справки, что проверить и куда обратиться. Памятка AngelGranit.",
        "seo_old": "../seo/dokumenty-posle-smerti/",
        "sections": [
            ("Базовый пакет", [
                "Обычно нужны медицинские документы о смерти и гербовое свидетельство. Количество копий зависит от банка, работодателя и кладбища.",
            ]),
            ("Типичные ошибки", [
                "Проверяйте ФИО, даты и печати. Ошибки лучше исправлять сразу, до ключевых обращений.",
            ]),
            ("Помощь агента", [
                f"AngelGranit подскажет последовательность. Звоните {PHONE} — разберём ваш случай без лишней бюрократии в голове.",
            ]),
        ],
    },
    {
        "slug": "stoimost-pohoron",
        "title": "Стоимость похорон в Алматы | AngelGranit",
        "h1": "Стоимость похорон в Алматы",
        "desc": "Стоимость похорон в Алматы: из чего складывается смета, пакеты от 150 000 ₸ и как снизить бюджет без потери достоинства.",
        "seo_old": "../seo/stoimost-pohoron/",
        "sections": [
            ("Из чего складывается цена", [
                "Транспорт, подготовка, принадлежности, зал, кладбище и координация. Памятник часто оплачивается отдельно позже.",
            ]),
            ("Ориентиры AngelGranit", [
                "Минимальный комплекс от 150 000 ₸, стандарт 400 000 ₸, элит 800 000 ₸. Актуальные пакеты — на странице цен и на главной.",
            ]),
            ("Как не переплатить", [
                "Сравнивайте состав, а не только цифру «от». Спросите, что входит и что оплачивается отдельно.",
            ]),
        ],
    },
    {
        "slug": "kogda-ustanavlivat-pamyatnik",
        "title": "Когда устанавливать памятник в Алматы | AngelGranit",
        "h1": "Когда устанавливать памятник в Алматы",
        "desc": "Когда ставить памятник после похорон в Алматы: грунт, сезон, фундамент и практичные сроки. Советы AngelGranit.",
        "seo_old": "../seo/kogda-ustanavlivat-pamyatnik/",
        "sections": [
            ("Сроки и грунт", [
                "Срок зависит от типа грунта, сезона и фундамента. Часто памятник ставят не в первые недели, а после усадки — но решение индивидуально.",
            ]),
            ("Что подготовить", [
                "Фото для портрета, тексты надписей, размеры участка и правила кладбища. Сначала эскиз, затем изготовление и монтаж.",
            ]),
            ("Связанные услуги", [
                "Смотрите памятники, гранитные памятники и благоустройство. Временный крест можно заменить позже.",
            ]),
        ],
    },
]


def build_articles() -> None:
    for art in ARTICLES:
        url = f"{BASE}/stati/{art['slug']}/"
        sections_html = []
        for h2, paras in art["sections"]:
            sections_html.append(f"<h2>{escape(h2)}</h2>")
            for para in paras:
                sections_html.append(f"<p>{escape(para)}</p>")
        body = f"""
      <article class="page-article">
        {''.join(sections_html)}
        <h2>Полезные ссылки</h2>
        <p>Материал в справочнике: <a href="{art['seo_old']}">версия в /seo/</a>. Услуги: <a href="../../uslugi/ritualnye-uslugi/">ритуальные услуги</a>, <a href="../../uslugi/organizaciya-pohoron/">организация похорон</a>, <a href="../../kontakty/">контакты</a>.</p>
      </article>
      <section>
        <h2>Похожие статьи</h2>
        <div class="related-grid">
          <a href="../chto-delat-esli-umer-chelovek/"><strong>Что делать если умер человек</strong><span>Статья</span></a>
          <a href="../kak-organizovat-pohorony/"><strong>Как организовать похороны</strong><span>Статья</span></a>
          <a href="../dokumenty-posle-smerti/"><strong>Документы после смерти</strong><span>Статья</span></a>
          <a href="../stoimost-pohoron/"><strong>Стоимость похорон</strong><span>Статья</span></a>
          <a href="../kogda-ustanavlivat-pamyatnik/"><strong>Когда устанавливать памятник</strong><span>Статья</span></a>
        </div>
      </section>
"""
        schema = {
            "@context": "https://schema.org",
            "@graph": org_graph()
            + [
                {
                    "@type": "Article",
                    "headline": art["h1"],
                    "description": art["desc"],
                    "url": url,
                    "author": {"@type": "Person", "name": AGENT},
                    "publisher": {"@id": f"{BASE}/#organization"},
                    "inLanguage": "ru-KZ",
                },
                breadcrumb_schema([
                    (f"{BASE}/", "Главная"),
                    (f"{BASE}/stati/", "Статьи"),
                    (url, art["h1"]),
                ]),
            ],
        }
        write(
            ROOT / "stati" / art["slug"] / "index.html",
            page_shell(
                depth=2,
                title=art["title"],
                desc=art["desc"],
                canonical=url,
                h1=art["h1"],
                lead="Практическая инструкция для семей в Алматы — без давления и лишней рекламы.",
                breadcrumbs=[("../../", "Главная"), ("../", "Статьи"), ("", art["h1"])],
                body=body,
                schema=schema,
                og_type="article",
            ),
        )


def patch_uslugi_hub_link() -> None:
    """Ensure uslugi hub lists ritualny-agent if missing."""
    p = ROOT / "uslugi" / "index.html"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    if "ritualny-agent" in t:
        return
    # insert a card near top of hub-grid if present
    card = '<a class="hub-card" href="ritualny-agent/"><strong>Ритуальный агент</strong><span>Вызов агента 24/7</span></a>\n'
    if "hub-grid" in t:
        t = t.replace('<div class="hub-grid">', '<div class="hub-grid">\n' + card, 1)
        p.write_text(t, encoding="utf-8", newline="\n")
        print("patched uslugi hub")


def patch_stati_hub_links() -> None:
    p = ROOT / "stati" / "index.html"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    block = """
      <h2>Ключевые статьи</h2>
      <div class="hub-grid">
        <a class="hub-card" href="chto-delat-esli-umer-chelovek/"><strong>Что делать если умер человек</strong><span>Первые шаги</span></a>
        <a class="hub-card" href="kak-organizovat-pohorony/"><strong>Как организовать похороны</strong><span>План</span></a>
        <a class="hub-card" href="dokumenty-posle-smerti/"><strong>Документы после смерти</strong><span>Бумаги</span></a>
        <a class="hub-card" href="stoimost-pohoron/"><strong>Стоимость похорон</strong><span>Бюджет</span></a>
        <a class="hub-card" href="kogda-ustanavlivat-pamyatnik/"><strong>Когда устанавливать памятник</strong><span>Сроки</span></a>
      </div>
"""
    if "chto-delat-esli-umer-chelovek" in t and "Ключевые статьи" in t:
        return
    if "<!-- silo-architecture:start -->" in t:
        t = t.replace("<!-- silo-architecture:start -->", block + "<!-- silo-architecture:start -->", 1)
    elif "</main>" in t:
        t = t.replace("</main>", block + "</main>", 1)
    else:
        t += block
    p.write_text(t, encoding="utf-8", newline="\n")
    print("patched stati hub")


def main() -> None:
    build_ceny()
    build_nashi_raboty()
    build_otzyvy()
    build_faq()
    build_ritualny_agent()
    build_articles()
    patch_uslugi_hub_link()
    patch_stati_hub_links()
    print("done", TODAY)


if __name__ == "__main__":
    main()
