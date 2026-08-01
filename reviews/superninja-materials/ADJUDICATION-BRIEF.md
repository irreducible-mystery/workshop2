# Adjudication brief — reference ledger for reviewing agents

This file exists so that reviewers of the SuperNinja materials have a fixed,
checkable list of what workshop2 has actually **proved in a kernel**, what it has
only **computed**, and what it has **retracted**. Do not treat anything outside
this list as established by workshop2.

---

## A. Kernel-verified (Lean 4.22.0, EXIT=0, `#print axioms` census injected)

### `gap/lean/` — 66 declarations, core Lean only, no imports

| file | key results |
|---|---|
| `Vieta.lean` | `sum_of_roots` (x+y = 1), `product_of_roots` (x·y = −G), `discriminant_is_gap` ((x−y)² = 1+4G) |
| `Reflexive.lean` | `gap_is_own_root` (G ∈ {0,2}), `no_gap_equals_discriminant`, `branch_point_not_integral` (1+4G = 0 has no ℤ solution), `collision_root_not_integral`, `five_not_square` |
| `Ceiling.lean` | `step_bound`, `run_bound` (\|fₙ\| ≤ Fₙ₊₂ under every sign schedule), `plus_is_fib`, `ceiling_sharp` |
| `Characteristic.lean` | 17 `decide` theorems: disc vanishes at G ≡ −1/4 in char 5 (= +1), char 3 (= −1), char 17 (= i); golden gap *is* the critical gap mod 5; char 2 additivity; char 7 control (golden gap has no roots) |
| `Quadratic.lean` | `imaginary_forced` ((2·Re(x) − 1)·t = 0), `integral_solutions_are_real`, `i_never_solves` |
| `Schedules.lean` | `minus_period_six`, `alternation_is_golden` — **no axioms at all** |
| `Tropical.lean` | `tropical_unique` (at most one root per gap in max-plus), `tropical_no_second_root` |
| `Shape.lean` | `gap_eq_sum_iff` (G = x+y ⟺ G = 1), `gap_root_counts_Fin8`, `half_the_gaps_reachable_Fin8` |
| `ArtinSchreier.lean` | GF(4) built explicitly with a proved-complete enumeration; `phi_additive`, `phi_kernel`, `two_roots_each`, `no_double_root`, `unreachable`. 7 of 8 need **no axioms** |

### `gap/lean-mathlib/` — 41 declarations, Mathlib 4.22.0 built from source

| file | key results |
|---|---|
| `Branch.lean` | `disc_zero_iff` (1 + 4G = 0 ⟺ G = −1/4), `double_root_at_branch` (the double root is exactly 1/2), `real_root_iff`, `no_real_root_below` |
| `Modulus.lean` | `normSq_eq_neg_gap`, `modulus_below_branch`, `gap_neg_one_cube` (z³ = −1), `gap_neg_one_unit_modulus` |
| `Golden.lean` | `sqrt5_irrational`, `sPlus_one_irrational`, `nilpotent_solution_at_branch`, `nilpotent_forces_branch` (a nilpotent solution exists **iff** G = −1/4, and then Re = 1/2) |
| `GeneralCeiling.lean` | `run_le_bound`, `const_attains` — **variation cannot beat commitment**: no sign schedule beats the constant gap |
| `Casoratian.lean` | `casoratian_step` (W(n+1) = −sₙ·W(n)), `independent_forever`, `catalan_gf_is_root`, `catalan_radius` (= 1/4) |
| `TransferWord.lean` | `cayley_hamilton`, `transfer_satisfies_gap` (M² = M + g·I for M = [[1,g],[1,0]]), `word_trace`, `word_det` |

**Axiom census result:** 66 core declarations carry at most `Classical.choice`;
`sorryAx` count is **0** across both trees. The census is *injected* by
`check.sh` over every extracted declaration and aborts if it cannot extract.

---

## B. Computed but NOT kernel-verified

