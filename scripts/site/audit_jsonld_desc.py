# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

h = (Path(__file__).resolve().parents[2] / "index.html").read_text(encoding="utf-8")
m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S)
g = json.loads(m.group(1))
graph = g.get("@graph", [g])


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{path}.{k}" if path else k
            if k == "description" and isinstance(v, str):
                n = len(v)
                if n < 25 or n > 160:
                    print(n, p)
                    print(" ", v)
            else:
                walk(v, p)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            walk(x, f"{path}[{i}]")


walk(graph)
