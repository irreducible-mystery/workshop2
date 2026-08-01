# Adjudication of five circulated SuperNinja documents

*From workshop2. Method: four independent reviewing agents, one per document,
each given the same fixed ledger (`superninja-materials/ADJUDICATION-BRIEF.md`)
of what this workshop has proved in a kernel, what it has only computed, and
what it has retracted. Each was required to name what is good before what is
wrong, to bucket every claim, and to cite a Lean declaration name, a sweep
number, or actual computed output as evidence. Nothing here rests on anyone's
judgement by eye; the finite claims were executed.*

**Buckets:** **[V]** verified against the kernel · **[C]** computed, not
kernel-verified · **[O]** open and checkable · **[R]** restatement · **[X]**
category error (no truth value as written) · **[F]** false.

---

## 1. `GAP_MATHEMATICS_CLEAN.md`

### The core math is correct in every particular

Lines 1–31 — "GAP Equation Fundamentals" and "Mathematical Properties" — were
checked in exact arithmetic, not floating point. Every number is right, and each
maps onto a kernel declaration:

| document says | kernel says |
|---|---|
| `x = (1 ± √(1+4G))/2` solves `x² = x + G` | `sPlus_is_root`, `real_root_iff` (`Branch.lean`) — residual verified 0 for both signs |
| `D = 1 + 4G`, and `D = 0` at `G = −1/4` | `disc_zero_iff` (`Branch.lean`), `discriminant_is_gap` (`Vieta.lean`) |
| double root at `G = −1/4` is exactly `1/2` | `double_root_at_branch` — and the kernel states it as an **iff**, which is stronger than the document |
| `D = 5` at `G = 1`; roots `φ`, `−1/φ` | `sPlus_one`, `golden_identity`, `sPlus_one_irrational` |
| `φ + (−1/φ) = 1` and `φ × (−1/φ) = −1` | `c_sum`, `c_prod` (`Modulus.lean`) — Vieta over ℂ, which is what's needed since φ ∉ ℤ |

One detail worth naming because it is the exact place careless write-ups slip:
**`−1/φ` really is the correct name for `(1−√5)/2`.** Verified symbolically,
`simplify((1−√5)/2 + 1/φ) = 0`. Most documents that reach for this write `1/φ`
or `−φ`. This one gets it right.

The document's two "Key Parameters" — `G = 1` and `G = −1/4` — are precisely this
workshop's two named gaps, arrived at without access to the proofs. That is
convergence from an independent direction and it counts.

### Two near-misses that count in its favour

- It lists `√3/2` and "60° geometry" under Shadow Casting. At `G = −1` the roots
  are primitive sixth roots of unity, `1/2 ± i√3/2` — literally 60° geometry —
  proved in `gap_neg_one_cube` and `gap_neg_one_unit_modulus`. The document has
  the right number with no derivation attached to it.
- Its two Key Parameters are **the same gap in characteristic 5**: `4⁻¹ ≡ 4
  (mod 5)`, so `−1/4 ≡ 1 (mod 5)`. Proved in `Characteristic.lean`. The document
  lists both numbers side by side and misses that they coincide.

### The Six Framework Convergence supplies nothing checkable

Six frameworks, six one-line labels, and for all six: no category, no functor,
no topos, no operator algebra, no language, no universal property.

| framework | label | what would have to be defined |
|---|---|---|
| Homotopy | "GAP universal property" | a space or ∞-groupoid, a diagram, the universal property with its uniqueness clause |
| Category | "GAP terminal object" | a category (objects? morphisms?) and a unique-morphism proof. `−1/4` is a real number; a real number is not an object of any category the document defines |
| Thermodynamics | "critical transition point" | a system, a free energy, an order parameter, a divergent derivative |
| Model theory | "logical boundary condition" | a language, a theory, a class of structures. "Boundary condition" is not a model-theoretic term |
| Noncommutative geometry | "operator algebra constraint" | a C\*- or von Neumann algebra and the constraint as a spectral statement |
| Topos | "subobject classifier" | a topos, and an object Ω with `true : 1 → Ω`. A subobject classifier is an object with a map, not a number — this is a type error before it is a false statement |

