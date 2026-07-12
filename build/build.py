#!/usr/bin/env python3
"""
Deterministic production build for carriebilleaud.com.

Pragmatic "keep the static output, add a deterministic build" generator
(code-review CR-002) — NOT a framework rebuild. Reads:

    build/production.config.json   single source of truth (tokens + flags)
    build/page_manifest.json       one entry per publishable marketing page

For every page with publish:true it copies site/<path> to dist/<path> and
transforms it (NAP tokens, canonical host, canonical/OG/Twitter/favicon/GA4,
broker-disclosure footer, de-demo, noindex gate, content-hashed assets), then
emits dist/robots.txt, dist/sitemap.xml and dist/404.html.

SAFETY GATE: if any published page would ship a "__FILL__" placeholder, the
build FAILS LOUDLY and writes nothing. That refusal is the point — it proves an
unfilled NAP/broker config cannot reach production.

Pure standard library. Run:

    python build/build.py            # full build (writes dist/)
    python build/build.py --check    # validate config/manifest only, no writes
"""

import argparse
import hashlib
import html as _html
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
DIST = REPO / "dist"
BUILD = REPO / "build"
FILL = "__FILL__"


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #
def load_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def canonical_host_bare(config):
    return re.sub(r"^https?://", "", config["canonical_host"]).rstrip("/")


def resolve_template(tmpl, config):
    """Resolve a nap_replacements value_template against tokens + specials.
    Returns the resolved string (which may still contain __FILL__)."""
    out = tmpl.replace("__CANONICAL_HOST_BARE__", canonical_host_bare(config))
    for key, val in config["tokens"].items():
        out = out.replace("{" + key + "}", str(val))
    return out


# --------------------------------------------------------------------------- #
# transforms  (each takes/returns the html string)
# --------------------------------------------------------------------------- #
def apply_nap(html, config):
    for rule in config["nap_replacements"]:
        html = html.replace(rule["find"], resolve_template(rule["value_template"], config))
    return html


def strip_demo(html):
    # demo banner div (contains only an <a>, so non-greedy to first close)
    html = re.sub(r'<div class="demo-banner">.*?</div>', "", html, flags=re.S)
    # footer demo disclaimer paragraph
    html = re.sub(r"<p>Demo concept built as part of an SEO audit.*?</p>", "", html, flags=re.S)
    # "Demo Concept" title suffix (em-dash separated)
    html = re.sub(r"\s*[—-]\s*Demo Concept", "", html)
    return html


def apply_noindex(html, config):
    if config["flags"].get("strip_noindex"):
        html = html.replace('<meta name="robots" content="noindex, nofollow">',
                            '<meta name="robots" content="index, follow">')
    return html


def hash_assets(html, css_hash):
    return re.sub(r"(style\.css)\?v=\d+", r"\1?v=" + css_hash, html)


def head_block(page, config):
    host = config["canonical_host"].rstrip("/")
    canon = page["canonical"]
    title = re.sub(r"\s*[—-]\s*Demo Concept", "", page["title"])
    desc = page["meta_description"]
    og_img = host + page["og_image"]
    fav = host + config["favicon"]
    tk = config["tokens"]

    lines = [
        f'<link rel="canonical" href="{canon}">',
        f'<link rel="icon" href="{fav}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{_html.escape(title, quote=True)}">',
        f'<meta property="og:description" content="{_html.escape(desc, quote=True)}">',
        f'<meta property="og:url" content="{canon}">',
        f'<meta property="og:image" content="{og_img}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{_html.escape(title, quote=True)}">',
        f'<meta name="twitter:description" content="{_html.escape(desc, quote=True)}">',
        f'<meta name="twitter:image" content="{og_img}">',
    ]
    if tk.get("gsc_verification") and tk["gsc_verification"] != FILL:
        lines.append(f'<meta name="google-site-verification" content="{tk["gsc_verification"]}">')
    if tk.get("ga4_id") and tk["ga4_id"] != FILL:
        gid = tk["ga4_id"]
        lines.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>')
        lines.append("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
                     f"gtag('js',new Date());gtag('config','{gid}');</script>")
    return "\n".join(lines) + "\n"


def inject_head(html, page, config):
    return html.replace("</head>", head_block(page, config) + "</head>", 1)


