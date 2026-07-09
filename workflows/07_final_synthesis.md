# Workflow 07 — Final Synthesis & QA

**Owner:** Fable. **QA delegate:** `agents/qa_fact_checker.md`

## Steps
1. Fable reads all reports + data files; resolves contradictions with evidence
   or marks them [client-confirm].
2. qa_fact_checker reviews every report: unsupported claims, broken/missing
   source URLs, unrealistic or unethical recommendations, priority sanity.
   Output: `/reports/qa_notes.md`.
3. Fable addresses QA flags, then writes client-facing deliverables:
   - `/reports/00_client_brief.md` — plain-English exec summary; "good raw
     materials, under-optimized public SEO/entity layer"; 5 highest-impact
     opportunities; 5 things NOT to spend money on; immediate client requests.
   - `/reports/07_30_60_90_day_plan.md`
   - `/reports/08_scope_and_pricing_options.md` (placeholder pricing, marked)
   - `/reports/09_questions_for_client.md`
4. Final tone check: direct, friendly, practical. No hype, no fake certainty,
   no guaranteed rankings, no unexplained jargon.
5. Commit and push everything to GitHub.

## Definition of done
- All checklist items in WF00 checked.
- Every report claim tagged with evidence level.
- QA notes exist and blocking flags are resolved.
