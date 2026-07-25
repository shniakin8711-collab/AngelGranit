# -*- coding: utf-8 -*-
from pathlib import Path

html_path = Path(r"C:\Users\РС\OneDrive\Desktop\AngelGranit-temp\index.html")
snippet = Path(r"C:\Users\РС\OneDrive\Desktop\AngelGranit-temp\scripts\monuments_catalog_snippet.js").read_text(encoding="utf-8").rstrip()
text = html_path.read_text(encoding="utf-8")

old_cats = """      var CATALOG_CATS = [
        { id: 'all', label: 'Все' },
        { id: 'coffin', label: 'Гробы' },
        { id: 'cross', label: 'Кресты' },
        { id: 'wreath', label: 'Венки' },
        { id: 'clothes', label: 'Одежда' },
        { id: 'transport', label: 'Транспорт' },
        { id: 'set', label: 'Наборы' }
      ];"""

new_cats = """      var CATALOG_CATS = [
        { id: 'all', label: 'Все' },
        { id: 'monument', label: 'Памятники' },
        { id: 'coffin', label: 'Гробы' },
        { id: 'cross', label: 'Кресты' },
        { id: 'wreath', label: 'Венки' },
        { id: 'clothes', label: 'Одежда' },
        { id: 'transport', label: 'Транспорт' },
        { id: 'set', label: 'Наборы' }
      ];"""

if old_cats not in text:
    raise SystemExit("CATALOG_CATS block not found")
text = text.replace(old_cats, new_cats, 1)

marker = (
    "        { id: 's2', cat: 'set', name: 'Orthodox Burial Set Classic White', "
    "note: 'Покрывало и подушка · модель Classic White', "
    "img: 'images/catalog/set-burial-classic-white.png', "
    "keys: ['покрывало', 'атлас набор', 'classic white', 'погребальн комплект'] }\n      ];"
)
if marker not in text:
    raise SystemExit("s2 marker not found")
replacement = marker.replace("\n      ];", ",\n" + snippet + "\n      ];")
text = text.replace(marker, replacement, 1)

old_chips = "          { label: 'Наборы', cat: 'set' }\n        ];"
new_chips = (
    "          { label: 'Наборы', cat: 'set' },\n"
    "          { label: 'Памятники', cat: 'monument' }\n"
    "        ];"
)
if old_chips not in text:
    raise SystemExit("chips not found")
text = text.replace(old_chips, new_chips, 1)

old_quick = """            'Покажи каталог',
            'Покажи гробы',
            'Покажи венки',
            'Поминки Алматы',
            'Вызвать батюшку'
"""
new_quick = """            'Покажи каталог',
            'Покажи памятники',
            'Покажи гробы',
            'Покажи венки',
            'Вызвать батюшку'
"""
if old_quick not in text:
    raise SystemExit("quick buttons not found")
text = text.replace(old_quick, new_quick, 1)

html_path.write_text(text, encoding="utf-8")
print("patched ok, monuments:", text.count("cat: 'monument'"))
