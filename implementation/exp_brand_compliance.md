# eXp / LREC / NAR marketing-compliance reference

Source of truth for what Carrie's public marketing site must satisfy. Compiled 2026-07-17
from eXp's Brand & Marketing Toolkit (exptoolkit.com/brand — JS-rendered; logo/color/font
specs + approval workflow; detailed guidelines live in a Canva deck that is login-gated),
the **LREC Advertising Guidelines Checklist** (Louisiana Real Estate Commission, Ch. 25 /
Ch. 19), and NAR's Membership Marks Manual. Items sourced from secondary pages are flagged
`[verify]`.

## Required disclosures (every ad / every website page)
- **Broker identification** — the sponsoring/qualifying **broker's full name AND telephone
  number**, conspicuous, in every advertisement (LREC Ch.25 §2501(F)). **← the current launch
  blocker: broker name/phone are still unknown (`__FILL__`).**
- **Website / social / email** — every website page (and the first & last page of commercial
  email / social) must show: the salesperson's name; the broker/trade name on the license
  (**eXp Realty**); the **city + state** of the broker's main/branch office; and the
  **jurisdiction(s)** where the broker is licensed (**Louisiana**) (LREC §2515).
- **eXp brokerage disclosure** — identify eXp Realty as the brokerage on personal/team-branded
  materials ("Brokered by eXp Realty" or the eXp Brokered-By logo). `[verify exact phrasing]`
- **Print dating** — brochures/flyers/pamphlets must state month + year printed (§2507). (N/A to
  the website; relevant if we make print assets.)

**Site disclosure block now applied to every public page footer:**
`Licensed by the Louisiana Real Estate Commission · Brokered by eXp Realty · Broker of record: <broker name, phone>`
(the demo shows "to be confirmed at launch"; the production build injects broker name/phone).

## Naming, team, and REALTOR®
- **Name** — advertise under the licensee's LREC-registered name (no unregistered nicknames,
  §2501(D)): "Carrie Billeaud". Canonical business name: "Carrie Billeaud, Realtor".
- **Teams** (LREC §1909) — a team name may be used ONLY with the sponsoring broker's **written
  approval**, must not imply the team/agent is the responsible broker, and may only advertise
  members who are **actually licensed**. → **"Elite Home Team" is a loose affiliation; do NOT
  present a formal team.** (This is why the sitewide "team of 4" claim was removed — it was both
  unapproved-as-advertised and inaccurate = misleading advertising under §2505.)
- **REALTOR®** (NAR) — ALL CAPS + ® , punctuation-separated from the name, used *with* but not
  *as part of* a firm name; only NAR members may use it; lowercase allowed only in domains/
  usernames. Standardize Carrie's own copy on "REALTOR®"; leave lowercase inside review quotes.

## Prohibited / accuracy
- **No false/misleading/inaccurate advertising** (§2505; La. R.S. 37:1455(A)(35)). Avoid
  unsubstantiated "#1" / "best" / guarantee claims.
- **Production stats** (174 sales / $44.6M / 11 yrs / 50+ families / 3× ICON) are **client-
  provided and unaudited** — client-approved for use, but keep them out of unqualified superlative
  framing; present as Carrie's own figures.
- **Association/membership** names only if she's a member (§2505; §1909(B)(1)) — RAA membership
  confirmed.
- **Self-serving review markup** — an agent may not mark up their own reviews/rating for Google
  star snippets. `aggregateRating` + self-referential `Review` JSON-LD removed sitewide (matches
  CR-009). Follow-up: `build/reviews/build_reviews.py` must stop emitting the per-review JSON-LD,
  or it will re-add it on the next run.
- **Owner/licensed-agent** disclosure if Carrie has an interest in an advertised property (§2511).
- **Rebates/incentives** are restricted under La. R.S. 37:1446 — confirm allowance + disclosure
  with the broker before offering (ties to Brook's buyer-rebate trade structure).

## eXp brand assets (for any branded graphic/video)
- **Logo**: approved eXp logos only, **black (#000000) or white (#FFFFFF)** only; no gradient,
  stroke/outline, drop shadow, distortion, rotation, or element removal. Co-branding: agent logo
  same size as the Brokered-By logo `[verify]`. Custom/co-branded/large-print assets need **State
  Broker approval** before use.
- **Fonts**: Manrope (headlines), Roboto (body). **Palette**: black, Charcoal Blue #31303F, Dark
  Navy #0C0F24, Slate Blue #506CAA, greys, white. *(Note: our listing graphics/videos use a
  charcoal/ivory/gold luxury palette + Playfair — that's Carrie's personal brand, allowed as long
  as the eXp brokerage is disclosed and any eXp logo used follows the black/white rule. Confirm
  the co-brand lockup with the broker before launch.)*

## Approvals & enforcement
- **All ads must be broker-approved before placement** (§2501(B)). eXp routes custom/co-branded/
  large-print materials to the State Broker; brand questions to expertcare@exprealty.net or
  marketing@exprealty.net for regulatory review.
- **Penalties** escalate ($250 → $500 → $1,500), and repeat violations require **both the agent
  AND the sponsoring broker** to appear before the Commission — i.e. compliance protects Carrie's
  broker relationship, not just her.

## Sources
exptoolkit.com/brand (JS-rendered); eXp Brand Guidelines Canva deck (login-gated, logo rules
pp.4-9); LREC Advertising Guidelines Checklist (Ch.25 §§2501-2515, Ch.19 §1909); NAR Membership
Marks Manual. `[verify]` items: exact eXp brokered-by phrasing; co-brand sizing; franchise line
(§2509 likely N/A — eXp is a single national brokerage, not a franchise — confirm with LA broker).

## Launch-gate status (2026-07-17)
- ✅ eXp brokerage identity present sitewide; ✅ canonical NAP; ✅ team-of-4 removed; ✅ agg.rating
  removed; ✅ jurisdiction + brokered-by footer added.
- ⛔ **BLOCKER:** broker legal name + broker phone (fill at kickoff → production build injects into
  the footer disclosure). Do not remove `noindex` until present.
