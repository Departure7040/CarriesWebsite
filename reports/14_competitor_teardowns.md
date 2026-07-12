# 14: Competitor Teardowns — The Full Field

**Date:** 2026-07-11
**Extends:** `reports/13_beat_robbie_breaux.md` (the Breaux teardown + overtake list — read that first; Breaux is only summarized here). Skim companion: `reports/11_top10_ranking_drivers.md`.
**Scope:** URL enumeration + small page samples for the 5 remaining custom-domain competitors from the report-11 cohort (Keaty, Jessica Broussard, Hettich, Bourque, McCubbin), plus the portal-only cohort (Fonseca, Stoma), consolidated into one master scoreboard against Carrie's current state.

**Tagging key:** `[verified]` = confirmed via direct `firecrawl_map`/`firecrawl_scrape` fetch in this pass (2026-07-11) or direct file check in this repo · `[claimed]` = self-reported/platform-sourced figure not independently audited · `[inferred]` = reasonable conclusion from verified evidence · `[client-confirm]` = needs Carrie's/Brook's input.

---

## (a) Method + Fairness Caveats

**Method:** `firecrawl_map` (sitemap-included, limit 300) on each of the 5 custom domains, then **one representative area-page scrape per site** (markdown, main-content-only): Keaty `/guide/scott`, JBroussard `/neighborhoods/youngsville`, Hettich `/communities/youngsville`, McCubbin `/community/.../Lafayette`, Bourque `/neighborhoods`. No forms submitted, no bulk crawls. The portal-only cohort (Fonseca, Stoma) was **not re-scraped** this pass — their rows rely on `data/top10_realtors.csv` anatomy data from the report-11 sweep `[inferred]`.

**Caveats — read before quoting any number:**

