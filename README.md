# AngelGranit

Православные памятники и ритуальные услуги · Алматы

Сайт: https://angelgranit.com/

## Сборка и публикация

Статический сайт для **GitHub Pages** (корень репозитория — документ root). HTML-страницы лежат в каталогах с `index.html`; карта сайта пересобирается скриптом:

```bash
python scripts/site/sitemap_utils.py
# или полный прогон правил индексации (noindex для /geo/ и тонких населённых пунктов + sitemap):
python scripts/site/apply_indexation_rules.py
```

Не правьте `sitemap.xml` вручную — только генераторы в `scripts/site/`.

## HTTPS и редиректы (обязательно вне репозитория)

GitHub Pages **не позволяет** задать в коде репозитория принудительный **301** с `http://angelgranit.com` и `http://www.angelgranit.com` на `https://angelgranit.com`. В HTML/JS **не** имитируйте редирект — только настройки хостинга/DNS.

1. **GitHub Pages** → Settings → Pages → Custom domain `angelgranit.com` → включить **Enforce HTTPS** (после выпуска сертификата Let’s Encrypt).
2. Проверка после включения:
   - `https://www.angelgranit.com/…` → **301** на `https://angelgranit.com/…` (уже работает при корректном apex).
   - `http://angelgranit.com/…` и `http://www.angelgranit.com/…` → **301** на `https://angelgranit.com/…` (path и query сохраняются).
3. Если apex по HTTP всё ещё отдаёт **200**, поставьте **Cloudflare** (или другой reverse proxy) перед доменом:
   - SSL/TLS: **Full (strict)**
   - **Always Use HTTPS**
   - Рекомендуется **HSTS** (минимум `max-age=31536000; includeSubDomains`) после стабильного HTTPS.
4. В коде и метаданных используйте только `https://angelgranit.com` (без `http://`).

## Подтверждение сайта в Яндекс Вебмастере (HTML-файл)

1. В [Вебмастере](https://webmaster.yandex.ru/) → сайт `angelgranit.com` → **Подтверждение прав** → способ **HTML-файл**.
2. Скопируйте **имя файла** (например `yandex_ab12cd34.html`) и **код** из строки `Verification: …`.
3. В корне репозитория создайте файл:

```bash
python scripts/site/create_yandex_verification.py yandex_XXXXX.html XXXXX
```

4. Закоммитьте файл в **корень** репозитория (рядом с `index.html`), задеployьте Pages и нажмите **Проверить** в Вебмастере. URL: `https://angelgranit.com/yandex_XXXXX.html`.

## SEO после деплоя

- Google Search Console / Яндекс Вебмастер: переотправить `https://angelgranit.com/sitemap.xml`, запросить переобход главной и ключевых money-URL.
- IndexNow (опционально): `node scripts/submit-indexnow.cjs`
