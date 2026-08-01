Complete the task below in this repository.

It already contains the definitions, three tools, and this file. Nothing else.
Do not add a lake project, a lakefile, or any dependency.

This is a **verification** task, not a discovery task. Several statements below
were computed in Python and are stated as targets. Python is not proof. Your job
is to settle them with the Lean kernel.

**If the kernel disagrees with any stated target, the kernel is right. Report the
disagreement as the result and do not adjust the statement to make it pass.**

## The definitions

Already in `lean/Core.lean`, reproduced here so this file is self-contained. Do
not redesign them and do not reconstruct the index assignments.

**`lean/Core.lean` is the authority. If this block and that file ever disagree,
the file wins and the disagreement is a defect to report.** `deriving
DecidableEq` on `GZ` is present so `decide` works on `GZ` equalities; if it
causes trouble, replace it with a hand-written instance rather than dropping it.

**It compiles.** Verified against Lean 4.22.0 core, zero imports, `EXIT=0`.
Confirm that yourself as step one rather than taking it on trust.

```lean
structure GZ where
  re : Int
  im : Int
  deriving DecidableEq

def zero : GZ := ⟨0, 0⟩
def one  : GZ := ⟨1, 0⟩
def I    : GZ := ⟨0, 1⟩

def add (z w : GZ) : GZ := ⟨z.re + w.re, z.im + w.im⟩
def neg (z : GZ) : GZ := ⟨-z.re, -z.im⟩
def mul (z w : GZ) : GZ :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def conj (z : GZ) : GZ := ⟨z.re, -z.im⟩

/-- The symbol. One free parameter `f`, carried on a single index pattern;
    `one` on the other admissible patterns; `zero` off the indicator. -/
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

`pentLhs` has three `Fs` factors and `pentRhs` has two. Label them:

    L1 = Fs f a b c y x u
    L2 = Fs f a u d t y v
    L3 = Fs f b c d v u w
    R1 = Fs f x c d t y w
    R2 = Fs f a b w t x v

## Part 0 — what the object actually is

Everything below this point, and everything said about the object anywhere in
this file, rests on properties of `GZ` that **the package asserts and does not
prove.** Establish them first. They are ordinary and they are all reachable.

- `mul` is associative and commutative. **`pentLhs` writes `mul (mul A B) C` and
  nothing in the package licenses that grouping.** The statement is well-defined
  either way because it fixes its own parentheses — but no reasoning may
  reassociate it until this exists.
- `one` is a two-sided identity for `mul`.
- `conj` satisfies `conj (mul z w) = mul (conj z) (conj w)`, and `conj (conj z) = z`.
  **This file describes `conj` as a ring automorphism. That is a claim about the
  object and it is unproved until you prove it.**
- `one ≠ neg one`. Without it, a two-element solution set might be one element.
- `Fs` really can return `zero`: exhibit arguments where the indicator fails. **If the
  `else zero` branch were unreachable it would be dead code in the definition
  under study**, and dead code is where an error hides unseen.

**A note on how, because it is not obvious and cost an hour to find.** `ring`
does not exist here — it is Mathlib. `omega` is linear and will not close
`conj (mul z w) = mul (conj z) (conj w)`. What does work is a local
normalisation set: `Int.add_mul`, `Int.mul_add`, `Int.sub_mul`, `Int.mul_sub`,
`Int.mul_assoc`, `Int.mul_comm`, `Int.mul_left_comm`, `Int.add_assoc`,
`Int.add_comm`, `Int.add_left_comm`, `Int.neg_mul`, `Int.mul_neg`,
`Int.sub_eq_add_neg`, `Int.neg_add`, `Int.neg_neg` — declared `attribute [local
simp]`, after which `cases` then `simp [mul]` closes all of them.

**That set is the whole automation budget for this part. Do not raise it without
saying why.**

## Part A — the indicator

**Target.** For every one of the sixteen assignments with `a b c d ∈ {0,1}`, all
five factors satisfy the `if` condition in `Fs`. No factor is ever `zero`.

Prove it as a theorem per factor, or one theorem covering all five, quantified
over the sixteen assignments with a live-instance count.

## Part B — the exponent table

For each of the sixteen assignments, each factor evaluates to `f` or to `one`.
Produce the table: assignment, which of L1 L2 L3 R1 R2 give `f`, and the
resulting powers on each side.

Emit it as kernel-checked theorems, not as `#eval` output. Something that fails
to compile if the table is wrong.

