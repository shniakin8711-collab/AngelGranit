# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP = {".git", "scripts", "node_modules", "__pycache__", "assets"}
MIN_L, MAX_L = 25, 160

bad = []
for p in ROOT.rglob("index.html"):
    if any(x in SKIP for x in p.parts):
        continue
    h = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<meta name="description" content="([^"]*)"', h, re.I)
    if not m:
        bad.append((p, 0, "MISSING"))
        continue
    t = m.group(1)
    n = len(t)
    if n < MIN_L or n > MAX_L:
        bad.append((p, n, t))

import json

out = [{"path": str(p.relative_to(ROOT)).replace("\\", "/"), "len": n, "text": t} for p, n, t in bad]
(ROOT / "scripts" / "audit_meta_desc_out.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(len(bad))
