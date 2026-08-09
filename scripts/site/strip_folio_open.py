# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(r"c:\Users\РС\OneDrive\Desktop\сайт кат\index.html")
text = path.read_text(encoding="utf-8")
text2, n = re.subn(
    r'\s*<button type="button" class="folio-card__open"[^>]*>\s*</button>',
    "",
    text,
)
path.write_text(text2, encoding="utf-8")
print("removed open buttons:", n)
print("folio section:", "vypolnennye-raboty" in text2)
print("initPortfolioLightbox:", "initPortfolioLightbox" in text2)
print("link-wa-folio:", "link-wa-folio" in text2)
print("portfolio.css link:", "portfolio.css" in text2)
print("remaining folio-card__open:", text2.count("folio-card__open"))
