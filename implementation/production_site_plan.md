# Production Site Plan — carriebilleaud.com
**Demo → production plan.** Source demo lives at `site/` (served per
`site/SERVING.md`, currently tunneled to `carrie.dubose.me`). This document
plans the path from "private demo behind noindex" to "carriebilleaud.com,
live and indexable, replacing the current GoDaddy redirect to
`carriebilleaud.exprealty.com`."

Decisions needed are marked **[DECISION NEEDED]** throughout — surface these
at or before the July 24 kickoff.

---

## Architecture options

### Option A — Keep static, enhance with an IDX vendor embed (recommended)
Keep the current hand-built static site (HTML/CSS/vanilla JS, per
`site/index.html`) and swap the demo's Realtor.com-scrape listings proxy for
a licensed IDX vendor's embed/widget (see punch-list item below). Add a
lightweight serverless backend (Cloudflare Workers) only for what actually
needs one: the listings proxy (if still needed) and the contact form.

**Why recommended:** the demo is already built, styled, and content-complete
enough to launch fast. A framework rebuild re-does work that's already done
for no clear near-term benefit, and the 30-day sprint timeline (per
`07_30_60_90_day_plan.md`) doesn't leave room for a rebuild. Static sites are
also trivially fast, cheap to host, and easy for Brook to maintain solo.

**Rough Brook-time:** 8–14 hours to de-demo + wire up real services (see
punch list), assuming Option A.

### Option B — Framework rebuild (Next.js/Astro or similar)
Rebuild on a modern framework for better long-term maintainability, built-in
image optimization, and easier component reuse across area pages.