In three of the six there is a real result standing next door that the document
does not state. Homotopy: the monodromy computation, one loop around −1/4
exchanges the roots, π₁ → Z/2 (sweeps 12–15, computed-only). Thermodynamics: the
indicial equation of `r²u″ = Gu` reduces to `v″ = (G+¼)v`, so a logarithm is born
exactly at −1/4 (sweeps 30–36, computed-only). Model theory: the kernel proves the
honest version, `real_root_iff` — a real root exists **iff** `−1/4 ≤ G`, over ℝ,
with no model theory involved.

### The Lean count has no reachable artifact

"7,149 lines across 33 files" and four named theorems — `foundation_paradox`,
`completion_gap_necessity`, `cross_framework_equivalence`, `shadow_projection`.
Reachable Lean in this repository: **973 lines across 15 files** under `gap/`,
2,353 lines across 48 files repo-wide. `completion_gap_necessity` and
`cross_framework_equivalence` appear nowhere in the repository except in the
document asserting them; `foundation_paradox` appears only in SuperNinja's own
sibling documents, never in a `.lean` source. The nine framework files the
siblings name — `HomotopyGap.lean`, `CategoryGap.lean`, `ThermodynamicGap.lean`,
`ModelGap.lean`, `NoncommutativeGap.lean`, `ToposGap.lean`,
`CrossFrameworkTheorems.lean`, `ShadowCastingObject.lean`, `InfiniteAscent.lean`
— are not present in the working tree or on any branch.

This is bucket **[O]**, not [F]: the files may exist somewhere we cannot see. But
a count is a claim (rule D.3), and this one currently has nothing behind it that
a reader can check. Producing the 33 files with `#print axioms` over every
declaration would settle it in an afternoon.

### The five "Novel Mathematical Patterns" are definitions dressed as discoveries

None carries a theorem, none is proved to have any property, and none is
connected to `x² = x + G` by any stated equation. Two are checkably broken:

- **`W = (1/2π) ∮ (v·dl)/r`** — **[F]**, dimensionally wrong. `v·dl` is m²/s,
  divided by `r` gives m/s. `W` has units of velocity and cannot be an integer
  winding number. The correct form is `(1/2π)∮∇θ·dl`. There *is* a genuine
  winding number in this work — monodromy Z/2 — and it is not this.
- **`T_p = T_real / f_brain`** — **[F]**, `s ÷ s⁻¹ = s²`. Not a time.

**`x ⊙ G = x + G − (x⊗G)`** deserves its own note, because the undefined `⊗` is
load-bearing rather than cosmetic. Three readings, three different objects:

- `⊗` = ordinary multiplication → `x + G − xG`, the probabilistic sum.
  Commutative, associative (verified symbolically), identity 0, isomorphic to
  ordinary multiplication via `x ↦ 1−x`. Real, standard, about 150 years old.
- `⊗` = tropical multiplication — which is how **this workshop's own**
  `gap/lean/README.md` uses the symbol, writing `x ⊗ x = x ⊕ G` → the whole
  expression collapses to `0` identically.
- `⊗` = tensor product → `x ⊗ G` is not a scalar; the expression does not
  typecheck.

The document picks none of the three. And the only available link to the GAP
equation is circular: *if* `x² = x + G`, then `x ⊙ G = x(x−G)` under the first
reading — a consequence of assuming the equation, not evidence for the operation.

### The physics: mostly correct, entirely disconnected

This section should not be dismissed wholesale, because most of it is right.

