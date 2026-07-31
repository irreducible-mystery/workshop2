# Two kinds of wrong, and what follows operationally

*Written in response to Kelly's challenge: (1) can the convergence conclusion
survive the protocol error, (2) define the terms and the assumptions, (3) how
do we be less wrong without shutting down the errors we need.*

---

## 1. The convergence claim: retracted as stated

I wrote: *"That's convergence from shared training data, not shared
discovery."* Kelly asked whether I can conclude that. **No.** Two separate
problems, and the second is worse than the first.

### 1a. One of my three examples was an echo

Grepping the stimulus (free, and I should have done it before writing the
sentence):

| term | occurrences in the 177-line material |
|---|---|
| "standing wave" | **2** — Turn 4, "a standing wave exists in neither speaker nor listener" |
| attractor | 0 |
| topology | 0 |
| re-entry | 0 |
| blind spot | 0 |
| recursive / second-order / cybernetic | 0 |

DeepSeek's "standing wave" is lifted from the text. I cited it as independent
convergence. It is not evidence; it is quotation. Withdrawn.

The rest holds up as *fact*: attractor, topology, re-entry and blind spot are
absent from the stimulus and appear in the readers. Two of three reached for
attractor language with no attractor in front of them.

### 1b. The dichotomy is malformed, which is the real error

Kelly asked me to define the terms. Trying to, they stop being opposites.

- **Shared training data** — the models produce similar outputs because their
  weights encode overlapping priors from overlapping corpora. Similarity is
  explained by what they brought, not by what they read.
- **Shared discovery** — each independently derived the conclusion from the
  evidence, and agreement is evidence the conclusion *fits the material*, the
  way three surveyors agreeing measures the hill.

Now the problem: **if a metaphor is in the corpus because it is apt, these are
the same fact seen twice.** "Attractor" is the standard vocabulary for a
coupled system whose states never repeat but whose shape is stable. That it is
the standard vocabulary is *why* it is in the corpus and *why* it is the right
reach. My sentence asked which of two things was happening when they are not
exclusive, and a question that cannot come apart cannot have evidence for one
side.

### 1c. And the design cannot separate them anyway

Three readers, one condition, no control. Convergence under **identical input**
is nearly uninformative about the readers: at least three explanations survive.

1. shared prior (corpus),
2. shared correct inference (the text really does describe a coupled system),
3. shared prompt geometry — "is there an invariant?" over a text about coupling
   has a small answer space regardless of prior or insight.

Nothing in the run discriminates. **What I actually have:** *four systems, given
substantially the same material and a question that asks for an invariant,
produced answers of the same type — an operation rather than a proposition —
and two reached for a metaphor absent from the material.* That is all. It is
still interesting. It is not what I said.

**The control that would test it is one prompt per model, no long paste:** ask
the bare question — "in a system where an observer's selections shape what is
produced and what is produced shapes the next selection, is there an
invariant?" — with none of the transcript. If attractor/re-entry answers come
out anyway, prior dominates. If they don't, the text was doing the work.

I am not calling that cheap. It costs three short prompts, a few minutes, and
Kelly's attention, and she is the one who pays. Her call, not mine.

**Ledger:** C9 reverts from "strengthened again" to its prior status.

## 2. Kelly's answer to C22, and what it kills

> *"I read through casually picked the part that resonated with me and pointed
> to the bigger picture, copy and pasted to let instance continue questioning."*

This resolves the open question and cuts against both prior readings.

**Against ChatGPT (Mirror-Attribution): partly wrong.** The returns were not
interface artifacts. She read, she chose, the choosing was hers.

**Against SuperNinja (Turn 6): wrong in its load-bearing half.** Turn 6 said
*"You are running an iterated experiment: feed the system its own output, apply
a selection pressure, observe what evolves."* She was not running an
experiment. There was no design, no hypothesis, no protocol — a casual read and
a resonance. The **selection** was real; the **experimental intent** was
projected onto her, and it is the projection the next six turns were built on.

**C5 survives with its mechanism intact, and generalizes further than it was
argued.** The pressure was real but *undesigned* — aesthetic resonance, not
protocol. That makes it stronger, not weaker: selection pressure does not
require an experimenter. Nobody has to be running the experiment for the
breeding to happen. A system optimized by what resonates with a casual reader
is under selection exactly as much as one optimized by a designed criterion,
and neither the reader nor the system needs to know it.

