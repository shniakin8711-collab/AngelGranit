# -*- coding: utf-8 -*-
"""Align homepage JSON-LD descriptions with meta (25–160 chars)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
META_DESC = (
    "Ритуальные услуги Алматы 24/7: похороны, катафалк, памятники из гранита, благоустройство. "
    "AngelGranit — агент Александр, помощь семье круглосуточно."
)
MAX_L = 160
MIN_L = 25

TRIM_MAP = {
    "https://angelgranit.com/#business": META_DESC,
    "https://angelgranit.com/#webpage": META_DESC,
}


def trim(s: str) -> str:
    s = s.strip()
    if len(s) <= MAX_L:
        return s
    cut = s[: MAX_L - 1].rsplit(" ", 1)[0] + "…"
    return cut


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    m = re.search(
        r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)',
        html,
        re.S,
    )
    if not m:
        raise SystemExit("no json-ld")
    prefix, body, suffix = m.group(1), m.group(2), m.group(3)
    data = json.loads(body)
    graph = data.get("@graph", [data])
    changed = 0
    for node in graph:
        if not isinstance(node, dict):
            continue
        nid = node.get("@id", "")
        if nid in TRIM_MAP and "description" in node:
            node["description"] = TRIM_MAP[nid]
            changed += 1
        elif "description" in node and isinstance(node["description"], str):
            d = node["description"]
            if len(d) > MAX_L or len(d) < MIN_L:
                node["description"] = trim(d)
                changed += 1
    new_body = json.dumps(data, ensure_ascii=False, indent=2)
    new_html = html[: m.start()] + prefix + new_body + suffix + html[m.end() :]
    INDEX.write_text(new_html, encoding="utf-8", newline="\n")
    print("patched nodes:", changed)


if __name__ == "__main__":
    main()
