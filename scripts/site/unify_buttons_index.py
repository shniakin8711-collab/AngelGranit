# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(r"c:\Users\РС\OneDrive\Desktop\сайт кат\index.html")
text = path.read_text(encoding="utf-8")

# Link buttons.css
if "assets/site/buttons.css" not in text:
    text = text.replace(
        '<link rel="stylesheet" href="assets/site/nav.css" />',
        '<link rel="stylesheet" href="assets/site/nav.css" />\n  <link rel="stylesheet" href="assets/site/buttons.css" />',
        1,
    )

# HTML class replacements
repls = [
    ('class="hero__btn hero__btn--call"', 'class="btn-primary"'),
    ('class="hero__btn hero__btn--wa"', 'class="btn-secondary"'),
    ('class="hero__btn hero__btn--consult"', 'class="btn-primary"'),
    ('class="hero__card-btn"', 'class="btn-primary"'),
    ('class="svc-cta__btn svc-cta__btn--call"', 'class="btn-primary"'),
    ('class="svc-cta__btn svc-cta__btn--wa"', 'class="btn-secondary"'),
    ('class="pcat-card__btn pcat-card__btn--more"', 'class="btn-secondary"'),
    ('class="pcat-card__btn pcat-card__btn--calc"', 'class="btn-primary"'),
    ('class="pcat-cta__btn"', 'class="btn-primary"'),
    ('class="pcat-modal__submit"', 'class="btn-primary"'),
    ('class="price-card__btn"', 'class="btn-primary"'),
    ('class="work-card__btn"', 'class="btn-secondary"'),
    ('class="btn btn--red"', 'class="btn-primary"'),
    ('class="btn btn--ghost"', 'class="btn-secondary"'),
    ('class="btn btn--wa"', 'class="btn-secondary"'),
    ('class="btn btn--gold"', 'class="btn-primary"'),
    ('class="btn btn--ai"', 'class="btn-primary"'),
    ('class="nav__call"', 'class="btn-primary nav__call"'),
]
for a, b in repls:
    text = text.replace(a, b)

# leftover btn-- variants
text = re.sub(r'class="btn btn--([a-z]+)"', lambda m: 'class="btn-primary"' if m.group(1) in ("red", "gold", "ai") else 'class="btn-secondary"', text)
text = text.replace('class="btn "', 'class="btn-primary"')

# hero actions / svc actions / pcat actions layout classes for mobile full width
text = text.replace('class="hero__actions"', 'class="hero__actions btn-row"')
text = text.replace('class="svc-cta__actions"', 'class="svc-cta__actions btn-row"')
text = text.replace('class="pcat-card__actions"', 'class="pcat-card__actions btn-row"')

# --- Prices in premium catalog ---
# helper to build price block with schema metas
def price_block(amount_int, display):
    return (
        f'<div class="card-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n'
        f'              <span class="card-price__label">Стоимость</span>\n'
        f'              <meta itemprop="priceCurrency" content="KZT" />\n'
        f'              <meta itemprop="price" content="{amount_int}" />\n'
        f'              <meta itemprop="availability" content="https://schema.org/InStock" />\n'
        f'              <span class="card-price__value">от {display} ₸</span>\n'
        f'            </div>'
    )

# Replace each pcat-card__price block individually by category order in file
# Simpler: regex replace old pcat price paragraphs
pcat_prices = [
    ("250000", "250 000", "500000", "500 000"),  # vertical
    ("280000", "280 000", "650000", "650 000"),  # horizontal
    ("300000", "300 000", "550000", "550 000"),  # muslim
    ("650000", "650 000", "900000", "900 000"),  # double
    ("2500000", "2 500 000", "2500000", "2 500 000"),  # complex unchanged
    ("400000", "400 000", "400000", "400 000"),  # fence
    ("450000", "450 000", "450000", "450 000"),  # landscape
    ("320000", "320 000", "500000", "500 000"),  # engraving vertical
]

