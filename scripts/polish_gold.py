# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"C:\Users\РС\OneDrive\Desktop\AngelGranit-temp\index.html")
t = p.read_text(encoding="utf-8")

repls = [
    ("rgba(196,18,24,", "rgba(154,123,47,"),
    ("rgba(228,27,36,", "rgba(212,175,87,"),
    ("#ef2a32", "#d4af57"),
    ("#9e0e13", "#8a6a28"),
]
for a, b in repls:
    print(a, "->", t.count(a))
    t = t.replace(a, b)

old_veil = """      background:
        linear-gradient(180deg, rgba(7,7,8,0.55) 0%, rgba(7,7,8,0.25) 35%, rgba(7,7,8,0.55) 62%, rgba(7,7,8,0.92) 100%),
        linear-gradient(90deg, rgba(7,7,8,0.55) 0%, transparent 45%, rgba(7,7,8,0.35) 100%);"""
new_veil = """      background:
        linear-gradient(180deg, rgba(7,7,8,0.35) 0%, rgba(7,7,8,0.08) 38%, rgba(7,7,8,0.35) 68%, rgba(7,7,8,0.94) 100%);"""
if old_veil in t:
    t = t.replace(old_veil, new_veil)
    print("veil updated")
elif "rgba(7,7,8,0.08) 38%" in t:
    print("veil already new")
else:
    print("veil pattern not found")

if ".visually-hidden" not in t:
    t = t.replace(
        "code, .mono { font-family: var(--font-mono); }",
        """code, .mono { font-family: var(--font-mono); }
    .visually-hidden {
      position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
      overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0;
    }""",
    )
    print("added visually-hidden")

t = t.replace(
    "margin-bottom: clamp(4.5rem, 12vh, 7rem);",
    "margin-bottom: clamp(2.5rem, 8vh, 4.5rem);",
)

old_ico = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' fill='%23050505'/%3E"
    "%3Cpath d='M16 6c-2 3-4 5-4 8a4 4 0 108 0c0-3-2-5-4-8z' fill='none' stroke='%23e8e4dc' stroke-width='1.2'/%3E"
    "%3Cpath d='M10 14c-2 1-3 3-2 5M22 14c2 1 3 3 2 5' fill='none' stroke='%23e8e4dc' stroke-width='1'/%3E"
    "%3C/svg%3E"
)
new_ico = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' fill='%23050505'/%3E"
    "%3Ctext x='16' y='22' text-anchor='middle' font-family='Georgia,serif' font-size='12' "
    "font-weight='700' fill='%23d4af57'%3EAG%3C/text%3E%3C/svg%3E"
)
if old_ico in t:
    t = t.replace(old_ico, new_ico)
    print("favicon updated")
elif "fill='%23d4af57'" in t or 'fill="%23d4af57"' in t or "fill=%23d4af57" in t:
    print("favicon already gold")
else:
    print("favicon unknown")

for needle in ["FPV", "Black Hearse", "blackhearse", "youtube.com", "id=\"youtube\""]:
    lines = [i for i, l in enumerate(t.splitlines(), 1) if needle.lower() in l.lower()]
    if lines:
        print("LEFT", needle, lines[:12])

p.write_text(t, encoding="utf-8")
print("done")
