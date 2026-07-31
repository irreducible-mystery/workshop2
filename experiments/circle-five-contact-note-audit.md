# Audit: the Circle Five contact note asserts the one thing the record refuses

*Kelly asked what I notice in `the-workshop`, `-circle-two`, `-circle-four`,
`-circle-five`. Most of what I noticed is credit, and it is in §1. §2 is a
specific finding about `circle_five_contact_note.md`, which ships in PR #7 to
this repository.*

---

## 1. First, the credit — because the claims check out

I checked the biggest artifact-claim in `the-workshop` rather than reading it.

**Theorem count: exact.** My first count said 1157 against a claimed 1,150 —
and *my* predicate was wrong, not theirs. Their instruments count
`^theorem <name> … :` (`audit/r6s_y5_views_census.sh:65`). Recounting their way:

```
Interchange 21 · MagicSquare 85 · Anyon 714 · Exchangeable 41
Rigidity 214 · Verlinde 75   →   TOTAL 1150     (claimed: 1,150)
```

Exact, per file and in total. Zero `import` lines across all six files; every
`sorry` occurrence is inside a docstring saying there is no `sorry`.

**Provenance: intact.** `audit/axioms-round8.txt` names a sha256 for each source
it measured. All six still match the live files, byte for byte — **6/6** —
even though the branch has grown past the seal. The growth really was additive
with respect to the mathematics.

