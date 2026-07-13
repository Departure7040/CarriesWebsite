# Branded social-graphic generator (`generate_graphics.py`)

Renders Carrie's luxury "Just Listed" graphics — the **1080×1080 feed square** and
the **1080×1920 story** — as branded PNGs from a single listing. Productionized
from the `render_post.py` POC: reusable, importable, one listing at a time.

Output: `build/social/out/<slug>-square.png` and `<slug>-story.png` @2x
(`device_scale_factor=2`). The property photo, Carrie's logo, and the Playfair
webfont are embedded as data URIs, so the render fetches nothing over the network.

## Run it for one listing (CLI)

```bash
python build/social/generate_graphics.py \
  --slug 204-ivy-cottage-dr --price '$1,510,000' \
  --address '204 Ivy Cottage Dr' --city 'Youngsville, LA' \
  --beds 4 --baths 3.5 --sqft 3918 \
  --photo site/assets/img/listings/204-ivy-cottage-dr.jpg
```

`--photo` accepts a **local path OR an https URL** (a URL is downloaded to a temp
file and cleaned up). `--slug` is optional (derived from the address if omitted).
`--label` defaults to `JUST LISTED`.

## Call it from the orchestrator (import)

```python
from build.social.generate_graphics import generate_graphics

square_png, story_png = generate_graphics({
    "slug": "204-ivy-cottage-dr", "price": "$1,510,000",
    "address": "204 Ivy Cottage Dr", "city": "Youngsville, LA",
    "beds": 4, "baths": "3.5", "sqft": 3918,
    "photo": "https://.../listing-photo.jpg",  # path or https URL
})
```

Returns `(square_path, story_path)` as `Path` objects.

## The "new listing → graphic" flow

1. A new listing hits her feed (`/api/listings`, snapshot in `data/`).
2. Orchestrator maps the feed record → the dict above (address/city/price/beds/
   baths/sqft + best photo URL).
3. Calls `generate_graphics(listing)` → two PNGs land in `build/social/out/`.
4. The graphics attach to the content package for **Carrie's one-tap approval**;
   publishing stays manual/aggregator (Tier-2 wall — no auto-publish here).

## Watermark caveat (production)

Feed photos from the MLS/Realtor.com may carry a portal watermark. For anything
Carrie actually posts, feed her **own or un-watermarked** listing photos —
compositing a watermarked image into the branded frame looks unprofessional and
can violate portal terms. The generator does not remove watermarks.

## Compliance

Facts only on the graphic: price / beds / baths / sqft / address / `JUST LISTED`.
No steering or fair-housing-sensitive language is ever composited. NAP on the
frame stays her real info (Carrie Billeaud, REALTOR®, eXp Realty, 337.258.5379).
