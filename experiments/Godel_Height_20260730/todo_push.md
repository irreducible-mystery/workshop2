# Section 11: keep pushing the math (tracking what can/cannot be claimed)

User: "keep pushing the math (remembering to note what cannot prove/claim yet
(or ever), may be important eventually, may not :)"

## Push 1 -- PROVE the rank-drop law (make section-10 sampling exhaustive)
- [x] cohomology_rank_law.py: exact Tate H2 + enumerate ALL order-2 automorphisms
      of a module (not a sample). Fixed a homomorphism-check (matrix must be a
      genuine module endomorphism: n_j*mat[i][j] == 0 mod n_i).
- [x] Fixed invariant-factor decomposition bug (phantom Z2 factors) via primary
      decomposition from element-order statistics; caught by FACT A cross-check.
- [x] PROVEN: trivial-action H2(Z2,M) = M/2M = M[2]; rank = dim_F2 M[2]. (theorem)
- [x] VERIFIED-ON-FAMILY: full rank ladder; Z4xZ4 realizes ranks 0,1,2 (28 actions).
- [x] REFUTED: "some frame-change always fully collapses the core" is FALSE --
      Z2xZ4 and Z2^3 never fully collapse (min |H2|=2). => adversary has no total
      win against those value grains (a robustness result).
- [x] OPEN (flagged): which 2-groups admit a full collapse; both natural
      conjectures (homocyclic / deep factor) refuted.

## Push 2 -- non-cyclic FRAME groups via LHS (the expected break)
- [x] cohomology_lhs.py: G=Z2xZ2 (no Tate). DIRECT cochain enumeration CAPPED at
      |M|<=2 (|M|^16 blow-up honestly avoided) + LHS/ring prediction.
- [x] PROVEN/CROSS-CHECKED: H2(Z2xZ2, Z2) = (Z2)^3 rank 3, DIRECT == LHS
      (H*(Z2xZ2,F2)=F2[x,y], dim H2 = 3). vs rank 1 for cyclic Z2, Z4.
- [x] => section-9 single-invariant (v2) law is a CYCLIC-G ARTIFACT. Non-cyclic
      frame group multiplies generative rank (3r per F2-generator).
- [x] NOT CLAIMED: r>=2 non-cyclic ranks (only LHS-predicted, 2^{3r}, DIRECT would
      need 4^16 cochains); non-trivial Z2xZ2 actions.

## Wrap
- [x] fig25 (rank ladder + refuted collapse), fig26 (cyclic vs non-cyclic rank)
- [x] report Section 11 with an explicit PROVEN / VERIFIED / REFUTED / OPEN ledger
- [x] Appendix updated; PDF (23 pages); HTML rebuilt; zip repackaged

## Standing open threads (may matter eventually, may not)
- non-cyclic frame-group phase law (classification) -- OPEN, may have no tidy form
- full-collapse characterization for 2-groups -- OPEN
- deferred: prose/dialectic artifact folding the whole arc together
- ALWAYS: governance reading stays ANALOGY; the paradox<->cochain bridge is
  unearned on real institutional data (true of every section).
