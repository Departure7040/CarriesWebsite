# Internal Notes: Facebook Reels & the $3,000/mo Marketing Spend
**Date:** 2026-07-08
**Audience:** Brook only — internal working notes, not client-facing. Tone is blunt but fair; nothing here should be pasted into a report or site page without rewriting for Carrie.

**Tagging key (same as the rest of the audit):** `[verified]` = directly observed in a live logged-in browser session on 2026-07-08 · `[inferred]` = a reasonable read of the data, not independently provable from outside the ad account · `[client-confirm]` = needs an answer from Carrie or the firm before it can be treated as settled.

**Why this file exists:** Carrie told us she pays an outside marketing firm ~$3,000/month, and the business Facebook page's reel view counts are the evidence she's been shown that it's working. Before we either validate or question that spend to her, it's worth being precise about what public view counts can and can't tell us — and this isn't a place to editorialize about the firm without evidence, so the framing below sticks to what's visible and what isn't.

---

## The data

Reel view counts, most-recent-first, sampled from a live logged-in browser session on 2026-07-08. These are the public-facing approximate view counts Facebook/Instagram displays on each reel (e.g., "21K"), not exact counts, and not pulled from any backend reporting — treat them as directionally accurate, not precise to the unit.

**Business page (`facebook.com/carriebilleaudrealty`) — 28 recent reels:**
535, 1K, 21K, 662, 62K, 445, 589, 48K, 31K, 953, 51K, 1.2K, 38K, 1.1K, 1K, 111, 69K, 67K, 71K, 36K, 21K, 60K, 28K, 23K, 1.1K, 463, 1K, 926

**Personal profile (`facebook.com/carriebilleaud`) — 27 recent reels:**
1.8K, 1.1K, 2.3K, 6.9K, 2.4K, 1.3K, 6.3K, 2.1K, 1.7K, 912, 4.1K, 8.8K, 2.1K, 1.4K, 1.3K, 2.3K, 1.4K, 5K, 1.2K, 1.3K, 1.2K, 1.3K, 1.2K, 1.1K, 2.2K, 1.3K, 2.2K

## What the shape of the data says

`[verified]` The business page numbers are real — roughly half the sample (13 of 28) sit in the 21K–71K range, and nothing on the personal profile comes anywhere close (personal profile max is 8.8K). If the question is "does the business page get more views than the personal profile," the answer is unambiguously yes.

`[inferred]` But look at the *distribution*, not just the top end. The business page is sharply **bimodal**: every value is either under ~1.2K or over 21K — there is nothing in between. Compare that to the personal profile, which is **unimodal** and clustered tightly around 1–2K (median ~1.4K, tightest range 912–2.3K, with two organic outliers at 6.3K–8.8K that look like a couple of reels that happened to hit).

A tight unimodal cluster is what organic reach normally looks like — some reels do a bit better or worse, but there's a continuous spread. A hard bimodal split — nothing between 1.2K and 21K — is the classic signature of **selective paid boosting**: some reels get ad spend behind them and jump to a different tier entirely, while the rest sit at whatever the page's baseline organic reach is. That baseline is the tell: the business page's *unboosted* reels (445–1.2K) are actually **weaker** than the personal profile's organic norm (1–2K).

This gap is more striking once you factor in followers: the personal profile has 5.5K followers vs. the business page's 2.5K — more than double. So on a per-follower basis, the personal profile's organic reels are doing considerably better than the business page's organic floor. That's another data point pointing toward "the high business-page numbers are bought reach," not general audience enthusiasm for the page.

## What we cannot tell from outside

`[inferred]` We are looking at this from the outside, logged in as a browser session, not as an ad account admin. From here we cannot:
- Confirm whether the 21K+ reels were boosted, or distinguish "boosted" from "one post that happened to go organically wide"
- See the ad targeting (geography, demographics, interest categories) — a Lafayette-only boost with real local reach is worth a lot more than a broad, cheap, low-relevance boost that inflates views without touching the local buyer pool
- See spend per reel, cost-per-view, cost-per-ThruPlay, or any efficiency metric
- See whether any of this produced a lead, a form fill, a call, a DM, or a closing — the actual thing $3,000/month is supposed to buy

## The honest verdict

**Views are real. Views are also the cheapest, least meaningful metric in paid social.** A view costs fractions of a cent to buy at scale and requires almost no intent from the viewer — someone scrolling past for half a second can register as a view. The business page's 21K–71K reels are not fake, but they also are not, by themselves, evidence that the $3,000/month is generating business for Carrie. The real question was never "do the reels get views" — it's **cost per lead**, and that's a number only the firm (or Carrie, if she has account access) can produce.

To be fair to the firm in the other direction: the production cadence itself (professional-looking reels, consistent posting, ~11 hours between posts observed on the business page) has real value independent of any boosting — someone is filming, editing, and scheduling content regularly, and that's work Carrie would otherwise have to do herself or pay for separately. Don't let the "views vs. leads" framing above turn into "the firm is doing nothing" — that's not what the data shows. It shows we can't see the ROI, not that there isn't one.

## What to request before forming a final opinion

This is the concrete list for the "Outside marketing firm" section of `reports/09_questions_for_client.md` — repeated here with the reasoning attached:

1. **Meta Business Suite / Ads Manager read-only access.** This is the single highest-value ask — it would show real spend, targeting, and Meta's own performance metrics (reach, ThruPlay cost, link clicks) directly, no inference needed.
2. **Spend breakdown: content production vs. media (ad) spend.** If most of the $3,000 is production (filming/editing time) and a small slice is boosting, that's a very different value proposition than $3,000 being mostly ad spend with views as the only return so far.
3. **Targeting details for boosted content** — at minimum, confirm boosts are geo-targeted to Acadiana/Lafayette-area audiences and not run broad/national. A national broad boost can produce huge view numbers for very little relevance to Carrie's actual market.
4. **Lead/conversion events** — does the firm track form fills, DMs, calls, or "message the page" clicks as a result of boosted content? If not set up, that's itself a finding worth flagging (no attribution = no way to know if this is working, regardless of good faith on either side).
5. **Attributed closings, if any** — has the firm (or Carrie) ever traced a specific closed deal back to a boosted reel or the business page generally? Even one or two anecdotal examples would be useful context, though not proof of a repeatable pattern.
6. **Contract scope** — what does the $3,000/month contractually include (number of reels/month, boosting included or extra, reporting cadence, ownership of raw footage/files)? Useful regardless of what the ROI analysis shows.

## Bottom line for Brook

Don't go into a conversation with Carrie (or the firm) with "the views are fake" — they're not, and that's not a defensible claim from this data. Go in with "the views are real, but they're not the metric that matters, and right now nobody outside the ad account can see the metric that does." The bimodal pattern is worth mentioning as the specific reason to ask for ad account access — it's a concrete, defensible observation, not an accusation. If the firm has nothing to hide, read-only Ads Manager access costs them nothing and answers this in five minutes.

**Client-side concurrence (Brook, 2026-07-08):** Brook independently observed the same pattern while browsing: the personal profile consistently clears 1K+ views on every reel (organic), while the business page is highly variable — "presumably depending on if ad spend was done on a post or not." This is the working hypothesis to verify via Ads Manager access. [inferred]
