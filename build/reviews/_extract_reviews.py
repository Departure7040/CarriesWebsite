#!/usr/bin/env python3
"""One-time helper: extract EVERY review verbatim from site/testimonials.html
into data/reviews.yaml. Kept in-repo for provenance/re-derivation, but the
canonical store is data/reviews.yaml — build_reviews.py reads THAT, not this.

Extracting programmatically (rather than retyping) guarantees the stored text is
byte-for-byte identical to what is visible on the page, incl. curly vs straight
quotes/apostrophes. Nothing is invented; ratings are recorded ONLY where the page
shows a visible star rating (the 3 Google cards).
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SRC = REPO / "site" / "testimonials.html"
OUT = REPO / "data" / "reviews.yaml"

CARD_RE = re.compile(
    r'<div class="card quote-card">\s*'
    r'<p class="quote">"(?P<text>.*?)"</p>\s*'
    r'<p><strong>(?P<author>.*?)</strong>(?P<suffix>[^<]*)</p>\s*'
    r'</div>',
    re.DOTALL,
)


def section(html: str, sec_id: str) -> str:
    start = html.index(f'id="{sec_id}"')
    end = html.index("</section>", start)
    return html[start:end]


def classify(suffix: str) -> tuple[str, object]:
    s = suffix
    if "Google review" in s:
        return "google", 5
    if "Alignable" in s:
        return "alignable", None
    if "NextDoor" in s:
        return "nextdoor", None
    return "website", None


def first_name(author: str) -> str:
    return author.split()[0]


HEADER = """\
# data/reviews.yaml — structured store of Carrie Billeaud's REAL, verified reviews.
#
# SCHEMA (one list under `reviews:`; each item):
#   author      str   — exact display name as shown on the page (e.g. "Amy L.", "Olivia")
#   first_name  str   — explicit first name for graphics/asks (stored, never string-split at
#                       runtime, so names like "Amy L." / "Jeff C. Wiresinger" are never mangled)
#   rating      int|null — 5 ONLY where the page shows a visible ★★★★★ star rating (the 3 Google
#                       cards). null everywhere else — the other cards display NO rating, and
#                       inventing "5 stars" for an unrated testimonial would be fabricating a
#                       quality statistic (banned). No reviewRating is emitted in JSON-LD where null.
#   source      enum  — google | zillow | website | alignable | nextdoor
#   text        str   — the review body, VERBATIM (block scalar; no wrapping quotes — the page/
#                       templates add the display "…" ). Curly vs straight quotes preserved exactly.
#   verified    bool  — always true; every entry is copied from a card already visible on
#                       site/testimonials.html. Nothing here is invented.
#
# PROVENANCE: generated from site/testimonials.html by build/reviews/_extract_reviews.py so the
# text is byte-identical to the page. Re-derive with:  python build/reviews/_extract_reviews.py
# The site builder (build/reviews/build_reviews.py) reads THIS file and regenerates the review
# card grids + individual Review JSON-LD, so this store is the single source of truth.
#
# NOTE on the "5-review API cap": Google's Places API returns at most 5 reviews, so we cannot pull
# all 185. This file surfaces the reviews already verified/visible on-site; review_request.py drives
# NEW ones. See build/reviews/README.md.
#
# Counts: 3 google (rating 5) · 20 website (rating null) · 2 alignable (rating null) · 1 nextdoor (rating null) = 26
"""


def yaml_block(text: str) -> str:
    # literal block scalar, strip-chomped; single logical line indented 6 spaces
    return "    text: |-\n      " + text + "\n"


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    entries = []
    for sec_id in ("google-reviews", "testimonials"):
        block = section(html, sec_id)
        for m in CARD_RE.finditer(block):
            text = m.group("text")
            author = m.group("author")
            source, rating = classify(m.group("suffix"))
            entries.append((author, first_name(author), rating, source, text))

    lines = [HEADER, "\nreviews:\n"]
    for author, fn, rating, source, text in entries:
        lines.append(f'  - author: "{author}"\n')
        lines.append(f'    first_name: "{fn}"\n')
        lines.append(f"    rating: {'null' if rating is None else rating}\n")
        lines.append(f"    source: {source}\n")
        lines.append("    verified: true\n")
        lines.append(yaml_block(text))
        lines.append("\n")
    OUT.write_text("".join(lines), encoding="utf-8")

    from collections import Counter
    by_src = Counter(e[3] for e in entries)
    rated = sum(1 for e in entries if e[2] is not None)
    print(f"Extracted {len(entries)} reviews -> {OUT}")
    print(f"  by source: {dict(by_src)}")
    print(f"  with visible rating: {rated}")


if __name__ == "__main__":
    main()
