# -*- coding: utf-8 -*-
from pathlib import Path
import re
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[2]


def check_local_encoding():
    p = ROOT / "ritualnye-uslugi-almaty" / "index.html"
    raw = p.read_bytes()
    text = p.read_text(encoding="utf-8")
    print("local has BOM", raw.startswith(b"\xef\xbb\xbf"))
    print("local charset meta", "charset=UTF-8" in text or 'charset="UTF-8"' in text)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text)
    print("local h1", h1.group(1) if h1 else None)
    alt = re.search(r'alt="([^"]+)"', text)
    print("local first alt", alt.group(1) if alt else None)
    # mojibake markers
    print("local has replacement char", "\ufffd" in text)


def check_live():
    url = "https://shniakin8711-collab.github.io/AngelGranit/ritualnye-uslugi-almaty/"
    with urllib.request.urlopen(url, timeout=30) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    print("live content-type", ctype)
    text = data.decode("utf-8")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text)
    print("live h1", h1.group(1) if h1 else None)
    alt = re.search(r'<figure class="seo-figure">.*?<img[^>]+alt="([^"]+)"', text, re.S)
    print("live first figure alt", alt.group(1) if alt else None)
    print("live has mojibake", "Ритуальные" not in text and "Ритуальн" not in text)


def check_schema():
    errs = []
    paths = [ROOT / "index.html"]
    paths += list(ROOT.glob("*/index.html"))
    for p in paths:
        if p.parent.name in {".idea", "assets"}:
            continue
        if "seo" in p.parts and p.parent.name == "assets":
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                errs.append(f"{p}: {e}")
    print("schema errors", len(errs))
    for e in errs[:10]:
        print(" ", e)


def check_imgs():
    missing = []
    for p in ROOT.glob("*/index.html"):
        if p.parent.name in {".idea"}:
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        for src in re.findall(r'src="([^"]+)"', t):
            if src.startswith(("http", "data:", "#")):
                continue
            cand = (p.parent / src).resolve()
            if not cand.exists():
                missing.append(f"{p.parent.name}: {src}")
    print("missing images", len(missing))
    for m in missing[:20]:
        print(" ", m)


if __name__ == "__main__":
    check_local_encoding()
    check_live()
    check_schema()
    check_imgs()
