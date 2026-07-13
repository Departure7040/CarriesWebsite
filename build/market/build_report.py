#!/usr/bin/env python3
"""
Build the branded Acadiana Market Report PDF from a market data YAML.

Reads:   data/market/<period>.yaml   (default: data/market/2026-07-sample.yaml)
         build/market/market-report-print.html   (the print template)
Writes:  site/market/acadiana-market-report-<YYYY-MM>.pdf

Mirrors build/build_ebook.py exactly: serve the filled HTML over a throwaway
localhost http.server, render with Chromium in "print" media emulation, Letter
size, CSS page size preferred, backgrounds on.

NEVER-FABRICATE CONTRACT
------------------------
Every number in the PDF comes ONLY from the YAML. The template has zero
hardcoded statistics; it is all {{TOKENS}}. A metric missing from the YAML
renders as an em-dash ("—"), never an invented value. When the YAML has
`sample: true`, a visible "SAMPLE — illustrative data" ribbon is stamped on the
cover and repeated on every page, and the disclaimer string is printed.

Re-runnable. Usage:

    python build/market/build_report.py
    python build/market/build_report.py data/market/2026-08.yaml
"""

import base64
import html
import http.server
import re
import socket
import sys
import threading
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent.parent
SRC_HTML = REPO / "build" / "market" / "market-report-print.html"
LOGO = REPO / "site" / "assets" / "img" / "carrie-logo.png"
DEFAULT_YAML = REPO / "data" / "market" / "2026-07-sample.yaml"
OUT_DIR = REPO / "site" / "market"

DASH = "—"  # em-dash for any missing metric

# Town display order for the by-area table.
AREA_ORDER = [
    "Lafayette", "Youngsville", "Broussard", "Carencro",
    "Scott", "Maurice", "Milton",
]

# Metric column order for the by-area table (key, formatter-name).
TABLE_COLS = [
    ("median_sale_price", "money"),
    ("closed_sales", "int"),
    ("avg_days_on_market", "int"),
    ("active_inventory", "int"),
    ("months_of_supply", "num"),
    ("median_price_per_sqft", "money"),
]


# ---------------------------------------------------------------- formatters
def fmt_money(v):
    if v is None or v == "":
        return DASH
    try:
        return "$" + f"{round(float(v)):,}"
    except (TypeError, ValueError):
        return DASH


def fmt_int(v):
    if v is None or v == "":
        return DASH
    try:
        return f"{round(float(v)):,}"
    except (TypeError, ValueError):
        return DASH


def fmt_num(v):
    """A small number that may be fractional (e.g. months of supply)."""
    if v is None or v == "":
        return DASH
    try:
        f = float(v)
        return f"{f:g}"
    except (TypeError, ValueError):
        return DASH


FORMATTERS = {"money": fmt_money, "int": fmt_int, "num": fmt_num}


def fmt(key, value):
    formatter = dict(TABLE_COLS).get(key, "int")
    return FORMATTERS[formatter](value)


# ---------------------------------------------------------------- prose
def build_means_prose(area, period, source, metrics):
    """
    Facts-only, COMPLIANT restatement of the supplied numbers.
    No predictions, no guarantees, no steering, no "great time to buy".
    Only sentences for metrics actually present in the YAML are emitted.
    """
    paras = []
    lead = (
        f"For {html.escape(area)} in {html.escape(period)}, here is what the "
        f"reported figures show, drawn from {html.escape(source)}."
    )
    paras.append(lead)

    price = metrics.get("median_sale_price")
    dom = metrics.get("avg_days_on_market")
    closed = metrics.get("closed_sales")
    inv = metrics.get("active_inventory")
    mos = metrics.get("months_of_supply")
    ppsf = metrics.get("median_price_per_sqft")

    # Buyers paragraph — restate inventory / DOM / supply as facts.
    buyer_bits = []
    if inv not in (None, ""):
        buyer_bits.append(
            f"there were {fmt_int(inv)} active listings on the market"
        )
    if dom not in (None, ""):
        buyer_bits.append(
            f"a home that sold took about {fmt_int(dom)} days on the market, on average"
        )
    if mos not in (None, ""):
        buyer_bits.append(
            f"inventory stood at {fmt_num(mos)} months of supply"
        )
    if buyer_bits:
        paras.append(
            "<strong>For buyers:</strong> During this period, "
            + _join(buyer_bits)
            + ". These are counts and averages for the period, not a forecast; "
            "what they mean for a specific search depends on the home, price "
            "range, and your financing and timeline."
        )

    # Sellers paragraph — restate price / closed / price-per-sqft as facts.
    seller_bits = []
    if price not in (None, ""):
        seller_bits.append(f"the median sale price was {fmt_money(price)}")
    if ppsf not in (None, ""):
        seller_bits.append(
            f"the median price per square foot was {fmt_money(ppsf)}"
        )
    if closed not in (None, ""):
        seller_bits.append(f"{fmt_int(closed)} sales closed")
    if seller_bits:
        paras.append(
            "<strong>For sellers:</strong> "
            + _cap(_join(seller_bits))
            + " for the period. A median is a midpoint across many different "
            "homes; the right list price for any one property depends on its "
            "condition, location, and the current comparable sales, which Carrie "
            "can review with you."
        )

    return "\n  ".join(f"<p>{p}</p>" for p in paras)


