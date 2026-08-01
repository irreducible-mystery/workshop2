Set up a new Lean 4 repository named `zero`. The repository is empty.
Initialize it with `git init` and do not clone anything into it.

## The definitions

These are given. Do not redesign them, and do not reconstruct the index
assignments — they are exactly as written. Put them in `lean/Core.lean` verbatim.

```lean
structure GZ where
  re : Int
  im : Int

def zero : GZ := ⟨0, 0⟩
def one  : GZ := ⟨1, 0⟩
def I    : GZ := ⟨0, 1⟩

def add (z w : GZ) : GZ := ⟨z.re + w.re, z.im + w.im⟩
def neg (z : GZ) : GZ := ⟨-z.re, -z.im⟩
def mul (z w : GZ) : GZ :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def conj (z : GZ) : GZ := ⟨z.re, -z.im⟩

def Fs (f : GZ) (a b c d x y : Int) : GZ :=
  if x = (a + b) % 2 ∧ y = (b + c) % 2 ∧ d = (a + b + c) % 2 then
    (if a = 1 ∧ b = 1 ∧ c = 1 then f else one)
  else zero

def pentLhs (f : GZ) (a b c d : Int) : GZ :=
  let x := (a + b) % 2; let y := (x + c) % 2; let t := (y + d) % 2
  let w := (c + d) % 2; let v := (b + w) % 2; let u := (b + c) % 2
  mul (mul (Fs f a b c y x u) (Fs f a u d t y v)) (Fs f b c d v u w)

def pentRhs (f : GZ) (a b c d : Int) : GZ :=
  let x := (a + b) % 2; let y := (x + c) % 2; let t := (y + d) % 2
  let w := (c + d) % 2; let v := (b + w) % 2
  mul (Fs f x c d t y w) (Fs f a b w t x v)

def pentagonHolds (f : GZ) : Prop :=
  ∀ a b c d : Int, (a = 0 ∨ a = 1) → (b = 0 ∨ b = 1) → (c = 0 ∨ c = 1) →
    (d = 0 ∨ d = 1) → pentLhs f a b c d = pentRhs f a b c d
```

Note two things about `Fs`, because they are what make the question non-trivial:

- `f` is a **free `GZ` parameter**, not a unit. It ranges over all Gaussian
  integers. `pentagonHolds` is a predicate on `f`, not a fixed claim.
- `Fs` returns `zero` off its indicator, so factors vanish for some label
  assignments and the identity is a mixture of vanishing and non-vanishing
  cases.

## The question

`pentLhs` has three `Fs` factors and `pentRhs` has two. Label them:

    L1 = Fs f a b c y x u
    L2 = Fs f a u d t y v
    L3 = Fs f b c d v u w
    R1 = Fs f x c d t y w
    R2 = Fs f a b w t x v

`conj` is the non-trivial ring automorphism of the Gaussian integers. The
identity above is stated with it applied nowhere.

For each non-empty subset S of {L1, L2, L3, R1, R2}, define the variant in which
`conj` is applied to exactly the factors in S — thirty-one variants — and
determine, for each one:

> **Does the variant hold for exactly the same set of `f` as the original?**

Three outcomes are equally reportable, and no one of them is the expected
answer:

- **Same.** The variant holds for exactly the `f` the original holds for.
- **Narrower.** Some `f` satisfies the original and not the variant. Give the
  witness.
- **Wider.** Some `f` satisfies the variant and not the original. Give the
  witness.

Report what you find. If all thirty-one come out **Same**, that is the result
and it should be stated plainly.

### On what the kernel can and cannot settle here

For a **fixed** `f`, the identity ranges over sixteen label assignments and is
decidable — `decide` after case-splitting `a b c d`.

Quantification over `f` is **not** decidable: `f` ranges over an infinite set.
So the work has this shape:

1. Characterize the original: prove `pentagonHolds f ↔ P f` for some explicit
   condition `P` on `f.re` and `f.im`.
2. Characterize each variant the same way.
3. Compare the two conditions.

Any claim that two variants differ must come with a **concrete witness** — a
specific `f` — and the witness must be checked by the kernel, not asserted.
`I`, `neg one`, and `⟨0,0⟩` are natural first candidates; there is no reason to
assume the answer lies among them.

## Constraints on the Lean

- Zero imports. No Mathlib, no Std, no lake project. Every file compiles
  standalone with `lean <file>` and exits 0.
- No `sorry`, marked or unmarked.
- No `native_decide`. Decidability goes through the kernel.
- Every statement quantified over a finite domain carries a live-instance count,
  so a vacuously true statement cannot pass as a theorem.
- Every check ships with a negative control that actually returns false.

## Layout

    README.md      what this is, one page
    QUESTION.md    the question above, stated once
    lean/Core.lean the definitions, verbatim
    lean/          one file per variant, or per group of variants
    tools/         the scripts below

## Four working conditions — state them in README.md, then follow them

1. This repository carries no inherited prose. Tools may be copied in freely,
   because a tool has to pass rather than be agreed with. Written conclusions
   are not copied in, because they have to be agreed with, and agreement is the
   thing new work has to be able to withdraw.

2. Nothing here requires anyone's approval before it happens. Any rule adopted
   must name an action with a checkable output, never a person or a permission.

3. Work leaves this repository by being rebuilt somewhere a stricter standard
   applies. Nothing here is relied on elsewhere until that happens, and that is
   exactly what makes trying things here cheap.

4. This arrangement has a term rather than running indefinitely. A rule not
   re-adopted lapses; re-adopting one costs a line.

## Tools

- `check.sh` — run `lean` over every file in `lean/`, report exit codes only.
- `controls.sh` — confirm each negative control returns false; fail if any
  passes.
- `census.sh` — count theorems per file with the pattern `^theorem <name> ... :`
  and print a table. Do not count a theorem twice across versioned files: where
  filenames share a stem with a version suffix, report only the highest and
  print which files it collapsed.

Each tool takes `--selftest`, which plants a defect, confirms the tool catches
it, confirms it passes on clean input, and then prints a short list of what the
tool cannot catch.

## Toolchain

If `lean` is not on PATH, install Lean 4 v4.22.0 from its GitHub release tarball
and put it on PATH. Confirm it works by checking that it accepts `2 + 2 = 4` and
rejects `2 + 2 = 5`. Commit whatever install script you write so the next person
does not repeat it.

## Order of work

Do these in order and stop at the end of step 3 to report before continuing.

1. Get the toolchain working and `lean/Core.lean` compiling as given.
2. Characterize the original — prove `pentagonHolds f ↔ P f` with `P` explicit.
   State `P` in plain terms in `QUESTION.md` once you have it.
3. Do **one** variant, the single-factor case `S = {L1}`, end to end: define it,
   characterize it, compare to `P`, and report Same, Narrower, or Wider with a
   kernel-checked witness if it is not Same.

Then continue through the remaining thirty variants.
