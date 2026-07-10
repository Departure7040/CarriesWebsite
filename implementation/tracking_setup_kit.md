# Tracking Setup Kit — GA4, Search Console, GBP Baseline, UTM Links

**Prepared for:** Carrie Billeaud
**Prepared:** 2026-07-09
**Sources:** `/reports/03_website_technical_audit.md` (platform limits), `/reports/02_local_seo_audit.md` (GBP checklist), `/data/public_assets.yaml` (domain/GBP findings)

---

## 1. GA4 Property Setup

Carrie currently has two relevant properties to track, at different stages of readiness:

- **Current site:** `https://carriebilleaud.exprealty.com` (live now, BoldTrail-hosted)
- **Future site:** `https://carriebilleaud.com` (domain already owned since 2021-12-14, currently just 301-redirects to the eXp site — see `data/public_assets.yaml`)

### Step-by-step

1. **Create the GA4 account/property now, even before carriebilleaud.com is built out.** Go to [analytics.google.com](https://analytics.google.com) > Admin > Create Account. Name the account "Carrie Billeaud Realtor" (or match whatever canonical name is chosen in `nap_fix_runbook.csv`).
2. **Create one GA4 property named for the brand, not the domain** (e.g. "Carrie Billeaud — Real Estate"), so it survives the eventual migration from the eXp subdomain to carriebilleaud.com without losing historical continuity in the account structure.
3. **Add a data stream for `carriebilleaud.exprealty.com` first** (Web stream). This gets you a Measurement ID (`G-XXXXXXX`) and the GA4 tag snippet.
4. **Platform limit — read before attempting installation:** Per `reports/03_website_technical_audit.md`, this site is a locked BoldTrail/kvCORE template. There is currently **no confirmed way for Carrie to self-inject a `<head>` script** (the same category of limitation that blocks fixing canonical tags and meta-robots — see `exp_support_ticket_draft.md`). Before spending time hunting for a "custom tracking code" field in the BoldTrail dashboard:
   - Check the BoldTrail/kvCORE agent dashboard for a "Google Analytics," "Tracking Code," or "Custom Scripts" field under Website Settings first — some IDX platforms do expose this even when canonical/robots.txt are locked.
   - If no such field exists, file a support request (can be added as a 5th item alongside the four tickets in `exp_support_ticket_draft.md`) asking BoldTrail support to confirm whether GA4 (or GTM container) injection is agent-configurable, and if not, whether they can install the Measurement ID for you.
   - **Do not treat "no GA4 on the eXp site" as a blocker for launching everything else** — GBP Insights (Section 3 below) and UTM-tagged links (Section 4) still give usable traffic-source data even without GA4 fully wired up.
5. **Add a second data stream for `carriebilleaud.com`** now, even though the domain currently just redirects. This means the property and stream both exist and are ready the moment the site build-out happens — no lost setup time later. Note in the stream name that it's "pending build-out."
6. **Link Google Search Console to the GA4 property** (Admin > Property > Search Console Links) once Search Console verification (Section 2) is complete for either domain — this pulls organic search query data directly into GA4 reporting.
7. **Set retention to 14 months** (Admin > Data Settings > Data Retention) — GA4 defaults to 2 months for some report types, which is too short for a real-estate sales-cycle business with long consideration windows.

---

## 2. Search Console Verification — Ranked by Feasibility

Two separate properties are needed (Search Console verification is domain/subdomain-specific and doesn't transfer).

### For `carriebilleaud.exprealty.com` (current site — platform-locked)

| Rank | Method | Feasibility | Notes |
|---|---|---|---|
| 1 | **HTML meta tag** | Medium — depends on whether BoldTrail exposes a page-`<head>` custom field | Same dependency as the GA4 tag (Section 1, step 4). If a custom-head-code field exists, this is the fastest option. |
| 2 | **Google Analytics verification** | Medium — depends on GA4 being successfully installed first (Section 1) | Once GA4 is live and Carrie has Edit access on the property, GSC can auto-verify through the existing GA4 tag with no separate file/DNS step. |
| 3 | **Google Tag Manager verification** | Low-Medium | Only usable if GTM container injection is also possible on this platform — ask about this alongside the GA4 request in the same support ticket to avoid a second round-trip. |
| 4 | **HTML file upload** | Low | Requires uploading a verification file to the site's root directory — not available on a hosted/managed platform like BoldTrail without file-system access, which agents don't have. |
| 5 | **DNS TXT record** | Not feasible | DNS for `exprealty.com` (and its subdomains) is controlled by eXp corporate, not Carrie. She cannot add a TXT record here. |

### For `carriebilleaud.com` (future site — Carrie owns the domain outright)

| Rank | Method | Feasibility | Notes |
|---|---|---|---|
| 1 | **DNS TXT record** | High | Carrie owns this domain via GoDaddy (registered 2021-12-14, confirmed in `data/public_assets.yaml`). She has full DNS control, so this is the most reliable, "set once and never re-verify" method — recommended default. |
| 2 | **HTML file upload** | High, once site is built | Fully available once a real hosting environment (not just a redirect) exists — upload the verification file to site root. |
| 3 | **HTML meta tag** | High, once site is built | Equally available once she controls the site's `<head>`; either this or DNS TXT is fine — DNS TXT is preferred because it survives a full site rebuild/re-platform. |
| 4 | **Google Analytics verification** | High, once GA4 stream is live on this domain | Convenient secondary option once Section 1's carriebilleaud.com stream is actually receiving traffic. |

**Recommendation:** Verify `carriebilleaud.com` via DNS TXT immediately — this can be done today regardless of whether the site is built yet, and it never needs to be redone. Verify `carriebilleaud.exprealty.com` opportunistically, contingent on the platform-limit questions raised in Section 1.

---

## 3. GBP Performance Metrics — Monthly Snapshot

**Capture the baseline BEFORE any changes are made — do this at the kickoff meeting, before touching the GBP name, address, phone, website link, or any other field in `nap_fix_runbook.csv`.** The GBP name-policy fix in particular (Section (b)(1) of `reports/02_local_seo_audit.md`) can trigger a re-verification review or a temporary visibility dip; without a documented "before" state, it will be impossible to tell whether any post-change metric movement was caused by the fix or was already happening.

### Baseline capture procedure (kickoff meeting, before any edits)

1. Open Google Business Profile Manager, go to the Performance/Insights tab, set the date range to the trailing 28 days (or the longest available window).
2. Screenshot every metric listed below.
3. Record the numbers in a simple tracking sheet (date-stamped) — this document doesn't need to contain the sheet itself, just note where it lives once created (e.g. a shared spreadsheet).
4. Repeat this exact capture monthly, same day of month, same date range length, so comparisons are apples-to-apples.

### Metrics to capture every month

| Metric | Why it matters |
|---|---|
| Total profile views (Search vs. Maps split) | Core visibility trend; also watch for a dip right after the name-policy edit |
| Search queries used to find the profile (Direct / Discovery / Branded breakdown) | Discovery-query growth signals relevance improvements from category/services/description work |
| Website clicks | Direct outcome of Section 4's UTM-tagged website link — cross-check against GA4 once linked |
| Call clicks (click-to-call) | Primary conversion metric for a solo agent |
| Direction requests | Relevant if storefront/pin address stays public per the SAB-vs-storefront decision |
| Booking clicks (Calendly link) | Cross-check against Section 4's Calendly UTM link |
| Photo views | Should trend up with the photo cadence plan in report 02 Section (b)(10) |
| Review count and average rating | Currently 185 reviews / 5.0 — track month-over-month net new reviews against the 2–4/month target in report 02 Section (d) |
| Q&A count and content | Watch for spam questions appearing; confirm seeded Q&A (report 02 Section (b)(11)) stays visible |
| Post views / engagement (if available) | Validates the sustain-cadence recommendation in report 02's live-profile addendum |
| Nearby-competitor review counts (from the "Similar profiles" or search comparison, where visible) | Baseline recorded 2026-07-08: Blake Arceneaux & Team 98, Brandy Smith 77, Nick Hundley 71, Kathy Leger 4, Beau Thomas 2 vs. Carrie's 185 — recheck monthly to confirm the lead is holding/growing |

---

## 4. UTM Link Table

**Convention:** `utm_source` = the platform the link lives on · `utm_medium` = `organic` (Google-surfaced placements: GBP) or `profile` (social bio/link-in-bio placements) · `utm_campaign` = `gbp`, `social`, or `reviews`. All links use the current live domain (`carriebilleaud.exprealty.com`); swap the base domain to `carriebilleaud.com` once the build-out decision is made and re-issue this table with the same parameters.

| Placement | Ready-to-paste URL |
|---|---|
| GBP website link | `https://carriebilleaud.exprealty.com/?utm_source=google&utm_medium=organic&utm_campaign=gbp&utm_content=profile_link` |
| GBP appointment/Calendly link | `{CALENDLY_URL}?utm_source=google&utm_medium=organic&utm_campaign=gbp&utm_content=booking_link` |
| Instagram bio | `https://carriebilleaud.exprealty.com/?utm_source=instagram&utm_medium=profile&utm_campaign=social&utm_content=bio_link` |
| Facebook business page (Links section) | `https://carriebilleaud.exprealty.com/?utm_source=facebook&utm_medium=profile&utm_campaign=social&utm_content=page_link` |
| TikTok bio | `https://carriebilleaud.exprealty.com/?utm_source=tiktok&utm_medium=profile&utm_campaign=social&utm_content=bio_link` |
| Threads bio | `https://carriebilleaud.exprealty.com/?utm_source=threads&utm_medium=profile&utm_campaign=social&utm_content=bio_link` |
| Review-request message — SMS/text | `{GOOGLE_REVIEW_LINK}?utm_source=sms&utm_medium=organic&utm_campaign=reviews&utm_content=text_request` |
| Review-request message — Email | `{GOOGLE_REVIEW_LINK}?utm_source=email&utm_medium=organic&utm_campaign=reviews&utm_content=email_request` |

**Notes:**
- `{CALENDLY_URL}` and `{GOOGLE_REVIEW_LINK}` are placeholders — insert Carrie's actual Calendly URL (visible on the live GBP per `data/public_assets.yaml`) and her direct Google review shortlink before use.
- Note that Google strips some UTM parameters from GBP fields in certain surfaces; verify the tagged link survives by clicking through from the live profile after saving, and re-check after any GBP edit.
- Once GA4 is linked (Section 1) and Search Console is verified (Section 2), these `utm_campaign` values (`gbp`, `social`, `reviews`) become the default breakdown for traffic-source reporting — keep the convention identical for any future links added outside this table (e.g. new GBP posts per report 02 Section (b)(12): `utm_campaign=gbp&utm_content=post_<topic>_<yyyy_mm>`).
