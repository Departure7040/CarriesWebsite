# QA Notes — Adversarial Review
**Reviewer:** qa_fact_checker · **Date:** 2026-07-08
**Scope:** Reports 01–06, `content/review_request_templates.md`, `content/google_business_profile_posts.md`, `content/social_repurposing_ideas.md`, and page briefs `lafayette_realtor.md`, `sell_my_house_lafayette.md`, `youngsville_realtor.md`, `first_time_homebuyers_lafayette.md`.
**Cross-checked against:** `data/known_claims.yaml`, `data/source_log.csv`, `data/public_assets.yaml`, `data/nap_consistency_matrix.csv`.

---

## 01_public_presence_inventory.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Line 62, "Years in Business: **11 years** `[verified]`" | `known_claims.yaml` lists `years_experience` as `status: unverified`. Role file explicitly requires "11 years" to read "verify with Carrie" unless independently confirmed. Tagging it `[verified]` will let this figure leak into marketing copy as fact. | **Blocking** | Retag `[client-confirm]`. |
| Line 96, "License: **0995689513** `[verified]`" | `known_claims.yaml` `license` status is `unverified`; the report itself later documents a conflicting variant (`09956895` on Homes.com, line 282-284) but the individual entry still asserts `[verified]`. | Should-fix | Retag `[inferred]` or `[client-confirm]` pending the variant conflict resolution; don't assert `[verified]` on a fact with a known internal conflict. |
| Lines 111-126 (Homes.com) & 162-175 (LoopNet), section "Assessment: `[verified]`" applied to entries containing 46 families, $10.5M, #45/1900, ICON Agent | These are exactly the metrics the role file says must read "verify with Carrie" (174 sales/$44.6M analog: same category of unverified production stat). The `[verified]` tag sits at the *assessment* level and could be read as validating the underlying numbers, not just confirming the page was fetched. | **Blocking** | Add explicit inline `[client-confirm]` tags on each specific stat (46 families, $10.5M, #45/1900, ICON Agent), not just a general "requires clarification" caveat in prose. |
| Report-wide use of `[verified]` | No tagging key is defined at the top of the report (unlike 02 and 03, which state "`[verified]` = confirmed via direct fetch of a live source" up front). As written, `[verified]` is ambiguous between "we successfully scraped this page" and "this fact is true." Data Quality Notes (line 432) confirms the report means the former ("accessible sources; direct fetch") but a reader skimming individual entries won't know that. | **Blocking** (systemic) | Add the same tagging-key preamble used in 02/03 at the top of the report, and audit every `[verified]` tag against it — several (11 years, license, production stats) should downgrade once the "fetched ≠ true" distinction is explicit. |
| Line 10, Executive Summary: "strong bio quality and reviews on Zillow (29 reviews, 5.0★)" | Stated as bare fact with no inline tag (tag appears later in the body but not here). | Nit | Add `[verified]` inline or note "see Per-Source Findings" for tag provenance. |
| Nowhere does 01 recommend "standardize using Zillow/Realtor.com as reference" | Checked specifically for this per task brief — **not found**. Report correctly defers all canonical NAP decisions to `[client-confirm]`. | N/A — confirmed clean | No action needed. |

---

## 02_local_seo_audit.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Section (d), "Target: **2–4 new reviews per month, sustained indefinitely**... 24–48/year" | Internally sound and well-hedged, but conflicts with 04's much faster review-acquisition target (20–30 in 90 days ≈ 7–10/month). See cross-report note below. | Should-fix (cross-report) | Reconcile pacing with 04; 02's sustained-pace rationale (avoiding a "burst" pattern) should be the standard both reports use. |
| Line 55, "Priority tier... `[verified — confirmed in phase-1 findings]`" | Tag format is nonstandard (adds a parenthetical to the tag) but meaning is clear and traceable. | Nit | Optional: normalize to the four standard tags for consistency. |
| Overall | Tagging key defined up front, applied correctly throughout; production stats (174/$44.6M etc.) explicitly gated `[client-confirm]` in Section (a)(6); no incentivized/gated review language; ethics section clean. | — | No blocking issues found. |

---

