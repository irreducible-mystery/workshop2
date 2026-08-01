# `gap/lean/` — what the kernel has actually settled

Thirty-nine theorems across nine files. Every file compiles standalone with
`lean <file>` and exits 0. Run `sh check.sh` to reproduce, including the axiom
census over every declaration.

**Toolchain.** Lean 4.22.0, core only. Not a principle — a Mathlib build is
running separately and the harder statements below are waiting on it. Core was
enough for everything here.

**Census.** Every theorem depends on `propext` and, where `omega` or `simp` was
used, `Quot.sound`. **No `sorryAx`, no `Classical.choice`, no `ofReduceBool`.**
The `decide`-only results in `Characteristic.lean` carry `propext` alone.

---

## `Vieta.lean` — the two invariants Kelly wrote down first

For distinct roots `x`, `y` of `x² = x + G` over `ℤ`:

| theorem | statement |
|---|---|
| `sum_of_roots` | **`x + y = 1`** |
| `product_of_roots` | **`x · y = -G`** |
| `discriminant_is_gap` | **`(x - y)² = 1 + 4G`** |

`φ + ψ = 1` and `φ × ψ = −1` are the case `G = 1`. They are not facts about the
golden ratio: they hold for **every** gap, and the third says the discriminant
**is** the squared distance between the two roots.

## `Reflexive.lean` — where the gap refers to itself

| theorem | statement |
|---|---|
| `gap_is_own_root` | `IsRoot G G ↔ G = 0 ∨ G = 2` |
| `no_gap_equals_discriminant` | no integer gap equals its own discriminant |
| `branch_point_not_integral` | **`1 + 4G = 0` has no integer solution** |
| `collision_root_not_integral` | **`2x = 1` has no integer solution** |
| `five_not_square` | `k² = 5` has no integer solution |

The middle two are the same fact twice: **the branch point is invisible to the
integers.** Not hard to reach — absent. This is the same statement that
characteristic 2 makes in its own way.

## `Ceiling.lean` — no schedule beats the constant gap

| theorem | statement |
|---|---|
| `step_bound` | `\|b + g·a\| ≤ \|a\| + \|b\|` for `g = ±1` |
| `run_bound` | **under EVERY sign schedule, `\|fₙ\| ≤ Fₙ₊₂`** |
| `plus_is_fib` | the all-plus schedule equals the Fibonacci numbers exactly |
| `ceiling_sharp` | so the bound is attained, hence sharp |

**Variation cannot beat commitment**, proved. Random, periodic, quasiperiodic,
adversarial or clairvoyant scheduling of `±1` never exceeds `φ` — and the
constant gap already achieves it.

## `Characteristic.lean` — where each named gap becomes the collision

All by `decide`, so the kernel evaluates them rather than trusting an argument.

| characteristic | fact |
|---|---|
| **5** | `1 + 4·1 = 0`, and `x² = x + 1` has the **unique** root 3 |
| **3** | `1 + 4·(−1) = 0`, and `x² = x − 1` has the unique root 2 |
| **17** | `4² = −1`, `1 + 4·4 = 0`, and `x² = x + 4` has the unique root 9 |
| **17** | `13² = −1` too, but `1 + 4·13 ≠ 0` and that gap **splits into two roots** |
| **2** | `x² + x = 0` identically; only the zero gap is reachable, and it has two roots — **no double root can exist** |
| **7** (control) | the golden gap has **no roots at all** |

The char-17 pair is the sharpest: **both `4` and `13` square to `−1`, and only
one of them is the collision.** Which one you call `i` decides which — and
nothing inside the field decides it for you.

## `Quadratic.lean` — why the mirror becomes a sphere, and why it doesn't here

| theorem | statement |
|---|---|
| `hmul_self` | quaternion squaring, componentwise |
| `factor` | `u·t + t·u = t → (2u − 1)·t = 0` |
| `imaginary_forced` | **every imaginary component `t` satisfies `(2·Re(x) − 1)·t = 0`** |
| `integral_solutions_are_real` | over `ℤ`, `2a = 1` is unreachable, so **the imaginary part must vanish** |
| `i_never_solves` | `i` solves no gap equation over `ℤ` |

