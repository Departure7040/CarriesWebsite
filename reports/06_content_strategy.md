# 06 Content Strategy

**Date:** 2026-07-08
**Author:** content_strategy_agent
**Reads first:** `agents/content_strategy_agent.md`, `data/keyword_intent_map.csv`, `reports/04_competitor_gap_analysis.md`, `reports/03_website_technical_audit.md`

---

## Content Principles

1. **Lead-intent first.** Every page in this strategy exists to produce a specific lead action — a call, a form, a consult booking. This is not a blog-volume play. No generic "5 tips for spring cleaning your home" filler; every piece maps to a query cluster in `data/keyword_intent_map.csv` with real commercial or transactional intent behind it.
2. **Human-first, locally specific.** Content must read like it was written by someone who actually works Lafayette/Acadiana — real neighborhood names, real commute patterns, real school zoning, real price realities — not templated "we serve the greater X area" copy. Anywhere the strategy doesn't have Carrie's real local knowledge, it's marked `[client-confirm]` rather than fabricated. See the individual page briefs in `content/page_briefs/` for the full list of open confirmations.
3. **No unverified metrics as fact.** `data/known_claims.yaml` documents several attractive but unverified or conflicting numbers (174 closed sales/$44.6M, 46 families/$10.5M, "#45 of 1900 realtors," 11 years experience, ICON Agent status). None of these appear as stated fact anywhere in this content set — they're either omitted or tagged `[client-confirm]`. Only Zillow's 29 reviews/5.0 rating, the UL Lafayette business degree (from her own Zillow bio), the team of 4 (roster only — the "father" detail was disputed by the client 2026-07-11 and must not be used), the home-stager credential, and the certified-mentor credential are treated as verified, per the task's asset inventory.
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

## Existing Social Strength to Fold In (added 2026-07-08, second pass)

Two things surfaced verifying a client-flagged Facebook page are worth building into the repurposing pipeline rather than treated as new work. First, **TikTok (`@carriebilleaud_realtor`) is already active** — 701 likes/311 followers per a search snippet, with listing videos and eXp event content already being posted — so it should be added as a standing repurposing target alongside Instagram/Facebook/Nextdoor/YouTube in `content/social_repurposing_ideas.md`, not launched from zero. Second, **her co-marketing relationship with lender Aimee Power (Approved Mortgage Now)** — cross-posted giveaway campaigns that drive entries to both partners' pages — is a legitimate, already-working local cross-promotion channel `[verified — visible in live cross-posted content]`; it's worth deliberately scheduling more of these joint giveaways/posts rather than treating this partnership as incidental. Both items are `[client-confirm]` before scaling up (confirm the partnership terms and cadence with Carrie), but neither requires new infrastructure — they extend what's already working.

## Measurement via Search Console

Once Google Search Console access is confirmed (open item, `09_questions_for_client.md` Q2):
- Track impressions/clicks for every query in `data/keyword_intent_map.csv`, mapped to the `target_page` column already present in that file.
- Watch for query variants the keyword map didn't anticipate (e.g., neighborhood-specific searches surfacing under the Youngsville/Broussard pages) — these become the seed list for steady-state blog topics.
- Flag any P1 query where the mapped page isn't appearing in the index at all — likely signals a platform indexation issue (robots.txt, canonical, or dual meta-robots bug — all documented in `03_website_technical_audit.md`) rather than a content problem, and should route back to a BoldTrail support ticket, not a rewrite.

---

## Tracking & Measurement

Measuring conversion is the only way to know if this content strategy is generating leads or just traffic. This section outlines GA4 event tracking, Search Console monitoring, and CRM source tagging so every lead can be traced back to the query, page, and call-to-action that captured it.

### Google Analytics 4: Core Events

Set up the following events in GA4 to measure funnel performance:

- **Form submission** (event name: `form_submit`): Fires when the contact form or lead capture block submits successfully (not on error). Tag with the form location (landing page, blog post, bio page) as an event parameter `form_location`. [best-practice]
- **Click-to-call** (event name: `call_click`): Fires when the visitor clicks the phone number or "Call now" button on any page. Tag with page path and device type. This is distinct from form submission and shows immediate intent. [best-practice]
- **Listing inquiry** (event name: `listing_inquiry`): If BoldTrail/eXp platform allows it, fire an event when a visitor initiates a listing inquiry or contact flow within an IDX results page. If not directly trackable, this workflow is less critical (IDX is platform-controlled). [inferred]

