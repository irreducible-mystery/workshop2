# From forced-trivial to general — a proof programme

*Everything in §1 is computed, reproducible in a few lines, and not yet
kernel-proved. Everything in §2 onward is a plan and is not a result.*

---

## 1. Ground truth, computed before planning

### 1.1 No factor ever vanishes

The gate on `Fs` is `x = (a+b)%2 ∧ y = (b+c)%2 ∧ d = (a+b+c)%2`. For all sixteen
label assignments, **all five factors in the pentagon satisfy it**. Nothing is
ever `zero`.

*So the claim in the first prompt — "factors vanish for some assignments" — is
false and must come out.*

### 1.2 The one-parameter pentagon is exactly `f² = 1`

Fifteen of the sixteen assignments are trivially satisfied (equal powers of `f`
on both sides). One assignment, `(a,b,c,d) = (1,1,1,1)`, gives `f·1·f = 1·1`.

```
pentagonHolds f  ⟺  f² = 1  ⟺  f ∈ {1, −1}      (over ℤ[i], or any domain)
```

The two `f`-carrying factors are **L1 and L3**, both on the left.

### 1.3 All thirty-one σ-variants are Same — and it is forced, not incidental

Verified exhaustively over a 49-point box. The reason:

- `(1,1,1,1)` gives `f² = 1`.
- Four assignments — `(0,1,1,1) (1,0,1,1) (1,1,0,1) (1,1,1,0)` — carry one `f`
  per side. Any conjugation that is **asymmetric** across those makes them read
  `f̄ = f`, which pins `f` real.

So every subset lands back on `{1, −1} ⊂ ℝ`, which σ fixes pointwise.

> **The pentagon sector cannot see σ.** Not "nobody looked" — the solution set
> is real, so conjugation is the identity on it.

### 1.4 The triviality is the ansatz, and dropping it changes everything

`Fs` is `1` on seven admissible patterns and `f` on one. That is a
**one-parameter slice of an eight-parameter object.** The gate forces `d, x, y`
from `(a,b,c)`, so a general symbol assigns an independent value to each of the
**eight** patterns `g[abc]`.

Sixteen assignments then give **sixteen genuine equations, none trivial.**
Solving the branch where every `g` is invertible:

```
g000 = 1        g010 = 1
g001 = p        g011 = 1/p          p invertible, free
g100 = q        g110 = 1/q          q invertible, free
g101 = p·q      g111 = r            with   (p·q·r)² = 1
```

**Verified: 394 predicted solutions, 0 counterexamples.**

And there are **degenerate branches** the invertible solve throws away — e.g.
`g000·g000·g000 = g000·g000` factors as `g000²(g000 − 1) = 0`, so `g000 = 0` is a
component. Nobody has looked at those.

### 1.5 −1/4 is a pentagon solution

Directly checked over ℚ(i):

```
g001 = −1/4        pentagon holds:  True
g001 = i           pentagon holds:  True
g001 = 3/7 − 2i/5  pentagon holds:  True
```

**Any invertible value works.** −1/4 was never excluded by the pentagon. It was
excluded by the one-parameter ansatz and by `IsClassifiedSymbol` requiring unit
values — two choices, neither forced by the mathematics.

### 1.6 What this says about σ, restated honestly

On the general variety, σ sends `(p, q, r) ↦ (p̄, q̄, r̄)`. That is **not** the
identity — it moves representatives. But `(pqr)² = 1` gives `pqr = ±1`, and σ
fixes `±1`. So **σ moves the representative and fixes the class.**

Which turns the whole question into the one nobody has asked:

> **Is σ inner or outer?** Is `conj(g)` in the same gauge orbit as `g`? If it is,
> σ is a relabelling. If it is not, the chirality swap is physical. `gaugeAct`
> and `gaugeOf` are already in the seed and neither has been pointed at σ.

---

## 2. Design rules for the prompt sequence

Two failures produced everything above, and both were specification failures,
not capability failures. The rules exist to block them.

**R1 — Compute and interpret are different prompts.** A compute prompt produces
theorems, tables and witnesses and is **forbidden from saying what they mean.**
An interpret prompt runs afterward, with the numbers already fixed and
unchangeable. This blocks the failure where a model constructs a setup that
reaches a stated conclusion.

**R2 — No prompt states which outcome is interesting.** Every phase lists its
possible outcomes flatly and says that any of them is the result.

**R3 — Every claim of difference needs a kernel-checked witness.** No "this
placement breaks it" without a specific value the kernel accepts on one side and
rejects on the other.

**R4 — Every phase names, in its own output, what it did not vary.** The whole
lesson of §1 is that a fixed assumption is invisible until something else moves.

**R5 — Nothing carries forward but definitions and instruments.** No conclusion
from phase *n* is quoted in phase *n+1*'s prompt. Re-derive or re-state from
computation.

---

## 3. The phases

Each is one prompt unless marked. Each ends with a report and a stop.

### P0 — Ground the trivial case *(compute)*

