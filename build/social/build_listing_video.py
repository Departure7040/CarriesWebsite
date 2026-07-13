#!/usr/bin/env python3
"""Render a branded vertical "Just Listed" walkthrough SHORT (9:16) from a real listing.

"AI video from content, done right": we NEVER fabricate a house. We frame Carrie's
REAL listing photos inside a branded motion template. If a full gallery has been
fetched (build/social/fetch_listing_photos.py) we pan across every room; otherwise
we fall back to the single cached hero photo.

Structure:  intro card -> [photo montage: each photo blurred-fill + Ken-Burns push,
cross-faded, with a persistent price/address bar] -> contact outro card. Branded
charcoal/ivory/gold, Playfair, her signature logo inverted to ivory. Facts-only
overlays (price/address/beds/baths/sqft) -- same compliance posture as the graphics
engine: no steering, no guarantees, only the listing's given facts.

Audio: SILENT by default. Pass --music with a licensed or AI-generated instrumental
track (ffmpeg can only synthesize test tones, not real music, so we never fake it).

    python build/social/build_listing_video.py 101-rio-ridge-dr
    python build/social/build_listing_video.py 101-rio-ridge-dr --music path/to/track.mp3

Output: site/studio/packages/videos/<slug>-short.mp4  (studio packages are
gitignored -- regenerate with this script).
"""

import argparse
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
GALLERY_ROOT = LISTINGS_DIR / "gallery"
LOGO_PATH = REPO / "site" / "assets" / "img" / "carrie-logo.png"
FONT_PATH = REPO / "build" / "social" / "_fonts" / "playfair-latin.woff2"
OUT_DIR = REPO / "site" / "studio" / "packages" / "videos"

LABEL = "JUST LISTED"
T_INTRO, T_OUTRO, XF_CARD = 2.0, 2.5, 0.4     # card durations + card cross-fade
T_PHOTO, XF_PHOTO = 1.9, 0.6                    # per-photo hold + montage transition (motion lives here)

LISTINGS = {
    "204-ivy-cottage-dr": {"photo": "204-ivy-cottage-dr.jpg", "price": "$1,510,000",
        "address": "204 Ivy Cottage Dr", "city": "Youngsville, LA", "beds": 4, "baths": "3.5", "sqft": 3918},
    "101-rio-ridge-dr": {"photo": "101-rio-ridge-dr.jpg", "price": "$3,400,000",
        "address": "101 Rio Ridge Dr", "city": "Lafayette, LA", "beds": 5, "baths": "5.5", "sqft": 6800},
    "205-queenstown-ave": {"photo": "205-queenstown-ave.jpg", "price": "$465,000",
        "address": "205 Queenstown Ave", "city": "Youngsville, LA", "beds": 4, "baths": "2", "sqft": 2202},
}


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    return f"data:{mime or 'application/octet-stream'};base64," + base64.b64encode(path.read_bytes()).decode()


def font_b64() -> str:
    return base64.b64encode(FONT_PATH.read_bytes()).decode()


def specs(l: dict) -> str:
    return f"{l['beds']} BD &middot; {l['baths']} BA &middot; {l['sqft']:,} SQFT"


_CSS = """
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


def intro_html(l, logo, font):
    return f"""<!doctype html><meta charset=utf-8><style>{_CSS.replace('{FONT}', font)}
  #root{{background:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;text-align:center;padding:0 90px}}
  .price{{color:var(--ivory);font-size:150px;line-height:1;letter-spacing:-.01em}}
  .addr{{color:var(--ivory);font-size:52px}} .city{{color:var(--muted);font-size:38px;letter-spacing:.16em;text-transform:uppercase;margin-top:6px}}
  .specs{{color:var(--gold);font-size:34px;letter-spacing:.14em;margin-top:10px}}
  .foot{{position:absolute;bottom:120px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:16px}}
  .foot img{{height:78px}} .foot .sub{{color:var(--muted);font-size:26px;letter-spacing:.24em;text-transform:uppercase}}
</style><div id=root><div class=kick>{LABEL}</div><hr class=rule>
  <div class="serif price">{l['price']}</div>
  <div><div class="serif addr">{l['address']}</div><div class=city>{l['city']}</div></div>
  <div class=specs>{specs(l)}</div>
  <div class=foot><img class=logo src="{logo}"><div class=sub>REALTOR&reg; &middot; eXp Realty</div></div></div>"""


def bug_html(l, font):
    """Compact persistent price/address bar for the photo montage."""
    return f"""<!doctype html><meta charset=utf-8><style>{_CSS.replace('{FONT}', font)}
  #root{{background:transparent}}
  .scrim{{position:absolute;left:0;right:0;bottom:0;height:390px;
    background:linear-gradient(to top,rgba(18,21,28,.92) 4%,rgba(18,21,28,.55) 48%,rgba(18,21,28,0) 100%)}}
  .bar{{position:absolute;left:60px;right:60px;bottom:100px;text-align:center}}
  .bar .price{{color:var(--ivory);font-size:76px;line-height:1;letter-spacing:-.01em}}
  .bar .addr{{color:var(--ivory);font-size:32px;letter-spacing:.02em;margin-top:16px;white-space:nowrap}}
  .bar .specs2{{color:var(--gold);font-size:28px;letter-spacing:.10em;margin-top:10px;white-space:nowrap}}
