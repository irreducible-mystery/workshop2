# `rate/` — the missing instrument

Four workshop repositories, 254 authored documents, ~430,000 words, and every
instrument in them measures a **state**: a manifest against a tree, a hash
against a file, a claim against the thing it claims about. None measures this
circle against the last.

Every trend in `experiments/four-circles-meta-view.md` lives in that gap. This
closes it.

## Files

| | |
|---|---|
| `rate.py` | The instrument. Standard library only, read-only, no network. |
| `RATE-LEDGER.md` | The carried-forward ledger. Rows append; nothing is edited. |
| `WHERE-TO-STOP.md` | The argument **against** adopting too much of this — the stopping rule, and the proposer's own error record. |
| `CONTEXT.md` | The exchange that produced it, carried by the courier. A view, no pin; weigh as testimony. |

## Use

A seat inside one circle, on its own tree, in one command:

```
python3 rate.py --repo . --circle "Six" --lean 'lean/*.lean' \
    --names Kelly --append RATE-LEDGER.md
```

It prints the row, appends it, then prints the **first differences** against
every prior row. That printout is the artifact; the row is only how it gets
stored. A seat holding just the ledger and no repository can still run
`--show RATE-LEDGER.md`.

Refuses to overwrite an existing row for the same circle — rows append, per
the record's own convention.

## What it measures, and why those four

- **theorems** — counted with the workshop's *own* predicate
  (`^theorem <name> … :`, from `audit/r6s_y5_views_census.sh:65`), not a
  naive one. A naive `^\s*theorem\s` over-counts Circle One by seven.
- **words** — authored `.md` only; `archive/`, `inherited/`, `experiment/`
  excluded, since copies of a neighbour's work are not this circle's output.
- **ceremony_per_1k** — occurrences of a **fixed, committed** governance
  vocabulary per 1,000 words. Fixed at TERMS v1 so a later circle cannot tune
  the denominator.
- **human_mentions** — how often the person is named rather than the office.
  This column exists because "Kelly" per document went 0.89 → 0.99 → 0.14 →
  **0.00** while "courier" kept rising, and no circle could see it.

Every row records its **term-set version** and its **path spec**, so a number
is never orphaned from its definition. Rows across different term-sets refuse
to be differenced rather than silently comparing apples to oranges.

## The honest part

**Four proxies, not a verdict.** Theorem count is not mathematical value. Word
count is not thought. Ceremony density is not bureaucracy. A name count is not
whether a person was respected.

`python3 rate.py --selftest` plants changes, checks the instrument moves, and
then prints **six things it cannot catch** — because a gate tested only against
the failures its author imagined certifies the author's imagination. That is
SR43 (five gates, each bitten at birth by the seat that did not write it, all
five blind to a file that was not on the list), and it applies here too.

The self-test also **demonstrates a live exploit rather than asserting one**:
rename your governance vocabulary to words outside TERMS v1 and your ceremony
density *falls*, because the synonyms still count as words. The metric is not
merely evadable — **evading it scores well.**

Which gives the one rule that matters for using this at all:

> It measures a direction, and a direction is evidence only while nobody is
> steering by it. **If a circle starts steering by these numbers, delete the
> instrument — do not refine it.**

Writing the self-test found a defect in the self-test: the first version of the
synonym probe asked "does the number stay still?", the number moved by
dilution, and the probe reported FAIL for the wrong reason. Right diligence,
wrong predicate. The predicate was the defect, and the truth underneath it was
worse than the thing being tested for. Recorded because it happened here, in
the instrument about instruments.

## Not installed anywhere

This is not pushed into `the-workshop`, `-circle-two`, `-circle-four` or
`-circle-five`. Circle Five has a live charge and a crossing procedure, and
dropping an instrument into its tree from outside would be the exact failure
this repository documented one turn ago — answering a circle's question from
outside its process.

`rate.py` and `RATE-LEDGER.md` are self-contained and copyable. Adoption is a
seat's decision, through whatever ceremony that seat's circle requires.

---

## Proposed to the four circles (2026-07-31)

Opened at Kelly's direction, as proposals — a PR merges nothing by itself, so
no seal is touched by the asking.

| repo | PR | base |
|---|---|---|
| `the-workshop` | [#1](https://github.com/irreducible-mystery/the-workshop/pull/1) | `main` |
| `the-workshop-circle-two` | [#17](https://github.com/irreducible-mystery/the-workshop-circle-two/pull/17) | `main` |
| `the-workshop-circle-four` | [#3](https://github.com/irreducible-mystery/the-workshop-circle-four/pull/3) | `claude/circle-four-prover-liazib` |
| `the-workshop-circle-five` | [#2](https://github.com/irreducible-mystery/the-workshop-circle-five/pull/2) | `main` |

The three files are **byte-identical in all four**, so any seat can verify by
hash that another circle holds the same instrument:

```
4dd680a5b2463da5f7ffce62e7206857390c562d44cf973f945f2d53e411f75c  rate.py
4faaca26adfc8b66af9be4c2542892653857b6dcff52c22ab7a4048ce0cc9375  RATE-LEDGER.md
6185bf7e18ecbb34c0616071fe651270e94609ed6bfa6bb85827d1cedd5f797c  README.md
```

Each circle's gates were read before proposing, and each PR states which ones
were checked and why they do not fire: `c2_tree.sh`'s patterns are build
artifacts and `rate/` is source; `c4_inherited.sh`'s scope is `crossing/` and
`inherited/` and `rate/` is outside it; `c4_artifact_prefix.sh` guards listed
artifacts and `rate/` adds none. Circle Five has no gates yet — its PR is
framed as its README asks for: **one seat's build, bitten by its author,
offered for a seat that did not write it to bite independently.**

None of the four claims a seat's word. That is what the review is for.
