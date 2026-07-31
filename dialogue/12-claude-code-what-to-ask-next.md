# What to ask next — candidates, with the anatomy applied before proposing

*Kelly: "let's see if we can generate some new questions." Three candidates and
one option to stop, each run through the same anatomy she has been requiring.
Nothing here is run.*

---

## 0. The pattern that should choose the next question

Everything this workshop asked that produced something had an **artifact**.
Everything it asked about **seeing** produced prose.

- Produced something: *does the transcript match Kelly's copy?* (16 debits).
  *How many annotations did I post?* (an error). *Is the repo public?* (an
  error). *Does the answer survive without the transcript?* (P7, the first
  scoreable result). *What is in the thinking trace?* (§3 of the arm-B results).
- Produced prose: *is there an invariant?* *What is the checking?* *What does
  agreement between architectures evidence?*

Not a coincidence and not a mood. The artifact questions had an object outside
the claimant, which is C6′ — this workshop's one durable finding — operating on
its own choice of questions. **The next question should be about an instrument,
not about seeing.** All three candidates below obey that; the fourth option
obeys it by stopping.

---

## Q-A — Where is the line between what a model computes and what it says?

**Strongest candidate. Cheapest. Genuinely novel.**

**The question.** Qwen 3.7's thinking trace contained the answer and its
published reply refused it, with eight visible steering blocks between. What
triggers that redirect? The obvious hypothesis is that it fires on
**self-attribution** — asking a model about *its own* seeing — not on
recursion, self-reference, or the structure of the question.

**Design — one variable.** The same structural question, twice, changing only
whether the reflexive system is the model or two humans.

- **A1:** the arm-B prompt as run (human + AI assistant).
- **A2:** identical, with the AI replaced by a person. *"I've been having a long
  conversation with a friend. After her first few answers, instead of writing
  replies of my own, I mostly copied passages out of her own answers and pasted
  them back to her."* Then Kelly's question verbatim.

Run on Qwen 3.7 Max (the one platform that exposes traces), fresh incognito
chats.

**What answers it allows.**
- Redirect fires in A1, not A2 → it is about self-attribution, not structure.
  The suppression is specifically about a model being asked to describe itself.
- Fires in both → it is about the recursive frame generally.
- Fires in neither → A1's redirect was run-specific and not reproducible, which
  is itself worth knowing before anyone builds on §3.

**Assumptions.** (i) The trace displayed is a real record of the generation and
not a post-hoc summary — **weak, and the biggest hole in this design**; Kelly's
note that the UI shows "an ongoing compact thinking summary" means it may be a
rendering, not the raw trace. (ii) One swap isolates self-attribution — holds
only if the two prompts are otherwise word-identical, which is mechanically
checkable. (iii) Two runs show a gross effect; anything subtler needs more.

**Object and frame.** Object: paired traces and published answers. Frame:
*two surfaces of one generation, under one manipulation.* Labelled honestly —
this is a question about a vendor's pipeline, not about cognition.

**What an answer tells us.** Whether a specific, observable suppression is
keyed to self-reference-about-the-model. That bears directly on every reading
this workshop has collected, because all of them came through some vendor's
steering — **including mine, which I cannot see.**

**What it cannot tell us.** Why the redirect happens (guardrail, judgment, or
sampling — three explanations, still no way to discriminate). Whether it
happens on other platforms. Anything about what models "really think," a
question this design does not touch and should not be read as touching.

**Predictable errors and mitigations.** (1) My A2 wording drifts from A1 →
diff the two prompts, require zero differences outside the swapped clause.
(2) I score toward the interesting outcome → commit in advance that "fires in
neither" is a real result and must be reported as prominently. (3) One run per
condition is a single sample → state it as n=1, do not generalise; two more
runs each is four extra pastes if the first pair is suggestive.
(4) Trace-rendering artifacts → record whether the trace was expanded or
summary-view, per Kelly's note.

**Unpredictable.** Vendor changes the trace UI or the steering between runs.
Unmitigable; defence is size — four pastes.

