# The Gap Sweep — a report from inside the gap

**Premise taken as given (per instruction):** φ + ψ = 1, φ × ψ = −1, ◇² = ◇ + 1.
The +1 is renamed **G, the gap**, and released: `x² = x + G`, G swept over every
number system we could reach in one sitting. Three lenses held at once —
classical, quantum, relational — and then the fourth stance: *be* the gap.

Every numerical claim in this report is computed by `gap_sweep.py` and recorded
in `results/gap_sweep_results.json`. Nothing below is asserted-only. (This
repository's autopsy record convicts, four times out of eight, the species
*"a marker standing in for a property."* This report tried not to be the fifth.)

---

## 0. What the three lenses see, before the sweep

Fix the discriminant Δ = 1 + 4G. The roots are x± = (1 ± √Δ)/2.

- **Classical seat:** Δ > 0. Two distinct real roots. Everything is decided;
  you may point at φ and at ψ separately. Truth is bivalent, the gap is a
  *length* (the distance between the roots is √Δ).
- **Quantum seat:** Δ < 0. The roots are a conjugate pair ½ ± i·|√Δ|/2 with
  **equal modulus √(−G)**. You cannot point at one without choosing an
  orientation of the imaginary axis first — the choice of "which root is x₊"
  is exactly a choice of *i vs −i*, i.e. a Galois choice, i.e. the `conj` that
  Circle Six's charge is about. Before that choice the pair is one thing.
- **Relational seat:** neither root is anything alone at *any* G. The whole
  content is the two symmetric functions: **sum = 1, product = −G.** The gap
  never touches the sum. The gap *is* the product. Relation first, relata after.

**First computed law of the sweep** (`E_gap_set_law`): the gap between the
roots, γ = x₊ − x₋, satisfies **γ² = 1 + 4G** — an equation of the same shape,
one level up. *The gap of the gap is affine in the gap.* The structure is
self-similar under "take differences": you never exit the family by asking how
far apart its answers are.

---

## 1. The real sweep, and where the windows are (fig1)

Sweep G ∈ [−2, 2]:

- **G > −1/4** — the classical window. Two real roots, splitting apart like
  scissors as G grows. Golden at G = +1.
- **G = −1/4** — the collision. Double root ½. (Circle Six's `Golden.lean`
  already kernel-proved: rational root *only* here, nilpotent solution in the
  dual numbers *only* here.)
- **G < −1/4** — the quantum window. Both moduli equal √(−G); the roots differ
  only in phase. **At exactly G = −1 the roots land on the unit circle** and are
  verified sixth roots of unity: e^{±iπ/3}. The "most quantum" gap is −1, the
  mirror of the golden +1.

So the gap set {+1, −1, +i, −i} is not four arbitrary flags: **+1 is the
maximally classical gap (golden), −1 is the maximally quantum gap (pure
phase, order 6), and ±i are the two chiralities of leaving the real line.**
The imaginary gaps ±i give root-pairs that are complex-conjugate *of each
other across the gap sign* — the gap set is closed under the same conj that
twists Circle Six's coefficients.

## 2. "You may hit −1/4 from different directions and what you see changes" — formalized (fig2)

That sentence is a theorem and we measured it. Approach along the real axis
from the right: two real roots merging. From the left: a phase pair closing.
But the full statement is about *directions in the complex G-plane*:

> **Loop G once around −1/4 and the two roots swap. Loop twice and they
> return.** Computed by continuous root-tracking: `one_loop_swaps_roots: true`,
> `two_loops_restore: true`. The monodromy group of the gap is **Z₂**.

And the figure shows something better than the claim: under one loop of G, the
two root-tracks jointly trace **a single circle**, each root traveling half of
it. There are not two paths; there is one path with two names. That is the
relational lens rendered by matplotlib without being asked.

