# BoldTrail (kvCORE) lead-routing plan — pipe `/api/lead` into her CRM

**Goal:** make sure captured leads land in Carrie's existing CRM (BoldTrail, the
rebuilt kvCORE, included in eXp's ~$85/mo tech fee) so nothing dies in an inbox —
speed-to-lead + nurture both depend on it. We are NOT building a CRM; she has one.
Gated on the kickoff answer: *does she actually use BoldTrail?* (ops question #3).

Today: leads are captured by the Cloudflare Pages Function `functions/api/lead.js`
(rate-limit + KV + notify Carrie). This adds a second, CRM-bound delivery.

## The four inbound paths BoldTrail exposes

| Path | How | Effort | Reliability |
|---|---|---|---|
| **Parse email (Lead Dropbox)** ⭐ | Every agent has a unique intake address (eXp format `leads+expcorporate###-a-#####@kvcore.com`, under Lead Engine → "Sync any lead source" → EMAIL). Any email to it becomes a contact. We add it as a 2nd recipient from the Function's existing email path, with `Name:/Email:/Phone:` lines. | **Low** — ~15 lines in `lead.js` + one env var; no API request, inside eXp's included stack. | High for delivery + speed (email is instant). Medium on field precision (parser is heuristic; NAP extracts well, UTM/listing rides along as body text). |
| **Public API v2 → POST Contacts** | Carrie generates a bearer token (Lead Engine → Lead Dropbox → My API Tokens). Function POSTs JSON to `https://api.kvcore.com` v2 Contacts with `Authorization: Bearer <token>`. The repo's existing `LEAD_WEBHOOK_URL/AUTH` path is ~90% of this — needs a field mapper. | Medium — token + payload mapper + a support request to Inside Real Estate for the field spec. Token renews annually. | High once wired (structured contact, real source attribution). Lower up-front confidence — exact endpoint/fields **UNVERIFIED** publicly. |
| **Zapier** (Lead Dropbox "Zapier Key" + Create Contact) | Webhooks-by-Zapier catch hook fed by the Function → kvCORE "Create Contact (Post)". | Medium — paid Zapier plan + per-Zap maintenance; breaks the "all included in eXp" story. | Medium — reliable but kvCORE Zapier triggers **poll every 5–15 min**, which undercuts speed-to-lead. Fallback only. |
| **Native connectors** (Zillow/Realtor.com/Google/Meta) | Lead Engine ingests those sources natively. | N/A | Irrelevant to routing our own site form. |

## Recommended

**Primary — dual-send via the parse email.** After `lead.js` does its existing job
(KV + notify Carrie), ALSO email each validated lead to her BoldTrail parse address
via the same Resend/MailChannels code already present. Fastest to ship, zero API
access, stays inside the included tech fee, true speed-to-lead (instant vs Zapier's
5–15 min poll).

**Phase 2 — Public API v2 direct POST** once Carrie generates a Contacts token, for
structured contacts + clean source attribution (reuse the existing
`LEAD_WEBHOOK_URL/AUTH` scaffolding + a field mapper). Treat **Zapier as a no-code
fallback only.**

## Steps (parse-email primary)

1. **Grab her parse address** (do it from her seat at kickoff): BoldTrail → Lead
   Engine → "Sync any lead source in kvCORE" → EMAIL → copy the `leads+...@kvcore.com`.
2. **Cloudflare env var:** add `BOLDTRAIL_PARSE_EMAIL` (Secret) to the site's Pages
   project. Keep the existing `LEAD_FROM_EMAIL` / `RESEND_API_KEY`.
3. **`forwardToBoldTrail(env, lead)`** helper in `lead.js`, mirroring `forwardEmail()`
   but TO `env.BOLDTRAIL_PARSE_EMAIL`, parser-friendly body: `New Lead`, then
   `Name:`, `Email:`, `Phone:`, then Address/Source/Message + the attribution block.
   Set `reply_to` to the lead's email.
4. **Dual-send** in `onRequestPost`, AFTER the existing owner-notification block, in
   its own try/catch so a BoldTrail failure never 502s the lead:
   `if (env.BOLDTRAIL_PARSE_EMAIL) { try { await forwardToBoldTrail(env, lead); } catch {} }`.
   ⚠️ The current code forwards EITHER webhook OR email (webhook wins) — the dual-send
   change is REQUIRED, or turning on BoldTrail would silence Carrie's own copy.
5. **Deliverability:** confirm From-domain can reach `kvcore.com` (MailChannels
   domain-lockdown TXT, or a verified Resend domain — Resend has better inbox
   placement). A bounced parse email = a silently lost contact.
6. **Test end-to-end:** submit `/l/101-rio-ridge-dr/?utm_source=instagram` → confirm
   (a) Carrie's notification, (b) a new BoldTrail contact with right NAP, (c) the
   Instagram/listing attribution visible in the contact's notes (within ~1 min).
7. **Phase 2 (API):** Carrie generates a Contacts/All-Scopes token → store as
   `BOLDTRAIL_API_TOKEN`; get the v2 Contacts spec from Inside Real Estate support;
   reuse `forwardWebhook()` to POST mapped fields (name→first/last, email, phone→cell,
   source/UTM → source + tag). Run alongside the parse email until confirmed.

## Fallbacks
- Parse-email deliverability blocked → switch that leg to a verified Resend domain.
- v2 field spec unobtainable → keep the parse email as the permanent primary (it fully
  satisfies "nothing dies in an inbox").
- Zero-repo-change no-code → point existing `LEAD_WEBHOOK_URL` at a Zapier/Make catch
  hook + kvCORE "Create Contact (Post)" (accept the 5–15 min delay + Zapier cost).
- Belt-and-suspenders: the Function emails Carrie regardless, so even a total
  BoldTrail outage never loses a lead (she gets the notification + KV persists).

## Caveats
- **UNVERIFIED:** exact Public API v2 contact-creation path + field names (docs are a
  gated Postman collection). Confirm before relying on the direct-POST phase.
- **UNVERIFIED (account-specific):** Carrie's exact parse address / whether her eXp seat
  shows the same UI — copy the real address from her account.
- BoldTrail Zapier triggers poll every 5–15 min — do NOT use Zapier for speed-to-lead.
- No native inbound webhook exists — inbound is parse email, Zapier action, or v2 POST only.
- API tokens: max 3 active, 1-year expiry — calendar reminder if you go the API route.
- Dedup: BoldTrail matches by email (re-submits update the same contact — good); keep a
  single ingestion path per lead to avoid duplicate-source noise.
- Compliance stays clean: only real human-submitted leads forwarded; the Function already
  strips control chars/CRLF and length-caps fields (no header injection into the email).

## Sources
Inside Real Estate KB (Zapier overview, API tokens, connect-lead-sources, Realtor.com
API delivery); eXp Cloud KB (find your unique kvCORE parse email); apidocs.kvcore.com;
kvCORE Public API v2 Postman collection; sellercompass / smartagentalliance CRM-choice.
*Researched 2026-07-14; account-specific + v2-field items flagged UNVERIFIED above.*
