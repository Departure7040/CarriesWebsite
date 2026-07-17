# Follow Up Boss lead-routing plan — `/api/lead` → FUB (primary) + BoldTrail (secondary)

**Goal:** land every captured lead in Carrie's likely PRIMARY CRM — **Follow Up Boss
(FUB)** — while ALSO keeping the BoldTrail leg (see `boldtrail_integration_plan.md`)
and Carrie's own email notification. Speed-to-lead + nurture both depend on the lead
hitting FUB instantly and triggering its action plans / agent alert. We are NOT building
a CRM; she has two. This EXTENDS the BoldTrail plan — same `functions/api/lead.js`.

Unlike BoldTrail, **FUB exposes a first-class, publicly documented inbound API**
(`POST /v1/events`) that is the *sanctioned* way to push your own leads in — so the
repo's existing `LEAD_WEBHOOK_URL` / `LEAD_WEBHOOK_AUTH` scaffold is ~90% of the primary
path. Only a field mapper is missing.

## The four inbound paths FUB exposes

| Path | How | Effort | Reliability |
|---|---|---|---|
| **API `POST /v1/events`** ⭐ (primary) | `https://api.followupboss.com/v1/events`, HTTP **Basic auth**: API key as username, blank password (`Authorization: Basic base64("<apiKey>:")`). Body = `{ source, type, message, person:{firstName,lastName,emails:[],phones:[]} }`. This is the ONE correct inbound endpoint — it de-dupes, assigns the agent, fires action plans + notifies. (Docs explicitly say do NOT use `/people` for new leads.) Reuses the repo's `forwardWebhook()` scaffold + a `toFubEvent()` mapper. | **Low–Medium** — Carrie self-generates her key (Admin → API), set 2 env vars, add ~20-line mapper. No third party, no paid plan, inside her existing FUB seat. | **High** — native, structured, instant, triggers automations. Real source attribution. Best of all paths. |
| **Lead Email Address (parse email)** | Every FUB user has a unique `…@followupboss.me` intake address (find in FUB under the user's Lead Email Address). Any lead-notification email to it is parsed into a contact. Add it as a 2nd recipient from the Function's existing email path with `Name:/Email:/Phone:` lines. Supports Short/Full/Advanced parser formats. | **Low** — ~10 lines, one env var; mirrors the BoldTrail parse-email leg exactly. | **High delivery / Medium field precision** — email is instant, parser is heuristic (NAP extracts well; UTM/listing ride along as body text). Good zero-API fallback. |
| **Zapier** ("New Inquiry or Website Event" action) | Webhooks-by-Zapier catch hook fed by the Function → FUB "New Inquiry or Website Event" (the action-plan-triggering variant, NOT "New Contact"). | Medium — paid Zapier plan + per-Zap upkeep; adds a dependency. | Medium — FUB's Zapier action is push-based (prompter than BoldTrail's 5–15 min poll), but the extra hop + cost make it a fallback only. |
| **Native connectors** (Zillow / Realtor.com / Google / Meta) | FUB ingests those sources natively. | N/A | Irrelevant to routing our own site form. |

## Recommended routing

**Primary — FUB via API `POST /v1/events`.** Repoint the existing webhook scaffold at
FUB with a small mapper. Instant, structured, triggers her action plans + agent alert,
clean source attribution, no third party. This is the single best path any of the CRMs
offer and it costs almost nothing to wire because the scaffold already exists.

**Secondary — BoldTrail via the parse-email dual-send** (unchanged from
`boldtrail_integration_plan.md`).

**Carrie's own email notification always fires** (durable inbox copy — nothing dies even
if both CRMs are down).

**Fallbacks:** if she can't produce an API key at kickoff, ship the **FUB parse email**
first (zero-friction), swap to the API later. Zapier is the no-code last resort.

### Why not just repoint `LEAD_WEBHOOK_URL` and be done?
Two blockers, both required work:
1. **Payload shape.** `forwardWebhook()` POSTs the raw `lead` object; FUB needs the
   `events` schema (`source`/`type`/`person{…}`). Add a `toFubEvent(lead)` mapper.
2. **The current EITHER/OR forwarding must become additive.** `onRequestPost` today does
   webhook **OR** email (webhook wins). Routing to FUB **AND** BoldTrail **AND** notifying
   Carrie means three independent legs, each in its own try/catch, so one CRM failing never
   drops the lead or silences her copy. This is the same refactor the BoldTrail plan flags —
   do it once, both plans depend on it.

## Steps (FUB API primary)

1. **Get her API key** (from her seat at kickoff): FUB → **Admin → API** → create/copy key
   (`fka_…`). API key = full account privileges — treat as a secret.
