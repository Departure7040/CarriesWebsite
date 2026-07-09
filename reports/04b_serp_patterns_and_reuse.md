# SERP Patterns & Reuse Analysis: What Top-Ranking Lafayette Pages Actually Do

**Date:** 2026-07-08
**Purpose:** Go deeper than the competitor list in `04_competitor_gap_analysis.md` — catalog the actual on-page structure, content elements, and conversion patterns that top-ranking Lafayette-area real estate pages use, and translate them into concrete, ethical adaptation notes for Carrie's 7 page briefs (`content/page_briefs/`).

**Tagging key:** `[verified]` = confirmed via direct fetch of the live page (source in `data/source_log.csv`) · `[inferred]` = reasonable conclusion, not independently confirmed · `[client-confirm]` = needs Carrie's input before use.

**SERP Approximation Caveat (repeated from `04_competitor_gap_analysis.md`):** All rankings below reflect Firecrawl searches run 2026-07-08 from a neutral, non-Lafayette IP with no personalization/search history. Google results are location- and personalization-dependent — a search from a Lafayette-based device, with local search history, will differ. Positions are directional evidence of SERP composition (what *type* of result tends to win a query), not a guarantee of Carrie's future rank if she adopts a pattern.

---

## Part A — Realistic-Query Sweep: What Wins, and Who Shows Up

