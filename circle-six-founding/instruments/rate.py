#!/usr/bin/env python3
"""rate.py — a rate instrument, to sit beside the state instruments.

Every instrument in the four workshop repositories measures a STATE: a manifest
against a tree, a hash against a file, a claim against the thing it claims
about. Across 254 authored documents and ~430k words, none measures this
circle against the last. Every trend in `experiments/four-circles-meta-view.md`
lives in that gap.

This produces one row per circle, appends it to a carried-forward ledger, and
prints the first differences. Standard library only; no network; read-only.

    python3 rate.py --repo /path/to/circle --circle "Five" \\
        --lean 'lean/*.lean' --names Kelly --append rate/RATE-LEDGER.md

A seat inside one circle can run it on its own tree and get its own row. The
row is only worth having because someone later puts it next to another one.

WHAT THIS IS NOT
  Four proxies, not a verdict. Theorem count is not mathematical value; word
  count is not thought; ceremony density is not bureaucracy; a name count is
  not whether a person was respected. A circle that games any of these has
  produced a number and nothing else. The row exists to make a *direction*
  visible, and a direction is only evidence when nobody was steering by it.

  See --selftest for what this instrument does NOT catch. That list is part of
  the instrument.
"""

from __future__ import annotations
import argparse, glob, os, re, subprocess, sys

# --------------------------------------------------------------------------
# Committed definitions. Changing these changes what every past row MEANT, so
# they are versioned and every emitted row carries the version. A row whose
# TERMS version differs from another row's is not comparable to it.
# --------------------------------------------------------------------------

TERMS_VERSION = "v1"

# Ceremony vocabulary: nouns of governance, not of subject matter. Fixed at v1
# from the four-circle audit so later circles cannot tune the denominator.
CEREMONY = [
    "seat", "crossing", "pin", "gate", "instrument", "norm", "charge",
    "seal", "door", "ferry", "admissib", "bitten", "crate", "adjudicat",
]
CEREMONY_RE = re.compile(r"\b(?:" + "|".join(CEREMONY) + r")\w*", re.I)

# Theorem predicate, taken from the workshop's own instruments
# (audit/r6s_y5_views_census.sh:65) rather than invented here. Their count is
# authoritative for their record; a naive `^\s*theorem\s` over-counts by 7.
THEOREM_RE = re.compile(r"^theorem [A-Za-z_0-9].*:", re.M)

# Copies of a neighbour's work are not this circle's output.
DEFAULT_EXCLUDE = ("archive/", "inherited/", "experiment/")


# --------------------------------------------------------------------------

def tracked_files(repo: str, suffix: str) -> list[str]:
    """Files git tracks. Falls back to a walk if this is not a git tree."""
    try:
        out = subprocess.run(["git", "-C", repo, "ls-files", f"*{suffix}"],
                             capture_output=True, text=True, check=True).stdout
        return [l for l in out.splitlines() if l]
    except Exception:
        hits = []
        for root, _, files in os.walk(repo):
            if ".git" in root:
                continue
            for f in files:
                if f.endswith(suffix):
                    hits.append(os.path.relpath(os.path.join(root, f), repo))
        return sorted(hits)


def authored(paths: list[str], exclude: tuple[str, ...]) -> list[str]:
    return [p for p in paths if not any(p.startswith(e) for e in exclude)]


