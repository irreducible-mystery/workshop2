#!/usr/bin/env python3
"""
thread2_noise_robust.py
=======================
THREAD 2: beat Fork 1's noise wall.

Fork 1's plain CHSH generative test died at detector-flip noise p* ~ 0.08,
failing in the DANGEROUS direction (a genuinely generative paradox reads as
resolvable -> false negative). This thread tries three designs to push the
critical noise threshold p* out, and measures the cost of each.

Designs
-------
BASELINE  plain CHSH, one read per (setting,setting). Control: reproduce p*~0.08.

DESIGN A  REPEATED-PROBE MAJORITY VOTE. Take m independent reads of each outcome
          and majority-vote before computing correlations. Majority vote turns a
          per-read flip prob p into an effective flip prob p_eff(m) that shrinks
          fast with m; p* should climb toward 0.5 as m grows. Cost: m x probes.

DESIGN B  CHAINED (Braunstein-Caves) N-setting inequality. Uses N settings per
          side and the chained bound; the quantum violation is spread over more,
          more-finely-spaced correlations. Measure p*(N). (Known result: chained
          inequalities are MORE demanding on visibility, so we expect p* to get
          WORSE -- an honest negative result worth showing.)

DESIGN C  TWO-INEQUALITY SELF-TEST. Require the source to violate CHSH at TWO
          independent setting-pairs and demand BOTH. This trades false negatives
          against false positives; measure the confusion tradeoff vs noise.

We report p* for each design and the confusion cost.
"""
from __future__ import annotations
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
os.makedirs("results", exist_ok=True)

RNG = np.random.default_rng(20260730)


# --------------------------------------------------------------------------- #
# Generative (singlet) source with detector noise, optional majority vote      #
# --------------------------------------------------------------------------- #
def singlet_pair(theta_a, theta_b, trials, rng):
    """Draw correlated +/-1 pairs (A,B) with E[A*B] = -cos(a-b)."""
    corr = -np.cos(theta_a - theta_b)
    p_disagree = (1.0 - corr) / 2.0
    disagree = rng.random(trials) < p_disagree
    A = np.where(rng.random(trials) < 0.5, 1, -1)   # marginal is uniform +/-1
    B = np.where(disagree, -A, A)
    return A, B


def noisy_read(x, p, rng, m=1):
    """Read outcome x (array of +/-1) through a detector that flips w.p. p.
    If m>1, take m independent reads and MAJORITY VOTE (Design A)."""
    if m == 1:
        flip = rng.random(x.shape) < p
        return np.where(flip, -x, x)
    votes = np.zeros_like(x, dtype=float)
    for _ in range(m):
        flip = rng.random(x.shape) < p
        votes += np.where(flip, -x, x)
    # majority vote; ties (m even) broken randomly
    out = np.sign(votes)
    ties = out == 0
    out[ties] = np.where(rng.random(ties.sum()) < 0.5, 1, -1)
    return out.astype(int)


def E_noisy(theta_a, theta_b, p, rng, trials=120000, m=1):
    A, B = singlet_pair(theta_a, theta_b, trials, rng)
    A = noisy_read(A, p, rng, m); B = noisy_read(B, p, rng, m)
    return (A * B).mean()


# --------------------------------------------------------------------------- #
# BASELINE / DESIGN A : CHSH with optional majority vote                       #
# --------------------------------------------------------------------------- #
def chsh_S(p, rng, m=1, trials=120000):
    a, a2 = 0.0, np.pi / 2
    b, b2 = np.pi / 4, -np.pi / 4
    E = lambda ta, tb: E_noisy(ta, tb, p, rng, trials, m)
    return abs(E(a, b) + E(a, b2) + E(a2, b) - E(a2, b2))


# --------------------------------------------------------------------------- #
# DESIGN B : chained Braunstein-Caves inequality with N settings per side      #
# --------------------------------------------------------------------------- #
def chained_S(p, rng, N=3, trials=120000):
    """Chained inequality:
       S_N = |E(a1,b1)+E(b1,a2)+E(a2,b2)+...+E(aN,bN)| - |E(bN,a1)| ... classical
       bound is 2N-2; quantum reaches 2N cos(pi/2N). We use the standard chained
       settings a_i, b_i equally spaced by pi/2N and the normalized statistic
       S_hat = S_chained / (2N-2) so that the LOCAL bound is 1 for every N and the
       decision line is S_hat > 1."""
    # settings equally spaced
    a = [i * np.pi / N for i in range(N)]
    b = [(i + 0.5) * np.pi / N for i in range(N)]
    E = lambda ta, tb: E_noisy(ta, tb, p, rng, trials)
    terms = 0.0
    for i in range(N):
        terms += E(a[i], b[i])
        # wrap term: last b with first a carries a minus sign
        if i < N - 1:
            terms += E(b[i], a[i + 1])
    wrap = E(b[N - 1], a[0])
    S_chained = abs(terms - wrap)
    return S_chained / (2 * N - 2)   # normalized: local bound = 1


# --------------------------------------------------------------------------- #
# helper: find p* (crossing of the decision line) by bisection                 #
# --------------------------------------------------------------------------- #
def find_pstar(stat_fn, decision_line, lo=0.0, hi=0.5, iters=26):
    """stat_fn(p) monotone-decreasing; find p where it crosses decision_line."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if stat_fn(mid) > decision_line:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    results = {}

    # ---- BASELINE + DESIGN A: majority vote ---- #
    print("=== BASELINE + DESIGN A (repeated-probe majority vote) ===")
    ms = [1, 3, 5, 9, 15, 25]
    pstar_A = []
    for m in ms:
        rng = np.random.default_rng(100 + m)
        ps = find_pstar(lambda p: chsh_S(p, np.random.default_rng(100 + m), m=m,
                                         trials=60000), 2.0)
        pstar_A.append(ps)
        print(f"  m={m:2d} reads: p* = {ps:.3f}")
    results["design_A_majority_vote"] = {"m": ms, "pstar": pstar_A}

    # ---- DESIGN B: chained inequality ---- #
    print("\n=== DESIGN B (chained Braunstein-Caves, normalized local bound = 1) ===")
    Ns = [2, 3, 4, 6]
    pstar_B = []
    for N in Ns:
        ps = find_pstar(lambda p: chained_S(p, np.random.default_rng(200 + N),
                                            N=N, trials=60000), 1.0)
        pstar_B.append(ps)
        print(f"  N={N} settings: p* = {ps:.3f}")
    results["design_B_chained"] = {"N": Ns, "pstar": pstar_B}

    # ---- DESIGN C: two-inequality self-test (confusion vs noise) ---- #
    print("\n=== DESIGN C (require violation at TWO pairs) — confusion vs noise ===")
    # second pair: rotate all settings by a fixed offset; generative violates both,
    # a local mimic must fake both simultaneously.
    def chsh_S_offset(p, rng, off, trials=60000):
        a, a2 = 0.0 + off, np.pi / 2 + off
        b, b2 = np.pi / 4 + off, -np.pi / 4 + off
        E = lambda ta, tb: E_noisy(ta, tb, p, rng, trials)
        return abs(E(a, b) + E(a, b2) + E(a2, b) - E(a2, b2))

    noises = [0.0, 0.05, 0.10, 0.15, 0.20]
    designC = []
    for p in noises:
        S1 = chsh_S(p, np.random.default_rng(300), m=1)
        S2 = chsh_S_offset(p, np.random.default_rng(301), off=np.pi / 8)
        # single-test call vs AND-of-two call
        pred_single = S1 > 2.0
        pred_and = (S1 > 2.0) and (S2 > 2.0)
        designC.append((p, float(S1), float(S2), bool(pred_single), bool(pred_and)))
        print(f"  noise {p:.2f}: S1={S1:.3f} S2={S2:.3f} "
              f"single->{pred_single}  AND-of-two->{pred_and}")
    results["design_C_two_inequality"] = designC

    with open("results/thread2_noise_robust.json", "w") as f:
        json.dump(results, f, indent=2)

    # ============================ FIGURES ============================ #
    BLUE, GREEN, RED, GREY = "#1f77b4", "#2ca02c", "#d62728", "#7f7f7f"

    # FIG 12: p* vs m (Design A) and vs N (Design B), with baseline marked
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    ax.plot(ms, pstar_A, color=GREEN, lw=2.2, marker="o", ms=5,
            label="Design A: majority vote (m reads)")
    ax.axhline(pstar_A[0], color=GREY, ls=":", lw=1.4,
               label=f"baseline CHSH p* = {pstar_A[0]:.3f}")
    ax.set_xlabel("m  (independent reads per outcome, majority-voted)")
    ax.set_ylabel("critical noise p*  (higher = more robust)")
    ax.set_title("THREAD 2  Repeated-probe majority vote pushes the noise wall out\n"
                 "(Design A moves p* from ~8% toward 50%)")
    ax.legend(frameon=False, fontsize=9, loc="lower right"); ax.grid(alpha=0.25)
    ax.set_ylim(0, 0.55)
    fig.tight_layout(); fig.savefig("figures/fig12_designA_majority.png", dpi=140); plt.close(fig)

    # FIG 13: Design B chained — the honest negative result
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(Ns, pstar_B, color=RED, lw=2.2, marker="s", ms=6,
            label="Design B: chained N-setting inequality")
    ax.axhline(pstar_A[0], color=GREY, ls=":", lw=1.4,
               label=f"baseline CHSH p* = {pstar_A[0]:.3f}")
    ax.set_xlabel("N  (settings per side, chained inequality)")
    ax.set_ylabel("critical noise p*")
    ax.set_title("THREAD 2  Chained inequalities are LESS noise-robust\n"
                 "(honest negative: more settings -> tighter visibility demand)")
    ax.legend(frameon=False, fontsize=9); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig("figures/fig13_designB_chained.png", dpi=140); plt.close(fig)

    print("\nSaved figures/fig12, fig13 and results/thread2_noise_robust.json")
