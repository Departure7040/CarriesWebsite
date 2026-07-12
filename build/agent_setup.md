# AI Lead-Response Assistant — Deploy & Test (for Brook)

The site's AI chat assistant. Three moving parts:

| File | What it is |
|---|---|
| `functions/api/chat.js` | Cloudflare Pages Function, `POST /api/chat`. Calls Anthropic, runs the `capture_lead` tool loop, forwards leads through the existing `/api/lead`. |
| `functions/api/_agent_system_prompt.md` | **The compliance guardrail.** Source-of-truth copy of the system prompt (mirrored as a const in `chat.js`). |
| `site/assets/chat-widget.js` | Vanilla-JS floating chat bubble. **Not yet included on any page** (feature-flagged for launch). |

---

## 1. Set the Anthropic secret

Cloudflare Pages → project → **Settings → Environment variables → Production** (and Preview if you want it on staging):

```
ANTHROPIC_API_KEY   sk-ant-...        (encrypt as a Secret)
```

Optional vars:
- `ALLOWED_ORIGIN` — defaults to `https://carriebilleaud.com`. Set for a staging origin if testing there.
- `CHATS_KV` — bind a KV namespace (same idea as `LEADS_KV`) to enable per-IP rate limiting (20 chats / 10 min). If unbound, rate limiting silently degrades to "allow" — chat still works.
- `CHAT_MOCK` — set to `1` to return canned replies without calling Anthropic (see § Local test).

Leads captured by the bot route through the **existing** `/api/lead` pipeline, so no new lead secrets are needed — whatever `/api/lead` already uses (webhook or email) is reused automatically. Captured chat leads arrive with `source: "ai-chat"`.

## 2. Fill the `{{CALENDLY_URL}}` token

Two spots (keep them identical):
- `functions/api/chat.js` → `const CALENDLY_URL = "{{CALENDLY_URL}}";`
- `functions/api/_agent_system_prompt.md` → the booking line near the end.

Replace with Carrie's real booking link, e.g. `https://calendly.com/carriebilleaud/15min`. Until it's filled, the bot will literally say the token — so fill it before launch.

## 3. Include the widget on production pages (LAUNCH ONLY)

The widget is **feature-flagged OFF**: it's not on any page yet. To turn it on, add ONE line before `</body>` on each page that should have it (near the existing `<script src="assets/nav.js" defer></script>`):

```html
<script src="assets/chat-widget.js?v=1" defer></script>
```

Do **not** add this until: (a) `ANTHROPIC_API_KEY` is set, (b) `{{CALENDLY_URL}}` is filled, and (c) **Carrie has signed off** on the assistant. The widget does not auto-open and keeps history in memory only.

---

## Cost expectation (Haiku 4.5)

Model const is `claude-haiku-4-5` (in `chat.js`). Haiku is the cheap tier — roughly **~$1 / MTok input, ~$5 / MTok output**. A typical short lead conversation (system prompt is cached-eligible but counted here conservatively as re-sent, ~1K tokens system + a handful of short turns + a tool round-trip) lands around **1–2 cents per full conversation**, often less. Budget generously: even a busy month of hundreds of chats is single-digit dollars.

## Model upgrade (one line)

In `functions/api/chat.js`:

```js
const MODEL = "claude-haiku-4-5"; // → "claude-sonnet-5" or "claude-opus-4-8" for higher quality
```

Swap the string, redeploy. No other code changes needed. (Higher tiers cost more per token but reason better on edge-case compliance phrasing.)

---

## ⚠️ Compliance note — the system prompt IS the guardrail

`_agent_system_prompt.md` (and its mirrored copy in `chat.js`) is what stands between the bot and a fair-housing or unauthorized-advice complaint. It encodes the hard rules: no steering / no fair-housing-sensitive characterizations, no personalized legal/tax/financial/lending advice, no rates or approval promises, no invented listings/prices/stats, no guarantees, no sensitive-data collection, and always-disclose-it's-an-assistant.

**Any edit to the prompt is a compliance change and must be re-reviewed before shipping.** Keep the two copies (the `.md` and the const in `chat.js`) identical. Don't loosen a rule to make the bot "more helpful."

---

## Local test

Two options.

### A) Mock mode — no API key needed
Exercise the widget end-to-end without calling Anthropic:

```bash
# from repo root, with wrangler installed
CHAT_MOCK=1 npx wrangler pages dev site --compatibility-date=2024-01-01
```

`chat.js` sees `CHAT_MOCK=1` and returns a canned reply for any POST to `/api/chat`, so the bubble, panel, send/receive, typing indicator, and accessibility all work with zero cost and no key. (You can also temporarily add `<script src="assets/chat-widget.js" defer></script>` to a local copy of `site/index.html` to see the bubble — just don't commit that include.)

### B) Real key locally
```bash
# put the key in a local .dev.vars (gitignored) instead of exporting inline:
#   echo 'ANTHROPIC_API_KEY = "sk-ant-..."' > .dev.vars
npx wrangler pages dev site --compatibility-date=2024-01-01
```

Then POST directly to check the loop without the UI:

```bash
curl -s http://localhost:8788/api/chat \
  -H 'content-type: application/json' \
  -d '{"messages":[{"role":"user","content":"Do you have any homes in Youngsville under 300k?"}]}'
# → {"reply":"...","lead_captured":false}
```

Try a capture flow by sending a name + email/phone and asking Carrie to reach out; confirm the lead lands wherever `/api/lead` is configured to forward, tagged `source: "ai-chat"`.

### Syntax check (no deploy)
```bash
node --check functions/api/chat.js
node --check site/assets/chat-widget.js
```