def broker_footer_block(config):
    tk = config["tokens"]
    return (
        '<div class="broker-disclosure">'
        f'<p>{tk["business_name"]} &middot; License #{tk["license_number"]}</p>'
        f'<p>Brokered by {tk["broker_name"]} &middot; {tk["broker_office"]} &middot; '
        f'Broker: <a href="tel:{tk["broker_phone"]}">{tk["broker_phone"]}</a></p>'
        f'<p>{tk["broker_jurisdiction"]}</p>'
        "</div>"
    )


def inject_broker_footer(html, config):
    block = broker_footer_block(config)
    if "</div></footer>" in html:
        return html.replace("</div></footer>", block + "</div></footer>", 1)
    return html.replace("</footer>", block + "</footer>", 1)


def transform(html, page, config, css_hash):
    html = apply_nap(html, config)
    html = strip_demo(html)
    html = apply_noindex(html, config)
    html = hash_assets(html, css_hash)
    html = inject_head(html, page, config)
    html = inject_broker_footer(html, config)
    return html


def find_fill(html):
    """Return sorted unique context snippets around each __FILL__ occurrence."""
    hits = []
    for m in re.finditer(re.escape(FILL), html):
        s = max(0, m.start() - 40)
        e = min(len(html), m.end() + 8)
        snip = re.sub(r"\s+", " ", html[s:e]).strip()
        hits.append(snip.encode("ascii", "replace").decode("ascii"))
    return sorted(set(hits))


# --------------------------------------------------------------------------- #
# generated files
# --------------------------------------------------------------------------- #
def robots_txt(config, published):
    host = config["canonical_host"].rstrip("/")
    if config["flags"].get("strip_noindex"):
        return ("User-agent: *\n"
                "Allow: /\n"
                "Disallow: /audit/\n\n"
                f"Sitemap: {host}/sitemap.xml\n")
    return ("# Pre-launch / staging artifact — strip_noindex is false, so this\n"
            "# build must NOT be crawlable yet (CR-002). Flip strip_noindex to\n"
            "# true only at launch, after DNS cutover and all launch gates close.\n"
            "User-agent: *\n"
            "Disallow: /\n")


def sitemap_xml(config, published):
    urls = "".join(f"  <url><loc>{p['canonical']}</loc></url>\n" for p in published)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}</urlset>\n")


def page_404(config, css_hash):
    host = config["canonical_host"].rstrip("/")
    tk = config["tokens"]
    name = tk["business_name"] if tk["business_name"] != FILL else "Carrie Billeaud, Realtor"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | {name}</title>
<link rel="stylesheet" href="/assets/style.css?v={css_hash}">
<link rel="icon" href="{host}{config['favicon']}">
</head>
<body id="top">
<header class="site-header"><div class="wrap nav">
  <a class="brand-logo" href="/"><img src="/assets/img/carrie-logo.png" alt="{name}" height="40"></a>
</div></header>
<main id="main"><section class="section"><div class="wrap">
  <h1>That page moved or never existed</h1>
  <p>Let's get you back on track.</p>
  <p><a class="btn btn-gold" href="/">Return to the homepage</a></p>
</div></section></main>
<footer class="footer"><div class="wrap">
  <p>{name} &middot; eXp Realty &middot; Lafayette, Louisiana</p>