53 numbered sweeps in `gap/sweeps/` (19 Python scripts, standard library only).
Exact-arithmetic sweeps (characteristic collisions, Catalan coefficients,
reflexive conditions, Cayley–Dickson identities, tropical counts, entropy) are
rational/integer and re-runnable. Numerical sweeps (monodromy, zero spacings,
winding parities, Lyapunov exponents, orbits) agree with prediction **to the
digits shown and no further**.

Notable computed-only results: monodromy group is Z/2; ℂ 2 points → ℍ 2-sphere
→ 𝕆 6-sphere, sphere dimension 2ⁿ − 2; the mirror is outer over ℂ and inner over
ℍ (j·i·j⁻¹ = −i); Mandelbrot cusp at −1/4; logistic window 1 < r < 3;
rotation numbers below −1/4 (period 3 at G = −1, 4 at −1/2, 6 at −1/3);
Viswanath's constant 1.13198824 from mixing gaps ±1; three growth rates for one
random system (mean 1, typical 1.131988, second-moment 1.272020).

---

## C. Retracted or corrected by workshop2 itself

- **−1/4 was misread twice** — once as a maximally excluded ring value (claim
  C153, retracted), once as a conformal weight. Both wrong. It is the value of
  the GAP at which the discriminant vanishes.
- **"Every rotation number gives an order premium"** — false; four negatives
  appear in workshop2's own table (sweep 69 is the retraction).
- **"The ceiling is the root at max\|G\|"** — false; workshop2's own row refuted
  it (sweep 70).
- **"A schedule cannot make it shrink"** — false. Correct statement:
  ceiling = s₊(\|G\|), floor = \|s₊(−\|G\|)\| (sweep 25). **This correction was
  itself stated without the absolute values until 2026-08-01, and in that form
  it is false for `G < 0`** — the gap set `{+G, −G}` is the same set for `G` and
  `−G`, so every invariant must be even in `G`, and `s₊(G)` is not. At
  `G = −0.2` the unrestricted form gives ceiling `0.7236` against a true ceiling
  of `1.1708`, exactly swapping the two. See `FAILURES.md` `F1`.
- **Fin 8 root counts asserted from memory** — conflated x² = 1 (4 roots mod 8)
  with the gap equation (2 roots). Corrected in kernel.
- Three of four kernel-forced corrections had **planted `sorryAx` in files that
  still exited 0**. Exit code alone proves nothing.

---

## D. Standing methodological rules in this workshop

1. **A file that compiles is not a file that proves.** `lean f.lean; echo $?`
   returns 0 for a file full of `sorry`. Only `#print axioms` over *every*
   declaration settles it.
2. **Piped exit status lies.** `lean file | head` reports head's status.
3. **A count is a claim.** "33 files, 7,149 lines, 4 key theorems" is checkable
   and must be checked.
4. **Framework name-dropping is not a framework result.** "Category theory: GAP
   terminal object" is a claim with a definition, a category, and a proof
   obligation attached. Absent those, it is a sentence.
5. Extracting a fragment out of a file that already contains it and then
   compiling the fragment standalone produces fake errors. Workshop2 made this
   mistake against SuperNinja's own section files.

---

## E. What reviewers are asked to do

For every distinct claim in the assigned document, assign exactly one bucket:

- **[V]** Verified — matches a kernel result in section A. Cite the declaration.
- **[C]** Computed — matches a sweep in section B. Say which.
- **[O]** Open and checkable — a well-posed mathematical claim nobody here has
  checked. Say precisely what computation or proof would settle it.
- **[R]** Restatement — true, but a re-labelling of something already in A or B
  with no new content. Say what it restates.
- **[X]** Category error — the sentence does not have a truth value as written
  (undefined terms, a metaphor stated as an identity, a physical constant
  attached to a dimensionless algebraic quantity). Say which term is undefined.
- **[F]** False — contradicts section A, B, or C, or is checkably wrong. Show
  the contradiction.

**Name the good first.** Several of these documents independently rediscover
results in section A without having seen the proofs. That convergence is a real
finding and must be stated before any criticism. Do not soften [F] or [X] to be
kind, and do not inflate [O] to [V] — but do not let a document's weakest
paragraph decide the verdict on its strongest.
