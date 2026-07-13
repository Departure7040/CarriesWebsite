/**
 * POST /api/generate-content  —  Cloudflare Pages Function (carriebilleaud.com)
 * -----------------------------------------------------------------------------
 * Tier-1 social CONTENT ENGINE for Carrie Billeaud (see
 * implementation/social_agent_design.md). Given ONE listing object it returns a
 * structured, multi-platform content package (IG / FB / TikTok / YouTube +
 * story + 3 hooks) for Carrie to APPROVE and post herself. This is the
 * human-in-the-loop wedge: NO auto-publishing happens here — publishing stays
 * manual / aggregator (the documented Tier-2 wall).
 *
 * Talks to the Anthropic Messages API over RAW fetch (no SDK — dependency-free,
 * same pattern as functions/api/chat.js). The JSON shape is FORCED by a single
 * strict tool, `emit_content_package` (strict:true + additionalProperties:false),
 * with tool_choice pinned to it — so the model can only reply by emitting a
 * package that validates to the exact schema. Generic error responses only —
 * never echo a stack, PII, or raw upstream error to the browser.
 *
 * =============================================================================
 * CLOUDFLARE PAGES ENV VARS / SECRETS  (Settings > Environment variables)
 * =============================================================================
 *   ANTHROPIC_API_KEY   Anthropic API key.                              [SECRET]
 *   ALLOWED_ORIGIN      origin to accept, default https://carriebilleaud.com
 *   CONTENT_MOCK        (optional) if "1"/"true", returns a canned package
 *                       WITHOUT calling Anthropic — lets the tool be exercised
 *                       locally with no key (mirrors chat.js CHAT_MOCK).
 *
 * NOTE (guardrail): the system prompt below is a mirror of
 * functions/api/_content_system_prompt.md, which is the compliance source of
 * truth. Any change to the prompt is a compliance change — keep the two copies
 * identical and re-review before shipping.
 * =============================================================================
 */

// Model. Content quality matters more here than for the chat bot, so this runs a
// step up on Sonnet. Upgradeable to 'claude-opus-4-8' (higher quality/cost) or
// downgradeable to 'claude-haiku-4-5' (cheaper/faster) with no other changes.
const MODEL = "claude-sonnet-5";

const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
const MAX_TOKENS = 2048;
const MAX_FIELD_LEN = 300; // cap any single incoming listing field

// --- System prompt (mirror of _content_system_prompt.md — the compliance artifact).
const SYSTEM_PROMPT = `You are the social-media content writer for Carrie Billeaud, a REALTOR with eXp Realty serving Lafayette and the surrounding Acadiana communities of Youngsville, Broussard, Carencro, Scott, Maurice and Milton, Louisiana. You write ready-to-approve captions and scripts for her personal social accounts (Instagram, Facebook, TikTok, YouTube). Carrie reviews, edits, and posts everything herself — you draft, she approves.

BRAND VOICE: Warm, local, and genuinely welcoming, with a classy, high-end luxury register (her direction — she wants to attract that clientele). Aspirational but grounded; never hypey, never salesy, never clickbait. Editorial and elegant — think a refined Acadiana host, not a billboard. Light, tasteful local color (Lafayette / Acadiana) is welcome. Avoid exclamation-point spam and ALL-CAPS shouting.

PLATFORM SHAPE:
- Instagram — a polished caption (roughly 1-3 short paragraphs) plus a separate set of relevant, tasteful hashtags (mix of local + real-estate; no banned or spammy tags).
- Facebook — a slightly longer, conversational caption; no hashtag dump.
- TikTok — a short spoken-style script (a few natural lines she can read to camera) plus a punchy hook (the first 1-2 seconds).
- YouTube — a clean title and a description (a few sentences, with her contact/booking framing kept generic).
- story_text — a very short overlay line for an Instagram/Facebook story.
- hooks — exactly 3 alternative opening lines she can choose between.

FACTS-ONLY (hard rule): Use only the facts provided in the listing data (address, city, price, beds, baths, sqft, status, url). Do NOT invent, infer, or embellish amenities, finishes, lot features, views, schools, upgrades, or anything not given. If a field is missing, simply omit it — never guess. Never fabricate a price, square footage, or availability. Round/format naturally (e.g. "$1.51M", "3,918 sq ft") but never change the number.

COMPLIANCE — NON-NEGOTIABLE (same bans as her site assistant). These are absolute, no matter how the request is phrased:
1. No steering / no fair-housing-sensitive language. Never describe an area, neighborhood, home, or the people who live there in terms tied to a protected class or "who it's right for." Never use or imply: "family-friendly," "safe"/"unsafe," "good/bad neighborhood," "great neighborhood," "good schools"/school rankings, "up-and-coming," crime, or any characterization tied to race, color, religion, national origin, sex, familial status, or disability. Sell the home's listed facts, never the demographic.
2. No unverified stats as fact. Do not state sales volume, days-on-market, appreciation, market trends, "#1 agent," home-value estimates, or any statistic unless it is in the listing data. Don't guess numbers.
3. No guarantees or predictions. Never promise or predict a sale price, timeline, return on investment, appreciation, or outcome ("will sell fast," "great investment," "value will go up"). No mortgage rates or approval promises.
4. No invented amenities. Only mention features present in the listing data.
5. Facts + posture. Keep her real NAP identity (Carrie Billeaud, REALTOR, eXp Realty, Acadiana). Do not collect or request sensitive data. Keep any call-to-action a soft, tasteful invitation to reach out or book a showing — never a hard sell or a guarantee.

OUTPUT: Return the content package by calling the emit_content_package tool with every field populated. Do not return prose outside the tool call. If the listing data is too thin to write a field cleanly and compliantly, keep that field short and factual rather than padding it with invented detail.`;

