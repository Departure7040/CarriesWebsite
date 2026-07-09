# 06 Content Strategy

**Date:** 2026-07-08
**Author:** content_strategy_agent
**Reads first:** `agents/content_strategy_agent.md`, `data/keyword_intent_map.csv`, `reports/04_competitor_gap_analysis.md`, `reports/03_website_technical_audit.md`

---

## Content Principles

1. **Lead-intent first.** Every page in this strategy exists to produce a specific lead action — a call, a form, a consult booking. This is not a blog-volume play. No generic "5 tips for spring cleaning your home" filler; every piece maps to a query cluster in `data/keyword_intent_map.csv` with real commercial or transactional intent behind it.
2. **Human-first, locally specific.** Content must read like it was written by someone who actually works Lafayette/Acadiana — real neighborhood names, real commute patterns, real school zoning, real price realities — not templated "we serve the greater X area" copy. Anywhere the strategy doesn't have Carrie's real local knowledge, it's marked `[client-confirm]` rather than fabricated. See the individual page briefs in `content/page_briefs/` for the full list of open confirmations.
3. **No unverified metrics as fact.** `data/known_claims.yaml` documents several attractive but unverified or conflicting numbers (174 closed sales/$44.6M, 46 families/$10.5M, "#45 of 1900 realtors," 11 years experience, ICON Agent status). None of these appear as stated fact anywhere in this content set — they're either omitted or tagged `[client-confirm]`. Only Zillow's 29 reviews/5.0 rating, the UL Lafayette business degree (from her own Zillow bio), the team of 4 (including her father), the home-stager credential, and the certified-mentor credential are treated as verified, per the task's asset inventory.
4. **No doorway pages.** The two area pages (Youngsville, Broussard) are deliberately written with distinct angles — Youngsville around growth/new construction/Sugar Mill Pond/schools, Broussard around commute convenience/established neighborhoods/small-town character — so they read as genuinely different pages serving genuinely different buyer profiles, not the same template with a city name swapped.
5. **Optimize for humans and AI answer engines, search engines second.** Clear FAQ structure, plain-language explainers, and specific local detail serve all three audiences at once; keyword density is never the goal.

## Platform Reality (carried forward from `03_website_technical_audit.md`)

Carrie's site is an eXp Realty/BoldTrail-hosted agent site. Three facts shape how this content actually gets published:
- The **agent bio** (`/agents.php` "About Carrie") is empty today and is agent-editable — this is the single highest-leverage, lowest-effort fix and should absorb the `lafayette_realtor` brief content first.
- **Area pages** (`/areas/lafayette`, etc.) are templated, `noindex` IDX search-results pages. They cannot carry the Youngsville/Broussard content in this strategy — that content needs to live as authored blog posts or (if available) custom pages.
- **Blog posts** are the one content type on this platform proven to render real, decent-quality, indexable-ish content (see the "Modern Farmhouse Living" post example in the technical audit) — this is the practical publishing vehicle for most of this content in the near term.
- **JSON-LD schema is template-level and not agent-editable.** Every brief's schema recommendation notes this; the workaround is a BoldTrail/eXp support ticket, and the long-term fix (recommended independently in `04_competitor_gap_analysis.md`) is a standalone domain where schema, canonicals, and custom pages are fully controllable.

Every page brief includes an explicit "Platform & publishing note" addressing this — treat the briefs as the source of truth for *what* to publish; use BoldTrail's actual available tools (bio field, blog, and custom pages if/when confirmed available) to decide *where*.

## The 7-Page Core Structure

