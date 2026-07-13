#!/usr/bin/env python3
"""
generate_nurture.py — the "captured lead -> drafted follow-up sequence" step of
Carrie Billeaud's lead-nurture engine (the SECOND lead leak: the lead who is not
ready today).

WHAT IT DOES (human-in-the-loop, NOT auto-send):
  1. Loads the cadence definitions from build/nurture/sequences.yaml.
  2. For a given LEAD {first_name, interest, source, optional listing} and a
     SEQUENCE KEY, drafts the copy for every step of that sequence.
        - email step -> {subject, body}   (body carries an unsubscribe line)
        - sms   step -> {body}            (body ends with "Reply STOP to opt out")
  3. Writes a REVIEW QUEUE JSON — an array of lead entries, each with its
     sequence key and an ordered steps[] list; EVERY step carries
     status:"draft" (nothing is sendable until Carrie approves it in the studio).
        - build/nurture/out/queue.sample.json           (build-side artifact)
        - site/studio/packages/nurture/queue.sample.json (studio reads this)

DRAFTING mirrors build/social/content_orchestrator.py exactly:
  - Real path: urllib raw POST to the Anthropic Messages API, model
    claude-sonnet-5, system = build/nurture/_nurture_system_prompt.md (the
    compliance artifact), a single strict `emit_nurture_drafts` tool with
    tool_choice forcing it, x-api-key + anthropic-version:2023-06-01 headers.
    Gated on ANTHROPIC_API_KEY present AND NURTURE_MOCK unset.
  - MOCK path: a deterministic, clearly-templated, facts-only draft per step
    (each with its opt-out line) when there is no key or NURTURE_MOCK=1. Falls
    back to mock on ANY API error (matches the orchestrator).

COMPLIANCE holds in mock too: every mock draft is built only from the lead's own
stated fields (first_name, free-text interest) and, if a listing is referenced,
only that listing's given facts — nothing is invented, no steering language, no
guarantees, no rates, and every message includes its opt-out line. See
_nurture_system_prompt.md — it IS the guardrail.

Run (mock unless a key is set):

    python build/nurture/generate_nurture.py                 # sample leads, mock
    NURTURE_MOCK=1 python build/nurture/generate_nurture.py  # force mock
    python build/nurture/generate_nurture.py --leads my_leads.json

NOTHING here sends. It only DRAFTS and writes the review queue. The approve/send
gate lives in functions/api/nurture.js (real deploy) and the studio UI.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

try:
    import yaml  # PyYAML — also used to read data/known_claims.yaml elsewhere
except ImportError:  # pragma: no cover - clear message beats a stack trace
    raise SystemExit(
        "PyYAML is required: pip install pyyaml  (needed to read sequences.yaml)"
    )

REPO = Path(__file__).resolve().parent.parent.parent
NURTURE_DIR = REPO / "build" / "nurture"
SEQUENCES_FILE = NURTURE_DIR / "sequences.yaml"
PROMPT_FILE = NURTURE_DIR / "_nurture_system_prompt.md"
OUT_DIR = NURTURE_DIR / "out"
# Publish a copy into the served web root so the studio (a real subsite at
# /studio/) can load the queue through a relative fetch, exactly like the
# content studio loads ./packages/index.json.
STUDIO_QUEUE_DIR = REPO / "site" / "studio" / "packages" / "nurture"

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"  # mirrors content_orchestrator.py / generate-content.js
MAX_TOKENS = 2048

# --- Compliance artifact: kept identical to _nurture_system_prompt.md and to the
#     copy in functions/api/nurture.js. Any edit here is a compliance change.
#     Loaded from the .md so the guardrail lives in exactly one authored place.
SYSTEM_PROMPT = PROMPT_FILE.read_text(encoding="utf-8")

# --- The single strict output tool. additionalProperties:false so inputs
#     validate exactly; tool_choice forces it (mirror of EMIT_TOOL).
EMIT_TOOL = {
    "name": "emit_nurture_drafts",
    "description": (
        "Emit the drafted follow-up messages for one lead's sequence. One array "
        "element per step, in order. Every message must obey the facts-only, "
        "fair-housing, low-pressure, and opt-out rules. Every step is a DRAFT."
    ),
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "day_offset": {"type": "integer"},
                        "channel": {"type": "string", "enum": ["email", "sms"]},
                        "intent": {"type": "string"},
                        # email fields (present for email channel)
                        "subject": {"type": "string"},
                        # body: for email = the message body incl. unsubscribe
                        # line; for sms = the message ending in the STOP line.
                        "body": {"type": "string"},
                    },
                    "required": ["day_offset", "channel", "body"],
                },
            }
        },
        "required": ["steps"],
    },
    "strict": True,
}

SMS_OPT_OUT = "Reply STOP to opt out"
EMAIL_OPT_OUT = "Reply UNSUBSCRIBE or use the unsubscribe link to stop these emails."
NAP = "Carrie Billeaud, REALTOR® · eXp Realty · Acadiana"


# --------------------------------------------------------------------------- #
# Sequence + lead loading
# --------------------------------------------------------------------------- #
def load_sequences() -> dict:
    data = yaml.safe_load(SEQUENCES_FILE.read_text(encoding="utf-8")) or {}
    seqs = data.get("sequences") or {}
    if not seqs:
        raise SystemExit(f"No sequences defined in {SEQUENCES_FILE}")
    return seqs


def sample_leads() -> list[dict]:
    """Demo leads — one per sequence — so the queue is never empty. These are
    obviously-sample identities (first names + free-text interest only); NO real
    contact data and NO invented market facts. `consent` is set true here purely
    so the demo queue renders; real-mode enqueue sources consent from the CRM."""
    return [
        {
            "first_name": "SAMPLE-Buyer",
            "interest": "buying a first home in the Youngsville area, budget around 250k",
            "source": "contact-form",
            "sequence": "new_buyer_lead",
            "consent": True,
        },
        {
            "first_name": "SAMPLE-Seller",
            "interest": "thinking about selling their current home in Lafayette",
            "source": "sell-my-house-valuation",
            "sequence": "new_seller_lead",
            "consent": True,
        },
        {
            "first_name": "SAMPLE-PastClient",
            "interest": "closed with Carrie last year; stay-in-touch",
            "source": "past-client",
            "sequence": "past_client_checkin",
            "consent": True,
        },
        {
            "first_name": "SAMPLE-ColdLead",
            "interest": "browsed listings months ago, went quiet",
            "source": "ai-chat",
            "sequence": "cold_lead_reengage",
            "consent": True,
            # Optional listing reference — facts-only if present. Left absent here.
        },
    ]


# --------------------------------------------------------------------------- #
# Brief building + real Anthropic call
# --------------------------------------------------------------------------- #
def listing_facts_lines(listing: dict | None) -> list[str]:
    """Only the given listing facts, never guessed. Missing fields omitted."""
    if not listing:
        return []
    fields = [
        ("Address", listing.get("address")),
        ("City", listing.get("city")),
        ("Price", listing.get("price")),
        ("Beds", listing.get("beds")),
        ("Baths", listing.get("baths")),
        ("SqFt", listing.get("sqft")),
        ("Status", listing.get("status")),
        ("Listing URL", listing.get("url")),
    ]
    return [f"  {k}: {v}" for k, v in fields if str(v or "").strip()]


def build_brief(lead: dict, seq_key: str, seq: dict) -> str:
    steps = seq.get("steps", [])
    step_lines = [
        f"  Step {i + 1}: day_offset={s['day_offset']} channel={s['channel']} "
        f"intent={s['intent']}"
        for i, s in enumerate(steps)
    ]
    listing = lead.get("listing")
    facts = listing_facts_lines(listing)
    parts = [
        "Draft the follow-up sequence below for this lead. Use ONLY the facts "
        "given here. Every step is a DRAFT for Carrie to approve.",
        "",
        "LEAD:",
        f"  First name: {lead.get('first_name', '')}",
        f"  Stated interest (their words): {lead.get('interest', '')}",
        f"  Source: {lead.get('source', '')}",
        "",
        f"SEQUENCE: {seq_key} — {seq.get('description', '')}",
        "STEPS (draft one message per step, in this exact order):",
        *step_lines,
    ]
    if facts:
        parts += ["", "REFERENCED LISTING (facts-only — do not embellish):", *facts]
    parts += [
        "",
        "Requirements: warm + low-pressure, no urgency, no guarantees, no rates, "
        "no steering/fair-housing-sensitive language. Email steps need a subject "
        "and a body with an unsubscribe line. SMS steps need a body ending in "
        f'"{SMS_OPT_OUT}". Keep her NAP: {NAP}.',
    ]
    return "\n".join(parts)


def call_anthropic(api_key: str, brief: str) -> list[dict]:
    body = json.dumps({
        "model": MODEL, "max_tokens": MAX_TOKENS, "system": SYSTEM_PROMPT,
        "tools": [EMIT_TOOL],
        "tool_choice": {"type": "tool", "name": "emit_nurture_drafts"},
        "messages": [{"role": "user", "content": brief}],
    }).encode("utf-8")
    req = urllib.request.Request(ANTHROPIC_URL, data=body, method="POST", headers={
        "x-api-key": api_key, "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310
        msg = json.loads(r.read().decode("utf-8"))
    block = next((b for b in msg.get("content", [])
                  if b.get("type") == "tool_use"
                  and b.get("name") == "emit_nurture_drafts"), None)
    if not block:
        raise RuntimeError("no tool_use block in Anthropic response")
    payload = block["input"]
    if isinstance(payload, str):
        payload = json.loads(payload)
    steps = payload.get("steps")
    if not isinstance(steps, list) or not steps:
        raise RuntimeError("emit_nurture_drafts returned no steps")
    return steps


# --------------------------------------------------------------------------- #
# Deterministic MOCK drafter (facts-only, opt-out-complete)
# --------------------------------------------------------------------------- #
def _first(lead: dict) -> str:
    name = str(lead.get("first_name") or "").strip()
    return name or "there"


def _listing_phrase(listing: dict | None) -> str:
    """A short, facts-only phrase for a referenced listing, or "" if none/thin."""
    if not listing:
        return ""
    bits = []
    addr = str(listing.get("address") or "").strip()
    city = str(listing.get("city") or "").strip()
    if addr:
        bits.append(addr + (f", {city}" if city else ""))
    elif city:
        bits.append(city)
    specs = []
    if str(listing.get("beds") or "").strip():
        specs.append(f"{listing['beds']} bed")
    if str(listing.get("baths") or "").strip():
        specs.append(f"{listing['baths']} bath")
    if str(listing.get("sqft") or "").strip():
        specs.append(f"{listing['sqft']} sq ft")
    if specs:
        bits.append(", ".join(specs))
    if str(listing.get("price") or "").strip():
        bits.append(f"offered at {listing['price']}")
    return " — ".join(bits)


# Fair-housing / steering terms that must never reach a draft body, even in the
# deterministic mock path. The LLM path is guarded by _nurture_system_prompt.md;
# this scrubber protects the fallback that echoes the lead's OWN free text, so a
# lead who typed "safe family-friendly area with good schools" can't have that
# language relayed into an outbound draft. (QA finding, defense-in-depth.)
_STEERING_TERMS = (
    "family-friendly", "family friendly", "families", "family",
    "safe", "unsafe", "safety",
    "good school", "good schools", "bad school", "bad schools",
    "great school", "great schools", "school district", "school districts", "schools", "school",
    "great neighborhood", "good neighborhood", "bad neighborhood", "nice neighborhood",
    "up-and-coming", "up and coming", "crime", "crime-free", "low crime",
)
_STEERING_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(t) for t in _STEERING_TERMS) + r")\b", re.IGNORECASE)


def _scrub_interest(interest: str) -> str:
    """Strip any fair-housing/steering language from lead-supplied free text
    before it is interpolated into a mock draft. Removes the banned terms and
    tidies leftover punctuation/whitespace rather than dropping the whole field,
    so legitimate remainder (price band, town, buyer/seller) survives."""
    cleaned = _STEERING_RE.sub("", interest)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip(" ,;.-")


def mock_draft_step(lead: dict, step: dict) -> dict:
    """Build one clearly-templated draft from the lead's OWN fields + the step
    intent. No invented market facts. Always opt-out-complete. (Demo mode.)"""
    first = _first(lead)
    interest = _scrub_interest(str(lead.get("interest") or "").strip())
    intent = step.get("intent", "")
    channel = step["channel"]
    listing_phrase = _listing_phrase(lead.get("listing"))
    interest_clause = f' about {interest}' if interest else ""

    if channel == "sms":
        line = f"Hi {first}, it's Carrie Billeaud with eXp Realty."
        # Keep it short + purpose-shaped by the step intent, no urgency.
        if "saved home search" in intent or "criteria" in intent:
            line += " Happy to set up a saved home search matching what you're looking for whenever you're ready — no rush."
        elif "value comparison" in intent or "home-value" in intent:
            line += " Whenever it's useful, I can put together a no-obligation look at your home's value — just say the word."
        elif "check-in" in intent:
            line += " Just checking in — no pressure at all. Reply anytime if I can help."
        else:
            line += " Reaching out to say I'm here whenever it's helpful."
        if listing_phrase:
            line += f" (Re: {listing_phrase}.)"
        body = f"{line}\n{SMS_OPT_OUT}\n\n[Demo mode — sample draft; Carrie approves before anything sends.]"
        return {
            "day_offset": step["day_offset"], "channel": "sms", "intent": intent,
            "body": body, "status": "draft",
        }

    # email
    if "welcome" in intent:
        subject = "Welcome — here whenever you're ready"
        para = (
            f"Hi {first},\n\n"
            f"Thanks so much for reaching out{interest_clause}. I wanted to say a warm hello and "
            f"let you know there's no pressure and no rush on my end — I'm happy to help at whatever "
            f"pace works for you. When you'd like, just reply and we'll take the next small step together."
        )
    elif "resource" in intent:
        subject = "A resource you might find useful"
        para = (
            f"Hi {first},\n\n"
            f"No ask here — just passing along a resource from my site that folks often find helpful. "
            f"Take a look whenever it's convenient, and reply anytime if a question comes up.\n\n"
            f"Useful resource: __FILL__ (link to the relevant on-site guide)"
        )
    elif "check-in" in intent:
        subject = "Just checking in"
        para = (
            f"Hi {first},\n\n"
            f"A quick, low-key check-in — is now still a good time, or would later be easier? "
            f"Totally fine to say \"not yet,\" and I'll happily check back down the road."
        )
    elif "value comparison" in intent or "home-value" in intent:
        subject = "Whenever it's useful — a look at your home's value"
        para = (
            f"Hi {first},\n\n"
            f"Whenever you'd find it helpful, I'm glad to put together a no-obligation comparison of "
            f"your home's value — something I prepare by hand from current local sales. No commitment, "
            f"and no rush at all. Just reply and I'll get started."
        )
    else:
        subject = "A quick hello from Carrie"
        para = (
            f"Hi {first},\n\n"
            f"Reaching out to let you know I'm here whenever it's helpful{interest_clause}. "
            f"No pressure — reply anytime."
        )

    if listing_phrase:
        para += f"\n\nRe: {listing_phrase}."

    body = (
        f"{para}\n\n"
        f"Warmly,\n{NAP}\n337-258-5379\n\n"
        f"{EMAIL_OPT_OUT}\n\n"
        f"[Demo mode — sample draft; Carrie approves before anything sends.]"
    )
    return {
        "day_offset": step["day_offset"], "channel": "email", "intent": intent,
        "subject": subject, "body": body, "status": "draft",
    }


def mock_sequence(lead: dict, seq: dict) -> list[dict]:
    return [mock_draft_step(lead, s) for s in seq.get("steps", [])]


# --------------------------------------------------------------------------- #
# Drafting entry point (real OR mock, with fallback) + normalization
# --------------------------------------------------------------------------- #
def _normalize_steps(raw_steps: list[dict], seq: dict) -> list[dict]:
    """Force every emitted step to status:"draft", backfill day_offset/intent
    from the sequence definition by position, and GUARANTEE the opt-out line is
    present (belt-and-suspenders even if the model omitted it)."""
    defs = seq.get("steps", [])
    out = []
    for i, s in enumerate(raw_steps):
        d = defs[i] if i < len(defs) else {}
        channel = s.get("channel") or d.get("channel") or "email"
        step = {
            "day_offset": s.get("day_offset", d.get("day_offset", 0)),
            "channel": channel,
            "intent": s.get("intent") or d.get("intent", ""),
            "status": "draft",
        }
        body = str(s.get("body") or "").rstrip()
        if channel == "sms":
            if SMS_OPT_OUT.lower() not in body.lower():
                body = f"{body}\n{SMS_OPT_OUT}"
        else:
            step["subject"] = s.get("subject") or "A note from Carrie"
            if "unsubscribe" not in body.lower():
                body = f"{body}\n\n{EMAIL_OPT_OUT}"
        step["body"] = body
        out.append(step)
    return out


def draft_sequence(lead: dict, seq_key: str, seq: dict) -> tuple[list[dict], bool]:
    """Return (steps, used_mock)."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    force_mock = os.environ.get("NURTURE_MOCK") in ("1", "true")
    if force_mock or key is None:
        return mock_sequence(lead, seq), True
    try:
        raw = call_anthropic(key, build_brief(lead, seq_key, seq))
        return _normalize_steps(raw, seq), False
    except Exception as e:
        print(f"    ! draft API failed ({e}); falling back to mock", file=sys.stderr)
        return mock_sequence(lead, seq), True


