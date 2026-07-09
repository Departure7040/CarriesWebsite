# 02 — Local SEO & Google Business Profile Audit
**Subject:** Carrie Billeaud, Realtor — eXp Realty, Lafayette LA
**Date:** 2026-07-08
**Prepared by:** local_seo_analyst

**Tagging key:** `[verified]` = confirmed via direct fetch of a live source · `[inferred]` = reasonable conclusion from available data, not independently confirmed · `[client-confirm]` = requires a decision or fact from Carrie before it can be used · `[best-practice]` = Google/industry guidance applied generically, not specific to Carrie's data.

---

## (a) What the Client Must Provide Before Work Can Proceed

This is the blocking list. Nothing in Section (b) can go fully live until these are answered. See `/reports/09_questions_for_client.md` for the full question set — the items below are the subset that gates this report specifically.

1. **Google Business Profile does not exist.** `[verified]` — searched 2026-07-08 across three query variants (business name + city, business name + "Google Business Profile," business name + "Google Maps rating"); zero results. This is not a claim/unclaim situation — a **brand-new profile must be created**. Carrie (or Brook, with Carrie's Google account access) needs to:
   - Confirm which Google account will own the profile (personal Gmail vs. a business-dedicated Google account — recommend creating a dedicated one so ownership doesn't get tangled with a personal account `[best-practice]`).
   - Be available to receive and enter the postcard/phone/email verification code Google sends after profile creation — this can take 1–14 days by mail `[best-practice]`.
2. **Canonical NAP decision.** `[client-confirm]` — Name, Address, Phone cannot be finalized. Current conflicts, per `/data/nap_consistency_matrix.csv`:
   - **Phone:** 337-258-5379 (6 of 8 sources) vs. 337-341-8976 (Homes.com only) vs. 337-522-7554 (LoopNet only).
   - **Address:** 5 distinct variants across 6 sources (110 Marais Ave Youngsville; 1318 Camellia Blvd Ste 222; 91 Settlers Trace Blvd Bldg 1; 1720 Kaliste Saloom Ste B 2; 3 Flagg Place Bldg B Ste B-4 — all Lafayette except the Youngsville one).
   - **Email:** carriebilleaud@gmail.com vs. carrie.billeaud@exprealty.com vs. southerncollectivegroup.info@gmail.com.
   - Everything phone/address/email-related in this report is written **conditionally** — "once canonical NAP is confirmed, use X here" — rather than picking one for you.
3. **Business name for GBP.** `[client-confirm]` — Google requires the real-world name used at your storefront/signage/stationery, not a keyword-stuffed variant. We need your confirmation of the exact legal/operating name: e.g. "Carrie Billeaud" vs. "Carrie Billeaud, Realtor" vs. "Carrie Billeaud Team." See Section (b)(1) for the policy detail.
4. **Storefront vs. service-area business (SAB) decision.** `[client-confirm]` — does Carrie meet clients at a fixed, staffed office with regular hours (e.g., an eXp Lafayette office desk), or does she work from home/on the road and meet clients at listings/coffee shops? This determines whether GBP shows a public address pin or hides the address and shows a service-area radius only. See Section (b)(4).
5. **Access:** Google Search Console / Analytics access, and confirmation of who can act as the GBP's Primary Owner (should be Carrie, with Brook added as Manager) `[client-confirm]`.
6. **Marketing-claim sign-off.** `[client-confirm]` — Every production statistic currently floating around Carrie's profiles (174 closed sales / $44.6M over 5 years, 11 years of experience, 50+ families/year, "2x" vs "3x" ICON Agent, RAA membership) is logged as `status: unverified` in `/data/known_claims.yaml`. None of these may go into the GBP description, posts, or Q&A until Carrie confirms them individually. Draft copy below marks every such figure `[client-confirm]` and uses bracket placeholders instead of hard numbers.

---

## (b) GBP Creation + Optimization Checklist

### 1. Business name

`[best-practice]` Google's guidelines require the Business Profile name to match what customers would actually see on a sign, invoice, or stationery — no keyword stuffing (e.g., "Carrie Billeaud - Lafayette Realtor - Homes for Sale Youngsville Broussard" would violate policy and risks suspension).

Recommended pattern, pending client confirmation: **"Carrie Billeaud, Realtor"** or **"Carrie Billeaud — eXp Realty"**. Do not append service-area or specialty keywords to the name field. `[client-confirm]` — final name string.

If Carrie ultimately wants a team brand ("Carrie Billeaud Team," referenced on Zillow Team and Nextdoor `[verified]`), that should be a **separate consideration for later**, not the initial GBP name — Google associates one GBP per distinct, verifiable business entity, and an individual agent profile is the safer, faster path to verification. `[inferred]`

### 2. Categories

- **Primary category:** Real Estate Agent `[best-practice]` — this is the standard, correctly-scoped category for an individual agent (not "Real Estate Agency," which implies a brokerage entity).
- **Secondary categories (add as many as accurately apply):** Real Estate Consultant, Property Management Company (only if she actively manages rentals — Zillow lists Property Management/Rentals as a specialty `[verified]`), Real Estate Appraiser (only if licensed for it — do not add unless true).
- Do not add unrelated categories to chase visibility; category-stuffing is a common Google spam trigger. `[best-practice]`

### 3. Services list

Based on specialties consistently listed across profiles `[verified]`: Buyer's Agent, Listing Agent/Seller's Agent, First-Time Home Buyer Assistance, Investment Property, Residential Sales, Relocation Assistance, New Construction. Add "Property Management" and "Staging" only if Carrie confirms she still actively offers them `[client-confirm]` (they appear on Zillow but not elsewhere).

### 4. Service-area setup (storefront vs. SAB)

`[client-confirm]` pending Section (a)(4) decision, but lay out both paths honestly:

- **If Carrie has a real, staffed address she'd want a client to walk into:** set up as a storefront listing with the canonical address visible, and set service areas around it. This is generally the stronger option for local-pack ranking because Google can more confidently verify and rank a fixed location. `[best-practice]`
- **If Carrie works from home or has no address she wants published:** set up as a Service-Area Business (SAB) — hide the address, and list service areas as cities/neighborhoods, not a radius. Google **caps SAB profiles at 20 service areas**, so pick deliberately rather than listing every town in the region. `[best-practice]`
  - Priority tier (core, list first): Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, Milton `[verified — confirmed in phase-1 findings]`.
  - Do NOT default to the 20+ extended list some profiles show (Abbeville, Opelousas, Ville Platte, etc. `[verified from public_presence_inventory]`) — spreading thin across 20+ areas dilutes relevance signal for the towns that matter most. Confirm the priority ranking with Carrie per question 7 in `09_questions_for_client.md`. `[client-confirm]`
- Either way, a home address should never be used as a public storefront address if Carrie doesn't want clients showing up there — Google will reject/suspend listings that use a residential address inconsistent with public-facing service. `[best-practice]`

### 5. Description (draft — verified facts only, placeholders for unconfirmed metrics)

> Carrie Billeaud is a Realtor with eXp Realty serving Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, and Milton, Louisiana. She works with first-time buyers, sellers, and investment property clients on residential real estate throughout the Acadiana area. [client-confirm: years of experience — publicly shown as 11 years on Realtor.com, unverified], [client-confirm: production stats — Homes.com references 46 families served and $10.5M in volume in one year, and a separate figure of 174 closed sales / $44.6M over 5 years appears in our source data; verify before use], [client-confirm: ICON Agent status — sources disagree between 2x and 3x, confirm the correct count]. Contact Carrie to buy, sell, or invest in Acadiana real estate.

`[best-practice]` GBP descriptions are capped at 750 characters and carry no direct ranking weight from keyword density, but should be scannable and accurate — this draft intentionally omits any unverified number until Section (a)(6) is resolved.

### 6. Attributes

`[best-practice]` Standard attributes to enable where true: Identifies as woman-owned (if applicable, `[client-confirm]`), Online appointments, Onsite services (if she does listing consults in-home), Languages spoken (`[client-confirm]` — none currently documented). Avoid enabling attributes that can't be substantiated if profile is audited.

### 7. Hours

`[client-confirm]` — real estate agents commonly list broad hours (e.g., Mon–Sun 8am–8pm) reflecting realistic availability rather than rigid office hours, since buyers/sellers search evenings and weekends. Confirm actual availability windows with Carrie before publishing; do not default to standard 9–5 business hours, which understates evening/weekend availability that's normal in this industry. `[best-practice]`

### 8. Phone

`[client-confirm]` — pending canonical NAP decision (Section a-2). Whichever number is chosen, it must then be:
- Used verbatim (same formatting) on the GBP, website, and every directory listed in `/data/nap_consistency_matrix.csv`.
- A number Carrie personally answers or that reliably reaches her — GBP phone numbers get call-tracked by Google's "call" button analytics, and a wrong/dead number actively damages prominence signals over time. `[best-practice]`

### 9. Website link (UTM-tagged)

`[best-practice]` Recommended primary link target: `https://carriebilleaud.exprealty.com` (her owned domain — see `01_public_presence_inventory.md` canonical URL recommendation). Apply UTM parameters so GBP-driven traffic is trackable in GA4 once access is granted (Section a-5):

```
https://carriebilleaud.exprealty.com/?utm_source=google&utm_medium=organic&utm_campaign=gbp_profile
```

Use a distinct campaign tag per GBP feature that links out (profile link vs. individual posts) so performance can be compared — see Section (b)(12).

### 10. Photos plan

`[best-practice]` Google ranks/rewards profiles with regularly updated, real (non-stock) photos; there is no evidence geotagging photo EXIF data affects local ranking — this is a persistent SEO myth and should not be treated as a task. Recommended photo types and cadence:

| Type | Examples | Cadence |
|---|---|---|
| Profile/cover photo | Professional headshot, branded cover image | Set once, refresh every 6–12 months |
| Team/at-work photos | Carrie with clients (with permission), at a closing table, at a sign install | 2–4 new photos/month |
| Listing photos | Exterior of active/recent listings (with seller permission) | Tied to listing cadence — add when a new listing goes live |
| Neighborhood/local photos | Recognizable Lafayette/Youngsville/Broussard/Carencro landmarks or streetscapes | 1–2/month, rotate by area |
| Behind-the-scenes | Office, open house setup, community event participation | 1–2/month |

Target: minimum 4–6 new photos/month sustained, rather than a single large upload burst — Google's own guidance and observed local-pack behavior favor consistent freshness signals over one-time volume. `[best-practice]`

### 11. Q&A seeding

`[best-practice]` Google allows any user to post Q&A, including the business owner — seeding legitimate, useful questions early prevents low-quality or spam questions from being the first thing a searcher sees. Suggested seed questions (answers must use only verified facts or `[client-confirm]` placeholders until resolved):

1. What areas do you serve? → List the 7 core cities `[verified]`.
2. Do you work with first-time home buyers? → Yes, confirm as core specialty `[verified]`.
3. Do you help with investment properties? → Yes, per profile specialties `[verified]`.
4. Are you a full-time Realtor? → `[client-confirm]`.
5. What brokerage are you with? → eXp Realty `[verified]`.
6. Do you charge buyers a fee to help them find a home? → `[client-confirm]` — standard buyer-agency answer, confirm current commission structure disclosure comfort.
7. How long have you been a Realtor? → `[client-confirm]` pending years-of-experience verification.
8. Do you help with new construction? → `[client-confirm]` — listed on eXp primary site specialties.
9. Can you help me sell my home if it needs repairs first? → `[client-confirm]` — confirm if this is a service Carrie offers/refers out.
10. Do you offer home staging advice? → `[client-confirm]` — appears on Zillow specialties only, confirm still active.

### 12. Posting cadence

`[best-practice]` Recommend 2–4 GBP posts/month minimum, ideally weekly, mixing content types (see `/content/google_business_profile_posts.md` for 12 ready drafts). Each post should carry its own UTM-tagged link variant (e.g., `utm_campaign=gbp_post_marketupdate_2026_07`) so performance is distinguishable from the static profile link.

---

## (c) Relevance / Distance / Prominence Gap Analysis

Google's local ranking framework rests on three factors. Current state for Carrie:

**Relevance** — `[inferred]` Currently weak-to-moderate. No GBP means zero relevance signal exists yet for local-pack queries ("realtor near me," "Lafayette LA realtor"). Once created, relevance depends on accurate categories/services/description (Section b) and matching those terms to how buyers/sellers actually search — the competitor gap analysis (`04_competitor_gap_analysis.md`) shows top-ranked agents use area-specific landing pages and dedicated content that reinforces the same relevance signals Google reads. Carrie's owned website currently has a weak, generic bio `[verified]`, which undercuts relevance even before GBP is factored in.

**Distance** — `[inferred]` Cannot be fully assessed without a set address, but the core service area (Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, Milton) is a compact, contiguous market `[verified]`, which is favorable — a tightly-defined service area is easier to rank consistently across than the 20+-city extended list seen on some profiles. Recommend the SAB service-area list stay disciplined per Section (b)(4) rather than sprawling.

**Prominence** — `[verified]` This is the clearest, most quantifiable gap. Per `04_competitor_gap_analysis.md`, the top 6 recurring competitors in Lafayette-area searches show 79–353 Zillow/platform reviews; Carrie currently has 29 reviews on Zillow, 2 on Realtor.com, 0 on Homes.com, and 0 on Google (because no GBP exists) `[verified]`. Prominence is also driven by citation consistency and overall web presence — the NAP chaos documented in Section (a)(2) actively suppresses prominence because Google can't confidently associate scattered, conflicting listings with one confirmed entity. **Prominence is the single highest-leverage, most fixable gap**, because review volume and NAP consistency are both entirely within the team's control, unlike relevance (which competes on content depth) or distance (fixed by geography).

---

## (d) Review Strategy

### Acquisition system

`[best-practice]` Sustained, steady review acquisition consistently outperforms review "bursts" (asking a pile of past clients all at once) — bursts look unnatural to Google's spam detection and create a visible cliff-and-plateau pattern in the review timeline that erodes trust with prospective clients reading dates. Target: **2–4 new reviews per month, sustained indefinitely**, rather than a one-time catch-up campaign. At that pace Carrie would add 24–48 reviews/year, closing meaningfully on the 79–353 competitor benchmark within 12–18 months without ever looking like a manufactured spike.

**Timing:** Ask at the single highest-goodwill moment — immediately after closing, ideally within 24–48 hours, while the experience is fresh and the relief/excitement is highest. `[best-practice]` A secondary ask at the 6-month mark (Section (d) templates) recaptures clients who didn't respond the first time or who have fresh perspective after living in the home.

**Channels:** Text message has the highest response rate for time-sensitive asks; email works well paired with a personal, non-templated opening line; in-person ask at the closing table (verbal, "would you mind leaving a quick Google/Zillow review?") primes the client before the text/email follow-up ever arrives. `[best-practice]`

**Which platforms to prioritize:** Google (once GBP exists — it directly feeds local-pack prominence) and Zillow (already Carrie's strongest platform at 29 reviews `[verified]`, worth reinforcing) should get priority asks. Realtor.com and Homes.com (2 and 0 reviews respectively `[verified]`) need dedicated catch-up attention since they currently show a credibility gap relative to the strong bios posted there.

### Policy compliance

`[best-practice]` Google's and most platforms' review policies prohibit: offering incentives (discounts, gift cards, prize entries) in exchange for reviews; review-gating (asking about experience privately first and only directing happy clients to the public review link while quietly deflecting unhappy ones); posting reviews on behalf of clients; and review swaps with other agents. None of the templates in `/content/review_request_templates.md` include incentive language, and all direct every client to the same public link regardless of anticipated sentiment.

### Response guidance

- **Positive reviews:** Respond within 48 hours `[best-practice]`. Thank the reviewer by first name, reference one specific, real detail from their transaction if known (not generic "thanks for the kind words"), and naturally mention the service area or property type once — this reinforces relevance signals without keyword-stuffing. Keep to 2–3 sentences.
- **Negative reviews:** Respond within 24–48 hours, always professionally, never defensively. Acknowledge the concern without admitting fault that isn't confirmed, offer to resolve it offline (phone/email), and stop there publicly. Never argue in the review thread. `[best-practice]` Do not attempt to get negative reviews removed unless they violate platform policy (fake reviewer, no actual transaction, hate speech, etc.) — flagging illegitimate reviews through the platform's official process is appropriate; pressuring a real client to delete a real complaint is not.

---

## (e) Local Citations / Consistency Plan

Tied directly to the canonical NAP decision in Section (a)(2). Once Carrie confirms name/phone/address/email:

1. **Update in this priority order** (highest authority / highest current traffic first, per `01_public_presence_inventory.md`): (1) new GBP listing — set correctly from day one; (2) eXp primary website + agent profile page — these are the owned, most-controllable sources `[verified: both currently show 337-258-5379, so likely just need address/email alignment]`; (3) Zillow individual profile (29 reviews, highest authority `[verified]`); (4) Zillow Team profile; (5) Realtor.com; (6) Nextdoor; (7) **Homes.com — priority fix**, since it's the only source showing 337-341-8976 `[verified]`, a likely data-entry error or an intentional alternate line that needs Carrie's confirmation either way; (8) **LoopNet — priority fix**, only source showing 337-522-7554 `[verified]`; (9) Facebook, LinkedIn, Instagram (currently blocked from full audit — manual check needed once access exists).
2. **Do not create new citations on additional directories (Yelp, BBB, Chamber of Commerce, etc.) until the canonical NAP is locked in** — adding more listings before standardizing existing ones compounds the inconsistency problem rather than fixing it. `[best-practice]`
3. **After standardization**, spot-check quarterly: search the canonical phone number and address in quotes to catch any new conflicting listing that appears (aggregators sometimes re-scrape stale data even after a source is corrected). `[best-practice]`
4. **License number discrepancy** (0995689513 on Realtor.com vs. 09956895 on Homes.com `[verified]`) should be corrected as part of the same pass — this is very likely a truncation/data-entry error rather than an intentional variant, but confirm the correct 10-digit license with Carrie before editing either listing `[client-confirm]`.

---

## Summary: Top Actions

| # | Action | Blocked on |
|---|---|---|
| 1 | Create Google Business Profile | Client: Google account decision, verification availability |
| 2 | Confirm canonical NAP (name/phone/address/email) | Client decision |
| 3 | Standardize NAP across Homes.com and LoopNet (priority — only sources with wrong phone) | Canonical NAP decision |
| 4 | Launch sustained review request system (2–4/month) | Nothing — templates ready now (`/content/review_request_templates.md`) |
| 5 | Begin GBP posting cadence + photo plan | GBP creation (#1) |