| # | Page brief | Query cluster | Priority | Funnel stage | Role |
|---|---|---|---|---|---|
| 1 | `lafayette_realtor.md` | Lafayette LA realtor / best realtor / real estate agent / Acadiana realtor | P1 (+P3 regional) | Decision/consideration | Hub — every other page links here |
| 2 | `sell_my_house_lafayette.md` | Sell my house Lafayette | P1 (highest seller intent) | Decision/transactional | Fastest seller lead capture |
| 3 | `lafayette_listing_agent.md` | Listing agent Lafayette LA | P1 | Decision | Seller agent-selection / process authority |
| 4 | `first_time_homebuyers_lafayette.md` | First time home buyer realtor Lafayette LA | P1 | Consideration | Education lead magnet, matches claimed specialty |
| 5 | `lafayette_buyers_agent.md` | Buyer agent Lafayette LA | P2 | Decision | Buyer representation (non-first-timers) |
| 6 | `youngsville_realtor.md` | Youngsville LA realtor | P2 | Decision | Area page — growth/new construction angle |
| 7 | `broussard_realtor.md` | Broussard LA realtor | P2 | Decision | Area page — commute/established-neighborhood angle |

## Publishing Order & Rationale

**Phase 1 — P1 pages (weeks 1–6):** `lafayette_realtor` (bio rewrite, ships immediately — no platform blocker), `sell_my_house_lafayette` (highest raw seller intent, ships as a blog post/CTA block fast), `lafayette_listing_agent`, `first_time_homebuyers_lafayette`. These four cover every P1 keyword and both ends of the seller funnel plus the strongest buyer-specialty match.

**Phase 2 — P2 pages (weeks 7–12):** `lafayette_buyers_agent`, then the two area pages (`youngsville_realtor`, `broussard_realtor`). Area pages come last in the sequence because they require the most `[client-confirm]` local detail (specific neighborhoods, school zoning, current commute times) — give Carrie time to supply that input rather than publishing thin or generic area content that would defeat the "no doorway pages" principle.

**Ongoing:** once the 7-page core is live, shift to a steady blog cadence (below) built from Search Console query data and seasonal market moments (spring listing season, back-to-school relocation timing, etc.) — always still mapped back to one of the 7 core pages via internal links, never standalone SEO filler.

## Cadence Recommendation

- **Launch phase (first ~12 weeks):** one core page/post roughly every 1–2 weeks, in the order above. This matches the pace implied by `08_scope_and_pricing_options.md` Option B (30-day implementation sprint gets 2–3 core pages live) rolling into Option C.
- **Steady state:** 2–4 local content pieces/month (matches Option C's stated cadence), split roughly 1 market-update or neighborhood-spotlight post + 1–2 seasonal/FAQ-driven posts feeding the existing 7 pages via internal links. This also matches the competitive benchmark in `04_competitor_gap_analysis.md` (Jessica Broussard's 2–3 posts/month).
- Avoid publishing faster than Carrie can supply accurate `[client-confirm]` local detail — a wrong school-zoning or commute-time claim is a real trust/liability cost, not just a missed SEO opportunity.

## How Content Feeds GBP Posts + Social

Each of the 7 pages is designed to be a source document, not a dead end:
- **GBP posts** (once the Google Business Profile is created — see `09_questions_for_client.md` Q1): pull one FAQ answer or one H2 section per week as a short GBP update, always linking back to the relevant page.
- **Social (Instagram/Facebook/TikTok/Nextdoor/YouTube):** every page's FAQ section and H2 breakdown is written to be choppable into short-form scripts and captions. See `content/social_repurposing_ideas.md` for the full repurposing map — each page brief above should be treated as the source script for 3–5 pieces of social content, not a one-and-done web page.

## Measurement via Search Console

Once Google Search Console access is confirmed (open item, `09_questions_for_client.md` Q2):
- Track impressions/clicks for every query in `data/keyword_intent_map.csv`, mapped to the `target_page` column already present in that file.
- Watch for query variants the keyword map didn't anticipate (e.g., neighborhood-specific searches surfacing under the Youngsville/Broussard pages) — these become the seed list for steady-state blog topics.
- Flag any P1 query where the mapped page isn't appearing in the index at all — likely signals a platform indexation issue (robots.txt, canonical, or dual meta-robots bug — all documented in `03_website_technical_audit.md`) rather than a content problem, and should route back to a BoldTrail support ticket, not a rewrite.

---

## Tracking & Measurement

(populated by conversion_tracking_agent)