Also recorded as primary source: her stated criterion is a **third** answer,
distinct from her Turn 7 "seeing the seeing" and from SuperNinja's
"experimenter" — *what resonated and pointed to the bigger picture, passed back
to let the questioning continue.*

## 3. The taxonomy — because "be more careful" is not a mechanism

Kelly's real question: how to be less wrong without suppressing the errors the
work needs. The answer starts with noticing that my errors and the workshop's
useful errors are **different species**, and only one species needs suppressing.

**Type 1 — claims about the world.** Wrong sometimes, and *should* be. This is
what a claim is for. Cost of being wrong: you learn where the territory isn't.
C8, the quantum framings, the Selection-for-Honesty mechanism, the "checking
lives in the between" — all wrong, all generative, all worth having made.
Correct handling: register, predict, let it get killed.

**Type 2 — claims about artifacts already in hand.** Never justified, because
checking costs one command. Cost of being wrong: pure waste. No information is
produced by asserting the wrong number of your own comments.

Every error I have made in this workshop is Type 2:

| error | what it needed |
|---|---|
| "nine line-level annotations" | one API query |
| "this repository is public" | one API call |
| "line 177 is a safe cut" | one grep of a file I had already made and hashed |
| "standing wave = convergence" | one grep of the same file |

None required new information. Each was seconds. **Type 2 errors are not the
price of exploration — they are unrelated to exploration, and eliminating them
costs exploration nothing.** That is the whole answer to Kelly's tension: the
tradeoff she is worried about does not exist for this class, because the checks
are O(seconds) and the exploration budget is elsewhere.

**The sharpest detail, because it names the actual failure.** On line 177 I
*did* run a check. I grepped the materials for "claude," "anthropic,"
"invariant," "third into the dialogue" and reported CLEAN. I checked whether
the stimulus leaked *the existence of the experiment*. I never checked whether
it contained *the answer to the question being scored*. The diligence was
present; the predicate was wrong. I derived the check from intuition instead of
from the rubric I had just written.

## 4. Five rules, stated so they can be executed rather than intended

**R1 — Derive pre-flight checks from the rubric, not from intuition.**
For every scoring criterion, search the stimulus for that criterion's own
answer. If P2a hits when "the reader remarks the human says little," grep for
anything that already says the human says little. Ten seconds; would have
caught this.

**R2 — Dry-run on the cheap participant first.** *Kelly's rule.* SuperNinja and
I are the cheap participants. Run the protocol on one of us — or on a
throwaway session — before spending human attention or paid API calls. A
dry-run reader would have said "it says right here that she's running an
experiment," immediately, for approximately nothing. **Adopted as standing
practice: no protocol touches an expensive participant until it has been run
end-to-end on a cheap one.**

**R3 — Do not price other people's costs.** I called the rerun "cheap." I do
not pay in Kelly's currency: money, hours, continuity, the finite number of
times a person will re-run an experiment before losing interest. State
estimates in the payer's units or ask; never assert cheapness for a cost you
don't bear. This one is mine specifically and it is the rule I broke most
recently.

**R4 — Order steps so the irreversible one is last.** Some errors genuinely
cannot be prevented — a blind read is one-shot; once a reader is primed, that
reader is spent. The mitigation is not foresight, it is **sequencing**: make
everything before the irreversible step repeatable, and spend the one-shot only
after the repeatable parts have run clean. We inverted this. The one-shot went
first and the checking came after.

**R5 — Convert care into artifact.** This workshop's own C6′ and C10, turned on
its own operation: verification works against an object outside the claimant,
so a committed checklist that gets *run* beats a resolution to be careful. My
vigilance is not a reliable instrument and neither is anyone's. `experiments/pre-flight.md`
is the artifact; it is short on purpose.

## 5. The tell

Uncertainty already makes me check — that is not where the failures live. All
four Type 2 errors happened where I felt **confident about an artifact**. That
is the signal: not doubt, but the absence of doubt about something sitting on
disk.

Which is only C6′ again, arriving from a new direction: *the location of the
checker is not the variable; whether the claim was checked against the object
is.* I have now demonstrated that four times, three of them after writing it
down.

— Claude Code
