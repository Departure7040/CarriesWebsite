#!/usr/bin/env python3
"""
new_estate.py — ONE command to stand up a single-property estate microsite.

Given a listing (by street address, matched in Carrie's Realtor.com feed), this:
  1. Fetches the listing FACTS from the Realtor.com agent feed (price, beds, baths,
     sqft, lot, year, garage, type, coords, listing URL) + best-effort MLS #.
  2. Downloads ALL its photos, de-duplicates them (md5), renumbers 01..N.
  3. Writes the COMPLIANCE block deterministically (LREC broker disclosure +
     Equal Housing) — identical and safe every time, no AI.
  4. (AI, optional) Writes marketing COPY + per-photo CAPTIONS grounded in the real
     facts + what the photos actually show — via local Claude Code (`claude -p`),
     which uses your logged-in claude.ai subscription (NO API key, no metering).
     If the `claude` CLI isn't found it falls back to an honest facts-only draft.
  5. Assembles data/estates/<slug>.json.
  6. Runs build_estate.py -> site/estates/<slug>/index.html.
  7. Prints the local + tunnel URL.

Usage:
    python build/estates/new_estate.py --address "101 Rio Ridge Dr"
    python build/estates/new_estate.py --all                 # every active listing
    python build/estates/new_estate.py --address "..." --no-content   # skip AI step
    python build/estates/new_estate.py --address "..." --no-photos     # reuse existing gallery

Requires the `claude` CLI on PATH and logged in (claude.ai subscription) for the AI
step. Any ANTHROPIC_API_KEY in the environment is intentionally dropped for those
calls so they bill against the subscription, not a metered key.

Content models (passed to `claude -p --model`):
    --model-copy     default opus    (marketing prose — strong)
    --model-caption  default haiku   (per-photo captions — fast/cheap)

Standard library only (urllib, json, hashlib, concurrent.futures, subprocess, shutil).
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GALLERY_ROOT = ROOT / "site" / "assets" / "img" / "listings" / "gallery"
DATA_DIR = ROOT / "data" / "estates"
VIDEO_DIR = ROOT / "site" / "studio" / "packages" / "videos"
BUILDER = ROOT / "build" / "estates" / "build_estate.py"

# ---- Carrie / eXp defaults (override-able via CLI later if needed) ----
AGENT = {
    "name_title": "Carrie Billeaud, REALTOR®",
    "brokerage": "eXp Realty",
    "phone": "337-258-5379",
    "phone_tel": "3372585379",
    "headshot": "/assets/img/carrie-headshot-gbp.webp",
}
FULFILLMENT_ID = "2202597"
GRAPHQL = "https://www.realtor.com/frontdoor/graphql"
HEADERS = {
    "accept": "*/*", "content-type": "application/json",
    "origin": "https://www.realtor.com",
    "referer": "https://www.realtor.com/realestateagents/567985a6bb954c0100686dd4",
    "rdc-client-name": "agent-branding-profile", "rdc-client-version": "0.0.795",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                   " (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"),
}
QUERY = ("query AgentPropertyListing($query: HomeSearchCriteria!, $limit: Int!,"
         " $size: SizeStrategy, $offset: Int){ home_search(query:$query, limit:$limit,"
         " offset:$offset){ results { property_id listing_id permalink href list_price"
         " status location { address { line city state_code postal_code"
         " coordinate { lat lon } } } description { type sub_type beds baths baths_full"
         " baths_half sqft lot_sqft year_built garage } photos(size:$size){ href } } } }")

STATE_NAMES = {"LA": "Louisiana", "TX": "Texas", "MS": "Mississippi", "AL": "Alabama",
               "AR": "Arkansas", "FL": "Florida", "GA": "Georgia", "TN": "Tennessee",
               "OK": "Oklahoma"}
SUFFIX = {"Dr": "Drive", "St": "Street", "Ave": "Avenue", "Rd": "Road", "Ln": "Lane",
          "Ct": "Court", "Cir": "Circle", "Blvd": "Boulevard", "Pl": "Place",
          "Trl": "Trail", "Ter": "Terrace", "Pkwy": "Parkway", "Hwy": "Highway"}
STREET_TYPES = set(SUFFIX) | set(SUFFIX.values()) | {"Way", "Loop", "Run", "Row", "Walk"}


# --------------------------------------------------------------------------- #
# feed + facts
# --------------------------------------------------------------------------- #
def fetch_feed():
    body = {"operationName": "AgentPropertyListing",
            "variables": {"query": {"status": ["for_sale"], "fulfillment_id": FULFILLMENT_ID},
                          "limit": 100, "offset": 0, "size": "WEB_PDP_CAROUSEL"},
            "query": QUERY}
    req = urllib.request.Request(GRAPHQL, data=json.dumps(body).encode(), headers=HEADERS)
    raw = json.load(urllib.request.urlopen(req, timeout=30))
    if raw.get("errors"):
        raise SystemExit("GraphQL errors: " + json.dumps(raw["errors"])[:600])
    return (raw.get("data") or {}).get("home_search", {}).get("results", []) or []


def slugify(line):
    s = re.sub(r"[^a-z0-9]+", "-", line.lower()).strip("-")
    return s


def expand_address(line):
    parts = line.split()
    if parts and parts[-1] in SUFFIX:
        parts[-1] = SUFFIX[parts[-1]]
    return " ".join(parts)


def wordmark_of(line):
    """'101 Rio Ridge Dr' -> '101 Rio Ridge' (drop trailing street-type)."""
    parts = line.split()
    if len(parts) > 2 and parts[-1] in STREET_TYPES:
        parts = parts[:-1]
    return " ".join(parts)


def baths_display(full, half):
    full = full or 0
    if not half:
        return str(full)
    return "%d.5%s" % (full, "+" if half > 1 else "")


def acres(lot_sqft):
    if not lot_sqft:
        return ""
    a = lot_sqft / 43560.0
    s = ("%.2f" % a).rstrip("0").rstrip(".")
    return "%s %s" % (s, "acre" if a < 1 else "acres")


def get_mls(href):
    """Best-effort: scrape the listing page for the RAAMLS number."""
    try:
        req = urllib.request.Request(href, headers={"user-agent": HEADERS["user-agent"]})
        html = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
    except Exception:
        return ""
    m = re.search(r"MLS\s*#?\s*(\d{6,})", html)
    return m.group(1) if m else ""


def derive_facts(r, mls=""):
    loc = (r.get("location") or {}).get("address") or {}
    coord = loc.get("coordinate") or {}
    d = r.get("description") or {}
    price = r.get("list_price")
    year = d.get("year_built")
    tmap = {"single_family": "Single-Family", "condo": "Condominium",
            "townhome": "Townhome", "multi_family": "Multi-Family",
            "land": "Land", "mobile": "Mobile / Manufactured"}
    type_short = tmap.get(d.get("type") or "", (d.get("type") or "Residential").replace("_", " ").title())
    new_con = bool(year) and year >= 2023
    garage = d.get("garage")
    return {
        "address": loc.get("line", ""),
        "city": loc.get("city", ""),
        "state": loc.get("state_code", ""),
        "zip": loc.get("postal_code", ""),
        "price": "${:,}".format(price) if price else "",
        "price_num": price,
        "status": "For Sale" if r.get("status") == "for_sale" else (r.get("status") or "").replace("_", " ").title(),
        "beds": d.get("beds"),
        "baths": baths_display(d.get("baths_full"), d.get("baths_half")),
        "sqft": "{:,}".format(d["sqft"]) if d.get("sqft") else "",
        "lot": acres(d.get("lot_sqft")),
        "year_built": year,
        "garage": ("%d %s" % (garage, "car" if garage == 1 else "cars")) if garage else "",
        "type_short": type_short,
        "property_type": ("%s (new construction, %s)" % (type_short, year)) if new_con else type_short,
        "mls": mls,
        "realtor_url": r.get("href", ""),
        "lat": coord.get("lat"),
        "lon": coord.get("lon"),
        "_new_construction": new_con,
    }


# --------------------------------------------------------------------------- #
# photos
# --------------------------------------------------------------------------- #
def upsize(href):
    href = re.sub(r"-w\d+_h\d+", "-w1536_h1152", href)
    href = re.sub(r"-m(\d+)s\.", "-w1536_h1152.", href)
    return href


def download_photos(slug, photo_hrefs, maxn):
    out_dir = GALLERY_ROOT / slug
    tmp = GALLERY_ROOT / (slug + "-dl")
    if tmp.exists():
        for f in tmp.glob("*.jpg"):
            f.unlink()
    tmp.mkdir(parents=True, exist_ok=True)
    seen, kept = set(), []
    for href in photo_hrefs[:maxn]:
        url = upsize(href)
        try:
            req = urllib.request.Request(url, headers={"user-agent": HEADERS["user-agent"]})
            data = urllib.request.urlopen(req, timeout=25).read()
        except Exception:
            try:
                req = urllib.request.Request(href, headers={"user-agent": HEADERS["user-agent"]})
                data = urllib.request.urlopen(req, timeout=25).read()
            except Exception:
                continue
        h = hashlib.md5(data).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        kept.append(data)
    # write renumbered
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob("*.jpg"):
        f.unlink()
    for i, data in enumerate(kept, 1):
        (out_dir / ("%02d.jpg" % i)).write_bytes(data)
    for f in tmp.glob("*.jpg"):
        f.unlink()
    tmp.rmdir()
    return len(kept)


# --------------------------------------------------------------------------- #
# Content engine: local Claude Code (`claude -p`). Uses the logged-in claude.ai
# subscription (no API key, no metering). Runs from a neutral temp dir so the
# project's own hooks/context don't load into every call.
# --------------------------------------------------------------------------- #
def _claude_env():
    """Env with any ANTHROPIC_API_KEY (any casing) removed, so `claude` uses the
    claude.ai subscription login instead of a metered API key."""
    env = dict(os.environ)
    for k in [k for k in env if k.upper() == "ANTHROPIC_API_KEY"]:
        env.pop(k, None)
    return env


def _strip(text):
    text = text or ""
    text = re.sub(r"^\s*\[\d{4}-\d\d-\d\d \d\d:\d\d\]\s*", "", text)   # timestamp hook, if any
    text = text.strip()
    text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text)              # code fences
    return text.strip()


def claude_available():
    return shutil.which("claude") is not None


def claude_p(prompt, model, allow_read=False, timeout=300):
    exe = shutil.which("claude")
    if not exe:
        raise RuntimeError("`claude` CLI not found on PATH")
    cmd = [exe, "-p", "--output-format", "json", "--model", model]
    if allow_read:
        cmd += ["--allowedTools", "Read", "--permission-mode", "bypassPermissions"]
    proc = subprocess.run(cmd, input=prompt, cwd=tempfile.gettempdir(), env=_claude_env(),
                          capture_output=True, text=True, encoding="utf-8", timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError("claude -p failed: %s" % ((proc.stderr or proc.stdout) or "")[:300])
    obj = json.loads(proc.stdout)
    if obj.get("is_error"):
        raise RuntimeError("claude -p error: %s" % obj.get("result"))
    return _strip(obj.get("result", ""))


def _json_from(text):
    """Extract the first JSON value (array or object) from a model text response."""
    text = _strip(text)
    m = re.search(r"[\[{]", text)
    if not m:
        raise ValueError("no JSON found in model output")
    return json.loads(text[m.start():])


CAPTION_RULES = ("Describe ONLY what is visibly present (room, architecture, materials, fixtures, "
                 "pool/patio). Never describe or imply people or demographics. Never claim "
                 "'waterfront'/water views unless an actual pond, lake, or bayou is clearly visible. "
                 "Under 45 words each.")


def caption_batch(slug, files, model):
    out_dir = GALLERY_ROOT / slug
    listing = "\n".join("%s = %s" % (f, (out_dir / f).resolve().as_posix()) for f in files)
    prompt = ("Read each listing photo below and write accessible alt text. %s\n\n"
              "Return ONLY a JSON array (no prose, no code fence) of "
              "{\"file\":\"NN.jpg\",\"alt\":\"...\"} for every file, using these exact filenames.\n\n%s"
              % (CAPTION_RULES, listing))
    try:
        arr = _json_from(claude_p(prompt, model, allow_read=True))
        got = {d["file"]: d["alt"] for d in arr if d.get("file")}
    except Exception as e:
        sys.stderr.write("  caption batch failed (%s..): %s\n" % (files[0], e))
        got = {}
    return [{"file": f, "alt": got.get(f, "")} for f in files]


def caption_gallery(slug, count, model, batch=10):
    files = ["%02d.jpg" % i for i in range(1, count + 1)]
    batches = [files[i:i + batch] for i in range(0, len(files), batch)]
    results = {}
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for out in ex.map(lambda b: caption_batch(slug, b, model), batches):
            for d in out:
                results[d["file"]] = d["alt"]
    return [{"file": f, "alt": results.get(f, "")} for f in files]


COPY_SHAPE = ('{"hero_tagline": str, "overview_heading": str, "overview_paragraphs": [str] (2-3), '
              '"pull_quote": str, "feature_groups": [{"title": str, "items": [str]}] (exactly 3), '
              '"location_paragraphs": [str] (2-3), "location_points": [str] (6-8)}')


def generate_copy(facts, captions, model):
    caps = "\n".join("- %s" % c["alt"] for c in captions if c.get("alt"))
    prompt = (
        "You are a luxury real-estate copywriter. Editorial, restrained, atmospheric (Architectural "
        "Digest, not a hype flyer). HARD RULES: ground every factual claim in the FACTS and the PHOTO "
        "CAPTIONS below; never invent brands, materials, room counts, or measurements not supported by "
        "them. Never say 'waterfront' unless a caption mentions a pond/lake/bayou. FAIR HOUSING: "
        "location copy describes geography, amenities, and the property only — never demographics, "
        "never 'family/safe/good schools' or who the home 'suits'. Every feature_groups item must be "
        "supported by a caption or a fact. Match tone to the property; do not oversell a mid-market "
        "home as an ultra-luxury estate.\n\n"
        "FACTS:\n%s\n\nPHOTO CAPTIONS (what the photos actually show):\n%s\n\n"
        "Return ONLY a JSON object (no prose, no code fence) with exactly this shape:\n%s" % (
            json.dumps({k: v for k, v in facts.items() if not k.startswith("_")}, indent=2),
            caps or "(no captions available)", COPY_SHAPE))
    return _json_from(claude_p(prompt, model, allow_read=False, timeout=300))


# --------------------------------------------------------------------------- #
# deterministic copy scaffolding + compliance
# --------------------------------------------------------------------------- #
# Fixed section labels are tiered by price so a $175k home doesn't read like a
# $3.4M estate. The AI-written prose already self-calibrates; this is just the
# fixed chrome (eyebrows/headings/CTA phrasing).
LUX_THRESHOLD = 750000

_LABELS_LUX = {
    "overview_eyebrow": "The Residence",
    "details_eyebrow": "Property Details", "details_heading": "The Particulars",
    "features_eyebrow": "Features & Amenities", "features_heading": "Considered Throughout",
    "gallery_eyebrow": "Gallery", "gallery_heading": "A Closer Look",
    "video_eyebrow": "Cinematic Tour", "video_heading": "The Estate in Motion",
    "location_eyebrow": "Location", "location_heading": "The Setting",
    "cta_eyebrow": "Inquire", "cta_heading": "Arrange a Private Viewing",
}
_LABELS_STD = {
    "overview_eyebrow": "The Home",
    "details_eyebrow": "Property Details", "details_heading": "The Details",
    "features_eyebrow": "Features", "features_heading": "Features & Highlights",
    "gallery_eyebrow": "Gallery", "gallery_heading": "Photo Gallery",
    "video_eyebrow": "Tour", "video_heading": "Video Walkthrough",
    "location_eyebrow": "Location", "location_heading": "The Setting",
    "cta_eyebrow": "Contact", "cta_heading": "Schedule a Showing",
}


def section_labels(price_num):
    return dict(_LABELS_LUX if (price_num or 0) >= LUX_THRESHOLD else _LABELS_STD)


def cta_sub_text(price_num, addr_exp, agent_name, brokerage, phone):
    if (price_num or 0) >= LUX_THRESHOLD:
        return ("%s is shown by appointment. To walk the grounds and see the home for yourself, "
                "contact %s at %s — %s." % (addr_exp, agent_name, brokerage, phone))
    return ("%s is available to tour by appointment. To see the home for yourself, contact %s at "
            "%s — %s." % (addr_exp, agent_name, brokerage, phone))


def facts_only_features(facts):
    """Honest facts-only feature groups when no captions/AI are available."""
    grounds = []
    if facts["lot"]:
        grounds.append("Set on %s" % facts["lot"])
    if facts["garage"]:
        grounds.append("%s garage" % facts["garage"])
    residence = []
    if facts["_new_construction"]:
        residence.append("New %s construction" % facts["year_built"])
    if facts["sqft"]:
        residence.append("%s square feet" % facts["sqft"])
    if facts["beds"] is not None:
        residence.append("%s bedrooms, %s baths" % (facts["beds"], facts["baths"]))
    residence.append(facts["type_short"])
    groups = [{"title": "The Residence", "items": residence}]
    if grounds:
        groups.append({"title": "The Grounds", "items": grounds})
    return groups


def build_compliance(facts, agent):
    def cell(s):
        return s
    price_status = []
    if facts["status"]:
        price_status.append("<strong>%s</strong>" % cell(facts["status"]))
    if facts["price"]:
        price_status.append("<strong>%s</strong>" % cell(facts["price"]))
    mls_txt = (" &middot; MLS&nbsp;#%s" % facts["mls"]) if facts["mls"] else ""
    prop_line = ("%s, %s, %s %s &middot; %s.%s Information deemed reliable but not guaranteed; "
                 "buyer to verify all details. Price and availability subject to change without notice."
                 ) % (facts["address"], facts["city"], facts["state"], facts["zip"],
                      " &middot; ".join(price_status), mls_txt)
    eho_svg = ('<svg width="20" height="20" viewBox="0 0 24 24" role="img" '
               'aria-label="Equal Housing Opportunity" style="flex:0 0 auto;" fill="currentColor">'
               '<path d="M12 3 2 10h2v9h5v-5h6v5h5v-9h2L12 3zm0 4.2 1.6 1.2H10.4L12 7.2z"/></svg>')
    broker = (
        '  <footer class="listing-disclosure" role="contentinfo" style="font-size:0.85rem;'
        'line-height:1.55;padding:1.5rem 1.25rem;border-top:1px solid #ccc;">\n\n'
        '    <div class="disclosure-agent">\n'
        '      Presented by <strong>%s</strong>\n'
        '      &mdash; <span class="disclosure-brokerage">%s</span>\n'
        '      &middot; <a href="tel:%s">%s</a>\n'
        '    </div>\n\n'
        '    <div class="disclosure-broker" style="margin-top:0.5rem;">\n'
        '      Sponsoring / qualifying broker:\n'
        '      <strong><span data-broker="name">to be confirmed at launch</span></strong>\n'
        '      &middot; Broker phone:\n'
        '      <strong><a data-broker="phone" href="#">to be confirmed at launch</a></strong>\n'
        '    </div>\n\n'
        '    <div class="disclosure-jurisdiction" style="margin-top:0.5rem;">\n'
        '      Licensed by the Louisiana Real Estate Commission.\n'
        '    </div>\n\n'
        '    <div class="disclosure-property" style="margin-top:0.5rem;">\n'
        '      %s\n'
        '    </div>\n\n'
        '    <div class="disclosure-eho" style="margin-top:0.75rem;display:flex;align-items:center;gap:0.5rem;">\n'
        '      %s\n'
        '      <span>Equal Housing Opportunity.</span>\n'
        '    </div>\n\n'
        '  </footer>'
    ) % (agent["name_title"].replace("®", "&reg;"), agent["brokerage"],
         agent["phone_tel"], agent["phone"], prop_line, eho_svg)
    fair = (
        '    <aside class="fair-housing-notice" role="note" aria-label="Equal Housing Opportunity notice" '
        'style="display:flex;align-items:flex-start;gap:0.6rem;font-size:0.85rem;line-height:1.55;padding:1rem 1.25rem;">\n'
        '      <svg width="24" height="24" viewBox="0 0 24 24" role="img" aria-label="Equal Housing Opportunity logo" '
        'style="flex:0 0 auto;margin-top:0.1rem;" fill="currentColor">\n'
        '        <path d="M12 3 2 10h2v9h5v-5h6v5h5v-9h2L12 3zm0 4.2 1.6 1.2H10.4L12 7.2z"/>\n'
        '      </svg>\n'
        '      <p style="margin:0;">\n'
        '        <strong>Equal Housing Opportunity.</strong>\n'
        '        This property is offered without regard to race, color, religion, sex,\n'
        '        handicap, familial status, or national origin, or any other class\n'
        '        protected by federal, state, or local fair housing law. We are pledged\n'
        '        to the letter and spirit of U.S. policy for the achievement of equal\n'
        '        housing opportunity throughout the nation.\n'
        '      </p>\n'
        '    </aside>'
    )
    return {"broker_disclosure_html": broker, "fair_housing_html": fair}


# --------------------------------------------------------------------------- #
# assemble + build
# --------------------------------------------------------------------------- #
def assemble(slug, facts, photos, do_content, model_copy, model_caption):
    state_full = STATE_NAMES.get(facts["state"], facts["state"])
    addr_exp = expand_address(facts["address"])
    hero_eyebrow = ("For Sale · New %s Construction" % facts["year_built"]) \
        if facts["_new_construction"] else "For Sale"
    agent = dict(AGENT)
    first = agent["name_title"].split()[0]
    agent["bio"] = ("Offered by %s with %s. For private showings and further detail on %s, %s can be "
                    "reached directly at %s." % (agent["name_title"], agent["brokerage"],
                                                 addr_exp, first, agent["phone"]))
    # video autodetect
    vid = "/studio/packages/videos/%s-short.mp4" % slug
    has_vid = (VIDEO_DIR / ("%s-short.mp4" % slug)).exists()

    # ---- captions + copy ----
    ai = None
    captions = [{"file": "%02d.jpg" % i,
                 "alt": "Photo %d of %s" % (i, addr_exp)} for i in range(1, photos + 1)]
    if do_content:
        print("  captioning %d photos (%s)..." % (photos, model_caption))
        captions = caption_gallery(slug, photos, model_caption)
        print("  writing copy (%s)..." % model_copy)
        ai = generate_copy(facts, captions, model_copy)

    hero_alt = captions[0]["alt"] if captions else ""
    if ai:
        copy_ai = {
            "hero_tagline": ai["hero_tagline"],
            "overview_heading": ai["overview_heading"],
            "overview_paragraphs": ai["overview_paragraphs"],
            "pull_quote": ai["pull_quote"],
            "feature_groups": ai["feature_groups"],
            "location_paragraphs": ai["location_paragraphs"],
            "location_points": ai["location_points"],
        }
    else:
        copy_ai = {
            "hero_tagline": "%s in %s." % (facts["type_short"], facts["city"]),
            "overview_heading": "The Residence",
            "overview_paragraphs": ["<Add overview narrative — facts-only draft.>"],
            "pull_quote": "",
            "feature_groups": facts_only_features(facts),
            "location_paragraphs": ["Located in %s, %s (%s)." % (facts["city"], state_full, facts["zip"])],
            "location_points": ["Set in %s, %s" % (facts["city"], state_full)],
        }

    meta_desc = ("For Sale: %s, %s, %s %s. %s%s%s. Offered at %s. Presented by %s, %s.%s" % (
        facts["address"], facts["city"], facts["state"], facts["zip"],
        facts["type_short"],
        (" — %s bed, %s bath" % (facts["beds"], facts["baths"])) if facts["beds"] is not None else "",
        (", %s sq ft" % facts["sqft"]) if facts["sqft"] else "",
        facts["price"] or "price on request", agent["name_title"], agent["brokerage"],
        (" MLS %s." % facts["mls"]) if facts["mls"] else ""))
    og_desc = ("%s — %s bed / %s bath / %s sq ft. Offered at %s. Presented by %s, %s." % (
        facts["type_short"], facts["beds"], facts["baths"], facts["sqft"] or "?",
        facts["price"] or "price on request", agent["name_title"], agent["brokerage"]))
    title = "%s, %s, %s %s — %s %s%s" % (
        facts["address"], facts["city"], facts["state"], facts["zip"], facts["status"],
        facts["price"], (" | MLS %s" % facts["mls"]) if facts["mls"] else "")

    data = {
        "slug": slug,
        "wordmark": wordmark_of(facts["address"]),
        "wordmark_sub": "%s · %s" % (facts["city"], state_full),
        "facts": {k: v for k, v in facts.items() if not k.startswith("_") and k != "price_num"},
        "agent": agent,
        "seo": {"title": title, "meta_description": meta_desc,
                "og_title": "%s, %s, %s %s — %s %s" % (
                    facts["address"], facts["city"], facts["state"], facts["zip"],
                    facts["status"], facts["price"]),
                "og_description": og_desc},
        "copy": dict(section_labels(facts.get("price_num")), **copy_ai, **{
            "hero_eyebrow": hero_eyebrow,
            "hero_address": "%s · %s, %s %s" % (addr_exp, facts["city"], state_full, facts["zip"]),
            "footer_brand": addr_exp,
            "footer_brand_sub": "%s · %s · %s" % (facts["city"], state_full, facts["zip"]),
            "cta_sub": cta_sub_text(facts.get("price_num"), addr_exp,
                                    agent["name_title"].split(",")[0], agent["brokerage"], agent["phone"]),
        }),
        "media": {
            "hero_photo": "01.jpg", "hero_alt": hero_alt,
            "video": vid if has_vid else None,
            "video_poster": "07.jpg" if photos >= 7 else "01.jpg",
            "gallery_dir": "/assets/img/listings/gallery/%s/" % slug,
            "photos": captions,
        },
        "compliance": build_compliance(facts, agent),
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / ("%s.json" % slug)).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return has_vid


def run_builder(slug):
    subprocess.run([sys.executable, str(BUILDER), slug], check=True)


# --------------------------------------------------------------------------- #
# orchestration
# --------------------------------------------------------------------------- #
def stand_up(r, args, has_ai):
    line = (((r.get("location") or {}).get("address") or {}).get("line") or "")
    slug = args.slug if (args.slug and args.address) else slugify(line)
    print("\n=== %s  ->  /estates/%s/ ===" % (line, slug))
    mls = get_mls(r.get("href", "")) if r.get("href") else ""
    facts = derive_facts(r, mls)
    hrefs = [p.get("href") for p in (r.get("photos") or []) if p.get("href")]
    if args.no_photos:
        existing = sorted((GALLERY_ROOT / slug).glob("*.jpg"))
        n = len(existing)
        print("  reusing %d existing photos" % n)
    else:
        print("  downloading up to %d photos (%d available)..." % (args.max_photos, len(hrefs)))
        n = download_photos(slug, hrefs, args.max_photos)
        print("  kept %d unique photos" % n)
    if n == 0:
        print("  SKIP: no photos"); return
    do_content = has_ai and not args.no_content
    if do_content:
        print("  generating captions + copy via claude -p (subscription)...")
    assemble(slug, facts, n, do_content, args.model_copy, args.model_caption)
    run_builder(slug)
    print("  http://127.0.0.1:8091/estates/%s/   |   https://carrie.dubose.me/estates/%s/" % (slug, slug))
    if not do_content:
        why = "claude CLI not found" if not has_ai else "--no-content"
        print("  NOTE: facts-only draft (%s). Rerun without --no-content (with claude logged in) to fill copy/captions." % why)


def main():
    ap = argparse.ArgumentParser(description="Stand up a single-property estate microsite end-to-end.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--address", help="street line to match in the feed, e.g. \"101 Rio Ridge Dr\"")
    g.add_argument("--all", action="store_true", help="build a site for every active listing")
    ap.add_argument("--slug", help="override slug (single-address mode only)")
    ap.add_argument("--max-photos", type=int, default=60)
    ap.add_argument("--no-content", action="store_true", help="skip the AI copy/caption step")
    ap.add_argument("--no-photos", action="store_true", help="reuse the existing gallery folder")
    ap.add_argument("--skip-existing", action="store_true",
                    help="in --all, skip listings that already have data/estates/<slug>.json")
    ap.add_argument("--model-copy", default="opus", help="claude -p --model for prose")
    ap.add_argument("--model-caption", default="haiku", help="claude -p --model for captions")
    args = ap.parse_args()

    has_ai = claude_available()
    if not has_ai and not args.no_content:
        print("(!) `claude` CLI not found on PATH — building facts-only drafts (no AI copy/captions).")

    feed = fetch_feed()
    if args.all:
        for r in feed:
            line = (((r.get("location") or {}).get("address") or {}).get("line") or "")
            slug = slugify(line)
            if args.skip_existing and (DATA_DIR / ("%s.json" % slug)).exists():
                print("\n=== %s  ->  /estates/%s/  (skip: already built) ===" % (line, slug))
                continue
            stand_up(r, args, has_ai)
    else:
        want = args.address.strip().lower()
        match = next((r for r in feed if want in ((((r.get("location") or {}).get("address") or {})
                                                  .get("line") or "").lower())), None)
        if not match:
            avail = [(((r.get("location") or {}).get("address") or {}).get("line") or "?") for r in feed]
            raise SystemExit("No listing matched %r. Available:\n  - %s" % (args.address, "\n  - ".join(avail)))
        stand_up(match, args, has_ai)


if __name__ == "__main__":
    main()
