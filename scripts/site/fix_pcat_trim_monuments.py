# -*- coding: utf-8 -*-
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[2]
path = root / "index.html"

# 1) Restore last 2 pcat cards from commit before mistaken removal
old = subprocess.check_output(
    ["git", "show", "96d03f2^:index.html"],
    cwd=root,
).decode("utf-8")

m = re.search(
    r'(        <article class="pcat-card" role="listitem" data-pcat-cat="vertical"[\s\S]*?'
    r'pcat-08-engraving\.webp[\s\S]*?</article>\s*'
    r'<article class="pcat-card" role="listitem" data-pcat-cat="vertical"[\s\S]*?'
    r'pcat-09-orthodox\.webp[\s\S]*?</article>)',
    old,
)
if not m:
    raise SystemExit("could not extract pcat-08/09 cards from previous commit")
cards = m.group(1)

text = path.read_text(encoding="utf-8")
if "pcat-08-engraving.webp" in text:
    print("pcat cards already present")
else:
    marker = '            <div class="pcat-card__actions">\n              <a class="pcat-card__btn pcat-card__btn--more" href="uslugi/blagoustrojstvo-mogil/">Подробнее</a>\n              <button type="button" class="pcat-card__btn pcat-card__btn--calc" data-pcat-calc="Благоустройство участка">Получить расчет</button>\n            </div>\n          </div>\n        </article>\n      </div>'
    if marker not in text:
        raise SystemExit("landscape card end marker not found")
    text = text.replace(
        marker,
        marker.replace(
            "        </article>\n      </div>",
            "        </article>\n\n" + cards + "\n      </div>",
        ),
        1,
    )
    # restore nth-child(9) delay if missing
    if "pcat-card:nth-child(9)" not in text:
        text = text.replace(
            ".pcat__grid.is-in .pcat-card:nth-child(8) { transition-delay: 0.46s; }",
            ".pcat__grid.is-in .pcat-card:nth-child(8) { transition-delay: 0.46s; }\n    .pcat__grid.is-in .pcat-card:nth-child(9) { transition-delay: 0.52s; }",
        )
    print("restored pcat-08 and pcat-09")

# 2) Remove last 2 monuments from big catalog (№079, №080)
text2, n = re.subn(
    r"\n        \{ id: 'mon79',[\s\S]*?\},\n"
    r"        \{ id: 'mon80',[\s\S]*?\},",
    "",
    text,
    count=1,
)
if n != 1:
    raise SystemExit(f"expected to remove mon79/mon80 once, got {n}")

path.write_text(text2, encoding="utf-8")
print("removed monument №079 and №080 from #monuments catalog")
