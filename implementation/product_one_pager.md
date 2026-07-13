# ListingLoop *(working name — the Inventory Marketing Engine)*

**Thesis (one line):** A structured-feed → branded-content + attribution platform. Every new inventory item auto-becomes a branded video, social posts, and a tracked link to a source-tagged lead — human-approved, real photos only. Realtors are the *beachhead*, not the ceiling.

---

### The wedge: the listing-video generator
One sentence sells it: *"Here's a branded Just-Listed 9:16 Short I made from your MLS photos in 30 seconds — no camera crew."* It's visceral, self-evidently valuable, and already built and running feed-driven for Carrie (`batch_listing_videos.py` renders one per active listing). It undercuts what agents pay **right now**: videographers at **$200–500/listing** basic (up to $1,000–1,500 premium) and Matterport at **$200–400+/listing** [verified from analyses]. A solo agent doing ~4 listings/mo spends into the thousands — a subscription is a **5–20x cost takeout** on a line item they already fund.

### Who buys + pricing
**Buyer:** the individual listing agent — median ~10 sides/yr, $58,100 gross income, 87% independent contractors = **single-seat, no-committee close** [verified, 2025 NAR]. The pain is real and unmet: **~74% of agents don't put video on every listing**, yet Reels get +67% engagement [verified].

**Model — monthly subscription, listing-based tiers** (reject credits; they tax the habitual posting you want to grow). All figures **[estimate]**, anchored to ListingAI ($36 Pro / $150 Expert, the closest competitor) and the videographer takeout:
- **Starter ~$49/mo** — up to ~3 listings/mo: video + graphics + per-platform captions.
- **Pro ~$99–149/mo [flagship]** — up to ~8–10 listings/mo: adds the **attribution loop + landing pages + market report + AI lead-response**. Gate the attribution loop here — it's the retention hook.
- **Team/Brokerage ~$299–499/mo** — multi-agent, shared branding, API.
- Levers: **$25–40/listing** à-la-carte on-ramp; **$500–1k/mo** concierge upsell.

### The horizontal play
The wedge isn't real estate — it's any business with **(a) a structured feed, (b) every unit photographed, (c) a steady stream of new-inventory events**. Ranked after realtors:
1. **Auto dealers** — best overall fit; most standardized feeds anywhere (DMS/Google Vehicle Ads/Meta catalog), 20–40 photos/unit, deepest local ad budget, higher ACV. No protected-class steering — compliance is *lighter* than real estate.
2. **Powersports / marine / RV** — same DMS rails (ARI/DX1, Trader Interactive), most organically shareable inventory (video shines most), thin incumbent competition.
3. **Local retail / boutiques (Shopify-native)** — cleanest feed, highest new-arrival velocity, near-zero compliance; honest weakness is low ACV/high churn → the eventual **self-serve volume** play.

*Parallel land-grab:* **property management / STR** reuses the current codebase and fair-housing layer verbatim (zero re-engineering). *Reject* med spas, restaurants, venues — photogenic but no feed and no new-inventory cadence, so the automation has nothing to bite on.

**Generalized product:** *"Turn your inventory feed into branded video, social posts, and tracked leads — automatically, human-approved, real photos only."* A catalog-to-content autopilot.

### Gaps to self-serve ("works for Carrie" → 50 accounts)
The content engine already generalizes across a feed; v1 is mostly a multi-tenant wrapper. Sizes: S=days, M=1–3wk, L=1–2mo [estimate].
1. **Multi-tenant / brand-kit model [M]** — replace hardcoded logo/palette/NAP/license/system-prompts with a per-tenant record. Token-replacement scaffolding already exists; it's a refactor, not greenfield.
2. **Per-account feed connection [L, part-legal] — THE make-or-break.** Today's feed is a reverse-engineered Realtor.com private-GraphQL scrape (fragile, likely ToS-violating, doesn't scale). Real path = MLS/IDX via RESO Web API — per-board credentials, licensing, fees. **Resolve this first as a spike; the licensing timeline gates the whole roadmap.**
3. **Auth + self-serve onboarding [M/L]** — none exists; needs signup + "connect feed / upload brand kit" wizard.
4. **Hosted render pipeline + queue + storage [L]** — move ffmpeg+Chromium off Brook's Windows box to containerized workers + R2/S3 + CDN. Cloudflare Functions can't render video.
5. **Billing [M]** — Stripe subscriptions + plan gating + render metering.
6. **Compliance-at-scale [S/M] + music licensing [M]** — per-*state* ad-disclosure config (LREC is hardcoded); videos ship silent until a licensed track library exists.

*Keep publishing manual and compliance human-in-loop — both are deliberate design choices, not debt. Market-report/reviews/nurture are v2; don't let them delay the video wedge.*

### GTM + Carrie's role
**Wedge-led, one channel.** Land on the listing video; expand into content + lead-response + attribution. Carrie isn't just the flagship user — she's a **credentialed insider seller** (eXp, 5.5K FB w/ verified badge, 185 reviews at 5.0, active in Acadiana agent circles). SaaS usually dies for lack of distribution; here it ships with the product: eXp peer groups, Lafayette agent FB groups, content-led "watch me make this" proof, then brokerage/team bulk deals and referrals.

### Moat + top risks
**Moat stack (weakest→strongest):** content features (copyable) → **compliance discipline** (fair-housing/no-steer/no-fabricated-stats/human-approves — competitors won't bother, and "won't get your license pulled" is a real buying reason for licensed agents) → **attribution loop** (data-accreting, switching-cost) → **Carrie-as-distribution** (can't be bought). Deterministic-on-property (real photos, no generative hallucination) is both compliance shield and anti-slop signal.

**Top risks + mitigations:**
- **Feed access / ToS (highest):** the Realtor.com scrape is fragile and legally exposed. → Move to licensed MLS/IDX; restrict video to the agent's *own* listings (clean rights); start licensing paperwork now.
- **Platform automation ToS:** → never auto-post; generate + human-approve + official APIs only (already the design).
- **Fair-housing at scale:** → banned-phrase lists, no demographic targeting, per-state disclosure config, audit log.

**Single riskiest assumption:** that **Carrie converts from happy *user* to active *distributor*** — selling/referring *other* agents. Every GTM/moat claim rests on it; it's unproven at n=1, and an agent may resist arming competitors in her own farm area (so aim distribution at other regions/brokerages). De-risk this cheaply *before* writing more code.

### Do next
1. **Feed-access spike (this week):** can you reliably resolve a Realtor.com `fulfillment_id` per agent for a handful of design partners? In parallel, open the MLS/IDX licensing conversation — it's the long pole.
2. **Cheap distribution test:** have Carrie show the 30-sec video to 5–10 peer agents; treat **a second committed-to-pay agent** as the go/no-go for productizing — gate the build on pull, not product completeness.
3. **At the kickoff, lock the Phase-2/3 arrangement in one written sentence** so the "free favor" can't silently expand into an unpaid six-month engagement.