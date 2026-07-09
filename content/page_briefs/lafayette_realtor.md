# Page brief: lafayette_realtor

**Role in structure:** Hub / pillar page. Every other brief links back here; this is the closest thing the site has to a homepage-for-search-intent. Publish first.

**Platform & publishing note:** This content belongs on the eXp/BoldTrail agent bio (`/agents.php` "About Carrie" field is agent-editable today — see `03_website_technical_audit.md` P1 fix) plus, if BoldTrail supports adding a custom page, a standalone page at this URL slug. If custom pages aren't available on the platform, fold this content into the bio field and a pinned blog post, and treat a future standalone domain (per `04_competitor_gap_analysis.md`) as the long-term home for the full pillar-page version.

## 1. Target query cluster
"Lafayette LA realtor," "best realtor Lafayette LA," "real estate agent Lafayette LA," "Acadiana realtor" (regional variant).

## 2. Search intent
Commercial-local, decision stage (with the regional "Acadiana realtor" term skewing slightly earlier, consideration stage). Someone comparing agents by name, credibility, and service area — not yet searching a specific listing.

## 3. Page purpose (lead action)
Primary contact conversion: phone call, text, or contact-form submission requesting a consultation. This page's job is to answer "who is this person and can I trust her" fast enough that the visitor calls instead of bouncing to the next agent's site.

## 4. Suggested title tag
`Lafayette, LA Realtor | Carrie Billeaud, eXp Realty` (49 chars)

## 5. Meta description
`Carrie Billeaud is a Lafayette, LA Realtor with eXp Realty serving Lafayette, Youngsville, Broussard & Acadiana. 5.0 rating, 29 reviews. Call or text today.` (154 chars)

## 6. H1
`Lafayette, LA Realtor — Carrie Billeaud, eXp Realty`

## 7. Outline

### H2: Meet Carrie Billeaud
- Short, human bio: Lafayette-area Realtor with eXp Realty, business degree from the University of Louisiana at Lafayette [verified — Zillow bio], analytical approach to pricing and investment.
- Family/team note: works alongside her father and a team of 4 [verified — Zillow team profile]. This is a genuine differentiator (multi-generational, local roots) — write it as a real detail, not a slogan.
- [client-confirm] Years licensed/active (public listings say 11 — confirm before publishing as fact).

### H2: Areas Carrie Serves
- Named list, each a short sentence, each linking to its own page where one exists: Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, Milton, and the wider Acadiana region.
- Frame as "I live and work here" not a generic service-area list — [client-confirm] a line about how long she's worked each area / any personal connection.

### H2: How Carrie Can Help
- Three short blocks, each linking out to its dedicated brief:
  - Buying your first home → `first_time_homebuyers_lafayette`
  - Buying (any stage) → `lafayette_buyers_agent`
  - Selling / listing your home → `lafayette_listing_agent` and `sell_my_house_lafayette`
- One line on investment/rental property specialty [claimed specialty — do not attach unverified transaction numbers].

### H2: Why Local Buyers and Sellers Choose Carrie
- Home stager credential [verified] — explain what it means in practice (she stages listings herself/with her team before photos, not an outsourced add-on).
- Certified mentor [verified] — frame as "trains other agents," a credibility signal, not a buyer/seller benefit per se — keep it brief.
- [client-confirm] ICON Agent / eXp production status — do not state without client sign-off; if confirmed, explain in one plain-English sentence what it means (eXp production tier), not just the badge name.
- 29 reviews, 5.0 average on Zillow [verified] — quote 1–2 real reviews if Carrie can supply permission; otherwise state the count/rating plainly and link to the Zillow profile.

### H2: Frequently Asked Questions
(see section 11)

## 8. Internal links
- **To:** `lafayette_listing_agent`, `lafayette_buyers_agent`, `first_time_homebuyers_lafayette`, `sell_my_house_lafayette`, `youngsville_realtor`, `broussard_realtor`.
- **From:** every other brief in this set links back here as "About Carrie" / hub; site nav; blog post author bios; GBP profile link (once created).

## 9. CTA
Primary: "Call or text Carrie" with `tel:` link — use `337-258-5379` [client-confirm canonical number; public listings conflict, see `09_questions_for_client.md` Q5]. Secondary: contact form ("Tell me what you're looking for") as a lower-friction fallback for visitors who won't call.

## 10. Trust signals
- Zillow: 29 reviews, 5.0 rating [verified]
- UL Lafayette business degree [verified — Zillow bio]
- Team of 4, including her father [verified — Zillow team profile]
- Home stager [verified]
- Certified mentor [verified]
- [client-confirm] 11 years of experience
- [client-confirm] ICON Agent status
- Do NOT use: 174 closed sales/$44.6M, 46 families helped/$10.5M, "#45 of 1900 realtors" — all unverified/conflicting across sources per `known_claims.yaml`; omit until Carrie confirms exact, current figures.

## 11. FAQ section
1. **What areas does Carrie Billeaud serve?** — List the 8 named areas; note she also works broader Acadiana on a case-by-case basis.
2. **Is Carrie Billeaud a buyer's agent or listing agent?** — Both; explain dual capability and that buyer representation typically costs the buyer nothing (commission convention — [client-confirm] current buyer-agreement/commission practice post-NAR settlement changes, since this varies by market and date).
3. **How many years has Carrie been a Realtor?** — [client-confirm] before answering with a number; otherwise answer qualitatively ("an established local agent — ask for her specific timeline").
4. **Does Carrie work with investment/rental property buyers?** — Yes, claimed specialty; keep answer general, no unverified stats.
5. **What makes Carrie different from other Lafayette agents?** — Home staging included, family team, local roots — human, specific answer, not marketing copy.
6. **How do I get started?** — Point to the CTA; explain what a first call/consult covers (5 minutes, no pressure).

## 12. Schema recommendation
Ideal: `Person` + `RealEstateAgent` (schema.org), with `areaServed` listing all 8 cities, `aggregateRating` (29 reviews / 5.0, sourced and dated), `alumniOf` (UL Lafayette), and `worksFor` → eXp Realty organization. **Do not include a `PostalAddress`** — no single confirmed office address exists across sources (see NAP conflicts in `00_client_brief.md`/`09_questions_for_client.md`); use `areaServed` only until an address is confirmed, consistent with eXp's virtual-brokerage model.
Per `03_website_technical_audit.md`, JSON-LD is a template-level gap on BoldTrail with no agent-side workaround — this schema should be requested via BoldTrail/eXp support ticket, or implemented directly if/when a standalone domain is built.
