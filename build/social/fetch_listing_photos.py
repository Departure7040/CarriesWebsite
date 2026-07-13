#!/usr/bin/env python3
"""Fetch a listing's full photo gallery from Carrie's public Realtor.com feed.

The site feed (server.py /api/listings) only pulls each listing's HERO photo.
A real walkthrough video needs the interior shots too, so this queries the same
AgentPropertyListing GraphQL with the `photos` list included and downloads up to
N photos for one listing (matched by street line) into:

    site/assets/img/listings/gallery/<slug>/01.jpg, 02.jpg, ...

These are Carrie's OWN MLS listing photos, already public on her Realtor.com
profile — the same source as the hero photos already in the repo. Used only to
build her branded listing videos.

    python build/social/fetch_listing_photos.py 101-rio-ridge-dr "101 Rio Ridge Dr" 14
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
GALLERY_ROOT = REPO / "site" / "assets" / "img" / "listings" / "gallery"

FULFILLMENT_ID = "2202597"
URL = "https://www.realtor.com/frontdoor/graphql"
HEADERS = {
    "accept": "*/*", "content-type": "application/json",
    "origin": "https://www.realtor.com",
    "referer": "https://www.realtor.com/realestateagents/567985a6bb954c0100686dd4",
    "rdc-client-name": "agent-branding-profile", "rdc-client-version": "0.0.795",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                   " (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"),
}
QUERY = {
    "operationName": "AgentPropertyListing",
    "variables": {"query": {"status": ["for_sale"], "fulfillment_id": FULFILLMENT_ID},
                  "limit": 100, "offset": 0, "size": "WEB_PDP_CAROUSEL"},
    "query": ("query AgentPropertyListing($query: HomeSearchCriteria!, $limit: Int!,"
              " $size: SizeStrategy, $offset: Int) { home_search(query: $query,"
              " limit: $limit, offset: $offset) { results { property_id"
              " location { address { line } } photos(size: $size) { href } } } }"),
}


def upsize(href: str) -> str:
    """Realtor.com image URLs carry a size token like -w1024_h768 (or -m###).
    Bump to a larger width so the photo is crisp when scaled to a 1080-wide frame."""
    href = re.sub(r"-w\d+_h\d+", "-w1536_h1152", href)
    href = re.sub(r"-m(\d+)s\.", "-w1536_h1152.", href)  # some use -m2400s.jpg style
    return href


def fetch(slug: str, line_match: str, count: int) -> None:
    req = urllib.request.Request(URL, data=json.dumps(QUERY).encode(), headers=HEADERS)
    raw = json.load(urllib.request.urlopen(req, timeout=25))
    if raw.get("errors"):
        raise SystemExit("GraphQL errors: " + json.dumps(raw["errors"])[:500])
    results = (raw.get("data") or {}).get("home_search", {}).get("results", []) or []

    target = None
    want = line_match.strip().lower()
    for r in results:
        line = ((r.get("location") or {}).get("address") or {}).get("line") or ""
        if line.strip().lower() == want or want in line.strip().lower():
            target = r
            break
    if not target:
        avail = [((r.get("location") or {}).get("address") or {}).get("line") for r in results]
        raise SystemExit(f"No listing matched '{line_match}'. Available: {avail}")

    photos = [p.get("href") for p in (target.get("photos") or []) if p.get("href")]
    if not photos:
        raise SystemExit("Listing matched but has no photos in the feed.")

    out_dir = GALLERY_ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    take = photos[:count]
    print(f"{line_match}: {len(photos)} photos available; downloading {len(take)} -> {out_dir}")
    for i, href in enumerate(take, 1):
        url = upsize(href)
        dst = out_dir / f"{i:02d}.jpg"
        try:
            req = urllib.request.Request(url, headers={"user-agent": HEADERS["user-agent"]})
            data = urllib.request.urlopen(req, timeout=25).read()
        except Exception:  # fall back to the original (un-upsized) href
            req = urllib.request.Request(href, headers={"user-agent": HEADERS["user-agent"]})
            data = urllib.request.urlopen(req, timeout=25).read()
        dst.write_bytes(data)
        print(f"  {dst.name}  ({len(data)/1024:.0f} KB)")
    print(f"Done. {len(take)} photos in {out_dir}")


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "101-rio-ridge-dr"
    line = sys.argv[2] if len(sys.argv) > 2 else "101 Rio Ridge Dr"
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 14
    fetch(slug, line, count)
