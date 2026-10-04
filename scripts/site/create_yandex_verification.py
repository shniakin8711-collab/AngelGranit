# -*- coding: utf-8 -*-
"""Create Yandex Webmaster HTML verification file at site root (GitHub Pages).

Usage:
  python scripts/site/create_yandex_verification.py yandex_XXXXXXXXX.html XXXXXXXXX

The code is the part after "Verification: " in the Webmaster UI (or the full line).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    if len(sys.argv) != 3:
        print(
            "Usage: python scripts/site/create_yandex_verification.py "
            "<filename> <verification_code>",
            file=sys.stderr,
        )
        sys.exit(1)
    filename, code = sys.argv[1], sys.argv[2].strip()
    if not re.fullmatch(r"yandex_[a-zA-Z0-9]+\.html", filename):
        print("Filename must match yandex_<code>.html from Yandex Webmaster", file=sys.stderr)
        sys.exit(1)
    if code.lower().startswith("verification:"):
        code = code.split(":", 1)[1].strip()
    html = (
        "<html>\n"
        "    <head>\n"
        '        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
        "    </head>\n"
        f"    <body>Verification: {code}</body>\n"
        "</html>\n"
    )
    out = ROOT / filename
    out.write_text(html, encoding="utf-8", newline="\n")
    print(f"Written: {out}")
    print(f"URL after deploy: https://angelgranit.com/{filename}")


if __name__ == "__main__":
    main()
