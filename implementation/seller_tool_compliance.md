# Seller tool ("Thinking of Selling?") — compliance record

The interactive seller tool at `site/tools/thinking-of-selling/` is a lead magnet for a
LICENSED agent — the seller-side mirror of the buyer readiness tool. This documents why
it's on the right side of the law. Designed via a 5-agent workflow (net-proceeds math,
LA seller closing costs, pricing education, prep checklist, guardrail spec), assembled
with guardrails baked in.

## The core rule: NO fabricated home value / NO AVM
The single biggest compliance (and trust) difference from the "what's my home worth?"
widgets sold to agents: **the tool never generates a home value.** The seller supplies
their *own* sample sale price; the tool does honest net-proceeds math on *that* number.
The valuation itself is explicitly routed to Carrie's human CMA. This avoids presenting an
unverified/fabricated value as fact and is stated on-page as the honest differentiator.

## The other pillars (same as the buyer tool)
- **Educational estimates only** — every figure labeled estimate; "your real number comes
  from a CMA and your closing statement." No guaranteed net, no guaranteed sale price.
- **Commission stated as negotiable** — "fully negotiable and not set by law in Louisiana"
  (adjustable input); post-2024-NAR-settlement note that buyer-agent comp is separate.
- **RESPA** — no steering to a specific title company, attorney, notary, stager,
  photographer, contractor, mover, or lender; "get quotes from a few."
- **Fair Housing** — never profiles *who will buy* the home; no "type of buyer," schools,
  safety, or demographics. Any market context is objective (price/DOM/inventory), behind a
  fair-housing bar.
- **Privacy** — mortgage balance, sample price, and all net math compute client-side and are
  never stored/sent. Only contact + a coarse seller summary (price band, timeline, reason)
  is captured, after opt-in consent (unchecked by default). Usable without contact info.
- **No legal/tax advice** — capital-gains, 1031, and divorce/probate/succession/estate sales
  route to a CPA/attorney. Homestead exemption is flagged as the *buyer's* future benefit,
  not part of the seller's proceeds (prevents a common misconception).
- **Louisiana specifics as education** — no statewide transfer tax, notary/attorney act of
  sale (no escrow), taxes billed in arrears (seller prorates to the buyer), required
  Residential Property Disclosure + flood disclosure — all "confirm with a licensed pro."

## Red lines (never cross)
Never output an automated value / AVM; never use any price but the seller's own; never
present a figure as a guarantee/appraisal; never store or transmit mortgage balance/price/net;
never capture without opt-in consent or include financials in the payload; never gate the
tool behind contact info; never steer to a paid vendor; never profile the likely buyer or use
protected-class/schools/safety/demographics; never give legal/tax advice; never imply payoff =
balance or that commissions are fixed/set by law.

Verified end-to-end via Playwright: net math correct ($285K − commission/closing/tax/payoff),
8 price-driver blocks, 10 cost items, 13 checklist steps, consent gates the send button.
