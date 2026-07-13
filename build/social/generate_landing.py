#!/usr/bin/env python3
"""
generate_landing.py — property LANDING PAGE generator (the attribution keystone).

Given one listing dict, writes a self-contained luxury-clean landing page at
    site/l/<slug>/index.html
plus copies the property photo to site/l/<slug>/photo.jpg.

The page is the destination of every tracked link (see links.py):
    social post -> /l/<slug>/?utm_source=<platform>... -> THIS page -> lead.

DEMO vs PRODUCTION
------------------
The DEMO serves site/ from a static Python server behind a Cloudflare tunnel, so
attribution must work with CLIENT-SIDE JS only:
  * inline JS reads utm_source/campaign/content from the URL query and injects
    them into the form's hidden fields (no server dependency);
  * a tasteful "Thanks for stopping by from {source}" line shows iff a source is
    present (proves tracking to the live demo);
  * on submit the demo shows a confirmation that names the captured source +
    listing (visibly proves the lead would be tagged).
In PRODUCTION the identical form POSTs to /api/lead (functions/api/lead.js) for
real, carrying the same hidden source/platform/listing fields.

COMPLIANCE (CR-007 / fair housing): facts only — price/beds/baths/sqft/address/
photo + Carrie's real NAP. No steering language, no unverified stats, privacy
notice on the form.

Importable:  from generate_landing import generate_landing
CLI:         python generate_landing.py            # builds the Ivy Cottage demo
"""

from __future__ import annotations

import html
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SITE = REPO / "site"
LISTING_IMG_DIR = SITE / "assets" / "img" / "listings"


def slugify(text: str) -> str:
    """Match content_orchestrator/_slugify: lowercase, hyphenated address."""
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def _fmt_price(v) -> str:
    """Accept 1510000 / '1510000' / '$1,510,000' -> '$1,510,000'."""
    if v is None or v == "":
        return ""
    if isinstance(v, str) and v.strip().startswith("$"):
        return v.strip()
    try:
        return "${:,}".format(int(float(str(v).replace(",", "").replace("$", ""))))
    except (ValueError, TypeError):
        return str(v)


def _spec(v) -> str:
    """Render a spec value (bed/bath/sqft) or an em dash if missing."""
    if v is None or v == "":
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    try:
        return "{:,}".format(int(v)) if str(v).isdigit() else str(v)
    except (ValueError, TypeError):
        return str(v)


def _resolve_photo(listing: dict, slug: str) -> Path | None:
    """Prefer an explicit photo path, else the local listing image by slug."""
    p = listing.get("photo")
    if p:
        pp = Path(p)
        if pp.is_file():
            return pp
    local = LISTING_IMG_DIR / f"{slug}.jpg"
    return local if local.is_file() else None


