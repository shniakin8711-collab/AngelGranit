# -*- coding: utf-8 -*-
"""Final site-wide quality pass: SEO, a11y, schema hubs, sitemap, meta cleanup."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
import time
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://shniakin8711-collab.github.io/AngelGranit"
TODAY = date.today().isoformat()
SKIP_DIRS = {".git", ".idea", "scripts", "node_modules", "__pycache__", "assets"}
PHONE = "+7 701 056 7667"
PHONE_TEL = "+77010567667"
ADDRESS = "ул. Осетинская, 5а"
REPORT: dict = {"fixes": [], "counts": {}}


def pages() -> list[Path]:
    out = []
    for p in ROOT.rglob("index.html"):
        if any(x in SKIP_DIRS for x in p.parts):
            continue
        out.append(p)
    # include 404
    if (ROOT / "404.html").exists():
        out.append(ROOT / "404.html")
    return out


def depth_of(p: Path) -> int:
    if p.name == "404.html":
        return 0
    rel = p.parent.relative_to(ROOT)
    if str(rel) == ".":
        return 0
    return len(rel.parts)


def prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def page_url(p: Path) -> str:
    if p.name == "404.html":
        return f"{BASE}/404.html"
    rel = p.parent.relative_to(ROOT).as_posix()
    return f"{BASE}/" if rel == "." else f"{BASE}/{rel}/"


def safe_write(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmpopt")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    last = None
    for _ in range(8):
        try:
            tmp.replace(path)
            return
        except OSError as e:
            last = e
            time.sleep(0.35)
    # fallback copy
    try:
        path.write_bytes(tmp.read_bytes())
        tmp.unlink(missing_ok=True)
    except OSError:
        if last:
            raise last
        raise


def record(msg: str) -> None:
    REPORT["fixes"].append(msg)


# ── shared CSS / JS ──────────────────────────────────────────────────────────

def enhance_shared_css() -> None:
    nav = ROOT / "assets" / "site" / "nav.css"
    page = ROOT / "assets" / "site" / "page.css"
    extra_nav = """
