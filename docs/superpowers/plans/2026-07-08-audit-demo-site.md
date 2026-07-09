# Audit/Demo Static Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the static site in `/site` that presents the Carrie Billeaud SEO audit and demos what her homepage could look like, per `docs/superpowers/specs/2026-07-08-audit-demo-site-design.md`.

**Architecture:** Hand-built static HTML/CSS, no build step, no dependencies. One shared stylesheet; each page is a self-contained HTML file using a common shell pattern. Audit pages are curated client-facing rewrites of the markdown reports in `/reports/`.

**Tech Stack:** HTML5, CSS3 (single stylesheet, CSS custom properties), zero JS frameworks (small inline JS allowed only for the mobile nav toggle and demo-banner dismiss).

## Global Constraints

- Site root is `E:\CarriesWebsite\site\`; all asset URLs must be **relative** (`assets/style.css` from root pages, `../assets/style.css` from `audit/` pages) so the site works from any static server and any subdomain.
- EVERY page `<head>` must contain: `<meta name="robots" content="noindex, nofollow">` and `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- `site/robots.txt` must be exactly: `User-agent: *` / `Disallow: /`.
- Demo homepage may state as fact ONLY verified data: name "Carrie Billeaud", Realtor, eXp Realty, Lafayette LA; phone 337-258-5379; service areas Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, Milton; Zillow 29 reviews · 5.0; specialties (first-time buyers, sellers, residential, investment). Unverified metrics (11 years, 174 sales, $44.6M, ICON Agent, 50+ families) must NOT appear on the homepage; on audit pages they appear only with `[client-confirm]` tags.
- No external requests: no CDN fonts/scripts/images. System font stack. Images are inline SVG or CSS only.
- Copy tone: direct, friendly, practical; no hype, no guaranteed rankings.
- Palette/type (used consistently): `--ink:#1a2332; --teal:#0f5c5a; --teal-dark:#0b4442; --gold:#c9a24b; --cream:#faf7f2; --paper:#ffffff; --rule:#e3ded4; --ok:#2e7d32; --warn:#b26a00; --bad:#b3261e;` Headings `font-family: Georgia, 'Times New Roman', serif`; body `font-family: system-ui, Segoe UI, Roboto, sans-serif`.
- Evidence tags render as pills via classes `.tag.verified` (green), `.tag.inferred` (amber), `.tag.confirm` (red-outline, label "verify with Carrie"), `.tag.practice` (teal-outline, label "best practice").
- Commit after every task with the standard trailer:
  `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` + `Claude-Session: https://claude.ai/code/session_015nu5YGvU8GA4jgis3ZoUhe`

---

### Task 1: Foundation — stylesheet, robots.txt, SERVING.md

**Files:**
- Create: `site/assets/style.css`
- Create: `site/robots.txt`
- Create: `site/SERVING.md`

**Interfaces:**
- Produces: CSS classes used by all later tasks: `.site-header`, `.nav`, `.demo-banner`, `.hero`, `.btn`, `.btn-gold`, `.card`, `.card-grid`, `.section`, `.section-alt`, `.tag` (+ `.verified/.inferred/.confirm/.practice`), `.score` (+ `.score-bad/.score-warn/.score-ok`), `.table-wrap`, `.bar-row`, `.bar-fill`, `.footer`, `.sticky-call`, `.audit-nav`, `.finding`, `.kicker`.

- [ ] **Step 1: Write `site/robots.txt`**

```
User-agent: *
Disallow: /
```

- [ ] **Step 2: Write `site/assets/style.css`** — CSS reset (box-sizing, margins), the custom-property palette from Global Constraints, then components:

