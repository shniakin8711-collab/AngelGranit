# -*- coding: utf-8 -*-
"""Full-site audit for AngelGranit static pages."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://angelgranit.com"
SKIP_DIRS = {".git", ".idea", "scripts", "node_modules", "__pycache__", "assets"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.scripts_ld: list[str] = []
        self._in_ld = False
        self._ld_buf: list[str] = []
        self.h1: list[str] = []
        self._in_h1 = False
        self._h1_buf: list[str] = []
        self.imgs: list[dict[str, str]] = []
        self.canonical = ""
        self.lang = ""
        self.has_viewport = False
        self.has_manifest = False
        self.has_favicon = False
        self.og: dict[str, str] = {}
        self.twitter: dict[str, str] = {}
        self.robots = ""
        self.description = ""
        self.a_hrefs: list[str] = []
        self._in_a = False
        self._a_attrs: dict[str, str] = {}
        self.empty_links = 0
        self.buttons_no_type = 0
        self.inputs_no_labelish = 0
        self._open_label = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = d.get("lang", "")
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            self.metas.append(d)
            name = d.get("name", "").lower()
            prop = d.get("property", "").lower()
            if name == "viewport":
                self.has_viewport = True
            if name == "description":
                self.description = d.get("content", "")
            if name == "robots":
                self.robots = d.get("content", "")
            if prop.startswith("og:"):
                self.og[prop] = d.get("content", "")
            if name.startswith("twitter:"):
                self.twitter[name] = d.get("content", "")
        if tag == "link":
            self.links.append(d)
            rel = d.get("rel", "").lower()
            href = d.get("href", "")
            if rel == "canonical":
                self.canonical = href
            if "icon" in rel or rel == "apple-touch-icon":
                self.has_favicon = True
            if rel == "manifest":
                self.has_manifest = True
        if tag == "script" and d.get("type") == "application/ld+json":
            self._in_ld = True
            self._ld_buf = []
        if tag == "h1":
            self._in_h1 = True
            self._h1_buf = []
        if tag == "img":
            self.imgs.append(d)
        if tag == "a":
            self._in_a = True
            self._a_attrs = d
            href = d.get("href", "").strip()
            self.a_hrefs.append(href)
            if not href or href == "#":
                # allow intentional placeholders with id handlers later
                if not any(k.startswith("data-") for k in d) and "id" not in d:
                    self.empty_links += 1
        if tag == "button" and "type" not in d:
            self.buttons_no_type += 1
        if tag == "label":
            self._open_label = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self._in_ld = False
            self.scripts_ld.append("".join(self._ld_buf).strip())
        if tag == "h1" and self._in_h1:
            self._in_h1 = False
            self.h1.append("".join(self._h1_buf).strip())
        if tag == "a":
            self._in_a = False
        if tag == "label":
            self._open_label = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._ld_buf.append(data)
        if self._in_h1:
            self._h1_buf.append(data)


def iter_html() -> list[Path]:
    out = []
    for p in ROOT.rglob("index.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    if (ROOT / "404.html").exists():
        out.append(ROOT / "404.html")
    return sorted(out)


def rel_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE}/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-10]}"
    return f"{BASE}/{rel}"


def schema_types(blobs: list[str]) -> set[str]:
    types: set[str] = set()
    for blob in blobs:
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            types.add("INVALID_JSON")
            continue
        stack = [data]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                t = cur.get("@type")
                if isinstance(t, list):
                    types.update(str(x) for x in t)
                elif t:
                    types.add(str(t))
                if "@graph" in cur and isinstance(cur["@graph"], list):
                    stack.extend(cur["@graph"])
                for v in cur.values():
                    if isinstance(v, (dict, list)):
                        stack.append(v)
            elif isinstance(cur, list):
                stack.extend(cur)
    return types


def main() -> None:
    pages = iter_html()
    issues: list[dict] = []
    titles: dict[str, list[str]] = defaultdict(list)
    descs: dict[str, list[str]] = defaultdict(list)
    canons: dict[str, list[str]] = defaultdict(list)
    h1s: dict[str, list[str]] = defaultdict(list)

    missing_canonical = 0
    missing_desc = 0
    missing_og = 0
    missing_twitter = 0
    missing_h1 = 0
    multi_h1 = 0
    bad_desc_len = 0
    imgs_no_alt = 0
    imgs_no_dims = 0
    imgs_eager_heavy = 0
    schema_invalid = 0
    no_favicon = 0
    no_lang = 0
    broken_internal = 0
    link_targets: Counter[str] = Counter()

    existing_urls = {rel_url(p).rstrip("/") + "/" if rel_url(p).endswith("/") or p.name == "index.html" else rel_url(p) for p in pages}
    # normalize set of path suffixes
    path_set = set()
    for p in pages:
        u = rel_url(p)
        path_set.add(u.rstrip("/"))
        path_set.add(u if u.endswith("/") else u + "/")

    for p in pages:
        html = p.read_text(encoding="utf-8", errors="replace")
        parser = PageParser()
        try:
            parser.feed(html)
        except Exception as e:
            issues.append({"sev": "high", "file": str(p.relative_to(ROOT)), "msg": f"HTML parse error: {e}"})
            continue
        url = rel_url(p)
        rel = str(p.relative_to(ROOT))

        title = parser.title.strip()
        if not title:
            issues.append({"sev": "high", "file": rel, "msg": "Missing <title>"})
        else:
            titles[title].append(rel)
            if len(title) < 30 or len(title) > 70:
                issues.append({"sev": "med", "file": rel, "msg": f"Title length {len(title)} (ideal 30–60)"})

        if not parser.description:
            missing_desc += 1
            if "404" not in rel:
                issues.append({"sev": "high", "file": rel, "msg": "Missing meta description"})
        else:
            descs[parser.description].append(rel)
            n = len(parser.description)
            if n < 120 or n > 170:
                bad_desc_len += 1
                issues.append({"sev": "med", "file": rel, "msg": f"Description length {n} (ideal 140–160)"})

        if not parser.canonical and "404" not in rel:
            missing_canonical += 1
            issues.append({"sev": "high", "file": rel, "msg": "Missing canonical"})
        elif parser.canonical:
            canons[parser.canonical].append(rel)
            if not parser.canonical.startswith(BASE):
                issues.append({"sev": "med", "file": rel, "msg": f"Canonical outside BASE: {parser.canonical}"})

        if not parser.h1:
            missing_h1 += 1
            if "404" not in rel:
                issues.append({"sev": "high", "file": rel, "msg": "Missing H1"})
        elif len(parser.h1) > 1:
            multi_h1 += 1
            issues.append({"sev": "med", "file": rel, "msg": f"Multiple H1 ({len(parser.h1)})"})
        else:
            h1s[parser.h1[0]].append(rel)

        need_og = ["og:title", "og:description", "og:url", "og:image"]
        if "404" not in rel and any(k not in parser.og for k in need_og):
            missing_og += 1
            miss = [k for k in need_og if k not in parser.og]
            issues.append({"sev": "med", "file": rel, "msg": f"Missing OG: {', '.join(miss)}"})

        if "404" not in rel and ("twitter:card" not in parser.twitter and "twitter:image" not in parser.twitter):
            # soft: twitter incomplete
            if "twitter:card" not in parser.twitter:
                missing_twitter += 1
                issues.append({"sev": "low", "file": rel, "msg": "Missing Twitter Card"})

        if not parser.has_favicon and "404" not in rel:
            no_favicon += 1
            issues.append({"sev": "low", "file": rel, "msg": "Missing favicon link"})

        if not parser.lang:
            no_lang += 1
            issues.append({"sev": "med", "file": rel, "msg": "Missing html lang"})

        if not parser.has_viewport:
            issues.append({"sev": "high", "file": rel, "msg": "Missing viewport meta"})

        types = schema_types(parser.scripts_ld)
        if "INVALID_JSON" in types:
            schema_invalid += 1
            issues.append({"sev": "high", "file": rel, "msg": "Invalid JSON-LD"})

        for img in parser.imgs:
            alt = img.get("alt")
            if alt is None or alt.strip() == "":
                # decorative empty alt ok if intentionally empty string present
                if "alt" not in img:
                    imgs_no_alt += 1
                    issues.append({"sev": "med", "file": rel, "msg": f"Img without alt: {img.get('src','')[:80]}"})
            if not img.get("width") or not img.get("height"):
                imgs_no_dims += 1
            if img.get("loading") == "eager" and "hero" not in img.get("src", "") and "ytimg" not in img.get("src", ""):
                imgs_eager_heavy += 1

        # internal link resolution (sample checks)
        for href in parser.a_hrefs:
            if not href or href.startswith(("http", "mailto:", "tel:", "javascript:", "#")):
                if href.startswith(BASE):
                    link_targets[href] += 1
                continue
            # relative
            if href.startswith("?"):
                continue
            pure = href.split("#")[0].split("?")[0]
            if not pure:
                continue
            # resolve relative to page dir
            base_dir = p.parent
            target = (base_dir / pure).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if pure.endswith("/"):
                ok = (target / "index.html").exists() or target.exists()
            elif pure.endswith(".html") or pure.endswith(".xml") or pure.endswith(".webmanifest"):
                ok = target.exists()
            else:
                ok = target.exists() or (target / "index.html").exists() or target.with_suffix(".html").exists()
            if not ok and not pure.startswith("images/") and "wa.me" not in pure:
                # only report once per file+href to avoid spam later; collect
                broken_internal += 1
                if broken_internal <= 80:
                    issues.append({"sev": "high", "file": rel, "msg": f"Broken internal link: {href}"})

    # duplicates
    for title, files in titles.items():
        if len(files) > 1:
            issues.append({"sev": "high", "file": files[0], "msg": f"Duplicate title ({len(files)} pages): {title[:70]}"})
            for f in files[1:5]:
                issues.append({"sev": "high", "file": f, "msg": f"Duplicate title shared with {files[0]}"})

    for desc, files in descs.items():
        if len(files) > 1 and len(desc) > 40:
            issues.append({"sev": "med", "file": files[0], "msg": f"Duplicate description ({len(files)} pages)"})

    for can, files in canons.items():
        if len(files) > 1:
            # SEO mirrors intentionally point canonical to pillar URLs
            mirrorish = any(
                ("seo\\" in f) or ("seo/" in f.replace("\\", "/"))
                for f in files
            )
            sev = "info" if mirrorish else "high"
            issues.append({
                "sev": sev,
                "file": files[0],
                "msg": f"{'Canonical cluster with mirrors' if mirrorish else 'Duplicate canonical'} ({len(files)}): {can}",
            })

    for h1, files in h1s.items():
        if len(files) > 1:
            issues.append({"sev": "med", "file": files[0], "msg": f"Duplicate H1 ({len(files)}): {h1[:60]}"})

    # sitemap vs pages
    sm = ROOT / "sitemap.xml"
    sm_urls = set(re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8"))) if sm.exists() else set()
    page_urls = {rel_url(p) if rel_url(p).endswith("/") or p.name != "index.html" else rel_url(p) for p in pages if p.name == "index.html"}
    page_urls = set()
    for p in pages:
        if p.name != "index.html":
            continue
        u = rel_url(p)
        if not u.endswith("/"):
            u += "/"
        if "404" in u:
            continue
        page_urls.add(u)

    missing_in_sm = sorted(page_urls - sm_urls)[:30]
    extra_in_sm = sorted(sm_urls - page_urls)[:30]
    for u in missing_in_sm:
        # skip SEO mirrors that canonicalize away from self
        if "/seo/" in u:
            # find page and check canonical
            rel = u.replace(BASE + "/", "").strip("/")
            p = ROOT / rel / "index.html" if rel else ROOT / "index.html"
            if p.exists():
                html = p.read_text(encoding="utf-8", errors="replace")
                m = re.search(r'rel="canonical" href="([^"]+)"', html)
                if m and m.group(1).rstrip("/") != u.rstrip("/"):
                    issues.append({"sev": "info", "file": "sitemap.xml", "msg": f"Mirror excluded from sitemap (ok): {u}"})
                    continue
        issues.append({"sev": "med", "file": "sitemap.xml", "msg": f"Page not in sitemap: {u}"})
    for u in extra_in_sm:
        issues.append({"sev": "low", "file": "sitemap.xml", "msg": f"Sitemap URL without page: {u}"})

    # robots
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT / "robots.txt").exists() else ""
    if "Sitemap:" not in robots:
        issues.append({"sev": "high", "file": "robots.txt", "msg": "No Sitemap directive"})

    # summarize
    sev_count = Counter(i["sev"] for i in issues)
    report = {
        "pages": len(pages),
        "sitemap_urls": len(sm_urls),
        "severity": dict(sev_count),
        "stats": {
            "missing_canonical": missing_canonical,
            "missing_desc": missing_desc,
            "missing_og": missing_og,
            "missing_twitter": missing_twitter,
            "missing_h1": missing_h1,
            "multi_h1": multi_h1,
            "bad_desc_len": bad_desc_len,
            "imgs_no_alt_attr": imgs_no_alt,
            "imgs_no_dims": imgs_no_dims,
            "schema_invalid": schema_invalid,
            "no_favicon": no_favicon,
            "broken_internal_reported": broken_internal,
            "duplicate_titles": sum(1 for f in titles.values() if len(f) > 1),
            "duplicate_descriptions": sum(1 for f in descs.values() if len(f) > 1),
            "duplicate_canonicals": sum(1 for f in canons.values() if len(f) > 1),
        },
        "top_issues": issues[:200],
        "issue_total": len(issues),
    }
    out = ROOT / "scripts" / "site" / "audit_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "pages": report["pages"],
        "sitemap_urls": report["sitemap_urls"],
        "severity": report["severity"],
        "stats": report["stats"],
        "issue_total": report["issue_total"],
        "sample": report["top_issues"][:40],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
