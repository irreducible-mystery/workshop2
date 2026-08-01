# Complex / imaginary extension — "climb anyway", the quadratic, and −1/4

## The invitation (my reading)
- Thread 1 called back-loaded harm "un-governable" because a GREEDY, REAL, contiguous
  climb never starts (early rungs have negative net value). That is a claim about the
  DECISION RULE and the NUMBER SYSTEM, not the world.
- "What if you climb anyway?" -> the greedy stop is a LOCAL trap; a negative-value rung
  can be a BRIDGE (barrier) to a deep payoff. Global vs myopic optimum. Barrier crossing.
- The −1/4 clue = quadratic vertex/discriminant + the z->z^2+c bifurcation:
    * min of x^2+x is −1/4 at x=−1/2 (additive/vertex view)
    * roots of x^2+x+c: real for c<=1/4, COMPLEX for c>1/4 (discriminant crosses 0)
    * z->z^2+c: attracting real fixed point for c in [−3/4? , 1/4]; c=1/4 is the
      tangent/fold bifurcation where two real fixed points COLLIDE and go complex.
    * "approach −1/4 from −1/2 vs from 1": path/branch matters -> branch point / Riemann sheet.
- Perspectives to hold at once:
    * CLASSICAL: real cost accounting; greedy fails; but GLOBAL (non-greedy) may win by
      crossing the valley. Also: complex ROOTS = oscillation/overshoot in the real dynamics.
    * QUANTUM: classically forbidden barrier crossed with IMAGINARY momentum (tunneling);
      evanescent decay exp(-kappa x); WKB action becomes imaginary under the barrier.
    * COMPLEX-ANALYTIC / AC-power: reactive (imaginary) power moves real power past a
      barrier; impedance Z = R + iX; you pay |Z| but only R dissipates.

## PART A — MODEL (note + deterministic checks)
- [x] complex_note.md: reframe governable-height as a COMPLEX optimization / barrier problem.
- [x] Formalize: net-value profile v(k) along the climb; greedy stop = first k with prefix
      sum turning down; GLOBAL optimum = argmax of cumulative V(k) allowing valleys.
- [x] The quadratic dictionary: cumulative value V(h) ~ quadratic in h; vertex = −1/4-type
      min; discriminant sign = "is there a real height that breaks even?" complex roots =
      "no real break-even; the payoff is reached only by tunneling / oscillatory overshoot."
- [x] checks_complex.py:
    * (C1) greedy vs global optimum on a back-loaded profile: greedy=0, global=deep. SHOW the gap.
    * (C2) discriminant law: sweep barrier depth; find c* where real break-even roots go complex;
      verify at c* the two real roots collide (== the −1/4 fold), matching x^2+x+c.
    * (C3) path-dependence: continue the root x(c) as c passes the branch point from two
      directions (from −1/2 side vs from +1 side); show the two analytic continuations land on
      DIFFERENT Riemann sheets (conjugate roots) -> "direction of approach matters."
    * (C4) tunneling action: WKB-style integral of sqrt(barrier) becomes IMAGINARY under the
      barrier; the "tunneling amplitude" exp(-|imag action|) = probability the climb pays off.

## PART B — SIMULATION (extend the sandbox)
- [x] complex_climb_sim.py: institution that may CLIMB ANYWAY through a value-valley.
    * real greedy climber (stops at valley) vs GLOBAL/commit climber (crosses) vs
      QUANTUM/tunneling climber (crosses with probability = tunneling amplitude, pays
      imaginary/reactive cost = volatility/trust drawdown while under the barrier).
    * back-loaded lattice from Thread 1 as the test bed (the "un-governable" case).
    * measure: does crossing pay? distribution of outcomes; the reactive cost paid; ruin risk.
    * the QUANTUM reading: sometimes you should commit through a locally-losing reform because
      the deep payoff is real; the imaginary cost is the drawdown you must survive to get there.
- [x] Figures: (1) cumulative value with a valley + greedy-stop vs global-opt; (2) discriminant
      /root-locus: real roots colliding at −1/4 and going complex (the classic parabola->complex);
      (3) tunneling amplitude vs barrier depth/width; (4) sim outcomes: greedy vs commit vs tunnel.

## PART C — REPORT
- [x] Extend report with §7 "Complex heights: climbing anyway, and when the payoff is imaginary"
- [x] Be honest: complex numbers here are (i) literal for oscillatory root dynamics, (ii) a rigorous
      analogy for tunneling/reactive cost. Say which is which. Where it's metaphor, label it.
- [x] Repackage.
