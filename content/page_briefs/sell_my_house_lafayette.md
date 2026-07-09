# Page brief: sell_my_house_lafayette

**Distinct from `lafayette_listing_agent`:** this is the highest-intent, most transactional page in the whole set — someone typing "sell my house Lafayette" wants a number and a next step *now*, not a deep dive on marketing philosophy (that's the listing-agent page). Keep this page shorter and CTA-dense; push process depth to the listing-agent page via internal link.

**Platform & publishing note:** This is the top priority page to get live in some form even if it's just a strong CTA block added near the top of the bio/blog, because it's the single highest seller-intent keyword in the map (P1, "highest seller intent" per `keyword_intent_map.csv`). If a true instant-valuation tool isn't available on BoldTrail, use a "request your home value" form routed to Carrie directly instead of a fake automated estimate — do not imply an automated valuation exists if it doesn't.

## 1. Target query cluster
"Sell my house Lafayette."

## 2. Search intent
Transactional-local, decision stage — highest seller intent in the keyword map. Reader wants to know what their house is worth and how fast they can sell, right now.

## 3. Page purpose (lead action)
Home value request / CMA request — the single most direct lead-capture form in the whole content set: address + basic property details + contact info.

## 4. Suggested title tag
`Sell My House in Lafayette, LA | Free Home Value | Carrie B.` (60 chars — trim "Free Home Value" if over)

## 5. Meta description
`Selling your home in Lafayette, LA? Get a free, no-obligation home value estimate from local Realtor Carrie Billeaud — staging included. Request yours now.` (154 chars)

## 6. H1
`Sell My House in Lafayette, LA — Get a Free Home Value Estimate`

## 7. Outline

### H2: What's My Lafayette Home Worth?
- Lead with the form, above the fold. Short supporting copy: how the estimate/CMA process works and what happens after they submit (Carrie personally follows up — set the expectation that this isn't an automated bot estimate).

### H2: How Selling Works With Carrie
- Condensed 3–4 step version (full detail lives on `lafayette_listing_agent`): valuation → staging/prep → marketing → offer/close.
- One line on staging [verified specialty] as a built-in step, not an upsell.

### H2: Current Lafayette Market Snapshot
- [client-confirm] Fresh market data (median price, typical days on market) sourced and dated at publish time — do not scrape the site's own dynamically-generated IDX area-page stats verbatim into static copy, since those numbers will go stale and the page becomes inaccurate. Set a reminder to refresh this section quarterly.

### H2: Selling in Youngsville, Broussard, or Elsewhere in Acadiana?
- Short paragraph + links to `youngsville_realtor` / `broussard_realtor` for readers whose home isn't in Lafayette proper.

### H2: Frequently Asked Questions
(see section 11)

## 8. Internal links
- **To:** `lafayette_listing_agent` (process depth), `youngsville_realtor`, `broussard_realtor`.
- **From:** `lafayette_realtor` hub, `lafayette_listing_agent`, GBP posts (this page is the natural landing target for any "thinking of selling?" GBP post or social CTA).

## 9. CTA
Primary, repeated (top and bottom): "Get my free home value estimate" form (address, basic details, phone/email). Secondary: click-to-call for sellers who'd rather just talk.

## 10. Trust signals
- Home stager credential [verified] — directly relevant, lead with it in the process section.
- Zillow 29 reviews, 5.0 [verified]
- Team of 4 [verified] — faster response to seller inquiries.
- [client-confirm] Any recent, permissioned sale results/testimonials specific to speed or price — do not use unverified figures from `known_claims.yaml`.

## 11. FAQ section
1. **How much is my house worth?** — Explain the CMA gives a real, personalized number — the form is how to get it, not a generic answer here.
2. **How fast can I sell my house in Lafayette?** — [client-confirm] realistic current timeline; don't guess.
3. **Do I need to make repairs or stage my home before selling?** — Tie to staging specialty; honest, practical answer.
4. **What fees/commission will I pay?** — [client-confirm] whether to publish a rate; keep transparent and accurate to current practice.
5. **Can I sell if I still owe money on my mortgage?** — General educational answer (payoff-at-closing explainer).
6. **Do you buy houses directly / is this a cash-offer service?** — Clarify Carrie is a traditional listing agent, not an iBuyer, unless [client-confirm] she offers something different.

## 12. Schema recommendation
`RealEstateAgent` + `Service` ("Home Valuation / Listing Services"). If a genuine on-page FAQ ships, add `FAQPage` schema too. Same platform-limited path as other briefs — flag for BoldTrail support ticket; this page's high intent value makes it the strongest single candidate to push for schema/indexing fixes first if the client only fixes one platform issue.
