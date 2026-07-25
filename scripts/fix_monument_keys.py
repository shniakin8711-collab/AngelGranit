# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"C:\Users\РС\OneDrive\Desktop\AngelGranit-temp\index.html")
t = p.read_text(encoding="utf-8")
for n in range(1, 6):
    nn = f"{n:03d}"
    old = (
        f'keys: ["памятник {n}", "памятник №{n}", "модель {n}", '
        f'"monument {n}", "памятник", "гранитн памят", "каталог памят"]'
    )
    new = (
        f'keys: ["памятник {n}", "памятник №{n}", "памятник №{nn}", '
        f'"модель {n}", "monument {n}"]'
    )
    if old in t:
        t = t.replace(old, new)
        print("fixed mon", n)
    else:
        print("missing mon", n)

# bump AI catalog preview for monuments
old_slice = "var list = (items || []).slice(0, 8);"
new_slice = (
    "var list = (items || []).slice(0, "
    "(items && items.length && items[0].cat === 'monument') ? 12 : 8);"
)
if old_slice in t:
    t = t.replace(old_slice, new_slice, 1)
    print("slice updated")

old_sub = "Гробы, кресты, венки, одежда, транспорт и наборы — выберите позицию и закажите у Александра 24/7."
new_sub = "Памятники, гробы, кресты, венки, одежда, транспорт и наборы — выберите позицию и закажите у Александра 24/7."
if old_sub in t:
    t = t.replace(old_sub, new_sub, 1)
    print("subtitle updated")

p.write_text(t, encoding="utf-8")
print("done")
