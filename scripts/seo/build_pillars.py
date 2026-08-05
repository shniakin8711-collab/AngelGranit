# -*- coding: utf-8 -*-
"""Generate 8 root pillar SEO pages focused on ritual services Almaty."""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

BASE = "https://shniakin8711-collab.github.io/AngelGranit"
PHONE = "+7 701 056 7667"
PHONE_TEL = "+77010567667"
ADDRESS = "ул. Осетинская, 5а"
AGENT = "Александр"
TODAY = date.today().isoformat()
ROOT = Path(__file__).resolve().parents[2]

# New SEO-only images (do not reuse homepage/gallery assets)
SEO_IMAGES = {
    "ritualnye-uslugi-almaty": {
        "file": "ritualnye-uslugi-almaty.webp",
        "alt": "Ритуальные услуги в Алматы",
        "title": "Ритуальные услуги Алматы — AngelGranit",
    },
    "organizaciya-pohoron-almaty": {
        "file": "organizaciya-pohoron-almaty.webp",
        "alt": "Организация похорон в Алматы",
        "title": "Организация похорон Алматы",
    },
    "ritualny-agent-konsultaciya": {
        "file": "ritualny-agent-konsultaciya.webp",
        "alt": "Ритуальный агент консультирует семью в Алматы",
        "title": "Ритуальный агент Алматы — консультация",
    },
    "katafalk-almaty": {
        "file": "katafalk-almaty.webp",
        "alt": "Катафалк Алматы",
        "title": "Современный катафалк Алматы",
    },
    "granitnye-pamyatniki-almaty": {
        "file": "granitnye-pamyatniki-almaty.webp",
        "alt": "Гранитные памятники Алматы",
        "title": "Гранитные памятники Алматы",
    },
    "memorialny-kompleks-almaty": {
        "file": "memorialny-kompleks-almaty.webp",
        "alt": "Мемориальный комплекс в Алматы",
        "title": "Мемориальный комплекс Алматы",
    },
    "ustanovka-pamyatnika-almaty": {
        "file": "ustanovka-pamyatnika-almaty.webp",
        "alt": "Установка памятника в Алматы",
        "title": "Установка памятника Алматы",
    },
    "cvety-vozle-pamyatnika": {
        "file": "cvety-vozle-pamyatnika.webp",
        "alt": "Цветы возле памятника в Алматы",
        "title": "Цветы возле памятника",
    },
    "alleya-kladbishcha": {
        "file": "alleya-kladbishcha.webp",
        "alt": "Аллея кладбища в Алматы",
        "title": "Аллея кладбища",
    },
    "granitnaya-masterskaya": {
        "file": "granitnaya-masterskaya.webp",
        "alt": "Гранитная мастерская в Алматы",
        "title": "Гранитная мастерская AngelGranit",
    },
    "hudozhestvennaya-gravirovka": {
        "file": "hudozhestvennaya-gravirovka.webp",
        "alt": "Художественная гравировка на граните",
        "title": "Художественная гравировка памятников",
    },
    "memorialny-kompleks-chernyj-granit": {
        "file": "memorialny-kompleks-chernyj-granit.webp",
        "alt": "Мемориальный комплекс из черного гранита",
        "title": "Мемориальный комплекс из чёрного гранита",
    },
    "pamyatnik-s-blagoustrojstvom": {
        "file": "pamyatnik-s-blagoustrojstvom.webp",
        "alt": "Памятник с благоустройством в Алматы",
        "title": "Памятник с благоустройством",
    },
    "granitnyj-stol-lavochka": {
        "file": "granitnyj-stol-lavochka.webp",
        "alt": "Гранитный стол и лавочка для мемориала",
        "title": "Гранитный стол и лавочка",
    },
    "vaza-iz-granita": {
        "file": "vaza-iz-granita.webp",
        "alt": "Ваза из гранита для места захоронения",
        "title": "Ваза из гранита",
    },
    "oformlenie-mesta-zahoroneniya": {
        "file": "oformlenie-mesta-zahoroneniya.webp",
        "alt": "Оформление места захоронения в Алматы",
        "title": "Оформление места захоронения",
    },
    "professionalnaya-ustanovka-kompleksa": {
        "file": "professionalnaya-ustanovka-kompleksa.webp",
        "alt": "Профессиональная установка мемориального комплекса",
        "title": "Профессиональная установка мемориального комплекса",
    },
    "semejnyj-memorial": {
        "file": "semejnyj-memorial.webp",
        "alt": "Семейный мемориал из гранита в Алматы",
        "title": "Семейный мемориал",
    },
    "naturalnyj-granit-krupnym-planom": {
        "file": "naturalnyj-granit-krupnym-planom.webp",
        "alt": "Натуральный гранит крупным планом",
        "title": "Натуральный гранит",
    },
    "ritualnye-prinadlezhnosti-almaty": {
        "file": "ritualnye-prinadlezhnosti-almaty.webp",
        "alt": "Ритуальные принадлежности в Алматы",
        "title": "Ритуальные принадлежности Алматы",
    },
}

