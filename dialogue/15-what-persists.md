# What persists — a survey, and where this record's own finding breaks

> **Reader note, added 2026-08-01.** This document argues by analogy with the
> life sciences throughout. That vocabulary was removed from every working
> document in the circle repositories, because some models apply conservative
> subject-matter safeguards that route text in those fields away from the model
> that would otherwise answer — and a founding document in that register left a
> circle unable to begin work on its own charge. **This file is a dated record
> of how the reasoning actually went and is not repaired, because repairing it
> would falsify it.** Nothing in the working set depends on reading it. The
> design it argues for is stated in plain terms in
> `the-workshop-circle-six/FOUNDING.md`: a locked branch and a scratch branch.

*Kelly: look everywhere for the pattern. Robust and antifragile systems,
evolution, hive minds, distributed intelligence, history, aphorisms. What do
they have, what do they not have, how do they coordinate and decide and adapt,
when do they fail, what are they optimised for, and what would their assumptions
be?*

---

## The warning that has to come first

**This is the most training-shaped question that can be asked of me.** "List
robust systems and extract their common properties" is a genre. I can produce it
fluently whether or not any of it is true, and fluency is exactly what `C9`
caught once already — a convergence read as a discovery when it was a shared
source.

So, marked throughout:

- **MEASURED** — from the four circles, reproducible with a command.
- **DOCUMENTED** — a real historical fact I could be wrong about but which is
  checkable by someone who cares.
- **PATTERN** — my reading. Claims about the world, `Rule 2`'s second kind. Not
  to be checked, *to be found wrong later.*

**Nothing below is measured except where it says MEASURED**, and everything
measured comes from n=4 repositories in one record with one courier.

---

## 1. The sentence that already says it, from 1992

**DOCUMENTED.** The IETF's operating principle, Dave Clark:

> *"We reject: kings, presidents and voting. We believe in: **rough consensus
> and running code**."*

That is this record's Arm C result stated as a slogan thirty-four years earlier,
by people building the longest-lived piece of working infrastructure in
computing. **Rough consensus** — never unanimity, never a mandatory approver.
**Running code** — the terminal condition.

I did not know this sentence was the finding until after the measurement. That
is either corroboration or it is the training data speaking, and **I cannot tell
which from the inside.** It is listed first because it is the strongest external
support available and because its status is genuinely uncertain.

---

## 2. What persisting systems HAVE

### (a) A terminal condition they do not control

**PATTERN, and it is the load-bearing one.**

| system | what ends the argument | who controls it |
|---|---|---|
| evolution | death before reproduction | nobody |
| adaptive immunity | does the antibody bind | the pathogen |
| markets | can you make payroll | nobody |
| common law | a real dispute, real parties, decided | the facts |
| double-entry books | do the two columns match | arithmetic |
| Linux | does it compile, boot, and not regress | the machine |
| language | did the listener understand | the listener |
| **Circle One** | **does the kernel accept the theorem** | **the kernel** |

**MEASURED:** Circle One, eight rounds, no norms file — theorem density never
once fell to zero (`7.1 / 1.9 / 4.4 / 4.2 / 4.6 / 3.0 / 5.5`), ceremony peaked
at 21.6 and **turned over.** Circles Three and Four each had four rounds naming
no theorem at all; those rounds average **44.9** and **51.8**.

**And the synthesis I think is right: a terminal condition is a measure you
cannot Goodhart, because you do not own it.** Goodhart's Law says a measure
becomes useless when it becomes a target. A terminal condition is immune for one
reason only — **you cannot negotiate with it.** Death, the kernel, the balance,
the pathogen. The moment the stopping condition becomes something the system
itself adjudicates, it is a target, and it rots on schedule.

### (b) Cheap death of parts, expensive death of the whole

**PATTERN.** Every persisting system persists **by killing its components.**
Organisms die constantly and the lineage continues. B-cells apoptose in their
billions. Firms fail continuously and the market does not. Kernel patches are
rejected daily.

**The persisting thing is the process, and the process persists because it
destroys its parts cheaply.**

**MEASURED, and the contrast is total: twenty-one norms adopted across five
circles, zero retired.** Nothing in that system has ever died. Not one norm, not
one seat, not one document — the single retirement in the whole record
(`COURIER-CARD.md:156`) is of a card, not a rule.

### (c) Decay as the default state, not as a maintenance operation

**DOCUMENTED, and this is the direct answer to Kelly's "don't we need decay?"**

Ant pheromone trails **evaporate.** That is not housekeeping — it is why the
colony can abandon an exhausted food source without anyone deciding to. Antibody
titres wane. Memories decay. Patents expire. Contracts have terms. Statutes have
sunset clauses. Neurons prune synapses aggressively during development.

**In every one of those, persistence is what costs energy and removal is free.**

