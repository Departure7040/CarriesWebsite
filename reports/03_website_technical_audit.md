# 03 Website Technical Audit

**Site audited:** https://carriebilleaud.exprealty.com (eXp Realty / BoldTrail-hosted agent site)
**Audit date:** 2026-07-08
**Method:** Rendered fetch via Firecrawl (JS-executing, waitFor 3–5s) for content/metadata; raw `curl` (no JS) to test bot-blocking; robots.txt/sitemap fetched directly. All claims tagged **[verified]** (directly observed in fetched output), **[inferred]** (reasoned from partial evidence), or **[best-practice]** (recommendation not tied to a specific observed defect).

---

## Summary

The site is a standard BoldTrail (formerly kvCORE) IDX template on the `exprealty.com` subdomain pattern. Content renders fine for a JS-executing crawler (Googlebot renders JS, so this is not a hard block), but there are four sitewide, template-level defects that materially hurt indexation and AI-search visibility:

1. **[verified] robots.txt blocks nearly all crawlers by default** — a second, later `User-agent: *` group with `Disallow: /` combines with the first `User-agent: *` group per Google's own robots.txt spec, meaning any crawler not explicitly named (Googlebot, bingbot, Twitterbot, etc. are named; ClaudeBot, GPTBot, PerplexityBot, Applebot, YandexBot, DuckDuckBot, CCBot, Bytespider are **not**) is disallowed from the entire site.
2. **[verified] Every page's canonical tag points off-domain to `exprealty.com`**, not to `carriebilleaud.exprealty.com`. This tells search engines the "real" URL is the corporate site, undermining Carrie's own branded domain's ability to rank.
3. **[verified] Zero JSON-LD structured data anywhere** (homepage, agent profile, blog post all checked) — no `RealEstateAgent`, `LocalBusiness`, `Person`, `BreadcrumbList`, or `FAQ` schema.
4. **[verified] The agent bio page (`/agents.php`) has no biography text** — the "About Carrie" section contains only a lead-capture form, no written bio, credentials, service-area narrative, or testimonials.

All four are template-level (BoldTrail platform), not agent-editable in the normal CMS sense, except the bio, which is very likely editable through the agent's BoldTrail/kvCORE dashboard profile fields.

---

## Crawlability & Indexation