## 03_website_technical_audit.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Line 123, NAP table: "Office number \| 337-522-7554" | This is the same number flagged elsewhere in 01/02/05 as the **known LoopNet phone conflict** — presenting it neutrally as "Office number" here, without a cross-reference flag, could read as if it's a separate, legitimate second line rather than the disputed number. | Should-fix | Add a note/tag cross-referencing the LoopNet conflict so a reader of this report alone doesn't miss it. |
| Overall | Rigorous, well-tagged, technically precise; realistic about what's agent-editable vs. platform-limited (explicitly flags items requiring a BoldTrail/eXp support ticket rather than assuming Carrie has that access). | — | No blocking issues found. |

---

## 04_competitor_gap_analysis.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Line 185, Summary: "Carrie... **ranks #8–10 in most organic queries**" | Stated as flat fact in the Summary despite the report's own "SERP Approximation Caveat" (lines 14–17) acknowledging results are approximate/personalized/unverified, and despite `source_log.csv` marking this a **low-confidence** inference ("Carrie visible in directory but ranks #8-10 in organic... low review count implied"). No tag anywhere in this report at all — 04 never adopts the `[verified]`/`[inferred]`/`[client-confirm]`/`[best-practice]` scheme used by 02/03/05/06. | **Blocking** | Retag as `[inferred, low confidence]` and repeat the SERP caveat inline; adopt the standard tagging scheme report-wide. |
| Line 103, "Dedicated domain + area pages **improve organic rank by 2–3 positions**" | Fabricated precision — no methodology, before/after data, or source supports a specific 2–3 position figure. Stated flatly under a "Why:" heading as if established fact. | **Blocking** | Rewrite without invented precision, e.g., "competitors with dedicated domains + area pages consistently outrank Carrie for these queries; expect improvement, not a specific position count." |
| Lines 192–195, "Realistic Timeline to 'Top 3'" (3/6/12-month rank projections: "#5–7," "#3–5," "sustain top 3") | This reads as an implicit **guaranteed-ranking promise** — specific SERP position outcomes tied to specific months. Directly contradicts `07_30_60_90_day_plan.md` ("**No ranking positions are guaranteed, by us or anyone**") and `05_ai_search_visibility_plan.md` Section 6 ("no one... can guarantee inclusion in any specific AI Overview... or a specific timeline"). Violates role-file ethics check #6 (guaranteed-ranking language). | **Blocking** | Delete or heavily rewrite as a directional, hedged illustration ("if X happens, position could plausibly improve — not a guarantee"), matching 07's and 05's disclaimer language. |
| Line 93, "Target: **20–30 new reviews in 90 days** to reach ~50+" | Contradicts 02's explicit, reasoned guidance that review "bursts" look unnatural to spam detection and recommends 2–4/month sustained (≈6–12 in 90 days). 04's pace is roughly double-to-triple that. Also inconsistent with 07's "~5–10 new Google reviews" by day 60. | Should-fix | Align pacing across 02/04/07 — adopt 02's sustained-pace rationale everywhere. |
| Gap Matrix, "Review Count \| `[TBD — low visibility in SERPs]` \| **CRITICAL** \| **1**" | Report 04 treats Carrie's review count as unknown/TBD despite 01 and 02 already documenting it precisely (29 Zillow, 2 Realtor.com, 0 Homes.com, 0 Google). Suggests 04 wasn't cross-referenced against 01/02 before publishing. | Should-fix | Pull the actual numbers from 01/02 instead of marking `[TBD]`. |
| Competitor table, column header "**Zillow Reviews**" | Column mixes platforms: Nah Senpeng's 97 is a **FastExpert** count (per `source_log.csv` row 11/14), Stephen Hundley's 79 is an **Experience.com** count (row 10) — neither is a Zillow review count. Labeling the column "Zillow Reviews" misrepresents the comparison against Carrie's actual 29 Zillow reviews. | Should-fix | Relabel column "Review Count (platform varies)" and note the source platform per row. |
| Row: Jessica Broussard "$105M+ sales, Top 1% claim" | Presented in the competitor table without flagging that this is the competitor's own unverified marketing copy (from her personal site), not independently confirmed. Lower stakes than Carrie's own unverified claims, but still worth a caveat since it's used to benchmark strategy decisions. | Nit | Add "(self-reported, unverified)" note. |
| Ethical Guardrails section (lines 142-145) | Section lists "Do NOT: buy fake reviews... misrepresent credentials" but never addresses guaranteed-ranking language — the exact violation present later in the same report (lines 192-195). | Should-fix | Add "Do not promise specific ranking positions or timelines" to the guardrail list, and make the report's own projections comply. |

