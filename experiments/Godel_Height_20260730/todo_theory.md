# §15 — turning §14's conjectures into theory (threads 1, 2, 3)

Standing bar: PROVEN means an actual argument (or a machine-checked exhaustive
finite verification of the exact hypothesis, clearly labelled). Everything else is
VERIFIED-ON-FAMILY / CONJECTURED / REFUTED / OPEN. Governance readings = analogy.

## OUTCOME (all three threads resolved; see §15 of the report)
- Thread 1: P3 provably SUFFICIENT (hyperbolic pairs, T1) but P3 and EVERY
  exponent-multiset predicate REFUTED as exact (T4, best 17/21, flip pairs).
- Thread 2: unified at the MECHANISM level (norm surjects onto fixed points);
  no closed multiset formula exists (proven negative).
- Thread 3: exp(H^2)|exp(G) PROVEN-EXHAUSTIVE for Z2 + cross-checked on all 28
  §14 engine spectra. Z4-core only at exp(G)=4.

## Thread 1 — PROVE P3 (the pair-up-the-2-torsion collapse invariant)
Claim to attack: for cyclic frame group G=Z2 acting on finite abelian M by an
involution u, H^2 collapses to 0 under SOME action iff the even invariant factors
of M pair up by equal 2-adic exponent (a nondegenerate alternating form on M[2]
the action can realize) — MODULO the separate §9 deep channel.
- [x] A. Write the exact Tate statement: H^2(Z2,M) = M^u / (1+u)M with the
      standard identification; collapse <=> (1+u)M = M^u for some involution u.
      Reduce to the 2-primary part M_2 (odd part is always rigid/irrelevant).
- [x] B. Prove the SUFFICIENCY direction on homocyclic pairs Z_{2^a} x Z_{2^a}:
      exhibit the involution u = swap (or hyperbolic pairing) that realizes
      (1+u)M = M^u, giving full collapse. This is the symplectic/hyperbolic plane.
- [x] C. Prove NECESSITY on a single cyclic 2-group Z_{2^a}: show NO involution
      collapses it for a in {1,2} (floor stays) — i.e. the unpaired factor is
      un-collapsible by the pairing channel. (a>=3 = the §9 deep channel, thread 2.)
- [x] D. Machine-check the exact algebraic claim (not just rank) exhaustively on
      all 2-groups up to a size cap: for each M enumerate ALL involutions u,
      test (1+u)M == M^u, confirm collapse-set == P3-or-deep prediction. This is
      the honest "PROVEN on a finite exhaustive family" fallback if the general
      proof has a gap.
- [x] E. State the result at the confidence reached: full proof, or proof of
      sufficiency + exhaustive-finite necessity, or refined conjecture.

## Thread 2 — UNIFY the two collapse channels
P3 (pairing) and §9-deep (v2>=3 valuation coincidence on a single generator) both
cause collapse. Find ONE invariant covering both.
- [x] F. Reframe both channels in one language: collapse <=> the involution u makes
      the NORM map (1+u) surject onto the fixed points M^u on the 2-primary part.
      Show P3-pairing and §9-deep are two ways the SAME surjectivity condition is met.
- [x] G. Test the unified predicate "exists involution u with (1+u)M_2 = (M_2)^u"
      against the FULL 8-module dataset AND the exhaustive 2-group sweep from D.
      Target: 8/8 and 100% on the sweep (vs P3's 7/8).
- [x] H. If it holds, state the unified law; note whether it extends to non-cyclic
      G=Z2xZ2 (use §13/§14 floor data as the test — does the analogous condition
      predict the §13 floors?). Mark clearly what stays cyclic-only.

## Thread 3 — the TORSION-INJECTION rule (general statement)
§14 observed: H^2(G,M) acquires a Z4 summand only when G has a Z4 direction; never
for elementary-abelian G. Find the general statement + a proof or exhaustive check.
- [x] I. Hypothesis: exponent(H^2(G,M)) divides exponent(G) (the frame group's
      exponent bounds the torsion of the core from ABOVE), and for TRIVIAL action
      the core is exactly killed by exp(G) [universal-coefficients/Bockstein].
      State precisely; separate the trivial-action theorem from the acting case.
- [x] J. PROVE the trivial-action direction: H^n(G,M) is annihilated by |G| (std),
      and for the core sharpen to exp(G) via the structure of H^*(G,Z). Cite the
      exact mechanism (transfer/restriction; exp(G)-torsion of reduced cohomology).
- [x] K. Exhaustively CHECK the acting case on the §14 engine data: for every
      (G,M,action) computed, verify exp(H^2) | exp(G). Report any violation.
- [x] L. State: PROVEN (trivial action, exp bound) + VERIFIED-ON-FAMILY (acting);
      the "only when G has a Z4 direction" phrasing = the exp(G) divisibility read
      in the elementary-abelian vs Z4 split.

## Deliverables
- [x] M. New code: cohomology_prove.py (exhaustive algebraic sweeps A–D,F–G,K),
      pure integer/exact, self-checking against the §14 engine where they overlap.
- [x] N. Figures: fig33 (P3 sufficiency=hyperbolic plane + necessity floors; the
      unified norm-surjectivity predicate 8/8), fig34 (torsion-injection: exp(H^2)
      | exp(G) scatter across all computed cases, elementary vs Z4 split).
- [x] O. Report §15, Appendix, PDF+HTML, zip. Strict ledger throughout.

## Honest bar
No claim of "proven" without an argument or an exhaustive finite check of the EXACT
predicate. Cross-check every new exact computation against the §14 resolution engine
on the overlap. Keep the refuted P1 and the OPEN unified-across-non-cyclic-G explicit.
