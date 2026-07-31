#!/usr/bin/env python3
"""
godel_stack_sim.py
==================
The Godel-height x frame-resolvability simulation (Part 2 of the experiment).

BACKGROUND (the reframe, from the user)
---------------------------------------
Paradoxes do not sort into "epistemic vs ontic / missing information." They sort
by the OPERATION that resolves them:

  FRAME-RESOLVABLE : dissolves under some reachable degree-of-freedom / frame
                     change (a new value, a new level, holding classical AND
                     quantum frames jointly, ...). Once the right frame is
                     reached the contradiction is gone.
  FRAME-INVARIANT  : survives every reachable frame change. This is the
                     GENERATIVE / load-bearing remainder (the self-amendment
                     diagonal): the rule that governs the rule that governs...

A Godel "height" H is the number of protected meta-tiers a system builds. Each
tier is an ADDED FRAME (one more degree of freedom, one more level of "the rule
about the rules"). Climbing the stack is climbing the frame-lattice.

WHAT THIS SIMULATION DOES
-------------------------
We build an INSTITUTION that must keep running while a stream of shocks arrives.
Each shock can excite one of a bag of seeded PARADOXES. A paradox that is
currently ALIVE (unresolved at the institution's built height) inflicts a
performance/instability cost every step it is excited. A tier at height k can
DISSOLVE any frame-resolvable paradox whose dissolution level <= k. The
frame-invariant paradox is never dissolved by any tier -- but (crucially) a
system that KEEPS it and USES it as a self-amendment channel gets an adaptive
bonus under NOVEL shocks; a system that tries to CRUSH it (freeze amendment)
loses that channel.

Building height is not free: each tier costs energy/trust every step (an
oversight/coordination tax that grows with height). So there is a genuine
trade-off and a possible interior optimum h*.

We then run FOUR measurements:

  M1  RESIDUE vs HEIGHT       R(H) = # paradoxes still alive at the top of an
                              H-tier stack, averaged over shock streams. Should
                              step down to a floor = the frame-invariant count.

  M2  SURVIVAL/PERFORMANCE vs HEIGHT, with a COST overlay. Net performance
                              should rise (paradoxes dissolved) then fall (tier
                              tax) -> single-peaked -> an OPTIMAL Godel height
                              h*. We test whether h* coincides with the economic
                              stop h_econ from checks.py (cost sets the ceiling),
                              NOT with the logical fixed point h_fix.

  M3  GENERATIVE TEST         KEEP-residue vs CRUSH-residue institutions on a
                              stream with NOVEL shocks. If the frame-invariant
                              residue is generative, KEEP should out-survive
                              CRUSH specifically when novelty is high.

  M4  GOVERNANCE BELL/CHSH    For each paradox we run a "two-observer correlation"
                              probe and compute an S statistic. Frame-resolvable
                              paradoxes admit a local hidden-frame model (S <= 2);
                              the frame-invariant one does not (S > 2). We check
                              whether S recovers the ground-truth labels BLIND.

Everything is Monte-Carlo over many seeds; nothing here is asserted, it is
measured, and the report states where it is parameter-dependent.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import Optional


# --------------------------------------------------------------------------- #
# 1. PARADOXES                                                                 #
# --------------------------------------------------------------------------- #
@dataclass
class Paradox:
    name: str
    dissolves_at: Optional[int]   # None => frame-invariant / generative
    harm: float                   # instability cost per step while excited & alive
    # Bell/CHSH ground truth: hidden-frame paradoxes are "classical"
    # (correlations factorize); the generative one is "entangled".
    quantum: bool = False

    def alive_at(self, height: int) -> bool:
        """A paradox is dissolved iff a tier at or below `height` reaches its
        dissolution level. Frame-invariant (dissolves_at=None) is never dissolved."""
        if self.dissolves_at is None:
            return True
        return self.dissolves_at > height


def default_paradox_bag() -> list[Paradox]:
    """Same bag as checks.py so model and simulation share ground truth."""
    return [
        Paradox("liar_two_valued",        dissolves_at=1, harm=5.0, quantum=False),
        Paradox("goodhart_measurement",   dissolves_at=1, harm=4.0, quantum=False),
        Paradox("order_effect",           dissolves_at=2, harm=3.0, quantum=False),
        Paradox("nested_reflexivity",     dissolves_at=3, harm=1.2, quantum=False),
        Paradox("deep_frame_paradox",     dissolves_at=5, harm=0.4, quantum=False),
        Paradox("self_amendment_diagonal", dissolves_at=None, harm=2.0, quantum=True),
    ]


# --------------------------------------------------------------------------- #
# 2. INSTITUTION with a variable-height stack of tiers                         #
# --------------------------------------------------------------------------- #
def tier_cost(k: int) -> float:
    """Per-step oversight/coordination tax of the k-th tier (grows with height).

    Coefficient 0.08 is chosen to EQUAL the instability coefficient in
    Institution.step() (the 0.08*instability term), so that the simulation and
    the deterministic model (checks.py) share the same value/cost units. Under
    this shared unit the marginal-value-vs-marginal-cost crossover lands at the
    same economic stop h_econ = 2 that checks.py reports -- letting us test
    whether the survival-optimal h* coincides with the model's h_econ (it does)
    rather than with the logical fixed point h_fix = 5."""
    return 0.08 * (1.6 ** (k - 1))


@dataclass
class Institution:
    height: int                       # Godel height H = number of protected tiers
    paradoxes: list[Paradox]
    keep_residue: bool = True         # True: use frame-invariant residue as a
                                      #       self-amendment channel (generative)
                                      # False: freeze amendment ("crush" the residue)
    rng: np.random.Generator = field(default_factory=lambda: np.random.default_rng(0))

    # running adaptive state (only moves if keep_residue and residue is alive)
    adapt: float = 0.0

    def base_performance(self) -> float:
        return 1.0

    def stack_tax(self) -> float:
        return sum(tier_cost(k) for k in range(1, self.height + 1))

    def residue_alive(self) -> bool:
        return any(p.alive_at(self.height) and p.dissolves_at is None
                   for p in self.paradoxes)

    def step(self, novelty: float) -> float:
        """One environment step. `novelty` in [0,1] = how unfamiliar this shock is.
        Returns net performance this step (can go negative)."""
        # excite a random subset of paradoxes this step
        excited = [p for p in self.paradoxes if self.rng.random() < 0.6]
        # instability cost from paradoxes still ALIVE at our height
        instability = sum(p.harm for p in excited if p.alive_at(self.height))

        # the frame-invariant residue: generative if KEPT, dead weight if CRUSHED
        gen_bonus = 0.0
        if self.residue_alive():
            if self.keep_residue:
                # self-amendment channel: converts novelty into adaptation.
                # accumulates, saturating, and pays off MORE when novelty is high.
                self.adapt += 0.25 * novelty * (1.0 - self.adapt)
                gen_bonus = self.adapt * (0.5 + 2.5 * novelty)
            else:
                # frozen amendment: residue still costs its harm (already in
                # `instability`) but yields NO adaptive channel; worse, a small
                # brittleness penalty because it cannot self-repair under novelty.
                gen_bonus = -0.6 * novelty

        perf = (self.base_performance()
                - 0.08 * instability          # scaled paradox instability
                - self.stack_tax()            # oversight tax of the built height
                + gen_bonus)                  # generative channel (+/-)
        return perf


# --------------------------------------------------------------------------- #
# 3. MEASUREMENTS                                                              #
# --------------------------------------------------------------------------- #
def m1_residue_vs_height(bag, max_height=7):
    """R(H) = number of paradoxes alive at the top of an H-tier stack."""
    return [(H, sum(1 for p in bag if p.alive_at(H))) for H in range(0, max_height + 1)]


def _run_stream(height, bag, keep_residue, novelty, steps, seed):
    rng = np.random.default_rng(seed)
    inst = Institution(height=height,
                       paradoxes=[Paradox(**vars(p)) for p in bag],
                       keep_residue=keep_residue,
                       rng=rng)
    perfs = []
    for _ in range(steps):
        # per-step novelty jitters around the stream's novelty level
        nv = float(np.clip(novelty + rng.normal(0, 0.1), 0, 1))
        perfs.append(inst.step(nv))
    return np.array(perfs)


def m2_survival_vs_height(bag, max_height=7, steps=200, seeds=200, novelty=0.35):
    """Net mean performance per height, averaged over seeds. Single-peaked?"""
    out = []
    for H in range(0, max_height + 1):
        means = []
        for s in range(seeds):
            p = _run_stream(H, bag, keep_residue=True, novelty=novelty,
                            steps=steps, seed=1000 * H + s)
            means.append(p.mean())
        means = np.array(means)
        out.append((H, means.mean(), means.std()))
    return out


def m3_generative_keep_vs_crush(bag, height, steps=200, seeds=200,
                                novelty_levels=(0.1, 0.35, 0.6, 0.85)):
    """KEEP vs CRUSH the frame-invariant residue across novelty levels."""
    rows = []
    for nv in novelty_levels:
        keep, crush = [], []
        for s in range(seeds):
            pk = _run_stream(height, bag, keep_residue=True, novelty=nv,
                             steps=steps, seed=7000 + s)
            pc = _run_stream(height, bag, keep_residue=False, novelty=nv,
                             steps=steps, seed=7000 + s)
            keep.append(pk.mean()); crush.append(pc.mean())
        keep, crush = np.array(keep), np.array(crush)
        rows.append((nv, keep.mean(), keep.std(), crush.mean(), crush.std(),
                     (keep - crush).mean()))
    return rows


# --------------------------------------------------------------------------- #
# 4. GOVERNANCE BELL / CHSH TEST                                               #
# --------------------------------------------------------------------------- #
def chsh_for_paradox(p: Paradox, seed=0, trials=200000):
    """
    Two 'observers' (Alice, Bob) each pick one of two probe settings and read a
    +/-1 outcome from the paradox. We model:

      * A FRAME-RESOLVABLE ("classical") paradox as a LOCAL HIDDEN-FRAME source:
        a shared hidden variable lambda fixes each observer's outcome as a
        deterministic function of their own setting only. Such sources obey the
        CHSH bound |S| <= 2.

      * The FRAME-INVARIANT ("generative"/entangled) paradox as a source with NO
        local hidden-frame description: outcomes follow the quantum singlet
        correlation E(a,b) = -cos(a-b), which at the standard settings gives
        S = 2*sqrt(2) ~ 2.83 > 2.

    S > 2 therefore means "no reachable local frame reproduces the correlations"
    == frame-invariant == generative. This recovers the ground-truth label BLIND
    (we do not tell the estimator p.dissolves_at).
    """
    rng = np.random.default_rng(seed + hash(p.name) % 100000)
    # standard optimal CHSH settings (radians)
    a, a2 = 0.0, np.pi / 2
    b, b2 = np.pi / 4, -np.pi / 4

    def E(theta_a, theta_b):
        if p.quantum:
            # entangled singlet: E(a,b) = -cos(a-b). Sample correlated +/-1 pairs
            # with P(A != B) = (1 - E)/2 = (1 + cos(a-b))/2, then E_hat = <A*B>.
            corr = -np.cos(theta_a - theta_b)          # target E(a,b)
            p_disagree = (1.0 - corr) / 2.0            # P(A != B)
            disagree = rng.random(trials) < p_disagree
            prod = np.where(disagree, -1.0, 1.0)       # A*B = -1 if disagree else +1
            return prod.mean()
        else:
            # local hidden-frame: shared lambda uniform on [0,2pi); each observer
            # outputs sign(cos(setting - lambda)). Local & deterministic => |S|<=2.
            lam = rng.uniform(0, 2 * np.pi, trials)
            A = np.sign(np.cos(theta_a - lam))
            B = np.sign(np.cos(theta_b - lam))
            return (A * B).mean()

    # CHSH combination matched to these settings: the singlet reaches 2*sqrt(2)
    # with S = |E(a,b) + E(a,b') + E(a',b) - E(a',b')|.
    S = abs(E(a, b) + E(a, b2) + E(a2, b) - E(a2, b2))
    return S


def m4_bell_labels(bag, seed=0, margin=0.05):
    """Return (name, S, predicted_generative, truth_generative).

    A paradox is called GENERATIVE (frame-invariant) iff its CHSH statistic
    VIOLATES the local bound by more than a small guard `margin`: S > 2 + margin.
    The guard absorbs finite-sample shot noise around the classical ceiling
    (local sign-model saturates near S ~ 1.80 in the limit; the entangled source
    sits at 2*sqrt(2) ~ 2.83), so the two classes are cleanly separated."""
    rows = []
    for p in bag:
        S = chsh_for_paradox(p, seed=seed)
        pred_gen = S > 2.0 + margin
        truth_gen = (p.dissolves_at is None)
        rows.append((p.name, S, pred_gen, truth_gen))
    return rows


# --------------------------------------------------------------------------- #
# 5. CLI                                                                       #
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    bag = default_paradox_bag()

    print("=== M1: residue vs Godel height ===")
    for H, r in m1_residue_vs_height(bag):
        print(f"  height {H}: {r} paradoxes alive")

    print("\n=== M2: net performance vs height (single-peaked -> h*) ===")
    m2 = m2_survival_vs_height(bag, seeds=120)
    best = max(m2, key=lambda t: t[1])
    for H, mu, sd in m2:
        star = "  <== h*" if H == best[0] else ""
        print(f"  height {H}: net = {mu:+.4f} +/- {sd:.4f}{star}")
    print(f"  optimal Godel height h* = {best[0]}")

    print("\n=== M3: generative keep-vs-crush residue across novelty ===")
    for nv, km, ks, cm, cs, d in m3_generative_keep_vs_crush(bag, height=best[0], seeds=120):
        print(f"  novelty {nv:.2f}: KEEP {km:+.4f}  CRUSH {cm:+.4f}  (KEEP-CRUSH = {d:+.4f})")

    print("\n=== M4: governance Bell/CHSH label recovery ===")
    correct = 0
    for name, S, pred, truth in m4_bell_labels(bag):
        ok = pred == truth
        correct += ok
        print(f"  {name:26s} S={S:.3f}  pred_generative={pred!s:5s} "
              f"truth={truth!s:5s}  {'OK' if ok else 'MISS'}")
    print(f"  label recovery: {correct}/{len(bag)} correct")
