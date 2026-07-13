#!/usr/bin/env python3
"""Render a branded vertical "Just Listed" SHORT (9:16) from a real listing.

"AI video from content, done right": we NEVER fabricate a house. We frame Carrie's
REAL listing photo(s) inside a branded motion template — a charcoal/ivory/gold
intro card, a cinematic Ken-Burns push over the photo with a facts-only lower
third, and a contact outro card — then hand it to her for approval. Same
compliance posture as the graphics engine: only the listing's given facts
(price, address, beds/baths/sqft) ever appear; no steering, no guarantees.

Pipeline:
  1. Playwright renders three 1080x1920 overlay cards to PNG (reusing the same
     data-URI/self-contained/local-server trick as render_post.py): an opaque
     intro card, a TRANSPARENT lower-third, and an opaque outro card. Her
     signature logo (black-on-transparent) is CSS-inverted to ivory for the
     dark cards.
  2. ffmpeg assembles: intro -> [blurred-fill bg + centered sharp photo with a
     slow zoom + lower third] -> outro, cross-faded, 1080x1920 @30fps, silent
     (drop in a licensed music bed before posting).

Output: site/studio/packages/videos/<slug>-short.mp4  (studio packages are
gitignored — regenerate with this script).

Production note: a real run pans across the FULL listing gallery (8-15 photos);
this sample uses the single cached hero photo we already store per listing.

    python build/social/build_listing_video.py            # renders the default sample listing
    python build/social/build_listing_video.py 101-rio-ridge-dr
"""

import base64
import http.server
import mimetypes
import socket
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent.parent
LISTINGS_DIR = REPO / "site" / "assets" / "img" / "listings"
LOGO_PATH = REPO / "site" / "assets" / "img" / "carrie-logo.png"
FONT_PATH = REPO / "build" / "social" / "_fonts" / "playfair-latin.woff2"
OUT_DIR = REPO / "site" / "studio" / "packages" / "videos"

LABEL = "JUST LISTED"

# The same real active listings used by render_post.py (hero photo per slug).
LISTINGS = {
    "204-ivy-cottage-dr": {
        "photo": "204-ivy-cottage-dr.jpg", "price": "$1,510,000",
        "address": "204 Ivy Cottage Dr", "city": "Youngsville, LA",
        "beds": 4, "baths": "3.5", "sqft": 3918,
    },
    "101-rio-ridge-dr": {
        "photo": "101-rio-ridge-dr.jpg", "price": "$3,400,000",
        "address": "101 Rio Ridge Dr", "city": "Lafayette, LA",
        "beds": 5, "baths": "5.5", "sqft": 6800,
    },
    "205-queenstown-ave": {
        "photo": "205-queenstown-ave.jpg", "price": "$465,000",
        "address": "205 Queenstown Ave", "city": "Youngsville, LA",
        "beds": 4, "baths": "2", "sqft": 2202,
    },
}

# Segment durations (seconds) and cross-fade.
T_INTRO, T_PHOTO, T_OUTRO, XF = 2.0, 6.5, 2.5, 0.4


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime or 'application/octet-stream'};base64,{b64}"


def font_b64() -> str:
    return base64.b64encode(FONT_PATH.read_bytes()).decode("ascii")


def specs(listing: dict) -> str:
    return f"{listing['beds']} BD &middot; {listing['baths']} BA &middot; {listing['sqft']:,} SQFT"


# --- Card HTML (self-contained; charcoal/ivory/gold, Playfair display) ------- #
_BASE_CSS = """
  :root{--ink:#12151c;--ivory:#faf7f2;--gold:#c9a24b;--muted:#aeb6c0;}
  @font-face{font-family:'Playfair';src:url(data:font/woff2;base64,{FONT}) format('woff2');font-weight:400 800;}
  *{margin:0;padding:0;box-sizing:border-box}
  #root{width:1080px;height:1920px;position:relative;overflow:hidden;
    font-family:'Helvetica Neue',Arial,sans-serif;-webkit-font-smoothing:antialiased}
  .serif{font-family:'Playfair',Georgia,serif}
  .logo{filter:invert(1) brightness(1.08);opacity:.92}
  .kick{color:var(--gold);letter-spacing:.42em;font-size:30px;font-weight:700;text-transform:uppercase}
  .rule{width:120px;height:2px;background:var(--gold);border:0}
"""


