# 05 — AI Search Visibility Plan

**Subject:** Carrie Billeaud, REALTOR®, eXp Realty — Lafayette/Acadiana, LA
**Date:** 2026-07-08
**Frame:** AI search visibility is not a separate discipline with its own tricks. It is the downstream result of three things done well: **entity clarity** (every surface agrees on who Carrie is), **authority** (independent, verifiable signals that she's real and good at her job), and **useful crawlable content** (pages a machine can actually read and quote). This report builds directly on the entity data gathered in `01_public_presence_inventory.md` / `data/nap_consistency_matrix.csv` (WF01) and the technical crawl findings in `03_website_technical_audit.md` (WF02).

**No gimmicks.** This plan contains no fake mentions, no fabricated citations, no llms.txt pitched as a ranking tactic, no AI-generated spam pages, and no incentivized/gated reviews. Every recommendation is either standard entity/SEO hygiene or genuinely useful content.

---

## 1. How AI search actually picks a real estate agent

Two different systems are worth separating, because they're commonly conflated.

**Google AI Overviews and AI Mode** are not a separate index — they're a generative layer sitting on top of regular Google Search and the Knowledge Graph. They surface an agent the same way classic Search does: by pulling from pages Google has crawled, indexed, and judged trustworthy, plus structured entity data (Knowledge Panels, Local Pack / Google Business Profile signals, review aggregators). If a page isn't indexed, isn't crawlable, or the entity behind it is ambiguous, AI Overviews has nothing reliable to synthesize from and will fall back to whatever generic, aggregated portal content ranks instead (Zillow, Realtor.com, Homes.com) — which, notably, Carrie already has reasonably strong profiles on.

**ChatGPT-style assistants** (ChatGPT browsing/search, Perplexity, Claude with web search, etc.) work differently: they run live web searches and/or rely on crawled snapshots, then read whatever pages they can actually fetch. They have a strong preference for content that is unambiguous, well-structured, and consistent across multiple independent sources, because consistency is their proxy for "this is true." An assistant asked "who is a good realtor in Lafayette, LA specializing in first-time buyers" is effectively doing a mini fact-check across whatever sources it can reach — if those sources disagree on Carrie's phone number, address, or credentials, or if her own website is invisible to the bot doing the fetching, she simply won't be cited, not because she isn't qualified, but because the machine can't confirm who she is.

Both paths converge on the same requirement: **be crawlable, be consistent, be backed by independent evidence.** There is no separate "AI SEO" trick that substitutes for these fundamentals — anyone claiming otherwise is selling gimmicks the framing above explicitly rules out.

---

## 2. Current-state scorecard

| Dimension | Verdict | Evidence |
|---|---|---|
| **Entity consistency (NAP + credentials)** | **Poor** | 3 distinct phone numbers (337-258-5379 primary; (337) 341-8976 Homes.com; (337) 522-7554 LoopNet), 5 distinct addresses across sources, 3 distinct emails (personal Gmail, exprealty.com domain, "Southern Collective Group" Gmail), name presented as "Carrie Billeaud," "Carrie Billeaud Team," and "Carrie Billeaud-Realtor EXP Realty" depending on platform, ICON Agent claim varies 2x (Zillow, Nextdoor) vs. 3x (Facebook). All [verified] in `data/nap_consistency_matrix.csv` and `01_public_presence_inventory.md`. |
| **Crawlability to AI bots** | **Blocked (site-wide)** | `robots.txt` on carriebilleaud.exprealty.com contains a duplicate `User-agent: *` group; the trailing group is `Disallow: /`. Per documented robots.txt parsing behavior, same-named groups merge, so any bot not explicitly named (ClaudeBot, GPTBot, PerplexityBot, Google-Extended, Applebot, CCBot, Bytespider, etc.) is disallowed from the entire site. Only Googlebot, Bingbot, and a handful of other explicitly-named bots get an `Allow: /`. [verified, `03_website_technical_audit.md`] |
| **Structured data (schema.org / JSON-LD)** | **Absent** | Zero JSON-LD anywhere on the site — no `RealEstateAgent`, `Person`, `LocalBusiness`, `BreadcrumbList`, `BlogPosting`, or `FAQPage` schema found on homepage, agent profile, area page, or blog post. [verified] |
| **Authority signals (third-party)** | **Moderate** | Real strengths: Zillow individual profile — 29 reviews, 5.0★, strong bio [verified]; Facebook page — 5,550 likes, 142 talking-about [verified via search snippet, page itself blocked from full audit]; strong, detailed bios on Homes.com, Realtor.com, Nextdoor, LoopNet [verified]. Weaknesses: zero Google Business Profile (the single highest-authority local entity source) [verified — not found], low review counts on Realtor.com (2) and none on Homes.com/LoopNet despite strong bio content there, no evidence yet of local press or association features beyond a stated RAA membership [unverified]. |
| **Contactability clarity** | **Confused** | A visitor or an AI system trying to answer "how do I reach Carrie Billeaud" gets three different phone numbers and three different email addresses depending on which source they land on, with no canonical designation anywhere. [verified] |
| **Owned-site entity content** | **Missing, not just weak** | The one page designed to be the entity anchor — `/agents.php`, "About Carrie" — has no bio text at all, just a lead form. Canonical tags on `/agents.php` and blog posts point off-domain to `exprealty.com` instead of `carriebilleaud.exprealty.com`, actively telling search/AI crawlers the branded domain isn't the authoritative source. [verified] |

**Bottom line:** Carrie has the raw material for AI visibility (real reviews, real bios, a real specialty and service area) scattered across third-party platforms, but her own site is currently unreadable by AI crawlers, contains no entity anchor content, and the entity data that does exist across the web contradicts itself on the basics (name, phone, address, credential count). An AI system trying to build a confident answer about her today would either find nothing (blocked) or find conflicting signals (inconsistent) — both outcomes suppress citation.

---

## 3. Fix plan — mapped to the five questions an AI must answer

An AI system (or a human skimming search results) is implicitly trying to answer five questions before it will confidently surface or cite an agent. Below is the fix for each, in Carrie's actual situation.

### WHO is she?
- Standardize the name used everywhere to a single form: **"Carrie Billeaud"** (drop "Carrie Billeaud Team" and "Carrie Billeaud-Realtor EXP Realty" as the *primary* label; the team brand and platform-generated suffix can remain as secondary/team-specific listings, but the individual entity name should be identical across profiles).
- Write one canonical bio (300-500 words) — background, license, brokerage, years of experience, specialties, personal note — and republish consistent (not copy-pasted, but consistent in facts) versions on: the eXp/BoldTrail "About Carrie" section (currently empty — highest-leverage single fix, see Section 4), Zillow, Realtor.com, Homes.com, Nextdoor, LinkedIn, Facebook.
- This bio is the raw text an AI system paraphrases when asked "who is Carrie Billeaud" — right now that text doesn't exist on her own site at all.

### WHERE does she serve?
- Publish one explicit, identical service-area statement site-wide and across profiles: the ~20 Acadiana-area cities already tracked as consistent across sources in `01_public_presence_inventory.md` (Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, Milton, Abbeville, Broussard, New Iberia, Opelousas, etc.) [verified — coverage list already consistent, this is a formatting/publication fix, not a data-gathering one].
- State it as a plain sentence near the top of the bio ("Carrie serves buyers and sellers across Lafayette and the greater Acadiana region, including Youngsville, Broussard, Carencro..."), not just as a sidebar list — plain-language sentences are what get quoted/paraphrased by generative systems, not bare lists.

### WHAT does she specialize in?
- Collapse the varying specialty lists (4 on Realtor.com, 5 on Homes.com/eXp, 6 on Zillow individual, 10 on Zillow Team) into one canonical short list of true specialties, then use that same list everywhere. Recommend [client-confirm]: which of residential/first-time buyers/investment-rental/luxury/relocation/land/commercial are genuinely her focus vs. team-level breadth that shouldn't be attributed to the individual profile.
- A shorter, consistent, and true list is more useful to an AI system than a longer, inconsistent one — specificity signals authority; breadth-without-consistency reads as template noise.

### WHY is she credible?
- Only publish metrics that are independently verifiable or client-confirmed. The strongest verified credibility signal today is the **Zillow 29 reviews / 5.0★** [verified] — this should be the anchor proof point cited everywhere, including on her own site, which currently displays zero reviews.
- The high-impact production claims currently seen only on Homes.com/LoopNet — **174 closed sales, $44.6M total sales volume, 11 years of experience, ICON Agent status** — are flagged in `data/known_claims.yaml` as `status: unverified` and must be tagged **[client-confirm]** before use in any new marketing copy. Until Carrie confirms exact figures and the correct ICON multiplier (2x vs. 3x discrepancy between Facebook and Zillow/Nextdoor), do not introduce these numbers onto the site or into schema markup — publishing an unverifiable number an AI system later can't corroborate against other sources is a self-inflicted consistency problem, the exact failure mode this report is trying to fix.
- Add (or confirm and surface) the Realtor Association of Acadiana membership referenced in the LinkedIn snippet [inferred, low confidence] — professional association membership is a strong, easily-verifiable authority signal AI systems weight favorably.

### HOW to contact her?
- Pick **one** canonical phone, **one** canonical email, and **one** canonical business address (this requires an explicit [client-confirm] decision from Carrie — the audit found 3 phones / 5 addresses / 3 emails and cannot pick one on her behalf). Once decided:
  - Update every owned and controllable third-party profile to match (eXp site, Zillow individual + team, Realtor.com, Homes.com, Nextdoor, LoopNet, Facebook, LinkedIn, Instagram, Google Business Profile once created).
  - The Homes.com phone `(337) 341-8976` and LoopNet phone `(337) 522-7554` are the two clearest outliers and should be corrected or explicitly explained (e.g., if 522-7554 is legitimately an office line, label it as such rather than presenting it as her direct number).

---

## 4. Technical prerequisites (cross-reference WF02 / `03_website_technical_audit.md`)

These are the gate an AI crawler has to get through before any of the entity-clarity work above can even be read. All three are template-level BoldTrail/eXp platform issues, not agent-editable in the CMS — they require a support ticket, not a content edit.

1. **Fix `robots.txt`.** The trailing duplicate `User-agent: *` / `Disallow: /` group must be removed or merged so it stops blocking every unnamed crawler. This is the single highest-priority technical fix in this entire engagement — no amount of good bio content or schema matters if ClaudeBot, GPTBot, PerplexityBot, and Google-Extended are all disallowed from fetching the site at all. [verified blocker, `03_website_technical_audit.md` P1]
2. **Add JSON-LD schema.** At minimum: `RealEstateAgent`/`Person` schema on `/agents.php` with `name`, `telephone`, `email`, `areaServed`, `knowsAbout` (specialties), and a `sameAs` array pointing to every verified profile (Zillow, Realtor.com, Homes.com, Nextdoor, LoopNet, LinkedIn, Facebook, Instagram, and Google Business Profile once created). The `sameAs` array is the direct, standard mechanism by which search/AI systems tie together a single entity across multiple web presences — this is the technical backbone that makes "entity consistency" machine-readable rather than just human-readable. Add `BlogPosting` schema to blog content and `LocalBusiness` for the brokerage/service area once schema support exists. [verified gap, template-level]
3. **Fix the canonical tag.** `/agents.php` and blog posts currently canonicalize to `exprealty.com` instead of `carriebilleaud.exprealty.com`, telling search engines Carrie's own branded domain isn't authoritative. This must point to the branded domain for any of her owned content to accrue ranking or citation credit in its own right. [verified, `03_website_technical_audit.md` P1]

Two secondary items worth flagging alongside these: the dual conflicting meta-robots tags (`index,follow` in static HTML vs. a rendered `noindex, nofollow` injected near the Cloudflare Turnstile widget) risk suppressing indexing outright and should be resolved in the same support request; and Cloudflare's bot-challenge mode currently returns HTTP 403 to any non-JS-rendering request, which may affect AI crawlers that don't execute JavaScript even after the robots.txt fix — worth explicit confirmation from BoldTrail support that legitimate AI/search crawler ranges are allowlisted, not just Googlebot/Bingbot.

---

## 5. Content structures AI systems actually cite

Once the site is crawlable and the entity is unambiguous, the content itself needs to be in a form generative systems can lift and paraphrase directly. Three structures matter most:

- **FAQ-style local content.** Direct question-and-answer pairs ("How much does it cost to sell a house in Lafayette, LA?", "What's the process for a first-time buyer in Acadiana?") are the single most citable content format for both AI Overviews and chat-style assistants, because the Q&A structure maps almost one-to-one onto how these systems phrase their own answers. This pairs with `FAQPage` schema (Section 4) to make the structure machine-explicit as well as visually clear.
- **Plain-language local market pages.** The site's current `/areas/*` pages are IDX-generated, `noindex`, and contain no agent voice — appropriately excluded from indexing since they're thin/templated, but that also means they produce zero AI-citable content. A small number of genuinely agent-written market pages (not IDX search-result pages) — e.g., "Buying a home in Youngsville, LA" with real neighborhood knowledge, price context, and Carrie's own commentary — are the kind of unique, first-hand content both classic SEO and AI summarization systems reward, and are explicitly the model already used successfully in the "Modern Farmhouse Living" blog post flagged as genuinely useful in the WF02 audit.
- **The 7-page-brief content pipeline** already scoped in `agents/content_strategy_agent.md` / WF06 (output: `/content/page_briefs/*.md` and `/reports/06_content_strategy.md`, not yet populated as of this report). Each brief in that pipeline is required to include an FAQ section and a schema recommendation by design — meaning the content strategy and AI-visibility work are meant to land as one coordinated deliverable, not two separate efforts. Recommend sequencing: fix crawlability and schema (Section 4) first, then populate those 7 briefs, since AI-citable content published behind a robots.txt block accomplishes nothing.

---

## 6. Realistic expectations

This is months, not days, and no one — including this report — can guarantee inclusion in any specific AI Overview, ChatGPT answer, or Knowledge Panel. Google's crawl-to-reindex cycle for a site of this size typically takes weeks after a technical fix like the robots.txt correction; schema additions take additional time to be parsed, trusted, and (if eligible) surfaced as rich results; and third-party platforms (Zillow, Realtor.com, GBP once created) each have their own independent update and re-indexing cadence. AI answer engines built on top of these systems inherit those same delays, plus their own crawl schedules, which for some tools (Perplexity, ChatGPT search) are not publicly documented and cannot be forced or expedited. The honest framing for Carrie: these fixes remove the barriers currently preventing visibility and put real, verifiable, differentiated content in front of the systems that decide who gets cited — they do not purchase a guaranteed outcome, and anyone promising a specific citation or ranking on a specific timeline is not being straight with her.

---

## 7. Prioritized action table

| Priority | Action | Type | Owner | Blocked by |
|---|---|---|---|---|
| P1 | File support ticket to remove/merge the trailing `Disallow: /` robots.txt group | Technical | Carrie → BoldTrail/eXp support | — |
| P1 | Write real bio for `/agents.php` "About Carrie" (300-500 words; verified facts only) | Content | Carrie/agency (site is agent-editable here) | [client-confirm] on production stats |
| P1 | [Client-confirm] canonical phone, email, and mailing/business address | Data decision | Carrie | — |
| P1 | [Client-confirm] verified production numbers (174 sales/$44.6M/11 yrs) and correct ICON multiplier (2x vs 3x) | Data decision | Carrie | — |
| P2 | Standardize name, bio facts, specialty list, and service-area statement across all owned/editable profiles (Zillow, Realtor.com, Homes.com, Nextdoor, LoopNet, LinkedIn, Facebook) | Content/entity | Carrie/agency | P1 data decisions |
| P2 | Create Google Business Profile using confirmed canonical NAP | Entity/local | Carrie/agency | P1 address decision |
| P2 | File support ticket to fix canonical tags (point to carriebilleaud.exprealty.com) and resolve dual meta-robots conflict | Technical | Carrie → BoldTrail/eXp support | — |
| P2 | Request `RealEstateAgent`/`Person` JSON-LD with `sameAs` array to all verified profiles | Technical | Carrie → BoldTrail/eXp support | P2 profile standardization (need final URLs) |
| P3 | Correct/clarify Homes.com and LoopNet phone number conflicts in platform admin | Data hygiene | Carrie | P1 canonical phone decision |
| P3 | Produce 7 page briefs (WF06) with FAQ sections and schema recommendations; publish 1-2 genuinely local, agent-voiced market pages | Content | agency (content_strategy_agent) | P1 robots.txt fix (publishing before crawlability is fixed wastes the content) |
| P3 | Confirm Cloudflare allowlists legitimate AI/search crawler ranges, not just Googlebot/Bingbot | Technical | Carrie → BoldTrail/eXp support | P1 robots.txt fix |
| P4 | Audit Instagram/TikTok/YouTube presence (currently unverified/blocked from this audit) | Research | agency | — |

---

*All findings above are cross-referenced to `01_public_presence_inventory.md`, `data/nap_consistency_matrix.csv`, `data/known_claims.yaml`, and `03_website_technical_audit.md`. No claim in this report that is tagged [client-confirm] should be published as fact until confirmed by Carrie.*