/* Final optimize: a11y + motion (no visual redesign) */
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0.75rem;
  z-index: 10000;
  padding: 0.65rem 1rem;
  background: var(--gold, #d4af57);
  color: #050505;
  font-family: var(--font-body, system-ui, sans-serif);
  font-weight: 700;
  text-decoration: none;
  border-radius: var(--radius, 4px);
}
.skip-link:focus {
  left: 0.75rem;
  outline: 2px solid #fff;
  outline-offset: 2px;
}
.site-nav a:focus-visible,
.site-nav button:focus-visible,
.btn-site:focus-visible,
.hub-card:focus-visible,
.related-grid a:focus-visible {
  outline: 2px solid var(--gold, #d4af57);
  outline-offset: 2px;
}
@media (prefers-reduced-motion: reduce) {
  .site-nav,
  .site-nav__menu,
  .site-nav__dropdown {
    transition: none !important;
  }
}
"""
    text = nav.read_text(encoding="utf-8")
    if ".skip-link" not in text:
        safe_write(nav, text.rstrip() + "\n" + extra_nav)
        record("nav.css: skip-link + focus-visible + reduced-motion")

    extra_page = """
/* Final optimize: readability + touch + a11y */
img { max-width: 100%; height: auto; }
.page-article h3 {
  margin: 1.35rem 0 0.55rem;
  font-family: var(--font-display, Georgia, serif);
  font-size: 1.05rem;
  color: #e8d9a8;
}
.page-faq summary:focus-visible {
  outline: 2px solid var(--gold, #d4af57);
  outline-offset: 2px;
}
@media (max-width: 720px) {
  .btn-site { min-height: 2.75rem; }
  .page-cta { gap: 0.65rem; }
}
@media (prefers-reduced-motion: reduce) {
  html:focus-within { scroll-behavior: auto; }
}
"""
    ptext = page.read_text(encoding="utf-8")
    if "Final optimize: readability" not in ptext:
        safe_write(page, ptext.rstrip() + "\n" + extra_page)
        record("page.css: img fluid + h3 + mobile CTA + reduced-motion")


def enhance_nav_js() -> None:
    path = ROOT / "assets" / "site" / "nav.js"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if "Escape" in current and "aria-controls" in current:
        return
    content = """(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  var nav = qs("[data-site-nav]");
  if (!nav) return;

  var toggle = qs("[data-nav-toggle]", nav);
  var menu = qs(".site-nav__menu", nav);
  if (menu && !menu.id) menu.id = "site-nav-menu";
  if (toggle && menu && !toggle.getAttribute("aria-controls")) {
    toggle.setAttribute("aria-controls", menu.id);
  }

  function closeMenu() {
    nav.classList.remove("is-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
    qsa("[data-dropdown]", nav).forEach(function (item) {
      item.classList.remove("is-open");
      var btn = qs("button", item);
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = !nav.classList.contains("is-open");
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  qsa("[data-dropdown]", nav).forEach(function (item) {
    var btn = qs("button", item);
    if (!btn) return;
    if (!btn.getAttribute("aria-expanded")) btn.setAttribute("aria-expanded", "false");
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var open = item.classList.contains("is-open");
      qsa("[data-dropdown]", nav).forEach(function (other) {
        other.classList.remove("is-open");
        var ob = qs("button", other);
        if (ob) ob.setAttribute("aria-expanded", "false");
      });
      if (!open) {
        item.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  document.addEventListener("click", function (e) {
    if (!nav.contains(e.target)) closeMenu();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenu();
  });

  var wa = "https://wa.me/77010567667?text=" + encodeURIComponent("Здравствуйте! AngelGranit — нужна консультация.");
  qsa("[data-wa]", document).forEach(function (el) {
    el.href = wa;
    if (!el.getAttribute("rel")) el.setAttribute("rel", "noopener noreferrer");
    if (!el.getAttribute("target")) el.setAttribute("target", "_blank");
  });
})();
"""
    safe_write(path, content)
    record("nav.js: Escape close, aria-expanded, aria-controls, WA rel")


# ── homepage LCP / meta ──────────────────────────────────────────────────────

def fix_homepage() -> None:
    p = ROOT / "index.html"
    t = p.read_text(encoding="utf-8")
    orig = t

    # LCP: WebP as primary img src; PNG as additional source fallback
    old_hero = (
        '<source srcset="images/hero-angelgranit.webp" type="image/webp" />\n'
        '        <img src="images/hero-angelgranit.png" alt="Ритуальные услуги Алматы 24/7 — организация похорон AngelGranit" '
        'width="1024" height="408" decoding="async" fetchpriority="high" />'
    )
    new_hero = (
        '<source srcset="images/hero-angelgranit.webp" type="image/webp" />\n'
        '        <source srcset="images/hero-angelgranit.png" type="image/png" />\n'
        '        <img src="images/hero-angelgranit.webp" alt="Ритуальные услуги Алматы 24/7 — организация похорон AngelGranit" '
        'width="1024" height="408" fetchpriority="high" decoding="sync" />'
    )
    if old_hero in t:
        t = t.replace(old_hero, new_hero, 1)
    else:
        # looser replace
        t = re.sub(
            r'(<source srcset="images/hero-angelgranit\.webp"[^/]*/>)\s*'
            r'<img src="images/hero-angelgranit\.png"([^>]*)>',
            r'\1\n        <source srcset="images/hero-angelgranit.png" type="image/png" />\n'
            r'        <img src="images/hero-angelgranit.webp"\2>',
            t,
            count=1,
        )
        t = t.replace(
            'images/hero-angelgranit.webp" alt="Ритуальные услуги Алматы 24/7 — организация похорон AngelGranit" width="1024" height="408" decoding="async" fetchpriority="high"',
            'images/hero-angelgranit.webp" alt="Ритуальные услуги Алматы 24/7 — организация похорон AngelGranit" width="1024" height="408" fetchpriority="high" decoding="sync"',
            1,
        )

    if 'name="referrer"' not in t:
        t = t.replace(
            '<meta name="robots"',
            '<meta name="referrer" content="strict-origin-when-cross-origin" />\n  <meta name="robots"',
            1,
        )

    t = t.replace('href="#top">Перейти к содержанию</a>', 'href="#main-content">Перейти к содержанию</a>', 1)
    if 'id="main-content"' not in t:
        t = t.replace('<section class="hero" id="top"', '<section class="hero" id="top" data-main-start', 1)
        t = t.replace(
            '<section class="hero" id="top" data-main-start',
            '<main id="main-content">\n  <section class="hero" id="top"',
            1,
        )
        # close before fab-wa (outside main chrome)
        if 'id="fab-wa"' in t and t.count("</main>") == 0:
            t = re.sub(
                r"(\n\s*<a class=\"fab-wa\")",
                r"\n  </main>\1",
                t,
                count=1,
            )

    if "deploy-bump:" in t:
        t = re.sub(
            r"<!-- deploy-bump: [^>]+-->",
            f"<!-- deploy-bump: {TODAY}-final-optimize -->",
            t,
            count=1,
        )

    if t != orig:
        tmp = p.with_suffix(".html.optwrite")
        safe_write(tmp, t)
        tmp.replace(p)
        record("homepage: LCP WebP, referrer, main landmark, skip target")


# ── meta / description cleanup ───────────────────────────────────────────────

def clean_duplicate_phone_descriptions() -> int:
    n = 0
    phone_re = re.compile(re.escape(PHONE))
    for p in pages():
        if p.name == "404.html":
            continue
        t = p.read_text(encoding="utf-8")
        m = re.search(r'<meta name="description" content="([^"]*)"', t)
        if not m:
            continue
        desc = m.group(1)
        # collapse repeated address/phone tails
        parts = desc.split(". ")
        seen = set()
        cleaned_parts = []
        for part in parts:
            key = re.sub(r"\s+", " ", part.strip().lower())
            if key in seen:
                continue
            seen.add(key)
            cleaned_parts.append(part.strip())
        new_desc = ". ".join(cleaned_parts)
        new_desc = re.sub(r"(" + re.escape(PHONE) + r")(\s*[.,]?\s*.*?\1)+", r"\1", new_desc)
        # specific kontakty junk
        new_desc = re.sub(
            r"(AngelGranit,\s*" + re.escape(ADDRESS) + r",\s*" + re.escape(PHONE) + r"\.?\s*)+",
            f"AngelGranit, {ADDRESS}, {PHONE}.",
            new_desc,
        )
        if new_desc != desc and len(new_desc) >= 70:
            t2 = t.replace(
                f'<meta name="description" content="{desc}"',
                f'<meta name="description" content="{new_desc}"',
                1,
            )
            # sync og/twitter if they matched old
            t2 = t2.replace(f'content="{desc}"', f'content="{new_desc}"')
            if t2 != t:
                safe_write(p, t2)
                n += 1
    if n:
        record(f"deduped descriptions on {n} pages")
    return n


# ── skip links + main id ─────────────────────────────────────────────────────

def inject_skip_and_main() -> int:
    n = 0
    for p in pages():
        if p.name == "index.html" and p.parent == ROOT:
            continue  # homepage handled separately
        t = p.read_text(encoding="utf-8")
        orig = t
        if "skip-link" not in t:
            t = re.sub(
                r"<body([^>]*)>",
                r'<body\1>\n  <a class="skip-link" href="#main-content">Перейти к содержанию</a>',
                t,
                count=1,
                flags=re.I,
            )
        if 'id="main-content"' not in t:
            if re.search(r"<main\b", t, re.I):

                def _main_id(m: re.Match[str]) -> str:
                    attrs = m.group(1) or ""
                    if re.search(r"\bid=", attrs):
                        return m.group(0)
                    return f"<main id=\"main-content\"{attrs}>"

                t = re.sub(r"<main(\s[^>]*)?>", _main_id, t, count=1, flags=re.I)
            else:
                # after first site header
                t = re.sub(
                    r"(</header>\s*)",
                    r'\1<main id="main-content">\n',
                    t,
                    count=1,
                    flags=re.I,
                )
                if 'id="main-content"' in t and "</main>" not in t:
                    if re.search(r"<footer\b", t, re.I):
                        t = re.sub(r"(<footer\b)", r"</main>\n\1", t, count=1, flags=re.I)
                    else:
                        t = re.sub(r"</body>", "</main>\n</body>", t, count=1, flags=re.I)

        # aria-controls on toggles
        if "data-nav-toggle" in t and 'aria-controls="' not in t:
            t = t.replace(
                'data-nav-toggle aria-expanded="false"',
                'data-nav-toggle aria-expanded="false" aria-controls="site-nav-menu"',
            )
            t = t.replace(
                'data-nav-toggle aria-expanded="false">',
                'data-nav-toggle aria-expanded="false" aria-controls="site-nav-menu">',
            )
            t = re.sub(
                r'(<ul class="site-nav__menu")(?![^>]*\bid=)',
                r'\1 id="site-nav-menu"',
                t,
                count=1,
            )

        if 'name="referrer"' not in t and p.suffix == ".html":
            t = re.sub(
                r"(<meta charset=\"UTF-8\"\s*/?>)",
                r'\1\n  <meta name="referrer" content="strict-origin-when-cross-origin" />',
                t,
                count=1,
                flags=re.I,
            )

        if t != orig:
            safe_write(p, t)
            n += 1
    if n:
        record(f"skip-link/main/referrer on {n} pages")
    return n


# ── hub schemas ──────────────────────────────────────────────────────────────

HUB_SCHEMA_PAGES = {
    "kontakty/index.html": ("ContactPage", "Контакты AngelGranit"),
    "temy/index.html": ("CollectionPage", "Тематические страницы AngelGranit"),
    "stati/index.html": ("CollectionPage", "Статьи AngelGranit"),
    "seo/index.html": ("CollectionPage", "Справочник AngelGranit"),
    "uslugi/index.html": ("CollectionPage", "Каталог услуг AngelGranit"),
    "rajony/index.html": ("CollectionPage", "Районы Алматы — AngelGranit"),
    "naselennye-punkty/index.html": ("CollectionPage", "Населённые пункты — AngelGranit"),
}


def schema_block(url: str, page_type: str, name: str, description: str) -> str:
    graph = {
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
                "@type": page_type,
                "@id": f"{url}#webpage",
                "url": url,
                "name": name,
                "description": description,
                "isPartOf": {"@id": f"{BASE}/#website"},
                "about": {"@id": f"{BASE}/#business"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": name, "item": url},
                ],
            },
        ],
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(graph, ensure_ascii=False, indent=2)
        + "\n  </script>"
    )


def add_missing_schemas() -> int:
    n = 0
    # known hubs
    for rel, (ptype, name) in HUB_SCHEMA_PAGES.items():
        p = ROOT / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        if "application/ld+json" in t:
            continue
        desc_m = re.search(r'<meta name="description" content="([^"]*)"', t)
        title_m = re.search(r"<title>(.*?)</title>", t, re.S)
        desc = desc_m.group(1) if desc_m else name
        title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else name
        url = page_url(p)
        block = schema_block(url, ptype, title, desc)
        t2 = re.sub(r"</head>", f"  {block}\n</head>", t, count=1, flags=re.I)
        if t2 != t:
            safe_write(p, t2)
            n += 1
            record(f"schema → {rel}")

    # stati category hubs
    stati = ROOT / "stati"
    if stati.exists():
        for child in stati.iterdir():
            if not child.is_dir():
                continue
            p = child / "index.html"
            if not p.exists():
                continue
            t = p.read_text(encoding="utf-8")
            if "application/ld+json" in t:
                continue
            # only category hubs (not deep articles) — depth 2: stati/cat/
            if len(child.relative_to(ROOT).parts) != 2:
                continue
            # articles live in stati/cat/slug/ — category index is stati/cat/index.html
            # check if this is a listing hub: has hub-grid or many links
            if "hub-grid" not in t and "hub-card" not in t and "article-list" not in t:
                # still add CollectionPage for category indexes
                pass
            desc_m = re.search(r'<meta name="description" content="([^"]*)"', t)
            title_m = re.search(r"<title>(.*?)</title>", t, re.S)
            desc = desc_m.group(1) if desc_m else child.name
            title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else child.name
            url = page_url(p)
            block = schema_block(url, "CollectionPage", title, desc)
            t2 = re.sub(r"</head>", f"  {block}\n</head>", t, count=1, flags=re.I)
            safe_write(p, t2)
            n += 1
            record(f"schema → stati/{child.name}/")
    return n


# ── SEO mirror H1 uniqueness ─────────────────────────────────────────────────

def unique_mirror_h1() -> int:
    n = 0
    seo = ROOT / "seo"
    for child in seo.iterdir():
        if not child.is_dir() or not (child / "index.html").exists():
            continue
        p = child / "index.html"
        t = p.read_text(encoding="utf-8")
        can = re.search(r'rel="canonical" href="([^"]+)"', t)
        if not can:
            continue
        self_url = f"{BASE}/seo/{child.name}/"
        if can.group(1).rstrip("/") == self_url.rstrip("/"):
            continue
        h1m = re.search(r"<h1([^>]*)>(.*?)</h1>", t, re.S)
        if not h1m:
            continue
        h1 = re.sub(r"<[^>]+>", "", h1m.group(2))
        h1 = re.sub(r"\s+", " ", h1).strip()
        if "справочник" in h1.lower():
            continue
        new_h1 = f"{h1} — справочник"
        t2 = t.replace(h1m.group(0), f"<h1{h1m.group(1)}>{escape(new_h1)}</h1>", 1)
        if t2 != t:
            safe_write(p, t2)
            n += 1
    if n:
        record(f"unique H1 on {n} SEO mirrors")
    return n


# ── cross-links ──────────────────────────────────────────────────────────────

def strengthen_crosslinks() -> None:
    # uslugi hub → temy
    for rel in ("uslugi/index.html", "stati/index.html", "kontakty/index.html"):
        p = ROOT / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        depth = depth_of(p)
        href = f"{prefix(depth)}temy/"
        if "temy/" in t:
            continue
        # add near CTA or footer links
        if "page-cta" in t:
            t2 = t.replace(
                "</div>\n      </header>",
                f'          <a class="btn-site btn-site--ghost" href="{href}">Темы</a>\n        </div>\n      </header>',
                1,
            )
            if t2 == t:
                t2 = t.replace(
                    'href="../kontakty/">Контакты</a>',
                    f'href="../kontakty/">Контакты</a></li>\n      <li><a href="{href}">Темы</a>',
                    1,
                )
            if t2 != t:
                safe_write(p, t2)
                record(f"crosslink temy → {rel}")

    # homepage seo-hub already has temy from previous work — ensure key themes
    home = ROOT / "index.html"
    ht = home.read_text(encoding="utf-8")
    if "temy/" in ht and "kladbishcha-almaty" not in ht:
        # add a few high-value theme links in seo-hub if present
        if 'href="temy/"' in ht or "href=\"temy/\"" in ht:
            snippet = (
                '<a href="kladbishcha-almaty/">Кладбища Алматы</a>\n'
                '        <a href="pravoslavnye-pohorony-almaty/">Православные похороны</a>\n'
                '        <a href="proshchalnyj-zal-almaty/">Прощальный зал</a>\n'
            )
            if 'href="gruz-200-almaty/"' in ht:
                ht2 = ht.replace(
                    'href="gruz-200-almaty/"',
                    'href="gruz-200-almaty/"',
                    1,
                )
                # inject after temy link block
                ht2 = re.sub(
                    r'(<a href="temy/"[^>]*>.*?</a>)',
                    r"\1\n        " + snippet.strip(),
                    ht,
                    count=1,
                    flags=re.S,
                )
                if ht2 != ht:
                    safe_write(home, ht2)
                    record("homepage: extra theme crosslinks")


# ── 404 / manifest ───────────────────────────────────────────────────────────

def fix_404_and_manifest() -> None:
    p = ROOT / "404.html"
    t = p.read_text(encoding="utf-8")
    if "temy/" not in t:
        t = t.replace(
            '<a class="btn-site btn-site--ghost" href="stati/">Статьи</a>',
            '<a class="btn-site btn-site--ghost" href="stati/">Статьи</a>\n'
            '        <a class="btn-site btn-site--ghost" href="temy/">Темы</a>',
            1,
        )
        safe_write(p, t)
        record("404: link to temy")

    man = ROOT / "site.webmanifest"
    data = json.loads(man.read_text(encoding="utf-8"))
    # Google: prefer separate purpose values
    data["icons"] = [
        {
            "src": "/AngelGranit/assets/icons/icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any",
        },
        {
            "src": "/AngelGranit/assets/icons/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any",
        },
        {
            "src": "/AngelGranit/assets/icons/icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "maskable",
        },
        {
            "src": "/AngelGranit/assets/icons/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable",
        },
    ]
    data["id"] = "/AngelGranit/"
    man.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    record("manifest: separate any/maskable icons + id")


# ── seo hub meta polish ──────────────────────────────────────────────────────

def polish_seo_hub() -> None:
    p = ROOT / "seo" / "index.html"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    # dedupe twitter:card
    while t.count('name="twitter:card"') > 1:
        # remove second occurrence
        first = t.find('name="twitter:card"')
        second = t.find('name="twitter:card"', first + 1)
        if second < 0:
            break
        # remove the whole meta tag around second
        start = t.rfind("<meta", 0, second)
        end = t.find(">", second) + 1
        t = t[:start] + t[end:]
    # sync og:title with title
    tm = re.search(r"<title>(.*?)</title>", t, re.S)
    if tm:
        title = re.sub(r"\s+", " ", tm.group(1)).strip()
        t = re.sub(
            r'(property="og:title" content=")[^"]*(")',
            rf"\1{title}\2",
            t,
            count=1,
        )
    safe_write(p, t)
    record("seo hub: dedupe twitter + OG title sync")


# ── sitemap ──────────────────────────────────────────────────────────────────

def rebuild_sitemap() -> int:
    urls: list[tuple[str, str]] = [(f"{BASE}/", "1.0")]

    def add(loc: str, pr: str) -> None:
        urls.append((loc, pr))

    # all index.html except intentional mirrors & assets
    for p in ROOT.rglob("index.html"):
        if any(x in SKIP_DIRS for x in p.parts):
            continue
        rel = p.parent.relative_to(ROOT).as_posix()
        loc = f"{BASE}/" if rel == "." else f"{BASE}/{rel}/"

        # skip SEO mirrors that canonicalize away
        if rel.startswith("seo/") and rel != "seo":
            html = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'rel="canonical" href="([^"]+)"', html)
            self_url = loc
            if m and m.group(1).rstrip("/") != self_url.rstrip("/"):
                continue

        parts = [] if rel == "." else rel.split("/")
        if not parts:
            pr = "1.0"
        elif parts[0] == "uslugi":
            pr = "0.95" if len(parts) == 1 else "0.9"
        elif parts[0] == "stati":
            pr = "0.9" if len(parts) == 1 else ("0.85" if len(parts) == 2 else "0.75")
        elif parts[0] in {"rajony", "naselennye-punkty"}:
            pr = "0.85" if len(parts) == 1 else "0.8"
        elif parts[0] == "kontakty":
            pr = "0.9"
        elif parts[0] == "seo":
            pr = "0.7"
        elif parts[0] == "temy":
            pr = "0.9"
        else:
            pr = "0.85"
        add(loc, pr)

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
            f"    <lastmod>{TODAY}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{pr}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    safe_write(ROOT / "sitemap.xml", "\n".join(lines) + "\n")
    record(f"sitemap rebuilt: {len(out)} URLs")
    return len(out)


# ── validation report ────────────────────────────────────────────────────────

def validate() -> dict:
    all_pages = [p for p in pages() if p.name == "index.html"]
    stats = {
        "pages": len(all_pages),
        "no_schema": 0,
        "no_canonical": 0,
        "no_desc": 0,
        "no_h1": 0,
        "multi_h1": 0,
        "no_skip": 0,
        "broken_links": 0,
        "imgs_no_alt": 0,
        "dup_titles": 0,
        "sitemap_urls": 0,
        "missing_from_sitemap": 0,
    }
    titles: dict[str, list[str]] = defaultdict(list)
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sm_urls = set(re.findall(r"<loc>(.*?)</loc>", sm))
    stats["sitemap_urls"] = len(sm_urls)
    broken = []

    for p in all_pages:
        t = p.read_text(encoding="utf-8", errors="ignore")
        url = page_url(p)
        if "application/ld+json" not in t:
            stats["no_schema"] += 1
        if 'rel="canonical"' not in t:
            stats["no_canonical"] += 1
        if 'name="description"' not in t:
            stats["no_desc"] += 1
        h1n = len(re.findall(r"<h1\b", t, re.I))
        if h1n == 0:
            stats["no_h1"] += 1
        elif h1n > 1:
            stats["multi_h1"] += 1
        if "skip-link" not in t:
            stats["no_skip"] += 1
        tm = re.search(r"<title>(.*?)</title>", t, re.S)
        if tm:
            titles[re.sub(r"\s+", " ", tm.group(1)).strip()].append(str(p.relative_to(ROOT)))
        for m in re.finditer(r"<img\b[^>]*>", t):
            if "alt=" not in m.group(0):
                stats["imgs_no_alt"] += 1
        if url not in sm_urls:
            # intentional mirrors
            if "/seo/" in url:
                html_can = re.search(r'rel="canonical" href="([^"]+)"', t)
                if html_can and html_can.group(1).rstrip("/") != url.rstrip("/"):
                    pass
                else:
                    stats["missing_from_sitemap"] += 1
            else:
                stats["missing_from_sitemap"] += 1

        for href in re.findall(r'href="([^"]+)"', t):
            if href.startswith(("http", "mailto", "tel", "#", "javascript:", "data:")):
                continue
            if "'" in href or "+" in href or "$" in href:
                continue
            path = href.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            target = (p.parent / path).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                continue
            ok = (
                target.is_file()
                or (target.is_dir() and (target / "index.html").exists())
                or (not target.suffix and (Path(str(target) + "/index.html")).is_file())
            )
            if not ok:
                broken.append((str(p.relative_to(ROOT)), href))

    stats["broken_links"] = len(broken)
    stats["dup_titles"] = sum(1 for v in titles.values() if len(v) > 1)
    REPORT["counts"] = stats
    REPORT["broken_samples"] = broken[:20]
    REPORT["dup_title_samples"] = {k: v for k, v in titles.items() if len(v) > 1}
    return stats


def fix_kontakty_desc() -> None:
    p = ROOT / "kontakty" / "index.html"
    t = p.read_text(encoding="utf-8")
    good = (
        "Контакты AngelGranit в Алматы: агент Александр, "
        f"{PHONE}, {ADDRESS}. Ритуальные услуги 24/7 — звонок и WhatsApp."
    )
    t2 = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{good}"',
        t,
        count=1,
    )
    t2 = re.sub(
        r'(property="og:description" content=")[^"]*(")',
        rf"\1{good}\2",
        t2,
        count=1,
    )
    t2 = re.sub(
        r'(name="twitter:description" content=")[^"]*(")',
        rf"\1{good}\2",
        t2,
        count=1,
    )
    if t2 != t:
        safe_write(p, t2)
        record("kontakty: clean description")


def main() -> None:
    enhance_shared_css()
    enhance_nav_js()
    fix_homepage()
    fix_kontakty_desc()
    clean_duplicate_phone_descriptions()
    inject_skip_and_main()
    add_missing_schemas()
    unique_mirror_h1()
    strengthen_crosslinks()
    fix_404_and_manifest()
    polish_seo_hub()
    rebuild_sitemap()
    stats = validate()
    out = ROOT / "scripts" / "site" / "final_optimize_report.json"
    out.write_text(json.dumps(REPORT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"fixes": len(REPORT["fixes"]), "stats": stats}, ensure_ascii=False, indent=2))
    for f in REPORT["fixes"]:
        print(" -", f)


if __name__ == "__main__":
    main()
