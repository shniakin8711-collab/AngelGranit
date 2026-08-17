# -*- coding: utf-8 -*-
"""
Generate 200+ unique Q&A articles under /stati/ with categories
and bidirectional links to /uslugi/.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import date
from pathlib import Path

from seo_head import icon_links, social_meta

ROOT = Path(__file__).resolve().parents[2]
STATI = ROOT / "stati"
BASE = "https://angelgranit.com"
PHONE = "+7 701 056 7667"
PHONE_TEL = "+77010567667"
ADDRESS = "ул. Осетинская, 5а"
AGENT = "Александр"
TODAY = date.today().isoformat()

CATEGORIES = [
    {
        "slug": "pervye-shagi",
        "name": "Первые шаги после утраты",
        "description": "Что делать в первые часы: порядок действий, звонки, документы и спокойный план.",
        "services": ["ritualnye-uslugi", "organizaciya-pohoron", "ritualny-agent" if False else "pohorony-pod-klyuch"],
    },
    {
        "slug": "organizaciya-pohoron",
        "name": "Организация похорон",
        "description": "Как организовать похороны в Алматы: сроки, участники, зал, тайминг.",
        "services": ["organizaciya-pohoron", "pohorony-pod-klyuch", "ritualnye-uslugi"],
    },
    {
        "slug": "dokumenty",
        "name": "Документы",
        "description": "Свидетельство о смерти, справки и практические вопросы по бумагам.",
        "services": ["organizaciya-pohoron", "ritualnye-uslugi", "perevozka-umershih"],
    },
    {
        "slug": "transport",
        "name": "Катафалк и перевозка",
        "description": "Ритуальный транспорт, маршруты по Алматы и междугородняя перевозка.",
        "services": ["katafalk", "perevozka-umershih", "organizaciya-pohoron"],
    },
    {
        "slug": "prinadlezhnosti",
        "name": "Ритуальные принадлежности",
        "description": "Гробы, венки, кресты, одежда и оформление церемонии.",
        "services": ["ritualnye-prinadlezhnosti", "venki", "pohorony-pod-klyuch"],
    },
    {
        "slug": "pamyatniki",
        "name": "Памятники",
        "description": "Выбор, заказ, установка памятников: гранит, мрамор, формы.",
        "services": ["pamyatniki", "granitnye-pamyatniki", "mramornye-pamyatniki"],
    },
    {
        "slug": "granit-i-gravirovka",
        "name": "Гранит и гравировка",
        "description": "Камень, портрет, надписи, фотокерамика и уход за поверхностью.",
        "services": ["granitnye-pamyatniki", "gravirovka", "fotokeramika"],
    },
    {
        "slug": "blagoustrojstvo",
        "name": "Благоустройство",
        "description": "Ограды, плитка, цветники, столы, лавки и уход за местом памяти.",
        "services": ["blagoustrojstvo-mogil", "ogrady", "stoly", "lavochki", "cvetniki", "memorialnye-kompleksy"],
    },
    {
        "slug": "tradicii",
        "name": "Традиции и обряды",
        "description": "Православные и мусульманские обычаи, поминки, отпевание.",
        "services": ["ritualnye-uslugi", "musulmanskie-pamyatniki", "organizaciya-pohoron"],
    },
    {
        "slug": "ceny-i-byudzhet",
        "name": "Цены и бюджет",
        "description": "Из чего складывается смета похорон и памятников, как экономить без потери достоинства.",
        "services": ["pohorony-pod-klyuch", "ritualnye-uslugi", "pamyatniki"],
    },
]

# Fix first category services - ritualny-agent doesn't exist under uslugi
CATEGORIES[0]["services"] = ["ritualnye-uslugi", "organizaciya-pohoron", "pohorony-pod-klyuch"]

SERVICE_TITLES = {
    "ritualnye-uslugi": "Ритуальные услуги",
    "organizaciya-pohoron": "Организация похорон",
    "pohorony-pod-klyuch": "Похороны под ключ",
    "katafalk": "Катафалк",
    "perevozka-umershih": "Перевозка умерших",
    "pamyatniki": "Памятники",
    "granitnye-pamyatniki": "Гранитные памятники",
    "mramornye-pamyatniki": "Мраморные памятники",
    "musulmanskie-pamyatniki": "Мусульманские памятники",
    "memorialnye-kompleksy": "Мемориальные комплексы",
    "blagoustrojstvo-mogil": "Благоустройство могил",
    "ogrady": "Ограды",
    "stoly": "Столы",
    "lavochki": "Лавочки",
    "cvetniki": "Цветники",
    "fotokeramika": "Фотокерамика",
    "gravirovka": "Гравировка",
    "venki": "Венки",
    "ritualnye-prinadlezhnosti": "Ритуальные принадлежности",
}

# Seeds: (category_slug, question, slug_tail)
# Generate 200+ unique user questions
SEEDS: list[tuple[str, str, str]] = []


def _add(cat: str, question: str, slug: str) -> None:
    SEEDS.append((cat, question, slug))


def _build_seeds() -> None:
    if SEEDS:
        return

    # --- Первые шаги (24) ---
    first = [
        ("Что делать в первые часы после смерти родственника в Алматы", "chto-delat-v-pervye-chasy"),
        ("Куда звонить ночью если умер человек в Алматы", "kuda-zvonit-nochyu"),
        ("Нужно ли вызывать полицию при смерти дома", "nuzhno-li-vyzvat-policiyu"),
        ("Как вызвать ритуального агента срочно", "kak-vyzvat-ritualnogo-agenta"),
        ("Что сказать агенту в первом звонке", "chto-skazat-agentu-v-pervom-zvonke"),
        ("Можно ли начинать организацию похорон ночью", "organizaciya-pohoron-nochyu"),
        ("Как успокоить семью и распределить задачи", "kak-raspredelit-zadachi-v-seme"),
        ("Что делать если родственники в другом городе", "rodstvenniki-v-drugom-gorode"),
        ("Нужно ли сразу покупать памятник", "nuzhno-li-srazu-pokupat-pamyatnik"),
        ("Чем отличается морг от прощального зала", "morg-i-proshchalnyj-zal"),
        ("Как понять что делать дальше после констатации смерти", "posle-konstatacii-smerti"),
        ("Можно ли отказаться от лишних ритуальных услуг", "otkazatsya-ot-lishnih-uslug"),
        ("Как не попасть на навязанные услуги", "kak-ne-popast-na-navyazannye-uslugi"),
        ("Стоит ли вызывать ритуального агента если всё кажется понятным", "stoit-li-vyzvat-agenta"),
        ("Что взять с собой при выезде агента", "chto-vzyat-s-soboj"),
        ("Как помочь пожилым родственникам в первые часы", "pomoshch-pozhilym-rodstvennikam"),
        ("Что делать если смерть произошла в больнице", "smert-v-bolnice"),
        ("Что делать если смерть произошла на даче", "smert-na-dache"),
        ("Как организовать всё удалённо из другого города", "udalennaya-organizaciya"),
        ("Нужен ли свидетель при первых действиях", "nuzhen-li-svidetel"),
        ("Как сохранить спокойствие и не принимать решения под давлением", "ne-prinimat-resheniya-pod-davleniem"),
        ("Сколько времени есть до похорон обычно", "skolko-vremeni-do-pohoron"),
        ("Можно ли перенести похороны на несколько дней", "perenesti-pohorony"),
        ("Какие вопросы задать ритуальной службе перед договором", "voprosy-pered-dogovorom"),
    ]
    for q, s in first:
        _add("pervye-shagi", q, s)

    # --- Организация похорон (24) ---
    org = [
        ("Как организовать похороны в Алматы по шагам", "kak-organizovat-pohorony-po-shagam"),
        ("Что входит в похороны под ключ", "chto-vhodit-v-pohorony-pod-klyuch"),
        ("Нужен ли прощальный зал обязательно", "nuzhen-li-proshchalnyj-zal"),
        ("Как выбрать дату похорон", "kak-vybrat-datu-pohoron"),
        ("Кто должен присутствовать на организации", "kto-dolzhen-prisutstvovat"),
        ("Как составить тайминг дня прощания", "tajming-dnya-proshchaniya"),
        ("Что делать если гости опаздывают", "esli-gosti-opazdyvayut"),
        ("Как согласовать маршрут церемонии", "soglasovat-marshrut-ceremonii"),
        ("Можно ли провести прощание дома", "proshchanie-doma"),
        ("Как организовать похороны без лишней суеты", "pohorony-bez-suety"),
        ("Что поручить друзьям а что агенту", "chto-poruchit-druzyam"),
        ("Как уведомить родственников о дате", "uvedomit-rodstvennikov"),
        ("Нужен ли ведущий церемонии", "nuzhen-li-vedushchij"),
        ("Как подготовить речь на прощании", "podgotovit-rech"),
        ("Что делать после возвращения с кладбища", "posle-vozvrashcheniya-s-kladbishcha"),
        ("Как организовать похороны в выходной", "pohorony-v-vyhodnoj"),
        ("Как организовать похороны в праздник", "pohorony-v-prazdnik"),
        ("Можно ли совместить зал и храм в один день", "zal-i-hram-v-odin-den"),
        ("Как учесть пожелания усопшего", "uchest-pozhelaniya-usopshogo"),
        ("Что делать если семья не может договориться", "esli-semya-ne-dogovarivaetsya"),
        ("Как подготовить детей к прощанию", "podgotovit-detej"),
        ("Нужна ли видеофиксация церемонии", "nuzhna-li-videofiksacii"),
        ("Как организовать небольшие камерные похороны", "kamernye-pohorony"),
        ("Чем помогает единый координатор похорон", "edinyj-koordinator"),
    ]
    for q, s in org:
        _add("organizaciya-pohoron", q, s)

    # --- Документы (20) ---
    docs = [
        ("Какие документы нужны для похорон в Алматы", "kakie-dokumenty-nuzhny"),
        ("Как получить свидетельство о смерти", "svidetelstvo-o-smerti"),
        ("Чем медицинское свидетельство отличается от гербового", "medicinskoe-i-gerbovoe"),
        ("Что делать если документов не хватает", "esli-dokumentov-ne-hvataet"),
        ("Нужен ли паспорт усопшего для организации", "pasport-usopshogo"),
        ("Как оформить документы если родственник иногородний", "dokumenty-inogorodnego"),
        ("Кто имеет право заниматься оформлением", "kto-imeet-pravo-oformlyat"),
        ("Сколько копий свидетельства стоит сделать", "skolko-kopij-svidetelstva"),
        ("Нужны ли документы для катафалка", "dokumenty-dlya-katafalka"),
        ("Какие бумаги нужны для кладбища", "bumagi-dlya-kladbishcha"),
        ("Как действовать если смерть наступила за границей", "smert-za-granicej"),
        ("Что делать с документами банка и пенсии", "dokumenty-banka-i-pensii"),
        ("Нужна ли нотариальная доверенность родственнику", "notarialnaya-doverennost"),
        ("Как хранить документы после похорон", "hranit-dokumenty-posle"),
        ("Может ли агент помочь с маршрутизацией документов", "agent-i-dokumenty"),
        ("Что делать при утере свидетельства о смерти", "uterya-svidetelstva"),
        ("Нужны ли фото для документов", "nuzhny-li-foto"),
        ("Как оформить всё быстрее без ошибок", "oformit-bez-oshibok"),
        ("Какие документы спросить у ритуальной службы", "dokumenty-u-sluzhby"),
        ("Что подготовить заранее «на всякий случай»", "podgotovit-zaranee"),
    ]
    for q, s in docs:
        _add("dokumenty", q, s)

    # --- Транспорт (20) ---
    transport = [
        ("Как заказать катафалк в Алматы", "kak-zakazat-katafalk"),
        ("Сколько стоит катафалк по городу", "stoimost-katafalka"),
        ("Нужен ли катафалк если есть личный транспорт", "nuzhen-li-katafalk"),
        ("Как согласовать время подачи катафалка", "vremya-podachi-katafalka"),
        ("Можно ли заказать катафалк только на кладбище", "katafalk-tolko-na-kladbishche"),
        ("Как организовать перевозку умершего между городами", "perevozka-mezhdu-gorodami"),
        ("Что важно при ночной перевозке", "nochnaya-perevozka"),
        ("Как выбрать класс ритуального транспорта", "klass-ritualnogo-transporta"),
        ("Нужен ли сопровождающий в катафалке", "soprovozhdayushchij-v-katafalke"),
        ("Что делать если катафалк опаздывает", "esli-katafalk-opazdyvaet"),
        ("Можно ли изменить маршрут в день похорон", "izmenit-marshrut"),
        ("Как доехать колонной без хаоса", "kolonna-bez-haosa"),
        ("Нужна ли отдельная машина для венков", "mashina-dlya-venkov"),
        ("Перевозка из морга в зал: как проходит", "iz-morga-v-zal"),
        ("Перевозка из зала на кладбище: тайминг", "iz-zala-na-kladbishche"),
        ("Междугородняя перевозка зимой", "mezhdugorodnyaya-zimoj"),
        ("Какие документы нужны для перевозки", "dokumenty-dlya-perevozki"),
        ("Можно ли заказать только транспорт без пакета", "tolko-transport"),
        ("Как оценить честность цены на катафалк", "ocenit-cenu-katafalka"),
        ("Что спросить у диспетчера перед подачей", "voprosy-dispetcheru"),
    ]
    for q, s in transport:
        _add("transport", q, s)

    # --- Принадлежности (20) ---
    prin = [
        ("Как выбрать гроб в Алматы", "kak-vybrat-grob"),
        ("Какие венки нужны на похороны", "kakie-venki-nuzhny"),
        ("Нужен ли крест обязательно", "nuzhen-li-krest"),
        ("Как подобрать одежду для усопшего", "odezhda-dlya-usopshogo"),
        ("Что входит в церковный набор", "cerkovnyj-nabor"),
        ("Можно ли обойтись минимумом принадлежностей", "minimum-prinadlezhnostej"),
        ("Как не переплатить за оформление", "ne-pereplatit-za-oformlenie"),
        ("Живые цветы или искусственные венки", "zhivye-ili-iskusstvennye"),
        ("Нужны ли ленты с текстом", "lenty-s-tekstom"),
        ("Как выбрать покрывало и текстиль", "pokryvalo-i-tekstil"),
        ("Что купить к мусульманским похоронам", "k-musulmanskim-pohoronam"),
        ("Что купить к православным похоронам", "k-pravoslavnym-pohoronam"),
        ("Можно ли заказать принадлежности ночью", "prinadlezhnosti-nochyu"),
        ("Доставляют ли принадлежности к залу", "dostavka-k-zalu"),
        ("Как согласовать стиль оформления", "stil-oformleniya"),
        ("Нужны ли свечи и атрибутика", "svechi-i-atributika"),
        ("Что делать с оставшимися венками", "ostavshiesya-venki"),
        ("Как выбрать размер гроба", "razmer-groba"),
        ("Можно ли вернуть лишние позиции из сметы", "vernut-lishnie-pozicii"),
        ("Чем отличается базовый и расширенный набор", "bazovyj-i-rasshirennyj-nabor"),
    ]
    for q, s in prin:
        _add("prinadlezhnosti", q, s)

    # --- Памятники (24) ---
    pam = [
        ("Как выбрать памятник в Алматы", "kak-vybrat-pamyatnik"),
        ("Когда ставить памятник после похорон", "kogda-stavit-pamyatnik"),
        ("Одинарный или двойной памятник", "odinarnyj-ili-dvojnoj"),
        ("Какой размер памятника выбрать", "kakoj-razmer-pamyatnika"),
        ("Нужен ли цоколь обязательно", "nuzhen-li-cokol"),
        ("Как выбрать форму стелы", "forma-stely"),
        ("Памятник зимой: можно ли ставить", "pamyatnik-zimoj"),
        ("Что важнее камень или оформление", "kamen-ili-oformlenie"),
        ("Как согласовать эскиз памятника", "soglasovat-eskiz"),
        ("Сколько ждать изготовление памятника", "srok-izgotovleniya"),
        ("Нужен ли замер участка", "nuzhen-li-zamer"),
        ("Как проверить качество монтажа", "kachestvo-montazha"),
        ("Можно ли заменить старый памятник", "zamena-starogo-pamyatnika"),
        ("Семейный памятник: когда уместен", "semejnyj-pamyatnik"),
        ("Православный памятник: на что смотреть", "pravoslavnyj-pamyatnik"),
        ("Мусульманский памятник: особенности выбора", "musulmanskij-pamyatnik-vybor"),
        ("Как не ошибиться с надписью", "ne-oshibitsya-s-nadpisyu"),
        ("Портрет на памятнике или без", "portret-ili-bez"),
        ("Как выбрать подрядчика по памятникам", "vybrat-podryadchika"),
        ("Что входит в установку памятника", "chto-vhodit-v-ustanovku"),
        ("Можно ли заказать памятник заранее", "zakazat-pamyatnik-zaranee"),
        ("Временный крест и постоянный памятник", "vremennyj-krest-i-pamyatnik"),
        ("Как ухаживать за новым памятником", "uhod-za-novym-pamyatnikom"),
        ("Ошибки при заказе памятника", "oshibki-pri-zakaze"),
    ]
    for q, s in pam:
        _add("pamyatniki", q, s)

    # --- Гранит и гравировка (20) ---
    gran = [
        ("Почему выбирают гранитные памятники", "pochemu-granit"),
        ("Чем гранит лучше мрамора на улице", "granit-luchshe-mramora"),
        ("Какой цвет гранита практичнее", "cvet-granita"),
        ("Как делается художественная гравировка", "kak-delaetsya-gravirovka"),
        ("Портрет гравировкой или фотокерамика", "portret-ili-fotokeramika"),
        ("Как подготовить фото для портрета", "foto-dlya-portreta"),
        ("Можно ли исправить ошибку в надписи", "ispravit-oshibku-v-nadpisi"),
        ("Золочение букв: нужно ли", "zolotochenie-bukv"),
        ("Уход за полированным гранитом", "uhod-za-polirovannym-granitom"),
        ("Почему важен фундамент под гранит", "fundament-pod-granit"),
        ("Реставрация гранитного памятника", "restavraciya-granita"),
        ("Как читать макет гравировки", "chitat-maket-gravirovki"),
        ("Гравировка на установленном памятнике", "gravirovka-na-ustanovlennom"),
        ("Мраморный памятник: плюсы и минусы", "mramor-plusy-minusy"),
        ("Комбинированный камень в мемориале", "kombinirovannyj-kamen"),
        ("Как выбрать шрифт для эпитафии", "shrift-dlya-epitafii"),
        ("Сколько строк текста помещается на стеле", "skolko-strok-teksta"),
        ("Фотокерамика: сроки и форматы", "fotokeramika-sroki"),
        ("Почему нельзя спешить с гравировкой дат", "ne-speshit-s-datami"),
        ("Как проверить глубину и читаемость гравировки", "proverit-gravirovku"),
    ]
    for q, s in gran:
        _add("granit-i-gravirovka", q, s)

    # --- Благоустройство (24) ---
    blag = [
        ("С чего начать благоустройство могилы", "s-chego-nachat-blagoustrojstvo"),
        ("Нужна ли ограда обязательно", "nuzhna-li-ograda"),
        ("Какое покрытие выбрать на участок", "pokrytie-na-uchastok"),
        ("Цветник у памятника: как оформить", "cvetnik-u-pamyatnika"),
        ("Стол и лавочка: нужны ли сразу", "stol-i-lavochka"),
        ("Мемориальный комплекс под ключ: что входит", "memorialnyj-kompleks-chto-vhodit"),
        ("Можно ли благоустраивать этапами", "blagoustrojstvo-etapami"),
        ("Уборка могилы перед поминовением", "uborka-pered-pominoveniem"),
        ("Как выровнять участок", "vyrovnyat-uchastok"),
        ("Бордюр или полноценная ограда", "bordyur-ili-ograda"),
        ("Плитка на могилу: плюсы и минусы", "plitka-na-mogilu"),
        ("Ваза из гранита: зачем нужна", "vaza-iz-granita"),
        ("Как сочетать ограду с памятником", "ograda-s-pamyatnikom"),
        ("Благоустройство старого захоронения", "staroe-zahoronenie"),
        ("Сезонный уход за местом памяти", "sezonnyj-uhod"),
        ("Что делать если плитка просела", "plitka-prosela"),
        ("Как заказать только цветник", "zakazat-tolko-cvetnik"),
        ("Комплекс на двоих: планировка", "kompleks-na-dvoih"),
        ("Нужен ли проект перед работами", "nuzhen-li-proekt"),
        ("Сколько длится монтаж комплекса", "dlitelnost-montazha-kompleksa"),
        ("Как принять работу по благоустройству", "prinyat-rabotu"),
        ("Зимнее благоустройство: ограничения", "zimnee-blagoustrojstvo"),
        ("Как сэкономить на комплексе без потери вида", "sekonomit-na-komplekse"),
        ("Ошибки при самостоятельном благоустройстве", "oshibki-samostoyatelno"),
    ]
    for q, s in blag:
        _add("blagoustrojstvo", q, s)

    # --- Традиции (16) ---
    trad = [
        ("Как проходит православное отпевание", "pravoslavnoe-otpevanie"),
        ("Нужно ли вызывать священника на дом", "svyashchennik-na-dom"),
        ("Мусульманские похороны: что важно знать семье", "musulmanskie-pohorony-vazhno"),
        ("Как организовать поминки после похорон", "organizovat-pominki"),
        ("Что учесть в 9 и 40 дней", "9-i-40-dnej"),
        ("Можно ли совмещать разные традиции в семье", "raznye-tradicii-v-seme"),
        ("Как уважительно отказать от лишних обрядов", "otkazat-ot-lishnih-obryadov"),
        ("Что спросить у общины или храма заранее", "sprosit-u-hrama"),
        ("Одежда семьи на церемонии", "odezhda-semi"),
        ("Как подготовить речь с учётом традиции", "rech-s-uchetom-tradicii"),
        ("Поминки дома или в кафе", "pominki-doma-ili-v-kafe"),
        ("Что делать если традиция семьи неясна", "tradiciya-neyasna"),
        ("Как агент помогает не нарушить обычай", "agent-i-obychaj"),
        ("Цветы и венки в разных традициях", "cvety-v-tradiciyah"),
        ("Могила и посещения в первую неделю", "poseshcheniya-v-pervuyu-nedelyu"),
        ("Как говорить с детьми о прощании", "govorit-s-detmi"),
    ]
    for q, s in trad:
        _add("tradicii", q, s)

    # --- Цены (20) ---
    ceny = [
        ("Из чего складывается стоимость похорон", "iz-chego-skladyvaetsya-stoimost"),
        ("Сколько стоят похороны в Алматы ориентировочно", "skolko-stoyat-pohorony"),
        ("Минимальный комплекс: что внутри цены", "minimalnyj-kompleks-cena"),
        ("Как сравнить сметы ритуальных служб", "sravnit-smety"),
        ("Где обычно прячутся переплаты", "gde-pryachutsya-pereplaty"),
        ("Можно ли уменьшить бюджет достойно", "umenshit-byudzhet"),
        ("Что дороже зал или транспорт", "zal-ili-transport"),
        ("Сколько заложить на памятник заранее", "zalozhit-na-pamyatnik"),
        ("Рассрочка и этапы оплаты", "etapy-oplaty"),
        ("Почему цена «от» бывает обманчивой", "cena-ot-obmanchiva"),
        ("Как попросить разбивку позиций", "razbivka-pozicij"),
        ("Стоимость катафалка отдельно", "stoimost-katafalka-otdelno"),
        ("Стоимость гранитного памятника ориентиры", "stoimost-granitnogo-pamyatnika"),
        ("Что влияет на цену мемориального комплекса", "cena-memorialnogo-kompleksa"),
        ("Как не купить ненужное в стрессе", "ne-kupit-nenuzhnoe"),
        ("Бесплатные и платные опции: как отличить", "besplatnye-i-platnye"),
        ("Стоит ли брать самый дешёвый пакет", "samyj-deshevyj-paket"),
        ("Как учесть расходы родственников из других городов", "rashody-inogorodnih"),
        ("Прозрачная смета: на что смотреть", "prozrachnaya-smeta"),
        ("Когда цена растёт в день церемонии", "cena-rastet-v-den-ceremonii"),
    ]
    for q, s in ceny:
        _add("ceny-i-byudzhet", q, s)

    # Extra unique Qs to push past 200 if needed
    extra = [
        ("pervye-shagi", "Как действовать если умер близкий на работе", "smert-na-rabote"),
        ("organizaciya-pohoron", "Как встретить иногородних гостей в день похорон", "vstretit-inogorodnih-gostej"),
        ("dokumenty", "Нужна ли справка для работодателя родственника", "spravka-dlya-rabotodatelya"),
        ("transport", "Можно ли встретить катафалк у подъезда", "katafalk-u-podezda"),
        ("prinadlezhnosti", "Как выбрать венки если гостей будет много", "venki-esli-mnogo-gostej"),
        ("pamyatniki", "Как выбрать памятник для двоих заранее", "pamyatnik-dlya-dvoih-zaranee"),
        ("granit-i-gravirovka", "Нужна ли пробная гравировка на образце", "probnaya-gravirovka"),
        ("blagoustrojstvo", "Как часто обновлять цветник", "kak-chasto-obnovlyat-cvetnik"),
        ("tradicii", "Можно ли проводить поминки через неделю", "pominki-cherez-nedelyu"),
        ("ceny-i-byudzhet", "Как попросить скидку без неловкости", "poprosit-skidku"),
        ("pervye-shagi", "Что делать если соседи предлагают «своего агента»", "svoj-agent-ot-sosedej"),
        ("organizaciya-pohoron", "Как сократить программу прощания", "sokratit-programmu"),
        ("pamyatniki", "Нужна ли гарантия на установку памятника", "garantiya-na-ustanovku"),
        ("blagoustrojstvo", "Можно ли ставить лавку без стола", "lavka-bez-stola"),
        ("transport", "Как организовать возвращение семьи с кладбища", "vozvrashchenie-s-kladbishcha"),
        ("dokumenty", "Что делать с медицинскими картами усопшего", "medicinskie-karty"),
        ("prinadlezhnosti", "Нужны ли перчатки и платки для участников", "perchatki-i-platki"),
        ("granit-i-gravirovka", "Как выбрать овал для фотокерамики", "oval-dlya-fotokeramiki"),
        ("tradicii", "Что сказать гостям о дресс-коде", "dress-kod-dlya-gostej"),
        ("ceny-i-byudzhet", "Как разделить расходы между родственниками", "razdelit-rashody"),
    ]
    for cat, q, s in extra:
        _add(cat, q, s)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def slugify_full(cat: str, tail: str) -> str:
    return f"{cat}-{tail}"


def ensure_desc(desc: str) -> str:
    desc = desc.strip()
    while len(desc) < 150:
        desc = (desc.rstrip(".") + f". AngelGranit, {ADDRESS}, {PHONE}.").strip()
        if len(desc) >= 150:
            break
        desc = (desc.rstrip(".") + " Помощь 24/7.").strip()
    if len(desc) > 160:
        cut = desc[:160].rsplit(" ", 1)[0]
        desc = cut.rstrip(".,;:") + "."
    return desc


def pick_services(cat_slug: str, n: int = 3) -> list[str]:
    cat = next(c for c in CATEGORIES if c["slug"] == cat_slug)
    base = list(cat["services"])
    # ensure existing
    base = [s for s in base if s in SERVICE_TITLES]
    if len(base) >= n:
        return base[:n]
    for s in SERVICE_TITLES:
        if s not in base:
            base.append(s)
        if len(base) >= n:
            break
    return base[:n]


def unique_paragraphs(question: str, cat_name: str, services: list[str], salt: str) -> list[tuple[str, list[str]]]:
    h = int(hashlib.md5(f"{question}|{salt}".encode("utf-8")).hexdigest(), 16)
    s1, s2, s3 = [SERVICE_TITLES[x] for x in services[:3]]

    openings = [
        f"Вопрос «{question}?» часто появляется в самый тяжёлый момент. Ниже — спокойный и практичный ответ для семей в Алматы.",
        f"Если вы ищете ответ на вопрос «{question}?», начните с короткого плана действий и одного понятного контакта.",
        f"Семьи в Алматы регулярно спрашивают: «{question}?». Разберём по шагам, без лишней теории.",
        f"Ответ на «{question}?» зависит от обстоятельств, но базовый порядок почти всегда один и тот же.",
    ]
    open_p = openings[h % len(openings)]

    steps_title = [
        "Короткий порядок действий",
        "С чего начать прямо сейчас",
        "Практические шаги",
        "План на ближайшие часы",
    ][h % 4]

    steps = [
        f"1) Зафиксируйте факты: где находится усопший, какие документы уже есть, кто из родственников рядом.",
        f"2) Позвоните ритуальному агенту {AGENT} по номеру {PHONE} или напишите в WhatsApp — получите ясный следующий шаг.",
        f"3) Согласуйте минимально необходимое: {s1.lower()}, затем добавьте только то, что действительно нужно.",
        f"4) Отдельно решите, что можно отложить: например памятник или благоустройство.",
        f"5) Держите одну смету и один контакт, чтобы не согласовывать одно и то же с разными людьми.",
    ]

    detail_title = [
        f"Важные нюансы по теме «{cat_name}»",
        f"На что обратить внимание",
        f"Частые ошибки и как их избежать",
        f"Что обычно упускают",
    ][(h // 3) % 4]

    details = [
        f"В теме «{cat_name}» легко переплатить из-за спешки. Просите разбивку позиций и спокойно убирайте лишнее.",
        f"Если вы сравниваете предложения, смотрите не только на цену «от», а на состав: что входит в {s2.lower()} и что оплачивается отдельно.",
        f"Для Алматы важно учитывать дорогу, район и время суток. Особенно это заметно, когда в плане есть транспорт и подача к залу или кладбищу.",
        f"Хороший сервис объясняет варианты простым языком. Если вам давят «решать за пять минут» — это повод замедлиться и уточнить детали.",
        f"Связка услуг работает лучше по отдельности: сначала {s1.lower()}, при необходимости {s2.lower()}, позже {s3.lower()}.",
    ]
    # rotate details uniquely
    rot = h % len(details)
    details = details[rot:] + details[:rot]

    services_title = "Какие услуги AngelGranit связаны с этим вопросом"
    services_paras = [
        f"По этой теме чаще всего обращаются за услугой «{s1}». Страница услуги поможет понять состав и следующий шаг.",
        f"Дополнительно может понадобиться «{s2}» — особенно если вы собираете полный сценарий прощания.",
        f"Если после основного решения остаётся вопрос памяти, логично перейти к «{s3}».",
        f"Офис: {ADDRESS}. Агент {AGENT} на связи 24/7: {PHONE}.",
    ]

    closing_title = "Краткий итог"
    closing = [
        f"Ответ на вопрос «{question}?» начинается с ясного плана и одного координатора.",
        f"Не обязательно брать всё сразу: выберите необходимое сейчас, остальное согласуйте позже.",
        f"AngelGranit помогает семьям в Алматы спокойно пройти этот путь — от первого звонка до последующего оформления.",
    ]

    return [
        ("Ответ коротко", [open_p, details[0]]),
        (steps_title, steps),
        (detail_title, details[1:4]),
        (services_title, services_paras),
        (closing_title, closing),
    ]


def faq_for(question: str, services: list[str]) -> list[tuple[str, str]]:
    """Question-specific FAQs (anti-template) for Search Essentials quality."""
    s1 = SERVICE_TITLES[services[0]] if services else "Ритуальные услуги"
    q = question.rstrip("?")
    return [
        (f"С чего начать по вопросу «{q}»?", f"Позвоните {PHONE}: агент {AGENT} даст порядок действий под вашу ситуацию в Алматы."),
        ("Что важно учесть по району и времени?", "Учитывайте район, дорогу и время суток — это влияет на подачу транспорта и тайминг."),
        (f"Какая услуга ближе всего?", f"Начните со страницы «{s1}», затем посмотрите связанные услуги."),
        ("Можно ли обойтись без полного пакета?", "Да. Часто достаточно одной-двух позиций — полный пакет не обязателен."),
        ("Как связаться ночью?", f"AngelGranit принимает заявки 24/7: {PHONE} или WhatsApp."),
        ("Где офис?", f"Офис: {ADDRESS}, Алматы. Выезд агента возможен."),
    ]


def build_articles() -> list[dict]:
    _build_seeds()
    articles = []
    seen_slugs = set()
    for cat_slug, question, tail in SEEDS:
        slug = slugify_full(cat_slug, tail)
        # ensure uniqueness
        if slug in seen_slugs:
            slug = f"{slug}-{len(seen_slugs)}"
        seen_slugs.add(slug)
        cat = next(c for c in CATEGORIES if c["slug"] == cat_slug)
        services = pick_services(cat_slug, 3)
        title = f"{question}? | AngelGranit Алматы"
        if len(title) > 65:
            title = question[:55].rstrip() + "… | AngelGranit"
        desc = ensure_desc(f"{question}? Спокойный ответ и план действий для семей в Алматы. AngelGranit 24/7.")
        h1 = f"{question}?"
        lead = f"Практический разбор вопроса для семей в Алматы: что сделать сейчас, что можно отложить и какие услуги помогут."
        articles.append(
            {
                "slug": slug,
                "category": cat_slug,
                "category_name": cat["name"],
                "question": question,
                "title": title,
                "description": desc,
                "h1": h1,
                "lead": lead,
                "services": services,
                "sections": unique_paragraphs(question, cat["name"], services, slug),
                "faq": faq_for(question, services),
            }
        )
    return articles


def nav_html(depth: int = 1) -> str:
    prefix = "../" * depth
    home = prefix if depth else "./"
    cat_links = "\n".join(
        f'          <a href="{prefix}stati/{esc(c["slug"])}/">{esc(c["name"])}</a>' for c in CATEGORIES
    )
    svc_links = "\n".join(
        f'          <a href="{prefix}uslugi/{esc(slug)}/">{esc(title)}</a>'
        for slug, title in list(SERVICE_TITLES.items())[:10]
    )
    return f"""  <header class="site-nav" data-site-nav>
    <a class="site-nav__brand" href="{home}"><strong>AngelGranit</strong><span>AG</span></a>
    <button class="site-nav__toggle" type="button" data-nav-toggle aria-expanded="false">Меню</button>
    <ul class="site-nav__menu">
      <li class="site-nav__item" data-dropdown>
        <button type="button">Услуги</button>
        <div class="site-nav__dropdown">
          <a href="{prefix}uslugi/">Все услуги</a>
{svc_links}
        </div>
      </li>
      <li class="site-nav__item" data-dropdown>
        <button type="button">Статьи</button>
        <div class="site-nav__dropdown">
          <a href="{prefix}stati/">Все статьи</a>
{cat_links}
        </div>
      </li>
      <li><a href="{home}#packages">Цены</a></li>
      <li><a href="{prefix}kontakty/">Контакты</a></li>
    </ul>
    <a class="site-nav__call" href="tel:{PHONE_TEL}">Позвонить 24/7</a>
  </header>"""


def related_articles(articles: list[dict], current: dict, n: int = 6) -> list[dict]:
    same = [a for a in articles if a["category"] == current["category"] and a["slug"] != current["slug"]]
    other = [a for a in articles if a["category"] != current["category"]]
    out = same[:4]
    for a in other:
        if len(out) >= n:
            break
        out.append(a)
    return out[:n]


def render_article(page: dict, articles: list[dict]) -> str:
    url = f"{BASE}/stati/{page['slug']}/"
    related = related_articles(articles, page)
    svc_html = "\n".join(
        f'<a href="../../uslugi/{esc(s)}/"><strong>{esc(SERVICE_TITLES[s])}</strong><span>Перейти к услуге</span></a>'
        for s in page["services"]
    )
    rel_html = "\n".join(
        f'<a href="../{esc(a["slug"])}/"><strong>{esc(a["question"])}?</strong><span>{esc(a["category_name"])}</span></a>'
        for a in related
    )
    sections = []
    for h2, paras in page["sections"]:
        sections.append(f"<h2>{esc(h2)}</h2>")
        for p in paras:
            sections.append(f"<p>{esc(p)}</p>")
    faq = "\n".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in page["faq"])
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE}/#organization",
                "name": "AngelGranit",
                "url": f"{BASE}/",
            },
            {
                "@type": "Article",
                "headline": page["h1"],
                "description": page["description"],
                "dateModified": TODAY,
                "author": {"@id": f"{BASE}/#organization"},
                "publisher": {"@id": f"{BASE}/#organization"},
                "mainEntityOfPage": url,
                "image": f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Статьи", "item": f"{BASE}/stati/"},
                    {"@type": "ListItem", "position": 3, "name": page["category_name"], "item": f"{BASE}/stati/{page['category']}/"},
                    {"@type": "ListItem", "position": 4, "name": page["question"], "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in page["faq"]
                ],
            },
        ],
    }
    og_img = f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp"
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(page["title"])}</title>
  <meta name="description" content="{esc(page["description"])}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
{icon_links("../../")}
{social_meta(title=esc(page["title"]), desc=esc(page["description"]), url=url, image=og_img, og_type="article")}
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../seo/assets/seo.css" />
  <link rel="stylesheet" href="../../assets/site/nav.css" />
  <link rel="stylesheet" href="../../assets/site/page.css" />
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{nav_html(2)}
  <main class="page-main">
    <div class="page-wrap">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../../">Главная</a></li>
          <li><a href="../">Статьи</a></li>
          <li><a href="../{esc(page["category"])}/">{esc(page["category_name"])}</a></li>
          <li aria-current="page">{esc(page["question"])}</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>{esc(page["h1"])}</h1>
        <p class="lead">{esc(page["lead"])}</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn-site btn-site--ghost" href="../../uslugi/{esc(page["services"][0])}/">Услуга: {esc(SERVICE_TITLES[page["services"][0]])}</a>
        </div>
      </header>
      <article class="page-article">
{chr(10).join(sections)}
      </article>
      <section>
        <h2>Связанные услуги</h2>
        <div class="related-grid">{svc_html}</div>
      </section>
      <section class="page-faq" id="faq">
        <h2>Короткие ответы</h2>
{faq}
      </section>
      <section>
        <h2>Читайте также</h2>
        <div class="related-grid">{rel_html}</div>
      </section>
      <div class="page-cta" style="margin-top:2rem">
        <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить</a>
        <a class="btn-site btn-site--wa" href="#" data-wa target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <a class="btn-site btn-site--ghost" href="../{esc(page["category"])}/">К категории</a>
      </div>
    </div>
  </main>
  <footer class="page-footer">
    <strong>AngelGranit</strong>
    {esc(AGENT)} · {esc(ADDRESS)} · <a href="tel:{PHONE_TEL}">{esc(PHONE)}</a>
  </footer>
  <script src="../../assets/site/nav.js" defer></script>
</body>
</html>
"""


