# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "index.html"
text = path.read_text(encoding="utf-8")

# 1) Root palette → heavenly sky (readable dark text)
old_root = """    :root {
      --bg: #070708;
      --bg-soft: #0d0d10;
      --panel: #111116;
      --line: rgba(236, 232, 224, 0.1);
      --line-strong: rgba(236, 232, 224, 0.18);
      --text: #ece8e0;
      --muted: #8e8980;"""

new_root = """    :root {
      --bg: #e8f2fb;
      --bg-soft: #f4f9fd;
      --panel: #ffffff;
      --line: rgba(55, 95, 140, 0.14);
      --line-strong: rgba(55, 95, 140, 0.24);
      --text: #1a2b3d;
      --muted: #5a7086;"""

if old_root not in text:
    raise SystemExit("root block not found")
text = text.replace(old_root, new_root, 1)

# body background sky wash
text = text.replace(
    """    body {
      margin: 0;
      font-family: var(--font-body);
      font-size: 1rem;
      line-height: 1.6;
      color: var(--text);
      background: var(--bg);
      -webkit-font-smoothing: antialiased;
    }""",
    """    body {
      margin: 0;
      font-family: var(--font-body);
      font-size: 1rem;
      line-height: 1.6;
      color: var(--text);
      background:
        radial-gradient(ellipse 90% 55% at 50% -10%, rgba(180, 215, 245, 0.85), transparent 55%),
        linear-gradient(180deg, #dceaf8 0%, #eef5fb 40%, #f7fbfe 100%);
      -webkit-font-smoothing: antialiased;
    }""",
    1,
)

# Nav frosted sky
text = text.replace(
    "      background: rgba(7, 7, 8, 0.72);",
    "      background: rgba(236, 245, 252, 0.82);",
    1,
)
text = text.replace(
    "      background: rgba(7, 7, 8, 0.92);",
    "      background: rgba(244, 249, 253, 0.94);",
    1,
)

# Angels slightly stronger on light sky
text = text.replace(
    """    .with-angel::before {
      content: "";
      position: absolute;
      z-index: 0;
      pointer-events: none;
      background-repeat: no-repeat;
      background-size: contain;
      opacity: 0.12;
      filter: saturate(0.9) brightness(0.95);
    }""",
    """    .with-angel::before {
      content: "";
      position: absolute;
      z-index: 0;
      pointer-events: none;
      background-repeat: no-repeat;
      background-size: contain;
      opacity: 0.16;
      filter: saturate(0.95) brightness(1.05);
    }
    .with-angel {
      background:
        radial-gradient(ellipse 80% 60% at 80% 0%, rgba(170, 210, 245, 0.45), transparent 55%),
        radial-gradient(ellipse 70% 50% at 10% 100%, rgba(210, 230, 250, 0.55), transparent 50%),
        linear-gradient(180deg, rgba(232, 242, 251, 0.92) 0%, rgba(244, 249, 253, 0.96) 100%);
      border-block: 1px solid rgba(55, 95, 140, 0.1);
    }""",
    1,
)

