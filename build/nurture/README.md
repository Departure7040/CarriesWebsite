# Lead-Nurture Engine

Plugs the **second lead leak**: the lead who is *not ready today*. When someone
reaches out but isn't ready to buy or sell yet, most follow-up either never
happens or turns into pressure. This engine drafts a warm, low-pressure,
multi-step follow-up sequence for that lead — and **Carrie approves every message
before anything sends.**

> Nothing here auto-sends or auto-posts. Every generated message is a **draft**.
> Consent and opt-out are first-class. The system prompt is the compliance
> guardrail.

---

## The model: trigger → draft → approve → send

| Stage | What happens | Where |
|-------|--------------|-------|
| **trigger** | A captured lead (from `/api/lead` — contact form, sell-my-house valuation, or ai-chat `capture_lead`) is enqueued into **one** sequence, keyed by what the lead is (buyer / seller / past client / cold). Enqueue **requires a stated-consent flag** on the lead. | `functions/api/nurture.js` (`action=enqueue`) / `generate_nurture.py` |
| **draft** | For each step of that sequence, the copy is drafted — real Anthropic path or a deterministic mock. Every draft is `status:"draft"`. | `generate_nurture.py`, `nurture.js` |
| **approve** | Carrie reviews each drafted message and Approves / Edits / Skips it. **Approval is the only thing that flips a draft to sendable.** | `site/studio/nurture.html` (demo, client-side) / `nurture.js` (`action=approve`) |
| **send** | Only an approved draft may send, on its `day_offset`, through the messaging gateway wired at deploy. STOP / unsubscribe suppression is honored first. | *out of scope here (deploy-time integration)* |

The four cadences live in **`sequences.yaml`** — spaced in **days, not hours**, so
there is no urgency/pressure feel:

- `new_buyer_lead` — welcome → criteria-matched saved-search offer → useful buyer resource → gentle check-in
- `new_seller_lead` — welcome → no-obligation value-comparison offer → useful seller resource → gentle check-in
- `past_client_checkin` — warm hello + resource → friendly check-in → occasional value touch
- `cold_lead_reengage` — low-key "still here" → one final gentle check-in, then stop

---

## Consent / opt-out posture

- **Consent is required before any real-mode drafting.** `nurture.js` hard-refuses
  (`403 consent_required`) an enqueue whose lead does not carry `consent:true`.
  The generator skips a lead with no `consent`. Consent state is **sourced from
  the CRM/webhook** that already receives leads (via `/api/lead`) — this engine
  does not collect or own consent, it honors it.
- **Every message carries its opt-out line**, guaranteed both by the drafter and
  by a belt-and-suspenders normalization pass:
  - **SMS** → body ends with `Reply STOP to opt out` *(TCPA)*
  - **email** → body includes an unsubscribe line *(CAN-SPAM)*
  The studio UI surfaces the opt-out line visibly and **blocks approval** of any
  message missing it.
- **Content compliance** (fair-housing / no steering, facts-only about any
  referenced listing, no unverified stats incl. `sales_volume`, no guarantees, no
  mortgage rates) is enforced by **`_nurture_system_prompt.md`** — the guardrail —
  which inherits every ban from `functions/api/_content_system_prompt.md`.
- **Nothing auto-sends.** No code path on the demo delivers a message. Real-mode
  delivery, and the STOP/unsubscribe suppression loop, are wired to the chosen
  SMS/email provider at deploy — this engine only proves the draft → approve gate.

---

## Run it

Drafting runs **without an API key** (mock mode) so the queue is never empty:

```bash
# Mock unless ANTHROPIC_API_KEY is set — drafts the 4 sample leads (one per sequence)
python build/nurture/generate_nurture.py

# Force mock even with a key present
NURTURE_MOCK=1 python build/nurture/generate_nurture.py

# Real Anthropic drafting (claude-sonnet-5, system = _nurture_system_prompt.md)
ANTHROPIC_API_KEY=sk-... python build/nurture/generate_nurture.py

# Draft your own leads (JSON array of {first_name, interest, source, sequence, consent, listing?})
python build/nurture/generate_nurture.py --leads my_leads.json
```

Requires `pyyaml` (also used to read `data/known_claims.yaml`).

### Where the queue lands

The generator writes the same review queue to two places:

- `build/nurture/out/queue.sample.json` — the build-side artifact
- `site/studio/packages/nurture/queue.sample.json` — the copy the studio reads

Each is `{ generated, note, count, leads:[ {first_name, interest, source,
sequence, sequence_label, consent, listing, steps:[…], mock} ] }`. Every step
carries `day_offset`, `channel`, `intent`, the draft (`subject`+`body` for email,
`body` for SMS), and `status:"draft"`.

### Review / approve in the studio

```bash
python -m http.server 8080     # serve the repo from root
# open  http://localhost:8080/site/studio/nurture.html
```

The page fetches `./packages/nurture/queue.sample.json`, groups drafts by lead
then step, shows channel / day-offset / intent / the message / the opt-out line,
and offers **Approve / Edit / Skip** per message. Approvals are saved in
`localStorage` only (demo — no real send). *(Opening the file over `file://`
will 404 the queue — serve from root, same as the content studio.)*

---

## The Function's approve gate (`functions/api/nurture.js`)

Mirrors `chat.js` / `lead.js`: no SDK, raw fetch to Anthropic, strict emit tool,
same-origin guard, KV-optional rate limit, generic JSON errors (never echoes PII
or a stack). Two actions:

- `POST {action:"enqueue", lead, listing?}` — validates, **requires consent**,
  drafts each step (real mode) or returns templated drafts (mock), stores them to
  `NURTURE_KV` as `status:"draft"`, and returns the drafts. **Sends nothing.**
- `POST {action:"approve", queue_id, step_index}` — the **only** path that flips a
  stored draft to `status:"approved"`. Even then, no code path here delivers a
  message on the demo.

Inert/mock when `ANTHROPIC_API_KEY` is absent or `NURTURE_MOCK` is set. `node
--check functions/api/nurture.js` passes.

---

## Deploy integration (not done here — see `integration_needs`)

- **`NURTURE_KV`** — a KV namespace binding for the draft store + rate limit
  (document alongside `CHATS_KV` / `LEADS_KV`).
- **`ANTHROPIC_API_KEY`** — secret for real-mode drafting. Absent → inert/mock.
- **`/api/lead` reuse** — a real enqueue originates from an already-captured lead;
  `nurture.js` consumes lead fields (name, email/phone, interest, source, consent)
  but does **not** re-implement lead capture or forwarding.
- **A "Nurture" tile/link in `site/studio/index.html`** pointing to `./nurture.html`
  (owned by the orchestrator — this engine does not edit the studio index).
- **Messaging gateway + suppression** — SMS/email delivery and the STOP/unsubscribe
  honor loop are wired to the chosen provider at deploy.