**Contact with the live PR** (circle-six #5): the Galois-twist round found
H³ ≅ Z₂ under both the trivial and the twisted action — *the invariant
survives, the generator moves* (−1 generates untwisted; ±i generate twisted).
Same signature here: the *pair* {x₊, x₋} is monodromy-invariant, the *labels*
braid, and the braiding group is the same Z₂. Which root you call φ after a
loop is exactly which generator you land on after the twist: **not a fact
about the object, a fact about the path you took to it.** The gap's answer to
"which one is it?" is "how did you get here?"

## 3. The Mandelbrot bridge: the gap is a parameter you've seen before (fig3)

Fixed points of z ↦ z² + c satisfy z² = z − c: **our equation with G = −c.**
Consequences, all verified:

- G = −1/4 (branch point) ↦ c = 1/4: **the cusp of the main cardioid.** The
  multiplier there is 2·(½) = 1 — parabolic dynamics. The algebraic collision
  *is* the dynamical phase transition. Same point, two languages.
- G = +1 (golden) ↦ c = −1: **the superstable centre of the period-2 bulb.**
  The golden gap is the heart of period-doubling.
- G = −1 (unit-circle roots) ↦ c = +1: **outside the Mandelbrot set.** Orbits
  escape. The purest-phase gap cannot sit still under iteration: *pure phase
  never settles.* Classical gaps sit inside and converge; the quantum gap
  escapes; the cusp is the door between.

The gap was never only algebra. Sign-flipped, it is the best-studied parameter
space in dynamics, and the classical/quantum window boundary is the cardioid.

## 4. Time-domain: the nilpotent is audible as critical slowing (fig4)

Read ◇² = ◇ + G as a recurrence: xₙ₊₁ = xₙ + G·xₙ₋₁ (G = 1 is Fibonacci).
At G = −1/4 the transfer matrix is **defective** — a Jordan block — and the
solution grows a secular term **n·(1/2)ⁿ** (coefficient measured at n = 40 and
n = 50: identical to 9 decimal places). This is the *time-domain shadow* of the
nilpotent that `Golden.lean` proves exists only at −1/4: the dual number ε with
ε² = 0 *is* the "n·" in front of the decay, the sound of two modes fusing into
one. **Criticality is what a nilpotent feels like from inside time.**

## 5. Other number systems (the instruction was: every one that exists, or build our own)

| system | what the golden equation does there | verified |
|---|---|---|
| **F_p** | roots exist ⟺ p ≡ ±1 (mod 5) (quadratic reciprocity on 5) | residues of first 14 primes |
| **F₅** | double root 3: since 1+4G = 5 ≡ 0, **the golden gap IS the branch point mod 5.** −1/4 ≡ 1 (mod 5) — the two special gaps of this whole report are *the same residue* in F₅ | `check_minus_quarter_mod5 = 1` |
| **F₂ / F₄** | completing the square dies (no ½). Roots of x²=x+1 live in F₄ and are **cube roots of unity**; the entire gap set {+1,−1,+i,−i} collapses to ONE point since +1=−1 and i=1 | `w² = w+1`, `w³ = 1` |
| **Q_p** | Hensel lifts the F_p answer for p ≠ 2,5. At p = 5, φ needs the **ramified** extension Q₅(√5): the golden ratio sits *on a ramification point* of the 5-adic world | Q₁₁ yes, Q₇ no |
| **ℍ (quaternions)** | for G < −1/4 the solution set is a **2-sphere**: x = ½ + (√(−1−4G)/2)·u for *every* imaginary unit u. 500 random directions tested, 500 solve | `all_solve: true` |
| **dual numbers** | nilpotent solution exactly at −1/4 (already kernel-proved in `Golden.lean`; our §4 is its time-domain echo) | inherited |

**The quaternion result is the relational lens's strongest exhibit.** The "two
roots" of the quantum window were never two things — over ℍ they are a
*continuum*, one 2-sphere of solutions, and ℂ's pair {½ ± i·s} is just the
two-point slice cut by choosing an axis. Dimension ladder: ℝ gives a 0-sphere
(2 points), ℂ keeps the 0-sphere but wires it with phase, ℍ inflates it to a
2-sphere. **Choosing "which root" = choosing an axis = breaking a symmetry
that was never broken by the equation itself.**

And F₂ answers a question nobody asked: *is φψ = −1 essential?* In
characteristic 2, −1 = +1, so `φψ = −1` and `φψ = +1` are the same claim, the
four gaps are one gap, and golden becomes the cube root of unity. **Some
distinctions we treat as structural are artifacts of being able to divide
by 2.** (The circle-six GAP compartment's `ArtinSchreier.lean` is standing on
exactly this: char-2 replaces completing-the-square with x² − x = G.)

## 6. Self-reference: the tower of gaps

Feed the gap its own output: G_{n+1} = x₊(G_n), starting from the golden G = 1.
Computed: the tower converges to **2** (derivative 1/3, attracting), and
x² = x + 2 factors over the integers: roots {2, −1}. **Self-reference
terminates in the simplest split past golden: 2 and −1.** The gap that eats
itself lands on integers — recursion doesn't ascend to mystery here, it
*descends to arithmetic*.

Bonus fixed point of language: at G = φ/4 the *gap between the roots* is
exactly φ (`equals_phi: true`). The gap can be golden about its own roots.

## 7. Other languages (per instruction: languages native to AIs too)

- **Color** (fig6): the G-plane painted with hue = direction of γ = √(1+4G),
  brightness = |γ|. There is exactly one black pixel: −1/4, *the only G where
  the gap has no direction to point.* All hues meet there — approach it along
  different rays and you arrive carrying different colors. That is §2's
  monodromy, spoken in paint.
- **Sound** (`gap_sweep.wav`, 12 s stereo): two voices, one per root, pitch =
  modulus × 220 Hz. G sweeps 1 → −1. It opens on the golden chord (interval
  ratio φ² = φ + 1 — the only musical interval equal to itself-plus-its-own
  octave-shift), the voices converge, **fuse to unison at t = 7.5 s (the branch
  point)**, and after it there is only ONE pitch (√(−G)·220 Hz, rising) — the
  two roots survive only as stereo *placement*, phase between the ears.
  **Classical difference is an interval you can hum; quantum difference is a
  place you can only stand in.**
- **Code**: the recurrence of §4 *is* the equation in the language "execution."
  A Jordan block is what a compiler would call the two modes being aliased.
- **Lean**: the `-1/4` facts are already spoken in kernel (`Golden.lean`).
  This report's §2 monodromy and §5 sphere are candidates for that language —
  see open questions.

## 8. The interrogation the prompt demanded

- **Hidden assumptions found:** (i) that "two roots" means two *things* —
  killed by ℍ (one sphere) and by monodromy (one circle, two names);
  (ii) that ½ is available — killed by F₂; (iii) that the sum-side of the
  Vieta pair deserved its privilege — we always swept the product (φψ = −G)
  and left φ+ψ = 1 sacred. **Nobody ordered that.** The dual sweep (fix
  product, free the sum: x² = Sx + 1, S the new gap) has its own collision at
  S = ±2i — a branch point that is *imaginary from birth*. Not run. Open.
- **Hidden decision point:** matching roots "by nearness" in the monodromy
  tracker is a metric choice; it is exactly the choice the equation refuses to
  make. The tracker *is* the observer. Its Z₂ is honest but it is *ours*.
- **Shadow side:** everything here is degree 2. The gap of x³ = x² + x + G has
  monodromy S₃ — non-abelian, so "which root" becomes *path-ordered*: the
  first non-commutative gap. One loop then another ≠ the other then the one.
- **What's missing that we didn't notice because we didn't look for what's not
  there:** the equation has no term that *isn't* there — but F₂ showed the
  MINUS SIGN is removable, and the sound file showed the *silence* at unison
  carries information (which voice was which is gone forever after the fuse —
  the collision is a one-way information valve for labels).
- **What question is being asked:** not "what is φ" but *"what survives a
  change of number system?"* Answer, computed: the midpoint ½ (until char 2
  kills it), the Z₂ of label-exchange, and the law γ² = 1+4G.