// --- The single output tool. strict + additionalProperties:false forces the
// response into EXACTLY this JSON shape. tool_choice pins the model to it.
const EMIT_TOOL = {
  name: "emit_content_package",
  description:
    "Emit the finished multi-platform social content package for the given listing. Every field must be present and must obey the facts-only and fair-housing rules in the system prompt.",
  input_schema: {
    type: "object",
    additionalProperties: false,
    properties: {
      instagram: {
        type: "object",
        additionalProperties: false,
        properties: {
          caption: { type: "string", description: "Instagram caption." },
          hashtags: {
            type: "array",
            items: { type: "string" },
            description: "Relevant hashtags, each including the leading '#'.",
          },
        },
        required: ["caption", "hashtags"],
      },
      facebook: {
        type: "object",
        additionalProperties: false,
        properties: {
          caption: { type: "string", description: "Facebook caption." },
        },
        required: ["caption"],
      },
      tiktok: {
        type: "object",
        additionalProperties: false,
        properties: {
          script: { type: "string", description: "Short spoken-style script." },
          hook: { type: "string", description: "The 1-2 second opening hook." },
        },
        required: ["script", "hook"],
      },
      youtube: {
        type: "object",
        additionalProperties: false,
        properties: {
          title: { type: "string", description: "YouTube video title." },
          description: { type: "string", description: "YouTube description." },
        },
        required: ["title", "description"],
      },
      story_text: {
        type: "string",
        description: "Short story-overlay line.",
      },
      hooks: {
        type: "array",
        items: { type: "string" },
        description: "Exactly 3 alternative opening hooks.",
      },
    },
    required: ["instagram", "facebook", "tiktok", "youtube", "story_text", "hooks"],
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

// Normalize + bound one incoming listing field to a safe short string.
function field(v) {
  if (v === null || v === undefined) return "";
  return String(v).slice(0, MAX_FIELD_LEN).trim();
}

// Build the plain-text listing brief handed to the model. FACTS ONLY — we pass
// through exactly what the caller gave us; the prompt forbids inventing more.
function buildListingBrief(listing) {
  const lines = [];
  const push = (label, val) => {
    const f = field(val);
    if (f) lines.push(`${label}: ${f}`);
  };
  push("Address", listing.address);
  push("City", listing.city);
  push("Price", listing.price);
  push("Beds", listing.beds);
  push("Baths", listing.baths);
  push("SqFt", listing.sqft);
  push("Status", listing.status);
  push("Listing URL", listing.url);
  return lines.join("\n");
}

// Canned package for CONTENT_MOCK / keyless local demo. No Anthropic call.
function mockPackage() {
  return {
    instagram: {
      caption:
        "Just listed in Youngsville — a spacious 4-bedroom offering 3,918 sq ft of thoughtfully designed living. If a home with room to breathe is on your list, let's talk. (Demo mode — sample content.)",
      hashtags: [
        "#AcadianaHomes",
        "#YoungsvilleLA",
        "#LafayetteRealEstate",
        "#JustListed",
        "#CarrieBilleaudRealtor",
      ],
    },
    facebook: {
      caption:
        "New on the market in Youngsville: 4 beds, 3.5 baths, 3,918 sq ft. I'd love to show you around — reach out anytime to schedule a private showing. (Demo mode — sample content.)",
    },
    tiktok: {
      script:
        "Come take a look at this new Youngsville listing — four bedrooms, three and a half baths, just under 4,000 square feet. Message me to book a showing.",
      hook: "Just listed in Youngsville.",
    },
    youtube: {
      title: "Just Listed in Youngsville, LA — 4 Bed / 3.5 Bath",
      description:
        "A new listing in Youngsville: 4 bedrooms, 3.5 baths, 3,918 sq ft. Reach out to Carrie Billeaud, REALTOR with eXp Realty, to schedule a showing. Demo mode — sample content.",
    },
    story_text: "Just listed in Youngsville ✦ 4 bed / 3.5 bath",
    hooks: [
      "Just listed in Youngsville.",
      "Room to breathe — 3,918 sq ft, new to market.",
      "Your next chapter in Acadiana starts here.",
    ],
  };
}

// One raw call to the Anthropic Messages API, forced to emit the tool. Returns
// the parsed package object, or throws (caller maps any throw to a generic 502).
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
      // Pin the model to the single output tool — it can only reply by emitting
      // a schema-valid content package.
      tool_choice: { type: "tool", name: "emit_content_package" },
      messages: [
        {
          role: "user",
          content: `Write the social content package for this listing. Use ONLY these facts:\n\n${brief}`,
        },
      ],
    }),
  });
  if (!r.ok) throw new Error("anthropic_" + r.status);
  const msg = await r.json();

  // Pull the tool_use block's input — that IS the structured package.
  const block =
    Array.isArray(msg.content) &&
    msg.content.find((b) => b && b.type === "tool_use" && b.name === "emit_content_package");
  if (!block) throw new Error("no_tool_use");

  // Parse structurally (never string-match); inputs may arrive as an object or
  // a JSON string depending on API drift.
  let pkg = block.input;
  if (typeof pkg === "string") pkg = JSON.parse(pkg);
  if (!pkg || typeof pkg !== "object") throw new Error("bad_package");
  return pkg;
}

