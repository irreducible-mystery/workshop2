# `gap/lean-mathlib/` — the half that needed real numbers

Forty-one theorems that could not be stated in core Lean, because they are about
`ℝ`, `ℂ`, `√5`, and **−1/4 as an actual number** rather than as an obstruction.

**Census.** `propext`, `Classical.choice`, `Quot.sound` throughout — the standard
three, and `Classical.choice` arrives with `ℝ` itself. **No `sorryAx`, no
`ofReduceBool`.**

**Reproducing.** `MATHLIB=/path/to/built/mathlib4 sh check.sh`. Mathlib 4.22.0
was built **from source** here because `cache.lean-lang.org`,
`release.lean-lang.org` and `reservoir.lean-lang.org` are all blocked by egress
policy in this environment — only GitHub is reachable, so the dependencies were
cloned individually at the revisions pinned in `lake-manifest.json`.

---

## `Branch.lean` — −1/4 as a number

| theorem | statement |
|---|---|
| `disc_zero_iff` | **`1 + 4G = 0 ↔ G = −1/4`** |
| `double_root_at_branch` | at that gap, `x² = x − ¼ ↔ x = ½` — **the two roots are one** |
| `disc_is_squared_gap` | `(x − y)² = 1 + 4G` over `ℝ` |
| `real_root_iff` | **a real root exists exactly when `G ≥ −1/4`** |
| `no_real_root_below` | below it, nothing real |
| `sPlus_is_root` | `(1 + √(1+4G))/2` is a root whenever one exists |
| `golden_identity` | at `G = 1` that root satisfies `φ² = φ + 1` |
| `sPlus_branch` | at `G = −1/4` it is exactly `1/2` |

In `Reflexive.lean` (core) the same point is proved *absent from `ℤ`*. Here it is
proved *present in `ℝ`, and unique*. Those are the same fact seen from the two
sides of the question the whole sweep was about.

## `Modulus.lean` — below the branch point, the gap fixes the modulus

| theorem | statement |
|---|---|
| `c_sum`, `c_prod` | Vieta over `ℂ`: sum 1, product −G |
| `conj_root` | the conjugate of a root is a root, when the gap is real |
| `normSq_eq_neg_gap` | **a non-real root satisfies `\|z\|² = −G`** |
| `modulus_below_branch` | so the common modulus is `√(−G)` — **the floor formula** |
| `gap_neg_one_cube` | at `G = −1`, **`z³ = −1`** |
| `gap_neg_one_sixth` | hence `z⁶ = 1` |
| `gap_neg_one_unit_modulus` | and `\|z\|² = 1` — **on the unit circle** |

Below −1/4 the two roots are a conjugate pair, so there is no "larger" one:
**only convention separates them, and the gap alone fixes how big they are.**
The `G = −1` case is the sweep's `e^{±iπ/3}` finding, proved: the roots are
primitive sixth roots of unity.

The modulus is written as `√(normSq z)` rather than `Complex.abs z` because that
API lives in an analysis module this build does not have. They are equal by
definition.

## `Golden.lean` — irrationality, and the one thing that exists only at −1/4

| theorem | statement |
|---|---|
| `sqrt5_irrational` | `√5` is irrational |
| `sPlus_one_irrational` | **the golden gap's root is irrational** |
| `sPlus_branch_rational` | **the branch point's root is exactly `1/2`** |
| `nilpotent_solution_at_branch` | in `ℝ[ε]/(ε²)`, `½ + ε` solves the gap equation at `G = −¼` |
| `nilpotent_forces_branch` | **and a solution with non-zero nilpotent part forces `G = −¼` and `Re = ½`** |

The last pair is the sharpest thing in this directory. The nilpotent direction —
the Jordan block, the logarithm in the ODE, the blocked deformation — **exists at
the branch point and provably nowhere else.** That was computed in sweeps 5, 17
and 36 and is now a theorem.

And the contrast with the line above it is worth stating: **the golden gap's root
is irrational; the collision's root is rational.** The gap where the object can
no longer tell itself apart is the one whose root is simplest.

## `GeneralCeiling.lean` — the ceiling at any gap magnitude

The core file proved `|fₙ| ≤ Fₙ` for unit gaps. This generalises it.

| theorem | statement |
|---|---|
| `bound_nonneg` | the bound sequence stays non-negative |
| `run_le_bound` | **any schedule of gaps of magnitude G is dominated term-by-term by the constant-G recurrence** |
| `const_attains` | and the constant schedule **is** that recurrence, so the bound is sharp |
| `geometric_solution` | `r² = r + G → rⁿ⁺² = rⁿ⁺¹ + G·rⁿ` — the bound grows at the object's own root |

**Variation cannot beat commitment, at every gap magnitude, not just 1.**

## `Casoratian.lean` — the determinant, and what it forbids

| theorem | statement |
|---|---|
| `casoratian_step` | **`W(n+1) = −sₙ · W(n)`** — the determinant identity with no matrix machinery |
| `casoratian_unit` | for unit gaps the Casoratian **never changes size** |
| `independent_forever` | so two independent solutions **stay independent forever**, whatever the schedule does |
| `catalan_gf_is_root` | `(1 − √(1−4x))/2` is a root of the gap equation at `G = −x` |
| `catalan_radius` | **a real root exists exactly for `x ≤ 1/4`** |
| `catalan_at_radius` | at the radius the two roots coincide at `1/2` |

The tree-counting series' radius of convergence **is** the branch point,
reflected. And growth and decay are locked together: the Casoratian cannot
vanish, so no schedule can make both solutions decay.

## `TransferWord.lean` — the closed form, via Cayley–Hamilton

No spectral API needed.

| theorem | statement |
|---|---|
| `det_T` | `det(T g) = −g` |
| `det_mul` | the determinant is **multiplicative** — no cancellation is ever possible across a word |
| `cayley_hamilton` | every 2×2 satisfies `M² = tr(M)·M − det(M)·I` |
| `transfer_satisfies_gap` | for the transfer matrix that reads **`M² = M + g·I`** — the gap equation itself |
| `Tpow_closed` | powers of the negative-gap matrix, in closed form via `p(k+1) = p(k) − b·p(k−1)` |
| `det_Tpow`, `word_det` | `det(+Tᵐ) = −bᵐ` |
| `word_trace` | **`tr(+Tᵐ) = (2−b)·p(m) − b·p(m−1)`** |

That trace-and-determinant pair is the sweep-75 closed form, proved. The
remaining step — reading the larger eigenvalue off `(|T| + √(T²−4D))/2` — is the
quadratic formula already proved in `Branch.lean`.

**`transfer_satisfies_gap` is the one I would keep.** The matrix that advances
the system by one step satisfies *the gap equation itself*. The object and its
own time-evolution obey the same law — which is why every scheduling question
kept coming back to the same two roots.

---

## Still not proved

**The joint spectral radius** for asymmetric gap sets — the sup over *all* words
is a limsup of matrix norms, and proving a particular word attains it is the
finiteness property, an open problem in general.

**The Lyapunov exponent and the large-deviation results** — Viswanath's
constant, the three growth rates, the rate function. These need ergodic theory
and a genuinely different toolkit.

**The Catalan coefficient identity** — that the series coefficients *are* the
Catalan numbers. The algebraic functional equation is proved above; the
coefficient extraction needs formal power series.

These are stopping points, not gaps I ran out of time on. Everything else in
`../sweeps/` that a kernel can reach, it has now reached.
