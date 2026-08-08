# -*- coding: utf-8 -*-
"""Shared SEO head fragments for generated pages."""
from __future__ import annotations


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
) -> str:
    return f"""  <meta property="og:type" content="{og_type}" />
  <meta property="og:locale" content="ru_RU" />
  <meta property="og:site_name" content="AngelGranit — ритуальные услуги Алматы" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="{image}" />
  <meta property="og:image:alt" content="{title}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{image}" />"""
