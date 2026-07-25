# -*- coding: utf-8 -*-
from pathlib import Path
import re
from collections import Counter

html = Path("index.html").read_text(encoding="utf-8")
srcs = re.findall(r'src=["\']([^"\']+)["\']', html)
missing = []
for s in srcs:
    if s.startswith("http") or s.startswith("data:"):
        continue
    if not Path(s).exists():
        missing.append(s)
print("missing", len(missing))
for m in missing:
    print(" MISSING", m)

ids = re.findall(r'\bid=["\']([^"\']+)["\']', html)
dups = [(i, c) for i, c in Counter(ids).items() if c > 1]
print("dup ids", dups)

for needle in ["FPV", "Black Hearse", "blackhearse", "youtube.com", "btn-ai-hero", "btn-share-hero", "hero__fpv"]:
    lines = [i for i, l in enumerate(html.splitlines(), 1) if needle in l]
    if lines:
        print("ref", needle, lines[:15])

# CSS brace balance in style
style = re.search(r"<style>(.*?)</style>", html, re.S)
if style:
    s = style.group(1)
    print("css braces", s.count("{"), s.count("}"))

# JS syntax rough check via node if available
js = re.search(r"<script>\s*(\(function \(\) \{.*\})\s*</script>\s*</body>", html, re.S)
print("inline script found", bool(js))
