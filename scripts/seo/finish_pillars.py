# -*- coding: utf-8 -*-
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
text = """User-agent: *
Allow: /
Allow: /seo/
Allow: /ritualnye-uslugi-almaty/
Allow: /organizaciya-pohoron-almaty/
Allow: /katafalk-almaty/
Allow: /pamyatniki-almaty/
Allow: /granitnye-pamyatniki-almaty/
Allow: /memorialnye-kompleksy-almaty/
Allow: /ritualny-agent-almaty/
Allow: /ritualnye-prinadlezhnosti-almaty/

Sitemap: https://shniakin8711-collab.github.io/AngelGranit/sitemap.xml
"""
(ROOT / "robots.txt").write_text(text, encoding="utf-8", newline="\n")
print("robots ok")

html = (ROOT / "index.html").read_text(encoding="utf-8")
m = re.search(r'name="description" content="([^"]*)"', html)
print("desc len", len(m.group(1)) if m else None)
art = re.search(r'id="seo-ritualnye-uslugi"[\s\S]*?</section>', html)
if art:
    plain = re.sub(r"<[^>]+>", " ", art.group(0))
    print("article words", len(re.findall(r"\w+", plain, flags=re.UNICODE)))

r = subprocess.run([sys.executable, str(Path(__file__).with_name("build_pillars.py"))], cwd=ROOT)
raise SystemExit(r.returncode)