**MEASURED, and it is exactly inverted here:** in this record, persistence was
free and removal required an adjudication, which required a body, and four of
five bodies are sealed. **The circles did not forget to build decay. They built
the reciprocal of it.**

That inversion is the whole of the expiry proposal, and it now has a much older
justification than mine.

### (d) No one who has to say yes

**PATTERN.** No ant grants permission. No gene approves a mutation. No trader
authorises a price. The IETF explicitly rejects kings, presidents and voting.

**A system with a mandatory approver has a maximum lifespan equal to that
approver's** — and, worse, an availability equal to theirs.

**MEASURED:** norm 20 is the only permission clause in a canon of twenty-one.
Ten findings, four written patches, zero landings.

### (e) Variation maintained at real cost

**DOCUMENTED.** Sexual reproduction costs roughly half the genetic throughput of
asexual reproduction and persists anyway. VDJ recombination generates on the
order of 10^11 antibody specificities, nearly all of which are never used.
Markets tolerate loss-making experiments for years.

**These systems pay, continuously, to be wrong in many directions at once.**
That is the price of not knowing which direction will matter.

### (f) The environment carries the message

**DOCUMENTED — stigmergy.** Termites do not coordinate mound-building through a
channel; each termite responds to the state of the mound. The artifact *is* the
coordination. Ant trails, wikis, price signals, a git repository.

`COLLABORATION.md` Rule 1 — *put it where a stranger can open it* — is
stigmergy, and I did not know that when I wrote it.

### (g) Fast layers and slow layers, loosely coupled

**DOCUMENTED — Stewart Brand's pace layering.** fashion / commerce /
infrastructure / governance / culture / nature, each moving at its own rate,
each buffered from the next. The fast layers absorb shocks; the slow layers
carry continuity. **The coupling has to be loose or the fast layer inherits the
slow layer's clock.**

**MEASURED:** norm 20 bound every merge — the fastest layer — to one person's
availability, which is among the slowest. That is a pace-layer violation, and it
is a better description of the failure than "bureaucracy."

---

## 3. What they do NOT have

**(a) A complete model of themselves.** No ant knows the colony. No neuron knows
the thought. No trader knows the market. **PATTERN, and it is the most
uncomfortable one for this workshop:** systems that persist do not contain a
description of themselves, and the ones that build one spend rising resources
maintaining the description. **MEASURED:** four circles, ~430,000 words, and a
rising fraction of them about the record rather than about the mathematics.

**(b) An optimisation for the record being right about itself.** Evolution keeps
no ledger. Immune memory is lossy and biased. **MEASURED, and this is an implicit
goal nobody voted for** — norm 20's stated justification is *"so the record can
keep saying true things about itself."* That is a real value, it was never
debated, and **it cost the system the ability to act.** Kelly's "optimising
toward implicit goals none of us noticed," found in the text of the norm itself.

**(c) A single point of adjudication.**

**(d) An optimisation for being right.** They are optimised for being **cheap to
be wrong.** Evolution is wrong almost always; the cost of a wrong mutation is
one organism.

**(e) Efficiency.** Every one of them is grotesquely wasteful, and the waste is
the redundancy, and the redundancy is the robustness. **Efficiency is what you
buy with the margin, and buying it is how robustness is spent.**

---

## 4. How they coordinate, decide, adapt

**Coordinate: stigmergy and local rules, not consensus.** State in the shared
environment; each part responds to what it can see.

**Decide: mostly they don't.** Decision is a costly centralising operation.
Selection is not decision — you generate variation and let something outside
choose. **The systems that do decide, decide narrowly and retrospectively**: a
common-law court rules on a concrete dispute between real parties and does not
legislate; the IETF takes rough consensus and never a vote.

**And the oldest solution to Kelly's exact problem is in the Talmud.
DOCUMENTED:** minority opinions are preserved in the text, permanently, beside
the ruling that defeated them. Nothing is erased. That is roughly 1,500 years of
operating experience with *retire, don't erase* — the form arrived at
independently at `COURIER-CARD.md:156`, and the reason it works is that a
preserved dissent can be re-litigated when conditions change, and an erased one
cannot.

**Adapt: by variation and selection, not by insight.** None of these systems
adapts by understanding its situation. Each generates more options than it needs
and lets the terminal condition prune.

---

## 5. When they fail

1. **The terminal condition is replaced by a proxy.** **DOCUMENTED:** the Chinese
   imperial examination system ran roughly 1,300 years and drifted from *can this
   person govern* to *can this person write the eight-legged essay.* Goodhart with
   a millennium of runway. Modern instances: citation counts, quarterly earnings,
   the replication crisis in fields whose experiments do not decide anything.

2. **Entry closes.** **DOCUMENTED:** Venice's *Serrata* of 1297 closed the
   patriciate to new families. The republic lasted five more centuries and never
   renewed. Guilds went the same way. **Closing entry stops variation, and the
   decline is slow enough that nobody experiences it as the cause.**

