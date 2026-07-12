#!/usr/bin/env python3
"""Static server for the demo site + live listings proxy.

Serves this folder like `python -m http.server` AND exposes /api/listings,
which proxies Carrie's public Realtor.com agent-listings GraphQL query
(the browser can't call it directly — realtor.com sends no CORS
Access-Control-Allow-Origin header). Results are cached for 15 minutes.

Run:  python server.py [port]   (default 8091)
If this isn't running, the page falls back to its baked-in snapshot cards.
"""
import http.server
import json
import sys
import threading
import time
import urllib.request

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8091
FULFILLMENT_ID = "2202597"  # Carrie Billeaud's Realtor.com advertiser id
TTL_SECONDS = 15 * 60

GRAPHQL_URL = "https://www.realtor.com/frontdoor/graphql"
QUERY = {
    "operationName": "AgentPropertyListing",
    "variables": {
        "query": {"status": ["for_sale"], "fulfillment_id": FULFILLMENT_ID},
        "limit": 100, "offset": 0, "size": "WEB_PDP_CAROUSEL",
    },
    "query": (
        "query AgentPropertyListing($query: HomeSearchCriteria!, $limit: Int!,"
        " $size: SizeStrategy, $offset: Int) { home_search(query: $query,"
        " limit: $limit, offset: $offset) { count total results { property_id"
        " listing_id status description { baths_consolidated beds sqft }"
        " location { address { postal_code city line } } list_price"
        " primary_photo(https: true, size: $size) { href } href } } }"
    ),
}
HEADERS = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://www.realtor.com",
    "referer": "https://www.realtor.com/realestateagents/567985a6bb954c0100686dd4",
    "rdc-client-name": "agent-branding-profile",
    "rdc-client-version": "0.0.795",
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                   " (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"),
}

_cache = {"ts": 0.0, "body": None}
_lock = threading.Lock()


def fetch_listings() -> bytes:
    with _lock:
        now = time.time()
        if _cache["body"] is not None and now - _cache["ts"] < TTL_SECONDS:
            return _cache["body"]
        req = urllib.request.Request(
            GRAPHQL_URL, data=json.dumps(QUERY).encode(), headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = json.load(resp)
        hs = (raw.get("data") or {}).get("home_search") or {}
        out = {
            "fetched_at": time.strftime("%Y-%m-%d %H:%M", time.localtime(now)),
            "total": hs.get("total"),
            "results": hs.get("results") or [],
        }
        body = json.dumps(out).encode()
        _cache.update(ts=now, body=body)
        return body


# Only these file types are served; everything else (server source, docs,
# logs, dotfiles) is invisible to the web. Directory URLs may serve index.html
# but never a listing. (Code-review finding CR-001.)
ALLOWED_EXT = {".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".webp",
               ".svg", ".gif", ".ico", ".txt", ".xml", ".woff", ".woff2"}


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.rstrip("/") == "/api/listings":
            try:
                body = fetch_listings()
                self.send_response(200)
            except Exception as exc:  # log privately, answer generically
                import sys
                print(f"upstream error: {exc}", file=sys.stderr)
                body = json.dumps({"error": "upstream unavailable"}).encode()
                self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "max-age=300")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        import os as _os
        import urllib.parse as _up
        clean = _up.urlparse(self.path).path
        if clean.endswith("/"):
            clean += "index.html"
        ext = _os.path.splitext(clean)[1].lower()
        base = _os.path.basename(clean)
        if ext not in ALLOWED_EXT or base.startswith("."):
            self.send_error(404)
            return
        super().do_GET()

    def list_directory(self, path):  # never expose directory indexes
        self.send_error(404)
        return None

    def send_error(self, code, message=None, explain=None):
        # generic error text only (no path echoes / tracebacks)
        super().send_error(code, message="error", explain="")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # loopback only: the Cloudflare tunnel and local previews both use
    # localhost; nothing else on the network should reach this directly.
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as srv:
        print(f"serving demo site + /api/listings on 127.0.0.1:{PORT}")
        srv.serve_forever()