def _join(bits):
    if len(bits) == 1:
        return bits[0]
    if len(bits) == 2:
        return bits[0] + " and " + bits[1]
    return ", ".join(bits[:-1]) + ", and " + bits[-1]


def _cap(s):
    return s[:1].upper() + s[1:] if s else s


# ---------------------------------------------------------------- period slug
def period_slug(period):
    """'July 2026' -> '2026-07'. Falls back to a safe slug of the string."""
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


# ---------------------------------------------------------------- serving
def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def serve_dir(directory, port):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(directory), **k
    )
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


# ---------------------------------------------------------------- main
def main():
    yaml_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_YAML
    if not yaml_path.exists():
        raise SystemExit(f"Market data YAML not found: {yaml_path}")
    if not SRC_HTML.exists():
        raise SystemExit(f"Source HTML not found: {SRC_HTML}")

    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    is_sample = bool(data.get("sample", False))
    period = str(data.get("period", "") or "")
    area = str(data.get("area", "") or "")
    raw_source = str(data.get("source", "") or "").strip()
    # Never name an unverified / unfilled source.
    if not raw_source or raw_source.startswith("__FILL__"):
        source = "(source pending)"
    else:
        source = raw_source
    disclaimer = str(data.get("disclaimer", "") or "")
    metrics = data.get("metrics") or {}
    by_area = data.get("by_area") or {}

    # Logo -> data URI (embed at build time; mirrors render_post.py).
    if LOGO.exists():
        logo_b64 = base64.b64encode(LOGO.read_bytes()).decode("ascii")
        logo_src = f"data:image/png;base64,{logo_b64}"
    else:
        logo_src = ""

    # Build the by-area table rows (towns present in YAML, ordered).
    towns = [t for t in AREA_ORDER if t in by_area]
    towns += [t for t in by_area if t not in AREA_ORDER]  # any extras, appended
    rows = []
    for town in towns:
        m = by_area.get(town) or {}
        cells = "".join(
            f"<td>{html.escape(fmt(key, m.get(key)))}</td>"
            for key, _ in TABLE_COLS
        )
        rows.append(f"<tr><td>{html.escape(str(town))}</td>{cells}</tr>")
    if not rows:
        rows.append(
            f'<tr><td colspan="{len(TABLE_COLS) + 1}">'
            f"No by-area data supplied.</td></tr>"
        )
    by_area_rows = "\n      ".join(rows)

    means_prose = build_means_prose(area or "the area", period or "this period",
                                    source, metrics)

    replacements = {
        "{{PERIOD}}": html.escape(period) or DASH,
        "{{AREA}}": html.escape(area) or DASH,
        "{{SOURCE}}": html.escape(source),
        "{{DISCLAIMER}}": html.escape(disclaimer),
        "{{SAMPLE_CLASS}}": "sample" if is_sample else "",
        "{{LOGO_SRC}}": logo_src,
        "{{MEDIAN_SALE_PRICE}}": fmt_money(metrics.get("median_sale_price")),
        "{{AVG_DAYS_ON_MARKET}}": fmt_int(metrics.get("avg_days_on_market")),
        "{{ACTIVE_INVENTORY}}": fmt_int(metrics.get("active_inventory")),
        "{{CLOSED_SALES}}": fmt_int(metrics.get("closed_sales")),
        "{{MONTHS_OF_SUPPLY}}": fmt_num(metrics.get("months_of_supply")),
        "{{MEDIAN_PRICE_PER_SQFT}}": fmt_money(metrics.get("median_price_per_sqft")),
        "{{BY_AREA_ROWS}}": by_area_rows,
        "{{MEANS_PROSE}}": means_prose,
    }

    filled = SRC_HTML.read_text(encoding="utf-8")
    for token, value in replacements.items():
        filled = filled.replace(token, value)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_pdf = OUT_DIR / f"acadiana-market-report-{period_slug(period)}.pdf"

    # Serve the filled HTML from a temp file in the template dir so relative
    # semantics match build_ebook.py.
    tmp_name = f".market-report-filled-{period_slug(period)}.html"
    tmp_html = SRC_HTML.parent / tmp_name
    tmp_html.write_text(filled, encoding="utf-8")

    port = free_port()
    httpd = serve_dir(SRC_HTML.parent, port)
    url = f"http://127.0.0.1:{port}/{tmp_name}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="load")
            page.emulate_media(media="print")
            page.pdf(
                path=str(out_pdf),
                format="Letter",
                print_background=True,
                prefer_css_page_size=True,
            )
            browser.close()
    finally:
        httpd.shutdown()
        try:
            tmp_html.unlink()
        except OSError:
            pass

    size_kb = out_pdf.stat().st_size / 1024
    print("Acadiana Market Report — build summary")
    print(f"  data source : {yaml_path.relative_to(REPO)}")
    print(f"  sample flag : {is_sample}")
    print(f"  period      : {period}")
    print(f"  attribution : {source}")
    print(f"  towns        : {', '.join(towns) if towns else '(none)'}")
    print(f"  output      : {out_pdf.relative_to(REPO)}  ({size_kb:.1f} KB)")
    if is_sample:
        print("  NOTE: sample:true — SAMPLE ribbon stamped; do not present as real.")


if __name__ == "__main__":
    main()
