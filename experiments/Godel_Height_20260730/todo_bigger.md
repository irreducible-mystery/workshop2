# §14 — (1) bigger frame groups + (2) the full-collapse characterization

## Part 1 — push the resolution engine to a bigger frame-bundle
Generalize the tensor-product ZG-resolution from Z2xZ2 to Z2xZ2xZ2 and Z4xZ2.
Test whether the two §13 structural facts survive a bigger/mixed bundle.
- [x] A. Generic tensor-product resolution builder for G = product of cyclics.
      (cohomology_bigger.py: GroupRing + Resolution + GModule + H2.)
- [x] B. Verify d^2=0 for each G. (True for Z2xZ2, Z2xZ2xZ2, Z4xZ2.)
- [x] C. Cross-check trivial action vs LHS/Kunneth for each G. (ENGINE==LHS, 0 mismatches.)
- [x] D. Compute H^2 spectrum over actions (capped by |M|^{r_2}).
      (cohomology_bigger.json: full spectra for both new groups.)
- [x] E. Do facts (i),(ii) survive? YES — trivial maximizes rank (all 41 action-
      classes); floor > 0 persists. BONUS: §12 k=3 rank 6 upgraded ring->DIRECT.
      NEW: Z4-summand injection only when G has a Z4 direction.

## Part 2 — the full-collapse characterization (the standing OPEN item)
- [x] F. Assembled combined collapse dataset (8 modules, cyclic G=Z2 min-rank).
      (cohomology_collapse.json.)
- [x] G. Searched invariants. P1 (dim M[2] even) = 6/8 REFUTED as the invariant.
      P3 (even invariant factors pair by equal 2-adic exponent = symplectic form
      on M[2]) = 7/8.
- [x] H. Stated at supported confidence: P1 REFUTED; P3 = best candidate,
      CONJECTURED-AND-VERIFIED-ON-FAMILY (7/8); lone miss Z8 = §9 SEPARATE deep
      channel; two-channel (P3 or §9-deep) fits 8/8; unified law OPEN/no-proof.

## Deliverables
- [x] I. Figures fig31 (facts survive + collapse predictor), fig32 (torsion injection).
- [x] J. Report §14 written, Appendix updated, PDF+HTML rebuilt (23pp), zip. Ledger throughout.

## Honest bar — MET
Every H^2 number = exact ker/im of an integer matrix from a d^2=0-VERIFIED complex,
cross-checked vs LHS on every trivial action before trusting non-trivial ones.
Collapse characterization is CONJECTURED (P3 7/8 + two-channel), NOT proven; refuted
candidate (P1) listed; unified law OPEN.
