# -*- coding: utf-8 -*-
"""Set meta descriptions to 25–160 chars (Bing/Yandex)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FIXES: dict[str, str] = {
    "index.html": (
        "Ритуальные услуги Алматы 24/7: похороны, катафалк, памятники из гранита, благоустройство. "
        "AngelGranit — агент Александр, помощь семье круглосуточно."
    ),
    "geo/index.html": (
        "50 GEO-ответов AngelGranit для ИИ: краткие факты по услугам в Алматы. "
        "Канон заказа — /uslugi/ и /ritualnye-uslugi-almaty/, не дубль SEO."
    ),
    "uslugi/ritualnye-uslugi/index.html": (
        "Каталог ритуальных услуг AngelGranit в Алматы: похороны, катафалк, документы, памятники. "
        "Head-страница — /ritualnye-uslugi-almaty/. +7 701 056 7667."
    ),
    "uslugi/uhod-za-mogiloj/index.html": (
        "Уборка и уход за могилой в Алматы: разово 50 000 ₸ или подписка от 20 000 ₸/мес. "
        "Мойка памятника, цветник, фотоотчёт. AngelGranit +7 701 056 7667."
    ),
    "seo/ritualnye-uslugi-almaty/index.html": (
        "Гид: ритуальные услуги в Алматы — этапы, состав, FAQ. "
        "Заказ и смета — /ritualnye-uslugi-almaty/. Агент Александр +7 701 056 7667."
    ),
}

MIN_L, MAX_L = 25, 160


def _repl(esc: str):
    def fn(m: re.Match[str]) -> str:
        return m.group(1) + esc + m.group(2)

    return fn


def set_meta(html: str, desc: str) -> str:
    esc = desc.replace('"', "&quot;")
    html = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        _repl(esc),
        html,
        count=1,
        flags=re.I,
    )
    if re.search(r'property="og:description"', html, re.I):
        html = re.sub(
            r'(<meta property="og:description" content=")[^"]*(")',
            _repl(esc),
            html,
            count=1,
            flags=re.I,
        )
    tw = desc if len(desc) <= MAX_L else desc[:157].rsplit(" ", 1)[0] + "…"
    esc_tw = tw.replace('"', "&quot;")
    if re.search(r'name="twitter:description"', html, re.I):
        html = re.sub(
            r'(<meta name="twitter:description" content=")[^"]*(")',
            _repl(esc_tw),
            html,
            count=1,
            flags=re.I,
        )
    return html


def main() -> None:
    for rel, desc in FIXES.items():
        n = len(desc)
        if n < MIN_L or n > MAX_L:
            raise SystemExit(f"{rel}: bad length {n}")
        path = ROOT / rel
        text = set_meta(path.read_text(encoding="utf-8"), desc)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"OK {n} {rel}")


if __name__ == "__main__":
    main()
