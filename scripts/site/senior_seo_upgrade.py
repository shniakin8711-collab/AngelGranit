# -*- coding: utf-8 -*-
"""
Senior SEO Architect upgrade — phases A–J (no design change).
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://shniakin8711-collab.github.io/AngelGranit"
TODAY = date.today().isoformat()
PHONE = "+7 701 056 7667"
PHONE_TEL = "+77010567667"
ADDRESS = "ул. Осетинская, 5а"
AGENT = "Александр"
SKIP = {".git", ".idea", "scripts", "node_modules", "__pycache__", "assets"}
REPORT: dict = {"phases": {}, "fixes": []}


def safe_write(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmpopt")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    last = None
    for _ in range(12):
        try:
            tmp.replace(path)
            return
        except OSError as e:
            last = e
            time.sleep(0.3)
    path.write_bytes(tmp.read_bytes())
    tmp.unlink(missing_ok=True)


def pages() -> list[Path]:
    out = [p for p in ROOT.rglob("index.html") if not any(x in SKIP for x in p.parts)]
    if (ROOT / "404.html").exists():
        out.append(ROOT / "404.html")
    return out


def log(phase: str, msg: str) -> None:
    REPORT["fixes"].append(f"[{phase}] {msg}")
    REPORT["phases"].setdefault(phase, []).append(msg)
    print(f"[{phase}] {msg}")


# ── Phase A ──────────────────────────────────────────────────────────────────

def phase_a() -> None:
    # robots
    robots = """# AngelGranit — crawl policy
User-agent: *
Allow: /

# Build tooling / IDE (not public content)
Disallow: /scripts/
Disallow: /.idea/

