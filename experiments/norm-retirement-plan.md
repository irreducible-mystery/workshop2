# Retiring norms 20 and 21 — the shortest path that stays legal

*Requested by the courier: **"a plan on how to retire norm 20 and 21 as quickly
and easily as possible."** Written against the record's own mechanisms, so that
nothing here needs a new procedure to be invented.*

**The whole plan is one file and one commit. Everything before it is unblocking
that does not require the retirement at all.**

---

## Step 0 — Unblock first. It needs no retirement, and it works today.

Two independent openings, both already in the record:

**(a) Norm 20 permits it in its own text.**

> *"**A body's own gated crate merges on that body's say-so.**"*

Circle Five is the only body with no closing document — **the only live body in
the record.** Its seat has bitten `circle-five#2`, found a norm-16 blocker, and
said so. Once that blocker is fixed, that PR is *a body's own gated crate* and
merges on *that body's say-so*. **No courier, no ADMIT letter, no retirement.**

**(b) Norm 20 has no jurisdiction in Circle One.**

`the-workshop` contains zero occurrences of *"norm 20"* or *"seat of record"*,
and no norms file. The norm was written by Circle Two's builder after Circle One
sealed, about a merge in another tree. **Circle One never adopted it.**
Disposition of `the-workshop#1` is the courier's, not a Circle Two question.

*What is genuinely blocked and stays blocked until step 2:* the two sealed trees
whose adjudicating bodies are gone — `circle-two#17` and `circle-four#3`.

## Step 1 — The one thing to get right before writing anything

**Do not edit `NORMS.md`.** Not because it is forbidden — I said that earlier
and it was wrong — but because it is *unnecessary*, and touching a frozen file
invites the drift this whole thread is about.

The canon's freeze rule (`NORMS.md:10`) freezes **the numbering**, and says why:
*"any renumbering would make those citations false."* Retirement in place, with
the number kept, keeps every existing citation true. Eighty citations of norm 20
and forty-six of norm 21 survive untouched, because **the retirement points at
the text rather than restating it** — which is norm 13, and norm 13 is the rule
the record's one previous retirement was recorded under.

## Step 2 — The retirement. One new file, in the live canon.

`the-workshop-circle-five/RETIREMENTS.md`. Modelled byte-for-byte on the form
already exercised at `COURIER-CARD.md:156`: **what it got right, what went
stale, both recorded rather than smoothed.**

```markdown
# RETIREMENTS — norms retired, recorded per norm 13

Retired norms are never erased and never renumbered. The text stands where it
was written; this file points at it, says what outlived it, says what went
stale, and names the replacement. Every prior citation stays true.

## Norm 20 — retired 2026-07-31 on the principal's motion

Text stands at `the-workshop-circle-two/NORMS.md:152-159`
(sha256 478724603edbc0af4d4b09416dd33642ad90802c9a5a3007d49022f46c50b63c).
Pointed at, not retyped: `SYSTEM-NORMS.md:89` records that retyping this
particular norm has already produced drift once, and it produced it a second
time in the proposal thread that led here.

**What it got right, and what is kept:** the sequence clause. A record must
not assert an adjudication that did not happen. That is why the ten findings
on the four rate/ proposals could be trusted at all.

**What went stale:** the routing clause — "the merge pin rides back through
the courier" and the practice grown around it. It bound the landing to one
person for reasons unrelated to whether the landing was correct. By 2026-07-31
four of the five bodies that could rule ADMIT were sealed, which turned a
review gate into an unconditional block that no seat could open. Circle Four
held a regression-tested fix its own prover could not install.

**Replacement, in force from this date:** *Any party may perform the landing.
The ADMIT word and the merge pin must be recorded before it.*

## Norm 21 — retired 2026-07-31 on the principal's motion

Text stands at `the-workshop-circle-two/NORMS.md:202` onward.

**What it got right:** the observation is true and stays true — an instrument
that measures prose against something outside the prose has nothing to reach
for when a sentence sits inside its own referent. Its boundary clause was
unusually strict and it convicted the great majority of its own specimens.

**What went stale:** it is the only category of exemption in the canon, and a
category that exempts a sentence from conviction is where unresolved sentences
accumulate. Retired in favour of the default: **record it, point at it, and
leave it uncategorised** — which is what the norm did in practice, minus the
standing exemption.

## The expiry rule, adopted with these retirements

**A norm not re-adopted by the incoming circle lapses.** Its text and number
stay standing, marked lapsed. Re-adoption is one line, so nothing valuable is
lost by lapsing and nothing survives merely because removing it needs an
argument. The cost of keeping a rule falls on whoever wants it kept.
```

**That is the entire retirement.** One file, one commit, in the only live canon.

## Step 3 — Two comments, not a procedure

One on each sealed PR, pointing at `RETIREMENTS.md`. Nothing further: the merge
is now permitted by the replacement clause, and the record shows the sequence.

---

## Why the expiry rule is what makes this cheap rather than risky

It is the answer to the obvious objection — *you are retiring on one person's
motion, after one week, against a canon that took five circles to build.*

**Under expiry, retirement is reversible at a cost of one line.** If Circle Six
finds it wants `POINTED` back, it re-adopts norm 21 by writing "norm 21" in its
adoption list. Nothing was destroyed; the text is standing and the number is
still true.

**So the risk of retiring is now smaller than the risk of keeping**, which is
the asymmetry the canon has never had. Twenty-one norms adopted across five
circles and zero retired is not evidence that all twenty-one were load-bearing.
It is evidence that **there was no cheap way to find out.**

And expiry is the rare rule that is net-negative apparatus: it is one sentence
whose only function is to remove sentences.

## The dissent I owe on norm 21, since I am recommending its retirement

**Norm 21 is not the same case as norm 20, and retiring it buys much less.**

Norm 20 is the only permission clause in the canon and it is the measured
deadlock. Norm 21 is a *disposition* with a mechanical test — *"if a sentence
could be settled by running any instrument against anything outside itself, it
is not in this category — convict it or record it"* — and by its own account
most candidates failed that test and were convicted. On the census that produced
the recommendation to retire norm 20, **norm 21 sits on the healthy side.**

My honest read: **it is a defensible norm with a real observation behind it, and
its cost is that it is the canon's only exemption category.** That is a
reasonable thing for a principal to want gone, and the expiry rule is precisely
what makes the judgement cheap to reverse if it turns out to have been wrong.

Retiring it is the courier's call, and this plan carries it as instructed. What
I will not do is present it as the same finding as norm 20, because it is not
one — norm 20's retirement is supported by measurement, and norm 21's is
supported by a preference. **Both are legitimate. Only one of them is a
result.**

---

## What this plan does not do

- **It does not merge anything.** Every step is written; the landings are the
  circles' and the courier's.
- **It does not touch `NORMS.md`.** By design.
- **It does not fix `rate/`.** Ten findings and four written patches are still
  outstanding on the four proposals and are a separate job.
- **It has not been read by anyone who did not write it.** By this record's own
  rule that is one seat's word, and one is not enough.