## Part C — the characterization

**Target.** `pentagonHolds f ↔ mul f f = one`.

**Target.** `mul f f = one ↔ (f = one ∨ f = neg one)`, over `GZ`.

Both directions of both. The second is a statement about `Int`, so it needs a
real argument, not `decide` — `f.re` and `f.im` are unbounded.

## Part D — the thirty-two cases

For **every** subset `S ⊆ {L1, L2, L3, R1, R2}` — all thirty-two, the empty one
included — let `pentagonHoldsσ S f` be the same statement with `conj` applied to
the **value** of each factor in `S`, that is `conj (Fs f …)` in place of
`Fs f …` for exactly those factors. `S = ∅` is the identity substitution and
recovers Part C's statement.

**Characterize all thirty-two the same way Part C characterizes one of them:** an
explicit condition on `f.re` and `f.im`, proved. Present them as a table of
thirty-two rows.

**Do not treat the empty subset as a baseline.** Asking whether a variant is
*Same, Wider or Narrower than the original* privileges the original as the
origin, and nothing justifies that — it is one of thirty-two, distinguished only
by having been written down first. Report the thirty-two conditions and, if some
coincide, say which and why.

**Every partition of the table is equally reportable.** If all thirty-two rows
carry the same condition, that is the result and should be stated flatly. If they
split, that is the result. Report what the kernel settles and do not editorialize
about it anywhere in this repository.

**Structural fact, verified, and it reframes the whole part.** Because `Fs`
returns `f` or `one` or `zero`, and `conj` fixes the latter two:

    conj (Fs f a b c d x y)  =  Fs (conj f) a b c d x y

**So a "twist" is not a new operation on the equation. It is substituting
`conj f` for `f` in selected factor positions.** Prove this first; it makes
every case a substitution rather than a wrapper, and it is the honest way to
see what the thirty-two are.

**Method note — parameterize, do not enumerate.** Thirty-two separate
developments is the wrong shape and will not fit. Introduce a flag per factor
and define the variant once:

    def tw (b : Bool) (z : GZ) : GZ := if b then conj z else z

Then `pentLhsV`, `pentRhsV` and `pentagonHoldsV` take five `Bool`s, and **all
thirty-two cases — the original included — are one theorem** whose proof
case-splits on the flags. That formulation has been checked to typecheck and to
reduce correctly; see the feasibility note below for how far it was taken.

**Method note — use Part B and do not grind thirty-two times.** Part B tells you,
for each assignment, which factors evaluate to `f` and which to `one`. Since
`conj one = one`, an assignment where **no** factor carries `f` reads `one = one`
under every `S`, and constrains nothing. Only the assignments that carry `f` can
constrain anything, and there are few of them.

So: derive the condition contributed by each `f`-carrying assignment once, as a
function of which of its factors are in `S`. A case's solution set is then the
intersection of those conditions.

**Method note.** The statement is a conjunction over all sixteen assignments, so
a condition read off one assignment is necessary, not sufficient. More than one
assignment can constrain `f`, and the solution set is the intersection.

**Method note.** For a **fixed** `f` the sixteen assignments are decidable. The
quantification over `f` is not — `f` ranges over an infinite set — so each
characterization needs a proof, and every witness must be checked by the kernel
rather than asserted.

## Zero imports: what it costs and what it does not

Stated because it is not a neutral stylistic preference and because the limits
are easy to guess wrong.

**What it buys.** Anyone with a `lean` binary can check the result with no
dependency, no version pin and no build system. The artifact is self-contained,
and the axiom census reports a real base rather than one that arrived with a
library.

**What it does not buy.** It is not a soundness argument. A library cannot
introduce unsoundness that `#print axioms` would not reveal — the census is the
protection, not the absence of imports. *(Stated as the standard understanding;
someone who has the library should confirm it rather than take it on trust.)*