</div></footer>
</body></html>
"""


# --------------------------------------------------------------------------- #
# check mode
# --------------------------------------------------------------------------- #
def run_check(config, manifest):
    print("== CONFIG CHECK ==")
    unfilled = [k for k, v in config["tokens"].items() if v == FILL]
    for k, v in config["tokens"].items():
        print(f"  {'MISSING ' if v == FILL else 'ok      '} {k} = {v!r}")

    print("\n== MANIFEST CHECK ==")
    problems = []
    pages = manifest["pages"]
    for p in pages:
        src = SITE / p["path"]
        if not src.exists():
            problems.append(f"missing source file: {p['path']}")
        if not p["canonical"].startswith(config["canonical_host"]):
            problems.append(f"canonical host mismatch: {p['path']} -> {p['canonical']}")
    published = [p for p in pages if p.get("publish")]
    print(f"  marketing pages in manifest : {len(pages)}")
    print(f"  publish:true (launch set)   : {len(published)}")
    print(f"  held (publish:false)        : {len(pages) - len(published)}")
    for prob in problems:
        print(f"  PROBLEM: {prob}")

    print(f"\n== VERDICT ==")
    print(f"  strip_noindex = {config['flags']['strip_noindex']}  include_audit = {config['flags']['include_audit']}")
    if unfilled:
        print(f"  NOT launch-ready: {len(unfilled)} __FILL__ token(s) remain: {', '.join(unfilled)}")
    if problems:
        print(f"  NOT launch-ready: {len(problems)} manifest problem(s).")
    if not unfilled and not problems:
        print("  Config complete and manifest valid.")
        return 0
    return 1


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #
def run_build(config, manifest):
    css_bytes = (SITE / "assets" / "style.css").read_bytes()
    css_hash = hashlib.md5(css_bytes).hexdigest()[:8]

    pages = manifest["pages"]
    published = [p for p in pages if p.get("publish")]
    held = [p for p in pages if not p.get("publish")]

    # ---- pass 1: transform in memory + collect unresolved token hits ----
    rendered = {}
    gate_failures = {}
    for p in published:
        src = SITE / p["path"]
        if not src.exists():
            gate_failures[p["path"]] = [f"SOURCE MISSING: {src}"]
            continue
        out = transform(src.read_text(encoding="utf-8"), p, config, css_hash)
        hits = find_fill(out)
        if hits:
            gate_failures[p["path"]] = hits
        else:
            rendered[p["path"]] = out

    # ---- report ----
    print("=" * 68)
    print("PRODUCTION BUILD REPORT — carriebilleaud.com")
    print("=" * 68)
    print(f"asset content-hash (style.css) : v={css_hash}")
    print(f"strip_noindex flag             : {config['flags']['strip_noindex']}")
    print(f"pages in manifest              : {len(pages)}  "
          f"(publish:true={len(published)}, held={len(held)})")

    print(f"\nPAGES HELD ({len(held)}) — publish:false, excluded from dist/sitemap:")
    for p in held:
        print(f"  - {p['path']}: {p['approval_gate']}")

    if gate_failures:
        print(f"\n*** BUILD FAILED — TOKEN GATE TRIPPED ***")
        print(f"{len(gate_failures)} published page(s) would ship an unresolved "
              f"__FILL__ value. Nothing was written to dist/.")
        for path in sorted(gate_failures):
            print(f"\n  [{path}] unresolved:")
            for hit in gate_failures[path]:
                print(f"      … {hit}")
        print("\nResolve every __FILL__ token in build/production.config.json "
              "(canonical NAP + broker identity) and re-run. This refusal is the "
              "safety gate working as designed.")
        return 1

    # ---- pass 2: write dist/ (only reached when gate is clean) ----
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(SITE / "assets", DIST / "assets", dirs_exist_ok=True)

    for path, out in rendered.items():
        dest = DIST / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")

    (DIST / "robots.txt").write_text(robots_txt(config, published), encoding="utf-8")
    (DIST / "sitemap.xml").write_text(sitemap_xml(config, published), encoding="utf-8")
    (DIST / "404.html").write_text(page_404(config, css_hash), encoding="utf-8")

    print(f"\nPAGES EMITTED ({len(rendered)}):")
    for path in sorted(rendered):
        print(f"  + dist/{path}")
    print("  + dist/robots.txt")
    print(f"  + dist/sitemap.xml ({len(published)} urls)")
    print("  + dist/404.html")
    print("  + dist/assets/ (copied)")
    if not config["flags"]["strip_noindex"]:
        print("\nNOTE: strip_noindex=false — robots.txt emits Disallow:/ and pages "
              "keep noindex. This dist/ is a private pre-launch artifact.")
    print("\nBUILD OK.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Deterministic production build for carriebilleaud.com")
    ap.add_argument("--check", action="store_true",
                    help="validate config/manifest completeness without writing")
    args = ap.parse_args()

    try:  # keep the report printable on legacy Windows codepages (cp1252)
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass

    config = load_json(BUILD / "production.config.json")
    manifest = load_json(BUILD / "page_manifest.json")

    if args.check:
        return run_check(config, manifest)
    return run_build(config, manifest)


if __name__ == "__main__":
    sys.exit(main())
