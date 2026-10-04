# -*- coding: utf-8 -*-
"""Sync Google Maps reviews from data/google-maps-reviews.json into site HTML."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "google-maps-reviews.json"
MAPS = "https://maps.app.goo.gl/iCafhcUum875QLf59"

STAR = (
    '<svg viewBox="0 0 20 20" aria-hidden="true">'
    '<path fill="currentColor" d="M10 1.6l2.35 4.76 5.25.76-3.8 3.7.9 5.22L10 13.58 5.3 16.04l.9-5.22-3.8-3.7 5.25-.76L10 1.6z"/></svg>'
)
STARS_5 = STAR * 5
GOOGLE_BADGE = (
    '<svg viewBox="0 0 24 24" aria-hidden="true">'
    '<path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1z"/>'
    '<path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>'
    '<path fill="#FBBC04" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>'
    '<path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>'
    "</svg>"
)


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def card_otzyvy(r: dict) -> str:
    name = html.escape(r["author"])
    text = html.escape(r["text"])
    letter = html.escape(r.get("avatarLetter") or r["author"][:1])
    color = html.escape(r.get("avatarColor") or "#4285f4")
    date = html.escape(r.get("relativeDate") or "")
    date_line = f'\n                <p class="gmaps-review__date">{date}</p>' if date else ""
    return f"""          <article class="gmaps-review">
            <header class="gmaps-review__head">
              <span class="gmaps-review__avatar" style="--avatar-bg:{color}" aria-hidden="true">{letter}</span>
              <div class="gmaps-review__who">
                <strong class="gmaps-review__name">{name}</strong>
                <div class="gmaps-review__stars" aria-label="Оценка 5 из 5">
                  {STARS_5}
                </div>{date_line}
                <p class="gmaps-review__source"><a href="{MAPS}" target="_blank" rel="noopener noreferrer">Google</a> · Maps</p>
              </div>
            </header>
            <p class="gmaps-review__text">{text}</p>
            <footer class="gmaps-review__foot">
              <span class="gmaps-review__google-badge">
                {GOOGLE_BADGE}
                Опубликовано в Google
              </span>
              <a href="{MAPS}" target="_blank" rel="noopener noreferrer">ИП Шнякина Н.</a>
            </footer>
          </article>"""


def card_home(r: dict) -> str:
    name = html.escape(r["author"])
    text = html.escape(r["text"])
    letter = html.escape(r.get("avatarLetter") or r["author"][:1])
    color = html.escape(r.get("avatarColor") or "#4285f4")
    return f"""            <article class="review-card gmaps-review">
              <header class="gmaps-review__head">
                <span class="gmaps-review__avatar" style="--avatar-bg:{color}" aria-hidden="true">{letter}</span>
                <div class="gmaps-review__who">
                  <strong class="gmaps-review__name">{name}</strong>
                  <div class="gmaps-review__stars" aria-label="Оценка 5 из 5">
                    {STARS_5}
                  </div>
                  <p class="gmaps-review__source"><a href="{MAPS}" target="_blank" rel="noopener noreferrer">Google</a> · Maps</p>
                </div>
              </header>
              <p class="gmaps-review__text">{text}</p>
              <footer class="gmaps-review__foot">
                <span class="gmaps-review__google-badge">
                  {GOOGLE_BADGE}
                  Опубликовано в Google
                </span>
                <a href="{MAPS}" target="_blank" rel="noopener noreferrer">ИП Шнякина Н.</a>
              </footer>
            </article>"""


def review_schema(r: dict, idx: int) -> dict:
    return {
        "@type": "Review",
        "@id": f"https://angelgranit.com/otzyvy/#review-{idx}",
        "author": {"@type": "Person", "name": r["author"]},
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": str(r["rating"]),
            "bestRating": "5",
        },
        "reviewBody": r["text"],
        "itemReviewed": {"@id": "https://angelgranit.com/#business"},
        "publisher": {"@type": "Organization", "name": "Google"},
    }


def patch_otzyvy(reviews: list[dict]) -> None:
    path = ROOT / "otzyvy" / "index.html"
    text = path.read_text(encoding="utf-8")
    block = "\n".join(card_otzyvy(r) for r in reviews)
    text = re.sub(
        r'(<div class="gmaps-reviews">)\s*[\s\S]*?(</div>\s*<h2>Хотите оставить отзыв)',
        rf"\1\n{block}\n        \2",
        text,
        count=1,
    )
    n = len(reviews)
    names = ", ".join(r["author"] for r in reviews[:3])
    if n > 3:
        names += f" и ещё {n - 3}"
    text = re.sub(
        r"<p class=\"lead\">[^<]*</p>",
        f'<p class="lead">Оригинальные отзывы с Google Maps — карточка ИП Шнякина Н / AngelGranit. На странице {n} публичных отзыва (5★); имена и текст — как в Google.</p>',
        text,
        count=1,
    )
    text = re.sub(
        r'content="Реальные отзывы Google Maps[^"]*"',
        f'content="Реальные отзывы Google Maps об AngelGranit / ИП Шнякина Н.: {n} отзыва, 5★. {names}."',
        text,
        count=1,
    )
    agg = {
        "@type": "AggregateRating",
        "ratingValue": "5",
        "reviewCount": str(n),
        "bestRating": "5",
    }
    graph_extra = [review_schema(r, i + 1) for i, r in enumerate(reviews)]
    if '"aggregateRating"' not in text:
        text = text.replace(
            '"openingHours": "Mo-Su 00:00-24:00"\n    }',
            '"openingHours": "Mo-Su 00:00-24:00",\n'
            f'      "aggregateRating": {json.dumps(agg, ensure_ascii=False)}\n    }}',
            1,
        )
    else:
        text = re.sub(
            r'"aggregateRating": \{[^}]+\}',
            f'"aggregateRating": {json.dumps(agg, ensure_ascii=False)}',
            text,
            count=1,
        )
    if '"@type": "Review"' not in text:
        insert = ",\n    " + ",\n    ".join(
            json.dumps(x, ensure_ascii=False, indent=2).replace("\n", "\n    ")
            for x in graph_extra
        )
        text = text.replace("\n  ]\n}\n  </script>", insert + "\n  ]\n}\n  </script>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")
    print("otzyvy/index.html:", n, "reviews")


def patch_home(reviews: list[dict]) -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    block = "\n".join(card_home(r) for r in reviews)
    text = re.sub(
        r'(<div class="reviews-carousel__track" data-reviews-track>)\s*[\s\S]*?(</div>\s*</div>\s*<div class="reviews-carousel__controls">)',
        rf"\1\n{block}\n          \2",
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8", newline="\n")
    print("index.html carousel:", len(reviews), "reviews")


def main() -> None:
    payload = load()
    reviews = payload["reviews"]
    patch_otzyvy(reviews)
    patch_home(reviews)


if __name__ == "__main__":
    main()
