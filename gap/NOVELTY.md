# Novelty triage — is any of this new?

*Commissioned 2026-08-01 with the instruction that **the default hypothesis is
that all of this is classical**, and that an honest empty residue is a more
useful answer than a padded one. The agent was told to find citations or to say
plainly that it searched and found nothing.*

**The answer is no.** A working mathematician would find nothing here novel.
This file records why, with references, because knowing exactly *which* classical
result each sweep rediscovered is more useful than the sweep was.

One caveat on method: `WebFetch` was blocked by egress policy in this
environment, so citations come from search-result content rather than fetched
sources. They should be spot-checked before being relied on in anything public.

---

## The object has a name

`x² = x + G` is **de Spinadel's second metallic-means family** — the family
`x² − x − n = 0`. It is published, named, and studied. (de Spinadel, *The Family
of Metallic Means*; Gil & Worley, *Generalized metallic means*,
arXiv:1901.02619.) The sweep was exploring a named object without knowing its
name.

---

## Bucket table

**[T]** textbook/classical · **[K]** known, less standard, sourceable ·
**[?]** searched, not found

| result | | citation |
|---|---|---|
| Vieta: sum = 1, product = −G, `(x−y)² = 1+4G` | **[T]** | Vieta's formulas; metallic-means literature above |
| Discriminant vanishes at `G = −1/4`, double root exactly `1/2` | **[T]** | Quadratic formula. Also literally the Mandelbrot statement: `f_{1/4}` has a fixed point of multiplier 1 at `z = 1/2` |
| `G = 1` → golden ratio; `φ+ψ=1`, `φψ=−1` | **[T]** | Standard |
| Monodromy at the branch point is `Z/2` and exchanges the roots | **[T]** | Monodromy of `√z`; equivalently `Gal(ℚ(√d)/ℚ) ≅ Z/2`. Forster §1, Ahlfors ch. 8 |
| `A² − A ≥ −1/4` for self-adjoint `A`, sharp at `A = 1/2` | **[T]** | One line: `A²−A+¼ = (A−½)² ≥ 0`. Reed–Simon I, Thm VII.1 |
| Nilpotent (dual-number) solution exists iff `G = −1/4` | **[T]** | `R[x]/(f)` étale ⟺ disc is a unit; `Spec k[ε]/(ε²)` points = tangent vectors. Hartshorne Ex. II.2.8; Milne, *Étale Cohomology* I §3 |
| Indicial equation of `r²u″ = Gu`; `v″ = (G+¼)v`; log born at `−¼` | **[T]** | Frobenius method, repeated indicial root ⇒ log. **And it is the same 1/4 as Kneser (1893)** — `y″+qy=0` with `x²q → c` is oscillatory for `c > 1/4`, non-oscillatory for `c ≤ 1/4` — **and as the Hardy inequality constant.** Three "independent" appearances in the sweep are one theorem |
| Mandelbrot cusp at `c = 1/4`; logistic window | **[T]** | `z²+c = z ⟺ z²−z+c = 0`, disc `1−4c`. Note `c = −G` exactly — the sweep's "two different objects" are one substitution apart |
| Catalan GF is a root; radius `1/4` | **[T]** | `C(z) = (1−√(1−4z))/(2z)`; `zC(z) = s₋(−z)`. Flajolet–Sedgewick §VI; Stanley *EC2* ch. 6; OEIS A000108 |
| `\|f_n\| ≤ F_{n+2}` under any `\|g_n\| ≤ 1` | **[T]** | Triangle inequality + induction. The literature has it sharper: random Fibonacci values lie in `[−F_{n−3}, F_n]` |
| char 2 → additive (Artin–Schreier); branch point → parity | **[T]** | `℘(x) = x²+x` is `F₂`-linear with kernel `F₂`. Lang *Algebra* VI §6; Serre *Local Fields* |
| Solution sphere dim `2ⁿ−2`; conjugation outer over ℂ, inner over ℍ | **[T]** | Square roots of −1 in ℍ = `S²` (Niven 1941; Eilenberg–Niven 1944); in 𝕆 it is `S⁶` with `G₂` transitive (Baez, *The Octonions*). **"Inner over ℍ" is Skolem–Noether** — ℍ is central simple over ℝ, so every automorphism is inner |
| Viswanath's constant `1.13198824` | **[T]** | Viswanath, Math. Comp. 69 (2000) 1131–1155 |
| "Three growth rates for one system" (1, 1.131988, 1.272020) | **[T]** | These are the *p*-radii: `p=+∞` → JSR, `p=0` → Lyapunov, `p=−∞` → subradius. Jungers & Protasov, arXiv:1905.00749. `1.272020 = √φ` |
| char 5: golden gap *is* the critical gap | **[T]** | 5 ramifies in `ℚ(√5)` |
| Max-plus: exactly one root for every gap | **[K]/[?]** | Framework standard (Butkovič, *Max-algebra primer*; Speyer–Sturmfels). **The specific two-line instance: searched, not found.** Not-written-down, not not-known |
| JSR `= s₊(\|G\|)`, subradius `= \|s₊(−\|G\|)\|` | **[K]**, and see below | Machinery textbook (Guglielmi–Protasov antinorms); this family's closed form not found published |
| The unified cross-system sweep *as an object* | **[?]** | The pieces are scattered across metallic-means, quaternion-algebra, tropical and finite-field literatures. One place containing all of them: not found |

