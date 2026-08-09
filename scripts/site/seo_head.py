# -*- coding: utf-8 -*-
"""Shared SEO head fragments for generated pages."""
from __future__ import annotations
from html import escape


def icon_links(prefix: str) -> str:
    """prefix e.g. '../' or '../../' relative to page."""
    return f"""  <link rel="icon" href="{prefix}assets/icons/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="{prefix}assets/icons/favicon-32.png" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="{prefix}assets/icons/apple-touch-icon.png" />
  <link rel="manifest" href="{prefix}site.webmanifest" />
  <meta name="theme-color" content="#d4af57" />"""


def social_meta(
    *,
    title: str,
    desc: str,
    url: str,
    image: str,
    og_type: str = "website",
    image_width: str = "1600",
    image_height: str = "900",
    keywords: str = "",
) -> str:
    t = escape(title, quote=True)
    d = escape(desc, quote=True)
    u = escape(url, quote=True)
    i = escape(image, quote=True)
    kw = ""
    if keywords:
        kw = f'\n  <meta name="keywords" content="{escape(keywords, quote=True)}" />'
    return f"""  <meta property="og:type" content="{og_type}" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:site_name" content="AngelGranit — ритуальные услуги Алматы" />
  <meta property="og:url" content="{u}" />
  <meta property="og:title" content="{t}" />
  <meta property="og:description" content="{d}" />
  <meta property="og:image" content="{i}" />
  <meta property="og:image:alt" content="{t}" />
  <meta property="og:image:width" content="{image_width}" />
  <meta property="og:image:height" content="{image_height}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{t}" />
  <meta name="twitter:description" content="{d}" />
  <meta name="twitter:image" content="{i}" />{kw}"""
