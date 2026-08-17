# -*- coding: utf-8 -*-
"""Generate Almaty district and nearby settlement location pages."""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

from seo_head import icon_links, social_meta

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://angelgranit.com"
PHONE = "+7 701 056 7667"
PHONE_TEL = "+77010567667"
ADDRESS = "ул. Осетинская, 5а"
AGENT = "Александр"
OFFICE_LAT = 43.289921
OFFICE_LNG = 76.961065
TODAY = date.today().isoformat()

DISTRICTS = [
    {
        "slug": "almalinskij",
        "name": "Алмалинский район",
        "short": "Алмалинский",
        "lat": 43.2505,
        "lng": 76.9120,
        "about": "центр и плотная городская застройка, много жилых кварталов и деловых улиц",
        "landmarks": "район проспекта Абая, улиц Байтурсынова и Толе би",
        "travel": "из офиса на Осетинской подача обычно занимает от 25–45 минут в зависимости от пробок",
    },
    {
        "slug": "auezovskij",
        "name": "Ауэзовский район",
        "short": "Ауэзовский",
        "lat": 43.2140,
        "lng": 76.8500,
        "about": "запад и юго-запад города с крупными жилыми массивами",
        "landmarks": "микрорайоны Аксай, Алтынсарина, Орбита",
        "travel": "выезд агента и катафалка планируем с запасом на развязки и загруженность Саина",
    },
    {
        "slug": "bostandykskij",
        "name": "Бостандыкский район",
        "short": "Бостандыкский",
        "lat": 43.2070,
        "lng": 76.9050,
        "about": "юг города, жилые комплексы и подъезд к предгорьям",
        "landmarks": "район Аль-Фараби, Розыбакиева, горной стороны",
        "travel": "учитываем подъёмы и вечерние пробки на южных магистралях",
    },
    {
        "slug": "zhetysuskij",
        "name": "Жетысуский район",
        "short": "Жетысуский",
        "lat": 43.2900,
        "lng": 76.9600,
        "about": "северо-восток Алматы, здесь же находится наш офис",
        "landmarks": "ул. Осетинская, район Рыскулова и Серыкова",
        "travel": "самый быстрый выезд: офис AngelGranit в этом же районе",
    },
    {
        "slug": "medeuskij",
        "name": "Медеуский район",
        "short": "Медеуский",
        "lat": 43.2400,
        "lng": 76.9600,
        "about": "восток и юго-восток, часть территории ближе к Медеу и горным дорогам",
        "landmarks": "Достык, Кульджинский тракт, горные подъезды",
        "travel": "время подачи зависит от уклонов и сезона, особенно зимой",
    },
    {
        "slug": "nauryzbajskij",
        "name": "Наурызбайский район",
        "short": "Наурызбайский",
        "lat": 43.1800,
        "lng": 76.8200,
        "about": "относительно новый район с активной застройкой на юго-западе",
        "landmarks": "жилые массивы Калкаман и прилегающие кварталы",
        "travel": "закладываем дополнительное время на новые развязки и навигацию по ЖК",
    },
    {
        "slug": "turksibskij",
        "name": "Турксибский район",
        "short": "Турксибский",
        "lat": 43.3300,
        "lng": 76.9400,
        "about": "север города, промышленные и жилые зоны",
        "landmarks": "район вокзала Алматы-1 и северных въездов",
        "travel": "удобно стыковать маршруты с междугородней перевозкой",
    },
    {
        "slug": "alatauskij",
        "name": "Алатауский район",
        "short": "Алатауский",
        "lat": 43.3500,
        "lng": 76.8800,
        "about": "крупный северный район с большой протяжённостью",
        "landmarks": "Шанырак, Айгерим и соседние массивы",
        "travel": "из-за расстояний заранее согласуем точку подачи катафалка",
    },
]

