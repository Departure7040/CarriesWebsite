#!/usr/bin/env python3
"""
Build a studio-style social content package from a market data YAML.

Reads:   data/market/<period>.yaml   (default: data/market/2026-07-sample.yaml)
Writes:  site/studio/packages/market/<YYYY-MM>.json
         site/studio/packages/market/<YYYY-MM>-ready-to-post.md

Mirrors the existing studio package shape (see
site/studio/packages/<listing>/captions.json + ready-to-post.md):
  package.instagram{caption,hashtags}, facebook{caption}, tiktok{script,hook},
  youtube{title,description}, story_text, hooks[3], plus tracked_links using the
  lead.js UTM pattern (utm_campaign="market-report", utm_content=<period-slug>).

COMPLIANCE (identical to functions/api/_content_system_prompt.md)
-----------------------------------------------------------------
* FACTS ONLY: captions cite ONLY numbers present in the YAML. A metric missing
  from the YAML never appears. No hardcoded statistics in this script.
* Source is always labeled; if it is still __FILL__/blank the copy says
  "(source pending)" rather than naming an unverified source.
* When sample:true, every caption states the figures are illustrative/sample
  and must not be quoted as real market data.
* NO steering / fair-housing-sensitive language, NO guarantees or predictions,
  NO "great time to buy", NO mortgage rates, NO "#1 agent".
* Nothing auto-posts. The .md repeats the manual-approval note.

Re-runnable. Usage:

    python build/market/build_market_posts.py
    python build/market/build_market_posts.py data/market/2026-08.yaml
"""

import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
DEFAULT_YAML = REPO / "data" / "market" / "2026-07-sample.yaml"
OUT_DIR = REPO / "site" / "studio" / "packages" / "market"

SITE = "https://carriebilleaud.com"
LANDING_PATH = "/market/"
CAMPAIGN = "market-report"
PLATFORMS = ["instagram", "facebook", "tiktok", "youtube", "threads"]

DASH = "—"  # em-dash


# ---------------------------------------------------------------- formatters
def fmt_money(v):
    try:
        return "$" + f"{round(float(v)):,}"
    except (TypeError, ValueError):
        return None


def fmt_int(v):
    try:
        return f"{round(float(v)):,}"
    except (TypeError, ValueError):
        return None


def fmt_num(v):
    try:
        return f"{float(v):g}"
    except (TypeError, ValueError):
        return None


def period_slug(period):
    months = {
        "january": "01", "february": "02", "march": "03", "april": "04",
        "may": "05", "june": "06", "july": "07", "august": "08",
        "september": "09", "october": "10", "november": "11", "december": "12",
    }
    m = re.search(r"([A-Za-z]+)\s+(\d{4})", period or "")
    if m and m.group(1).lower() in months:
        return f"{m.group(2)}-{months[m.group(1).lower()]}"
    slug = re.sub(r"[^a-z0-9]+", "-", (period or "report").lower()).strip("-")
    return slug or "report"


def tracked_link(platform, slug):
    return (
        f"{SITE}{LANDING_PATH}?utm_source={platform}&utm_medium=social"
        f"&utm_campaign={CAMPAIGN}&utm_content={slug}"
    )


def join(bits):
    if not bits:
        return ""
    if len(bits) == 1:
        return bits[0]
    if len(bits) == 2:
        return bits[0] + " and " + bits[1]
    return ", ".join(bits[:-1]) + ", and " + bits[-1]


def build_fact_bits(metrics):
    """Ordered, human-readable restatements of ONLY the present metrics."""
    bits = []
    price = fmt_money(metrics.get("median_sale_price"))
    if price:
        bits.append(f"a median sale price of {price}")
    dom = fmt_int(metrics.get("avg_days_on_market"))
    if dom:
        bits.append(f"an average of {dom} days on market")
    inv = fmt_int(metrics.get("active_inventory"))
    if inv:
        bits.append(f"{inv} active listings")
    closed = fmt_int(metrics.get("closed_sales"))
    if closed:
        bits.append(f"{closed} closed sales")
    mos = fmt_num(metrics.get("months_of_supply"))
    if mos:
        bits.append(f"{mos} months of supply")
    ppsf = fmt_money(metrics.get("median_price_per_sqft"))
    if ppsf:
        bits.append(f"{ppsf} per square foot (median)")
    return bits