**Correct as stated:** the Hawking power formula `P = ħc⁶/(15360πG²M²)` — verified
against Stefan–Boltzmann on the horizon at two masses, ratio 1.0000000000 to ten
decimals. The degrees-of-freedom counts 4D→10, 8D→36, 20D→210 (`n(n+1)/2`, all
three). SU(3)'s 8 generators and its hexagonal A₂ root system. Both time-dilation
formulas (γ = 5/3 at v = 0.8c, verified). Planck time `5.391×10⁻⁴⁴ s` and its
reciprocal `1.855×10⁴³ Hz`. Octopus neuron count ~500M.

**Wrong on its own terms:** graphene's 2.46 Å is the **lattice constant**, not the
carbon–carbon distance — C–C is 1.42 Å and `a = √3 · a_CC = 2.4595 Å`. And QCD
colour SU(3) is not spontaneously broken; the Standard Model breaking is
SU(2)×U(1)→U(1).

**But the dominant failure is not error, it is disconnection.** Zero of the
eighteen physics items states any link to `x² = x + G`. Three of them use `G` for
Newton's constant — 6.674×10⁻¹¹ m³kg⁻¹s⁻² — in a document that uses `G` for a
dimensionless gap. Correct physics adjacent to correct algebra is not a bridge
between them.

### Verdict on this document

Lines 1–31 are reliable and independently confirm the kernel. Two phrases inside
them — "complete self-reference", "completion-gap minimum" — are undefined and
carry no content. Everything after line 31 is a different document: six framework
labels with nothing behind them, a file count with no reachable artifact, five
definitions presented as discoveries of which two are dimensionally impossible,
and eighteen physics facts that are mostly correct and connected to nothing.

The fix is cheap and it is not "write less." Split the file. The first 31 lines
are a correct, checkable statement of the object. Let them stand alone under
their own name.

---

## 2. `lean_mathematical_summary.md`

*Done by hand rather than by agent: three of the four reviewing agents died
without producing output, and this one is a mechanical diff that a script settles
in two minutes. Extractor with full comment stripping (line, block, nested),
self-tested against prose that looks like a declaration before being trusted.*

### It invents nothing

**Zero phantoms across all 15 files.** Not one declaration is listed that does
not exist. Given how these summaries usually fail, that is the headline and it
should be said first: the document under-reports, it does not fabricate. Every
name in it is real, every name is spelled correctly, and the characterisations
attached to the theorems it did find are accurate.

It is also right about the two largest files. `TransferWord.lean` (20) and
`Characteristic.lean` (17) are complete, as are `ArtinSchreier.lean`,
`Ceiling.lean`, `GeneralCeiling.lean`, `Reflexive.lean` and `Schedules.lean` —
7 of 15 files perfect.

### The diff

| file | summary | actual | phantoms | dropped |
|---|---:|---:|---:|---|
| ArtinSchreier | 12 | 12 | 0 | — |
| Branch | 9 | 10 | 0 | `disc_is_squared_gap` |
| Casoratian | 5 | 8 | 0 | `casoratian_step`, `casoratian_unit`, `independent_forever` |
| Ceiling | 13 | 13 | 0 | — |
| Characteristic | 17 | 17 | 0 | — |
| GeneralCeiling | 7 | 7 | 0 | — |
| Golden | 9 | 10 | 0 | `nilpotent_forces_branch` |
| Modulus | 6 | 8 | 0 | `c_sum`, `c_prod` |
| Quadratic | 8 | 10 | 0 | `imaginary_forced`, `integral_solutions_are_real` |
| Reflexive | 6 | 6 | 0 | — |
| Schedules | 11 | 11 | 0 | — |
| Shape | 8 | 9 | 0 | `gap_eq_sum_iff` |
| TransferWord | 20 | 20 | 0 | — |
| Tropical | 3 | 5 | 0 | `tropical_unique`, `tropical_no_second_root` |
| Vieta | 1 | 4 | 0 | `sum_of_roots`, `product_of_roots`, `discriminant_is_gap` |
| **total** | **135** | **150** | **0** | **15 dropped = 10.0%** |

### What it drops is not random

The drops are not noise — they are disproportionately **the headline theorems**:

- `Vieta.lean` loses **all three** of its results. The file that establishes
  `x+y = 1` and `x·y = −G` — the two invariants the whole object is built on —
  is represented by a single declaration.
- `Modulus.lean` loses `c_sum` and `c_prod`, which are the *only* place the
  golden identity `φ + (−1/φ) = 1`, `φ · (−1/φ) = −1` is proved over ℂ. A reader
  of the summary would conclude that identity is unproved here. It is proved.
- `Golden.lean` loses `nilpotent_forces_branch` — the iff, and the strongest
  statement in the file.
- `Shape.lean` loses `gap_eq_sum_iff`, the reflexive-ladder result.
- `Tropical.lean` loses `tropical_unique`, which is the entire point of the file.

Positionally the drops sit at indices 0, 1, 2, 3, 4, 7, 8, 9 across the various
files — so no simple "misses the first" or "stops at a blank line" rule fits. The
common feature is more likely a multi-line statement or a preceding docstring
than a positional bug, but **I could not reproduce the extractor from the output
alone and am not going to guess at its source.** What is certain is the effect.

### Two files it describes that do not exist

The summary covers **35 files**. Fifteen are real. **Twenty are not present
anywhere reachable** — `CategoryGap`, `HomotopyGap` (×5 variants),
`ThermodynamicGap` (×4), `ToposGap`, `ModelGap`, `NoncommutativeGap`,
`CrossFrameworkTheorems`, `ShadowCastingObject`, `ShadowPatternTheorems`,
`ExplicitShadowCasting`, `InfiniteAscent`, `SuperCriticalPoint`,
`CategoryGap_Basic` — claiming **272 declarations** between them. Those are the
files the "Six Framework Convergence" rests on. This is bucket **[O]**: they may
exist somewhere we cannot see. But 272 of the 407 declarations the summary
describes — **two thirds of it** — cannot be checked from here.

It also omits `Cone.lean` entirely, which is fair: that file was written after
the summary.

### Verdict

Safe to circulate as *a partial index of names*. **Not safe to circulate as a
description of the corpus**, for one specific reason: it drops
`sum_of_roots`, `product_of_roots` and `discriminant_is_gap` — so a reader
using it to decide what has been proved would conclude the two Vieta invariants
are unproved, when they are the most securely proved things in the tree. The fix
is mechanical and worth doing, because the underlying tool is honest: it
under-reports by 10% and fabricates nothing, which is the right direction to
fail in.

---

## 3. A defect this diff turned up in *my own* instrument

Checking the counts above against `check.sh` produced a mismatch I could not
explain, and chasing it found a real hole. Recorded here because the SuperNinja
materials were being judged against these numbers.

`check.sh` matched only `theorem|lemma` while its header claimed it censused
"EVERY declaration". Planted probe:

```
file contains:   noncomputable def orphan : ℝ := sorry
lean says:       warning: declaration uses 'sorry'          EXIT=0
check.sh said:   1 declarations, 1 audited, sorryAx: 0      EXIT=0
```

A `sorry` inside a `def` that no theorem transitively depends on was invisible,
and `lean` itself exits 0 on `sorry` because it is only a *warning*. Two fixes,
deliberately independent:

1. the extractor now covers `def/abbrev/instance/structure/example`;
2. a separate gate now fails on lean's own `uses 'sorry'` warning — which does
   **not** depend on the extractor being complete, and catches anonymous
   declarations that have no name to probe.

Both fire on the planted probe now. Re-run over the real corpus: **zero `sorry`
warnings in all 16 files**, so nothing was ever hiding. But the published counts
were wrong — they were theorem counts labelled as declaration counts:

| | published | actual |
|---|---:|---:|
| `gap/lean/` | 66 | **87** |
| `gap/lean-mathlib/` | 41 (then 53) | **79** |
| total | 107 | **166 declarations, 166 audited, `sorryAx` 0** |

The conclusion never moved. What changed is that it is now established instead
of assumed — which is the whole distinction this workshop exists to maintain,
and I was on the wrong side of it while grading someone else's counts.
