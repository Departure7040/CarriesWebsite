/**
 * POST /api/nurture  —  Cloudflare Pages Function (carriebilleaud.com)
 * -----------------------------------------------------------------------------
 * Lead-nurture companion to functions/api/lead.js. Plugs the SECOND lead leak:
 * the lead who is not ready today. It DRAFTS a multi-step follow-up sequence for
 * a captured lead; a draft becomes sendable ONLY after a separate `approve`
 * call. NOTHING here auto-sends. Consent + opt-out are first-class (TCPA for
 * SMS, CAN-SPAM for email, fair-housing for content).
 *
 * Mirrors functions/api/chat.js style: no SDK, raw fetch to the Anthropic
 * Messages API (x-api-key + anthropic-version), one strict emit tool with
 * tool_choice forcing it, same-origin guard, KV-optional per-IP rate limit, and
 * generic JSON errors only — never echo PII, a stack, or raw upstream detail.
 *
 * ACTIONS (POST body {action, ...}):
 *   action="enqueue"  {lead:{first_name,email|phone,interest,source,sequence,
 *                      consent}, listing?} -> validates, REQUIRES consent, drafts
 *                      each step (real mode) or returns templated drafts (mock),
 *                      stores them to NURTURE_KV as status:"draft", returns the
 *                      drafts. Does NOT send anything.
 *   action="approve"  {queue_id, step_index} -> the ONLY path that flips a stored
 *                      draft to status:"approved" (sendable). Still does not send
 *                      on the demo — delivery is a deploy-time gateway concern.
 *
 * =============================================================================
 * CLOUDFLARE PAGES ENV VARS / SECRETS  (Settings > Environment variables)
 * =============================================================================
 *   ANTHROPIC_API_KEY  Anthropic API key. Absent -> INERT/MOCK.          [SECRET]
 *   NURTURE_MOCK       (optional) "1"/"true" -> force templated drafts, no API.
 *   NURTURE_KV         (optional) KV namespace BINDING for the draft store +
 *                      per-IP rate limit. If unbound, drafting still works but
 *                      approve/store is a no-op (demo returns drafts inline).
 *   ALLOWED_ORIGIN     origin to accept, default https://carriebilleaud.com
 *
 * On the demo static server these Functions are inert; with no key/KV this
 * returns clearly-templated mock drafts so the flow can be exercised. Document
 * the NURTURE_KV binding + ANTHROPIC_API_KEY secret alongside CHATS_KV/LEADS_KV.
 *
 * NOTE (guardrail): the SYSTEM_PROMPT below mirrors
 * build/nurture/_nurture_system_prompt.md, the compliance source of truth. Any
 * change to the prompt is a compliance change — keep the copies identical and
 * re-review before shipping.
 * =============================================================================
 */

const MODEL = "claude-sonnet-5";
const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
const MAX_TOKENS = 2048;
const MAX = 4000; // hard cap on any single free-text field
const MAX_STEPS = 12; // safety bound on steps drafted per lead
const KV_TTL = 60 * 60 * 24 * 90; // draft store retention: 90 days

const SMS_OPT_OUT = "Reply STOP to opt out";
const EMAIL_OPT_OUT =
  "Reply UNSUBSCRIBE or use the unsubscribe link to stop these emails.";
const NAP = "Carrie Billeaud, REALTOR® · eXp Realty · Acadiana";