SETTLEMENTS = [
    {"slug": "kaskelen", "name": "Каскелен", "lat": 43.1980, "lng": 76.6310, "about": "крупный город рядом с Алматы, частые заявки на катафалк и похороны", "travel": "ориентир подачи — 40–70 минут от офиса в зависимости от трассы"},
    {"slug": "talgar", "name": "Талгар", "lat": 43.3030, "lng": 77.2380, "about": "город у предгорий к востоку от Алматы", "travel": "учитываем Кульджинское направление и загруженность в часы пик"},
    {"slug": "esik", "name": "Есик", "lat": 43.3550, "lng": 77.4640, "about": "город восточнее Талгара, заявки на перевозку и организацию похорон", "travel": "междугородний маршрут согласуем заранее по времени"},
    {"slug": "uzynagash", "name": "Узынагаш", "lat": 43.2150, "lng": 76.3150, "about": "населённый пункт западнее Алматы по трассе", "travel": "подача транспорта планируется с запасом на загородную дорогу"},
    {"slug": "qonaev", "name": "Қонаев (Капшагай)", "lat": 43.8830, "lng": 77.0680, "about": "город у водохранилища, востребована междугородняя перевозка", "travel": "рейс занимает заметно больше времени — фиксируем тайминг отдельно"},
    {"slug": "boraldaj", "name": "Боралдай", "lat": 43.3450, "lng": 76.8700, "about": "посёлок рядом с северной частью Алматы", "travel": "удобно стыковать с Турксибским и Алатауским направлениями"},
    {"slug": "otegen-batyr", "name": "Отеген батыр", "lat": 43.4200, "lng": 77.0200, "about": "населённый пункт к северо-востоку от города", "travel": "согласуем точку встречи и маршрут без лишних пересадок"},
    {"slug": "irgeeli", "name": "Иргели", "lat": 43.1700, "lng": 76.8700, "about": "посёлок у южной границы Алматы", "travel": "часто совмещаем с выездом в Бостандыкский/Наурызбайский сектор"},
    {"slug": "besagash", "name": "Бесагаш", "lat": 43.3000, "lng": 77.1500, "about": "населённый пункт в сторону Талгара", "travel": "подача зависит от состояния восточной трассы"},
    {"slug": "guljala", "name": "Гулдала", "lat": 43.3600, "lng": 77.0500, "about": "посёлок в Алматинской агломерации", "travel": "маршруты строим через северные/восточные выезды"},
    {"slug": "panfilovo", "name": "Панфилово", "lat": 43.3300, "lng": 77.1000, "about": "населённый пункт восточнее города", "travel": "катафалк и агент выезжают по предварительному времени"},
    {"slug": "bajserke", "name": "Байсерке", "lat": 43.4800, "lng": 77.0500, "about": "посёлок севернее Алматы", "travel": "для междугородней логистики заранее подтверждаем адреса"},
    {"slug": "pokrovka", "name": "Покровка", "lat": 43.2800, "lng": 76.7000, "about": "населённый пункт западнее города", "travel": "время в пути зависит от загруженности западных развязок"},
    {"slug": "kemer", "name": "Кемертоган", "lat": 43.2100, "lng": 76.7600, "about": "населённый пункт в пригороде Алматы", "travel": "выезд планируем с учётом пригородного трафика"},
    {"slug": "atau", "name": "Атамекен", "lat": 43.1900, "lng": 76.7800, "about": "пригородный массив с жилой застройкой", "travel": "навигацию уточняем по ориентирам ЖК и улицам"},
    {"slug": "zhanaturmys", "name": "Жаңатіршілік", "lat": 43.2600, "lng": 76.7500, "about": "населённый пункт в западном пригороде", "travel": "подача службы согласуется по телефону 24/7"},
]

