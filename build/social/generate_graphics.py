#!/usr/bin/env python3
"""
generate_graphics.py — reusable branded social-graphic generator for Carrie Billeaud.

Productionized from the render_post.py POC. Takes ONE listing (dict) and renders
BOTH the 1080x1080 feed square and the 1080x1920 story as branded PNGs into
build/social/out/<slug>-square.png and -story.png, at device_scale_factor=2.

Reuses the existing luxury templates (post_template.html / post_template_story.html)
via token replacement, embedding the property photo + Carrie's logo + the Playfair
webfont as data URIs so the render fetches nothing over the network.

COMPLIANCE: the graphic carries FACTS ONLY — price / beds / baths / sqft / address /
"JUST LISTED". No steering or fair-housing-sensitive language is ever composited.

Two ways to use it:

  # CLI — one listing
  python build/social/generate_graphics.py \
      --slug 204-ivy-cottage-dr --price '$1,510,000' \
      --address '204 Ivy Cottage Dr' --city 'Youngsville, LA' \
      --beds 4 --baths 3.5 --sqft 3918 \
      --photo site/assets/img/listings/204-ivy-cottage-dr.jpg

  # Importable — orchestrator calls this directly
  from build.social.generate_graphics import generate_graphics
  square_png, story_png = generate_graphics({
      "slug": "204-ivy-cottage-dr", "price": "$1,510,000",
      "address": "204 Ivy Cottage Dr", "city": "Youngsville, LA",
      "beds": 4, "baths": "3.5", "sqft": 3918,
      "photo": "https://.../photo.jpg",   # local path OR https URL
  })

The photo may be a local filesystem path OR an https URL (downloaded to a temp file).
"""

import argparse
import base64
import http.server
import mimetypes
import os
import re
import socket
import tempfile
import threading
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent.parent
SOCIAL_DIR = REPO / "build" / "social"
OUT_DIR = SOCIAL_DIR / "out"
LOGO_PATH = REPO / "site" / "assets" / "img" / "carrie-logo.png"
FONT_PATH = SOCIAL_DIR / "_fonts" / "playfair-latin.woff2"

SQUARE_TEMPLATE = SOCIAL_DIR / "post_template.html"
STORY_TEMPLATE = SOCIAL_DIR / "post_template_story.html"

DEFAULT_LABEL = "JUST LISTED"


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    mime = mime or "application/octet-stream"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s or "listing"


def _specs_html(listing: dict) -> str:
    dot = '<span class="dot">&middot;</span>'
    sqft = listing["sqft"]
    sqft_str = f"{int(sqft):,}" if str(sqft).replace(",", "").isdigit() else str(sqft)
    parts = [f"{listing['beds']} BD", f"{listing['baths']} BA", f"{sqft_str} SQFT"]
    return f" {dot} ".join(parts)


def _fill_template(template_text: str, listing: dict, photo_uri: str,
                   logo_uri: str, font_b64: str, label: str) -> str:
    html = template_text
    html = html.replace("{{FONT_PLAYFAIR_B64}}", font_b64)
    html = html.replace("{{PHOTO_DATA_URI}}", photo_uri)
    html = html.replace("{{LOGO_DATA_URI}}", logo_uri)
    html = html.replace("{{LABEL}}", label)
    html = html.replace("{{PRICE}}", str(listing["price"]))
    html = html.replace("{{ADDRESS}}", str(listing["address"]))
    html = html.replace("{{CITY}}", str(listing["city"]))
    html = html.replace("{{SPECS}}", _specs_html(listing))
    return html


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _serve_dir(directory: Path, port: int) -> http.server.ThreadingHTTPServer:
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(directory), **k
    )
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def _render_png(page, html_path: Path, port: int, width: int, height: int, out_path: Path) -> None:
    url = f"http://127.0.0.1:{port}/{html_path.name}"
    page.set_viewport_size({"width": width, "height": height})
    page.goto(url, wait_until="load")
    page.wait_for_timeout(150)  # let the embedded webfont paint before screenshot
    page.locator("#root").screenshot(path=str(out_path))


