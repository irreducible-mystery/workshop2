#!/bin/sh
# axioms.sh — census of soundness escape hatches over EVERY declaration.
#
# Two passes, because they catch different things:
#   1. #print axioms on every named declaration, FILE BY FILE.
#   2. a source scan for hatches that are not axioms.
#
# WHY FILE BY FILE, AND NOT ONE CONCATENATED PROBE
#   With zero imports there is no import. A file in lean/ cannot see another
#   file's definitions, so every file that proves anything must CARRY the
#   definitions itself. Concatenating them therefore declares GZ several times
#   and nothing compiles. An earlier version concatenated, and it also swept in
#   the negative controls - which are REQUIRED to fail - so the census aborted
#   the moment the task was followed as written. Verified: it did.
#
# THE THING THIS TOOL GOT WRONG ONCE, AND WHY IT NOW ABORTS
#   An earlier version extracted `theorem foo` inside `namespace Foo` as `foo`
#   rather than `Foo.foo`. `#print axioms foo` then failed with "unknown
#   constant", the error was ignored, and the census printed sorryAx 0 for a
#   file containing a planted sorry. A CLEAN REPORT ON A FILE THAT CHEATS.
#
#   Better name extraction is not the fix, because the next unhandled form
#   breaks it again. The fix is that ANY error in the probe output is fatal:
#   the tool refuses to report a census it could not actually take.
#
# THE SECOND THING, AND IT IS WORSE
#   An anonymous declaration - `example : ... := by sorry` - produces NO name,
#   so #print axioms never runs on it, and `lean` exits 0 with only a warning.
#   BOTH check.sh AND this tool reported green on a file containing a hole.
#   Verified. So anonymous declarations now ABORT: what cannot be named cannot
#   be audited.
#
# ON ONE PATTERN THAT IS DELIBERATELY NOT SCANNED FOR
#   Lean has a modifier marking a definition compiler-only. It needs no pattern
#   here, because the KERNEL refuses any declaration depending on such a
#   definition - the file does not compile and check.sh is the check. Verified
#   directly: the kernel emits "invalid declaration, it uses ..." and exits 1.
#   A grep would be strictly weaker than the check already running.
set -u
SELF=$(cd "$(dirname "$0")" && pwd)/$(basename "$0")