---

## 05_ai_search_visibility_plan.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Section 6, "Realistic expectations" | Strong, explicit ethics safeguard — "no one... can guarantee inclusion in any specific AI Overview, ChatGPT answer, or Knowledge Panel... anyone promising a specific citation or ranking on a specific timeline is not being straight with her." This is the standard the rest of the report set (esp. 04) should match. | — (praise, not a flag) | Hold this report up as the model; align 04 to it. |
| Line 58, RAA membership `[inferred, low confidence]` | Correctly matches `known_claims.yaml` (`raa_member: status unverified`). | — | No issue. |
| Overall | No unverified production stat stated as fact anywhere; consistently gates 174/$44.6M/11 yrs/ICON multiplier behind `[client-confirm]`; realistic about platform-limited (BoldTrail) vs. agent-editable fixes. | — | No blocking issues found. |

---

## 06_content_strategy.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Line 13, "Only Zillow's 29 reviews/5.0..., the team of 4 (**including her father**)... are treated as verified" | The "father" detail is not from the Zillow team profile (which lists only 4 names with no relationships) — it originates from the **Realtor.com** bio note ("team with father," `data/public_assets.yaml` line 106). Source attribution issue carries into the page briefs (see below). | Should-fix | Correct sourcing to Realtor.com bio note. |
| Overall | Clear content principles explicitly banning unverified metrics as fact (Principle 3); no doorway-page pattern (Principle 4, and area pages are deliberately differentiated); GA4/GBP tracking sections are well-hedged with `[client-confirm]`/`[best-practice]`. | — | No blocking issues found. |

---

## content/review_request_templates.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Overall | No incentive language, no review-gating (every template routes to the same public link regardless of anticipated sentiment), canonical phone/email correctly left as `[client-confirm]` placeholders, response templates handle negative reviews ethically (no pressure to delete, no public argument). | — | No issues found. |

## content/google_business_profile_posts.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Overall | All stats placeholder-gated `[client-confirm]`; "Just Listed"/"Just Sold" posts correctly require seller/client permission before publishing; no keyword-stuffed copy, no fabricated numbers. | — | No issues found. |

## content/social_repurposing_ideas.md

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| Line 38, "team of 4 including her father" | Same sourcing issue as 06 (see above) — repeats the imprecise attribution. | Should-fix | Fix at the source (public_assets.yaml citation) and it will propagate correctly. |
| Line 56, "2–3x/week Reels cadence recommended in `04_competitor_gap_analysis.md`" | Faithful citation of 04, but inherits 04's lack of a hedge on that cadence being a competitor-observed pattern vs. a guaranteed outcome driver. | Nit | No independent fix needed here; resolve at 04. |

---

## Page briefs (spot-checked: lafayette_realtor, sell_my_house_lafayette, youngsville_realtor, first_time_homebuyers_lafayette)

| Claim/line | Issue | Severity | Suggested fix |
|---|---|---|---|
| `lafayette_realtor.md` lines 29, 62; `lafayette_buyers_agent.md` lines 38, 55; `lafayette_listing_agent.md` lines 34, 55 | "Team of 4 including her father `[verified — Zillow team profile]`" — the Zillow team profile only lists 4 names (Carrie, Jake, Blake, Arrow) with no stated relationships; the "father" detail is sourced from the **Realtor.com** bio note. Citation attributes the claim to the wrong source across at least 3 briefs. | Should-fix | Correct citation to "[verified — Realtor.com bio]" (or "Realtor.com + Zillow team roster" if combining both facts). |
| `lafayette_realtor.md` line 67, "Do NOT use: 174 closed sales/$44.6M, 46 families helped/$10.5M, '#45 of 1900 realtors'" | Correctly excludes all suspect metrics — this is the standard every brief should follow. | — (praise) | None. |
| `sell_my_house_lafayette.md`, `youngsville_realtor.md`, `first_time_homebuyers_lafayette.md` | Consistently `[client-confirm]` any local-knowledge claim (school zoning, subdivision names, commute times, program eligibility) rather than fabricating it; explicitly warns against publishing stale IDX-scraped market stats as static copy; refuses to imply an automated valuation tool exists if BoldTrail doesn't support one. | — | No blocking issues found. |
| Realism check | All 4 briefs correctly flag JSON-LD schema and custom pages as platform-limited (BoldTrail), requiring a support ticket rather than assuming Carrie/Brook has that access — matches 03's technical findings. | — | Confirmed realistic. |