def main():
    yaml_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_YAML
    if not yaml_path.exists():
        raise SystemExit(f"Market data YAML not found: {yaml_path}")

    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    is_sample = bool(data.get("sample", False))
    period = str(data.get("period", "") or "").strip()
    area = str(data.get("area", "") or "").strip()
    raw_source = str(data.get("source", "") or "").strip()
    source = "(source pending)" if (not raw_source or raw_source.startswith("__FILL__")) else raw_source
    metrics = data.get("metrics") or {}

    slug = period_slug(period)
    facts = build_fact_bits(metrics)
    facts_sentence = join(facts)

    # Illustrative disclaimer appended to every caption when sample:true.
    sample_note = (
        " These figures are SAMPLE / illustrative only — not real market data, "
        "and not to be quoted as such."
        if is_sample else ""
    )
    source_line = f" Source: {source}."

    links = {p: tracked_link(p, slug) for p in PLATFORMS}

    # --- headline sentence shared by several platforms -----------------------
    if facts_sentence:
        headline = (
            f"Acadiana market snapshot for {period} ({area}): {facts_sentence}."
        )
    else:
        headline = (
            f"The {period} Acadiana market report ({area}) is ready."
        )

    # --- Instagram -----------------------------------------------------------
    ig_caption = (
        f"{headline}{source_line}{sample_note}\n\n"
        "Want the full monthly report for your town and price range? "
        "Tap the link to get it in your inbox.\n\n"
        f"{links['instagram']}"
    )
    hashtags = [
        "#AcadianaHomes",
        "#LafayetteRealEstate",
        "#AcadianaMarketReport",
        "#LouisianaRealEstate",
        "#CarrieBilleaudRealtor",
        "#eXpRealty",
    ]

    # --- Facebook ------------------------------------------------------------
    fb_caption = (
        f"{headline}{source_line}{sample_note}\n\n"
        "Every month I put the Acadiana numbers into one short report — median "
        "price, days on market, inventory, and a by-town breakdown — so you can "
        "see the figures for yourself. Reach out or grab the report at the link "
        "and I'm glad to walk through what they mean for your specific search.\n\n"
        f"Carrie Billeaud, REALTOR · eXp Realty · Acadiana.\n\n"
        f"{links['facebook']}"
    )

    # --- TikTok --------------------------------------------------------------
    tt_script = (
        f"Here's the Acadiana market snapshot for {period}. "
        + (f"We're looking at {facts_sentence}. " if facts_sentence else "")
        + f"{source.rstrip('.')}.{sample_note} "
        "Want the full report for your town? The link will send it to you.\n\n"
        f"{links['tiktok']}"
    )
    tt_hook = f"Acadiana numbers are in for {period}."

    # --- YouTube -------------------------------------------------------------
    yt_title = f"Acadiana Market Report — {period} ({area})"
    yt_description = (
        f"{headline}{source_line}{sample_note}\n\n"
        "Reach out to Carrie Billeaud, REALTOR with eXp Realty, for the full "
        "monthly Acadiana market report and a breakdown for your specific "
        "search.\n\n"
        f"{links['youtube']}"
    )

    # --- story + hooks -------------------------------------------------------
    story_text = f"Acadiana market snapshot ✦ {period}" + (
        " (sample data)" if is_sample else ""
    )
    price = fmt_money(metrics.get("median_sale_price"))
    dom = fmt_int(metrics.get("avg_days_on_market"))
    hooks = [
        f"Acadiana numbers are in for {period}.",
        (f"Median sale price this month: {price}." if price
         else f"The {period} Acadiana report is here."),
        (f"Homes sold in about {dom} days on average." if dom
         else f"See the full Acadiana breakdown by town."),
    ]

    package = {
        "instagram": {"caption": ig_caption, "hashtags": hashtags},
        "facebook": {"caption": fb_caption},
        "tiktok": {"script": tt_script, "hook": tt_hook},
        "youtube": {"title": yt_title, "description": yt_description},
        "story_text": story_text,
        "hooks": hooks,
    }

    doc = {
        "report": {
            "period": period,
            "area": area,
            "source": source,
            "sample": is_sample,
            "metrics_present": [k for k in metrics if metrics.get(k) not in (None, "")],
        },
        "package": package,
        "tracked_links": links,
        "landing_url": f"{SITE}{LANDING_PATH}",
        "landing_path": LANDING_PATH,
        "campaign": CAMPAIGN,
        "sample": is_sample,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / f"{slug}.json"
    md_path = OUT_DIR / f"{slug}-ready-to-post.md"

    json_path.write_text(json.dumps(doc, indent=2, ensure_ascii=True), encoding="utf-8")

    # --- ready-to-post markdown ---------------------------------------------
    sample_banner = " _(SAMPLE / illustrative data — not real market figures)_" if is_sample else ""
    md = []
    md.append(f"# Ready to post — Acadiana Market Report, {period}{sample_banner}")
    md.append("")
    md.append(f"**{area} · Source: {source}**")
    if facts_sentence:
        md.append(f"Reported figures: {facts_sentence}.")
    if is_sample:
        md.append("")
        md.append("> ⚠️ SAMPLE DATA. These are illustrative placeholder numbers, "
                  "not real Acadiana market data. Do not publish until real, "
                  "sourced figures replace them (set `sample: false` in the YAML).")
    md.append("")
    md.append("> Review, tweak if you like, then copy the caption and post with your graphic.")
    md.append("> Publishing stays manual — nothing auto-posts, Carrie approves everything.")
    md.append("")
    md.append("**Tracked links** (already appended to each caption below → clicks + leads attribute to the right post/platform):")
    for p in PLATFORMS:
        md.append(f"- **{p.capitalize()}:** {links[p]}")
    md.append("")
    md.append(f"Landing page: {SITE}{LANDING_PATH}")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Instagram")
    md.append(ig_caption)
    md.append("")
    md.append(" ".join(hashtags))
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Facebook")
    md.append(fb_caption)
    md.append("")
    md.append("---")
    md.append("")
    md.append("## TikTok / Reels")
    md.append(f"**Hook (first 1-2s):** {tt_hook}")
    md.append("")
    md.append(tt_script)
    md.append("")
    md.append("---")
    md.append("")
    md.append("## YouTube")
    md.append(f"**Title:** {yt_title}")
    md.append("")
    md.append(yt_description)
    md.append("")
    md.append("---")
    md.append("")
    md.append("## Instagram / Facebook Story")
    md.append(story_text)
    md.append("")
    md.append("## Alternate hooks")
    for h in hooks:
        md.append(f"- {h}")
    md.append("")
    md_path.write_text("\n".join(md), encoding="utf-8")

    print("Acadiana Market Report — social package build summary")
    print(f"  data source : {yaml_path.relative_to(REPO)}")
    print(f"  sample flag : {is_sample}")
    print(f"  period      : {period}")
    print(f"  attribution : {source}")
    print(f"  metrics cited: {', '.join(doc['report']['metrics_present']) or '(none)'}")
    print(f"  wrote       : {json_path.relative_to(REPO)}")
    print(f"  wrote       : {md_path.relative_to(REPO)}")
    if is_sample:
        print("  NOTE: sample:true — captions marked illustrative; do not present as real.")


if __name__ == "__main__":
    main()
