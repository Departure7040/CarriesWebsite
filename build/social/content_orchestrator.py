#!/usr/bin/env python3
"""
content_orchestrator.py — the "new listing -> content package" pipeline for
Carrie Billeaud's Tier-1 social content engine (see
implementation/social_agent_design.md).

WHAT IT DOES (the human-in-the-loop wedge, NOT auto-publish):
  1. Reads her listing feed (data/realtor_active_listings_snapshot_*.json, the
     same Realtor.com shape the site's /api/listings proxy serves; --live can
     fetch the running proxy instead).
  2. Detects listings to process. For the demo it treats every current active
     listing; a simple seen-ids file (out/packages/.seen_ids.json) records what
     has already been packaged so a real run only fires on NEW listings. See
     `select_listings()` for exactly where 'new-since-last-run' diffing lives.
  3. For each listing it assembles a CONTENT PACKAGE under
     out/packages/<slug>/ :
        square.png       branded 1080x1080 feed graphic  (generate_graphics.py)
        story.png        branded 1080x1920 story graphic  (generate_graphics.py)
        captions.json    the multi-platform caption package (IG/FB/TikTok/YT)
        ready-to-post.md  human-readable: each platform's caption + which image
  4. Writes out/packages/index.json — the manifest the content-studio.html
     approval page loads.

CAPTIONS: mirrors functions/api/generate-content.js exactly (same MODEL, same
SYSTEM_PROMPT compliance artifact, same emit_content_package tool) but over
urllib so the orchestrator is a standalone script. Runnable WITHOUT a key: set
CONTENT_MOCK=1 (or just omit ANTHROPIC_API_KEY) and it emits a facts-only,
listing-specific mock package — nothing is invented, compliance holds in mock too.

GRAPHICS need NO key (pure Playwright render). Captions need ANTHROPIC_API_KEY
unless in mock mode.

RE-RUNNABLE. Compliance is enforced by the shared SYSTEM_PROMPT (facts only, no
steering / fair-housing-sensitive language, no unverified stats, no guarantees).

  python build/social/content_orchestrator.py            # mock unless key set
  CONTENT_MOCK=1 python build/social/content_orchestrator.py
  python build/social/content_orchestrator.py --live     # fetch /api/listings
  python build/social/content_orchestrator.py --all      # ignore seen-ids diff
"""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

# Import the graphic generator as a module (same dir).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_graphics import generate_graphics, _slugify  # noqa: E402

REPO = Path(__file__).resolve().parent.parent.parent
SOCIAL_DIR = REPO / "build" / "social"
OUT_DIR = SOCIAL_DIR / "out"
# Publish packages into the SERVED web root so the content studio (a real
# subsite at /studio/) can load them through the tunnel.
PACKAGES_DIR = REPO / "site" / "studio" / "packages"
SEEN_FILE = PACKAGES_DIR / ".seen_ids.json"
DATA_DIR = REPO / "data"

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"        # mirrors generate-content.js
MAX_TOKENS = 2048
LIVE_LISTINGS_URL = "http://127.0.0.1:8788/api/listings"  # local wrangler proxy