def _page_html(l: dict) -> str:
    slug = l["slug"]
    e = html.escape
    address = e(str(l.get("address", "")))
    city = e(str(l.get("city", "")))
    price = e(_fmt_price(l.get("price")))
    beds = e(_spec(l.get("beds")))
    baths = e(_spec(l.get("baths")))
    sqft = e(_spec(l.get("sqft")))
    view_url = e(str(l.get("url", "")))
    prefill = f"I'm interested in {l.get('address','')}, {l.get('city','')}.".strip()
    prefill_attr = e(prefill)

    # NOTE: noindex here because this is the DEMO. In PRODUCTION these are real,
    # crawlable per-property pages — drop the robots noindex so they INDEX.
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow"><!-- DEMO ONLY: remove in production so property pages INDEX -->
<title>{price} · {address}, {city} — Carrie Billeaud, REALTOR</title>
<meta name="description" content="Just listed: {address}, {city}. {beds} bd · {baths} ba · {sqft} sq ft · {price}. Presented by Carrie Billeaud, REALTOR with eXp Realty.">
<link rel="stylesheet" href="/assets/style.css?v=10">
<style>
  .lp-hero{{position:relative;min-height:62vh;display:flex;align-items:flex-end;
    background:#1a2332 center/cover no-repeat;color:#fff}}
  .lp-hero::after{{content:"";position:absolute;inset:0;
    background:linear-gradient(180deg,rgba(26,35,50,.15) 0%,rgba(26,35,50,.82) 100%)}}
  .lp-hero-inner{{position:relative;z-index:2;width:100%;max-width:960px;margin:0 auto;
    padding:2.5rem 1.25rem}}
  .lp-badge{{display:inline-block;background:var(--gold);color:var(--ink);
    font-weight:700;letter-spacing:.16em;text-transform:uppercase;font-size:.72rem;
    padding:.4rem .8rem;border-radius:4px}}
  .lp-price{{font-family:Georgia,"Times New Roman",serif;font-weight:700;
    font-size:clamp(2.4rem,6vw,3.6rem);line-height:1.05;margin:.6rem 0 .2rem;
    text-shadow:0 1px 12px rgba(0,0,0,.35)}}
  .lp-addr{{font-size:1.15rem;font-weight:600;margin:0}}
  .lp-city{{opacity:.9;margin:.1rem 0 0}}
  .lp-specs{{display:flex;flex-wrap:wrap;gap:1.5rem;list-style:none;padding:0;
    margin:1.1rem 0 0;border-top:1px solid rgba(255,255,255,.28);padding-top:1rem}}
  .lp-specs li{{display:flex;flex-direction:column}}
  .lp-specs .n{{font-family:Georgia,serif;font-size:1.6rem;font-weight:700;line-height:1}}
  .lp-specs .k{{text-transform:uppercase;letter-spacing:.1em;font-size:.68rem;
    opacity:.85;margin-top:.2rem}}
  .lp-wrap{{max-width:640px;margin:0 auto;padding:2.5rem 1.25rem}}
  .lp-src{{display:none;background:#e6f2e7;color:var(--teal-dark);border-radius:8px;
    padding:.7rem 1rem;font-weight:600;margin-bottom:1.5rem;text-align:center}}
  .lp-form label{{display:block;font-weight:600;font-size:.9rem;margin:.9rem 0 .3rem}}
  .lp-form input,.lp-form textarea{{width:100%;padding:.7rem .8rem;border:1px solid var(--rule);
    border-radius:6px;font:inherit;background:#fff}}
  .lp-hp{{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}}
  .lp-note{{font-size:.8rem;color:#5a6472;margin-top:.8rem}}
  .lp-ok{{display:none;background:var(--cream);border:1px solid var(--gold);
    border-left:4px solid var(--gold);border-radius:8px;padding:1.1rem 1.2rem;
    margin-top:1rem;font-weight:600}}
  .lp-back{{display:inline-block;margin-top:1.5rem}}
</style>
</head>
<body>
<div class="demo-banner">Demo concept — property landing page. <a href="/">Back to site &rarr;</a></div>

<header class="lp-hero" id="lp-hero">
  <div class="lp-hero-inner">
    <span class="lp-badge">Just Listed</span>
    <div class="lp-price">{price}</div>
    <p class="lp-addr">{address}</p>
    <p class="lp-city">{city}</p>
    <ul class="lp-specs">
      <li><span class="n">{beds}</span><span class="k">Beds</span></li>
      <li><span class="n">{baths}</span><span class="k">Baths</span></li>
      <li><span class="n">{sqft}</span><span class="k">Sq Ft</span></li>
    </ul>
  </div>
</header>

<main class="lp-wrap">
  <p class="lp-src" id="lp-src"></p>

  <p class="kicker">Contact</p>
  <h2 style="margin-top:.2rem">Interested in this home?</h2>
  <p>Send Carrie a note and she'll reach out about {address}.</p>

  <form class="lp-form" id="lp-form" method="post" action="/api/lead">
    <!-- Honeypot: real people leave this empty; bots fill it. -->
    <div class="lp-hp" aria-hidden="true">
      <label for="company">Company</label>
      <input id="company" type="text" name="company" tabindex="-1" autocomplete="off">
    </div>

    <!-- Attribution + context hidden fields. source/platform/utm_* are filled
         CLIENT-SIDE from the URL query by the inline script below. -->
    <input type="hidden" name="listing_slug" value="{e(slug)}">
    <input type="hidden" name="listing_address" value="{address}, {city}">
    <input type="hidden" name="source" id="f-source" value="website">
    <input type="hidden" name="platform" id="f-platform" value="">
    <input type="hidden" name="utm_source" id="f-utm-source" value="">
    <input type="hidden" name="utm_campaign" id="f-utm-campaign" value="">
    <input type="hidden" name="utm_content" id="f-utm-content" value="">

    <label for="name">Name</label>
    <input id="name" type="text" name="name" placeholder="Your name" required>

    <label for="email">Email</label>
    <input id="email" type="email" name="email" placeholder="you@example.com">

    <label for="phone">Phone</label>
    <input id="phone" type="tel" name="phone" placeholder="337-000-0000">

    <label for="message">Message</label>
    <textarea id="message" name="message" rows="3">{prefill_attr}</textarea>

    <p class="lp-note">By submitting, you agree Carrie Billeaud may contact you about
      your inquiry. Your information is never sold or shared. (CR-007)</p>

    <button class="btn btn-gold" type="submit" style="margin-top:1rem">Request details</button>
  </form>

  <div class="lp-ok" id="lp-ok" role="status" aria-live="polite"></div>

  <a class="lp-back btn" href="/#listings">&larr; View all listings</a>
</main>

<footer class="footer"><div class="wrap">
  <img class="footer-logo" src="/assets/img/carrie-logo.png" alt="Carrie Billeaud, Realtor — eXp Realty">
  <p>Carrie Billeaud, REALTOR® · eXp Realty · Lafayette, Louisiana · <a href="tel:3372585379">337-258-5379</a></p>
  <p>Demo concept built as part of an SEO audit by Brook DuBose. Not Carrie's live website. Sample copy marked as placeholder is illustrative only.</p>
</div></footer>

<script>
(function(){{
  var q = new URLSearchParams(location.search);
  var utmSource = q.get('utm_source') || '';
  var platform  = q.get('platform')   || utmSource; // platform defaults to utm_source
  var campaign  = q.get('utm_campaign')|| '';
  var content   = q.get('utm_content') || {slug!r};

  // Set the hero photo (kept as a JS-set background so the file is optional).
  var hero = document.getElementById('lp-hero');
  if (hero) hero.style.backgroundImage = "url('photo.jpg')";

  // Inject attribution into the form's hidden fields (client-side, no server).
  function set(id, v){{ var el = document.getElementById(id); if (el) el.value = v; }}
  set('f-utm-source', utmSource);
  set('f-utm-campaign', campaign);
  set('f-utm-content', content);
  if (platform) {{ set('f-platform', platform); set('f-source', platform); }}

  // Tasteful "thanks for stopping by" line — only when a source is present.
  if (utmSource) {{
    var pretty = utmSource.charAt(0).toUpperCase() + utmSource.slice(1);
    var line = document.getElementById('lp-src');
    line.textContent = 'Thanks for stopping by from ' + pretty + ' ✨';
    line.style.display = 'block';
  }}

  // DEMO: intercept submit and show a confirmation that PROVES attribution.
  // In production this block is a no-op path — the form POSTs to /api/lead.
  var DEMO = true;
  var form = document.getElementById('lp-form');
  form.addEventListener('submit', function(ev){{
    if (!DEMO) return;                 // production: let it POST to /api/lead
    ev.preventDefault();
    if (document.getElementById('company').value) return; // honeypot
    var src = platform || 'website';
    var ok = document.getElementById('lp-ok');
    ok.innerHTML = 'Got it — Carrie will reach out about <strong>{address}</strong>.' +
      '<br><span style="font-weight:400;font-size:.85rem;color:#5a6472">' +
      '(Demo: this lead would be tagged source=' + src + ', listing={slug}.)</span>';
    ok.style.display = 'block';
    form.style.display = 'none';
    ok.scrollIntoView({{behavior:'smooth', block:'center'}});
  }});
}})();
</script>
</body>
</html>
"""


def generate_landing(listing: dict, out_root: Path | None = None) -> Path:
    """
    Build site/l/<slug>/index.html + photo.jpg for one listing dict.

    listing keys used: address, city, price, beds, baths, sqft, url,
    property_id (optional), slug (optional; derived from address if absent),
    photo (optional path; else falls back to site/assets/img/listings/<slug>.jpg).

    Returns the path to the written index.html.
    """
    out_root = out_root or (SITE / "l")
    slug = listing.get("slug") or slugify(listing.get("address", "listing"))
    l = dict(listing)
    l["slug"] = slug

    page_dir = out_root / slug
    page_dir.mkdir(parents=True, exist_ok=True)

    # Copy the property photo alongside the page (relative photo.jpg reference).
    photo = _resolve_photo(listing, slug)
    if photo:
        shutil.copyfile(photo, page_dir / "photo.jpg")

    index = page_dir / "index.html"
    index.write_text(_page_html(l), encoding="utf-8")
    return index


# --- CLI: build the Ivy Cottage demo + print the tracked links ---------------
if __name__ == "__main__":
    from links import all_links, base_url  # local import so module stays clean

    ivy = {
        "slug": "204-ivy-cottage-dr",
        "property_id": "8075596386",
        "address": "204 Ivy Cottage Dr",
        "city": "Youngsville, LA",
        "price": 1510000,
        "beds": 4,
        "baths": "3.5",
        "sqft": 3918,
        "url": "https://www.realtor.com/realestateandhomes-detail/"
        "204-Ivy-Cottage-Dr_Youngsville_LA_70592_M80755-96386",
    }

    out = generate_landing(ivy)
    slug = ivy["slug"]
    print(f"Wrote: {out}")
    print(f"Photo: {out.parent / 'photo.jpg'} "
          f"(exists={ (out.parent / 'photo.jpg').is_file() })")
    print(f"\nLanding URL: {base_url(slug)}")
    print("\nPer-platform tracked links (DIRECT / demo-working):")
    for p, links in all_links(slug).items():
        print(f"  {p:10s} {links['direct']}")

    sys.exit(0)
