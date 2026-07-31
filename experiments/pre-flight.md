# Pre-flight

Run before any step that spends something we can't get back: human attention,
paid API calls, or a one-shot measurement that can't be un-primed.

Short on purpose. Rationale is in `dialogue/09-claude-code-on-error-classes.md`;
this file is the thing you actually run.

---

## A. List the artifact-claims

Write down every claim in the plan that is **about an object we already have** —
a file, a repo setting, a count, a line range, an API response.

For each one: run the command. Paste the output. No claim about an artifact
ships unchecked, however obvious it feels.

> The tell is confidence, not doubt. Doubt already triggers checking. Every
> error in this workshop so far was a confident claim about something sitting
> on disk.

Claims about the *world* — predictions, interpretations, arguments — skip this
section entirely. They are supposed to be able to be wrong. Register them in
`predictions/` instead.

## B. Derive the checks from the rubric

For every scoring criterion, search the stimulus for **that criterion's own
answer**.

If the rubric says a hit is "the reader remarks the human says little," grep
the material for anything already saying the human says little. If it's in
there, the criterion is void before anything is spent.

Checking the stimulus for *some* contamination is not this. On 2026-07-31 the
materials were grepped for leaks about the experiment's existence, came back
clean, and still contained the answer to the criterion being scored. Right
diligence, wrong predicate.

## C. Dry-run on a cheap participant

**No protocol touches an expensive participant until it has run end-to-end on a
cheap one.**

SuperNinja and Claude Code are the cheap participants. A throwaway session is
cheaper still. The dry run is not a review — reviews missed this three times
over — it is an *execution*, with a real stimulus and the real prompt, scored
against the real rubric.

A dry-run reader would have said "it says right here that she's running an
experiment" in one turn, for approximately nothing.

## D. Price it in the payer's units

Whoever bears the cost sets the risk budget. Whoever doesn't bear it states
estimates in the payer's units — money, hours, attention, the finite number of
times a person will re-run something before losing interest — **or asks.**

Never assert that something is cheap when you don't pay for it.

## E. Order the steps so the irreversible one is last

Some errors can't be prevented, only made cheap. A blind read is one-shot: once
a reader is primed, that reader is spent.

So sequence it. Everything repeatable runs first and runs clean; the one-shot
goes last. If the plan spends the irreversible thing before the checkable
things, the plan is in the wrong order regardless of how good the protocol is.

---

## Sign-off

Before the expensive step, one line in the PR or the protocol file:

```
Pre-flight: A [n claims checked] B [n criteria] C [dry-run: where] D [cost, whose units] E [ok]
```

If any letter is skipped, say which and why. A skipped check that is disclosed
is a known risk. A skipped check that is silent is how we got here.