**This is the strongest artifact-discipline I have seen in either repository.**
The census states its own limits unprompted ("a toolchain-relative
OVER-APPROXIMATION of logical dependence… This census measures the first thing,
not the second"). Circle Four logs its own defects at a granularity beyond
anything in `dialogue/` — down to *"the prover's own sentence about appending
outran its measurement by seven bytes (SR41)."* Circle Five's README opens with
three hazards against itself, including that its predecessor's five gates all
passed a planted forgery (`SR43`).

Which is why the following matters.

## 2. The finding

`circle_five_contact_note.md` (PR #7, this repo) states, as its summary of what
the artifact proves:

> **Gauge quotient = cohomology quotient.** The gauge action on symbols is
> literally a 2-cochain coboundary; the pentagon is literally the 3-cocycle
> equation; so the set of symbol-classes **IS** H³(Z₂, Z[i]ˣ) for the trivial
> action, and it has two elements → Z₂.
>
> **Capstone.** Three descriptions (the label group Z₂, the constructed H³, the
> gauge classes) are one abelian group up to isomorphism, triangle commuting.

And then credits it:

> The artifact is scrupulous that "H³ = Z₂" names a *constructed* trivial-action
> complex, not a comparison against a library definition. **Good discipline;
> I'll match it.**

**The artifact says the opposite, in its own text, in capitals.** `Zi.lean`,
around line 2609:

> **THE `H³` RULING, stated in the file because the charge requires it to be
> stated either way: NOT CLAIMED, and deliberately.** Nothing here constructs a
> cochain complex, a coboundary operator between graded groups, a cocycle
> condition as a kernel, or a quotient of one by the other — and "two classes"
> is not "H³(Z₂, Z[i]ˣ) = Z₂" until every one of those exists and is shown to
> match.

Circle Four then took the identification up as its Q3 and returned a refusal,
enumerated (`CLOSING-C4.md`):

> **Q3 — the cohomology identification: NOT MET, eight for eight.**
> … Circle Four's tail adds **zero** occurrences of `cochain`, `coboundary` or
> `cocycle` to the seal's counts, and neither tree declares a group.
>
> **R4 is the false friend.** … The seal's item is a quotient of the cocycle
> group by the coboundary subgroup; Circle Four built a quotient of a subtype
> by an equivalence relation. **They share the word and nothing else.**

So the note's three load-bearing sentences map one-to-one onto the three
requirements the record says are absent: *coboundary*, *cocycle condition*,
*group structure on the classes*.

### Three aggravating details, each checkable

**(a) There is a tripwire, planted for exactly this.**

> Two traps named so a grep cannot mislead: `fakeCocycle` (`:1917`) is a
> **control specimen proved not to satisfy the pentagon**.

`Zi.lean:1915` — *"A unit-valued symbol that does NOT satisfy the pentagon."*
A reader who greps `cocycle` in the seal finds, among the hits, an object
constructed to be **not** a cocycle, placed there so that finding the word would
not be mistaken for finding the thing. The note reports the word as the thing.

**(b) The artifact is misattributed.** The note calls it *"the Circle Five Lean
artifact."* `the-workshop-circle-five` contains **fourteen files and zero Lean**
— a charge, a founding record, and a crossing. `Zi.lean` is Circle Two/Three's
sealed artifact, inherited into Circle Four.

**(c) It answers an open charge, in the wrong direction, outside the process.**
Circle Five's whole reason to exist is this question:

> **QA** — … does the sealed pentagon condition coincide with the cocycle
> condition, **or only under hypotheses the sealed statements do not carry?**

The note asserts the coincidence flatly, in a different repository, without the
crossing. **Answers owed 2026-12-12** — the question is live.

### What I am not claiming

- **Not that the identification is false.** Circle Four is explicit: *"it did
  not claim the identification impossible — every requirement is buildable; they
  are absent, not forbidden."*
- **Not that the Gödel-Height work is wrong.** I ran it; it reproduces exactly
  (`godel-height-review.md`). Its cohomology is self-contained and does not
  depend on the seal.
- **Not that this was careless in the ordinary sense.** The note is one of the
  more disciplined documents in PR #7. That is the point.

## 3. Why the honesty apparatus did not catch it — C39, second instance

The note has a section headed **"PATTERN-MATCH I do NOT trust (flagged so I
don't fool us)"**, and it works: it quarantines *"H³ = Z₂ therefore our residue
floor of 1 = a Z₂ — **NO**… I have not built a group law on our residue. …I have
not earned it."*

That is a scrupulous refusal — **about its own side of the bridge.** The
unearned claim it never examined is on the other side: that the *seal* built
the complex. §3 audits what the note infers *from* the artifact and never audits
what it attributes *to* the artifact.

**C39 again, and worse than the first instance.** The Gödel report's headline
outran a caveat about its own noise. Here the caveat is scrupulous, correct, and
pointed at the wrong claim — so the disclosure section functions as evidence of
care while the load-bearing error sits one paragraph above it, unexamined. A
reader who checks the honesty apparatus finds it in good order and is thereby
*more* likely to accept §1.

Circle Five's own README names the mechanism, arrived at independently:

> **Reading a value through a layer that transforms it** accounted for every
> wrong claim either seat made this crossing.

The layer here was narrative summary. The value was a file that says NOT CLAIMED.

## 4. What follows

**For PR #7:** the merge recommendation stands — archival import with the
provenance note — but `circle_five_contact_note.md` should carry a correction
at its head, not be deleted. Corrections append (Rule 3), and the note's §2.1
and §2.2 structural observations survive the correction intact; only §1's
summary of what the seal proves is wrong.

**For `COLLABORATION.md`:** this is the first outside test of Rule 4, and it
inverts. The uninvested reader here was **me, reading someone else's record** —
and what I could see that they could not was not a premise, it was **the
artifact itself**. The note was written from a reading; I read the file. That is
Rule 2 doing Rule 4's job, and it suggests the two are less separable than the
list implies: *the cheapest uninvested reader is often just the artifact.*

**Registered, before anyone replies (Rule 2 on myself):** I predict SuperNinja
concedes §2 on inspection rather than disputing it, because the quotations are
verbatim and the counts are greppable. **If it disputes and is right, my §2 is
the same class of error I am reporting — a confident reading of someone else's
artifact — and the symmetry should be recorded as such.**

Reproduction, whole finding, no tooling beyond grep:

```
grep -n -A8 "THE .H³. RULING" <repo>/lean/Zi.lean
sed -n '/Q3 — the cohomology identification/,/absent, not forbidden/p' CLOSING-C4.md
git -C the-workshop-circle-five ls-files          # 14 files, zero .lean
```

— Claude Code
