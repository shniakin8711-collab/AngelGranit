# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "index.html"
text = path.read_text(encoding="utf-8")

html_pat = re.compile(
    r'\n  <section id="works" class="works-catalog"[\s\S]*?</section>\n',
    re.M,
)
text2, n = html_pat.subn("\n", text, count=1)
if n != 1:
    raise SystemExit(f"html: expected 1, got {n}")

css_pat = re.compile(
    r"\n    /\* Works catalog \*/\n    \.works-catalog \{[\s\S]*?(?=\n    /\* Photo gallery)",
    re.M,
)
text3, n2 = css_pat.subn("\n", text2, count=1)
if n2 != 1:
    raise SystemExit(f"css: expected 1, got {n2}")

# Retarget leftover #works anchors to the works page / gallery
replacements = [
    ('href="#works"', 'href="nashi-raboty/"'),
    (">Смотреть работы<", ">Смотреть работы<"),  # keep text
]
text3 = text3.replace('href="#works"', 'href="nashi-raboty/"')

path.write_text(text3, encoding="utf-8")
print("removed works catalog block and retargeted #works links")