**GA4 Event Implementation**: These events likely require custom event tags in Google Tag Manager (GTM) or direct GA4 code insertion. Because Carrie's site is hosted on BoldTrail/eXp, GA4 container may be read-only or require a platform support ticket for custom event setup. [client-confirm] whether BoldTrail allows GTM access or if eXp support must wire these events. Once confirmed, implement tags for all three events before publishing P1 content.

### Google Search Console Access & Verification

GSC is the primary tool for seeing which queries drive clicks to which pages and measuring ranking position over time. Verification options:

- **HTML tag** (recommended if DNS access is unavailable): Generate a verification code in GSC and add it via the BoldTrail CMS meta field if available. This is the fastest route if the platform supports custom meta tags. [best-practice]
- **DNS record** (preferred but requires access to domain DNS): If Carrie or her team controls DNS for carriebilleaud.exprealty.com, add the CNAME or TXT record GSC provides. [client-confirm] whether DNS control exists or if a platform/registrar support ticket is needed.
- **Google Analytics connection**: If GA4 is already set up on BoldTrail and the account is verified, GSC may auto-connect. Check this first. [best-practice]

Once verified: Submit the XML sitemap (carriebilleaud.exprealty.com/sitemap-index.xml per the technical audit) and monitor the "Discover" and "Search results" reports monthly. Flag any P1 query where the target page is not appearing in the index; route to BoldTrail support if canonicals, meta robots, or robots.txt are the likely cause.

### Google Business Profile Performance Metrics

Once the GBP is created (see backlog row 13), track these metrics monthly:

- **Profile views**: How many people searched and clicked into the profile.
- **Website clicks**: How many went from GBP to carriebilleaud.exprealty.com.
- **Call clicks**: Direct calls initiated from GBP (compare to GA4 call_click events).
- **Direction requests**: Clicks to Google Maps navigation — less relevant for a service-area business, but a signal of mobile searcher intent.

Export these monthly to a shared dashboard or spreadsheet so Carrie sees the correlation between profile activity and lead form submissions. [best-practice]

### UTM Convention for GBP Links & Citations

When GBP links back to the website (e.g., in the "Website" field or GBP posts), use a consistent UTM structure:

- **Website link (to homepage/bio)**: `?utm_source=google&utm_medium=organic&utm_campaign=gbp`
- **Appointment/booking link**: `?utm_source=google&utm_medium=organic&utm_campaign=gbp_appointments`
- **GBP post links**: `?utm_source=google&utm_medium=organic&utm_campaign=gbp_posts`

This ensures GA4 correctly attributes these high-intent organic clicks to GBP, not direct/organic. Apply the same convention to any links in Zillow, Realtor.com, or other controlled profiles: `utm_source=zillow`, `utm_source=realtor_com`, etc. [best-practice]

### Call Tracking Tradeoff

Dynamic number insertion (swapping phone numbers based on traffic source) conflicts with NAP consistency and citation authority. Recommendation: Keep the canonical phone number on GBP, citations, and the website. If Carrie needs paid-media call tracking, use a **dedicated tracked number only in paid ad campaigns** (Google Ads, Facebook), not on organic pages or citations. This avoids confusing search algorithms and customers. [best-practice] + [client-confirm] whether Carrie intends to run paid campaigns that would warrant a separate tracking number.

### Contact Form Tracking & Spam Filtering

- Track form submissions to Google Sheets or Carrie's CRM automatically so no leads go unnoticed. Most BoldTrail forms have a CRM integration; confirm it's connected. [client-confirm]
- Implement basic spam filtering (CAPTCHA, honeypot field, rate limiting) to reduce bot submissions without creating friction for human leads. [best-practice]

### CRM Source Tagging Convention

The CRM (likely kvCORE or a BoldTrail default, [inferred]) must tag every inbound lead with its source: "Website contact form", "GBP call", "Zillow message", etc. This is the bridge between GA4 events and actual lead quality. Without it, high traffic is meaningless. [client-confirm] the CRM system and set up source tags in the CRM intake flow, then audit that 100% of leads are tagged within 2 weeks. [best-practice]

### Landing Page CTA Improvements

- **Above-fold phone**: On every page (bio, seller/buyer landing pages), place the canonical phone number prominently above the fold. No hover-to-reveal or buried contact info.
- **Sticky mobile call button**: On mobile viewport, add a persistent "Call now" button at screen bottom so one tap initiates a call. [best-practice]
- **Form above fold**: Lead capture form (minimal: name, email, phone, brief message) must appear or be clickable above the fold on high-intent pages (sell_my_house, listing_agent, buyers_agent). [best-practice]

These three elements are the measurable difference between a page that ranks and a page that converts. Track click rates on each via GA4 events.
