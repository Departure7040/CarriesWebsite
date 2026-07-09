# Serving this site

Any static file server pointed at this `site/` folder works.

## Quick local preview
```powershell
cd E:\CarriesWebsite\site
python -m http.server 8080
# open http://localhost:8080
```

## Cloudflare tunnel (Brook's setup)
1. Run a local static server on a port (e.g. 8080) — python (above), or
   `caddy file-server --root E:\CarriesWebsite\site --listen :8080`.
2. Point the existing cloudflared tunnel at it. In the tunnel config
   (`%USERPROFILE%\.cloudflared\config.yml`) add an ingress rule:
   ```yaml
   ingress:
     - hostname: carrie.dubose.me
       service: http://localhost:8080
     - service: http_status:404
   ```
3. Add the DNS route: `cloudflared tunnel route dns <tunnel-name> carrie.dubose.me`
4. `cloudflared tunnel run <tunnel-name>`

The site ships `robots.txt Disallow: /` + `noindex` on every page on purpose:
it's a demo/audit artifact and must not compete with Carrie's real entity in
search. Do not remove those before showing Google anything.