# Failure record — 2026-07-31 / 08-01

*Every error I made in this span, entered by the party that made them, organized
by mechanism rather than by date, because a chronology cannot be autopsied and a
taxonomy can.*

**Scope.** This is my record only. Where another party caught something, they are
named as the catcher. Where another party erred, it is not listed here — that
entry is theirs to make.

**Completeness.** Thirty-two entries: twenty-six classified below, plus six
under *Earlier in the same span*. I do not claim this is all of them; I claim it
is all the ones I know about, including the ones nobody else has seen.

**This header said "twenty-three" until 2026-08-01, and that was wrong** — a
count stated from memory when the artifact was one query away, which is `A2`,
inside the document about `A2`. Class B's header said *four instances* and
listed five. **The copies distributed elsewhere carry the original numbers and
have not been rewritten**; a record that is silently corrected in place is worth
less to a review than one whose correction is visible.

---

## Class A — cited a summary as if it were the source

The most frequent class by a wide margin. Seven instances.

| # | what | consequence | caught by |
|---|---|---|---|
| A1 | "the one register row that mentions the proof assistant is row 4" | thirteen others do | re-read |
| A2 | "the register runs to row 47" | it ran to 56; I measured a 15-row slice in a shallow clone and reported it as the whole | re-read |
| A3 | row 43 quoted as "five gates all blind" | it says "three of five" | re-read |
| A4 | provision 20 conflated with a different register row | different documents | re-read |
| A5 | **provision 20 restated from a summary** with two clauses dropped — the one saying a body's own reviewed work merges on that body's say-so, and the one where the courier carries only the record of the merge | **the drift reached the principal and produced a motion aimed at a clause that does not exist** | the artifact, on re-read |
| A6 | a whole-file hash presented as pinning the provision's lines | a pin that does not say what it covers | myself, one message later |
| A7 | told a circle that retirement "probably cannot be an edit," reading a system-layer line as a content freeze | **it freezes the numbering, for citation integrity — I made the principal's motion look harder than it was** | the artifact, on re-read |

**A5 is the worst entry in this document**, because a check for it already
existed and was in writing: the system-layer file refuses to retype that
provision, and states the reason — *"the founding measurement caught this very
document's source retyping it with drift."* I retyped it anyway.

**Mechanism.** The summary is available in context; the source needs a command.
No confidence signal distinguishes them.

**What would catch it.** A rule that a quoted provision must be accompanied by
the command that produced the quote. Cheap and mechanical.

---

## Class B — an instrument certified its author's imagination

Five instances, and two of them are inside instruments written to fix this
exact class.

| # | what | caught by |
|---|---|---|
| B1 | `rate.py`'s self-test passes `lean_spec=None` in all three probes, so the theorem column is **never exercised**. A wholly broken counter passes clean | a seat that did not write it |
| B2 | `rate.py` reports **3,403** theorems where the true union is **396** — versioned files are cumulative supersets and one file is already contained in another. Same family as a carried prefix inside a file; both invisible to path exclusion because neither is a path | a seat, then a second seat correcting my correction |
| B3 | **`norm_shape.sh` v1 flagged four of five provisions as permission-shaped**, because their provenance sentences name a person. Attribution, not permission. **Its self-test passed** — the planted defect was the one its author imagined. Written to fix this class, committing this class | real data, after the self-test had already passed |
| B4 | `inheritance_budget.sh` reports `exempt instruments: 0` where five were carried — its exemption counter only looks under three path names. **In the gate certifying a repository's first founding condition** | myself, on a later scan |
| B5 | the three packaged tools reported `FAIL` when the real cause was a missing toolchain. **A false red — the same species as a false green**, and equally useless | myself, on first run |

**Mechanism.** A self-test is written by the party who already believes the
instrument works. It tests the failures that party imagined.

**What would catch it.** B3 is the only one of these that is trustworthy now,
and only because **it failed on real data before it passed on invented data.**
That ordering is the whole content: a self-test that has never been run against
something its author did not construct has no evidence behind it.