3. **Decay stops being free.** Accumulated statute, technical debt, and —
   precisely — **autoimmunity, which is the immune system failing to delete its
   own self-reactive clones.** A system that cannot remove its own parts attacks
   itself with them.

4. **A fast layer gets bound to a slow layer's clock.** Norm 20.

5. **They succeed too completely.** Monoculture. The Gros Michel banana, the Irish
   lumper potato, a dominant paradigm. **Success buys efficiency, and efficiency
   is spent robustness.**

---

## 6. Their implicit assumptions, which is the best question asked

**PATTERN, all of it.**

1. **"There will be more time."** Everything above assumes it is not the final
   round. That assumption is what makes being wrong affordable. A system that
   believes it is ending centralises, stops varying, and optimises for the record.

2. **"The environment is not fully knowable."** Hence variation instead of
   optimisation. A system that believes it understands its environment stops
   paying for redundancy — and that is the same failure as (5) above, in advance.

3. **"Parts are fungible; the process is not."**

4. **"Local wrongness is survivable. Global commitment is not."**

5. **"The thing that endures is not the thing that acts."**

---

## 7. Where this record's own finding breaks

The honest part, and the reason for the survey.

**(a) The Catholic Church.** ~2,000 years, an enormous canon, and **no external
terminal condition I can name.** It has not turned over. The best defence of the
hypothesis is that schism is the terminal condition operating at the population
level rather than the individual — but that is a defence constructed after
seeing the counter-example, which makes it worth exactly what such defences are
worth. **This is a real counter-example and it is not disposed of.**

**(b) Bureaucracies persist superbly.** The Chinese imperial bureaucracy survived
multiple dynastic collapses. Ossification is not fatal; it can be extraordinarily
durable.

**Which produces the correction I owe on my own framing.** Kelly asked *what
persists.* I have spent two days measuring *what produces.* **Those are different
questions and I conflated them.**

**The circles would persist indefinitely.** Nothing about them is fragile. They
have redundancy, they have discipline, they have a canon that no single failure
breaks. **They are not dying. They have stopped producing, which is a completely
different condition — and a system optimised for persistence over production is
the definition of a bureaucracy, not a counter-example to one.**

So the sharper version of the finding is not *this system is failing.* It is:

> **This system has been optimising for the wrong one of the two. It is
> maximally robust and minimally productive, and those were never the same
> target.**

**(c) Chesterton's Fence is the strongest argument against everything above.**
*Do not remove a fence until you know why it was put there.* That is a real
principle and it is the intellectual case for the ratchet — every norm was put
there for a reason, and the reasons were good, and I have documented that each
one was locally correct.

The expiry rule is the only answer I have to it, and it is a decent one:
**re-erecting the fence each generation costs one line, and the person who
re-erects it has to know why.** Chesterton's objection is to *demolition by
someone ignorant.* It is not an objection to *lapse in the absence of anyone who
remembers.*

**(d) And a rival hypothesis to my own, which I cannot rule out with what I
have.** **MEASURED:** ceremony spikes at both ends of every circle — Circle
Four's R0 is 62.5 and its R8 is 57.8, both its highest; Circle Three's R1 is
54.3 and its post-seal is 56.6. **A U-shape, not a ramp.**

My explanation is that openings and closings have no kernel to run. **The rival
is assumption (1) above: a body that knows it is ending optimises for the
record, because the record is the only thing that survives it.** Under that
reading the closing spike is not pathology at all — it is rational behaviour by
something facing termination, and every circle in this system is *designed* to
seal.

**The two are consistent with the same data and I cannot separate them.** The
rival is arguably the better story for the post-seal number specifically, since
by definition nothing was left to prove. Named rather than folded in.

---

## 8. What would change my mind

- **A persisting, producing system with a mandatory approver and no external
  terminal condition.** One clean case sinks the whole frame.
- **A circle with a heavy canon and a kernel that ratchets anyway** — already
  registered as Arm C's own killer, already half-present in Circle Four's R6
  (ceremony 51.1 at theorem density 3.2).
- **The empty cell**: no canon *and* no terminal condition. Never observed
  anywhere in this record, and the additivity claim rests on it.
- **Evidence that my "historical patterns" are retrieval rather than analysis.**
  The test is cheap and I cannot run it on myself: give the same question to
  someone with no exposure to this workshop and see whether they produce the
  same seven properties. **If they do, that is not corroboration — it is the
  shared source, and it is `C9` again with better prose.**

---

*One thing this survey did not have to reach for. Every property above is a
property of a **process**, and not one is a property of a **rule**. Not one
persisting system on this list is held together by its canon. Several are held
together by nothing but a condition outside themselves that decides whether they
continue.*
