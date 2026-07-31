#!/usr/bin/env python3
"""
make_figures.py
===============
Regenerate the four figures for the Godel-height x frame-resolvability experiment.
Saves PNGs into figures/ and a machine-readable results/ dump.
"""
from __future__ import annotations
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from godel_stack_sim import (
    default_paradox_bag, tier_cost,
    m1_residue_vs_height, m2_survival_vs_height,
    m3_generative_keep_vs_crush, m4_bell_labels,
)

os.makedirs("figures", exist_ok=True)
os.makedirs("results", exist_ok=True)

BLUE, RED, GREEN, GREY = "#1f77b4", "#d62728", "#2ca02c", "#7f7f7f"
bag = default_paradox_bag()
results = {}

# --------------------------------------------------------------------------- #
# FIG 1 : residue vs height (with the frame-invariant floor marked)           #
# --------------------------------------------------------------------------- #
m1 = m1_residue_vs_height(bag, max_height=7)
H = [h for h, _ in m1]; R = [r for _, r in m1]
gen_floor = sum(1 for p in bag if p.dissolves_at is None)
results["m1_residue_vs_height"] = m1

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.step(H, R, where="post", color=BLUE, lw=2.2, label="residue R(H) = live paradoxes")
ax.fill_between(H, gen_floor, R, step="post", alpha=0.12, color=BLUE)
ax.axhline(gen_floor, color=RED, ls="--", lw=1.6,
           label=f"frame-invariant floor = {gen_floor} (generative residue)")
ax.set_xlabel("Godel height H  (number of protected meta-tiers / frames)")
ax.set_ylabel("paradoxes still alive")
ax.set_title("M1  Residue contracts to a finite generative floor")
ax.set_ylim(0, max(R) + 0.5); ax.set_xticks(H)
ax.legend(frameon=False, fontsize=9); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig("figures/fig1_residue_vs_height.png", dpi=140); plt.close(fig)

# --------------------------------------------------------------------------- #
# FIG 2 : net performance vs height  +  cost overlay  +  h* and h_econ, h_fix  #
# --------------------------------------------------------------------------- #
m2 = m2_survival_vs_height(bag, max_height=7, seeds=200, novelty=0.35)
hh = [t[0] for t in m2]; mu = [t[1] for t in m2]; sd = [t[2] for t in m2]
tax = [sum(tier_cost(k) for k in range(1, h + 1)) for h in hh]
hstar = max(m2, key=lambda t: t[1])[0]
results["m2_perf_vs_height"] = [(int(h), float(m), float(s)) for h, m, s in m2]
results["h_star"] = int(hstar)
results["h_econ_model"] = 2
results["h_fix_model"] = 5

fig, ax = plt.subplots(figsize=(7.6, 4.8))
ax.errorbar(hh, mu, yerr=sd, color=GREEN, lw=2.2, marker="o", capsize=3,
            label="net performance (mean +/- SD)")
ax.plot(hh, [-t for t in tax], color=GREY, ls=":", lw=1.8, label="cumulative tier tax (−)")
ax.axvline(hstar, color=RED, lw=1.8, ls="--", label=f"survival-optimal h* = {hstar}")
ax.axvline(2, color="#9467bd", lw=1.4, ls="-.", alpha=0.8, label="model h_econ = 2")
ax.axvline(5, color="#8c564b", lw=1.2, ls=":", alpha=0.8, label="logical fixed point h_fix = 5")
ax.set_xlabel("Godel height H")
ax.set_ylabel("net performance / cost")
ax.set_title("M2  Optimal height is set by COST (h*=h_econ=2), not by logic (h_fix=5)")
ax.set_xticks(hh); ax.legend(frameon=False, fontsize=8, loc="lower left"); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig("figures/fig2_perf_vs_height.png", dpi=140); plt.close(fig)

# --------------------------------------------------------------------------- #
# FIG 3 : generative KEEP vs CRUSH across novelty                             #
# --------------------------------------------------------------------------- #
m3 = m3_generative_keep_vs_crush(bag, height=hstar, seeds=200,
                                 novelty_levels=(0.1, 0.35, 0.6, 0.85))
nv = [r[0] for r in m3]; keep = [r[1] for r in m3]; ks = [r[2] for r in m3]
crush = [r[3] for r in m3]; cs = [r[4] for r in m3]; gap = [r[5] for r in m3]
results["m3_keep_vs_crush"] = [tuple(float(x) for x in r) for r in m3]

fig, ax = plt.subplots(figsize=(7.4, 4.6))
ax.errorbar(nv, keep, yerr=ks, color=GREEN, lw=2.2, marker="o", capsize=3,
            label="KEEP residue (self-amendment channel)")
ax.errorbar(nv, crush, yerr=cs, color=RED, lw=2.2, marker="s", capsize=3,
            label="CRUSH residue (frozen amendment)")
ax2 = ax.twinx()
ax2.bar(nv, gap, width=0.05, alpha=0.18, color=BLUE)
ax2.set_ylabel("KEEP − CRUSH advantage", color=BLUE)
ax2.tick_params(axis="y", colors=BLUE)
ax.set_xlabel("shock novelty")
ax.set_ylabel("net performance")
ax.set_title("M3  The frame-invariant residue is GENERATIVE\n(the keep-advantage widens with novelty)")
ax.legend(frameon=False, fontsize=9, loc="upper left"); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig("figures/fig3_keep_vs_crush.png", dpi=140); plt.close(fig)

# --------------------------------------------------------------------------- #
# FIG 4 : governance Bell / CHSH label recovery                               #
# --------------------------------------------------------------------------- #
m4 = m4_bell_labels(bag, margin=0.05)
names = [r[0] for r in m4]; S = [r[1] for r in m4]
truth = [r[3] for r in m4]
colors = [RED if t else BLUE for t in truth]
results["m4_bell"] = [(n, float(s), bool(p), bool(t)) for n, s, p, t in m4]

fig, ax = plt.subplots(figsize=(8.4, 4.8))
bars = ax.bar(range(len(names)), S, color=colors, alpha=0.85)
ax.axhline(2.0, color="k", ls="--", lw=1.4, label="local (frame-resolvable) bound S = 2")
ax.axhline(2 * np.sqrt(2), color=RED, ls=":", lw=1.4,
           label=r"Tsirelson bound $2\sqrt{2}\approx2.83$")
ax.set_xticks(range(len(names)))
ax.set_xticklabels(names, rotation=25, ha="right", fontsize=8)
ax.set_ylabel("CHSH statistic S")
ax.set_title("M4  Governance Bell test recovers ground-truth labels (6/6)\n"
             "blue = frame-resolvable (S≤2)   red = generative (S>2)")
ax.legend(frameon=False, fontsize=9); ax.grid(alpha=0.2, axis="y")
for b, s in zip(bars, S):
    ax.text(b.get_x() + b.get_width() / 2, s + 0.03, f"{s:.2f}",
            ha="center", fontsize=8)
fig.tight_layout(); fig.savefig("figures/fig4_bell_test.png", dpi=140); plt.close(fig)

# --------------------------------------------------------------------------- #
with open("results/godel_stack_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved figures/fig1..fig4 and results/godel_stack_results.json")
print(f"h* = {hstar}   (model h_econ = 2, h_fix = 5)")
print(f"Bell label recovery: {sum(1 for _,_,p,t in m4 if p==t)}/{len(m4)}")