extract() {   # qualified names, tracking namespace nesting
    awk '
      /^[[:space:]]*namespace[[:space:]]+/ { ns[++d]=$2; next }
      /^[[:space:]]*end[[:space:]]+/       { if (d>0 && $2==ns[d]) d--; next }
      {
        line=$0
        sub(/^[[:space:]]*/,"",line)
        sub(/^@\[[^]]*\][[:space:]]*/,"",line)
        sub(/^(private|protected|noncomputable)[[:space:]]+/,"",line)
        sub(/^(private|protected|noncomputable)[[:space:]]+/,"",line)
        if (line ~ /^(theorem|lemma|def|abbrev|instance|structure|inductive)[[:space:]]+[A-Za-z_]/) {
          n=line; sub(/^[a-z]+[[:space:]]+/,"",n); sub(/[^A-Za-z_0-9.'"'"'].*/,"",n)
          if (n=="") next
          p=""
          for (i=1;i<=d;i++) p = p ns[i] "."
          print p n
        }
      }' "$@"
}

if [ "${1:-}" = "--selftest" ]; then
    if ! command -v lean >/dev/null 2>&1; then
        echo "SELFTEST SKIPPED - no lean on PATH. This tool is UNEXERCISED."
        exit 3
    fi
    t=$(mktemp -d); trap 'rm -rf "$t"' EXIT; ok=0; mkdir -p "$t/lean"
    p1() { ( cd "$t" && sh "$SELF" 2>&1 ); }

    printf 'theorem clean_one : 2 + 2 = 4 := by decide\n' > "$t/lean/a.lean"
    p1 | grep -q 'sorryAx  *0' || { echo "FAIL 1: clean file not reported clean"; ok=1; }

    printf 'theorem dirty : 2 + 2 = 5 := by sorry\n' > "$t/lean/a.lean"
    p1 | grep -q 'sorryAx  *0' && { echo "FAIL 2: planted sorry reported as clean"; ok=1; }

    printf 'namespace Foo\ntheorem ns_sorry : 2 + 2 = 5 := by sorry\nend Foo\n' > "$t/lean/a.lean"
    p1 | grep -q 'sorryAx  *0' && { echo "FAIL 3: sorry inside a namespace reported as clean"; ok=1; }

    printf '@[simp] theorem attr_sorry : 2 + 2 = 5 := by sorry\n' > "$t/lean/a.lean"
    p1 | grep -q 'sorryAx  *0' && { echo "FAIL 4: sorry on an attributed decl reported as clean"; ok=1; }

    printf 'private theorem priv_sorry : 2 + 2 = 5 := by sorry\n' > "$t/lean/a.lean"
    p1 | grep -q 'sorryAx  *0' && { echo "FAIL 5: sorry on a private decl reported as clean"; ok=1; }

    # a required negative control must NOT abort the census
    printf 'theorem clean_one : 2 + 2 = 4 := by decide\n' > "$t/lean/a.lean"
    printf 'theorem must_fail : 2 + 2 = 5 := by decide\n' > "$t/lean/a_control.lean"
    p1 | grep -q 'ABORT' && { echo "FAIL 6: a negative control aborted the census"; ok=1; }
    rm -f "$t/lean/a_control.lean"

    # self-contained files repeat their definitions; that must not collide
    printf 'def shd : Nat := 1\ntheorem t1 : shd = 1 := rfl\n' > "$t/lean/a.lean"
    printf 'def shd : Nat := 1\ntheorem t2 : shd = 1 := rfl\n' > "$t/lean/b.lean"
    p1 | grep -q 'ABORT' && { echo "FAIL 7: two self-contained files aborted the census"; ok=1; }
    p1 | grep -q 'audited: *4' || { echo "FAIL 8: not every declaration across files was audited"; ok=1; }
    rm -f "$t/lean/b.lean"

    # the hole that made BOTH tools report green
    printf 'theorem named_ok : 1 = 1 := rfl\nexample : 2 + 2 = 5 := by sorry\n' > "$t/lean/a.lean"
    p1 | grep -q 'ABORT' || { echo "FAIL 9: anonymous declaration did not abort"; ok=1; }

    [ $ok -eq 0 ] && echo "SELFTEST PASS"
    echo
    echo "NOT CAUGHT:"
    echo "  1. a sound proof of a statement that says the wrong thing."
    echo "     A zero-axiom census certifies the proof, never the proposition."
    echo "  2. a Decidable instance is proof-carrying and cannot lie, but the"
    echo "     PREDICATE it decides may not be the one you meant."
    echo "  3. a declaration form this extractor does not recognise. Any probe"
    echo "     error is fatal, and the one known form producing NO name and NO"
    echo "     error - the anonymous declaration - now aborts. A form that does"
    echo "     both AND is not the anonymous one would still be invisible."
    echo "  4. anything inside lean/*_control.lean. Those are REQUIRED to fail,"
    echo "     so they are excluded here and controls.sh is what checks them."
    exit $ok
fi

command -v lean >/dev/null 2>&1 || { echo "no lean on PATH"; exit 2; }

allout=$(mktemp /tmp/axout.XXXXXX)
trap 'rm -f "$allout"' EXIT
found=0; audited=0; files=0

for f in lean/*.lean; do
    [ -e "$f" ] || continue
    case "$f" in *_control.lean) continue ;; esac
    files=$((files+1))

    anon=$(sed 's|--.*||' "$f" | grep -cE '^[[:space:]]*example[[:space:]]*[:({]')
    if [ "$anon" -ne 0 ]; then
        echo "ABORT: $anon anonymous declaration(s) in $f."
        echo "  An anonymous declaration has no name, so no census can be taken"
        echo "  of it, and lean exits 0 on one containing a hole. Give it a name."
        exit 1
    fi

    names=$(extract "$f" | sort -u)
    [ -z "$names" ] && continue
    n=$(printf '%s\n' "$names" | wc -l | tr -d ' ')

    probe=$(mktemp /tmp/axprobe.XXXXXX.lean)
    { cat "$f"; echo
      for nm in $names; do printf '#print axioms %s\n' "$nm"; done ; } > "$probe"
    out=$(lean "$probe" 2>&1)
    rm -f "$probe"

    if printf '%s' "$out" | grep -q 'error:'; then
        echo "ABORT: the probe for $f did not compile, so no census was taken."
        printf '%s\n' "$out" | grep 'error:' | head -5 | sed 's/^/  /'
        echo "  A census that could not run is not a clean census."
        echo "  If this file references definitions from another file: there is"
        echo "  no import here. Every file must carry its own definitions."
        exit 1
    fi

    a=$(printf '%s' "$out" | grep -c "depends on axioms\|does not depend on any axioms")
    if [ "$n" -ne "$a" ]; then
        echo "ABORT: in $f, found $n declaration(s) and audited $a."
        exit 1
    fi
    printf '%s\n' "$out" >> "$allout"
    found=$((found+n)); audited=$((audited+a))
done

[ "$files" -eq 0 ] && { echo "ABORT: no files to audit in lean/"; exit 1; }
[ "$found" -eq 0 ] && { echo "ABORT: no declarations found in $files file(s)"; exit 1; }

echo "files audited: $files   declarations found: $found   audited: $audited"
for ax in propext Classical.choice Quot.sound sorryAx Lean.ofReduceBool Lean.ofReduceNat; do
    printf '  %-22s %s\n' "$ax" "$(grep -c "$ax" "$allout")"
done
echo
echo "source scan, non-axiom hatches (controls included, they are source too):"
strip=$(sed 's|--.*||' lean/*.lean 2>/dev/null)
for pat in '\baxiom\b' '\bsorry\b' 'native_decide' '\bpartial\b' '\bopaque\b' '\bexample\b' \
           '@\[extern' '@\[implemented_by' '@\[csimp' '\bClassical\.' '\bnoncomputable\b' 'macro_rules' 'set_option'; do
    printf '  %-22s %s\n' "$pat" "$(printf '%s' "$strip" | grep -cE "$pat")"
done
