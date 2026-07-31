#!/usr/bin/env python3
"""Figures for section 11: the exhaustive rank ladder (push 1) and the
cyclic-vs-non-cyclic frame-group break (push 2)."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
rank = json.load(open("results/cohomology_rank_law.json"))["results"]


def fig25():
    """Push 1: for each module, the distribution of H^2 ranks over ALL order-2
    actions -- a stacked bar showing the rank ladder, plus the refuted-collapse mark."""
    mods = [r for r in rank if r["module"] != "Z3xZ3"]  # keep 2-groups
    names = [r["module"] for r in mods]
    # rank of each H2 type key
    def rank_of(key):
        return 0 if key == "trivial" else key.count("Z")
    # collect per module: dict rank -> count
    maxrank = 3
    data = np.zeros((len(mods), maxrank + 1))
    for i, r in enumerate(mods):
        for key, cnt in r["distribution_of_H2_types"].items():
            data[i, rank_of(key)] += cnt
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4"]
    labels = ["rank 0 (collapsed / gauge)", "rank 1", "rank 2", "rank 3"]
    bottom = np.zeros(len(mods))
    for k in range(maxrank + 1):
        ax.bar(names, data[:, k], bottom=bottom, color=colors[k], label=labels[k],
               edgecolor="white")
        bottom += data[:, k]
    # annotate whether full collapse (rank 0) is reachable
    for i, r in enumerate(mods):
        killable = r["some_action_kills_class"]
        ax.text(i, bottom[i] + 0.3, "collapse\u2713" if killable else "no full\ncollapse",
                ha="center", va="bottom", fontsize=8,
                color="#d62728" if killable else "#555")
    ax.set_ylabel("number of order-2 actions giving that H\u00b2 rank")
    ax.set_title("Section 11, push 1: EXHAUSTIVE rank ladder of H\u00b2(Z\u2082, M) over ALL "
                 "order-2 actions\n"
                 "Full collapse to rank 0 is MODULE-DEPENDENT (refuted as a universal "
                 "law): Z\u2082\u00d7Z\u2084 and Z\u2082\u00b3 never fully collapse.")
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(axis="y", ls=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig("figures/fig25_rank_ladder.png", dpi=130)
    plt.close(fig)
    print("wrote figures/fig25_rank_ladder.png")


def fig26():
    """Push 2: cyclic vs non-cyclic frame group, same module M=Z2 (trivial).
    Bar of |H^2| / rank, showing the non-cyclic multiplication of generative rank."""
    groups = ["Z\u2082\n(cyclic)", "Z\u2084\n(cyclic)", "Z\u2082\u00d7Z\u2082\n(non-cyclic)"]
    ranks = [1, 1, 3]
    orders = [2, 2, 8]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5))
    cols = ["#1f77b4", "#1f77b4", "#d62728"]
    a1.bar(groups, ranks, color=cols, edgecolor="black")
    for i, v in enumerate(ranks):
        a1.text(i, v + 0.05, f"(Z\u2082)^{v}" if v > 1 else "Z\u2082",
                ha="center", va="bottom", fontsize=11)
    a1.set_ylabel("rank of generative core  H\u00b2(G, Z\u2082)")
    a1.set_title("Frame-group shape controls generative RANK\n"
                 "same module M=Z\u2082, trivial action")
    a1.set_ylim(0, 3.7)
    a1.grid(axis="y", ls=":", alpha=0.4)

    # the v2 law survival panel: cyclic -> a bit; non-cyclic -> grows as 3r
    r = np.arange(1, 5)
    a2.plot(r, [1] * len(r), "o--", color="#1f77b4", label="cyclic G (Z\u2082 or Z\u2084): rank = 1, a BIT")
    a2.plot(r, 3 * r, "s-", color="#d62728", label="non-cyclic G=Z\u2082\u00d7Z\u2082: rank = 3r (LHS)")
    a2.scatter([1], [3], s=160, facecolors="none", edgecolors="#d62728", linewidths=2,
               zorder=5, label="DIRECT-verified (r=1): rank 3")
    a2.set_xlabel("F\u2082-rank r of the module M = (Z\u2082)^r")
    a2.set_ylabel("rank of H\u00b2(G, M)")
    a2.set_title("The section-9 single-invariant law is a CYCLIC-G artifact\n"
                 "non-cyclic frame groups multiply generative rank by 3 per generator")
    a2.set_xticks(r)
    a2.legend(fontsize=8, loc="upper left")
    a2.grid(ls=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig("figures/fig26_noncyclic_framegroup.png", dpi=130)
    plt.close(fig)
    print("wrote figures/fig26_noncyclic_framegroup.png")


if __name__ == "__main__":
    fig25()
    fig26()
