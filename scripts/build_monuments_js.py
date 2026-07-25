# -*- coding: utf-8 -*-
from pathlib import Path
import json

items_dir = Path(r"C:\Users\РС\OneDrive\Desktop\AngelGranit-temp\images\catalog\monuments\items")
index = json.loads((items_dir / "index.json").read_text(encoding="utf-8"))
lines = []
for it in index:
    n = it["num"]
    fname = f"monument-{n:03d}.jpg"
    name = f"Памятник №{n:03d}"
    note = "Гранитный памятник из каталога · цена по запросу · изготовление и установка"
    keys = [f"памятник {n}", f"памятник №{n}", f"модель {n}", f"monument {n}"]
    if n <= 5:
        keys += ["памятник", "гранитн памят", "каталог памят"]
    keys_js = ", ".join(json.dumps(k, ensure_ascii=False) for k in keys)
    lines.append(
        "        { id: '%s', cat: 'monument', name: %s, note: %s, img: %s, keys: [%s] },"
        % (
            f"mon{n}",
            json.dumps(name, ensure_ascii=False),
            json.dumps(note, ensure_ascii=False),
            json.dumps(f"images/catalog/monuments/items/{fname}", ensure_ascii=False),
            keys_js,
        )
    )

out = Path(r"C:\Users\РС\OneDrive\Desktop\AngelGranit-temp\scripts\monuments_catalog_snippet.js")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("entries", len(lines), "->", out)
size = sum(f.stat().st_size for f in items_dir.glob("*.jpg")) / 1e6
print(f"jpg MB {size:.1f}")