Either the real part sits exactly at the collision, or the imaginary part is
zero. Over a field containing ½ that first branch opens and the solution set
becomes a **sphere**. Over the integers it cannot, so **every solution is real
and the sphere is absent rather than unfound.**

## `Schedules.lean` — two exact facts about specific schedules

| theorem | statement |
|---|---|
| `minus_period_six` | the constant `-1` schedule is **periodic with period 6** |
| `minus_bounded` | hence `\|fₙ\| ≤ 1` forever — **the floor, exactly** |
| `alternation_is_golden` | the `+-` transfer matrix has **trace 1, det −1** |
| `alt_char_poly` | so its characteristic polynomial is **L² = L + 1** |

The first is "the roots of `x² = x − 1` are primitive sixth roots of unity" in
elementary form. The last two are **the golden equation reappearing at double
the period** — alternating the two named gaps *is* the golden gap, half speed.
`alternation_is_golden` depends on **no axioms at all.**

## `Tropical.lean` — remove subtraction and the mirror cannot exist

In max-plus, `x ⊗ x = x ⊕ G` reads `2x = max x G`.

| theorem | statement |
|---|---|
| `tropical_unique` | **at most one solution, for every gap** |
| `tropical_solutions` | the full solution description, so uniqueness isn't vacuous |
| `tropical_no_second_root` | two distinct solutions is a contradiction |

There is never a second root, so **there is nothing for a mirror to exchange.**
The discriminant `1 + 4G` is built from a subtraction the semiring does not
have.

## `Shape.lean` — the golden gap is the reflexive one, and a correction

| theorem | statement |
|---|---|
| `gap_eq_sum_iff` | **`G = x + y ↔ G = 1`** — the gap equals the sum of its own roots at exactly one gap |
| `sq_one_Fin8` | `x² = 1` has **four** roots mod 8 |
| `gap_root_counts_Fin8` | but the **gap equation** has 2 or 0, never 4 |
| `gap_never_exceeds_degree_Fin8` | it never exceeds the degree bound, even though the ring is not a domain |
| `half_the_gaps_reachable_Fin8` | exactly half the gaps are reachable — the char-2 parity again, at 8 |

**A correction the kernel forced.** I claimed the gap equation inherits the
four-root shape over `ℤ/8`. `decide` refused it and left `sorryAx` in the
census. It does not: `x² − x` factors as `x(x−1)` with coprime factors, so the
count stays at 2 or 0. **The four-root shape belongs to `x² = 1`, a different
equation, and I had conflated them across several sweeps.**

## `ArtinSchreier.lean` — in characteristic 2 the branch point does not exist

`Fin 4` is not a field, so GF(4) is built explicitly. Core derives `DecidableEq`
but not an enumeration, so quantifiers go through an element list whose
**completeness is proved first** (`all_complete`).

| theorem | statement |
|---|---|
| `all_complete` | the enumeration is exhaustive — nothing else exists to quantify over |
| `F4_units` | every non-zero element is invertible: it really is a field |
| `phi_additive` | **`φ(x) = x² + x` is additive** — Frobenius minus identity, all sixteen pairs |
| `phi_kernel` | its kernel is exactly the prime field `{0,1}` |
| `half_reachable` | **exactly half the gaps are reachable** |
| `two_roots_each` | each reachable gap has **exactly two** roots |
| `no_double_root` | **no gap ever has a double root** |
| `unreachable` | the two unreachable gaps, named |

**There is no branch point in characteristic 2 at all.** The obstruction stops
being a collision and becomes a **parity**: half the gaps are simply out of
reach, and the ones in reach always have two distinct roots.

**Seven of these eight depend on no axioms whatsoever** — the strongest census
in the tree.

---

## What is not proved here

The spectral statements — the ceiling/floor duality `s₊(G)` and `|s₊(−G)|` for
symmetric gap sets, the joint spectral radius for asymmetric sets, the closed
form for `+T^m` — all involve moduli of complex roots and are waiting on
Mathlib. So is anything about `ℚ`, `ℝ`, `−1/4` as an actual number, the Catalan
identity, and the Lyapunov results.

**Everything in `../sweeps/` remains computed and unproved.** These nineteen
theorems are the subset a kernel has now checked.
