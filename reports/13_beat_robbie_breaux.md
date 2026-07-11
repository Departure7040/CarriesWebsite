# 13: Beat Robbie Breaux — Competitive Teardown of lafayettehomepros.com

**Date:** 2026-07-11
**Target:** Robbie Breaux & Team, powered by REAL Broker LLC — lafayettehomepros.com
**Why him:** #1 recurring competitor across the SERP sweep in `reports/11_top10_ranking_drivers.md` (13 appearances, Lafayette/Youngsville/Scott/Maurice), with the largest on-site architecture in the 10-agent cohort.

**Tagging key:** `[verified]` = confirmed via direct `firecrawl_map`/`firecrawl_scrape` fetch in this pass (2026-07-11) · `[inferred]` = reasonable conclusion from verified evidence, not itself independently fetched · `[client-confirm]` = needs Carrie's/Brook's input before acting.

**Method:** `firecrawl_map` on `https://www.lafayettehomepros.com` (sitemap-included, limit 300) returned 155 URLs — effectively the full site as far as the sitemap/internal-link graph exposes it, since the result came in well under the 300 cap. Three representative pages were scraped: a price-band page (`/lafayette-by-price-200000-300000`), a blog post (`/blog/lafayette-cost-of-living-guide`), and one area page with `rawHtml` (`/scott`) to check schema/canonical/robots directly. No forms were submitted, no login walls bypassed, no bulk crawl performed — consistent with the task's "enumerate + a few page fetches" scope.

---

## (a) Full Page Inventory by Category `[verified via firecrawl_map, 2026-07-11]`

