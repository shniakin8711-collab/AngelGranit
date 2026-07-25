# -*- coding: utf-8 -*-
from pathlib import Path
import re
import subprocess
import tempfile

html = Path(r"C:\Users\РС\OneDrive\Desktop\AngelGranit-temp\index.html").read_text(encoding="utf-8")
scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.S | re.I)
print("script blocks:", len(scripts))
for i, s in enumerate(scripts):
    if "var CATALOG" not in s:
        continue
    # wrap in function or just check syntax - strip DOM-dependent? just syntax check
    path = Path(tempfile.gettempdir()) / f"angel_catalog_check_{i}.js"
    path.write_text(s, encoding="utf-8")
    r = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
    print("CATALOG script check:", r.returncode)
    if r.stderr:
        print(r.stderr[:2000])
    # find CATALOG end
    m = re.search(r"var CATALOG = \[", s)
    print("CATALOG start at", m.start() if m else None)
    # count braces balance around monuments
    print("mon entries", s.count("cat: 'monument'"))
    print("has mon80", "mon80" in s)
    # show around end of CATALOG
    end = s.find("];\n\n      var catFilter")
    if end < 0:
        end = s.find("var catFilter")
        print("near catFilter:", repr(s[end-200:end+50]))
    else:
        print("catalog close ok, last 250:", repr(s[end-250:end+30]))