---

## Cross-report consistency check

| Issue | Reports involved | Severity |
|---|---|---|
| Guaranteed-ranking language in 04 ("Realistic Timeline to Top 3") directly contradicts explicit no-guarantee disclaimers in 07 and 05. | 04 vs. 05, 07 | **Blocking** |
| Review-pace targets disagree: 02 recommends 2–4/month sustained; 04 recommends 20–30 in 90 days (~7–10/month); 07 projects ~5–10 by day 60. | 02, 04, 07 | Should-fix |
| `09_questions_for_client.md` Q5 lists only 2 conflicting phone numbers (337-258-5379 vs. 337-522-7554), omitting the Homes.com 337-341-8976 conflict documented in 00, 01, 02, and `nap_consistency_matrix.csv`. Q6 similarly lists only 2 of the 5 documented address variants. | 09 vs. 00/01/02 | Should-fix |
| Phone numbers, review counts (29 Zillow / 2 Realtor.com / 0 Homes.com), and the "3 phones / 5 addresses / 3 emails" framing are otherwise consistent across 00, 01, 02, 03, 05. | — | Confirmed clean |
| No report recommends "standardize using Zillow/Realtor.com addresses as reference" — the suspected canonical-NAP overreach was specifically checked for in 01 and not found; every report correctly defers the canonical NAP decision to Carrie via `[client-confirm]`. | 01, 02, 05 | Confirmed clean |
| No fake reviews, incentivized reviews, bought links, doorway pages, or keyword-stuffed GBP names found anywhere in the reviewed set. | All | Confirmed clean |
| ICON Agent 2x vs. 3x discrepancy is consistently flagged `[client-confirm]` everywhere it appears (01, 02, 05, page briefs) — never silently resolved in one direction. | 01, 02, 05, briefs | Confirmed clean |

---

## Summary

**Total flags:** 24
- **Blocking:** 6
- **Should-fix:** 14
- **Nit:** 4

(Plus 6 explicit "confirmed clean" checks that were specifically tested per the QA brief and found to have no issue.)

### Top blocking issues