**What it costs, measured.** Core Lean 4 offers `Nat.gcd` and `Fin` and little
else of use here. There is no `ring`, no `linarith`, no `nlinarith`, no
`positivity`, and few `Int` order lemmas. Proving `mul` associative is an hour
of hand-built normalisation. **The cost is automation.**

**What it does not cost: expressive range.** This was checked rather than
assumed. With zero imports you can declare a commutative-ring class by hand,
define an eight-parameter symbol and the pentagon generically over it, state
invertibility as `∃ u, mul p u = one` — no division needed — and instantiate the
whole thing at `GZ`, `Int`, `Fin 2`, `Fin 8`, and a ring with nilpotents. It
compiles, `EXIT=0`. Two of its theorems are the point: `x * x = 1` has **one**
root in `Fin 2` and **four** in `Fin 8`, so a value ring where the solution set
changes shape rather than size is two lines away.

**The one thing it removes outright.** `Rat` is **not a core identifier** —
`#check Rat` fails. The rationals, and any question posed at a value like
`-1/4`, need either an import or a hand-rolled ring. That is work, not a wall.

> **So the value ring, not the import list, is what confines this task.** `GZ`
> hardcodes `Int` in its own fields. A later task that varies the ring should
> change the definition first, and drop zero imports only if it actually needs
> `Rat` or the automation.

## The automation you have, named

`nlinarith`, `linarith`, `positivity`, `ring`, `norm_num`, `sq_nonneg`,
`Int.mul_self_nonneg` and most of the `Int` order lemmas **do not exist here.**
`omega`, `decide`, `simp`, `rcases` and `congrArg` do. `Int.mul_eq_zero`,
`Int.eq_one_of_mul_eq_one_right`, `Int.mul_nonneg`, `Int.neg_mul_neg` and
`Int.lt_or_le` are in core and are enough for the arithmetic here.

`omega` is linear only — it will not settle `a * a = 1 → a = 1 ∨ a = -1` on its
own. Facts of that shape need a short hand proof, and the core lemmas above are
sufficient to build one.

`decide` refuses a goal containing free variables. Reduce first, or case-split.

**Reaching for an absent tactic does not fail the way a wrong proof does.** Lean
reports `unknown tactic` and **the theorem silently acquires `sorryAx`**. The
file may still exit non-zero for the error, but if it does not, only the axiom
census will show you. This is the concrete reason `tools/axioms.sh` treats any
probe error as fatal, and the reason to run it rather than trust a green
`check.sh`.

**Feasibility, stated exactly, because the two halves differ.**

**Part C is settled.** Both targets were independently proved in Lean 4.22.0
core, zero imports, before this task was issued. The proof is deliberately not
supplied — the construction is the task, and a proof handed over can only be
agreed with.

**Part D is likely but not established.** The five-flag formulation above was
built and taken to within two remaining goals, both of the same shape already
closed in Part C — a non-negativity fact and a square-root fact, each provable
from the core lemmas listed. It was **not** finished. Treat Part D as probable
rather than proven, and **if it turns out not to close, that is a finding worth
reporting rather than a failure to work around.**

## The encoding, checked against something outside itself

`pentLhs` and `pentRhs` are the standard 3-cocycle pentagon. Reading off the
index triple each factor carries:

    LHS   w(a,b,c) · w(a, b+c, d) · w(b,c,d)
    RHS   w(a+b, c, d) · w(a, b, c+d)                 sums mod 2

Confirmed to match at all sixteen assignments. **This had never been checked**
and is worth re-deriving rather than trusting: a kernel-checked theorem about a
mis-encoded object is a correct proof of the wrong proposition, and no census or
self-test can see that.

Under the one-parameter shape, `Fs` is the cocycle that is `1` everywhere except
one pattern. Whatever the pentagon then forces on `f` can be compared against
the known order of the third cohomology of a two-element group with unit
coefficients. **Do that comparison and report whether they agree.** An
independent check on the statement is worth more than another check on the
proof.

## On the axiom census