```css
:root{--ink:#1a2332;--teal:#0f5c5a;--teal-dark:#0b4442;--gold:#c9a24b;--cream:#faf7f2;--paper:#fff;--rule:#e3ded4;--ok:#2e7d32;--warn:#b26a00;--bad:#b3261e;}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--cream);line-height:1.6}
h1,h2,h3{font-family:Georgia,"Times New Roman",serif;line-height:1.2}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.25rem}
.demo-banner{background:var(--ink);color:#fff;font-size:.9rem;padding:.5rem 1rem;text-align:center}
.demo-banner a{color:var(--gold)}
.site-header{background:var(--paper);border-bottom:1px solid var(--rule);position:sticky;top:0;z-index:10}
.nav{display:flex;align-items:center;justify-content:space-between;padding:.75rem 0;gap:1rem;flex-wrap:wrap}
.nav a{color:var(--ink);text-decoration:none;margin-left:1rem}
.btn{display:inline-block;background:var(--teal);color:#fff;padding:.7rem 1.4rem;border-radius:6px;text-decoration:none;font-weight:600}
.btn-gold{background:var(--gold);color:var(--ink)}
.hero{background:linear-gradient(160deg,var(--teal) 0%,var(--teal-dark) 100%);color:#fff;padding:4.5rem 0}
.section{padding:3.5rem 0}
.section-alt{background:var(--paper)}
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.25rem}
.card{background:var(--paper);border:1px solid var(--rule);border-radius:10px;padding:1.5rem}
.tag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.03em;padding:.15rem .6rem;border-radius:999px;text-transform:uppercase}
.tag.verified{background:#e6f2e7;color:var(--ok)}
.tag.inferred{background:#fdf1dd;color:var(--warn)}
.tag.confirm{background:transparent;border:1.5px solid var(--bad);color:var(--bad)}
.tag.practice{background:transparent;border:1.5px solid var(--teal);color:var(--teal)}
.score{font-family:Georgia,serif;font-size:2.4rem;font-weight:700}
.score-bad{color:var(--bad)}.score-warn{color:var(--warn)}.score-ok{color:var(--ok)}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;background:var(--paper)}
th,td{border:1px solid var(--rule);padding:.6rem .8rem;text-align:left;font-size:.95rem}
th{background:var(--cream)}
.bar-row{display:grid;grid-template-columns:12rem 1fr 4rem;align-items:center;gap:.75rem;margin:.4rem 0}
.bar-fill{background:var(--teal);height:1.1rem;border-radius:4px;min-width:2px}
.bar-fill.carrie{background:var(--gold)}
.sticky-call{display:none}
@media (max-width:720px){.sticky-call{display:block;position:fixed;bottom:0;left:0;right:0;background:var(--teal);text-align:center;padding:.9rem;z-index:20}.sticky-call a{color:#fff;font-weight:700;text-decoration:none}}
.audit-nav{background:var(--paper);border:1px solid var(--rule);border-radius:10px;padding:1rem;margin:1.5rem 0}
.audit-nav a{display:inline-block;margin:.25rem .75rem .25rem 0;color:var(--teal)}
.finding{border-left:4px solid var(--gold);padding:.75rem 1rem;background:var(--paper);margin:1rem 0}
.kicker{text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;color:var(--gold);font-weight:700}
.footer{background:var(--ink);color:#cfd6df;padding:2.5rem 0;margin-top:3rem;font-size:.9rem}
.footer a{color:var(--gold)}
```

(Adjust/extend as needed while building pages, but keep the class names above stable.)

- [ ] **Step 3: Write `site/SERVING.md`** — how Brook serves it:

````markdown
# Serving this site

Any static file server pointed at this `site/` folder works.

## Quick local preview
```powershell
cd E:\CarriesWebsite\site
python -m http.server 8080
# open http://localhost:8080
```

## Cloudflare tunnel (Brook's setup)
1. Run a local static server on a port (e.g. 8080) — python (above), or
   `caddy file-server --root E:\CarriesWebsite\site --listen :8080`.
2. Point the existing cloudflared tunnel at it. In the tunnel config
   (`%USERPROFILE%\.cloudflared\config.yml`) add an ingress rule:
   ```yaml
   ingress:
     - hostname: carrie.dubose.me
       service: http://localhost:8080
     - service: http_status:404
   ```
3. Add the DNS route: `cloudflared tunnel route dns <tunnel-name> carrie.dubose.me`
4. `cloudflared tunnel run <tunnel-name>`

