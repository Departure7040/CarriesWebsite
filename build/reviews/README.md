# Review Syndication Engine

Turns Carrie Billeaud's **real, already-visible** testimonials into three things:

1. **Richer SEO** — individual `schema.org/Review` JSON-LD (for ⭐ rich-snippet eligibility),
   injected *in addition to* the existing `AggregateRating`.
2. **Branded social graphics** — luxury "Client Love" quote cards (1080×1080 + 1080×1920).
3. **New reviews** — a compliant, personalized post-close review-**ask** generator.

Everything derives from the ~26 reviews already on `site/testimonials.html`. **Nothing is invented.**

---

## The honest "5-review API cap" story

Carrie's Google Business Profile shows **185 reviews at 5.0**, but Google's Places API returns at
most **5** reviews per place — so we *cannot* legitimately pull and republish all 185. Rather than
scrape (against ToS) or fabricate, this engine does honest **syndication**:

- **Surface what's verified.** The 26 reviews already visible on her testimonials page are captured
  verbatim in `data/reviews.yaml` and marked up as individual `Review` structured data so search
  engines can read them as discrete, sourced reviews (not just an aggregate number).
- **Drive new ones.** `review_request.py` produces a warm post-close ask that points clients at her
  real Google write-a-review link — the compliant way to *grow* the real review count over time.

### The syndication SEO play

The page already carries one `AggregateRating` (5.0 / 185). That alone gives Google a number but no
individual review content. This engine adds a JSON-LD **array of `Review` nodes** — each with the
author, the verbatim `reviewBody`, and `itemReviewed` → the `RealEstateAgent` (Carrie) — which is
what makes a page eligible for individual-review rich results. A `reviewRating` is attached **only**
to reviews that display a visible star rating on the page (the 3 Google cards); the unrated
testimonials carry no rating in markup. See the compliance note below.

---

## Files

| File | What it does |
|------|--------------|
| `../../data/reviews.yaml` | Structured store of every real review, verbatim. Schema documented in its header. Single source of truth. |
| `_extract_reviews.py` | One-time provenance helper: regenerates `reviews.yaml` from the page so the stored text is byte-identical. Not part of the normal build. |
| `build_reviews.py` | Regenerates the review-card grids of `site/testimonials.html` between `REVIEWS:AUTO:START/END` sentinels **and** injects the per-review `Review` JSON-LD. Idempotent. |
| `review_template.html` / `review_template_story.html` | Self-contained "Client Love" graphic templates (charcoal/ivory/gold, Playfair). Tokens: `{{QUOTE}}`, `{{FIRST_NAME}}`, `{{SOURCE_LABEL}}`, `{{LOGO_DATA_URI}}`, `{{FONT_PLAYFAIR_B64}}`. |
| `build_review_graphics.py` | Renders sample graphics from `reviews.yaml` via the same Playwright/data-URI/`#root`/@2x pattern as `build/social/render_post.py`. Outputs to `site/studio/packages/reviews/`. |
| `review_request.py` | Generates a compliant post-close review-**ask** (SMS + email), personalized by `{first_name, address}`, carrying her real Google review link. Mock/no-API; Carrie sends it herself. |

---

## How to run

```bash
# 1. (only if reviews changed on the page) re-derive the store verbatim
python build/reviews/_extract_reviews.py

# 2. regenerate the testimonials card grids + inject Review JSON-LD (idempotent)
python build/reviews/build_reviews.py

# 3. render the sample "Client Love" graphics (needs Playwright + chromium)
python build/reviews/build_review_graphics.py

# 4. preview a review-ask message
python build/reviews/review_request.py
```

`build_reviews.py` is re-runnable: on the first run it wraps the two existing review sections in
`<!-- REVIEWS:AUTO:START -->` / `<!-- REVIEWS:AUTO:END -->` sentinels; on every later run it
replaces only the content between those sentinels. The page's `<meta robots noindex>`, demo banner,
`AggregateRating`, and every non-review section are preserved. Verified: after the first run the 26
visible cards are **byte-for-byte identical** to the hand-authored originals — the builder only adds
the sentinels, a caveat comment, and the JSON-LD.

---

## Compliance posture

- **Verbatim only.** Every review is copied from a card already visible on the page. No review,
  author, quote, or number is authored here.
- **`rating: null` discipline.** Only the 3 Google cards show `★★★★★`; those get `rating: 5`. The
  other 23 show no star, so they are stored `rating: null` and emit **no** `reviewRating` in JSON-LD
  and **no** stars on graphics. Inventing "5 stars" for an unrated testimonial would be fabricating a
  quality statistic — banned. The graphics builder favors the rated Google reviews for samples.
- **No unverified stats.** No sales volume, days-on-market, appreciation, price, "#1 agent", or
  outcome figures appear anywhere. `data/known_claims.yaml` marks `sales_volume` UNVERIFIED; it is
  never cited. The existing `AggregateRating` (5.0/185) is preserved as-is, not recomputed.
- **No steering / fair-housing-sensitive language.** Reviews are reproduced as written (not
  paraphrased). The graphics and the review-ask contain zero neighborhood / "family-friendly" /
  "safe" / "good schools" / "up-and-coming" / "right for you" language.
- **No guarantees.** The review-ask makes no promises, predictions, rates, or outcome claims.
- **No incentive.** The ask **never** offers anything of value in exchange for a review (RESPA +
  Google/Zillow ToS) — a genuine, no-pressure ask only.
- **Human-in-the-loop + consent.** Nothing auto-sends or auto-posts. `review_request.py` only returns
  template strings for Carrie to review and send herself; the message honors opt-out (STOP / "let me
  know"). Graphics are drafts for her to approve before posting.
- **Noindex / demo.** `site/testimonials.html` keeps `<meta name="robots" content="noindex,
  nofollow">` and the demo banner. Because the demo is noindex there is no live rich-snippet risk
  now; **before any indexable launch, validate the individual `Review` markup against Google's
  review-snippet rules** (markup must match visible, clearly-sourced review content). The AUTO region
  carries a caveat comment flagging exactly this.
