# Home-Readiness tool — compliance record

The interactive **"Am I Ready to Buy in Acadiana?"** tool at `site/tools/home-readiness/`
is a lead magnet for a LICENSED agent. This documents why it stays on the right side of
the law, so a broker review has an answer on file. Designed via workflow (5 parallel
agents: affordability math, LA closing costs, checklist, compliant area-match, guardrail
spec) then assembled with the guardrails baked in.

## The five pillars
1. **Educational estimates only — no lending behavior.** Never quotes a mortgage rate
   (the rate inputs are labeled "illustrative sample, not a quote"), never says "you're
   approved for $X" (uses "buyers in a similar spot often shop around $X–$Y"), no
   application intake, no pass/fail lending gate. Keeps Carrie clear of SAFE Act / loan-
   originator triggers. The readiness score is explicitly a self-assessment, not credit-
   worthiness or qualification.
2. **RESPA — no vendor steering.** Never names or links a specific paid lender, inspector,
   insurer, or title company; says "get quotes from a few." (Deliberately avoids the
   existing mortgage calculator's "preferred lenders" link, which the review flagged.)
3. **Fair Housing — the area match uses ONLY objective, buyer-entered criteria** (budget,
   new-vs-established, commute to a place the buyer picks, lot size, property type). It
   never uses or mentions schools, safety/crime, "family-friendly," demographics, or who
   lives anywhere — deliberately excluding the demographic attributes that exist in the
   site's own `which-town-fits.html` guide. Framed as "towns that fit your budget and
   criteria," never "right for people like you." No town is hidden — only ranked.
4. **Privacy — financial inputs never leave the browser.** Income/debts/cash and all
   affordability math run client-side; nothing financial is stored, logged, put in the
   URL, or sent. The tool is fully usable without entering contact info. Only contact +
   a coarse readiness summary (budget band, timeline, readiness tier, area preference) is
   captured, and only after an explicit opt-in consent checkbox (unchecked by default).
5. **No fabrication.** Every cost is a labeled range with a stated reason it varies; town
   price positions are labeled mid-2026 estimates to verify against current listings.

## Where the guardrails live in the page
- Persistent `.legal-bar` disclaimers: top of page, inside the area-match module, and full
  fine-print at the bottom (real on-screen text, shown before and around results).
- Rate inputs carry an "illustrative — not a quote" tag; results carry "estimate" tags.
- Consent checkbox gates the send button (`disabled` until checked); the consent text
  states financial inputs are computed locally and not sent.
- Area-match scoring (`TOWNS` + scorer) contains only objective attributes; a code comment
  and the fair-housing bar document the ban list.

## Red lines (never cross)
No rate/APR quote; no "approved/qualified for $X"; no loan-origination behavior; readiness
score ≠ credit score; no paid-vendor steering; no schools/safety/crime/"family-friendly"/
demographics in inputs, logic, copy, or the captured summary; never store/transmit income
or debts; no capture without opt-in consent; no invented exact figure as fact; never assert
a specific buyer/property IS eligible for USDA/homestead/any program; no legal or tax advice.

Louisiana specifics (attorney/notary act-of-sale, no statewide transfer tax, flood-by-zone,
homestead exemption as future savings, USDA rural zero-down) are surfaced as education and
cross-linked to the existing guide pages, always "confirm with the appropriate licensed
professional."
