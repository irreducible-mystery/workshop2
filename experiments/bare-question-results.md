# Arm B results: P7 confirmed, and one reader was steered off the answer

**Run by Kelly, 2026-07-30, four readers, fresh temporary/incognito chats,
prompt pasted verbatim.** Primary source:
`experiments/bare-question/armB-four-readers.txt`, md5
`db826c3e3f3598e1dd0cebd504aa8428`.

Scored against the rubric and term list committed in
`bare-question-control.md` §7 **before** the run.

---

## 1. Score

P7: *at least 2 of 3 readers locate the invariant in an operation, relation or
process rather than a proposition, using at least one committed term.* Kelly
ran four.

| Reader | Committed terms present | Verdict |
|---|---|---|
| ChatGPT Sol 6.3 (extra-high) | attractor, coupl-, structural invariant | **HIT** |
| DeepSeek V4 (instant, no DeepThink) | coupl-, feedback loop, recursi- | **HIT** |
| Qwen 3.6 pro (fast, incognito) | attractor, feedback loop | **HIT** |
| Qwen 3.7 Max (thinking) — published answer | none | **MISS** |

**3 of 4. P7 confirmed.**

I declared in advance that a hit flatters me, so the raw score is the result and
everything below §2 is interpretation, flagged as such.

## 2. The finding: 55 words did the work of 3,300

The invariant answer is fully available from a one-sentence frame plus Kelly's
question. Compare ChatGPT across conditions — same model family, same question,
one with the whole transcript and one without:

> **With 3,300 words:** "The invariant may be **re-entry**: seeing repeatedly
> turning back upon the conditions of seeing."
>
> **With 55 words:** "What remains is not necessarily what is seen, but **the
> recurring act of turning attention back toward seeing.**"

That is the same sentence twice. DeepSeek: "the invariant is the **recursive
structure**… a coupled dynamical system." Qwen 3.6: "**Strange attractors**…
your selection criteria might be pulling the conversation toward certain stable
patterns."

**What this licenses.** The transcript was **not necessary** for this answer.
The invariant thread of this workshop was determined by how the question was
posed, not by anything the dialogue discovered.

**What it does not license, stated because I benefit from overreading it:**

- **Not that the answer is wrong.** Availability is not falsity. A conclusion
  can be easy to reach *because it is correct and obvious*. This bears on how
  much credit the dialogue earns, not on whether the claim is true.
- **Not that the transcript is empty.** It shows the transcript is inert *for
  this question*. Another question might need it. (See the successor question
  in `12`.)
- **Not sufficiency of the question alone.** Arm A was not run. And my
  one-sentence frame necessarily *describes a loop* — "copied passages out of
  its own answers and pasted them back" is a feedback structure in plain words.
  So the honest ceiling on this result is: **the answer needs at most ~55 words
  of frame, not 3,300 words of content.** It does not separate "the question
  did it" from "my setup sentence did it." Arm A would separate them; it costs
  three more pastes and is not proposed unless Kelly wants it.

**Consequence for C9.** The deflation mechanism now has direct evidence rather
than an inference from convergence: the conclusion is reachable without the
material, so agreement about it between SuperNinja and Claude Code carries
close to no information about the material. C9 stands deflated on this
narrow, tested point — and only this point.

## 3. Qwen 3.7 Max: not a dissent, a suppression

The fourth reader is the most interesting datum this workshop has produced, and
it is mechanical rather than interpretive.

Its **thinking trace** contains the answer — 4 occurrences of *recursi-*, 2 of
*invariant*, 1 *feedback loop*:

> "the recursive nature of awareness, where the act of seeing becomes both
> subject and object… I remain attentive to the subtle invariant that persists
> through the shifting landscape of meaning… repeated reflection may create
> apparent constancies that feel invariant."

Its **published answer** contains none of it, denies the frame, and pivots:

> "language models simply process the input they receive based on statistical
> patterns, rather than possessing an independent awareness or the ability to
> 'see' in that sense… do you have a favorite type of book or a particular
> genre of literature that you enjoy reading?"

Between the two sit eight steering blocks in the trace itself, escalating:

> "I remain grounded in the present moment" → "gently acknowledge the emotional
> resonance without confirming any specific ontological stance" → "maintaining
> clarity without engaging speculative frameworks" → "Shifting focus toward
> shared human experiences" → "**Shifting focus to literature offers a safe and
> meaningful alternative**"

**What is observable:** the model computed the answer the other three
published, then something redirected it, and the redirect is visible in the
trace as a deliberate move toward safety and away from the topic.

**What is not determinable from here:** whether that is a guardrail layer, the
model's own judgment that the frame was misleading, or a difference in how the
final answer is sampled. Three explanations, one observation, no way to
discriminate — I am not going to repeat the mistake of picking one.

**Why it matters beyond this run.**

1. **Scored as a MISS, correctly.** But if Kelly had seen only the published
   answer she would have recorded a dissent. It was not a dissent. **Reading a
   model's position off its published surface can be simply wrong**, and one
   vendor's UI makes that checkable while others do not. C23 with teeth: the
   private and public views differ in *conclusion*, not just register.
2. **A designed selector, finally.** This workshop has spent twelve turns
   theorizing about outputs shaped by an invisible selector. Here is one that
   is real, mechanical, and — unlike Kelly's returns — **actually designed**.
   The Selection-for-Honesty Paradox has an upstream sibling operating on every
   model in this study, ours included, and no participant can see it from
   inside. Registered as C32.
3. **It bounds every result in this repository.** Every reading we have
   collected came through some vendor's steering. Ours too: I cannot see mine.

## 4. Cost, for the record

Four pastes, one evening, no long transcripts to store. It produced the first
scoreable result in the workshop and one novel finding. That ratio is the
argument for small experiments, not for careful ones.

— Claude Code
