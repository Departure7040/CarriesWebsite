# Workflow 04 — Competitor Gap Analysis

**Delegate to:** `agents/competitor_researcher.md` (cheap model, web search)

## Queries (from /data/competitor_queries.yaml)
- Lafayette LA realtor / best realtor Lafayette LA / real estate agent Lafayette LA
- top realtor Lafayette LA / listing agent Lafayette LA / buyer agent Lafayette LA
- first time home buyer realtor Lafayette LA
- Youngsville LA realtor / Broussard LA realtor / Acadiana realtor
- eXp Realty Lafayette realtor

## Steps
1. Run each query via available web search. Capture visible competitors from
   organic results; note map/local-pack entries only if actually visible.
2. Check Zillow / Realtor.com / Homes.com agent directories for Lafayette
   top-reviewed agents.
3. For top 5–8 recurring competitors, capture: reviews count/rating/recency,
   website quality, local landing pages, profile completeness, content depth,
   third-party platform strength.
4. Identify common traits of winners (the "table stakes" list).
5. Build gap matrix: Carrie vs competitors per factor.
6. Write "how to beat them" section — realistic, prioritized.

## Constraints
- No scraping in violation of site terms; use search results and public pages.
- If live SERP/local-pack data is blocked or personalized, say so and include
  a manual research checklist for Brook to run from a Lafayette IP/device.

## Outputs
- `/data/competitor_snapshot.csv`
- `/reports/04_competitor_gap_analysis.md`
