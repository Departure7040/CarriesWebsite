#!/usr/bin/env python3
"""Perpetual activity ledger for the studio performance dashboard.

Append-only log of what Carrie's marketing engine has PRODUCED over time, so the
dashboard can show cumulative totals + a trend (posts, videos, tracked links,
review graphics, market reports — by date). The generators call log_activity()
each run, so the ledger grows perpetually.

Lives at site/studio/activity.json (TRACKED + served — not under the gitignored
packages/ dir, so the history persists in the repo).

    from activity_log import log_activity
    log_activity("listing_video", 9, "active-listings batch")
"""
import datetime
import json
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent.parent / "site" / "studio" / "activity.json"


def log_activity(event_type: str, count: int, detail: str = "", date: "str | None" = None) -> Path:
    """Append one dated production event to the ledger and return its path."""
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    data = {"events": []}
    if LEDGER.exists():
        try:
            data = json.loads(LEDGER.read_text(encoding="utf-8"))
        except Exception:
            data = {"events": []}
    data.setdefault("events", []).append({
        "date": date or datetime.date.today().isoformat(),
        "type": event_type,
        "count": int(count),
        "detail": detail,
    })
    LEDGER.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return LEDGER


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        log_activity(sys.argv[1], int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
        print(f"logged {sys.argv[1]} x{sys.argv[2]} -> {LEDGER}")
    else:
        print("usage: python activity_log.py <type> <count> [detail]")
