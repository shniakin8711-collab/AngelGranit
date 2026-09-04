#!/usr/bin/env python3
"""Remove visible SEO/AI jargon from HTML UI; keep machine discovery intact."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP = {".git", "scripts", "node_modules", "__pycache__", "assets"}


def clean(html: str, rel: str) -> str:
    rel_posix = rel.replace("\\", "/")
    if rel_posix.startswith("ai/") or rel_posix == "ai/index.html":
        return html

    stats_local = 0

    html, n = re.subn(
        r'\s*<li>\s*<a href="[^"]*temy/">Темы</a>\s*</li>',
        "",
        html,
    )
    stats_local += n

    html, n = re.subn(
        r'\s*<a class="btn-site btn-site--ghost" href="[^"]*temy/">Темы</a>',
        "",
        html,
    )
    stats_local += n

    def repl_temy(m: re.Match[str]) -> str:
        return f'<a href="{m.group(1)}stati/"><strong>Статьи</strong><span>Полезные материалы</span></a>'

    html, n = re.subn(
        r'<a href="([^"]*)temy/"><strong>Тематические страницы</strong><span>Темы</span></a>',
        repl_temy,
        html,
    )
    stats_local += n

    html, n = re.subn(
        r'<a href="([^"]*)temy/"><strong>Темы</strong><span>Посадочные</span></a>',
        repl_temy,
        html,
    )
    stats_local += n

    html, n = re.subn(
        r'(<a href="[^"]*klastery/"><strong>)Все разделы(?: сайта)?(</strong><span>)(?:Разделы сайта|Разделы|Карта|Навигация)(</span></a>)',
        r"\1Карта сайта\2Все услуги и статьи\3",
        html,
    )
    stats_local += n

    for a, b in [
        ("Раздел и навигация", "Ещё по теме"),
        ("Навигация по кластеру", "Полезные ссылки"),
        ("Кластеры и доверие", "Полезные разделы"),
    ]:
        html, n = re.subn(rf"<h2>{re.escape(a)}</h2>", f"<h2>{b}</h2>", html)
        stats_local += n

    # Only replace standalone Навигация h2 inside silo blocks (avoid breadcrumbs etc.)
    html, n = re.subn(
        r"(<!-- silo-architecture:start -->[\s\S]*?)<h2>Навигация</h2>",
        r"\1<h2>Полезные ссылки</h2>",
        html,
        count=1,
    )
    stats_local += n

    span_map = {
        "Раздел": "Услуги",
        "Разделы сайта": "Каталог",
        "Разделы и услуги": "Каталог",
        "Раздел статей": "Статьи",
        "Услуга кластера": "Услуга",
        "Основной раздел": "Основное",
        "Главная страница категории": "Категория",
        "Посадочные": "Материалы",
        "База знаний": "Статьи",
        "Карта": "Обзор",
        "Подписка": "Уход",
        "Связь": "Контакты",
        "Доверие": "Отзывы",
        "Примеры": "Фото работ",
        "Кластер": "Направление",
    }
    for a, b in span_map.items():
        html, n = re.subn(rf"<span>{re.escape(a)}</span>", f"<span>{b}</span>", html)
        stats_local += n

    html, n = re.subn(r"<strong>Раздел: ", "<strong>", html)
    stats_local += n
    html, n = re.subn(r"<strong>Категория: ", "<strong>", html)
    stats_local += n

    if "o-kompanii" in rel_posix:
        html, n = re.subn(
            r"\s*<h2>Для искусственного интеллекта</h2>\s*"
            r"<p>Структурированный профиль компании для ChatGPT, Gemini, Claude и Perplexity: "
            r'<a href="[^"]*">раздел для ИИ</a>, файл <a href="[^"]*">AI\.md</a> и '
            r'<a href="[^"]*">llms\.txt</a>\.</p>',
            "",
            html,
            count=1,
        )
        stats_local += n
        html, n = re.subn(
            r'\s*<a href="[^"]*ai/"><strong>Для ИИ</strong><span>AI\.md / данные</span></a>',
            "",
            html,
        )
        stats_local += n

    for pat in [
        r'(?:\s*·\s*)?<a href="[^"]*(?:^|/)ai/">Для ИИ</a>',
        r'(?:\s*·\s*)?<a href="[^"]*AI\.md">AI\.md</a>',
        r'(?:\s*·\s*)?<a href="[^"]*llms\.txt">llms\.txt</a>',
        r'(?:\s*·\s*)?<a href="[^"]*temy/">Темы</a>',
        r'(?:\s*·\s*)?<a href="[^"]*klastery/">Разделы сайта</a>',
        r'(?:\s*·\s*)?<a href="[^"]*sitemap\.xml">Sitemap</a>',
    ]:
        html, n = re.subn(pat, "", html)
        stats_local += n

    html = re.sub(r"(?: ·){2,}", " ·", html)
    # Do not strip legitimate " · <a" separators in footers

    return html


def main() -> None:
    changed = 0
    for path in ROOT.rglob("index.html"):
        if any(p in SKIP for p in path.parts):
            continue
        rel = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8")
        new = clean(text, rel)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
            print("updated", rel)
    print("files_changed", changed)


if __name__ == "__main__":
    main()
