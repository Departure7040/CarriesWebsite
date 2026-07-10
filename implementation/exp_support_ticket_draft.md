# eXp / BoldTrail Support Ticket Draft — Platform-Level Technical Fixes

**Prepared for:** Carrie Billeaud
**Site:** https://carriebilleaud.exprealty.com
**Prepared:** 2026-07-09
**Source:** Findings a–d from `/reports/03_website_technical_audit.md`, audited 2026-07-08

These four issues cannot be fixed by Carrie through the normal agent-side BoldTrail CMS (bio text, photos, etc.) — they are template/platform-level and require eXp's marketing tech / BoldTrail support team. Below is one cover message plus four discrete, reproducible tickets. Submit as one ticket with four numbered sections, or as four separate tickets, whichever eXp's support portal handles better for tracking — the content is written to work either way.

---

## Cover paragraph (paste-ready, send from Carrie's account)

> Hi eXp/BoldTrail Support team,
>
> I'm writing about four technical SEO issues on my agent site, https://carriebilleaud.exprealty.com, that I believe are template-level (not something I can fix from my agent dashboard). I've documented each one below with the exact URL, what's currently happening, and what I'd expect instead, so your team can reproduce and confirm quickly. These affect how search engines and AI answer-engines (Google, Bing, ChatGPT/Claude/Perplexity-style crawlers) can find and index my site, so I'd appreciate a fix or an explanation of whether these are configurable per-agent. Happy to hop on a call if that's faster. Thank you!
>
> — Carrie Billeaud

---

## Issue 1: robots.txt blocks unnamed crawlers site-wide (duplicate `User-agent: *` group)

**URL to check:** `https://carriebilleaud.exprealty.com/robots.txt`

**What's happening (current, verified 2026-07-08):**
The file contains two separate blocks for `User-agent: *`. The first block disallows only specific paths (e.g. `/emails_kvarea/`, `/wp-admin/`, IDX query parameters). A second, later block reads:
```
User-agent: *
Disallow: /
```
Per Google's own documented robots.txt parsing rules, multiple groups that share the same user-agent token are merged together — so the effective rule for the generic `*` group becomes "disallow everything." Only crawlers explicitly named elsewhere in the file (Googlebot, Googlebot-Mobile, bingbot, Slurp, msnbot, Twitterbot, facebookexternalhit, AdsBot-Google, Mediapartners-Google, PowerMapper, Screaming Frog, SemrushBot, TermlyBot) get their own `Allow: /` group and escape the block. Every other crawler — including AI answer-engine bots such as ClaudeBot, GPTBot, PerplexityBot, Google-Extended, Applebot, YandexBot, DuckDuckBot, CCBot, and Bytespider — is currently disallowed from the entire site.

**What we'd expect instead:**
A single, consolidated `User-agent: *` group containing only the intended path exclusions, with no trailing global `Disallow: /`. If a sitewide block was intentional for some other reason, please confirm — otherwise please remove the second `User-agent: *` / `Disallow: /` block.

**How to reproduce (under 2 minutes):**
1. Fetch `https://carriebilleaud.exprealty.com/robots.txt` directly in a browser or via `curl`.
2. Confirm there are two separate `User-agent: *` blocks in the file.
3. Confirm the second one contains `Disallow: /` with no `Allow` override for the generic group.
4. Optionally verify against Google's robots.txt testing tool (Search Console > robots.txt Tester, or the public documentation on group-merging behavior) to confirm the effective merged rule blocks the `*` group entirely.

---

## Issue 2: Canonical tags point to exprealty.com instead of my agent subdomain

**URLs to check:**
- `https://carriebilleaud.exprealty.com/agents.php` (canonical currently renders as `https://exprealty.com/agents/1172379/Carrie+Billeaud`)
- Any blog post, e.g. `https://carriebilleaud.exprealty.com/blog/375489/Modern+Farmhouse+Living...` (canonical currently renders as `https://exprealty.com/blog/375489/...`)
- Homepage `https://carriebilleaud.exprealty.com/` (no canonical tag present at all)

**What's happening (current, verified 2026-07-08):**
View source / inspect the rendered `<head>` on the agent profile page and any blog post — the `<link rel="canonical">` tag points to the corporate `exprealty.com` domain, not to my own branded subdomain `carriebilleaud.exprealty.com`. This tells Google the "real," authoritative version of each page lives on the corporate site, which undermines my own site's ability to rank for my own content. The homepage has no canonical tag at all.

**What we'd expect instead:**
Each page's canonical tag should be self-referencing — pointing to its own URL on `carriebilleaud.exprealty.com`, not to `exprealty.com`. Please confirm whether "self-canonical" is a configurable setting per agent site, and if so, enable it for my site. If it's not configurable, please let me know and I'll escalate through my broker.

