# 17: Current SERP Competitor Audit and Organic Overtake Plan

- **Initial observation date:** 2026-07-11 (America/Chicago)
- **Status:** Running document. Append dated observations; do not silently replace old rankings.
- **Scope:** Lafayette, Youngsville, Broussard, Maurice, Milton, Carencro, Scott, Lafayette Parish, and Acadiana; broad agent, buyer, seller, luxury, new-construction, acreage, and homes-for-sale intent.
- **Raw query summary:** [`data/serp_query_summary_2026-07-11.csv`](../data/serp_query_summary_2026-07-11.csv)

**Related internal work:** reports 04, 04b, 11, 13, 14 competitor teardowns, and 15.

## Executive Findings

### 1. Broad discovery is a portal contest before it is an agent contest

For broad phrases such as `best realtor Lafayette LA`, `realtor near me Lafayette LA`, and the town-level `best realtor` variants, Zillow, Realtor.com, FastExpert, US News, Yelp, and other directories occupy most or all of the first page. In the neutral-index capture, portals/directories held all ten observed slots for five broad queries and nine or more slots for many others.

**Implication:** an owned website alone will not capture the whole journey. Carrie needs two coordinated lanes:

1. An owned-domain lane for specific intent, evidence, conversion, and long-tail visibility.
2. A profile/entity lane across Google Business Profile, Realtor.com, Zillow, Homes.com, brokerage records, licensing records, and local citations.

### 2. Specific intent is where local-owned sites break through

The Google desktop validation showed local-owned pages winning when the query became specific:

- `first time home buyer realtor Lafayette LA`: [Lafayette Home Pros](https://www.lafayettehomepros.com/buyers/first-time-buyers/) was #1, [Allanson](https://www.allansonrealestate.com/) #3, and [SoLux](https://thesoluxgroup.com/first-time-home-buyer-lafayette-la/) #4.
- `luxury realtor Lafayette LA`: [SoLux](https://thesoluxgroup.com/) was #1, [Jessica Broussard](https://therealjessicabroussard.com/) #2, and [Gleason Group](https://www.gleasonla.com/) #3.
- `listing agent Lafayette LA`: [Keaty](https://www.keatyrealestate.com/) was the first owned result at #3 and Jessica Broussard followed at #5.
- `real estate team Acadiana` in the neutral index: [Allanson](https://allansonrealestate.com/about) was #1 and [The AI Team](https://www.theaiteam.us/about) followed.

**Implication:** the fastest organic gains will come from pages that solve one explicit decision, not another generic "local Realtor" homepage.

### 3. Milton and Maurice are the clearest open lanes

`Milton homes for sale realtor` returned zero Louisiana results in the neutral top ten. Results resolved to Florida, Massachusetts, Delaware, Georgia, and Ontario. `houses with land Maurice LA realtor` returned ten portal/directory results and no local-owned page.

**Implication:** a definitive Milton, Louisiana entity page and a Maurice acreage/property-due-diligence cluster have a better initial opportunity than another heavily contested Lafayette head-term page.

### 4. Google local visibility and organic visibility are related but separate

The successful Google desktop captures exposed visible map/local business names that did not always match the organic leaders. For example:

- `best realtor Lafayette LA`: Keaty, Robbie Breaux, and Brice Trahan appeared in visible map directions.
- `listing agent Lafayette LA`: Robbie Breaux, Keaty, and Sean Hettich appeared.
- `luxury realtor Lafayette LA`: Keaty, SoLux, and **Carrie Billeaud** appeared.

Carrie's appearance for the luxury query is material. It shows an existing local foothold that the owned site can reinforce with a focused luxury page, proof, listings, and consistent entity data.

### 5. The current strongest SEO challenger is SoLux, not just the legacy names

[The SoLux Group](https://thesoluxgroup.com/) combines an exact luxury homepage title, current articles, three community pages, ZIP-code pages, calculators, IDX links, structured data, and a tightly linked Lafayette topic cluster. It ranked #1 in the Google luxury capture and #4 for first-time-buyer intent.

Its execution is not flawless: the HTML is heavy, 191 tag archive URLs create index bloat, lead flows split across external subdomains, and some prose is generic or weakly sourced. The architecture and query targeting are still the clearest current model to study.

### 6. Rank is not proof of site quality

Several visible competitors have serious defects:

- [Brice Trahan Team](https://www.bricetrahanteam.com/) returned a live 500 error, a mismatched BoomStatic certificate, `noindex`, and a broken sitemap during the audit, while Brice still recurred through portal profiles.
- [The AI Team sitemap](https://www.theaiteam.us/sitemap.xml) listed 73 non-`www` URLs even though the non-`www` host returned 404; several `www` exact-match routes served generic homepage content without a self-canonical.
- [Avenue Real Estate](https://avenuerela.com/) was effectively a two-URL Canva site with no useful robots file, canonical, JSON-LD, owned IDX, or conventional content architecture.
- [Trahan Group](https://www.trahangroup.com/) had only 13 sitemap pages, little recent content, no local guide layer, and an invalid schema type string (`RealEstate Agent` rather than `RealEstateAgent`).

**Implication:** competitors are often being carried by portals, entity history, reviews, transactions, local citations, or a few strong pages. Carrie does not need to copy their entire sites to compete.

### 7. Seller language means two different markets

`sell my house Lafayette LA` and `sell my house Youngsville LA` were controlled by cash buyers, investor sites, HomeLight, and market portals. Conventional listing agents were absent from the observed top tens.

**Implication:** the opportunity is not a generic listing-agent page. It is an honest comparison page covering traditional listing versus cash offer, likely net, preparation, timing, showings, inspection, appraisal/financing risk, certainty, and who each route fits.

### 8. Fair-housing-safe local content can be a quality advantage

Robbie Breaux, Keaty, Jessica Broussard, Sean Hettich, and other competitors use phrases such as "safe," "family-friendly," "best schools," "ideal for families," and similar resident targeting. This is both a compliance risk and weak information design.

Carrie's pages should use objective, cited facts: amenities, routes, commute distances, property types, municipal services, flood/drainage considerations, official school-boundary links, buyer-selected criteria, and dated market data.

## Method and Limits

This study used three evidence layers.

### Google desktop validation

Headless Microsoft Edge loaded actual Google result pages with `num=10`, `hl=en`, `gl=us`, and personalization disabled (`pws=0`). Nine query captures completed before Google returned an unusual-traffic challenge; the challenge was not bypassed. Successful results and visible map-direction names were preserved in the CSV.

This was not a GPS-pinned Lafayette device. IP location, search history, exact viewport effects, and local-pack personalization still vary. The capture is a validation sample, not a permanent rank claim.

### Neutral web-index discovery

Thirty-five exact human-language queries were submitted individually to a neutral web-search interface. That interface exposed web results but not ads or local/map packs. Engine identity, device, and exact geolocation were not configurable. Duplicate URL variants and wrong-market results were retained because they demonstrate entity ambiguity and real search friction.

### Direct site inspection

Competitor homepages, representative landing pages, `robots.txt`, sitemaps, titles, descriptions, canonicals, headings, schema, internal paths, current content, IDX surfaces, trust elements, and lead paths were checked directly. No forms were submitted.

Rank order is **observed**. Statements about why a page is visible are **inferences from correlated on-page, entity, profile, and architecture evidence**, not claims that a single factor caused the ranking.

## Current Visibility by Lane

| Search lane | Google validation leaders | Broader discovery signal | What it means |
|---|---|---|---|
| Lafayette broad | Portals first; Robbie and Keaty entered the organic top ten | Portals often held 8-10 slots | Profiles and owned site must work together |
| Best/listing agent | Keaty, Jessica, Sean; Robbie/Keaty/Sean in local surfaces | Brice, Guidry, Stephen Hundley recur through profiles | Proof, seller positioning, and profile strength matter |
| First-time buyer | Robbie #1, Allanson #3, SoLux #4 | Allanson, 337 Home Search, Kris Bourque | A precise educational page can beat directories |
| Luxury | SoLux #1, Jessica #2; Carrie visible locally | Trahan, Paige Gary, SoLux, Avenue, Sean | Carrie already has a local foothold to reinforce |
| New construction | Google capture was rate-limited | Portal profiles dominated; Jessica was the only owned result at #9 | Builder/subdivision expertise is under-owned |
| Youngsville | Portals first; Robbie was the owned result at #6 | No owned domain in broad neutral top tens | City page needs proof, fresh data, and subdivision depth |
| Maurice | Not completed on Google | McGeeScott only at #9 for homes; no acreage-owned result | Strong underserved cluster opportunity |
| Milton | Not completed on Google | Wrong-market results dominated; zero LA homes results | Highest entity-disambiguation opportunity |
| Scott | Portals first; Gleason #6 and McGeeScott #7 | McGeeScott first owned result at #10 for homes | Spell out Scott, Louisiana and add unique local depth |
| Acadiana | Association first; McGeeScott #4, Gleason #7, Parish #10 | Michael Carr and Alyson Finch surfaced for regional terms | Regional authority needs a different page than city intent |
| Seller/cash | Not completed on Google | Cash buyers and lead-gen sites controlled both captured markets | Publish a neutral listing-versus-cash decision page |

## Observed Local Contender Shortlist

There is no defensible single "#1 Realtor" across these results. The leaders change by query intent and result type. This table records the strongest observed signals rather than averaging incompatible organic, portal, and local-pack positions.

| Local entity | Strongest observed placements/signals | Owned-site condition | Competitive interpretation |
|---|---|---|---|
| Robbie Breaux / Lafayette Home Pros | Google #1 first-time buyer, #6 Lafayette broad, #6 Youngsville, #5 Lafayette Parish; repeated visible local results | Large, tiered IDX/content footprint; flagship pages are much stronger than the long tail | Strongest all-around local entity/content incumbent |
| Keaty Real Estate | Google #3 listing agent, #4 best Realtor, #8 Lafayette broad, #8 Lafayette Parish; repeated visible local results | Deep tools, guides, subdivisions, IDX, and team proof | Strongest brokerage-scale utility/entity competitor |
| Jessica Broussard | Google #2 luxury, #5 listing agent, #7 best Realtor; only owned result in neutral new-construction top ten | Deep, current construction/subdivision cluster and conversion funnel | Strongest niche competitor for new build and micro-market expertise |
| SoLux / Drake Abshire | Google #1 luxury and #4 first-time buyer; visible local result for luxury | Current topic cluster, exact targeting, calculators, schema, ZIP/community layer | Fast-rising owned-site SEO competitor and clearest current architecture model |
| Sean Hettich | Google #8 best Realtor; visible local result for listing; neutral luxury result | Strong reviews/results/seller proof, current blog, only three city pages | Proof-led seller competitor with geographic gaps |
| McGeeScott Realty | Google #4 Acadiana and #7 Scott; neutral #8 Carencro, #9 Maurice homes, #10 Scott homes | Broad city/IDX architecture and current blog; thin original city copy | Strongest smaller-market owned inventory footprint |
| The Allanson Team | Neutral #1 first-time buyer and #1 Acadiana team; Google #3 first-time buyer | Strong voice/proof, weak crawl/metadata architecture | Niche/brand competitor outperforming its technical implementation |
| Guidry & Company | Neutral #7 general agent and #5 listing agent; repeated owned results | Working IDX and broad services, thin location layer, review-quality problems | Entity/service competitor with an open local-content gap |
| Michael Carr / Alyson Finch | Neutral #3 Acadiana for Michael; #2 Lafayette Parish for Alyson | Platform city/data pages, regional branding, generic automated copy | Regional-query competitors rather than head-term leaders |
| Brice Trahan | Recurrent portal placements and visible local result for best Realtor | Owned site was broken, 500/noindex, during audit | Portal/entity equity remains strong despite site failure |
| Stephen Hundley / Nah Senpeng | Recurrent high portal visibility | No distinctive current owned-domain moat observed | Proof/profile competitors; opportunity to beat them on owned content |

## Competitor Deep Dives

### The SoLux Group / Drake Abshire

**References:** [home](https://thesoluxgroup.com/), [first-time buyer guide](https://thesoluxgroup.com/first-time-home-buyer-lafayette-la/), [neighborhood comparison](https://thesoluxgroup.com/lafayette-neighborhoods/), [sitemap](https://thesoluxgroup.com/sitemap.xml).

**What they do well**

- The homepage directly owns luxury intent in its title and description.
- Thirty-one blog URLs form a current Lafayette topic cluster: neighborhoods, school zones, traffic, taxes, cost of living, market updates, moving, first-time buying, and lifestyle.
- Six ZIP pages, three community pages, calculators, IDX search, valuation, cash-sale, and pre-approval paths cover multiple decision stages.
- Article, breadcrumb, organization, person, and FAQ schema are present on key articles.
- Internal links connect articles, communities, ZIPs, listings, calculators, and contact paths.

**What is weak**

- About 191 tag pages for 31 posts is excessive taxonomy/index bloat.
- The homepage and major pages return roughly 200-400 KB of HTML before other assets.
- Search and seller conversion paths leave the main domain for `search.thesoluxgroup.com` and `hifello.com`.
- Some prose is generic and some sources do not substantiate the nearby claim.

**Likely visibility pattern:** exact intent targeting + current topic cluster + local entity signals + structured internal graph + working conversion tools.

- **Adopt:** query ownership, current topic clusters, calculators, visible sources, breadcrumbs.
- **Avoid:** tag proliferation, weak citations, generic filler, split-domain journeys.

### Robbie Breaux / Lafayette Home Pros

**References:** [ranking domain](https://www.lafayettehomepros.com/), [first-time buyer page](https://www.lafayettehomepros.com/buyers/first-time-buyers/), [Youngsville](https://www.lafayettehomepros.com/-youngsville/), [brand/editorial site](https://robbiebreaux.com/).

**What they do well**

- Strong local entity history, recurring Google local visibility, exact city/intent pages, IDX inventory, and a broad market footprint.
- First-person Lafayette experience, finance/investing/remodeling context, community video, and named subdivision knowledge create authentic expertise.
- The first-time-buyer page won the Google validation query outright.

**What is weak**

- Much editorial material dates to 2018-2020 and contains stale prices, population figures, school claims, or performance claims.
- Page quality is tiered: a few strong flagship pages sit above many thin inventory shells.
- Older copy contains steering-sensitive language and the brand is split across more than one domain.

**Likely visibility pattern:** durable entity/GBP strength + domain history + breadth + a few highly relevant flagship pages + IDX.

- **Adopt:** first-person local evidence, community video, one strong page per priority intent.
- **Avoid:** undated claims, mass thin pages, split brand signals, subjective resident targeting.

### Keaty Real Estate

**References:** [home](https://www.keatyrealestate.com/), [guide hub](https://www.keatyrealestate.com/guides/), [Youngsville](https://www.keatyrealestate.com/guide/youngsville/), [Broussard](https://www.keatyrealestate.com/guide/broussard/).

**What they do well**

- Broadest functional tool set in the field: IDX, map/gallery search, valuation, financing, calculators, market updates, app, flood maps, assessors, school-zone resources, residential and commercial inventory.
- Community pages link into subdivisions and listings, creating a large internal graph.
- Team scale, transaction history, testimonials, and repeated local-module visibility reinforce the entity.

**What is weak**

- Some guide prose and market snapshots are thin or stale.
- The site spans Lafayette and Northshore/New Orleans markets, which dilutes a pure Acadiana focus.
- Several trust claims lack a visible source/date; some local-selection language warrants fair-housing review.

**Likely visibility pattern:** entity/review scale + tool depth + internal links + inventory + domain history.

- **Adopt:** useful tools and subdivision-to-listing pathways.
- **Avoid:** trying to match brokerage-scale page count or copying generic guide prose.

### Jessica Broussard

**References:** [home](https://therealjessicabroussard.com/), [neighborhoods](https://therealjessicabroussard.com/neighborhoods), [Youngsville](https://therealjessicabroussard.com/neighborhoods/youngsville), [home valuation](https://therealjessicabroussard.com/home-valuation/), [River Ranch pricing](https://therealjessicabroussard.com/blog/pricing-your-river-ranch-home-in-this-micro-market).

**What they do well**

- The strongest owned new-construction/subdivision cluster: plats, setbacks, allowances, builder context, title matters, development pages, property microsites, and current micro-market articles.
- Sitemap footprint includes 62 blog posts, 9 neighborhood pages, development pages, testimonials, listings, valuation, guides, and sold-property proof.
- Current local comps, FAQs, data widgets, named places, and polished original imagery support both discovery and conversion.

**What is weak**

- No useful entity/local-business JSON-LD was observed.
- Sitemap hygiene includes a 404 URL and a placeholder development page.
- Some city prose is repetitive, generic, and steering-sensitive; the technical construction content is much stronger.

**Likely visibility pattern:** topical authority around new construction + fresh micro-market content + strong conversion funnel + local sales proof.

- **Adopt:** technical subdivision guidance, current comps, property case studies.
- **Avoid:** generic area copy and unsourced "top" claims.

### Sean Hettich / Top Agent 337

**References:** [home](https://topagent337.com/), [Youngsville](https://topagent337.com/communities/youngsville/), [reviews](https://topagent337.com/about/reviews/), [results](https://topagent337.com/about/results/), [valuation](https://topagent337.com/home-valuation/).

**What they do well**

- Quantified seller proof, results pages, detailed review narratives, valuation flow, and strong portal review visibility.
- Youngsville/Broussard content names subdivisions, schools, sports facilities, parks, and local amenities rather than relying only on generic prose.
- Blog updates continued into July 2026.

**What is weak**

- Only three community pages and no meaningful Maurice/Milton coverage.
- Schema still points core WebSite/Organization IDs to a temporary host.
- On-site review examples are old and proof counts differ across pages.
- No first-party property/IDX sitemap footprint was observed.

**Likely visibility pattern:** review/transaction proof + seller specialization + entity history + specific community copy.

- **Adopt:** tagged review stories and results/case-study proof.
- **Avoid:** inconsistent counters, old proof, and temporary-host schema IDs.

### McGeeScott Realty

**References:** [home](https://www.mcgeescott.com/), [Scott](https://www.mcgeescott.com/scott/), [Maurice](https://www.mcgeescott.com/maurice/), [Carencro](https://www.mcgeescott.com/carencro/), [blog](https://www.mcgeescott.com/blog/), [Angela Scott](https://www.mcgeescott.com/agents/angela-scott/).

**What they do well**

- More than 100 sitemap URLs cover communities, buyer/seller resources, agent credentials, testimonials, current blog posts, and IDX.
- City pages expose current listing counts, market statistics, alert/favorite/tour actions, and inventory, which keeps pages operationally fresh.
- Angela Scott's profile supplies unusually strong credential context: broker/owner role, legal/paralegal background, designations, and experience.
- The site was the only relevant local-owned result for the neutral `Maurice homes for sale realtor` top ten.

**What is weak**

- City introductions are mostly templated and thin; the page weight comes from inventory rather than decision-support content.
- HTML responses for sampled city pages were roughly 396-409 KB before other assets.
- Reviews are not a prominent, current proof layer and Milton is absent.

**Likely visibility pattern:** exact city titles + fresh IDX data + broad crawlable community architecture + established brokerage entity.

- **Adopt:** fresh market/inventory modules and credential-rich profiles.
- **Avoid:** treating IDX listings as sufficient city content.

### The Allanson Team

**References:** [home](https://allansonrealestate.com/), [about](https://allansonrealestate.com/about), [buyers](https://allansonrealestate.com/buyers), [sellers](https://allansonrealestate.com/sellers).

**What they do well**

- Strong, differentiated voice; visible first-time-buyer, land-home/mobile/modular, marketing, and social-media positioning.
- Numerous specific testimonials, recognitions, quantified experience, guide download, and direct booking paths.
- Won the neutral first-time-buyer and Acadiana-team queries.

**What is weak**

- Empty `robots.txt` and sitemap responses were observed.
- Major pages lacked canonicals and JSON-LD; homepage HTML was about 601 KB and contained many H1 elements.
- Buyer/seller pages shared generic `Services` titles; agent page used `Resources`; there is no useful city/subdivision architecture or owned IDX.
- Multiple conversion paths leave the domain.

**Likely visibility pattern:** exact brand/intent language + distinctive niche + social/third-party proof rather than technical depth.

- **Adopt:** voice, specificity, niche positioning, human testimonials.
- **Avoid:** weak metadata, heading misuse, empty crawl files, and external-only conversion.

### Guidry & Company

**References:** [home](https://www.guidryandcompany.com/), [IDX search](https://www.guidryandcompany.com/search-mls-listings/), [Acadiana homes](https://www.guidryandcompany.com/acadiana-homes/), [reviews](https://www.guidryandcompany.com/reviews/), [sitemap](https://www.guidryandcompany.com/sitemap_index.xml).

**What they do well**

- Broad residential/commercial/land/inherited-property architecture, working current IDX, office NAP, team/license proof, and direct lead paths.
- Correct canonical/indexability baseline on core pages.
- Recurred for general-agent and listing-agent discovery.

**What is weak**

- Little city or neighborhood depth; `Acadiana Homes` is mainly a lead form.
- Generic schema, indexable test/legacy price-table URLs, and robots/index inconsistencies.
- The reviews page shows 4.6/5 from 90 reviews but contains visible recent gibberish/spam entries, which damages credibility.

**Likely visibility pattern:** long-standing brokerage entity + service breadth + current IDX + profile signals.

- **Adopt:** broad service clarity and first-party IDX where operationally feasible.
- **Avoid:** unmoderated review feeds and crawl-hygiene debt.

### Michael Carr and Alyson Finch

**References:** [Michael Carr](https://michaelcarrsells.com/), [Michael's Carencro page](https://michaelcarrsells.com/carencro-LA), [Alyson Finch](https://www.livinginthe337.com/), [Alyson's Acadiana guide](https://www.livinginthe337.com/blog/Living-in-the-337-Homebuyer-s-Guide-for-Acadiana).

Both use a Lofty/Real Broker platform and surfaced for regional or buyer intent. Michael's sitemap contains 59 URLs with seven city hubs plus listing and market variants; Alyson's contains 40 URLs, five city pages, current local articles, reviews, valuation, calculator, and guides.

**What works:** crawlable city titles/descriptions, live market/demographic/amenity data, IDX, canonical URLs, contact paths, local identity, and enough distinct regional language to rank for Acadiana/Lafayette Parish variants.

**Weaknesses:** ordinary browser requests first received a custom status 218 JavaScript retry page while a Googlebot user agent received content; the server HTML had no useful H1 or JSON-LD; automated city prose is generic. Michael's `reviews` page rendered no actual review corpus and contained generic luxury copy.

- **Adopt:** region-branded identity and data-backed city pages.
- **Avoid:** platform defaults, empty proof pages, generic generated copy, and crawler-dependent delivery.

### The AI Team

**References:** [home](https://www.theaiteam.us/), [Carencro](https://www.theaiteam.us/areas/carencro), [about](https://www.theaiteam.us/about), [sitemap](https://www.theaiteam.us/sitemap.xml).

**What they do well:** lightweight pages, exact city titles/descriptions, breadcrumbs, Person/Organization graphs, FAQs, clear NAP, a memorable technology position, and regional/team-intent coverage.

**What is weak:** all 73 sitemap locations used the non-`www` host, which returned 404 during direct checks. Several exact-match `www` routes served generic homepage content without a self-canonical. Area pages were short and repeated the same unsupported performance claims and market-price language. Schema IDs also used the broken non-`www` host.

**Likely visibility pattern:** fresh entity optimization and exact phrasing, but current technical defects limit durable growth.

- **Adopt:** concise entity clarity and breadcrumb/FAQ structure.
- **Avoid:** mass exact-match routes, unsupported figures, host inconsistency, and soft-homepage fallbacks.

### Portal-first and weak-site competitors

- **Brice Trahan:** strong recurring Zillow visibility despite a currently broken owned site. This proves profile equity can outlive a site failure, but it is not a model to copy.
- **Stephen Hundley:** the most recurrent local identity in the Lafayette neutral set, but visibility was portal-first and no clearly attributable owned domain surfaced.
- **Nah Senpeng:** large third-party proof and production signals; the owned Keller Williams site is generic, locally thin, and stale.
- **Trahan Group:** strong luxury/service label but a small stale site with no content or area moat.
- **Avenue:** visually polished and personally credible, but technically and architecturally thin.

The lesson is not that technical SEO is unimportant. It is that local search combines entity history, profiles, reviews, transaction evidence, citations, proximity, and owned content. Carrie's plan must cover all of them.

## What the Winners Share

1. **A clear entity:** stable name, phone, address/service area, brokerage/license context, and consistent third-party profiles.
2. **One page for one decision:** first-time buyer, listing agent, luxury, new construction, city, subdivision, valuation, or seller option.
3. **Operational proof:** current listings, sold history, dated market figures, reviews, credentials, or case studies.
4. **A path below the city:** subdivisions, ZIPs, property types, price bands, builder developments, or micro-markets.
5. **Conversion matched to intent:** save search, request valuation, book consultation, download checklist, compare options, or request a tour.
6. **Internal pathways:** city -> subdivision -> listings/content -> service/proof -> CTA.
7. **Freshness:** current articles and dates outperform a large archive that has not been maintained.
8. **Off-site corroboration:** portal profiles and local business data frequently introduce the agent before the owned site does.

## What Is Missing From Carrie's Current Go-to-Market

The repository already contains strong planned/demo area, service, guide, testimonial, and calculator assets. The critical gap is that those assets are not yet a proven, indexed production presence on Carrie's owned domain.

Priority gaps for this competitive set:

1. **Production launch and measurement.** Until the owned site is live, canonical, submitted, and measured, demo depth contributes no rankings.
2. **Milton, Louisiana entity ownership.** Competitors and portals fail to disambiguate it.
3. **Maurice acreage decision support.** No local-owned competitor answered the observed rural-property query.
4. **Youngsville new-construction authority.** Portals own the query; Jessica owns the best first-party technical model.
5. **Listing versus cash-offer comparison.** Cash buyers currently define seller-intent results.
6. **Luxury corroboration.** Carrie already appeared in the Google local surface but lacks a matching owned content/proof cluster.
7. **Profile completeness and review distribution.** Broad queries are portal-led, so each major profile must be complete, current, linked, and reviewed.
8. **Dated first-hand proof.** Publish transaction stories, builder walkthroughs, inspection observations, market notes, and source-backed updates.
9. **Local authority links/citations.** Earn links and mentions from chambers, builders, lenders/title partners, neighborhood/community organizations, local media, and professional bodies where editorially legitimate.

## Recommended Approach

### Phase 0: establish a defensible baseline (week 1)

- Manually capture Google mobile and desktop from a device physically in each target market or through a reputable ZIP/grid rank tracker.
- Track organic results, local pack, map grid, ads/local services, and the exact landing URL separately.
- Baseline Google Search Console, GA4, GBP Insights, calls, forms, booked consultations, and profile referral traffic.
- Track at least ZIPs 70508, 70592, 70518, 70555, 70520, and 70583; add Milton's practical search context.
- Preserve screenshots and raw exports so later movement is auditable.

### Phase 1: make the entity and production site reliable (days 1-30)

- Launch the approved owned site on the canonical domain with HTTPS, one hostname, correct redirects, XML sitemap, robots file, canonicals, indexable HTML, and validated structured data.
- Align name, phone, brokerage/license, service areas, headshot, bio, and owned-domain URL across GBP, Realtor.com, Zillow, Homes.com, eXp, RAA, Facebook, and other material profiles.
- Fix sold-transaction attribution and request reviews on the platforms that actually appear for target queries.
- Put current, attributed review excerpts and transaction/service context on the owned site.
- Publish or strengthen five money pages: Milton LA, Maurice acreage, Youngsville new construction, listing-vs-cash, and Lafayette luxury.

### Phase 2: build evidence clusters, not page counts (days 31-90)

- Add two to four subdivision/development pages chosen from actual sales, builder relationships, GSC impressions, and weak competitor coverage.
- Publish one dated market note per priority city with source period, author/reviewer, and change log.
- Add anonymized case studies for first-time buyer, luxury, acreage, new build, and seller scenarios.
- Connect every city page to relevant services, guides, proof, listings/search, nearby markets, and one intent-specific CTA.
- Repurpose existing short-form video into owned-page embeds and YouTube with matching local titles and transcripts.

### Phase 3: earn regional corroboration (days 46-120)

- Build legitimate partner/resource pages with builders, lenders, inspectors, title firms, chambers, and community organizations.
- Pitch useful local data, maps, checklists, and market commentary to regional publications rather than generic guest posts.
- Keep local profiles current with photos, posts, services, Q&A, listings, and consistent landing URLs.
- Create a review routing process that follows platform rules and avoids gating or incentives.

### Phase 4: expand only from measured demand (days 91-180)

- Use GSC queries and lead quality to choose the next town, subdivision, property type, and guide.
- Consolidate overlapping pages rather than allowing cannibalization.
- Refresh market facts quarterly and transactional/legal guidance on a documented review schedule.
- Remove or `noindex` obsolete searches, thin tags, placeholders, test pages, and expired campaigns.

## Priority Page Briefs

| Priority | Page/cluster | Required differentiator | Primary CTA |
|---:|---|---|---|
| 1 | Milton, Louisiana real estate | Explicit LA/parish/ZIP/route context, original field photos, flood/drainage/utilities, nearby-market comparison | Request Milton consultation / save search |
| 2 | Maurice homes with land | Survey, servitude/easement, drainage/flood, well/septic, outbuildings, restrictions, rural financing, permit/tax contacts | Save acreage search / request due-diligence checklist |
| 3 | Youngsville new construction | Builder/subdivision matrix, phases, incentives with dates, representation, inspections, warranties, plats/setbacks, drainage | Book new-build review |
| 4 | Listing vs cash offer | Neutral net/timing/effort/risk comparison with scenarios and calculator/net sheet | Request side-by-side estimate |
| 5 | Lafayette luxury Realtor | Specific marketing plan, current luxury inventory/sold examples, confidentiality, staging/media, review/case-study proof | Book confidential strategy call |
| 6 | City market snapshots | Current source period, DOM, inventory, list-to-sale context, what changed, method notes | Get a local market update |

## Editorial and Technical Rules

- Use "Milton, Louisiana" and "Scott, Louisiana" in title, H1, intro, breadcrumb, schema, image context, and internal anchors where ambiguity exists.
- Do not claim "best," "top," "safe," "family-friendly," or school quality without an appropriate, clearly cited basis; avoid resident-type targeting entirely.
- Cite government, MLS/association, FEMA, parish/city, school-district, and other first-party sources where available.
- Put a source period next to market figures. Do not let dynamic and static figures contradict one another.
- Each page needs unique information gain: field observation, map, comparison, decision table, process detail, case study, or current local data.
- Keep the primary conversion on the owned domain when practical.
- Use one canonical host, self-canonicals, clean sitemaps, valid schema IDs, one descriptive H1, and server-rendered/indexable core content.
- Treat IDX as a utility and freshness layer, not a substitute for original local guidance.

## What Not to Copy

- SoLux's 191 tag pages for 31 posts.
- Brice Trahan's broken domain/hosting handoff.
- The AI Team's non-`www` sitemap pointing at 404 URLs.
- Allanson's generic page titles and many-H1 structure.
- Avenue's off-site forms and two-URL Canva architecture.
- Guidry's unmoderated spam review feed and test URLs.
- Trahan Group's stale 13-page footprint and invalid schema type.
- Competitors' undated market claims, stale review counts, generic city copy, and steering-sensitive neighborhood language.

## Measurement Scorecard

Report monthly by query cluster and market:

1. Google organic top-10 share for Carrie's owned domain.
2. Local-pack/map-grid share of voice and median position.
3. Number of target queries where Carrie owns the highest local-agent page.
4. GSC impressions, clicks, CTR, and average position by landing page and non-brand query.
5. Indexed/canonical pages versus submitted pages; crawl/index exclusions.
6. GBP actions and calls; profile referral traffic.
7. Qualified inquiries, booked consultations, and closed opportunities by landing page/source.
8. Review volume, velocity, recency, response rate, and distribution by platform.
9. Content freshness SLA compliance and pages refreshed.

Do not report "ranking #1" without query, location, device, result type, date/time, and landing URL.

## Manual Verification Checklist

Before using this audit in a sales or investment decision:

- Re-run the exact CSV queries from a Lafayette-area mobile device and desktop browser in signed-out/incognito mode.
- Record ads, local services, map pack, organic, People Also Ask, forums, video, and AI/answer features separately.
- Repeat from each priority market because proximity materially changes local results.
- Confirm every competitor destination and remove duplicates before calculating share of voice.
- Repeat monthly for three months before declaring a durable winner.

## Source Index

Primary direct sources used repeatedly:

- [Google-oriented query summary](../data/serp_query_summary_2026-07-11.csv)
- [Realtor.com Lafayette agents](https://www.realtor.com/realestateagents/Lafayette_LA)
- [Zillow Lafayette agent reviews](https://www.zillow.com/professionals/real-estate-agent-reviews/lafayette-la/)
- [FastExpert Lafayette](https://www.fastexpert.com/top-real-estate-agents/lafayette-la/)
- [REALTOR Association of Acadiana](https://realtoracadiana.com/)
- [SoLux sitemap](https://thesoluxgroup.com/sitemap.xml)
- [Jessica Broussard sitemap](https://therealjessicabroussard.com/sitemap.xml)
- [Keaty guide hub](https://www.keatyrealestate.com/guides/)
- [Top Agent 337 sitemap](https://topagent337.com/sitemap_index.xml)
- [McGeeScott sitemap](https://www.mcgeescott.com/sitemap.xml)
- [Allanson home](https://allansonrealestate.com/)
- [Guidry sitemap](https://www.guidryandcompany.com/sitemap_index.xml)
- [The AI Team sitemap](https://www.theaiteam.us/sitemap.xml)
- [Michael Carr sitemap](https://michaelcarrsells.com/sitemap.xml)
- [Alyson Finch sitemap](https://www.livinginthe337.com/sitemap.xml)

## Running Log

| Date | Update |
|---|---|
| 2026-07-11 | Initial 35-query neutral discovery capture, 9-query Google desktop validation, direct technical/content inspection, competitor deep dives, opportunity map, and phased approach. |
