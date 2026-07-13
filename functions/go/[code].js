/**
 * GET /go/<code>  —  Cloudflare Pages Function (carriebilleaud.com)
 * -----------------------------------------------------------------------------
 * ROUTING: this file lives at functions/go/[code].js, so Cloudflare Pages maps
 * the dynamic segment to /go/<code> automatically (params.code === "<code>").
 * This is the tracked short-link the studio embeds in each social caption.
 * A DISTINCT code per platform (<slug>-<platform>) yields per-platform
 * attribution. Example: /go/1204-oak-instagram  ->  redirects to the property
 * landing page carrying UTM campaign labels.
 *
 * Behavior:
 *   1. Parse code as "<slug>-<platform>" (platform = last "-" segment).
 *   2. Log the click to CLICKS_KV binding IF bound: bump a per-code counter and
 *      append to a small rolling log (timestamp, code, slug, platform, referer,
 *      UA, cf-connecting-ip). Degrades silently to a plain redirect if unbound
 *      or on any KV error — a click is NEVER blocked on logging.
 *   3. 302 -> /l/<slug>/?utm_source=<platform>&utm_medium=social
 *              &utm_campaign=just-listed&utm_content=<slug>
 *
 * DEMO NOTE: inert on the static demo server (site/server.py). It runs only on
 * Cloudflare Pages. For the live demo, landing pages read UTMs client-side.
 *
 * =============================================================================
 * BINDINGS (Cloudflare Pages > Settings > Functions)
 *   CLICKS_KV   KV namespace BINDING (not a var). Optional — if unbound, the
 *               redirect still works; only click logging is skipped.
 * =============================================================================
 */

const MAX_LOG = 200; // rolling per-code log cap (keep KV values small)

// Split "<slug>-<platform>" -> { slug, platform }. Platform is the final
// hyphen segment; slug is everything before it. Falls back gracefully.
function parseCode(code) {
  const i = code.lastIndexOf("-");
  if (i <= 0 || i === code.length - 1) return { slug: code, platform: "unknown" };
  return { slug: code.slice(0, i), platform: code.slice(i + 1) };
}

// Only allow simple slug/platform chars into the outbound URL (defense-in-depth).
const clean = (v) => (v || "").replace(/[^a-z0-9._-]/gi, "").slice(0, 120);

async function logClick(env, ctx, entry) {
  if (!env.CLICKS_KV) return;
  const doLog = (async () => {
    try {
      const countKey = `count:${entry.code}`;
      const n = (parseInt((await env.CLICKS_KV.get(countKey)) || "0", 10) || 0) + 1;
      await env.CLICKS_KV.put(countKey, String(n));

      const logKey = `log:${entry.code}`;
      let log = [];
      try {
        log = JSON.parse((await env.CLICKS_KV.get(logKey)) || "[]");
        if (!Array.isArray(log)) log = [];
      } catch {
        log = [];
      }
      log.push(entry);
      if (log.length > MAX_LOG) log = log.slice(-MAX_LOG);
      await env.CLICKS_KV.put(logKey, JSON.stringify(log));
    } catch {
      // swallow — logging must never break the redirect
    }
  })();
  // Don't make the visitor wait on KV writes.
  if (ctx && typeof ctx.waitUntil === "function") ctx.waitUntil(doLog);
  else await doLog;
}

export async function onRequestGet(context) {
  const { request, env, params } = context;
  try {
    const code = clean(String(params.code || ""));
    if (!code) return new Response("Not found", { status: 404 });

    const { slug, platform } = parseCode(code);
    const cleanSlug = clean(slug);
    const cleanPlatform = clean(platform) || "unknown";

    await logClick(env, context, {
      ts: new Date().toISOString(),
      code,
      slug: cleanSlug,
      platform: cleanPlatform,
      referer: (request.headers.get("referer") || "").slice(0, 300),
      ua: (request.headers.get("user-agent") || "").slice(0, 300),
      ip: request.headers.get("cf-connecting-ip") || "",
    });

    const dest =
      `/l/${cleanSlug}/?utm_source=${encodeURIComponent(cleanPlatform)}` +
      `&utm_medium=social&utm_campaign=just-listed` +
      `&utm_content=${encodeURIComponent(cleanSlug)}`;

    return new Response(null, {
      status: 302,
      headers: { location: dest, "cache-control": "no-store" },
    });
  } catch {
    return new Response("Something went wrong", { status: 500 });
  }
}
