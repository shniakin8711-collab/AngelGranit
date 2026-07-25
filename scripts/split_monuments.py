# -*- coding: utf-8 -*-
"""Split printed monument catalog page photos into individual product tiles."""
from __future__ import annotations

from pathlib import Path
import json
import re

import cv2
import numpy as np

ROOT = Path(r"C:\Users\РС\OneDrive\Desktop\AngelGranit-temp\images\catalog\monuments")
OUT = ROOT / "items"
OUT.mkdir(parents=True, exist_ok=True)

# Known page layouts from OCR-ish visual inventory (page hash -> model numbers LTR/TTB)
PAGE_MODELS: dict[str, list[int]] = {
    # filled after detection + optional overrides
}


def find_panels(img: np.ndarray) -> list[tuple[int, int, int, int]]:
    """Return list of (x, y, w, h) panels sorted top-to-bottom, left-to-right."""
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Spiral / desk margins: focus on inner content
    y0, y1 = int(h * 0.06), int(h * 0.96)
    x0, x1 = int(w * 0.04), int(w * 0.96)
    roi = gray[y0:y1, x0:x1]
    blur = cv2.GaussianBlur(roi, (5, 5), 0)
    # Frames are light borders around dark monument cards
    edges = cv2.Canny(blur, 40, 120)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=2)
    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    rh, rw = roi.shape[:2]
    area_min = rh * rw * 0.06
    area_max = rh * rw * 0.55
    for c in cnts:
        x, y, bw, bh = cv2.boundingRect(c)
        area = bw * bh
        if area < area_min or area > area_max:
            continue
        ar = bw / float(bh)
        if ar < 0.55 or ar > 2.2:
            continue
        # absolute coords
        boxes.append((x + x0, y + y0, bw, bh))

    if len(boxes) < 2:
        return grid_fallback(img)

    # NMS-ish: drop heavily overlapping boxes
    boxes = sorted(boxes, key=lambda b: b[2] * b[3], reverse=True)
    kept = []
    for b in boxes:
        x, y, bw, bh = b
        ok = True
        for kx, ky, kw, kh in kept:
            ix0 = max(x, kx)
            iy0 = max(y, ky)
            ix1 = min(x + bw, kx + kw)
            iy1 = min(y + bh, ky + kh)
            inter = max(0, ix1 - ix0) * max(0, iy1 - iy0)
            if inter > 0.5 * min(bw * bh, kw * kh):
                ok = False
                break
        if ok:
            kept.append(b)
        if len(kept) >= 4:
            break

    if len(kept) < 2:
        return grid_fallback(img)

    # sort reading order
    kept.sort(key=lambda b: (b[1] // max(1, int(h * 0.12)), b[0]))
    return kept[:4]


def grid_fallback(img: np.ndarray) -> list[tuple[int, int, int, int]]:
    h, w = img.shape[:2]
    # Detect whether 2 stacked or 2x2 by comparing mid horizontal gutter brightness variance
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mid_band = gray[int(h * 0.45) : int(h * 0.55), int(w * 0.15) : int(w * 0.85)]
    # If mid band is bright (page paper between two rows), likely 2x2 or 1x2
    mean = float(np.mean(mid_band))
    top = int(h * 0.08)
    bot = int(h * 0.94)
    left = int(w * 0.07)
    right = int(w * 0.93)
    mid_y = (top + bot) // 2
    mid_x = (left + right) // 2
    gap = int(h * 0.012)
    gapx = int(w * 0.012)

    # Check vertical gutter existence (two columns)
    vert_gutter = gray[top:bot, mid_x - 4 : mid_x + 4]
    has_cols = float(np.mean(vert_gutter)) > mean * 0.85 and float(np.std(vert_gutter)) < 45

    if has_cols and mean > 90:
        # 2x2
        return [
            (left, top, mid_x - left - gapx, mid_y - top - gap),
            (mid_x + gapx, top, right - mid_x - gapx, mid_y - top - gap),
            (left, mid_y + gap, mid_x - left - gapx, bot - mid_y - gap),
            (mid_x + gapx, mid_y + gap, right - mid_x - gapx, bot - mid_y - gap),
        ]
    # 2 stacked
    return [
        (left, top, right - left, mid_y - top - gap),
        (left, mid_y + gap, right - left, bot - mid_y - gap),
    ]


def read_number_near(img: np.ndarray, box: tuple[int, int, int, int]) -> int | None:
    """Heuristic: look at bottom-right badge of panel for digits via simple template-less OCR-ish."""
    x, y, bw, bh = box
    # badge region
    rx0 = x + int(bw * 0.72)
    ry0 = y + int(bh * 0.82)
    rx1 = x + bw - 2
    ry1 = y + bh - 2
    if rx1 <= rx0 or ry1 <= ry0:
        return None
    crop = img[ry0:ry1, rx0:rx1]
    if crop.size == 0:
        return None
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    # dark badge with white digits -> invert
    _, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Prefer darker badge: if mostly dark, invert for white digits
    if np.mean(thr) > 127:
        thr = 255 - thr
    # Upscale for readability if we had tesseract; without it return None
    return None


def imread_unicode(path: Path) -> np.ndarray | None:
    """cv2.imread fails on non-ASCII Windows paths — use fromfile."""
    data = np.fromfile(str(path), dtype=np.uint8)
    if data.size == 0:
        return None
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return img


def imwrite_unicode(path: Path, img: np.ndarray, quality: int = 88) -> None:
    ok, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not ok:
        raise RuntimeError(f"encode failed: {path}")
    buf.tofile(str(path))


def process_all() -> list[dict]:
    items = []
    pages = sorted(ROOT.glob("page-*.png"))
    seq = 1
    for page in pages:
        img = imread_unicode(page)
        if img is None:
            print("skip unreadable", page.name)
            continue
        panels = find_panels(img)
        page_id = page.stem.replace("page-", "")
        for i, (x, y, bw, bh) in enumerate(panels):
            # pad inward slightly to drop white frame
            pad = int(min(bw, bh) * 0.03)
            x1 = max(0, x + pad)
            y1 = max(0, y + pad)
            x2 = min(img.shape[1], x + bw - pad)
            y2 = min(img.shape[0], y + bh - pad)
            tile = img[y1:y2, x1:x2]
            if tile.size == 0:
                continue
            # enhance mild contrast
            lab = cv2.cvtColor(tile, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l2 = clahe.apply(l)
            tile = cv2.cvtColor(cv2.merge([l2, a, b]), cv2.COLOR_LAB2BGR)
            # resize max side 900
            th, tw = tile.shape[:2]
            scale = 900 / max(th, tw)
            if scale < 1:
                tile = cv2.resize(tile, (int(tw * scale), int(th * scale)), interpolation=cv2.INTER_AREA)
            num = seq
            fname = f"monument-{num:03d}.jpg"
            out_path = OUT / fname
            imwrite_unicode(out_path, tile)
            items.append(
                {
                    "id": f"m{num}",
                    "num": num,
                    "file": f"images/catalog/monuments/items/{fname}",
                    "page": page_id,
                    "slot": i + 1,
                }
            )
            seq += 1
    (OUT / "index.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"pages={len(pages)} items={len(items)} -> {OUT}")
    return items


if __name__ == "__main__":
    process_all()