2. **Cloudflare env vars** (Pages project, both Secrets):
   - `FUB_API_KEY` — the `fka_…` key. (Or precompute `LEAD_WEBHOOK_AUTH = "Basic " + base64(key + ":")` if reusing the scaffold verbatim.)
   - keep `LEAD_TO_EMAIL` / `LEAD_FROM_EMAIL` / `RESEND_API_KEY` (Carrie's notification) and
     `BOLDTRAIL_PARSE_EMAIL` (BoldTrail leg).
3. **`forwardToFub(env, lead)` helper** in `lead.js`:
   - `POST https://api.followupboss.com/v1/events`
   - headers: `Authorization: Basic base64(FUB_API_KEY + ":")`, `Content-Type: application/json`,
     `Accept: application/json`, and (recommended) `X-System` / `X-System-Key`.
   - `toFubEvent(lead)` mapper:
     - `person.firstName` / `person.lastName` ← split `lead.name` (first token / remainder).
     - `person.emails` ← `[lead.email]` (omit if empty); `person.phones` ← `[lead.phone]`.
     - `type`: `"General Inquiry"` for the contact form; `"Seller Inquiry"` for the
       valuation/sell page; `"Property Inquiry"` for listing landing pages. (Only
       Registration / Seller Inquiry / Property Inquiry / General Inquiry / Visited Open
       House trigger action plans — pick from these.)
     - `source`: `lead.utm_source` or `lead.platform` or `"carriebilleaud.com"`.
     - `message`: `lead.message` + the attribution block (listing/UTM) so nothing is lost
       even though FUB has no native slot for those.
   - treat `200`/`201` as success.
4. **Additive dual/tri-send** in `onRequestPost`, replacing the current EITHER/OR block:
   ```
   const results = await Promise.allSettled([
     env.FUB_API_KEY        ? forwardToFub(env, lead)        : null,   // primary CRM
     env.BOLDTRAIL_PARSE_EMAIL ? forwardToBoldTrail(env, lead) : null, // secondary CRM
     env.LEAD_TO_EMAIL      ? forwardEmail(env, lead)         : null,  // Carrie's copy
   ]);
   ```
   Return `200` if the lead was captured and **at least one** leg succeeded; log/notify on
   partial failure but never 502 a real lead just because one CRM leg errored.
5. **Verify by curl before shipping:**
   `curl -s https://api.followupboss.com/v1/events -u "<fka_key>:" -H "Content-Type: application/json" -d '{"source":"carriebilleaud.com","type":"General Inquiry","person":{"firstName":"Test","lastName":"Lead","emails":["t@example.com"]}}'`
   → expect `201` + a new person in FUB.
6. **Test end-to-end:** submit `/l/101-rio-ridge-dr/?utm_source=instagram` →
   confirm (a) new FUB person w/ correct NAP + source + Instagram/listing in the note,
   (b) her FUB action plan / agent alert fired, (c) a BoldTrail contact, (d) Carrie's email —
   all within ~1 min.
7. **Register the system (recommended):** email `integrations@followupboss.com` for an
   `X-System` / `X-System-Key` pair so her events are attributed to the site integration and
   protected from the shared rate-limit bucket. Not strictly enforced for a single agent
   pushing her own leads with her own key, but best practice.

## Caveats

- **UNVERIFIED — exact API rate limit.** FUB rate-limits per API key (commonly cited ~250
  req / 10 s, not confirmed in current docs). A single site form won't approach it; verify
  before any bulk/backfill use. Endpoints `/rateLimit/usage` + `/rateLimit/limits` report it.
- **UNVERIFIED — `X-System` enforcement.** Docs *request* system registration for third
  parties "providing services to a FUB customer." For Carrie pushing her own leads with her
  own key it appears optional; register anyway (step 7).
- **Use `/events`, never `/people`** for new leads — `/people` skips automations, can
  duplicate, and won't alert the agent (per FUB's own integration guide).
- **API key = full account access.** Store only as a Cloudflare Secret; never in the repo or
  client bundle. `build/production.config.json` documents the destination, not the secret.
- **Name splitting is lossy** (single-name or multi-word surnames). Send raw `lead.name` in
  `message` too as a safety net.
- **Dedup:** FUB matches person by email/phone (re-submits update the same contact — good).
  Keep ONE FUB ingestion path per lead (API only — do NOT also forward the parse email to
  FUB, or you double-create/split the contact). BoldTrail's parse email is a *separate* CRM,
  so that dual-send is fine.
- **Which CRM is truly primary is still an open kickoff question.** Context says FUB is
  *likely* primary. If confirmed otherwise, swap the primary/secondary labels — the additive
  send handles both regardless.
- **Compliance stays clean:** only real human-submitted leads forwarded; the Function already
  strips control chars / CRLF and length-caps fields (no injection into email or JSON).

## Sources
FUB API docs: `docs.followupboss.com/reference/events-post` (POST /v1/events),
`/reference/authentication` (Basic auth, API key as username), `/reference/getting-started`
(base URL, system registration → integrations@followupboss.com, rate-limit endpoints),
`/docs/lead-provider-integration-guide` (use /events not /people; source = domain).
FUB Help Center: API Key (Admin → API), Follow Up Boss Lead Email Address (@followupboss.me),
Email Parser (Short/Full/Advanced), Zapier ("New Inquiry or Website Event" triggers plans).
*Researched 2026-07-17; rate-limit number + X-System enforcement flagged UNVERIFIED above.*
