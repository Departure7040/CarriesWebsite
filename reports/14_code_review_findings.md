# Running Code Review Findings - SEO Portal and Internet Presence

**Last updated:** 2026-07-11 (America/Chicago)  
**Reviewed snapshot:** `3191635` (`main`)  
**Review type:** Read-only code, content, rendered-page, crawl, security,
accessibility, performance, and production-readiness review  
**Implementation changes made by this review:** None. This report is the only
new file.

## How to maintain this document

This is a running register. Keep finding IDs stable, update the status and
verification notes when work is completed, and append a dated review-log entry.
Do not delete closed findings; they are useful regression context.

Status values:

- **Open** - confirmed and not addressed.
- **Decision needed** - implementation depends on an owner, broker, vendor, or
  product decision.
- **Ready to verify** - a change exists but has not been independently checked.
- **Closed** - the correction was verified against its acceptance criteria.
- **Accepted risk** - the owner explicitly accepted the documented consequence.

Severity values:

- **P0 / launch blocker** - do not publish the production site until resolved.
- **High** - material security, accuracy, compliance, conversion, or SEO risk.
- **Medium** - meaningful quality or maintainability risk.
- **Low** - optimization or polish with limited immediate impact.

## Executive assessment

The repository is a strong demo and research package, but it is not a safe or
indexable production artifact yet. The architecture is lightweight, the public
pages have a sound semantic baseline, and the content plan is substantially
more useful than a templated IDX shell. The main risk is the gap between
"private demo" and "production portal": the current origin is publicly
reachable, crawl controls are internally contradictory, operational and audit
files are served from the same root, production metadata still names the eXp
host, several high-stakes content claims are wrong or unverified, and the lead
and listing workflows are still demonstrations.

At snapshot `3191635`, automated inspection found:

- 30 HTML pages: 23 candidate marketing pages and 7 audit pages.
- All 30 pages have `noindex, nofollow`; `robots.txt` also blocks the entire
  origin.
- No page has a canonical URL, Open Graph image set, or Twitter Card metadata.
- The homepage has no meta description.
- `/sitemap.xml` returns `404`.
- All JSON-LD blocks parse, all pages have exactly one `H1`, all scanned images
  have `alt`, and all local files/assets resolve.
- Eight fragment links on `testimonials.html` are broken.
- Every scanned `<img>` is missing at least one intrinsic dimension.
- True 320, 390, and 768 CSS-pixel device emulation showed no horizontal page
  overflow.

## Production launch gate

The following must be closed before removing production crawl blocks:

| Gate | Required outcome | Findings |
|---|---|---|
| Publish boundary | Public build excludes `/audit/`, source, operational notes, and directory indexes; private material requires authentication | CR-001, CR-002 |
| Compliance approval | Sponsoring broker approves every advertising page; LREC and fair-housing requirements are satisfied | CR-003 |
| Factual QA | USDA, school-system, price-comparison, and all placeholder claims are corrected or removed | CR-004, CR-010 |
| Security | Listing rendering cannot execute upstream markup; production headers and error handling are configured | CR-005, CR-012 |
| Search foundation | One production origin, URL policy, redirects, canonicals, schema URLs, sitemap, and indexability tests agree | CR-002, CR-008, CR-009 |
| Lead path | Forms submit with privacy/spam controls and the listing/search experience is licensed and functional | CR-006, CR-007 |
| Policy operations | GBP cadence and review-solicitation guidance matches current Google policy | CR-015 |

---

## Findings

### CR-001 - The private demo is public, and its crawl controls do not guarantee exclusion

- **Severity:** P0 / launch blocker
- **Status:** Open
- **Area:** Privacy, deployment, technical SEO

**Evidence**

