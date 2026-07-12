# 18: Production & Throughput — Who Actually Sells the Most Houses (Portal-Displayed)

> **[CORRECTED BY REPORT 19, 2026-07-11]** An independent audit (reports/19)
> found a source-interpretation error in this report: Zillow's "188" for
> Carrie is her **career/total** sales, NOT trailing-12-month. Her actual
> trailing-12-month figures are ~22 (Zillow) and ~34 / $9.48M (Homes.com) —
> consistent with each other, not the "188 / 46 / 1" spread this report
> headlined. The Realtor.com "1" remains the attribution-broken outlier.
> **The load-bearing conclusion is unchanged and reinforced:** portal
> production numbers are attribution-limited and mix time windows; nothing
> is marketing-safe without Carrie's own authorized ROAM/MLS export. See
> reports/19 for the corrected numbers and the exact ROAM export spec.

**Date:** 2026-07-11
**Supersedes:** `reports/15_top_producers_vs_seo.md`, which lost its data-collection scout mid-run and shipped with an incomplete/inconsistent production dataset. This report keeps report 15's framing (two leaderboards — SEO visibility vs. production — and where they overlap) but replaces its data with a fresh, single-pass collection across 16 agents/teams and 6 portals (Zillow, Homes.com, Realtor.com, FastExpert, HomeLight, RateMyAgent), collected 2026-07-11.
**Reads with:** `reports/11_top10_ranking_drivers.md` (SEO top 10), `reports/17_current_serp_competitor_audit.md` (current SERP capture), `data/known_claims.yaml` (Carrie's own unverified claims registry).

**Tagging key:** every production number in this report is `[portal-shown]` — displayed by a third-party website, never independently audited by this project. `[client-confirm]` = needs Carrie's input. `[inferred]` = our read of a pattern. **No number in this report should ever be read or repeated as `[true]` or `[verified production]`.**

---

## (a) Methodology and Hard Caveats — Read This Before the Table

**MLS production is not public data.** No portal, ranking site, or this report has access to audited closed-transaction records. What follows is what six consumer-facing websites *chose to display* on each agent's profile page on one day (2026-07-11), scraped by parallel research agents. That is a fundamentally different thing from production, and the gap is large and uneven:

1. **Portal counts are attribution-limited, and they under-count *unevenly*.** Each portal only shows deals it can match to an agent's MLS/IDX feed — which depends on brokerage data-sharing agreements, feed hygiene, and how the agent's name is tagged on each transaction. This is not random noise; some agents' feeds are clean on one portal and broken on another.

2. **Carrie's own data is the canonical proof of this.** On 2026-07-11, her three major portals show **three different orders of magnitude for the same 12-month window**: Zillow displays 188 sales, Homes.com's family/volume figures imply roughly 46 in the same period, and Realtor.com displays **1** closing in the last 24 months. Same agent, same year, same MLS activity underneath — three portals, three wildly different pictures. If this happens to the agent we can compare against her own internal claims, it is happening to every agent in this dataset and we have no way to know by how much.

3. **These are self-reported/portal-attributed numbers, never audited.** Several figures in the raw dataset are internally implausible on their face (Sean Hettich's Homes.com profile shows 584 "last 12 months" transactions against a $168.9M volume and only 31 sales on Realtor.com; Brice Trahan's Homes.com profile shows 3 sales in the last year against Zillow's "67+ homes sold in 1 year" and FastExpert's $140M). We report these as-shown and flag the contradiction rather than picking a winner or smoothing them out.

4. **Team vs. individual attribution is frequently ambiguous or actively misleading.** Several of the largest headline numbers in this dataset (Robbie Breaux, Keaty Real Estate, Mary & Tim McCubbin, Nah Senpeng & Charles ILonya, Destinee Allanson/Allanson Real Estate) are team- or brokerage-aggregated on at least one portal, sometimes presented with no disclosure that it's a team number. An "individual" agent profile can also be inflated by team credit flowing through a shared brokerage feed (this is a plausible, not proven, explanation for some of the larger single-agent figures below).

5. **The only authoritative production source is Louisiana parish Clerk of Court conveyance records** — real property transfer filings, which are public. But they are indexed by **buyer/seller name, not by real estate agent**, so there is no query that returns "all of Agent X's 2025 closings." Verifying any single agent's true production against these records means manually pulling and cross-referencing individual deed filings — a per-deal, per-agent manual effort, not a sweep. **We have not done this for anyone in this report, including Carrie.** It is named here as the escalation path if audited numbers are ever required (e.g., for a "top producer" marketing claim), not as something this pass accomplished.

Given all of the above, **section (b)'s sort order is a presentation convenience, not a ranking of truth.** Treat every row as "this is what the internet currently shows," full stop.

---

## (b) The Production Table (portal-displayed, not verified)

Sorted by each agent's best-available "sales, last 12 months" figure — chosen per-agent as the most-corroborated or most-explicitly-labeled 12-month figure where portals conflict (basis noted per row). Agents with no reliable 12-month figure across any portal are listed at the bottom. **This ordering is portal-displayed, not verified — read the Notes column before drawing any conclusion from position.**

| # | Agent | Team/Individual | Sales, last 12mo `[portal-shown]` | Total / Volume `[portal-shown]` | Primary source | Notes |
|---|---|---|---|---|---|---|
| 1 | **Keaty Real Estate** (brokerage, 37 agents) | **TEAM/BROKERAGE** | 2,453 (undated) | 2,453 total | [Zillow](https://www.zillow.com/profile/Keaty%20RE) | Brokerage-wide aggregate across 37 agents, not a single producer. Individual member Charles Ditch shows only 8 sales/12mo on Homes.com — the brokerage total is not distributable to any one agent from this data. |
| 2 | **Mary & Tim McCubbin** | **TEAM** | 254 | $47.6M (Homes.com, 443 total) | [Zillow](https://www.zillow.com/profile/c21actionla) | Century 21 Action Realty broker/owner team profile. Individual Tim McCubbin shows 20/12mo on both Realtor.com and RateMyAgent (rare cross-portal agreement) — the 254 figure is the team's, not his alone. |
| 3 | **Carrie Billeaud** | Individual | 188 | not shown (Zillow) | [Zillow](https://www.zillow.com/profile/carriebilleaud) | **Contradicts her own Homes.com (~46/12mo, see §e) and Realtor.com (~1/24mo) by an order of magnitude each.** See §(e) and caveat #2 above. |
| 4 | **Robert Hillard** | Individual | 70 | $50.8M (Homes.com, 263 total) | [Zillow](https://www.zillow.com/profile/Robert%20Hillard) / [Homes.com](https://www.homes.com/real-estate-agents/robert-hillard/sgtsen7/) | Zillow and Homes.com agree exactly at 70 — one of the only cross-portal-consistent figures in the dataset. Realtor.com shows "profile isn't ready to view." |
| 5 | **Destinee Allanson** (Allanson Real Estate) | **TEAM** | 66 | $11.5M (Homes.com, 66 total) | [Homes.com](https://www.homes.com/real-estate-agents/destinee-allanson/1hde875/) | Business operates as "The Allanson Team \| TK Group \| eXp." FastExpert shows a related profile ("Ashley," presumably Ashley Allanson) at 84 sales/$7M, timeframe unclear. |
| 6 | **Nah Senpeng & Charles ILonya** ("Dream Team of Acadiana") | **TEAM** | 45–51 | $57M (Homes.com, 286 total) | [Zillow](https://www.zillow.com/profile/Nah%20and%20Charles) | Zillow explicitly labels team sales (45); Realtor.com shows 51 with unconfirmed timeframe. Homes.com's 286/$57M figure is likely a multi-year total mislabeled as 12-month — treat with skepticism. |
| 7 | **Matthew Delcambre** (Keaty) | Individual | 50 | $41.1M (Homes.com, 170 total, 3 yrs) | [FastExpert](https://www.fastexpert.com/top-real-estate-agents/lafayette-la/) | Ranked #1 Lafayette on FastExpert; Homes.com's 170-total/3-years works out to ~57/yr, roughly consistent with the FastExpert 50. Facebook/brokerage awards independently corroborate him as Keaty's top individual producer — one of the stronger multi-source signals in this dataset despite zero SEO-top-10 presence (see §d). |
| 8 | **Cassidy Stoma** | Ambiguous, low confidence | 40 | not shown | [HomeLight via US News](https://realestate.usnews.com/agents/louisiana/lafayette) | Medium confidence: accessible Zillow/Realtor.com profiles show a Crowley, LA-based agent with Core Realty and no disclosed sales count; the 40-sales figure comes from a separate US News/HomeLight listing showing Schwebach Realty in Lafayette. May be the same agent post-brokerage-change or two different agents — not resolved. |
| 9 | **Robbie Breaux Team** | **TEAM** | 33 | $102.6M (Homes.com, 273 total) | [Homes.com](https://www.homes.com/real-estate-agents/robbie-breaux/w9dg34k/) | Zillow shows "Robbie Breaux & Team" collectively; individual members (Gerren Benoit, Amber Parker, Diana Richard, etc.) have separate profiles not captured here. Zillow's 1,453 "total sales shown" is likely a career/brand-level figure, not comparable to the 12-month numbers. |
| 10 | **Drake Abshire** (SoLux Group) | Individual (within team brand) | 29 | $7.1M (calc., Homes.com, 131 total lifetime) | [Homes.com](https://www.homes.com/real-estate-agents/drake-abshire/lxttz8d/) | SoLux Group's own website separately claims ~$80M/500 transactions — that figure is team-aggregated and not attributable to Abshire individually; do not conflate with the 29 shown here. FastExpert's 125 (timeframe unclear) is likely a longer window. |
| 11 | **Jessica Broussard** | Individual | 25 | $47.3M career (Homes.com, 109 closed) | [Zillow](https://www.zillow.com/profile/RealJessicaBroussard) | FastExpert shows 82 sales/$25M with an unclear timeframe; Realtor.com shows 15/12mo. All portals agree she is a genuine solo producer at moderate-to-strong scale; the exact 12-month number is simply not consistent across sources. |
| 12 | **Tassie Fonseca** | Ambiguous, portal-only | 24 | $255.7M career (Homes.com, 909 total) | [Zillow](https://www.zillow.com/profile/tim8351) | **A 4x discrepancy on her own 12-month figure**: Zillow shows 24, US News/report 11 shows ~90 closings/yr for the same period. No owned website found anywhere — her entire visibility and production signal run through portals. Treat the true 12-month number as unresolved between 24 and 90. |
| 13 | **Will Taylor** (The Gleason Group) | Individual (within team) | 20 | $36.6M/5yr (Homes.com, 144 total) | [Zillow](https://www.zillow.com/profile/Willtaylor07) | David Gleason's own separate Zillow profile shows only 6 total sales / 0 in the last 12 months — the Gleason Group's production is concentrated in Taylor, not evenly distributed across the named principals. |
| 14 | **Kris Bourque** | Individual | 14 | $4.3M/5yr (Homes.com, 22 total) | [Homes.com](https://www.homes.com/real-estate-agents/kris-bourque/kfv3bwc/) | FastExpert shows $1.5M in volume for "last year" (no unit count) — roughly consistent order of magnitude with 14 sales at Homes.com's ~$195K average price. The smallest confirmed producer in this dataset who also holds SEO-top-10 position #10 (report 11) — the report 11/15 cautionary case still holds. |
| 15 | **Sean Hettich** | Ambiguous | **not reliably shown** | $168.9M (Homes.com, 584 — see note) | [Homes.com](https://www.homes.com/real-estate-agents/sean-hettich/h4e90w0/) | Homes.com's 584-transactions/$168.9M "last 12 months" figure is implausible on its face for a solo-labeled profile and is not corroborated anywhere else — Realtor.com shows only 31 (timeframe unclear) and Zillow's 300+ reviews mention couldn't be paired with a sales count. Likely a portal data error, a longer-window mislabel, or team/brand bleed. |
| 16 | **Brice Trahan** | Ambiguous | **not reliably shown** | $17.8M/5yr (Homes.com, 69 total) | [Homes.com](https://www.homes.com/real-estate-agents/brice-trahan/l6l7jkg/) | The widest internal contradiction in the dataset: Homes.com shows 3 sales in the last year; Zillow says "67+ homes sold in 1 year" and "$50 million+" lifetime; FastExpert claims "$140M Total Sales Last Year" (almost certainly team/brokerage volume, not individual). Do not cite any single number from this row without flagging all three. |

---

## (c) Team vs. Individual — Summary

**Explicitly team-aggregated on at least one major portal:** Keaty Real Estate (37-agent brokerage), Robbie Breaux Team, Mary & Tim McCubbin, Nah Senpeng & Charles ILonya ("Dream Team of Acadiana"), Destinee Allanson/Allanson Real Estate. Their table rows above are **team totals, not individual production** — the individual-level numbers where visible (Charles Ditch 8/12mo, Tim McCubbin 20/12mo) are 10-30x smaller than the team figure shown on the same or a sibling portal.

**Individual but operating inside a team/brand structure, where the individual number may still carry some team-routed lead credit:** Matthew Delcambre (Keaty), Drake Abshire (SoLux Group — whose own site separately claims team-level $80M/500 transactions), Will Taylor (The Gleason Group).

**Solo practitioners with individually-attributed numbers on every portal checked:** Jessica Broussard, Robert Hillard, Kris Bourque, Carrie Billeaud.

**Unresolved / can't classify from available data:** Tassie Fonseca, Cassidy Stoma, Sean Hettich, Brice Trahan — either because the portal data is internally contradictory or because a possible brokerage-change/duplicate-listing question wasn't resolved this pass.

**The inflation risk this flag exists to catch:** any time a large individual-labeled number sits next to a team/brand name in the profile copy (SoLux Group, Dream Team of Acadiana, The Gleason Group, Elite Home Team), treat the number as team-influenced until proven otherwise. This is exactly the ambiguity report 15 flagged for Robbie Breaux and Keaty and it recurs here for at least four more names.

---

## (d) Overlap With SEO Visibility (reports 11 and 17)

Report 11's SEO top 10 (by SERP recurrence) cross-referenced against this table:

| Agent | SEO top 10 (report 11)? | Production signal (this report) | Read |
|---|---|---|---|
| Robbie Breaux Team | #1 | Team, 33/12mo, $102.6M | Both — largest on-site architecture in the cohort backs a real team production number |
| Tassie Fonseca | #2 | Portal-only, 24-90/12mo (unresolved) | Both, but the production number itself is internally contested |
| Jessica Broussard | #3 | Individual, 25/12mo, $47.3M career | Both, moderate scale, most internally consistent of the SEO top 3 |
| Cassidy Stoma | #4 | Low-confidence, 40/12mo | SEO-heavy, production-light/uncertain — the report 15 cautionary case still holds |
| James Keaty / Keaty RE | #5-6 | Team/brokerage, 2,453 (undated) | Both, but the *brand* ranks — individual top producer (Delcambre) does not rank |
| Sean Hettich | #7 | Not reliably shown (internal contradiction) | Nominally "both," but the production number underneath is not trustworthy this pass |
| Mary & Tim McCubbin | #8 | Team, 254/12mo | Both — team number, individual (Tim, 20/12mo) is far smaller |
| Robert Hillard | #9 | Individual, 70/12mo (rare cross-portal agreement) | Both, and one of the most internally consistent production signals in the dataset |
| Kris Bourque | #10 | Individual, 14/12mo — smallest in this dataset | SEO-visible, production-light — clearest cautionary case, unchanged from report 15 |
| **Matthew Delcambre** | Absent | Individual, 50/12mo, $41.1M, corroborated by brokerage awards | **Production without SEO** — still the strongest "invisible producer" story in the data |
| **Destinee Allanson** | Absent | Team, 66/12mo, $11.5M | **Production without SEO** |
| **Nah Senpeng & Charles ILonya** | Absent | Team, 45-51/12mo | **Production without SEO** |
| **Will Taylor / Gleason Group** | Absent | Individual, 20/12mo, $36.6M/5yr | **Production without SEO** |
| **Drake Abshire / SoLux Group** | Not in report 11's top 10, but **#1 on Google for "luxury realtor Lafayette LA" per report 17** | Individual, 29/12mo | The one name where SEO strength (report 17, not report 11) and a real production number now coincide — worth flagging as the sharpest current competitor, consistent with report 17 §5 |

This confirms report 15's core finding rather than overturning it: **producers and rankers are only partially the same people.** Delcambre, Allanson, and the Nah Senpeng team all show real portal-displayed production with zero presence in the SEO top 10 — they are winning on sphere/referral/team-ops, not search. Bourque and (per this pass) Stoma remain the clearest evidence that a SERP position converts nothing by itself. The one update from report 15: SoLux/Drake Abshire has emerged (per report 17, run after report 11) as a competitor with *both* a real production number and the current strongest owned-site SEO execution in the market — the closest thing to a "both, and doing it well" case in this dataset.

---

## (e) Where Carrie Sits

**Portal-shown production:** Homes.com displays **46 families served / $10.5M in the last 12 months**, a **#45-of-~1,900** Lafayette-area-Realtor ranking `[portal-shown, Homes.com]`, and a longer-window total of 174 closed sales / $44.6M career volume `[portal-shown, Homes.com]`. That places her, on Homes.com's own numbers, comfortably above the SEO-top-10 floor (Kris Bourque's 14/12mo) and in the same rough band as several "both lists" agents in §(d) — she is not a beginner; she is a mid-tier producer by this portal's account.

**But her own portals contradict each other badly.** Realtor.com shows roughly **1 closing** in the last 24 months `[portal-shown]` — the most severe under-attribution in this entire 16-agent dataset, worse than Sean Hettich's or Brice Trahan's internal contradictions. Zillow, in the opposite direction, shows **188 sales in the last 12 months** `[portal-shown]` — a figure that, if taken at face value, would make her the single largest individual producer in this dataset, ahead of every other agent's individual (non-team) number by 2-4x. Neither the 1 nor the 188 is credible on its own; the Homes.com 46/$10.5M figure sits between them and is at least internally plausible against her other portal data (174 total ÷ ~4 years ≈ 43/yr). **The 188 figure should not be repeated anywhere — including internally — until someone checks whether her individual Zillow profile is pulling in numbers from the "Elite Home Team" page she's also associated with** (see caveat #4 — this is exactly the team-bleed risk flagged for other agents in this report, and it may be happening to Carrie herself).

**The cheapest credibility gain available:** none of this requires new production — it requires portal attribution hygiene. Report 17 and `implementation/portal_claim_sync_checklist.md` already spec claiming and syncing her Realtor.com, Homes.com, and RateMyAgent profiles; backlog row 44 (`seo_backlog.csv`) already prioritizes the Realtor.com fix as P1. This report adds one finding to that effort: **the Zillow 188 number needs the same scrutiny as the Realtor.com 1** — both are display bugs, just in opposite directions, and both should be resolved in the same claim-and-sync pass rather than treating Realtor.com as the only broken portal.

---

## (f) Honest Conclusion

**What this report can tell you:** what six websites currently display about sixteen Lafayette-area agents and teams, on one day, with contradictions flagged rather than smoothed over. It can tell you that portal attribution is unreliable in both directions (under-counting, as on Carrie's Realtor.com, and apparently over-counting, as on her Zillow), that team/brand numbers get presented next to individual names without disclosure often enough that it should be a standing suspicion, and that — consistent with report 15 — several of the market's most credible producers (Delcambre, Allanson, the Nah Senpeng team) are functionally invisible to the SEO strategy this project is built around.

**What this report cannot tell you:** Carrie's actual production. Not a number in section (b), (c), (d), or (e) is audited. The only source that could produce an audited number — Louisiana parish Clerk of Court conveyance records — is name-indexed by buyer/seller, not by agent, meaning even that path is a manual per-deal lookup, not a report we can generate. We have not walked that path for anyone in this dataset, including Carrie.

**The real input this project still needs is the one from the July 24 kickoff ask: Carrie's own closed-transaction list by city, from her MLS export.** Everything in this report is a stand-in for that — useful for competitive context and for finding her own portal bugs, but not a substitute for it. Until that export exists, every production number attached to Carrie's name in this project, including the ones in this report, stays `[portal-shown]`, never `[true]`.

---

## Source Notes

Sixteen parallel data-collection passes across Zillow, Homes.com, Realtor.com, FastExpert, HomeLight, and RateMyAgent, run 2026-07-11. Raw per-agent JSON retained in this session's working notes (not committed as a data file this pass — flag for a future `data/production_portal_scan_2026-07-11.json` if this dataset needs to be machine-readable later). Cross-referenced against `reports/11_top10_ranking_drivers.md`, `reports/15_top_producers_vs_seo.md`, `reports/17_current_serp_competitor_audit.md`, and `data/known_claims.yaml`.
