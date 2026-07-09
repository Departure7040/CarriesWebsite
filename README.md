# Carrie Billeaud — Local SEO & AI Search Visibility Audit

Practical SEO, local search, AI-search visibility, and lead-generation audit for
**Carrie Billeaud, Realtor (eXp Realty)** — Lafayette, Louisiana & Acadiana.

## Goal
Determine how Carrie can generate more organic real estate leads from:
- Google Search
- Google Maps / local pack
- Google AI Overviews / AI Mode
- ChatGPT / AI search surfaces
- Third-party real estate platforms (Zillow, Realtor.com, Homes.com)
- Local Lafayette / Acadiana search intent

## Repo layout

| Path | Purpose |
|---|---|
| `/workflows/` | Orchestrator runbooks (executed in order 00 → 07) |
| `/agents/` | Subagent role definitions (research, audit, content, QA) |
| `/data/` | Structured evidence: public assets, NAP matrix, source log, competitor data |
| `/reports/` | Client-facing and internal audit reports |
| `/backlog/` | Prioritized SEO task backlog (CSV) |
| `/content/` | Page briefs, review templates, GBP posts, social repurposing |

## Evidence standard
Every claim in reports is tagged with one of:
- **[verified]** — verified from public source (URL in `/data/source_log.csv`)
- **[inferred]** — inferred from available evidence
- **[client-confirm]** — needs client confirmation
- **[best-practice]** — recommended best practice

## Hard rules
- No access is assumed to Google Business Profile, Search Console, GA4, or CRM.
  Missing access items go to `/reports/09_questions_for_client.md`.
- No black-hat tactics: no fake reviews, bought backlinks, doorway pages,
  AI-spam pages, keyword stuffing, or fabricated citations.
- AI search visibility = entity clarity + authority + useful crawlable content.

## Execution status
See `/workflows/00_fable_orchestrator_plan.md` for the execution checklist.