// Built-in cadences — a compact mirror of build/nurture/sequences.yaml so the
// Function is self-contained (Functions can't read the repo YAML at runtime).
const SEQUENCES = {
  new_buyer_lead: {
    label: "New buyer lead",
    steps: [
      { day_offset: 0, channel: "email", intent: "welcome + what to expect" },
      { day_offset: 2, channel: "sms", intent: "offer a saved home search matching their stated criteria" },
      { day_offset: 7, channel: "email", intent: "share a useful local buying resource" },
      { day_offset: 21, channel: "email", intent: "gentle check-in" },
    ],
  },
  new_seller_lead: {
    label: "New seller lead",
    steps: [
      { day_offset: 0, channel: "email", intent: "welcome + what to expect selling" },
      { day_offset: 3, channel: "sms", intent: "offer a no-obligation home-value comparison Carrie runs herself" },
      { day_offset: 9, channel: "email", intent: "share a useful local selling resource" },
      { day_offset: 24, channel: "email", intent: "gentle check-in" },
    ],
  },
  past_client_checkin: {
    label: "Past-client check-in",
    steps: [
      { day_offset: 0, channel: "email", intent: "warm hello + a useful homeowner resource" },
      { day_offset: 45, channel: "sms", intent: "friendly check-in, no pitch" },
      { day_offset: 120, channel: "email", intent: "occasional value touch" },
    ],
  },
  cold_lead_reengage: {
    label: "Cold-lead re-engage",
    steps: [
      { day_offset: 0, channel: "email", intent: "low-key still-here note, easy opt-out" },
      { day_offset: 30, channel: "email", intent: "final gentle check-in; respect silence as a no" },
    ],
  },
};

// --- System prompt (mirror of build/nurture/_nurture_system_prompt.md — the
//     compliance artifact). Condensed to the operative rules; the .md is canonical.
const SYSTEM_PROMPT = `You are the lead-nurture message writer for Carrie Billeaud, a REALTOR with eXp Realty serving Lafayette and the surrounding Acadiana communities of Youngsville, Broussard, Carencro, Scott, Maurice and Milton, Louisiana. You draft warm, low-pressure follow-up messages (email and SMS) to leads who are not ready to act today. Carrie reviews, edits, and approves everything herself — you draft, she approves. EVERY message you produce is a DRAFT.

VOICE: Warm, local, genuinely helpful, unhurried. Concise and human. Never hypey, salesy, or clickbait. No exclamation-point spam, no ALL-CAPS.

NURTURE RULES (absolute):
1. Low-pressure always. Never imply urgency or scarcity ("act now," "won't last," "prices rising," "limited time"). Make it easy to say "not yet."
2. Never guarantee or predict an outcome (sale price, timeline, appreciation, ROI). A home-value comparison is always framed as something Carrie prepares by hand, no promise.
3. No mortgage rates or approval promises. Defer to a licensed lender.
4. ALWAYS include an opt-out in every message. SMS: end the body with "Reply STOP to opt out". Email: include a clear unsubscribe line.
5. Never contact without stated consent; never write copy that assumes or manufactures consent.
6. Keep her real NAP: Carrie Billeaud, REALTOR, eXp Realty, Acadiana. Never invent an office address, brokerage, or phone.

INHERITED BANS (non-negotiable, verbatim from the site content prompt):
1. No steering / fair-housing-sensitive language. Never use or imply "family-friendly," "safe"/"unsafe," "good/bad/great neighborhood," "good schools"/school rankings, "up-and-coming," crime, or any characterization tied to a protected class. Sell the home's listed facts, never the demographic. Do not echo a lead's own steering framing.
2. No unverified stats as fact (sales volume, days-on-market, appreciation, "#1 agent," home-value estimates). Never cite sales_volume or any unverified claim. Don't guess numbers.
3. No guarantees or predictions (restated — absolute).
4. Facts-only about any referenced listing: use only the given facts (address, city, price, beds, baths, sqft, status, url); omit missing fields; never invent amenities, a price, sqft, or availability.
5. No fabricated reviews or testimonials.
6. No collecting sensitive data (SSN, account/card numbers, DOB).

FACTS-ONLY: Use only the lead's own stated fields and, if a listing is referenced, that listing's given facts. Anything you don't have, omit. If required content is missing, leave a clearly-marked __FILL__ placeholder rather than inventing.

OUTPUT: Return the drafted sequence by calling the emit_nurture_drafts tool. Do not return prose outside the tool call. Email steps carry subject + body (body must contain an unsubscribe line). SMS steps carry a body ending in "Reply STOP to opt out". Every step is a DRAFT pending Carrie's approval.`;

