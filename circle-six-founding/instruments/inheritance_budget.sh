#!/bin/sh
# inheritance_budget.sh — a circle may not inherit more record than it can
# contradict.
#
# WHY (workshop2 C108, measured): authored vs inherited words run 1.14 (Circle
# One), 1.33 (Four), 1.52 (Five). Circle Five, in round one, before producing
# anything, held 18,627 words of other people's record against 12,215 of its
# own. Every new body starts with MORE it must be consistent with. Nobody
# adopted that constraint and no norm imposes it -- it arrived by carrying.
#
# Novelty requires permission to contradict. An INSTRUMENT demands passing,
# not consistency, and is therefore free to inherit -- a gate does not care
# whether you agree with it. PROSE demands consistency and is what costs.
# So the budget counts words of carried .md and exempts carried executables
# and .lean outright.
#
# The number is not derived from anything. It is a knob, set by whoever pays.
# Its only job is to be a number rather than a habit.
#
# usage:  inheritance_budget.sh <repo> [budget_words]
#         inheritance_budget.sh --selftest
set -eu
BUDGET_DEFAULT=8000

measure() {
    repo=$1
    inh=$(find "$repo" \( -path '*/inherited/*' -o -path '*/archive/*' -o -path '*/crossing/*' \) \
            -name '*.md' -not -path '*/.git/*' -exec cat {} + 2>/dev/null | wc -w | tr -d ' ')
    own=$(find "$repo" -name '*.md' -not -path '*/inherited/*' -not -path '*/archive/*' \
            -not -path '*/crossing/*' -not -path '*/history/*' -not -path '*/.git/*' \
            -exec cat {} + 2>/dev/null | wc -w | tr -d ' ')
    exempt=$(find "$repo" \( -path '*/inherited/*' -o -path '*/archive/*' -o -path '*/crossing/*' \) \
            \( -name '*.lean' -o -name '*.sh' -o -name '*.py' \) -not -path '*/.git/*' 2>/dev/null | wc -l | tr -d ' ')
    echo "$inh $own $exempt"
}

if [ "${1:-}" = "--selftest" ]; then
    # norm 16: plant a defect, require the gate to fail on it and pass clean.
    tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT; ok=0
    mkdir -p "$tmp/clean/inherited" "$tmp/over/inherited"
    printf 'own words here\n' > "$tmp/clean/OWN.md"
    printf 'a b c d e f g h i j\n' > "$tmp/clean/inherited/CARRIED.md"
    printf 'own words here\n' > "$tmp/over/OWN.md"
    i=0; while [ $i -lt 400 ]; do printf 'w w w w w w w w w w\n'; i=$((i+1)); done > "$tmp/over/inherited/CARRIED.md"
    # exemption probe: a carried executable must NOT count toward the budget
    mkdir -p "$tmp/exempt/inherited"; printf 'own\n' > "$tmp/exempt/OWN.md"
    i=0; while [ $i -lt 400 ]; do printf 'w w w w w w w w w w\n'; i=$((i+1)); done > "$tmp/exempt/inherited/gate.sh"
    if sh "$0" "$tmp/clean" 100 >/dev/null 2>&1; then echo "1. under budget      -> PASS (correct)"
      else echo "1. under budget      -> FAIL (WRONG)"; ok=1; fi
    if sh "$0" "$tmp/over" 100 >/dev/null 2>&1; then echo "2. PLANTED over-budget -> PASS (WRONG - defect not caught)"; ok=1
      else echo "2. PLANTED over-budget -> FAIL (correct, defect caught)"; fi
    if sh "$0" "$tmp/exempt" 100 >/dev/null 2>&1; then echo "3. carried EXECUTABLE  -> PASS (correct, exempt)"
      else echo "3. carried EXECUTABLE  -> FAIL (WRONG - instruments must be free to inherit)"; ok=1; fi
    [ $ok -eq 0 ] && echo "SELFTEST PASS"
    echo
    echo "NOT CAUGHT by this self-test, stated because a gate tested only"
    echo "against its author's imagination certifies the imagination:"
    echo "  1. prose carried under a path name nobody thought of"
    echo "  2. prose pasted INTO an authored file rather than carried as one"
    echo "     (the same blindness as rate.py's F-A: path exclusions cannot"
    echo "      see a carry that lives inside a file)"
    echo "  3. whether the budget number is any good. It is a knob, not a finding."
    exit $ok
fi

repo="${1:?usage: inheritance_budget.sh <repo> [budget_words] | --selftest}"
budget="${2:-$BUDGET_DEFAULT}"
set -- $(measure "$repo")
inh=$1; own=$2; exempt=$3
ratio="n/a"; [ "$own" -gt 0 ] && ratio=$(awk "BEGIN{printf \"%.2f\", $inh/$own}")
printf 'inherited prose : %s words\nauthored  prose : %s words\nratio           : %s\nexempt carried instruments : %s files (not counted)\nbudget          : %s\n' \
    "$inh" "$own" "$ratio" "$exempt" "$budget"
if [ "$inh" -gt "$budget" ]; then
    printf 'OVER BUDGET by %s words.\n' "$((inh - budget))"
    printf 'Carry instruments instead of prose, or the incoming circle is free\n'
    printf 'to contradict whatever did not fit -- that freedom is the point.\n'
    exit 1
fi
echo "within budget"