1. **04_competitor_gap_analysis.md — guaranteed-ranking language.** The "Realistic Timeline to Top 3" section (lines 192–195) promises specific SERP position ranges by month 3/6/12, contradicting the explicit no-guarantee disclaimers in `05_ai_search_visibility_plan.md` (Section 6) and `07_30_60_90_day_plan.md` ("No ranking positions are guaranteed, by us or anyone"). This is the report set's clearest ethics/consistency violation and should not ship to the client as-is.
2. **04_competitor_gap_analysis.md — fabricated precision.** "Dedicated domain + area pages improve organic rank by 2–3 positions" (line 103) states an invented, unsourced specific number as fact.
3. **04_competitor_gap_analysis.md — unhedged low-confidence claim.** "Carrie... ranks #8–10 in most organic queries" (Summary, line 185) is stated as flat fact despite `source_log.csv` explicitly marking this a low-confidence inference, and despite the report's own SERP-approximation caveat earlier in the same document.
4. **04_competitor_gap_analysis.md — no evidence-tagging scheme.** Unlike 02/03/05/06, report 04 never adopts the `[verified]`/`[inferred]`/`[client-confirm]`/`[best-practice]` key, making it impossible to distinguish confirmed data from inference throughout the document.
5. **01_public_presence_inventory.md — systemic `[verified]` mislabeling.** The report uses `[verified]` to mean "successfully fetched," not "confirmed true," with no tagging-key preamble to disambiguate. This causes explicitly unverified metrics (11 years of experience, license number) to be tagged `[verified]` in violation of the role file's explicit instruction that these must read "verify with Carrie."
6. **01_public_presence_inventory.md — unverified production stats tagged at too-confident a level.** The Homes.com and LoopNet entries (46 families, $10.5M, #45/1900, ICON Agent) carry an overall `[verified]` assessment tag even though the specific stats inside them are exactly the category of claim the role file requires to be gated `[client-confirm]`.

Everything downstream of 01 and 04 (02, 03, 05, 06, the content templates, and the 4 spot-checked page briefs) is materially more disciplined — correctly gates unverified metrics, avoids fake/incentivized-review and doorway-page patterns, and is realistic about platform (BoldTrail) access limits. The fixes needed are concentrated in reports 01 and 04.

---

## Resolution log (2026-07-08)

All blocking and should-fix items below were applied directly to `01_public_presence_inventory.md` and `04_competitor_gap_analysis.md`. Original QA tables above are left intact for the record.

### 01_public_presence_inventory.md
- Added a tagging-key preamble distinguishing `[verified]` = "confirmed this appears on the source" from factual truth, plus an explicit note that NAP-as-displayed stays `[verified]` while career/production claims are downgraded — **Fixed**.
- Line 62/66, "11 years" retagged from `[verified]` to `[client-confirm]` — **Fixed**.
- Line 96/100, License number retagged from `[verified]` to `[client-confirm]`, cross-referenced to the Homes.com variant conflict — **Fixed**.
- Homes.com bio stats (ICON Agent, Certified Mentor, 46 families, $10.5M, #45/1900) given explicit inline `[client-confirm]` tags; section-level "Assessment" split into `[verified]` (page fetched/displays this) vs. `[client-confirm]` (stats aren't fact) — **Fixed**.
- LoopNet bio stats given the same inline `[client-confirm]` treatment and split assessment — **Fixed**.
- Nextdoor ICON/mentor/top-producer credentials retagged `[client-confirm]`; LinkedIn RAA/mentor credentials retagged `[client-confirm]` — **Fixed**.
- Bio Quality Assessment section: added a caveat that "Strong" rates writing quality, not truth, and tagged each credential-bearing bio `[client-confirm]` — **Fixed**.
- Data Quality Notes rewritten to separate "source fetched successfully" from "claims on it are true," with an explicit list of all career/production claims requiring `[client-confirm]` — **Fixed**.
- Critical Gaps recommendation #2 (update website bio) rewritten to require client confirmation of every stat before publishing, instead of listing unverified figures as ready-to-use bio content — **Fixed**.
- Executive Summary and Conclusion: added inline `[verified]`/`[client-confirm]` tags to the review-count and credentials claims mentioned in prose — **Fixed** (nit).
- Homes.com/LoopNet overall `[verified]` assessments corrected per QA (see above) — **Fixed**.

### 04_competitor_gap_analysis.md
- Added the standard `[verified]`/`[inferred]`/`[client-confirm]`/`[best-practice]` tagging key at the top, matching 02/03/05/06, and applied tags throughout (competitor table, Common Traits of Winners, Gap Matrix, Summary) — **Fixed**.
- "Realistic Timeline to Top 3" (specific #5–7/#3–5/top-3 rank-by-month promises) rewritten to directional, hedged language: no ranking positions are guaranteed; meaningful map-pack/organic gains are realistic by months 4–6 if cadence holds — **Fixed**.
- "Dedicated domain + area pages improve organic rank by 2–3 positions" rewritten to correlation language: competitors with dedicated area pages consistently outrank those without; magnitude varies, no specific position count promised — **Fixed**.
- "Carrie ranks #8–10 in most organic queries" restated as `[inferred, low confidence — SERPs vary by location/personalization]`, cross-referenced to the SERP Approximation Caveat and `source_log.csv` — **Fixed**.
- Gap Matrix "Review Count: [TBD]" replaced with the actual figures from 01/02 (29 Zillow / 2 Realtor.com / 0 Homes.com / 0 Google) — **Fixed**.
- "Zillow Reviews" column header relabeled "Review Count (platform varies)"; Stephen Hundley (Experience.com) and Nah Senpeng (FastExpert) rows annotated with their actual source platform instead of implying Zillow — **Fixed**.
- Jessica Broussard's "$105M+ sales, Top 1% claim" and Keaty's "most innovative" positioning annotated "(self-reported, unverified)" — **Fixed** (nit).
- Review-pace target changed from "20–30 in 90 days" to a sustained 2–4/month (≈6–12/90 days) pace, matching 02's anti-burst rationale, and reconciled with 07 — **Fixed**.
- Ethical Guardrails "Do NOT" list expanded to include "promise specific ranking positions or timelines" — **Fixed**.

---

## Addendum (2026-07-08): Major factual correction — Google Business Profile

**What happened:** This audit's original conclusion — stated in `01_public_presence_inventory.md`, `02_local_seo_audit.md`, `00_client_brief.md`, `04_competitor_gap_analysis.md`, `05_ai_search_visibility_plan.md`, `07_30_60_90_day_plan.md`, `data/public_assets.yaml`, `data/nap_consistency_matrix.csv`, and `site/audit/index.html` — was that **no Google Business Profile exists** for Carrie Billeaud, based on three search-query variants returning zero results. This was **wrong**. Carrie's GBP exists and is strong: 185 reviews, 5.0 rating, live at `https://share.google/kcBY0AQWmnVjNLAy4`. The client (Brook) supplied the profile link directly, and it was verified against the live Google knowledge panel on 2026-07-08 (kgmid `/g/11s57kl156`).

**Correction applied across:** `data/public_assets.yaml`, `data/nap_consistency_matrix.csv`, `data/source_log.csv`, `data/known_claims.yaml`, `reports/01_public_presence_inventory.md` (including a dedicated Errata section), `reports/00_client_brief.md`, `reports/02_local_seo_audit.md`, `reports/04_competitor_gap_analysis.md`, `reports/04b_serp_patterns_and_reuse.md`, `reports/05_ai_search_visibility_plan.md`, `reports/07_30_60_90_day_plan.md`, and `site/audit/index.html`. The framing shifted from "create a GBP" to "obtain manager access to and optimize the existing GBP," with a new, honestly-flagged issue: the profile's business name ("Carrie Billeaud Realtor | Acadiana & Surrounding Area | eXp Realty") is keyword/area-decorated and risks a Google real-world-name policy action — this needs to be fixed carefully (discuss with Carrie, change only the name in one pass, document before/after), not lumped in with other edits.

**Lesson for this engagement and future audits:** *absence of search evidence is not evidence of absence.* A search sweep (here, 3 query variants) failing to surface an entity should be reported as "not found via our search methodology" with appropriately hedged confidence — not escalated to "does not exist," especially before checking with the client, who may simply know something the audit's search tools couldn't surface. In this case the GBP's own decorated name likely degraded how easily it matched our search queries, which is itself a legitimate discoverability finding — but it should have been investigated further or flagged as low-confidence, not asserted as fact. The original `01_public_presence_inventory.md` GBP entry was tagged `[verified]` for "No GBP exists" — that tag was applied to an absence-of-evidence conclusion, which is exactly the kind of overconfident labeling this QA pass exists to catch. Going forward: any "NOT FOUND" / "does not exist" conclusion about a client's public asset should be tagged `[inferred, low confidence — search sweep only]` rather than `[verified]`, and should prompt an explicit direct question to the client before being treated as a finding to build recommendations on.

**Addendum (2026-07-08, second pass):** TikTok (`@carriebilleaud_realtor`) was visible in the Homes.com profile's `social_links` field captured during the first pass but was not separately inventoried as its own asset — an inventory-completeness miss, not a factual error. Caught while verifying a client-flagged second Facebook page (`/carriebilleaudrealty`); see `01_public_presence_inventory.md` Addendum (2026-07-08, second pass) for the full write-up.

**Addendum (2026-07-08, third pass):** Instagram and both Facebook entities — previously BLOCKED/not_found across `data/public_assets.yaml`, `data/nap_consistency_matrix.csv`, and `01_public_presence_inventory.md` — were directly verified via a live logged-in browser session. All "no data" rows for these three sources are now resolved to `[verified]`; the "two Facebooks" open question is resolved as a personal-profile/business-page split, not competing identities. See `01_public_presence_inventory.md` Addendum (third pass), `04_competitor_gap_analysis.md` Addendum (owned domain), and new `10_facebook_reels_and_marketing_spend.md`.

**Addendum (2026-07-11):** The "father on team" detail (Realtor.com bio extraction) was flatly disputed by the client — purged from all client-facing copy and marked `contradicted` in known_claims.yaml. Lesson: a bio *mentioning* a family member is not the same as the extracted relationship claim; single-source extracted biography details should be [client-confirm] by default, not [verified].