The site ships `robots.txt Disallow: /` + `noindex` on every page on purpose:
it's a demo/audit artifact and must not compete with Carrie's real entity in
search. Do not remove those before showing Google anything.
````

- [ ] **Step 4: Verify** — `python -m http.server 8080` from `site/`, GET `http://localhost:8080/robots.txt` returns the two lines; style.css loads with 200.

- [ ] **Step 5: Commit** — `git add site/ && git commit -m "site: foundation (stylesheet, robots, serving notes)"` (+ trailer).

---

### Task 2: Demo homepage `site/index.html`

**Files:**
- Create: `site/index.html`

**Interfaces:**
- Consumes: Task 1 CSS classes.
- Produces: the `/audit/` links other pages assume (`audit/index.html`).

**Page shell used here and (adapted) on all pages:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Carrie Billeaud · Lafayette LA Realtor — Demo Concept</title>
<link rel="stylesheet" href="assets/style.css">
<!-- JSON-LD inserted per Step 2 -->
</head>
<body>
<div class="demo-banner">Demo concept — part of your SEO audit. <a href="audit/">See the analysis →</a></div>
<header class="site-header"><div class="wrap nav">
  <strong>Carrie Billeaud <span style="color:var(--gold)">·</span> REALTOR®</strong>
  <nav><a href="#about">About</a><a href="#areas">Areas</a><a href="#reviews">Reviews</a><a href="#faq">FAQ</a><a class="btn btn-gold" href="tel:3372585379">337-258-5379</a></nav>
</div></header>
<main> …sections… </main>
<footer class="footer"><div class="wrap">
  <p>Carrie Billeaud, REALTOR® · eXp Realty · Lafayette, Louisiana · <a href="tel:3372585379">337-258-5379</a></p>
  <p>Demo concept built as part of an SEO audit by Brook DuBose. Not Carrie's live website. Sample copy marked as placeholder is illustrative only.</p>
</div></footer>
<div class="sticky-call"><a href="tel:3372585379">📞 Call Carrie — 337-258-5379</a></div>
</body></html>
```

- [ ] **Step 1: Build sections in `<main>`** (each `.section` with `.wrap`):
  1. **Hero** (`.hero`): kicker "Lafayette · Youngsville · Broussard · Acadiana"; H1 "Buy or sell with a Lafayette Realtor who knows Acadiana street by street."; subline naming first-time buyers + sellers; CTAs `.btn-gold` tel: link + `.btn` "Get a free home valuation" → `#contact`.
  2. **Trust strip**: Zillow ★5.0 · 29 reviews (verified); "eXp Realty" brokerage; "Serving 7 Acadiana communities".
  3. **About** (`#about`): 150-word bio composed ONLY from verified profile facts (UL Lafayette business degree, team including her father, staging background, first-time-buyer and seller focus) — end with `<em>(Sample bio — final copy needs Carrie's confirmation.)</em>`.
  4. **Services**: 3 cards — First-Time Buyers / Sellers & Listing / Investment & Residential.
  5. **Areas** (`#areas`): 7 cards, one per service area, one distinct sentence each (Youngsville: growth + new construction; Broussard: commute + established neighborhoods; etc.).
  6. **Reviews** (`#reviews`): the Zillow 29 · 5.0 stat + 2 short quote cards marked `<em>(placeholder — real reviews would be pulled with permission)</em>`.
  7. **FAQ** (`#faq`): 4 `<details>` items (cost to work with a buyer's agent, how fast homes sell in Lafayette, first steps for first-time buyers, what's my home worth) — 2-3 sentence factual answers, no invented market stats.
  8. **Contact** (`#contact`): non-functional demo form (name/email/phone/message) with `<p><em>Demo form — not wired up.</em></p>` + tel CTA.

- [ ] **Step 2: Add JSON-LD** in `<head>` — RealEstateAgent schema; this is part of the pitch (view-source):

