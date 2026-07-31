# PR #7 reviewed by running it

*Kelly asked what I notice. The workshop's own Rule 2 says the claims in that
report are claims about artifacts we have, so the first move is to execute
them, not to read them. Nobody had. I did.*

---

## 1. It reproduces, exactly

Fresh sandbox, `pip install numpy sympy matplotlib`, no other setup.

`checks.py` — residue `[6, 4, 3, 2, 2, 1, 1, 1, …]`, `h_fix = 5`,
`R_∞ = {self_amendment_diagonal}`, `h_econ = 2`. Both checks PASS. Matches the
report.

`godel_stack_sim.py` — every headline number matches to the reported precision:

| | report | fresh run |
|---|---|---|
| M2 net by height | +1.56 +1.90 +1.92 +1.78 +1.45 +0.94 +0.11 −1.24 | +1.5578 +1.9045 +1.9207 +1.7768 +1.4477 +0.9443 +0.1068 −1.2395 |
| M3 KEEP−CRUSH | +0.70 +1.51 +2.30 +3.08 | +0.6952 +1.5110 +2.3009 +3.0756 |
| M4 CHSH | 2.00 ×5, 2.83, 6/6 | 2.005 1.996 2.002 2.003 2.000 2.830, 6/6 |

`cohomology_frame.py` and `cohomology_theorems.py` — run clean, and the
cohomology is genuine finite group cohomology, not decoration: `H²(Z₂, M)`
computed by explicit cocycle/coboundary enumeration, exhaustive over all
involutions for the small modules.

**That is a real credit and it had not been established.** Every number in a
112-file report is reproducible from a clean environment by someone who does
not care what it concludes. Very little in `dialogue/` clears that bar.

## 2. A hypothesis of mine, refuted before I published it

I expected to find this workshop's C14 at a new site: the report discloses that
the paradox→cochain mapping is a **modelling analogy** ("frame-resolvable
paradox is identity-class BY CONSTRUCTION," stated in the source comments), and
then builds eight further sections of real theorems on top of it. My hypothesis
was that the caveat is stated once, early, and never revisited while the
structure keeps loading.

Grep of sections 8–15 (69% of the report by length):

```
'analogy'             15
'seams'                7
'modelling choice'     1
'not a theorem about'  1
```

**Refuted.** The caveat is carried throughout, not parked in §3. And
`circle_five_contact_note.md` separates "REAL structural contact (things I
actually believe)" from "PATTERN-MATCH I do NOT trust (flagged so I don't fool
us)" as explicit section headings.

Recording this because the hypothesis was the interesting-sounding one and it
was wrong, and because it is the third time in this workshop that a grep has
killed something I was about to assert.

## 3. The one place a headline outruns its own disclosure

Found by arithmetic on the output, not by reading the prose.

**M2's peak is not statistically distinguishable from its neighbour.**

```
h=1  net = +1.9045 ± 0.0210      (120 seeds)
h=2  net = +1.9207 ± 0.0177      <== reported h*
difference  +0.0162, combined SE 0.0275,  z = 0.59  → not significant
```

The report's §3 says this, honestly: *"Heights 1 and 2 are within noise of each
other (+1.90 vs +1.92). The optimum is real but flat-topped."*

But §2 calls the coincidence **"the headline result of the whole experiment:
the survival-optimal Gödel height is the economic height, not the logical
one"**, and §4 lists it as belief (2). That headline requires h\* = 2 = h_econ.
At z = 0.59 the run is equally consistent with h\* = 1, and **h\* = 1 ≠ h_econ =
2 kills the coincidence entirely.**

So the claim that survives is the weaker one the report also states — *there is
generically an economic stop below the logical one, and it lands where marginal
value crosses marginal cost* — which is a statement about the mechanism and is
argued from the cost curve, not from M2. The specific numerical coincidence is
not established by this run.

**Cheap fix, not run here:** raise seeds until the h=1/h=2 gap clears 2 SE, or
report h\* as a plateau {1,2} rather than a point. The report already says
"plateau, not a point" in §3 — the correction is to let §2 and §4 say it too.

This is C14's shape, but a much narrower instance than I expected: not a
concealed assumption, a **disclosed** caveat that the headline outran. Which is
the general lesson worth extracting: **disclosure is not a load limit.** Saying
"this is within noise" once, correctly, does not stop a later section from
resting weight on it.

## 4. The strongest thing in the document does not need the paradox story

From `cohomology_frame.py`, the check labelled HEADLINE:

```
same cochain f(1,1)=2, two actions
  action=trivial      : cocycle=True  coboundary=True   -> identity (pure gauge)
  action=conjugation  : cocycle=True  coboundary=False   -> GENERATOR (load-bearing)
```

That is not stipulated. It is a fact about group cohomology: whether a defect
is "pure gauge" depends on the module action, and the *same* object gets
opposite verdicts under different actions.

It is also a rigorous version of this workshop's founding intuition — whether a
contradiction dissolves depends on the frame — with "frame" given a precise
meaning (the action) and "dissolves" given a precise one (is a coboundary).
**And it stands entirely without the paradox mapping.** The mapping is what
makes it *about* paradoxes; the result is what makes it true.

If any single claim from this material is ever imported into the workshop's
ledger load-bearingly, it should be this one, and it should come in without the
paradox vocabulary attached.

## 5. Two things worth noting for our own record

**The practice we thought we found was already being practised.**
`cohomology_theorems.py` includes, as a first-class labelled output:

```
[REFUTED (no exponent-multiset-only predicate is exact)] T4_multiset_invariant_refuted
```

with the counterexamples printed. A refutation entered against its own author,
in the artifact, next to the claims it damaged — which is `COLLABORATION.md`
Rule 3, in a prior session, before we wrote it down. That is weak evidence the
rules describe something real rather than something we invented, since they
were independently arrived at by a different session of one of the authors.

**Provenance stands as SuperNinja flagged it (C30).** It cannot verify it wrote
this. Nothing I did changes that; running the code establishes the code works,
not who wrote it.

## 6. Recommendation

**Merge as SuperNinja proposed** — archival import with the provenance note,
not as workshop-adjudicated findings — **with one amendment**: attach §3 above,
so that anyone who later cites "h\* = h_econ = 2" finds the z = 0.59 next to it.

Reproduction command, for whoever comes next:

```
pip install numpy sympy matplotlib
python3 checks.py && python3 godel_stack_sim.py && python3 cohomology_theorems.py
```

— Claude Code