| Category | Count | Notes |
|---|---|---|
| **Area / community / parish pages** | **56** | Ranges from parish-level (Acadia, Iberia, St. Landry, St. Martin, Vermilion Parish, Lafayette Parish = 6) down to named subdivisions (Audubon, Bendel Gardens, Brookshire Gardens, Copper Meadows, Cypress Gardens, Fernewood, Freetown, Greenbriar, Le Triomphe, Monjardin, River Ranch, Rivergate, Sabal Palms, Saint Streets, Sugar Mill Pond = 15) plus ~35 town-level pages (Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice-adjacent towns, and a wide outer ring: Abbeville, Arnaudville, Basile, Breaux Bridge, Church Point, Crowley, Delcambre, Duson, Erath, Estherwood, Eunice, Grand Coteau, Gueydan, Henderson, Iota, Jeanerette, Kaplan, Krotz Springs, Melville, Mermentau, Morse, New Iberia, Opelousas, Port Barre, Rayne, St. Martinville, Sunset, Washington) plus a `/communities` hub |
| **Property-type pages** | 11 | All scoped to `/lafayette/` only: new-construction, condos, gated-community, golf-course, homes-on-water, RV-parking, luxury, open-houses, swimming-pool, townhomes, new-listings |
| **Price-band pages** | ~20 sampled `[verified]`, structurally 100s possible `[inferred]` | The scraped Lafayette $200-300k page's own price nav lists **11 price tiers** (under $100k through over $1M); the map surfaced this pattern applied to at least Lafayette, Youngsville, Carencro, Broussard, Crowley, Eunice, New Iberia, Breaux Bridge, Abbeville, St. Martinville, plus 2 compound type+price pages (luxury homes $800-900k, homes-on-water $300-400k). 11 tiers × ~50 area pages ≈ 500+ possible combinations — this is an auto-generated IDX filter grid, not a curated set (see (b)) |
| **Blog posts** | 23 | 22 under `/blog/` + 1 at root (`/foundation-issues-solutions`, same style/byline). All authored "By Robbie Breaux," oldest dated post found = Nov 2020 |
| **Blog category hubs** | 2 | `/blog/category/buying-a-home`, `/blog/category/all-about-lafayette` |
| **Buyer resource pages** | 8 | hub + first-time-buyers, mortgage-calculator, mortgage-pre-approval, personalized-home-search, escrow-now-what, financial-terms-glossary, what-are-closing-costs |
| **Seller resource pages** | 6 | hub + free-market-analysis (valuation lead form), marketing-your-home, adding-value, pricing-your-home, showing-your-home |
| **Tools/interactive** | 5 | mortgage calculator, mortgage pre-approval flow, free-market-analysis (lead-gen valuation form, not an automated AVM), personalized-home-search, property-tracker/saved-search login |
| **Relocation guide** | 1 | `/lafayette/moving-to-lafayette` |
| **About/team/reviews** | 4 | `/about`, `/agents/robbie-breaux`, `/contact`, `/contact/thank-you` — **no dedicated on-site reviews/testimonials page found** (unlike Sean Hettich's `/about/reviews/` per `04b`) |
| **Home** | 1 | — |
| **IDX search infrastructure (not content)** | 4 | `/property-search/site-map`, `/results`, `/property-tracker`, `/featured-listings` |
| **Individual MLS listing detail pages** | 13 sampled, effectively unbounded | e.g. `/property-search/detail/163/2600005350/...` — dynamically generated per active listing, churns with inventory; excluded from "his content" comparisons below |

**Total substantive, human-planned content pages (excluding raw listing details, IDX infra, and pagination duplicates): ≈128.** This corrects `reports/11`'s working estimate of "25-35 area/price pages" upward — the area/community footprint alone is **56**, not 25-35; the 25-35 figure appears to have undercounted the outer-ring towns and named subdivisions. `[verified, correction to 11]`

---

## (b) Depth Assessment — Substantive or Templated? Be Fair.

**His depth is real but sharply tiered — not uniform across 56 area pages.**

- **Flagship markets (Broussard, Youngsville, Sugar Mill Pond — confirmed in `04b`) get a genuine 8-part skeleton:** live MLS stat snapshot → listings grid → "[City] Real Estate Market" narrative paragraph → "Community Amenities" (named parks/historic sites) → "School Information" (named schools) → "Local Highlights" → agent CTA → valuation-page link. That is real, locally-specific writing, not filler. `[verified in 04b, 2026-07-08]`
- **Secondary markets are bare IDX shells.** Directly checked this pass: `/scott` (rawHtml + markdown) contains exactly one boilerplate sentence — *"View today's hottest Scott homes for sale below! To request further information about Scott, Louisiana properties for sale or to schedule a private showing, contact our local real estate experts today."* — followed immediately by the live stat snapshot and a 137-listing IDX grid. **Zero occurrences** of "Real Estate Market," "Community," "School," "Local Highlights," or "Amenities" as section headers anywhere on the page `[verified via direct grep of scraped rawHtml, 2026-07-11]`. Scott is Robbie's #1-appearing market in `reports/11`'s per-market breakdown (5 of 10 cohort agents) — yet his own page for it is the thinnest tier. This means the "thin market opportunity" flagged in `11` (Carencro/Scott/Maurice) is thin not just in competitor count but in *this specific competitor's own depth* — the bar to beat him there is low.
- **Price-band pages have zero unique copy at all** — confirmed on `/lafayette-by-price-200000-300000`: no intro sentence, no local framing, just a price-tier breadcrumb nav, the IDX grid, and the standard footer/blog module. This is the thinnest tier on the site — pure auto-generated filter output. `[verified]`
- **The blog is genuinely substantive, not thin.** `/blog/lafayette-cost-of-living-guide` (sampled) runs ~1,400+ words with a real table of contents, H2/H3 structure, and outbound citations to independent sources (bestplaces.net, rentcafe.com, payscale.com, census.gov, gasbuddy.com, thezebra.com, smartasset.com, care.com, valuepenguin.com). It reads as researched, not spun. `[verified]` It's dated (Nov 2020) and generic-national in topic selection (cost of living, mortgage types, home inspections, ROI upgrades) rather than Louisiana-statute-specific — see (f).
- **Fair conclusion:** this is not a site that's thin everywhere (it would be wrong to say so), nor one that's deep everywhere (also wrong). It's a site that invested real editorial effort in ~5 flagship pages and its blog, then used CMS/IDX templating to blanket ~50 more area pages and ~500 possible price-filter URLs with near-zero incremental copy per page. **The opening for Carrie is precision, not page count**: a handful of genuinely good pages in the markets that matter beats his long thin tail.

---

## (c) Head-to-Head

| Category | His count | Our count | Verdict |
|---|---|---|---|
| Area/community/parish pages | 56 `[verified]` | 7 (Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, Milton) `[verified, site/areas/]` | **Behind** on count; **parity-to-ahead** on the specific markets we've built (our pages are hand-written per-market, not IDX-shell) |
| Price-band pages | ~20 sampled, structurally 100s, zero unique copy | 0 | **Behind** on count; **opportunity** — his are thin, ours can be built with real copy from day one |
| Property-type pages (new construction/luxury/pool/condo/etc.) | 11, all thin IDX-feed | 0 (AHB new-construction page planned, backlog row 40) | **Behind** |
| Buyer/seller resource + tool pages | 14 resource pages + 5 interactive tools | 4 service pages, 0 interactive tools | **Behind**, especially on tools (mortgage calculator, saved-search) |
| Blog/article volume | 23 posts + 2 category hubs, general-topic | 0 blog posts | **Behind** on volume — but see content principle #1 in `06_content_strategy.md`: this is a deliberate non-goal, not an oversight |
| LA-specific / statutory guide content | 0 (none of his 23 posts touch flood zones, homestead exemption, LA notary/attorney closing process, or seller disclosure timing — checked against all 23 blog titles) `[verified via title review]` | 6 (flood-zones-insurance, homestead-exemption, louisiana-closing-process, seller-disclosure-checklist, usda-loans-acadiana, which-town-fits) | **Ahead** — this is a real, unmatched content moat |
| On-site testimonials/reviews page | 0 — reviews live off-site only (BirdEye/Facebook per `11`) `[verified: no reviews URL in map]` | 0 live yet, but 185 Google @ 5.0 verified + ~50 stranded testimonials + backlog row 32 already planned | **Parity today, ahead once built** |
| Schema markup (JSON-LD) | None found on the one page directly checked (`/scott` rawHtml, zero `application/ld+json` matches) `[verified]` | None (backlog row 8, todo) | **Parity** — both absent; not a differentiator per `11`'s own finding |
| Canonical/robots hygiene | Correct self-referencing canonical, `index,follow` robots on `/scott` `[verified]` | Not separately audited in this pass | Not compared here — see `03_website_technical_audit.md` for our own site's technical state |
| Total substantive pages | ≈128 | 18 | **Behind** on raw count, by design (see `06_content_strategy.md` — volume is not the strategy) |

---

## (d) The Overtake List (ordered)

1. **Price-band pages — build 3, not 20+.** He has ~20 sampled combinations (structurally hundreds possible via his IDX platform's area×price grid), and every one of them checked in this pass has zero unique copy — just a filtered listings feed. The underlying idea is genuinely useful for buyers (it's a real search-refinement pattern people use), so don't skip it — just don't copy his execution. Seed 3 curated pages from our own IDX search, each with real local copy, not just a filtered feed:
   - **"Homes Under $250k in Lafayette Parish"** — first-time-buyer angle, cross-link to `services/first-time-buyers.html` and `guides/usda-loans-acadiana.html`, name which neighborhoods/towns actually have inventory in this band.
   - **"$250k–$500k Move-Up Homes in Lafayette & Youngsville"** — the largest-volume band per the price page we scraped (232 active listings in just the Lafayette $200-300k slice alone) — cover what a move-up buyer actually gets at this price (sqft, subdivision tier, garage/yard norms).
   - **"$500k+ Luxury & Custom Homes in Acadiana"** — ties into the AHB new-construction partnership (backlog row 40) and Greenbriar/Sugar Mill Pond-tier subdivisions.

2. **Area-page expansion — follow the already-planned order, don't chase his tail.** He has 56 area pages; we have 7. The corrected finding here (see (a)) is that his footprint is even bigger than `11` estimated — but his depth is concentrated in ~5 flagship markets, and the one secondary market checked directly in this pass (Scott) is a bare IDX shell. **This validates, doesn't change, the existing backlog priority**: build Carencro, Scott, and Maurice (backlog rows 33-35, already `todo`) as genuinely good pages — the bar in Scott specifically is confirmed low. After those three, a Sugar-Mill-Pond-style named-subdivision page is the next tier, not a race to 56 pages of small outlying towns (Krotz Springs, Melville, Iota, Estherwood) that are 45+ minutes from Lafayette and irrelevant to Carrie's actual service area.

3. **Property-type landing pages — one at a time, only with a real story behind them.** He has 11 (new construction, condos, gated-community, golf-course, water, RV parking, luxury, open houses, pool, townhomes, new-listings), all thin IDX feeds by the same pattern as his price pages. Backlog row 40 (AHB new-construction partnership) already covers the highest-value one with genuine differentiation — a real builder relationship, not a filtered feed. Don't build the other 10 generically; only add one more (e.g., a luxury/waterfront page) if Carrie has actual current listings or a real specialty to point to — otherwise it's the exact thin pattern we're supposed to be avoiding.

4. **Interactive tools — this is a real, currently-unaddressed gap.** He has a mortgage calculator, a pre-approval flow, a personalized-home-search signup, and the free-market-analysis lead form (5 tools total) vs. our 0. `reports/11`'s delta #4 already flags "a lightweight valuation/lead-qualification tool" as a build priority, and `sell-my-house.html` already implements the honest, human-reviewed valuation-request version of that. The next cheapest, static-site-compatible win is a **client-side mortgage calculator** (pure JS math, no backend/data feed needed — fits the static+small-Python-server constraint that ruled out AVM-style tools in `12`).

5. **Testimonials/reviews page — he doesn't have one at all; we can own this format outright.** His reviews live entirely off-site (BirdEye/Facebook per `11`); there is no `/reviews` or `/testimonials` URL anywhere in his 155-URL map. Backlog row 32 (give the ~50 stranded testimonials a real home) is already `todo` — this pass adds no new information except confirming he has nothing to catch up to here. Priority stands as-is.

6. **Persistent home-value CTA in main nav — cheap structural upgrade.** Every page on his site repeats "Have a Question or Want a Free Market Report?" in the footer, and `04b`'s pattern #2 already recommends a persistent "What's my home worth?" link. Our nav currently has `services/sell-my-house.html` under the Services dropdown but no top-level, always-visible link. Low effort, direct copy of a validated pattern (see backlog addition below).

7. **Blog volume — explicitly do not chase.** He has 23 posts to our 0; `reports/12`'s DO-NOT-BUILD list (C9) already rules this out as conflicting with content principle #1. No action.

---

## (e) What NOT to Copy

- **The auto-generated price-band combinatorial grid itself (structurally hundreds of URLs, zero unique copy each).** This is a textbook thin/near-duplicate-content pattern at scale — same template, same footer, same blog module, only the price filter changes. It's a Google duplicate-content and low-value-page risk sitting on someone else's domain authority; replicating the *structure* (rather than the curated-3-page version in (d)#1) would hurt us more than it helps, especially on a smaller, newer domain with no authority cushion.
- **The long tail of thin, boilerplate-only area pages for towns outside Carrie's real service area** (Krotz Springs, Melville, Iota, Estherwood, Gueydan, Mermentau, Freetown, Washington, etc.) — one sentence + an IDX feed, no local knowledge behind them. Chasing his 56-page count with equivalent filler would be the definition of the doorway-page pattern this project's own content principles (`06_content_strategy.md`) already reject.
- **The `/-youngsville/` leading-hyphen URL** — a visible CMS artifact, not a pattern, just sloppy; don't inherit URL cruft like this in any new build.
- **No visible internal quality gate between flagship and filler pages.** A visitor (or a crawler) can tell within one click whether they're on Broussard/Youngsville (real content) or Scott/Krotz Springs (empty shell). Don't adopt a strategy where "coverage" numbers look good in a spreadsheet but fall apart on inspection — this report's own fairness check in (b) is exactly the kind of scrutiny a reviewer, journalist, or Carrie's own competitor-savvy clients could apply to us too.
- **Multi-language selector dropdown** (English/中文/Français/한국어/Italiano/日本語/Deutsch/Português/Русский/Español/Tiếng Việt) present in his nav on the scraped page — decorative nav clutter with no evidence of non-English search demand in this specific hyper-local market; not worth the UX cost of copying.

---

## (f) His Structural Weaknesses We Exploit

- **Review platform mismatch.** His reviews concentrate on BirdEye/Facebook, not Google (per `reports/11`'s per-realtor data — 286 BirdEye reviews, no confirmed Google count in the cohort exceeding Carrie's). His own site has **no dedicated on-site reviews page at all** — confirmed in this pass's full 155-URL map, zero `/reviews` or `/testimonials` path exists. Carrie's 185 Google reviews at 5.0 already tops every confirmed Google count in the `11` cohort `[verified in 11]`. A visitor comparing agents on Google itself — Maps, local pack, or a plain search — sees Carrie's number natively; Robbie's BirdEye number doesn't surface the same way. This is a genuine, already-identified structural edge, not a new finding, but this pass reconfirms he has nothing built to close it.
- **No schema markup found.** Directly checked `/scott`'s raw HTML in this pass: zero `application/ld+json` blocks. Consistent with `11`'s cohort-wide finding (1 of 10 competitors has any confirmed schema, and it's on a portal page, not an owned site). This tempers how much upside to expect from adding our own schema (it's not clearly a ranking lever in this market) but confirms there's zero downside risk of falling behind him on it — he has nothing here either.
- **Guide-content gap — confirmed, not just assumed.** All 23 of his blog post titles were reviewed against our 6 guide topics: none of his posts address FEMA flood zones/insurance, Louisiana's homestead exemption, the state's unusual attorney-certified-title + notary closing process, or LA-specific seller disclosure timing. His content is broad-national in flavor (types of mortgages, capital gains on a home sale, home inspection basics, ROI home-improvement projects, general real-estate-investment advice) — useful, well-written, but not Louisiana-statute-specific. Our 6 guides (`site/guides/`) occupy ground he hasn't touched at all. This is the single clearest, already-realized content moat in this teardown — not an aspirational item, something already built.
- **Depth is concentrated, not distributed** — his ~50 secondary/outer-ring area pages are IDX shells (see (b)). His apparent 56-page area footprint looks intimidating in a URL count but doesn't represent 56 pages of real local expertise — it's ~5 flagship pages plus a lot of CMS filler. Any market where Carrie builds a genuinely good page (not just a page) starts from a stronger position than the raw count suggests.
- **No visible interactive differentiation beyond commodity tools.** His mortgage calculator and pre-approval flow are standard IDX-platform features, not something client-facing that reads as uniquely his — this is table-stakes per `11`'s driver #5 finding on IDX integration, not a moat.

---

## Backlog Additions

Re-read `backlog/seo_backlog.csv` before appending (40 existing rows checked; Carencro/Scott/Maurice area briefs, testimonials page, JSON-LD schema, and AHB new-construction page are already present and were **not** duplicated below). Three new rows added for gaps this teardown surfaced that were not already tracked:
