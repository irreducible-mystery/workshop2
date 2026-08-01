#!/usr/bin/env python3
"""
thread1_lattice_density.py
==========================
THREAD 1: generalize the dead-tier finding.

Fork 2 found that a single empty rung ("dead tier") at height 4 structurally
capped the contiguous climb -- you can never economically justify building
through a tier that dissolves nothing. This thread asks the general question:

    Does the DISTRIBUTION of paradox dissolution-levels (the lattice DENSITY,
    and the way harm is spread across heights) systematically set how high it
    pays to climb?

Model of a lattice
------------------
A lattice over heights 1..L is defined by:
  * density rho in (0,1]  -- each height independently contains a resolvable
    paradox with probability rho. (rho=1 -> dense, no gaps; small rho -> gappy.)
  * a total harm budget B spread across the occupied heights by a HARM PROFILE:
      'front'  : harm concentrated at low heights (cheap, high-value early)
      'flat'   : harm spread evenly
      'back'   : harm concentrated at high heights (payoff is deep)
  * exactly one frame-invariant (generative) paradox always present (the floor).

Three heights per lattice
-------------------------
  h_reach : the CONTIGUOUS structural cap = (first empty height) - 1. A climb
            that must build every rung below k stops at the first gap. Dead
            tiers cap this regardless of cost.
  h_econ  : the economic stop under a fixed cost curve tier_cost(k)=coef*base^(k-1):
            largest contiguous k s.t. every tier<=k pays its marginal cost.
            By construction h_econ <= h_reach.
  h_star  : the survival-optimal height from a Monte-Carlo shock stream (the
            dynamic check that h_econ is the right predictor).

Predictions
-----------
  (1) E[h_reach], E[h_econ], E[h*] all RISE with density rho.
  (2) h_econ <= h_reach <= L always; gaps bite hardest at low rho.
  (3) E[h_reach] has a clean closed form: with i.i.d. occupancy prob rho,
      P(first gap at height k) = rho^(k-1)*(1-rho), so
      E[h_reach] = sum_{k>=1} k * rho^k * (1-rho) / ... -> = rho/(1-rho) truncated at L.
  (4) BACK-loaded harm is 'un-governable-deep': even dense lattices won't pay to
      climb to the deep payoff because the cheap early rungs don't cover their cost
      -- so harm PROFILE matters as much as density.
"""
from __future__ import annotations
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
os.makedirs("results", exist_ok=True)

L = 8                 # max lattice height considered
P_EXCITE = 0.6
INST_SCALE = 0.08
COEF, BASE = 0.05, 1.4   # a fixed, middling cost curve for the density sweep


def sample_lattice(rho, harm_profile, budget, rng):
    """Return dict height-> harm for occupied resolvable heights (1..L)."""
    occupied = [k for k in range(1, L + 1) if rng.random() < rho]
    if not occupied:
        return {}
    if harm_profile == "front":
        w = np.array([1.0 / k for k in occupied])
    elif harm_profile == "flat":
        w = np.ones(len(occupied))
    elif harm_profile == "back":
        w = np.array([float(k) for k in occupied])
    else:
        raise ValueError(harm_profile)
    w = w / w.sum()
    return {k: float(budget * wi) for k, wi in zip(occupied, w)}


def tier_cost(k):
    return COEF * (BASE ** (k - 1))


def h_reach(harm_at):
    """Contiguous structural cap = first empty height minus 1."""
    h = 0
    for k in range(1, L + 1):
        if harm_at.get(k, 0.0) > 0:
            h = k
        else:
            break
    return h


def h_econ(harm_at):
    """Largest contiguous k where every tier<=k pays its marginal cost."""
    h = 0
    for k in range(1, L + 1):
        value_k = P_EXCITE * INST_SCALE * harm_at.get(k, 0.0)
        if harm_at.get(k, 0.0) > 0 and value_k >= tier_cost(k):
            h = k
        else:
            break
    return h


def h_star_mc(harm_at, novelty=0.35, steps=120, seeds=30):
    """Monte-Carlo survival-optimal height for this lattice."""
    def net_at(height):
        means = []
        for s in range(seeds):
            rng = np.random.default_rng(4242 + 17 * height + s)
            adapt = 0.0
            stack_tax = sum(tier_cost(k) for k in range(1, height + 1))
            perfs = []
            for _ in range(steps):
                nv = float(np.clip(novelty + rng.normal(0, 0.1), 0, 1))
                # instability from resolvable paradoxes still ALIVE (level > height)
                instab = sum(h for k, h in harm_at.items()
                             if k > height and rng.random() < P_EXCITE)
                # generative floor always alive -> self-amendment channel
                adapt += 0.25 * nv * (1.0 - adapt)
                gen_bonus = adapt * (0.5 + 2.5 * nv)
                perfs.append(1.0 - INST_SCALE * instab - stack_tax + gen_bonus)
            means.append(np.mean(perfs))
        return np.mean(means)
    nets = [net_at(H) for H in range(0, L + 1)]
    return int(np.argmax(nets))


