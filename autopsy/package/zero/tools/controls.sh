#!/bin/sh
# controls.sh — a negative control must FAIL. If one passes, the check is empty.
#
# Convention: any file matching lean/*_control.lean MUST NOT compile.
set -u
SELF=$(cd "$(dirname "$0")" && pwd)/$(basename "$0")
fail=0
if [ "${1:-}" = "--selftest" ]; then
    if ! command -v lean >/dev/null 2>&1; then
        echo "SELFTEST SKIPPED - no lean on PATH."
        echo "This tool is UNEXERCISED. Run --selftest again once the toolchain"
        echo "is installed, and repair whatever fails, before trusting any"
        echo "output from it. A tool that has never caught its planted defect"
        echo "is a tool with no evidence behind it."
        exit 3
    fi
    t=$(mktemp -d); trap 'rm -rf "$t"' EXIT; ok=0
    mkdir -p "$t/lean"
    printf 'theorem c : 2 + 2 = 5 := by decide\n' > "$t/lean/a_control.lean"
    ( cd "$t" && sh "$SELF" >/dev/null 2>&1 ) || { echo "FAIL: a properly failing control was reported bad"; ok=1; }
    printf 'theorem c : 2 + 2 = 4 := by decide\n' > "$t/lean/a_control.lean"
    ( cd "$t" && sh "$SELF" >/dev/null 2>&1 ) && { echo "FAIL: a control that PASSED was not caught"; ok=1; }
    rm -f "$t/lean/a_control.lean"
    printf 'def d : Nat := 0\n' > "$t/lean/defs.lean"
    ( cd "$t" && sh "$SELF" >/dev/null 2>&1 ) || { echo "FAIL 3: definitions and no theorems reported as a defect"; ok=1; }
    printf 'theorem t : 1 = 1 := rfl\n' >> "$t/lean/defs.lean"
    ( cd "$t" && sh "$SELF" >/dev/null 2>&1 ) && { echo "FAIL 4: a theorem with no control was not caught"; ok=1; }

    [ $ok -eq 0 ] && echo "SELFTEST PASS"
    echo
    echo "NOT CAUGHT:"
    echo "  1. a control that fails for the wrong reason — a typo, not the defect."
    echo "  2. a claim with no control written for it at all."
    echo "  3. whether the controls cover the failures that matter."
    exit $ok
fi
command -v lean >/dev/null 2>&1 || { echo "no lean on PATH"; exit 2; }
n=0
for f in lean/*_control.lean; do
    [ -e "$f" ] || continue
    n=$((n+1))
    if lean "$f" >/dev/null 2>&1; then
        printf '%-40s PASSED - a negative control must fail\n' "$f"; fail=1
    else
        printf '%-40s fails as required\n' "$f"
    fi
done
if [ "$n" -eq 0 ]; then
    # Zero controls is only a defect once there is something to control.
    # On arrival lean/ holds the given definitions and no theorems, so demanding
    # a control here is a FALSE RED - as useless as a false green, and it would
    # greet whoever opens this package with a failure they did not cause.
    thms=$(sed 's|--.*||' lean/*.lean 2>/dev/null | grep -cE '^[[:space:]]*(@\[[^]]*\][[:space:]]*)?(private |protected |noncomputable )*(theorem|lemma)[[:space:]]')
    if [ "$thms" -eq 0 ]; then
        echo "no theorems in lean/ yet - nothing to control. Not a defect."
        exit 0
    fi
    echo "$thms theorem(s) in lean/ and NO negative control - nothing is being controlled"
    exit 1
fi
exit $fail
