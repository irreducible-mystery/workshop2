# §13 — Non-trivial actions on non-cyclic frame group Z2xZ2, via ZG-resolution  [COMPLETE]

Side-question answer (recorded in §13 intro): LHS is NOT the only route.
  (1) direct enum  -- blocked (4^16 wall)
  (2) LHS          -- valid but hides d2 differentials + extensions for nontrivial action
  (3) explicit ZG-resolution + exact ker/im  <-- USED (poly cost, self-checking)
  (4) minimal F2-resolution -- trivial coeffs only

## Plan
- [x] A. ZG for G=Z2xZ2; left-mult operators (s-1),(s+1),(t-1),(t+1).
- [x] B. Tensor-product resolution P0<-P1<-P2<-P3; VERIFIED d^2=0, eps d1=0.
- [x] C. Hom(-,M) -> cochain complex; H2=ker(delta2)/im(delta1) EXACT finite quotient.
- [x] D. CROSS-CHECK trivial action THREE ways (resolution = LHS/Kunneth =
      independent bar enum): Z2->8=(Z2)^3, Z4->8, Z2xZ2->64. All agree. Engine trusted.
      (Caught+fixed a baseline-LABEL bug on Z2xZ4; spectrum was always correct.)
- [x] E. NEW RESULT: full H2 rank spectrum of Z2xZ2 acting on Z4, Z2xZ2, Z2xZ4,
      Z4xZ4 over EVERY commuting order-<=2 action pair.
- [x] F. Ledger PROVEN/VERIFIED-ON-FAMILY/OPEN.
- [x] G. fig29 (three-method agreement), fig30 (nontrivial rank spectrum).
- [x] H. Report §13 (13.1-13.3), Appendix, PDF (27pp) + HTML, zip.

## Headline results (reproduced, all past the 4^16 wall)
- Engine validated: resolution == LHS == bar enum on trivial action.
- Z4        : trivial rank 3; ALL actions rank 3 (rigid, cannot move).
- Z2xZ2     : trivial rank 6; 9/10 actions collapse to rank 1 (brittle).
- Z2xZ4     : trivial rank 6; drops to 4 or 3, FLOOR 3 (partial).
- Z4xZ4     : trivial rank 6; full ladder 1,2,3,4,6 over 400 actions.
- TWO structural facts (all modules): (i) trivial action MAXIMIZES rank — no
  non-trivial action ever exceeds it; (ii) module-dependent FLOOR — some modules
  keep an irreducible generative remainder no acting bundle can gauge away.

## Still OPEN (may matter eventually, may not)
- Frame groups G beyond Z2xZ2 (each needs its own resolution).
- Closed formula for H2(Z2xZ2, M, action) over ALL finite M / all actions
  (Z4xZ4 ladder suggestive, not proven).
- [inherited] which 2-groups admit a fully-collapsing action (now with the
  non-cyclic floor phenomenon as new data toward it).
