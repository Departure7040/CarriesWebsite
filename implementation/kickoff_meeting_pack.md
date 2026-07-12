# Kickoff Meeting Pack — July 24, 2026
**Brook DuBose + Carrie Billeaud · runsheet for the implementation kickoff**

Goal of this meeting: show her what's already been done, get 7 quick yes/no
decisions, get logged into the accounts we need together (so nothing sits in
her inbox as a follow-up), and leave with a signed/verbal deal memo covering
the 30-day foundation sprint.

---

## (a) Agenda — 45 minutes

| Time | Segment | What happens |
|---|---|---|
| 0:00–0:05 | **Wins tour** | Show the live demo (`carrie.dubose.me` or localhost) — GBP finding (185 reviews, 5.0, tops every nearby agent Google shows), the audit site, the mocked-up carriebilleaud.com concept. Set the tone: real assets, fixable gaps, not a doom-and-gloom pitch. |
| 0:05–0:25 | **The 7 decisions** | Walk section (b) below in order. Each has a recommendation — she just says yes/no/other. Target: under 3 min per decision. |
| 0:25–0:40 | **Access setup, together** | Do the phone taps live, side by side (section (c)). Don't leave any of this for "I'll send it later" — access delays are the #1 way a 30-day plan becomes a 90-day plan. |
| 0:40–0:45 | **Next steps + deal confirmation** | Confirm scope (section (d)), both sign/initial or verbally confirm, set the next check-in date. |

---

## (b) The 7 decisions

Bring a printed or on-screen copy of this section — the idea is she can say
"yes" to the recommendation and move on, or flag the ones she wants to think
about.

### 1. Canonical business name
**Recommend:** `Carrie Billeaud, Realtor`
Why: her GBP currently reads "Carrie Billeaud Realtor | Acadiana & Surrounding
Area | eXp Realty" — a keyword/area-decorated name that risks a Google policy
action. Google requires the real-world name used on signage/cards. This is
also decision #6 below (the GBP fix itself), so confirming the plain name now
unblocks that fix.
**Needs her call only if:** her actual signage/cards say something else
(e.g., "Carrie Billeaud Team"). Bring the field checklist photos if the
July 24 in-town verification (see `lafayette_field_checklist.md`) happens
before this meeting.

### 2. Canonical phone number
**Recommend:** `337-258-5379`
Why: 6-source majority (GBP, eXp agent page click-to-call, and others) plus
it's the number GBP itself shows. The outliers to retire: `337-522-7554`
(office/LoopNet) and `337-341-8976` (Homes.com).

### 3. Canonical address
**Needs her call — no confidant recommendation.** `3 Flagg Place Bldg B
Suite B-4, Lafayette LA 70508` matches GBP + Nextdoor + Facebook, which is a
real signal, but `1720 Kaliste Saloom Ste B-2` also appears in the wild. Ask
directly: "which office do you actually work out of / want shown publicly?"
If the July 24 field visit (checklist doc) confirms working signage at 3
Flagg Place, that's strong corroboration — bring the photo.

### 4. Canonical email
**Recommend:** pick one professional address (not the personal Gmail
currently used in blog signatures). Note for her: we found 3 emails
circulating. Whichever she picks, it should be the one on the contact form,
GBP, and every profile going forward.

### 5. Target client mix
No single recommendation — this drives content and page-brief priority.
Ask her to rank: buyers / sellers / first-time buyers / luxury / investors /
relocation. Even a rough gut-call ("70% sellers, mostly move-up buyers")
is enough to steer the next 60 days of content.

### 6. GBP name-fix approval + timing
**Recommend:** approve the fix, but sequence it carefully — one change at a
time, documented before/after, not bundled with other GBP edits in the same
week, to avoid tripping Google's spam-detection on rapid profile changes.
Confirm: does she want this done the week of the 24th, or held until after
manager access is fully sorted and tested on a smaller edit first (e.g., the
website link/UTM fix) to make sure access works cleanly?


### 7. Listing search at launch
**Recommend:** launch with a clean "Search homes" link out to your eXp search
(new tab), and add licensed IDX search on the site later only if the data says
it earns its cost (~$70/mo + setup). The demo's embedded search is a concept
preview, not the launch plan. **Needs her call only if:** she wants on-site
IDX from day one regardless.

---

## (b2) Operations questions

Added 2026-07-11 from `16_operations_and_lifecycle.md` — these decide the
post-acquisition plan (lead response, CRM, transaction workflow). Aim for
~5 minutes; rough answers are fine.

