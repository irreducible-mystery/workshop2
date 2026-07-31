#!/bin/sh
# norm_shape.sh — flags rules that grant standing rather than name an action.
#
# The measured cut (workshop2 C71/C83): a rule naming an action with a
# checkable output survives its author and runs for anyone holding the tree.
# A rule naming a person, seat or office dies with them and then blocks.
# Twenty of twenty-one norms in the circle canon are the first kind.
#
# Mechanical proxy: does the rule's OPERATIVE CLAUSE name a role?
#
# *** The operative clause only. This gate's first version scanned whole
# *** norm entries and flagged four of five as permission-shaped, because
# *** their provenance sentences say "Proposed by the builder" -- attribution,
# *** not permission. Its self-test passed anyway: the planted defect was the
# *** one its author imagined. SR43's species, in the instrument written to
# *** fix that species. The false positives are now in the self-test as the
# *** third and fourth probes, which is the only reason the gate is trusted
# *** at all -- it failed on real data first.
#
# This is a FLAGGER, not a lock. It cannot tell a good permission clause
# from a bad one and does not try. It says where to look.
#
# usage:  norm_shape.sh <norms-file>
#         norm_shape.sh --selftest
set -eu

ROLES="seat of record|seats of record|the courier|a body|that body|the principal|say-so|written word of|rules ADMIT|waits on a branch|on the word of"

# operative clause = text between the norm heading and the closing '**'
scan() {
    awk '
      /^\*\*Norm [0-9]+/ { collecting=1; buf=""; }
      collecting {
        buf = buf " " $0
        if (index(buf, "**") > 0) {
          n = buf; sub(/^ *\*\*Norm /, "", n); sub(/ .*/, "", n); sub(/[^0-9]/, "", n)
          op = buf
          sub(/^ *\*\*Norm [0-9]+ [^ ]* */, "", op)     # drop heading
          i = index(op, "**")                            # operative clause ends at closing **
          if (i > 0) op = substr(op, 1, i-1)
          print n "\t" op
          collecting = 0
        }
      }
    ' "$1" | while IFS="$(printf '\t')" read -r num op; do
        [ -z "$num" ] && continue
        hits=$(printf '%s' "$op" | grep -oEi "$ROLES" | sort -u | tr '\n' ',' | sed 's/,$//')
        if [ -n "$hits" ]; then
            printf 'PERMISSION-SHAPED  norm %-3s  names: %s\n' "$num" "$hits"
        else
            printf 'instrument         norm %-3s\n' "$num"
        fi
    done
}

if [ "${1:-}" = "--selftest" ]; then
    tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT; ok=0
    cat > "$tmp/a.md" <<'P'
**Norm 99 — a check that cannot fail is not a check.** Every gate ships with
a planted defect it is required to catch, and the run is recorded.
P
    cat > "$tmp/b.md" <<'P'
**Norm 98 — nothing enters the default branch but on the written word of a
seat of record.** Anything from outside waits on a branch until a body
audits it and rules ADMIT in a letter.
P
    # probes 3 and 4 exist because the first version got these WRONG on real data
    cat > "$tmp/c.md" <<'P'
**Norm 97 — a repair and the first thing that depends on it never ride in the
same crate.** Proposed by the builder in the repairs verification and adopted
here on the courier's word. A body of record co-signed.
P
    cat > "$tmp/d.md" <<'P'
**Norm 96 — a count the views render is never retyped; the record points, the
view counts.** Ruled by the courier, reasoned about by the prover's seat.
P
    r() { scan "$1"; }
    echo "1. action rule                          -> $(r "$tmp/a.md")"
    echo "2. planted permission clause            -> $(r "$tmp/b.md")"
    echo "3. action rule, PROVENANCE names roles  -> $(r "$tmp/c.md")"
    echo "4. action rule, PROVENANCE names roles  -> $(r "$tmp/d.md")"
    r "$tmp/a.md" | grep -q '^instrument'        || { echo "FAIL 1"; ok=1; }
    r "$tmp/b.md" | grep -q '^PERMISSION-SHAPED' || { echo "FAIL 2: plant not caught"; ok=1; }
    r "$tmp/c.md" | grep -q '^instrument'        || { echo "FAIL 3: provenance false positive"; ok=1; }
    r "$tmp/d.md" | grep -q '^instrument'        || { echo "FAIL 4: provenance false positive"; ok=1; }
    [ $ok -eq 0 ] && echo "SELFTEST PASS — fires on the plant, silent on all three clean rules"
    exit $ok
fi
scan "${1:?usage: norm_shape.sh <norms-file> | --selftest}"