def E_h_reach_analytic(rho):
    """Expected contiguous reach with i.i.d. occupancy prob rho, truncated at L.
    P(reach = j) = rho^j * (1-rho) for j<L, plus rho^L for j=L."""
    E = 0.0
    for j in range(0, L):
        E += j * (rho ** j) * (1 - rho)
    E += L * (rho ** L)
    return E


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    rhos = np.linspace(0.2, 1.0, 17)
    profiles = ["front", "flat", "back"]
    N = 400            # lattices sampled per (rho, profile)
    BUDGET = 12.0

    results = {"rhos": rhos.tolist(), "profiles": profiles, "L": L,
               "coef": COEF, "base": BASE, "budget": BUDGET}

    # ---- density sweep, front-loaded harm (the canonical case) ---- #
    print("=== density sweep (front-loaded harm) ===")
    curves = {"h_reach": [], "h_econ": [], "h_star": [], "h_reach_analytic": []}
    for rho in rhos:
        rng = np.random.default_rng(int(rho * 1000))
        hr, he, hs = [], [], []
        for _ in range(N):
            lat = sample_lattice(rho, "front", BUDGET, rng)
            hr.append(h_reach(lat)); he.append(h_econ(lat))
        # h* is expensive; sample a subset
        rng2 = np.random.default_rng(int(rho * 1000) + 7)
        for _ in range(60):
            lat = sample_lattice(rho, "front", BUDGET, rng2)
            hs.append(h_star_mc(lat, seeds=20, steps=90))
        curves["h_reach"].append(float(np.mean(hr)))
        curves["h_econ"].append(float(np.mean(he)))
        curves["h_star"].append(float(np.mean(hs)))
        curves["h_reach_analytic"].append(E_h_reach_analytic(rho))
        print(f"  rho={rho:.2f}: E[h_reach]={np.mean(hr):.2f} "
              f"(analytic {E_h_reach_analytic(rho):.2f})  "
              f"E[h_econ]={np.mean(he):.2f}  E[h*]={np.mean(hs):.2f}")
    results["front_curves"] = curves

    # ---- harm-profile comparison at fixed density ---- #
    print("\n=== harm profile comparison (rho=0.9) ===")
    prof_econ = {}
    for prof in profiles:
        rng = np.random.default_rng(99)
        he = [h_econ(sample_lattice(0.9, prof, BUDGET, rng)) for _ in range(N)]
        prof_econ[prof] = float(np.mean(he))
        print(f"  profile={prof:5s}: E[h_econ]={np.mean(he):.2f}")
    results["profile_econ_rho0.9"] = prof_econ

    # ---- heatmap: E[h_econ] over (density, profile-skew) ---- #
    skews = ["front", "flat", "back"]
    grid = np.zeros((len(skews), len(rhos)))
    for i, prof in enumerate(skews):
        for j, rho in enumerate(rhos):
            rng = np.random.default_rng(500 + i * 100 + int(rho * 50))
            he = [h_econ(sample_lattice(rho, prof, BUDGET, rng)) for _ in range(N)]
            grid[i, j] = np.mean(he)
    results["heatmap_h_econ"] = grid.tolist()

    with open("results/thread1_lattice_density.json", "w") as f:
        json.dump(results, f, indent=2)

    # ============================ FIGURES ============================ #
    BLUE, GREEN, RED, GREY = "#1f77b4", "#2ca02c", "#d62728", "#7f7f7f"

    # FIG 9: E[h] vs density, three heights + analytic overlay
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    ax.plot(rhos, curves["h_reach"], color=BLUE, lw=2.2, marker="o", ms=4,
            label="E[h_reach]  (structural cap)")
    ax.plot(rhos, curves["h_reach_analytic"], color=BLUE, ls="--", lw=1.4,
            label="  analytic  rho-occupancy prediction")
    ax.plot(rhos, curves["h_econ"], color=GREEN, lw=2.2, marker="s", ms=4,
            label="E[h_econ]  (economic stop)")
    ax.plot(rhos, curves["h_star"], color=RED, lw=2.0, marker="^", ms=5,
            label="E[h*]  (Monte-Carlo optimum)")
    ax.set_xlabel("lattice density  rho  (fraction of rungs that carry a resolvable paradox)")
    ax.set_ylabel("expected governable height")
    ax.set_title("THREAD 1  Lattice density sets the governable height\n"
                 "gaps cap the climb; density raises it (front-loaded harm)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left"); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig("figures/fig9_density_vs_height.png", dpi=140); plt.close(fig)

    # FIG 10: heatmap E[h_econ] over (profile, density)
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    im = ax.imshow(grid, origin="lower", aspect="auto", cmap="viridis",
                   extent=[rhos[0], rhos[-1], -0.5, len(skews) - 0.5])
    ax.set_yticks(range(len(skews))); ax.set_yticklabels(
        ["front (cheap early)", "flat", "back (deep payoff)"])
    cbar = fig.colorbar(im, ax=ax); cbar.set_label("E[h_econ]")
    ax.set_xlabel("lattice density  rho")
    ax.set_title("THREAD 1  Harm PROFILE matters as much as density\n"
                 "back-loaded harm stays un-governable-deep even when dense")
    fig.tight_layout(); fig.savefig("figures/fig10_profile_density_heatmap.png", dpi=140); plt.close(fig)

    # FIG 11: governable-height distribution at 3 densities
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    for rho, c in [(0.4, BLUE), (0.7, GREEN), (1.0, RED)]:
        rng = np.random.default_rng(int(rho * 333))
        hr = [h_reach(sample_lattice(rho, "front", BUDGET, rng)) for _ in range(2000)]
        vals, counts = np.unique(hr, return_counts=True)
        ax.plot(vals, counts / counts.sum(), lw=2.0, marker="o", color=c,
                label=f"rho = {rho}")
    ax.set_xlabel("structural cap  h_reach")
    ax.set_ylabel("probability")
    ax.set_title("THREAD 1  Distribution of the governable height\n"
                 "low density -> mass piled at low heights (frequent dead tiers)")
    ax.legend(frameon=False, fontsize=9); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig("figures/fig11_height_distribution.png", dpi=140); plt.close(fig)

    print("\nSaved figures/fig9, fig10, fig11 and results/thread1_lattice_density.json")
