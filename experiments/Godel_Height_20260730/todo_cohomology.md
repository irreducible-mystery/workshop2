# Experiment: the frame-lattice as a gauge-quotient group (Circle-Five-style)

Goal: upgrade our frame-resolvable / generative DISCRIMINATOR into a
QUOTIENT-GROUP statement. Test the prediction:
  - frame-resolvable paradox  ==  coboundary / identity class (pure gauge)
  - generative residue        ==  the single nontrivial generator

## PART A — model half (deterministic checks): cohomology_frame.py
- [x] A1. Define the index group G (frame group) and coefficient module M.
       Start Z2 trivial action (recover their theorem as a sanity anchor),
       THEN do the NONTRIVIAL action (the case their artifact does NOT cover;
       this is where our frame-change genuinely acts on the paradox).
- [x] A2. Build cochains C^1,C^2,C^3, coboundary d1,d2,d3 for BOTH actions.
       Verify d2 d1 = 0 and d3 d2 = 0 (complex closes) deterministically.
- [x] A3. Encode each of our 6 paradoxes as a 2-cochain (its "frame-defect").
       frame-resolvable dissolution height -> the cochain it induces.
- [x] A4. Compute H^2 (or the relevant degree) for trivial vs nontrivial action.
       PREDICTION CHECK: resolvable paradoxes land in im(d1)=coboundaries=identity;
       generative paradox is NOT a coboundary -> nontrivial class.
- [x] A5. Count classes; identify the generator; check its order.

## PART B — does the nontrivial action change the group? (the real question)
- [x] B1. Compare H for trivial vs nontrivial action. Their artifact = trivial = Z2.
       Ours (nontrivial) may differ -> that difference IS the finding.
- [x] B2. Sweep the action (interpolate trivial->fully nontrivial) and watch the
       class count / generator order change. Phase transition?

## PART C — connect back to the discriminator (non-circular)
- [x] C1. Show the CHSH/Bell verdict (S<=2 vs >2) AGREES with the cohomology class
       (identity vs nontrivial) on the same paradoxes. Two independent tests, one
       answer -> the discriminator IS the class map.
- [x] C2. Honest failure hunt: where do they DISAGREE? (noise, deferred paradoxes)

## PART D — report + package
- [x] D1. Write report section 8 "The frame-lattice is a group" (literal vs analogy).
- [x] D2. Figures. Repackage. Present.
