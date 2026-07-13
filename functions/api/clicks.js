/**
 * GET /api/clicks  —  Cloudflare Pages Function (carriebilleaud.com)
 * -----------------------------------------------------------------------------
 * Attribution readout that backs the studio's attribution view. Returns per-code
 * click counts (and optionally the rolling log) recorded by /go/<code>.
 *
 *   GET /api/clicks            -> { ok, bound, generated_at, codes: [...] }
 *   GET /api/clicks?code=<c>   -> single code + its rolling log entries
 *
 * DEMO NOTE: inert on the static demo server (site/server.py) — runs only on
 * Cloudflare Pages. With no CLICKS_KV bound it returns an empty/mock structure
 * so the attribution view renders without error.
 *
 * =============================================================================
 * BINDINGS (Cloudflare Pages > Settings > Functions)
 *   CLICKS_KV   KV namespace BINDING. Optional — if unbound, returns bound:false
 *               and an empty codes[] (a small mock code when ?mock=1).
 * =============================================================================
 */

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function parseCode(code) {
  const i = code.lastIndexOf("-");
  if (i <= 0 || i === code.length - 1) return { slug: code, platform: "unknown" };
  return { slug: code.slice(0, i), platform: code.slice(i + 1) };
}

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const wanted = url.searchParams.get("code");
  const mock = url.searchParams.get("mock") === "1";
  const generated_at = new Date().toISOString();

  // No KV bound: empty (or tiny mock) structure so the UI still renders.
  if (!env.CLICKS_KV) {
    const codes = mock
      ? [{ code: "sample-instagram", slug: "sample", platform: "instagram", clicks: 0 }]
      : [];
    return json(200, { ok: true, bound: false, generated_at, codes });
  }

  try {
    // Single-code detail (includes rolling log).
    if (wanted) {
      const { slug, platform } = parseCode(wanted);
      const clicks = parseInt((await env.CLICKS_KV.get(`count:${wanted}`)) || "0", 10) || 0;
      let log = [];
      try {
        log = JSON.parse((await env.CLICKS_KV.get(`log:${wanted}`)) || "[]");
        if (!Array.isArray(log)) log = [];
      } catch {
        log = [];
      }
      return json(200, {
        ok: true,
        bound: true,
        generated_at,
        code: wanted,
        slug,
        platform,
        clicks,
        log,
      });
    }

    // Summary across all codes (list count:* keys).
    const codes = [];
    let cursor;
    do {
      const page = await env.CLICKS_KV.list({ prefix: "count:", cursor });
      for (const k of page.keys) {
        const code = k.name.slice("count:".length);
        const { slug, platform } = parseCode(code);
        const clicks = parseInt((await env.CLICKS_KV.get(k.name)) || "0", 10) || 0;
        codes.push({ code, slug, platform, clicks });
      }
      cursor = page.list_complete ? null : page.cursor;
    } while (cursor);

    codes.sort((a, b) => b.clicks - a.clicks);
    const total = codes.reduce((s, c) => s + c.clicks, 0);
    return json(200, { ok: true, bound: true, generated_at, total, codes });
  } catch {
    return json(200, { ok: true, bound: true, generated_at, codes: [], error: "read" });
  }
}