def intro_html(listing: dict, logo: str, font: str) -> str:
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{_BASE_CSS.replace('{FONT}', font)}
  #root{{background:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;text-align:center;padding:0 90px}}
  .price{{color:var(--ivory);font-size:150px;line-height:1;letter-spacing:-.01em}}
  .addr{{color:var(--ivory);font-size:52px;letter-spacing:.01em}}
  .city{{color:var(--muted);font-size:38px;letter-spacing:.16em;text-transform:uppercase;margin-top:6px}}
  .specs{{color:var(--gold);font-size:34px;letter-spacing:.14em;margin-top:10px}}
  .foot{{position:absolute;bottom:120px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:16px}}
  .foot img{{height:78px}}
  .foot .sub{{color:var(--muted);font-size:26px;letter-spacing:.24em;text-transform:uppercase}}
</style></head><body><div id=root>
  <div class=kick>{LABEL}</div>
  <hr class=rule>
  <div class="serif price">{listing['price']}</div>
  <div><div class="serif addr">{listing['address']}</div><div class=city>{listing['city']}</div></div>
  <div class=specs>{specs(listing)}</div>
  <div class=foot><img class=logo src="{logo}"><div class=sub>REALTOR&reg; &middot; eXp Realty</div></div>
</div></body></html>"""


def lowerthird_html(listing: dict, font: str) -> str:
    # Transparent card; content + scrim anchored to the bottom third.
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{_BASE_CSS.replace('{FONT}', font)}
  #root{{background:transparent}}
  .scrim{{position:absolute;left:0;right:0;bottom:0;height:760px;
    background:linear-gradient(to top,rgba(18,21,28,.94) 8%,rgba(18,21,28,.72) 42%,rgba(18,21,28,0) 100%)}}
  .lt{{position:absolute;left:80px;right:80px;bottom:150px}}
  .lt .kick{{font-size:28px;margin-bottom:18px}}
  .lt .price{{color:var(--ivory);font-size:112px;line-height:1;letter-spacing:-.01em}}
  .lt .addr{{color:var(--ivory);font-size:46px;margin-top:14px}}
  .lt .city{{color:var(--muted);font-size:32px;letter-spacing:.14em;text-transform:uppercase;margin-top:4px}}
  .lt .specs{{color:var(--gold);font-size:32px;letter-spacing:.12em;margin-top:20px}}
</style></head><body><div id=root>
  <div class=scrim></div>
  <div class=lt>
    <div class=kick>{LABEL}</div>
    <div class="serif price">{listing['price']}</div>
    <div class="serif addr">{listing['address']}</div>
    <div class=city>{listing['city']}</div>
    <div class=specs>{specs(listing)}</div>
  </div>
</div></body></html>"""


def outro_html(logo: str, font: str) -> str:
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{_BASE_CSS.replace('{FONT}', font)}
  #root{{background:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;text-align:center;padding:0 90px}}
  .logo{{height:150px}}
  .name{{color:var(--ivory);font-size:60px;letter-spacing:.02em}}
  .sub{{color:var(--muted);font-size:32px;letter-spacing:.22em;text-transform:uppercase}}
  .cta{{color:var(--ivory);font-size:44px;letter-spacing:.02em;margin-top:8px}}
  .phone{{color:var(--gold);font-size:58px;letter-spacing:.03em}}
</style></head><body><div id=root>
  <img class=logo src="{logo}">
  <div class="serif name">Carrie Billeaud</div>
  <div class=sub>REALTOR&reg; &middot; eXp Realty &middot; Acadiana</div>
  <hr class=rule>
  <div class="serif cta">Schedule a private showing</div>
  <div class=phone>337-258-5379</div>
