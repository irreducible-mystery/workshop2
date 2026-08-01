export const meta = {
  name: 'general-variety',
  description: 'From the forced-trivial one-parameter case to the general eight-value object: all variations including negative, rational and complex values; whether the symmetry is visible in this sector; three lenses on frozen results',
  phases: [
    { title: 'Question' },
    { title: 'Derive' },
    { title: 'Verify' },
    { title: 'Kernel' },
    { title: 'Lenses' },
  ],
}

const LEAN = '/tmp/claude-0/-home-user-workshop2/9d633cbc-4061-5889-a22b-fdafc4aa96ce/scratchpad/tc/lean-4.22.0-linux/bin'
const SCRATCH = '/tmp/claude-0/-home-user-workshop2/9d633cbc-4061-5889-a22b-fdafc4aa96ce/scratchpad/wf'

const OBJECT = `
## The object, stated from nothing

Let R be a commutative ring. A SYMBOL is a function

    w : {0,1} x {0,1} x {0,1}  ->  R

so a symbol is EIGHT values: w[000], w[001], w[010], w[011], w[100], w[101],
w[110], w[111].

The PENTAGON CONDITION on w is: for every (a,b,c,d) in {0,1}^4,

    w[a,b,c] * w[a, b^c, d] * w[b,c,d]  =  w[a^b, c, d] * w[a, b, c^d]

where ^ is addition modulo 2. That is sixteen equations in eight unknowns.

This is the standard 3-cocycle pentagon for a two-element group with
coefficients in R. Do not redesign it. If you think the encoding is wrong, say
so as a finding and give the correction.

## Working rules, and they are not optional

- You must not state, guess, or work toward an expected outcome. Report what you
  compute. Every possible answer is equally reportable.
- Exact arithmetic only. Python 'fractions.Fraction' is available; sympy may or
  may not be, check before relying on it. NEVER use floating point for an
  equality test.
- For values in Q(i), represent a number as a pair of Fractions and implement
  add/mul yourself. Do not trust a library you have not checked.
- Every claim of the form "X holds" or "X fails" needs a specific witness that
  you actually evaluated, printed in your answer.
- End your answer by naming, explicitly, WHAT YOU DID NOT VARY.

## Tools available

- python3, with fractions. Write scripts under ${SCRATCH} .
- Lean 4.22.0 at ${LEAN} (add to PATH). CORE ONLY - Mathlib is NOT installed and
  must not be downloaded. Core Lean has no Rat and no ring tactic. A commutative
  ring CAN be declared by hand as a class and instantiated; Fin n gives Z/n;
  'decide' works on finite types and refuses goals with free variables.
`

const FINDINGS = {
  type: 'object',
  additionalProperties: false,
  required: ['summary', 'findings', 'not_varied'],
  properties: {
    summary: { type: 'string', description: 'What you established, flatly, no interpretation' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['claim', 'evidence', 'confidence'],
        properties: {
          claim: { type: 'string' },
          evidence: { type: 'string', description: 'The specific computation and its printed output' },
          confidence: { type: 'string', enum: ['computed-exhaustively', 'computed-on-samples', 'argued-not-computed'] },
        },
      },
    },
    not_varied: { type: 'array', items: { type: 'string' } },
  },
}

const VERDICT = {
  type: 'object',
  additionalProperties: false,
  required: ['refuted', 'reason'],
  properties: {
    refuted: { type: 'boolean' },
    reason: { type: 'string' },
    counterexample: { type: 'string' },
  },
}

