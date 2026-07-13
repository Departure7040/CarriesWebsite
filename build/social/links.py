#!/usr/bin/env python3
"""
links.py — the canonical tracked-link builder for Carrie's content engine.

Closes the attribution loop:  social post -> tracked link -> property landing
page (/l/<slug>/) -> lead with a KNOWN source.

Two documented forms per (listing, platform):

  (a) DIRECT  — demo-working + simplest. All attribution lives in the query
      string, which the landing page reads CLIENT-SIDE (no server needed):
        https://carriebilleaud.com/l/<slug>/?utm_source=<platform>
            &utm_medium=social&utm_campaign=<campaign>&utm_content=<slug>

  (b) SHORT   — production. A pretty per-platform code that a Cloudflare
      redirect Function (/go/<code>) logs (click funnel) then 302s to form (a):
        https://carriebilleaud.com/go/<slug>-<platform>

Privacy (CR-007): UTMs are campaign LABELS only — never PII. The platform is a
public fact (the post lives there); no personal data ever rides in the URL.

Importable:  from links import tracked_link, short_link, all_links, PLATFORMS
CLI:         python links.py <slug> [campaign]
"""

from __future__ import annotations
from urllib.parse import urlencode

# Canonical production host. The demo serves the same paths from a Cloudflare
# tunnel on a *.dubose.me subdomain; swap CANONICAL_HOST -> the demo host at
# build time if you need the links to resolve on the live demo.
CANONICAL_HOST = "carriebilleaud.com"

# Platforms Carrie posts to. utm_source differs per platform => per-platform
# attribution falls out of the same landing page + /api/lead automatically.
PLATFORMS = ["instagram", "facebook", "tiktok", "youtube", "threads"]

DEFAULT_CAMPAIGN = "just-listed"


def base_url(slug: str, host: str = CANONICAL_HOST) -> str:
    """The un-tracked landing URL for a listing."""
    return f"https://{host}/l/{slug}/"


def tracked_link(
    slug: str,
    platform: str,
    campaign: str = DEFAULT_CAMPAIGN,
    host: str = CANONICAL_HOST,
) -> str:
    """Form (a) DIRECT — the demo + default link. UTMs read client-side."""
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}; expected one of {PLATFORMS}")
    qs = urlencode(
        {
            "utm_source": platform,
            "utm_medium": "social",
            "utm_campaign": campaign,
            "utm_content": slug,
        }
    )
    return f"{base_url(slug, host)}?{qs}"


def short_link(slug: str, platform: str, host: str = CANONICAL_HOST) -> str:
    """Form (b) SHORT — production redirect code logged by /go Function."""
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}; expected one of {PLATFORMS}")
    return f"https://{host}/go/{slug}-{platform}"


def all_links(
    slug: str, campaign: str = DEFAULT_CAMPAIGN, host: str = CANONICAL_HOST
) -> dict[str, dict[str, str]]:
    """Every platform's {direct, short} link for one listing."""
    return {
        p: {
            "direct": tracked_link(slug, p, campaign, host),
            "short": short_link(slug, p, host),
        }
        for p in PLATFORMS
    }


if __name__ == "__main__":
    import sys

    slug = sys.argv[1] if len(sys.argv) > 1 else "204-ivy-cottage-dr"
    campaign = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_CAMPAIGN
    print(f"Landing (untracked): {base_url(slug)}")
    for p, links in all_links(slug, campaign).items():
        print(f"\n{p}")
        print(f"  direct: {links['direct']}")
        print(f"  short : {links['short']}")