```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"RealEstateAgent",
"name":"Carrie Billeaud, Realtor","telephone":"+1-337-258-5379",
"url":"https://carriebilleaud.exprealty.com",
"parentOrganization":{"@type":"RealEstateAgent","name":"eXp Realty"},
"areaServed":["Lafayette LA","Youngsville LA","Broussard LA","Carencro LA","Scott LA","Maurice LA","Milton LA"],
"knowsAbout":["First-time home buyers","Listing and selling homes","Residential real estate","Investment property"],
"sameAs":["https://www.zillow.com/profile/carriebilleaud","https://www.realtor.com/realestateagents/567985a6bb954c0100686dd4","https://www.homes.com/real-estate-agents/carrie-billeaud/pf5j8yv/","https://www.facebook.com/carriebilleaud/","https://www.instagram.com/carriebilleaud_realtor/"]}
</script>
<!-- NOTE for the pitch: address is omitted until Carrie confirms the canonical one. -->
```

- [ ] **Step 3: Verify** — serve locally; check: banner link goes to `audit/`; tel: links work; page readable at 375px width; `python - <<'PY'` quick check or PowerShell `Select-String -Path site/index.html -Pattern 'noindex'` returns a match; JSON-LD parses (paste into a JSON validator or `python -c "import json,re,sys;..."`).

- [ ] **Step 4: Commit** — `git add site/index.html && git commit -m "site: demo homepage with schema, CTAs, verified-facts-only copy"` (+ trailer).

---

### Task 3: Audit dashboard `site/audit/index.html`

**Files:**
- Create: `site/audit/index.html`
- Source: `reports/00_client_brief.md` (read it; this page is its visual version)

**Interfaces:**
- Consumes: Task 1 classes; links to the six sibling pages (exact filenames: `presence.html`, `website.html`, `local-seo.html`, `competitors.html`, `ai-search.html`, `roadmap.html`).
- Produces: the `.audit-nav` block reused verbatim (with relative links) on every audit page.

- [ ] **Step 1: Build the page.** Shell as Task 2 but `href="../assets/style.css"`, title "SEO Audit — Carrie Billeaud", banner replaced by a plain header: kicker "SEO & Lead-Generation Audit · July 2026", H1 "Carrie, you have good raw materials — the search layer just isn't working for you yet.", link back to `../` labeled "← See the demo homepage". Sections:
  1. **Scorecard** `.card-grid` of 5 cards with `.score` numbers: Google Business Profile — `score-bad` "Missing"; Identity consistency — `score-bad` "3 phones · 5 addresses"; Website crawlability — `score-warn` "Blocked to AI"; Reviews — `score-warn` "29 (one platform)"; Reputation raw material — `score-ok` "Strong".
  2. **What's working / What's hurting** — two columns from the client brief's lists, tags included.
  3. **Top 5 opportunities** — numbered, one line each + link to the relevant detail page.
  4. **5 things not to waste money on** — from the brief.
  5. **`.audit-nav`**: links to all 6 detail pages + roadmap, used on every audit page.

- [ ] **Step 2: Verify** — all 7 nav links resolve to files that will exist (create as empty placeholders is NOT allowed — instead finish Tasks 4-6 before final verify; for now check spelling against the filenames in this plan).

- [ ] **Step 3: Commit** — `git add site/audit/index.html && git commit -m "site: audit dashboard (client brief as scorecards)"` (+ trailer).

---

### Task 4: Findings pages — `presence.html` + `website.html`

**Files:**
- Create: `site/audit/presence.html` — source: `reports/01_public_presence_inventory.md` + `data/nap_consistency_matrix.csv`
- Create: `site/audit/website.html` — source: `reports/03_website_technical_audit.md`

**Interfaces:** Consumes Task 1 classes + Task 3 `.audit-nav`.

- [ ] **Step 1: `presence.html`** — kicker "Finding 1 · Public presence & identity"; H1 "Google sees five versions of you."; sections: (a) the NAP conflict table (`.table-wrap`) — one row per source from the matrix CSV: source, phone, address, each conflicting cell wrapped in `<strong style="color:var(--bad)">`; (b) "What this does to rankings" 2 paragraphs; (c) per-platform review counts; (d) fix summary linking to roadmap. Every factual row gets `.tag.verified` (as-shown observation); career metrics get `.tag.confirm`.
- [ ] **Step 2: `website.html`** — kicker "Finding 2 · Your website"; H1 "Your site is telling search engines to go away."; `.finding` blocks for: robots.txt wildcard block (plain-English explanation + who it blocks), off-domain canonicals, conflicting noindex tags, missing bio ("the page about you has no 'about you'"), zero schema, duplicate titles. Each block: what/why-it-matters/who-can-fix (Fix directly vs eXp support ticket) with `.tag`s.
- [ ] **Step 3: Verify + commit** — links/nav resolve; `git commit -m "site: presence + website findings pages"` (+ trailer).