// ---------------------------------------------------------------- Question
phase('Question')
const gap = await agent(`A principal asked for this, verbatim:

"Plan a proof prompt structure that can get us from a forced unit trivial to
general. I want to see all variations, complex, imaginary, not only unit forced.
What happens when we vary everything. For example what's at -1/4, what happens
coming from a different direction. Look from classical, quantum and relational.
I need you to not make assumptions about what we think results mean
automatically."

A task file was then produced. Read it at /tmp/claude-0/-home-user-workshop2/9d633cbc-4061-5889-a22b-fdafc4aa96ce/scratchpad/zero/TASK.md .

Answer three things, coldly:
1. What question does that task file actually settle, stated in one sentence?
2. What does the principal's question ask for that the task file does not touch?
3. Is there anything in the task file's own construction that makes it STRUCTURALLY unable to answer the principal's question? Quote the lines.

Do not be polite about it. Do not propose fixes. This is an audit.`,
  { label: 'audit:question', schema: FINDINGS })

// ---------------------------------------------------------------- Derive
const DERIVATIONS = [
  {
    key: 'variety',
    prompt: `${OBJECT}

## Your task

Derive and solve the full pentagon system for the general eight-value symbol.

1. Write out all sixteen equations explicitly, as products of the eight unknowns.
   Report how many are trivial (both sides identical as expressions) and how many
   are genuine constraints.
2. Solve the system COMPLETELY over a field (work over Q and over Q(i)).
   Find every irreducible component, not just the generic one.
3. CRITICAL: do not divide by anything without splitting into cases. Any step
   that assumes a value is invertible discards a component. Enumerate the
   degenerate components where one or more values are zero, separately.
4. Verify your solution description by exhaustive check: generate many symbols
   from your parameterisation, confirm each satisfies all sixteen equations; and
   search for satisfying symbols OUTSIDE your parameterisation. Report both counts.

Report the dimension of the solution set and a free parameterisation of each
component.`,
  },
  {
    key: 'values',
    prompt: `${OBJECT}

## Your task

The question is which ring elements can appear as a value of a symbol
satisfying the pentagon.

For EACH test value v below, and for EACH of the eight index patterns p, decide:
does there exist a symbol w over Q(i) with w[p] = v satisfying all sixteen
pentagon equations? If yes, print one such w in full. If no, say which equation
is violated for every choice of the remaining seven values, and prove it.

Test values:  0,  1,  -1,  2,  1/2,  -1/4,  i,  -i,  2i,  1/3,  3/7 - 2i/5,
              -1 + i,  (1+i)/2

Produce a table: rows = test values, columns = the eight patterns, entries =
yes with a witness, or no with the obstruction.

THEN, separately: repeat the same question under the additional restriction that
the symbol takes the value 1 on all patterns except ONE. Report the table again
under that restriction and state plainly where the two tables differ.`,
  },
  {
    key: 'sigma',
    prompt: `${OBJECT}

Let R = Q(i) and let s be complex conjugation, a ring automorphism of R.
For a symbol w define s(w) by s(w)[a,b,c] = s( w[a,b,c] ).

A GAUGE TRANSFORMATION is a function u : {0,1} x {0,1} -> R^x (invertible
values). It acts on symbols by

    (u . w)[a,b,c]  =  w[a,b,c] * u[b,c] * u[a, b^c] * inverse( u[a^b, c] ) * inverse( u[a,b] )

Two symbols are GAUGE EQUIVALENT if one is u . w for some u.

## Your task

1. Verify that the gauge action preserves the pentagon condition: if w satisfies
   it, so does u . w. Check computationally on many random u and w.
2. For each pentagon-satisfying w you can construct, decide: is s(w) gauge
   equivalent to w? Compute the full gauge orbit where the orbit is finite, or
   solve the equivalence directly. Report the answer as a table over a family of
   w covering the solution set.
3. Report whether the answer depends on w, and if so exactly which w.
4. Repeat over R = Z/n for n = 2,3,4,5,8,9 with s = identity, and over
   R = Z/5 with s = the Frobenius-type map x -> x^k for each k where that is a
   ring automorphism. Report which rings admit a NON-IDENTITY automorphism at all.

Report a table. Do not draw a conclusion about what it means.`,
  },
  {
    key: 'sector',
    prompt: `${OBJECT}

There is a second condition on a symbol, involving an additional datum.
A BRAIDING is a function r : {0,1} x {0,1} -> R. The hexagon conditions couple
w and r: for all a,b,c in {0,1},

    w[c,a,b] * r[a, b^c]... 

STOP. Do not take that half-written formula on trust - it is deliberately
incomplete, because the point of this task is that you derive the conditions
yourself rather than accept a stated one.

## Your task

1. From the standard theory of a braided monoidal structure on graded vector
   spaces over a two-element group - equivalently, abelian 3-cocycles - state
   the TWO hexagon conditions relating w and r, with correct indices. Cite what
   you are reconstructing them from and show the derivation.
2. Solve the combined system (pentagon + both hexagons) over Q(i) for the
   general eight-value w together with the four-value r.
3. Let s be complex conjugation acting on both w and r. Is the solution set of
   the combined system stable under s? Is each individual solution fixed by s,
   or does s move solutions to other solutions?
4. Compare: is the solution set of the PENTAGON ALONE fixed pointwise by s?
   Is the solution set of the COMBINED system fixed pointwise by s? Report both
   as computed facts with witnesses.

This is the question of whether the two sectors differ in what they can see.
Report what you find. Both answers are equally reportable.`,
  },
  {
    key: 'direction',
    prompt: `${OBJECT}

## Your task: approaching a solution from different directions

1. DEGENERATE LIMITS. Some pentagon solutions have one or more values equal to
   zero. For each such degenerate solution, decide whether it is a limit of
   solutions with all values invertible, or a separate component that cannot be
   reached. Do this by explicit paths: parameterise a family and take the limit.

2. FORMAL DEFORMATION. Work over R[e]/(e^k) for k = 2,3,4. Take a pentagon
   solution w0 with invertible values and set w = w0 * (1 + e*h) for an unknown
   h : {0,1}^3 -> R. Expand the pentagon order by order in e. At each order you
   get a linear system in h. Report:
     - the dimension of the solution space at each order
     - the order, if any, at which the system first becomes inconsistent for
       some h that solved all lower orders
   That order is a computable invariant. Report it. If there is no obstruction at
   any order up to k=4, report that.

3. Do the same over Z/2 and Z/4 and report whether the answer differs from Q(i).

Report numbers and tables. Do not say what any of it means.`,
  },
]