for old_n, old_d, new_n, new_d in pcat_prices:
    old_block = re.compile(
        rf'<p class="pcat-card__price" itemprop="offers" itemscope itemtype="https://schema\.org/Offer">\s*'
        rf'<meta itemprop="priceCurrency" content="KZT" />\s*'
        rf'<meta itemprop="price" content="{old_n}" />\s*'
        rf'<meta itemprop="availability" content="https://schema\.org/InStock" />\s*'
        rf'от {re.escape(old_d)} ₸\s*'
        rf'</p>',
        re.S,
    )
    text, c = old_block.subn(price_block(new_n, new_d), text, count=1)
    print(f"pcat {old_d} -> {new_d}: {c}")

# JSON-LD catalog prices
text = text.replace('"price": "250000"', '"price": "500000"', 1)  # first vertical in list
# careful - replace specific product names in schema
text = text.replace(
    '"name": "Вертикальный памятник из гранита Габбро"',
    '"name": "Вертикальный памятник из гранита Габбро"',
)
# Update schema offers by product name context via sequential known strings
schema_map = [
    ('"name": "Вертикальный памятник из гранита Габбро"', "500000"),
    ('"name": "Двойной памятник из гранита"', "900000"),
    ('"name": "Мусульманский памятник из чёрного гранита"', "550000"),
    ('"name": "Мемориальный комплекс под ключ"', "2500000"),
    ('"name": "Гранитная ограда"', "400000"),
    ('"name": "Благоустройство места захоронения"', "450000"),
]
for name, price in schema_map:
    idx = text.find(name)
    if idx == -1:
        print("schema miss", name)
        continue
    # find next "price": "...." after name within 800 chars
    chunk = text[idx:idx + 900]
    chunk2, n = re.subn(r'"price": "[0-9]+"', f'"price": "{price}"', chunk, count=1)
    if n:
        text = text[:idx] + chunk2 + text[idx + 900:]
        print("schema", name, "->", price)

# Price cards section (#prices)
price_card_updates = [
    (
        """          <h3>Памятники</h3>
          <p>Одинарные и фигурные памятники из натурального гранита с установкой.</p>
          <div class="price-card__from">цена по запросу</div>""",
        """          <h3>Памятники</h3>
          <p>Одинарные и фигурные памятники из натурального гранита с установкой.</p>
          <div class="card-price">
            <span class="card-price__label">Стоимость</span>
            <span class="card-price__value">от 500 000 ₸</span>
          </div>""",
    ),
    (
        """          <h3>Мемориальные комплексы</h3>
          <p>Комплексное оформление места: стела, цоколь, цветник и монтаж.</p>
          <div class="price-card__from"><span>от</span>150 000 ₸</div>""",
        """          <h3>Мемориальные комплексы</h3>
          <p>Комплексное оформление места: стела, цоколь, цветник и монтаж.</p>
          <div class="card-price">
            <span class="card-price__label">Стоимость</span>
            <span class="card-price__value">от 2 500 000 ₸</span>
          </div>""",
    ),
    (
        """          <h3>Благоустройство</h3>
          <p>Выравнивание участка, плитка, уход и аккуратное оформление места.</p>
          <div class="price-card__from">цена по запросу</div>""",
        """          <h3>Благоустройство</h3>
          <p>Выравнивание участка, плитка, уход и аккуратное оформление места.</p>
          <div class="card-price">
            <span class="card-price__label">Стоимость</span>
            <span class="card-price__value">от 450 000 ₸</span>
          </div>""",
    ),
    (
        """          <h3>Ограды</h3>
          <p>Металлические и гранитные ограждения участка — от простых до сложных.</p>
          <div class="price-card__from">цена по запросу</div>""",
        """          <h3>Ограды</h3>
          <p>Металлические и гранитные ограждения участка — от простых до сложных.</p>
          <div class="card-price">
            <span class="card-price__label">Стоимость</span>
            <span class="card-price__value">от 400 000 ₸</span>
          </div>""",
    ),
    (
        """          <h3>Портреты</h3>
          <p>Фотокерамика и гравированный портрет — точная передача образа на камне.</p>
          <div class="price-card__from">цена по запросу</div>""",
        """          <h3>Портреты</h3>
          <p>Фотокерамика и гравированный портрет — точная передача образа на камне.</p>
          <div class="card-price">
            <span class="card-price__label">Стоимость</span>
            <span class="card-price__value">от 100 000 ₸</span>
          </div>""",
    ),
]
for a, b in price_card_updates:
    if a in text:
        text = text.replace(a, b, 1)
        print("price-card updated")
    else:
        print("price-card MISS")