# --------------------------------------------------------------------------- #
# Queue assembly + write
# --------------------------------------------------------------------------- #
def process_lead(lead: dict, sequences: dict) -> dict | None:
    seq_key = lead.get("sequence")
    seq = sequences.get(seq_key)
    if not seq:
        print(f"  ! unknown sequence '{seq_key}' for {lead.get('first_name')}; skipping",
              file=sys.stderr)
        return None

    # CONSENT GATE (mirrors the Function): no stated consent -> no drafting.
    # The demo sample leads set consent:true; real leads source it from the CRM.
    if not lead.get("consent"):
        print(f"  ! no stated consent for {lead.get('first_name')}; refusing to draft",
              file=sys.stderr)
        return None

    print(f"  [{lead.get('first_name')}] drafting '{seq_key}' "
          f"({len(seq.get('steps', []))} steps)...")
    steps, mock = draft_sequence(lead, str(seq_key), seq)

    return {
        "first_name": lead.get("first_name", ""),
        "interest": lead.get("interest", ""),
        "source": lead.get("source", ""),
        "sequence": seq_key,
        "sequence_label": seq.get("label", seq_key),
        "consent": True,
        "listing": lead.get("listing") or None,
        "steps": steps,
        "mock": mock,
    }


def write_queue(entries: list[dict]) -> None:
    payload = {
        "generated": "2026-07-13",
        "note": ("Lead-nurture review queue. Every message is a DRAFT — Carrie "
                 "approves each one before anything sends. Nothing auto-sends."),
        "count": len(entries),
        "leads": entries,
    }
    text = json.dumps(payload, indent=2)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    STUDIO_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "queue.sample.json").write_text(text, encoding="utf-8")
    (STUDIO_QUEUE_DIR / "queue.sample.json").write_text(text, encoding="utf-8")


