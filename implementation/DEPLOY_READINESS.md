# DEPLOY READINESS — carriebilleaud.com

**This is the go-live gate.** No production launch happens until every box in
Sections A, B, and C is checked in order. The single most dangerous step in this
whole document is **C-7 (flip `strip_noindex`)** — read the boxed warning there
before you touch anything.

- **Source of truth:** `build/production.config.json` (tokens + flags) and
  `build/page_manifest.json` (which pages publish). The build FAILS LOUDLY if any
  published page still carries a `__FILL__` value — that refusal is a feature.
- **Build tool:** `python build/build.py --check` (validate, no writes) and
  `python build/build.py` (write `dist/`).
- **Launch-gate register:** `reports/14_code_review_findings.md`.
- **Plan of record:** `implementation/production_site_plan.md`.
- **DNS specifics:** `implementation/carriebilleaud_com_dns_cutover.md`.

**Gate count: 12 blanks to fill · 4 compliance gates · 7 deploy steps.**

---

## A. BLANKS TO FILL — the `__FILL__` tokens in `production.config.json`

Every token below is `__FILL__` today. The build will not emit a page that
contains one, so all 12 must be resolved before Step C-2 can succeed. "Who
provides" is the person who owns the answer, not who types it in.

### A1. NAP (canonical name / address / phone) — 6 tokens
Flows from Kickoff decisions #1–#4 (`kickoff_meeting_pack.md` §b).

