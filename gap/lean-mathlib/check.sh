#!/bin/sh
# These files need Mathlib. Set MATHLIB to a built mathlib4 checkout.
set -u
: "${MATHLIB:?set MATHLIB to a built mathlib4 checkout, e.g. MATHLIB=/tmp/mathlib4}"
LP="$MATHLIB/.lake/build/lib/lean"
for p in "$MATHLIB"/.lake/packages/*/.lake/build/lib/lean; do LP="$LP:$p"; done
export LEAN_PATH="$LP"
command -v lean >/dev/null 2>&1 || { echo "no lean on PATH"; exit 2; }
fail=0
for f in *.lean; do
    [ -e "$f" ] || continue
    lean "$f" >/dev/null 2>&1; rc=$?
    printf '%-20s EXIT=%s\n' "$f" "$rc"
    [ "$rc" -eq 0 ] || fail=1
done
echo
echo "axiom census:"
for f in *.lean; do [ -e "$f" ] && lean "$f" 2>/dev/null | sed "s|^|  |"; done
exit $fail