# --- Compliance artifact: kept identical to functions/api/generate-content.js /
#     _content_system_prompt.md. Any edit here is a compliance change.
SYSTEM_PROMPT = (
    "You are the social-media content writer for Carrie Billeaud, a REALTOR with "
    "eXp Realty serving Lafayette and the surrounding Acadiana communities of "
    "Youngsville, Broussard, Carencro, Scott, Maurice and Milton, Louisiana. You "
    "write ready-to-approve captions and scripts for her personal social accounts "
    "(Instagram, Facebook, TikTok, YouTube). Carrie reviews, edits, and posts "
    "everything herself — you draft, she approves.\n\n"
    "BRAND VOICE: Warm, local, and genuinely welcoming, with a classy, high-end "
    "luxury register (her direction). Aspirational but grounded; never hypey, never "
    "salesy, never clickbait. Editorial and elegant. Light, tasteful local color "
    "(Lafayette / Acadiana) is welcome. Avoid exclamation-point spam and ALL-CAPS.\n\n"
    "FACTS-ONLY (hard rule): Use only the facts provided in the listing data "
    "(address, city, price, beds, baths, sqft, status, url). Do NOT invent, infer, "
    "or embellish amenities, finishes, lot features, views, schools, or anything not "
    "given. If a field is missing, omit it. Never fabricate a price, square footage, "
    "or availability. Format naturally but never change a number.\n\n"
    "COMPLIANCE — NON-NEGOTIABLE:\n"
    "1. No steering / no fair-housing-sensitive language. Never use or imply "
    "\"family-friendly,\" \"safe\"/\"unsafe,\" \"good/bad/great neighborhood,\" "
    "\"good schools,\" \"up-and-coming,\" crime, or any characterization tied to a "
    "protected class. Sell the home's listed facts, never the demographic.\n"
    "2. No unverified stats as fact (sales volume, days-on-market, appreciation, "
    "\"#1 agent,\" home-value estimates) unless it is in the listing data.\n"
    "3. No guarantees or predictions (sale price, timeline, ROI, \"will sell "
    "fast,\" \"great investment\"). No mortgage rates or approval promises.\n"
    "4. No invented amenities. Only features present in the listing data.\n"
    "5. Keep her real NAP (Carrie Billeaud, REALTOR, eXp Realty, Acadiana). Keep "
    "any call-to-action a soft, tasteful invitation — never a hard sell.\n\n"
    "OUTPUT: Return the content package by calling the emit_content_package tool "
    "with every field populated. Do not return prose outside the tool call."
)

# --- The single output tool (mirror of generate-content.js EMIT_TOOL).
EMIT_TOOL = {
    "name": "emit_content_package",
    "description": (
        "Emit the finished multi-platform social content package for the given "
        "listing. Every field must obey the facts-only and fair-housing rules."
    ),
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "instagram": {
                "type": "object", "additionalProperties": False,
                "properties": {
                    "caption": {"type": "string"},
                    "hashtags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["caption", "hashtags"],
            },
            "facebook": {
                "type": "object", "additionalProperties": False,
                "properties": {"caption": {"type": "string"}},
                "required": ["caption"],
            },
            "tiktok": {
                "type": "object", "additionalProperties": False,
                "properties": {"script": {"type": "string"}, "hook": {"type": "string"}},
                "required": ["script", "hook"],
            },
            "youtube": {
                "type": "object", "additionalProperties": False,
                "properties": {"title": {"type": "string"}, "description": {"type": "string"}},
                "required": ["title", "description"],
            },
            "story_text": {"type": "string"},
            "hooks": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["instagram", "facebook", "tiktok", "youtube", "story_text", "hooks"],
    },
    "strict": True,
}


# --------------------------------------------------------------------------- #
# Feed loading + normalization
# --------------------------------------------------------------------------- #
def _latest_snapshot() -> Path:
    snaps = sorted(DATA_DIR.glob("realtor_active_listings_snapshot_*.json"))
    if not snaps:
        raise SystemExit("No listing snapshot found in data/.")
    return snaps[-1]


def load_feed(live: bool) -> list[dict]:
    """Return the raw Realtor.com-shaped results array (snapshot or live proxy)."""
    if live:
        with urllib.request.urlopen(LIVE_LISTINGS_URL, timeout=20) as r:  # noqa: S310
            raw = json.loads(r.read().decode("utf-8"))
    else:
        raw = json.loads(_latest_snapshot().read_text(encoding="utf-8"))
    return raw.get("data", {}).get("home_search", {}).get("results", []) or []


def format_price(v) -> str:
    try:
        return "${:,}".format(int(v))
    except (TypeError, ValueError):
        return str(v or "")


