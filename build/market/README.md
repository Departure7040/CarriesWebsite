# Market-report engine

Turns **real Acadiana MLS numbers** (supplied by Carrie) into three synchronized
outputs from **one** source file:

1. a branded monthly **PDF market report** (`site/market/acadiana-market-report-<YYYY-MM>.pdf`)
2. a studio-style **social content package** (`site/studio/packages/market/<YYYY-MM>.json` + `-ready-to-post.md`)
3. the **lead-magnet landing page** (`site/market/index.html`) that links the PDF and captures emails

## THE ONE RULE: never fabricate a statistic

Every number in every output is read **only** from `data/market/<period>.yaml`.
There are **zero** hardcoded statistics in the HTML template or the build scripts.

- A metric missing from the YAML renders as an **em-dash (`—`)** — never a guess.
- The captions only cite metrics actually present in the YAML.
- The shipped demo file (`data/market/2026-07-sample.yaml`) carries `sample: true`,
  which stamps a visible **"SAMPLE — illustrative data"** ribbon on the PDF,
  marks every caption as illustrative, and shows a SAMPLE note on the landing page.
- The data `source` is always labeled. While it is still `__FILL__`/blank, the copy
  says **"(source pending)"** rather than naming an unverified source.
- Do **not** pull in `data/known_claims.yaml` figures (e.g. `sales_volume`) — those
  are UNVERIFIED and must never appear as fact.

## Data-in → report/posts/landing-out

```
data/market/<period>.yaml   (the ONLY source of numbers)
        │
        ├── build/market/build_report.py ──────► site/market/acadiana-market-report-<YYYY-MM>.pdf
        │        (fills build/market/market-report-print.html, renders via Playwright)
        │
        └── build/market/build_market_posts.py ► site/studio/packages/market/<YYYY-MM>.json
                                                  site/studio/packages/market/<YYYY-MM>-ready-to-post.md

site/market/index.html  (landing page) links the PDF + captures emails → /api/lead
```

## How to run

Requires **Python** with **PyYAML** and **Playwright** (Chromium) installed —
Playwright is already used by the ebook/social builders; PyYAML is the one new
dependency (`pip install pyyaml`, plus `python -m playwright install chromium`
if the browser isn't present).

```bash
# 1. Edit the data file with REAL MLS numbers (or keep sample:true for the demo).
#    Copy to a new period file for each month, e.g. data/market/2026-08.yaml.

# 2. Build the PDF report:
python build/market/build_report.py                      # uses 2026-07-sample.yaml
python build/market/build_report.py data/market/2026-08.yaml

# 3. Build the social content package:
python build/market/build_market_posts.py                # uses 2026-07-sample.yaml
python build/market/build_market_posts.py data/market/2026-08.yaml
```

Both scripts are re-runnable and print a summary (source file, sample flag,
period, attribution, output paths).

## The YAML contract

`build_report.py` and `build_market_posts.py` read a fixed set of metric keys.
If Carrie's real export uses different metric names, keep the token map in the
scripts in sync with the YAML. Expected keys:

| Top-level        | Meaning                                   |
|------------------|-------------------------------------------|
| `sample`         | `true` → SAMPLE ribbon + illustrative copy |
| `disclaimer`     | printed on the PDF disclaimer page         |
| `period`         | e.g. `"July 2026"` → filename slug `2026-07` |
| `area`           | e.g. `"Acadiana / Lafayette Parish"`       |
| `source`         | data attribution; `__FILL__` → "(source pending)" |
| `metrics.*`      | area-wide headline metrics (see below)     |
| `by_area.<Town>.*` | same metric keys, per town               |

Metric keys (any may be omitted → renders as `—`):
`median_sale_price`, `avg_days_on_market`, `active_inventory`, `closed_sales`,
`months_of_supply`, `median_price_per_sqft`.

## Per-month notes

- The PDF filename embeds the period (`acadiana-market-report-2026-07.pdf`). A new
  month means a **new file** — the landing-page download link (and any nav/tile
  reference) points at the current month's file and must be updated per month.
- The landing form posts `source="market-report"` with `utm_campaign="market-report"`.
  `functions/api/lead.js` already accepts an arbitrary `source` + the attribution
  fields, so no Function change is needed.

## Compliance (reused from `functions/api/_content_system_prompt.md`)

The "what this means for buyers & sellers" prose and every caption restate the
supplied numbers as **facts only**. Absolute bans, mirrored from the content
system prompt:

1. **No steering / fair-housing-sensitive language** — no "family-friendly",
   "safe", "good/bad schools", "great neighborhood", "up-and-coming", or "who
   it's right for".
2. **No unverified stats** — only numbers present in the YAML; nothing from
   `known_claims.yaml`.
3. **No guarantees / predictions / rates** — no "great time to buy", "prices will
   rise", "sell fast", mortgage rates, or "#1 agent". Descriptive present-tense
   reporting only.
4. **Nothing auto-sends / auto-posts** — the scripts only write files; publishing
   stays manual, Carrie approves everything; the landing form captures opt-in
   leads via the existing consented `/api/lead` flow.