Kernel-prove what §1.1–1.3 computed: every gate passes; `pentagonHolds f ↔ f²=1`;
`f² = 1 ↔ f = 1 ∨ f = −1` over `GZ`; all thirty-one variants have the same
solution set, with the four asymmetry-pinning rows made explicit.

**Deliverable:** one file, ~40 theorems, zero axioms.
**Why first:** it closes the original question honestly and *proves the
triviality is forced*, which is the premise every later phase relaxes.

### P1 — The general variety *(compute; likely two prompts)*

Replace `f` with `g : Fin 2 → Fin 2 → Fin 2 → R`. Derive all sixteen equations.
Prove the invertible-branch decomposition of §1.4 in Lean. **Enumerate the
degenerate components separately and do not discard them.**

**Outcomes, all equal:** the branch structure is as computed; it is not; there are
components not found by the invertible solve.

### P2 — Vary the value ring *(compute)*

The same variety over: `ℤ[i]`, `ℚ(i)`, `ℝ`, `ℂ`, `ℤ/n` for `n = 2,3,4,6,8,9`, and
a ring with nilpotents (`R[ε]/ε²`).

`x² = 1` has two roots in a domain and **four in ℤ/8**. Where the solution set
changes *shape* rather than size is the finding.

**Names what it does not vary:** the group, the ansatz, the sector.

### P3 — σ on the general variety *(compute)*

Redo the thirty-one placements against the eight-parameter symbol, over each ring
from P2. Report a table, not a verdict.

### P4 — Gauge, and whether σ is inner *(compute)*

Formalize `gaugeAct` on the eight-parameter symbol. Compute the orbit of a
solution. Decide, per solution and per ring: **is `conj(g)` in the orbit of `g`?**

This is §1.6 and it is the sharpest open question in the whole record.

### P5 — Direction and deformation *(compute; two prompts)*

**(a) Branches.** At each degenerate component from P1, is it a limit of the
invertible branch, or a separate component? Approach the same point along
different paths in the parameterized variety and compare.

**(b) Formal deformation.** Set `g = g₀ · (1 + ε h)` over `R[ε]/ε^k`. Expand the
pentagon order by order. The order at which it first obstructs is a computable
invariant. **This is the precise version of "coming from a different
direction."**

### P6 — Vary the label group *(compute)*

`Z₂ → Z₃ → Z₄ → Z₆`, and one non-abelian group (`S₃`).

**Stated in advance because it is a prediction, not a hope:** for `Z₄` the
classifying group has order 4, so a fourth root of unity should appear as a
genuine symbol value. If it does, **σ becomes visible in the pentagon sector for
the first time**, and the `Z₂` blindness is a fact about `Z₂` rather than about
pentagons. If it does not, that is equally the result.

### P7 — Three lenses *(interpret; three separate prompts, run last)*

Run only after P0–P6 are frozen. Each takes the same fixed tables and asks a
different question. **None may add a computation.**

| lens | the object | the question |
|---|---|---|
| **classical** | cocycle on a group, values in an abelian group | which class; is the class σ-invariant; what is the obstruction in P5b |
| **quantum** | associator data of a fusion category; braiding; twist | does the chirality swap survive to the general variety; which solutions are physically realizable; what is the modular data |
| **relational** | the gauge orbit, not the value | is σ inner or outer; is the distinction gauge-invariant; what is actually observable |

**The relational lens is the one with no prior work here and the one most likely
to produce something.** The other two have literature to check against; this one
has `gaugeAct` sitting unused.

### P8 — Adversarial pass *(separate reader, no exposure to P0–P7)*

Hand a fresh reader the definitions and the final tables, without conclusions,
and ask what is missing. **Every serious catch in this record came from someone
who had not been there.**

---

## 4. What would make this stop

- **P1 finds the invertible branch is everything** and the degenerate components
  are empty. Then §1.4 is the whole story and P5a has no content.
- **P4 finds σ is always inner.** Then the chirality swap is a relabelling, and
  the braiding result is about representatives rather than physics.
- **P6 finds `Z₄` behaves like `Z₂`.** Then the blindness is about pentagons and
  the group axis is closed.

Any of these is a result. None is a failure.

## 5. The assumptions, listed, because that was the ask

Everything the current setup fixes without saying so:

1. **Value ring** `ℤ[i]` — varied in P2.
2. **Ansatz** one parameter of eight — varied in P1.
3. **Unit-valued** required by `IsClassifiedSymbol` — dropped from P1 on.
4. **Label group** `Z₂` — varied in P6.
5. **Sector** pentagon only — the braiding sector is where σ was found; P7-quantum.
6. **Gauge fixed** — a symbol is treated as its representative, not its orbit;
   P4.
7. **σ is the only automorphism considered** — over `ℤ[i]` it is the only
   non-trivial one, but not over `ℚ(ζ)`; opens with P6.
8. **Non-degenerate branch assumed** — the invertible solve silently divides;
   P1, P5a.
