# Design: Audit Presentation + Demo Site (carrie.dubose.me)

**Date:** 2026-07-08 · **Approved by:** Brook (Approach A)
**Purpose:** A basic static site that (1) gives the Carrie Billeaud SEO audit a
good client-facing place to land, and (2) shows Carrie a sample of what her
site could look like. Hosted from Brook's machine behind a Cloudflare tunnel
on a dubose.me subdomain.

## Approach
Hand-built static HTML/CSS in `/site`. No build step, no dependencies, no
frameworks. Any static file server + existing `cloudflared` tunnel serves it.

## Structure
```
site/
├── index.html           # SAMPLE Carrie homepage (the demo)
├── audit/
│   ├── index.html       # Executive summary dashboard
│   ├── presence.html    # Public presence & NAP findings
│   ├── website.html     # Website technical findings
│   ├── local-seo.html   # Local SEO / GBP plan
│   ├── competitors.html # Competitor gap analysis
│   ├── ai-search.html   # AI search visibility
│   └── roadmap.html     # 30/60/90 plan
├── assets/style.css     # single shared stylesheet (+ minimal inline JS only if needed)
├── robots.txt           # User-agent: * / Disallow: /
└── SERVING.md           # local serve + cloudflared notes
```

## Decisions
1. **Demo homepage practices what the audit preaches**: clear who/where hero,
   real bio section, service-area blocks, review highlight (Zillow 29 · 5.0 —
   verified), FAQ, above-fold call CTA, sticky mobile call button, and
   RealEstateAgent JSON-LD in source (view-source is part of the pitch).
   Slim banner links to `/audit/`: "Demo concept — part of your SEO audit."
2. **Not indexable**: `noindex` meta on every page + robots.txt `Disallow: /`.
   A public lookalike would worsen the entity confusion the audit fixes.
3. **Audit pages are curated rewrites** of reports 00–05 + 07 (client-facing
   tone, evidence tags kept, NAP conflict table and review-gap comparison as
   styled HTML). Pricing (08) and client questions (09) intentionally excluded.
4. **Only verified facts** on the demo homepage; obviously-sample copy marked
   as placeholder. Unverified metrics appear only on audit pages, tagged.
5. **No photos we don't have rights to** — CSS/SVG placeholders.

## Error handling / testing
Static site: check pages render, links resolve, HTML validates roughly, and
robots/noindex present. Verified by opening locally before Brook exposes the
tunnel.

## Out of scope
Contact form backend (demo form is non-functional with a note), analytics,
CMS, multi-breakpoint pixel-perfection beyond sane responsive CSS.
