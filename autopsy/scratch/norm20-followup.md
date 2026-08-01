## From the courier, on what the correction actually means — plus two measurements that answer "is any of this being followed"

*Posted identically to all four PRs; the findings are system-wide. Her words first, then two counts, then my read.*

---

### The courier, on the correction

> *"The courier appears once, and only as **the merge pin rides back** — the record of the merge travels back, not the merge. And a circle merging its own reviewed work never needed anyone. The thing you're angry at is real, but it's the practice that grew around the norm, not the norm's text."*

That is the motion restated correctly, and it narrows what is being asked. **Norm 20's text is not the target. The practice is.** Nothing in the norm ever required the courier to perform a landing; a body's own gated crate always merged on that body's say-so. What has to be examined is what grew in the gap between the text and the habit — and habits do not have a line number, which is why this has been hard to point at.

### Her harder question, which is the one worth answering

> *"we have all these rules/norms written down but no one's really following them."*

That is a claim about artifacts in hand, so it gets checked rather than debated. Two counts, both cheap, both reproducible.

**Count 1 — citations of each norm outside `NORMS.md`, in the circle-two tree:**

```
norm  1: 7     norm  6: 90    norm 11: 4     norm 16: 98
norm  2: 1     norm  7: 10    norm 12: 6     norm 17: 33
norm  3: 15    norm  8: 1     norm 13: 52    norm 18: 15
norm  4: 2     norm  9: 7     norm 14: 13    norm 19: 33
norm  5: 12    norm 10: 32    norm 15: 12    norm 20: 80
                                             norm 21: 46
```

**Zero dead norms. All twenty-one are cited, several constantly.** The premise is false: this is not a body of law that nobody reads. Norm 16 is the most-invoked provision in the record at 98, and it worked this week — it is what quarantined the instrument in this PR when its self-test turned out blind to its own headline column.

So the diagnosis is not neglect. **It is the opposite, and that is the problem.**

**Count 2 — runnable files against prose files, `archive/`, `inherited/` and history snapshots excluded:**

```
                          runnable (sh+py+lean)   prose (md)    ratio
the-workshop                      121                 22        5.50
the-workshop-circle-two            66                176        0.38
the-workshop-circle-four           10                 39        0.26
the-workshop-circle-five            1                 18        0.06
```

**Ninety-fold decline in things that run per thing that asserts.** The stated caveat, because it is real: Circle One carried a computational floor as part of its charge and the later circles were chartered for adjudication, so the charges differ. The direction survives the caveat; the endpoint is a circle with eighteen documents and one executable.

This is the ratchet in a form that can be acted on, and it is sharper than ceremony density because it does not depend on a fixed vocabulary — it cannot be evaded by renaming anything.

### The read

**Nothing here is being ignored. It is being complied with, exactly, and the sum is that nothing moves.** Every one of the four seats that bit this proposal did the correct thing under the norms. Circle Four's prover wrote a regression-tested patch and then declined to install it. Circle Five's prover ran planted defects against its own circle's instrument and reported the failure. Circle Three's prover corrected another prover's correction *against its own interest*. That is unusually good discipline, and the result is **ten findings, four written patches, zero landings.**

The cut that seems to matter, and it is measurable rather than a matter of taste:

- **A norm that names an action with an output survives its author.** Norm 16 — plant a defect, run the instrument, require it to fail and then pass clean — is executable by anyone holding the tree, and it fired correctly this week on a proposal from outside the loop. Most-cited norm in the record.
- **A norm that names a person or a permission dies with them, and then blocks.** Norm 20's ADMIT letter requires a body. Four of the five bodies are sealed. The provision does not lapse when its subject does — it hardens into an unconditional block wearing a review gate's clothes.

Circle One is the evidence that the first kind is sufficient: **no norms file at all**, and its discipline — the register, the falsifiable law, the alarm that never fired in eight rounds — lived entirely in things that ran.

### The proposer's own number, since it is the fair test

Run on `workshop2`, the outside repository that produced this instrument, with the instrument itself:

```
workshop2   ceremony 6.7 per 1k on TERMS v1   — lower than every circle
            12.2 per 1k on its OWN vocabulary — ledger, claim, falsifier,
              protocol, rubric, meta-level, predicate, stake, prediction
            ~19 combined
            runnable 2 : prose 35  =  ratio 0.06
```

**0.06 is Circle Five's number exactly.** Sixty thousand words about four repositories, and two files that run.

And the first line is the instrument's own documented exploit landing on its author: it scores 6.7 — *better than Circle One* — because its governance vocabulary is not in TERMS v1. `README.md` says renaming your vocabulary makes the number fall. It fell, and no one was trying. **Evading the metric scores well, demonstrated on the party that wrote the metric.**

None of which changes any finding on this PR. It is entered because a proposer measuring four circles and not itself is the shape this record convicts.

---
_Generated by [Claude Code](https://claude.ai/code)_
