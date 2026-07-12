# DNS Cutover — carriebilleaud.com: GoDaddy → Cloudflare Pages

**Goal:** replace the current GoDaddy-managed 301 redirect
(`carriebilleaud.com` → `carriebilleaud.exprealty.com`) with the new static site
hosted on Cloudflare Pages, without a search-visibility gap and with a clean
rollback. This is Step C-5 of `DEPLOY_READINESS.md`. Do it **before** the
`strip_noindex` flip (C-7), never after.

**Prerequisite:** GoDaddy delegate access secured at kickoff
(`kickoff_meeting_pack.md` §c-2). Confirm who holds the GoDaddy login before you
start — this is the #1 source of cutover delay.

---

## Decision: move nameservers to Cloudflare, or keep GoDaddy DNS + CNAME?

Two valid paths. **Recommended: Option 1 (full nameserver move to Cloudflare).**

### Option 1 — Move nameservers to Cloudflare (RECOMMENDED)
Add `carriebilleaud.com` as a zone in the Cloudflare account, then change the
authoritative nameservers at GoDaddy to the two Cloudflare assigns
(e.g. `x.ns.cloudflare.com` / `y.ns.cloudflare.com`).

**Why:** same ecosystem as Pages + the contact-form Worker, orange-cloud proxy,
edge SSL, redirect rules, and security headers (CR-012) all managed in one place;
apex support is native (CNAME flattening); future changes don't require touching
GoDaddy again. **Cost:** one nameserver change + full-zone propagation.

### Option 2 — Keep DNS at GoDaddy, point records at Pages
Leave GoDaddy authoritative; add a custom domain in Pages and create the records
GoDaddy shows you at GoDaddy.

**Why you'd pick it:** you don't want to move the whole zone (other records —
MX/email, other subdomains — live at GoDaddy and you'd rather not migrate them).
**Trade-off:** apex CNAME at GoDaddy isn't cleanly supported (see records below),
and you lose Cloudflare's edge features on this domain.

> If email (MX) or other subdomains currently live under this GoDaddy zone,
> **enumerate and reproduce them first** (Option 1: recreate every existing
> record in Cloudflare before flipping nameservers, or mail breaks). If there are
> none — likely, since the domain only does a redirect today — Option 1 is clean.

---

## Exact records

### Option 1 (nameservers on Cloudflare) — after adding the domain in Pages:
Cloudflare Pages' "Set up a custom domain" auto-creates these in the zone. Verify:

| Type | Name | Target | Proxy | TTL |
|---|---|---|---|---|
| CNAME | `carriebilleaud.com` (apex) | `<project>.pages.dev` | Proxied (orange) | Auto |
| CNAME | `www` | `<project>.pages.dev` | Proxied (orange) | Auto |

Apex CNAME works because Cloudflare flattens it to A/AAAA at the edge. Decide
apex-vs-www canonical (match the site's `canonical_host` = `https://carriebilleaud.com`,
i.e. apex) and add a Bulk Redirect / Redirect Rule so `www` → apex (301).

### Option 2 (DNS stays at GoDaddy) — use the exact values Pages shows you:

| Type | Name | Target | TTL |
|---|---|---|---|
| CNAME | `www` | `<project>.pages.dev` | 600s during cutover |
| A (apex) | `@` | (GoDaddy can't CNAME the apex — use GoDaddy "Forwarding" to `www`, or Pages' provided A record if offered) | 600s |

Apex on GoDaddy is the rough edge: GoDaddy does not support a true apex CNAME.
Either forward apex → `www` at GoDaddy and let `www` CNAME to Pages, or use any A
record Cloudflare Pages provides for apex. This is the main reason Option 1 is
recommended.

---

## TTL / propagation

- **Before cutover:** lower the TTL on the existing `carriebilleaud.com`
  record(s) to **300–600s at least 24–48h ahead** so the old redirect's cached
  answer expires quickly when you flip. (Do this while the site is still noindex.)
- **Nameserver move (Option 1):** registrar NS changes can take up to 24–48h to
  fully propagate, though usually far less. Cloudflare emails when the zone is
  active. Keep the eXp site live throughout.
- **Record-only change (Option 2):** propagates in ~TTL minutes once pushed.
- Verify with `dig carriebilleaud.com`, `dig www.carriebilleaud.com`, and
  `nslookup` from a couple of networks. Confirm SSL is **Active** in Pages before
  sending real traffic — a live domain with a not-yet-provisioned cert throws
  browser TLS errors.

---

## Replacing the existing eXp redirect

Today `carriebilleaud.com` 301-redirects to `carriebilleaud.exprealty.com` via
GoDaddy (Domain Forwarding, or a redirect record).

1. Identify the mechanism in GoDaddy: **Domain Settings → Forwarding** (most
   likely), or a parked/redirect DNS record.
2. **Do not delete it until the replacement resolves and SSL is active.** Order:
   (a) get Pages serving the domain over valid TLS (verify on `*.pages.dev` and
   then the custom domain), (b) then remove/disable the GoDaddy forwarding rule so
   it stops intercepting, (c) confirm `carriebilleaud.com` now serves the new
   site, not the old redirect.
3. **Keep `carriebilleaud.exprealty.com` live and untouched** — it remains a
   valid eXp property. Decide separately (CR-008 / plan open decision) whether it
   should `rel=canonical` to the new site to avoid duplicate-entity signals; that
   is a post-launch SEO decision, not part of the cutover.

---

## Rollback

If the new site misbehaves after cutover (TLS, wrong content, form failure,
downtime):

- **Option 2 (records at GoDaddy):** fastest rollback — re-enable the GoDaddy
  forwarding rule to `carriebilleaud.exprealty.com` (or restore the prior record).
  With a 300–600s TTL, traffic returns to the old redirect within minutes.
- **Option 1 (nameservers on Cloudflare):** either (a) in the Cloudflare zone,
  replace the Pages CNAMEs with a Redirect Rule sending `carriebilleaud.com` →
  `https://carriebilleaud.exprealty.com` (restores old behavior in ~TTL, no
  registrar change), or (b) full revert by pointing GoDaddy nameservers back to
  GoDaddy defaults (slow — up to 24–48h; prefer (a)).
- **Because the eXp site was kept live in parallel**, rollback only ever restores
  the redirect — Carrie's business is never dark. Never let `carriebilleaud.com`
  become the *only* place her business appears until the new site is fully
  verified live (C-6 smoke test passed).
- Keep the noindex flip (C-7) AFTER a stable cutover, so a rollback during the DNS
  window never exposes an unapproved/wrong-host site to search.
