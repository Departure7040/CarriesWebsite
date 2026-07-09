# Public Presence Inventory: Carrie Billeaud, Realtor
**Date:** 2026-07-08  
**Agent:** Carrie Billeaud, eXp Realty, Lafayette LA  
**Scope:** 12 public profiles across platforms, websites, social media, and local directories

**Tagging key:** `[verified]` = we directly fetched the source and confirmed a specific fact **appears on it as shown** (e.g., "this page displays phone number X," "this page displays the words '46 families helped'"). This is an observation about what a source page states, **not** a determination that the underlying fact is true. `[inferred]` = a reasonable conclusion drawn from available data, not independently confirmed. `[client-confirm]` = requires a decision or fact-check from Carrie before it can be used or published, especially anything touching her career history, production stats, or credentials — per `data/known_claims.yaml`, none of these are independently verifiable from public web sources alone. `[best-practice]` = general SEO/industry guidance, not specific to Carrie's data.

NAP data (phone numbers, addresses, emails **as displayed** on each source) is genuinely `[verified]` as an observation of what each platform shows — the fact that a given page displays a given number is directly confirmed by fetch. Which number/address is *canonically correct* remains `[client-confirm]`. Career/production claims (years of experience, license number, family/sales counts, dollar volume, rank claims, ICON Agent count, association membership) are downgraded to `[client-confirm]` throughout this report even where a source page was successfully fetched, because "we confirmed the page says X" is not the same as "X is true," and these specific categories are the ones the role file requires to be confirmed with Carrie before any marketing use.

---

## Executive Summary

Carrie Billeaud maintains a moderately strong public presence across major real estate platforms and social media, and her strongest asset is her **Google Business Profile: 185 reviews at a 5.0 rating** `[verified]` — see `## Errata (2026-07-08)` for a correction to this report's original conclusion. She also has strong bio quality and reviews on Zillow (29 reviews, 5.0★ `[verified]`; see Per-Source Findings for tag provenance). However, significant issues exist:

1. **GBP name-policy risk + discoverability gap** — the profile's business name is keyword/area-decorated, which risks a Google policy action, and our own search sweeps failed to find the profile despite it existing live
2. **Critical NAP inconsistencies** across address and phone fields
3. **Email variations** across platforms (gmail vs exprealty domain)
4. **Soft primary website** with weak bio and generic messaging
5. **Blocked platforms** (LinkedIn, Facebook, Instagram) limit full visibility assessment

---

## Per-Source Findings

### Tier 1: Primary/Owned Channels

#### eXp Primary Website
- **Status:** ✓ Checked
- **URL:** https://carriebilleaud.exprealty.com
- **Fetched:** Yes
- **Data Found:**
  - Phone: **337-258-5379** [verified]
  - Address: **110 Marais Avenue, Youngsville, LA 70592** [differs from other sources]
  - Service Areas: 20 cities (strong breadth)
  - Specialties: Single Family, Multi-Family, Commercial, Land, Rentals
  - Bio Quality: **WEAK** — generic customer testimonial only; no credentials, experience, or professional positioning
  - Reviews/Rating: None displayed
  - Website Links: Active (search, sell, finance, contact pages)
- **Assessment:** **[inferred]** Primary web presence lacks professional depth; bio should highlight ICON Agent status, years of experience, and key credentials visible elsewhere — all `[client-confirm]` before publishing (see Bio Quality Assessment)

---

#### eXp Agent Profile Page
- **Status:** ✓ Checked
- **URL:** https://carriebilleaud.exprealty.com/agents.php
- **Fetched:** Yes
- **Data Found:**
  - Phone: **337-258-5379** [verified]
  - Bio Quality: **WEAK** — template/generic bio ("dedicated REALTOR® serving Lafayette")
  - Specialties: 5 types listed (Residential, First-Time Buyers, Investment, Luxury, Relocation)
- **Assessment:** **[verified]** Minimal detail; no competitive differentiation

---

### Tier 2: Major Portal Profiles (High Authority)