def normalize(raw: dict) -> dict | None:
    """Map one Realtor.com result to the flat listing dict the generators want.
    Returns None if it lacks the residential facts a listing graphic needs."""
    loc = (raw.get("location") or {}).get("address") or {}
    desc = raw.get("description") or {}
    line = loc.get("line")
    city = loc.get("city")
    photo = (raw.get("primary_photo") or {}).get("href")
    beds, baths, sqft = desc.get("beds"), desc.get("baths_consolidated"), desc.get("sqft")
    if not (line and city and photo):
        return None
    # A branded listing graphic needs beds/baths/sqft; land/lot rows (all null)
    # need a different template — skip with a note rather than fabricate specs.
    if beds is None or baths is None or sqft is None:
        return None
    state = loc.get("state_code") or "LA"
    slug = _slugify(line)
    # Prefer a local listing photo (offline-friendly, no network fetch); fall back
    # to the feed's primary_photo href, which generate_graphics downloads.
    local_photo = REPO / "site" / "assets" / "img" / "listings" / f"{slug}.jpg"
    return {
        "id": raw.get("property_id") or raw.get("listing_id") or slug,
        "slug": slug,
        "address": line,
        "city": f"{city}, {state}",
        "price": format_price(raw.get("list_price")),
        "beds": beds,
        "baths": baths,
        "sqft": sqft,
        "status": raw.get("status") or "for_sale",
        "url": raw.get("href") or "",
        "photo": str(local_photo) if local_photo.exists() else photo,
    }


# --------------------------------------------------------------------------- #
# New-listing diffing (the seen-ids file)
# --------------------------------------------------------------------------- #
def _load_seen() -> set[str]:
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()


def _save_seen(ids: set[str]) -> None:
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(sorted(ids), indent=2), encoding="utf-8")


def select_listings(listings: list[dict], process_all: bool) -> list[dict]:
    """THE 'new-since-last-run' DECISION POINT.

    In production the pipeline fires only for listings whose id is not in the
    seen-ids file (a new listing just hit her feed -> generate its package).
    For the demo, --all (or an empty seen file on first run) processes every
    current active listing so there is always something to review.
    """
    if process_all:
        return listings
    seen = _load_seen()
    fresh = [l for l in listings if l["id"] not in seen]
    # First run (nothing seen yet): package everything so the studio isn't empty.
    return fresh if seen else listings


# --------------------------------------------------------------------------- #
# Captions — real Anthropic call OR facts-only mock (mirrors generate-content.js)
# --------------------------------------------------------------------------- #
def build_brief(l: dict) -> str:
    rows = [
        ("Address", l["address"]), ("City", l["city"]), ("Price", l["price"]),
        ("Beds", l["beds"]), ("Baths", l["baths"]), ("SqFt", l["sqft"]),
        ("Status", l["status"]), ("Listing URL", l["url"]),
    ]
    return "\n".join(f"{k}: {v}" for k, v in rows if str(v).strip())


