#!/usr/bin/env python3
"""
build_estates_index.py — generate the Estates directory page.

Reads every data/estates/<slug>.json and writes site/estates/index.html: a single
page that lists every estate microsite as a card (hero photo, price, address, specs,
link). All listings are hosted from the one main site under /estates/<slug>/.

Optional per-listing field `canonical_domain` (e.g. "101rioridge.com"): if set, the
card links to that domain instead of the /estates/<slug>/ subpath — so when a listing
gets its own domain you just add the field and re-run (the DNS/redirect itself points
the domain at this same host — see build/estates/README.md).

    python build/estates/build_estates_index.py

Pure standard library.
"""
import glob
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "estates"
OUT = ROOT / "site" / "estates" / "index.html"


def esc(x):
    return html.escape(str(x), quote=True)


def price_num(p):
    m = re.sub(r"[^\d]", "", p or "")
    return int(m) if m else 0


def card(d):
    f = d["facts"]
    slug = d["slug"]
    href = ("https://%s/" % d["canonical_domain"]) if d.get("canonical_domain") else ("%s/" % slug)
    hero = "/assets/img/listings/gallery/%s/%s" % (slug, d.get("media", {}).get("hero_photo", "01.jpg"))
    specs = []
    if f.get("beds"):
        specs.append("%s bd" % f["beds"])
    if f.get("baths") and str(f["baths"]) != "0":
        specs.append("%s ba" % f["baths"])
    if f.get("sqft"):
        specs.append("%s sqft" % f["sqft"])
    specs = specs or ["Land / lot"]
    domain_note = ('<span class="ecard-domain">%s</span>' % esc(d["canonical_domain"])) \
        if d.get("canonical_domain") else ""
    return (
        '    <a class="ecard" href="%s">\n'
        '      <div class="ecard-img" style="background-image:url(\'%s\')"></div>\n'
        '      <div class="ecard-body">\n'
        '        <div class="ecard-price">%s</div>\n'
        '        <div class="ecard-addr">%s<span class="ecard-city">%s, %s</span></div>\n'
        '        <div class="ecard-specs">%s</div>\n'
        '        <div class="ecard-cta">View the estate site &rarr; %s</div>\n'
        '      </div>\n'
        '    </a>'
    ) % (esc(href), esc(hero), esc(f.get("price", "")), esc(f.get("address", "")),
         esc(f.get("city", "")), esc(f.get("state", "")), esc(" · ".join(specs)), domain_note)


def build():
    listings = []
    for p in sorted(glob.glob(str(DATA_DIR / "*.json"))):
        try:
            listings.append(json.loads(Path(p).read_text(encoding="utf-8")))
        except Exception as e:
            print("  skip %s: %s" % (p, e))
    listings.sort(key=lambda d: price_num(d.get("facts", {}).get("price", "")), reverse=True)
    cards = "\n".join(card(d) for d in listings)
    count = len(listings)

    page = PAGE.replace("{{CARDS}}", cards).replace("{{COUNT}}", str(count))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(page)
    print("built %s  (%d listings)" % (OUT, count))


