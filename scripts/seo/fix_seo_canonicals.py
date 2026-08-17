# -*- coding: utf-8 -*-
"""Point overlapping /seo/ pages to root pillar canonicals."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://angelgranit.com"

MAP = {
    "ritualnye-uslugi-almaty": "ritualnye-uslugi-almaty",
    "organizaciya-pohoron-almaty": "organizaciya-pohoron-almaty",
    "katafalk-almaty": "katafalk-almaty",
    "granitnye-pamyatniki": "granitnye-pamyatniki-almaty",
    "memorialnye-kompleksy": "memorialnye-kompleksy-almaty",
    "vyzov-ritualnogo-agenta": "ritualny-agent-almaty",
    "venki": "ritualnye-prinadlezhnosti-almaty",
    "izgotovlenie-pamyatnikov": "pamyatniki-almaty",
    "ustanovka-pamyatnikov": "pamyatniki-almaty",
    "kak-vybrat-pamyatnik": "pamyatniki-almaty",
}

for seo_slug, root_slug in MAP.items():
    path = ROOT / "seo" / seo_slug / "index.html"
    if not path.exists():
        print("skip", seo_slug)
        continue
    html = path.read_text(encoding="utf-8")
    canon = f"{BASE}/{root_slug}/"
    if re.search(r'rel="canonical"', html):
        html = re.sub(
            r'<link rel="canonical" href="[^"]*"\s*/?>',
            f'<link rel="canonical" href="{canon}" />',
            html,
            count=1,
        )
    else:
        html = html.replace(
            "</title>",
            f'</title>\n  <link rel="canonical" href="{canon}" />',
            1,
        )
    path.write_text(html, encoding="utf-8", newline="\n")
    print("canonical", seo_slug, "->", root_slug)
