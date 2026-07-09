# Workflow 06 — Content & Conversion Plan

**Delegate to:** `agents/content_strategy_agent.md` + `agents/conversion_tracking_agent.md`

## Content strategy (content_strategy_agent)
Create page briefs in `/content/page_briefs/` for:
- Lafayette Realtor (lafayette_realtor.md)
- Lafayette listing agent (lafayette_listing_agent.md)
- Lafayette buyer's agent (lafayette_buyers_agent.md)
- First-time home buyer Lafayette (first_time_homebuyers_lafayette.md)
- Sell my house Lafayette (sell_my_house_lafayette.md)
- Youngsville Realtor (youngsville_realtor.md)
- Broussard Realtor (broussard_realtor.md)

Every brief must include: target query cluster, search intent, page purpose,
suggested title, meta description, H1, outline, internal links, CTA, trust
signals, FAQ section, schema recommendation.

Also produce:
- `/reports/06_content_strategy.md` — strategy narrative, no generic blog spam;
  emphasize local expertise, relocation, sellers, first-time buyers, Acadiana
  neighborhoods, pricing/prep education.
- `/content/social_repurposing_ideas.md`

## Conversion & tracking (conversion_tracking_agent)
- GA4 + Google Search Console setup requests
- GBP performance monitoring
- UTM-tagged GBP links
- Call tracking (only if it won't break NAP consistency — flag the tradeoff)
- Contact form tracking, CRM source tagging
- Landing page CTA improvements

Outputs: tracking section appended to `/reports/06_content_strategy.md`;
implementation rows in `/backlog/seo_backlog.csv`.
