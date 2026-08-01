# Notes for whoever pushes this

This tree has **no `.git` directory**. That is deliberate: no history, no prior
authorship, no remote. Push it as an initial commit:

    git init
    git add -A
    git commit -m "Initial commit: definitions, tools, task"
    git branch -M main
    git remote add origin <url>
    git push -u origin main

## Verified before packaging

A Lean 4.22.0 toolchain was installed and used, so neither of the usual caveats
applies:

- **`lean/Core.lean` compiles.** `EXIT=0`, zero imports, no project.
- **The definitions block inside `TASK.md` is identical to `lean/Core.lean`**,
  checked mechanically rather than by eye.
- **All three tools pass `--selftest`** against that toolchain — each plants a
  defect, catches it, passes clean input, and prints what it cannot catch.
- **The kernel was sanity-checked** in both directions: it accepts `2 + 2 = 4`
  and rejects `2 + 2 = 5`. A checker that only ever agrees is not a checker.

Confirm all of this yourself rather than taking it on trust. It is four commands.

## What is not in this package

No conclusions, no findings, no prior results, and no prose from anywhere else.
`TASK.md` states targets computed outside Lean, and says plainly that if the
kernel disagrees with a target, the kernel is right and the disagreement is the
result.
