# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "index.html"
text = path.read_text(encoding="utf-8")

# Remove four place-map sections in one go
html_pat = re.compile(
    r'\n  <section class="cemeteries" id="cemeteries"[\s\S]*?'
    r'</section>\n\n'
    r'  <section class="morgues" id="morgues"[\s\S]*?'
    r'</section>\n\n'
    r'  <section class="churches" id="churches"[\s\S]*?'
    r'</section>\n\n'
    r'  <section class="cafes" id="cafes"[\s\S]*?'
    r'</section>\n',
    re.M,
)
text2, n = html_pat.subn("\n", text, count=1)
if n != 1:
    raise SystemExit(f"html sections: expected 1, got {n}")

css_pat = re.compile(
    r"\n    /\* Place maps: cemeteries, morgues, churches, cafes \*/\n"
    r"[\s\S]*?(?=\n    /\* Map \*/)",
    re.M,
)
text3, n2 = css_pat.subn("\n", text2, count=1)
if n2 != 1:
    raise SystemExit(f"css: expected 1, got {n2}")

# Fix leftover in-page link to removed churches section
text3 = text3.replace(
    " · <a href=\"#churches\">карта церквей</a>.",
    ".",
)

path.write_text(text3, encoding="utf-8")
print("removed cemeteries/morgues/churches/cafes map blocks")