Run it and report what it says. **A straightforward core proof of these targets
carries `propext`, and `Classical.choice` and `Quot.sound` arrive with `omega`
and `rcases`.** That is normal and is not a defect.

Driving the count to zero is possible but is separate, deliberate work —
replacing `simp` with explicit `congrArg`, and directed rewrites for
`decide_eq_true_eq`. **Do that only if you want to; do not hide a non-zero count
either way.** The census is a measurement, not a target.

## Constraints on the Lean

**Which of these are load-bearing, stated so the list can be argued with.** Only
some of these keep the proofs honest. The rest are choices, and a choice that
travels as if it were a requirement is how a constraint stops being examined.

| constraint | keeps the proofs honest? |
|---|---|
| no `sorry` | **yes.** A hole is a hole |
| axiom census over every declaration | **yes — this is the mechanism.** Everything else is downstream of it |
| live-instance counts | **yes.** Otherwise a vacuous statement passes as a theorem |
| negative controls that really fail | **yes.** Otherwise a check that always passes reads as a check |
| no `native_decide` | **yes, though redundant** — it trusts the compiler, and the census would show it as `Lean.ofReduceBool` anyway |
| name every declaration | **yes.** An anonymous one cannot be audited, and `lean` exits 0 on one containing a hole |
| do not interpret results here | not about proofs. It protects the *result* from being written in advance |
| **zero imports** | **no.** See below |

**Zero imports is the one constraint here that is not a soundness requirement.**
A library cannot introduce unsoundness that `#print axioms` would not reveal, so
the census is the protection. What zero imports buys is self-containment — one
binary, no version pin, no build — and one thing worth more: **the automation
budget stays legible.** With a large library, `simp` closes goals from an opaque
lemma set and you cannot see what was used; here the fifteen lemmas of Part 0
are the whole budget and they are written down.

That is a real argument and it is not a soundness argument. It is kept for this
task because everything in it is small, finite and decidable over `Int`. **A
later task should decide it again rather than take it as given.**

- Zero imports. No Mathlib, no Std, no lake project. Every file compiles
  standalone with `lean <file>` and exits 0.
- No `sorry`, marked or unmarked.
- **Every declaration has a name.** No anonymous declarations in `lean/`. One
  proved by `sorry` **compiles, exits 0, and is invisible to the census**, so
  `tools/axioms.sh` aborts on any it finds. Verified, not assumed.
- No `native_decide`. Decidability goes through the kernel.
- Every statement quantified over a finite domain carries a live-instance count,
  so a vacuously true statement cannot pass as a theorem. Note that
  `pentagonHolds` quantifies over `Int` **with hypotheses**, not over a finite
  type — so the count is a separate theorem: exactly sixteen assignments satisfy
  the four hypotheses, and each is exhibited.
- Every check ships with a negative control that actually returns false. Name
  those files `lean/*_control.lean`: `controls.sh` requires them to fail, and
  `check.sh` skips them for exactly that reason. **Any other naming makes the
  two tools contradict each other and no tree containing a control can be
  green.**
- Run `#print axioms` over **every** declaration — theorems, definitions,
  abbreviations, instances — and report the totals for `propext`,
  `Classical.choice`, `Quot.sound`, `sorryAx`, `ofReduceBool`, `ofReduceNat`.
  Report whatever they are. Do not treat a non-zero count as a failure.

## The tools

`tools/check.sh`, `tools/controls.sh` and `tools/axioms.sh` are present and all
three **pass `--selftest` against Lean 4.22.0** — each plants a defect, catches
it, passes clean input, and then prints what it cannot catch.

**They also run green with no arguments on the package exactly as it arrives**,
and green again once a Part file and a negative control exist. Both states were
simulated end to end. That is worth stating because an earlier version of this
package **failed on arrival** — `controls.sh` demanded a negative control before
there was anything to control, and `axioms.sh` aborted the moment a control
existed, because it swept the control into its own probe. **A false red is the
same species as a false green and equally useless.**

Run all three yourself before trusting any output from them. Each is a few dozen
lines; read them rather than assuming. **A tool is evidence only for the failures
its author imagined**, and each says so in its own output.