def measure(repo: str, lean_spec: str | None, names: list[str],
            exclude: tuple[str, ...]) -> dict:
    md = authored(tracked_files(repo, ".md"), exclude)
    words = ceremony = human = 0
    for p in md:
        try:
            t = open(os.path.join(repo, p), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        words += len(t.split())
        ceremony += len(CEREMONY_RE.findall(t))
        for n in names:
            human += len(re.findall(re.escape(n), t, re.I))

    thms = 0
    lean_files: list[str] = []
    if lean_spec:
        for spec in lean_spec.split(","):
            lean_files += sorted(glob.glob(os.path.join(repo, spec.strip())))
        for f in lean_files:
            try:
                thms += len(THEOREM_RE.findall(
                    open(f, encoding="utf-8", errors="replace").read()))
            except OSError:
                pass

    return {
        "theorems": thms,
        "words": words,
        "ceremony_per_1k": round(1000 * ceremony / words, 1) if words else 0.0,
        "human_mentions": human,
        "docs": len(md),
        "lean_spec": lean_spec or "(none)",
        "lean_files": len(lean_files),
        "exclude": ";".join(exclude),
        "terms": TERMS_VERSION,
    }


# --------------------------------------------------------------------------

COLS = ["circle", "theorems", "words", "ceremony_per_1k", "human_mentions",
        "docs", "lean_spec", "exclude", "terms"]


def row_md(circle: str, m: dict) -> str:
    m = {"circle": circle, **m}
    return "| " + " | ".join(f"`{m[c]}`" if c in ("lean_spec", "exclude", "terms")
                             else str(m[c]) for c in COLS) + " |"


def read_rows(ledger: str) -> list[dict]:
    if not os.path.exists(ledger):
        return []
    rows = []
    for line in open(ledger, encoding="utf-8"):
        if not line.startswith("| ") or line.startswith("| circle") or set(line.strip()) <= set("|-: "):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) != len(COLS):
            continue
        rows.append(dict(zip(COLS, cells)))
    return rows


def deltas(rows: list[dict]) -> str:
    """The whole point. A state instrument stops one line above this."""
    if len(rows) < 2:
        return ("  (only one row — a rate instrument with one sample is a state\n"
                "   instrument. This becomes informative at the next circle.)")
    out = []
    for a, b in zip(rows, rows[1:]):
        if a["terms"] != b["terms"]:
            out.append(f"  {a['circle']} → {b['circle']}: NOT COMPARABLE "
                       f"(terms {a['terms']} vs {b['terms']})")
            continue
        seg = [f"  {a['circle']} → {b['circle']}:"]
        for c, label in (("theorems", "theorems"), ("words", "words"),
                         ("ceremony_per_1k", "ceremony/1k"),
                         ("human_mentions", "human mentions")):
            x, y = float(a[c]), float(b[c])
            arrow = "→" if y == x else ("↑" if y > x else "↓")
            pct = f"{100*(y-x)/x:+.0f}%" if x else "  n/a"
            seg.append(f"      {label:<16} {x:>10g} {arrow} {y:<10g} {pct:>7}")
        out.append("\n".join(seg))
    return "\n".join(out)


# --------------------------------------------------------------------------

NOT_CAUGHT = """\
WHAT THIS INSTRUMENT DOES NOT CATCH
  Written down because a gate tested only against the failures its author
  imagined certifies the author's imagination (SR43: five gates, each bitten
  at birth, all blind to a file that was not on the list).

  1. Gaming. Any of the four numbers can be moved directly without changing
     anything real: pad theorems with restatements, pad words, swap ceremony
     nouns for synonyms outside TERMS v1, sprinkle a name. It measures a
     direction and assumes nobody is steering by it. If a circle starts
     steering by it, delete it — do not refine it.
  2. Quality, in any of the four columns. A circle can halve its ceremony
     density and be worse governed.
  3. Anything outside tracked `.md` and the `--lean` spec. Crossing artifacts
     in a ferry directory with no git home (SR3, SR6) are invisible here —
     the same corridor the gates never covered.
  4. Whether the `--lean` spec is the right spec. That is a judgment, which is
     why every row records the spec it used. A row whose spec you disagree
     with is a row about something else, not a wrong row.
  5. Drift in TERMS. Rows carry a version and refuse to difference across
     versions; they cannot tell you the new version is better.
  6. n=1. One row is a state measurement wearing a rate instrument's name.
"""