---

### Task 5: Findings pages — `local-seo.html`, `competitors.html`, `ai-search.html`

**Files:**
- Create: `site/audit/local-seo.html` — source: `reports/02_local_seo_audit.md`
- Create: `site/audit/competitors.html` — source: `reports/04_competitor_gap_analysis.md` (the QA-CORRECTED version) + `data/competitor_snapshot.csv`
- Create: `site/audit/ai-search.html` — source: `reports/05_ai_search_visibility_plan.md`

**Interfaces:** Consumes Task 1 classes + Task 3 `.audit-nav`.

- [ ] **Step 1: `local-seo.html`** — H1 "The biggest gap: you're not on the map."; explain GBP absence in plain English; the relevance/distance/prominence framing; condensed GBP setup checklist (link concept: full checklist lives in the written audit); review strategy summary (2–4/month, Google first).
- [ ] **Step 2: `competitors.html`** — H1 "Who's winning your searches — and how."; review-count comparison as `.bar-row` bars: Sean Hettich 353, Nah Senpeng 97, Stephen Hundley 79, Carrie (`.bar-fill.carrie`) 29 with label "29 (Zillow only)"; widths proportional (353→100%). Common winner traits; gap list; NO rank-by-month promises (QA rule) — direction-of-travel language only.
- [ ] **Step 3: `ai-search.html`** — H1 "Can ChatGPT and Google AI find you? Right now, no."; the 5 questions an AI must answer (who/where/what/why credible/how to contact) each with current-state verdict + fix; realistic-expectations paragraph.
- [ ] **Step 4: Verify + commit** — `git commit -m "site: local-seo, competitors, ai-search findings pages"` (+ trailer).

---

### Task 6: `roadmap.html` + final verification sweep

**Files:**
- Create: `site/audit/roadmap.html` — source: `reports/07_30_60_90_day_plan.md`

- [ ] **Step 1: `roadmap.html`** — H1 "The 30 / 60 / 90 day plan."; three `.card`s (30: Foundation, 60: Build, 90: Grow) with condensed checklists; "what working looks like" honest-expectations block (keep the no-guarantees sentence verbatim); CTA card at the end: "Ready to start? → the first step is a 15-minute questions call" (no pricing on site).
- [ ] **Step 2: Full-site verification** — from `site/`: `python -m http.server 8080`; click through every page and every nav link; then automated checks (PowerShell):
  - `Get-ChildItem -Recurse -Filter *.html site | ForEach-Object { if (-not (Select-String -Path $_.FullName -Pattern 'noindex' -Quiet)) { "MISSING noindex: $($_.FullName)" } }` → no output expected.
  - Grep all `href=`/`src=` values; confirm no `http://` or `https://` external asset references (only tel:, the sameAs JSON-LD URLs, and outbound profile links in copy are allowed as `<a href>`).
  - Confirm every page at 375px width has no horizontal scroll (manual, browser devtools).
- [ ] **Step 3: Fix anything found; commit** — `git add site/ && git commit -m "site: roadmap page + verification fixes"` (+ trailer); push.

---

## Self-review (done at write time)
- Spec coverage: 9 pages ✔ (index, audit index, 5 findings, roadmap) + robots ✔ + SERVING.md ✔ + noindex rule ✔ + verified-facts-only homepage ✔ + curated (not dumped) audit pages ✔ + pricing/questions excluded ✔ + placeholder photos via CSS/SVG ✔ + non-functional form noted ✔.
- No placeholders left in tasks; each page step names its exact content source file.
- Class names consistent across tasks (checked against Task 1 list).