# Soften angel opacities for light
replacements = [
    (".with-angel--a::before {\n      background-image: url(\"images/angels/angel-bg-01.webp\");\n      width: min(340px, 38vw);\n      aspect-ratio: 2 / 3;\n      height: auto;\n      left: -1%;\n      bottom: 0;\n      background-position: center bottom;\n      background-size: contain;\n      opacity: 0.13;",
     ".with-angel--a::before {\n      background-image: url(\"images/angels/angel-bg-01.webp\");\n      width: min(340px, 38vw);\n      aspect-ratio: 2 / 3;\n      height: auto;\n      left: -1%;\n      bottom: 0;\n      background-position: center bottom;\n      background-size: contain;\n      opacity: 0.18;"),
    (".with-angel--b::before {\n      background-image: url(\"images/angels/angel-bg-02.webp\");\n      width: min(320px, 36vw);\n      aspect-ratio: 2 / 3;\n      height: auto;\n      right: -1%;\n      bottom: 0;\n      left: auto;\n      background-position: center bottom;\n      background-size: contain;\n      opacity: 0.12;",
     ".with-angel--b::before {\n      background-image: url(\"images/angels/angel-bg-02.webp\");\n      width: min(320px, 36vw);\n      aspect-ratio: 2 / 3;\n      height: auto;\n      right: -1%;\n      bottom: 0;\n      left: auto;\n      background-position: center bottom;\n      background-size: contain;\n      opacity: 0.17;"),
    ("opacity: 0.1;\n      mask-image: linear-gradient(180deg, transparent 0%, #000 35%, #000 100%);",
     "opacity: 0.14;\n      mask-image: linear-gradient(180deg, transparent 0%, #000 35%, #000 100%);"),
    (".with-angel--a.with-angel--soft::before { opacity: 0.08; }\n    .with-angel--b.with-angel--soft::before { opacity: 0.08; }\n    .with-angel--wings.with-angel--soft::before { opacity: 0.07; }",
     ".with-angel--a.with-angel--soft::before { opacity: 0.14; }\n    .with-angel--b.with-angel--soft::before { opacity: 0.14; }\n    .with-angel--wings.with-angel--soft::before { opacity: 0.12; }"),
    ("opacity: 0.11;\n      transform: none;\n      filter: saturate(0.85) brightness(1.05);\n    }",
     "opacity: 0.16;\n      transform: none;\n      filter: saturate(0.9) brightness(1.08);\n    }"),
]
for a, b in replacements:
    if a in text:
        text = text.replace(a, b, 1)

# pcat → sky
text = text.replace(
    """    .pcat {
      --pcat-bg: #0b0b0b;
      --pcat-card: #181818;
      --pcat-gold: #c8a24a;
      --pcat-white: #ffffff;
      --pcat-muted: rgba(255, 255, 255, 0.68);""",
    """    .pcat {
      --pcat-bg: transparent;
      --pcat-card: rgba(255, 255, 255, 0.88);
      --pcat-gold: #9a7b2f;
      --pcat-white: #1a2b3d;
      --pcat-muted: rgba(26, 43, 61, 0.68);""",
    1,
)

# packages block background
text = text.replace(
    """    #packages {
      position: relative;
      background:
        radial-gradient(ellipse 70% 45% at 50% 0%, rgba(200, 162, 74, 0.07), transparent 55%),
        linear-gradient(180deg, #0c0c0e 0%, #09090b 100%);
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }""",
    """    #packages {
      position: relative;
      background: transparent;
      border-top: 1px solid rgba(55, 95, 140, 0.1);
      border-bottom: 1px solid rgba(55, 95, 140, 0.1);
    }""",
    1,
)

# package cards light
text = text.replace(
    """      background: linear-gradient(165deg, #17181d 0%, #101114 100%);
      box-shadow: 0 14px 36px rgba(0, 0, 0, 0.35);""",
    """      background: linear-gradient(165deg, rgba(255,255,255,0.95) 0%, rgba(240,247,252,0.98) 100%);
      box-shadow: 0 14px 36px rgba(55, 95, 140, 0.12);""",
    1,
)
text = text.replace(
    """    .package {
      display: flex;
      flex-direction: column;
      height: 100%;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;""",
    """    .package {
      display: flex;
      flex-direction: column;
      height: 100%;
      border: 1px solid rgba(55, 95, 140, 0.14);
      border-radius: 10px;""",
    1,
)
text = text.replace(
    """    .package__name {
      margin: 0;
      font-family: var(--font-display);
      font-size: clamp(1.05rem, 1.6vw, 1.22rem);
      font-weight: 600;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      color: #f7f7f5;
      line-height: 1.25;
    }""",
    """    .package__name {
      margin: 0;
      font-family: var(--font-display);
      font-size: clamp(1.05rem, 1.6vw, 1.22rem);
      font-weight: 600;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      color: #1a2b3d;
      line-height: 1.25;
    }""",
    1,
)
text = text.replace(
    """    .package__desc {
      margin: 0;
      color: rgba(236, 232, 224, 0.62);
      font-size: 0.88rem;
      line-height: 1.5;
    }
    .package__list {
      margin: 0.15rem 0 0.35rem;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 0.3rem;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      line-height: 1.4;
      color: rgba(236, 232, 224, 0.72);
    }""",
    """    .package__desc {
      margin: 0;
      color: rgba(26, 43, 61, 0.62);
      font-size: 0.88rem;
      line-height: 1.5;
    }
    .package__list {
      margin: 0.15rem 0 0.35rem;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 0.3rem;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      line-height: 1.4;
      color: rgba(26, 43, 61, 0.72);
    }""",
    1,
)
text = text.replace(
    """    .package__meta {
      display: flex;
      justify-content: space-between;
      gap: 0.75rem;
      align-items: baseline;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: rgba(255, 255, 255, 0.42);
    }""",
    """    .package__meta {
      display: flex;
      justify-content: space-between;
      gap: 0.75rem;
      align-items: baseline;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: rgba(26, 43, 61, 0.45);
    }""",
    1,
)

