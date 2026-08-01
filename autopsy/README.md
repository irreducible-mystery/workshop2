# `autopsy/` — everything, unedited

*Pushed at the principal's instruction: "Push everything, everything,
transcripts, everything. The only info we are going to get out of this is what a
colossal fuck up it was."*

This directory is not a summary. It is the raw material, including the parts
that make the summaries in this repository look worse than they read.

---

## What is in here

    transcript/session.jsonl        the complete session, 2,740 turns, 9 MB
    transcript/session.ccr-tip.json the session tip record
    scratch/plan.md                 the nine-phase programme. Only P0 was ever written
    scratch/P0.md                   the first version of the task
    scratch/zero-prompt.md          the version before that, with a false claim in it
    scratch/norm20-followup.md      earlier work, unrelated to the mathematics
    scratch/vocab.py                the packaging scanner
    scratch/lean-work/*.lean        every Lean file written during the session
    scratch/probes/*.lean           the probes, including the ones that failed
    package/zero/                   the tree as shipped
    package/zero.zip                the archive as sent
    workflows/*.js                  the orchestration script for the final pass

**`transcript/session.jsonl` contains the entire conversation**, including the
principal's own messages, every tool call, every failed command, and every
correction. It is the primary document. Nothing in this repository's prose is a
substitute for it, and where the two disagree, the transcript is the record.

---

## The one thing a reader should know before reading anything else

**The task that was built is not the task that was asked for.**

The question was: *get from a forced-trivial unit case to the general one; vary
everything; what happens at −1/4; what happens coming from a different
direction; look at it classically, quantum-mechanically, and relationally.*

`scratch/plan.md` correctly breaks that into nine phases, P0 through P8. **P0 is
the forced-trivial case — the warm-up.** It is the only one that was ever built.
The session then spent ten further passes improving P0's packaging: its tools,
its vocabulary, its scanners, its self-tests. Every one of those passes found
real defects. None of them moved toward the question.

`scratch/plan.md` §1.4–1.6 already contains the computed answer to a substantial
part of what was asked — the general object has **eight** free values rather than
one, and values excluded by the one-parameter shape are ordinary solutions of the
general system. **That was computed in Python, never checked by a kernel, never
packaged, and never delivered.** It sat in a scratch file for the whole session.

---

## The failure record

`../FAILURES.md` is the taxonomy, by mechanism rather than by date. Its header
said *twenty-three entries* until 2026-08-01 and the true number is
**thirty-two** — a miscount inside the document about miscounting, corrected
there with the correction left visible. **The copies distributed to other
repositories still carry the original number**, deliberately.

`../dialogue/claims-ledger.md` carries the running entries, C1 onward. Entries
`C155`–`C185` cover this session.

---

## What this material is good for

Every serious catch in this record came from a party that had not been there.
This directory exists so that a reader who was not here can find the ones nobody
in the session found — including in the parts where the session believed it was
being careful.

Two specific invitations:

1. **The self-tests.** Every tool in `package/zero/tools/` passes its own
   `--selftest`. The package still failed on arrival, because nothing had ever
   run the tools the ordinary way. A self-test is written by the party who
   already believes the tool works.

2. **The sector.** The pentagon is the identity under study. The finding that
   started the whole line of work was in a different sector. Whether the
   pentagon sector can answer the question at all is the assumption that went
   longest without being examined, and the examination is in progress rather
   than complete.