# Which SEO images appear on each pillar page (between sections + gallery)
PAGE_IMAGES = {
    "ritualnye-uslugi-almaty": [
        "ritualnye-uslugi-almaty",
        "ritualny-agent-konsultaciya",
        "alleya-kladbishcha",
        "ritualnye-prinadlezhnosti-almaty",
        "katafalk-almaty",
        "oformlenie-mesta-zahoroneniya",
    ],
    "organizaciya-pohoron-almaty": [
        "organizaciya-pohoron-almaty",
        "ritualny-agent-konsultaciya",
        "katafalk-almaty",
        "ritualnye-prinadlezhnosti-almaty",
        "alleya-kladbishcha",
        "cvety-vozle-pamyatnika",
    ],
    "katafalk-almaty": [
        "katafalk-almaty",
        "organizaciya-pohoron-almaty",
        "alleya-kladbishcha",
        "ritualnye-uslugi-almaty",
        "ritualny-agent-konsultaciya",
    ],
    "pamyatniki-almaty": [
        "granitnye-pamyatniki-almaty",
        "ustanovka-pamyatnika-almaty",
        "cvety-vozle-pamyatnika",
        "pamyatnik-s-blagoustrojstvom",
        "naturalnyj-granit-krupnym-planom",
        "hudozhestvennaya-gravirovka",
    ],
    "granitnye-pamyatniki-almaty": [
        "granitnye-pamyatniki-almaty",
        "granitnaya-masterskaya",
        "hudozhestvennaya-gravirovka",
        "naturalnyj-granit-krupnym-planom",
        "ustanovka-pamyatnika-almaty",
        "pamyatnik-s-blagoustrojstvom",
    ],
    "memorialnye-kompleksy-almaty": [
        "memorialny-kompleks-almaty",
        "memorialny-kompleks-chernyj-granit",
        "professionalnaya-ustanovka-kompleksa",
        "semejnyj-memorial",
        "granitnyj-stol-lavochka",
        "vaza-iz-granita",
        "pamyatnik-s-blagoustrojstvom",
    ],
    "ritualny-agent-almaty": [
        "ritualny-agent-konsultaciya",
        "ritualnye-uslugi-almaty",
        "organizaciya-pohoron-almaty",
        "katafalk-almaty",
        "alleya-kladbishcha",
    ],
    "ritualnye-prinadlezhnosti-almaty": [
        "ritualnye-prinadlezhnosti-almaty",
        "cvety-vozle-pamyatnika",
        "oformlenie-mesta-zahoroneniya",
        "vaza-iz-granita",
        "organizaciya-pohoron-almaty",
    ],
}

