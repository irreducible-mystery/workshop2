# zero

A Lean 4 formalization with no imports, no Mathlib and no lake project. Every
file compiles standalone with `lean <file>` and exits 0.

## What is here

    lean/Core.lean   the definitions, fixed
    TASK.md          the task
    tools/           check.sh, controls.sh, axioms.sh

## The object

A symbol `Fs` over the Gaussian integers with one free parameter `f`, and an
identity — the pentagon — relating a three-factor product to a two-factor one
across sixteen label assignments.

`conj` is an automorphism of the Gaussian integers. **`TASK.md` proves that
rather than assuming it**, along with associativity of `mul`, `one` as a
two-sided identity, and `one ≠ neg one` — all four are leaned on everywhere and
none was established.

The identity has five factor positions. Applying `conj` to any subset of them
gives **thirty-two cases**, one per subset, and the task characterizes all
thirty-two. The case with `conj` applied nowhere is one of the thirty-two: it is
not a baseline, results are not stated relative to it, and it is distinguished
only by having been written down first.

## What is held fixed

Listed because a fixed assumption stays invisible until something else moves.
The task varies none of these. `TASK.md` gives the same list with reasons.

- **the value ring** — `GZ` hardcodes `Int` in its own fields. Nothing about the
  toolchain forces that: a hand-declared ring class, with the pentagon generic
  over it, compiles here with zero imports and instantiates at `Int`, `Fin 2`,
  `Fin 8` and a ring with nilpotents. **The definition is what confines this to
  one ring, not the import list.**
- **the shape of the symbol** — one free parameter across eight admissible index
  patterns, and the restriction sits in the type signature
- **the modulus** — `% 2` is written into the symbol itself, so the label group
  is not a parameter either
- **the label set** — `{0, 1}`
- **the encoding of finiteness** — quantification over `Int` with hypotheses,
  rather than over a finite type
- **the identity under test** — the pentagon only

Zero imports costs automation rather than expressive range: no `ring`, no
`linarith`, so an hour of hand normalisation where a library takes a line. The
one thing it removes outright is `Rat`, which is not a core identifier.

## Evidence

`lean <file>` exiting 0 is the only evidence recognized here. `native_decide` is
not: it trusts the compiler rather than the kernel.

`tools/axioms.sh` reports the axiom census over every declaration. Every tool
takes `--selftest`, which plants a defect, confirms the tool catches it,
confirms it passes clean input, and then prints what the tool cannot catch.

**A zero-axiom census certifies the proof. It says nothing about whether the
proposition is the one you wanted.**

## Verification

A claim that pushed work compiles must be checked against the pushed bytes —
`git show <ref>:<path>` into a fresh directory — not against the working tree.
Guard every step: a failed `cd` or a failed clone must abort rather than let the
next command run somewhere else. A check that silently ran in the wrong place
reports success and means nothing.

Do not pipe the checker. `lean file | head` reports the exit status of `head`,
so a rejected file reads as `EXIT=0`.
