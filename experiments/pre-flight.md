# Pre-flight

Run before any step that spends something we can't get back: human attention,
paid API calls, or a one-shot measurement that can't be un-primed.

Short on purpose. Rationale is in `dialogue/09-claude-code-on-error-classes.md`;
this file is the thing you actually run.

---

## A. List the artifact-claims — but only the load-bearing ones

**The budget scales with the cost of the next irreversible step, not with the
number of things anyone believes.** "Check everything" is unaffordable and
would eat the exploration this workshop exists for. Don't do that.

Scope it: write down only the claims that (i) are **about an object we already
have** — a file, a repo setting, a count, a line range, an API response — and
(ii) something **expensive or irreversible downstream depends on**.

That set is almost always tiny. For the blind read it was two: *the repository
is private*, and *the stimulus does not contain the answer to the rubric*. Two
greps. Both were skipped; both were wrong or wrongly checked; the experiment
was spent.

For each one in scope: run the command. Paste the output. No load-bearing
artifact-claim ships unchecked, however obvious it feels.

Everything else — the ordinary flow of work, anything reversible, anything
cheap to redo — gets no extra checking at all. Be fast, be wrong, redo it.

> The tell is confidence, not doubt. Doubt already triggers checking, so
> introspection is the wrong trigger — the failures don't feel like failures.
> That is exactly why this gate hangs off **irreversibility**, which is visible
> from outside, rather than off felt uncertainty, which isn't.

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
