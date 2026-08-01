#!/bin/sh
# check.sh — compile every file in lean/ and report exit codes. Nothing else.
#
# EXCEPT lean/*_control.lean. Those are negative controls and are REQUIRED to
# fail; controls.sh owns them. Without this exclusion the two tools contradict
# each other, and no repository containing a control can ever be green.
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
    printf 'theorem probe_ok : 2 + 2 = 4 := by decide\n'  > "$t/lean/good.lean"
    printf 'theorem probe_bad : 2 + 2 = 5 := by decide\n' > "$t/lean/bad.lean"
    ( cd "$t" && sh "$SELF" >/dev/null 2>&1 ) && { echo "FAIL: planted bad file passed"; ok=1; }
    rm "$t/lean/bad.lean"
    ( cd "$t" && sh "$SELF" >/dev/null 2>&1 ) || { echo "FAIL: clean tree rejected"; ok=1; }
    printf 'theorem c : 2 + 2 = 5 := by decide\n' > "$t/lean/x_control.lean"
    ( cd "$t" && sh "$SELF" >/dev/null 2>&1 ) || { echo "FAIL: a negative control sank check.sh"; ok=1; }
    rm "$t/lean/x_control.lean"
    [ $ok -eq 0 ] && echo "SELFTEST PASS"
    echo
    echo "NOT CAUGHT:"
    echo "  1. a hole that lean only WARNS about. An anonymous declaration"
    echo "     proved by sorry exits 0 here. Verified. axioms.sh aborts on it;"
    echo "     this tool cannot see it and a green check.sh does not mean clean."
    echo "  2. a file that compiles and proves the wrong thing."
    echo "  3. a theorem that is vacuously true. Use live-instance counts."
    echo "  4. anything about lean/ files that are never referenced."
    exit $ok
fi
command -v lean >/dev/null 2>&1 || { echo "no lean on PATH"; exit 2; }
for f in lean/*.lean; do
    [ -e "$f" ] || continue
    case "$f" in *_control.lean) continue ;; esac
    lean "$f" >/dev/null 2>&1
    rc=$?
    printf '%-40s EXIT=%s\n' "$f" "$rc"
    [ "$rc" -eq 0 ] || fail=1
done
exit $fail