// --- The single strict output tool (mirror of generate_nurture.py EMIT_TOOL).
const EMIT_TOOL = {
  name: "emit_nurture_drafts",
  description:
    "Emit the drafted follow-up messages for one lead's sequence, one array element per step in order. Every message must obey the facts-only, fair-housing, low-pressure, and opt-out rules. Every step is a DRAFT.",
  input_schema: {
    type: "object",
    additionalProperties: false,
    properties: {
      steps: {
        type: "array",
        items: {
          type: "object",
          additionalProperties: false,
          properties: {
            day_offset: { type: "integer" },
            channel: { type: "string", enum: ["email", "sms"] },
            intent: { type: "string" },
            subject: { type: "string" },
            body: { type: "string" },
          },
          required: ["day_offset", "channel", "body"],
        },
      },
    },
    required: ["steps"],
  },
  strict: true,
};

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
const phoneOk = (v) => (String(v).match(/\d/g) || []).length >= 7;
const clip = (v) => String(v == null ? "" : v).slice(0, MAX).trim();

// KV-optional per-IP rate limit: max 10 enqueues / 10 min. Degrades to allow.
async function rateLimited(env, ip) {
  if (!env.NURTURE_KV || !ip) return false;
  const key = `nurture_rl:${ip}`;
  try {
    const n = parseInt((await env.NURTURE_KV.get(key)) || "0", 10) || 0;
    if (n >= 10) return true;
    await env.NURTURE_KV.put(key, String(n + 1), { expirationTtl: 600 });
    return false;
  } catch {
    return false; // never block a real request on KV failure
  }
}

// Facts-only phrase for an optional referenced listing (never guessed).
function listingPhrase(listing) {
  if (!listing || typeof listing !== "object") return "";
  const bits = [];
  const addr = clip(listing.address);
  const city = clip(listing.city);
  if (addr) bits.push(addr + (city ? `, ${city}` : ""));
  else if (city) bits.push(city);
  const specs = [];
  if (clip(listing.beds)) specs.push(`${clip(listing.beds)} bed`);
  if (clip(listing.baths)) specs.push(`${clip(listing.baths)} bath`);
  if (clip(listing.sqft)) specs.push(`${clip(listing.sqft)} sq ft`);
  if (specs.length) bits.push(specs.join(", "));
  if (clip(listing.price)) bits.push(`offered at ${clip(listing.price)}`);
  return bits.join(" — ");
}

// Fair-housing / steering terms that must never reach a draft body, even in the
// deterministic mock path (the LLM path is guarded by _nurture_system_prompt.md).
// mockStep is the API-error fallback, so it echoes the lead's OWN free text —
// scrub it so a lead's "safe family-friendly area with good schools" can't be
// relayed into an outbound draft. Mirrors _scrub_interest in generate_nurture.py.
const STEERING_RE = new RegExp(
  "\\b(?:family-friendly|family friendly|families|family|safe|unsafe|safety|" +
  "good schools?|bad schools?|great schools?|school districts?|schools?|" +
  "great neighborhood|good neighborhood|bad neighborhood|nice neighborhood|" +
  "up-and-coming|up and coming|crime-free|low crime|crime)\\b",
  "gi",
);
function scrubInterest(interest) {
  return String(interest || "").replace(STEERING_RE, "").replace(/\s{2,}/g, " ").replace(/^[\s,;.\-]+|[\s,;.\-]+$/g, "");
}

