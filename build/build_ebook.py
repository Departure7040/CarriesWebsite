#!/usr/bin/env python3
"""
Render the Acadiana Home Buyer's & Seller's Guide print HTML to PDF.

Reads:   build/ebook/acadiana-home-guide-print.html
                (self-contained: all CSS inlined, logo embedded as a data URI)
Writes:  site/guides/acadiana-home-guide.pdf
                (the hosted path the "get the guide" form links to)

Pure-Python, Playwright-based. Serves the source HTML over a throwaway local
http.server (rather than file://) so page load semantics match a normal
navigation and any relative asset paths resolve reliably, then renders with
Chromium in "print" media emulation, Letter size, CSS page size preferred,
and backgrounds enabled so the cover/back-cover bands and callout boxes
render as designed.

Re-run any time the source HTML changes:

    python build/build_ebook.py
"""

import http.server
import socket
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
SRC_HTML = REPO / "build" / "ebook" / "acadiana-home-guide-print.html"
OUT_PDF = REPO / "site" / "guides" / "acadiana-home-guide.pdf"


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


def main() -> None:
    if not SRC_HTML.exists():
        raise SystemExit(f"Source HTML not found: {SRC_HTML}")

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    port = free_port()
    httpd = serve_dir(SRC_HTML.parent, port)
    url = f"http://127.0.0.1:{port}/{SRC_HTML.name}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="load")
            page.emulate_media(media="print")
            page.pdf(
                path=str(OUT_PDF),
                format="Letter",
                print_background=True,
                prefer_css_page_size=True,
            )
            browser.close()
    finally:
        httpd.shutdown()

    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"Wrote {OUT_PDF}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
