# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "index.html"
text = path.read_text(encoding="utf-8")

html_pat = re.compile(
    r'\n  <section id="prices" class="prices-block"[\s\S]*?</section>\n',
    re.M,
)
text2, n = html_pat.subn("\n", text, count=1)
if n != 1:
    raise SystemExit(f"html: expected 1, got {n}")

css_pat = re.compile(
    r"\n    /\* Price cards \*/\n    \.prices-block \{[\s\S]*?(?=\n    /\* Packages \*/)",
    re.M,
)
text3, n2 = css_pat.subn("\n", text2, count=1)
if n2 != 1:
    raise SystemExit(f"css: expected 1, got {n2}")

text3 = text3.replace('<a href="#prices">цены</a>', '<a href="ceny/">цены</a>')
path.write_text(text3, encoding="utf-8")
print("removed prices-block section and CSS")
