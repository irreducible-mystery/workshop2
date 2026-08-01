# `gap/lean-mathlib/` — the half that needed real numbers

Fifteen theorems that could not be stated in core Lean, because they are about
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

---

## Still not proved

The joint spectral radius for asymmetric gap sets, the `+Tᵐ` closed form, the
Catalan coefficient identity, and the Lyapunov/large-deviation results. Those
need either a spectral-radius API or genuinely new work, not just a bigger
tactic set.
