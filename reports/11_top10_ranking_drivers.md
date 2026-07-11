# Top-10 Recurring Realtors: Ranking Drivers Across the Acadiana SERP Sweep

**Date:** 2026-07-11
**Purpose:** Extend `04_competitor_gap_analysis.md` and `04b_serp_patterns_and_reuse.md` with a systematic top-10 built from recurring appearances across Lafayette/Youngsville/Broussard/Carencro/Scott/Maurice/Acadiana sweeps, cross-referenced against per-realtor page anatomy. Companion data file: `data/top10_realtors.csv` (one row per realtor).

**Tagging key:** `[verified]` = confirmed via direct fetch/scrape of a live source · `[inferred]` = reasonable conclusion from the provided anatomy data, not independently re-verified in this pass · `[client-confirm]` = needs Carrie's input · unlabeled anatomy fields marked "unknown" in the source data are left as **unknown** here — they are not converted into estimates.

---

## (a) Method + Caveats

This report synthesizes two inputs supplied for this pass: (1) a recurring-appearance count of realtors across SERP sweeps tagged by market and intent (Lafayette general, buyer intent, seller intent, relocation, Youngsville, Carencro, Scott, Maurice, Broussard, Acadiana), and (2) a per-realtor "page anatomy" — site type, review counts, area-page counts, schema presence, lead-capture mechanics, and a ranking-driver guess for each.

**This is not a rank-tracking tool.** Caveats that apply to every number below:

- **SERP positions are `[inferred, location-dependent]`.** As established in `04_competitor_gap_analysis.md` and `04b`, all underlying searches were run from a neutral, non-Lafayette IP with no personalization or search history. `bestPos` values in the source data (mostly 1–2) reflect a specific run at a specific moment, not a stable rank. A Lafayette-based device with local search history will see a different order, and Google Maps/local-pack results (mobile-heavy, review- and proximity-weighted) were not part of this sweep at all.
- **"Appearances" is a recurrence count across sweep queries, not a composite rank score.** An agent who appears 13 times at position 4 and one who appears 8 times at position 1 are not directly comparable by appearance count alone — this report's CSV ranks primarily by appearance count with best-position as tiebreaker, which is a defensible ordering choice, not a ground truth ranking.
- **Portal snippets are not the same as owned content.** Several entries (Tassie Fonseca, Cassidy Stoma) rank via Realtor.com/Zillow/US News directory pages, not a site they control. Their "ranking driver" is largely the portal's domain authority plus their transaction data feeding that portal — a different mechanism than an agent with a custom site ranking on its own authority.
- **Anatomy fields marked "unknown" are left unknown in this report.** Several agents have no located Google Business Profile or unconfirmed schema markup in the source data — this is *absence of data*, not evidence of absence. Do not read "unknown" as "zero."
- **Review counts are platform-specific and not additive or comparable across agents** without noting the source platform (Google vs. Zillow vs. BirdEye vs. Facebook), consistent with the caveat already established in `04_competitor_gap_analysis.md`.

---

## (b) The Top 10

Full detail in `data/top10_realtors.csv`. Summary:

| Rank | Agent | Appearances | Markets | What they primarily rank with |
|---|---|---|---|---|
| 1 | Robbie Breaux Team | 13 | Lafayette (buyer/seller intent), Youngsville, Scott, Maurice | Largest on-site architecture in the cohort (25–35+ area/price pages) + BirdEye/Facebook reviews + lead-capture tools (mortgage calc, pre-approval, free market analysis) |
| 2 | Tassie Fonseca | 12 | Lafayette (+ seller/relocation), Youngsville, Carencro, Scott, Maurice, Acadiana | Portal-only presence (Realtor.com/Zillow/US News/Homes.com) riding high claimed transaction volume; no owned site |
| 3 | Jessica Broussard | 11 | Lafayette (+ seller), Youngsville, Broussard | Owned domain + valuation page that independently outranks Homes.com's own tool `[verified in 04b]`; sales-volume claims |
| 4 | Cassidy Stoma | 11 | Lafayette (+ seller/relocation), Youngsville, Carencro, Maurice, Acadiana | Portal-only (Zillow/Realtor.com); listing velocity + multi-community coverage; only cohort member with confirmed JSON-LD (on Zillow's page, not her own) |
| 5 | James Keaty | 11 | Lafayette (+ seller/relocation), Youngsville, Carencro, Scott, Acadiana | Personal profile riding Keaty Real Estate's brokerage authority (600+ Google reviews, 10+ area pages, video cadence) |
| 6 | Keaty Real Estate | 11 | Lafayette (+ buyer/seller/relocation), Youngsville, Scott, Acadiana | Brokerage-level: 15+ community pages, 600+ Google reviews, daily-ish YouTube video, real-time IDX |
| 7 | Sean Hettich | 10 | Lafayette (+ buyer/seller), Youngsville, Acadiana | 350+ Zillow reviews, dated year-by-year "top producer" stats, dedicated reviews page with sale-date/city tags |
| 8 | Mary & Tim McCubbin | 9 | Lafayette (+ seller/relocation), Scott, Acadiana | CENTURY 21 franchise authority, Zillow team review aggregate (95), multi-MLS reach — only 3 dedicated area pages despite serving 35 |
| 9 | Robert Hillard | 9 | Lafayette (+ seller/relocation), Carencro, Acadiana | Keller Williams brand + transaction volume (263 deals) + 6 area pages; largely portal-hosted (Homes.com) |
| 10 | Kris Bourque | 8 | Lafayette (+ buyer/seller), Carencro, Acadiana | Personal-brand differentiation + downloadable guides + valuation tool + AI chatbot; no dedicated area pages despite listing 15+ communities in copy |

---

## (c) Ranking Drivers, Ranked by Evidence Strength Across the Cohort

Each driver below is scored by how many of the 10 cohort entries exhibit it **as confirmed or claimed in the source anatomy data**, not by re-verification. Counts are conservative — ambiguous cases are called out rather than rounded up.

### 1. Custom/branded domain (not portal-only) — **7 of 10** `[inferred from site_type field]`
James Keaty, Keaty Real Estate, Robbie Breaux Team, Sean Hettich, Mary & Tim McCubbin, Kris Bourque, and Jessica Broussard all operate on a domain they control. Tassie Fonseca and Cassidy Stoma are portal-only (no owned site found). Robert Hillard sits in between — primary discoverable URL is a Homes.com profile, broker-hosted via Keller Williams.
**Carrie: partial.** She owns `carriebilleaud.com` (registered 2021, per `04`'s addendum) but it currently just redirects to her eXp subdomain — unused, not built out.

### 2. Multiple dedicated area/community landing pages (5+ confirmed) — **5 of 10** `[verified/inferred per anatomy]`
James Keaty (10+), Keaty Real Estate (15+), Robbie Breaux Team (25–35+), Jessica Broussard (6+), Robert Hillard (6). Tassie Fonseca has 4 (just under the bar). Cassidy Stoma's "11+ communities" reflects listing/service-area coverage on portals rather than confirmed dedicated pages, so not counted here. Mary & Tim McCubbin have only 3 dedicated pages despite serving 35 areas per Zillow — a case where broad service-area *claims* did not translate into built pages. Kris Bourque explicitly has "no dedicated location landing pages detected" despite naming 15+ towns in copy.
**Carrie: missing.** Zero area pages exist today; 2 of the planned 7 page briefs (`youngsville_realtor.md`, `broussard_realtor.md`) are area-specific and not yet built; nothing planned yet for Carencro, Scott, or Maurice.

### 3. High review volume (100+) on at least one platform — **4 of 10** `[verified/claimed per anatomy]`
Keaty Real Estate / James Keaty (600+ Google, shared brokerage figure — counted once for brokerage-level credit, though it inflates both individual rows in the CSV), Sean Hettich (350+ Zillow), Robbie Breaux Team (286 BirdEye). Mary & Tim McCubbin's 95 Zillow reviews are close but under the 100 line as scored here. Jessica Broussard, Cassidy Stoma, Kris Bourque, Robert Hillard, Tassie Fonseca all show single-digit-to-unknown counts on the platforms captured in this sweep.
**Carrie: has, but platform-mismatched.** Her 185 Google reviews at 5.0 already tops the *Google* counts known in this project (per `04`'s addendum — no cohort member here has a confirmed Google count above hers). But this cohort's "100+" wins are concentrated on Zillow/BirdEye/Facebook, where Carrie is thin (Zillow 29). The volume exists; it's on the platform this particular sweep under-samples.

### 4. Active lead-capture beyond a basic contact form (valuation tool, mortgage calculator, qualifying form, chatbot) — **4 of 10** `[verified/inferred]`
Robbie Breaux Team (mortgage calculator + pre-approval + free market analysis), Jessica Broussard (home valuation tool), Kris Bourque (valuation tool + mortgage calculator + AI chatbot + Calendly), Keaty Real Estate ("Get Instant Offer" CTA). The rest offer phone/email/basic contact forms only, per the anatomy notes.
**Carrie: missing.** No valuation or calculator tooling exists on the current eXp-hosted site; this is already spec'd as a to-build item in the page briefs (`sell_my_house_lafayette.md`) but not live.

### 5. IDX/MLS search integration — **7 of 10 confirmed "yes"; 3 unconfirmed (not "no")**
James Keaty, Keaty Real Estate, Robbie Breaux Team, Mary & Tim McCubbin, Robert Hillard, Jessica Broussard, and Tassie Fonseca (via Flexmls/REALTOR Association of Acadiana) all confirm IDX integration. Cassidy Stoma, Sean Hettich, and Kris Bourque are marked "unknown"/not checked, not confirmed absent. This is close to table-stakes in the cohort rather than a differentiator — worth having but unlikely to be a ranking lever on its own.
**Carrie: has** (via eXp/BoldTrail platform), though the platform's known technical problems (per `production_site_plan.md`) may undercut its value.

### 6. Schema markup (confirmed JSON-LD) — **1 of 10 confirmed present, and it's not their own site**
Only Cassidy Stoma has confirmed JSON-LD (LocalBusiness + BreadcrumbList) — and it's on her Zillow profile page, not a domain she controls. Every other cohort member is "not checked," "not detected," or explicitly confirmed absent (Sean Hettich, per `04b`'s direct HTML check — the #1-position agent in an earlier sweep has no schema at all).
**Reads as a weak/unproven driver for this cohort specifically** — its near-total absence among agents who are ranking well suggests schema is not currently a load-bearing local-SEO factor for this market, or at minimum isn't differentiating winners from each other. This tempers, but does not eliminate, the existing backlog item (`seo_backlog.csv` P2: "Add JSON-LD schema sitewide") — still worth doing for correctness/rich-result eligibility, but should not be sold internally as a likely ranking mover based on this evidence.
**Carrie: missing** (confirmed via direct grep in `02_local_seo_audit.md`, zero `application/ld+json` matches).

### 7. High claimed transaction/sales volume — **6 of 10** `[claimed, largely self-reported / platform-sourced]`
Tassie Fonseca (90+ closings/yr per US News), Cassidy Stoma (33–40 sales), Robert Hillard (263 deals/$50.8M), Jessica Broussard ($25M/yr, 82+ transactions), Mary & Tim McCubbin (5,291 lifetime/260 recent), Sean Hettich ($47–74M range across years). These are largely self-reported or portal-sourced figures, not independently audited — treat as claims, consistent with this project's existing discipline around Carrie's own unverified production numbers (`known_claims.yaml`).
**Carrie: unknown/unverified** — no comparable audited volume figure currently exists for her in this project's data; do not manufacture one to match this pattern.

---

## (d) Per-Market and Per-Intent Notes

### By intent (using the market tags in the sweep)

- **General "agent-seeking" (plain "Lafayette LA," "Acadiana"):** Portal-driven and volume-driven — 8–9 of 10 cohort members appear here, including both portal-only entries (Tassie, Cassidy). This is the most contested, most portal-owned intent tier; consistent with `04b`'s finding that broad head terms are portal territory. **Defensive note, not an opportunity:** no realistic amount of content on Carrie's own site displaces Zillow/Realtor.com/US News from the *broad* "Lafayette LA realtor" query type — the achievable win here is appearing *within* those portal profiles (review count, profile completeness), not out-ranking the portal itself.
- **Seller intent / valuation:** All 10 cohort members appear here — the single most-contested and most evenly-distributed intent in the sweep. This corroborates `04b`'s Part A finding (query #7, "how much is my house worth lafayette") that agent-branded valuation content can out-rank portals' own tools. It also means this is where competition is fiercest, not thinnest — a page here needs to be genuinely good (education + honest framing + real form), not just present.
- **Buyer intent:** Only 4 of 10 appear (Keaty Real Estate, Robbie Breaux Team, Sean Hettich, Kris Bourque) — a noticeably thinner field than seller intent. Buyer-intent queries may be more portal-saturated at the head-term level (inventory search) with less room for agent-branded pages to break in, or fewer competitors have built buyer-specific content. Either way, this is a real relative opening: the buyer-agent brief (`lafayette_buyers_agent.md`) faces less entrenched agent-vs-agent competition than the seller/valuation brief does.
- **Relocation:** 6 of 10 appear (Tassie, James Keaty, Cassidy, Keaty RE, Mary & Tim, Robert Hillard) — but this is driven by **portal profile presence** (US News agent directory pages), not dedicated relocation content. **Defensive note, not an opportunity:** this matches `04b`'s separate finding that "moving to lafayette la" as a query returns zero agent/team presence in the top 8 (Reddit, Facebook groups, moving blogs, city guides own it outright). The agents appearing under "relocation" tags here are being surfaced via their general portal profiles, not because they built relocation-specific pages — nobody in this cohort has actually cracked relocation content, and there's no evidence a local agent site could.

### By geographic market

- **Lafayette, Youngsville, Acadiana (regional):** Deep fields (7–9 of 10 cohort members each). Expected — these are the largest, most competed markets, and match the two markets Carrie's plan already prioritizes (`lafayette_realtor.md`, `youngsville_realtor.md`).
- **Carencro, Scott, Maurice: thin fields — cheap wins.** Carencro: 5 of 10 (Tassie, James Keaty, Cassidy, Robert Hillard, Kris Bourque). Scott: 5 of 10 (Tassie, James Keaty, Keaty RE, Robbie Breaux, Mary & Tim). Maurice: only 3 of 10 (Tassie, Cassidy, Robbie Breaux). None of these three markets has a *dedicated, purpose-built* area page from any cohort member matching the depth of the Lafayette/Youngsville pages — coverage is mostly incidental (portal profiles or broad service-area mentions), not a competitor investing in the market specifically. This is the clearest opportunity signal in the dataset: a well-built Carencro, Scott, or Maurice page (using the same skeleton validated in `04b` Part C #5 — market snapshot → subdivisions → amenities → schools → CTA → valuation link) would face materially less built-out competition than a Lafayette or Youngsville page would.
- **Broussard: thin field, but for a different reason.** Only Jessica Broussard appears under the "Broussard LA" tag in this sweep (1 of 10) — not because the market is uncontested in general (04b's earlier sweep showed Robbie Breaux's `/broussard/` page and eXp's own generic Broussard IDX page both appearing for "broussard la real estate"), but because this particular top-10 cohort's recurrence pattern happens to concentrate there around one agent. Treat this as thin-*in-this-cohort*, not thin-in-market — cross-check against `04b`'s Part A #5 before treating Broussard as an easy win the way Carencro/Scott/Maurice are.
- **Named micro-communities (e.g., Sugar Mill Pond):** Not present as a distinct market tag in this sweep's dataset, but carried forward from `04b` (Part A #6): a well-built, named-subdivision page can break into an otherwise portal/builder-dominated SERP. Worth keeping on the roadmap as a phase-2 idea once the core area pages exist, not as an immediate priority from this pass.

---

## (e) What This Changes in Our Plan (deltas only)

This does **not** restate the existing backlog (`backlog/seo_backlog.csv`) or page-brief set (`content/page_briefs/`). Deltas only:

1. **Add Carencro, Scott, and Maurice to the area-page roadmap, prioritized above a second Youngsville/Broussard content pass.** Currently only `youngsville_realtor.md` and `broussard_realtor.md` exist as area briefs; nothing is planned for Carencro, Scott, or Maurice despite this sweep showing them as the thinnest-competition markets in the entire dataset (3–5 of 10 vs. 7–9 of 10 for Lafayette/Youngsville/Acadiana). This is a new, higher-leverage-per-effort item than anything currently in the backlog's area-page scope.
2. **De-prioritize relocation-intent content.** Two independent sweeps now agree (this one and `04b`'s Part A #8) that no agent — including any in this top-10 — has built dedicated relocation content that ranks, and that the intent is owned by Reddit/Facebook groups/moving blogs/city guides. Do not add a relocation-specific page brief; the existing plan's silence on this is correct and should stay that way.
3. **Temper the schema-markup backlog item's expected impact, but don't drop it.** `seo_backlog.csv`'s P2 "Add JSON-LD schema sitewide" is still correct to do (Google-recommended, low-risk, enables rich results), but this pass found only 1 of 10 top-ranking competitors has *any* confirmed schema, and it's on a portal page they don't control — not their own site. Reframe internally from "likely ranking lever" to "correctness/future-proofing item," so effort isn't over-invested here relative to items with stronger cohort evidence (area pages, valuation tooling).
4. **Add a lightweight valuation/lead-qualification tool to the site-build priority list, not just the page-brief copy.** `sell_my_house_lafayette.md` already specs the honest, human-reviewed valuation-request approach (validated by `04b`). This pass adds a structural note: 4 of 10 top competitors (including 2 of the top 3 by appearance count) have *some* form of interactive lead-capture beyond a contact form (valuation estimator, mortgage calculator, qualifying dropdown, chatbot). This should be treated as a production_site_plan.md build requirement, not only a content/copy decision.
5. **Buyer-intent pages face a thinner competitive field than seller-intent pages — sequence accordingly if a choice must be made.** Only 4 of 10 cohort members appear under buyer-intent tags vs. all 10 under seller-intent tags. If site-build capacity forces a sequencing decision between `lafayette_buyers_agent.md` and `sell_my_house_lafayette.md`/`lafayette_listing_agent.md`, this data leans toward buyer-intent being the less-crowded near-term opportunity — though seller/valuation content remains necessary regardless, since it's also where Carrie's differentiation (185 Google reviews) is most likely to be seen by a comparison-shopping seller.

---

## Source Data

- `data/top10_realtors.csv` — one row per realtor: rank, agent_name, markets_seen, serp_appearances, best_position, primary_url, site_type, google_reviews, other_reviews, area_pages, schema_markup, ranking_driver_guess.
- Ranking order in the CSV: sorted by `serp_appearances` descending, tie-broken by `best_position` ascending (lower/better first), then alphabetically. This is a presentation ordering, not a validated composite rank — see caveats in (a).