| # | Query | Winning result type(s) | Local players who appear | Notes |
|---|-------|------------------------|---------------------------|-------|
| 1 | homes for sale lafayette la | Pure IDX portals (Zillow, Realtor.com, Trulia, Redfin, Homes.com, ForSaleByOwner) | None — no individual agent/team site in top 8 | Broad inventory head terms are portal-owned; not a realistic organic target for any of Carrie's 7 briefs |
| 2 | realtor near me lafayette | Directory (Zillow agent-reviews, Realtor.com) + team site | Keaty Real Estate (#3) | 3 of 8 results were actually **Lafayette, Indiana** — confirms "near me" is highly location/personalization sensitive, consistent with `04`'s SERP caveat |
| 3 | best real estate agent in lafayette louisiana | Directory + dedicated agent sites | Jessica Broussard (#2), Keaty (#3), FastExpert list w/ Nah Senpeng, Stephen Hundley, Jessica (#4), Sean Hettich (#7) | This is the one query where personal-brand agent sites genuinely compete with directories |
| 4 | youngsville la homes for sale new construction | Portals + home builders (NewHomeSource, LevelHomesLifestyle) | None | Notably, lafayettehomepros.com did **not** appear here despite ranking for related community queries — new-construction head terms skew portal/builder |
| 5 | broussard la real estate | Portals + team area page | Robbie Breaux/lafayettehomepros.com/broussard (#4), eXp Realty's own generic Broussard IDX page (#7) | Carrie's own brokerage (eXp) already has a templated, non-differentiated page competing in this exact SERP |
| 6 | sugar mill pond youngsville homes | Portals + builder + team micro-community page | Robbie Breaux/lafayettehomepros.com/sugar-mill-pond (#4) | Proof that a well-built, named-community landing page can break into a portal-dominated SERP |
| 7 | how much is my house worth lafayette | Mix: generic tools (Zillow Zestimate, Homes.com) + agent-branded valuation/lead pages | lafayettehomepros.com/sellers/free-market-analysis (#2, **above Zestimate**), therealjessicabroussard.com/home-valuation (#4, above Homes.com's own tool), atlasofacadiana.com (another local agent's valuation content, #7) | Strongest single validation in this sweep that an agent-branded valuation page can outrank the big portals' own tools |
| 8 | moving to lafayette la | Reddit (r/Acadiana), Facebook groups, moving-company blogs, city guides | None | Zero agent/team presence in top 8 — a top-of-funnel relocation query, not an achievable near-term target |
| 9 | first time home buyer programs louisiana | Government (LHC.la.gov #1) + finance sites (Bankrate, FHA.com) | None | Zero agent presence — program-detail authority belongs to government/finance sites |
| 10 | sell house fast lafayette la | Cash-buyer / iBuyer companies exclusively | None (no traditional agents) | 100% of top 8 are "we buy houses" / cash-offer operators — a real estate agent has essentially no organic path into this SERP |

**Takeaway pattern:** Agent/team sites only compete successfully in the SERP where (a) the query names an agent/team directly, (b) the query is a **named micro-community** (Sugar Mill Pond, specific subdivisions), or (c) the query is a **home-valuation/lead-capture intent**. Generic inventory queries, relocation queries, program-detail queries, and "sell fast" queries are owned by portals, content sites, government sites, or iBuyers respectively — no amount of on-page optimization is likely to out-rank those categories of competitor for those specific head terms. This should calibrate expectations in `06_content_strategy.md` and `07_30_60_90_day_plan.md`: prioritize page-brief queries and community-specific/valuation content over broad inventory or relocation terms.

---

## Part B — Winner Page Anatomy

### Sean Hettich — topagent337.com `[verified]`

| Element | What's actually there |
|---|---|
| Hero | "Lafayette's Realtor" H1, no immediate photo emphasis in markdown extraction (image-heavy, likely photo in design) |
| Trust ribbon | Year-by-year "Top Producer" stats: units sold + $ volume, 2020–2025, laid out as 6 columns |
| Stat tiles | "Over 9,500 page likes on Facebook," "Over 350 5-star reviews on Zillow," "139+ cancelled or expired listings turned into SOLD" |
| Nav structure | About (→ Results, Reviews) / Sellers (→ Strategy, Seller Process, Ready to Sell?) / Buyers / Blog / Contact |
| Persistent micro-CTA | "What's my home worth?" link lives in a secondary top bar, visible on every page, separate from primary nav — always accessible regardless of scroll position |
| Reviews page | Dedicated `/about/reviews/` page: 11+ full permissioned testimonials, each tagged with **sale date + city + transaction type** ("Sold a single family home in 2019 in Lafayette, LA"), plus outbound links to Zillow/Facebook review profiles |
| Social proof | Live Instagram feed embed on homepage |
| Footer | Phone/email, office address, social icons, Zillow profile link, legal pages |
| Schema | **No `application/ld+json` structured data found in the homepage source** `[verified]` — the #1-ranking competitor in this set has no visible schema markup |

### Jessica Broussard — therealjessicabroussard.com `[verified]`

| Element | What's actually there |
|---|---|
| Hero | "Real Estate Professional and Residential Stylist" tagline; embedded location/area search widget |
| Stat-tile row | 13+ Years Experience / $105M+ Sales Volume / 200+ Families Helped / 15+ Homes Styled / 50+ New Construction Projects / Top 1% in Acadiana |
| Hero CTA split | Three distinct buttons: **Buy a Home** / **Let's Connect** / **Sell a Home** — pre-qualifies visitor intent immediately instead of one generic "contact" button |
| Testimonials | Carousel of ~12 short testimonials, each with first-name + last-initial + photo |
| Bio | "Hello, I'm Jessica" — personal narrative tying her specialty (new construction) to a personal detail (married to a home builder) and a secondary service (interior decorating for new-construction clients) |
| Lead forms | "Interested in..." dropdown (Selling & Buying / Selling / Buying / Renting / Other) present on every contact form — routes/qualifies leads at capture time |
| Valuation page (`/home-valuation`) | Embedded instant-estimate widget **plus** substantial educational content: "What is a Home Valuation?", "How is the Valuation Calculated?", "How Accurate is the Online Home Valuation?" (honest about limitations), "Why Is a Valuation Important?" broken into Refinancing / Home Improvements / Qualifying for Credit / Planning sub-reasons, with outbound citations to Investopedia for CMA and appraisal definitions |
| Listings | Featured/Sold listings grid embedded on homepage |

### Robbie Breaux & Team — lafayettehomepros.com `[verified]`

| Element | What's actually there |
|---|---|
| Homepage | IDX search hero; "What's Your Home Worth? ... Get a FREE Home Valuation Now!" banner; grid of 40+ linked community/neighborhood pages (Abbeville through Youngsville); "Recently from Our Blog" module surfacing local-interest posts (Things to Do in Lafayette, Best Neighborhoods, Best Places to Live) |
| Area-page template (consistent across Broussard, Youngsville, Sugar Mill Pond) | 1) live MLS stat snapshot (# Listed / Avg Days on Market / Avg $-per-sqft / Median List Price), 2) listings grid, 3) "[City] Real Estate Market" paragraph (median price, home age/style, named subdivisions), 4) "[City] Community Amenities" (parks, National Historic Register sites for Broussard), 5) "[City] School Information" (district + named schools), 6) "[City] Local Highlights" bullet list, 7) agent CTA with phone number repeated, 8) link to the free market analysis / valuation page |
| Valuation/lead page (`/sellers/free-market-analysis/`) | Long-form intake form: name/email/phone, moving timeline, interest type, full property detail fields (type/beds/baths/sqft/garage/basement/year built), free-text "what I love about my house" |
| Footer | Repeated on every page: office address, phone (O + M numbers), "Have a Question or Want a Free Market Report?" CTA |
| URL quirk | Youngsville's URL is `/-youngsville/` (leading hyphen) — a CMS artifact, not a pattern to replicate |

### Keaty Real Estate — keatyrealestate.com `[verified]`

| Element | What's actually there |
|---|---|
| Homepage headline | "Get An Instant Offer On Your Home!" — aggressive iBuyer-style framing |
| **Friction pattern (caution, not a model)** | The homepage is gated behind a **mandatory login/registration modal** (Google/Facebook/email sign-up) before a visitor can browse freely — this is a BoldTrail/IDX platform default, not a deliberate choice, but it's a real UX cost worth naming explicitly so it isn't accidentally copied |
| Video | YouTube video loop embedded near the top (agent-branded property/intro video) |

---

## Part C — Top 10 Reusable Patterns, Ranked by Impact/Effort

| # | Pattern | Who does it well | Why it likely works | How Carrie adapts it | Effort | Ethics check |
|---|---------|-------------------|----------------------|------------------------|--------|----------------|
| 1 | **Home-value request page, framed as education + a real form (not a fake instant tool)** | lafayettehomepros.com (#2 for "how much is my house worth lafayette," above Zestimate), therealjessicabroussard.com (#4, above Homes.com's own tool) `[verified]` | This is the single most direct evidence in this sweep that an agent-branded valuation page can out-rank the big portals' own tools for exactly the query with the highest seller intent | `sell_my_house_lafayette.md` already specs a "request your home value" form (not a fake automated estimate) — this is validated as correct. Add a short **educational block** near the form modeled on Jessica's page: "How is my home's value calculated?" (CMA basics, 2–3 sentences) and an honest "why an online estimate alone isn't enough" line — builds the same trust Jessica's page does, without implying a tool Carrie doesn't have | Low | Write original explanatory copy; do not copy Jessica's or Zillow's wording verbatim. Do not build or fake an "instant" widget — the brief's existing honesty constraint is correct and should stay |
| 2 | **Persistent, always-visible "What's my home worth?" micro-CTA** | topagent337.com — separate secondary nav bar, present on every page regardless of scroll `[verified]` | Removes friction for the single highest-intent visitor type (a seller) regardless of which page they land on | If the platform (BoldTrail) supports a persistent header/utility bar, add a "Home Value" link pointing to `sell_my_house_lafayette`. If not available site-wide, at minimum link to it from every other page brief's "internal links" section (already partially true — audit `lafayette_realtor.md`, `lafayette_listing_agent.md` internal-link lists to confirm all 7 pages link here) | Low | No ethics concern — pure information architecture |
| 3 | **Verified-stat trust ribbon near the top of the hub page** | Sean Hettich's yearly Top Producer ribbon; Jessica's 6-tile stat row `[verified]` | Immediate, scannable authority signal before the visitor has to read a paragraph | `lafayette_realtor.md` section 10 ("Trust signals") lists Carrie's verified numbers; as of the 2026-07-08 correction her strongest verified figure is now **185 Google reviews / 5.0** (`data/public_assets.yaml`), which should lead the stat row ahead of the 29 Zillow reviews/5.0, team of 4, home stager, certified mentor. Turn the list into a visual stat-tile row near the top of the page instead of burying it under "Why Local Buyers and Sellers Choose Carrie." **Critical constraint:** use ONLY the `[verified]` figures — do not add production/volume numbers, since `known_claims.yaml` flags 174 closed sales/$44.6M and similar figures as unverified/conflicting | Low | Do not fabricate or borrow competitor-style volume stats ($105M+, 353 reviews, etc.) — those are specific to Sean/Jessica and using anything like them for Carrie without her own verified numbers would be a false claim |
| 4 | **Testimonials tagged with sale date + city + transaction type, not just a star badge** | topagent337.com `/about/reviews/` `[verified]` | Turns generic "5.0 stars" into specific, checkable proof tied to a real place and year — reads as more credible than an aggregate score alone | `lafayette_realtor.md` and `lafayette_listing_agent.md` both note "quote 1–2 real reviews if Carrie can supply permission." Extend that: if/when Carrie gets permission for even 3–5 reviews, format them exactly this way — quote + city + year + transaction type — rather than as an unattributed pull-quote | Low (once permission exists) | **Do not** copy Sean's or Jessica's actual review text or reviewer names under any circumstance — those are their clients' words, not reusable content, and reusing them would be both dishonest and a likely ToS/copyright problem. Only Carrie's own permissioned reviews may be used |
| 5 | **Consistent area-page skeleton: market snapshot → subdivisions → amenities/history → schools → agent CTA → valuation link** | lafayettehomepros.com's Broussard/Youngsville/Sugar Mill Pond pages `[verified]` | This exact structure independently ranked for a specific micro-community query ("sugar mill pond youngsville homes," #4) against portals and builders — proof the structure itself is SEO-competitive, not just the domain authority | `youngsville_realtor.md` and `broussard_realtor.md` already cover most of these H2s (growth story, subdivisions, schools, commute). Two additions: (a) add an explicit "Local Points of Interest / Amenities" H2 (parks, historic sites, civic identity) — currently implied but not a dedicated section; (b) end each page with an explicit link to the `sell_my_house_lafayette` valuation-request CTA, mirroring how every lafayettehomepros area page closes with a market-analysis link | Low–Medium (content research effort for `[client-confirm]` local details already flagged in both briefs) | Do not fabricate subdivision names, amenities, or historic-site claims Carrie hasn't verified — both briefs already flag this correctly with `[client-confirm]` tags; keep that discipline |
| 6 | **Three-way, intent-splitting hero CTA (Buy / Sell / Connect) instead of one generic button** | therealjessicabroussard.com `[verified]` | Pre-sorts visitors by intent at the first click, likely reducing bounce for a visitor who doesn't want to read a full bio before acting | `lafayette_realtor.md`'s current CTA is single-path ("Call or text Carrie" + contact form). Consider a 3-button variant once the buyer/seller-specific pages exist: **Buying?** → `lafayette_buyers_agent`, **Selling?** → `lafayette_listing_agent`/`sell_my_house_lafayette`, **Just want to talk?** → contact form/phone. This is a genuine structural upgrade, not just copy | Low–Medium (depends on whether BoldTrail's bio/page editor supports button rows) | No ethics concern |
| 7 | **"Interested in..." qualifying dropdown on every lead form** | Both therealjessicabroussard.com and lafayettehomepros.com forms `[verified]` | Cheap to build, immediately tells Carrie what the lead wants without a follow-up email, and slightly increases perceived form legitimacy (feels like a real intake process, not a generic contact box) | Every page brief with a form CTA (`sell_my_house_lafayette`, `lafayette_listing_agent`, `lafayette_buyers_agent`, `first_time_homebuyers_lafayette`) should specify this same field: a simple "I'm interested in: Buying / Selling / Both / Just Asking" dropdown, if the platform's form builder supports custom fields | Low | No ethics concern |
| 8 | **Blog/content module cross-linked from the homepage, covering local-interest (not just transactional) topics** | lafayettehomepros.com's "Recently from Our Blog" (Things to Do in Lafayette, Best Neighborhoods, Best Places to Live) `[verified]` | Captures top-of-funnel local-interest search traffic (the "moving to lafayette la" query type — see Part A #8) that a purely transactional page never will, and adds internal-linking depth | `first_time_homebuyers_lafayette.md` is already the closest brief to this model (education-first). Consider one additional lightweight content piece post-MVP — a short "why people move to Lafayette / Youngsville" post — as a phase-2 idea to capture relocation-intent traffic the 7 core briefs don't target. Not urgent; flag as a future content-calendar item in `06_content_strategy.md`, not a rewrite of the existing briefs | Medium (new content, not a brief edit) | Original writing only; do not paraphrase lafayettehomepros' actual blog posts |
| 9 | **Honest "why this isn't just an automated number" framing on valuation content** | therealjessicabroussard.com's "How Accurate is the Online Home Valuation?" section explicitly says online estimates "may not factor in recent renovations, unique features... consider scheduling an in-person appraisal" `[verified]` | Builds trust by being honest about a tool's limits instead of oversell — ironically strengthens the CTA to talk to a human | Directly reinforces `sell_my_house_lafayette.md`'s existing instruction not to imply an automated valuation exists if it doesn't. Use this same honest framing as the *reason* the page routes to a human-reviewed request instead of a number: "A quick online number can't see your renovations or your neighborhood's real comps — that's what a personal CMA is for." | Low | Original copy; concept (not text) borrowed |
| 10 | **Cancelled/expired-listing-turned-SOLD stat as a specific objection-handler** | topagent337.com: "139+ cancelled or expired listings turned into SOLD" `[verified]` | Directly answers the specific fear of a seller whose house didn't sell with a previous agent — sharper than a generic "results speak for themselves" | Only adopt if genuinely true for Carrie — `[client-confirm]` whether she has any comparable track record (does she have relisted/expired-turned-sold transactions?). If yes, add as a trust signal on `lafayette_listing_agent.md`. If not confirmed, skip — do not invent an equivalent number | Low (if the underlying fact exists) | Do not publish this stat, or any similar-sounding one, without Carrie confirming an actual, current, accurate count — same discipline already applied to the "174 closed sales" figure flagged in `known_claims.yaml` |

---

## Part D — Do NOT Copy List

1. **Any competitor's testimonial/review text or reviewer names** — these are the competitor's clients' words, not Carrie's, and reusing them (even reworded closely) risks both plagiarism/ToS issues and outright dishonesty about whose clients said what.
2. **Any competitor's photos** — headshots, listing photos, staged-home photos, logo marks. All visually identifying assets are the competitor's/their clients' property.
3. **Specific production statistics belonging to a competitor** — Sean Hettich's "353 reviews / 139+ expired listings / $47.3M 2025 volume," Jessica Broussard's "$105M+ / 200+ families / Top 1%." These are proof points *for them*; using anything numerically similar for Carrie without her own verified figures is a false claim, not a "pattern" to adapt.
4. **Jessica Broussard's or Keaty's proprietary embedded valuation-tool widget** — these are third-party vendor JS tools (likely a BoldTrail/Follow Up Boss-style valuation integration) tied to their specific platform license. Carrie's site should not fake an equivalent instant-estimate widget; the brief's existing "request your home value" form (human-reviewed, not automated) is the correct, honest substitute.
5. **Keaty Real Estate's forced-login/registration wall** — flagged in Part C as a caution, not a pattern: gating the entire homepage behind a mandatory sign-up modal is a friction cost, not a feature worth replicating.
6. **Any specific neighborhood, school-zoning, or historic-site claim made on a competitor's page** — e.g., lafayettehomepros' Broussard "National Historic Register" sites, or Youngsville school-zoning details. Even where accurate for their content, these must be independently verified for Carrie's pages (the `youngsville_realtor.md` and `broussard_realtor.md` briefs already flag equivalent details as `[client-confirm]` — that discipline stays; don't shortcut it by lifting a competitor's factual claims uncredited).
7. **Site copy/paragraph structure verbatim** — e.g., Jessica's "How is the Valuation of My Home Calculated?" answer text, or lafayettehomepros' "Community Amenities" paragraphs. Adapt the *concept* (what topic to cover, in what order) — write original sentences.

---

## Part E — Refinements to Existing Page Briefs

### `lafayette_realtor.md` (hub)
- Add a persistent "Home Value" / valuation micro-CTA link (Pattern #2) — confirm every other brief's internal-links list actually points here (spot-check: `youngsville_realtor.md`, `broussard_realtor.md`, `lafayette_buyers_agent.md` all currently link out to `sell_my_house_lafayette` only indirectly via `lafayette_listing_agent`; consider a direct link from each).
- Convert the existing "Trust signals" list (section 10) into a visual stat-tile row near the top of the page (Pattern #3), using only the brief's already-`[verified]` figures — no new numbers.
- Consider the 3-way intent-splitting hero CTA (Pattern #6) once buyer/seller pages are live, replacing or supplementing the single "Call or text Carrie" CTA.

### `youngsville_realtor.md` / `broussard_realtor.md`
- Add an explicit "Local Points of Interest / Amenities" H2 (parks, civic identity, any historic designation) as its own section rather than folding it into "Why Buyers Choose..." (Pattern #5) — matches the structure that independently ranked for a named-community query.
- Add an explicit closing link to `sell_my_house_lafayette`'s valuation-request CTA, mirroring how every winning area page in this sweep ends with a value-estimate link.
- Flag as a phase-2 idea (not required for MVP): a dedicated Sugar Mill Pond subsection or future standalone page under Youngsville, since that micro-community name independently ranks (Part A, #6) — do not build this now, just note it for the content roadmap.

### `sell_my_house_lafayette.md`
- Validated, no change needed: the brief's existing "request a home value, not a fake instant estimate" approach is exactly what the two ranking competitor valuation pages do successfully (Pattern #1) — this is confirmation, not a gap.
- Add a short educational trust block near the form (Pattern #1/#9): 2–3 sentences on how a real CMA differs from an automated online number, framed honestly per the brief's existing no-fake-tool constraint.
- Add the "Interested in..." qualifying dropdown to the lead form spec (Pattern #7).
- Confirm the brief's title-tag decision to target "sell my house Lafayette" rather than "sell house fast Lafayette" — validated by Part A #10 (the "fast" variant is a 100%-cash-buyer SERP with zero room for a traditional agent).

### `lafayette_listing_agent.md`
- If Carrie has any relisted/previously-expired listings she successfully sold, add that as a trust signal (Pattern #10) — `[client-confirm]` required, do not publish without her confirming a real, current number.
- When permissioned reviews become available, format them with sale city + year + transaction type (Pattern #4), not just a star rating.

### `first_time_homebuyers_lafayette.md`
- No structural change; the brief's existing approach (link out to LHC.la.gov and similar authorities for program specifics, rather than trying to restate eligibility rules) is validated by Part A #9 — no agent site competes with government/finance sites on program-detail SEO, so Carrie's differentiation should stay "personal local guidance," not "alternate authority on program rules."

### `lafayette_buyers_agent.md`
- Add the "Interested in..." qualifying dropdown to its consultation-booking form (Pattern #7); no other structural changes indicated by this sweep.

---

## Method Notes & Limitations

- Query sweep used `firecrawl_search` (10 queries, 8 results each) run 2026-07-08 from a neutral, non-Lafayette search context — see the SERP Approximation Caveat above.
- Page anatomy used `firecrawl_scrape` against public pages only: topagent337.com (homepage + reviews page), therealjessicabroussard.com (homepage + home-valuation page), lafayettehomepros.com (homepage + Broussard + Youngsville + free-market-analysis pages), keatyrealestate.com (homepage). No login walls were bypassed, no forms were submitted, no bulk crawling was performed.
- JSON-LD schema was directly checked (raw HTML `application/ld+json` search) only for topagent337.com's homepage, where none was found `[verified]`. Schema presence on the other competitor pages was not checked in this pass (markdown-only fetches were used to manage response size) — treat those as unconfirmed, not "no schema present."
- All content-length, market-stat, and CTA-copy figures cited in Part B are what was live at fetch time (2026-07-08) and will drift — do not treat specific numbers (e.g., "350+ Zillow reviews," "$105M+") as current beyond this date; they are cited only to illustrate the *pattern* of displaying such a stat, not as facts about Carrie's market.
