# Workflow 02 — Website Crawl & Technical SEO

**Delegate to:** `agents/technical_seo_auditor.md` (cheap model for crawl,
mid model for report drafting)

## Scope
Primary site: https://carriebilleaud.exprealty.com
Pages: homepage, agent profile (`/agents.php`), area/community pages, blog,
property search/listing pages, contact page.

## Checks
- robots.txt, XML sitemap, indexability (noindex, canonicals)
- Title tags, meta descriptions, H1/H2 structure, duplication across pages
- Schema markup (RealEstateAgent, LocalBusiness, Person, FAQ, Breadcrumb)
- Internal linking, orphan pages, broken links
- Thin/duplicate content (esp. templated eXp/BoldTrail pages)
- Image alt text, page speed signals (render-blocking, image weight)
- Mobile basics
- Conversion CTAs: visibility, placement, forms, phone click-to-call
- Agent profile page: is the bio/entity content missing or weak?

## Platform reality check
Separate every finding into:
- **Fix directly** — editable via agent-level site settings/content areas
- **Platform-limited** — controlled by eXp / BoldTrail / IDX templates; note
  workaround (e.g., separate personal domain/landing pages) if relevant.
Do not assume full site admin access.

## Outputs
- `/reports/03_website_technical_audit.md`
- Rows appended to `/backlog/seo_backlog.csv`
