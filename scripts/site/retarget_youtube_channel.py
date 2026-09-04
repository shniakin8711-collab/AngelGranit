# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTS = {".html", ".md", ".txt", ".py", ".xml", ".js", ".css"}

BLACK = "https://www.youtube.com/@AngelGranitfpv"
BARE = re.compile(r"https://www\.youtube\.com/@AngelGranit(?!fpv)")
NEW = "https://www.youtube.com/@AngelGranitfpv"


def main() -> None:
    n = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        if "node_modules" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        new = text.replace(BLACK, NEW)
        new = BARE.sub(NEW, new)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            n += 1
            print(path.relative_to(ROOT))
    print(f"updated={n}")


if __name__ == "__main__":
    main()
