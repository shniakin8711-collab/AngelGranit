# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "index.html"
text = path.read_text(encoding="utf-8")
start = text.find('id="katalog-pamyatnikov"')
end = text.find('id="pcat-modal"')
if start < 0 or end < 0:
    raise SystemExit(f"markers not found {start} {end}")

chunk = text[start:end]
new_price = (
    '<p class="pcat-card__price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n'
    '              <meta itemprop="priceCurrency" content="KZT" />\n'
    '              <meta itemprop="availability" content="https://schema.org/InStock" />\n'
    "              цена по запросу\n"
    "            </p>"
)
chunk2, n = re.subn(
    r'<p class="pcat-card__price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\s*'
    r'<meta itemprop="priceCurrency" content="KZT" />\s*'
    r'<meta itemprop="price" content="[^"]+" />\s*'
    r'<meta itemprop="availability" content="https://schema.org/InStock" />\s*'
    r"от [^<]+\s*"
    r"</p>",
    new_price,
    chunk,
)
if n != 9:
    raise SystemExit(f"expected 9 replacements, got {n}")

path.write_text(text[:start] + chunk2 + text[end:], encoding="utf-8")
print(f"updated {n} pcat prices")
