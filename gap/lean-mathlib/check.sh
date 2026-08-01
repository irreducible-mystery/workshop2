#!/bin/sh
# check.sh - compile every file standalone AND census EVERY declaration.
#
# The census is INJECTED, not read from the file. An earlier version reported
# only the `#print axioms` lines the author happened to write, which covered
# 45 of 66 declarations while the README claimed "every declaration". That
# claim was false and a cold reader caught it. This version extracts every
# theorem/lemma name and probes it, and ABORTS if it cannot.
set -u
: "${MATHLIB:?set MATHLIB to a built mathlib4 checkout}"
LP="$MATHLIB/.lake/build/lib/lean"
for p in "$MATHLIB"/.lake/packages/*/.lake/build/lib/lean; do LP="$LP:$p"; done
export LEAN_PATH="$LP"
command -v lean >/dev/null 2>&1 || { echo "no lean on PATH"; exit 2; }
fail=0

extract() {
    awk '
      /^[[:space:]]*namespace[[:space:]]+/ { ns[++d]=$2; next }
      /^[[:space:]]*end[[:space:]]+/       { if (d>0 && $2==ns[d]) d--; next }
      {
        line=$0
        sub(/^[[:space:]]*/,"",line)
        sub(/^@\[[^]]*\][[:space:]]*/,"",line)
        sub(/^(private|protected|noncomputable)[[:space:]]+/,"",line)
        if (line ~ /^(theorem|lemma)[[:space:]]+[A-Za-z_]/) {
          n=line; sub(/^[a-z]+[[:space:]]+/,"",n); sub(/[^A-Za-z_0-9.'"'"'].*/,"",n)
          if (n=="") next
          p=""; for (i=1;i<=d;i++) p = p ns[i] "."
          print p n
        }
      }' "$1"
}

echo "=== compile ==="
for f in *.lean; do
    [ -e "$f" ] || continue
    lean "$f" >/dev/null 2>&1
    rc=$?
    printf '  %-24s EXIT=%s\n' "$f" "$rc"
    [ "$rc" -eq 0 ] || fail=1
done

echo
echo "=== axiom census, injected over EVERY declaration ==="
tot=0; aud=0
for f in *.lean; do
    [ -e "$f" ] || continue
    names=$(extract "$f" | sort -u)
    [ -z "$names" ] && continue
    n=$(printf '%s\n' "$names" | wc -l | tr -d ' ')
    probe=$(mktemp /tmp/gapcensus.XXXXXX.lean)
    { sed 's/^#print axioms.*//' "$f"; echo
      for nm in $names; do printf '#print axioms %s\n' "$nm"; done ; } > "$probe"
    out=$(lean "$probe" 2>&1); rm -f "$probe"
    if printf '%s' "$out" | grep -q 'error:'; then
        echo "  ABORT: census probe for $f did not compile - NO CENSUS TAKEN"
        printf '%s\n' "$out" | grep 'error:' | head -3 | sed 's/^/    /'
        fail=1; continue
    fi
    a=$(printf '%s' "$out" | grep -c "depends on axioms\|does not depend on any axioms")
    if [ "$n" -ne "$a" ]; then
        echo "  ABORT: $f has $n declarations but $a were audited"
        fail=1; continue
    fi
    tot=$((tot+n)); aud=$((aud+a))
    bad=$(printf '%s' "$out" | grep -c "sorryAx\|ofReduceBool\|ofReduceNat")
    printf '  %-24s %3s declarations, %3s audited, sorryAx/native: %s\n' "$f" "$n" "$a" "$bad"
    [ "$bad" -eq 0 ] || fail=1
done
echo
echo "  TOTAL: $tot declarations, $aud audited"
[ "$tot" -eq "$aud" ] || { echo "  MISMATCH"; fail=1; }
exit $fail
