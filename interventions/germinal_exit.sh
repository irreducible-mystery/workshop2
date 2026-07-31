#!/bin/sh
# germinal_exit.sh — a compartment where error is free, and a hard exit.
#
# WHY (workshop2 C109): no organism runs a moderate mutation rate everywhere.
# Histone and ribosomal genes are near-immutable; immunoglobulin variable
# regions hypermutate at ~10^6x background inside a bounded compartment, under
# ruthless selection at the exit, with a time limit. Maximum novelty and
# maximum selection in one body, SEPARATED BY COMPARTMENT rather than averaged
# into a middle. The averaged design does not appear in nature and it is the
# design this record has.
#
# The compartment is a directory. Inside it: the canon does not apply, output
# is disposable by default, and being wrong is free. The gate enforces exactly
# one thing -- the property that makes "disposable" true rather than aspirational:
#
#   THE CUMULATIVE RECORD MAY NOT CITE THE COMPARTMENT.
#
# Nothing leaves except by being rewritten outside it, where the canon applies
# and something outside the prose decides. A germinal centre with a leaky exit
# is not a compartment; it is a second record with a lower standard.
#
# usage:  germinal_exit.sh <repo> [compartment-dir]
#         germinal_exit.sh --selftest
set -eu
DIR_DEFAULT=germinal

check() {
    repo=$1; dir=$2
    [ -d "$repo/$dir" ] || { echo "no compartment at $dir/ -- nothing to enforce"; return 0; }
    hits=$(grep -rIl --exclude-dir=.git -- "$dir/" "$repo" 2>/dev/null \
             | grep -v "^$repo/$dir/" | grep -v 'germinal_exit.sh' || true)
    if [ -n "$hits" ]; then
        echo "LEAK -- the cumulative record cites the compartment:"
        printf '%s\n' "$hits" | sed "s|^$repo/|  |"
        echo "Rewrite it outside $dir/ where the canon applies, or drop it."
        return 1
    fi
    echo "sealed -- $dir/ is cited by nothing outside itself"
    return 0
}

if [ "${1:-}" = "--selftest" ]; then
    tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT; ok=0
    mkdir -p "$tmp/clean/germinal" "$tmp/leak/germinal"
    printf 'a rough idea\n' > "$tmp/clean/germinal/try.md"
    printf 'the record, citing nothing\n' > "$tmp/clean/RECORD.md"
    printf 'a rough idea\n' > "$tmp/leak/germinal/try.md"
    printf 'as shown in germinal/try.md we conclude\n' > "$tmp/leak/RECORD.md"
    if sh "$0" "$tmp/clean" >/dev/null 2>&1; then echo "1. sealed compartment -> PASS (correct)"
      else echo "1. sealed compartment -> FAIL (WRONG)"; ok=1; fi
    if sh "$0" "$tmp/leak" >/dev/null 2>&1; then echo "2. PLANTED leak       -> PASS (WRONG - not caught)"; ok=1
      else echo "2. PLANTED leak       -> FAIL (correct, leak caught)"; fi
    [ $ok -eq 0 ] && echo "SELFTEST PASS"
    echo
    echo "NOT CAUGHT:"
    echo "  1. an idea CARRIED OUT by retyping, with no path cited. The gate"
    echo "     sees references, not provenance -- and retyping without a pointer"
    echo "     is this record's oldest convicted species (norm 13)."
    echo "  2. whether anything good ever comes out of the compartment."
    echo "  3. the time limit. A germinal centre has one; this gate does not."
    exit $ok
fi
check "${1:?usage: germinal_exit.sh <repo> [dir] | --selftest}" "${2:-$DIR_DEFAULT}"
