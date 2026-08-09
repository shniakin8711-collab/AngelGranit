# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(r"c:\Users\РС\OneDrive\Desktop\сайт кат")

html_files = list(root.rglob("*.html"))
changed = []
for path in html_files:
    text = path.read_text(encoding="utf-8")
    orig = text
    text = text.replace("btn-site btn-site--gold", "btn-primary")
    text = text.replace("btn-site btn-site--wa", "btn-secondary")
    text = text.replace("btn-site btn-site--ghost", "btn-secondary")
    text = text.replace('class="btn-site--gold"', 'class="btn-primary"')
    text = text.replace('class="btn-site--wa"', 'class="btn-secondary"')
    text = text.replace('class="btn-site--ghost"', 'class="btn-secondary"')

    if "assets/site/buttons.css" not in text and (
        "assets/site/page.css" in text or "assets/site/nav.css" in text
    ):
        rel = path.relative_to(root)
        depth = len(rel.parts) - 1
        prefix = "../" * depth if depth else ""
        link_line = f'<link rel="stylesheet" href="{prefix}assets/site/buttons.css" />'
        page_link = f'<link rel="stylesheet" href="{prefix}assets/site/page.css" />'
        nav_link = f'<link rel="stylesheet" href="{prefix}assets/site/nav.css" />'
        if page_link in text:
            text = text.replace(page_link, page_link + "\n  " + link_line, 1)
        elif nav_link in text:
            text = text.replace(nav_link, nav_link + "\n  " + link_line, 1)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        changed.append(str(path.relative_to(root)))

print("updated html files:", len(changed))

page_css = root / "assets" / "site" / "page.css"
pc = page_css.read_text(encoding="utf-8")
old = """\.btn-site \{
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 2\.55rem; padding: 0\.55rem 1rem;
  border: 1px solid transparent; border-radius: 4px;
  font-family: var\(--font-mono, monospace\); font-size: 0\.72rem; font-weight: 600;
  text-decoration: none; cursor: pointer;
\}
\.btn-site--gold \{
  border-color: #d4af57;
  background: linear-gradient\(180deg, #e0c36a 0%, #d4af57 55%, #8a6a28 100%\);
  color: #1a1408;
\}
\.btn-site--ghost \{ border-color: rgba\(236,232,224,0\.18\); color: #ece8e0; background: transparent; \}
\.btn-site--wa \{ border-color: #25d366; background: #25d366; color: #04140a; \}
"""
pc_new, n = re.subn(
    old,
    "/* Buttons: see assets/site/buttons.css (.btn-primary / .btn-secondary) */\n.page-cta .btn-primary,\n.page-cta .btn-secondary { margin: 0; }\n",
    pc,
    count=1,
)
if n == 0:
    # try without escapes via plain replace
    plain_old = """.btn-site {
  display: inline-flex; align-items: center; justify-content: center;
  min-height: 2.55rem; padding: 0.55rem 1rem;
  border: 1px solid transparent; border-radius: 4px;
  font-family: var(--font-mono, monospace); font-size: 0.72rem; font-weight: 600;
  text-decoration: none; cursor: pointer;
}
.btn-site--gold {
  border-color: #d4af57;
  background: linear-gradient(180deg, #e0c36a 0%, #d4af57 55%, #8a6a28 100%);
  color: #1a1408;
}
.btn-site--ghost { border-color: rgba(236,232,224,0.18); color: #ece8e0; background: transparent; }
.btn-site--wa { border-color: #25d366; background: #25d366; color: #04140a; }
"""
    if plain_old in pc:
        pc_new = pc.replace(
            plain_old,
            "/* Buttons: see assets/site/buttons.css (.btn-primary / .btn-secondary) */\n.page-cta .btn-primary,\n.page-cta .btn-secondary { margin: 0; }\n",
        )
        n = 1
page_css.write_text(pc_new, encoding="utf-8")
print("page.css replacements:", n)

nav_css = root / "assets" / "site" / "nav.css"
nc = nav_css.read_text(encoding="utf-8")
nc2 = nc.replace(
    ".btn-site:focus-visible,",
    ".btn-primary:focus-visible,\n.btn-secondary:focus-visible,",
)
nav_css.write_text(nc2, encoding="utf-8")
print("nav.css updated")