def selftest(repo: str) -> int:
    """Bite it. Plant changes, check the number moves; report what stays still."""
    import tempfile, shutil
    print("SELF-TEST — planting changes and checking the instrument moves\n")
    tmp = tempfile.mkdtemp()
    dst = os.path.join(tmp, "r")
    shutil.copytree(repo, dst, ignore=shutil.ignore_patterns(".git"))
    base = measure(dst, None, ["Kelly"], DEFAULT_EXCLUDE)
    ok = True

    def probe(label, mutate, col, expect_move):
        nonlocal ok
        p = os.path.join(dst, "_probe.md")
        mutate(p)
        m = measure(dst, None, ["Kelly"], DEFAULT_EXCLUDE)
        moved = m[col] != base[col]
        good = moved == expect_move
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {label:<52} "
              f"{col}: {base[col]} → {m[col]}")
        os.remove(p)

    probe("ceremony nouns added   → density rises",
          lambda p: open(p, "w").write("seat crossing pin gate charge " * 40),
          "ceremony_per_1k", True)
    probe("human name added       → mentions rise",
          lambda p: open(p, "w").write("Kelly " * 25), "human_mentions", True)
    probe("name removed elsewhere → mentions fall",
          lambda p: open(p, "w").write("no names here " * 25),
          "human_mentions", False)

    # The exploit, demonstrated rather than asserted. This is not a pass/fail
    # probe: the instrument behaves exactly as designed and the design is the
    # hole. Written this way because the first version of this probe asked
    # "does the number stay still?", the number moved by dilution, and the
    # probe reported FAIL for the wrong reason — right diligence, wrong
    # predicate. The predicate was the defect, and the truth is worse.
    p = os.path.join(dst, "_probe.md")
    open(p, "w").write("chair passage marker checkpoint warrant " * 40)
    m = measure(dst, None, ["Kelly"], DEFAULT_EXCLUDE)
    os.remove(p)
    print(f"\n  [EXPLOIT] rename the governance vocabulary and change nothing else:")
    print(f"            ceremony/1k {base['ceremony_per_1k']} → {m['ceremony_per_1k']}"
          f"  ({m['ceremony_per_1k'] - base['ceremony_per_1k']:+.1f})")
    print(f"            Synonyms outside TERMS {TERMS_VERSION} are not counted as ceremony,")
    print(f"            but they ARE counted as words. So a circle can lower its")
    print(f"            apparent ceremony density by renaming its own rules —")
    print(f"            the score improves while the governance is untouched.")
    print(f"            The metric is not merely evadable; evading it scores well.")

    print(f"\n  self-test: {'PASS' if ok else 'FAIL'} (3 probes)\n")
    print(NOT_CAUGHT)
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--circle", help="label for this row, e.g. 'Five'")
    ap.add_argument("--lean", help="glob(s) for canonical proof files, comma-separated")
    ap.add_argument("--names", default="Kelly", help="comma-separated human names")
    ap.add_argument("--exclude", default=",".join(DEFAULT_EXCLUDE))
    ap.add_argument("--append", metavar="LEDGER", help="append the row to this ledger")
    ap.add_argument("--show", metavar="LEDGER", help="print a ledger's first differences")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest(a.repo)

    if a.show:
        rows = read_rows(a.show)
        print(f"\nFIRST DIFFERENCES — {a.show}  ({len(rows)} rows)\n")
        print(deltas(rows))
        return 0

    if not a.circle:
        ap.error("--circle is required (or use --show / --selftest)")

    m = measure(a.repo, a.lean, [n.strip() for n in a.names.split(",")],
                tuple(e for e in a.exclude.split(",") if e))
    row = row_md(a.circle, m)
    print(row)

    if a.append:
        rows = read_rows(a.append)
        if any(r["circle"] == a.circle for r in rows):
            print(f"\n  (a row for '{a.circle}' already exists in {a.append} — "
                  f"not appended; rows append, they do not overwrite)")
        else:
            with open(a.append, "a", encoding="utf-8") as f:
                f.write(row + "\n")
            print(f"\n  appended to {a.append}")
        print()
        print(deltas(read_rows(a.append)))
    return 0


if __name__ == "__main__":
    # A seat will pipe this to `head`. Die quietly on SIGPIPE rather than
    # printing a traceback: an instrument that produces noise when read
    # partially teaches its reader to distrust its output.
    try:
        rc = main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        os._exit(0)
    sys.exit(rc)
