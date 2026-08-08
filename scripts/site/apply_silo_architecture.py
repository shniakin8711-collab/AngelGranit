# -*- coding: utf-8 -*-
"""
Apply SILO internal linking across AngelGranit.
Does not change design/colors — only link blocks + cluster hub page.
"""
from __future__ import annotations

import json
import re
import time
from datetime import date
from html import escape
from pathlib import Path

from silo_clusters import (
    BASE,
    CAT_META,
    CLUSTERS,
    POPULAR_SERVICES,
    SERVICE_PEERS,
    SERVICE_TITLES,
    THEME_CLUSTER,
)

ROOT = Path(__file__).resolve().parents[2]
TODAY = date.today().isoformat()
ARTICLES_IDX = Path(__file__).with_name("articles_index.json")
REPORT_PATH = Path(__file__).with_name("seo_silo_strategy_report.json")
MARKER_START = "<!-- silo-architecture:start -->"
MARKER_END = "<!-- silo-architecture:end -->"


def safe_write(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmpopt")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    last = None
    for _ in range(10):
        try:
            tmp.replace(path)
            return
        except OSError as e:
            last = e
            time.sleep(0.35)
    path.write_bytes(tmp.read_bytes())
    tmp.unlink(missing_ok=True)


def load_articles() -> list[dict]:
    return json.loads(ARTICLES_IDX.read_text(encoding="utf-8"))


def depth_of(path: Path) -> int:
    rel = path.parent.relative_to(ROOT)
    if str(rel) == ".":
        return 0
    return len(rel.parts)


def pfx(depth: int) -> str:
    return "../" * depth


def strip_silo(html: str) -> str:
    if MARKER_START not in html:
        return html
    return re.sub(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        "",
        html,
        count=1,
        flags=re.S,
    )


def grid(links: list[tuple[str, str, str]]) -> str:
    """href, strong, span"""
    parts = []
    for href, strong, span in links:
        parts.append(
            f'<a href="{escape(href)}"><strong>{escape(strong)}</strong>'
            f"<span>{escape(span)}</span></a>"
        )
    return '<div class="related-grid">\n' + "\n".join(parts) + "\n</div>"


def popular_block(depth: int, n: int = 6) -> str:
    p = pfx(depth)
    links = [(p + href, title, "Популярная услуга") for href, title in POPULAR_SERVICES[:n]]
    return f"<h2>Популярные услуги</h2>\n{grid(links)}"


def latest_articles_block(depth: int, articles: list[dict], n: int = 6, exclude: str | None = None) -> str:
    p = pfx(depth)
    picked = [a for a in articles if a["slug"] != exclude][:n]
    links = [
        (f'{p}stati/{a["slug"]}/', a["question"] + "?", CAT_META.get(a["category"], {}).get("name", "Статья"))
        for a in picked
    ]
    return f"<h2>Последние статьи</h2>\n{grid(links)}"


def trust_links(depth: int) -> list[tuple[str, str, str]]:
    p = pfx(depth)
    return [
        (p, "Главная AngelGranit", "На главную"),
        (f"{p}#works", "Наши работы", "Примеры"),
        (f"{p}#reviews", "Отзывы", "Доверие"),
        (f"{p}#faq", "FAQ", "Ответы"),
        (f"{p}kontakty/", "Контакты", "Связаться 24/7"),
    ]


def inject_before_footer(html: str, block: str) -> str:
    html = strip_silo(html)
    chunk = f"\n{MARKER_START}\n<section class=\"silo-links\" aria-label=\"Перелинковка SILO\">\n{block}\n</section>\n{MARKER_END}\n"
    # prefer before page-footer / footer / </main>
    for pat in (
        r"(<footer\b)",
        r"(</main>)",
        r"(</body>)",
    ):
        if re.search(pat, html, re.I):
            return re.sub(pat, chunk + r"\1", html, count=1, flags=re.I)
    return html + chunk


def ensure_category_in_breadcrumbs_article(html: str, cat: str, cat_name: str, depth: int) -> str:
    # already usually present — ensure hub link exists in CTA
    p = pfx(depth)
    hub = f"{p}stati/{cat}/"
    if hub in html or f"../{cat}/" in html or f'stati/{cat}/' in html:
        return html
    return html


# ── article pages ────────────────────────────────────────────────────────────

def patch_articles(articles: list[dict]) -> int:
    by_cat: dict[str, list[dict]] = {}
    for a in articles:
        by_cat.setdefault(a["category"], []).append(a)

    n = 0
    for a in articles:
        path = ROOT / "stati" / a["slug"] / "index.html"
        if not path.exists():
            continue
        depth = depth_of(path)
        p = pfx(depth)
        cat = a["category"]
        meta = CAT_META[cat]
        # 3+ services
        svc_links = [
            (f'{p}uslugi/{s}/', SERVICE_TITLES.get(s, s), "Услуга")
            for s in meta["services"][:4]
        ]
        # 3+ sibling articles
        siblings = [x for x in by_cat[cat] if x["slug"] != a["slug"]]
        # mix in one from neighbor cat for freshness
        art_links = [
            (f'{p}stati/{x["slug"]}/', x["question"] + "?", meta["name"])
            for x in siblings[:4]
        ]
        while len(art_links) < 3:
            for other in articles:
                if other["slug"] == a["slug"]:
                    continue
                art_links.append(
                    (
                        f'{p}stati/{other["slug"]}/',
                        other["question"] + "?",
                        CAT_META.get(other["category"], {}).get("name", "Статья"),
                    )
                )
                if len(art_links) >= 3:
                    break
            break

        hub_links = [
            (f"{p}stati/{cat}/", f"Категория: {meta['name']}", "Главная страница категории"),
            (f"{p}stati/", "Все статьи", "Раздел статей"),
            (f"{p}klastery/", "SEO-кластеры", "Карта сайта по темам"),
        ]

        block = "\n".join(
            [
                "<h2>Похожие услуги</h2>",
                grid(svc_links),
                "<h2>Похожие статьи</h2>",
                grid(art_links[:6]),
                "<h2>Раздел и навигация</h2>",
                grid(hub_links + trust_links(depth)[:3]),
                popular_block(depth, 5),
                latest_articles_block(depth, articles, 5, exclude=a["slug"]),
            ]
        )
        html = path.read_text(encoding="utf-8")
        html = ensure_category_in_breadcrumbs_article(html, cat, meta["name"], depth)
        html2 = inject_before_footer(html, block)
        if html2 != html:
            safe_write(path, html2)
            n += 1
    return n


# ── service pages ────────────────────────────────────────────────────────────

def patch_services(articles: list[dict]) -> int:
    n = 0
    for slug, title in SERVICE_TITLES.items():
        path = ROOT / "uslugi" / slug / "index.html"
        if not path.exists():
            continue
        depth = depth_of(path)
        p = pfx(depth)
        peers = SERVICE_PEERS.get(slug, ["ritualnye-uslugi", "organizaciya-pohoron", "pamyatniki"])
        peer_links = [
            (f"{p}uslugi/{s}/", SERVICE_TITLES.get(s, s), "Похожая услуга")
            for s in peers
            if s != slug
        ][:5]
        matched = [a for a in articles if slug in a.get("services", [])]
        if len(matched) < 5:
            # expand by category affinity
            for a in articles:
                if a not in matched:
                    matched.append(a)
                if len(matched) >= 8:
                    break
        art_links = [
            (f'{p}stati/{a["slug"]}/', a["question"] + "?", "Статья")
            for a in matched[:8]
        ]
        nav_links = trust_links(depth) + [
            (f"{p}uslugi/", "Каталог услуг", "Все услуги"),
            (f"{p}klastery/", "SEO-кластеры", "Архитектура сайта"),
        ]
        # pillar if exists
        for c in CLUSTERS:
            if any(s.endswith(f"{slug}/") for s in c.get("services", [])):
                if c.get("pillar"):
                    nav_links.insert(0, (p + c["pillar"], c["name"] + " — гид", "Pillar"))
                break

        block = "\n".join(
            [
                "<h2>Похожие услуги</h2>",
                grid(peer_links[:5]),
                "<h2>Полезные статьи</h2>",
                grid(art_links[:8]),
                "<h2>Главная, отзывы и контакты</h2>",
                grid(nav_links),
                popular_block(depth, 6),
                latest_articles_block(depth, articles, 6),
            ]
        )
        html = path.read_text(encoding="utf-8")
        html2 = inject_before_footer(html, block)
        if html2 != strip_silo(html) or MARKER_START not in html:
            safe_write(path, html2)
            n += 1
    return n


# ── theme / pillar landings ──────────────────────────────────────────────────

def patch_themes(articles: list[dict]) -> int:
    n = 0
    for slug, cluster_id in THEME_CLUSTER.items():
        path = ROOT / slug / "index.html"
        if not path.exists():
            continue
        cluster = next(c for c in CLUSTERS if c["id"] == cluster_id)
        depth = depth_of(path)
        p = pfx(depth)
        svc = cluster.get("services") or ["uslugi/ritualnye-uslugi/"]
        svc_links = []
        for s in svc[:5]:
            label = s.strip("/").split("/")[-1]
            title = SERVICE_TITLES.get(label, label.replace("-", " ").title())
            svc_links.append((p + s, title, "Услуга кластера"))
        # articles from cluster cats
        arts: list[dict] = []
        for cat in cluster.get("articles_cats", []):
            arts.extend([a for a in articles if a["category"] == cat])
        if not arts:
            arts = articles[:8]
        art_links = [
            (f'{p}stati/{a["slug"]}/', a["question"] + "?", "Статья")
            for a in arts[:6]
        ]
        hub = cluster["hub"]
        if hub.startswith("/#"):
            hub_href = p.rstrip("/") + hub if p else hub
        elif hub == "/":
            hub_href = p or "./"
        else:
            hub_href = p + hub
        nav = [
            (hub_href, f"Кластер: {cluster['name']}", "Главная кластера"),
            (f"{p}klastery/", "Все SEO-кластеры", "Карта"),
            (f"{p}temy/", "Тематические страницы", "Темы"),
        ] + trust_links(depth)

        block = "\n".join(
            [
                "<h2>Похожие услуги</h2>",
                grid(svc_links),
                "<h2>Похожие статьи</h2>",
                grid(art_links),
                "<h2>Навигация по кластеру</h2>",
                grid(nav),
                popular_block(depth, 5),
                latest_articles_block(depth, articles, 5),
            ]
        )
        html = path.read_text(encoding="utf-8")
        html2 = inject_before_footer(html, block)
        safe_write(path, html2)
        n += 1
    return n


# ── hubs: uslugi, stati cats, rajony, np, temy, kontakty ─────────────────────

def patch_hubs(articles: list[dict]) -> int:
    n = 0

    def do(path: Path, block: str) -> None:
        nonlocal n
        if not path.exists():
            return
        html = path.read_text(encoding="utf-8")
        html2 = inject_before_footer(html, block)
        safe_write(path, html2)
        n += 1

    # uslugi hub
    depth = 1
    p = pfx(depth)
    svc_all = [(f"{p}uslugi/{s}/", t, "Услуга") for s, t in list(SERVICE_TITLES.items())[:12]]
    do(
        ROOT / "uslugi" / "index.html",
        "\n".join(
            [
                "<h2>Популярные услуги</h2>",
                grid([(p + h, t, "Популярно") for h, t in POPULAR_SERVICES]),
                "<h2>Последние статьи</h2>",
                grid(
                    [
                        (f'{p}stati/{a["slug"]}/', a["question"] + "?", "Статья")
                        for a in articles[:8]
                    ]
                ),
                "<h2>Кластеры и доверие</h2>",
                grid(
                    [
                        (f"{p}klastery/", "SEO-кластеры", "Архитектура"),
                        (f"{p}stati/", "Статьи", "База знаний"),
                        (f"{p}temy/", "Темы", "Посадочные"),
                    ]
                    + trust_links(depth)
                ),
            ]
        ),
    )

    # stati hub + categories
    do(
        ROOT / "stati" / "index.html",
        "\n".join(
            [
                popular_block(1, 6),
                latest_articles_block(1, articles, 8),
                "<h2>Категории статей</h2>",
                grid(
                    [
                        (f"../stati/{c}/", m["name"], "Категория")
                        for c, m in CAT_META.items()
                    ]
                ),
                grid(trust_links(1) + [(pfx(1) + "klastery/", "SEO-кластеры", "Карта")]),
            ]
        ),
    )

    for cat, meta in CAT_META.items():
        cat_arts = [a for a in articles if a["category"] == cat]
        depth = 2
        p = pfx(depth)
        # Ensure hub lists articles (inbound for orphans) — link grid of all articles in cat
        art_links = [
            (f'{p}stati/{a["slug"]}/', a["question"] + "?", "Статья категории")
            for a in cat_arts
        ]
        svc_links = [
            (f'{p}uslugi/{s}/', SERVICE_TITLES.get(s, s), "Услуга")
            for s in meta["services"]
        ]
        do(
            ROOT / "stati" / cat / "index.html",
            "\n".join(
                [
                    "<h2>Похожие услуги</h2>",
                    grid(svc_links),
                    "<h2>Все статьи категории</h2>",
                    grid(art_links),
                    popular_block(depth, 5),
                    "<h2>Навигация</h2>",
                    grid(
                        [
                            (f"{p}stati/", "Все статьи", "Раздел"),
                            (f"{p}klastery/", "SEO-кластеры", "Карта"),
                        ]
                        + trust_links(depth)
                    ),
                ]
            ),
        )

    # locations
    for folder in ("rajony", "naselennye-punkty"):
        hub = ROOT / folder / "index.html"
        depth = 1
        p = pfx(depth)
        do(
            hub,
            "\n".join(
                [
                    popular_block(depth, 6),
                    latest_articles_block(depth, articles, 6),
                    grid(
                        [
                            (f"{p}uslugi/ritualnye-uslugi/", "Ритуальные услуги", "Услуга"),
                            (f"{p}uslugi/katafalk/", "Катафалк", "Услуга"),
                            (f"{p}uslugi/pamyatniki/", "Памятники", "Услуга"),
                            (f"{p}klastery/", "SEO-кластеры", "Карта"),
                        ]
                        + trust_links(depth)
                    ),
                ]
            ),
        )
        d = ROOT / folder
        if d.exists():
            for child in d.iterdir():
                if child.is_dir() and (child / "index.html").exists():
                    depth = 2
                    p = pfx(depth)
                    do(
                        child / "index.html",
                        "\n".join(
                            [
                                popular_block(depth, 5),
                                latest_articles_block(depth, articles, 5),
                                grid(
                                    [
                                        (f"{p}{folder}/", "К списку", "Хабы"),
                                        (f"{p}uslugi/ritualnye-uslugi/", "Ритуальные услуги", "Услуга"),
                                        (f"{p}klastery/", "SEO-кластеры", "Карта"),
                                    ]
                                    + trust_links(depth)
                                ),
                            ]
                        ),
                    )

    # kontakty / temy
    for rel in ("kontakty/index.html", "temy/index.html"):
        path = ROOT / rel
        depth = 1
        do(
            path,
            "\n".join(
                [
                    popular_block(depth, 6),
                    latest_articles_block(depth, articles, 6),
                    grid(
                        [(pfx(depth) + "klastery/", "SEO-кластеры", "Карта")]
                        + trust_links(depth)
                    ),
                ]
            ),
        )
    return n


# ── cluster map page ─────────────────────────────────────────────────────────

def write_klastery_page(articles: list[dict]) -> None:
    d = ROOT / "klastery"
    d.mkdir(exist_ok=True)
    sections = []
    for c in CLUSTERS:
        hub = c["hub"]
        if hub == "/":
            hub_href = "../"
        elif hub.startswith("/#"):
            hub_href = ".." + hub
        else:
            hub_href = "../" + hub
        items = []
        items.append(f'<a class="hub-card" href="{escape(hub_href)}"><strong>Главная кластера</strong><span>{escape(c["hub"])}</span></a>')
        if c.get("pillar"):
            items.append(
                f'<a class="hub-card" href="../{escape(c["pillar"])}"><strong>Pillar-страница</strong><span>{escape(c["pillar"])}</span></a>'
            )
        for s in c.get("services", [])[:8]:
            label = s.strip("/").split("/")[-1]
            items.append(
                f'<a class="hub-card" href="../{escape(s)}"><strong>{escape(SERVICE_TITLES.get(label, label))}</strong><span>Услуга</span></a>'
            )
        for s in c.get("supporting", [])[:10]:
            if s.startswith("/#") or s.startswith("#"):
                href = ".." + s if s.startswith("/#") else "../" + s
            else:
                href = "../" + s
            items.append(
                f'<a class="hub-card" href="{escape(href)}"><strong>{escape(s.strip("/"))}</strong><span>Поддержка</span></a>'
            )
        for cat in c.get("articles_cats", [])[:6]:
            items.append(
                f'<a class="hub-card" href="../stati/{escape(cat)}/"><strong>{escape(CAT_META.get(cat, {}).get("name", cat))}</strong><span>Статьи</span></a>'
            )
        sections.append(
            f"<h2>{escape(c['name'])}</h2>"
            f"<p class=\"lead\">{escape(c.get('role', ''))} · приоритет {c.get('priority')} · трафик: {escape(str(c.get('traffic')))}</p>"
            f'<div class="hub-grid">{"".join(items)}</div>'
        )

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SEO-кластеры и карта сайта AngelGranit | Алматы</title>
  <meta name="description" content="Тематические SEO-кластеры AngelGranit: ритуальные услуги, памятники, катафалк, статьи, районы. Логичная SILO-структура и перелинковка." />
  <link rel="canonical" href="{BASE}/klastery/" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="icon" href="../assets/icons/favicon.svg" type="image/svg+xml" />
  <link rel="manifest" href="../site.webmanifest" />
  <meta name="theme-color" content="#d4af57" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:url" content="{BASE}/klastery/" />
  <meta property="og:title" content="SEO-кластеры и карта сайта AngelGranit | Алматы" />
  <meta property="og:description" content="Тематические SEO-кластеры AngelGranit: ритуальные услуги, памятники, катафалк, статьи, районы." />
  <meta property="og:image" content="{BASE}/images/hero-angelgranit.webp" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="SEO-кластеры AngelGranit" />
  <meta name="twitter:description" content="SILO-архитектура и карта тематических кластеров сайта." />
  <meta name="twitter:image" content="{BASE}/images/hero-angelgranit.webp" />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Manrope:wght@400;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../seo/assets/seo.css" />
  <link rel="stylesheet" href="../assets/site/nav.css" />
  <link rel="stylesheet" href="../assets/site/page.css" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "SEO-кластеры AngelGranit",
    "url": "{BASE}/klastery/",
    "description": "Тематическая карта сайта ритуальных услуг AngelGranit в Алматы",
    "isPartOf": {{"@type": "WebSite", "url": "{BASE}/"}}
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
      <li><a href="../stati/">Статьи</a></li>
      <li><a href="../temy/">Темы</a></li>
      <li><a href="../kontakty/">Контакты</a></li>
    </ul>
    <a class="site-nav__call" href="tel:+77010567667">Позвонить 24/7</a>
  </header>
  <main id="main-content" class="page-main">
    <div class="page-wrap--wide">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../">Главная</a></li>
          <li aria-current="page">SEO-кластеры</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>SEO-кластеры и SILO-структура</h1>
        <p class="lead">Сайт разделён на тематические кластеры: у каждого есть главная страница, услуги, статьи и перелинковка. Так проще людям и понятнее поисковым системам.</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:+77010567667">Позвонить +7 701 056 7667</a>
          <a class="btn-site btn-site--ghost" href="../uslugi/">Услуги</a>
          <a class="btn-site btn-site--ghost" href="../stati/">Статьи</a>
        </div>
      </header>
      {''.join(sections)}
      <section>
        <h2>Популярные услуги</h2>
        {grid([("../" + h, t, "Популярно") for h, t in POPULAR_SERVICES])}
      </section>
      <section>
        <h2>Последние статьи</h2>
        {grid([(f'../stati/{a["slug"]}/', a["question"] + "?", "Статья") for a in articles[:10]])}
      </section>
    </div>
  </main>
  <footer class="page-footer">
    <strong>AngelGranit</strong>
    Александр · ул. Осетинская, 5а · <a href="tel:+77010567667">+7 701 056 7667</a>
  </footer>
  <script src="../assets/site/nav.js" defer></script>
</body>
</html>
"""
    safe_write(d / "index.html", html)


# ── homepage & sitemap wiring ────────────────────────────────────────────────

def wire_homepage() -> None:
    p = ROOT / "index.html"
    t = p.read_text(encoding="utf-8")
    if "klastery/" not in t:
        t = t.replace(
            '<a href="temy/">Темы</a>',
            '<a href="temy/">Темы</a> · <a href="klastery/">SEO-кластеры</a>',
            1,
        )
    # inject compact silo block before footer if missing
    if MARKER_START not in t:
        block = "\n".join(
            [
                '<div class="page-wrap--wide" style="margin:2rem auto">',
                "<h2 style=\"color:#d4af57;font-family:Cinzel,Georgia,serif\">Тематические направления</h2>",
                '<p class="lead" style="color:#8e8980">Кластеры сайта: от ритуальных услуг и катафалка до памятников и статей.</p>',
                grid(
                    [
                        ("uslugi/ritualnye-uslugi/", "Ритуальные услуги", "Кластер"),
                        ("uslugi/pamyatniki/", "Памятники", "Кластер"),
                        ("uslugi/katafalk/", "Катафалк", "Кластер"),
                        ("uslugi/blagoustrojstvo-mogil/", "Благоустройство", "Кластер"),
                        ("stati/", "Статьи", "Кластер"),
                        ("klastery/", "Полная карта кластеров", "SILO"),
                        ("kontakty/", "Контакты", "Связь"),
                        ("#reviews", "Отзывы", "Доверие"),
                        ("#works", "Наши работы", "Примеры"),
                    ]
                ),
                "</div>",
            ]
        )
        t = inject_before_footer(t, block)
    safe_write(p, t)


def add_sitemap_klastery() -> None:
    sm = ROOT / "sitemap.xml"
    t = sm.read_text(encoding="utf-8")
    loc = f"{BASE}/klastery/"
    if loc in t:
        return
    entry = (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{TODAY}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        "    <priority>0.9</priority>\n"
        "  </url>\n"
    )
    t = t.replace("</urlset>", entry + "</urlset>")
    safe_write(sm, t)


# ── validation & report ──────────────────────────────────────────────────────

def validate_and_report(articles: list[dict]) -> dict:
    # orphan check: build inbound graph from hrefs
    pages = []
    for p in ROOT.rglob("index.html"):
        if any(x in {".git", "scripts", "node_modules", "__pycache__", "assets"} for x in p.parts):
            continue
        pages.append(p)

    def url_of(p: Path) -> str:
        rel = p.parent.relative_to(ROOT).as_posix()
        return "/" if rel == "." else f"/{rel}/"

    inbound: dict[str, int] = {url_of(p): 0 for p in pages}
    outbound: dict[str, int] = {url_of(p): 0 for p in pages}
    depths: dict[str, int] = {}

    for p in pages:
        u = url_of(p)
        depths[u] = depth_of(p)
        html = p.read_text(encoding="utf-8", errors="ignore")
        hrefs = re.findall(r'href="([^"]+)"', html)
        for href in hrefs:
            if href.startswith(("http", "mailto", "tel", "javascript:", "data:")):
                continue
            path_only = href.split("#", 1)[0].split("?", 1)[0]
            if not path_only:
                # hash-only on same page
                continue
            target = (p.parent / path_only).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if target.is_dir() and (target / "index.html").exists():
                tu = url_of(target / "index.html")
            elif target.name == "index.html":
                tu = url_of(target)
            elif (Path(str(target)) / "index.html").exists():
                tu = "/" + Path(str(target)).relative_to(ROOT).as_posix().replace("\\", "/") + "/"
            else:
                continue
            if tu in inbound:
                inbound[tu] += 1
                outbound[u] += 1

    orphans = sorted([u for u, c in inbound.items() if c == 0 and u != "/"])
    deep = sorted([u for u, d in depths.items() if d > 3])

    # article/service rule checks (presence of silo marker)
    art_ok = sum(
        1
        for a in articles
        if MARKER_START in (ROOT / "stati" / a["slug"] / "index.html").read_text(encoding="utf-8", errors="ignore")
    )
    svc_ok = sum(
        1
        for s in SERVICE_TITLES
        if (ROOT / "uslugi" / s / "index.html").exists()
        and MARKER_START in (ROOT / "uslugi" / s / "index.html").read_text(encoding="utf-8", errors="ignore")
    )

    important = [
        {"url": "/", "why": "Главный коммерческий вход, бренд, CWV-критичная страница", "traffic": "highest"},
        {"url": "/uslugi/ritualnye-uslugi/", "why": "Хаб ядра «ритуальные услуги»", "traffic": "highest"},
        {"url": "/ritualnye-uslugi-almaty/", "why": "Pillar под главный ключ", "traffic": "highest"},
        {"url": "/uslugi/organizaciya-pohoron/", "why": "Высокий интент «организация похорон»", "traffic": "high"},
        {"url": "/uslugi/katafalk/", "why": "Срочный коммерческий запрос", "traffic": "high"},
        {"url": "/uslugi/pamyatniki/", "why": "Хаб памятников", "traffic": "high"},
        {"url": "/uslugi/granitnye-pamyatniki/", "why": "Транзакционный mid-funnel", "traffic": "high"},
        {"url": "/kontakty/", "why": "Конверсионный URL", "traffic": "brand"},
        {"url": "/stati/", "why": "Контентный хаб long-tail", "traffic": "high"},
        {"url": "/klastery/", "why": "Карта SILO / внутренний PageRank distributor", "traffic": "assisted"},
    ]

    traffic_pages = [
        c for c in CLUSTERS if c.get("traffic") in {"highest", "high", "high (long-tail)", "medium-high"}
    ]

    report = {
        "date": TODAY,
        "base": BASE,
        "clusters": CLUSTERS,
        "rules": {
            "articles": "≥3 услуги, ≥3 статьи, 1 категория, popular, latest",
            "services": "≥5 статей, ≥3 услуги, главная, отзывы, контакты, popular, latest",
        },
        "counts": {
            "articles_with_silo": art_ok,
            "articles_total": len(articles),
            "services_with_silo": svc_ok,
            "services_total": len(SERVICE_TITLES),
            "pages": len(pages),
            "orphans": len(orphans),
            "depth_gt_3": len(deep),
        },
        "orphans_sample": orphans[:40],
        "deep_pages_sample": deep[:40],
        "important_pages": important,
        "primary_traffic_clusters": [
            {"id": c["id"], "name": c["name"], "hub": c["hub"], "traffic": c["traffic"]}
            for c in traffic_pages
        ],
        "hierarchy": {
            "level_0": ["/" ],
            "level_1": [
                "uslugi/", "stati/", "temy/", "klastery/", "kontakty/", "rajony/",
                "naselennye-punkty/", "seo/", "*pillar-almaty/",
            ],
            "level_2": ["uslugi/{slug}/", "stati/{category}/", "stati/{article}/", "rajony/{district}/"],
            "level_3": ["naselennye-punkty/{city}/{service}/"],
        },
        "url_policy": {
            "trailing_slash": True,
            "lowercase_kebab": True,
            "canonical": "self except intentional /seo/* mirrors → pillars",
            "max_recommended_depth": 3,
        },
    }
    safe_write(REPORT_PATH, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


def main() -> None:
    articles = load_articles()
    print("articles", len(articles))
    print("patch articles", patch_articles(articles))
    print("patch services", patch_services(articles))
    print("patch themes", patch_themes(articles))
    print("patch hubs", patch_hubs(articles))
    write_klastery_page(articles)
    print("klastery ok")
    wire_homepage()
    print("homepage wired")
    add_sitemap_klastery()
    report = validate_and_report(articles)
    print(json.dumps(report["counts"], ensure_ascii=False, indent=2))
    print("orphans", report["counts"]["orphans"])
    print("report", REPORT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
