# Section 10: quotient made real (opt 2) + phase law past Z2 (opt 1)

User asked for "2 and 1 please" after the section-9 phase diagram.

## Option 2 -- build the actual quotient TYPE (match the Lean's Quot)
- [x] cohomology_quotient.py: build H2 = Z2/B2 as a CONCRETE finite abelian group
      (element list, addition table, identity, inverses)
- [x] VERIFY abelian-group axioms on H2 (closure/assoc/id/inverse/comm) -- one
      config per section-9 phase. All PASS.
- [x] gauge map phi = d1 : C1 -> B2 proven a HOMOMORPHISM
      phi(f+g)=phi f+phi g ; phi(0)=0 ; phi(-f)=-phi f
      (= the Lean's gaugePhi_comp / gaugePhi_inv). True everywhere.
- [x] first iso |C1| = |ker phi| * |im phi| ; quotient |Z2| = |H2| * |B2|. Both hold.
- [x] anchor: Gaussian units Z4 trivial -> H2 = Z2 (constructed). fragile Z8 u=3 ->
      H2 = trivial group (quotient collapses to a POINT).

## Option 1 -- push past G=Z2 and past cyclic modules; find the next invariant
- [x] cohomology_general.py, ENGINE A: exact Tate H2 = M^G / Norm(M) for cyclic G
      of ANY order m (O(|M|), no cochain blow-up); H1 + Herbrand for context.
- [x] ENGINE B brute validation -- zero mismatches (incl. non-cyclic Z2xZ2).
- [x] Part 2: G = Z_p on Z_N for p=2,3,5.  FINDINGS:
        trivial-action law   |H2| = gcd(p,N)
        existence law        generative <=> p | N  (need p-torsion)
        fragility law        fragile once p-torsion is DEEP, threshold:
                             v_2 >= 3 (8|N) for p=2  BUT  v_p >= 2 (p^2|N) for odd p
                             => p=2 is EXCEPTIONAL (surprise, not predicted by s9)
- [x] Part 3: non-cyclic modules. FINDING: H2 acquires a RANK.
        Z2xZ2 trivial -> H2 = Z2xZ2 (rank-2 generative core);
        swap/shear collapse it to trivial (a rank DROP, not a bit toggle).
        scalar v_p replaced by p-rank of p-torsion modulated by the action.
- [x] fig23 (v_p three-panel phase law), fig24 (non-cyclic rank + collapse)
- [x] report Section 10 (10.1-10.6), literal-vs-analogy labeled, seams visible
- [x] Appendix updated; PDF regenerated (20 pages); HTML rebuilt; zip repackaged
