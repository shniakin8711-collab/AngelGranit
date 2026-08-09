# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "index.html"
text = path.read_text(encoding="utf-8")

# Remove muslim filter button
text = text.replace(
    '        <button type="button" class="pcat__filter" data-pcat-filter="muslim" aria-pressed="false">Мусульманские памятники</button>\n',
    "",
)
# Add cvetnik filter if missing
if 'data-pcat-filter="cvetnik"' not in text:
    text = text.replace(
        '        <button type="button" class="pcat__filter" data-pcat-filter="landscape" aria-pressed="false">Благоустройство</button>',
        '        <button type="button" class="pcat__filter" data-pcat-filter="landscape" aria-pressed="false">Благоустройство</button>\n'
        '        <button type="button" class="pcat__filter" data-pcat-filter="cvetnik" aria-pressed="false">Цветники</button>',
    )

ICONS = {
    "vertical": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21V8l4-5 4 5v13"/><path d="M10 21v-6h4v6"/><path d="M10.5 10h3"/></svg>',
    "horizontal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="10" width="18" height="8" rx="1.2"/><path d="M7 10V8.5A2.5 2.5 0 0 1 9.5 6h5A2.5 2.5 0 0 1 17 8.5V10"/><path d="M8 14h8"/></svg>',
    "double": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V9l4-5 4 5"/><path d="M12 21V9l4-5 4 5v12"/><path d="M6.5 21v-5h3v5"/><path d="M14.5 21v-5h3v5"/></svg>',
    "complex": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><path d="M3 20h18"/><path d="M5 20V10l7-6 7 6v10"/><path d="M9 20v-5h6v5"/><path d="M10 9.5h4"/></svg>',
    "fence": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V7l2-2 2 2v13"/><path d="M10 20V7l2-2 2 2v13"/><path d="M16 20V7l2-2 2 2v13"/><path d="M4 11h16"/><path d="M4 15h16"/></svg>',
    "landscape": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18h18"/><path d="M5 18V12l3-2 3 2 3-2 3 2v6"/><path d="M12 5c1.2 1.4 2 2.8 2 4.2a2 2 0 1 1-4 0C10 7.8 10.8 6.4 12 5z"/></svg>',
    "engraving": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="16" rx="1.5"/><circle cx="12" cy="10" r="2.6"/><path d="M8 17c.9-1.8 2.3-2.7 4-2.7s3.1.9 4 2.7"/></svg>',
    "orthodox": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M7 9h10"/><path d="M9 13.5h6"/><path d="M8.5 21h7"/></svg>',
    "cvetnik": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20V10"/><path d="M12 10c2.5-1 4-3 4-5a4 4 0 1 0-8 0c0 2 1.5 4 4 5z"/><path d="M8 20h8"/></svg>',
}