## Verification discipline

Any claim that the pushed work compiles must be checked against the **pushed
bytes**, not the working tree — `git show <ref>:<path>` into a fresh temporary
directory.

Guard every step of that check. A `cd` into a directory that does not exist, or
a clone that fails, must abort rather than let the next command run somewhere
else. **A verification that silently ran in the wrong directory reports success
and means nothing.** If you catch yourself producing one, say so in the report.

## Layout

    README.md        what this is, one page
    lean/Core.lean   the definitions, verbatim
    lean/            Parts 0–D, one file or several
    lean/*_control.lean   the negative controls
    tools/           check.sh, controls.sh, axioms.sh
    RESULTS.md       the tables from Parts B and D, and nothing else

**Read this before writing the second file, because it is not obvious and it
will cost you an hour.** Zero imports means **there is no import.** A file in
`lean/` cannot see another file's definitions. Writing

    -- lean/PartA.lean
    theorem gate_ok : mul one one = one := by decide

fails with `Function expected at mul`, because `mul` is in a different file and
nothing brings it into scope. Verified.

**So every file in `lean/` that proves anything must begin with the contents of
`lean/Core.lean`.** Each file is standalone; that is what "compiles with
`lean <file>`" means. `tools/axioms.sh` probes **one file at a time** for
exactly this reason — the definitions legitimately repeat across files, and
concatenating them would declare `GZ` several times and compile nothing.

Negative controls follow the same rule and are named `lean/*_control.lean`.
`check.sh` and `axioms.sh` both skip them, because they are required to fail;
`controls.sh` is what checks them.

## What this task does not do

State this in `README.md` as a list, because a fixed assumption is invisible
until something else moves. This task holds all of the following fixed and
varies none of them:

- **the value ring** — `GZ` hardcodes `Int` in its own fields. It did not have to.
  A hand-declared `CRing R` class, the eight-parameter symbol over it, the
  pentagon over it, and invertibility stated as `∃ u, mul p u = one` all
  **compile in core with zero imports**, instantiated at `GZ`, `Int`, `Fin 2`,
  `Fin 8` and a ring with nilpotents — checked, not assumed, `EXIT=0`.
  **Varying the ring was never blocked by the toolchain; it is blocked by this
  definition.** The one thing the toolchain does block is `Rat`, which is not a
  core identifier, so the rationals need an import or a hand-rolled ring.
- **the shape of `Fs`** — one free parameter across eight admissible index
  patterns, and **the restriction is in the type signature**, not just the
  values. A general symbol would be `Int → Int → Int → GZ`.
- **the modulus** — `% 2` is written into `Fs` itself, so the label group is not
  a parameter either.
- the label set — `{0, 1}`
- **the encoding of finiteness** — `pentagonHolds` quantifies over `Int` with
  disjunction hypotheses rather than over `Fin 2`. `Fin 2` would make finiteness
  structural and the instance count free; the present form needs a separate
  theorem to recover what the type would have given.
- **the identity under test** — the pentagon only. The object satisfies other
  identities and none of them is examined here.

## Not part of this task

**Do not interpret the results.** No conclusions about what the tables mean, no
connection to any other structure, no discussion of significance. `RESULTS.md`
contains tables and theorem names. Interpretation happens separately, later,
after these numbers are fixed.

## Toolchain

If `lean` is not on PATH, install Lean 4 v4.22.0 from its GitHub release tarball
and put it on PATH. Confirm it works by checking that it accepts `2 + 2 = 4` and
rejects `2 + 2 = 5`. Commit whatever install script you write so the next person
does not repeat it.

## Order of work

Stop and report at the end of step 5 before continuing.

1. Toolchain working; `lean/Core.lean` compiling; all three tool `--selftest`s
   run and passing. All three are known to pass — if one does not, that is a
   finding about the environment and should be reported.
2. Part 0, complete. Nothing below it is meaningful until the object's own
   properties are established.
3. Part A, complete.
4. Part B, complete — the table, as theorems.
5. Part C, complete — both targets, both directions.

Then Part D, which uses Part B.
