#!/usr/bin/env python3
"""
build_estate.py — deterministic builder for single-property estate microsites.

Reads   data/estates/<slug>.json  +  build/estates/estate_template.html
Writes  site/estates/<slug>/index.html

Usage:
    python build/estates/build_estate.py <slug>      # build one listing
    python build/estates/build_estate.py --all       # rebuild every data/estates/*.json

Pure standard library (json, html, re, os, sys, pathlib). No external deps.
"""
import json
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # E:/CarriesWebsite
TEMPLATE = ROOT / "build" / "estates" / "estate_template.html"
DATA_DIR = ROOT / "data" / "estates"
SITE_DIR = ROOT / "site" / "estates"

LAYOUT_CYCLE = ["wide", "", "half", "half", "", "", ""]  # 7-tile mosaic cycle


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def esc(x):
    """Escape a value for insertion as HTML text/attribute (& < >, quotes left as-is
    to match the reference page, which never quotes inside these fields)."""
    return html.escape(str(x), quote=False)


def num(v, places):
    """Format a float to <places> decimals, then drop trailing zeros / dot."""
    s = ("{:.%df}" % places).format(float(v))
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


# --------------------------------------------------------------------------- #
# generated blocks
# --------------------------------------------------------------------------- #
def gen_spec_strip(facts):
    lot_number = str(facts["lot"]).split()[0]  # "0.56 acre" -> "0.56"
    rows = [
        (facts["beds"], "Bedrooms"),
        (facts["baths"], "Baths"),
        (facts["sqft"], "Sq Ft"),
        (lot_number, "Acre Lot"),
    ]
    return "\n".join(
        '      <div><span class="n">%s</span><span class="l">%s</span></div>'
        % (esc(v), esc(l))
        for v, l in rows
    )


def gen_spec_grid(facts):
    rows = [
        ("Price", facts["price"]),
        ("Status", facts["status"]),
        ("Bedrooms", facts["beds"]),
        ("Bathrooms", facts["baths"]),
        ("Living Area", "%s sq ft" % facts["sqft"]),
        ("Lot Size", facts["lot"]),
        ("Year Built", facts["year_built"]),
        ("Garage", facts["garage"]),
        ("Type", facts["type_short"]),
        ("MLS #", facts["mls"]),
    ]
    return "\n".join(
        '      <div class="spec-cell"><div class="l">%s</div><div class="v">%s</div></div>'
        % (esc(label), esc(value))
        for label, value in rows
    )


def gen_overview_paragraphs(paras):
    return "\n".join("      <p>%s</p>" % esc(p) for p in paras)


def gen_feature_cards(groups):
    cards = []
    for g in groups:
        items = "\n".join("          <li>%s</li>" % esc(it) for it in g["items"])
        cards.append(
            '      <div class="feature-card reveal">\n'
            "        <h3>%s</h3>\n"
            "        <ul>\n"
            "%s\n"
            "        </ul>\n"
            "      </div>" % (esc(g["title"]), items)
        )
    return "\n".join(cards)


def gen_location_paragraphs(paras):
    return "\n".join("        <p>%s</p>" % esc(p) for p in paras)


def gen_location_points(points):
    return "\n".join("          <li>%s</li>" % esc(pt) for pt in points)


def gen_photos(photos):
    return ",\n".join(
        "    {f:%s,a:%s}" % (json.dumps(p["file"]), json.dumps(p["alt"]))
        for p in photos
    )


def gen_layout(n):
    vals = [LAYOUT_CYCLE[i % len(LAYOUT_CYCLE)] for i in range(n)]
    return ",".join(json.dumps(v) for v in vals)


def gen_map(lat, lon):
    minlon, minlat = num(lon - 0.01, 5), num(lat - 0.005, 5)
    maxlon, maxlat = num(lon + 0.01, 5), num(lat + 0.005, 5)
    bbox = "%2C".join([minlon, minlat, maxlon, maxlat])
    marker = "%s%%2C%s" % (num(lat, 6), num(lon, 6))
    return bbox, marker