cards = [
    dict(cat="vertical", icon="vertical", img="images/catalog/pcat/pcat-01-vertical-gabbro.webp", w=1024, h=1536,
         open_i=0, label="Вертикальные памятники", name="Вертикальный памятник",
         desc="Классическая стела из чёрного гранита с портретом и надписью.",
         meta="Чёрный гранит Габбро", href="uslugi/granitnye-pamyatniki/", calc="Вертикальный памятник · Габбро",
         alt="Вертикальный памятник из чёрного гранита — AngelGranit"),
    dict(cat="horizontal", icon="horizontal", img="images/catalog/pcat/pcat-02-horizontal.webp", w=1024, h=1536,
         open_i=1, label="Горизонтальные памятники", name="Горизонтальный памятник",
         desc="Широкая композиция для надписи и декоративных элементов на участке.",
         meta="Натуральный гранит", href="uslugi/pamyatniki/", calc="Горизонтальный памятник",
         alt="Горизонтальный гранитный памятник — AngelGranit"),
    dict(cat="double", icon="double", img="images/catalog/pcat/pcat-04-double.webp", w=1024, h=1536,
         open_i=2, label="Двойные памятники", name="Двойной памятник",
         desc="Единая композиция для двоих с согласованными пропорциями и надписями.",
         meta="Гранит", href="uslugi/memorialnye-kompleksy/", calc="Двойной памятник",
         alt="Двойной семейный памятник из гранита — AngelGranit"),
    dict(cat="complex", icon="complex", img="images/catalog/pcat/pcat-05-complex.webp", w=1536, h=1024,
         open_i=3, label="Мемориальные комплексы", name="Мемориальный комплекс",
         desc="Проект под ключ: камень, цветник, монтаж и финальная сдача на кладбище.",
         meta="Под ключ", href="uslugi/memorialnye-kompleksy/", calc="Мемориальный комплекс под ключ",
         alt="Мемориальный комплекс из чёрного гранита — AngelGranit"),
    dict(cat="fence", icon="fence", img="images/catalog/pcat/pcat-06-fence.webp", w=1536, h=1024,
         open_i=4, label="Ограды", name="Гранитная ограда",
         desc="Индивидуальное изготовление ограды под размеры участка и стиль памятника.",
         meta="Индивидуальное изготовление", href="uslugi/ogrady/", calc="Гранитная ограда",
         alt="Гранитная ограда вокруг места захоронения — AngelGranit"),
    dict(cat="landscape", icon="landscape", img="images/catalog/pcat/pcat-07-landscape.webp", w=1536, h=1024,
         open_i=5, label="Благоустройство", name="Благоустройство участка",
         desc="Плитка, фундамент, цветник и аккуратное оформление места захоронения.",
         meta="Плитка, фундамент, цветник", href="uslugi/blagoustrojstvo-mogil/", calc="Благоустройство участка",
         alt="Благоустройство могилы — AngelGranit"),
    dict(cat="vertical", icon="engraving", img="images/catalog/pcat/pcat-08-engraving.webp", w=1024, h=1536,
         open_i=6, label="Вертикальные памятники", name="Памятник с гравировкой",
         desc="Точная лазерная гравировка портрета и эпитафии на натуральном камне.",
         meta="Натуральный гранит", href="uslugi/gravirovka/", calc="Памятник с гравировкой",
         alt="Гравировка на гранитном памятнике — AngelGranit"),
    dict(cat="vertical", icon="orthodox", img="images/catalog/pcat/pcat-09-orthodox.webp", w=1024, h=1536,
         open_i=7, label="Вертикальные памятники", name="Православный памятник",
         desc="Сдержанная композиция с крестом — достоинство формы и чистота камня.",
         meta="Чёрный гранит", href="uslugi/pamyatniki/", calc="Православный памятник",
         alt="Православный гранитный памятник с крестом — AngelGranit"),
    dict(cat="cvetnik", icon="cvetnik", img="images/catalog/pcat/pcat-03-cvetnik.webp", w=1024, h=1536,
         open_i=8, label="Цветники", name="Гранитный цветник",
         desc="Долговечный гранитный цветник и ваза — аккуратный вид на годы.",
         meta="Чёрный гранит", href="uslugi/cvetniki/", calc="Гранитный цветник",
         alt="Гранитный цветник у памятника — AngelGranit"),
]

parts = []
for c in cards:
    icon = ICONS[c["icon"]]
    parts.append(f'''        <article class="pcat-card" role="listitem" data-pcat-cat="{c['cat']}" itemscope itemtype="https://schema.org/Product">
          <button type="button" class="pcat-card__media" data-pcat-open="{c['open_i']}" aria-label="Открыть фото: {c['name']}">
            <img src="{c['img']}" alt="{c['alt']}" width="{c['w']}" height="{c['h']}" loading="lazy" decoding="async" itemprop="image" />
          </button>
          <div class="pcat-card__body">
            <div class="pcat-card__top">
              <span class="pcat-card__icon" aria-hidden="true">{icon}</span>
              <p class="pcat-card__cat">{c['label']}</p>
            </div>
            <h3 itemprop="name">{c['name']}</h3>
            <p class="pcat-card__desc" itemprop="description">{c['desc']}</p>
            <ul class="pcat-card__meta">
              <li><span>Материал:</span> {c['meta']}</li>
            </ul>
            <p class="pcat-card__price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
              <meta itemprop="priceCurrency" content="KZT" />
              <meta itemprop="availability" content="https://schema.org/InStock" />
              цена по запросу
            </p>
            <div class="pcat-card__actions">
              <a class="pcat-card__btn pcat-card__btn--more" href="{c['href']}">Подробнее</a>
              <button type="button" class="pcat-card__btn pcat-card__btn--calc" data-pcat-calc="{c['calc']}">Получить расчет</button>
            </div>
          </div>
        </article>''')

grid = "\n\n".join(parts)
pattern = re.compile(
    r'(<div class="pcat__grid reveal" id="pcat-grid" role="list">)([\s\S]*?)(</div>\s*\n\s*<aside class="pcat-cta)',
    re.M,
)
m = pattern.search(text)
if not m:
    raise SystemExit("pcat grid not found")
text = pattern.sub(lambda mo: mo.group(1) + "\n" + grid + "\n      " + mo.group(3), text, count=1)

path.write_text(text, encoding="utf-8")
print("pcat updated: 9 cards, muslim removed, new photos")
