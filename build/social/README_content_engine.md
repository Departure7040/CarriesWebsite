# Social Content Engine — Carrie Billeaud (Tier-1 wedge)

The human-in-the-loop content engine from `implementation/social_agent_design.md`.
It turns **a new listing on Carrie's live feed** into a **ready-to-approve content
package** — branded graphics + a caption written for every platform — that she
reviews, copies, and posts herself. This is the **personal-posting wedge**: it
solves the cross-posting pain she owns and asked for ("All of this would be
perfect!!!!"). **Nothing auto-publishes** — publishing stays manual, or is later
handed to a scheduling aggregator. That's the deliberate Tier-2 wall, not a gap.

## Architecture: trigger → generate → approve → post

```
TRIGGER    new listing hits her feed (Realtor.com snapshot / live /api/listings)
   │          content_orchestrator.py detects it (seen-ids diff = "new since last run")
   ▼
GENERATE   ├─ generate_graphics.py   → branded square.png (1080²) + story.png (1080×1920)
   │       └─ captions (Anthropic)   → IG / FB / TikTok / YouTube / story / 3 hooks
   │          assembled into out/packages/<slug>/  + index.json manifest
   ▼
APPROVE    site/tools/content-studio.html — she reviews each package, one-tap COPY
   │          per platform, DOWNLOAD the graphic, toggle APPROVE. (Voice + compliance
   │          stay human — the point of the wedge.)
   ▼
POST       she pastes + posts (2 min), OR later hands the approved batch to
           Buffer / Metricool / Publer. NO platform auto-publish is built.
```

## Pieces

| File | Role | Needs API key? |
|---|---|---|
| `content_orchestrator.py` | Pipeline: feed → detect → package → manifest | Captions only (mock otherwise) |
| `generate_graphics.py` | Branded PNG render (Playwright, luxury template) | **No** — pure render |
| `../../functions/api/generate-content.js` | The same caption engine, as a Cloudflare Function (site-side) | Yes (or `CONTENT_MOCK`) |
| `../../site/tools/content-studio.html` | Approval / review UI (noindex, site palette) | No — static + fetch |
| `post_template*.html`, `_fonts/` | Luxury graphic templates + embedded webfont | No |

## Run it

```bash
# 1. Generate packages (mock captions — no key needed; graphics are always real)
CONTENT_MOCK=1 python build/social/content_orchestrator.py

#    Real captions: export the key first, drop CONTENT_MOCK
export ANTHROPIC_API_KEY=sk-ant-...
python build/social/content_orchestrator.py

#    Fetch the LIVE feed instead of the snapshot (needs the proxy running):
python build/social/content_orchestrator.py --live
#    Repackage everything (ignore the new-since-last-run diff):
python build/social/content_orchestrator.py --all

# 2. Review: serve the repo root and open the studio
python -m http.server 8080
#    → http://localhost:8080/site/tools/content-studio.html
```

Output per listing: `build/social/out/packages/<slug>/` with `square.png`,
`story.png`, `captions.json` (the structured multi-platform package) and
`ready-to-post.md` (human-readable, tells her which image to use where).
The orchestrator also writes `packages/index.json`, which the studio loads.

## The API key — what needs it

- **Graphics: nothing.** `generate_graphics.py` is a local Playwright HTML→PNG
  render. Always works offline, no key, free.
- **Captions: `ANTHROPIC_API_KEY`.** The orchestrator mirrors
  `functions/api/generate-content.js` — same `MODEL` (claude-sonnet-5), same
  `SYSTEM_PROMPT`, same forced `emit_content_package` tool. Without a key (or with
  `CONTENT_MOCK=1`) it emits a **facts-only, listing-specific mock** so the whole
  pipeline and the studio are demoable with zero setup. The mock invents nothing —
  compliance holds in mock mode too.

## Cost ballpark

Captions are one small Sonnet call per listing (~1–2K output tokens). Order of a
**fraction of a cent to ~2¢ per listing**; a busy month of new listings is a few
dollars. Graphics are free (local render). Compare to the **$3k/mo firm** — the
engine handles content volume + repurposing + consistency at ~coffee money.

## Compliance (non-negotiable — the system prompt IS the guardrail)

The caption `SYSTEM_PROMPT` is the compliance artifact and is kept **identical**
across `content_orchestrator.py`, `functions/api/generate-content.js`, and
`_content_system_prompt.md`. It hard-bans: steering / fair-housing-sensitive
language ("family-friendly," "safe," "good/great neighborhood," "good schools,"
"up-and-coming"), unverified stats stated as fact, guarantees/predictions,
invented amenities. **Facts only** — captions and graphics use exclusively the
listing's own fields (price, beds, baths, sqft, address, status). Her real NAP
(Carrie Billeaud, REALTOR, eXp Realty, Acadiana) is preserved. The human approval
step keeps a licensed person on the compliance line — that protects her license
and is the whole reason approval is a *feature*.

## How a real "new listing" flows through

1. A new home hits her Realtor.com feed. A scheduled run (or `--live`) pulls the
   feed; `select_listings()` compares each `property_id` against
   `out/packages/.seen_ids.json` and processes only the **new** one.
2. The orchestrator renders her branded square + story from the listing's own
   photo, calls the caption engine (facts-only), and writes the package folder +
   updates `index.json`.
3. She opens the Content Studio, sees the new package at the top, reads the
   captions, one-tap **copies** each platform's text, **downloads** the graphic,
   flips **Approve**, and posts — or hands the approved batch to an aggregator.
4. Nothing posts without her. Voice and compliance stay human by design.

## Productization note

This is **Brook's module** — the productizable Tier-1 content-engine + approval
loop for solo agents (textbook AI-integration consulting). **Carrie is the
flagship / proof.** Ship Tier-1 as the value; price Tier-2 (aggregator wiring) and
Tier-3 (engagement) as the service, evidence-first — the firm/$3k conversation
stays a later, data-backed decision. Wedge first, firm later.
```
