# Workflow 01 — Public Presence Recon

**Delegate to:** `agents/public_presence_researcher.md` (cheap model, web tools)

## Steps
1. Visit every URL in `/data/public_assets.yaml`. For each, extract:
   name-as-shown, phone, address, brokerage, email, website links, bio text
   presence/quality, service areas, specialties, review count/rating,
   credentials, social links, claims (sales volume, years, awards).
2. Log every source in `/data/source_log.csv` with confidence + date.
3. Fill `/data/nap_consistency_matrix.csv` — one row per source.
4. Flag conflicts explicitly (phone, address, business name variants). Do NOT
   resolve conflicts; mark `needs_update = VERIFY`.
5. Search for a Google Business Profile / Google Maps listing. If none found,
   record "GBP not found — client must confirm ownership/existence".
6. Identify which profiles link back to the primary website and which don't.
7. Recommend a canonical primary URL choice (with reasoning, marked [inferred]).

## Outputs
- `/data/public_assets.yaml` (updated with findings)
- `/data/source_log.csv`
- `/data/nap_consistency_matrix.csv`
- `/reports/01_public_presence_inventory.md` (draft)

## Return to orchestrator
Structured summary only: per-source facts table, conflict list, missing-profile
list, GBP status. No raw HTML.
