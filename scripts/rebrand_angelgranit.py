# -*- coding: utf-8 -*-
"""Rebrand site to AngelGranit: gold theme, remove FPV, keep contacts/maps."""
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
ASSETS = Path(r"C:\Users\РС\.cursor\projects\c-Users-OneDrive-Desktop-AngelGranit-temp\assets")
BANNER_SRC = ASSETS / "c__Users____AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_WhatsApp_Image_2026-07-25_at_19.36.05-5fd636f8-2043-45ac-b593-78288800b10d.png"
BANNER_DST = ROOT / "images" / "hero-angelgranit.png"

def main():
    if BANNER_SRC.exists():
        BANNER_DST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BANNER_SRC, BANNER_DST)
        print("banner ok", BANNER_DST.stat().st_size)
    else:
        print("banner missing", BANNER_SRC)

    text = HTML.read_text(encoding="utf-8")

    # --- CSS gold palette (keep --red* names so class hooks still work) ---
    text = text.replace(
        """      --red: #c41218;
      --red-bright: #e41b24;
      --red-soft: rgba(196, 18, 24, 0.14);
      --red-glow: rgba(196, 18, 24, 0.4);""",
        """      --red: #b8943f;
      --red-bright: #d4af57;
      --red-soft: rgba(212, 175, 87, 0.14);
      --red-glow: rgba(212, 175, 87, 0.45);
      --gold: #d4af57;
      --gold-deep: #9a7b2f;"""
    )

    text = text.replace(
        """    .btn--red {
      background: linear-gradient(180deg, #ef2a32 0%, var(--red) 48%, #9e0e13 100%);""",
        """    .btn--red {
      background: linear-gradient(180deg, #e0c36a 0%, var(--red) 48%, #8a6a28 100%);
      color: #1a1408;"""
    )
    text = text.replace(
        """    .btn--red:hover {
      background: linear-gradient(180deg, #ff3b44 0%, var(--red-bright) 45%, var(--red) 100%);""",
        """    .btn--red:hover {
      background: linear-gradient(180deg, #f0d78a 0%, var(--red-bright) 45%, var(--red) 100%);"""
    )

    # Hero tagline instead of FPV flash
    text = text.replace(".hero__fpv {", ".hero__tagline {")
    text = text.replace(".hero__fpv::before,", ".hero__tagline::before,")
    text = text.replace(".hero__fpv::after {", ".hero__tagline::after {")
    text = text.replace(
        """      letter-spacing: 0.48em;
      color: var(--red-bright);
      text-shadow: 0 0 20px var(--red-glow);
    }
    .hero__tagline::before,
    .hero__tagline::after {
      content: "";
      width: clamp(2rem, 7vw, 4.5rem);
      height: 1px;
      background: var(--red);
    }""",
        """      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--red-bright);
      text-shadow: 0 0 20px var(--red-glow);
    }
    .hero__tagline::before,
    .hero__tagline::after {
      content: "";
      width: clamp(1.5rem, 5vw, 3.5rem);
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--red), transparent);
    }
    .hero h1 {
      color: var(--gold);
    }
    .nav__brand strong {
      color: var(--gold);
    }"""
    )

    # Fix duplicate .hero h1 if we injected badly — read original had .hero h1 before .hero__fpv
    # Restore single gold color on h1 by patching the earlier rule
    text = text.replace(
        """    .hero h1 {
      margin: 0;
      font-family: var(--font-display);
      font-size: clamp(2.4rem, 8vw, 5.4rem);
      font-weight: 700;
      letter-spacing: 0.06em;
      line-height: 0.95;
      text-transform: uppercase;
      color: var(--white);
      text-shadow: 0 10px 40px rgba(0,0,0,0.55);
    }""",
        """    .hero h1 {
      margin: 0;
      font-family: var(--font-display);
      font-size: clamp(2.2rem, 7vw, 4.8rem);
      font-weight: 700;
      letter-spacing: 0.1em;
      line-height: 0.95;
      text-transform: uppercase;
      color: var(--gold);
      text-shadow: 0 10px 40px rgba(0,0,0,0.65), 0 0 30px rgba(212,175,87,0.25);
    }"""
    )

    # Soften hero veil for banner readability + brand CTAs at bottom
    text = text.replace(
        """      background:
        linear-gradient(180deg, rgba(7,7,8,0.45) 0%, rgba(7,7,8,0.2) 40%, rgba(7,7,8,0.78) 75%, rgba(7,7,8,0.98) 100%);""",
        """      background:
        linear-gradient(180deg, rgba(7,7,8,0.55) 0%, rgba(7,7,8,0.25) 35%, rgba(7,7,8,0.55) 62%, rgba(7,7,8,0.92) 100%),
        linear-gradient(90deg, rgba(7,7,8,0.55) 0%, transparent 45%, rgba(7,7,8,0.35) 100%);"""
    )

    text = text.replace(
        'object-position: center 32%;',
        'object-position: center center;'
    )

    # Meta / schema
    replacements = [
        (
            "<title>Black Hearse FPV · Ритуальные услуги и FPV · Алматы</title>",
            "<title>AngelGranit · Православные памятники и ритуальные услуги · Алматы</title>",
        ),
        (
            'content="Black Hearse FPV — ритуальные услуги 24/7 и кинематографичная FPV-съёмка в Алматы. Организация похорон, транспорт, памятники. Агент Александр."',
            'content="AngelGranit — православные памятники по всем канонам и ритуальные услуги 24/7 в Алматы. Гранит, гравировка, установка. Агент Александр."',
        ),
        (
            'content="Black Hearse FPV · Ритуальные услуги и FPV"',
            'content="AngelGranit · Православные памятники и ритуальные услуги"',
        ),
        (
            'content="Ритуальные услуги 24/7 и FPV-съёмка. Алматы."',
            'content="Православные памятники и ритуальные услуги 24/7. Алматы."',
        ),
        (
            'content="images/hero-black-hearse.jpg"',
            'content="images/hero-angelgranit.png"',
        ),
        (
            '"name": "Black Hearse FPV"',
            '"name": "AngelGranit"',
        ),
        (
            '"description": "Ритуальные услуги 24/7 и FPV-съёмка в Алматы."',
            '"description": "Православные памятники и ритуальные услуги 24/7 в Алматы."',
        ),
    ]
    for a, b in replacements:
        if a not in text:
            print("WARN missing:", a[:60])
        else:
            text = text.replace(a, b)

    # Nav brand
    text = text.replace(
        """    <a class="nav__brand" href="#top">
      <strong>Black Hearse</strong>
      <span>FPV</span>
    </a>""",
        """    <a class="nav__brand" href="#top">
      <strong>AngelGranit</strong>
      <span>AG</span>
    </a>"""
    )
    text = text.replace('      <a href="#showcase">портфолио</a>\n      <a href="#youtube">YouTube</a>\n', '      <a href="#showcase">портфолио</a>\n')

    # Hero block
    old_hero = """  <section class="hero" id="top" aria-label="Black Hearse FPV">
    <div class="hero__media" aria-hidden="true">
      <img src="images/hero-black-hearse.jpg" alt="" width="1920" height="1080" decoding="async" fetchpriority="high" />
    </div>
    <div class="hero__veil" aria-hidden="true"></div>
    <div class="hero__content">
      <div class="hero__chip"><i aria-hidden="true"></i> статус: на связи · 24/7</div>
      <h1>Black Hearse</h1>
      <div class="hero__fpv">FPV</div>
      <p class="hero__lead">Ритуальные услуги и кинематографичная FPV-съёмка в Алматы — с уважением к памяти и точностью кадра.</p>
      <div class="hero__actions">
        <button type="button" class="btn btn--ai" id="btn-ai-hero" data-open-ai>ИИ-помощник 24/7</button>
        <a class="btn btn--red" href="tel:+77010567667">Позвонить</a>
        <a class="btn btn--ghost" id="link-wa-hero" href="#" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <button type="button" class="btn btn--ghost" id="btn-share-hero" data-share>Поделиться</button>
      </div>
    </div>
  </section>"""

    new_hero = """  <section class="hero" id="top" aria-label="AngelGranit">
    <div class="hero__media" aria-hidden="true">
      <img src="images/hero-angelgranit.png" alt="" width="1920" height="1080" decoding="async" fetchpriority="high" />
    </div>
    <div class="hero__veil" aria-hidden="true"></div>
    <div class="hero__content">
      <div class="hero__chip"><i aria-hidden="true"></i> Алматы · 24/7</div>
      <h1>AngelGranit</h1>
      <div class="hero__tagline">Память, достойная вечности</div>
      <p class="hero__lead">Православные памятники по всем канонам и ритуальные услуги — с уважением к традиции и достойной памятью на поколения.</p>
      <div class="hero__actions">
        <button type="button" class="btn btn--ai" id="btn-ai-hero" data-open-ai>ИИ-помощник 24/7</button>
        <a class="btn btn--red" href="tel:+77010567667">Позвонить</a>
        <a class="btn btn--ghost" id="link-wa-hero" href="#" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        <button type="button" class="btn btn--ghost" id="btn-share-hero" data-share>Поделиться</button>
      </div>
    </div>
  </section>"""
    if old_hero not in text:
        print("WARN hero block not found")
    else:
        text = text.replace(old_hero, new_hero)

    # Status bar — remove youtube channel
    text = text.replace(
        """  <div class="status" role="status">
    <span>агент: <strong>Александр</strong></span>
    <span>город: <strong>Алматы</strong></span>
    <span>телефон: <a href="tel:+77010567667">+7 701 056 7667</a></span>
    <span>канал: <a href="https://www.youtube.com/@blackhearsefpv" target="_blank" rel="noopener noreferrer">@blackhearsefpv</a></span>
  </div>""",
        """  <div class="status" role="status">
    <span>агент: <strong>Александр</strong></span>
    <span>город: <strong>Алматы</strong></span>
    <span>телефон: <a href="tel:+77010567667">+7 701 056 7667</a></span>
    <span>направление: <strong>памятники · ритуал</strong></span>
  </div>"""
    )

    # Directions dual panels
    old_dual = """  <section id="directions" aria-label="Направления">
    <div class="wrap">
      <div class="dual reveal">
        <article class="dual__panel">
          <img src="images/service-funeral.png" alt="" loading="lazy" decoding="async" />
          <p class="eyebrow">// ритуал</p>
          <h3>Ритуальные услуги</h3>
          <p>Организация похорон под ключ: документы, транспорт, венки, памятники. Работаем круглосуточно.</p>
          <a class="btn btn--ghost" href="#packages">Смотреть пакеты</a>
        </article>
        <article class="dual__panel">
          <img src="images/fpv-studio-panel.png" alt="FPV-дрон Black Hearse в ночном полёте" width="1600" height="900" loading="lazy" decoding="async" />
          <p class="eyebrow">// fpv-студия</p>
          <h3>FPV Studio</h3>
          <p>Динамичные пролёты, синематик и ролики для YouTube-канала Black Hearse FPV.</p>
          <a class="btn btn--red" href="#youtube">Смотреть видео</a>
        </article>
      </div>
    </div>
  </section>"""

    new_dual = """  <section id="directions" aria-label="Направления">
    <div class="wrap">
      <div class="dual reveal">
        <article class="dual__panel">
          <img src="images/service-funeral.png" alt="Ритуальные услуги AngelGranit" loading="lazy" decoding="async" />
          <p class="eyebrow">// ритуал</p>
          <h3>Ритуальные услуги</h3>
          <p>Организация похорон под ключ: документы, транспорт, венки, памятники. Работаем круглосуточно.</p>
          <a class="btn btn--ghost" href="#packages">Смотреть пакеты</a>
        </article>
        <article class="dual__panel">
          <img src="images/showcase-monument.png" alt="Гранитные памятники AngelGranit" width="1600" height="900" loading="lazy" decoding="async" />
          <p class="eyebrow">// гранит</p>
          <h3>Памятники</h3>
          <p>Православные памятники из натурального гранита — изготовление, художественная гравировка и установка по Казахстану.</p>
          <a class="btn btn--red" href="#monuments">Смотреть каталог</a>
        </article>
      </div>
    </div>
  </section>"""
    if old_dual not in text:
        print("WARN dual block not found")
    else:
        text = text.replace(old_dual, new_dual)

    # Services — replace FPV row with memorial complex
    text = text.replace(
        """        <article class="service-row">
          <span class="service-row__num">05</span>
          <div>
            <h3>FPV-синематик</h3>
            <p>Съёмка дроном для портфолио, мемориала и YouTube.</p>
          </div>
          <span class="service-row__tag">FPV</span>
        </article>""",
        """        <article class="service-row">
          <span class="service-row__num">05</span>
          <div>
            <h3>Мемориальные комплексы</h3>
            <p>Оформление места захоронения под ключ: оградка, стол, скамья, установка.</p>
          </div>
          <span class="service-row__tag">комплекс</span>
        </article>"""
    )
    text = text.replace(
        '<p class="sub">Агент Александр поможет на каждом этапе — от первого звонка до памятника.</p>',
        '<p class="sub">Агент Александр поможет на каждом этапе — от организации прощания до установки гранитного памятника.</p>'
    )

    # Showcase
    old_show = """  <section id="showcase">
    <div class="wrap">
      <header class="section-head reveal">
        <p class="eyebrow">// портфолио</p>
        <h2>Кадр и память</h2>
        <p class="sub">Атмосфера студии: дрон, гранит, ночной город.</p>
      </header>
      <div class="showcase-grid reveal">
        <figure class="shot">
          <img src="images/showcase-hearse.png" alt="Чёрный катафалк ночью" width="900" height="1200" loading="lazy" decoding="async" />
          <span>чёрный катафалк</span>
        </figure>
        <figure class="shot">
          <img src="images/showcase-drone.png" alt="FPV-дрон в ночном небе" width="1200" height="900" loading="lazy" decoding="async" />
          <span>fpv-дрон</span>
        </figure>
        <figure class="shot">
          <img src="images/showcase-monument.png" alt="Памятник из чёрного гранита" width="1200" height="900" loading="lazy" decoding="async" />
          <span>гранит</span>
        </figure>
      </div>
    </div>
  </section>"""

    new_show = """  <section id="showcase">
    <div class="wrap">
      <header class="section-head reveal">
        <p class="eyebrow">// портфолио</p>
        <h2>Память в камне</h2>
        <p class="sub">Катафалк, гранитные памятники и достойное оформление места упокоения.</p>
      </header>
      <div class="showcase-grid reveal">
        <figure class="shot">
          <img src="images/showcase-hearse.png" alt="Чёрный катафалк" width="900" height="1200" loading="lazy" decoding="async" />
          <span>ритуальный транспорт</span>
        </figure>
        <figure class="shot">
          <img src="images/catalog/monuments/banner-monuments.jpg" alt="Каталог гранитных памятников" width="1200" height="900" loading="lazy" decoding="async" />
          <span>памятники</span>
        </figure>
        <figure class="shot">
          <img src="images/showcase-monument.png" alt="Памятник из чёрного гранита" width="1200" height="900" loading="lazy" decoding="async" />
          <span>гранит</span>
        </figure>
      </div>
    </div>
  </section>"""
    if old_show not in text:
        print("WARN showcase not found")
    else:
        text = text.replace(old_show, new_show)

    # Remove YouTube section entirely
    yt_pat = re.compile(
        r'\n  <section class="yt" id="youtube">.*?</section>\n',
        re.DOTALL
    )
    text2, n = yt_pat.subn('\n', text, count=1)
    if n != 1:
        print("WARN youtube section remove count", n)
    else:
        text = text2

    # Contacts — remove youtube row, add monuments note
    text = text.replace(
        """              <li>
                <span>youtube</span>
                <a href="https://www.youtube.com/@blackhearsefpv" target="_blank" rel="noopener noreferrer">@blackhearsefpv</a>
              </li>""",
        """              <li>
                <span>специализация</span>
                <strong>памятники · ритуал</strong>
              </li>"""
    )

    text = text.replace(
        '<option value="FPV-съёмка">FPV-съёмка</option>',
        '<option value="Памятник из гранита">Памятник из гранита</option>\n                <option value="Мемориальный комплекс">Мемориальный комплекс</option>'
    )

    text = text.replace(
        "alt=\"Сохраните наш номер и поделитесь ссылкой в трудную минуту — Black Hearse FPV, Александр +7 701 056 7667\"",
        "alt=\"Сохраните наш номер и поделитесь ссылкой в трудную минуту — AngelGranit, Александр +7 701 056 7667\""
    )

    text = text.replace(
        """  <footer class="footer">
    <strong>Black Hearse FPV</strong>
    Ритуальные услуги · FPV · Алматы<br />
    Александр · <a href="https://2gis.kz/almaty/geo/9430047375176085" target="_blank" rel="noopener noreferrer">ул. Осетинская, 5а</a><br />
    <a href="tel:+77010567667">+7 701 056 7667</a>
  </footer>""",
        """  <footer class="footer">
    <strong>AngelGranit</strong>
    Православные памятники · ритуальные услуги · Алматы<br />
    Александр · <a href="https://2gis.kz/almaty/geo/9430047375176085" target="_blank" rel="noopener noreferrer">ул. Осетинская, 5а</a><br />
    <a href="tel:+77010567667">+7 701 056 7667</a>
  </footer>"""
    )

    # Calc alts
    text = text.replace("Black Hearse FPV — гробы", "AngelGranit — гробы")
    text = text.replace("Black Hearse FPV — надгробия", "AngelGranit — надгробия")

    # JS brand strings
    text = text.replace(
        """      var CONFIG = {
        whatsapp: 'https://wa.me/77010567667',
        youtube: 'https://www.youtube.com/@blackhearsefpv'
      };

      var waUrl = CONFIG.whatsapp + '?text=' + encodeURIComponent('Здравствуйте! Black Hearse FPV — нужна консультация.');""",
        """      var CONFIG = {
        whatsapp: 'https://wa.me/77010567667'
      };

      var waUrl = CONFIG.whatsapp + '?text=' + encodeURIComponent('Здравствуйте! AngelGranit — нужна консультация.');"""
    )
    text = text.replace(
        "return 'Здравствуйте! Black Hearse FPV.\\n'",
        "return 'Здравствуйте! AngelGranit.\\n'"
    )
    text = text.replace(
        "Black Hearse FPV — смета из калькулятора",
        "AngelGranit — смета из калькулятора"
    )
    text = text.replace(
        "Я помощник Black Hearse FPV по ритуальным услугам в Алматы.",
        "Я помощник AngelGranit по ритуальным услугам и памятникам в Алматы."
    )
    text = text.replace(
        """        {
          keys: ['fpv', 'дрон', 'видео', 'youtube', 'съёмк', 'синематик'],
          answer: 'FPV Studio Black Hearse снимает кинематографичные пролёты и ролики для YouTube.\\n\\nКанал: https://www.youtube.com/@blackhearsefpv\\nПо съёмке напишите Александру в WhatsApp: ' + WA_LINK
        },""",
        """        {
          keys: ['гравировк', 'портрет', 'фото на памятник', 'художествен'],
          answer: 'Делаем художественную гравировку и портреты на граните по канонам.\\n\\nКаталог памятников: #monuments\\nЗаказ у Александра: ' + PHONE
        },"""
    )

    # Remaining Black Hearse / FPV mentions
    leftovers = []
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        if 'black hearse' in low or 'fpv' in low or 'blackhearse' in low:
            leftovers.append(f"{i}:{line.strip()[:120]}")

    HTML.write_text(text, encoding="utf-8")
    print("written", HTML)
    print("leftovers", len(leftovers))
    for L in leftovers[:40]:
        print(L)

if __name__ == "__main__":
    main()