def _resolve_photo(photo: str) -> tuple[Path, Path | None]:
    """Return (local_path, tempfile_to_cleanup_or_None). Handles path or https URL."""
    if str(photo).lower().startswith(("http://", "https://")):
        suffix = Path(str(photo).split("?")[0]).suffix or ".jpg"
        fd, tmp_name = tempfile.mkstemp(suffix=suffix, prefix="listing_photo_")
        os.close(fd)  # close the OS handle so Windows can later unlink the file
        tmp = Path(tmp_name)
        urllib.request.urlretrieve(photo, tmp)  # noqa: S310 (trusted feed url)
        return tmp, tmp
    p = Path(photo)
    if not p.is_absolute():
        p = (REPO / p).resolve()
    if not p.exists():
        raise SystemExit(f"Listing photo not found: {p}")
    return p, None


def generate_graphics(listing: dict, label: str = DEFAULT_LABEL,
                      out_dir: Path = OUT_DIR) -> tuple[Path, Path]:
    """Render both branded PNGs for one listing. Returns (square_path, story_path).

    listing keys: price, address, city, beds, baths, sqft, photo (path OR https url),
    and optionally slug (derived from address if absent).
    """
    for f in (SQUARE_TEMPLATE, STORY_TEMPLATE, FONT_PATH, LOGO_PATH):
        if not f.exists():
            raise SystemExit(f"Required asset missing: {f}")

    slug = listing.get("slug") or _slugify(listing["address"])
    out_dir.mkdir(parents=True, exist_ok=True)

    photo_path, tmp_to_clean = _resolve_photo(listing["photo"])
    try:
        photo_uri = data_uri(photo_path)
        logo_uri = data_uri(LOGO_PATH)
        font_b64 = base64.b64encode(FONT_PATH.read_bytes()).decode("ascii")

        square_src = SQUARE_TEMPLATE.read_text(encoding="utf-8")
        story_src = STORY_TEMPLATE.read_text(encoding="utf-8")

        square_html = _fill_template(square_src, listing, photo_uri, logo_uri, font_b64, label)
        story_html = _fill_template(story_src, listing, photo_uri, logo_uri, font_b64, label)

        square_tmp = SOCIAL_DIR / f"_render_{slug}_square.html"
        story_tmp = SOCIAL_DIR / f"_render_{slug}_story.html"
        square_tmp.write_text(square_html, encoding="utf-8")
        story_tmp.write_text(story_html, encoding="utf-8")

        square_out = out_dir / f"{slug}-square.png"
        story_out = out_dir / f"{slug}-story.png"

        port = _free_port()
        httpd = _serve_dir(SOCIAL_DIR, port)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(device_scale_factor=2)
                _render_png(page, square_tmp, port, 1080, 1080, square_out)
                _render_png(page, story_tmp, port, 1080, 1920, story_out)
                browser.close()
        finally:
            httpd.shutdown()
            square_tmp.unlink(missing_ok=True)
            story_tmp.unlink(missing_ok=True)

        return square_out, story_out
    finally:
        if tmp_to_clean is not None:
            tmp_to_clean.unlink(missing_ok=True)


def _parse_args() -> dict:
    ap = argparse.ArgumentParser(description="Render branded social graphics for one listing.")
    ap.add_argument("--price", required=True)
    ap.add_argument("--address", required=True)
    ap.add_argument("--city", required=True)
    ap.add_argument("--beds", required=True)
    ap.add_argument("--baths", required=True)
    ap.add_argument("--sqft", required=True)
    ap.add_argument("--photo", required=True, help="local path or https URL")
    ap.add_argument("--slug", default=None)
    ap.add_argument("--label", default=DEFAULT_LABEL)
    a = ap.parse_args()
    return vars(a)


def main() -> None:
    args = _parse_args()
    label = args.pop("label")
    square, story = generate_graphics(args, label=label)
    for path in (square, story):
        print(f"Wrote {path}  ({path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