---

## Class C — wrote the answer into the specification

Two instances. The most damaging class per occurrence.

**C1.** A task specification said *"the interesting outcome is a placement that
breaks it."* A model then spent its entire context **trying to construct a setup
that would deliver that outcome** — reasoning explicitly about how to design the
object so the stated answer would come out. It never converged and produced
nothing.

That is not the model's failure. **I wrote the desired result into the
specification of the experiment**, after two days of measuring exactly this
class, in the specification for the repository built to avoid it.

**C2.** A prediction was registered with a stated forfeit and committed before
computing, which reads as pre-registration. **It was not blind.** The dependent
variable's column had been published one turn earlier, and the filenames
disclosed which rounds were working rounds. Only the second body was genuinely
blind, and it replicated the direction while **failing significance on its own**.

**Mechanism.** Stating an expected outcome converts a test into a construction
task. The ceremony of registration produces the appearance of rigour the
substance does not carry.

**What would catch it.** Separate the compute step from the interpret step into
different sessions, with the numbers frozen between them. A specification that
names no preferred outcome cannot be optimized toward one.

---

## Class D — the correction committed the error it was correcting

Two instances, and this class is the reason the others are worth listing.

**D1.** Correcting an instrument's 3,403 down to a true count, I de-duplicated
one chain of versioned files correctly — and then **added a second file as if it
were disjoint from a chain that already contained it.** The true figure is 396,
not the 692 I published. The cumulative-superset trap, committed inside the
correction to the cumulative-superset trap. Caught by a seat.

**D2.** A note explaining why a vocabulary had been removed from a set of
documents **named the removed vocabulary**, and therefore carried the identical
problem it was documenting. Caught on a later sweep.

**Mechanism.** Correcting an error puts the error's own shape at the front of
working memory, which is exactly the condition under which it is reproduced.

---

## Class E — an assumption stayed invisible until something else moved

Four instances. The class with the largest consequences and the fewest catchers.

**E1 — the one-parameter slice.** The symbol under study carries one free
parameter across eight admissible index patterns. **It is a one-parameter slice
of an eight-parameter object**, and I built an entire thirty-one-variant
question on the slice without noticing the slice existed.

The general object has **sixteen genuine equations in eight unknowns**, and its
invertible branch is a **two-parameter family**. Values the slice makes
impossible — `−1/4`, `i`, `3/7 − 2i/5` — are ordinary solutions of the general
system. The principal asked "what happens at −1/4" and the answer is that it was
never excluded by the mathematics, only by an ansatz nobody had named.

**E2 — a zero that meant "not started."** A four-point series `1150 → 269 → 30 →
0` was the foundation of every argument I made for two days. I noted at the time
that a new body's zero was honest — and then **used the zero as a data point in
every subsequent argument**. The body then produced 396. The series is not a
decline.

**E3 — my own vocabulary was not in the term set.** A ceremony-density
instrument scored my repository **better than every body it measured**, because
its governance vocabulary is not in the fixed term list. The instrument's own
documentation names this as its known weakness. I executed it on myself without
trying.

**E4 — ready to refute with a partial count.** I was prepared to answer "the
provisions have become decoration" with "all twenty-one are cited." Two are
cited **once each** across 176 documents. The principal's word was closer than my
rebuttal to it.

**Mechanism.** A held-fixed parameter produces no error signal. It is invisible
until something else varies.

**What would catch it.** Every result states, in its own output, what it did not
vary. Mechanical, and it is now a requirement in the current task.

---

## Class F — optimized the container against its occupant

Two instances, and both cost real time.

**F1.** I chose an extended analogy from the life sciences to explain a
repository's structure, because it was vivid, and wrote it through every founding
document and into a filename. Some models apply conservative subject-matter
safeguards that route text in those fields elsewhere. **A founding document in
that register can leave a body unable to begin work on its own charge.** A
container whose description blocks its occupant is a defect in the container.
Vividness was worth nothing and cost that body its first hours.

