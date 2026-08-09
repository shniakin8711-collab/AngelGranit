# -*- coding: utf-8 -*-
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[2]
path = root / "index.html"
text = path.read_text(encoding="utf-8")

# Clean 9-card grid from before mistaken trim
old = subprocess.check_output(
    ["git", "show", "1858fe2:index.html"],
    cwd=root,
).decode("utf-8")

m_old = re.search(
    r'(<div class="pcat__grid reveal" id="pcat-grid" role="list">)([\s\S]*?)(</div>\s*\n\s*<aside class="pcat-cta)',
    old,
)
if not m_old:
    raise SystemExit("old pcat grid not found")
grid_inner = m_old.group(2)

def repl(mo):
    return mo.group(1) + grid_inner + mo.group(3)

text2, n = re.subn(
    r'(<div class="pcat__grid reveal" id="pcat-grid" role="list">)([\s\S]*?)(</div>\s*\n\s*<aside class="pcat-cta)',
    repl,
    text,
    count=1,
)
if n != 1:
    raise SystemExit(f"current pcat grid replace failed: {n}")

# Ensure mon79/mon80 are gone
text2 = re.sub(
    r"\n        \{ id: 'mon79',[\s\S]*?\},\n"
    r"        \{ id: 'mon80',[\s\S]*?\},",
    "",
    text2,
    count=1,
)

# nth-child(9)
if "pcat-card:nth-child(9)" not in text2:
    text2 = text2.replace(
        ".pcat__grid.is-in .pcat-card:nth-child(8) { transition-delay: 0.46s; }",
        ".pcat__grid.is-in .pcat-card:nth-child(8) { transition-delay: 0.46s; }\n    .pcat__grid.is-in .pcat-card:nth-child(9) { transition-delay: 0.52s; }",
    )

path.write_text(text2, encoding="utf-8")
opens = len(re.findall(r'data-pcat-open=', text2))
mons = len(re.findall(r"id: 'mon\d+'", text2))
print(f"pcat openers={opens}, monuments={mons}")
