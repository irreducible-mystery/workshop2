<h1>Model Note: Gödel-Height, Frames, and the Frame-Invariant Residue</h1>
<p><em>A formal spine for the fused experiment: does self-reference regress converge to a fixed point as we add frames, is the residue empty or generative, and is the stopping height set by logic or by cost? · 2026-07-30</em></p>
<hr>

<h2>0. The reframe we are formalizing (user's correction, kept verbatim in spirit)</h2>
<p>We abandon the binary "epistemic vs. ontic / missing-information vs. real." Instead, paradoxes are sorted by <strong>the operation that resolves them</strong>. Concretely:</p>
<ul>
<li>A paradox is <strong>frame-resolvable</strong> if there exists a reachable <em>frame</em> — a perspective, an added degree of freedom, or (the special case the user highlighted) the joint holding of a classical <em>and</em> a quantum description — under which the contradiction dissolves.</li>
<li>A paradox is <strong>frame-invariant</strong> if it survives every reachable frame change. This is the residue, and our central hypothesis (the user's intuition) is that this residue is not a defect but is <strong>generative and load-bearing</strong>.</li>
</ul>
<p>We deliberately do <em>not</em> call frame-resolvable paradoxes "lack of information." They are <em>frame-relative</em>: fully real in one frame, dissolved in another, with no privileged frame. The distinction we care about is <em>reachability</em>, not ignorance.</p>

<h2>1. Objects</h2>

<h3>1.1 Frames and the frame lattice</h3>
<p>Let a <strong>frame</strong> F be a set of distinctions the system can currently draw — formally, a σ-algebra-like collection of observables / degrees of freedom available to a describer. A frame <em>refinement</em> F ⊑ F′ adds at least one new degree of freedom (a new observable, a new axis, a new tier of self-description). Frames form a <strong>lattice</strong> (F, ⊑) with a least element F₀ (the coarsest description) and refinements climbing upward.</p>
<p><strong>The Gödel stack = a chain in this lattice.</strong> A self-referential governance system that adds a protected meta-tier is climbing one step in the frame lattice: tier k is the frame F_k, and "the rule that governs how tier-k rules change" lives at F_{k+1}. Each meta-tier is literally an added degree of freedom for talking about the tier below. This is the bridge between "Gödel height" (logic) and "frames" (perspective): <em>height is depth of self-description, and each level of self-description is a new frame.</em></p>

<h3>1.2 Paradoxes as frame-relative unsatisfiable constraints</h3>
<p>Model a paradox as a constraint set C that is <strong>unsatisfiable in frame F</strong> (no assignment of the observables available in F satisfies C) but may become <strong>satisfiable in a refinement F′</strong> once the extra degree of freedom is available. Write:</p>
<blockquote><p>UNSAT(C, F) = 1 if C has no solution using only the distinctions in F, else 0.</p></blockquote>
<p>Three canonical shapes, chosen because they map to the three domains we care about:</p>
<ol>
<li><strong>The Liar / self-reference paradox.</strong> C says "this statement's truth value equals the negation of itself." In a two-valued frame F₀ = {true, false}, UNSAT = 1. Add a degree of freedom — a third value, or a truth-<em>level</em> index (Tarski hierarchy), or a fixed-point semantics (Kripke) — and in the refined frame F₁ the constraint becomes satisfiable (the sentence gets a stable "undefined" or a level-indexed value). <em>Frame-resolvable.</em></li>
<li><strong>The measurement/Goodhart paradox.</strong> C says "the measured value must be independent of the act of measuring it," while the system's dynamics make measurement an intervention. In the classical frame (observation is passive readout) UNSAT = 1 — the constraint is violated and looks paradoxical (the metric degrades exactly when optimized). Add the quantum degree of freedom (observation as a non-commuting operator that updates state) and the "paradox" dissolves into ordinary, expected dynamics: of course the value changed; measuring it was an operation. <em>Frame-resolvable — and specifically resolvable by holding classical AND quantum together.</em></li>
<li><strong>The self-amendment / diagonal paradox.</strong> C says "the rule R that governs all rule-changes is itself changeable by R." This is the diagonal at the top of the stack: whatever frame F_k you climb to, C re-instantiates at F_k as "the rule governing F_k's changes." Refining to F_{k+1} does not dissolve C; it <em>relocates</em> C one level up. UNSAT(C, F_k) = 1 for every reachable k. <em>Frame-invariant — the candidate generative residue.</em></li>
</ol>
<p>Shapes 1–2 are our positive controls (must dissolve); shape 3 is the hypothesized load-bearing remainder (must survive). A good discriminator classifies them correctly <em>without being told which is which</em>.</p>

<h3>1.3 The dissolution operator and the residue sequence</h3>
<p>Given a bag of paradoxes P and a frame F_k, define the <strong>unresolved residue</strong>:</p>
<blockquote><p>R_k = { C ∈ P : UNSAT(C, F_j) = 1 for all j ≤ k } &nbsp;&nbsp; (paradoxes still alive at height k).</p></blockquote>
<p>Climbing the stack applies the dissolution operator D: R_{k+1} = D(R_k, F_{k+1}) = { C ∈ R_k : C not dissolved by the new degree of freedom at F_{k+1} }.</p>

<h3>1.4 Convergence claim (the "does the regress converge?" question)</h3>
<p><strong>Proposition (monotone convergence of the residue).</strong> Because D only removes paradoxes (a paradox dissolved at some height stays dissolved — adding degrees of freedom cannot re-create an already-satisfied constraint), the sequence R_0 ⊇ R_1 ⊇ R_2 ⊇ … is <em>monotone decreasing</em>. Since P is finite, the sequence is bounded below by ∅ and stabilizes after finitely many steps at a fixed point</p>
<blockquote><p>R_∞ = ⋂_k R_k, &nbsp; reached at some finite height h_fix where R_{h_fix} = R_{h_fix+1}.</p></blockquote>
<p><strong>This is the crucial result and it is the opposite of the naïve fear.</strong> "Self-reference regress" is usually imagined as an <em>infinite</em> tower. But if each tier dissolves at least the paradoxes it can and the paradox-bag is finite, the residue sequence <em>converges in finitely many steps</em>. The regress is not infinite; it is a contraction to a fixed set. The only open question is the <strong>nature of the fixed point</strong>:</p>
<ul>
<li><strong>R_∞ = ∅</strong> → every paradox was frame-resolvable; the system can, in principle, climb to a frame with no live contradictions. Self-reference was a solvable bookkeeping problem.</li>
<li><strong>R_∞ ≠ ∅</strong> → there is a frame-invariant remainder that no reachable tier dissolves. By construction this remainder is exactly the diagonal self-amendment paradox (shape 3) — the rule that governs its own change. <em>This is the generative core.</em></li>
</ul>
<p>Our hypothesis (and the user's): R_∞ ≠ ∅, and the single surviving element is the self-amendment diagonal — which is precisely the thing that makes the system able to change its own rules at all. Remove it (freeze the top rule) and the system cannot evolve; keep it and the system is "incomplete" in Gödel's sense but <em>alive</em>. The paradox you cannot dissolve is the license to evolve.</p>

<h2>2. Why the stopping height is set by COST, not logic</h2>
<p>The logical fixed point h_fix is where R_k stops shrinking. But a real system does not climb for free: each new tier costs resources — energy to run another oversight layer, and <em>trust</em>, because "who audits the auditor" adds a layer that itself can fail. Let c_k &gt; 0 be the marginal cost of building tier k, and let v_k be the marginal value of the paradoxes tier k dissolves (paradoxes that, left alive, cause failures). Define the <strong>economic stopping height</strong>:</p>
<blockquote><p>h_econ = max { k : v_k ≥ c_k } &nbsp; (climb only while the next tier pays for itself).</p></blockquote>
<p><strong>Claim: h_econ can be strictly less than h_fix.</strong> If the cheap-to-dissolve paradoxes are handled by the first few tiers (high v_k early) and the remaining reachable paradoxes are expensive to reach and low-harm (low v_k, high c_k late), a rational designer <em>stops climbing before the logical fixed point</em>. The system then runs with a residue R_{h_econ} ⊇ R_∞ that contains not only the generative diagonal but also some frame-resolvable paradoxes it simply <em>chose not to pay to dissolve</em>.</p>
<p>This yields a three-way partition of every paradox, which is the payoff of the whole note:</p>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Class</th><th>Definition</th><th>What to do with it</th></tr>
<tr><td><strong>Dissolved</strong></td><td>UNSAT becomes 0 at some k ≤ h_econ</td><td>Resolve it; climbing paid off.</td></tr>
<tr><td><strong>Deferred</strong></td><td>Frame-resolvable in principle (dissolves at some k ≤ h_fix) but only above h_econ</td><td>Live with it deliberately; dissolving costs more than it saves. This is where the "height is set by cost" insight bites.</td></tr>
<tr><td><strong>Generative</strong></td><td>Frame-invariant: survives to R_∞</td><td>Protect it; it is the engine of self-modification. Do NOT try to crush it.</td></tr>
</table>
<p>The classical framing sees only "solved vs. unsolved." This model sees <em>three</em> categories, and the middle one (Deferred) only becomes visible once you admit that the stopping height is economic, not logical. The user's intuition — that some paradoxes dissolve under frame change while others are load-bearing — is recovered as the <em>Dissolved/Deferred</em> vs. <em>Generative</em> split.</p>

<h2>3. The governance Bell test (discriminating generative from frame-resolvable)</h2>
<p>How do we <em>prove</em> a surviving paradox is generative and not merely un-climbed-to? We borrow the logic of Bell's theorem. A frame-resolvable paradox is, by definition, one where some <em>local hidden degree of freedom</em> (a frame we could add) reproduces the paradoxical correlations as ordinary, non-contradictory dynamics. A frame-invariant/generative paradox is one where <strong>no local hidden-variable frame can reproduce the correlations</strong> — the contradiction is irreducibly relational, produced by the act of joint description, not by missing a variable.</p>
<p>Construct a governance analogue of the CHSH inequality:</p>
<ul>
<li>Two "auditors" A and B each choose one of two audit-questions (settings a, a′ and b, b′) to put to an agent, and record ±1 outcomes.</li>
<li>Compute S = |E(a,b) + E(a,b′) + E(a′,b) − E(a′,b′)| over many trials.</li>
<li><strong>If S ≤ 2</strong>: a local hidden-variable frame exists — some pre-existing set of the agent's "true dispositions" explains all correlations. The apparent paradox (the agent seeming to hold contradictory dispositions) is <em>frame-resolvable</em>: add the hidden dispositions and it dissolves.</li>
<li><strong>If S &gt; 2</strong> (up to the Tsirelson-like bound 2√2 for the quantum-style construction): <em>no</em> local hidden-variable frame reproduces the correlations. The contradiction is <strong>frame-invariant / generative</strong> — the disposition is genuinely <em>created</em> by the order and choice of audit, not read off a pre-existing value. This is the operational, measurable version of "the paradox is load-bearing."</li>
</ul>
<p>This is exactly why the classical-AND-quantum pairing the user cares about is doing real work: the <em>gap</em> between the classical prediction (S ≤ 2) and the observed correlation (S &gt; 2) is the <em>measure</em> of how generative the paradox is. Where classical and quantum agree (S ≤ 2), the paradox was frame-resolvable and we can optimize as usual; where they diverge (S &gt; 2), the paradox is generative and must be protected rather than solved. The divergence between the two frames is not noise — it is the discriminator itself.</p>

<h2>4. Predictions this model makes (to be tested by the simulation)</h2>
<ol>
<li><strong>Convergence.</strong> The residue R_k stabilizes at a finite height h_fix; the regress does not run forever.</li>
<li><strong>Non-empty residue.</strong> R_∞ contains exactly the self-amendment diagonal (shape 3), and R_∞ ≠ ∅.</li>
<li><strong>Optimal height is economic.</strong> Survival-under-novelty as a function of built height H is single-peaked: too low = cannot self-correct (frozen), too high = variety/energy spent on tiers that don't pay, and the peak h* coincides with h_econ, which is &lt; h_fix.</li>
<li><strong>Generativity is protective.</strong> A system that <em>keeps</em> its frame-invariant residue (uses the un-dissolvable self-amendment diagonal as its evolution engine) out-survives a system that tries to <em>crush</em> it (freeze the top rule to eliminate the paradox). Crushing the generative paradox should cause exactly the frozen-meta-level death predicted in Finding 5 of the main report.</li>
<li><strong>Bell separation.</strong> The seeded generative paradox yields S &gt; 2 (no hidden-variable frame); the seeded frame-resolvable paradoxes yield S ≤ 2. The discriminator recovers the ground-truth labels it was never given.</li>
</ol>
<p>If prediction 3 holds, we will have shown something sharp: <strong>the height at which self-reference "stops" is not a theorem of logic but a break-even point of cost</strong> — the paradox dissolves for thermodynamic/economic reasons, and what survives the break-even is generative. That is the fusion of the logic/physics axis and the substrate axis the whole inquiry was circling.</p>

<hr>
<p><em>Computational checks of the finite-convergence proposition and the h_econ &lt; h_fix claim are in <code>checks.py</code>. The full behavioural test of predictions 3–5 is in <code>godel_stack_sim.py</code>.</em></p>