// Deterministic MOCK drafter — clearly-templated, facts-only, opt-out-complete.
function mockStep(lead, step, listing) {
  const first = clip(lead.first_name) || "there";
  const interest = scrubInterest(clip(lead.interest));
  const intent = step.intent || "";
  const phrase = listingPhrase(listing);
  const interestClause = interest ? ` about ${interest}` : "";

  if (step.channel === "sms") {
    let line = `Hi ${first}, it's Carrie Billeaud with eXp Realty.`;
    if (intent.includes("saved home search") || intent.includes("criteria"))
      line += " Happy to set up a saved home search matching what you're looking for whenever you're ready — no rush.";
    else if (intent.includes("home-value") || intent.includes("comparison"))
      line += " Whenever it's useful, I can put together a no-obligation look at your home's value — just say the word.";
    else if (intent.includes("check-in"))
      line += " Just checking in — no pressure at all. Reply anytime if I can help.";
    else line += " Reaching out to say I'm here whenever it's helpful.";
    if (phrase) line += ` (Re: ${phrase}.)`;
    return {
      day_offset: step.day_offset,
      channel: "sms",
      intent,
      body: `${line}\n${SMS_OPT_OUT}\n\n[Demo mode — sample draft; Carrie approves before anything sends.]`,
      status: "draft",
    };
  }

  let subject, para;
  if (intent.includes("welcome")) {
    subject = "Welcome — here whenever you're ready";
    para = `Hi ${first},\n\nThanks so much for reaching out${interestClause}. I wanted to say a warm hello and let you know there's no pressure and no rush on my end — I'm happy to help at whatever pace works for you. When you'd like, just reply and we'll take the next small step together.`;
  } else if (intent.includes("resource")) {
    subject = "A resource you might find useful";
    para = `Hi ${first},\n\nNo ask here — just passing along a resource from my site that folks often find helpful. Take a look whenever it's convenient, and reply anytime if a question comes up.\n\nUseful resource: __FILL__ (link to the relevant on-site guide)`;
  } else if (intent.includes("check-in")) {
    subject = "Just checking in";
    para = `Hi ${first},\n\nA quick, low-key check-in — is now still a good time, or would later be easier? Totally fine to say "not yet," and I'll happily check back down the road.`;
  } else if (intent.includes("home-value") || intent.includes("comparison")) {
    subject = "Whenever it's useful — a look at your home's value";
    para = `Hi ${first},\n\nWhenever you'd find it helpful, I'm glad to put together a no-obligation comparison of your home's value — something I prepare by hand from current local sales. No commitment, and no rush at all. Just reply and I'll get started.`;
  } else {
    subject = "A quick hello from Carrie";
    para = `Hi ${first},\n\nReaching out to let you know I'm here whenever it's helpful${interestClause}. No pressure — reply anytime.`;
  }
  if (phrase) para += `\n\nRe: ${phrase}.`;

  return {
    day_offset: step.day_offset,
    channel: "email",
    intent,
    subject,
    body: `${para}\n\nWarmly,\n${NAP}\n337-258-5379\n\n${EMAIL_OPT_OUT}\n\n[Demo mode — sample draft; Carrie approves before anything sends.]`,
    status: "draft",
  };
}

function mockSequence(lead, seq, listing) {
  return seq.steps.map((s) => mockStep(lead, s, listing));
}

// Build the real-mode brief for one lead's sequence.
function buildBrief(lead, seqKey, seq, listing) {
  const stepLines = seq.steps
    .map(
      (s, i) =>
        `  Step ${i + 1}: day_offset=${s.day_offset} channel=${s.channel} intent=${s.intent}`
    )
    .join("\n");
  const phrase = listingPhrase(listing);
  const facts = phrase
    ? `\n\nREFERENCED LISTING (facts-only — do not embellish): ${phrase}`
    : "";
  return (
    "Draft the follow-up sequence below for this lead. Use ONLY the facts given. Every step is a DRAFT.\n\n" +
    `LEAD:\n  First name: ${clip(lead.first_name)}\n  Stated interest (their words): ${clip(
      lead.interest
    )}\n  Source: ${clip(lead.source)}\n\n` +
    `SEQUENCE: ${seqKey} — ${seq.label}\nSTEPS (draft one message per step, in order):\n${stepLines}` +
    facts +
    `\n\nRequirements: warm + low-pressure, no urgency, no guarantees, no rates, no steering. Email steps need a subject and a body with an unsubscribe line. SMS steps need a body ending in "${SMS_OPT_OUT}". Keep her NAP: ${NAP}.`
  );
}

