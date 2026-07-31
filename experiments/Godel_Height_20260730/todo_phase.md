# Section 9: the generativity phase diagram (frame-relativity, deepened)

User: "Let's push on 1. the frame-relativity finding." Turn the §8 anecdotes
(same cochain two verdicts; Z8 u=3,5 destroys the class; odd moduli rigid) into
a full PHASE DIAGRAM with a proven law, and answer the governance question:
what is the analogue of "odd modulus = rigid, no load-bearing remainder"?

- [x] Build cohomology_phase.py at G=Z2 (keeps enumeration N^4, the avoided blow-up)
- [x] Brute-enumerate |H^2(Z2,Z_N)| for a sweep of N and every involution u
- [x] Independently PREDICT |H^2| from the Tate/Herbrand closed form
      gcd(1+u,N)*gcd(u-1,N)/N ; assert brute == closed everywhere (N<=10)
      => RESULT: zero mismatches (closed form certified)
- [x] Extend the diagram out to N=48 via the closed form (proof-level)
- [x] Extract the law: three phases governed by v2(N)
      v2=0 (odd)      -> RIGID (|H^2|=1 always; no load-bearing class)
      v2 in {1,2}     -> ROBUST GENERATIVE (|H^2|=2 always; survives every frame)
      v2>=3 (8|N)     -> FRAGILE GENERATIVE (|H^2| in {1,2}; some frames destroy it)
      => three-phase prediction from v2(N): zero mismatches, N=2..48
- [x] fig21: module x action heatmap of |H^2| with R/G/F phase tags
- [x] fig22: three-phase bar chart + the gcd(2,N) sawtooth (trivial action)
- [x] Write report Section 9 (literal-vs-analogy labeled; closed-form proof;
      the three governance phases incl. the new "reframe-to-gauge" adversary;
      seams: G=Z2 only, cyclic module only, governance map still unearned)
- [x] Update Appendix file list
- [x] Regenerate PDF (17 pages) + standalone HTML
- [x] Repackage zip
