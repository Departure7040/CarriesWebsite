# Workflow 00 — Fable Orchestrator Plan

**Owner:** Fable (orchestrator). Fable plans, coordinates, verifies, resolves
contradictions, and writes final client-ready synthesis. All detailed research,
crawling, extraction, and drafting is delegated to subagents on the cheapest
adequate model.

## Success criteria
1. Complete public presence inventory with NAP consistency matrix and every
   conflict flagged (not silently resolved).
2. Website technical audit separating "fixable now" from "platform-limited
   (eXp / BoldTrail / IDX)".
3. GBP optimization checklist + review strategy usable even without GBP access.
4. Competitor gap analysis with a concrete "how to beat them" section.
5. AI search visibility plan framed as entity clarity + authority + crawlable
   content — no gimmicks.
6. Content plan with complete page briefs (query cluster, intent, title, meta,
   H1, outline, internal links, CTA, trust signals, FAQ, schema).
7. Client-facing brief, 30/60/90 plan, pricing options, and question list.
8. Every claim tagged: [verified] / [inferred] / [client-confirm] / [best-practice].
9. QA pass completed; unsupported claims flagged in /reports/qa_notes.md.

## Model routing policy
| Task | Model tier |
|---|---|
| Web recon, extraction, crawling | cheapest adequate (Haiku) |
| Report drafting, page briefs | mid (Sonnet) |
| Synthesis, contradiction resolution, QA verdicts, final client docs | Fable |

## Execution checklist
- [x] Repo structure created
- [x] Workflow + agent definitions written
- [x] Data schemas created (source log, backlog, NAP matrix, competitor CSV)
- [x] Known public assets populated from provided URLs
- [x] WF01 — Public presence recon (public_presence_researcher)
- [x] WF02 — Website crawl & technical SEO (technical_seo_auditor)
- [x] WF03 — Local SEO / GBP audit (local_seo_analyst)
- [x] WF04 — Competitor gap analysis (competitor_researcher)
- [x] WF05 — AI search visibility (ai_search_visibility_agent)
- [x] WF06 — Content & conversion plan (content_strategy_agent + conversion_tracking_agent)
- [x] WF07 — Final synthesis + QA (Fable + qa_fact_checker)
- [x] Push all work to https://github.com/Departure7040/CarriesWebsite.git
- [x] EXTRA — WF04b SERP patterns & reuse research (client-requested)
- [x] EXTRA — GBP correction: profile EXISTS (185 reviews, 5.0) — client-verified 2026-07-08
- [x] EXTRA — Client-facing audit/demo site built in /site (9 pages, noindex, self-hosted via Cloudflare tunnel)

## Contradiction handling
Known conflicts to resolve with evidence (never guess):
- Phone: 337-258-5379 vs 337-522-7554 (LoopNet)
- Address: 1720 Kaliste Saloom Ste B 2 vs 3 Flagg Place Bldg B Suite B-4 (both Lafayette 70508)
- Metrics: 174 closed sales / $44.6M (Homes.com), 11 yrs experience (Realtor.com),
  50+ families/yr (Instagram), eXp Icon Agent — all [client-confirm] until verified.

## Context discipline
Subagents return structured summaries only (facts + URLs + confidence), never
raw page dumps. Fable reads summaries and data files, not source HTML.
