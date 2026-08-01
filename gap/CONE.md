# The branch point is the collapse of the common invariant cone

*Found while playing, 2026-08-01. Kernel-verified. This is the one thing in the
sweep that I think has actual content, and it was found by trying to break a
result rather than by extending one.*

---

## The setup

The gap recurrence `f(n+1) = f(n) + g(n)·f(n−1)` has transfer matrix

    T(g) = [[1, g], [1, 0]]      char. poly   λ² = λ + g

so the eigenvalues of `T(g)` are the roots of the gap equation at gap `g`. Fix
`a > 0` and let the schedule choose freely from `{+a, −a}` at every step. Two
questions: how fast can the product grow, and how slowly?

These are the **joint spectral radius** and the **joint spectral subradius** of
the pair `{T(+a), T(−a)}`. In general both are NP-hard, and the finiteness
property — that the extreme is attained by a periodic word — is *false* in
general (Bousch–Mairesse). So a closed form is not something to expect.

## What the numerics said

    ceiling = s₊(a)          floor = |s₊(−a)|

to 8 decimals at every `a` tested, where `s₊(G) = (1 + √(1+4G))/2`. But the
minimizing words split the picture in two:

| a | minimizing word |
|---|---|
| 0.24 | `-------` (constant) |
| 0.26 | `----` |
| 0.30 | `--++--++----` |
| 0.50 | `++-+--+---` |
| 2.00 | `++-++-` |

Above `a = 1/4` the minimizer stops being constant, and the number of words
attaining the floor explodes: 105 at a = 0.3, 1738 at a = 0.5, 5060 at a = 1,
6191 at a = 2 (lengths ≤ 14). That degeneracy is the tell.

**Above 1/4 the floor is free.** `s₊(−a)` has complex roots there, so
`|s₊(−a)| = √|det| = √a`, and every 2×2 matrix satisfies `ρ ≥ √|det|` while every
letter has `|det| = a`. The bound is the determinant bound; anything whose two
eigenvalues have equal modulus attains it. Nothing to prove.

**Below 1/4 it is not free.** There `√a < 1/2 < s₊(−a)`, so the determinant
bound is strictly slack and the true floor sits above it. Exact rational
arithmetic over every sign word to length 18, at a = 0.10, 0.20, 0.24: **no word
beats the constant schedule.** Agreement to 1e-16.

Two regimes, two different reasons, glued at 1/4 by a formula that happens to be
uniform because the modulus of the complex root is exactly the determinant bound.

## Why — and this is the part worth keeping

Take the sector

    K(α) = { (x, y) : 0 ≤ y  ∧  α·y ≤ x }

and ask when **both** letters preserve it. One step is `(x,y) ↦ (x + g·y, x)`.

- `T(+a)`: needs `x(1−α) + a·y ≥ 0`. **Free**, for any `0 ≤ α ≤ 1`.
- `T(−a)`: needs `x(1−α) ≥ a·y`. Since `x ≥ α·y`, it suffices that

      α·(1 − α) ≥ a

and `max(α − α²) = 1/4`. So:

> **A cone preserved by both letters exists if and only if `a ≤ 1/4`.**

And `α² = α − a` **is the gap equation at gap `G = −a`.** The admissible slope
condition is that equation's discriminant being nonnegative. The threshold is
not *analogous* to the branch point; it is the branch point, computed again in
a different currency.

The sharp form is better still. The admissible slopes are exactly

    rMinus(a)  ≤  α  ≤  rPlus(a)          rPlus/rMinus = (1 ± √(1−4a))/2

— **the closed interval between the two roots.** Verified numerically before it
was proved:

    a=0.050  admissible α ∈ [0.052786405, 0.947213595]
    a=0.150  admissible α ∈ [0.183772234, 0.816227766]
    a=0.240  admissible α ∈ [0.400000000, 0.600000000]
    a=0.250  admissible α ∈ [0.500000000, 0.500000000]   ← a point

At the branch point the interval degenerates to the single slope `1/2`, which is
the double root. So this is not "a cone exists below and not above." It is:

> **The space of common invariant cones is an interval whose endpoints are the
> two roots. It shrinks as the roots approach each other, becomes a single cone
> at the moment they collide, and is empty thereafter.**

The collapse of the two roots into one and the collapse of the cone family into
one cone are the same event, seen from inside and from outside.

And it explains the growth result rather than restating it. Below the branch
point the pair is cone-preserving, which is precisely the regime where
Perron–Frobenius-type theory hands you extremal norms and constant words as
extremizers. Above it, no common cone survives, and the floor falls back onto
the free determinant bound — which is exactly the degeneracy the word counts
showed.

## What is proved

`gap/lean-mathlib/Cone.lean`, Lean 4.22.0 + Mathlib, **12 declarations, 12
audited, `sorryAx` 0**:

| declaration | statement |
|---|---|
| `step_pos_mem` | `T(+a)` preserves `K(α)` for every `0 ≤ α ≤ 1`, no condition on `a` |
| `step_neg_mem` | `T(−a)` preserves `K(α)` whenever `a ≤ α(1−α)` |
| `step_both_mem` | hence the whole sign family preserves one sector |
| `admissible_iff_square` | `a ≤ α(1−α) ↔ (α − ½)² ≤ ¼ − a` |
| `cone_exists_iff` | **`(∃α ∈ [0,1], a ≤ α(1−α)) ↔ a ≤ 1/4`** |
| `cone_unique_at_branch` | at the branch point the slope is forced to be `1/2` |
| `no_cone_above_branch` | above it, nothing |
| `rPlus_is_root`, `rMinus_is_root` | the endpoints really are roots of `x² = x − a` |
| `admissible_iff_between_roots` | **the admissible slopes are exactly `[rMinus, rPlus]`** |
| `interval_collapses_at_branch` | **`rMinus = rPlus ↔ a = 1/4`** |

## What is NOT proved

The growth statement itself. `cone_exists_iff` and
`admissible_iff_between_roots` are proved; that the cone's existence *implies*
JSR = `s₊(a)` and subradius = `s₊(−a)` is the Perron–Frobenius half and is not
formalised. The ceiling half is separately proved in `GeneralCeiling.lean`
(`const_attains`). The floor half below 1/4 is **computed to length 18 in exact
arithmetic and not proved.**

Standing caveat, unchanged: the cone geometry is elementary and someone has
almost certainly written it down. It is being checked against the literature.
The claim here is that it is *true* and *kernel-verified*, not that it is new.