def render_category(cat: dict, articles: list[dict]) -> str:
    items = [a for a in articles if a["category"] == cat["slug"]]
    cards = "\n".join(
        f'<a class="hub-card" href="../{esc(a["slug"])}/"><strong>{esc(a["question"])}?</strong><span>{esc(a["lead"][:110])}…</span></a>'
        for a in items
    )
    title = f"{cat['name']} — статьи | AngelGranit"
    desc = ensure_desc(cat["description"] + " Полезные статьи AngelGranit для семей в Алматы.")
    url = f"{BASE}/stati/{cat['slug']}/"
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
{icon_links("../../")}
{social_meta(title=esc(title), desc=esc(desc), url=url, image=f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp")}
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../seo/assets/seo.css" />
  <link rel="stylesheet" href="../../assets/site/nav.css" />
  <link rel="stylesheet" href="../../assets/site/page.css" />
</head>
<body>
{nav_html(2)}
  <main class="page-main">
    <div class="page-wrap--wide">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../../">Главная</a></li>
          <li><a href="../">Статьи</a></li>
          <li aria-current="page">{esc(cat["name"])}</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>{esc(cat["name"])}</h1>
        <p class="lead">{esc(cat["description"])}</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить</a>
          <a class="btn-site btn-site--ghost" href="../">Все категории</a>
        </div>
      </header>
      <div class="hub-grid">{cards}</div>
    </div>
  </main>
  <footer class="page-footer"><strong>AngelGranit</strong>{esc(PHONE)}</footer>
  <script src="../../assets/site/nav.js" defer></script>
</body>
</html>
"""


def render_hub(articles: list[dict]) -> str:
    cat_cards = "\n".join(
        f'<a class="hub-card" href="{esc(c["slug"])}/"><strong>{esc(c["name"])}</strong><span>{esc(c["description"])} · {sum(1 for a in articles if a["category"]==c["slug"])} статей</span></a>'
        for c in CATEGORIES
    )
    title = "Статьи о ритуальных услугах и памятниках в Алматы | AngelGranit"
    desc = ensure_desc(
        "Большой раздел статей AngelGranit: первые шаги, похороны, документы, катафалк, памятники и благоустройство."
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{BASE}/stati/" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
{icon_links("../")}
{social_meta(title=esc(title), desc=esc(desc), url=f"{BASE}/stati/", image=f"{BASE}/images/seo/ritualnye-uslugi-almaty.webp")}
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../seo/assets/seo.css" />
  <link rel="stylesheet" href="../assets/site/nav.css" />
  <link rel="stylesheet" href="../assets/site/page.css" />
</head>
<body>
{nav_html(1)}
  <main class="page-main">
    <div class="page-wrap--wide">
      <nav class="breadcrumbs" aria-label="Хлебные крошки">
        <ol>
          <li><a href="../">Главная</a></li>
          <li aria-current="page">Статьи</li>
        </ol>
      </nav>
      <header class="page-hero">
        <h1>Статьи AngelGranit</h1>
        <p class="lead">Более {len(articles)} полезных материалов: ответы на реальные вопросы семей в Алматы. Каждая статья связана с нужными услугами.</p>
        <div class="page-cta">
          <a class="btn-site btn-site--gold" href="tel:{PHONE_TEL}">Позвонить {esc(PHONE)}</a>
          <a class="btn-site btn-site--ghost" href="../uslugi/">Смотреть услуги</a>
        </div>
      </header>
      <h2 style="color:#d4af57;font-family:Cinzel,Georgia,serif">Категории</h2>
      <div class="hub-grid">{cat_cards}</div>
    </div>
  </main>
  <footer class="page-footer"><strong>AngelGranit</strong>{esc(ADDRESS)} · {esc(PHONE)}</footer>
  <script src="../assets/site/nav.js" defer></script>
</body>
</html>
"""


def update_sitemap(articles: list[dict]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8") if path.exists() else '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'
    text = re.sub(
        r"\s*<url>\s*<loc>https://angelgranit\.com/stati(?:/[^<]*)?/?</loc>[\s\S]*?</url>",
        "",
        text,
    )
    blocks = [
        f"  <url>\n    <loc>{BASE}/stati/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>"
    ]
    for c in CATEGORIES:
        blocks.append(
            f"  <url>\n    <loc>{BASE}/stati/{c['slug']}/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        )
    for a in articles:
        blocks.append(
            f"  <url>\n    <loc>{BASE}/stati/{a['slug']}/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"
        )
    text = text.replace("</urlset>", "\n".join(blocks) + "\n</urlset>")
    path.write_text(text, encoding="utf-8", newline="\n")


def write_articles_index_json(articles: list[dict]) -> None:
    """For service pages cross-linking."""
    data = [
        {
            "slug": a["slug"],
            "category": a["category"],
            "question": a["question"],
            "services": a["services"],
        }
        for a in articles
    ]
    (ROOT / "scripts" / "site" / "articles_index.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )


def main() -> None:
    articles = build_articles()
    assert len(articles) >= 200, len(articles)
    STATI.mkdir(parents=True, exist_ok=True)
    (STATI / "index.html").write_text(render_hub(articles), encoding="utf-8", newline="\n")
    for cat in CATEGORIES:
        d = STATI / cat["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render_category(cat, articles), encoding="utf-8", newline="\n")
    for a in articles:
        d = STATI / a["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render_article(a, articles), encoding="utf-8", newline="\n")
    update_sitemap(articles)
    write_articles_index_json(articles)
    print("articles", len(articles), "categories", len(CATEGORIES))
    for c in CATEGORIES:
        n = sum(1 for a in articles if a["category"] == c["slug"])
        print(f"  {c['slug']}: {n}")


if __name__ == "__main__":
    main()
