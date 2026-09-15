# SEO / GEO — финальный отчёт (вариант B)

Дата: **2026-09-15**  
Сайт: https://angelgranit.com/  
Скоуп: read-only P0 → безопасные фиксы → citability на хабах → push

---

## Вердикт

P0-база уже была чистой. Вариант B усилил **цитируемость для ИИ** на денежных/entity-хабах и поправил мелкий NAP в футерах — без массовых переписываний и без выдуманных рейтингов/цен.

| Область | Было (план) | После B | Комментарий |
| --- | ---: | ---: | --- |
| Technical SEO | 78 | **80** | lastmod хабов, footer NAP, schema Organization на /uslugi/ |
| On-Page / citability | 74 | **82** | WHO/WHAT/WHERE блоки на 6 хабах |
| Local SEO | 85 | **86** | единый NAP + Maps CID в speakable-блоках |
| GEO / AI | 82 | **86** | хабы явно ведут в /geo/ + /ai/ |
| Schema | 76 | **78** | Organization на каталоге услуг; без AggregateRating |
| **Итоговый SEO** | ~77 | **~81** | |
| **Итоговый GEO** | ~82 | **~86** | |
| **Итоговый Local** | ~85 | **~86** | |

---

## Что найдено (P0 audit)

- HTML ~454; `noindex` только на служебных (404 / klastery / temy) — ок.
- Критичных битых относительных ссылок на хабах — 0.
- `http://` canonical/href на проде — не найдено.
- `AggregateRating` в schema — нет (упоминания только как анти-фейк текст).
- Мелочь: в футерах часто `5а<a href="tel:` без пробела/разделителя — исправлено скриптом.

---

## Что сделано в B

1. **Citability** (класс `.citability`, speakable):  
   `/uslugi/`, `/kontakty/`, `/ceny/`, `/o-kompanii/`, `/geo/`, `/ai/`
2. **Schema:** Organization + связанный CollectionPage на `/uslugi/`
3. **CSS:** стили `.citability` в `assets/site/page.css`
4. **NAP footer:** пробел/` · ` перед `tel:` по всему сайту
5. **Homepage:** `dateModified` → 2026-09-15
6. **Sitemap:** lastmod хабов → 2026-09-15
7. Скрипты: `scripts/fix-nap-footer-space.cjs`, `scripts/bump-hub-lastmod.cjs` (+ уже был `audit-p0.cjs`)

Не трогали: формы, WA, телефон, карты, дизайн hero, цены/отзывы/рейтинги, силосы `/uslugi` · `/seo` · `/geo`.

---

## Remaining (владелец / вне кода)

- GSC: переобход хабов после деплоя  
- Bing: sitemap = `https://angelgranit.com/sitemap.xml` (не github.io)  
- GBP / 2ГИС: сверка NAP с сайтом вручную  
- Performance / Lighthouse главной — отдельный замер  
- Не запускать полный mega-rewrite без нового запроса  

---

## Силосы (напоминание)

| Путь | Роль |
| --- | --- |
| `/uslugi/` | коммерческий канон (money) |
| `/seo/` | Google-лендинги |
| `/geo/` | краткие ответы для ИИ |
| `/ai/` + `AI.md` + `llms.txt` | машиночитаемый канон сущности |