</style><div id=root><div class=scrim></div>
  <div class=bar><div class="serif price">{l['price']}</div>
  <div class=addr>{l['address']}, {l['city']}</div>
  <div class=specs2>{specs(l)}</div></div></div>"""


def lowerthird_html(l, font):
    """Full lower third for single-hero fallback."""
    return f"""<!doctype html><meta charset=utf-8><style>{_CSS.replace('{FONT}', font)}
  #root{{background:transparent}}
  .scrim{{position:absolute;left:0;right:0;bottom:0;height:760px;
    background:linear-gradient(to top,rgba(18,21,28,.94) 8%,rgba(18,21,28,.72) 42%,rgba(18,21,28,0) 100%)}}
  .lt{{position:absolute;left:80px;right:80px;bottom:150px}}
  .lt .kick{{font-size:28px;margin-bottom:18px}} .lt .price{{color:var(--ivory);font-size:112px;line-height:1}}
  .lt .addr{{color:var(--ivory);font-size:46px;margin-top:14px}} .lt .city{{color:var(--muted);font-size:32px;letter-spacing:.14em;text-transform:uppercase;margin-top:4px}}
  .lt .specs{{color:var(--gold);font-size:32px;letter-spacing:.12em;margin-top:20px}}
</style><div id=root><div class=scrim></div><div class=lt>
  <div class=kick>{LABEL}</div><div class="serif price">{l['price']}</div>
  <div class="serif addr">{l['address']}</div><div class=city>{l['city']}</div><div class=specs>{specs(l)}</div></div></div>"""


def outro_html(logo, font):
    return f"""<!doctype html><meta charset=utf-8><style>{_CSS.replace('{FONT}', font)}
  #root{{background:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;text-align:center;padding:0 90px}}
  .logo{{height:150px}} .name{{color:var(--ivory);font-size:60px}} .sub{{color:var(--muted);font-size:32px;letter-spacing:.22em;text-transform:uppercase}}
  .cta{{color:var(--ivory);font-size:44px;margin-top:8px}} .phone{{color:var(--gold);font-size:58px;letter-spacing:.03em}}
</style><div id=root><img class=logo src="{logo}">
  <div class="serif name">Carrie Billeaud</div><div class=sub>REALTOR&reg; &middot; eXp Realty &middot; Acadiana</div>
  <hr class=rule><div class="serif cta">Schedule a private showing</div><div class=phone>337-258-5379</div></div>"""


def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0)); return s.getsockname()[1]


def serve_dir(directory, port):
    h = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(directory), **k)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), h)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def render_cards(listing, work):
    logo, font = data_uri(LOGO_PATH), font_b64()
    cards = {"intro": intro_html(listing, logo, font), "bug": bug_html(listing, font),
             "lowerthird": lowerthird_html(listing, font), "outro": outro_html(logo, font)}
    port = free_port(); httpd = serve_dir(work, port); out = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
            for name, html in cards.items():
                (work / f"{name}.html").write_text(html, encoding="utf-8")
                page.goto(f"http://127.0.0.1:{port}/{name}.html", wait_until="load")
                page.wait_for_timeout(150)
                png = work / f"{name}.png"
                page.locator("#root").screenshot(path=str(png), omit_background=(name in ("bug", "lowerthird")))
                out[name] = png
            browser.close()
    finally:
        httpd.shutdown()
    return out


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2500:]); raise SystemExit("ffmpeg failed")


def kenburns_card(png, dur, out):
    """Branded cards are STATIC (solid background + text) — no motion, so no
    text shimmer. The xfade transitions give them life."""
    run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-loop", "1", "-t", f"{dur}",
         "-i", str(png), "-vf", "format=yuv420p", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", "30", str(out)])


def photo_clip(photo, dur, out):
    """Each photo is a STATIC composite: a blurred-fill background + the sharp
    photo centered. No intra-clip zoom — ffmpeg's zoompan rounds the crop to whole
    pixels every frame, so a slow zoom "sticks then jumps" (the phone-over-a-photo
    judder). Instead ALL motion comes from the smooth float-interpolated xfade
    transitions between clips (see xfade_chain), which don't judder."""
    fc = ("[0:v]split=2[bg][fg];"
          "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "boxblur=32:2,eq=brightness=-0.16:saturation=1.04[bgb];"
          "[fg]scale=1080:-1[fgs];"
          "[bgb][fgs]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-loop", "1", "-t", f"{dur}",
         "-i", str(photo), "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-r", "30", str(out)])


