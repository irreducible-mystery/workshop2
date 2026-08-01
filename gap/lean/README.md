# `gap/lean/` — what the kernel has actually settled

Nineteen theorems across five files. Every file compiles standalone with
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

---

## What is not proved here

The spectral statements — the ceiling/floor duality `s₊(G)` and `|s₊(−G)|` for
symmetric gap sets, the joint spectral radius for asymmetric sets, the closed
form for `+T^m` — all involve moduli of complex roots and are waiting on
Mathlib. So is anything about `ℚ`, `ℝ`, `−1/4` as an actual number, the Catalan
identity, and the Lyapunov results.

**Everything in `../sweeps/` remains computed and unproved.** These nineteen
theorems are the subset a kernel has now checked.