PAGE = """<!DOCTYPE html>
<html lang="en">
<meta name="robots" content="noindex, nofollow">
<meta name="googlebot" content="noindex, nofollow">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Estates — Current Listings | Carrie Billeaud, REALTOR®, eXp Realty</title>
<meta name="description" content="A collection of current listings presented by Carrie Billeaud, REALTOR with eXp Realty in Acadiana. Each home has its own dedicated site.">
<link rel="icon" href="/assets/img/carrie-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root{--ivory:#f6f3ee;--ink:#1b1a18;--brass:#7c5e2b;--rule:#e2dccf;--dark:#14130f;--ease:cubic-bezier(.2,.7,.2,1)}
  *{box-sizing:border-box}
  body{margin:0;background:var(--ivory);color:var(--ink);font-family:'Inter',system-ui,sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}
  a{color:inherit;text-decoration:none}
  .demo-banner{background:var(--dark);color:#e8e2d6;font-size:.78rem;text-align:center;padding:.5rem 1rem}
  .demo-banner a{color:#e8d5ab;border-bottom:1px solid rgba(232,213,171,.4)}
  .wrap{max-width:1180px;margin:0 auto;padding:0 1.5rem}
  header.top{position:sticky;top:0;z-index:50;background:rgba(246,243,238,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--rule)}
  .top-in{display:flex;align-items:center;justify-content:space-between;padding:.9rem 1.5rem;max-width:1180px;margin:0 auto}
  .brand{font-family:'Playfair Display',serif;font-weight:600;font-size:1.15rem;letter-spacing:.01em}
  .brand span{display:block;font-family:'Inter';font-weight:500;font-size:.62rem;letter-spacing:.22em;text-transform:uppercase;color:var(--brass);margin-top:.1rem}
  .top a.back{font-size:.82rem;color:var(--brass)}
  .hero{padding:clamp(3rem,7vw,6rem) 0 clamp(1.5rem,3vw,2.5rem)}
  .eyebrow{font-size:.72rem;letter-spacing:.24em;text-transform:uppercase;color:var(--brass);font-weight:600}
  .hero h1{font-family:'Playfair Display',serif;font-weight:600;font-size:clamp(2.2rem,5.5vw,3.6rem);line-height:1.05;margin:.5rem 0 .6rem}
  .hero p{max-width:56ch;color:#4a463f;font-weight:300;font-size:1.05rem;margin:0}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.6rem;padding-bottom:5rem}
  .ecard{display:flex;flex-direction:column;background:#fff;border:1px solid var(--rule);border-radius:4px;overflow:hidden;transition:transform .4s var(--ease),box-shadow .4s var(--ease)}
  .ecard:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(20,19,15,.14)}
  .ecard-img{aspect-ratio:4/3;background:#ddd6c8 center/cover no-repeat}
  .ecard-body{padding:1.1rem 1.2rem 1.3rem}
  .ecard-price{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:600}
  .ecard-addr{font-weight:500;margin-top:.15rem}
  .ecard-city{display:block;font-weight:300;color:#6b6659;font-size:.9rem}
  .ecard-specs{font-size:.82rem;letter-spacing:.04em;color:#6b6659;text-transform:uppercase;margin-top:.55rem}
  .ecard-cta{margin-top:.9rem;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--brass);font-weight:600}
  .ecard-domain{display:inline-block;margin-left:.5rem;color:#6b6659;text-transform:none;letter-spacing:0;font-weight:400}
  footer.site{background:var(--dark);color:#cfc9bc;font-size:.82rem;line-height:1.6;padding:2.2rem 0 2.6rem}
  footer.site .wrap>*{margin:.2rem 0}
  footer.site strong{color:#ece7db}
  footer.site .eho{display:flex;align-items:center;gap:.5rem;margin-top:.7rem}
  footer.site a{color:#e8d5ab}
</style>

<div class="demo-banner">Demo concept &mdash; estates directory. Each listing is hosted here and can point its own domain to its page. <a href="/">Back to main site &rarr;</a></div>

<header class="top">
  <div class="top-in">
    <div class="brand">Carrie Billeaud<span>Estates &middot; Acadiana</span></div>
    <a class="back" href="/">&larr; Main site</a>
  </div>
</header>

<main class="wrap">
  <section class="hero">
    <div class="eyebrow">Estates</div>
    <h1>Current Listings</h1>
    <p>A collection of {{COUNT}} homes currently presented by Carrie Billeaud, REALTOR®, with eXp Realty across Acadiana. Each listing has its own dedicated site &mdash; all hosted here, each able to point to its own domain.</p>
  </section>

  <section class="grid">
{{CARDS}}
  </section>
</main>

<footer class="site">
  <div class="wrap">
    <div>Presented by <strong>Carrie Billeaud, REALTOR®</strong> &mdash; eXp Realty &middot; <a href="tel:3372585379">337-258-5379</a></div>
    <div style="margin-top:.5rem">Sponsoring / qualifying broker: <strong><span data-broker="name">to be confirmed at launch</span></strong> &middot; Broker phone: <strong><span data-broker="phone">to be confirmed at launch</span></strong></div>
    <div style="margin-top:.5rem">Licensed by the Louisiana Real Estate Commission. Information deemed reliable but not guaranteed; buyer to verify all details.</div>
    <div class="eho">
      <svg width="18" height="18" viewBox="0 0 24 24" role="img" aria-label="Equal Housing Opportunity" fill="currentColor"><path d="M12 3 2 10h2v9h5v-5h6v5h5v-9h2L12 3zm0 4.2 1.6 1.2H10.4L12 7.2z"/></svg>
      <span>Equal Housing Opportunity.</span>
    </div>
    <div style="margin-top:.6rem;opacity:.7">Demo concept built by Brook DuBose. Not Carrie's live website.</div>
  </div>
</footer>
</html>
"""

if __name__ == "__main__":
    build()