# Color flower card - no specific price from user; leave or skip
# Work cards: add Стоимость + map by title
work_map = {
    "Гранитный памятник": "от 500 000 ₸",
    "Катафалк": "цена по запросу",  # not in list - keep request? User only listed monument prices. Keep as card-price with value
    "Мемориальный комплекс": "от 2 500 000 ₸",
    "Художественная гравировка": "от 100 000 ₸",  # portrait-ish
    "Благоустройство могил": "от 450 000 ₸",
    "Семейный мемориал": "от 900 000 ₸",
    "Установка комплекса": "от 2 500 000 ₸",
    "Стол и лавочка": "от 400 000 ₸",
    "Комплекс под ключ": "от 2 500 000 ₸",
}

def replace_work_card_price(html, title, value):
    # find h3 title then following work-card__price
    pattern = re.compile(
        rf'(<h3>{re.escape(title)}</h3>[\s\S]*?<div class="work-card__price">)([^<]*)(</div>)',
        re.M,
    )
    def sub(m):
        return (
            m.group(0).split('<div class="work-card__price">')[0]
            + '<div class="card-price">'
            + '<span class="card-price__label">Стоимость</span>'
            + f'<span class="card-price__value">{value}</span>'
            + '</div>'
        )
    # simpler approach
    m = pattern.search(html)
    if not m:
        return html, False
    new = pattern.sub(
        lambda mm: mm.group(1).replace('<div class="work-card__price">', '<div class="card-price"><span class="card-price__label">Стоимость</span><span class="card-price__value">')
        + value
        + '</span></div><!--x-->',
        html,
        count=1,
    )
    # cleanup botched - do manual
    return html, False

# Manual work card replacements
for title, value in work_map.items():
    old = f"<h3>{title}</h3>"
    idx = text.find(old)
    if idx == -1:
        print("work miss", title)
        continue
    # find work-card__price after title within 500 chars
    chunk = text[idx:idx + 500]
    m = re.search(r'<div class="work-card__price">[^<]*</div>', chunk)
    if not m:
        print("work price miss", title)
        continue
    new_price = (
        '<div class="card-price">'
        '<span class="card-price__label">Стоимость</span>'
        f'<span class="card-price__value">{value}</span>'
        "</div>"
    )
    chunk2 = chunk[: m.start()] + new_price + chunk[m.end() :]
    text = text[:idx] + chunk2 + text[idx + 500 :]
    print("work ok:", title.encode("ascii", "ignore").decode())

# For катафалк user didn't give price - use "по запросу" still in gold format
# Already set

# CSS cleanup: neutralize old button component styles by replacing key blocks with empty comments
# Replace .btn { ... } through btn--ai pulse with unified note
btn_block = re.search(r"    /\* Unified buttons|    \.btn \{", text)
# Find `.btn {` main block
m = re.search(r"\n    \.btn \{\n      position: relative;", text)
if m:
    # find end at `@keyframes aiBtnPulse` block end or next major section
    start = m.start()
    end_m = re.search(r"\n    @keyframes aiBtnPulse \{[\s\S]*?\n    \}\n", text[start:])
    if end_m:
        end = start + end_m.end()
        text = (
            text[:start]
            + "\n    /* Legacy .btn* removed — use assets/site/buttons.css (.btn-primary / .btn-secondary) */\n"
            + text[end:]
        )
        print("removed .btn block")

# Remove hero button specific styles - keep layout for actions
hero_btn = re.search(r"\n    \.hero__btn \{\n", text)
if hero_btn:
    start = hero_btn.start()
    # until .hero__card {
    end = text.find("\n    .hero__card {", start)
    if end != -1:
        text = (
            text[:start]
            + "\n    .hero__actions .btn-primary,\n    .hero__actions .btn-secondary { flex: 0 1 auto; }\n"
            + text[end:]
        )
        print("removed hero__btn styles")

# Remove hero__card-btn styles
hcb = re.search(r"\n    \.hero__card-btn \{\n", text)
if hcb:
    start = hcb.start()
    end = text.find("\n    .hero__fade {", start)
    if end != -1:
        text = (
            text[:start]
            + "\n    .hero__card .btn-primary { width: 100%; min-width: 0; }\n"
            + text[end:]
        )
        print("removed hero__card-btn")

