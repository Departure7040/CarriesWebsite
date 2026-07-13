#!/usr/bin/env python3
"""
Render branded "Just Listed" social graphics for real Carrie Billeaud listings.

Reads:   build/social/post_template.html        (1080x1080 feed square, self-contained)
         build/social/post_template_story.html   (1080x1920 story, self-contained)
Writes:  build/social/out/<slug>-square.png
         build/social/out/<slug>-story.png

Pure-Python, Playwright-based. For each hardcoded listing, the matching
property photo and Carrie's logo are embedded into the template as data
URIs (along with the Playfair Display webfont, also embedded as a data
URI so nothing is fetched over the network at render time), the tokens
are filled by string replacement, and the page is rendered via a
throwaway local http.server (so relative/data-URI resources resolve like
a normal navigation). The #root element is screenshotted directly (not
full_page) so output is exactly 1080x1080 / 1080x1920 CSS pixels, at
device_scale_factor=2 for a crisp @2x PNG.

Re-runnable — re-run any time the template or listing data changes:

    python build/social/render_post.py
"""

import base64
import http.server
import mimetypes
import socket
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent.parent
SOCIAL_DIR = REPO / "build" / "social"
OUT_DIR = SOCIAL_DIR / "out"
LISTINGS_DIR = REPO / "site" / "assets" / "img" / "listings"
LOGO_PATH = REPO / "site" / "assets" / "img" / "carrie-logo.png"
FONT_PATH = SOCIAL_DIR / "_fonts" / "playfair-latin.woff2"

SQUARE_TEMPLATE = SOCIAL_DIR / "post_template.html"
STORY_TEMPLATE = SOCIAL_DIR / "post_template_story.html"

LABEL = "JUST LISTED"

# Three real active listings (from data/realtor_active_listings_snapshot_2026-07-08.json)
LISTINGS = [
    {
        "slug": "204-ivy-cottage-dr",
        "photo": "204-ivy-cottage-dr.jpg",
        "price": "$1,510,000",
        "address": "204 Ivy Cottage Dr",
        "city": "Youngsville, LA",
        "beds": 4,
        "baths": "3.5",
        "sqft": 3918,
    },
    {
        "slug": "101-rio-ridge-dr",
        "photo": "101-rio-ridge-dr.jpg",
        "price": "$3,400,000",
        "address": "101 Rio Ridge Dr",
        "city": "Lafayette, LA",
        "beds": 5,
        "baths": "5.5",
        "sqft": 6800,
    },
    {
        "slug": "205-queenstown-ave",
        "photo": "205-queenstown-ave.jpg",
        "price": "$465,000",
        "address": "205 Queenstown Ave",
        "city": "Youngsville, LA",
        "beds": 4,
        "baths": "2",
        "sqft": 2202,
    },
]


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    mime = mime or "application/octet-stream"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def font_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def specs_html(listing: dict) -> str:
    dot = '<span class="dot">&middot;</span>'
    parts = [
        f"{listing['beds']} BD",
        f"{listing['baths']} BA",
        f"{listing['sqft']:,} SQFT",
    ]
    return f" {dot} ".join(parts)


def fill_template(template_text: str, listing: dict, logo_uri: str, font_b64_str: str) -> str:
    photo_path = LISTINGS_DIR / listing["photo"]
    html = template_text
    html = html.replace("{{FONT_PLAYFAIR_B64}}", font_b64_str)
    html = html.replace("{{PHOTO_DATA_URI}}", data_uri(photo_path))
    html = html.replace("{{LOGO_DATA_URI}}", logo_uri)
    html = html.replace("{{LABEL}}", LABEL)
    html = html.replace("{{PRICE}}", listing["price"])
    html = html.replace("{{ADDRESS}}", listing["address"])
    html = html.replace("{{CITY}}", listing["city"])
    html = html.replace("{{SPECS}}", specs_html(listing))
    return html


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def serve_dir(directory: Path, port: int) -> http.server.ThreadingHTTPServer:
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(
        *args, directory=str(directory), **kwargs
    )
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def render_png(page, html_path: Path, port: int, width: int, height: int, out_path: Path) -> None:
    url = f"http://127.0.0.1:{port}/{html_path.name}"
    page.set_viewport_size({"width": width, "height": height})
    page.goto(url, wait_until="load")
    page.wait_for_timeout(150)  # let the embedded webfont paint before screenshot
    root = page.locator("#root")
    root.screenshot(path=str(out_path))


def main() -> None:
    if not SQUARE_TEMPLATE.exists() or not STORY_TEMPLATE.exists():
        raise SystemExit("Template HTML not found under build/social/")
    if not FONT_PATH.exists():
        raise SystemExit(f"Font not found: {FONT_PATH}")
    if not LOGO_PATH.exists():
        raise SystemExit(f"Logo not found: {LOGO_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    logo_uri = data_uri(LOGO_PATH)
    fb64 = font_b64(FONT_PATH)
    square_src = SQUARE_TEMPLATE.read_text(encoding="utf-8")
    story_src = STORY_TEMPLATE.read_text(encoding="utf-8")

    # Filled HTML is written to temp files alongside the templates so the
    # local server can serve them (data URIs make them fully self-contained).
    port = free_port()
    httpd = serve_dir(SOCIAL_DIR, port)

    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(device_scale_factor=2)

            for listing in LISTINGS:
                photo_path = LISTINGS_DIR / listing["photo"]
                if not photo_path.exists():
                    raise SystemExit(f"Listing photo not found: {photo_path}")

                square_html = fill_template(square_src, listing, logo_uri, fb64)
                story_html = fill_template(story_src, listing, logo_uri, fb64)

                square_tmp = SOCIAL_DIR / f"_render_{listing['slug']}_square.html"
                story_tmp = SOCIAL_DIR / f"_render_{listing['slug']}_story.html"
                square_tmp.write_text(square_html, encoding="utf-8")
                story_tmp.write_text(story_html, encoding="utf-8")

                square_out = OUT_DIR / f"{listing['slug']}-square.png"
                story_out = OUT_DIR / f"{listing['slug']}-story.png"

                render_png(page, square_tmp, port, 1080, 1080, square_out)
                render_png(page, story_tmp, port, 1080, 1920, story_out)

                square_tmp.unlink()
                story_tmp.unlink()

                results.append(square_out)
                results.append(story_out)

            browser.close()
    finally:
        httpd.shutdown()

    for path in results:
        size_kb = path.stat().st_size / 1024
        print(f"Wrote {path}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