# catalog backgrounds that used dark radial
text = text.replace(
    """    .catalog {
      background:
        radial-gradient(ellipse 55% 40% at 50% 0%, rgba(154,123,47,0.1), transparent 55%),
        var(--bg);
      border-block: 1px solid var(--line);
    }""",
    """    .catalog {
      background: transparent;
      border-block: 1px solid var(--line);
    }""",
    1,
)

# Insert broad section sky overrides after angel CSS block
SKY = r"""
    /* Heavenly sky surfaces for content blocks */
    #directions,
    #calc,
    #gallery,
    #production,
    #youtube,
    #why-us,
    #guarantees,
    #reviews,
    #faq,
    #contact,
    #share,
    #seo-ritualnye-uslugi,
    #seo-guides,
    .silo-links,
    .gallery-block,
    .benefits,
    .faq-block,
    .reviews-modern,
    .contact,
    .share,
    .calc,
    .seo-longform,
    .seo-hub,
    .yt {
      background:
        radial-gradient(ellipse 75% 55% at 70% 0%, rgba(165, 205, 240, 0.35), transparent 55%),
        linear-gradient(180deg, rgba(232, 242, 251, 0.9) 0%, rgba(244, 249, 253, 0.95) 100%) !important;
      color: var(--text);
      border-block-color: rgba(55, 95, 140, 0.1);
    }
    .section-head h2,
    .share__box h2,
    .benefits .section-head h2,
    .faq-block .section-head h2,
    .gallery-block .section-head h2 {
      color: #1a2b3d;
    }
    .section-head .sub,
    .share__box p,
    .eyebrow {
      color: var(--muted);
    }
    .work-card,
    .benefit-card,
    .faq-item,
    .review-card,
    .seo-hub__grid a,
    .cat-card,
    .catalog-item,
    .price-card {
      background: rgba(255, 255, 255, 0.88) !important;
      border-color: rgba(55, 95, 140, 0.14) !important;
      color: var(--text);
    }
    .footer,
    footer.site-footer,
    .site-footer {
      background: linear-gradient(180deg, #d5e6f5 0%, #c8daf0 100%) !important;
      color: var(--text);
    }
"""

if "/* Heavenly sky surfaces for content blocks */" not in text:
    text = text.replace(
        "    @media (prefers-reduced-motion: reduce) {\n      .with-angel::before { opacity: 0.06; }\n    }",
        "    @media (prefers-reduced-motion: reduce) {\n      .with-angel::before { opacity: 0.1; }\n    }\n" + SKY,
        1,
    )

# Keep hero dark explicitly
if "/* Hero stays night sky over church */" not in text:
    text = text.replace(
        "    /* Hero — premium minimalism, glass card, parallax */\n    .hero {",
        """    /* Hero stays night sky over church */
    .hero {
      color: #ffffff;
    }
    /* Hero — premium minimalism, glass card, parallax */
    .hero {""",
        1,
    )

path.write_text(text, encoding="utf-8")
print("sky theme applied")
