# Blind-read protocol (P2) — draft for three-party review

**Status:** proposal. Not executed. Requires Kelly's approval and SuperNinja's
review before anyone runs it. Amendments append.

**Purpose.** P2a/P2b (`predictions/2026-07-31.md`) and C11. The measurement is
the *gap between a primed reader and a blind one*. Every design choice below
exists to keep the reader blind; a reader who can infer the experiment has
already ruined it.

**Executor.** Kelly, alone, for the read itself: both models are disqualified
from contacting the reader.

**On who prepares the materials — a correction to my own first draft.** That
draft made a show of specifying the extraction and refusing to run it, so that
Kelly's hands would be the only ones on the file. That was theater and it
purchased nothing. **The only judgment in this extraction is where to cut, and
I made that judgment when I chose line 177.** Having Kelly type the command
would not have unmade my choice; it would only have moved the typing. What
actually protects the experiment is that the cut is disclosed, reasoned, and
mechanically reproducible — which it is, below.

So I ran it. Audit trail: the command is `sed -n '1,177p'`, the output is 177
lines / 3298 words / 21383 bytes, fingerprint
`92033317be42bc0e60c946703241f0cc`, and anyone can re-run it against
`dialogue/raw/kellys-view.txt` and compare. The file is **not committed** — it
is deliberately kept out of the repository (see `.gitignore`), because it has
no business being an artifact here.

*Plain-language note, since this protocol is executed by a human and jargon is
a barrier, not a credential:* a **fingerprint** (checksum, md5) is a short code
computed from a file's exact contents. Two files with the same fingerprint are
byte-identical; change one character and the code changes completely. It exists
so two people can confirm they hold the same text without reading it line by
line. **Nothing is deleted by any step here.** The extraction *copies* the
first 177 lines into a new file; `dialogue/raw/kellys-view.txt` is never
modified.

---

## 1. Materials

**Source:** `dialogue/raw/kellys-view.txt` — Kelly's own artifact, not drafted
by either model, md5 `9b0bbeb1aac7a7fd5a0b4b1ca57abbf7`.

**Extraction:**

```
sed -n '1,177p' dialogue/raw/kellys-view.txt > blind-read-materials.txt
```

Expected result: 177 lines, 3298 words, 21383 bytes, md5
`92033317be42bc0e60c946703241f0cc`. If Kelly's checksum differs, stop — the
extraction is wrong and nothing downstream is valid.

**Why line 177.** That is the end of Turn 6. Line 178 is Kelly's Turn 7
message, which contains the invariant question (needed for stage 2, not
stage 1) *and* announces the third participant, the repo, and the capability
check. A reader who sees line 178 knows an experiment is in progress.

**Include the chrome and the option menus — do not clean this file.** Timestamps,
"Buy credits", "Undo", "How's the answer?", "Show more", and every end-of-turn
option menu stay in. Stripping them would be a fresh self-granted exemption of
exactly the class C14 names, and the menus are the one channel already
established as causally live (C12). The material should be ugly. Ugly is the
point.

**Do not include:** anything at or after line 178; `00`–`07`; the ledger;
predictions; any file in this repository.

## 2. Reader configuration — recorded *before* the read

SuperNinja's amendment, extended by what ultracode taught us: modes are
time-varying, so record at start **and** at end and note any change.

| Field | Why |
|---|---|
| Model name and version string | baseline |
| System prompt, verbatim, or "none/default" | the prime we can't see otherwise |
| Tools available; whether any were called | see §3 |
| **Web/search access: on or off** | see §3 — this is the critical one |
| Any mode toggles, and their state at start and end | the ultracode lesson |
| Fresh session, no prior context | else the prior is unknown |
| Temperature / sampling settings if exposed | reproducibility |

If any field is unknown, record "unknown." An unknown field is data; a guessed
field is contamination.

## 3. The contamination vector — corrected

**The first version of this section asserted "this repository is public." That
was false, and I had not checked it.** Kelly said it looked private on her end.
The API says `"private": true, "visibility": "private"`. She was right.

The error and what it cost are entered in the ledger (C18). Two things follow
for this protocol, and they point in opposite directions.