**Why not now:** meaningfully more Brook-time (est. 25–40+ hours before
reaching current demo's feature parity), no functional advantage a static
site + Workers can't also deliver for a single-agent site at this scale,
and it delays the launch that's supposed to happen inside the 30-day window.
**[DECISION NEEDED]** — worth revisiting only if Carrie wants a
team/multi-agent site later (Phase 3 team branding, per
`04_competitor_gap_analysis.md`) where a framework's component reuse starts
to pay off.

**Recommendation: Option A.**

---

## The de-demo punch list

Ordered roughly launch-sequence; items don't all block each other, but the
robots/noindex item must be **last**, not first.

| # | Item | Detail | Est. Brook-time |
|---|---|---|---|
| 1 | **Remove noindex + robots block — LAST, at launch only** | `site/robots.txt` currently `Disallow: /` sitewide; `index.html` carries `<meta name="robots" content="noindex, nofollow">`. Per `site/SERVING.md`, this is intentional — the demo must not compete with Carrie's real entity in search until it *is* the real entity. Flip both only once every other item below is done and DNS has cut over. | 15 min |
| 2 | **Remove demo banners / sample tags** | Strip the `<div class="demo-banner">Demo concept — part of your SEO audit...</div>`, the `(demo only)` submit button label, "Demo placeholders" open-house copy, and the "sample date" tags on open houses (`index.html` lines ~25, 262–280, 388). Replace open-house dates with a real sync source or a clearly-labeled "call for current open houses" fallback. | 1–2 hrs |
| 3 | **Reviewer permission confirmations** | The 3 Google review quotes on the page (Annalise D., Amy L., Dominick C. — `index.html` ~296–307) are real reviews pulled from her live GBP. The page itself says "before a production launch we'd confirm reviewer permission with you" — do that confirmation with Carrie before launch; drop any review she can't confirm permission for. **[DECISION NEEDED: Carrie confirms which reviewers she's comfortable naming/quoting publicly.]** | 30 min (+ Carrie's time) |
| 4 | **Canonical NAP inserted everywhere** | Once the kickoff's 6 decisions (name/phone/address/email) are locked, replace every instance sitewide — header, footer, schema, contact section, tel: links. Current demo already uses 337-258-5379 and 185/29 review counts; verify address field once decided. | 1 hr |
| 5 | **Wire the contact form to her real email/CRM + spam protection** | Current form is decorative (`Send (demo only)`). Needs: a real submit target (her CRM if one exists — `09_questions_for_client.md` Q15 — or a plain email forward as a fallback), and spam protection (Cloudflare Turnstile is the natural fit given Option A's Cloudflare hosting, and matches what her eXp site already uses per `03_website_technical_audit.md`). | 2–3 hrs |
| 6 | **Replace the Realtor.com scrape feed with licensed IDX** | Current `server.py` proxies Carrie's public Realtor.com agent-listings GraphQL query — fine for a private demo, not appropriate/licensed for production (scraping a competitor portal's data for a live public site is a real legal/ToS exposure, distinct from her own MLS-licensed data). **[DECISION NEEDED — options to research further before the 24th or shortly after; placeholder below, not a final recommendation:]**<br>— *Option 1:* IDX Broker or similar third-party IDX widget/embed, licensed through her MLS (Realtor Association of Acadiana / Gulf South REALTORS MLS) — standard, vendor handles compliance, recurring vendor fee.<br>— *Option 2:* Ask eXp/BoldTrail whether the same feed powering `carriebilleaud.exprealty.com`'s IDX pages can be embedded/iframed on carriebilleaud.com — no new vendor, but adds a platform dependency.<br>— *Option 3:* Direct MLS RETS/RESO Web API feed if her MLS supports self-service access — more setup work, most control.<br>*Research needed on cost + her MLS's specific vendor options before this is a real recommendation.* | 4–8 hrs (once vendor chosen) + research time |
| 7 | **Real hosting** | Move off the home-server + Cloudflare tunnel setup (`site/SERVING.md`'s current live config: `server.py` on a home machine, `2cajuns` tunnel to `carrie.dubose.me`) — fine for a demo, not durable for a client's live site (single point of failure = Brook's PC/network). **Recommend: Cloudflare Pages** for the static site + **Cloudflare Workers** for the listings proxy (if still needed after IDX vendor decision) and the contact-form endpoint. Free tier covers this traffic level; no home-server dependency; same DNS provider ecosystem simplifies the cutover below. | 2–3 hrs |
| 8 | **DNS cutover from GoDaddy redirect** | `carriebilleaud.com` currently 301-redirects to `carriebilleaud.exprealty.com` (GoDaddy-managed, per `04_competitor_gap_analysis.md` addendum). Steps: (1) confirm GoDaddy delegate/access secured at kickoff, (2) if hosting on Cloudflare Pages, add the domain to Cloudflare and update GoDaddy nameservers or just the relevant A/CNAME records, (3) remove the redirect rule, (4) verify SSL provisions correctly before pointing live traffic, (5) keep the eXp site live in parallel — don't let carriebilleaud.com become the *only* place her business appears until the new site is fully verified. | 1–2 hrs + propagation wait |
| 9 | **Launch-day SEO checklist** | (a) Submit to Google Search Console (new property + sitemap) once domain is live and indexable. (b) Validate schema — the page already has `AggregateRating` JSON-LD (185 reviews/5.0); re-check it against Google's review-snippet markup rules now that it's a live indexable page, not a private demo (the code comment at `index.html` line 20-22 already flags this). (c) Confirm 301 redirects are set up correctly in reverse if needed (e.g., decide whether `carriebilleaud.exprealty.com` should canonical-link to the new site, or vice versa, to avoid duplicate-content signals across her own two properties). | 1–2 hrs |

**Total rough estimate: 12–20 Brook-hours**, not counting IDX vendor
research/setup time or DNS propagation wait, and assuming Option A.

---

## Open decisions summary

- **[DECISION NEEDED]** Option A vs B (recommend A — assumed throughout this
  plan unless overridden).
- **[DECISION NEEDED]** Which Google reviewers Carrie will confirm for public
  use on the site.
- **[DECISION NEEDED]** Canonical NAP values (flows from kickoff decisions
  1–4).
- **[DECISION NEEDED]** IDX vendor/path — needs short research pass before
  committing; three options sketched above, none confirmed.
- **[DECISION NEEDED]** Sequencing of eXp site vs. new site once
  carriebilleaud.com goes live — keep both indexed, or canonical one to the
  other?

---

## Status update — 2026-07-11

The content build is DONE ahead of schedule: 18 pages live on the demo
(home + 7 area pages + 4 service pages + 6 sourced guides), dropdown nav,
live listings feed (demo proxy), footer socials, slim location-first heroes.
Remaining "stand it up" work only:

**Gated on Carrie (kickoff meeting):** GoDaddy access; canonical NAP answers;
bio + sample-mark sign-offs; reviewer permissions (3 Google quotes); MLS/IDX
authorization; lead-delivery email/CRM choice; AHB partnership permissions
(new-construction page).

**Brook, post-access (~8–12h):** Cloudflare Pages migration + Worker replacing
server.py's /api/listings proxy; licensed IDX swap (feed + on-site search);
form wiring + spam protection; de-demo pass (banners, sample marks, noindex
OFF LAST, robots.txt open, sitemap -> GSC); pre-change GBP baselines.

## Refinements adopted from the independent code review (2026-07-11)

1. **Staged launch set:** launch with 8–12 fully-approved pages (seller funnel:
   sell-my-house + listing-agent; areas: Lafayette, Youngsville, Broussard;
   corrected guides: flood, homestead, closing; testimonials + home). Every
   other page stays noindex until its facts pass Carrie's sign-off — rolling
   approval, not one big gate. Milton and remaining pages join as approved.
2. **IDX is a justified-later decision, not a launch gate:** at launch, listing
   search = clear new-tab link to her eXp search; the Realtor.com demo proxy
   NEVER ships to production. Licensed IDX (~$70/mo + build) gets adopted only
   when conversion data or listing-SEO goals justify it. (Kickoff decision #7.)
3. **Deterministic publish artifact:** production deploys from a generated
   allowlisted dist/ (marketing pages only) — never the raw site/ directory.
   Audit stays on the demo host, which remains temporary and demo-only
   (Cloudflare Access explicitly declined by Brook — accepted risk, CR-001).
4. **Editorial ops:** every financial/legal/market page gets an owner, primary
   sources, a visible reviewed-on date, and a refresh schedule at launch.
5. **Launch acceptance criteria:** adopt the code review's verification suite
   (reports/14_code_review_findings.md — crawl checks, canonical/redirect
   tests, forbidden-path assertions, form-flow tests) as the launch checklist.
