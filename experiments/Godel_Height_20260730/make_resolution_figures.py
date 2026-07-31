#!/usr/bin/env python3
"""Figures for section 13: H^2(Z2xZ2, M) under NON-TRIVIAL actions via the
explicit Z[G]-resolution engine.
fig29 -- engine validation: resolution == LHS == bar/DIRECT on trivial action.
fig30 -- the non-trivial-action rank spectrum per module (the new numbers).
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
D = json.load(open("results/cohomology_resolution.json"))


def fig29():
    """Three independent methods agree on the trivial action -> engine trusted."""
    mods = ["Z2", "Z4", "Z2xZ2"]
    # |H2| from each method (bar & LHS computed in the verification step; hard-coded
    # here as the cross-checked constants, all == the resolution engine's output)
    resolution = [8, 8, 64]
    lhs        = [8, 8, 64]
    bar_direct = [8, 8, 64]
    x = np.arange(len(mods)); w = 0.25
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.bar(x - w, resolution, w, label="explicit Z[G]-resolution (this engine)",
           color="#1f77b4")
    ax.bar(x,      lhs,        w, label="LHS / K\u00fcnneth assoc-graded", color="#2ca02c")
    ax.bar(x + w,  bar_direct, w, label="bar resolution (independent enum)",
           color="#ff7f0e")
    for xi, v in zip(x, resolution):
        ax.text(xi, v + 1.2, f"|H\u00b2|={v}", ha="center", fontsize=9)
    ax.set_yscale("log", base=2)
    ax.set_xticks(x); ax.set_xticklabels([f"M={m}\n(trivial action)" for m in mods])
    ax.set_ylabel("|H\u00b2(Z\u2082\u00d7Z\u2082, M)|  (log\u2082)")
    ax.set_title("Section 13 engine validation: THREE independent methods, one answer\n"
                 "the resolution engine is trusted before it is used past the 4\u00b9\u2076 wall",
                 fontsize=10)
    ax.legend(fontsize=8, loc="upper left"); ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig("figures/fig29_engine_validation.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote figures/fig29_engine_validation.png")


def fig30():
    """The NEW result: rank spectrum of H^2(Z2xZ2, M) over all non-cyclic actions."""
    order = ["Z4", "Z2xZ2", "Z2xZ4", "Z4xZ4"]
    B = D["part_B"]
    maxrank = 6
    colors = {1: "#d62728", 2: "#ff7f0e", 3: "#e6c200",
              4: "#2ca02c", 5: "#17becf", 6: "#1f77b4"}
    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    bottoms = np.zeros(len(order))
    # build rank -> count per module
    rank_counts = {name: {r: 0 for r in range(1, maxrank + 1)} for name in order}
    for name in order:
        for inv_str, cnt in B[name]["spectrum"].items():
            r = len([c for c in inv_str.strip("[]").split(",") if c.strip()])
            rank_counts[name][r] += cnt
    for r in range(1, maxrank + 1):
        vals = [rank_counts[name][r] for name in order]
        if sum(vals) == 0:
            continue
        ax.bar(order, vals, bottom=bottoms, color=colors[r],
               edgecolor="white", label=f"rank {r}")
        bottoms += np.array(vals)
    # annotate trivial-action rank (the maximum) on each bar
    for i, name in enumerate(order):
        triv = len(B[name]["trivial_invariants"])
        mn = B[name]["rank_min"]
        ax.text(i, bottoms[i] + max(bottoms) * 0.02,
                f"trivial=rank {triv} (max)\nfloor=rank {mn}",
                ha="center", va="bottom", fontsize=8)
    ax.set_ylabel("number of commuting order-\u22642 action pairs giving that H\u00b2 rank")
    ax.set_xlabel("value module M  (frame group fixed at G = Z\u2082\u00d7Z\u2082)")
    ax.set_title("Section 13: H\u00b2(Z\u2082\u00d7Z\u2082, M) rank over ALL non-trivial non-cyclic actions\n"
                 "(computed by explicit Z[G]-resolution + SNF \u2014 strictly past the 4\u00b9\u2076 direct-enum wall)",
                 fontsize=10.5)
    ax.legend(fontsize=8, title="generative-core rank", ncol=6, loc="upper center",
              bbox_to_anchor=(0.5, -0.08))
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig("figures/fig30_nontrivial_action_spectrum.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote figures/fig30_nontrivial_action_spectrum.png")


if __name__ == "__main__":
    fig29()
    fig30()
