#!/usr/bin/env python3
"""Exhaustive coverage check between two views of the same conversation.

Not a sample. Every substantive line of view A is checked for presence in
view B, after normalizing away the differences the views are *expected* to
have (markdown emphasis, headers, bullets, smart quotes, dashes, whitespace).

Written for the P1 adjudication, generalized so any participant can re-run it
on any pair of views. The point of the deflationary program is to ship the
checker, not the claim.

    python3 coverage.py dialogue/raw/kellys-view.txt dialogue/raw/transcript.md

Exit status is 0 always; read the report. Lines shorter than --min normalized
characters are skipped as too short to be distinctive.
"""
import argparse
import re
import sys
import unicodedata


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("—", "-").replace("–", "-")
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = re.sub(r"[*_`#>]", "", s)
    s = re.sub(r"^\s*[-+]\s+", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("view_a", help="view whose lines are checked")
    ap.add_argument("view_b", help="view searched for those lines")
    ap.add_argument("--min", type=int, default=60,
                    help="minimum normalized line length to check (default 60)")
    ap.add_argument("--window", type=int, default=120,
                    help="substring window used to tolerate line-wrap differences")
    args = ap.parse_args()

    a_lines = open(args.view_a, encoding="utf-8").read().splitlines()
    b_blob = norm(open(args.view_b, encoding="utf-8").read())

    missing, checked = [], 0
    for i, raw in enumerate(a_lines, 1):
        n = norm(raw)
        if len(n) < args.min:
            continue
        checked += 1
        if n in b_blob:
            continue
        # A line may be split differently in B; accept if any window survives.
        w = args.window
        if any(n[a:a + w] in b_blob for a in range(0, max(1, len(n) - w), w // 3)):
            continue
        missing.append((i, len(n), raw.strip()))

    print(f"A: {args.view_a}\nB: {args.view_b}")
    print(f"Lines in A with >= {args.min} normalized chars: {checked}")
    print(f"Not found in B: {len(missing)}\n")
    for ln, length, txt in missing:
        print(f"--- {args.view_a}:{ln}  ({length} chars)")
        print(txt[:400] + ("..." if len(txt) > 400 else ""))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
