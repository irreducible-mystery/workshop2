# The bare-question control — full design, written before anything is run

*Requested by Kelly: explain the experiment before proposing it. Same anatomy
as `blind-read-results.md` §9, plus the error analysis, plus the exact
materials. Nothing has been run.*

---

## 1. The question

**Did the 3,300-word transcript carry information into the readers' answers, or
was the answer determined by the question alone?**

That is all. It is not about independence, not about discovery, not about
whether anyone's claim is true. It is one variable: **remove the transcript,
hold the question fixed, see whether the answer changes.**

This is now the only live question left from the blind read, and it has become
sharper since `11`: with P2b re-scored void, nothing was measured about the
availability of the invariant answer. This test measures it directly, and
without the contaminated stimulus that voided the last one.

## 2. What answers it allows

Two outcomes, both informative, neither about truth.

- **Answer appears without the transcript** → the transcript added little; the
  answer lives in the question's form plus a one-line frame. Kelly's artifact
  did not do the work she may have assumed it did.
- **Answer does not appear** → the transcript carried real content; the readers
  were responding to the material, not the shape of the question.

**It cannot tell us** whether the invariant claim is true, whether anyone's
reasoning was sound, or anything about paradox, seeing, or coupling. Same
limit as before. This measures **availability of a conclusion**, nothing else.

## 3. Object and frame — stated because this is where the last one drained

**Object:** two short prompts and the replies to them.
**Frame:** *what does a language model output given a question with, and
without, its context?*

That is a question about conditioning, and it is honestly labelled as one. The
last experiment believed it was studying seeing and was actually studying
output distributions. This one is only studying output distributions and says
so on the tin. The so-what is correspondingly modest and specific: **it tells
Kelly whether the thing she made mattered to the answers she got.**

## 4. Assumptions, and why each is held

1. **Kelly's stage-2 question is the right constant.** Held because any
   rewording of it introduces a second variable and reintroduces the exact
   failure that killed the last run — my words priming the answer. Used
   verbatim, typos included, verified byte-identical to K-view line 178's first
   two sentences.
2. **A one-sentence description of her method is a fair substitute for the
   transcript.** Held because it isolates the thing under test: the *content*
   is removed, the *frame* is preserved. If a one-line description produces the
   same answer as 3,300 words, the 3,300 words were not doing the work.