**How to reproduce (under 2 minutes):**
1. Open `https://carriebilleaud.exprealty.com/agents.php` in a browser, view page source (or use a rendered-DOM inspector, since this may be JS-injected).
2. Search for `rel="canonical"` and confirm the `href` value points to `exprealty.com`, not `carriebilleaud.exprealty.com`.
3. Repeat on any published blog post URL.
4. Load the homepage and confirm no canonical tag is present at all.

---

## Issue 3: Conflicting dual meta-robots tags (static `index,follow` vs. rendered `noindex,nofollow`)

**URLs to check:**
- `https://carriebilleaud.exprealty.com/agents.php`
- Any blog post, e.g. `https://carriebilleaud.exprealty.com/blog/375489/Modern+Farmhouse+Living...`

**What's happening (current, verified 2026-07-08):**
Two conflicting meta robots tags render in the same document: `<meta name="robots" content="index,follow">` appears in the static `<head>`, but a second tag, `<meta name="robots" content="noindex, nofollow">`, is injected later into the rendered DOM — it appears co-located with Cloudflare Turnstile / CSP script tags, suggesting it comes from the bot-challenge widget bundle rather than the page template itself. Google's stated behavior when multiple robots directives exist on one page is to honor the most restrictive one, meaning the rendered `noindex` can suppress indexing of this page even though the static HTML says `index,follow`.

**What we'd expect instead:**
Only one meta-robots directive per page, matching the intended indexing state (`index,follow` for the agent profile and blog posts, since these are meant to rank). If the Cloudflare Turnstile/bot-challenge bundle is the source of the injected `noindex,nofollow` tag, please either remove that injection for real visitors/crawlers or confirm it only fires for actual bot-challenge states (not for normal page loads, including Googlebot's rendering pass).

**How to reproduce (under 2 minutes):**
1. Load `https://carriebilleaud.exprealty.com/agents.php` in a browser with dev tools open.
2. View page source (static HTML) — note the `<meta name="robots">` tag reads `index,follow`.
3. Inspect the live rendered DOM (Elements panel, not view-source) — note a second `<meta name="robots">` tag reads `noindex, nofollow`, typically near Turnstile/CSP-related script tags.
4. Repeat on a blog post URL to confirm the same pattern.
5. Optionally cross-check actual indexing status in Google Search Console's URL Inspection tool once Search Console access is set up (see `tracking_setup_kit.md`).

---

## Issue 4: `/sitemap.xml` returns 404 instead of pointing to the real sitemap

**URLs to check:**
- `https://carriebilleaud.exprealty.com/sitemap.xml` (currently 404)
- `https://carriebilleaud.exprealty.com/sitemap-index.xml` (currently 200 OK — this is the real, working sitemap index)

**What's happening (current, verified 2026-07-08):**
`robots.txt` correctly references `sitemap-index.xml`, and that file works fine (200 OK, references fresh `sitemap-structure-1.xml.gz`, `sitemap-areas-1.xml.gz`, and `sitemap-listings-1.xml.gz`, all dated 2026-07-08). However, the conventional location most tools and humans check first, `/sitemap.xml`, returns a 404 and is served the site's generic "Page Not Found" template. This isn't breaking indexing today since the correct sitemap is referenced in robots.txt, but any SEO tool, auditor, or person manually checking the standard `/sitemap.xml` path finds nothing, which looks broken and can trigger false-positive "no sitemap found" flags in third-party tools.

**What we'd expect instead:**
`/sitemap.xml` should either 301-redirect to `/sitemap-index.xml`, or directly serve the same sitemap index content, so the conventional URL isn't a dead end.

**How to reproduce (under 2 minutes):**
1. Fetch `https://carriebilleaud.exprealty.com/sitemap.xml` directly — confirm it returns HTTP 404 and the site's "Page Not Found" template.
2. Fetch `https://carriebilleaud.exprealty.com/sitemap-index.xml` — confirm it returns HTTP 200 with valid sitemap-index XML content.
3. Confirm `robots.txt` references `sitemap-index.xml` (not `sitemap.xml`).

---

## Notes for whoever submits this

- If the support portal requires one issue per ticket, submit Issues 1–4 as separate tickets but keep the cover paragraph as the opening message on the first one, or a shortened version ("this is 1 of 4 related tickets, see also #___") on the others.
- Reference this being reported by the site owner/agent (Carrie), not a third-party — some support queues deprioritize tickets that don't come from the account holder.
- Ask specifically whether these are: (a) a bug the platform will fix globally, (b) a per-agent configurable setting Carrie can toggle herself once pointed to it, or (c) intentional platform behavior that won't change — getting a clear answer on which bucket each issue falls into determines whether this needs re-escalation or is closed for good.