# Sitemap (absolute)
Sitemap: https://shniakin8711-collab.github.io/AngelGranit/sitemap.xml
"""
    safe_write(ROOT / "robots.txt", robots)
    log("A", "robots.txt refreshed")

    # homepage: remove keywords meta (noise)
    home = ROOT / "index.html"
    ht = home.read_text(encoding="utf-8")
    ht2 = re.sub(r'\n\s*<meta name="keywords" content="[^"]*"\s*/?>', "", ht, count=1)
    if ht2 != ht:
        safe_write(home, ht2)
        log("A", "removed meta keywords from homepage")

    # OG dims + og:url sync + title length + twitter card
    n_og = n_title = n_tw = 0
    for p in pages():
        if p.name == "404.html":
            continue
        t = p.read_text(encoding="utf-8")
        orig = t
        can_m = re.search(r'rel="canonical" href="([^"]+)"', t)
        can = can_m.group(1) if can_m else ""
        if can and 'property="og:url"' in t:
            t = re.sub(
                r'(property="og:url" content=")[^"]*(")',
                rf"\1{can}\2",
                t,
                count=1,
            )
        if 'property="og:image"' in t and 'og:image:width' not in t:
            # insert after og:image or og:image:alt
            if 'og:image:alt' in t:
                t = re.sub(
                    r'(property="og:image:alt" content="[^"]*"\s*/?>)',
                    r'\1\n  <meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />',
                    t,
                    count=1,
                )
            else:
                t = re.sub(
                    r'(property="og:image" content="[^"]*"\s*/?>)',
                    r'\1\n  <meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />',
                    t,
                    count=1,
                )
            n_og += 1
        if 'name="twitter:card"' not in t and 'property="og:image"' in t:
            t = re.sub(
                r'(property="og:image"[^>]*>)',
                r'\1\n  <meta name="twitter:card" content="summary_large_image" />',
                t,
                count=1,
            )
            n_tw += 1
        # title length
        tm = re.search(r"<title>(.*?)</title>", t, re.S)
        if tm:
            title = re.sub(r"\s+", " ", tm.group(1)).strip()
            new_title = title
            if len(new_title) < 35 and "AngelGranit" in new_title:
                new_title = new_title.replace(" | AngelGranit", " в Алматы | AngelGranit")
                if len(new_title) < 35:
                    new_title = f"{new_title.rstrip(' |')} — ритуальные услуги | AngelGranit"
            if len(new_title) > 65:
                # keep brand
                core = re.sub(r"\s*\|\s*AngelGranit\s*$", "", new_title).strip()
                if len(core) > 48:
                    core = core[:48].rsplit(" ", 1)[0]
                new_title = f"{core} | AngelGranit"
            if new_title != title:
                t = t.replace(f"<title>{tm.group(1)}</title>", f"<title>{new_title}</title>", 1)
                t = re.sub(r'(property="og:title" content=")[^"]*(")', rf"\1{new_title}\2", t, count=1)
                t = re.sub(r'(name="twitter:title" content=")[^"]*(")', rf"\1{new_title}\2", t, count=1)
                n_title += 1
        if t != orig:
            safe_write(p, t)
    log("A", f"og dims added={n_og}, titles fixed={n_title}, twitter cards={n_tw}")

    # rebuild sitemap indexable
    urls: list[tuple[str, str]] = []
    for p in ROOT.rglob("index.html"):
        if any(x in SKIP for x in p.parts):
            continue
        rel = p.parent.relative_to(ROOT).as_posix()
        loc = f"{BASE}/" if rel == "." else f"{BASE}/{rel}/"
        if rel.startswith("seo/") and rel != "seo":
            html = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'rel="canonical" href="([^"]+)"', html)
            if m and m.group(1).rstrip("/") != loc.rstrip("/"):
                continue
        parts = [] if rel == "." else rel.split("/")
        pr = "0.85"
        if not parts:
            pr = "1.0"
        elif parts[0] == "uslugi":
            pr = "0.95" if len(parts) == 1 else "0.9"
        elif parts[0] == "stati":
            pr = "0.9" if len(parts) == 1 else ("0.85" if len(parts) == 2 else "0.75")
        elif parts[0] in {"ceny", "faq", "otzyvy", "nashi-raboty", "kontakty", "klastery", "o-kompanii"}:
            pr = "0.9"
        elif parts[0] == "temy":
            pr = "0.88"
        urls.append((loc, pr))
    seen = set()
    out = []
    for loc, pr in urls:
        if loc not in seen:
            seen.add(loc)
            out.append((loc, pr))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pr in out:
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{pr}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    safe_write(ROOT / "sitemap.xml", "\n".join(lines) + "\n")
    log("A", f"sitemap rebuilt {len(out)} urls")


# ── Phase B ──────────────────────────────────────────────────────────────────

def phase_b() -> None:
    home = ROOT / "index.html"
    t = home.read_text(encoding="utf-8")
    # async font load pattern without changing families
    old = '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />'
    new = (
        '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" '
        'rel="stylesheet" media="print" onload="this.media=\'all\'" />\n'
        '  <noscript><link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" /></noscript>'
    )
    if old in t and "media=\"print\" onload" not in t:
        t = t.replace(old, new, 1)
        log("B", "homepage fonts async media=print")
    # defer heavy catalog/map init further — flag already using IO; add idle callback wrapper marker
    if "requestIdleCallback" not in t and "catalog-filters" in t:
        # wrap first DOMContentLoaded heavy block lightly: inject helper near script start
        t = t.replace(
            "<script src=\"assets/site/nav.js\" defer></script>\n  <script>",
            "<script src=\"assets/site/nav.js\" defer></script>\n  <script>\n"
            "    window.__agIdle=function(cb){if('requestIdleCallback' in window)requestIdleCallback(cb,{timeout:2000});else setTimeout(cb,1);};\n",
            1,
        )
        log("B", "added requestIdleCallback helper")
    safe_write(home, t)


# ── Phase C: o-kompanii + reviews schema ─────────────────────────────────────

def phase_c_about_and_reviews() -> None:
    # About page
    url = f"{BASE}/o-kompanii/"
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>О компании AngelGranit — ритуальные услуги Алматы</title>
  <meta name="description" content="О компании AngelGranit в Алматы: агент Александр, ритуальные услуги 24/7, памятники, катафалк. Адрес {ADDRESS}, телефон {PHONE}." />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="icon" href="../assets/icons/favicon.svg" type="image/svg+xml" />
  <link rel="manifest" href="../site.webmanifest" />
  <meta name="theme-color" content="#d4af57" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="О компании AngelGranit — ритуальные услуги Алматы" />
  <meta property="og:description" content="AngelGranit: кто мы, как работаем, адрес и режим 24/7 в Алматы." />
  <meta property="og:image" content="{BASE}/images/hero-angelgranit.webp" />
  <meta property="og:image:width" content="1024" />
  <meta property="og:image:height" content="408" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="О компании AngelGranit" />
  <meta name="twitter:description" content="Ритуальные услуги Алматы 24/7 — AngelGranit." />
  <meta name="twitter:image" content="{BASE}/images/hero-angelgranit.webp" />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Manrope:wght@400;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../seo/assets/seo.css" />
  <link rel="stylesheet" href="../assets/site/nav.css" />
  <link rel="stylesheet" href="../assets/site/page.css" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "AboutPage",
        "@id": "{url}#webpage",
        "url": "{url}",
        "name": "О компании AngelGranit",
        "description": "Ритуальные услуги Алматы 24/7: организация похорон, катафалк, памятники.",
        "about": {{"@id": "{BASE}/#business"}}
      }},
      {{
        "@type": ["LocalBusiness", "FuneralHome"],
        "@id": "{BASE}/#business",
        "name": "AngelGranit",
        "url": "{BASE}/",
        "telephone": "{PHONE_TEL}",
        "image": "{BASE}/images/hero-angelgranit.webp",
        "address": {{
          "@type": "PostalAddress",
          "streetAddress": "{ADDRESS}",
          "addressLocality": "Алматы",
          "addressCountry": "KZ"
        }},
        "geo": {{"@type": "GeoCoordinates", "latitude": 43.289921, "longitude": 76.961065}},
        "openingHoursSpecification": {{
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
          "opens": "00:00",
          "closes": "23:59"
        }},
        "priceRange": "₸₸₸",
        "areaServed": [{{"@type": "City", "name": "Алматы"}}, {{"@type": "AdministrativeArea", "name": "Алматинская область"}}],
        "sameAs": [
          "https://www.youtube.com/@AngelGranit",
          "https://www.youtube.com/@Blackurbanfpv"
        ]
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type": "ListItem", "position": 1, "name": "Главная", "item": "{BASE}/"}},
          {{"@type": "ListItem", "position": 2, "name": "О компании", "item": "{url}"}}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>
  <a class="skip-link" href="#main-content">Перейти к содержанию</a>
  <header class="site-nav" data-site-nav>
    <a class="site-nav__brand" href="../"><strong>AngelGranit</strong><span>AG</span></a>
    <button class="site-nav__toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav-menu">Меню</button>
    <ul class="site-nav__menu" id="site-nav-menu">
      <li><a href="../uslugi/">Услуги</a></li>
      <li><a href="../nashi-raboty/">Работы</a></li>
      <li><a href="../otzyvy/">Отзывы</a></li>
      <li><a href="../kontakty/">Контакты</a></li>
    </ul>
    <a class="site-nav__call" href="tel:{PHONE_TEL}">Позвонить 24/7</a>
  </header>
  <main id="main-content" class="page-main">
    <div class="page-wrap">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../">Главная</a></li>
          <li aria-current="page">О компании</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>О компании AngelGranit</h1>
        <p class="lead">Ритуальные услуги в Алматы 24/7: организация похорон, катафалк, памятники и благоустройство — с одним координатором для семьи.</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {PHONE}</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn-site btn-site--ghost" href="../kontakty/">Контакты</a>
        </div>
      </header>
      <article class="page-article">
        <h2>Кто мы</h2>
        <p>AngelGranit — ритуальная служба и гранитная мастерская в Алматы. Агент {AGENT} принимает обращения круглосуточно и помогает выстроить порядок действий без давления «обязательным» премиум-пакетом.</p>
        <p>Мы совмещаем организацию прощания и последующее оформление места памяти: от катафалка до гранитного памятника и благоустройства.</p>
        <h2>Как работаем</h2>
        <p>После звонка уточняем обстоятельства, район и пожелания семьи. Составляем понятный план и ориентир по бюджету. В день церемонии держим единый тайминг. После похорон остаёмся на связи по памятникам и уходу за участком.</p>
        <h2>Адрес и режим</h2>
        <p>Офис: {ADDRESS}, Алматы. Режим приёма заявок: 24/7. Карта и маршрут — на <a href="../kontakty/">странице контактов</a>.</p>
        <h2>Доказательства работы</h2>
        <p>Смотрите <a href="../nashi-raboty/">наши работы</a>, блок <a href="../#production">производства</a>, <a href="../#guarantees">гарантии</a>, <a href="../otzyvy/">отзывы</a> и видео на YouTube-каналах AngelGranit.</p>
      </article>
      <div class="related-grid">
        <a href="../uslugi/ritualnye-uslugi/"><strong>Ритуальные услуги</strong><span>Каталог</span></a>
        <a href="../uslugi/granitnye-pamyatniki/"><strong>Гранитные памятники</strong><span>Производство</span></a>
        <a href="../faq/"><strong>FAQ</strong><span>Ответы</span></a>
      </div>
    </div>
  </main>
  <footer class="page-footer">
    <strong>AngelGranit</strong>
    {AGENT} · {ADDRESS} · <a href="tel:{PHONE_TEL}">{PHONE}</a>
  </footer>
  <script src="../assets/site/nav.js" defer></script>
</body>
</html>
"""
    d = ROOT / "o-kompanii"
    d.mkdir(exist_ok=True)
    safe_write(d / "index.html", html)
    log("C", "created /o-kompanii/")

    # Homepage reviews → Review schema (no fake AggregateRating scores)
    home = ROOT / "index.html"
    t = home.read_text(encoding="utf-8")
    if '"@type": "Review"' not in t and "review-card__quote" in t:
        quotes = re.findall(
            r'<p class="review-card__quote">(.*?)</p>\s*<div class="review-card__meta">\s*<strong>(.*?)</strong>',
            t,
            re.S,
        )
        if quotes:
            reviews = []
            for body, author in quotes[:5]:
                body = re.sub(r"\s+", " ", body).strip()
                author = re.sub(r"\s+", " ", author).strip()
                reviews.append(
                    {
                        "@type": "Review",
                        "author": {"@type": "Person", "name": author},
                        "reviewBody": body,
                        "itemReviewed": {"@id": f"{BASE}/#business"},
                    }
                )
            # inject into first ld+json graph if possible
            block = ",\n      " + ",\n      ".join(json.dumps(r, ensure_ascii=False) for r in reviews)
            # insert before closing of @graph array — find first script ld+json
            m = re.search(r'(<script type="application/ld\+json">\s*\{.*?"@graph"\s*:\s*\[)(.*?)(\]\s*\}\s*</script>)', t, re.S)
            if m:
                inner = m.group(2).rstrip()
                if inner.endswith(","):
                    inner = inner + "\n      " + ",\n      ".join(json.dumps(r, ensure_ascii=False) for r in reviews)
                else:
                    inner = inner + block
                t = t[: m.start()] + m.group(1) + inner + m.group(3) + t[m.end() :]
                # link about in nav/footer
                if "o-kompanii/" not in t:
                    t = t.replace('href="kontakty/">Контакты</a>', 'href="kontakty/">Контакты</a> · <a href="o-kompanii/">О компании</a>', 1)
                safe_write(home, t)
                log("C", f"added {len(reviews)} Review entities to homepage schema")

    # Enrich LocalBusiness on kontakty if thin
    kp = ROOT / "kontakty" / "index.html"
    if kp.exists():
        kt = kp.read_text(encoding="utf-8")
        if "openingHoursSpecification" not in kt and "LocalBusiness" in kt:
            # leave existing; NAP UX in phase F
            pass
        if "o-kompanii/" not in kt:
            kt = kt.replace("</main>", '      <p class="lead"><a href="../o-kompanii/">О компании AngelGranit</a></p>\n  </main>', 1)
            safe_write(kp, kt)
            log("C", "kontakty → o-kompanii link")