const derived = await pipeline(
  DERIVATIONS,
  d => agent(d.prompt, { label: `derive:${d.key}`, phase: 'Derive', schema: FINDINGS, effort: 'high' }),
  (res, d) => {
    if (!res || !res.findings || !res.findings.length) return { key: d.key, result: res, verdicts: [] }
    const top = res.findings.slice(0, 4)
    return parallel(top.map(f => () =>
      agent(`${OBJECT}

Another party computed the following and you are to REFUTE it. Assume it is
wrong until you cannot make it wrong. Default to refuted=true if you are unsure.

CLAIM: ${f.claim}
THEY SAY THEIR EVIDENCE IS: ${f.evidence}

Re-derive from the definitions yourself. Do not reuse their code or their
approach. Then try specifically to break it: boundary values, zero values,
non-invertible values, characteristic 2, and any case their evidence does not
cover. If you find a counterexample, print it in full and verify it satisfies or
violates the sixteen equations explicitly.`,
        { label: `refute:${d.key}`, phase: 'Verify', schema: VERDICT, effort: 'high' })
        .then(v => ({ claim: f.claim, evidence: f.evidence, verdict: v }))))
      .then(vs => ({ key: d.key, result: res, verdicts: vs.filter(Boolean) }))
  },
)

const clean = derived.filter(Boolean)
const confirmed = []
const refuted = []
for (const d of clean) {
  for (const v of d.verdicts) {
    if (v.verdict && v.verdict.refuted) refuted.push({ key: d.key, ...v })
    else confirmed.push({ key: d.key, ...v })
  }
}
log(`derive complete: ${confirmed.length} survived refutation, ${refuted.length} refuted`)