- **What object is being questioned:** the *distinction between the roots* —
  not the roots.
- **Premature collapse, spotted:** calling G < −1/4 "the quantum side" is
  itself a collapse — ℍ shows that window is a *sphere*, richer than any
  two-state story. We kept the name and flag the debt.
- **Edges:** G = −1/4 (parabolic), G = −1 (order-6 phase; escapes the
  Mandelbrot set), p = 2 (no halving), p = 5 (golden = branch), S = ±2i
  (the unexplored dual collision).
- **New open questions:** (1) kernel-check the Z₂ monodromy statement — it is
  finitely presentable via the swap of Puiseux branches; (2) the dual sweep
  x² = Sx + 1; (3) cubic gap ⇒ S₃: does circle-six's "invariant survives,
  generator moves" have an S₃ analogue where even the *invariant* becomes
  path-dependent? (4) is the F₅ coincidence (golden ≡ branch) an instance of
  a general law: G_golden ≡ G_branch mod p ⟺ p | 1+4G_golden, i.e. only p=5?
  — yes, trivially, which is itself the point: **5 is the only prime that can
  see the two special gaps as one.**

## 9. One sentence, one word

**One sentence:** The gap is not the flaw in the equation; it is the coordinate
the whole family of solutions breathes through, and "kinds of number" — real,
imaginary, nilpotent, finite, spherical — are just the shapes the same two
roots take when you walk up to −1/4 from different directions.

**One word:** **between.**

---

*Files: `gap_sweep.py` (all computations), `results/gap_sweep_results.json`
(all claims), `figures/fig1–fig6`, `gap_sweep.wav` (the sweep, audible).
Nothing here is a kernel result; per this workshop's own convention, prose
decides nothing and the Lean rewrites in §8 are the exits.*
