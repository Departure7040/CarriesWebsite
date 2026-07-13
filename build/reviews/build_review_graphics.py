#!/usr/bin/env python3
"""Render branded "Client Love" review graphics from Carrie's REAL verified reviews.

Reads:   data/reviews.yaml                            (the verified review store)
         build/reviews/review_template.html           (1080x1080 feed square, self-contained)
         build/reviews/review_template_story.html     (1080x1920 story, self-contained)
Writes:  site/studio/packages/reviews/<slug>-square.png
         site/studio/packages/reviews/<slug>-story.png   (a SERVED path)

Same pattern as build/social/render_post.py: the Playfair Display webfont and Carrie's logo are
embedded as data URIs (nothing fetched at render time), tokens are filled by string replacement,
the page is served over a throwaway localhost, and the #root element is screenshotted directly
(not full_page) so output is exactly 1080x1080 / 1080x1920 CSS px at device_scale_factor=2 (@2x).

Compliance: quotes are reproduced VERBATIM from data/reviews.yaml (which is itself verbatim from
the page). A star rating is shown ONLY for reviews that carry a real rating (the Google cards);
unrated reviews get no stars. Long quotes are truncated at a WORD boundary with an ellipsis —
the wording up to the cut is never altered. Nothing is invented; Carrie approves before posting.

Re-runnable:

    python build/reviews/build_review_graphics.py
"""

import base64
import html
import http.server
import mimetypes
import re
import socket
import threading
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent.parent
REVIEWS_DIR = REPO / "build" / "reviews"
DATA = REPO / "data" / "reviews.yaml"
OUT_DIR = REPO / "site" / "studio" / "packages" / "reviews"
LOGO_PATH = REPO / "site" / "assets" / "img" / "carrie-logo.png"
FONT_PATH = REPO / "build" / "social" / "_fonts" / "playfair-latin.woff2"

SQUARE_TEMPLATE = REVIEWS_DIR / "review_template.html"
STORY_TEMPLATE = REVIEWS_DIR / "review_template_story.html"

# How many sample graphics to render, and the longest quote (chars) we'll place on a card
# before truncating at a word boundary. Keeps the square legible without rewording.
SAMPLE_COUNT = 3
MAX_QUOTE_CHARS = 240

SOURCE_LABELS = {
    "google": "Google Review",
    "zillow": "Zillow Review",
    "alignable": "Alignable Recommendation",
    "nextdoor": "Nextdoor Recommendation",
    "website": "Client Review",
}


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    mime = mime or "application/octet-stream"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def font_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def slugify(author: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", author.lower()).strip("-")
    return s or "review"


def truncate_verbatim(text: str, limit: int) -> str:
    """Truncate at a word boundary with an ellipsis; wording up to the cut is unchanged."""
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:—- ")
    return cut + "…"  # …


def source_label(review: dict) -> str:
    label = SOURCE_LABELS.get(review["source"], "Client Review")
    rating = review.get("rating")
    if rating is not None:
        stars = "★" * int(rating)  # ★
        return f"{stars} · {label}"
    return label


def pick_samples(reviews: list) -> list:
    """Favor the visibly-rated Google reviews, then fill with shorter quotes."""
    rated = [r for r in reviews if r.get("rating") is not None]
    rest = sorted(
        (r for r in reviews if r.get("rating") is None),
        key=lambda r: len(r["text"]),
    )
    ordered = rated + rest
    return ordered[:SAMPLE_COUNT]


def fill_template(template_text: str, review: dict, logo_uri: str, font_b64_str: str) -> str:
    quote = truncate_verbatim(review["text"], MAX_QUOTE_CHARS)
    html_out = template_text
    html_out = html_out.replace("{{FONT_PLAYFAIR_B64}}", font_b64_str)
    html_out = html_out.replace("{{LOGO_DATA_URI}}", logo_uri)
    html_out = html_out.replace("{{QUOTE}}", html.escape(quote, quote=False))
    html_out = html_out.replace("{{FIRST_NAME}}", html.escape(review["first_name"], quote=False))
    html_out = html_out.replace("{{SOURCE_LABEL}}", html.escape(source_label(review), quote=False))
    return html_out


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
    for p in (SQUARE_TEMPLATE, STORY_TEMPLATE, FONT_PATH, LOGO_PATH, DATA):
        if not p.exists():
            raise SystemExit(f"Required file not found: {p}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    reviews = yaml.safe_load(DATA.read_text(encoding="utf-8"))["reviews"]
    samples = pick_samples(reviews)

    logo_uri = data_uri(LOGO_PATH)
    fb64 = font_b64(FONT_PATH)
    square_src = SQUARE_TEMPLATE.read_text(encoding="utf-8")
    story_src = STORY_TEMPLATE.read_text(encoding="utf-8")

    port = free_port()
    httpd = serve_dir(REVIEWS_DIR, port)

    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(device_scale_factor=2)

            for review in samples:
                slug = slugify(review["author"])
                square_html = fill_template(square_src, review, logo_uri, fb64)
                story_html = fill_template(story_src, review, logo_uri, fb64)

                square_tmp = REVIEWS_DIR / f"_render_{slug}_square.html"
                story_tmp = REVIEWS_DIR / f"_render_{slug}_story.html"
                square_tmp.write_text(square_html, encoding="utf-8")
                story_tmp.write_text(story_html, encoding="utf-8")

                square_out = OUT_DIR / f"{slug}-square.png"
                story_out = OUT_DIR / f"{slug}-story.png"

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