// ---------------------------------------------------------------- Kernel
phase('Kernel')
const kernelTargets = confirmed.slice(0, 6).map(c => c.claim)
const kernel = await agent(`${OBJECT}

## Your task: settle what a kernel can settle

Lean 4.22.0 core is at ${LEAN}. Mathlib is NOT available and must not be
downloaded. Work under ${SCRATCH}/lean .

You CAN, with zero imports: declare a commutative ring as a class by hand with
its axioms; define the eight-value symbol as a function; define the pentagon
condition; instantiate at Fin n for Z/n; use 'decide' over finite types; use
'omega' for linear integer facts. You CANNOT: use Rat, ring, linarith, norm_num.

NOTE: reaching for an absent tactic makes the theorem silently acquire sorryAx.
After every file, run '#print axioms' on every theorem you prove and report the
result. A theorem that depends on sorryAx is not proved.

The following statements were computed by other parties in Python and survived a
refutation attempt. Python is not proof. Settle whichever of them a kernel can
settle over a FINITE ring - Fin 2, Fin 3, Fin 4, Fin 5, Fin 8 - where 'decide'
can do the work:

${kernelTargets.map((t, i) => `${i + 1}. ${t}`).join('\n')}

For each: either give the Lean theorem and its axiom census, or state precisely
why it is not expressible or not decidable in this setting. Report every file's
exit code. If the kernel disagrees with a stated claim, THE KERNEL IS RIGHT -
report the disagreement as the result.

Report the exact Lean source of everything you prove.`,
  { label: 'kernel', schema: FINDINGS, effort: 'high' })

// ---------------------------------------------------------------- Lenses
phase('Lenses')
const frozen = JSON.stringify({
  audit: gap,
  results: clean.map(d => ({ area: d.key, summary: d.result && d.result.summary, findings: d.result && d.result.findings })),
  refuted: refuted.map(r => ({ claim: r.claim, why: r.verdict.reason })),
  kernel,
}, null, 1).slice(0, 60000)

const LENSES = [
  { key: 'classical', q: 'Treat the object as a 3-cocycle on a two-element group with coefficients in the multiplicative group of the ring. Which cohomology class is each solution? Is the class fixed by the automorphism, even where the representative is not? What is the group of classes over each ring examined, and does the computed solution count agree with it? Where it disagrees, that disagreement is the finding.' },
  { key: 'quantum', q: 'Treat the object as the associator of a fusion category graded by a two-element group, with the braiding datum where present. Which solutions are realizable as an actual category? What does the automorphism correspond to physically, and does the distinction survive to the general object or collapse? What would the modular data separate that the equations alone do not?' },
  { key: 'relational', q: 'Treat the object as its gauge orbit rather than its representative. Is the automorphism inner - that is, does it act as some gauge transformation - or outer? Is that distinction itself gauge invariant? What is actually observable, as opposed to an artifact of choosing a representative? This lens has no prior work here and is the one most likely to produce something.' },
]

const lenses = await parallel(LENSES.map(l => () => agent(
  `Below are frozen computational results. You may NOT compute anything new and
you may NOT contradict a number. Your job is to say what these results are, seen
through one specific lens.

If the results do not support a conclusion under your lens, SAY THAT. "This lens
cannot see anything here, and the reason is X" is a complete and valuable answer.
Do not manufacture significance.

LENS: ${l.key}
${l.q}

FROZEN RESULTS:
${frozen}`,
  { label: `lens:${l.key}`, phase: 'Lenses', schema: FINDINGS, effort: 'high' })))

return {
  audit: gap,
  derived: clean.map(d => ({ area: d.key, summary: d.result && d.result.summary, findings: d.result && d.result.findings, not_varied: d.result && d.result.not_varied })),
  confirmed: confirmed.map(c => ({ area: c.key, claim: c.claim })),
  refuted: refuted.map(r => ({ area: r.key, claim: r.claim, why: r.verdict.reason, counterexample: r.verdict.counterexample })),
  kernel,
  lenses: lenses.filter(Boolean),
}
