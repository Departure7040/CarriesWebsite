# Social-Media Manager AI Agent — Design & Reality Check

**2026-07-12.** For Carrie (Play 3 in `growth_strategy_beyond_website.md`).
Honest architecture: what's a weekend, what's a thicket, what actually ships.

## The trap in "seems straightforward"
A social agent splits into three tiers of wildly different difficulty. People
picture tier 1 (easy) and quote a weekend; the pain is all in tier 2.

### Tier 1 — Content generation *(EASY, ~80% of the value)*
LLM + her brand voice + guardrails. Given an input (new listing, sold, open
house, market stat, testimonial) it produces a full **content package**:
- platform-specific captions (IG / FB / TikTok script / YouTube description /
  LinkedIn / Threads / Nextdoor), each in the right length + voice
- 3 hook variations, hashtag sets, a suggested post time
- a shot list or which of her existing photos/clips to use
This is just the Claude API + good prompts + her context. Straightforward, and
it's the part worth having.

### Tier 2 — Publishing / scheduling *(THE WALL)*
Auto-posting across platforms is **not** straightforward — it's per-platform API
politics:
- **Instagram**: Content Publishing API needs a Business/Creator acct linked to
  a FB Page + Meta app review; feed/reels only, rate-limited.
- **Facebook Pages**: Graph API works, but Meta app review + permissions.
- **TikTok**: Content Posting API exists but unaudited apps can only push to
  **private/drafts**; direct-post needs approval.
- **YouTube**: Data API upload — the most permissive.
- **LinkedIn**: restrictive API.
- **Threads**: Meta API, limited.
- **Nextdoor**: effectively **no** public posting API.
**Do not build six integrations.** Use a scheduling aggregator that already did
(Buffer / Metricool / Publer / Postiz — ~$15–100/mo) OR have her post the
approved package herself in 2 minutes. This is the single biggest "straightforward"
misconception.

### Tier 3 — Engagement (auto comment/DM replies) *(HARD + RISKY — mostly skip)*
Same fair-housing/compliance surface as the site bot, plus platform ToS on
automation and authenticity risk. Auto-DM reeks of spam and breaks rules. Keep
this human, or limit to a draft-a-reply assist.

## The architecture that actually ships (human-in-the-loop content engine)
```
TRIGGER            → new listing / sold / open house / stat / testimonial
   (auto or Carrie)   (LISTINGS CAN AUTO-TRIGGER — see below)
        │
GENERATE (Claude)  → full multi-platform content package + shot list
        │
APPROVE (Carrie)   → daily digest (email/text/simple web UI); 1-tap approve/edit
   (voice + compliance stay human — this is the point)
        │
PUBLISH            → aggregator API (Buffer/Metricool)  OR  she posts it
        │
MEASURE            → pull back reach/engagement where APIs allow → learn
```
The approval step is a feature, not a compromise: it keeps her voice authentic
and a human on the compliance line, which is exactly what protects her license.

## The Carrie-specific killer feature
**We already have her live listing feed** (the Realtor.com data powering the
site). A listing-triggered engine can detect a new listing the moment it hits
her feed and auto-generate the full social package — "just listed" post, reel
script, story, YouTube description — ready for her one-tap approval. That
directly attacks the exact deliverable she pays the $3k/mo firm for.

## Compliance (non-negotiable, same as the site bot)
The generation prompt carries the same guardrails: no steering /
fair-housing-sensitive language ("family-friendly," "safe," "good schools"), no
unverified stats as fact, no guarantees, keep required disclaimers, her real
NAP. A caption engine that writes "great family neighborhood" is a liability —
the prompt bans it exactly like the assistant does.

## Build reality
- **Weekend-buildable:** the content engine (tier 1) + a daily approval digest.
  Genuinely straightforward, immediately useful, low risk.
- **Not a weekend:** full multi-platform auto-publish (Meta/TikTok app reviews
  take days–weeks and business-account setup) — outsource to an aggregator.
- **Don't:** auto-engagement.

## Ties to the $3k/mo decision
This IS what the firm is paid for. Options once it exists: (a) replace the firm
if they're just boosting views; (b) keep the firm for hero video/production and
let the engine handle volume + repurposing + consistency; (c) run it in-house
and reallocate the $36k/yr. The engine reframes that conversation from "trust
the firm" to "here's what I produce, what are they adding?"

