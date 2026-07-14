#!/usr/bin/env python3
"""Batch-render branded "Just Listed" Shorts for ALL of Carrie's active listings.

Feed-driven, end-to-end: queries her public Realtor.com agent feed (metadata +
full photo gallery per listing), downloads each gallery, and renders a silent
9:16 Short via build_listing_video.render_video. Silent by design (she adds
licensed music in-app; or --music per listing later).

    python build/social/batch_listing_videos.py
    python build/social/batch_listing_videos.py --photos 12 --min-photos 4
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_listing_photos import GALLERY_ROOT, HEADERS, URL, FULFILLMENT_ID, upsize  # noqa: E402
from build_listing_video import render_video, OUT_DIR  # noqa: E402

QUERY = {
    "operationName": "AgentPropertyListing",
    "variables": {"query": {"status": ["for_sale"], "fulfillment_id": FULFILLMENT_ID},
                  "limit": 100, "offset": 0, "size": "WEB_PDP_CAROUSEL"},
    "query": ("query AgentPropertyListing($query: HomeSearchCriteria!, $limit: Int!,"
              " $size: SizeStrategy, $offset: Int) { home_search(query: $query,"
              " limit: $limit, offset: $offset) { results { property_id list_price"
              " description { beds baths_consolidated sqft }"
              " location { address { line city } } photos(size: $size) { href } } } }"),
}


def slugify(line: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (line or "").lower()).strip("-")
    return s or "listing"


def money(n) -> str:
    try:
        return f"${int(n):,}"
    except (TypeError, ValueError):
        return ""


def download_gallery(slug: str, hrefs: list, count: int) -> list:
    out_dir = GALLERY_ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, href in enumerate(hrefs[:count], 1):
        dst = out_dir / f"{i:02d}.jpg"
        for url in (upsize(href), href):
            try:
                req = urllib.request.Request(url, headers={"user-agent": HEADERS["user-agent"]})
                dst.write_bytes(urllib.request.urlopen(req, timeout=25).read())
                paths.append(dst)
                break
            except Exception:
                continue
    return paths


def main(count: int, min_photos: int) -> None:
    req = urllib.request.Request(URL, data=json.dumps(QUERY).encode(), headers=HEADERS)
    raw = json.load(urllib.request.urlopen(req, timeout=30))
    if raw.get("errors"):
        raise SystemExit("GraphQL errors: " + json.dumps(raw["errors"])[:500])
    results = (raw.get("data") or {}).get("home_search", {}).get("results", []) or []
    print(f"Feed: {len(results)} active listing(s).\n")

    rendered, skipped = [], []
    for r in results:
        line = ((r.get("location") or {}).get("address") or {}).get("line") or ""
        city = ((r.get("location") or {}).get("address") or {}).get("city") or "Lafayette"
        desc = r.get("description") or {}
        slug = slugify(line)
        hrefs = [p.get("href") for p in (r.get("photos") or []) if p.get("href")]
        if len(hrefs) < min_photos:
            print(f"SKIP {slug}: only {len(hrefs)} photo(s) (< {min_photos})")
            skipped.append((slug, len(hrefs)))
            continue
        meta = {
            "price": money(r.get("list_price")),
            "address": line,
            "city": f"{city}, LA",
            "beds": desc.get("beds") or "",
            "baths": desc.get("baths_consolidated") or "",
            "sqft": int(desc.get("sqft") or 0),
        }
        print(f"=== {slug}  ({len(hrefs)} photos, {meta['price']}) ===")
        photos = download_gallery(slug, hrefs, count)
        if not photos:
            print(f"SKIP {slug}: gallery download failed")
            skipped.append((slug, 0))
            continue
        try:
            render_video(slug, meta, photos, is_gallery=len(photos) > 1, music_arg=None)
            rendered.append(slug)
        except Exception as e:
            print(f"ERROR {slug}: {e}")
            skipped.append((slug, len(photos)))
        print()

    # Manifest for the studio video gallery — scan the dir so it reflects ALL
    # rendered videos, not just this run.
    def _title(s):
        return re.sub(r"\b(\w)", lambda m: m.group(1).upper(), s.replace("-", " "))
    vids = [{"slug": p.name[:-len("-short.mp4")], "title": _title(p.name[:-len("-short.mp4")]), "file": p.name}
            for p in sorted(OUT_DIR.glob("*-short.mp4"))]
    (OUT_DIR / "index.json").write_text(json.dumps({"videos": vids}, indent=2), encoding="utf-8")

    print("=" * 60)
    print(f"RENDERED {len(rendered)}: {', '.join(rendered)}")
    if skipped:
        print(f"SKIPPED {len(skipped)}: {', '.join(f'{s}({n})' for s, n in skipped)}")
    print(f"Manifest: {len(vids)} videos -> {OUT_DIR/'index.json'}")
    print(f"Output: site/studio/packages/videos/<slug>-short.mp4 (silent — add music in-app)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--photos", type=int, default=14, help="max photos per listing")
    ap.add_argument("--min-photos", type=int, default=4, help="skip listings with fewer photos")
    a = ap.parse_args()
    main(a.photos, a.min_photos)