| Item | Finding | Tag |
|---|---|---|
| `robots.txt` (200, fetched 2026-07-08) | Contains a **duplicate `User-agent: *` block**: first block disallows only specific paths (`/emails_kvarea/`, `/wp-admin/`, IDX query params, etc.); a **second, later `User-agent: *` block contains only `Disallow: /`**. Per Google's documented robots.txt parsing, multiple groups sharing the same user-agent are merged, so the effective rule for the generic `*` group becomes "disallow everything." Explicitly-named bots (Googlebot, Googlebot-Mobile, bingbot, Slurp, msnbot, Twitterbot, facebookexternalhit, AdsBot-Google[-Mobile[-Apps]], Mediapartners-Google, PowerMapper, Screaming Frog, SemrushBot, TermlyBot) get their own `Allow: /` group and are unaffected. Any other bot (ClaudeBot, GPTBot, PerplexityBot, Google-Extended, Applebot, YandexBot, DuckDuckBot, CCBot, Bytespider, etc.) is blocked site-wide. | [verified] |
| `sitemap.xml` (root) | Returns **404** and is served the site's "Page Not Found" template (itself tagged `noindex,nofollow`, correctly). Not itself a problem since robots.txt correctly references `sitemap-index.xml`, but any tool/human checking the conventional `/sitemap.xml` location will find nothing. | [verified] |
| `sitemap-index.xml` | 200 OK. References `sitemap-structure-1.xml.gz`, `sitemap-areas-1.xml.gz`, `sitemap-listings-1.xml.gz`, all dated 2026-07-08 (fresh). | [verified] |
| Homepage meta robots | `index,follow`, single tag, no conflict. | [verified] |
| `/agents.php` meta robots | **Two conflicting meta robots tags render in the DOM**: `<meta name="robots" content="index,follow">` in the static `<head>`, and a second `<meta name="robots" content="noindex, nofollow">` injected later in the rendered document (co-located with Cloudflare Turnstile / CSP script tags — appears to come from the bot-challenge widget bundle). Google's rule when multiple robots directives exist is to combine the most restrictive; a rendered `noindex` can suppress indexing even if the static HTML says `index,follow`. | [verified] |
| Blog post meta robots | Same dual-tag pattern as `/agents.php`. | [verified] |
| `/areas/lafayette` meta robots | Single tag, `noindex,nofollow` — correct/intentional (prevents thin/duplicate MLS search-results pages from indexing). | [verified] |
| Bot-blocking via Cloudflare | Plain `curl` (no JS, no browser fingerprint) to `/` and `/agents.php` both returned **HTTP 403** with a 5–5.5KB Cloudflare challenge body. A JS-rendering fetch (Firecrawl, and presumably Googlebot) gets 200 with full content. Confirms Cloudflare bot-fight/Turnstile mode is active; non-JS tools (some SEO auditors, some AI/LLM crawlers that don't render JS) will see only a challenge page. | [verified] |
| Canonical tags | `/agents.php` canonical → `https://exprealty.com/agents/1172379/Carrie+Billeaud`. Blog post canonical → `https://exprealty.com/blog/375489/...`. **Homepage has no canonical tag at all.** All checked on rendered HTML. | [verified] |

---

## On-page findings (per page)

### 1. Homepage — `https://carriebilleaud.exprealty.com/` (HTTP 200, fetched 2026-07-08)
- **Title tag:** "Lafayette LA Real Estate & Homes for Sale | eXp Realty - Lafayette, LA and Surrounding Areas - Licensed by Louisiana Real Estate Commission" — 130+ characters, will truncate heavily in SERPs. [verified]
- **Meta description:** Identical text to the title tag, word for word. This is a duplicate-content-in-metadata pattern; Google will likely rewrite the snippet itself. [verified]
- **H1/H2:** Not clearly exposed in the rendered content extraction beyond blog/area list headings ("Latest Blog Posts", "Areas We Cover"); no evidence of a keyword-focused H1 introducing Carrie or her service area on the homepage itself. [inferred — main hero H1 may exist visually but was not distinctly captured in the text extraction]
- **Canonical:** None present. [verified]
- **Structured data:** No JSON-LD found anywhere in the rendered HTML. [verified]
- **Internal links:** Strong internal linking to 20 area/community pages (Abbeville, Lafayette, Youngsville, etc.) and to 4 recent blog posts. [verified]
- **Images/alt text:** Blog thumbnail images carry descriptive alt text ("couple looking at laptop computer", "family of four smiling while sitting on couch", etc.); at least 2 images (icon/logo-type) have empty `alt=""`. [verified]
- **Mobile viewport:** Present and correctly configured (`width=device-width, initial-scale=1`). [verified]
- **Conversion CTAs:** Facebook Messenger "Chat With Me" widget sitewide; lead-capture form gated behind Cloudflare Turnstile (email + cell phone + message, with TCPA consent language). No visible click-to-call phone link captured in the homepage extraction (present on the agent page). [verified/partial]
- **Google Translate widget** present in the footer of every page — minor UX/perf overhead, not a ranking issue.

### 2. Agent profile — `https://carriebilleaud.exprealty.com/agents.php` (HTTP 200, resolves to `/agents/1172379/Carrie+Billeaud`, fetched 2026-07-08)
- **Title tag:** "Carrie Billeaud - REALTOR®" — clean, appropriately short. [verified]
- **Meta description:** "The professional page for REALTOR® Carrie Billeaud" — generic, boilerplate, does not mention Lafayette/Acadiana, specialties, or years of experience. Weak for a page meant to be the entity anchor. [verified]
- **H1:** "Carrie Billeaud - REALTOR®". Sub-headers: "Carrie Billeaud [license #] 0995689513" (H3), "eXp Realty - Lafayette, LA and Surrounding Areas..." (H3), "Information" (H2), "About Carrie" (H2). [verified]
- **Bio content under "About Carrie":** **Empty.** The section header is immediately followed by a "Send Carrie a Message" contact form — no biography paragraph, no credentials, no specialties, no years-in-business, no testimonials, no professional photo credit/description captured in the text extraction. [verified]
- **Canonical:** Points to `https://exprealty.com/agents/1172379/Carrie+Billeaud` — off Carrie's own branded domain. [verified]
- **Structured data:** No `Person` or `RealEstateAgent` JSON-LD found. [verified]
- **NAP on page:** Cell `337-258-5379` (click-to-call `tel:` link present — good), languages "English", social links to Facebook, X/Twitter, YouTube, LinkedIn, Instagram, Pinterest (all working URLs, good E-E-A-T/entity signal). [verified]
- **Conversion CTA:** Click-to-call tel: link, "E-mail Me" anchor, lead form. Good mechanics, but the surrounding page has almost nothing to convince a visitor to use them since there's no bio to build trust.

### 3. Area/community page — `https://carriebilleaud.exprealty.com/areas/lafayette` (HTTP 200, fetched 2026-07-08)
- **Title tag:** "Lafayette Real Estate" — reasonable. **Meta description:** unique, data-driven ("Search homes for sale in Lafayette, LA for free. View all 1,834 listings... average price of $346,174..."). This is good, non-duplicated metadata. [verified]
- **Meta robots:** `noindex,nofollow` — intentional, appropriate for an IDX search-results/stats page that is dynamically generated and would otherwise create massive thin/duplicate content across dozens of area pages and neighborhood sub-pages (170+ neighborhood links found on this one page alone). [verified] This is correct SEO hygiene by the platform, not a bug.
- **Content:** Market stats (avg price, sqft, days on market, town vs. parish comparison), a Leaflet map, and ~170 neighborhood links. Templated/generated content, not written by the agent — expected and fine for an IDX search page, since it's deliberately excluded from the index.
- **Thin/duplicate content risk:** Because these pages are `noindex`, they aren't a duplicate-content risk for Google, but they are also **not driving any organic search value** — all 20 area pages linked from the homepage nav are non-indexable. Only genuinely unique written content (blog posts, the bio) can rank.

### 4. Blog post — `https://carriebilleaud.exprealty.com/blog/375489/Modern+Farmhouse+Living...` (HTTP 200, fetched 2026-07-08)
- **Title tag / OG title:** "Modern Farmhouse Living with Space, Style, and Thoughtful Upgrades" — good, descriptive, matches `og:title`. [verified]
- **Meta description / OG description:** Truncated automatically from body text ("110 Marais Avenue, Youngsville, LA 70592Modern Farmhouse Living...") — run-on, no space between address and headline, reads as a scraping artifact rather than an authored description. [verified]
- **H1 structure:** Two H1-equivalent headers appear back-to-back — the page title, then an image with alt text immediately followed by a duplicate "## Modern Farmhouse Living..." heading. Mild header-hierarchy redundancy. [verified]
- **Canonical:** Points to `https://exprealty.com/blog/375489/...` — off Carrie's branded domain, same issue as the agent page. [verified]
- **Meta robots:** Dual conflicting tags (`index,follow` static + `noindex, nofollow` rendered), same pattern as `/agents.php`. [verified]
- **Structured data:** No `Article`/`BlogPosting` JSON-LD found despite this being clearly blog content — a missed rich-result opportunity. [verified]
- **Content quality:** This particular post is genuinely useful, unique, well-written listing-marketing content (not thin) — good example of the kind of content that should be the site's SEO backbone. [verified]
- **Conversion CTA:** Personal Gmail address (`carriebilleaud@gmail.com`) and phone number given directly in the post body — good for conversion, but using a personal Gmail rather than a branded email is a minor professionalism/trust signal issue. [verified]
- **Outbound links:** Links to `sites.totalexpert.net` (single-property site) and `flexmls.com` listing — both external, `nofollow`-tagged per the homepage nofollow pattern observed. Not broken, just outbound with no link equity passed (expected/appropriate).

---

## Schema / structured data

**No JSON-LD structured data was found on any of the four pages checked in full (homepage, agent profile, area page, blog post).** [verified] Specifically absent:
- `RealEstateAgent` / `Person` schema on the agent profile (would support Knowledge Panel eligibility and rich snippets for "Carrie Billeaud realtor Lafayette" type queries)
- `LocalBusiness` schema for the brokerage/service area
- `BlogPosting`/`Article` schema on blog posts
- `BreadcrumbList` schema (no breadcrumbs observed in any page's markup)
- `FAQPage` schema (no FAQ content observed anywhere)

This is a sitewide template gap, not specific to this agent's content — it affects every agent site on this BoldTrail template family unless the platform has since added an opt-in schema module.

---

## Entity/bio assessment of `/agents.php`

**Verdict: The bio/entity content is missing, not merely weak.** The "About Carrie" section — the one place on the entire site meant to establish who Carrie Billeaud is, her credentials, her specialties, and why a visitor should trust her — contains no biographical text at all in the rendered output. It goes straight from the section header to a lead-capture form. Combined with:
- a generic, non-differentiated meta description ("The professional page for REALTOR® Carrie Billeaud"),
- no `Person`/`RealEstateAgent` schema,
- a canonical tag that points away from this domain entirely,

...the agent profile page currently does almost nothing to build E-E-A-T (Experience, Expertise, Authoritativeness, Trust) signals for Google, and gives a human visitor no reason to trust Carrie beyond her name, license number, and a phone number. This is the single highest-leverage content fix available on the site, and it is very likely editable directly by the agent through the BoldTrail/kvCORE backend "Agent Profile" or "About Me" field — this is standard, agent-owned content on this platform (not a template-locked element like schema or canonical tags).

---

## Conversion / CTA assessment

- **Click-to-call:** Present and correctly implemented as a `tel:` link on the agent profile (`337-258-5379`). [verified]
- **Lead forms:** Present sitewide (email + cell phone + message + TCPA consent checkbox), gated behind Cloudflare Turnstile bot verification — reasonable spam protection but adds a friction step and a dependency on third-party JS loading correctly.
- **Messenger chat widget:** "Chat With Me" (Facebook Messenger deep link) present on every page checked — good low-friction, mobile-native CTA.
- **Blog CTAs:** Individual listing blog posts include a direct email/phone signature and calls to action ("Schedule Your Private Tour", "FREE Home Evaluation" link) — well done, human-written CTAs.
- **Gap:** The agent profile page — the highest-intent destination for someone researching "who is Carrie Billeaud" — has a form and a phone number but no supporting bio/trust content to move a visitor from curious to convinced before they reach the CTA.

---

## NAP (Name / Address / Phone) as shown on site

| Field | Value observed | Where |
|---|---|---|
| Name | Carrie Billeaud, REALTOR® | agents.php, blog byline |
| Brokerage | eXp Realty | sitewide footer/header |
| Service area (no street address given) | "Lafayette, LA and Surrounding Areas — Licensed by Louisiana Real Estate Commission" | sitewide footer |
| Agent cell / click-to-call | 337-258-5379 | agents.php, blog post signature |
| Office number | 337-522-7554 | homepage/footer |
| Corporate toll-free | 800-746-9840 | homepage/footer |
| Agent license # | 0995689513 | agents.php |
| Email | carriebilleaud@gmail.com | blog post signature (not found elsewhere in crawled pages) |

**No physical street address was found anywhere on the crawled pages** — expected for eXp Realty's cloud/virtual brokerage model (no local branch office), but worth confirming this matches (or intentionally omits, consistently) whatever address is used on Google Business Profile and other citation sites, since NAP consistency checks typically expect either a matching address everywhere or a deliberate, consistent "service-area business" (no address) configuration across all platforms. [inferred — full NAP consistency check requires comparing against GBP/citations, outside this crawl's scope]

---

## Prioritized fixes

### Fix directly (agent-editable)

| Priority | Task | Why | Effort |
|---|---|---|---|
| P1 | Write and publish a real bio on `/agents.php` "About Carrie" section — background, years of experience, specialties (e.g., Acadiana communities, first-time buyers), credentials, a personal note. 150–400 words. | Currently empty; this is the entity/trust anchor page and the highest-leverage content gap on the site. | Low |
| P2 | Rewrite the homepage title tag and meta description so they are not identical to each other; make the meta description a compelling, unique summary (~150–160 chars). | Duplicate title/description is a wasted SERP-snippet opportunity. | Low |
| P2 | Rewrite the agent-profile meta description to include location + specialty keywords instead of generic boilerplate. | Currently non-differentiated; hurts CTR from search. | Low |
| P3 | Replace the personal Gmail address used in blog post signatures with a branded/professional email if one exists, or confirm this is the intended contact address. | Minor trust/branding signal. | Low |
| P3 | Add unique intro copy to at least the top few area pages if the platform allows agent-authored text above the IDX feed (check BoldTrail CMS options). | Area pages are `noindex` and currently 100% templated data with no agent voice. | Medium |

### Platform-limited (eXp / BoldTrail / IDX) — with workaround

| Priority | Task | Why | Workaround |
|---|---|---|---|
| P1 | Fix robots.txt so the trailing `User-agent: *` / `Disallow: /` block is removed or merged into the first `*` group. | As written, it blocks every crawler not explicitly named — including AI answer-engine crawlers (ClaudeBot, GPTBot, PerplexityBot, Google-Extended) that increasingly drive referral traffic in 2026. | Cannot be edited by the agent (robots.txt is platform-served). File a support ticket with BoldTrail/eXp Tech Support citing the duplicate `User-agent: *` groups and requesting the trailing global disallow be removed; reference Google's documented behavior of merging same-named user-agent groups. |
| P1 | Fix the canonical tag on `/agents.php` and blog posts so it points to `carriebilleaud.exprealty.com`, not `exprealty.com`. | Actively tells Google the branded agent domain is not the authoritative version of its own content. | Platform templating issue — request via BoldTrail support/eXp marketing tech team; ask specifically whether "self-canonical" is a configurable setting per agent site. |
| P1 | Resolve the conflicting dual meta-robots tags on `/agents.php` and blog posts (static `index,follow` vs. rendered `noindex, nofollow` injected alongside the Cloudflare Turnstile widget). | Risk of the page being excluded from the index despite the static tag saying otherwise. | Ask BoldTrail support to confirm which tag is authoritative and remove the duplicate; in the interim, verify actual indexing status via Google Search Console URL Inspection tool (requires Search Console access — flag to site owner/Carrie). |
| P2 | Add `RealEstateAgent`/`Person`, `LocalBusiness`, `BlogPosting`, and `BreadcrumbList` JSON-LD schema. | No structured data anywhere on the site; missed rich-result and Knowledge Panel opportunities. | Template-level — request as a feature/fix from BoldTrail; no agent-side workaround exists on this platform. |
| P3 | Make `/sitemap.xml` (the conventional location) either redirect to or serve the real sitemap index instead of a 404/Page-Not-Found template. | Minor hygiene issue; tools/humans checking the default location find nothing. | Platform routing — low priority support request. |
| P3 | Reduce/allowlist Cloudflare bot-challenge scope so non-JS-rendering legitimate crawlers/tools aren't universally 403'd. | `curl`-level (non-JS) requests get HTTP 403 with a Turnstile challenge; may affect some SEO/AI tools that don't execute JS, though major search engines render JS fine. | Cloudflare configuration is platform-managed; request confirmation from BoldTrail that verified Googlebot/Bingbot IP ranges are allowlisted (this is normal Cloudflare practice, likely already fine for the engines that matter, but worth confirming for AI crawlers too). |
