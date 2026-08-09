# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(r"c:\Users\РС\OneDrive\Desktop\сайт кат\index.html")
text = path.read_text(encoding="utf-8")

cards = [
    {
        "full": "images/catalog/monuments/items/monument-001.webp",
        "title": "Черный гранит Габбро · 120×60 см · от 500 000 ₸",
        "alt": "Памятник из чёрного гранита Габбро 120×60 см — выполненная работа AngelGranit",
        "w": 900, "h": 1200,
        "name": "Черный гранит Габбро",
        "meta": "Материал: гранит Габбро · 120×60 см",
        "price": "от 500 000 ₸",
        "href": "uslugi/granitnye-pamyatniki/",
    },
    {
        "full": "images/seo/memorialny-kompleks-chernyj-granit.webp",
        "title": "Мемориальный комплекс · 3×4 м · от 2 500 000 ₸",
        "alt": "Мемориальный комплекс 3×4 м из чёрного гранита — AngelGranit",
        "w": 1600, "h": 900,
        "name": "Мемориальный комплекс",
        "meta": "Материал: чёрный гранит · 3×4 м",
        "price": "от 2 500 000 ₸",
        "href": "uslugi/memorialnye-kompleksy/",
    },
    {
        "full": "images/seo/semejnyj-memorial.webp",
        "title": "Двойной памятник · Гранит · от 900 000 ₸",
        "alt": "Двойной памятник из гранита — выполненная работа AngelGranit",
        "w": 1600, "h": 900,
        "name": "Двойной памятник",
        "meta": "Материал: гранит",
        "price": "от 900 000 ₸",
        "href": "uslugi/memorialnye-kompleksy/",
    },
    {
        "full": "images/catalog/monuments/items/monument-012.webp",
        "title": "Мусульманский памятник · от 550 000 ₸",
        "alt": "Мусульманский памятник из гранита — AngelGranit Алматы",
        "w": 900, "h": 1200,
        "name": "Мусульманский памятник",
        "meta": "Материал: чёрный гранит",
        "price": "от 550 000 ₸",
        "href": "uslugi/musulmanskie-pamyatniki/",
    },
    {
        "full": "images/catalog/monuments/items/monument-005.webp",
        "title": "Горизонтальный памятник · от 650 000 ₸",
        "alt": "Горизонтальный гранитный памятник — выполненная работа AngelGranit",
        "w": 900, "h": 1200,
        "name": "Горизонтальный памятник",
        "meta": "Материал: натуральный гранит · 100×50 см",
        "price": "от 650 000 ₸",
        "href": "uslugi/pamyatniki/",
    },
    {
        "full": "images/seo/granitnye-pamyatniki-almaty.webp",
        "title": "Вертикальный памятник · от 500 000 ₸",
        "alt": "Вертикальный гранитный памятник Алматы — AngelGranit",
        "w": 1200, "h": 800,
        "name": "Вертикальный памятник",
        "meta": "Материал: гранит · 120×60 см",
        "price": "от 500 000 ₸",
        "href": "uslugi/granitnye-pamyatniki/",
    },
    {
        "full": "images/seo/pamyatnik-s-blagoustrojstvom.webp",
        "title": "Благоустройство участка · от 450 000 ₸",
        "alt": "Благоустройство места захоронения — плитка и цветник AngelGranit",
        "w": 1200, "h": 800,
        "name": "Благоустройство участка",
        "meta": "Плитка, фундамент, цветник",
        "price": "от 450 000 ₸",
        "href": "uslugi/blagoustrojstvo-mogil/",
    },
    {
        "full": "images/seo/granitnyj-stol-lavochka.webp",
        "title": "Гранитная ограда и лавочка · от 400 000 ₸",
        "alt": "Гранитная ограда, стол и лавочка — работа AngelGranit",
        "w": 1600, "h": 900,
        "name": "Гранитная ограда",
        "meta": "Материал: гранит · индивидуальные размеры",
        "price": "от 400 000 ₸",
        "href": "uslugi/ogrady/",
    },
    {
        "full": "images/seo/professionalnaya-ustanovka-kompleksa.webp",
        "title": "Установка комплекса · от 2 500 000 ₸",
        "alt": "Профессиональная установка мемориального комплекса — AngelGranit",
        "w": 1600, "h": 900,
        "name": "Установка комплекса",
        "meta": "Материал: гранит · монтаж на кладбище",
        "price": "от 2 500 000 ₸",
        "href": "uslugi/memorialnye-kompleksy/",
    },
    {
        "full": "images/seo/hudozhestvennaya-gravirovka.webp",
        "title": "Художественная гравировка · портрет от 100 000 ₸",
        "alt": "Художественная гравировка портрета на граните — AngelGranit",
        "w": 1200, "h": 800,
        "name": "Художественная гравировка",
        "meta": "Портрет и надписи на граните",
        "price": "от 100 000 ₸",
        "href": "uslugi/gravirovka/",
    },
    {
        "full": "images/seo/memorialny-kompleks-almaty.webp",
        "title": "Комплекс под ключ · от 2 500 000 ₸",
        "alt": "Мемориальный комплекс под ключ в Алматы — AngelGranit",
        "w": 1600, "h": 900,
        "name": "Комплекс под ключ",
        "meta": "Материал: гранит · проект и монтаж",
        "price": "от 2 500 000 ₸",
        "href": "uslugi/memorialnye-kompleksy/",
    },
    {
        "full": "images/seo/ustanovka-pamyatnika-almaty.webp",
        "title": "Установка памятника · от 500 000 ₸",
        "alt": "Установка гранитного памятника на кладбище Алматы — AngelGranit",
        "w": 1200, "h": 800,
        "name": "Установка памятника",
        "meta": "Материал: гранит · 120×60 см",
        "price": "от 500 000 ₸",
        "href": "uslugi/pamyatniki/",
    },
]

parts = []
for c in cards:
    parts.append(f'''        <article class="folio-card" role="listitem" data-folio-item data-full="{c['full']}" data-title="{c['title']}">
          <div class="folio-card__media">
            <img src="{c['full']}" alt="{c['alt']}" width="{c['w']}" height="{c['h']}" loading="lazy" decoding="async" />
            <button type="button" class="folio-card__open" data-folio-open aria-label="Открыть фото: {c['name']}"></button>
            <div class="folio-card__overlay">
              <h3>{c['name']}</h3>
              <p class="folio-card__meta">{c['meta']}</p>
              <p class="folio-card__price">{c['price']}</p>
              <a class="btn-secondary" href="{c['href']}">Подробнее</a>
            </div>
          </div>
        </article>''')

grid = "\n\n".join(parts)

pattern = re.compile(
    r'(<div class="folio__grid reveal" id="folio-grid" role="list">)([\s\S]*?)(</div>\s*\n\s*<aside class="folio-cta)',
    re.M,
)
m = pattern.search(text)
if not m:
    raise SystemExit("folio grid not found")
text = pattern.sub(r"\1\n" + grid + r"\n      \3", text, count=1)
path.write_text(text, encoding="utf-8")
print("folio cards rewritten:", len(cards))
