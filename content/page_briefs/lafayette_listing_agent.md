# Page brief: lafayette_listing_agent

**Distinct from `sell_my_house_lafayette`:** this page is for the *agent-selection* moment — a homeowner who knows they'll sell soon and is comparing listing agents on process, marketing, and track record. `sell_my_house_lafayette` is the *transactional* moment — "I want a number and a plan now." Do not merge these; they serve different points in the funnel and target different query intent (commercial vs. transactional).

**Platform & publishing note:** Best built as a blog post initially (the technical audit confirms blog posts render real, indexable-quality content on this platform, unlike the noindex `/areas/` templates). If BoldTrail's custom-page feature is available, promote to a standalone page later; otherwise keep as a pinned, linked blog post until a standalone domain exists.

## 1. Target query cluster
"Listing agent Lafayette LA."

## 2. Search intent
Commercial-local, decision stage. Homeowner is choosing between agents (or between an agent and a discount/FSBO/iBuyer route) and wants proof of process and marketing capability.

## 3. Page purpose (lead action)
Book a listing consultation (in-home or virtual walkthrough + pricing conversation) — not an instant online valuation (that's the other page's job).

## 4. Suggested title tag
`Lafayette Listing Agent | Carrie Billeaud, eXp Realty` (52 chars)

## 5. Meta description
`Choosing a listing agent in Lafayette, LA? Carrie Billeaud pairs a full marketing plan with in-house home staging. 5.0-rated, local team. Book a consult.` (152 chars)

## 6. H1
`Lafayette Listing Agent — Sell With a Local Marketing Plan`

## 7. Outline

### H2: What a Listing Agent Actually Does For You
- Plain-language explainer: pricing strategy, marketing/exposure, negotiation, paperwork/closing coordination. Written for a homeowner who's never sold before, not real-estate jargon.

### H2: Carrie's Listing Process
- H3: Pricing — data-driven approach (tie to her analytical/business-degree background [verified]), not "list high and see."
- H3: Staging — she's a certified home stager [verified]; explain that staging is done in-house as part of the listing, not an upsell. This is a genuine differentiator vs. most competitor agents named in `04_competitor_gap_analysis.md`.
- H3: Marketing & exposure — [client-confirm] specifics: professional photography, MLS syndication, social promotion (tie to her Instagram/Facebook presence), team support (team of 4 [verified] means faster showings coordination).
- H3: Negotiation & closing — team of 4 including her father [verified] gives a "always someone available" framing — write honestly, not as a gimmick.

### H2: Neighborhoods & Home Types
- Note she lists across Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, Milton — link to area pages for Youngsville/Broussard specifically.
- [client-confirm] any notable recent listings/neighborhoods she's most active in.

### H2: Why Sell With a Local Agent (vs. Discount Brokerage or iBuyer)
- Honest, non-fear-mongering comparison: full-service marketing and negotiation vs. flat-fee/limited-service or cash-offer models. [client-confirm] if Carrie wants this section — some agents prefer not to disparage alternatives; keep tone neutral/educational if included.

### H2: Frequently Asked Questions
(see section 11)

## 8. Internal links
- **To:** `sell_my_house_lafayette` (for the reader who wants a number now), `lafayette_realtor` (hub/bio), `youngsville_realtor`, `broussard_realtor`.
- **From:** `lafayette_realtor` hub, `sell_my_house_lafayette` (cross-link both directions), homepage blog index.

## 9. CTA
Primary: "Schedule your free listing consultation" (form: address + timeframe + phone). Secondary: click-to-call.

## 10. Trust signals
- Home stager credential [verified] — the single strongest differentiator for this specific page; lead with it.
- Team of 4, father on team [verified]
- Zillow 29 reviews, 5.0 [verified]
- Certified mentor [verified] — brief mention only, less relevant to a seller than staging/reviews.
- [client-confirm] Years of experience, ICON Agent status, any specific listing performance stats (days-on-market, list-to-sale ratio) — do not publish without client-supplied, current, verifiable numbers.

## 11. FAQ section
1. **How does Carrie price my home?** — Explain CMA-based pricing in plain terms; avoid promising a specific number.
2. **Does staging cost extra?** — Explain what's included vs. not [client-confirm exact scope — full staging, consultation only, or partial].
3. **How long does it typically take to sell a home in Lafayette?** — [client-confirm] current local market timing; do not guess a number.
4. **What's Carrie's commission?** — [client-confirm] whether to publish a rate or keep it "ask during your consultation" (common practice; also affected by post-NAR-settlement buyer-agreement norms — confirm current approach with Carrie).
5. **Do I need to make repairs before listing?** — General educational answer (a stager's perspective is a natural fit here — small fixes vs. major renovation ROI).
6. **What areas does Carrie list in?** — Restate the 8 service areas.

## 12. Schema recommendation
`RealEstateAgent` + `Service` (schema.org) describing "Home Listing / Seller Representation," with `areaServed` for the 8 cities and `provider` linking to the `Person` entity on the hub page. Platform-limited per `03_website_technical_audit.md` — same BoldTrail support-ticket path as the hub page; if published as a blog post short-term, request `BlogPosting`/`Article` schema instead as the interim, since that's the content type BoldTrail actually renders today.