- **Page counts are `[verified]` as lower bounds only.** A site map reflects what the sitemap/internal-link graph exposes at one moment; JBroussard's map hit content-heavy territory (60+ blog URLs surfaced) and may still undercount, while Bourque's Wix map surfaced only ~21 URLs total.
- **Quality judgments are `[inferred]` from single-page samples.** One area page per site was read in full. A site could be better or worse elsewhere; where report `04b` or `13` sampled other pages of the same site, that's cited.
- **Review counts are platform-specific, non-additive, and a mix of `[verified]` (seen on the page/profile) and `[claimed]` (self-reported, e.g. "600+ Google reviews" repeated on Keaty's own materials and BBB).** Do not sum across platforms.
- **This is not rank tracking.** Nothing here says who outranks whom today — see report 11's caveats, which all still apply.
- **Carrie's cells distinguish live vs. demo.** Her production site (`site/`) is built but **not launched**; her live presence is the eXp subdomain + GBP + portals. Cells marked *(demo)* count for nothing in SERPs until launch.

---

## (b) Per-Competitor Teardowns

### Robbie Breaux Team — lafayettehomepros.com (summary; full teardown = report 13)

≈128 substantive pages: 56 area, ~20 sampled price-band (structurally 100s, zero unique copy), 11 type pages, 23 blog posts, 14 resource pages, 5 tools `[verified in 13]`. Depth sharply tiered: ~5 real flagship pages + IDX-shell tail. **No on-site reviews page** (reviews live on BirdEye/Facebook), no JSON-LD on the page checked. Overtake list stands as written in 13 — with one correction from this pass: his missing reviews page makes him the **outlier** in the field, not the norm (see (d)).

### Keaty Real Estate / James Keaty — keatyrealestate.com

| Category | Count | Notes `[verified via map, 2026-07-11]` |
|---|---|---|
| Area/community guide pages | **21** | lafayette, youngsville, broussard, scott, carencro, duson, sunset, arnaudville, abbeville, eunice, opelousas, new-iberia, breaux-bridge, river-ranch (≈14 Acadiana-relevant) + covington, mandeville, madisonville, lacombe, slidell, new-orleans + one `/guide/489-2` cruft URL |
| Resource/tool pages | **~25** | home-valuation, seller-net-sheet + seller-net-form, pre-qualification-form, investment calculator, market-reports, interest-rate, appreciation-chart, flood-map, assessors, school-zone, crime map, sheriffs-sale, buyer/seller guides, one-day-listing-agreement, DR Horton buyer bonus, credit-report, moving-to-louisiana, millennials-guide… |
| Blog | 8+ posts surfaced | Mix of local-flavor (Avery Island, Zea Lafayette, mid-year market update) and generic tips |
| Reviews page | **Yes** — `/reviews` | |
| Agent roster pages | ~70 | Brokerage scale on display |
| Price-band / type landing pages | **0 found** | Filters exist in IDX search but no landing-page grid like Breaux's |

**Depth verdict:** the `/guide/scott` sample is **genuinely written** — ~450 words of real local specificity (J.B. Scott sugar-mill history, Boudin Festival, named schools incl. St. Peter and Paul, named restaurants) plus live per-subdivision listing counts `[verified]`. One quality flaw: the "Top Neighborhoods" widget on the Scott page lists Sugar Mill Pond and River Ranch (not in Scott) — a sitewide component, not local curation `[verified]`.
**Review strategy:** the 600+ Google figure is **brokerage-level and `[claimed]`** (repeated on their materials/BBB, no individual-agent Google count confirmed); + Facebook 230 `[claimed]`.
**Their edge:** the deepest tool/resource arsenal in the field + brokerage review mass + video cadence (daily-ish YouTube per report 11 `[claimed]`).
**Their weakness:** split identity — the site serves two metros (Lafayette AND Covington/Northshore/New Orleans), diluting Acadiana focus; guide copy is good but brochure-generic (no market stats, no buyer-decision help); no reviews *numbers* on their own domain checked pages; `/guide/489-2` and `sunset-2`/`carencro-2` URL cruft.
**Do-not-copy:** the two-metro sprawl (Carrie's tight service area is an asset); ~70 agent pages of brokerage scaffolding she doesn't need; gated "free account activation" interrupt on guide pages.

### Jessica Broussard — therealjessicabroussard.com

| Category | Count | Notes `[verified via map, 2026-07-11]` |
|---|---|---|
| Neighborhood pages | **9** | lafayette, youngsville, broussard, river-ranch, sugar-mill-pond, sabal-palms, scott-west-village, west-bayou-parkway-greenbriar, audubon-plantation/parc + hub |
| New-construction "developments" pages | **2 + hub** | Signature Series Homes / Sonoma Gardens — a **builder-partnership showcase, the direct analog of Carrie's AHB play (backlog row 40)** |
| Blog posts | **60+** | Overwhelmingly hyper-local: River Ranch HOA/ARC rules, Sabal South plats & setbacks, **"Real Estate Contingencies in Louisiana Explained," "Title Insurance in Louisiana," "Closing Costs in Lafayette"** — see (d), this is the only encroachment on our guide moat in the whole field |
| Tools | Home-valuation page + platform widgets (census, Walk Score, Yelp POI, school data on every neighborhood page) | |
| Reviews page | **Yes** — `/testimonials` | |
| Other | `/videos` gallery, `/properties/sold` page, per-listing subdomain microsites | |

**Depth verdict:** voluminous but **platform-generated**. The Youngsville sample is long (2,000+ words) yet the prose is unmistakably AI/template-generic ("These activities showcase the community spirit…", numbered listicles with no specific facts a local would add); the genuinely valuable parts are the **data widgets** (census, Walk Score, Yelp, schools) her platform injects `[verified]`. Template sloppiness: the contact page metadata says "top real estate expert in **Los Angeles**" `[verified via map metadata]`.
**Review strategy:** thin everywhere — Zillow 6, FastExpert 6, BirdEye 4 `[verified in 11 data]`. She ranks on content volume + valuation page + sales claims ($25M/yr `[claimed]`), not reviews.
**Their edge:** the most complete *structural* mirror of our own plan — subdivision pages + builder partnership + valuation + testimonials + hyper-local blog — executed at volume on a polished platform.
**Their weakness:** the copy is generic at scale and reviews are near-zero; a comparison-shopping client who checks proof finds 6 Zillow reviews vs. Carrie's 185 Google.
**Do-not-copy:** AI-listicle area copy (long ≠ good; ours must contain facts hers doesn't); the LA/Louisiana metadata confusion; 60-post cadence for its own sake (content principle #1 in `06`).

### Sean Hettich — topagent337.com

| Category | Count | Notes `[verified via map, 2026-07-11]` |
|---|---|---|
| Community pages | **3 + hub** | lafayette, broussard, youngsville only |
| Blog posts | **~33** | Mostly seller-tips (staging, curb appeal, open houses); several **agent-facing** posts ("The KISS Method for Real Estate Agents," "How Agents Can Use the Holiday Season") that dilute consumer focus |
| Tools | Home-valuation lead form | |
| Reviews page | **Yes** — `/about/reviews`, plus `/about/results` (year-by-year top-producer stats) | Best-in-class review formatting per `04b` (sale-date + city + transaction-type tags) |

**Depth verdict:** the Youngsville sample is **hand-written and genuinely local** — named subdivisions including small ones no one else covers (Autumn Run "off Guillot Road," Beacon Hills Village), schools linked to lpssonline.com, real amenity specifics (116-acre sports complex, Les Vieux Chenes since 1977) `[verified]`. Small footprint, real quality — the inverse of Breaux.
**Review strategy:** concentrated on **Zillow: 353** `[verified in 11 data]`, marketed hard on-site ("350+ 5-star reviews" in the homepage title).
**Their edge:** proof stack — reviews page + results page + trust ribbon; the model `04b` already told us to reuse.
**Their weakness:** only 3 area pages (nothing for Carencro/Scott/Maurice), no buyer tools beyond a form, blog wanders off-audience.
**Do-not-copy:** agent-facing blog content on a consumer site; cookie-consent modal that buries the page (his raw scrape is 40% cookie UI).

### Kris Bourque — thekrisbourqueway.com

| Category | Count | Notes `[verified via map, 2026-07-11]` |
|---|---|---|
| Area pages | **0 real** | `/neighborhoods` exists but is `noindex` and still contains **Wix template placeholders for Tarrant County / Fort Worth / Plano, Texas** `[verified via scrape]` |
| Blog posts | ≥6 surfaced | Local and specific (Lake Martin real estate, Church Point listing, "homes for sale in Lafayette under 300k," mortgage-rate buydowns) — his blog posts function as de facto micro-area/price pages |
| Tools | `/calculator` + **Jotform AI chatbot** + Calendly booking | |
| Reviews page | **Yes** — `/testimonials` | |

**Depth verdict:** smallest real footprint in the cohort; personality-led homepage + a handful of sharp local blog posts. The Texas-placeholder neighborhoods page is the single most instructive artifact in this whole pass: a top-8 recurring SERP competitor is ranking with an **unfinished template site**, on brand + portals + a few good posts.
**Review strategy:** scattered and thin (FastExpert 2; Zillow count not visible) `[verified in 11 data]`; leans on Facebook reach (1,689 likes `[claimed]`).
**Their edge:** differentiation (voice, chatbot, Calendly friction-removal) at near-zero content cost.
**Their weakness:** no area pages, noindexed/broken key pages, no review depth anywhere.
**Do-not-copy:** shipping placeholder pages live; relying on an AI chatbot as the primary lead path — it reads as a gimmick where Carrie's differentiator is *human* responsiveness (185×5.0 says clients agree).

### Mary & Tim McCubbin — southlouisianahomesales.com

| Category | Count | Notes `[verified via map, 2026-07-11]` |
|---|---|---|
| Total mapped URLs | **12** | Smallest site in the field |
| Community pages | **3** | Houma, Lafayette, Thibodaux — their center of gravity is Bayou region, not Acadiana |
| Tools / blog / reviews page | **0 / 0 / 0** | Market Leader template + IDX only |

**Depth verdict:** the Lafayette page's entire copy is the **Google knowledge-panel description of Lafayette pasted verbatim** ("Downtown, the Alexandre Mouton House… has 1800s furnishings") above IDX stat tiles `[verified]`. Thinnest owned content in the cohort — thinner than Breaux's Scott shell.
**Review strategy:** everything lives on **Zillow: 95 team reviews, 5,291 lifetime sales** `[claimed/platform]`; the site exists to catch clicks and hand them to the Zillow profile.
**Their edge:** multi-MLS reach (Bayou/Acadiana/Baton Rouge/New Orleans boards) + CENTURY 21 brand + Zillow volume history.
**Their weakness:** zero owned content that could hold a ranking on merit; Lafayette is their satellite market, not home turf.
**Do-not-copy:** duplicated third-party copy as area content (a literal duplicate-content liability); building a site whose only job is to bounce visitors to Zillow.

### Portal-only cohort — Tassie Fonseca & Cassidy Stoma `[inferred from 11 data; not re-scraped this pass]`

No owned sites. They rank via Realtor.com/Zillow/US News/Homes.com directory pages riding **transaction-volume data** (Fonseca 90+ closings/yr per US News; Stoma 33–40 sales `[claimed]`) and multi-town service-area tags — 12 and 11 SERP appearances respectively, #2 and #4 in the whole cohort. Review counts are startlingly low (Fonseca: Zillow shows **0 reviews**; Stoma: none found) `[verified in 11 data]`. **Lesson:** the portal lane rewards *attributed transaction data and profile completeness*, not reviews or content — and it's the one lane where a competitor beats Carrie today without owning a single page.

---

## (c) Master Scoreboard

Verdicts: **strong / ok / weak / none** (+ number where known). *(demo)* = built in `site/` but not launched — worth nothing in SERPs today. Carrie-now = live eXp subdomain + GBP + portals.

| Capability | Carrie-now | Breaux | Keaty | JBroussard | Hettich | Bourque | McCubbin | Portal-cohort |
|---|---|---|---|---|---|---|---|---|
| Area-page coverage | **none live** (7 *(demo)*; live IDX area pages noindexed) | strong (56) | strong (21, ~14 Acadiana) | ok (9 + 2 dev) | weak (3) | none (placeholder pg) | weak (3, 1 Acadiana) | n/a (portal service-area tags) |
| Area-page QUALITY | strong *(demo — hand-written per-market)* | tiered: ~5 real, rest shells | ok-strong (real copy, generic tone) | weak-ok (long but AI-generic; good data widgets) | strong (small but real) | n/a | weak (pasted Google text) | n/a |
| Price/type pages | none live (3 price-band *(demo)*) | ok-count/weak-quality (~20+11, zero copy) | none | ok (2 new-constr. dev pages) | none | weak (1 blog post) | none | n/a |
| Tools/calculators | none live (mortgage calc + valuation form *(demo)*) | ok (5) | **strong (~25 incl. net sheet, invest calc)** | ok (valuation + widgets) | weak (valuation form) | ok (calc + AI chatbot + Calendly) | none | n/a |
| Guides/educational | none live (6 LA-law guides *(demo)*) | ok (23 posts, national-topic) | ok (~25 resources + blog, mixed) | strong-volume/weak-depth (60+ hyper-local posts, 3 LA-law-adjacent) | ok (~33 posts, drifts off-audience) | weak (≥6 good local posts) | none | n/a |
| On-site reviews page | none live (~50 testimonials stranded on lenders URL; testimonials.html *(demo)*) | **none** | yes | yes | **yes — best format** | yes | none | n/a |
| Google review count | **strong: 185 @ 5.0 `[verified]`** | unknown (BirdEye 286) | 600+ `[claimed, brokerage-level]` | unknown (Zillow 6) | unknown (Zillow 353) | unknown | unknown (Zillow 95 team) | Fonseca 0 shown / Stoma unknown |
| Portal profile strength | ok (Zillow 29, R.com 2, strong bios; sold-attribution unverified) | ok | ok | weak | strong (Zillow) | weak-ok | strong (Zillow) | **strong — it's their whole play** |
| Schema (JSON-LD, own domain) | none `[verified in 02]` | none found | none detected | none found | none detected | unconfirmed | none | Stoma: yes, on Zillow's page only |
| Video / content cadence | ok but off-site (paid FB reels, $3k/mo) | weak (blog dormant since ~2020 sample) | **strong (daily-ish YouTube `[claimed]`)** | ok (/videos + steady blog) | ok (steady blog) | ok (recent local posts) | none | n/a |
| Custom domain | weak (owns carriebilleaud.com, redirect only) | yes | yes | yes | yes | yes (Wix) | yes | **none** |

**Headline:** Carrie **already wins** exactly one row — Google review count — and it's the row visible where clients actually compare agents (Maps/local pack). She **loses today** on every owned-content row purely because nothing is launched: the demo work in `site/` would immediately put her at parity-or-better on area quality, guides, price pages, on-site reviews, and tools vs. everyone except Keaty's tool arsenal. **Fastest flips:** launch (converts five *(demo)* cells at once), Realtor.com sold-attribution + 15–20 reviews (flips portal row vs. a cohort sitting at ~zero), and JSON-LD (nobody has it — cheap symbolic lead, low ranking upside per report 11).

---

## (d) Cross-Competitor Patterns

**What multiple winners share (that report 11 couldn't see at anatomy depth):**

1. **An on-site reviews/testimonials page is table stakes, not a differentiator.** 4 of 5 custom-domain sites have one (Keaty `/reviews`, Hettich `/about/reviews`, JBroussard `/testimonials`, Bourque `/testimonials`) `[verified]`. Report 13 framed Breaux's missing reviews page as "we can own this format outright" — corrected: **Breaux is the outlier**. Carrie's testimonials page isn't a moat, it's catching up to the field median; the *moat* is that hers can headline 185 Google @ 5.0, a number nobody else confirms on Google.
2. **Every big site is tiered — flagship + filler — and quality varies more *within* sites than between them.** Keaty's Scott page is real where Breaux's Scott page is a shell; McCubbin's Lafayette page is pasted Google text. Raw page counts (56 vs 21 vs 9) are near-meaningless as quality signals `[verified across samples]`.
3. **Builder/new-construction partnership pages are a repeated winner pattern.** JBroussard (Signature Series developments pages), Breaux (new-construction page), Keaty (DR Horton buyer bonus) — 3 of 6 monetize a builder relationship on-site `[verified]`. This upgrades backlog row 40 (AHB page) from "good idea" to "field-validated pattern."
4. **A named-subdivision layer below town level.** Sugar Mill Pond appears as a dedicated page on 3 sites (Breaux, JBroussard, Keaty's river-ranch/results-gallery), Sabal Palms on 2 `[verified]`. Confirms report 13's phase-2 sequencing — and warns that Sugar Mill Pond specifically is now the *most contested* micro-page in Acadiana; pick a less-claimed subdivision first.
5. **Blog-as-area-page:** JBroussard and Bourque both use hyper-local posts ("homes under 300k Lafayette," "River Ranch HOA fees") as de facto landing pages for long-tail queries — cheaper than page-count expansion and consistent with our curated price-band approach.

**What NOBODY does — open lanes, stated plainly:**

1. **No one has a Louisiana-statutory guide cluster.** Zero pages anywhere in the field on FEMA flood zones/insurance, homestead exemption, USDA loans, or seller-disclosure timing `[verified across all 6 maps]`. **One honest qualification:** JBroussard has 3 LA-law-*adjacent* blog posts (contingencies, title insurance, closing costs) — the only encroachment found, scattered and generic where our guides are consolidated and specific. The flood/homestead/USDA lanes are fully open; the closing-process lane is ours but no longer untouched.
2. **No confirmed JSON-LD on any owned domain** — 0 of 6, consistent with 11's finding. Not a ranking lever here; still zero downside.
3. **Nobody surfaces Google reviews on their own site.** All review proof shown on-site is Zillow/BirdEye/testimonial quotes. An area page that embeds live Google-review proof is an unclaimed format.
4. **Nobody has a real Maurice (or Milton) page.** Breaux's Maurice coverage is adjacency, Keaty/JBroussard/Hettich have nothing `[verified via maps]`. Carrie's demo has both.
5. **Nobody except Keaty has seller-math tools** (net sheet); nobody has an honest LA-specific closing-cost calculator.

---

## (e) Strategy Deltas (adjustments to the report-13 overtake plan, full field considered)

1. **Reprioritize the testimonials page from "own the format" to "close a table-stakes gap" — and ship it with Hettich's tagging format.** 4 of 5 owned-site competitors have one (see (d)#1). Backlog row 32 stays, but its framing changes: the differentiator is *Google-sourced* proof (185 @ 5.0) + sale-date/city tags, not the page's existence.
2. **Open the portal lane as a first-class workstream — it's where 2 of the top 4 competitors live and the cheapest visible win on the board.** (i) **Fix Realtor.com sold-attribution and profile completeness** `[client-confirm]` — Fonseca and Stoma rank on attributed transaction data alone; Carrie's Realtor.com profile shows 2 reviews and unverified sold history. (ii) **Per-portal review targets vs. named counts:** Realtor.com 15–20 (the whole cohort sits at ~zero there — instant visible leadership); Zillow 50+ near-term (vs. McCubbin team 95, Hettich 353 — parity is a multi-year project, but 29→50 changes the comparison-shopping read). New backlog rows 44–45.
3. **Defend the guide moat where it's actually being probed.** JBroussard's LA-law-adjacent posts (contingencies, title insurance, closing costs) are the only threat to our clearest content edge. Extend `louisiana-closing-process.html` with title-insurance and contingencies sections rather than building new pages — consolidated depth beats her scattered posts. New backlog row 47.
4. **Don't chase Keaty's tool arsenal; take exactly one item from it.** His ~25 resource pages are brokerage-scale. The one field-unique, static-compatible piece worth having is a **seller net sheet estimator** (client-side JS, pairs with sell-my-house.html) — new backlog row 46. The mortgage calculator (row 42) already covers the buyer side.
5. **Close the video-cadence row with assets already paid for.** Keaty (daily-ish YouTube) and JBroussard (/videos) are the only cadence winners; Carrie already funds reel production ($3k/mo, report 10) that lives solely on Facebook. Republish existing reels to YouTube + embed on matching area pages at near-zero marginal cost — new backlog row 48.
6. **Sequencing of area pages is unchanged but the bar per market is now precise:** Scott must beat Keaty's real ~450-word guide (not just Breaux's shell — report 13's "the bar in Scott is low" was true of Breaux only `[verified, correction]`); Carencro must beat Keaty's carencro-2 guide; **Maurice/Milton have no competitor page at all**. Youngsville is the hardest: three genuinely decent competitor pages (Hettich, JBroussard, Keaty) — ours needs data + video + Google-review proof, not just prose.
7. **Subdivision phase-2 pick should avoid Sugar Mill Pond first** (3 competitors already there); prefer an AHB-aligned or Youngsville-growth subdivision with zero dedicated pages `[client-confirm which subdivisions AHB actually builds in]`.

---

## (f) Backlog Additions

Re-read `backlog/seo_backlog.csv` immediately before appending (43 rows checked; rows 40–43 already cover AHB page, price-band pages, mortgage calculator, and nav home-value CTA — **not** duplicated). Five new rows appended (44–48): Realtor.com sold-attribution fix, per-portal review targets, seller net sheet estimator, closing-process guide extension, and FB-reel→YouTube repurposing. Testimonials-page reframing (delta #1) edits the *rationale* of existing row 32, not a new row.