- [ ] `business_name` — exact licensed trade name (CR-003). **Who:** Carrie (kickoff #1; recommend `Carrie Billeaud, Realtor`).
- [ ] `phone` — visible display NAP, e.g. `337-258-5379`. **Who:** Carrie (kickoff #2).
- [ ] `phone_tel` — digits-only for `tel:` hrefs, e.g. `3372585379`. **Who:** Brook (derived from `phone`).
- [ ] `address` — canonical office/mailing address. **Who:** Carrie (kickoff #3 — no default; 3 Flagg Place vs 1720 Kaliste Saloom vs 100 Goodwood Circle unresolved).
- [ ] `email` — public contact email (not the personal Gmail). **Who:** Carrie (kickoff #4).
- [ ] `license_number` — Carrie's LREC license number (CR-003). **Who:** Carrie / broker.

### A2. Broker disclosures (LREC CR-003) — 3 tokens
`broker_jurisdiction` is pre-filled; confirm its wording with the broker but it
is not a blank.

- [ ] `broker_name` — sponsoring/qualifying broker legal name. **Who:** eXp sponsoring broker.
- [ ] `broker_phone` — broker-OWNED telephone (LREC requires it conspicuously). **Who:** eXp sponsoring broker.
- [ ] `broker_office` — broker office city/state. **Who:** eXp sponsoring broker.

### A3. Analytics / Search Console — 2 tokens
GA4 + GSC snippets inject only when set and not `__FILL__` (build lines 115–121).

- [ ] `ga4_id` — GA4 measurement ID (`G-XXXXXXX`). **Who:** Brook + Carrie (create together at kickoff, access item c-4).
- [ ] `gsc_verification` — Search Console verification token. **Who:** Brook + Carrie (kickoff c-4).

### A4. Form destination — 1 token
- [ ] `form_destination` — contact-form POST endpoint / Worker URL (CR-007). **Who:** Brook (stands up the Cloudflare Worker + Turnstile), lead-delivery target confirmed by Carrie (email vs CRM).

> **Verify:** `python build/build.py --check` prints `Config complete and
> manifest valid.` with zero `MISSING` rows. Do not proceed to Section B sign-off
> or Step C-2 until it does.

---

## B. COMPLIANCE GATES — all four GREEN before `strip_noindex` can flip

These gate the *content*, not the config. They must be satisfied for **every page
with `publish:true`** in the manifest (the initial launch set — see Section D).
`strip_noindex` stays `false` until all four are signed off in writing.

- [ ] **B1. Broker written approval of the published pages (CR-003).** The eXp
  sponsoring/qualifying broker approves, in writing, every advertising page in the
  launch set and every reusable social template. **Owner:** Carrie + broker.
  *Evidence to file: dated written approval naming the exact pages/URLs.*

- [ ] **B2. LREC broker-ID disclosures present (CR-003).** The generated
  broker-disclosure footer (licensee name + license #, broker name, broker office,
  **broker-owned phone**, jurisdiction line) renders on every published page.
  Blocked until A1/A2 tokens are filled; verify it appears in `dist/` output.
  **Owner:** Brook to build, broker to confirm wording.

- [ ] **B3. Testimonials — surface public reviews the clean way (not permission-gated).**
  `testimonials.html` is PUBLISHABLE (`publish:true`). These are genuine *public*
  reviews; surfacing a client's own public praise is standard and does not require
  signed permission. The real standard (practical/industry guidance, not legal
  advice — broker marketing-compliance review in B1 is the backstop):
  (a) **Google reviews** — surface via Google's official review widget/badge OR an
  attributed quote that **links to the live Google profile** (keeps it within
  platform ToS and auto-current); avoid presenting scraped Google text as static
  hard-coded content;
  (b) **the ~23 testimonials from Carrie's own eXp site** — her existing published
  content, free to reuse as-is;
  (c) **FTC** — keep the displayed set genuine and *representative*, not cherry-picked
  to mislead (they are).
  **Owner:** Brook (implement widget/attributed-link at build); **courtesy only:**
  give Carrie a heads-up on which named reviews feature prominently.

- [ ] **B4. Fair-housing language sign-off (CR-003 / CR-010).** Neutral,
  consistently-presented facts only — no steering / demographic-fit language; the
  documented fair-housing editorial standard is approved and applied to every
  published area page and guide. **Owner:** Carrie + broker (compliance review
  where appropriate).

> Supporting, per-page: each published guide also needs an editorial owner + a
> visible reviewed-on date (CR-004/CR-010), and the closing-process/calculator
> old-host schema fixes (CR-008) must be resolved for any such page in the set.
> These are page-readiness conditions folded into the manifest's `approval_gate`
> notes; B1–B4 are the four hard compliance gates.

---

## C. DEPLOY STEPS — in order

### C-1. Fill the config
Resolve all 12 `__FILL__` tokens in `build/production.config.json` (Section A).
Leave `flags.strip_noindex = false` and `flags.include_audit = false` — do not
touch them here. **Gate:** `python build/build.py --check` → `Config complete and
manifest valid.`

### C-2. Run the build
```
python build/build.py --check      # expect: Config complete and manifest valid.
python build/build.py              # writes dist/
```
Expect `BUILD OK.` and the `NOTE: strip_noindex=false … private pre-launch
artifact` line. If the token gate trips, the build writes nothing — fix the named
tokens and re-run. This is still a **private** artifact (noindex + `Disallow: /`).

### C-3. Verify `dist/` — run the CR verification suite (`reports/14` §"Recommended verification suite")
All must pass before anything is published:
- [ ] **No `__FILL__`** anywhere in `dist/` (build gate enforces; re-grep to confirm).
- [ ] **No forbidden/audit paths:** no `/audit/`, no `.py`/`.md`, no source, no logs, no directory listings in `dist/` (CR-001/CR-002).
- [ ] **Canonical + sitemap present:** every page has a self-referential `rel="canonical"`; `dist/sitemap.xml` lists exactly the `publish:true` set and nothing else; `dist/robots.txt` and `dist/404.html` exist (CR-008).
- [ ] **Wrong-host check:** zero `carriebilleaud.exprealty.com` references in schema/links (CR-008).
- [ ] **Forms POST:** contact/valuation forms use `method="post"` to `form_destination` over HTTPS, with spam control (Turnstile); test success/validation/spam/duplicate and reconcile a live test lead (CR-007).
- [ ] **noindex is INTENTIONAL and still ON:** every page carries `noindex` and robots.txt is `Disallow: /` at this stage. This is correct — do NOT "fix" it here.
- [ ] JSON-LD validates (Rich Results Test); one Lighthouse/a11y pass per template.

### C-4. Cloudflare Pages — connect + secrets
- [ ] Create the Pages project; set build output to the generated `dist/` (deploy the built artifact, never raw `site/`).
- [ ] Stand up the contact-form Worker; set `form_destination` and Turnstile secret as environment secrets (not committed).
- [ ] Confirm edge security headers (CSP incl. `frame-ancestors`, HSTS, `X-Content-Type-Options`, Referrer-Policy) (CR-012).
- [ ] Verify the `*.pages.dev` preview renders correctly end-to-end **while still noindex**.

### C-5. DNS cutover from GoDaddy
Follow `implementation/carriebilleaud_com_dns_cutover.md` exactly. Add the custom
domain in Cloudflare Pages, provision SSL, confirm the cert is active BEFORE live
traffic points at it, and replace the existing GoDaddy → `carriebilleaud.exprealty.com`
redirect. **Keep the eXp site live in parallel.** Rollback path is documented there.

### C-6. Smoke test on the live domain (still noindex)
- [ ] `https://carriebilleaud.com/` and every published URL load over valid TLS.
- [ ] Apex/www, `/index.html`, trailing-slash, and `.html` redirects behave.
- [ ] Submit one real test lead through the live form; confirm it arrives.
- [ ] Broker-disclosure footer + NAP correct on every page.
- [ ] Re-confirm Sections A and B are fully checked.

### C-7. FINAL STEP — flip `strip_noindex`, rebuild, submit sitemap
> ## ⚠️ THE SINGLE MOST DANGEROUS STEP ⚠️
> **`strip_noindex` is the LAST switch flipped, and only here.** Flipping it early
> — before DNS cutover (C-5), before the smoke test (C-6), and before ALL of
> Section B is GREEN — publishes an unapproved and/or wrong-host site to Google,
> the exact failure the whole build is designed to prevent. While it is `false`,
> the site is safely private (every page `noindex` + `Disallow: /`). Once it is
> `true`, Google can index. **There is no partial credit: do not flip it until
> C-1 through C-6 are complete and every box in A and B is checked.**

Then, and only then:
- [ ] Set `flags.strip_noindex = true` in `production.config.json`.
- [ ] `python build/build.py` → confirm robots.txt now emits `Allow: /` + `Sitemap:` and pages read `index, follow`.
- [ ] Redeploy `dist/` to Cloudflare Pages.
- [ ] Spot-check 2–3 live URLs: `index, follow` present, canonical correct, `/robots.txt` allows crawling.
- [ ] Submit `https://carriebilleaud.com/sitemap.xml` in Google Search Console; request indexing on the homepage.
- [ ] Confirm GA4 receives live traffic (DebugView).

---

## D. STAGED LAUNCH — initial set, then rolling flip-flag

**Launch set (11 pages, `publish:true` in `page_manifest.json`):** home;
services `sell-my-house`, `listing-agent`, `first-time-buyers`, `buyers-agent`;
areas `lafayette`, `youngsville`, `broussard`; guides `flood-zones-insurance`,
`homestead-exemption`, `louisiana-closing-process`. `testimonials.html` is
authored but **HELD** pending B3 (reviewer permissions) and joins when confirmed.

**Everything else is `publish:false` and excluded from `dist/` and the sitemap by
construction** — the remaining area pages, comparison/USDA/disclosure guides, the
price-band home pages (gated on the IDX decision, CR-006), and the mortgage
calculator. They ship nothing until approved.

**Flip-flag process to add a page later (rolling approval — not one big gate):**
1. Close that page's `approval_gate` conditions (broker approval B1, fair-housing
   B4, factual QA, placeholders replaced, reviewed-on date).
2. Set the page's `publish` to `true` in `page_manifest.json`.
3. `python build/build.py --check` then `python build/build.py` — the new page
   enters `dist/` and the sitemap automatically; `strip_noindex` stays `true`.
4. Redeploy; resubmit the sitemap in GSC.

No global re-flip is ever needed again after C-7 — adding pages is a per-page
`publish: true` + rebuild, so an unapproved page can never slip in with an
approved one.