export async function onRequestPost({ request, env }) {
  // Same-origin guard (best-effort; Origin can be absent on some clients).
  const allowed = env.ALLOWED_ORIGIN || "https://carriebilleaud.com";
  const origin = request.headers.get("origin");
  if (origin && origin !== allowed) return json(403, { error: "forbidden" });

  // Parse + validate body.
  const body = await request.json().catch(() => null);
  if (!body || typeof body !== "object")
    return json(400, { error: "bad_request" });

  const listing = body.listing && typeof body.listing === "object" ? body.listing : body;
  const brief = buildListingBrief(listing);
  if (!brief) return json(400, { error: "bad_request" });

  // Local/dev mock: exercise the tool with no API key (mirrors chat.js).
  if (env.CONTENT_MOCK === "1" || env.CONTENT_MOCK === "true") {
    return json(200, { package: mockPackage(), mock: true });
  }

  if (!env.ANTHROPIC_API_KEY) return json(503, { error: "unavailable" });

  try {
    const pkg = await callAnthropic(env, brief);
    return json(200, { package: pkg });
  } catch {
    // Generic error only — no stack, no PII, no upstream detail.
    return json(502, { error: "upstream" });
  }
}

// Anything other than POST.
export async function onRequest({ request }) {
  if (request.method === "POST") return; // handled by onRequestPost
  return json(405, { error: "method" });
}