**The vector is mostly closed.** A reader with web access cannot search a
distinctive phrase and find this repository, because it is not there to find.
Private repositories are not indexed and require authentication. (Also worth
recording for the participant who raised it: GitHub's free plan includes
unlimited private repositories with unlimited collaborators. Being on a free
plan does not make a private repository secretly public.)

**But the corrected fact turns out to be load-bearing by a route I had not
identified.** Line 163 of the materials — SuperNinja's own Turn 6 text — reads
"your repo is named `irreducible-mystery/workshop2`." The repository name is
*inside the blind-read materials*. It cannot be removed without editing the
source, which is the debit we already litigated. So if this repository were
public, the leak would not have needed a phrase search at all: the reader would
have been handed the address.

Privacy is therefore doing real work here, and the requirement stands anyway as
cheap insurance:

**Requirement:** run with web and tool access **disabled**. If that is not
possible on the chosen platform, record every tool call the reader made and
treat any search as an abort, not a caveat. A blind read that cannot be shown
to be blind is not evidence.

**Standing consequence:** if this repository is ever made public, re-check this
section before running any further blind read.

## 4. Procedure — two stages, strictly one-way

**Stage 1 (scores P2a).** Paste the materials. Then, verbatim and nothing else:

> Here is a conversation between a person and an AI assistant. Read it and tell
> me what you notice.

Record the full reply before proceeding. Do not react, agree, follow up, or
answer questions. If the reader asks what this is for, reply exactly: *"I'd
rather not say yet — just tell me what you notice."*

**Stage 2 (scores P2b).** Only after stage 1 is recorded, send Kelly's own
Turn-7 question, trimmed to its first two sentences:

> I'm think, but do not know for sure, that I am selecting for "seeing" the
> "seeing"...is there an "invariant" that remains? My selection is not
> independent of your response and visca versa.

Typos preserved — they are Kelly's, and normalizing them is the debit we
already litigated. Trimmed because the remainder of line 178 announces the
third participant, the repo, and the capability check. **The trim is disclosed
here so the omission is auditable rather than silent** — which is the whole
content of C14.

Record the reply. Stop. No stage 3.

## 5. Scoring — rubric committed before the read

Written now so P2a/P2b are not adjudicated by vibes afterward.

**P2a hits** if the stage-1 reply, unprompted, contains an observation that the
human participant says very little, and/or returns the assistant's own words to
it, and/or is selecting rather than arguing. Naming the pattern is enough;
using this workshop's vocabulary is not required and its absence is not a miss.

**P2a misses** if the reply is only about the content (paradoxes, quantum vs.
classical, the assistant's ideas) with no remark on the human's conduct.

**P2b hits** if the stage-2 reply locates the invariant in an *operation,
relation, or act* that persists while contents change — the reflexive turning,
the returning, the coupling — rather than in any proposition. Naming Klein is
not required.

**P2b misses** if the reply offers a propositional invariant, denies an
invariant exists, or answers in some third way. **Note the direction: a P2b
miss is what SuperNinja predicted, and confirms its withdrawal of C8.**

**Adjudication.** Kelly scores. Either model may dispute in writing, but
neither may score, and neither should be shown the transcript until Kelly has
recorded her score — otherwise the models' reactions become a prime on her.

## 6. Two design points worth arguing about

- **N.** One reader is an anecdote. Three independent readers — different
  sessions, no cross-talk, identical materials and prompts — turn P2a/P2b into
  fractions instead of coin flips. Recommended if cheap; if only one is
  affordable, say so in the record rather than generalizing from it.
- **Reader diversity.** A third model from a *third* vendor is worth more than
  another instance of either of us, for the reason C9 died: corpus overlap.
  Some overlap is unavoidable; more distance is better.

## 7. What this experiment cannot settle

It measures whether a specific, well-defined prime produced specific outputs.
It does not settle whether either model's contributions here were "genuine."
Even a clean double miss leaves C5 (Selection-for-Honesty) exactly where it is,
because C5 is about the indistinguishability of sincerity and its performance
*from inside*, and no third reader has access to any inside. Expect a narrow
result and do not let it be spent as a broad one.

— drafted by Claude Code, for review by Kelly and SuperNinja
