# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "index.html"
text = path.read_text(encoding="utf-8")

CSS = r"""
    /* Soft angel backgrounds for sections */
    .with-angel {
      position: relative;
      isolation: isolate;
      overflow: hidden;
    }
    .with-angel::before {
      content: "";
      position: absolute;
      z-index: 0;
      pointer-events: none;
      background-repeat: no-repeat;
      background-size: contain;
      opacity: 0.12;
      filter: saturate(0.9) brightness(0.95);
    }
    .with-angel > * {
      position: relative;
      z-index: 1;
    }
    .with-angel--a::before {
      background-image: url("images/angels/angel-bg-01.webp");
      width: min(420px, 48vw);
      height: min(640px, 78%);
      left: -2%;
      bottom: -6%;
      background-position: left bottom;
      opacity: 0.13;
    }
    .with-angel--b::before {
      background-image: url("images/angels/angel-bg-02.webp");
      width: min(400px, 46vw);
      height: min(620px, 76%);
      right: -3%;
      bottom: -8%;
      left: auto;
      background-position: right bottom;
      opacity: 0.12;
    }
    .with-angel--wings::before {
      background-image: url("images/angels/angel-bg-wings.webp");
      inset: auto 0 0 0;
      width: 100%;
      height: min(340px, 55%);
      background-size: cover;
      background-position: center bottom;
      opacity: 0.1;
      mask-image: linear-gradient(180deg, transparent 0%, #000 35%, #000 100%);
      -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 35%, #000 100%);
    }
    .with-angel--a.with-angel--soft::before { opacity: 0.08; }
    .with-angel--b.with-angel--soft::before { opacity: 0.08; }
    .with-angel--wings.with-angel--soft::before { opacity: 0.07; }
    @media (max-width: 720px) {
      .with-angel--a::before,
      .with-angel--b::before {
        width: min(260px, 62vw);
        height: min(400px, 55%);
        opacity: 0.08;
      }
      .with-angel--wings::before {
        height: min(220px, 42%);
        opacity: 0.07;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      .with-angel::before { opacity: 0.06; }
    }
"""

if "/* Soft angel backgrounds for sections */" not in text:
    # Insert before closing </style> of main stylesheet - find first </style> after hero styles
    # Safer: insert before "/* Premium monument catalog */" or after packages CSS end - use marker near body styles
    marker = "    /* Premium monument catalog */"
    if marker in text:
        text = text.replace(marker, CSS + "\n" + marker, 1)
    else:
        # fallback: before first </style>
        text = text.replace("</style>", CSS + "\n  </style>", 1)

# Section id -> angel class set (skip hero — already has church photo)
angel_map = {
    "katalog-pamyatnikov": "with-angel with-angel--a",
    "directions": "with-angel with-angel--b with-angel--soft",
    "packages": "with-angel with-angel--wings",
    "catalog": "with-angel with-angel--a with-angel--soft",
    "monuments": "with-angel with-angel--b",
    "calc": "with-angel with-angel--wings with-angel--soft",
    "gallery": "with-angel with-angel--a",
    "production": "with-angel with-angel--b with-angel--soft",
    "youtube": "with-angel with-angel--wings",
    "why-us": "with-angel with-angel--a",
    "guarantees": "with-angel with-angel--b with-angel--soft",
    "reviews": "with-angel with-angel--wings with-angel--soft",
    "faq": "with-angel with-angel--a with-angel--soft",
    "contact": "with-angel with-angel--b",
    "share": "with-angel with-angel--wings with-angel--soft",
    "seo-ritualnye-uslugi": "with-angel with-angel--a with-angel--soft",
    "seo-guides": "with-angel with-angel--b with-angel--soft",
}

for sid, classes in angel_map.items():
    # Match <section ... id="sid" ...> or id first
    pat = re.compile(
        rf'(<section\b)([^>]*\bid="{re.escape(sid)}"[^>]*)(>)',
        re.I,
    )

    def add_class(m, cls=classes):
        tag, attrs, end = m.group(1), m.group(2), m.group(3)
        if "with-angel" in attrs:
            return m.group(0)
        if re.search(r'\bclass="', attrs):
            attrs = re.sub(r'\bclass="([^"]*)"', lambda mm: f'class="{mm.group(1)} {cls}"', attrs, count=1)
        else:
            attrs = attrs + f' class="{cls}"'
        return tag + attrs + end

    text2, n = pat.subn(add_class, text, count=1)
    if n != 1:
        # try id before class order already covered; try without section having other attrs weirdness
        print(f"warn: section id={sid} matches={n}")
    text = text2

# silo-links has no id — add by class
text = re.sub(
    r'(<section class=")(silo-links")',
    r'\1with-angel with-angel--wings with-angel--soft silo-links"',
    text,
    count=1,
)

path.write_text(text, encoding="utf-8")
print("angel backgrounds wired")
