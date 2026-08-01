#!/bin/sh
# exit_gate.sh — keeps the sandbox and the cumulative record separate.
#
# WHY
#   A codebase does not run one review standard everywhere. The release branch
#   is locked and the scratch branch is not, and the reason that works is that
#   nothing on the scratch branch is load-bearing until it has been rebuilt on
#   the branch where things are load-bearing. Averaging the two standards into
#   one middling standard gives you neither: too strict to try things, too loose
#   to depend on.
#
#   This circle is the scratch branch, made a whole repository so the separation
#   is structural instead of a habit. Inside it, a line of attack that turns out
#   not to work costs the attempt and nothing else.
#
#   The gate enforces the one property that makes that true:
#
#     THE CUMULATIVE RECORD MAY NOT CITE THE SANDBOX.
#
#   Work enters the record by being rebuilt where the canon applies and
#   something outside the prose decides. Remove this rule and the freedom goes
#   with it -- a sandbox the record cites is not a sandbox, it is a second
#   record with a lower standard.
#
# usage:  exit_gate.sh <repo> [sandbox-dir]
#         exit_gate.sh --selftest
set -eu
DIR_DEFAULT=sandbox

check() {
    repo=$1; dir=$2
    [ -d "$repo/$dir" ] || { echo "no sandbox at $dir/ -- nothing to enforce"; return 0; }
    hits=$(grep -rIl --exclude-dir=.git -- "$dir/" "$repo" 2>/dev/null \
             | grep -v "^$repo/$dir/" | grep -v 'exit_gate.sh' || true)
    if [ -n "$hits" ]; then
        echo "LEAK -- the cumulative record cites the sandbox:"
        printf '%s\n' "$hits" | sed "s|^$repo/|  |"
        echo "Rewrite it outside $dir/ where the canon applies, or drop it."
        return 1
    fi
    echo "separated -- $dir/ is cited by nothing outside itself"
    return 0
}

if [ "${1:-}" = "--selftest" ]; then
    tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT; ok=0
    mkdir -p "$tmp/clean/sandbox" "$tmp/leak/sandbox"
    printf 'a rough idea\n' > "$tmp/clean/sandbox/try.md"
    printf 'the record, citing nothing\n' > "$tmp/clean/RECORD.md"
    printf 'a rough idea\n' > "$tmp/leak/sandbox/try.md"
    printf 'as shown in sandbox/try.md we conclude\n' > "$tmp/leak/RECORD.md"
    if sh "$0" "$tmp/clean" >/dev/null 2>&1; then echo "1. separated sandbox -> PASS (correct)"
      else echo "1. separated sandbox -> FAIL (WRONG)"; ok=1; fi
    if sh "$0" "$tmp/leak" >/dev/null 2>&1; then echo "2. PLANTED leak      -> PASS (WRONG - not caught)"; ok=1
      else echo "2. PLANTED leak      -> FAIL (correct, leak caught)"; fi
    [ $ok -eq 0 ] && echo "SELFTEST PASS"
    echo
    echo "NOT CAUGHT:"
    echo "  1. an idea carried out by retyping, with no path cited. The gate sees"
    echo "     references, not provenance -- and retyping without a pointer is"
    echo "     this record's oldest convicted species (norm 13)."
    echo "  2. whether anything good ever comes out of the sandbox."
    echo "  3. the term. This circle has one; this gate does not enforce it."
    exit $ok
fi
check "${1:?usage: exit_gate.sh <repo> [dir] | --selftest}" "${2:-$DIR_DEFAULT}"
