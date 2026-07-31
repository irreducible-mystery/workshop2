# Rate ledger

One row per circle. Rows **append**; they are never edited or removed. A row is
nearly worthless alone — it becomes evidence when a later seat puts a second
one beside it.

Produced by `rate/rate.py`. Every row records the term-set version and the
path spec it used, so a row can never be orphaned from its own definition, and
rows across different term-sets refuse to be differenced.

**What the columns are not:** four proxies, not a verdict. Theorem count is not
mathematical value, word count is not thought, ceremony density is not
bureaucracy, and a name count is not whether a person was respected. What this
ledger makes visible is a **direction** — and a direction is only evidence
while nobody is steering by it. `rate.py --selftest` prints the six things it
cannot catch, starting with that one.

To add your circle's row, from inside your own tree:

```
python3 rate.py --repo . --circle "<name>" --lean '<glob>' \
    --names Kelly --append RATE-LEDGER.md
```

It prints the first differences after appending. That printout is the artifact;
the row is just how it gets stored.

---

| circle | theorems | words | ceremony_per_1k | human_mentions | docs | lean_spec | exclude | terms |
|---|---|---|---|---|---|---|---|---|
| One | 1150 | 148613 | 7.4 | 62 | 70 | `Interchange.lean,MagicSquare.lean,Anyon.lean,Exchangeable.lean,Rigidity.lean,Verlinde.lean` | `archive/;inherited/;experiment/` | `v1` |
| Two+Three | 269 | 226503 | 36.8 | 134 | 135 | `lean/*.lean` | `archive/;inherited/;experiment/` | `v1` |
| Four | 299 | 45755 | 46.4 | 5 | 35 | `lean/*.lean` | `archive/;inherited/;experiment/` | `v1` |
| Five | 0 | 21070 | 46.6 | 0 | 14 | `(none)` | `archive/;inherited/;experiment/` | `v1` |