# ── Phase D: expand service content in HTML ──────────────────────────────────

SERVICE_EXPANSIONS: dict[str, list[tuple[str, list[str]]]] = {}


def _exp(slug: str, sections: list[tuple[str, list[str]]]) -> None:
    SERVICE_EXPANSIONS[slug] = sections


def build_service_expansions() -> None:
    common_price = [
        "Цена зависит от состава: что обязательно сегодня и что можно перенести. Ориентиры пакетов на главной — от 150 000 ₸.",
        f"Точную смету озвучим по телефону {PHONE} или в WhatsApp — без скрытых позиций «в последний момент».",
    ]
    # Generate unique expansions for each known service
    specs = {
        "ritualnye-uslugi": (
            "ритуальные услуги",
            [
                ("Когда обращаются за ритуальными услугами", [
                    "К нам обращаются в первые часы после утраты и когда нужно спокойно собрать весь сценарий: документы, транспорт, прощание и дальнейшее оформление места памяти.",
                    "Ритуальные услуги в Алматы — это не «один стандартный пакет», а набор шагов под вашу ситуацию: можно взять полный цикл или только отдельные позиции.",
                    "Агент Александр принимает звонки ночью и в праздники. Важно сразу понять район, место нахождения усопшего и пожелания семьи по традиции.",
                ]),
                ("Этапы работы с AngelGranit", [
                    "Сначала фиксируем обстоятельства и ближайшие задачи. Затем согласуем маршрут, время и состав услуг.",
                    "В день церемонии держим тайминг: подача транспорта, зал или дом, путь на кладбище. После похорон остаёмся на связи по памятникам и благоустройству.",
                    "Для иногородних родственников удобна удалённая координация через WhatsApp — без обязательного визита в офис.",
                ]),
                ("Что входит и что можно отложить", [
                    "Обычно в ближайшие сутки нужны документы, подготовка и транспорт. Зал, расширенное оформление и памятник часто решаются отдельно.",
                    "Мы честно разделяем обязательное и желательное, чтобы семья не переплачивала за ненужное в стрессе.",
                ]),
                ("Логистика по Алматы и области", [
                    "Выезжаем по районам города и в населённые пункты области по согласованию. Время подачи зависит от дороги и адреса.",
                    "Если нужен только катафалк или только консультация агента — это тоже нормальный сценарий.",
                ]),
                ("Как формируется цена", common_price),
            ],
        ),
        "organizaciya-pohoron": (
            "организация похорон",
            [
                ("С чего начать организацию", [
                    "Определите дату, формат прощания и круг участников. Параллельно соберите базовые документы и решите вопрос транспорта.",
                    "Один координатор снижает хаос: семья не разрывается между звонками водителям, залу и родственникам.",
                ]),
                ("Этапы дня прощания", [
                    "Согласуем подачу катафалка, место церемонии и маршрут на кладбище. Заранее закладываем запас времени на дорогу по Алматы.",
                    "Если гости опаздывают или меняется адрес — агент корректирует тайминг и предупреждает участников.",
                ]),
                ("Документы и решения семьи", [
                    "Помогаем выстроить порядок обращений, чтобы не ездить по кругу. Решения по традиции уважаем: православный, мусульманский или светский формат.",
                ]),
                ("Бюджет без сюрпризов", common_price + [
                    "Можно организовать камерные похороны или полный комплекс — состав обсуждаем до ключевых работ.",
                ]),
            ],
        ),
        "pohorony-pod-klyuch": (
            "похороны под ключ",
            [
                ("Кому подходит формат «под ключ»", [
                    "Когда семье нужен единый ответственный за документы, транспорт, принадлежности и тайминг дня. Особенно помогает иногородним родственникам.",
                ]),
                ("Что обычно входит", [
                    "Координация агента, ритуальный транспорт, согласованный набор принадлежностей и сопровождение по маршруту. Точный состав фиксируем в смете.",
                ]),
                ("Что можно упростить", [
                    "Не всё обязательно. Можно убрать зал, сократить оформление или перенести памятник на позже — без потери достоинства церемонии.",
                ]),
                ("Сроки и связь", [
                    f"Начинаем сразу после звонка. Агент {AGENT} на связи 24/7: {PHONE}.",
                ]),
                ("Цена пакета", common_price),
            ],
        ),
        "katafalk": (
            "катафалк",
            [
                ("Когда нужен катафалк", [
                    "Катафалк заказывают для маршрута дом или морг → зал/храм → кладбище. Важно заранее согласовать адреса и время подачи.",
                ]),
                ("Город и область", [
                    "Организуем подачу по Алматы. Междугородние рейсы и Груз 200 обсуждаются отдельно по расстоянию и документам.",
                ]),
                ("Заказ без полного пакета", [
                    "Можно заказать только транспорт. Сопровождение агента подключается по желанию.",
                ]),
                ("Как проходит подача", [
                    "Диспетчер подтверждает класс авто, точку и запас на дорогу. При изменении времени предупредите заранее — скорректируем маршрут.",
                ]),
                ("Стоимость", common_price),
            ],
        ),
        "perevozka-umershih": (
            "перевозка умерших",
            [
                ("Виды перевозки", [
                    "По городу, между моргом и залом, на кладбище, а также междугородняя перевозка при наличии документов.",
                ]),
                ("Документы и подготовка", [
                    "Перед рейсом уточняем пакет документов и требования маршрута. Для сложных случаев подскажем порядок действий.",
                ]),
                ("Бережная логистика", [
                    "Согласуем время, точки и сопровождение. Семья получает понятный план без хаотичных перезвонов.",
                ]),
                ("Цена", common_price),
            ],
        ),
        "pamyatniki": (
            "памятники",
            [
                ("Как выбрать памятник", [
                    "Смотрите материал, форму, правила кладбища, портрет и реальный бюджет. Сначала эскиз — потом изготовление.",
                ]),
                ("Этапы заказа", [
                    "Замер участка, согласование макета, изготовление, фундамент и монтаж. Сроки зависят от сложности и сезона.",
                ]),
                ("Гранит и мрамор", [
                    "Гранит долговечнее для климата Алматы. Мрамор выбирают за светлый вид — честно объясняем особенности ухода.",
                ]),
                ("Цена и состав", common_price + [
                    "В смету могут входить стела, тумба, цветник, гравировка и установка — уточняйте состав «под ключ».",
                ]),
            ],
        ),
        "granitnye-pamyatniki": (
            "гранитные памятники",
            [
                ("Почему гранит", [
                    "Гранит сохраняет форму и читаемость надписи годами при правильном фундаменте и монтаже.",
                ]),
                ("Производство", [
                    "Подбираем камень, готовим макет портрета и текста, согласуем с семьёй, затем изготавливаем и устанавливаем.",
                ]),
                ("Монтаж на кладбищах Алматы", [
                    "Учитываем правила конкретного кладбища и состояние грунта. Аккуратный монтаж важнее «быстрой поставки».",
                ]),
                ("Цена", common_price),
            ],
        ),
        "mramornye-pamyatniki": (
            "мраморные памятники",
            [
                ("Особенности мрамора", [
                    "Мрамор даёт светлый благородный вид. Для климата Алматы важно понимать уход и сравнение с гранитом.",
                ]),
                ("Когда выбирают мрамор", [
                    "Когда семье важен светлый тон и классическая эстетика. Мы поможем сравнить варианты без давления.",
                ]),
                ("Заказ и установка", [
                    "Макет, изготовление, фундамент, монтаж — как и для гранитных изделий, с контролем размеров участка.",
                ]),
                ("Цена", common_price),
            ],
        ),
        "musulmanskie-pamyatniki": (
            "мусульманские памятники",
            [
                ("Учёт традиции", [
                    "Форма, оформление и текст подбираем с учётом пожеланий семьи и правил кладбища.",
                ]),
                ("Этапы", [
                    "Согласование эскиза, изготовление, монтаж. При необходимости поможем с благоустройством участка.",
                ]),
                ("Цена", common_price),
            ],
        ),
        "memorialnye-kompleksy": (
            "мемориальные комплексы",
            [
                ("Что входит в комплекс", [
                    "Единый проект: памятник, цоколь, ограда, покрытие, малые формы. Без разрозненных подрядчиков.",
                ]),
                ("Проектирование", [
                    "Сначала план участка и бюджет. Затем поэтапный монтаж — можно разбить работы по сезонам.",
                ]),
                ("Цена", common_price),
            ],
        ),
        "blagoustrojstvo-mogil": (
            "благоустройство могил",
            [
                ("С чего начать", [
                    "Оцените состояние участка: усадка, плитка, ограда, цветник. Составим план работ без лишнего.",
                ]),
                ("Виды работ", [
                    "Выравнивание, покрытие, ограда, цветник, стол и лавочка, уход перед датами поминовения.",
                ]),
                ("Цена", common_price),
            ],
        ),
        "ogrady": ("ограды", [("Ограда на могилу", ["Подбираем размер и материал под правила кладбища и стиль памятника.", "Монтаж согласуем с остальным благоустройством."]), ("Цена", common_price)]),
        "stoly": ("гранитные столы", [("Столы на участок", ["Гранитный стол делают место визитов удобнее и завершают композицию с лавочкой."]), ("Цена", common_price)]),
        "lavochki": ("лавочки", [("Лавочки", ["Подбираем в одном стиле с памятником и столом. Учитываем размер участка."]), ("Цена", common_price)]),
        "cvetniki": ("цветники", [("Цветник", ["Цветник оформляет зону у стелы и упрощает уход. Можно заказать отдельно или в комплексе."]), ("Цена", common_price)]),
        "fotokeramika": ("фотокерамика", [("Фотокерамика на памятник", ["Готовим изображение для читаемости на камне: контраст, ретушь, согласование макета."]), ("Сроки", ["Сроки зависят от формата овала и загрузки производства — озвучим при заказе."]), ("Цена", common_price)]),
        "gravirovka": ("гравировка", [("Гравировка текста и портрета", ["Шрифт, размер и композиция должны читаться. Согласуем макет до работы на камне."]), ("Исправления", ["Ошибки в тексте лучше ловить на этапе макета. Если нужно — обсудим варианты правки."]), ("Цена", common_price)]),
        "venki": ("венки", [("Ритуальные венки", ["Подберём композиции к церемонии, оформим ленты и доставим к залу, дому или на кладбище."]), ("Цена", common_price)]),
        "ritualnye-prinadlezhnosti": ("ритуальные принадлежности", [("Набор принадлежностей", ["Гроб, текстиль, крест, венки — собираем минимум или расширенный набор под традицию семьи."]), ("Цена", common_price)]),
        "ritualny-agent": ("ритуальный агент", [("Вызов агента 24/7", [f"Агент {AGENT} принимает звонки круглосуточно и даёт порядок действий на ближайшие часы.", "Можно начать с консультации без полного пакета услуг."]), ("Цена консультации", common_price)]),
    }
    for slug, (label, sections) in specs.items():
        SERVICE_EXPANSIONS[slug] = sections


