# Threads 1 & 2 — Lattice density × dead tiers,  and a noise-robust generative test

## THREAD 1 — GENERALIZE THE DEAD-TIER FINDING (lattice density -> governable height)
Claim to test: the DISTRIBUTION of paradox dissolution-levels (lattice density)
systematically sets how high it pays to climb. Gaps ("dead tiers") cap the
contiguous climb; density raises it. Quantify.

- [x] thread1_lattice_density.py
- [x] Parameterise a lattice by density rho in (0,1]: prob that each height 1..L
      has >=1 resolvable paradox. Also vary total harm budget + how harm is spread.
- [x] For each sampled lattice: compute h_reach (contiguous cap set by first dead tier),
      h_econ (economic stop under a fixed cost curve), h* (survival-optimal, Monte-Carlo).
- [x] Sweep rho; show E[h_reach], E[h_econ], E[h*] vs rho. Predict: all rise with rho,
      but h_econ <= h_reach always, and gaps bite hardest at low rho.
- [x] "Dead-tier probability" analytic: P(first gap at k) and E[h_reach] closed form; overlay.
- [x] Second axis: HARM PROFILE (front-loaded vs flat vs back-loaded). Show back-loaded
      harm is un-governable-deep (you must pay through cheap-value rungs to reach the payoff).
- [x] Figures: (1) E[h] vs density with 3 curves + analytic; (2) heatmap h* over
      (density, harm-skew); (3) governable-height distribution at a few densities.
- [x] Honest failure section: where the contiguous-climb assumption is the wrong model.

## THREAD 2 — NOISE-ROBUST GENERATIVE TEST (beat Fork 1's p* ~ 8%)
Fork 1's CHSH died at 8% detector noise, failing in the dangerous direction.
Try designs that push the threshold way out.

- [x] thread2_noise_robust.py
- [x] Baseline: plain CHSH (reproduce p* ~ 0.08 as the control).
- [x] Design A: REPEATED-PROBE MAJORITY VOTE. Aggregate m independent reads per
      (setting,setting) before signing -> effective noise (1-2p)^? ; find p*(m).
- [x] Design B: CHAINED / Braunstein-Caves N-setting inequality. Larger N is more
      noise-tolerant per-correlation? Measure p*(N).
- [x] Design C: a SELF-TEST style consistency check — demand the generative source
      also violate a SECOND independent inequality; require BOTH -> lowers false negatives?
      (trade FN for possible FP — measure the confusion tradeoff).
- [x] Report p* for each design; which one moves the dangerous FN wall the most, and
      at what cost (probes, settings, false positives).
- [x] Figures: p*(design/param) bars or curves; confusion vs noise for the best design.
- [x] Honest: is any of this reachable for a REAL auditing channel, or just more knobs?

## DELIVER
- [x] Extend Godel_Height_Report.md with a "Threads 1 & 2" section (§6)
- [x] Repackage zip
