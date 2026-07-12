/**
 * POST /api/lead  —  Cloudflare Pages Function (carriebilleaud.com)
 * -----------------------------------------------------------------------------
 * Receives the contact form (site/index.html #contact) and the valuation form
 * (site/services/sell-my-house.html #home-value), validates + anti-spams, then
 * forwards the lead to ONE of two destinations depending on which secrets are
 * set. Returns generic JSON only — never echoes submitted PII back to the
 * client (CR-007).
 *
 * =============================================================================
 * CLOUDFLARE PAGES ENV VARS / SECRETS  (Settings > Environment variables)
 * =============================================================================
 * Mode is chosen by whichever forwarding secret exists (webhook wins if both):
 *
 *   MODE (a) EMAIL
 *     LEAD_TO_EMAIL     lead inbox, e.g. carrie@carriebilleaud.com   (secret/plain)
 *     LEAD_FROM_EMAIL   verified From, e.g. no-reply@carriebilleaud.com
 *     RESEND_API_KEY    (optional) if set -> send via Resend API.        [SECRET]
 *                       If absent, falls back to MailChannels (no key; requires
 *                       the domain-lockdown DNS TXT record MailChannels needs).
 *
 *   MODE (b) CRM WEBHOOK  (BoldTrail / kvCORE lead-import webhook)
 *     LEAD_WEBHOOK_URL  full https webhook URL from BoldTrail/kvCORE.     [SECRET]
 *     LEAD_WEBHOOK_AUTH (optional) value for an Authorization header.     [SECRET]
 *
 *   SHARED (optional)
 *     LEADS_KV          KV namespace BINDING (not a var) for per-IP rate
 *                       limiting. If unbound, rate limiting silently degrades
 *                       to "allow" — the form still works.
 *     ALLOWED_ORIGIN    origin to accept, default https://carriebilleaud.com
 *
 * build/production.config.json tokens.form_destination documents the chosen
 * destination for the human build; the ACTUAL address/URL lives only in these
 * Cloudflare secrets, never in the repo.
 * =============================================================================
 */

const MAX = 4000; // hard cap on any single field length

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

// Accept both application/json and normal form-encoded POSTs.
async function readBody(request) {
  const ct = (request.headers.get("content-type") || "").toLowerCase();
  const out = {};
  if (ct.includes("application/json")) {
    const j = await request.json().catch(() => ({}));
    for (const k in j) out[k] = typeof j[k] === "string" ? j[k] : String(j[k] ?? "");
  } else {
    const form = await request.formData().catch(() => null);
    if (form) for (const [k, v] of form.entries()) out[k] = typeof v === "string" ? v : "";
  }
  // trim + cap every field
  for (const k in out) out[k] = String(out[k]).slice(0, MAX).trim();
  return out;
}

const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
const phoneOk = (v) => (v.match(/\d/g) || []).length >= 7;

// KV-optional per-IP rate limit: max 5 submissions / 10 min. Degrades to allow.
async function rateLimited(env, ip) {
  if (!env.LEADS_KV || !ip) return false;
  const key = `lead:${ip}`;
  try {
    const n = parseInt((await env.LEADS_KV.get(key)) || "0", 10) || 0;
    if (n >= 5) return true;
    await env.LEADS_KV.put(key, String(n + 1), { expirationTtl: 600 });
    return false;
  } catch {
    return false; // never block a real lead on KV failure
  }
}

async function forwardWebhook(env, lead) {
  const headers = { "content-type": "application/json" };
  if (env.LEAD_WEBHOOK_AUTH) headers["authorization"] = env.LEAD_WEBHOOK_AUTH;
  const r = await fetch(env.LEAD_WEBHOOK_URL, {
    method: "POST",
    headers,
    body: JSON.stringify(lead),
  });
  return r.ok;
}

async function forwardEmail(env, lead) {
  const to = env.LEAD_TO_EMAIL;
  const from = env.LEAD_FROM_EMAIL || "no-reply@carriebilleaud.com";
  if (!to) return false;

  const subject = `New ${lead.source || "website"} lead: ${lead.name}`;
  const text =
    `Name: ${lead.name}\n` +
    `Email: ${lead.email || "-"}\n` +
    `Phone: ${lead.phone || "-"}\n` +
    `Address: ${lead.address || "-"}\n` +
    `Source: ${lead.source || "-"}\n\n` +
    `${lead.message || ""}\n`;

  // Resend if key present, else MailChannels (keyless, Cloudflare-native).
  if (env.RESEND_API_KEY) {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        authorization: `Bearer ${env.RESEND_API_KEY}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ from, to: [to], subject, text, reply_to: lead.email || undefined }),
    });
    return r.ok;
  }

  const r = await fetch("https://api.mailchannels.net/tx/v1/send", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      personalizations: [{ to: [{ email: to }] }],
      from: { email: from, name: "Carrie Billeaud Website" },
      reply_to: lead.email ? { email: lead.email } : undefined,
      subject,
      content: [{ type: "text/plain", value: text }],
    }),
  });
  return r.ok;
}

export async function onRequestPost({ request, env }) {
  // Same-origin guard (best-effort; Origin can be absent on some clients).
  const allowed = env.ALLOWED_ORIGIN || "https://carriebilleaud.com";
  const origin = request.headers.get("origin");
  if (origin && origin !== allowed) return json(403, { ok: false });

  const ip = request.headers.get("cf-connecting-ip") || "";
  const body = await readBody(request);

  // 1. Honeypot: bots fill hidden "company" field. Pretend success, drop it.
  if (body.company) return json(200, { ok: true });

  // 2. Validation: name required + at least one of email/phone.
  const name = body.name || "";
  const email = body.email || "";
  const phone = body.phone || "";
  if (!name || name.length < 2) return json(400, { ok: false, error: "invalid" });
  if (!(emailOk(email) || phoneOk(phone))) return json(400, { ok: false, error: "invalid" });

  // 3. Rate limit (KV-optional).
  if (await rateLimited(env, ip)) return json(429, { ok: false, error: "rate" });

  const lead = {
    name,
    email: emailOk(email) ? email : "",
    phone,
    address: body.address || "",
    message: body.message || "",
    source: body.source || "website",
    submitted_at: new Date().toISOString(),
  };

  // 4. Forward. Webhook takes precedence when configured, else email.
  try {
    let ok = false;
    if (env.LEAD_WEBHOOK_URL) ok = await forwardWebhook(env, lead);
    else ok = await forwardEmail(env, lead);
    if (!ok) return json(502, { ok: false, error: "forward" });
  } catch {
    return json(502, { ok: false, error: "forward" });
  }

  return json(200, { ok: true });
}

// Anything other than POST.
export async function onRequest({ request }) {
  if (request.method === "POST") return; // handled by onRequestPost
  return json(405, { ok: false, error: "method" });
}