# Smooth, eased transitions carry all the motion (float-interpolated -> no judder).
# A tasteful mix: mostly gentle dissolves with occasional directional glides.
TRANSITIONS = ["fade", "smoothleft", "fade", "smoothup", "fade", "smoothright", "fade", "smoothdown"]


def xfade_chain(clips, dur, xf, out):
    """Cross-fade a list of equal-duration clips into one montage using varied
    eased transitions, so the montage feels like video without any per-photo zoom."""
    if len(clips) == 1:
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clips[0]), "-c", "copy", str(out)]); return
    inputs, parts, prev = [], [], "[0]"
    for c in clips:
        inputs += ["-i", str(c)]
    for k in range(1, len(clips)):
        off = k * (dur - xf)
        trans = TRANSITIONS[(k - 1) % len(TRANSITIONS)]
        label = "[v]" if k == len(clips) - 1 else f"[x{k}]"
        parts.append(f"{prev}[{k}]xfade=transition={trans}:duration={xf}:offset={off:.3f}{label}")
        prev = label
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(parts),
         "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(out)])


def overlay_bug(montage, bug_png, dur, out):
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(montage), "-loop", "1", "-t", f"{dur}", "-i", str(bug_png),
         "-filter_complex", "[0:v][1:v]overlay=0:0,format=yuv420p[v]", "-map", "[v]",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(out)])


def assemble(intro, montage, outro, montage_dur, music, out):
    off1 = T_INTRO - XF_CARD
    off2 = (T_INTRO + montage_dur - XF_CARD) - XF_CARD
    fc = (f"[0][1]xfade=transition=fade:duration={XF_CARD}:offset={off1:.3f}[a];"
          f"[a][2]xfade=transition=fade:duration={XF_CARD}:offset={off2:.3f}[v]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(intro), "-i", str(montage), "-i", str(outro)]
    if music:
        cmd += ["-i", str(music), "-filter_complex", fc, "-map", "[v]", "-map", "3:a",
                "-c:a", "aac", "-b:a", "160k", "-shortest"]
    else:
        cmd += ["-filter_complex", fc, "-map", "[v]"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", str(out)]
    run(cmd)


def gather_photos(slug, listing):
    gdir = GALLERY_ROOT / slug
    if gdir.is_dir():
        photos = sorted(gdir.glob("*.jpg"))
        if photos:
            return photos, True
    hero = LISTINGS_DIR / listing["photo"]
    if not hero.exists():
        raise SystemExit(f"No gallery and no hero photo for {slug}")
    return [hero], False


def build(slug, music_arg):
    listing = LISTINGS.get(slug)
    if not listing:
        raise SystemExit(f"Unknown listing '{slug}'. Options: {', '.join(LISTINGS)}")
    photos, is_gallery = gather_photos(slug, listing)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    final = OUT_DIR / f"{slug}-short.mp4"

    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        print(f"[{slug}] {'gallery' if is_gallery else 'single-hero'}: {len(photos)} photo(s); rendering cards...")
        cards = render_cards(listing, work)

        # Photo montage (or single hero with a full lower third).
        segs = []
        for i, ph in enumerate(photos, 1):
            seg = work / f"seg_{i:02d}.mp4"
            photo_clip(ph, T_PHOTO, seg)
            segs.append(seg)
        montage_dur = len(segs) * T_PHOTO - (len(segs) - 1) * XF_PHOTO
        print(f"[{slug}] montage ({len(segs)} clips, ~{montage_dur:.1f}s)...")
        montage = work / "montage.mp4"
        xfade_chain(segs, T_PHOTO, XF_PHOTO, montage)

        overlay_png = cards["bug"] if is_gallery else cards["lowerthird"]
        montage_bug = work / "montage_bug.mp4"
        overlay_bug(montage, overlay_png, montage_dur, montage_bug)

        print(f"[{slug}] intro/outro...")
        intro, outro = work / "intro.mp4", work / "outro.mp4"
        kenburns_card(cards["intro"], T_INTRO, intro)
        kenburns_card(cards["outro"], T_OUTRO, outro)

        total = T_INTRO + montage_dur + T_OUTRO - 2 * XF_CARD
        music = None
        if music_arg:
            music = Path(music_arg)
            if not music.exists():
                raise SystemExit(f"--music file not found: {music}")
            print(f"[{slug}] using music track: {music.name}")

        print(f"[{slug}] final assembly...")
        assemble(intro, montage_bug, outro, montage_dur, music, final)

    kb = final.stat().st_size / 1024
    audio = f"music: {Path(music_arg).name}" if music_arg else "silent (add --music)"
    print(f"Wrote {final}  ({kb:.0f} KB, ~{total:.1f}s, 1080x1920, {audio})")
    return final


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?", default="101-rio-ridge-dr")
    ap.add_argument("--music", default=None, help="path to a licensed/AI-generated instrumental track (mp3/wav)")
    a = ap.parse_args()
    build(a.slug, a.music)