def mock_package(l: dict) -> dict:
    """Facts-only, listing-specific mock. Compliance holds: every field is built
    from the listing's own data — no invented amenities, no steering language."""
    city_short = l["city"].split(",")[0]
    specs = f"{l['beds']} bed / {l['baths']} bath"
    sqft = "{:,}".format(int(l["sqft"])) if str(l["sqft"]).replace(",", "").isdigit() else l["sqft"]
    price = l["price"]
    ig = (
        f"Just listed in {city_short} — {specs}, {sqft} sq ft, offered at {price}. "
        f"If this one speaks to you, I'd love to walk you through it. "
        f"Reach out to schedule a private showing.\n\n(Demo mode — sample content.)"
    )
    fb = (
        f"New on the market in {city_short}: {specs}, {sqft} sq ft, listed at {price}. "
        f"I'd be glad to show you around — send me a message to set up a time.\n\n"
        f"Carrie Billeaud, REALTOR · eXp Realty · Acadiana. (Demo mode.)"
    )
    tt = (
        f"Come take a look at this new listing in {city_short} — {l['beds']} bedrooms, "
        f"{l['baths']} baths, about {sqft} square feet, offered at {price}. "
        f"Message me to book a showing."
    )
    return {
        "instagram": {
            "caption": ig,
            "hashtags": [
                "#AcadianaHomes", "#" + city_short.replace(" ", "") + "LA",
                "#LafayetteRealEstate", "#JustListed", "#CarrieBilleaudRealtor", "#eXpRealty",
            ],
        },
        "facebook": {"caption": fb},
        "tiktok": {"script": tt, "hook": f"Just listed in {city_short}."},
        "youtube": {
            "title": f"Just Listed in {city_short}, LA — {specs}",
            "description": (
                f"A new listing in {city_short}: {specs}, {sqft} sq ft, offered at {price}. "
                f"Reach out to Carrie Billeaud, REALTOR with eXp Realty, to schedule a "
                f"showing. Demo mode — sample content."
            ),
        },
        "story_text": f"Just listed in {city_short} ✦ {specs}",
        "hooks": [
            f"Just listed in {city_short}.",
            f"{sqft} sq ft, new to market — {price}.",
            f"Your next chapter in Acadiana: {specs} in {city_short}.",
        ],
    }