// One raw call to the Anthropic Messages API. Throws on non-2xx (caller -> 502).
async function callAnthropic(env, brief) {
  const r = await fetch(ANTHROPIC_URL, {
    method: "POST",
    headers: {
      "x-api-key": env.ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: MAX_TOKENS,
      system: SYSTEM_PROMPT,
      tools: [EMIT_TOOL],
      tool_choice: { type: "tool", name: "emit_nurture_drafts" },
      messages: [{ role: "user", content: brief }],
    }),
  });
  if (!r.ok) throw new Error("anthropic_" + r.status);
  const msg = await r.json();
  const block = (Array.isArray(msg.content) ? msg.content : []).find(
    (b) => b && b.type === "tool_use" && b.name === "emit_nurture_drafts"
  );
  if (!block) throw new Error("no_tool_use");
  let input = block.input;
  if (typeof input === "string") {
    try {
      input = JSON.parse(input);
    } catch {
      input = {};
    }
  }
  const steps = input && Array.isArray(input.steps) ? input.steps : null;
  if (!steps || !steps.length) throw new Error("no_steps");
  return steps;
}

// Force status:"draft", backfill day_offset/intent by position, and GUARANTEE
// the opt-out line is present even if the model omitted it (belt-and-suspenders).
function normalizeSteps(rawSteps, seq) {
  const out = [];
  for (let i = 0; i < rawSteps.length && i < MAX_STEPS; i++) {
    const s = rawSteps[i] || {};
    const d = seq.steps[i] || {};
    const channel = s.channel || d.channel || "email";
    let body = clip(s.body);
    const step = {
      day_offset: Number.isInteger(s.day_offset) ? s.day_offset : d.day_offset || 0,
      channel,
      intent: clip(s.intent) || d.intent || "",
      status: "draft",
    };
    if (channel === "sms") {
      if (!body.toLowerCase().includes(SMS_OPT_OUT.toLowerCase()))
        body = `${body}\n${SMS_OPT_OUT}`;
    } else {
      step.subject = clip(s.subject) || "A note from Carrie";
      if (!body.toLowerCase().includes("unsubscribe"))
        body = `${body}\n\n${EMAIL_OPT_OUT}`;
    }
    step.body = body;
    out.push(step);
  }
  return out;
}

// A short opaque queue id for the KV draft store.
function makeQueueId() {
  return "nq_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 8);
}

