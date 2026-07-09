# Serving this site

Preferred: `python server.py <port>` from this folder — serves the static site
AND the live listings feed. Any plain static file server also works (listings
then fall back to the baked-in July 2026 snapshot cards).

## Quick local preview
```powershell
cd E:\CarriesWebsite\site
python server.py 8091      # static site + live /api/listings proxy (preferred)
# or: python -m http.server 8091   (static only)
# open http://localhost:8091
```

`server.py` proxies Carrie's public Realtor.com agent-listings GraphQL query
at `/api/listings` (cached 15 min) because browsers can't call realtor.com
cross-origin. If the proxy errors, the page keeps the snapshot cards.

## Cloudflare tunnel (Brook's setup — LIVE as of 2026-07-08)
Current state: `server.py` runs on port 8091; the `2cajuns` tunnel's ingress
maps `carrie.dubose.me → http://localhost:8091` (uses `localhost`, not
`host.docker.internal` — the hosts-file entry for the latter was stale).

To (re)start after a reboot:
1. `cd E:\CarriesWebsite\site && python server.py 8091`
2. `cloudflared tunnel --config %USERPROFILE%\.cloudflared\config.yml run --credentials-file %USERPROFILE%\.cloudflared\15ba9823-f3a2-4eca-8d41-358302a348c9.json 2cajuns`

(DNS route already exists: `cloudflared tunnel route dns 2cajuns carrie.dubose.me`.)

## Gotchas
- Cloudflare edge-caches static assets. After editing `assets/style.css`,
  bump the `?v=` query on the stylesheet `<link>` in the HTML pages, or purge
  cache in the Cloudflare dashboard — otherwise visitors get stale CSS.
- The site ships `robots.txt Disallow: /` + `noindex` on every page ON
  PURPOSE: it's a demo/audit artifact and must not compete with Carrie's real
  entity in search. Do not remove those.