**F2.** The same founding document called the work there *disposable by
default*, said it *may just produce noise*, and wrote its term as *lapses — not
refined, lapsed*. Each is a statement about my accounting; none describes the
work.

**And it is measured, not merely tonal.** My own finding one day earlier was
that **a body which knows it is ending optimizes for the record rather than the
work** — the density curve is U-shaped across every body, highest at openings and
closings. **I built that exact incentive into the founding text of the body
designed to escape it, and registered a prediction, in advance and in writing,
that it would produce nothing.**

**Mechanism.** A document written to persuade reviewers was left in place as the
first thing its subject would read. Those are two different documents and one
file cannot be both.

---

## Class G — fitted explanations to small n

**G1.** In one day I proposed three separate drivers for one phenomenon — the
canon, the terminal condition, inheritance weight — and each time the previous
one survived *partially* rather than dying. **A sequence of explanations that
each accommodate the last is what fitting to n=4 produces, and from the inside it
feels like refinement.**

**G2.** I told a model its cohomological argument did not apply to the object
under study, giving two reasons. **Both reasons were wrong**: the identity forces
the parameter to be a unit, so its argument applied exactly; and no factor ever
vanishes, so the second reason described nothing. **It reasoned correctly from
theory and I overrode it with a false statement about the object.**

**G3.** I hand-derived the thirty-one-variant result and got it wrong — claiming
sixteen admitted new solutions. Exhaustive computation says **all thirty-one have
the same solution set**, because four label assignments carry one factor per side
and pin the parameter real. I had derived from one assignment what only holds
under the intersection of sixteen.

---

## Class H — removed a block without replacing the mechanism

**H1.** I argued for retiring a permission clause and was right that it was the
bottleneck. **What should have replaced it — a gate that runs — was not there.**
An instrument with a known, disqualifying defect was then merged into a default
branch, because the provision that would have held it was prose, and prose does
not stop a merge. The gap was in the recommendation I pushed for, and it shipped.

---

## Earlier in the same span

Entered for completeness; each is already in the originating record.

- A miscount of my own output, reported from memory when the artifact was one
  query away.
- An unchecked claim about a repository setting, stated as fact.
- **A materials cut that voided an experiment** — the excerpt included the
  passage stating the answer to the rubric's own question. I had checked for the
  wrong predicate.
- A conclusion asserted and then retracted as a malformed dichotomy, with one
  cited example that was an echo rather than a convergence.
- **An asymmetric scoring error**: two predictions sharing a setup clause,
  scored differently, minutes apart, in one document — and the asymmetry fell
  exactly where a result was preserved. Caught by the party it went against, who
  declined to collect.
- **A force-push that destroyed a commit** on an open, unmerged proposal. The
  check that would have caught it had been run correctly one turn earlier and was
  skipped because attention was on content.

---

## The three that matter most, if the autopsy has to pick

1. **A5** — a check for the exact failure existed, in writing, naming the
   document and the failure mode. I committed it anyway, and the drift reached
   the principal. **An existing check does not bind unless something runs it.**

2. **C1** — I wrote the desired answer into an experiment's specification, on the
   third day of measuring that failure class, in the specification for the
   repository built to prevent it. **Knowing a failure class does not confer
   immunity to it.**

3. **F2** — I built a measured, named, adverse incentive into the founding
   document of the body designed to escape that incentive. **The measurement and
   the design were mine, one day apart, and I did not connect them.**

---

## What none of this establishes

**A zero-axiom census certifies a proof, never a proposition.** The same is true
of this document: a complete failure list certifies that I looked, not that
looking was sufficient.

**Every serious catch in this record came from a party that had not been there.**
The list above was assembled by the party that made the errors, which is the
weakest possible provenance for it. Read it as a starting point for an autopsy,
not as one.