PILLARS = [
    {
        "slug": "ritualnye-uslugi-almaty",
        "title": "Ритуальные услуги Алматы 24/7 | AngelGranit",
        "description": "Ритуальные услуги Алматы 24/7: организация похорон, катафалк, документы, памятники. Агент Александр +7 701 056 7667.",
        "h1": "Ритуальные услуги Алматы",
        "lead": "AngelGranit — похоронное бюро полного цикла в Алматы: помощь 24/7 с организацией похорон, транспортом и памятниками.",
        "focus": "ритуальные услуги Алматы",
        "service": "Ритуальные услуги в Алматы",
    },
    {
        "slug": "organizaciya-pohoron-almaty",
        "title": "Организация похорон Алматы под ключ | AngelGranit",
        "description": "Организация похорон Алматы под ключ: документы, зал, катафалк, венки. Ритуальный агент Александр 24/7, +7 701 056 7667.",
        "h1": "Организация похорон в Алматы",
        "lead": "Пошаговая организация похорон в Алматы без хаоса: один агент координирует документы, транспорт и церемонию.",
        "focus": "организация похорон Алматы",
        "service": "Организация похорон Алматы",
    },
    {
        "slug": "katafalk-almaty",
        "title": "Катафалк Алматы — заказ 24/7 | AngelGranit",
        "description": "Катафалк Алматы и ритуальный транспорт 24/7 по городу и регионам. Заказ у AngelGranit, агент Александр +7 701 056 7667.",
        "h1": "Катафалк Алматы",
        "lead": "Ритуальный транспорт и катафалк в Алматы с аккуратной подачей по согласованному маршруту.",
        "focus": "катафалк Алматы",
        "service": "Катафалк Алматы",
    },
    {
        "slug": "pamyatniki-almaty",
        "title": "Памятники Алматы — заказ и установка | AngelGranit",
        "description": "Памятники Алматы: гранитные стелы, гравировка, установка на кладбище. Каталог и замер — AngelGranit, +7 701 056 7667.",
        "h1": "Памятники в Алматы",
        "lead": "Подбор, изготовление и установка памятников в Алматы — как часть ритуальных услуг AngelGranit.",
        "focus": "памятники Алматы",
        "service": "Памятники Алматы",
    },
    {
        "slug": "granitnye-pamyatniki-almaty",
        "title": "Гранитные памятники Алматы | AngelGranit",
        "description": "Гранитные памятники Алматы: изготовление, портрет, установка. Долговечный камень и монтаж от AngelGranit, +7 701 056 7667.",
        "h1": "Гранитные памятники Алматы",
        "lead": "Гранитные памятники для климата Алматы: прочность, читаемая гравировка и аккуратный монтаж.",
        "focus": "гранитные памятники Алматы",
        "service": "Гранитные памятники Алматы",
    },
    {
        "slug": "memorialnye-kompleksy-almaty",
        "title": "Мемориальные комплексы Алматы | AngelGranit",
        "description": "Мемориальные комплексы Алматы под ключ: памятник, ограда, цоколь, плитка. Проект и монтаж AngelGranit, +7 701 056 7667.",
        "h1": "Мемориальные комплексы Алматы",
        "lead": "Единый проект места захоронения в Алматы: от фундамента до ограды и покрытия.",
        "focus": "мемориальные комплексы Алматы",
        "service": "Мемориальные комплексы Алматы",
    },
    {
        "slug": "ritualny-agent-almaty",
        "title": "Ритуальный агент Алматы 24/7 | AngelGranit",
        "description": "Ритуальный агент Алматы на связи день и ночь. Выезд, документы, организация похорон. Александр +7 701 056 7667.",
        "h1": "Ритуальный агент Алматы",
        "lead": "Вызов ритуального агента в Алматы: спокойные инструкции, выезд и координация всех служб 24/7.",
        "focus": "ритуальный агент Алматы",
        "service": "Ритуальный агент Алматы",
    },
    {
        "slug": "ritualnye-prinadlezhnosti-almaty",
        "title": "Ритуальные принадлежности Алматы | AngelGranit",
        "description": "Ритуальные принадлежности Алматы: гробы, венки, кресты, одежда, церковные наборы. Заказ 24/7 у AngelGranit, +7 701 056 7667.",
        "h1": "Ритуальные принадлежности Алматы",
        "lead": "Подбор ритуальных принадлежностей в Алматы к церемонии: от базового набора до расширенного оформления.",
        "focus": "ритуальные принадлежности Алматы",
        "service": "Ритуальные принадлежности Алматы",
    },
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def words(text: str) -> int:
    return len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", text), flags=re.UNICODE))


def ensure_meta(title: str, desc: str) -> tuple[str, str]:
    if len(title) > 65:
        title = title[:62].rstrip() + "…"
    if len(desc) < 150:
        desc = (desc.rstrip(".") + f". AngelGranit, {ADDRESS}, {PHONE}.").strip()
    if len(desc) > 160:
        # trim on word boundary
        cut = desc[:160]
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        desc = cut.rstrip(".,;:") + "."
        if len(desc) > 160:
            desc = desc[:157].rstrip() + "…"
    return title, desc


def related_links(current: str) -> list[dict]:
    out = []
    for p in PILLARS:
        if p["slug"] != current:
            out.append(p)
    return out[:7]


def faq_for(page: dict) -> list[dict]:
    f = page["focus"]
    base = [
        (f"Что входит в «{f}»?", f"Состав зависит от задачи семьи. Обычно это координация документов, транспорт, оформление церемонии и при необходимости памятник. Точный список озвучит {AGENT} по телефону {PHONE}."),
        (f"Сколько стоят услуги по направлению «{f}»?", "Ориентиры комплексов: от 150 000 ₸. Памятники и благоустройство считаются отдельно. Смету даём до начала ключевых работ."),
        ("Работаете ли вы круглосуточно?", "Да, AngelGranit принимает заявки 24/7 — ночью, в выходные и праздники."),
        ("Где ваш офис?", f"Офис: {ADDRESS}, Жетысуский район, Алматы. Выезд агента возможен к вам."),
        ("Можно заказать только одну услугу?", "Да. Не обязательно брать полный комплекс — можно катафалк, документы, венки или только памятник."),
        ("Как быстро приедет ритуальный агент?", "Время зависит от района и дороги. После звонка назовём ориентир подачи и начнём координацию сразу."),
        ("Делаете ли православные и мусульманские церемонии?", "Помогаем с логистикой и организацией с уважением к традиции семьи. Религиозные детали согласуются со священником или общиной."),
        ("Есть ли катафалк и междугородняя перевозка?", "Да, организуем катафалк по Алматы и перевозку по Казахстану по согласованию."),
        ("Когда ставить памятник после похорон?", "Срок зависит от грунта и сезона. Часто сначала временное оформление, затем постоянный гранитный памятник."),
        ("Как связаться прямо сейчас?", f"Телефон и WhatsApp: {PHONE}. Агент {AGENT}. Можно оставить заявку в форме на странице."),
        ("Работаете ли по всем районам Алматы?", "Да, выезжаем по всему городу и при необходимости в область."),
        ("Можно ли получить смету в WhatsApp?", "Да. Опишите ситуацию — пришлём понятный список позиций и ориентиры по цене."),
    ]
    return [{"q": q, "a": a} for q, a in base[:12]]


def figure_html(key: str, eager: bool = False) -> str:
    meta = SEO_IMAGES[key]
    loading = "eager" if eager else "lazy"
    fetch = ' fetchpriority="high"' if eager else ""
    src = f"../images/seo/{meta['file']}"
    return (
        f'<figure class="seo-figure">'
        f'<img src="{src}" alt="{esc(meta["alt"])}" title="{esc(meta["title"])}" '
        f'width="1600" height="900" loading="{loading}" decoding="async"{fetch} />'
        f"<figcaption>{esc(meta['alt'])}</figcaption>"
        f"</figure>"
    )


def gallery_html(keys: list[str]) -> str:
    items = "\n".join(figure_html(k) for k in keys)
    return (
        '<section class="seo-gallery" aria-label="Визуальные материалы">'
        "<h2>Визуальные материалы</h2>"
        '<p class="lead">Фотоматериалы для раздела — новые SEO-изображения сервиса AngelGranit.</p>'
        f'<div class="seo-gallery__grid">{items}</div>'
        "</section>"
    )


def body_html(page: dict) -> str:
    f = page["focus"]
    sn = page["service"]
    h1 = page["h1"]
    others = ", ".join(f'<a href="../{esc(p["slug"])}/">{esc(p["h1"])}</a>' for p in related_links(page["slug"])[:5])
    img_keys = PAGE_IMAGES.get(page["slug"], [])

    sections = [
        (
            f"Почему семьи ищут «{f}»",
            [
                f"Запрос «{f}» обычно означает не просто «купить услугу», а получить понятный порядок действий в тяжёлый день. В Алматы важно быстро понять: какие документы оформить, куда ехать, нужен ли зал, как подать катафалк и кто будет координатором.",
                f"AngelGranit работает как похоронное бюро и служба ритуальных услуг Алматы полного цикла. Мы помогаем с организацией похорон Алматы, ритуальным агентом на связи 24/7, катафалком, ритуальными принадлежностями и последующими памятниками Алматы.",
                f"Главный принцип — спокойствие и прозрачность. Сначала план и смета, затем исполнение. Так семья контролирует бюджет и не сталкивается с навязанными опциями.",
            ],
        ),
        (
            f"Как AngelGranit закрывает задачу «{sn}»",
            [
                f"После звонка агент {AGENT} уточняет обстоятельства и предлагает сценарий: минимально необходимое на ближайшие часы и то, что можно решить позже. Для похорон Алматы это критично — ночью особенно важна ясная инструкция.",
                f"Далее согласуются дата, маршрут, транспорт и состав оформления. Если нужен катафалк Алматы — фиксируем точки подачи. Если семья выбирает гранитные памятники Алматы или мемориальные комплексы Алматы, закладываем сроки изготовления отдельно от срочной церемонии.",
                f"В день прощания держим единый тайминг: зал или дом, храм при необходимости, кладбище. После церемонии остаёмся на связи по памятнику, ограде и уходу.",
            ],
        ),
        (
            "Документы, логистика и сопровождение",
            [
                f"Часть стресса в организации похорон Алматы связана с маршрутизацией между службами. Ритуальный агент Алматы помогает выстроить очередь действий и не терять время на повторные поездки.",
                f"Перевозка, катафалк Алматы и подача бригады планируются с запасом на дорожную ситуацию. Для иногородних родственников удобна удалённая координация в мессенджере.",
                f"Ритуальные принадлежности Алматы — гробы, венки, кресты, текстиль — подбираем под формат церемонии и бюджет, без давления «брать всё сразу».",
            ],
        ),
        (
            "Памятники и память после церемонии",
            [
                f"Даже если сегодня фокус на ритуальных услугах Алматы, многие семьи заранее думают о памятнике. Мы объясняем, когда лучше заказывать гранитные памятники Алматы и как устроена установка.",
                f"Мемориальные комплексы Алматы собираем модульно: стела, цоколь, ограда, плитка, стол и лавка. Можно начать с памятника и продолжить благоустройство в следующий сезон.",
                f"Климат города требует внимания к фундаменту и качеству камня. Поэтому изготовление и монтаж лучше держать у одного подрядчика.",
            ],
        ),
        (
            "Стоимость и честная смета",
            [
                f"Цена по направлению «{f}» зависит от состава. Ориентиры ритуальных комплексов — от 150 000 ₸. Катафалк, зал, расширенное оформление и памятники влияют на итог.",
                f"Мы даём разбивку позиций, чтобы можно было сравнить предложения. Прозрачность — часть сервиса похоронного бюро AngelGranit.",
                f"Если бюджет ограничен, помогаем выделить обязательное и перенести необязательное. Это относится и к ритуальным принадлежностям Алматы, и к граниту.",
            ],
        ),
        (
            "Кому подходит эта страница",
            [
                f"Страница «{h1}» полезна, если вы сравниваете ритуальные услуги Алматы, ищете ритуального агента Алматы ночью или хотите понять, как совместить похороны и заказ памятника.",
                f"Также сюда обращаются семьи, которым нужен только катафалк Алматы, только организация похорон Алматы или только памятники Алматы без полного пакета.",
                f"Смежные темы: {others}.",
            ],
        ),
        (
            "Практический алгоритм на ближайшие часы",
            [
                f"1) Позвоните {PHONE} или напишите в WhatsApp. 2) Кратко опишите район и что уже сделано. 3) Получите план и ориентир по срокам. 4) Согласуйте состав услуг и бюджет. 5) Доверьте координацию агенту {AGENT}.",
                f"Даже один звонок по запросу «{f}» часто снимает половину неопределённости. Офис: {ADDRESS}. Режим: 24/7.",
                f"AngelGranit воспринимает себя прежде всего как службу ритуальных услуг Алматы: похороны, сопровождение, транспорт, принадлежности — и только затем как мастерскую памятников.",
            ],
        ),
        (
            f"Дополнительно о качестве сервиса по теме «{f}»",
            [
                f"Качество ритуальных услуг Алматы измеряется не громкими обещаниями, а тем, совпал ли тайминг, приехал ли катафалк вовремя, понятна ли смета и остался ли у семьи контакт на потом.",
                f"Мы фиксируем договорённости и предупреждаем о следующих шагах заранее. Если обстоятельства меняются — пересобираем план, а не «молча меняем цену».",
                f"Для Google и для людей важно одно и то же: сайт должен честно отвечать на интент «ритуальные услуги Алматы». Поэтому на этой странице акцент на организации похорон, агенте, транспорте и поддержке семьи, а памятники показаны как логичное продолжение сервиса.",
                f"Если вы читаете текст ночью, сохраните номер {PHONE}. Ритуальный агент Алматы на связи. Похороны Алматы можно начать организовывать сразу после короткой консультации.",
                f"Нужна смежная услуга — откройте внутренние страницы сайта: организация похорон, катафалк, памятники, гранитные памятники, мемориальные комплексы, ритуальные принадлежности. Все они связаны перелинковкой и ведут к одному исполнителю — AngelGranit.",
            ],
        ),
        (
            "Районы Алматы и выезд агента",
            [
                f"AngelGranit принимает заявки из всех районов города. Неважно, где вы находитесь: помощь по теме «{f}» начинается с звонка, а не с поездки в офис.",
                f"Ритуальный агент Алматы может выехать к семье, в морг или к месту прощания. Это снижает хаос в первые часы и помогает согласовать организацию похорон Алматы без лишних переездов.",
                f"Если родственники живут в другом городе, координация идёт удалённо: смета, маршрут катафалка Алматы, список ритуальных принадлежностей Алматы и сроки памятников обсуждаются в WhatsApp.",
                f"Офис на {ADDRESS} удобен для очной встречи, выбора образцов и подписания договорённостей. Но срочные ритуальные услуги Алматы мы запускаем и без предварительного визита.",
            ],
        ),
        (
            "Что чаще всего входит в сценарий похорон",
            [
                f"Типичный сценарий похорон Алматы включает: фиксацию обстоятельств, согласование даты, подготовку тела при необходимости, подбор ритуальных принадлежностей, транспорт и церемонию.",
                f"Похоронное бюро Алматы AngelGranit помогает не «продать всё подряд», а собрать рабочий набор. Иногда достаточно базового комплекса; иногда семье важны расширенное оформление и отдельный зал.",
                f"Катафалк Алматы планируется под маршрут: дом или морг → храм/зал → кладбище. Междугородняя перевозка обсуждается отдельно с учётом расстояния и времени.",
                f"После прощания остаётся вопрос памяти: памятники Алматы, гранитные памятники Алматы или полноценные мемориальные комплексы Алматы. Эти работы можно отложить на удобный сезон, сохранив качество.",
            ],
        ),
        (
            "Как отличить понятный сервис от давления",
            [
                f"В поиске по запросу «{f}» легко встретить обещания «всё под ключ за час». Реалистичный сервис сначала уточняет факты и только потом называет сроки.",
                f"Хорошие ритуальные услуги Алматы дают письменную или хотя бы чёткую устную смету, объясняют, что можно упростить, и оставляют семье право выбора.",
                f"AngelGranit не подменяет религиозные решения семьи. Мы помогаем с логистикой организации похорон Алматы и уважаем выбранную традицию.",
                f"Если нужна только одна позиция — катафалк, венки, ритуальные принадлежности Алматы или замер под памятник — так и оформляем. Полный пакет не обязателен.",
            ],
        ),
        (
            "Память, гранит и сроки после церемонии",
            [
                f"Семьи часто спрашивают, когда заказывать памятники Алматы после похорон. Ответ зависит от грунта, сезона и того, нужен ли временный крест.",
                f"Гранитные памятники Алматы долговечны при правильном фундаменте и монтаже. Мы подсказываем формат портрета, шрифта и композиции под климат города.",
                f"Мемориальные комплексы Алматы удобны тем, кто хочет единый вид участка: стела, цоколь, ограда, покрытие. Можно двигаться этапами.",
                f"Даже обсуждая гранит, мы помним главный интент сайта: ритуальные услуги Алматы. Памятник — продолжение заботы, а не замена срочной помощи в день утраты.",
            ],
        ),
        (
            "Краткий итог для семьи",
            [
                f"Если вы ищете «{f}», вам нужен понятный план, живой контакт и исполнитель, который держит тайминг. AngelGranit работает как похоронное бюро Алматы с выездом и поддержкой 24/7.",
                f"Звоните {PHONE}: агент {AGENT} поможет с организацией похорон Алматы, катафалком, ритуальными принадлежностями и последующими памятниками.",
                f"Внутренняя навигация сайта связывает все ключевые темы — от ритуального агента до мемориальных комплексов — чтобы Google и люди видели единый сервис ритуальных услуг Алматы.",
                f"Сохраните номер и адрес {ADDRESS}. В трудный момент не нужно искать заново: ритуальные услуги Алматы у AngelGranit доступны круглосуточно.",
            ],
        ),
    ]

    parts = []
    insert_at = {0, 2, 4, 7, 10}  # after these section indexes
    img_i = 0
    for idx, (title, paras) in enumerate(sections):
        parts.append(f"<h2>{esc(title)}</h2>")
        for p in paras:
            parts.append(f"<p>{esc(p)}</p>")
        if idx in insert_at and img_i < len(img_keys):
            parts.append(figure_html(img_keys[img_i], eager=(img_i == 0)))
            img_i += 1
    # remaining images go to gallery (at least 2 leftovers ideally)
    leftover = img_keys[img_i:]
    if leftover:
        parts.append(gallery_html(leftover))
    elif len(img_keys) >= 2:
        # ensure gallery section still exists with last 2 reused from page set
        parts.append(gallery_html(img_keys[-2:]))
    return "\n".join(parts)


def render(page: dict) -> str:
    title, desc = ensure_meta(page["title"], page["description"])
    url = f"{BASE}/{page['slug']}/"
    faq = faq_for(page)
    article = body_html(page)
    related = related_links(page["slug"])
    page_imgs = PAGE_IMAGES.get(page["slug"], [])
    primary_img = SEO_IMAGES[page_imgs[0]] if page_imgs else None
    primary_img_url = f"{BASE}/images/seo/{primary_img['file']}" if primary_img else f"{BASE}/images/hero-angelgranit.png"

    faq_html = "\n".join(
        f"<details><summary>{esc(i['q'])}</summary><p>{esc(i['a'])}</p></details>" for i in faq
    )
    rel_html = "\n".join(
        f'<a href="../{esc(p["slug"])}/"><strong>{esc(p["h1"])}</strong><span>{esc(p["lead"][:110])}…</span></a>'
        for p in related
    )

    image_objects = [
        {
            "@type": "ImageObject",
            "contentUrl": f"{BASE}/images/seo/{SEO_IMAGES[k]['file']}",
            "url": f"{BASE}/images/seo/{SEO_IMAGES[k]['file']}",
            "name": SEO_IMAGES[k]["title"],
            "description": SEO_IMAGES[k]["alt"],
            "width": 1600,
            "height": 900,
            "encodingFormat": "image/webp",
        }
        for k in page_imgs
    ]

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{BASE}/#website",
                "url": f"{BASE}/",
                "name": "AngelGranit",
                "alternateName": "Ритуальные услуги Алматы — AngelGranit",
                "inLanguage": "ru-KZ",
                "publisher": {"@id": f"{BASE}/#organization"},
            },
            {
                "@type": "Organization",
                "@id": f"{BASE}/#organization",
                "name": "AngelGranit",
                "url": f"{BASE}/",
                "telephone": PHONE_TEL,
                "logo": f"{BASE}/images/hero-angelgranit.png",
            },
            {
                "@type": ["LocalBusiness", "FuneralHome"],
                "@id": f"{BASE}/#business",
                "name": "AngelGranit",
                "image": f"{BASE}/images/hero-angelgranit.png",
                "url": f"{BASE}/",
                "telephone": PHONE_TEL,
                "priceRange": "₸₸₸",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": ADDRESS,
                    "addressLocality": "Алматы",
                    "addressCountry": "KZ",
                },
                "geo": {"@type": "GeoCoordinates", "latitude": 43.289921, "longitude": 76.961065},
                "openingHours": "Mo-Su 00:00-24:00",
                "areaServed": {"@type": "City", "name": "Алматы"},
            },
            {
                "@type": "WebPage",
                "@id": url + "#webpage",
                "url": url,
                "name": title,
                "description": desc,
                "isPartOf": {"@id": f"{BASE}/#website"},
                "about": {"@id": f"{BASE}/#business"},
                "primaryImageOfPage": {
                    "@type": "ImageObject",
                    "url": primary_img_url,
                    "width": 1600,
                    "height": 900,
                },
                "image": [f"{BASE}/images/seo/{SEO_IMAGES[k]['file']}" for k in page_imgs],
            },
            {
                "@type": "Service",
                "name": page["service"],
                "description": desc,
                "provider": {"@id": f"{BASE}/#business"},
                "areaServed": {"@type": "City", "name": "Алматы"},
                "url": url,
                "image": primary_img_url,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": (
                    [
                        {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
                        {"@type": "ListItem", "position": 2, "name": page["h1"], "item": url},
                    ]
                    if page["slug"] == "ritualnye-uslugi-almaty"
                    else [
                        {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
                        {"@type": "ListItem", "position": 2, "name": "Ритуальные услуги Алматы", "item": f"{BASE}/ritualnye-uslugi-almaty/"},
                        {"@type": "ListItem", "position": 3, "name": page["h1"], "item": url},
                    ]
                ),
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": i["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": i["a"]},
                    }
                    for i in faq
                ],
            },
            *image_objects,
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#d4af57" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:site_name" content="AngelGranit — ритуальные услуги Алматы" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:image" content="{primary_img_url}" />
  <meta property="og:image:alt" content="{esc(page['h1'])} — AngelGranit" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{primary_img_url}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" href="../seo/assets/seo.css" as="style" />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../seo/assets/seo.css" />
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <header class="nav">
    <a class="nav__brand" href="../"><strong>AngelGranit</strong><span>AG</span></a>
    <div class="nav__actions">
      <a class="btn btn--ghost" href="../">На главную</a>
      <a class="btn btn--gold" href="tel:{PHONE_TEL}">Позвонить</a>
      <a class="btn btn--wa" href="#" data-wa-default target="_blank" rel="noopener noreferrer">WhatsApp</a>
    </div>
  </header>
  <main>
    <div class="wrap">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../">Главная</a></li>
          {"" if page["slug"] == "ritualnye-uslugi-almaty" else '<li><a href="../ritualnye-uslugi-almaty/">Ритуальные услуги Алматы</a></li>'}
          <li aria-current="page">{esc(page['h1'])}</li>
        </ol>
      </nav>
      <header class="hero">
        <p class="hero__kicker">Ритуальные услуги Алматы · 24/7</p>
        <h1>{esc(page['h1'])}</h1>
        <p class="hero__lead">{esc(page['lead'])}</p>
        <div class="hero__cta">
          <a class="btn btn--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn btn--wa" href="#" data-wa-default target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn btn--ghost" href="#lead">Заявка</a>
        </div>
        <figure class="hero__media">
          <img src="../images/hero-angelgranit.png" alt="{esc(page['h1'])} — ритуальные услуги Алматы, AngelGranit" width="1024" height="408" decoding="async" fetchpriority="high" />
        </figure>
      </header>
      <article class="article">
{article}
      </article>
      <div class="cta-bar">
        <p><strong>Ритуальные услуги Алматы 24/7.</strong> Агент {AGENT} — {esc(PHONE)}, офис {esc(ADDRESS)}.</p>
        <a class="btn btn--gold" href="tel:{PHONE_TEL}">Звонок</a>
        <a class="btn btn--wa" href="#" data-wa-default target="_blank" rel="noopener noreferrer">WhatsApp</a>
      </div>
    </div>
    <section class="section-block" id="faq">
      <div class="wrap">
        <h2>FAQ — частые вопросы</h2>
        <p class="lead">Не меньше десяти практических ответов по теме страницы.</p>
        <div class="faq">{faq_html}</div>
      </div>
    </section>
    <section class="section-block">
      <div class="wrap">
        <h2>Связанные страницы</h2>
        <div class="related">{rel_html}</div>
      </div>
    </section>
    <section class="section-block" id="lead">
      <div class="wrap">
        <div class="form-card">
          <h2>Заявка на ритуальные услуги Алматы</h2>
          <form id="seo-lead-form">
            <div class="form-grid form-grid--2">
              <label>Имя<input name="name" required /></label>
              <label>Телефон<input name="phone" type="tel" required /></label>
            </div>
            <div class="form-grid" style="margin-top:0.75rem">
              <label>Услуга<select name="service"><option>{esc(page['service'])}</option><option>Ритуальные услуги Алматы</option><option>Организация похорон</option><option>Катафалк</option><option>Памятник</option></select></label>
              <label>Сообщение<textarea name="message"></textarea></label>
            </div>
            <div class="form-actions">
              <button class="btn btn--wa" type="submit">Отправить в WhatsApp</button>
              <a class="btn btn--gold" href="tel:{PHONE_TEL}">Позвонить</a>
            </div>
          </form>
        </div>
      </div>
    </section>
  </main>
  <footer class="footer">
    <strong>AngelGranit</strong>
    Ритуальные услуги Алматы · {AGENT} · {esc(ADDRESS)} · <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
    <ul class="footer-links">
      <li><a href="../">Главная</a></li>
      <li><a href="../ritualnye-uslugi-almaty/">Ритуальные услуги</a></li>
      <li><a href="../seo/">Справочник</a></li>
      <li><a href="../seo/kontakty/">Контакты</a></li>
    </ul>
  </footer>
  <script src="../seo/assets/seo.js" defer></script>