- The design describes image use as acceptable for a "private-audience" demo
  ([design spec, line 44](../docs/superpowers/specs/2026-07-08-audit-demo-site-design.md#L44)).
- The serving guide says the Cloudflare tunnel is live and documents its host,
  tunnel name, credential-file path, and restart procedure
  ([SERVING.md:19](../site/SERVING.md#L19),
  [SERVING.md:24](../site/SERVING.md#L24)).
- The origin blocks all crawling
  ([robots.txt:1](../site/robots.txt#L1)), while every HTML file also carries a
  robots `noindex`; the homepage example is
  [site/index.html:6](../site/index.html#L6).
- The demo banner links to the audit from every marketing page; see
  [site/index.html:25](../site/index.html#L25).
- The generic file handler serves every non-API path from the full `site/`
  directory ([server.py:74](../site/server.py#L74),
  [server.py:89](../site/server.py#L89),
  [server.py:94](../site/server.py#L94)). Point-in-time probes returned `200`
  for `/server.py`, `/SERVING.md`, and the audit pages, and exposed directory
  indexes.

**Why it matters**

`robots.txt` is not access control. More subtly, blocking a URL in
`robots.txt` prevents Googlebot from reading the page-level `noindex`, so a URL
can still appear in results if another source links to it. The served audit and
operational files also reveal internal research, infrastructure details, and
contact information to anyone with the URL.

**Required outcome**

1. Put the demo/audit behind Cloudflare Access or equivalent authentication.
2. Publish from an allowlisted artifact, not the repository `site/` directory.
3. Exclude `.py`, `.md`, audit/internal files, logs, and directory listings.
4. If a publicly reachable page must remain excluded from search, allow the
   crawler to read its `noindex`; use authentication for information that is
   actually private.

**Acceptance test**

- An unauthenticated request cannot read the audit or operational files.
- Directory URLs do not list files.
- Search-engine URL inspection can see the intended index directive on every
  publicly reachable URL.

**Authoritative references**

- [Google: Block Search indexing with `noindex`](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
- [Google: robots.txt is not a mechanism for hiding pages](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

### CR-002 - Demo and production publication states are duplicated and unsafe to flip globally

- **Severity:** P0 / launch blocker
- **Status:** Open
- **Area:** Release engineering, indexability

**Evidence**

- The production plan correctly says crawl blocking must be removed last, but
  describes the change principally through `robots.txt` and `index.html`
  ([production plan:50](../implementation/production_site_plan.md#L50),
  [production plan:55](../implementation/production_site_plan.md#L55)).
- In fact, all 30 HTML pages hard-code `noindex, nofollow`, including the seven
  audit pages ([audit/index.html:6](../site/audit/index.html#L6)).
- Demo titles, banners, schema hosts, footer disclaimers, and form behavior are
  also repeated in individual HTML files. The plan calls out visible demo
  cleanup at [production plan:56](../implementation/production_site_plan.md#L56),
  but there is no build-time environment or publish manifest.

**Why it matters**

A broad replacement could index the client audit and internal material. A
partial replacement could leave valuable marketing pages excluded. With 30
hand-maintained pages, launch behavior cannot be demonstrated as one atomic,
repeatable build.

**Required outcome**

- Define two artifacts: an authenticated audit/demo artifact and a production
  marketing artifact.
- Generate index directives, canonical host, demo banners, analytics, and
  environment-specific headers from one configuration source.
- Add a production assertion that every intended marketing URL is indexable and
  every audit/operational path is absent or authenticated.

### CR-003 - Broker-advertising and fair-housing review is required before publication

- **Severity:** P0 / launch blocker
- **Status:** Decision needed
- **Owner:** Carrie and the eXp sponsoring/qualifying broker, with legal or
  compliance review where appropriate
- **Area:** Regulatory compliance, content

**Evidence**

- The standard footer identifies Carrie, `eXp Realty`, Lafayette, and Carrie's
  phone, but it does not show a broker-owned telephone number or explicitly
  identify the broker office/jurisdiction
  ([site/index.html:419](../site/index.html#L419),
  [site/index.html:421](../site/index.html#L421)). The same footer pattern is
  repeated across the marketing pages.
- Copy targets or recommends communities using phrases such as
  "family-friendly" ([site/index.html:198](../site/index.html#L198)),
  "Kids & family-oriented feel"
  ([which-town-fits.html:90](../site/guides/which-town-fits.html#L90)),
  "top public schools" and "low crime"
  ([which-town-fits.html:96](../site/guides/which-town-fits.html#L96)), and
  "best for families with children"
  ([which-town-fits.html:122](../site/guides/which-town-fits.html#L122)).
- The Youngsville meta description makes an unsourced "top-rated schools"
  claim ([youngsville.html:8](../site/areas/youngsville.html#L8)).

**Why it matters**

The current LREC advertising checklist requires broker review, conspicuous
broker identification and a broker-owned phone, and page-level internet
disclosures including office city/state and regulatory jurisdictions. The
exact licensed trade name and office details must come from the broker, not be
inferred. For fair housing, current HUD guidance permits objective school and
crime data when shared consistently and without discriminatory intent; the
subjective recommendations and family-targeting language here still create a
steering/compliance review risk. This finding is not a legal conclusion.

**Required outcome**

1. Submit every production advertising page and reusable social template to the
   sponsoring broker for written approval.
2. Add the exact LREC-required broker identity, broker-owned phone, office
   location, and jurisdiction disclosures to every page.
3. Replace subjective demographic fit and steering language with neutral,
   consistently presented facts and direct official data links.
4. Document the approved fair-housing editorial standard for all future area
   pages and posts.

**Authoritative references**

- [Louisiana Real Estate Commission advertising guidelines](https://lrec.gov/enforcement/advertising-guidelines)
- [LREC Advertising Guidelines Checklist (PDF)](https://cdn.prod.website-files.com/6696cedcb19f4a286c91f2e8/66e4d775e9d2bc959c4761c9_Advertising-Guidelines-Checklist.pdf)
- [HUD: current clarification on school and crime data](https://www.hud.gov/news/hud-no-26-028)
- [NAR: 2026 steering, crime, and schools FAQ](https://www.nar.realtor/fair-housing/faqs-on-steering-crime-and-schools)
- [HUD: Fair Housing rights and obligations](https://www.hud.gov/program_offices/fair_housing_equal_opp/fair_housing_rights_and_obligations)

### CR-004 - Published-candidate guides contain material program and geography errors

- **Severity:** P0 / launch blocker
- **Status:** Open
- **Area:** Content accuracy, financial information, local expertise

**Evidence**

1. The USDA page explicitly explains the Section 502 **Guaranteed** program
   ([usda-loans-acadiana.html:52](../site/guides/usda-loans-acadiana.html#L52)),
   but applies a `$324,700` ceiling from the USDA **Single Family Housing
   Direct** area-limit document
   ([usda-loans-acadiana.html:67](../site/guides/usda-loans-acadiana.html#L67),
   [usda-loans-acadiana.html:70](../site/guides/usda-loans-acadiana.html#L70)).
   A disclaimer does not cure a concrete program mismatch.
2. The town comparison says Maurice is served by LPSS
   ([which-town-fits.html:65](../site/guides/which-town-fits.html#L65)) and that
   all six towns are in LPSS
   ([which-town-fits.html:70](../site/guides/which-town-fits.html#L70),
   [which-town-fits.html:127](../site/guides/which-town-fits.html#L127)). Maurice
   is in Vermilion Parish; the repository's Maurice page itself recognizes the
   parish boundary ([maurice.html:86](../site/areas/maurice.html#L86)).
3. A section titled "Median home prices" mixes median sale price, Zillow
   average value, and median listing price
   ([which-town-fits.html:53](../site/guides/which-town-fits.html#L53),
   [which-town-fits.html:61](../site/guides/which-town-fits.html#L61),
   [which-town-fits.html:65](../site/guides/which-town-fits.html#L65)).

**Why it matters**

These are decision-affecting housing and financing claims. They can mislead
users, undermine the claimed local expertise, and weaken trust signals for both
search engines and human readers.

**Required outcome**

- Separate Guaranteed and Direct USDA program rules, or remove any figure that
  cannot be tied to the exact program and geography.
- Correct Maurice school-system content and verify address-level zoning through
  official sources.
- Compare like-for-like market measures with the same period and clearly label
  measure, source, and retrieval date.
- Add visible "reviewed on" dates and an owner for recurring factual review.

**Authoritative references**

- [USDA Section 502 Guaranteed Loan Program](https://www.rd.usda.gov/programs-services/single-family-housing-programs/single-family-housing-guaranteed-loan-program)
- [USDA Single Family Housing Direct area limits (PDF)](https://www.rd.usda.gov/sites/default/files/RD-SFHAreaLoanLimitMap.pdf)
- [Vermilion Parish School System](https://www.vpsb.net/)

### CR-005 - Upstream listing data is inserted through a DOM-XSS-capable sink

- **Severity:** High
- **Status:** Open
- **Area:** Application security

**Evidence**

- The server forwards upstream Realtor.com fields without a response schema or
  value validation ([server.py:59](../site/server.py#L59),
  [server.py:63](../site/server.py#L63),
  [server.py:67](../site/server.py#L67)).
- `esc()` serializes text as HTML, which does not make quote characters or URL
  schemes safe for an HTML-attribute context
  ([site/index.html:429](../site/index.html#L429)).
- The code concatenates those values into `src`, `alt`, `data-*`, and `href`
  attributes, leaves `specs.join(...)` unescaped, and assigns the result to
  `innerHTML` ([site/index.html:435](../site/index.html#L435),
  [site/index.html:442](../site/index.html#L442),
  [site/index.html:446](../site/index.html#L446)).

**Why it matters**

Malformed or compromised upstream data containing quotes or an unsafe URL
scheme can break out of an attribute and execute script in the site's origin.
The present likelihood depends on the third-party feed, but the impact is
same-origin code execution.

**Required outcome**

- Validate the upstream response against explicit scalar types and bounds.
- Build cards with `createElement`, property assignment, and `textContent`, not
  HTML string concatenation.
- Allowlist `https:` and expected image/listing hosts before setting URLs.
- Add a restrictive Content Security Policy as defense in depth.

**Authoritative reference**

- [OWASP DOM-based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

### CR-006 - Search/listings are not a functional or licensed first-party SEO experience

- **Severity:** High
- **Status:** Decision needed
- **Area:** IDX, conversion, SEO

**Evidence**

- Search submits into a cross-origin eXp iframe
  ([site/index.html:115](../site/index.html#L115),
  [site/index.html:129](../site/index.html#L129),
  [site/index.html:134](../site/index.html#L134)). The target currently responds
  to non-browser requests with a Cloudflare challenge and `X-Frame-Options:
  SAMEORIGIN`, so it cannot be embedded from the demo or future custom domain.
  The code's iframe `error` listener does not provide a reliable fallback for
  frame-policy failures ([site/index.html:138](../site/index.html#L138)).
- Dynamic cards link users to Realtor.com rather than first-party property
  routes ([site/index.html:446](../site/index.html#L446)).
- The proxy imitates Realtor.com browser/client headers
  ([server.py:23](../site/server.py#L23),
  [server.py:39](../site/server.py#L39)).
- The repository already identifies licensing/ToS exposure and the need for
  licensed IDX ([production plan:60](../implementation/production_site_plan.md#L60)).

**Why it matters**

The primary search workflow can produce a blank embedded panel, listing-detail
content is not crawlable on the owned domain, and the demo data source is not a
production license. This blocks both conversion reliability and any goal of
ranking first-party listing pages.

**Required outcome**

- Choose a licensed MLS/IDX path and document which listing/search URLs may be
  indexed under the vendor and MLS rules.
- Until that exists, use a clear new-tab link to the eXp search and remove the
  nonfunctional iframe promise.
- If listing SEO is in scope, require crawlable server-rendered detail routes,
  stable canonicals, status behavior for sold/removed listings, and compliant
  attribution.

### CR-007 - Lead forms do not submit and lack a complete privacy failure model

- **Severity:** High
- **Status:** Open
- **Area:** Conversion, privacy, reliability

**Evidence**

- The homepage form cancels submission through inline JavaScript
  ([site/index.html:393](../site/index.html#L393)) and labels the action as demo
  only ([site/index.html:410](../site/index.html#L410)).
- The valuation form also cancels submission and disables its CTA
  ([sell-my-house.html:61](../site/services/sell-my-house.html#L61),
  [sell-my-house.html:78](../site/services/sell-my-house.html#L78)).
- Name, email, phone, property address, and messages are requested without a
  linked privacy notice. The homepage form has no `method` or `action`; if its
  inline handler is unavailable, the browser default is a GET that can place
  PII in the URL, history, and logs.
- The production plan covers delivery and spam protection, but not this GET
  failure mode or data handling
  ([production plan:59](../implementation/production_site_plan.md#L59)).

**Required outcome**

- Keep every nonfunctional form explicitly disabled until a backend exists.
- Use POST over HTTPS, server-side validation, generic responses, spam/rate
  controls, and defined retention/deletion behavior.
- Add a reviewed privacy notice and any required consent language before data
  collection.
- Test success, validation, spam, outage, duplicate-submit, and CRM/email
  delivery behavior.

### CR-008 - Canonical origin, URL normalization, and sitemap policy are missing

- **Severity:** High
- **Status:** Open
- **Area:** Technical SEO, migration

**Evidence**

- The production target is `carriebilleaud.com`
  ([production plan:1](../implementation/production_site_plan.md#L1)), but
  entity schema declares `https://carriebilleaud.exprealty.com`
  ([site/index.html:12](../site/index.html#L12)). Service entities and the
  calculator repeat the old host
  ([listing-agent.html:12](../site/services/listing-agent.html#L12),
  [mortgage-calculator.html:16](../site/tools/mortgage-calculator.html#L16)).
- Some articles use old-host URLs as `mainEntityOfPage`
  ([louisiana-closing-process.html:16](../site/guides/louisiana-closing-process.html#L16)).
- None of the 30 pages has `rel="canonical"`.
- `/` and `/index.html` both return `200`, as do `/audit/` and
  `/audit/index.html`; extensionless area URLs return `404`; directory URLs can
  list files under the current handler.
- There is no sitemap; `/sitemap.xml` returned `404`, and
  [robots.txt](../site/robots.txt#L1) has no `Sitemap:` directive.

**Why it matters**

The new owned domain, old eXp domain, default-index variants, `.html` paths,
schema identifiers, and future sitemap can send conflicting entity and
canonical signals. This also fragments analytics and makes a domain migration
harder to validate.

**Required outcome**

1. Select one HTTPS host and one path convention.
2. Add edge-level permanent redirects for host, scheme, index-file, slash, and
   extension variants.
3. Emit self-canonicals and use those exact URLs in internal links, schema,
   sitemap, Open Graph, and analytics.
4. Include only indexable marketing canonicals in `sitemap.xml`; exclude audit,
   API, operational, search-parameter, and duplicate URLs.
5. Validate the migration and submitted sitemap in Search Console.

**Authoritative references**

- [Google: canonical URL methods](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Google: build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google: site moves with URL changes](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)

### CR-009 - Search snippets, social previews, and structured-data identity are incomplete

- **Severity:** High
- **Status:** Open
- **Area:** Search appearance, entity/schema

**Evidence**

- The homepage has no meta description between its title and stylesheet
  ([site/index.html:7](../site/index.html#L7),
  [site/index.html:8](../site/index.html#L8)).
- All 30 pages lack a complete Open Graph image set, Twitter Card metadata, and
  favicon declaration.
- Ten candidate pages still put "Demo Concept" in the `<title>`, including the
  homepage and testimonials
  ([site/index.html:7](../site/index.html#L7),
  [testimonials.html:7](../site/testimonials.html#L7)).
- Thirteen titles and seven descriptions are long enough to be frequent
  truncation/rewrite candidates. Google has no fixed character limit, so these
  require device/SERP testing rather than blind 60/160 truncation.
- `AggregateRating` is attached to Carrie's own `RealEstateAgent` entity
  ([site/index.html:16](../site/index.html#L16)). Google says self-serving local
  business/organization review markup is ineligible for the star feature and
  says not to aggregate ratings from other sites. The source comment already
  calls for validation ([site/index.html:19](../site/index.html#L19)).
- Nine `Article` objects are syntactically valid, but none has an `image`, only
  two have `datePublished`, and their author nodes do not reference a stable
  Carrie entity. A minimal example is
  [first-home-under-250k.html:10](../site/homes/first-home-under-250k.html#L10).

**Required outcome**

- Create a metadata matrix for every indexable page: unique title and
  description, self-canonical, social title/description/image, and favicon.
- Use one stable production entity `@id`; connect page, author, service,
  organization, and `sameAs` nodes consistently.
- Remove business `AggregateRating` markup unless a documented, current Google
  eligibility review supports it; visible testimonials can remain without
  promising stars.
- Add honest visible author/reviewer/date information and the applicable
  recommended Article properties.

**Authoritative references**

- [Google: meta descriptions and snippets](https://developers.google.com/search/docs/appearance/snippet)
- [Google: review snippet structured data](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)
- [Google: Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article)

### CR-010 - Placeholder content, metadata claims, and authorship are not production-ready

- **Severity:** High
- **Status:** Open
- **Area:** On-page SEO, trust, content operations

**Evidence**

- Area pages contain repeated sample/confirmation markers for neighborhoods,
  employers, commute times, schools, market figures, and FAQ answers. Broussard
  examples appear at
  [broussard.html:62](../site/areas/broussard.html#L62),
  [broussard.html:87](../site/areas/broussard.html#L87),
  [broussard.html:102](../site/areas/broussard.html#L102), and
  [broussard.html:153](../site/areas/broussard.html#L153).
- Metadata sometimes asserts what the body calls unverified. Youngsville claims
  "top-rated schools" in metadata
  ([youngsville.html:8](../site/areas/youngsville.html#L8)) but marks school
  quality for confirmation in the body
  ([youngsville.html:152](../site/areas/youngsville.html#L152)). Maurice claims
  "Vermilion Parish expertise"
  ([maurice.html:8](../site/areas/maurice.html#L8)) while parish/zoning details
  remain unresolved ([maurice.html:86](../site/areas/maurice.html#L86)).
- Guide/home pages identify Carrie as `Article` author in JSON-LD without a
  visible byline, credentials, reviewed date, or approval record. The homepage
  itself says the sample bio requires approval
  ([site/index.html:161](../site/index.html#L161),
  [site/index.html:162](../site/index.html#L162)).
- Testimonials expose names and long quotations while the page says source
  links and permissions remain pending
  ([testimonials.html:91](../site/testimonials.html#L91),
  [testimonials.html:184](../site/testimonials.html#L184)).

**Why it matters**

Publishing near-duplicate location templates with conspicuous placeholders or
unsupported local claims weakens user trust and the intended first-hand local
advantage. Metadata/body contradictions are especially damaging because users
see the claim before they see the caveat.

**Required outcome**

- Create a per-page sign-off checklist tied to `data/known_claims.yaml` and
  primary source URLs.
- Do not publish an area page until placeholders are replaced with sourced or
  Carrie-confirmed first-hand detail.
- Make title, description, schema, visible copy, and the claims registry agree.
- Record author approval and visible review dates; secure testimonial permission
  and source links.

**Authoritative reference**

- [Google: creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

### CR-011 - A sitewide navigation regression demonstrates the need for templates and CI

- **Severity:** Medium
- **Status:** Open
- **Area:** Navigation, maintainability, QA

**Evidence**

- The testimonials header uses homepage fragments as same-page links
  ([testimonials.html:29](../site/testimonials.html#L29)). The page does not have
  `#search`, `#listings`, `#open-houses`, `#areas`, `#services`, `#guides`, or
  `#about`; eight fragment references fail.
- File/resource crawling otherwise found zero missing local files, which makes
  this a focused navigation regression rather than a missing-page problem.
- Header, footer, metadata, and schema blocks are copied across 30 hand-authored
  HTML files. The test requirement only calls for links and HTML to validate
  "roughly" ([design spec:49](../docs/superpowers/specs/2026-07-08-audit-demo-site-design.md#L49)).

**Required outcome**

- Generate repeated chrome and metadata from build-time templates while still
  deploying static output. A full client framework is not required.
- Add CI checks for internal files, cross-page fragments, duplicate IDs,
  metadata requirements, JSON-LD parsing, sitemap parity, and forbidden
  production paths.
- Add responsive screenshots for representative home, area, guide, service,
  testimonial, and tool pages.

### CR-012 - The current server and home-tunnel origin are not production-grade

- **Severity:** High
- **Status:** Open
- **Area:** Hosting, reliability, security headers

**Evidence**

- Restart depends on manually running a home-PC process and tunnel
  ([SERVING.md:19](../site/SERVING.md#L19),
  [SERVING.md:24](../site/SERVING.md#L24)).
- The development server binds every network interface
  ([server.py:95](../site/server.py#L95)) even though the tunnel is configured
  for localhost.
- API failures send raw exception text to callers
  ([server.py:80](../site/server.py#L80)).
- The source defines no static security-header policy; the production plan
  correctly identifies managed hosting as necessary
  ([production plan:61](../implementation/production_site_plan.md#L61)).

**Required outcome**

- Move the static artifact to managed hosting and dynamic endpoints to a
  managed function/worker.
- Until migration, bind only loopback and place authentication/rate controls at
  the edge.
- Version an edge-header policy: CSP (including `frame-ancestors`), HSTS,
  `X-Content-Type-Options`, Referrer-Policy, and a minimal Permissions-Policy.
- Log detailed upstream failures privately and return a generic public error.

### CR-013 - Image/listing behavior creates avoidable layout, payload, and cache risk

- **Severity:** Medium
- **Status:** Open
- **Area:** Core Web Vitals, performance

**Evidence**

- None of the scanned images has both intrinsic `width` and `height`. Key
  homepage examples are the logo, hero, about image, and footer logo
  ([site/index.html:27](../site/index.html#L27),
  [site/index.html:44](../site/index.html#L44),
  [site/index.html:157](../site/index.html#L157),
  [site/index.html:420](../site/index.html#L420)). Hero/about CSS sets width but
  not an aspect ratio
  ([style.css:44](../site/assets/style.css#L44),
  [style.css:53](../site/assets/style.css#L53)).
- The API asks for up to 100 listing results
  ([server.py:27](../site/server.py#L27)); the browser replaces six stable
  snapshot cards with every returned image/card after load
  ([site/index.html:430](../site/index.html#L430),
  [site/index.html:435](../site/index.html#L435)). The reviewed live response had
  10 remote JPEGs totaling about 1.49 MB; local fallback listing images total
  about 1.10 MB.
- Cache busting is a manual query-string/purge procedure
  ([SERVING.md:30](../site/SERVING.md#L30)); `nav.js` is unversioned and cache
  policy is not stored in the repository.

**Required outcome**

- Emit correct dimensions or `aspect-ratio`; consider high-priority loading for
  the actual LCP image.
- Cap/paginate the initial listings, reserve a stable result region, request
  right-sized modern formats, and provide `srcset`/`sizes`.
- Use content-hashed assets and committed immutable-cache rules.
- Establish Lighthouse budgets and collect field Web Vitals after launch.

**Authoritative reference**

- [web.dev: optimize Cumulative Layout Shift](https://web.dev/articles/optimize-cls)

### CR-014 - Navigation semantics and small-text contrast miss accessibility baselines

- **Severity:** Medium
- **Status:** Open
- **Area:** Accessibility, UX

**Evidence**

- Dropdown parents are links that double as touch toggles, but do not expose
  `aria-expanded`, `aria-controls`, or `aria-haspopup`, and there is no Escape
  handling ([nav.js:2](../site/assets/nav.js#L2),
  [nav.js:4](../site/assets/nav.js#L4),
  [nav.js:17](../site/assets/nav.js#L17)). There is no skip link.
- Gold `#c9a24b` on cream `#faf7f2` measures about `2.25:1` and on white about
  `2.40:1`, while `.kicker` is only `.78rem`
  ([style.css:40](../site/assets/style.css#L40)). The inferred-tag combination
  is about `3.79:1` at `.72rem`
  ([style.css:18](../site/assets/style.css#L18),
  [style.css:20](../site/assets/style.css#L20)). Normal text requires `4.5:1`
  under WCAG 2.2 AA.
- Calculator results update without a live region
  ([mortgage-calculator.html:85](../site/tools/mortgage-calculator.html#L85),
  [mortgage-calculator.html:175](../site/tools/mortgage-calculator.html#L175)).
- Comparison tables have no caption or header `scope`
  ([which-town-fits.html:56](../site/guides/which-town-fits.html#L56)).

**Required outcome**

- Use an accessible disclosure/menu-button pattern with keyboard behavior and
  state announcements; add a skip link.
- Select colors that meet AA in every actual foreground/background pairing.
- Announce calculator changes politely and add table captions/header scope.
- Run automated accessibility checks plus keyboard and screen-reader smoke tests.

**Authoritative reference**

- [WCAG 2.2, Success Criterion 1.4.3 Contrast (Minimum)](https://www.w3.org/TR/WCAG22/#contrast-minimum)

### CR-015 - GBP cadence and review-request guidance conflict with current Google policy

- **Severity:** P0 for the review campaign; High otherwise
- **Status:** Open
- **Area:** Local SEO operations, platform policy

**Evidence**

- The GBP content guide says posts expire from the main profile after seven
  days ([google_business_profile_posts.md:163](../content/google_business_profile_posts.md#L163),
  [google_business_profile_posts.md:165](../content/google_business_profile_posts.md#L165)).
  Current Google help says posts older than six months are archived unless a
  date range is set.
- The review templates claim policy compliance
  ([review_request_templates.md:3](../content/review_request_templates.md#L3))
  but invite friends, family, and referral partners and permit a review based on
  "just knowing me as your realtor"
  ([review_request_templates.md:60](../content/review_request_templates.md#L60),
  [review_request_templates.md:62](../content/review_request_templates.md#L62)).
  Google requires genuine experience and identifies familial/professional
  conflicts as biased content.

**Why it matters**

Incorrect cadence guidance wastes effort. More seriously, broad solicitation
of people without a genuine service/referral experience can produce removals or
rating-manipulation enforcement against the profile the strategy is intended to
protect.

**Required outcome**

- Correct the six-month archive behavior; choose cadence for audience value,
  not a false seven-day expiry.
- Restrict requests to people with a genuine transaction, service, or directly
  relevant referral experience; remove friends/family and "just knowing me"
  wording.
- Do not gate, incentivize, prescribe sentiment, or selectively request only
  positive reviews.

**Authoritative references**

- [Google Business Profile: create and manage posts](https://support.google.com/business/answer/7342169)
- [Google Maps policy: genuine experience, conflicts, and rating manipulation](https://support.google.com/contributionpolicy/answer/7400114)

### CR-016 - Production measurement does not yet cover the actual conversion journey

- **Severity:** Medium
- **Status:** Open
- **Area:** Analytics, privacy, optimization

**Evidence**

- The tracking kit proposes GA4 streams
  ([tracking_setup_kit.md:18](../implementation/tracking_setup_kit.md#L18)) and
  focuses primarily on GBP metrics and campaign UTMs
  ([tracking_setup_kit.md:58](../implementation/tracking_setup_kit.md#L58)).
- There is no committed event/QA specification for click-to-call, contact and
  valuation success, listing inquiry, search use, IDX outbound navigation,
  cross-domain continuity to eXp/IDX, spam rejection, or Web Vitals.
- Analytics was explicitly outside demo scope
  ([design spec:54](../docs/superpowers/specs/2026-07-08-audit-demo-site-design.md#L54)),
  so this is a production gate rather than a demo defect.

**Required outcome**

- Define event names, required parameters, consent basis, deduplication, and
  test cases before wiring forms/IDX.
- Decide whether cross-domain measurement is technically and legally
  appropriate with the chosen vendor.
- Verify events in GA4 DebugView and reconcile leads against the receiving
  inbox/CRM.
- Add field Core Web Vitals monitoring and Search Console ownership at launch.

---

## Verified strengths

1. **Lean runtime:** one 10 KB CSS file and one sub-1 KB navigation script, no
   framework or third-party runtime dependency, and system fonts
   ([style.css:3](../site/assets/style.css#L3)).
2. **Efficient primary portrait:** the local hero is a roughly 17 KB WebP and is
   not lazy-loaded; lower listing images use native lazy loading.
3. **Semantic baseline:** every reviewed page has one `H1`, `lang="en"`, a
   viewport declaration, and a `<main>` landmark. Forms use explicit labels and
   FAQs use native `<details>/<summary>`.
4. **Image text alternatives:** all scanned images have `alt`; listing alts are
   concise and address-specific.
5. **Machine-readable syntax:** all JSON-LD blocks parse and visible FAQ text
   matches FAQ schema where used.
6. **Static discoverability:** all 30 pages have at least one inbound HTML link;
   all local files and assets resolve at the reviewed snapshot.
7. **Source transparency:** guides generally link claims inline, show caveats,
   and distinguish verified, inferred, and client-confirmation states. The
   repository's evidence standard is explicit
   ([README.md:27](../README.md#L27)).
8. **Resilient listing fallback:** an upstream/API failure retains baked-in
   listing cards instead of blanking the page
   ([site/index.html:451](../site/index.html#L451)).
9. **Existing plan awareness:** the production plan already recognizes the
   contact backend, licensed IDX, managed hosting, DNS, crawl-control, and GSC
   work ([production plan:53](../implementation/production_site_plan.md#L53)).

## Verification gaps

The review could not establish the following from repository source alone:

- Cloudflare Access/WAF, DNS, firewall, cache-rule, redirect-rule, and header
  configuration.
- Sponsoring broker approval, exact licensed broker trade name/phone/office,
  fair-housing review, reviewer/vendor permissions, IDX rights, or photo rights.
- Search Console index status, live sitemap coverage, GA4/CRM delivery, or Google
  Business Profile manager configuration.
- CrUX/field LCP, CLS, and INP. File size, local rendering, and point-in-time
  TTFB do not prove a Core Web Vitals pass.
- Rich Results Test output on the final production URLs.
- Upstream Realtor/MLS schema changes, outage behavior after cache expiry,
  production load behavior, or vendor-specific crawl/index rules.
- Screen-reader coverage across VoiceOver, NVDA, and mobile assistive technology.

## Recommended verification suite

Add these checks before launch and keep them in CI/operations:

1. Crawl the production artifact and fail on broken files/fragments, duplicate
   IDs, missing required metadata, wrong-host URLs, or forbidden paths.
2. Assert indexability and self-canonical behavior for the exact sitemap set.
3. Assert authentication or absence for `/audit/`, `.py`, `.md`, logs, source
   maps, and directory URLs.
4. Test redirects for HTTP/HTTPS, apex/www, `/index.html`, trailing slashes, and
   the selected `.html` policy.
5. Validate JSON-LD with the Rich Results Test and schema tooling.
6. Run Lighthouse mobile budgets and accessibility automation on one page per
   template, followed by keyboard/screen-reader smoke tests.
7. Exercise form success/failure/spam/privacy flows and reconcile each test lead
   with the receiving system.
8. Monitor uptime, 4xx/5xx, worker/API failures, Web Vitals, GSC indexing, and
   sitemap drift after release.

## Review log

| Date | Snapshot | Work performed | Result |
|---|---|---|---|
| 2026-07-11 | `3191635` | Initial read-only repository, rendered-page, crawl, SEO, content, accessibility, security, performance, and production-readiness review | 16 open findings recorded; no existing source file changed |