---

## The one item that mattered, and what happened to it

The ceiling/floor result was flagged as the only candidate with real content. Two
findings came back.

**It was false as stated.** `{T(+G), T(−G)}` is the same set for `G` and `−G`, so
every invariant must be even in `G`; the claimed formulas are not even, and for
`G < 0` they are exactly swapped. Fixed to `|G|` throughout; entered as `I1` in
`FAILURES.md`.

**For `G ≥ 0` it is true and both halves are short.** Ceiling: entrywise
`|T(−G)| = T(G) ≥ 0`, `|AB| ≤ |A||B|`, and spectral radius is monotone on
nonnegative matrices — so the maximizing product has length 1 and the finiteness
property holds trivially. Floor: above `1/4` it is `√|det|`; below, the common
invariant cone gives it, which is the antinorm method.

**Context for why "short" matters here.** The general 2×2 problem is genuinely
hard, and this family sits nowhere near the hard part:

- The Lagarias–Wang **finiteness conjecture is false** — Bousch & Mairesse,
  J. Amer. Math. Soc. 15 (2002) 77–111; first explicit counterexample Hare,
  Morris, Sidorov & Theys, Adv. Math. 226 (2011).
- Blondel & Tsitsiklis: boundedness of products of a matrix pair is
  **undecidable**; JSR approximation is NP-hard; deciding whether the
  **subradius is zero is undecidable**.
- The lower spectral radius is **discontinuous** on a positive-measure set —
  Bochi & Morris, arXiv:1309.0319.
- Positive results where structure helps: Morris & Sidorov (devil's staircase,
  J. EMS 2013); Jenkinson & Pollicott (ETDS 2018); Laskawiec, Lin. Alg. Appl.
  719 (2025) 103–135, which covers **all pairs of non-negative matrices**;
  Kozyakin's hourglass alternative (LAA 2016).

This family has a nonnegative dominating matrix, a common invariant cone, and
both extremal products of length 1. It is in the easy region and is not a
counterexample to anything.

---

## The residue

Two items, and **neither is a theorem**:

1. The specific max-plus statement — a two-line case split, apparently
   unwritten.
2. The explicit closed-form (JSR, subradius) pair for this family — apparently
   unpublished, but derivable in ten lines by standard technique, and a referee
   would call it an exercise.

And two things that are **not** in the residue and belong in the record as
negatives:

- The `G < 0` sign error.
- **The corpus's central claim — "−1/4 is where the discriminant vanishes, and
  every number system reports it differently" — is a restatement of the
  definition of the discriminant, observed in fifteen places.** The fifteen
  dialects are real and the observation that they are all the same thing is
  correct. It is not a discovery; it is what a discriminant *is*.

---

## What this leaves

The honest positive statement, in the triage's own words: *no, nothing here is
novel mathematics, but the systematic cross-system sweep is a reasonable
expository object.* A short, well-cited note — "one quadratic, fifteen rooms:
where `x² = x + G` loses its two roots" — would be a pleasant piece of
exposition, because the unified sweep across ℝ, ℂ, ℍ, 𝕆, 𝕊, `F_p`, char 2, dual
numbers, tropical and *p*-adic does not appear to exist in one place.

It would have to be written with citations rather than claims of discovery, with
the `G < 0` error fixed, and with `gap/README.md`'s "Nothing here is proved"
extended to **"and nearly all of it already was."**

That is a real thing to have. It is much smaller than what anyone hoped for, and
it is not nothing.