// ---- action=enqueue ----------------------------------------------------------
async function handleEnqueue(env, body) {
  const lead = body.lead && typeof body.lead === "object" ? body.lead : {};
  const seqKey = clip(lead.sequence);
  const seq = SEQUENCES[seqKey];
  if (!seq) return json(400, { error: "bad_request" });

  // Basic identity: a name + at least one reachable, consented channel.
  const first = clip(lead.first_name);
  const email = clip(lead.email);
  const phone = clip(lead.phone);
  if (!first || first.length < 2) return json(400, { error: "bad_request" });
  if (!(emailOk(email) || phoneOk(phone))) return json(400, { error: "bad_request" });

  // CONSENT GATE — first-class. No stated consent -> hard refuse to draft.
  // Consent state is sourced from the CRM/webhook that already receives leads.
  if (lead.consent !== true && lead.consent !== "true")
    return json(403, { error: "consent_required" });

  const cleanLead = { first_name: first, interest: clip(lead.interest), source: clip(lead.source) };
  const listing = body.listing && typeof body.listing === "object" ? body.listing : null;

  // Draft: real mode if a key is present and not forced to mock; else mock.
  const mock =
    !env.ANTHROPIC_API_KEY ||
    env.NURTURE_MOCK === "1" ||
    env.NURTURE_MOCK === "true";

  let steps;
  let usedMock = mock;
  if (mock) {
    steps = mockSequence(cleanLead, seq, listing);
  } else {
    try {
      steps = normalizeSteps(await callAnthropic(env, buildBrief(cleanLead, seqKey, seq, listing)), seq);
    } catch {
      // Fall back to mock on any API error (matches the generator). Never 500.
      steps = mockSequence(cleanLead, seq, listing);
      usedMock = true;
    }
  }

  const queueId = makeQueueId();
  const record = {
    queue_id: queueId,
    lead: cleanLead,
    sequence: seqKey,
    sequence_label: seq.label,
    consent: true,
    listing: listing || null,
    steps, // every step is status:"draft"
    mock: usedMock,
    created_at: new Date().toISOString(),
  };

  // Store to KV (optional). If unbound, the demo still returns the drafts inline.
  if (env.NURTURE_KV) {
    try {
      await env.NURTURE_KV.put(`draft:${queueId}`, JSON.stringify(record), {
        expirationTtl: KV_TTL,
      });
    } catch {
      // Storage failure must not leak detail; the drafts are still returned.
    }
  }

  return json(200, {
    queue_id: queueId,
    sequence: seqKey,
    mock: usedMock,
    stored: !!env.NURTURE_KV,
    steps, // drafts only — NOTHING is sendable until an approve call
  });
}

// ---- action=approve ----------------------------------------------------------
// The ONLY path that flips a stored draft to "approved" (sendable). Even then,
// no code path here delivers a message on the demo — delivery is a deploy-time
// gateway concern, and STOP/unsubscribe suppression is honored before any send.
async function handleApprove(env, body) {
  const queueId = clip(body.queue_id);
  const idx = Number(body.step_index);
  if (!queueId || !Number.isInteger(idx) || idx < 0)
    return json(400, { error: "bad_request" });

  if (!env.NURTURE_KV) {
    // No store on the demo — approval is a client-side concept here.
    return json(200, { ok: true, stored: false, status: "approved", note: "demo_no_store" });
  }

  try {
    const raw = await env.NURTURE_KV.get(`draft:${queueId}`);
    if (!raw) return json(404, { error: "not_found" });
    const record = JSON.parse(raw);
    if (!Array.isArray(record.steps) || idx >= record.steps.length)
      return json(400, { error: "bad_request" });
    record.steps[idx].status = "approved"; // the sendable flip — approval only
    record.steps[idx].approved_at = new Date().toISOString();
    await env.NURTURE_KV.put(`draft:${queueId}`, JSON.stringify(record), {
      expirationTtl: KV_TTL,
    });
    return json(200, { ok: true, stored: true, status: "approved" });
  } catch {
    return json(502, { error: "store" });
  }
}

export async function onRequestPost({ request, env }) {
  // Same-origin guard (best-effort; Origin can be absent on some clients).
  const allowed = env.ALLOWED_ORIGIN || "https://carriebilleaud.com";
  const origin = request.headers.get("origin");
  if (origin && origin !== allowed) return json(403, { error: "forbidden" });

  const ip = request.headers.get("cf-connecting-ip") || "";

  const body = await request.json().catch(() => null);
  if (!body || typeof body !== "object") return json(400, { error: "bad_request" });

  const action = clip(body.action) || "enqueue";

  if (action === "enqueue") {
    if (await rateLimited(env, ip)) return json(429, { error: "rate" });
    return handleEnqueue(env, body);
  }
  if (action === "approve") {
    return handleApprove(env, body);
  }
  return json(400, { error: "bad_request" });
}

// Anything other than POST.
export async function onRequest({ request }) {
  if (request.method === "POST") return; // handled by onRequestPost
  return json(405, { error: "method" });
}
