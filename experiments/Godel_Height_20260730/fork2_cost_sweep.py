#!/usr/bin/env python3
"""
fork2_cost_sweep.py
==================
FORK 2: stress the flat top.

M2 found a single-peaked performance-vs-height curve with optimum h* = 2, but the
peak was flat (h=1 vs h=2 within noise) and h* depends on the cost curve. This
fork maps the WHOLE cost -> h* surface. The cost of tier k is

    tier_cost(k) = coef * base**(k-1)

We sweep (coef, base) over a wide grid and, for each, find the survival-optimal
Godel height h*. Questions:

  * Where does h* = 0 (never build oversight), 1, 2, ..., up to the logical
    fixed point h_fix = 5?
  * Under what cost regime does it EVER pay to climb all the way to logical
    closure (h* = h_fix)?  -> the "climb-to-closure" corner.
  * Is the flat top a knife-edge or a broad plateau? i.e. how large a region of
    cost-space maps to each h*?

We also lay an ANALYTIC prediction of the jump locations over the Monte-Carlo
result: tier k pays iff its expected dissolved instability >= its cost, i.e.

    P_excite * inst_scale * harm_dissolved_at(k)  >=  coef * base**(k-1)

and h* is the largest contiguous k from 1 for which every tier <= k pays.
Because value is front-loaded and cost grows, h* is where marginal value first
falls below marginal cost.
"""
from __future__ import annotations
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap

from godel_stack_sim import default_paradox_bag, Institution, Paradox

os.makedirs("figures", exist_ok=True)
os.makedirs("results", exist_ok=True)

BAG = default_paradox_bag()
H_FIX = 5
MAX_H = 7
P_EXCITE = 0.6      # matches Institution.step (rng<0.6)
INST_SCALE = 0.08   # matches Institution.step (0.08*instability)

# harm dissolved when you ADD tier k = sum of harms of paradoxes with dissolves_at==k
HARM_AT = {}
for p in BAG:
    if p.dissolves_at is not None:
        HARM_AT[p.dissolves_at] = HARM_AT.get(p.dissolves_at, 0.0) + p.harm


def make_tier_cost(coef, base):
    return lambda k: coef * (base ** (k - 1))


def run_perf(height, tier_cost_fn, novelty=0.35, steps=150, seeds=60):
    """Mean net performance at a given height under a given cost curve."""
    means = []
    for s in range(seeds):
        rng = np.random.default_rng(9000 + 137 * height + s)
        inst = Institution(height=height,
                           paradoxes=[Paradox(**vars(p)) for p in BAG],
                           keep_residue=True, rng=rng)
        # monkey-patch this institution's stack_tax to use the swept cost curve
        inst_stack_tax = sum(tier_cost_fn(k) for k in range(1, height + 1))
        perfs = []
        for _ in range(steps):
            nv = float(np.clip(novelty + rng.normal(0, 0.1), 0, 1))
            # replicate step() but with swept tax
            excited = [q for q in inst.paradoxes if rng.random() < P_EXCITE]
            instability = sum(q.harm for q in excited if q.alive_at(height))
            gen_bonus = 0.0
            if inst.residue_alive():
                inst.adapt += 0.25 * nv * (1.0 - inst.adapt)
                gen_bonus = inst.adapt * (0.5 + 2.5 * nv)
            perf = 1.0 - INST_SCALE * instability - inst_stack_tax + gen_bonus
            perfs.append(perf)
        means.append(np.mean(perfs))
    return float(np.mean(means))


def h_star_mc(tier_cost_fn, **kw):
    perfs = [run_perf(H, tier_cost_fn, **kw) for H in range(0, MAX_H + 1)]
    return int(np.argmax(perfs)), perfs