## Brook's professional note
This is textbook AI-integration consulting (his actual domain). The content
engine + approval loop + measurement is a productizable module for solo agents,
Carrie as flagship. Ship tier 1 as the proof; price tiers 2–3 as the service.

---

## Customer validation + the clean wedge (2026-07-12, from Carrie directly)
Asked "are you manually posting everything to FB/IG, to each one?" she said:
**"My personal yes and my business platform posts."** Then to the pitch —
streamline it so one post goes everywhere, multiply her time, handle more
volume with a lighter load — she replied **"All of this would be perfect!!!!"**

Two things this locks:
1. **The pain is real and felt** — she manually cross-posts, one platform at a
   time. This is exactly the Tier-1 content-engine + scheduling problem, and
   she's already asking for it. Build signal, not speculation.
2. **The clean entry wedge = her PERSONAL posting.** Her personal social she
   does herself (hers to control); the *business page* is the $3k/mo firm's
   turf. So the no-politics first build is a tool that streamlines HER personal
   cross-posting + generates the content — it solves the pain she owns, proves
   the value, and touches nothing of the firm relationship. The firm/$3k
   conversation stays a later, evidence-based decision. Wedge first, firm later.

**Recommended first build:** the human-in-the-loop content engine (Tier 1) +
one-tap multi-post, scoped to her personal accounts, listing-triggered off the
feed we already have. Ships the "perfect" she just asked for without opening the
firm question.

---

## Expanded requirements (2026-07-12, from Carrie)
- **Auto-branded graphics** — she asked "there has to be a way to automatically
  brand the posts too?" YES. Approach = **templated image composition** (branded
  HTML/CSS template + her logo + property photo + feed specs → render to PNG via
  the SAME Playwright pipeline used for the ebook PDF). NOT generative image AI
  (never hallucinate a house — composite HER real photo into a branded frame).
  Options: self-hosted HTML→PNG render (full control, free) or a templating-image
  API (Bannerbear/Placid/Canva) if she wants a template GUI. Brook already does
  this class of thing for PowerPoints/Word.
- **Brand direction: "classy, high-end luxury to attract that clientele."** This
  is the visual brief for the post templates (and, later, a lean toward a more
  luxury site aesthetic). Editorial/restrained: deep tones, ivory, gold accent
  (matches her existing gold), elegant serif, generous whitespace, thin rules —
  Sotheby's/The Agency register, not busy. Ties to Play 2 (luxury/AHB vertical).

---

## Auto-publish options (the "one button → posts" question, 2026-07-13)
**Hard platform limits decide what's even possible:**
- FB **personal profile**: NO publishing API, ever. Only Pages are postable.
- IG: auto-post ONLY with a Business/Creator account (free convert). Personal IG = no API.
- Nextdoor: no posting API. TikTok: drafts free; public post needs app audit.
- YouTube / FB Page / Threads / LinkedIn / Pinterest / X: auto-postable.
→ "one button everywhere" = ~6 platforms auto + 2-3 manual holdouts. Honest.

**The four routes:**
1. **Aggregator API (RECOMMENDED)** — Ayrshare (API-first, ~$150/mo, they did the
   Meta/TikTok app reviews) or self-hosted **Postiz** (open-source, free + Brook
   hosts). Studio "Post" button → their API with caption+graphic+accounts. Fastest ship.
2. **Direct platform APIs** — full control, no fee, but weeks of Meta/TikTok app
   review + business accounts + maintenance. Only at product scale.
3. **Browser automation (RPA)** — DON'T. ToS violation, fragile, risks banning her
   real accounts.
4. **Hybrid (realistic)** — aggregator for what it covers; TikTok→drafts; FB-personal
   + Nextdoor stay manual.

**Recommendation:** wire the studio Post button to Ayrshare/Postiz, convert her
personal IG to Creator, accept the manual holdouts. ~$150/mo (or self-host free)
= 1/20th of the $3k/mo firm for the mechanical half of their job. One-time: HER
accounts connect via OAuth once. This is Phase-2 (metered/hosting cost → arrangement).
