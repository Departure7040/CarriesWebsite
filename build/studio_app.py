#!/usr/bin/env python3
"""Local Studio App — run the content studio as a web host on Carrie's machine.

This is the LOCAL control plane: it serves the site + studio AND exposes generate
endpoints that shell out to the render scripts (ffmpeg/Playwright/Python) on THIS
machine. That's what makes the studio's "Generate" buttons real — there's an
actual backend here, unlike the public static demo.

SECURITY — this is deliberately LOCAL-ONLY:
  * binds 127.0.0.1 on a SEPARATE port (8092), and must NOT be exposed through the
    Cloudflare tunnel (the tunnel points at :8091, the read-only public demo).
  * /api/generate runs local commands, so it is gated to loopback requests only.
Never tunnel or port-forward this. The public demo stays on server.py (:8091).

    python build/studio_app.py          # then open http://127.0.0.1:8092/studio/
    python build/studio_app.py 8093     # custom port

Generate tasks (each runs the existing scripts, one job at a time):
  content · videos · reviews · market · all
"""
import http.server
import json
import os
import subprocess
import sys
import threading
import time
import urllib.parse
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8092
REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
PY = sys.executable

# task -> ordered list of commands (run from REPO root).
TASKS = {
    "content": [[PY, "build/social/content_orchestrator.py"]],
    "reviews": [[PY, "build/reviews/build_reviews.py"],
                [PY, "build/reviews/build_review_graphics.py"]],
    "market":  [[PY, "build/market/build_report.py"],
                [PY, "build/market/build_market_posts.py"]],
    "videos":  [[PY, "build/social/batch_listing_videos.py"]],
}
TASKS["all"] = TASKS["content"] + TASKS["reviews"] + TASKS["market"] + TASKS["videos"]

# Estate microsites are PARAMETERIZED (need an address / --all), so they're resolved
# dynamically rather than living in the static TASKS map. Both rebuild the /estates/
# directory index afterward.
INDEX_CMD = [PY, "build/estates/build_estates_index.py"]


def _resolve_commands(task, body):
    """Return a list of commands for `task`, a str error message, or None if unknown."""
    if task == "estate":
        addr = (body.get("address") or "").strip()
        if not addr or len(addr) > 120:
            return "an address is required (e.g. 101 Rio Ridge Dr)"
        return [[PY, "build/estates/new_estate.py", "--address", addr], INDEX_CMD]
    if task == "estate-all":
        return [[PY, "build/estates/new_estate.py", "--all", "--skip-existing"], INDEX_CMD]
    if task in TASKS:
        return TASKS[task]
    return None

ALLOWED_EXT = {".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg",
               ".gif", ".ico", ".txt", ".xml", ".woff", ".woff2", ".pdf", ".json",
               ".mp4", ".webm", ".mov"}

# Single-job model: one render at a time (avoids clobbering + resource contention).
_job = {"id": 0, "task": None, "status": "idle", "log": [], "started": 0.0, "returncode": None}
_lock = threading.Lock()


def _run_job(task, commands):
    with _lock:
        _job.update(id=_job["id"] + 1, task=task, status="running", log=[],
                    started=time.time(), returncode=None)
    ok = True
    for cmd in commands:
        _job["log"].append(f"$ {' '.join(cmd)}")
        try:
            proc = subprocess.Popen(cmd, cwd=str(REPO), stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True)
            for line in (proc.stdout or []):  # stream output into the log
                _job["log"].append(line.rstrip())
                if len(_job["log"]) > 400:
                    _job["log"] = _job["log"][-400:]
            proc.wait()
            if proc.returncode != 0:
                ok = False
                _job["log"].append(f"! exited {proc.returncode}")
                break
        except Exception as exc:
            ok = False
            _job["log"].append(f"! error: {exc}")
            break
    _job["status"] = "done" if ok else "failed"
    _job["returncode"] = 0 if ok else 1


class Handler(http.server.SimpleHTTPRequestHandler):
    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _local_only(self):
        host = self.client_address[0]
        if host not in ("127.0.0.1", "::1", "localhost"):
            self._json(403, {"error": "local only"})
            return False
        return True

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/jobs":
            self._json(200, {k: _job[k] for k in ("id", "task", "status", "returncode")}
                       | {"log": _job["log"][-25:]})
            return
        # static (mirror server.py hardening)
        clean = parsed.path
        if not clean.endswith("/") and not os.path.splitext(clean)[1]:
            fs = os.path.join(".", clean.lstrip("/"))
            if os.path.isdir(fs) and os.path.isfile(os.path.join(fs, "index.html")):
                dest = clean + "/" + (("?" + parsed.query) if parsed.query else "")
                self.send_response(301); self.send_header("Location", dest)
                self.send_header("Content-Length", "0"); self.end_headers(); return
        if clean.endswith("/"):
            clean += "index.html"
        ext = os.path.splitext(clean)[1].lower()
        if ext not in ALLOWED_EXT or os.path.basename(clean).startswith("."):
            self.send_error(404); return
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/generate":
            self.send_error(404); return
        if not self._local_only():
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            body = {}
        task = body.get("task")
        commands = _resolve_commands(task, body)
        if commands is None:
            self._json(400, {"error": f"unknown task; choose {list(TASKS) + ['estate', 'estate-all']}"}); return
        if isinstance(commands, str):        # validation error (e.g. missing address)
            self._json(400, {"error": commands}); return
        if _job["status"] == "running":
            self._json(409, {"error": "a job is already running", "job": _job["id"]}); return
        threading.Thread(target=_run_job, args=(task, commands), daemon=True).start()
        time.sleep(0.1)
        self._json(202, {"started": task, "job": _job["id"] + 1})

    def list_directory(self, path):
        self.send_error(404); return None

    def log_message(self, format, *args):  # quieter console
        pass


if __name__ == "__main__":
    os.chdir(str(SITE))
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as srv:
        print(f"Studio app (LOCAL ONLY) on http://127.0.0.1:{PORT}/studio/")
        print("Generate tasks:", ", ".join(TASKS))
        print("Do NOT tunnel this port — the public demo stays on server.py :8091.")
        srv.serve_forever()
