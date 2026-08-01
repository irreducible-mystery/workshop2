#!/bin/sh
# Compile every file standalone and report exit codes. Zero imports: each file
# carries its own definitions, because with no import a file cannot see another.
set -u
command -v lean >/dev/null 2>&1 || { echo "no lean on PATH"; exit 2; }
fail=0
for f in *.lean; do
    [ -e "$f" ] || continue
    lean "$f" >/dev/null 2>&1
    rc=$?
    printf '%-24s EXIT=%s\n' "$f" "$rc"
    [ "$rc" -eq 0 ] || fail=1
done
echo
echo "axiom census over every theorem:"
for f in *.lean; do
    [ -e "$f" ] || continue
    lean "$f" 2>/dev/null | sed "s|^|  $f: |"
done
exit $fail