def load_leads(path: str | None) -> list[dict]:
    if not path:
        return sample_leads()
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw.get("leads", [])
    if not isinstance(raw, list):
        raise SystemExit(f"--leads file must be a JSON array (or {{leads:[...]}}): {path}")
    return raw


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Captured lead -> DRAFTED nurture sequence (review queue). Nothing sends.")
    ap.add_argument("--leads", default=None,
                    help="path to a JSON array of leads {first_name, interest, source, "
                         "sequence, consent, optional listing}. Omit for built-in samples.")
    args = ap.parse_args()

    sequences = load_sequences()
    leads = load_leads(args.leads)
    print(f"Drafting nurture sequences for {len(leads)} lead(s)...\n")

    entries = []
    for lead in leads:
        entry = process_lead(lead, sequences)
        if entry:
            entries.append(entry)

    write_queue(entries)

    print("\n" + "=" * 60)
    n_mock = sum(1 for e in entries if e["mock"])
    print(f"DONE. {len(entries)} lead sequence(s) drafted "
          f"({n_mock} mock, {len(entries) - n_mock} live).")
    print(f"  build-side queue : {OUT_DIR / 'queue.sample.json'}")
    print(f"  studio queue     : {STUDIO_QUEUE_DIR / 'queue.sample.json'}")
    for e in entries:
        tag = " (mock)" if e["mock"] else ""
        print(f"  - {e['first_name']}: {e['sequence']} — {len(e['steps'])} drafts{tag}")
    print("Review/approve at /studio/nurture.html. Nothing sends until approved.")
    print("=" * 60)


if __name__ == "__main__":
    main()
