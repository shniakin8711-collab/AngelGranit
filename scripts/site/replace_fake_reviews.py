# -*- coding: utf-8 -*-
"""Replace template SEO review blocks with real Google Maps reviews."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NEW = (
    '<figure class="review"><p>«AngelGranit.com огромное спасибо агенту Александру '
    "за профессиональную организацию похорон все было сделано с большим уважением. "
    "Сопровождал на всех этапах морг кладбище захоронение памятник оградка и цена "
    "очень не дорого рекомендую Александра как ответственный агент и человек.»</p>"
    "<footer>— Надежда Заварухина · Google Maps</footer></figure>\n"
    '<figure class="review"><p>«Хочу выразить благодарность Ип Шнякина и лично '
    "ритуальному агенту Александру за профессиональную и ответственную работу "
    "Александр внимательно отнёсся ко всем вопросам помог с организацией и "
    "оформлением необходимых услуг все объяснил и был на связи. Работа выполнена "
    "качественно спокойно и без лишних переживаний для семьи.»</p>"
    "<footer>— Наталья Пономарева · Google Maps</footer></figure>"
)

PAT = re.compile(r'(?:<figure class="review">.*?</figure>\s*){2,}', re.S)


def main() -> None:
    updated = 0
    for path in (ROOT / "seo").rglob("index.html"):
        text = path.read_text(encoding="utf-8")
        if '<figure class="review">' not in text:
            continue
        new_text, count = PAT.subn(NEW + "\n", text, count=1)
        if count:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            updated += 1
    leftover = []
    for path in ROOT.rglob("*.html"):
        if "Семья из Алматы" in path.read_text(encoding="utf-8", errors="ignore"):
            leftover.append(str(path.relative_to(ROOT)))
    print(f"seo_updated={updated}")
    print(f"leftover_family={len(leftover)}")
    for item in leftover[:20]:
        print(item)


if __name__ == "__main__":
    main()
