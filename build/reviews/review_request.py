#!/usr/bin/env python3
"""Post-close review-ASK generator for Carrie Billeaud.

Produces a warm, compliant review request in two forms — an SMS-length message and an email
(subject + body) — personalized by {first_name, address}. Every version carries Carrie's REAL
Google write-a-review link.

    from build.reviews.review_request import build_request
    msg = build_request(first_name="Jordan", address="123 Rue Example, Youngsville, LA")
    print(msg["sms"])          # -> str, SMS-length
    print(msg["email_subject"])
    print(msg["email_body"])

This is a mock/no-API generator: it returns template strings for Carrie to review and send
HERSELF. Nothing here auto-sends.

COMPLIANCE (baked in, non-negotiable):
  * GENUINE ASK ONLY — it never offers anything of value (gift card, discount, entry, credit) in
    exchange for a review. Incentivized reviews violate RESPA and Google/Zillow platform ToS.
  * NO PRESSURE — one soft, optional ask; it explicitly tells the client "no worries at all" if
    they'd rather not, and to reply STOP to opt out (honor consent).
  * NO STEERING / FAIR-HOUSING language, no guarantees, no predictions, no rates, no "#1 agent",
    no market stats. It talks only about her service and provides the Google link.
  * HUMAN-IN-LOOP — Carrie personally reviews and sends each message; her name is the signature.
"""

# Carrie's REAL Google write-a-review deep link (place id ChIJdUhCUO2dJIYRe6NLEeyEd_M).
GOOGLE_PLACE_ID = "ChIJdUhCUO2dJIYRe6NLEeyEd_M"
GOOGLE_REVIEW_URL = f"https://search.google.com/local/writereview?placeid={GOOGLE_PLACE_ID}"

SIGNATURE = "Carrie Billeaud, REALTOR® · eXp Realty · 337-258-5379"


def build_request(first_name: str, address: str) -> dict:
    """Return {sms, email_subject, email_body} for a post-close review ask.

    Args:
        first_name: the client's first name (e.g. "Jordan"). Kept verbatim.
        address:    the property that just closed (e.g. "123 Rue Example, Youngsville, LA").
                    Used only as a warm, personal reference — never published anywhere.

    No incentive is offered, no outcome is claimed, and the client can opt out.
    """
    name = first_name.strip()
    addr = address.strip()

    sms = (
        f"Hi {name}, it was truly a joy helping you at {addr}! If you have a minute, "
        f"a quick Google review would mean the world and helps other Acadiana buyers and sellers "
        f"find me: {GOOGLE_REVIEW_URL} — no worries at all if now's not a good time. "
        f"Thank you! – Carrie. (Reply STOP to opt out.)"
    )

    email_subject = f"Thank you, {name} — a quick favor?"

    email_body = (
        f"Hi {name},\n\n"
        f"It was such a pleasure working with you on {addr}. Getting you to the closing "
        f"table was the best part of my week, and I'm so grateful you trusted me with it.\n\n"
        f"If you have a couple of minutes, I'd be honored if you'd share a few words about "
        f"your experience in a Google review. Even a sentence or two genuinely helps other "
        f"Acadiana buyers and sellers find someone to guide them — and it means a great deal to me.\n\n"
        f"Here's the link to leave one:\n{GOOGLE_REVIEW_URL}\n\n"
        f"And of course, absolutely no pressure — if now isn't a good time, that's completely "
        f"okay. Either way, I'm always just a call or text away if you ever need anything.\n\n"
        f"With gratitude,\n{SIGNATURE}\n\n"
        f"(Prefer not to receive follow-ups like this? Just let me know and I won't send another.)"
    )

    return {
        "sms": sms,
        "email_subject": email_subject,
        "email_body": email_body,
        "review_url": GOOGLE_REVIEW_URL,
    }


def _demo() -> None:
    # SAMPLE / __FILL__ placeholders — this is illustrative only; Carrie supplies real values
    # and sends the message herself.
    msg = build_request(first_name="SAMPLE (e.g. Jordan)", address="__FILL__ property address")
    print("=== SMS ===")
    print(msg["sms"])
    print("\n=== EMAIL SUBJECT ===")
    print(msg["email_subject"])
    print("\n=== EMAIL BODY ===")
    print(msg["email_body"])
    print("\n(Google review link:", msg["review_url"], ")")


if __name__ == "__main__":
    _demo()