def phase_d_expand_services() -> None:
    build_service_expansions()
    n = 0
    for slug, sections in SERVICE_EXPANSIONS.items():
        path = ROOT / "uslugi" / slug / "index.html"
        if not path.exists():
            continue
        t = path.read_text(encoding="utf-8")
        if "senior-content-expand" in t:
            continue
        chunks = ['<div class="senior-content-expand">']
        for h2, paras in sections:
            chunks.append(f"<h2>{escape(h2)}</h2>")
            for p in paras:
                chunks.append(f"<p>{escape(p)}</p>")
        chunks.append("</div>")
        block = "\n".join(chunks)
        if '<article class="page-article">' in t:
            t = t.replace('<article class="page-article">', '<article class="page-article">\n' + block, 1)
        elif "</article>" in t:
            t = t.replace("</article>", block + "\n</article>", 1)
        else:
            continue
        safe_write(path, t)
        n += 1
    log("D", f"expanded service content on {n} pages")

    # key pillars lightly
    pillars = [
        "ritualnye-uslugi-almaty",
        "organizaciya-pohoron-almaty",
        "katafalk-almaty",
        "pamyatniki-almaty",
        "granitnye-pamyatniki-almaty",
    ]
    for slug in pillars:
        path = ROOT / slug / "index.html"
        if not path.exists():
            continue
        t = path.read_text(encoding="utf-8")
        if "senior-content-expand" in t:
            continue
        extra = f"""
<div class="senior-content-expand">
<h2>Практический порядок для семей в Алматы</h2>
<p>Если вы открыли эту страницу в поиске, начните с одного звонка агенту {escape(AGENT)}: {escape(PHONE)}. Мы коротко объясним, что нужно сделать сейчас, а что можно решить завтра.</p>
<p>AngelGranit совмещает организацию прощания и последующие работы по памятникам. Это удобно, когда семье нужен один понятный контакт, а не десяток подрядчиков.</p>
<p>Адрес офиса: {escape(ADDRESS)}. Заявки принимаем 24/7. Подробные услуги смотрите в каталоге <a href="../uslugi/">/uslugi/</a>.</p>
</div>
"""
        if '<article class="page-article">' in t:
            t = t.replace('<article class="page-article">', '<article class="page-article">\n' + extra, 1)
            safe_write(path, t)
    log("D", "pillar pages enriched")