#### Zillow Individual Agent Profile
- **Status:** ✓ Checked  
- **URL:** https://www.zillow.com/profile/carriebilleaud
- **Fetched:** Yes
- **Data Found:**
  - Phone: **337-258-5379** [verified]
  - Email: **carriebilleaud@gmail.com** [verified]
  - Address: **1318 Camellia Blvd. Ste 222, Lafayette, LA 70508** [CONFLICT]
  - Years in Business: **11 years** [client-confirm — shown on Zillow, unverified as fact per `known_claims.yaml`]
  - Review Count: **29 reviews** (substantial)
  - Rating: **5.0/5★** (perfect)
  - Bio Quality: **STRONG** — mentions business degree from UL Lafayette, analytical ability, real estate investments, problem-solving, market trend expertise
  - Specialties: 6 types (Buyer's Agent, Listing Agent, Staging, Property Management, Investment Properties, Rentals)
- **Assessment:** **[verified]** Strongest individual profile; real review volume and ratings provide credibility

---

#### Zillow Team Profile
- **Status:** ✓ Checked
- **URL:** https://www.zillow.com/profile/carriebilleaudteam
- **Fetched:** Yes
- **Data Found:**
  - Phone: **337-258-5379** [consistent]
  - Email: **carrie.billeaud@exprealty.com** [domain variation]
  - Address: **91 Settlers Trace Blvd Bldg1, Lafayette, LA 70508** [CONFLICT - 3rd address]
  - Team Members: 4 (Carrie, Jake, Blake, Arrow)
  - Rating: **5.0/5★**
  - Bio Quality: **STRONG** — describes team as top-producing agents brokered by eXp Realty
  - Specialties: 10 types (comprehensive)
  - Service Areas: 7 cities
- **Assessment:** **[verified]** Team profile provides expansion potential; separate entity from individual profile

---

#### Realtor.com Agent Profile
- **Status:** ✓ Checked
- **URL:** https://www.realtor.com/realestateagents/567985a6bb954c0100686dd4
- **Fetched:** Yes
- **Data Found:**
  - Phone: **337-258-5379** [verified]
  - Address: **1720 Kaliste Saloom Ste B 2, Lafayette, LA 70508** [CONFLICT - matches asset file]
  - Brokerage: **EXP Realty LLC** [verified]
  - License: **0995689513** [client-confirm — shown on Realtor.com, unverified as fact; conflicts with an 8-digit variant shown on Homes.com, see License Variations below]
  - Review Count: **2 reviews** (low)
  - Rating: Display unclear
  - Bio Quality: **STRONG** — professional detail about business degree, analytical skills, investment focus, team structure
  - Specialties: 4 types
  - Service Areas: 7 cities
- **Assessment:** **[verified]** Lower review volume than Zillow; bio competitive; address matches one known conflict variant

---

#### Homes.com Agent Profile
- **Status:** ✓ Checked
- **URL:** https://www.homes.com/real-estate-agents/carrie-billeaud/pf5j8yv/
- **Fetched:** Yes
- **Data Found:**
  - Phone: **(337) 341-8976** **[MAJOR CONFLICT]** Only source showing this number
  - License: **09956895** [slight variant from Realtor.com]
  - Brokerage: **EXP Realty LLC** [verified]
  - Bio Quality: **STRONG** — detailed bio emphasizing:
    - ICON Agent status `[client-confirm — shown on Homes.com, unverified as fact; multiplier also disputed, see ICON Agent Claim Discrepancy below]`
    - Certified Mentor at EXP `[client-confirm — shown on Homes.com, unverified as fact]`
    - 46 families helped (last year) `[client-confirm — shown on Homes.com, unverified as fact]`
    - **$10.5 million production volume** `[client-confirm — shown on Homes.com, unverified as fact]`
    - **Ranked #45 out of 1,900 realtors** in area `[client-confirm — shown on Homes.com, unverified as fact]`
    - Mom of four; understands family needs
  - Credentials Listed: Louisiana Realtor, Acadiana Top Producer, Certified Mentor, ICON Agent `[client-confirm — shown on Homes.com, unverified as fact]`
  - Specialties: 5 types
  - Service Areas: 16 cities (comprehensive)
  - Social Links: Facebook, Instagram, TikTok, LinkedIn
  - Reviews/Rating: None displayed
- **Assessment:** **[verified]** that this page was fetched and displays the phone number, license variant, and bio text shown above. **[client-confirm]** for every specific stat within the bio (46 families, $10.5M, #45/1900, ICON Agent, Certified Mentor) — none of these are independently verified as fact; phone conflict also requires investigation.

---

### Tier 3: Social/Local Platforms

#### Nextdoor Local Profile
- **Status:** ✓ Checked
- **URL:** https://nextdoor.com/pages/carrie-billeaud-realtor-exp-realty-lafayette-la/
- **Fetched:** Yes
- **Data Found:**
  - Phone: **337-258-5379** [verified]
  - Email: **southerncollectivegroup.info@gmail.com** [alternate email]
  - Address: **3 Flagg Place Building B, Suite B-4, Lafayette, LA 70508** [MATCHES known conflict variant #2]
  - Ratings: **6 faves**
  - Bio Quality: **STRONG** — professional positioning:
    - 2x ICON Agent `[client-confirm — shown on Nextdoor, unverified as fact; multiplier disputed, see ICON Agent Claim Discrepancy below]`
    - Top producer `[client-confirm — shown on Nextdoor, unverified as fact]`
    - Certified mentor `[client-confirm — shown on Nextdoor, unverified as fact]`
    - Home stager
    - Mom of four
  - Social Links Provided:
    - Facebook: bit.ly/3GfBUNF
    - Instagram: bit.ly/3X4lqxR
    - YouTube: bit.ly/3WZfq9n
    - LinkedIn: bit.ly/3O4PhSt
  - Website: carriebilleaud.exprealty.com
- **Assessment:** **[verified]** that this page was fetched and displays the phone, address, and bio text shown above. **[client-confirm]** for the ICON/mentor/top-producer credential claims within it. Alternate email suggests different entity (Southern Collective Group); address matches one known conflict variant.

---

#### LoopNet Broker Profile
- **Status:** ✓ Checked
- **URL:** https://www.loopnet.com/commercial-real-estate-brokers/profile/carrie-billeaud/bh92wrcb
- **Fetched:** Yes
- **Data Found:**
  - Phone: **(337) 522-7554** **[KNOWN CONFLICT]** Matches conflict noted in asset file
  - Address: **Lafayette, LA 70508** (city/zip only; partial)
  - Brokerage: **eXp Realty**
  - Bio Quality: **STRONG** — full professional bio:
    - ICON Agent `[client-confirm — shown on LoopNet, unverified as fact]`
    - Acadiana top producer `[client-confirm — shown on LoopNet, unverified as fact]`
    - Certified mentor `[client-confirm — shown on LoopNet, unverified as fact]`
    - Investment portfolio (long-term + short-term rentals)
    - 46 families served; $10.5M volume; ranked #45/1900 `[client-confirm — shown on LoopNet, unverified as fact]`
    - Business degree from UL Lafayette `[client-confirm — shown on LoopNet, unverified as fact]`
    - Market trend expertise
  - Service Areas: Lafayette
  - Specialties: Not specifically listed
- **Assessment:** **[verified]** that this page was fetched and displays the phone number and bio text shown above; this is a commercial (non-residential) platform. **[client-confirm]** for every specific stat within the bio (46 families, $10.5M, #45/1900, ICON Agent, Certified Mentor, business degree) — none of these are independently verified as fact. Phone conflict is intentional or a data error and also requires clarification.

---

#### LinkedIn Profile
- **Status:** ✗ Blocked by firecrawl
- **URL:** https://www.linkedin.com/in/carrie-billeaud-921ab6a1
- **Fetched:** Search snippet only
- **Data Available (from search):**
  - Title: "Licensed Real Estate Agent at eXp Realty Acadiana"
  - Bio Snippet: "top-producing Realtor and Icon Agent with Exp Realty here in Lafayette, LA. I am also a proud member of the Realtor Association of Acadiana, as well as a certified mentor with EXP"
  - Credentials: RAA member; certified mentor `[client-confirm — shown in LinkedIn search snippet, unverified as fact]`
- **Assessment:** **[inferred]** Profile exists and reinforces ICON/mentor positioning; full profile blocked from view; confidence=low. Credential claims within remain `[client-confirm]`.

---

#### Facebook Profile
- **Status:** ✗ Blocked by firecrawl
- **URL:** https://www.facebook.com/carriebilleaud/
- **Fetched:** Search snippet only
- **Data Available (from search):**
  - Phone: **337-258-5379** [verified from snippet]
  - Email: **carriebilleaud@gmail.com** [verified from snippet]
  - Engagement: **5,550 likes; 142 discussing**
  - Bio Snippet: "Acadiana Realtor Lafayette Luxury & Lifestyle **3x ICON Agent** Buy • Build • Sell • Invest"
  - Credentials: 3x ICON Agent (vs. 2x on Zillow/Nextdoor - **DISCREPANCY**)
- **Assessment:** **[inferred]** Strong social following; ICON claim varies (2x vs. 3x) [client-confirm]; high engagement indicates active community building

---

#### Instagram Profile
- **Status:** ✗ Not Supported
- **URL:** https://www.instagram.com/carriebilleaud_realtor/
- **Fetched:** Cannot access (platform not supported by firecrawl)
- **Manual Note:** Asset file references this profile; appears active but cannot be inventoried programmatically
- **Assessment:** **[unverified]** Requires manual audit

---

### Tier 1.5: Google Business Profile (corrected 2026-07-08 — see Errata)

#### Google Business Profile
- **Status:** ✓ Checked — EXISTS
- **URL:** https://share.google/kcBY0AQWmnVjNLAy4 (share link → live Google knowledge panel; kgmid `/g/11s57kl156`)
- **Source:** Provided by client (Brook); verified live 2026-07-08.
- **Data Found:**
  - Business name as shown: **"Carrie Billeaud Realtor | Acadiana & Surrounding Area | eXp Realty"** [verified]
  - Category: **Real estate agent** [verified]
  - Rating: **5.0** [verified]
  - Reviews: **185** [verified] — this is Carrie's single strongest public asset; more Google reviews than any competitor's *Google* review count captured in this audit (competitor counts we have are platform-specific — Sean Hettich's 353 are Zillow, not Google — see `04_competitor_gap_analysis.md`)
  - Address: **3 Flagg Place, 4 building b suite b, Lafayette, LA 70508** [verified] — matches the Nextdoor address variant (known conflict #2)
  - Phone: **(337) 258-5379** [verified] — matches the 6-source primary phone
  - Website link: **https://carriebilleaud.exprealty.com/?fbclid=IwAR1...** [verified] — carries a Facebook `fbclid` tracking artifact instead of a clean UTM-tagged link
- **Assessment:** **[verified]** GBP exists and is strong on reviews/rating, but has two fixable issues: (1) `[verified observation]` the business name is keyword/area-decorated ("| Acadiana & Surrounding Area | eXp Realty"), which `[best-practice]` likely violates Google's real-world-name policy and risks suspension or a forced edit — this should be fixed carefully (discuss with Carrie first, change only the name in one pass, document before/after); (2) the website link needs the fbclid artifact replaced with a clean UTM link (`utm_source=google&utm_medium=organic&utm_campaign=gbp`). The address corroborates the Nextdoor variant, which is relevant to (but does not decide) the canonical-NAP question. Separately, our own search sweep (see original assessment below) failed to surface this profile despite it existing live — a discoverability finding worth investigating (the name decoration may hurt match quality for "Carrie Billeaud realtor" queries) and an internal process lesson: absence of search evidence is not evidence of absence.

**Original (incorrect) assessment, retained for the record:** *"Search Queries Used: 'Carrie Billeaud' 'Google Business Profile' Lafayette Louisiana realtor; Carrie Billeaud Lafayette Louisiana Google Maps rating reviews; 3 total search attempts. Result: Zero search results for GBP or Maps listing. Assessment: No GBP exists; this is a critical gap."* This was wrong — see `## Errata (2026-07-08)` below.

---

## NAP Consistency Analysis

### Critical Issues

#### Phone Number Conflicts
| Source | Phone | Notes |
|--------|-------|-------|
| eXp Website | 337-258-5379 | Primary; most common |
| Zillow (individual) | 337-258-5379 | Consistent |
| Zillow Team | 337-258-5379 | Consistent |
| Realtor.com | 337-258-5379 | Consistent |
| Nextdoor | 337-258-5379 | Consistent |
| Facebook (search) | 337-258-5379 | Consistent |
| **Homes.com** | **(337) 341-8976** | **CONFLICT - Only source** |
| **LoopNet** | **(337) 522-7554** | **KNOWN CONFLICT per asset file** |

**Status:** 2 phones identified; requires [client-confirm]. LoopNet conflict was known; Homes.com conflict is new discovery.

---

#### Address Conflicts
| Source | Address | Notes |
|--------|---------|-------|
| eXp Primary | 110 Marais Avenue, Youngsville, LA 70592 | Physical office location |
| Zillow Individual | 1318 Camellia Blvd. Ste 222, Lafayette, LA 70508 | Service address? |
| Zillow Team | 91 Settlers Trace Blvd Bldg1, Lafayette, LA 70508 | Team office |
| Realtor.com | 1720 Kaliste Saloom Ste B 2, Lafayette, LA 70508 | **Matches known conflict #1** |
| Nextdoor | 3 Flagg Place Building B, Suite B-4, Lafayette, LA 70508 | **Matches known conflict #2** |
| LoopNet | Lafayette, LA 70508 | City/zip only |

**Status:** 5 distinct addresses identified across 6 sources. Multiple properties suggest:
- Physical office(s)
- Co-working/shared space
- Team locations
- Service addresses
Requires [client-confirm] which is primary/canonical address for NAP standardization.

---

#### Email Variations
| Source | Email | Notes |
|--------|-------|-------|
| Zillow Individual | carriebilleaud@gmail.com | Gmail; personal |
| Zillow Team | carrie.billeaud@exprealty.com | Company domain |
| Nextdoor | southerncollectivegroup.info@gmail.com | **Alternate entity/brand** |
| Facebook (search) | carriebilleaud@gmail.com | Personal |

**Status:** 3 distinct emails; one suggests alternate branding ("Southern Collective Group"). Requires [client-confirm] for canonical email.

---

#### License Variations
| Source | License | Notes |
|--------|---------|-------|
| Realtor.com | 0995689513 | 10-digit |
| Homes.com | 09956895 | 8-digit variant |

**Status:** Possible data entry error in one source; [client-confirm].

---

### ICON Agent Claim Discrepancy
| Source | Claim |
|--------|-------|
| Zillow Team | 2x ICON Agent |
| Nextdoor | 2x ICON Agent |
| Facebook (search) | **3x ICON Agent** |
| Homes.com bio | ICON Agent (no multiplier) |

**Status:** Facebook shows 3x; others show 2x. Requires [client-confirm] for accurate credential.

---

## Bio Quality Assessment

### Strong Bios (Detail + Credentials + Social Proof)
*"Strong" here rates writing quality and depth, not truth — every specific credential/production figure below is `[client-confirm]` until Carrie confirms it.*
- **Zillow Individual:** Business degree, analytical skill, investments, market trends ✓
- **Zillow Team:** Top-producing team, brokered by eXp ✓
- **Realtor.com:** Business degree, investments, team structure ✓
- **Homes.com:** ICON Agent, Certified Mentor, 46 families, $10.5M, ranked #45/1900 ✓✓ `[client-confirm]`
- **Nextdoor:** 2x ICON, top producer, mentor, home stager ✓ `[client-confirm]`
- **LoopNet:** Full credentials, production stats, investment portfolio ✓ `[client-confirm]`

### Weak Bios (Generic/Template)
- **eXp Primary Website:** Generic customer testimonial only ✗
- **eXp agents.php:** Template text ("dedicated REALTOR®") ✗

### Blocked/Unavailable
- LinkedIn: Search snippet only (strong positioning evident)
- Facebook: Search snippet only (strong positioning + high engagement)
- Instagram: No data

**Recommendation:** Update weak bios on owned eXp website to match caliber of Homes.com / Realtor.com / Zillow profiles.

---

## Service Area Coverage

**Listed Across All Sources:** 20+ distinct locations
- Core: Lafayette, Youngsville, Broussard, Carencro, Scott, Maurice, Milton
- Extended: Abbeville, Arnaudville, Breaux Bridge, Duson, Erath, Esther, Eunice, Kaplan, New Iberia, Opelousas, Parks, Rayne, St. Martinville, Sunset, Ville Platte, Church Point, Cankton, Rayne

**Assessment:** Coverage is consistent and broad; [verified] across platforms.

---

## Specialties Coverage

| Source | Specialties | Count |
|--------|-------------|-------|
| Homes.com | Residential, Investment, First-Time Buyers, Luxury, Relocation | 5 |
| Zillow Individual | Buyer's Agent, Listing Agent, Staging, Property Mgmt, Investments, Rentals | 6 |
| Zillow Team | 10 types (+ Military/Veterans, New Construction, Lot/Land) | 10 |
| Realtor.com | First-time, Sellers, Buyer's, Seller's agent | 4 |
| eXp Primary | Single/Multi-Family, Commercial, Land, Rentals | 5 |

**Assessment:** Claims consistent but scope varies; team profile shows broadest reach; [verified].

---

## Review & Rating Summary

| Source | Review Count | Rating | Notes |
|--------|--------------|--------|-------|
| **Google (GBP)** | **185** | **5.0★** | **Strongest asset — highest review count of any platform in this inventory [verified]** |
| Zillow Individual | **29** | **5.0★** | Second-strongest; perfect score [verified] |
| Zillow Team | – | 5.0★ | Team aggregate |
| Realtor.com | 2 | – | Low volume |
| Homes.com | 0 | – | No ratings shown |
| Nextdoor | 6 faves | – | Local engagement |
| LoopNet | – | – | No ratings |

**Gaps:** The "review gap" is no longer about Google (185 reviews, 5.0★ is now Carrie's leading platform) — it's about spreading reviews to Realtor.com (2), Homes.com (0), and reinforcing Zillow (29), and protecting the Google lead she already has. Nextdoor local presence modest (6 faves).

---

## Critical Gaps & Recommendations

### Top 5 Priority Gaps

1. **GBP name-policy risk + protect/optimize the existing profile [CRITICAL]**
   - Status: GBP EXISTS (185 reviews, 5.0 rating) — corrected 2026-07-08, see Errata
   - Impact: Strongest public asset, but the keyword/area-decorated business name risks a Google policy action (suspension or forced edit); website link has a tracking artifact instead of a clean UTM link; profile wasn't discoverable via our own search sweeps
   - Action: Obtain manager access; fix the business name carefully (discuss with Carrie, change only the name in one pass, document before/after) `[client-confirm]`; replace the fbclid website link with a clean UTM link; complete categories/services/photos/Q&A/posts
   - Timeline: Week 1

2. **Weak Primary Website Bio**
   - Status: Generic testimonial vs. competitive detail
   - Impact: Low conversion on owned channel
   - Action: `[client-confirm first]` — Before publishing, confirm with Carrie: ICON Agent status/multiplier, 11 years experience, Icon/Mentor credentials, and production stats (46 families, $10.5M, #45/1900). None of these are independently verified as fact; do not publish them to the owned website until Carrie confirms each figure.
   - Timeline: Week 1 for confirmation; bio update only after confirmation

3. **NAP Inconsistencies (Address + Phone)**
   - Status: 5 addresses, 2 phones, 3 emails across platforms
   - Impact: Confusion in search ranking; SEO penalty; customer friction
   - Action: [client-confirm] canonical address, phone, email; standardize across all platforms; create mapping of multi-location strategy if intentional
   - Timeline: Week 1-2

4. **Homes.com Phone Conflict**
   - Status: (337) 341-8976 shown only on Homes.com
   - Impact: Misdirected calls; data integrity issue
   - Action: [client-confirm] phone validity; correct in Homes.com admin if error
   - Timeline: Week 1

5. **ICON Agent Credential Discrepancy (2x vs. 3x)**
   - Status: Facebook claims 3x; Zillow/Nextdoor claim 2x
   - Impact: Inconsistent messaging; credibility confusion
   - Action: [client-confirm] correct multiplier; standardize all profiles
   - Timeline: Week 1

---

## Social Media Presence Assessment

| Platform | Status | Engagement | Data Quality |
|----------|--------|------------|--------------|
| Zillow | ✓ Active | 29 reviews; 5★ | Excellent |
| Realtor.com | ✓ Active | 2 reviews | Moderate |
| Facebook | ✓ Active | 5,550 likes; 142 discussing | High (blocked from full view) |
| LinkedIn | ✓ Active | Unknown (blocked) | Medium (snippet only) |
| Instagram | ✓ Active | Unknown | No data (not supported) |
| Nextdoor | ✓ Active | 6 faves | Good |
| TikTok | Likely (referenced) | Unknown | No data |
| YouTube | Likely (referenced) | Unknown | No data |

**Assessment:** Multi-platform presence evident but inconsistent detail; major platforms (Facebook, Instagram, LinkedIn) blocked from verification.

---

## Canonical URL Recommendation

**Recommended Primary URL:** https://carriebilleaud.exprealty.com
- Status: Owned channel; controlled by Carrie
- Current Issue: Weak bio; generic messaging
- Improvement Path: Update bio, credentials, production stats; ensure NAP matches canonical version

**Strongest Authority Asset:** Google Business Profile (https://share.google/kcBY0AQWmnVjNLAy4)
- Status: 185 reviews; 5.0★; highest-authority local entity source
- Strength: Largest review count in this inventory; corroborates the Nextdoor address variant
- Risk: Keyword/area-decorated business name (policy risk); website link carries a tracking artifact
- Use For: Protect and optimize first — fix name policy issue, clean the website link, complete categories/services/photos/Q&A — before pursuing new-platform review growth elsewhere

**Secondary Canonical:** https://www.zillow.com/profile/carriebilleaud
- Status: 29 verified reviews; 5.0★; high authority platform
- Strength: Real social proof; detailed professional bio
- Use For: Link target; review generation campaigns; SEO anchor

---

## Data Quality Notes

- **High Confidence [verified]:** That these sources were successfully fetched and display the NAP data (phone/address/email as shown) reported above — Zillow, Realtor.com, Nextdoor, eXp primary, Homes.com, LoopNet (accessible sources; direct fetch). This is an observation of what each page shows, not a determination that career/production claims on those pages are factually true.
- **[client-confirm] — requires Carrie's confirmation before any marketing use:** 11 years of experience; license number (0995689513 vs. 09956895 variant); 46 families helped; $10.5M production volume; #45/1900 rank; ICON Agent status and multiplier (2x vs. 3x); Certified Mentor status; RAA membership. None of these are independently verifiable from public sources alone, consistent with `data/known_claims.yaml`.
- **Low Confidence [client-confirm — canonical NAP]:** All phone/address/email conflicts (which value is correct, not just which value is displayed where)
- **Unverified:** Instagram, TikTok, YouTube (no data access); full LinkedIn detail (blocked)

---

## Summary Table: All Sources

| Source | Type | Status | Phone | Address | Email | Rating | Reviews | Bio Quality |
|--------|------|--------|-------|---------|-------|--------|---------|-------------|
| eXp Website | Owned | ✓ | 337-258-5379 | 110 Marais, Youngsville | – | 0 | 0 | Weak |
| eXp agents.php | Owned | ✓ | 337-258-5379 | eXp office | – | – | – | Weak |
| Zillow Indiv. | Portal | ✓ | 337-258-5379 | 1318 Camellia | carriebilleaud@gmail.com | 5.0★ | 29 | Strong |
| Zillow Team | Portal | ✓ | 337-258-5379 | 91 Settlers | carrie.billeaud@exprealty.com | 5.0★ | – | Strong |
| Realtor.com | Portal | ✓ | 337-258-5379 | 1720 Kaliste | – | – | 2 | Strong |
| Homes.com | Portal | ✓ | **341-8976** | – | – | – | 0 | Strong |
| Nextdoor | Local | ✓ | 337-258-5379 | 3 Flagg Place | southerncolect..@gmail.com | – | 6 faves | Strong |
| LoopNet | Portal | ✓ | **522-7554** | Lafayette, LA | – | – | – | Strong |
| LinkedIn | Social | ✗ Blocked | – | – | – | – | – | Strong (snippet) |
| Facebook | Social | ✗ Blocked | 337-258-5379 | – | carriebilleaud@gmail.com | – | 5,550 likes | Strong (snippet) |
| Instagram | Social | ✗ Unsupported | – | – | – | – | – | No data |
| GBP | Local | ✓ Checked | (337) 258-5379 | 3 Flagg Place, Lafayette | – | 5.0★ | 185 | Strong (name policy risk) |

---

## Conclusion

Carrie Billeaud has established a **moderately strong** public presence across major real estate platforms, and her Google Business Profile — 185 reviews, 5.0★ — is her single strongest asset (see Errata below for the correction to this report's original "no GBP" conclusion). She also has strength on Zillow (29★ reviews) and detailed self-reported credentials on Homes.com/Realtor.com (`[client-confirm]` — unverified as fact). However, critical gaps remain:

1. **GBP name-policy risk + discoverability gap** — the business name is keyword/area-decorated (policy risk), and our own search sweeps failed to surface the profile despite it existing live
2. **NAP inconsistencies** — Address and phone conflicts across platforms require standardization; the GBP address corroborates one existing variant (Nextdoor)
3. **Weak owned website bio** — Primary channel lacks professional depth
4. **Blocked social verification** — Cannot fully audit LinkedIn, Facebook, Instagram

**Recommendation:** Prioritize obtaining GBP manager access, fixing the name-policy risk (carefully, with Carrie's input), cleaning the website link, and completing NAP standardization and website bio update in Week 1. Secondary focus: Generate reviews on Homes.com/Realtor.com; verify credential claims (2x vs. 3x ICON); audit Instagram presence.

---

## Errata (2026-07-08)

This report originally concluded, in the Google Business Profile section: **"No GBP exists; this is a critical gap"** — based on three search queries returning zero results. **This was wrong.** Carrie's Google Business Profile exists and is live: 185 reviews, 5.0 rating, verified via a share link the client (Brook) supplied and confirmed against the live Google knowledge panel on 2026-07-08 (`https://share.google/kcBY0AQWmnVjNLAy4`, kgmid `/g/11s57kl156`).

The corrected findings are reflected throughout this report (Per-Source Findings, Executive Summary, Critical Gaps, Review & Rating Summary, Canonical URL Recommendation, Summary Table, Conclusion). Full field-level facts are in `data/public_assets.yaml` and `data/nap_consistency_matrix.csv`.

**Lesson:** absence of search evidence is not evidence of absence. Our search sweep (3 query variants) failing to surface a live, active, high-review-count profile is itself a discoverability finding worth investigating (the profile's keyword/area-decorated name may be hurting match quality), but it should never have been reported as "does not exist" without exhausting other verification paths (e.g., asking the client directly) first. This correction was applied across `data/public_assets.yaml`, `data/nap_consistency_matrix.csv`, `data/source_log.csv`, `data/known_claims.yaml`, and all downstream reports; see `reports/qa_notes.md` for the dated addendum.

---

**Report Generated:** 2026-07-08 (corrected 2026-07-08)
**Data Sources:** 12 public profiles (12 fetched; 1 initially search-only later corrected via client-supplied source)
**Confidence:** High (9 verified sources); Medium (2 conflict areas); Low (3 blocked sources)
**Methodology:** Firecrawl scrape + web search + data extraction JSON + client-supplied verification