SERVICE_LINKS = [
    ("ritualnye-uslugi", "Ритуальные услуги"),
    ("organizaciya-pohoron", "Организация похорон"),
    ("katafalk", "Катафалк"),
    ("perevozka-umershih", "Перевозка"),
    ("pamyatniki", "Памятники"),
    ("granitnye-pamyatniki", "Гранитные памятники"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def ensure_desc(desc: str) -> str:
    desc = desc.strip()
    while len(desc) < 150:
        desc = (desc.rstrip(".") + f". AngelGranit, {ADDRESS}, {PHONE}.").strip()
        if len(desc) >= 150:
            break
        desc = (desc.rstrip(".") + " 24/7.").strip()
    if len(desc) > 160:
        desc = desc[:160].rsplit(" ", 1)[0].rstrip(".,;:") + "."
    return desc


def nav_html(depth: int = 1) -> str:
    prefix = "../" * depth
    home = prefix if depth else "./"
    dist = "\n".join(f'          <a href="{prefix}rajony/{esc(d["slug"])}/">{esc(d["short"])}</a>' for d in DISTRICTS)
    sett = "\n".join(f'          <a href="{prefix}naselennye-punkty/{esc(s["slug"])}/">{esc(s["name"])}</a>' for s in SETTLEMENTS[:8])
    return f"""  <header class="site-nav" data-site-nav>
    <a class="site-nav__brand" href="{home}"><strong>AngelGranit</strong><span>AG</span></a>
    <button class="site-nav__toggle" type="button" data-nav-toggle aria-expanded="false">Меню</button>
    <ul class="site-nav__menu">
      <li><a href="{prefix}uslugi/">Услуги</a></li>
      <li><a href="{prefix}stati/">Статьи</a></li>
      <li class="site-nav__item" data-dropdown>
        <button type="button">Районы</button>
        <div class="site-nav__dropdown">
          <a href="{prefix}rajony/">Все районы Алматы</a>
{dist}
          <a href="{prefix}naselennye-punkty/">Населённые пункты</a>
{sett}
        </div>
      </li>
      <li><a href="{prefix}kontakty/">Контакты</a></li>
    </ul>
    <a class="site-nav__call" href="tel:{PHONE_TEL}">Позвонить 24/7</a>
  </header>"""


def map_block(lat: float, lng: float, label: str, map_id: str) -> str:
    return f"""
      <section class="loc-map-block" aria-label="Карта">
        <h2>Карта: {esc(label)}</h2>
        <p class="lead">Точка ориентира на карте и офис AngelGranit ({esc(ADDRESS)}).</p>
        <div id="{esc(map_id)}" class="loc-map" role="img" aria-label="Карта {esc(label)}"></div>
        <p class="loc-map-links">
          <a class="btn-site btn-site--ghost" href="https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=13/{lat}/{lng}" target="_blank" rel="noopener noreferrer">Открыть в OpenStreetMap</a>
          <a class="btn-site btn-site--ghost" href="https://2gis.kz/almaty/geo/9430047375176085" target="_blank" rel="noopener noreferrer">Офис в 2ГИС</a>
        </p>
      </section>
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="" />
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
      <script>
        (function () {{
          if (!window.L) return;
          var map = L.map('{esc(map_id)}').setView([{lat}, {lng}], 12);
          L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 18,
            attribution: '&copy; OpenStreetMap'
          }}).addTo(map);
          L.marker([{lat}, {lng}]).addTo(map).bindPopup({json.dumps(label, ensure_ascii=False)});
          L.marker([{OFFICE_LAT}, {OFFICE_LNG}]).addTo(map).bindPopup('Офис AngelGranit');
        }})();
      </script>
"""


def page_shell(title: str, desc: str, url: str, body: str, schema: dict, depth: int) -> str:
    css_prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <meta name="geo.region" content="KZ-ALA" />
  <meta name="geo.placename" content="Алматы" />
{icon_links(css_prefix)}
{social_meta(title=esc(title), desc=esc(desc), url=url, image=f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp")}
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{css_prefix}seo/assets/seo.css" />
  <link rel="stylesheet" href="{css_prefix}assets/site/nav.css" />
  <link rel="stylesheet" href="{css_prefix}assets/site/page.css" />
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{nav_html(depth)}
{body}
  <footer class="page-footer">
    <strong>AngelGranit</strong>
    {esc(AGENT)} · {esc(ADDRESS)} · <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
  </footer>
  <script src="{css_prefix}assets/site/nav.js" defer></script>
</body>
</html>
"""


def local_business_schema(name: str, url: str, lat: float, lng: float, desc: str) -> dict:
    return {
        "@type": ["LocalBusiness", "FuneralHome"],
        "@id": url + "#localbusiness",
        "name": f"AngelGranit — {name}",
        "image": f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp",
        "url": url,
        "telephone": PHONE_TEL,
        "priceRange": "₸₸₸",
        "description": desc,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ADDRESS,
            "addressLocality": "Алматы",
            "addressRegion": "Алматы",
            "addressCountry": "KZ",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
        "openingHours": "Mo-Su 00:00-24:00",
        "areaServed": {"@type": "Place", "name": name},
        "parentOrganization": {"@id": f"{BASE}/#organization"},
    }


def render_location(kind: str, loc: dict, peers: list[dict]) -> str:
    is_district = kind == "rajony"
    folder = "rajony" if is_district else "naselennye-punkty"
    place = loc["name"]
    short = loc.get("short", place)
    title = f"Ритуальные услуги в {place}, Алматы | AngelGranit"
    desc = ensure_desc(
        f"Ритуальные услуги в {place}: организация похорон, катафалк, памятники. Выезд 24/7, агент {AGENT}."
    )
    url = f"{BASE}/{folder}/{loc['slug']}/"
    h1 = f"Ритуальные услуги в {place}"
    svc = "\n".join(
        f'<a href="../../uslugi/{esc(slug)}/"><strong>{esc(title_)}</strong><span>Заказать в {esc(short)}</span></a>'
        for slug, title_ in SERVICE_LINKS
    )
    peer_list = [p for p in peers if p["slug"] != loc["slug"]][:8]
    peer_links = "\n".join(
        f'<a href="../{esc(p["slug"])}/"><strong>{esc(p.get("short", p["name"]))}</strong><span>Ритуальные услуги</span></a>'
        for p in peer_list
    )
    other_kind = "naselennye-punkty" if is_district else "rajony"
    other_label = "Населённые пункты" if is_district else "Районы Алматы"
    articles = f"""
        <a href="../../stati/pervye-shagi/"><strong>Первые шаги</strong><span>Что делать сразу</span></a>
        <a href="../../stati/organizaciya-pohoron/"><strong>Организация похорон</strong><span>Статьи по теме</span></a>
        <a href="../../stati/transport/"><strong>Катафалк и перевозка</strong><span>Логистика</span></a>
        <a href="../../stati/pamyatniki/"><strong>Памятники</strong><span>Выбор и установка</span></a>
"""
    about = loc["about"]
    landmarks = loc.get("landmarks", loc.get("about", ""))
    travel = loc["travel"]
    kind_word = "районе" if is_district else "населённом пункте"

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
                "@type": "WebSite",
                "@id": f"{BASE}/#website",
                "url": f"{BASE}/",
                "name": "AngelGranit",
                "publisher": {"@id": f"{BASE}/#organization"},
            },
            {
                "@type": "WebPage",
                "name": title,
                "description": desc,
                "url": url,
                "isPartOf": {"@id": f"{BASE}/#website"},
                "about": local_business_schema(place, url, loc["lat"], loc["lng"], desc),
            },
            local_business_schema(place, url, loc["lat"], loc["lng"], desc),
            {
                "@type": "Service",
                "name": f"Ритуальные услуги в {place}",
                "provider": {"@id": f"{BASE}/#organization"},
                "areaServed": {"@type": "Place", "name": place},
                "url": url,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Районы" if is_district else "Населённые пункты", "item": f"{BASE}/{folder}/"},
                    {"@type": "ListItem", "position": 3, "name": place, "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"Выезжаете ли в {place}?",
                        "acceptedAnswer": {"@type": "Answer", "text": f"Да, AngelGranit оказывает ритуальные услуги в {place}. Звоните {PHONE}."},
                    },
                    {
                        "@type": "Question",
                        "name": f"Как быстро приедет агент в {place}?",
                        "acceptedAnswer": {"@type": "Answer", "text": f"{travel.capitalize()}. Точный ориентир назовём после звонка."},
                    },
                    {
                        "@type": "Question",
                        "name": "Можно заказать только катафалк?",
                        "acceptedAnswer": {"@type": "Answer", "text": "Да, транспорт можно заказать отдельно от полного пакета."},
                    },
                    {
                        "@type": "Question",
                        "name": "Где ваш офис?",
                        "acceptedAnswer": {"@type": "Answer", "text": f"Офис: {ADDRESS}, Жетысуский район, Алматы."},
                    },
                    {
                        "@type": "Question",
                        "name": "Работаете ночью?",
                        "acceptedAnswer": {"@type": "Answer", "text": "Да, круглосуточно 24/7."},
                    },
                    {
                        "@type": "Question",
                        "name": "Делаете памятники после похорон?",
                        "acceptedAnswer": {"@type": "Answer", "text": "Да, гранитные памятники и благоустройство можно заказать отдельно."},
                    },
                ],
            },
        ],
    }

    body = f"""  <main class="page-main">
    <div class="page-wrap">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../../">Главная</a></li>
          <li><a href="../">{"Районы Алматы" if is_district else "Населённые пункты"}</a></li>
          <li aria-current="page">{esc(place)}</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>{esc(h1)}</h1>
        <p class="lead">Выезд ритуального агента, организация похорон, катафалк и памятники для семей в {esc(kind_word)} {esc(place)}.</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn-site btn-site--ghost" href="../../uslugi/ritualnye-uslugi/">Все ритуальные услуги</a>
        </div>
      </header>
      <article class="page-article">
        <h2>Помощь семьям в {esc(place)}</h2>
        <p>{esc(place)} — {esc(about)}. AngelGranit принимает заявки 24/7 и помогает без навязанных опций.</p>
        <p>Ориентиры местности: {esc(landmarks)}. Агент {esc(AGENT)} подскажет порядок действий уже в первом звонке.</p>
        <h2>Как проходит выезд</h2>
        <p>После обращения уточняем адрес в {esc(place)}, что уже сделано и какой формат помощи нужен: полная организация похорон или отдельные услуги.</p>
        <p>{esc(travel).capitalize()}. Для катафалка заранее фиксируем точки подачи и запас по времени.</p>
        <h2>Какие услуги доступны здесь</h2>
        <p>В {esc(place)} можно заказать ритуальные услуги, организацию похорон под ключ, перевозку, венки и принадлежности, а также памятники и благоустройство позже.</p>
        <p>Офис: {esc(ADDRESS)}. Телефон: {esc(PHONE)}. Работаем по Алматы и области.</p>
      </article>
      {map_block(loc["lat"], loc["lng"], place, f"map-{loc['slug']}")}
      <section>
        <h2>Услуги для {esc(short)}</h2>
        <div class="related-grid">{svc}</div>
      </section>
      <section>
        <h2>Полезные статьи</h2>
        <div class="related-grid">{articles}</div>
      </section>
      <section>
        <h2>Другие {"районы" if is_district else "населённые пункты"}</h2>
        <div class="related-grid">{peer_links}</div>
        <p style="margin-top:1rem"><a href="../../{other_kind}/">{esc(other_label)}</a></p>
      </section>
      <section class="page-faq">
        <h2>FAQ по {esc(place)}</h2>
        <details><summary>Выезжаете ли в {esc(place)}?</summary><p>Да, обслуживаем {esc(place)} круглосуточно.</p></details>
        <details><summary>Как быстро будет агент?</summary><p>{esc(travel).capitalize()}.</p></details>
        <details><summary>Можно только катафалк?</summary><p>Да, транспорт заказывается отдельно.</p></details>
        <details><summary>Где офис?</summary><p>{esc(ADDRESS)}, Алматы.</p></details>
        <details><summary>Есть ли памятники?</summary><p>Да, изготовление и установка по согласованию.</p></details>
        <details><summary>Как связаться?</summary><p>{esc(PHONE)}, WhatsApp, агент {esc(AGENT)}.</p></details>
      </section>
      <div class="page-cta" style="margin-top:2rem">
        <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить</a>
        <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
      </div>
    </div>
  </main>
"""
    return page_shell(title, desc, url, body, schema, 2)


def render_hub(kind: str) -> str:
    is_district = kind == "rajony"
    items = DISTRICTS if is_district else SETTLEMENTS
    folder = kind
    title = "Ритуальные услуги по районам Алматы | AngelGranit" if is_district else "Ритуальные услуги в населённых пунктах у Алматы | AngelGranit"
    desc = ensure_desc(
        "Выезд AngelGranit по районам Алматы 24/7." if is_district else "Ритуальные услуги в пригороде Алматы: Каскелен, Талгар, Есик и другие."
    )
    url = f"{BASE}/{folder}/"
    cards = "\n".join(
        f'<a class="hub-card" href="{esc(i["slug"])}/"><strong>{esc(i.get("short", i["name"]))}</strong><span>{esc(i["about"][:120])}…</span></a>'
        for i in items
    )
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "name": title, "description": desc, "url": url},
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Районы Алматы" if is_district else "Населённые пункты", "item": url},
                ],
            },
        ],
    }
    h1 = "Районы Алматы" if is_district else "Населённые пункты"
    lead = "Выберите район — откроется страница с выездом, картой и услугами." if is_district else "Пригород Алматы и область: выезд агента, катафалк, похороны и памятники."
    body = f"""  <main class="page-main">
    <div class="page-wrap--wide">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../">Главная</a></li>
          <li aria-current="page">{esc(h1)}</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>{esc(h1)}</h1>
        <p class="lead">{esc(lead)}</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn-site btn-site--ghost" href="../{"naselennye-punkty" if is_district else "rajony"}/">{"Населённые пункты" if is_district else "Районы Алматы"}</a>
        </div>
      </header>
      <div class="hub-grid">{cards}</div>
    </div>
  </main>
"""
    return page_shell(title, desc, url, body, schema, 1)


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8") if path.exists() else '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'
    text = re.sub(
        r"\s*<url>\s*<loc>https://angelgranit\.com/(?:rajony|naselennye-punkty)(?:/[^<]*)?/?</loc>[\s\S]*?</url>",
        "",
        text,
    )
    blocks = []
    for folder, items, pr in (
        ("rajony", DISTRICTS, "0.85"),
        ("naselennye-punkty", SETTLEMENTS, "0.8"),
    ):
        blocks.append(
            f"  <url>\n    <loc>{BASE}/{folder}/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>"
        )
        for it in items:
            blocks.append(
                f"  <url>\n    <loc>{BASE}/{folder}/{it['slug']}/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{pr}</priority>\n  </url>"
            )
    text = text.replace("</urlset>", "\n".join(blocks) + "\n</urlset>")
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    for kind, items in (("rajony", DISTRICTS), ("naselennye-punkty", SETTLEMENTS)):
        root = ROOT / kind
        root.mkdir(parents=True, exist_ok=True)
        (root / "index.html").write_text(render_hub(kind), encoding="utf-8", newline="\n")
        for loc in items:
            d = root / loc["slug"]
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(render_location(kind, loc, items), encoding="utf-8", newline="\n")
            print("OK", kind, loc["slug"])
    update_sitemap()
    print("districts", len(DISTRICTS), "settlements", len(SETTLEMENTS))


if __name__ == "__main__":
    main()