# ── Phase E: unique article FAQ ──────────────────────────────────────────────

TEMPLATE_FAQ_MARKERS = [
    "Можно решить это без полного пакета?",
    "Какая услуга ближе всего к теме?",
    "Работаете ли круглосуточно?",
    "Можно ли получить ответ в WhatsApp?",
    "Где вы находитесь?",
    "Сколько это примерно стоит?",
    "Нужно ли приезжать в офис?",
]


def unique_faq(question: str, category: str, slug: str) -> list[tuple[str, str]]:
    h = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    q_short = question.rstrip("?")
    faqs = [
        (
            f"С чего начать по вопросу «{q_short}»?",
            f"Кратко опишите ситуацию агенту {AGENT} по телефону {PHONE}: район, срочность и что уже сделано. Дадим порядок шагов под ваш случай.",
        ),
        (
            f"Что важно учесть именно в Алматы?",
            "Учитывайте район, время суток, дорогу до морга/зала/кладбища и правила конкретного кладбища. Это влияет на тайминг и смету.",
        ),
        (
            "Какие услуги AngelGranit обычно рядом с этой темой?",
            {
                "pervye-shagi": "Чаще всего — ритуальные услуги, организация похорон и консультация агента.",
                "organizaciya-pohoron": "Организация похорон, похороны под ключ и катафалк.",
                "dokumenty": "Организация похорон и сопровождение по документам; транспорт при необходимости.",
                "transport": "Катафалк и перевозка умерших; при необходимости — полный цикл организации.",
                "prinadlezhnosti": "Ритуальные принадлежности, венки и похороны под ключ.",
                "pamyatniki": "Памятники, гранитные памятники и гравировка.",
                "granit-i-gravirovka": "Гранитные памятники, гравировка и фотокерамика.",
                "blagoustrojstvo": "Благоустройство могил, ограды и мемориальные комплексы.",
                "tradicii": "Ритуальные услуги и организация похорон с учётом традиции семьи.",
                "ceny-i-byudzhet": "Прозрачная смета по ритуальным услугам, катафалку и памятникам.",
            }.get(category, "Ритуальные услуги и консультация агента 24/7."),
        ),
    ]
    extras = [
        (
            "Можно ли решить вопрос только консультацией?",
            "Да. Полный пакет не обязателен — иногда достаточно совета и одной услуги.",
        ),
        (
            "Как быстро отвечаете ночью?",
            f"Заявки принимаем 24/7. Позвоните {PHONE} или напишите в WhatsApp.",
        ),
        (
            "Нужен ли выезд в офис на Осетинской?",
            f"Не обязательно. Многие вопросы решаем удалённо. Офис: {ADDRESS}.",
        ),
        (
            "Как не переплатить?",
            "Сравнивайте состав сметы, а не только цену «от». Спросите, что входит и что оплачивается отдельно.",
        ),
    ]
    # pick 2 extras uniquely by hash
    faqs.append(extras[h % len(extras)])
    faqs.append(extras[(h // 7) % len(extras)])
    # dedupe
    seen = set()
    out = []
    for q, a in faqs:
        if q in seen:
            continue
        seen.add(q)
        out.append((q, a))
    return out[:5]


def phase_e_articles() -> None:
    idx_path = Path(__file__).with_name("articles_index.json")
    articles = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else []
    n = 0
    for a in articles:
        path = ROOT / "stati" / a["slug"] / "index.html"
        if not path.exists():
            continue
        t = path.read_text(encoding="utf-8")
        faqs = unique_faq(a["question"], a["category"], a["slug"])
        faq_html = "\n".join(
            f"<details><summary>{escape(q)}</summary><p>{escape(ans)}</p></details>" for q, ans in faqs
        )
        # replace page-faq section content
        if 'class="page-faq"' in t:
            t2 = re.sub(
                r'(<section class="page-faq"[^>]*>\s*<h2>[^<]*</h2>)(.*?)(</section>)',
                rf"\1\n{faq_html}\n      \3",
                t,
                count=1,
                flags=re.S,
            )
        else:
            t2 = t
        # light body enrichment if template phrases dominate
        tip = (
            f"<p><strong>Краткий чеклист:</strong> сформулируйте вопрос «{escape(a['question'])}?», "
            f"отметьте район Алматы и срочность, затем позвоните {escape(PHONE)} — так консультация будет предметной.</p>"
        )
        if "Краткий чеклист:" not in t2 and "</article>" in t2:
            t2 = t2.replace("</article>", tip + "\n      </article>", 1)
        # update FAQPage schema block roughly
        if "FAQPage" in t2:
            try:
                entity = [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": ans},
                    }
                    for q, ans in faqs
                ]
                t2 = re.sub(
                    r'("@type"\s*:\s*"FAQPage"[\s\S]*?"mainEntity"\s*:\s*)\[[^\]]*\]',
                    lambda m: m.group(1) + json.dumps(entity, ensure_ascii=False),
                    t2,
                    count=1,
                )
            except re.error:
                pass
        if t2 != t:
            safe_write(path, t2)
            n += 1
    log("E", f"unique FAQ/body patched on {n} articles")

        # future builds handled separately in build_articles.py


# ── Phase F: NAP footer / kontakty / 404 ─────────────────────────────────────

NAP_FOOTER = """  <footer class="page-footer">
    <strong>AngelGranit</strong>
    Александр · ул. Осетинская, 5а · <a href="tel:+77010567667">+7 701 056 7667</a>
    <div class="page-cta" style="justify-content:center;margin-top:1rem">
      <a class="btn-site btn-site--gold" href="tel:+77010567667">Позвонить</a>
      <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
      <a class="btn-site btn-site--ghost" href="{home}nashi-raboty/">Работы</a>
      <a class="btn-site btn-site--ghost" href="{home}otzyvy/">Отзывы</a>
      <a class="btn-site btn-site--ghost" href="{home}kontakty/">Контакты</a>
      <a class="btn-site btn-site--ghost" href="{home}o-kompanii/">О компании</a>
    </div>
  </footer>"""


def phase_f_ux() -> None:
    n = 0
    for p in pages():
        if p.name == "404.html" or p == ROOT / "index.html":
            continue
        depth = 0 if p.parent == ROOT else len(p.parent.relative_to(ROOT).parts)
        home = "../" * depth
        t = p.read_text(encoding="utf-8")
        if "page-footer" not in t:
            continue
        if 'data-wa' in t and "o-kompanii/" in t and "nashi-raboty/" in t and re.search(r'class="page-footer"', t):
            # already rich?
            if "page-cta" in t[t.find("page-footer"): t.find("page-footer") + 800]:
                continue
        footer = NAP_FOOTER.format(home=home)
        t2 = re.sub(r"<footer class=\"page-footer\">.*?</footer>", footer, t, count=1, flags=re.S)
        if t2 != t:
            safe_write(p, t2)
            n += 1
    log("F", f"NAP footers updated on {n} pages")

    # kontakty above-fold CTA
    kp = ROOT / "kontakty" / "index.html"
    if kp.exists():
        kt = kp.read_text(encoding="utf-8")
        if "kontakty-quick-cta" not in kt:
            block = f"""
      <div class="page-cta kontakty-quick-cta" style="margin-bottom:1.5rem">
        <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {PHONE}</a>
        <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <a class="btn-site btn-site--ghost" href="https://2gis.kz/almaty/geo/9430047375176085" target="_blank" rel="noopener noreferrer">Маршрут в 2ГИС</a>
      </div>
"""
            kt = kt.replace("<header class=\"page-hero\">", "<header class=\"page-hero\">" + block, 1)
            if "<header class=\"page-hero\">" not in kt:
                kt = kt.replace("<h1>", block + "<h1>", 1)
            safe_write(kp, kt)
            log("F", "kontakty quick CTA")

    # 404 links
    f404 = ROOT / "404.html"
    if f404.exists():
        t = f404.read_text(encoding="utf-8")
        if "ceny/" not in t:
            t = t.replace(
                'href="uslugi/">Услуги</a>',
                'href="uslugi/">Услуги</a>\n        <a class="btn-site btn-site--ghost" href="ceny/">Цены</a>\n        <a class="btn-site btn-site--ghost" href="faq/">FAQ</a>',
                1,
            )
            safe_write(f404, t)
            log("F", "404 links expanded")


# ── Phase G–I ────────────────────────────────────────────────────────────────

def phase_ghi() -> None:
    # touch targets already in page.css — ensure silo-links mobile
    css = ROOT / "assets" / "site" / "page.css"
    ct = css.read_text(encoding="utf-8")
    if "senior-content-expand" not in ct:
        ct += """
.senior-content-expand h2 {
  margin: 2rem 0 0.75rem;
  font-family: var(--font-display, Georgia, serif);
  font-size: 1.25rem;
  color: #d4af57;
}
.page-footer .page-cta .btn-site { min-height: 2.75rem; }
"""
        safe_write(css, ct)
        log("G", "page.css senior content + touch")

    # SILO gaps: apply marker to pages missing it among hubs
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from apply_silo_architecture import (  # type: ignore
        inject_before_footer,
        latest_articles_block,
        load_articles,
        popular_block,
        trust_links,
        grid,
        MARKER_START,
    )

    articles = load_articles()
    n = 0
    for rel in [
        "ceny/index.html",
        "faq/index.html",
        "otzyvy/index.html",
        "nashi-raboty/index.html",
        "o-kompanii/index.html",
        "klastery/index.html",
    ]:
        p = ROOT / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        if MARKER_START in t:
            continue
        depth = len(Path(rel).parts) - 1
        block = "\n".join(
            [
                popular_block(depth, 5),
                latest_articles_block(depth, articles, 5),
                "<h2>Навигация</h2>",
                grid(trust_links(depth)),
            ]
        )
        safe_write(p, inject_before_footer(t, block))
        n += 1
    log("H", f"SILO added to {n} hub pages")

    # Prefer WebP when sibling file exists (skip hero PNG fallback inside picture)
    converted = 0
    for p in pages():
        t = p.read_text(encoding="utf-8")
        orig = t
        for src in set(re.findall(r'src="([^"]+\.png)"', t)):
            if "hero-angelgranit.png" in src:
                continue
            webp_rel = src[:-4] + ".webp"
            candidates = [
                (p.parent / webp_rel),
            ]
            # root-relative like images/foo.png
            cleaned = src.replace("\\", "/").lstrip("./")
            while cleaned.startswith("../"):
                cleaned = cleaned[3:]
            candidates.append(ROOT / (cleaned[:-4] + ".webp"))
            ok = False
            for c in candidates:
                if c is not None and c.exists():
                    ok = True
                    break
            # also resolve ../ chains
            if not ok and (p.parent / webp_rel).resolve().exists():
                ok = True
            if ok:
                t = t.replace(f'src="{src}"', f'src="{webp_rel}"')
                converted += 1
        if t != orig:
            safe_write(p, t)
    log("I", f"png→webp replacements={converted}")


# ── Phase J ──────────────────────────────────────────────────────────────────

def phase_j() -> None:
    # ensure o-kompanii in sitemap
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    loc = f"{BASE}/o-kompanii/"
    if loc not in sm:
        entry = f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>\n"
        sm = sm.replace("</urlset>", entry + "</urlset>")
        safe_write(ROOT / "sitemap.xml", sm)
        log("J", "o-kompanii in sitemap")

    # metrics
    arts = list((ROOT / "stati").glob("*/index.html"))
    templ = 0
    for p in arts:
        if p.parent.name in {
            "pervye-shagi", "organizaciya-pohoron", "dokumenty", "transport",
            "prinadlezhnosti", "pamyatniki", "granit-i-gravirovka", "blagoustrojstvo",
            "tradicii", "ceny-i-byudzhet",
        }:
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if "Можно решить это без полного пакета?" in t:
            templ += 1

    svc_words = {}
    for p in (ROOT / "uslugi").glob("*/index.html"):
        t = p.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"<article[^>]*>(.*?)</article>", t, re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", m.group(1) if m else "")
        svc_words[p.parent.name] = len(re.sub(r"\s+", " ", text).split())

    og_missing = 0
    for p in pages():
        if p.name == "404.html":
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if 'property="og:image"' in t and "og:image:width" not in t:
            og_missing += 1

    report = {
        "date": TODAY,
        "phases": REPORT["phases"],
        "fixes": REPORT["fixes"],
        "metrics": {
            "template_faq_remaining": templ,
            "service_word_counts": svc_words,
            "services_below_450": [k for k, v in svc_words.items() if v < 450],
            "og_missing_dims": og_missing,
            "sitemap_urls": len(re.findall(r"<loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))),
            "o_kompanii_exists": (ROOT / "o-kompanii" / "index.html").exists(),
        },
    }
    safe_write(
        Path(__file__).with_name("senior_seo_upgrade_report.json"),
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    )
    log("J", f"report written; template_faq_remaining={templ}; thin_services={report['metrics']['services_below_450']}")


def main() -> None:
    phase_a()
    phase_b()
    phase_c_about_and_reviews()
    phase_d_expand_services()
    phase_e_articles()
    phase_f_ux()
    phase_ghi()
    phase_j()
    print(json.dumps({"fixes": len(REPORT["fixes"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