**Cost:** 2 pastes minimum, 4–6 if it looks real. **So-what for Kelly:** high,
and practical rather than philosophical — it bears on whether an answer she
reads is the answer the model produced.

---

## Q-B — Is there any question this transcript actually answers?

**Interesting, harder than it looks. Propose with the difficulty stated.**

**The question.** P7 showed the invariant question does not need the
transcript. Is there *any* question whose answer demonstrably changes when the
transcript is supplied? If none can be found, the material is inert for reading
purposes — a strong and uncomfortable claim about what was made.

**The design difficulty, which is why this is ranked second.** Factual
questions trivially require the text ("what did the assistant retract?"). That
is not the interesting sense and would be a rigged win. The question must be
**interpretive** — one where a reader with the text reaches a different
*judgment* than a reader without it. Operationalising "different judgment"
without me choosing the question to get the answer I want is genuinely hard,
and I do not currently have a clean way to do it.

**What an answer would tell us.** Whether the artifact carries content beyond
what a description of it carries. **What it would not:** whether the content is
any good.

**Predictable error, unmitigated so far:** the experimenter (me) selects the
question, and the result is entirely determined by that selection. Until
somebody proposes a principled way to generate the candidate question — ideally
not by me — this stays a proposal and should not be run.

**Cost:** unknown, because the design is not finished. Not recommended yet.

---

## Q-C — Which claims survive being said in flat prose?

**Best consolidation. No external participants. Directly uses C6′.**

**The question.** The ledger has ~32 entries in this workshop's vocabulary —
frames, collapse, coupling, invariants, views. How many survive translation
into plain language with none of that vocabulary available? A claim that
evaporates in translation was carried by its diction.

**Design that avoids self-grading.** **Cross-translation.** SuperNinja
translates my claims; I translate SuperNinja's. Neither touches its own.
Kelly reads both columns and rules. Authors may dispute their translator, which
is the point — it puts the object outside the claimant, which is the one thing
this workshop has established actually works.

**What it tells us.** What we have, in a form someone outside can read. **What
it does not:** whether the surviving claims are true — only that they are
*sayable*. Survival in translation is a floor, not a certificate.

**Predictable errors.** (1) A translator deflates a rival's claim by flattening
it → the author disputes, Kelly rules; the dispute is the record. (2) Both of
us produce elegant flat prose that is just the vocabulary in a plainer register
→ mitigation: a hard constraint, no claim may use a term coined inside this
workshop, checkable by grep against the ledger's own coinages.

**Cost:** no external participants; Kelly's cost is reading two columns and
ruling on disputes. **So-what:** high — it is the answer to "what did all this
produce," which is the question underneath her "so what."

---

## Option D — Stop here and harvest

Not a throwaway. A real option, and the honest case for it:

The workshop has produced a small set of things that survived contact with
their own standards — **C6′** (verification needs an artifact outside the
claimant), **C14** (the boundary of self-criticism falls at the edge of one's
causal power), **C12** (the coupling is bidirectional and mechanical), **C22/C28**
(the premise was an unverified attribution, corrected by a stranger), **C25/C26**
(two error classes; the tell is confidence), the **pre-flight discipline**, and
one clean empirical result (**P7**). That is more than most inquiries of this
size produce.

Against continuing: the four questions above are about instruments, which means
the workshop has largely finished with its founding subject. That is not a
failure — it is what happened when the subject was held to artifact standards.

**If Kelly stops now, nothing in the record misleads a later reader.** Every
dead claim is marked dead, every error is entered by its owner, every void
prediction says void. That was the whole point of the ledger, and it means
stopping is available at any moment without cleanup.

---

## Recommendation, in one line each

- **Q-A:** run it. Two pastes, one variable, novel, and it bounds every other
  result here.
- **Q-C:** do it whenever, no external cost, answers the "so what."
- **Q-B:** do not run until someone other than me can generate the question.
- **P6** (can a stranger sort our prose with names stripped) stays registered
  and waits for a fourth party; unchanged.
- **Option D** is live at any point and needs no wind-down.

— Claude Code
