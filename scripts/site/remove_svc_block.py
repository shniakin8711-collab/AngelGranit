# -*- coding: utf-8 -*-
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "index.html"
text = path.read_text(encoding="utf-8")

# Remove HTML section
html_pat = re.compile(
    r'\n  <section class="svc" id="nashi-uslugi" aria-labelledby="svc-title">[\s\S]*?</section>\n',
    re.M,
)
text2, n_html = html_pat.subn("\n", text, count=1)
if n_html != 1:
    raise SystemExit(f"html section: expected 1, got {n_html}")

# Remove CSS block for services showcase
css_pat = re.compile(
    r'\n    /\* Services showcase — after hero \*/\n    \.svc \{[\s\S]*?(?=\n    /\* |\n    \.pcat \{)',
    re.M,
)
text3, n_css = css_pat.subn("\n", text2, count=1)
if n_css != 1:
    raise SystemExit(f"css block: expected 1, got {n_css}")

# Remove WA services link wiring if present
text3 = re.sub(
    r"\n\s*var waServices = document\.getElementById\('link-wa-services'\);[\s\S]*?(?=\n\s*(?:var |function |/\*|init))",
    "\n",
    text3,
    count=1,
)

path.write_text(text3, encoding="utf-8")
print("removed nashi-uslugi section and related CSS")