</div></body></html>"""


# --- Playwright render ------------------------------------------------------- #
def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0)); return s.getsockname()[1]


def serve_dir(directory: Path, port: int):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(directory), **k)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render_cards(listing: dict, work: Path) -> dict:
    logo = data_uri(LOGO_PATH)
    font = font_b64()
    cards = {
        "intro": intro_html(listing, logo, font),
        "lowerthird": lowerthird_html(listing, font),
        "outro": outro_html(logo, font),
    }
    port = free_port()
    httpd = serve_dir(work, port)
    out = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
            for name, html in cards.items():
                (work / f"{name}.html").write_text(html, encoding="utf-8")
                page.goto(f"http://127.0.0.1:{port}/{name}.html", wait_until="load")
                page.wait_for_timeout(150)
                png = work / f"{name}.png"
                # lower third must keep its transparency for the ffmpeg overlay
                page.locator("#root").screenshot(path=str(png), omit_background=(name == "lowerthird"))
                out[name] = png
            browser.close()
    finally:
        httpd.shutdown()
    return out


# --- ffmpeg assembly --------------------------------------------------------- #
def run(cmd: list):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2500:])
        raise SystemExit(f"ffmpeg failed ({' '.join(cmd[:2])} ...)")


def kenburns_card(png: Path, dur: float, out: Path):
    """Static branded card -> mp4 with a very subtle push, so it breathes."""
    vf = (f"fps=30,scale=1150:2044,zoompan=z='min(pzoom+0.00035,1.05)':d=1:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p")
    run(["ffmpeg", "-y", "-loop", "1", "-t", f"{dur}", "-i", str(png),
         "-vf", vf, "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-r", "30", str(out)])


def photo_segment(photo: Path, lt: Path, dur: float, out: Path):
    """Blurred-fill bg + centered sharp photo with a slow Ken-Burns push + lower third."""
    fc = (
        "[0:v]split=2[bgsrc][fgsrc];"
        "[bgsrc]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=26:2,eq=brightness=-0.14:saturation=1.05[bg];"
        "[fgsrc]fps=30,scale=1760:-1,"
        "zoompan=z='min(pzoom+0.00060,1.12)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        "s=1080x720:fps=30[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2[base];"
        "[base][1:v]overlay=0:0,format=yuv420p[v]"
    )
    run(["ffmpeg", "-y", "-loop", "1", "-t", f"{dur}", "-i", str(photo),
         "-loop", "1", "-t", f"{dur}", "-i", str(lt),
         "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-r", "30", str(out)])


def assemble(intro: Path, photo: Path, outro: Path, out: Path):
    off1 = T_INTRO - XF
    off2 = (T_INTRO + T_PHOTO - XF) - XF
    fc = (f"[0][1]xfade=transition=fade:duration={XF}:offset={off1}[a];"
          f"[a][2]xfade=transition=fade:duration={XF}:offset={off2}[v]")
    run(["ffmpeg", "-y", "-i", str(intro), "-i", str(photo), "-i", str(outro),
         "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", str(out)])


def build(slug: str) -> Path:
    listing = LISTINGS.get(slug)
    if not listing:
        raise SystemExit(f"Unknown listing '{slug}'. Options: {', '.join(LISTINGS)}")
    photo = LISTINGS_DIR / listing["photo"]
    if not photo.exists():
        raise SystemExit(f"Hero photo not found: {photo}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    final = OUT_DIR / f"{slug}-short.mp4"

    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        print(f"[{slug}] rendering branded cards...")
        cards = render_cards(listing, work)
        print(f"[{slug}] intro segment...");  kenburns_card(cards["intro"], T_INTRO, work / "s_intro.mp4")
        print(f"[{slug}] photo segment...");  photo_segment(photo, cards["lowerthird"], T_PHOTO, work / "s_photo.mp4")
        print(f"[{slug}] outro segment...");  kenburns_card(cards["outro"], T_OUTRO, work / "s_outro.mp4")
        print(f"[{slug}] cross-fading...");   assemble(work / "s_intro.mp4", work / "s_photo.mp4", work / "s_outro.mp4", final)

    kb = final.stat().st_size / 1024
    total = T_INTRO + T_PHOTO + T_OUTRO - 2 * XF
    print(f"Wrote {final}  ({kb:.0f} KB, ~{total:.1f}s, 1080x1920, silent — add a licensed music bed before posting)")
    return final


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "204-ivy-cottage-dr")
