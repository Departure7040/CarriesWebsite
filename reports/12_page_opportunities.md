# 12: Page Opportunities — Synthesis of 39 Raw Ideas Across 5 Research Modes

**Date:** 2026-07-11
**Purpose:** Synthesize page-opportunity research gathered via 5 independent research modes into a scored, deduped, buildable roadmap for `carriebilleaud.com` (static site + small Python server; one technical builder, Brook). Reads against `reports/11_top10_ranking_drivers.md` (ranking drivers), `reports/06_content_strategy.md` (content principles), and `data/keyword_intent_map.csv` (existing coverage).

**Tagging key:** `[verified]` = the underlying claim was found stated concretely in the raw research evidence (a search snippet, a cited source, a Reddit quote) — this project did not independently re-fetch every source in this pass, so "verified" here means "verified as present in the supplied research," not independently re-checked by this report. `[inferred]` = this report's own synthesis, clustering judgment, or extrapolation, not directly stated in the raw evidence. `[client-confirm]` = needs Carrie's local knowledge before publishing.

---

## (a) Method + Caveats

39 raw page ideas were supplied from 5 source modes: **question-mining** (8 ideas — what buyers/sellers search for), **competitor-page-inventory** (7 ideas — page types top local competitors have that Carrie's site lacks), **forum-and-reddit** (8 ideas — r/Acadiana / r/Louisiana threads showing real relocator/buyer concerns), **louisiana-specific** (7 ideas — LA statutory/regulatory quirks with no national equivalent), and **tools-and-lead-magnets** (9 ideas — interactive tools and gated content competitors/industry blogs use).

Caveats:
- **Demand signals are secondhand.** None of the 39 raw ideas cite Search Console, keyword-volume tools, or ad-platform data for Carrie's actual market — they're inferred from SERP presence, competitor page existence, and forum thread frequency. Treat "strong demand" as "strong topical relevance," not a confirmed search-volume number.
- **This report evaluates against a specific platform constraint the raw research did not have:** the site is a **static site + small Python server**, not a full CMS or app backend. Several raw ideas (automated valuation tools, live eligibility calculators, quiz engines, listing-alert segmentation) assume a data/backend layer that isn't confirmed to exist here. This is the single biggest filter applied in section (e).
- **Two independent prior reports already ruled on part of this space.** `reports/11` and `reports/04b` both found that broad relocation queries ("moving to lafayette la," "is lafayette safe," cost-of-living generically) are owned by Reddit/Facebook groups/moving blogs, with **zero** agent/team presence ranking for the broad head terms across a 10-agent competitive cohort. This report does not re-litigate that finding — it's applied directly to cluster C6 below.
- Competition notes in the raw data are qualitative (source counts a search returned), not authority/backlink metrics.

---

## (b) Clustering — Dedupe and Convergence

Grouping the 39 raw ideas by underlying topic surfaces **convergence**: when the same underlying need shows up independently across multiple source modes, that's a stronger signal than any single mode alone (different research methods hitting the same wall from different directions).

| Cluster | Raw ideas rolled up | Modes converging | Convergence strength |
|---|---|---|---|
| **C1. Flood zones & flood insurance** | "Understanding Flood Zones in Lafayette," "Hurricane & Flood Preparedness," "Flood Insurance & Hurricane Protection" (Reddit), "Flood Insurance Requirements & Annual Cost Guide" (LA-specific) | question-mining, forum-and-reddit, louisiana-specific | **Strongest in the set — 3 of 5 modes, 4 raw ideas** `[verified: each mode surfaced it independently without cross-referencing the others]` |
| **C2. Louisiana closing process (attorney/notary/costs)** | "Louisiana Closing Costs Explained," "Why LA Requires a Closing Attorney," "Notary-Based Real Estate Closing Process" | question-mining, louisiana-specific | 2 of 5 modes, 3 raw ideas |
| **C3. Homestead exemption & property tax** | "Lafayette Property Tax & Homestead Exemption," "Louisiana Homestead Exemption: How to File," "Volunteer Firefighter Exemption" (niche sub-item) | question-mining, louisiana-specific | 2 of 5 modes, 3 raw ideas |
| **C4. Market overview & seasonal timing** | "Lafayette Real Estate Market Overview," "When to Sell Your House: Seasonal Timing," "Hyper-Local Market Report" | question-mining, tools-and-lead-magnets | 2 of 5 modes, 3 raw ideas — but competition explicitly flagged "strong" (Redfin/Zillow/Homes.com) |
| **C5. Neighborhood decision hub (comparison/safety/schools/family)** | "Youngsville vs Broussard vs Lafayette," "Is Lafayette Safe? Crime Guide," "Best Schools in Lafayette," "Family-Friendly Neighborhoods," "Neighborhood Guides hub" (competitor), "Which Acadiana Neighborhood Quiz" | forum-and-reddit, competitor-page-inventory, tools-and-lead-magnets | 3 of 5 modes, **6 raw ideas — largest single cluster** |
| **C6. Broad relocation / cost-of-living / jobs / walkability** | "Is Lafayette Right for You?," "Real Cost of Living," "Jobs & Career Opportunities," "Do You Need a Car? Walkability," "Relocation Guide to Acadiana PDF" | question-mining, forum-and-reddit, tools-and-lead-magnets | 3 of 5 modes, 5 raw ideas — high demand, but see (e): already ruled unwinnable by `reports/11`/`04b` |
| **C7. Home valuation / seller lead tool** | "Home Valuation Tool," "Home Value Estimator Tool" | competitor-page-inventory, tools-and-lead-magnets | 2 of 5 modes; reinforced by `reports/11`'s independent finding that valuation pages are a proven ranking/conversion driver |
| **C8. Testimonials / client stories page** | "Testimonials/Client Stories gallery" | competitor-page-inventory | 1 mode, but **converges with an internal-audit finding** (`seo_backlog.csv` row 32: ~50 testimonials already exist but are stranded on the wrong URL) |
| **C9. Blog/educational content hub** | "Blog/Educational content hub" | competitor-page-inventory | 1 mode — conflicts with content principle #1 (see e) |
| **C10. Developments/new construction page** | "Developments/New Construction focused page" | competitor-page-inventory | 1 mode |
| **C11. Video content gallery** | "Video content gallery page" | competitor-page-inventory | 1 mode, thinnest evidence (only 1 of ~5 competitors surveyed has this) |
| **C12. Results/transaction showcase** | "Results/Transaction Showcase page" | competitor-page-inventory | 1 mode — conflicts with content principle #3 (no unverified metrics) |
| **C13. Buyer/seller process flowchart** | "Buyer/Seller Process flowchart page" | competitor-page-inventory | 1 mode — overlaps existing 4 service pages |
| **C14. USDA rural loan eligibility** | "USDA Rural Loan Eligibility Calculator" | louisiana-specific | 1 mode, but concrete geo/income data cited |
| **C15. Louisiana property disclosure requirements** | "Property Disclosure Requirements Checklist" | louisiana-specific | 1 mode, concrete statutory citation (pre-contract timing) |
| **C16. Rent-vs-buy / affordability calculators** | "Rent vs. Buy Calculator," "Home Affordability Calculator" | tools-and-lead-magnets | 1 mode, national commodity tools |
| **C17. Seller prep checklist / readiness quiz** | "Seller Preparation Checklist" | tools-and-lead-magnets | 1 mode |
| **C18. New listing alert signup** | "New Listing Alert Signup" | tools-and-lead-magnets | 1 mode |
| **C19. First-time buyer guide** | "First-Time Home Buyer Guide for Lafayette LA" | question-mining | 1 mode — **overlaps an existing site page** (`site/services/first-time-buyers.html`) `[verified: file exists in repo]` |

---

## (c) Scored Opportunity Matrix

Scored for evidence strength, lead-intent (does this attract someone about to transact, not just browse?), competition thinness, Louisiana-specificity moat, and build effort **on this specific static+small-Python-server stack**. Priority 1 (skip) – 5 (build now).

| Cluster | Evidence strength | Lead-intent | Competition thinness | LA-specificity moat | Build effort (static site) | Priority |
|---|---|---|---|---|---|---|
| C1 Flood zones & insurance | Strong (3 modes, 4 ideas) `[verified]` | High — buyer evaluating a specific area/purchase | Thin (only FEMA/Zillow generic pages rank) `[verified]` | Very high — mandatory in high-risk LA zones, NFIP vs. private | Low-Medium — static content, link out to FEMA's own zone lookup rather than rebuild it | **5** |
| C7 Home valuation lead tool | Moderate (2 modes) + reinforced by `reports/11` ranking-driver #4 `[verified]` | Very high — seller ready to transact | Fierce (most-contested intent per `reports/11`, all 10 cohort agents present) but **provably winnable** with owned content `[verified in 04b]` | Low, but doesn't need it | Low-Medium — static form + manual CMA follow-up (matches already-spec'd human-reviewed approach in `sell_my_house_lafayette.md`) | **5** |
| C5 Neighborhood decision hub | Strong (3 modes, 6 ideas, direct Reddit quotes) `[verified]` | High — active relocation/buy decision point | Thin (no dedicated realtor guide found) `[verified]` | High — hyper-local names (Youngsville, David Thibodaux STEM) | Medium — content-heavy, `[client-confirm]`-dependent, but no backend/quiz engine required if built as a content hub, not a quiz | **5** |
| C2 LA closing process (attorney/notary) | Strong (2 modes, 3 ideas, concrete citations) `[verified]` | High — buyer/seller near closing, esp. relocators unfamiliar with the mechanic | Thin-moderate (national content genericizes this) `[verified]` | Very high — genuinely unique closing mechanic, not a rehash | Low — static content | **5** |
| C3 Homestead exemption & property tax | Strong (2 modes, 3 ideas, concrete $ figures) `[verified]` | Moderate-high — post-purchase but funnel-relevant; also useful seller-side (proration) | Thin (only government assessor pages rank) `[verified]` | High | Low — static content | **4** |
| C8 Testimonials page | 1 mode, but converges with internal audit (`seo_backlog.csv` row 32) `[verified]` | Trust/support layer across every page, not a standalone conversion page | 2 of surveyed competitors have this | N/A | Very low — content already exists, needs a real home | **4** |
| C15 LA property disclosure checklist | 1 mode, concrete statutory timing citation `[verified]` | High — seller nearing listing | Moderate | High — pre-contract delivery timing is LA-specific | Low — static content | **4** |
| C14 USDA rural loan eligibility (informational) | 1 mode, concrete income/geo data `[verified]` | High — rural-adjacent buyers (Youngsville/Scott/Maurice) | Thin | High — parish-specific eligibility | Low, **if** scoped as informational + link to USDA's own map (not a rebuilt eligibility engine) | **4** |
| C4 Market overview & seasonal timing | Moderate (2 modes) but competition explicitly "strong" (Redfin/Zillow/Homes.com) `[verified]` | High | Crowded — not thin | Low (just localized numbers) | Medium — requires ongoing data refresh, a real weakness for a static site | **3** |
| C17 Seller prep checklist | 1 mode | High — seller | Thin locally, but a commodity format | Low | Low — static checklist | **3** |
| C10 Developments/new construction | 1 mode | Moderate | Moderate | Moderate | Medium — needs ongoing subdivision curation, heavy `[client-confirm]` | **2-3** |
| C16 Rent-vs-buy / affordability calculators | 1 mode | Moderate | Dominated by national platforms | None | Low (pure client-side JS math, no data feed needed) but low differentiation | **2** |
| C18 New listing alert signup | 1 mode | High in theory | Dominated by Zillow/Realtor.com's own free versions | Low | Medium-High — true custom segmentation needs IDX/email infra not confirmed available | **2** |
| C11 Video gallery | 1 mode | Low-moderate | Only 1 competitor has it | N/A | Low, but no confirmed video asset library beyond social clips | **2** |
| C13 Buyer/seller process flowchart (standalone) | 1 mode | Moderate | Moderate | Low | Redundant with 4 existing service pages | **1-2** |
| C19 First-time buyer guide (as new page) | 1 mode | High, but **already exists** on-site | N/A | N/A | N/A — enhance, don't duplicate | **1** (as new page) |
| C6 Broad relocation/COL/jobs/walkability | Strong demand (3 modes, 5 ideas) `[verified]` | High-looking, but... | ...**zero agent presence ranks for the broad terms** per `reports/11`/`04b` `[verified]` | High topically, doesn't help since the terms aren't winnable | Low-medium | **1** |
| C9 Blog/educational content hub | 1 mode | N/A — violates lead-intent-first principle | Competitors have 30-50+ posts; a volume play | N/A | High (ongoing volume) | **1** |
| C12 Results/transaction showcase | 1 mode | Trust, but built on numbers Carrie doesn't have | N/A | N/A | Low, but blocked on data | **1** |

---

## (d) Top 8 Recommended

1. **Flood Zones & Flood Insurance Guide for Lafayette Parish Buyers** — angle: which zones carry mandatory insurance and what it actually costs, mapped to real neighborhoods. Links from/to: all 7 area pages, `buyers-agent.html`, `first-time-buyers.html`.
2. **Home Valuation Request Page** (human-reviewed, not automated) — angle: "what's my Lafayette home worth" backed by a real CMA, not a Zestimate guess. Links from/to: `sell-my-house.html`, `listing-agent.html`, homepage `#reviews`.
3. **Neighborhood Decision Hub** — angle: Youngsville vs. Broussard vs. Lafayette vs. Carencro/Scott/Maurice on safety, schools, and family fit, one honest local take. Links from/to: all 7 area pages, homepage `#areas`.
4. **Louisiana Closing Process Guide** (attorney-certified title + notary closing) — angle: demystify the one mechanic every relocating buyer is confused by. Links from/to: `buyers-agent.html`, `first-time-buyers.html`, `sell-my-house.html`.
5. **Homestead Exemption & Property Tax Savings Guide** — angle: the real $787/yr number and how to file it in Lafayette Parish. Links from/to: `first-time-buyers.html`, area page footers.
6. **Testimonials / Client Stories Page** — angle: give the ~50 stranded testimonials and 185 Google reviews an actual home. Links from/to: homepage `#reviews`, every service page CTA.
7. **Louisiana Property Disclosure Requirements Checklist** — angle: LA's pre-contract disclosure timing, explained simply, for sellers who don't want a surprise. Links from/to: `listing-agent.html`, `sell-my-house.html`.
8. **USDA Rural Loan Eligibility (informational)** — angle: which parts of Youngsville/Scott/Maurice qualify for zero-down financing, with a link to USDA's own map. Links from/to: `youngsville.html`, `scott.html`, `maurice.html`, `first-time-buyers.html`.

**Strongest convergence finding:** Flood zones/flood insurance is the one topic three independent research modes (question-mining, forum-and-reddit, louisiana-specific) surfaced without cross-referencing each other — the clearest, least-arguable signal in the whole set.

---

## (e) Explicit DO-NOT-BUILD List

- **Broad relocation/cost-of-living/jobs/walkability pages (C6)** — high raw demand, but `reports/11` and `04b` already found zero agent/team presence ranks for these exact query types across a 10-competitor cohort; owned by Reddit/Facebook groups/moving blogs. `[verified]`
- **Automated "instant" home-value estimator (Zestimate-style AVM)** — no MLS-sold-comp data feed is confirmed available on the static+small-Python stack; build the human-reviewed request-a-CMA version instead (already in C7/top-8 #2).
- **"Which Acadiana Neighborhood Fits You" quiz engine** — the underlying intent is better served by the content-only Neighborhood Decision Hub (C5); a quiz UI is backend/logic complexity this stack doesn't need to take on for the same payoff.
- **Blog/educational content hub matching competitors' 30-50+ article volume (C9)** — directly conflicts with content principle #1 ("not a blog-volume play, no generic filler"); the existing 7-page-brief plan plus a steady 2-4 posts/month cadence is the deliberate alternative, not a gap.
- **Results/Transaction Showcase page with metrics (C12)** — conflicts with content principle #3 (no unverified metrics as fact); `reports/11` already confirmed Carrie has no audited transaction-volume figure to display — do not manufacture one to match competitors.
- **Fully automated, segmented New Listing Alert Signup (C18)** — real segmentation needs IDX/email-automation infrastructure not confirmed available; national platforms (Zillow/Realtor.com) already give buyers this for free with more data. A manual/lightweight version could exist later, not as scoped.
- **Rent-vs-Buy and Home Affordability calculators as dedicated pages (C16)** — technically buildable (pure client-side math, no data feed needed), but zero Louisiana-specificity and dominated by national tools (Zillow, NerdWallet) with more inputs; low differentiation for the effort.
- **USDA eligibility as a live interactive calculator** — only the informational/static version (top-8 #8) is recommended; the real-time eligibility lookup is USDA's own map/API, not ours to rebuild.
- **Volunteer Firefighter Property Tax Exemption as its own page (C3 sub-item)** — audience is too narrow for a standalone page; fold it into the Homestead Exemption guide as one FAQ line instead.
- **Video content gallery page (C11)** — thinnest evidence in the set (1 of ~5 competitors surveyed), and no confirmed video asset library beyond existing social clips.
- **Buyer/Seller Process flowchart as new standalone pages (C13)** — redundant with the 4 existing service pages; enhance those with step-by-step sections instead of creating doorway-adjacent duplicates (content principle #4).

---

## (f) Note on `[client-confirm]` items

C5 (Neighborhood Decision Hub) references specific schools (e.g., David Thibodaux STEM Magnet, Lafayette High's gifted program) and safety comparisons pulled from Reddit threads — these are `[verified]` as *stated in the raw research* but need Carrie's local confirmation before publishing as the site's own claims, consistent with `06_content_strategy.md` principle #2. Same applies to any subdivision-level detail in C10 if pursued later.


---

*Orchestrator note (2026-07-11): Recommendation #2 (human-reviewed valuation request page) was BUILT the same night as this research ran — `site/services/sell-my-house.html` implements exactly this pattern; its backlog row was removed as already-done. Recommendation #6 (testimonials home) was already in the backlog from the 2026-07-08 vendors-page discovery. Net-new builds from this report: flood guide, neighborhood decision hub, closing-process guide, homestead-exemption guide, disclosure checklist, USDA-eligibility guide.*