def h_star_analytic(coef, base):
    """Largest contiguous k from 1 s.t. every tier<=k pays its marginal cost."""
    h = 0
    for k in range(1, MAX_H + 1):
        value_k = P_EXCITE * INST_SCALE * HARM_AT.get(k, 0.0)
        cost_k = coef * (base ** (k - 1))
        if value_k >= cost_k:
            h = k
        else:
            break
    return h


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    coefs = np.linspace(0.01, 0.60, 24)
    bases = np.linspace(1.10, 2.50, 20)

    print("Building h*(coef, base) surface (Monte-Carlo)...")
    grid_mc = np.zeros((len(bases), len(coefs)), dtype=int)
    grid_an = np.zeros((len(bases), len(coefs)), dtype=int)
    for i, base in enumerate(bases):
        for j, coef in enumerate(coefs):
            tc = make_tier_cost(coef, base)
            hstar, _ = h_star_mc(tc, seeds=40, steps=120)
            grid_mc[i, j] = hstar
            grid_an[i, j] = h_star_analytic(coef, base)
        print(f"  base={base:.2f} done")

    agree = float((grid_mc == grid_an).mean())
    print(f"\nMonte-Carlo vs analytic agreement: {agree*100:.1f}%")

    results = {
        "coefs": coefs.tolist(), "bases": bases.tolist(),
        "h_star_mc": grid_mc.tolist(), "h_star_analytic": grid_an.tolist(),
        "mc_analytic_agreement": agree, "h_fix": H_FIX,
        "climb_to_closure_fraction": float((grid_mc >= H_FIX).mean()),
        "dont_bother_fraction": float((grid_mc == 0).mean()),
    }
    with open("results/fork2_cost_sweep.json", "w") as f:
        json.dump(results, f, indent=2)

    # ---- FIG 5: heatmap of h*(coef, base) ---- #
    levels = list(range(0, MAX_H + 2))
    cmap = ListedColormap(plt.cm.viridis(np.linspace(0, 1, MAX_H + 1)))
    norm = BoundaryNorm(levels, cmap.N)
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    im = ax.imshow(grid_mc, origin="lower", aspect="auto", cmap=cmap, norm=norm,
                   extent=[coefs[0], coefs[-1], bases[0], bases[-1]])
    cs = ax.contour(coefs, bases, grid_an, levels=np.arange(0.5, MAX_H + 1),
                    colors="white", linewidths=1.0, linestyles="--")
    ax.clabel(cs, fmt=lambda v: f"h*={int(round(v))}", fontsize=7)
    cbar = fig.colorbar(im, ax=ax, ticks=range(MAX_H + 1))
    cbar.set_label("survival-optimal Godel height h*")
    ax.set_xlabel("cost coefficient  (coef)")
    ax.set_ylabel("cost growth base")
    ax.set_title("FORK 2  h*(cost) surface\n"
                 "colour = Monte-Carlo h*;  white dashed = analytic jump contours")
    fig.tight_layout(); fig.savefig("figures/fig5_cost_heatmap.png", dpi=140); plt.close(fig)

    # ---- FIG 6: staircase h* vs coef at fixed bases ---- #
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    fine_coefs = np.linspace(0.005, 0.6, 120)
    for base in [1.2, 1.6, 2.0]:
        hs = [h_star_analytic(c, base) for c in fine_coefs]
        ax.step(fine_coefs, hs, where="post", lw=2.0, label=f"base = {base}")
    ax.axhline(H_FIX, color="k", ls=":", lw=1.2, label=f"logical fixed point h_fix = {H_FIX}")
    ax.set_xlabel("cost coefficient  (coef)")
    ax.set_ylabel("survival-optimal Godel height h*")
    ax.set_title("FORK 2  The flat top is a STAIRCASE\n"
                 "h* jumps down as oversight gets more expensive")
    ax.set_yticks(range(0, MAX_H + 1)); ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout(); fig.savefig("figures/fig6_hstar_staircase.png", dpi=140); plt.close(fig)

    print("\n=== summary ===")
    print(f"  fraction of cost-space where h* reaches logical closure (>= {H_FIX}): "
          f"{results['climb_to_closure_fraction']*100:.1f}%")
    print(f"  fraction of cost-space where h* = 0 (don't build oversight): "
          f"{results['dont_bother_fraction']*100:.1f}%")
    # where does closure happen?
    idx = np.argwhere(grid_mc >= H_FIX)
    if len(idx):
        cheapest = min(coefs[j] for _, j in idx)
        print(f"  climb-to-closure requires coef <= ~{cheapest:.3f} (very cheap tiers)")
    print("  Saved figures/fig5, figures/fig6, results/fork2_cost_sweep.json")
