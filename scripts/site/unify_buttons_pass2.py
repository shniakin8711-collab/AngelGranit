# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(r"c:\Users\РС\OneDrive\Desktop\сайт кат")

# Pass: remaining legacy btn classes on all HTML
count_files = 0
count_repl = 0
for path in root.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    orig = text
    pairs = [
        ('class="btn btn--gold"', 'class="btn-primary"'),
        ('class="btn btn--red"', 'class="btn-primary"'),
        ('class="btn btn--ai"', 'class="btn-primary"'),
        ('class="btn btn--ghost"', 'class="btn-secondary"'),
        ('class="btn btn--wa"', 'class="btn-secondary"'),
        ("class='btn btn--gold'", "class='btn-primary'"),
        ("class='btn btn--ghost'", "class='btn-secondary'"),
        ("class='btn btn--wa'", "class='btn-secondary'"),
        ('class="work-card__btn"', 'class="btn-secondary"'),
    ]
    for a, b in pairs:
        n = text.count(a)
        if n:
            text = text.replace(a, b)
            count_repl += n
    # inject buttons.css for seo pages that use seo.css but not buttons.css
    if "assets/site/buttons.css" not in text and ("seo/assets/seo.css" in text or "btn-primary" in text or "btn-secondary" in text):
        rel = path.relative_to(root)
        depth = len(rel.parts) - 1
        prefix = "../" * depth if depth else ""
        link = f'<link rel="stylesheet" href="{prefix}assets/site/buttons.css" />'
        # after seo.css or nav.css
        for marker in [
            f'<link rel="stylesheet" href="{prefix}seo/assets/seo.css" />',
            f'<link rel="stylesheet" href="{prefix}assets/site/nav.css" />',
            f'<link rel="stylesheet" href="{prefix}assets/site/page.css" />',
        ]:
            if marker in text and link not in text:
                text = text.replace(marker, marker + "\n  " + link, 1)
                break
        # seo pages often use ../../seo/assets/seo.css from seo/*
        if "buttons.css" not in text:
            m = re.search(r'(<link rel="stylesheet" href="[^"]*seo\.css" />)', text)
            if m:
                # compute relative to buttons from this file
                text = text.replace(m.group(1), m.group(1) + "\n  " + link, 1)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        count_files += 1

print("files", count_files, "replacements", count_repl)

# Update nashi-raboty prices to match homepage works
nr = root / "nashi-raboty" / "index.html"
if nr.exists():
    t = nr.read_text(encoding="utf-8")
    mapping = [
        ("Гранитный памятник", "от 500 000 ₸"),
        ("Катафалк", "по запросу"),
        ("Мемориальный комплекс", "от 2 500 000 ₸"),
        ("Художественная гравировка", "от 100 000 ₸"),
        ("Благоустройство могил", "от 450 000 ₸"),
        ("Семейный мемориал", "от 900 000 ₸"),
        ("Установка комплекса", "от 2 500 000 ₸"),
        ("Стол и лавочка", "от 400 000 ₸"),
        ("Комплекс под ключ", "от 2 500 000 ₸"),
    ]
    for title, value in mapping:
        idx = t.find(f"<h3>{title}</h3>")
        if idx == -1:
            continue
        chunk = t[idx: idx + 450]
        m = re.search(r'<div class="work-card__price">[^<]*</div>', chunk)
        if not m:
            continue
        newp = (
            '<div class="card-price">'
            '<span class="card-price__label">Стоимость</span>'
            f'<span class="card-price__value">{value}</span>'
            "</div>"
        )
        chunk2 = chunk[: m.start()] + newp + chunk[m.end():]
        t = t[:idx] + chunk2 + t[idx + 450:]
    t = t.replace('class="work-card__btn"', 'class="btn-secondary"')
    if 'assets/site/buttons.css' not in t:
        t = t.replace(
            '<link rel="stylesheet" href="../assets/site/page.css" />',
            '<link rel="stylesheet" href="../assets/site/page.css" />\n  <link rel="stylesheet" href="../assets/site/buttons.css" />',
            1,
        )
    nr.write_text(t, encoding="utf-8")
    print("nashi-raboty updated")

# page.css leftovers
pc = (root / "assets/site/page.css").read_text(encoding="utf-8")
pc = pc.replace("  .btn-site { min-height: 2.75rem; }\n", "")
pc = pc.replace(".page-footer .page-cta .btn-site { min-height: 2.75rem; }\n", ".page-footer .page-cta .btn-primary,\n.page-footer .page-cta .btn-secondary { min-height: 2.75rem; }\n")
(root / "assets/site/page.css").write_text(pc, encoding="utf-8")

# index: neutralize conflicting nav__call styles — keep only layout
idx = root / "index.html"
text = idx.read_text(encoding="utf-8")
text = re.sub(
    r"\n    \.nav__call \{\n[\s\S]*?\n    \}\n    \.nav__call::after \{\n[\s\S]*?\n    \}\n    \.nav__call:hover \{\n[\s\S]*?\n    \}\n",
    "\n    .nav__call {\n      /* visual style from .btn-primary */\n      min-width: 0;\n      padding: 0.55rem 0.9rem;\n      font-size: 0.8rem;\n    }\n",
    text,
    count=1,
)
text = text.replace(".pcat-cta__btn,\n", "")
text = text.replace(
    """    .pcat-card__price {
      margin: 0 0 0.55rem;
      font-family: var(--font-display);
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--pcat-gold);
    }
""",
    "",
)
text = text.replace(
    """      .btn::after,
      .nav__call::after,
      .btn--ai { animation: none !important; }
""",
    "",
)
# leftover price-card__btn in media
text = text.replace("      .price-card__btn:hover { transform: none; }\n", "")
# work-card__price style -> card-price in works
text = re.sub(
    r"\n    \.work-card__price \{\n[\s\S]*?\n    \}\n",
    "\n",
    text,
    count=1,
)
idx.write_text(text, encoding="utf-8")
print("index cleanup done")

# remaining counts
left_btn = 0
left_site = 0
for path in root.rglob("*.html"):
    t = path.read_text(encoding="utf-8", errors="ignore")
    left_btn += t.count("btn btn--")
    left_site += t.count("btn-site")
print("remaining btn btn--", left_btn, "btn-site", left_site)