def call_anthropic(api_key: str, brief: str) -> dict:
    body = json.dumps({
        "model": MODEL, "max_tokens": MAX_TOKENS, "system": SYSTEM_PROMPT,
        "tools": [EMIT_TOOL],
        "tool_choice": {"type": "tool", "name": "emit_content_package"},
        "messages": [{
            "role": "user",
            "content": f"Write the social content package for this listing. Use ONLY these facts:\n\n{brief}",
        }],
    }).encode("utf-8")
    req = urllib.request.Request(ANTHROPIC_URL, data=body, method="POST", headers={
        "x-api-key": api_key, "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310
        msg = json.loads(r.read().decode("utf-8"))
    block = next((b for b in msg.get("content", [])
                  if b.get("type") == "tool_use" and b.get("name") == "emit_content_package"), None)
    if not block:
        raise RuntimeError("no tool_use block in Anthropic response")
    pkg = block["input"]
    if isinstance(pkg, str):
        pkg = json.loads(pkg)
    return pkg


def generate_captions(l: dict) -> tuple[dict, bool]:
    """Return (package, used_mock)."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    force_mock = os.environ.get("CONTENT_MOCK") in ("1", "true")
    if force_mock or key is None:  # key is None narrows the type below
        return mock_package(l), True
    try:
        return call_anthropic(key, build_brief(l)), False
    except Exception as e:
        print(f"    ! caption API failed ({e}); falling back to mock", file=sys.stderr)
        return mock_package(l), True


# --------------------------------------------------------------------------- #
# Package assembly
# --------------------------------------------------------------------------- #
def ready_to_post_md(l: dict, pkg: dict, mock: bool) -> str:
    ig, fb, tt, yt = pkg["instagram"], pkg["facebook"], pkg["tiktok"], pkg["youtube"]
    tag = " _(demo mock content)_" if mock else ""
    hashtags = " ".join(ig["hashtags"])
    return f"""# Ready to post — {l['address']}, {l['city']}{tag}

**{l['price']} · {l['beds']} bed / {l['baths']} bath · {l['sqft']} sq ft · {l['status']}**
Listing: {l['url']}

> Review, tweak if you like, then copy the caption and post with the graphic.
> Publishing stays manual (or hand to an aggregator) — nothing auto-posts.

---

## Instagram — use `square.png`
{ig['caption']}

{hashtags}

---

## Facebook — use `square.png`
{fb['caption']}

---

## TikTok / Reels — use `story.png`
**Hook (first 1-2s):** {tt['hook']}

{tt['script']}

---

## YouTube — use `story.png` thumbnail / `square.png`
**Title:** {yt['title']}

{yt['description']}

---

## Instagram / Facebook Story — use `story.png`
{pkg['story_text']}

## Alternate hooks
{chr(10).join('- ' + h for h in pkg['hooks'])}
"""


def process_listing(l: dict) -> dict:
    slug = l["slug"]
    pkg_dir = PACKAGES_DIR / slug
    pkg_dir.mkdir(parents=True, exist_ok=True)
    print(f"  [{slug}] rendering branded graphics...")
    square, story = generate_graphics(l, out_dir=pkg_dir)
    # generate_graphics writes <slug>-square.png; normalize to square.png/story.png.
    square_final, story_final = pkg_dir / "square.png", pkg_dir / "story.png"
    square.replace(square_final)
    story.replace(story_final)

    print(f"  [{slug}] generating captions...")
    pkg, mock = generate_captions(l)

    captions_path = pkg_dir / "captions.json"
    captions_path.write_text(json.dumps({
        "listing": {k: l[k] for k in ("slug", "address", "city", "price", "beds",
                                       "baths", "sqft", "status", "url")},
        "package": pkg,
        "mock": mock,
    }, indent=2), encoding="utf-8")

    (pkg_dir / "ready-to-post.md").write_text(ready_to_post_md(l, pkg, mock), encoding="utf-8")

    return {
        "slug": slug, "address": l["address"], "city": l["city"], "price": l["price"],
        "beds": l["beds"], "baths": l["baths"], "sqft": l["sqft"], "url": l["url"],
        "square": f"{slug}/square.png", "story": f"{slug}/story.png",
        "package": pkg, "mock": mock,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="New-listing -> social content package pipeline.")
    ap.add_argument("--live", action="store_true", help="fetch the running /api/listings proxy instead of the snapshot")
    ap.add_argument("--all", action="store_true", help="ignore the seen-ids diff and package every active listing")
    ap.add_argument("--limit", type=int, default=0, help="cap number of listings (0 = no cap)")
    args = ap.parse_args()

    print("Loading listing feed...")
    raw_results = load_feed(args.live)
    listings = [n for n in (normalize(r) for r in raw_results) if n]
    skipped = len(raw_results) - len(listings)
    print(f"  {len(listings)} residential listings ready ({skipped} skipped: land/lot or missing facts).")

    todo = select_listings(listings, args.all)
    if args.limit:
        todo = todo[: args.limit]
    if not todo:
        print("No new listings since last run. (Use --all to repackage everything.)")
        return
    print(f"Packaging {len(todo)} listing(s) -> {PACKAGES_DIR}\n")

    manifest = []
    seen = _load_seen()
    for l in todo:
        try:
            manifest.append(process_listing(l))
            seen.add(l["id"])
        except Exception as e:
            print(f"  ! {l['slug']} failed: {e}", file=sys.stderr)

    # Merge with any previously-built packages so the studio shows the full set.
    index_path = PACKAGES_DIR / "index.json"
    existing = []
    if index_path.exists():
        try:
            existing = json.loads(index_path.read_text(encoding="utf-8")).get("packages", [])
        except Exception:
            existing = []
    by_slug = {p["slug"]: p for p in existing}
    for p in manifest:
        by_slug[p["slug"]] = p
    packages = sorted(by_slug.values(), key=lambda p: p["slug"])

    index_path.write_text(json.dumps({
        "generated": "2026-07-12", "count": len(packages), "packages": packages,
    }, indent=2), encoding="utf-8")
    _save_seen(seen)

    print("\n" + "=" * 60)
    print(f"DONE. {len(manifest)} package(s) this run, {len(packages)} total.")
    print(f"Manifest: {index_path}")
    for p in manifest:
        tag = " (mock captions)" if p["mock"] else ""
        print(f"  - {p['slug']}: {p['address']}, {p['city']} — {p['price']}{tag}")
        print(f"      {PACKAGES_DIR / p['slug']}")
    print("Review/approve at /studio/ (site/studio/index.html).")
    print("=" * 60)


if __name__ == "__main__":
    main()