# --------------------------------------------------------------------------- #
# video conditional
# --------------------------------------------------------------------------- #
def apply_video(tpl, has_video):
    if has_video:
        # keep content, strip the (own-line, column-0) marker lines
        tpl = tpl.replace("<!--{{#VIDEO}}-->\n", "").replace("<!--{{/VIDEO}}-->\n", "")
    else:
        # remove each marked region entirely
        tpl = re.sub(
            r"<!--\{\{#VIDEO\}\}-->\n.*?<!--\{\{/VIDEO\}\}-->\n",
            "",
            tpl,
            flags=re.DOTALL,
        )
    return tpl


# --------------------------------------------------------------------------- #
# main build
# --------------------------------------------------------------------------- #
def build(slug):
    data_path = DATA_DIR / ("%s.json" % slug)
    if not data_path.exists():
        raise SystemExit("data file not found: %s" % data_path)
    d = json.loads(data_path.read_text(encoding="utf-8"))

    facts = d["facts"]
    agent = d["agent"]
    seo = d["seo"]
    copy = d["copy"]
    media = d["media"]
    comp = d["compliance"]

    # ---- derived values ----
    placename = d["wordmark_sub"].replace(" · ", ", ")          # "Lafayette, Louisiana"
    agent_name = agent["name_title"].split(",")[0].strip()      # "Carrie Billeaud"
    bbox, marker = gen_map(facts["lat"], facts["lon"])
    has_video = bool(media.get("video"))

    tpl = TEMPLATE.read_text(encoding="utf-8")

    # ---- generated block markers (must run before scalar replace) ----
    blocks = {
        "      <!--SPEC_STRIP-->": gen_spec_strip(facts),
        "      <!--SPEC_GRID-->": gen_spec_grid(facts),
        "      <!--OVERVIEW_PARAGRAPHS-->": gen_overview_paragraphs(copy["overview_paragraphs"]),
        "      <!--FEATURE_CARDS-->": gen_feature_cards(copy["feature_groups"]),
        "        <!--LOCATION_PARAGRAPHS-->": gen_location_paragraphs(copy["location_paragraphs"]),
        "          <!--LOCATION_POINTS-->": gen_location_points(copy["location_points"]),
        "<!--FAIR_HOUSING-->": comp["fair_housing_html"],
        "<!--BROKER_DISCLOSURE-->": comp["broker_disclosure_html"],
        "/*PHOTOS*/": gen_photos(media["photos"]),
        "/*LAYOUT*/": gen_layout(len(media["photos"])),
    }
    for marker_str, value in blocks.items():
        if marker_str not in tpl:
            raise SystemExit("template marker missing: %s" % marker_str)
        tpl = tpl.replace(marker_str, value)

    # ---- video conditional ----
    tpl = apply_video(tpl, has_video)

    # ---- scalar tokens ----
    raw = {                                   # inserted verbatim (urls / paths / codes)
        "{{SLUG}}": d["slug"],
        "{{GALLERY_DIR}}": media["gallery_dir"],
        "{{MEDIA_HERO_PHOTO}}": media["hero_photo"],
        "{{MEDIA_VIDEO}}": media.get("video") or "",
        "{{MEDIA_VIDEO_POSTER}}": media.get("video_poster") or "",
        "{{AGENT_HEADSHOT}}": agent["headshot"],
        "{{AGENT_PHONE_TEL}}": agent["phone_tel"],
        "{{FACTS_REALTOR_URL}}": facts["realtor_url"],
        "{{MAP_BBOX}}": bbox,
        "{{MAP_MARKER}}": marker,
        "{{GEO_POSITION}}": "%s;%s" % (num(facts["lat"], 6), num(facts["lon"], 6)),
        "{{GEO_REGION}}": "US-%s" % facts["state"],
        "{{PHOTO_COUNT}}": str(len(media["photos"])),
    }
    text = {                                  # HTML-escaped text / attribute content
        "{{SEO_TITLE}}": seo["title"],
        "{{SEO_META_DESCRIPTION}}": seo["meta_description"],
        "{{SEO_OG_TITLE}}": seo["og_title"],
        "{{SEO_OG_DESCRIPTION}}": seo["og_description"],
        "{{SEO_AUTHOR}}": "%s — %s" % (agent["name_title"], agent["brokerage"]),
        "{{GEO_PLACENAME}}": placename,
        "{{WORDMARK}}": d["wordmark"],
        "{{WORDMARK_SUB}}": d["wordmark_sub"],
        "{{FACTS_PRICE}}": facts["price"],
        "{{FACTS_ADDRESS}}": facts["address"],
        "{{HERO_ALT}}": media["hero_alt"],
        "{{HERO_ADDRESS}}": copy["hero_address"],
        "{{COPY_HERO_EYEBROW}}": copy["hero_eyebrow"],
        "{{COPY_HERO_TAGLINE}}": copy["hero_tagline"],
        "{{COPY_OVERVIEW_EYEBROW}}": copy["overview_eyebrow"],
        "{{COPY_OVERVIEW_HEADING}}": copy["overview_heading"],
        "{{COPY_PULL_QUOTE}}": copy["pull_quote"],
        "{{COPY_DETAILS_EYEBROW}}": copy["details_eyebrow"],
        "{{COPY_DETAILS_HEADING}}": copy["details_heading"],
        "{{COPY_FEATURES_EYEBROW}}": copy["features_eyebrow"],
        "{{COPY_FEATURES_HEADING}}": copy["features_heading"],
        "{{COPY_GALLERY_EYEBROW}}": copy["gallery_eyebrow"],
        "{{COPY_GALLERY_HEADING}}": copy["gallery_heading"],
        "{{COPY_VIDEO_EYEBROW}}": copy.get("video_eyebrow", ""),
        "{{COPY_VIDEO_HEADING}}": copy.get("video_heading", ""),
        "{{COPY_LOCATION_EYEBROW}}": copy["location_eyebrow"],
        "{{COPY_LOCATION_HEADING}}": copy["location_heading"],
        "{{COPY_CTA_EYEBROW}}": copy["cta_eyebrow"],
        "{{COPY_CTA_HEADING}}": copy["cta_heading"],
        "{{COPY_CTA_SUB}}": copy["cta_sub"],
        "{{FOOTER_BRAND}}": copy["footer_brand"],
        "{{FOOTER_BRAND_SUB}}": copy["footer_brand_sub"],
        "{{FOOTER_CONTACT_LINE2}}": "%s · %s, %s" % (agent["brokerage"], facts["city"], facts["state"]),
        "{{AGENT_NAME_TITLE}}": agent["name_title"],
        "{{AGENT_NAME}}": agent_name,
        "{{AGENT_BROKERAGE}}": agent["brokerage"],
        "{{AGENT_PHONE}}": agent["phone"],
        "{{AGENT_ROLE_LINE}}": "%s · %s" % (agent["brokerage"], placename),
        "{{AGENT_HEADSHOT_ALT}}": "Portrait of %s with %s." % (agent["name_title"], agent["brokerage"]),
        "{{AGENT_BIO}}": agent["bio"],
        "{{FORM_LISTING_ADDRESS}}": "%s, %s, %s" % (facts["address"], facts["city"], facts["state"]),
        "{{FORM_TEXTAREA}}": "I'd like to schedule a private showing of %s." % facts["address"],
        "{{MAP_TITLE}}": "Map showing the location of %s, %s, %s" % (facts["address"], facts["city"], facts["state"]),
    }

    for tok, val in raw.items():
        tpl = tpl.replace(tok, str(val))
    for tok, val in text.items():
        tpl = tpl.replace(tok, esc(val))

    # ---- safety: no unresolved tokens / markers ----
    leftovers = re.findall(r"\{\{[A-Z_#/]+\}\}|<!--\{\{|/\*PHOTOS\*/|/\*LAYOUT\*/", tpl)
    if leftovers:
        raise SystemExit("unresolved tokens/markers remain: %s" % sorted(set(leftovers)))

    out_dir = SITE_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    # Match the reference page's Windows (CRLF) line-ending convention.
    with open(out_path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(tpl)
    print("built %s  (%d bytes, %d photos, video=%s)"
          % (out_path, len(tpl), len(media["photos"]), "yes" if has_video else "no"))
    return out_path


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    if argv[0] == "--all":
        slugs = sorted(p.stem for p in DATA_DIR.glob("*.json"))
        if not slugs:
            raise SystemExit("no json files in %s" % DATA_DIR)
        for slug in slugs:
            build(slug)
    else:
        build(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
