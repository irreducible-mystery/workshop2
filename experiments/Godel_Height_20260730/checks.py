#!/usr/bin/env python3
"""
checks.py
=========
Small computational checks of the two formal claims in model_note.md:

  CHECK 1  Finite convergence of the residue sequence R_0 ⊇ R_1 ⊇ ... to a
           fixed point R_inf reached at a finite height h_fix, with R_inf equal
           to exactly the frame-invariant (self-amendment diagonal) paradoxes.

  CHECK 2  The economic stopping height h_econ can be STRICTLY LESS than the
           logical fixed-point height h_fix, so the stopping point is set by
           cost, not by logic -- and the residue at h_econ therefore contains
           'Deferred' (frame-resolvable but un-dissolved) paradoxes on top of
           the 'Generative' ones.

These are deterministic checks, not Monte-Carlo -- they verify the algebra.
"""
from dataclasses import dataclass


# --------------------------------------------------------------------------- #
# A paradox: the height at which its added degree of freedom dissolves it.     #
#   dissolves_at = k  means UNSAT becomes 0 once we reach frame F_k.            #
#   dissolves_at = None means frame-invariant (never dissolves) -> generative. #
# --------------------------------------------------------------------------- #
@dataclass
class Paradox:
    name: str
    dissolves_at: int | None   # None => frame-invariant / generative
    harm: float                # value of dissolving it (harm if left alive)


def residue_sequence(paradoxes, max_height):
    """R_k = paradoxes still unresolved at height k."""
    seq = []
    for k in range(max_height + 1):
        alive = [p for p in paradoxes
                 if (p.dissolves_at is None) or (p.dissolves_at > k)]
        seq.append(alive)
    return seq


def check1_finite_convergence(paradoxes, max_height=20):
    seq = residue_sequence(paradoxes, max_height)
    sizes = [len(r) for r in seq]

    # find h_fix: first height where residue stops changing forever after
    h_fix = None
    for k in range(len(sizes) - 1):
        if all(sizes[j] == sizes[k] for j in range(k, len(sizes))):
            h_fix = k
            break
    R_inf = set(p.name for p in seq[-1])
    generative = set(p.name for p in paradoxes if p.dissolves_at is None)

    monotone = all(sizes[i] >= sizes[i + 1] for i in range(len(sizes) - 1))

    print("=== CHECK 1: finite convergence of the residue ===")
    print(f"  residue sizes by height: {sizes}")
    print(f"  monotone decreasing?      {monotone}")
    print(f"  fixed point height h_fix: {h_fix}")
    print(f"  R_inf (survivors):        {sorted(R_inf)}")
    print(f"  ground-truth generative:  {sorted(generative)}")
    ok = monotone and (h_fix is not None) and (R_inf == generative)
    print(f"  => R_inf == generative set, reached at finite height: {ok}")
    return ok, h_fix, R_inf


def check2_economic_vs_logical(paradoxes, tier_cost, max_height=20):
    """h_econ = highest k such that the marginal value dissolved by tier k still
    covers the marginal cost c_k of building tier k."""
    seq = residue_sequence(paradoxes, max_height)

    # marginal value of tier k = harm of paradoxes dissolved GOING from k-1 to k
    def dissolved_between(k):
        prev = set(p.name for p in seq[k - 1]) if k >= 1 else set(p.name for p in paradoxes)
        now = set(p.name for p in seq[k])
        newly = prev - now
        return sum(p.harm for p in paradoxes if p.name in newly)

    h_econ = 0
    for k in range(1, max_height + 1):
        v_k = dissolved_between(k)
        c_k = tier_cost(k)
        pays = v_k >= c_k
        if pays:
            h_econ = k
        # keep scanning; a later cheap-high-value tier could still pay, but with
        # our monotone construction value is front-loaded, so first failure that
        # is never recovered sets the practical stop. We report the max paying k.

    # logical fixed point again
    sizes = [len(r) for r in seq]
    h_fix = next(k for k in range(len(sizes) - 1)
                 if all(sizes[j] == sizes[k] for j in range(k, len(sizes))))

    print("\n=== CHECK 2: economic stop h_econ vs logical fixed point h_fix ===")
    for k in range(1, h_fix + 2):
        print(f"  tier {k}: value dissolved = {dissolved_between(k):.2f}, "
              f"cost = {tier_cost(k):.2f}, pays = {dissolved_between(k) >= tier_cost(k)}")
    print(f"  h_econ (economic stop) = {h_econ}")
    print(f"  h_fix  (logical stop)  = {h_fix}")
    print(f"  => h_econ < h_fix (height set by COST, not logic): {h_econ < h_fix}")

    # what remains at the economic stop: generative + deferred(frame-resolvable but skipped)
    residue_econ = set(p.name for p in seq[h_econ])
    generative = set(p.name for p in paradoxes if p.dissolves_at is None)
    deferred = residue_econ - generative
    print(f"  residue at h_econ: {sorted(residue_econ)}")
    print(f"    of which generative (protect): {sorted(generative & residue_econ)}")
    print(f"    of which deferred (live with):  {sorted(deferred)}")
    return h_econ < h_fix, h_econ, h_fix, deferred


if __name__ == "__main__":
    # A bag of paradoxes mixing the three shapes from the model note.
    # Front-loaded value: cheap paradoxes dissolve early and matter a lot;
    # later-dissolving ones are lower harm -> sets up h_econ < h_fix.
    paradoxes = [
        Paradox("liar_two_valued",        dissolves_at=1, harm=5.0),   # shape 1
        Paradox("goodhart_measurement",   dissolves_at=1, harm=4.0),   # shape 2 (classical+quantum)
        Paradox("order_effect",           dissolves_at=2, harm=3.0),
        Paradox("nested_reflexivity",     dissolves_at=3, harm=1.2),
        Paradox("deep_frame_paradox",     dissolves_at=5, harm=0.4),   # expensive, low harm
        Paradox("self_amendment_diagonal", dissolves_at=None, harm=99.0),  # shape 3: generative
    ]

    # tier cost grows with height (deeper oversight tiers cost more energy/trust)
    def tier_cost(k):
        return 1.0 * (1.6 ** (k - 1))   # 1.0, 1.6, 2.56, 4.1, 6.55, ...

    ok1, h_fix, R_inf = check1_finite_convergence(paradoxes)
    ok2, h_econ, h_fix2, deferred = check2_economic_vs_logical(paradoxes, tier_cost)

    print("\n=== SUMMARY ===")
    print(f"  Check 1 (finite convergence, R_inf = generative): {'PASS' if ok1 else 'FAIL'}")
    print(f"  Check 2 (h_econ < h_fix, cost sets the stop):      {'PASS' if ok2 else 'FAIL'}")
    print(f"  The generative residue R_inf = {sorted(R_inf)} survives every reachable frame.")
    print(f"  At the economic stop, we also 'live with' deferred paradoxes: {sorted(deferred)}")
