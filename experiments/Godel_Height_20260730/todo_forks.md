# Forks 1 & 2 — Earn-the-label + Stress-the-flat-top

## FORK 1 — EARN THE LABEL (make M4 non-circular)
Problem: current M4 works because the generative paradox is HAND-BUILT as a
non-local singlet source. That is assuming what we want to test. Fix it.

- [x] fork1_earn_label.py
- [x] Generate correlation data from the SIMULATION's own dynamics, not an assumed singlet:
      two independent "auditor" probes read unit behaviour under two settings each;
      the paradox's effect on behaviour produces the +/-1 outcomes. No singlet hard-coded.
- [x] A frame-resolvable paradox: its effect is a FUNCTION OF EACH AUDITOR'S OWN SETTING
      (a shared local hidden state) -> correlations should factorize -> S <= 2.
- [x] A generative (self-amendment) paradox: its effect couples the two auditors'
      settings irreducibly (the amendment channel reacts to the JOINT probe) -> may break S>2.
- [x] Adversarial cases (red-team the discriminator):
      (a) a "signalling mimic": a resolvable paradox with strong but LOCAL correlation
          (should still be S<=2 -> not fooled)
      (b) a "noisy generative": generative but with detector noise -> does S degrade below 2?
      (c) a "confounded" pair: shared randomness that inflates correlation -> false positive?
- [x] Report the confusion matrix: does S recover labels when they are NOT hand-coded?
- [x] Figure: S per paradox with the S=2 line, colour = TRUE label, mark hits/misses.
- [x] HONESTLY report where it fails (this is the point of the fork).

## FORK 2 — STRESS THE FLAT TOP (cost-curve sweep)
Problem: M2's optimum is flat-topped (h=1 vs h=2 within noise) and h* depends on
the cost curve. Map the whole (cost) -> h* surface.

- [x] fork2_cost_sweep.py
- [x] Parameterise the cost curve: tier_cost(k) = coef * base**(k-1).
      Sweep coef in [tiny .. large] x base in [~1.1 .. ~2.5].
- [x] For each (coef, base): compute h* (survival-optimal height) over seeds.
- [x] Heatmap h*(coef, base): where does h* = 0,1,2,3,4,5? When does it EVER reach h_fix=5?
- [x] Identify the "climb-to-closure" regime: cheap + flat cost -> h* -> h_fix.
      Identify the "don't-bother" regime: expensive + steep -> h* = 0.
- [x] Line plot: h* vs coef at a few fixed bases, showing the staircase jumps.
- [x] Analytic overlay: predict jump locations from marginal value vs marginal cost, compare.
- [x] Report: is the flat top a knife-edge or a broad plateau? how sensitive is the headline?

## DELIVER
- [x] Extend Godel_Height_Report.md with a "Forks 1 & 2" section
- [x] Repackage zip
