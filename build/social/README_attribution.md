# Attribution layer — post → tracked link → landing page → attributed lead

The measurement layer that makes every social post accountable. Closes the loop
so we can say *"here are clicks + leads per post/platform"* — the number the firm
can't produce.

## The flow

```
social post (caption embeds a tracked short-link, one per platform)
      │
      ▼
GET carriebilleaud.com/go/<slug>-<platform>     ← functions/go/[code].js
      │   • parse code as "<slug>-<platform>"
      │   • log click to CLICKS_KV (count + rolling log): ts, code, slug,
      │     platform, referer, UA, cf-connecting-ip  (degrades if no KV)
      ▼
302 → /l/<slug>/?utm_source=<platform>&utm_medium=social
                &utm_campaign=just-listed&utm_content=<slug>
      │
      ▼
property landing page /l/<slug>/     (facts-only: price/beds/baths/sqft/addr/photo)
      │   • reads UTM params (CLIENT-SIDE JS) → fills hidden form fields
      ▼
POST /api/lead   ← functions/api/lead.js
      │   • records listing_slug, listing_address, platform,
      │     utm_source, utm_campaign, utm_content on the lead
      ▼
email / CRM webhook — every lead now carries its SOURCE
```

**Two funnels per post:** clicks (from `/go`, includes non-converters) and leads
(from the form's source fields). Studio generates a distinct link per platform
(the `<platform>` suffix differs → `utm_source` differs → per-platform attribution).

## Demo vs. production split

| Piece | Demo (site/server.py static + Cloudflare tunnel) | Production (Cloudflare Pages) |
|---|---|---|
| Landing pages `/l/<slug>/` | **Work** — read UTMs with client-side JS, no server dep | Same, plus real form POST |
| `/go/<code>` redirect | **Inert** (no functions on static server) — use full `/l/<slug>/?utm_*` links directly in the demo | `functions/go/[code].js` logs + 302s |
| `/api/lead` | Inert (static server only wires `/api/listings`) | Records lead + attribution |
| `/api/clicks` readout | Inert | `functions/api/clicks.js` reads CLICKS_KV |

The Cloudflare Pages Functions (`functions/**`) are **production artifacts**. They
do not run on the demo static server. For a live demo, embed the fully-formed
`/l/<slug>/?utm_source=…&utm_campaign=just-listed&utm_content=<slug>` URL directly
so the landing page still attributes client-side.

## Cloudflare routing

- **Redirect:** file `functions/go/[code].js` → serves **`GET /go/<code>`**
  (the `[code]` filename is the dynamic segment; `params.code` is the value).
- **Lead:** `functions/api/lead.js` → `POST /api/lead`.
- **Readout:** `functions/api/clicks.js` → `GET /api/clicks`
  (`?code=<c>` for one code + its log; `?mock=1` for a sample row when no KV).

## The CLICKS_KV binding Brook must create

1. Cloudflare dashboard → **Workers & Pages → KV → Create namespace**, e.g.
   `carrie-clicks`.
2. Pages project → **Settings → Functions → KV namespace bindings → Add**:
   - Variable name: **`CLICKS_KV`**  (must match exactly)
   - Namespace: `carrie-clicks`
3. Redeploy. Until it's bound, `/go/<code>` still redirects and `/api/clicks`
   returns `bound:false` with an empty `codes[]` — nothing breaks.

Data model in KV: `count:<code>` = integer click count; `log:<code>` = JSON array
of the last 200 click entries.

## GA4 UTM note

The redirect lands users on `/l/<slug>/` with standard UTM params, so GA4 attributes
the **pageview** automatically (Traffic acquisition → Session source/medium =
`<platform> / social`, campaign `just-listed`). `/go` click counts (our first-party
funnel) and GA4 sessions are complementary: `/go` counts every click incl. bots and
non-landers; GA4 counts sessions that actually rendered the page.

## Privacy (CR-007)

- **No PII in URLs.** UTMs are campaign labels only (`platform`, `just-listed`,
  `slug`) — never a name, email, or phone.
- Attribution fields on the lead are sanitized + length-capped (CR/LF stripped for
  header-safety) before forwarding.
- The landing-page form keeps its privacy-notice line. Landing pages are
  listing-facts only — no steering / fair-housing language, no unverified stats.
- `/api/lead` still returns generic JSON and never echoes submitted PII back.