# Remove svc-cta__btn styles
svc = re.search(r"\n    \.svc-cta__btn \{\n", text)
if svc:
    start = svc.start()
    end = text.find("\n    @media (max-width: 560px) {\n      .svc-cta__actions", start)
    if end == -1:
        end = text.find("\n    @media (prefers-reduced-motion: reduce) {\n      .svc-card,", start)
    if end != -1:
        text = (
            text[:start]
            + "\n    .svc-cta__actions .btn-primary,\n    .svc-cta__actions .btn-secondary { min-width: 10.5rem; }\n"
            + text[end:]
        )
        print("removed svc-cta__btn")

# Remove pcat-card__btn styles
pcb = re.search(r"\n    \.pcat-card__btn \{\n", text)
if pcb:
    start = pcb.start()
    end = text.find("\n    .pcat-empty {", start)
    if end != -1:
        text = (
            text[:start]
            + "\n    .pcat-card__actions { margin-top: auto; }\n    .pcat-card__actions .btn-primary,\n    .pcat-card__actions .btn-secondary { min-width: 0; width: 100%; padding-left: 0.7rem; padding-right: 0.7rem; font-size: 0.84rem; }\n"
            + text[end:]
        )
        print("removed pcat-card__btn")

# Remove pcat-cta__btn
pct = re.search(r"\n    \.pcat-cta__btn \{\n", text)
if pct:
    start = pct.start()
    end = text.find("\n    .pcat-lightbox {", start)
    if end != -1:
        text = text[:start] + "\n" + text[end:]
        print("removed pcat-cta__btn")

# Remove pcat-modal__submit
pms = re.search(r"\n    \.pcat-modal__submit \{\n", text)
if pms:
    start = pms.start()
    end = text.find("\n    .pcat-modal__note {", start)
    if end != -1:
        text = (
            text[:start]
            + "\n    .pcat-modal__form .btn-primary { width: 100%; min-width: 0; }\n"
            + text[end:]
        )
        print("removed pcat-modal__submit")

# Remove price-card__btn and restyle price-card__from unused
pcb2 = re.search(r"\n    \.price-card__btn \{\n", text)
if pcb2:
    start = pcb2.start()
    end = text.find("\n    @media (max-width: 900px) {\n      .price-grid", start)
    if end == -1:
        end = text.find("\n      .price-grid { grid-template-columns: repeat(2", start)
    # find following media that mentions price-card__btn
    end2 = text.find("\n    .package", start)
    # cut until .package if nearby
    if end2 != -1 and end2 - start < 800:
        text = (
            text[:start]
            + "\n    .price-card .btn-primary { width: 100%; min-width: 0; margin-top: auto; }\n"
            + text[end2:]
        )
        print("removed price-card__btn block")

# Remove work-card__btn
wcb = re.search(r"\n    \.work-card__btn \{\n", text)
if wcb:
    start = wcb.start()
    end = text.find("\n    .work-card:hover .work-card__btn", start)
    # find end of that rule
    end2 = text.find("\n    }", start)
    # better find next selector after hover rule
    m2 = re.search(r"\n    \.work-card:hover \.work-card__btn \{[\s\S]*?\n    \}\n", text[start:])
    if m2:
        end = start + m2.end()
        text = (
            text[:start]
            + "\n    .work-card .btn-secondary { width: 100%; min-width: 0; }\n"
            + text[end:]
        )
        print("removed work-card__btn")

# calc-summary actions
text = text.replace(
    ".calc-summary__actions .btn {",
    ".calc-summary__actions .btn-primary,\n    .calc-summary__actions .btn-secondary {",
)

# nav__call keep layout but inherit btn-primary; neutralize conflicting nav__call color rules lightly
# leave nav__call CSS for positioning

# Fix double replacements of nav call
text = text.replace('class="btn-primary nav__call btn-primary nav__call"', 'class="btn-primary nav__call"')

# Ensure mobile hero full width still works
if ".hero__actions" in text and "btn-row" in text:
    pass

path.write_text(text, encoding="utf-8")
print("index.html written, length", len(text))