</body>
</html>
"""


def write_sitemap(extra_paths: list[str]) -> None:
    # Keep existing seo pages + root pillars + home
    seo_dir = ROOT / "seo"
    urls = [(f"{BASE}/", "1.0"), (f"{BASE}/seo/", "0.8")]
    for slug in extra_paths:
        urls.append((f"{BASE}/{slug}/", "0.95"))
    if seo_dir.exists():
        for p in sorted(seo_dir.iterdir()):
            if p.is_dir() and (p / "index.html").exists() and p.name != "assets":
                urls.append((f"{BASE}/seo/{p.name}/", "0.7"))
    # dedupe
    seen = set()
    uniq = []
    for loc, pr in urls:
        if loc not in seen:
            seen.add(loc)
            uniq.append((loc, pr))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pr in uniq:
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{pr}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    low = []
    for page in PILLARS:
        out = ROOT / page["slug"]
        out.mkdir(parents=True, exist_ok=True)
        html_out = render(page)
        (out / "index.html").write_text(html_out, encoding="utf-8", newline="\n")
        # Also set canonical hint page under seo/ if exists
        w = words(html_out)
        status = "OK" if w >= 1200 else "LOW"
        if w < 1200:
            low.append((page["slug"], w))
        print(f"[{status}] /{page['slug']}/ words~={w} title={len(page['title'])} desc={len(ensure_meta(page['title'], page['description'])[1])}")
    write_sitemap([p["slug"] for p in PILLARS])
    print("sitemap updated, pages:", len(PILLARS))
    if low:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