1. **Jake, Blake, Arrow** — who are they day-to-day, and does any of them
   take a new-lead handoff or drive a transaction today? (Zillow shows a
   4-person team; the ops plan differs completely if she's effectively solo.)
2. **Last web/social lead, walked through:** where did it land, who
   responded, how fast, and where is that person now?
3. **BoldTrail (kvCORE):** working database — past clients, close dates,
   active drips — or mostly an unused login? Open it together if possible
   (pairs with access item (c)3).
4. **SkySlope:** who drives it on her files, and roughly how many hours does
   contract-to-close admin take per deal?
5. **The 2pm-Tuesday test:** if a lead comes in while she's in a two-hour
   listing appointment, what happens right now — and is she open to an
   auto-text going out under her name within 60 seconds? (Speed-to-lead is
   the single most predictive conversion variable — MIT Lead Response study:
   contact odds drop ~100x between a 5- and 30-minute response.)
6. **Volume numbers:** closings per month this year, and new inquiries per
   month from all sources — sets real thresholds for the hire-a-TC /
   showing-partner / ISA triggers in `16_operations_and_lifecycle.md` §(e).

---

## (c) Access checklist — do this together, on her phone

Walk each of these live rather than emailing instructions — most failure
points are "which menu is that in," which disappears when you're both looking
at the screen.

**1. Google Business Profile — manager access**
Exact taps: Google Maps app → tap her profile photo/icon → **Business
Profile** → the pencil/settings icon → **Business Profile settings** →
**People and access** → **Add** → enter Brook's email → set role to
**Manager** (not Owner, unless she prefers) → send.
*(If she manages via the Google Business Profile app instead of Maps, the
same path exists under the profile's settings gear.)*

**2. GoDaddy — delegate access for carriebilleaud.com**
Login at godaddy.com → Account → **Delegate Access** → add Brook's email
with access to the domain. If she doesn't have the GoDaddy login handy,
this is the moment to find it (see `09_questions_for_client.md` Q20) —
don't leave the meeting without resolving who holds it.

**3. eXp / BoldTrail site editor**
Try: log into `kvcore`/BoldTrail dashboard together → confirm Brook can be
added as a collaborator/team member on the agent profile, OR confirm this
isn't possible and note the eXp/BoldTrail support-ticket path instead (see
`03_website_technical_audit.md` — several fixes, like robots.txt and
canonical tags, are platform-level and require a support ticket regardless
of agent-level access).

**4. GA4 / Google Search Console**
If she has them: add Brook as a user (Admin → Property Access Management for
GA4; Settings → Users and permissions for Search Console). If she doesn't
have them: create fresh, together, right now — takes about 10 minutes total
and nothing downstream (rankings, leads, content ROI) can be measured
without this.

**5. Meta Business access (or the firm's reporting)**
Frame this neutrally, not as an audit of the firm: **"so we can see what the
$3,000/month is producing in leads, not just views."** Ask for read-only
access to Meta Business Suite/Ads Manager for the business page directly, or
— if that feels like a bigger ask — start by requesting the firm forward
their last 2-3 reports (leads, cost per lead, cost per click). See
`10_facebook_reels_and_marketing_spend.md` for why this matters: the
business page's reel views are real but bimodal in a way consistent with
selective paid boosting, and views alone can't show whether the spend is
producing leads.

---

## (d) Deal memo skeleton

> Fill in and print/share before the meeting; leave signature lines blank
> for the meeting itself.

**Parties:** Brook DuBose (___) and Carrie Billeaud (___)

**Structure:** Services-for-trade. Research (see `research_notes.md` §1)
found buyer-side commission rebates ARE legal in Louisiana per AG Opinion
21-0030 (2021), provided the rebate is disclosed in writing (the Buyer
Representation Agreement is the natural vehicle) and, on a financed purchase,
appears as a credit on the Closing Disclosure — never off-the-books. The
even-simpler alternative remains a reduced listing fee if Carrie sells
Brook's current home. *Final wording after Carrie confirms with her eXp
broker at or before the meeting — research, not legal advice.*

**Scope — IN:**
- 30-day foundation sprint (per `07_30_60_90_day_plan.md` Days 1–30): GBP
  access + name-policy fix, canonical NAP rollout, bio + metadata fixes,
  robots.txt/canonical support ticket, GA4/Search Console setup, review
  system launch.
- carriebilleaud.com site build (per `production_site_plan.md`): de-demo,
  real hosting, launch.

**Scope — OUT (explicitly, a later conversation):**
- Ongoing content operations (blog/page cadence beyond the initial launch
  set).
- Ad management / paid spend decisions (including anything related to the
  $3,000/month firm).
- 24/7 support or maintenance retainer.

**Date:** ___________  **Next check-in:** ___________

**Signatures / initials:**
Brook: ___________  Carrie: ___________

---

## (e) Bring to the meeting

**Brook brings:**
- Laptop with the live demo loaded (and a offline/localhost fallback if wifi
  is bad — `python server.py 8091` per `site/SERVING.md`).
- Printed copy of the 6 decisions (section (b)) and the deal memo skeleton.
- `09_questions_for_client.md` in case any of the 16 questions come up
  unprompted.
- A notes doc/laptop open to log the before/after of any GBP edit made live.

**Carrie brings:**
- Phone, logged into Google (for GBP), and unlocked.
- GoDaddy login (or knowledge of who has it).
- eXp/BoldTrail dashboard login.
- Any existing CRM/lead-source notes (rough where-leads-come-from
  percentages — Q14 in `09_questions_for_client.md`).
- A gut answer on target client mix (decision #5) — doesn't need to be
  precise, just directional. NOTE (2026-07-11): Carrie volunteered that she's
  working with Acadiana Home Builders to push luxury listings and custom-build
  buyers — luxury/new-construction likely belongs at the top of the mix.
- **Acadiana Home Builders partnership details** (new, from her 7/11 text):
  what the arrangement includes (listing their specs? buyer referrals?
  co-marketing?), whether it's exclusive, whether we can name them + use
  their photos/listings on her site, and whether a builder co-marketing
  budget exists. This gates a dedicated new-construction/custom-build page
  that would be genuinely unique content.
- **Closed transactions by city, last 3 years** (a CRM/MLS export or even a
  hand list). This decides which expansion markets get pages next (Duson,
  Rayne, Breaux Bridge, St. Martinville, New Iberia, Abbeville…): the rule is
  real deals + something locally true to say + thin competition — all three
  or no page.