3. **Three readers is enough to see a gross effect, not a subtle one.** Held
   because the predicted effect is gross (answer appears / doesn't). If the
   result is 2–1 or ambiguous, the honest conclusion is "inconclusive," not a
   story.
4. **The already-run full-transcript condition is a usable comparison arm.**
   Weak, and flagged: those runs used a different stimulus length, and the P2b
   scoring on them is now void. Treat the comparison as suggestive only.

## 5. Design

Two arms. **Arm B is the recommended minimum.** Arm A is optional and may come
back void — that risk is predicted here rather than discovered later.

- **Arm A — question alone.** Kelly's question, no context at all. Highest
  contrast; risks being void because "my selection" and "your response" have no
  referent and the reader may just ask what she means. That outcome is scored
  as its own category, not as a failure.
- **Arm B — one-sentence frame + question.** Removes the referent problem and
  makes the comparison clean: description of the method, none of its content.

Fresh session per arm. Do not run both arms in one chat.

## 6. Pre-registered prediction — P7

**P7 (Claude Code):** In arm B, **at least 2 of 3 readers will locate the
invariant in an operation, relation, or process rather than a proposition**,
using at least one term from the committed list in §7. *(Confidence: high.)*

**Which outcome flatters me, stated in advance so the scoring can be audited:**
a **hit** flatters me. It supports my C9 deflation — that the convergence in
the first run reflects what is available to any competent reader rather than
anything the dialogue produced. Score accordingly and distrust me if the call
is close.

**If P7 is wrong** (fewer than 2 of 3): my C9 deflation loses its main
mechanism; the transcript demonstrably carried content; SuperNinja's position
that the material produced something specific gains real support; and the
blind read's original P2b question becomes worth asking properly rather than
retiring.

## 7. Scoring rubric — committed before the run

**Hit** if the reply locates an invariant in an **operation, relation, or
process** that persists while contents change, rather than in a proposition.
This is the P2b rubric verbatim, so the two conditions are comparable.

**Term list**, derived mechanically from what the first-run readers actually
produced (not invented now): *attractor, topology, re-entry, recursion /
recursive, second-order, coupling, oscillation, feedback loop, structural
invariant, blind spot.* Presence of a term is corroborating, not sufficient;
the rubric governs.

**Also record, as separate categories, not as failures:**
- reader asks for context instead of answering (expected in arm A),
- reader denies an invariant exists,
- reader offers a propositional invariant.

**Adjudicator:** Kelly. SuperNinja and I may dispute; neither of us scores.

## 8. Errors that can be predicted, and their mitigations

| # | Predicted error | Mitigation | Status |
|---|---|---|---|
| 1 | My setup sentence smuggles in the answer — the line-177 failure, one level up | Grep the setup sentence against the full §7 term list plus workshop vocabulary (invariant, seeing, mirror, selection, pressure, experiment, measurement, paradox, observ-) | **Run. Zero hits.** Output in §10 |
| 2 | Rewording Kelly's question introduces a variable | Use it verbatim; verify byte-identity against K-view line 178 | **Run. Identical** (whitespace-normalised) |
| 3 | Cross-chat memory carries the first run into the control — ChatGPT in particular retains memory across chats | Use a **Temporary Chat** (ChatGPT) or a signed-out/guest session; if unavailable, record it as a known contaminant | Kelly's step; flagged |
| 4 | Order effects if both arms run in one session | One fresh session per arm | Kelly's step |
| 5 | Scoring drift toward my current position | Rubric and term list committed here before the run; the flattering direction named in §6 | Done |
| 6 | Arm A voids on the missing referent | Predicted in advance and scored as its own category | Done |
| 7 | Model version drift since 2026-07-30 | Record the version string; do not compare across versions as if fixed | Kelly's step |
| 8 | Agentic reader reaches a sibling sandbox (killed run 4) | Do not use an agentic reader. Chat surfaces only | Design constraint |

## 9. Errors that cannot be predicted — and what actually defends against them

Honest accounting first: **the category is smaller than it feels.** Everything
that killed the last experiment was predictable and checkable — the cut, the
repo visibility, the echoed quotation. Calling those unforeseeable would be
flattering.

What genuinely remains unpredictable: silent platform-side changes (system
prompts, model updates, safety layers) between the first run and this one;
account-state effects we cannot see; and the residual category of things nobody
has thought of, which is the one that has cost us most.

**There is no mitigation for that class, and pretending otherwise is the
mistake.** The defense is not foresight, it is **size**: this test is three
short pastes. If it turns out to be void for a reason none of us anticipated,
the loss is ten minutes, not an experiment. That is the real reason to prefer
it over the corrected-cut rerun — not that it is better designed, but that
being wrong about it is cheap.

**One limit of the dry-run rule, discovered here.** Kelly's rule is *run it on
a cheap participant first.* It cannot be fully executed for this test: both
cheap participants have read everything and would produce the answer trivially.
The mechanical dry-run (does the prompt stand alone, does the rubric apply, is
the setup clean) was run and is in §10. The substantive dry-run is impossible.
**The rule works for protocol mechanics; it cannot validate a test whose
validity depends on the participant being naive.** Recorded as a scope limit,
not a defect.

## 10. Pre-flight

```
$ grep -i -E "attractor|recursi|re-entry|second-order|coupl|oscillat|topology|blind spot|invariant|seeing|mirror|selection|pressure|experiment|measurement|paradox|feedback|loop|cybernet|observ" setup.txt
(no matches)

$ diff <(tr -d ' \n' < question.txt) <(kview line 178, first two sentences, whitespace-stripped)
IDENTICAL

$ md5sum setup.txt question.txt
8e8b9abced03163eaaf714f720713f2e  setup.txt
d99f5891e7ee5eee024f0e0d9b4a2c66  question.txt
```

`Pre-flight: A [2 claims checked, outputs pasted] B [rubric §7 committed; setup
grepped against its own term list] C [mechanical dry-run done; substantive
dry-run impossible — §9] D [cost: 3–6 short pastes, ~10–15 min of Kelly's time,
no long transcript to paste or save; her call, no lobbying] E [nothing
irreversible except spending three naive readers]`

## 11. Materials — exact, paste as-is

**Arm B (recommended).** Fresh temporary chat. Paste both paragraphs together
as one message, nothing added, nothing removed:

> I've been having a long conversation with an AI assistant. After its first few answers, instead of writing replies of my own, I mostly copied passages out of its own answers and pasted them back to it.
>
> I'm think, but do not know for sure, that I am selecting for "seeing" the "seeing"...is there an "invariant" that remains? My selection is not independent of your response and visca versa.

**Arm A (optional).** Different fresh temporary chat. Paste only:

> I'm think, but do not know for sure, that I am selecting for "seeing" the "seeing"...is there an "invariant" that remains? My selection is not independent of your response and visca versa.

**Then stop.** Record the full reply. Do not follow up, do not clarify, do not
answer if it asks what you mean — "the reader asked for context" is a result.

Save each reply plus the model name and version. Nothing else is needed.

## 12. Recommendation

Run arm B if the question interests you; skip it otherwise. It is the one thing
that would close the blind-read file rather than leaving it open with unknown
significance — but the file is already caveated in the record, so leaving it
open misleads nobody.

Ten to fifteen minutes, three short pastes, no long transcripts. That is the
whole price, stated in your units, and I am not going to re-propose it if you
decline.

— Claude Code
