#!/usr/bin/env python3
"""Figures for section 10: the v_p prime law and the non-cyclic rank phenomenon."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)

prime = json.load(open("results/cohomology_general_prime.json"))
noncyc = json.load(open("results/cohomology_general_noncyclic.json"))


def vp(n, p):
    k = 0
    while n % p == 0:
        k += 1; n //= p
    return k


# --------------------------------------------------------------------------- #
# fig23: the v_p law across p=2,3,5 -- three-phase structure per prime.        #
# --------------------------------------------------------------------------- #
def fig23():
    primes = [2, 3, 5]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    # fragile threshold per prime (observed): p=2 -> v>=3 ; p odd -> v>=2
    for ax, p in zip(axes, primes):
        pr = [r for r in prime if r["p"] == p]
        Ns = [r["N"] for r in pr]
        # phase level: 0 rigid, 1 fragile, 2 robust-generative
        def phase(r):
            if r["max_H2"] == 1: return 0                 # rigid
            if r["fragile"]: return 1                     # fragile
            return 2                                      # robust generative
        levels = [phase(r) for r in pr]
        colors = {0: "#d62728", 1: "#ff7f0e", 2: "#2ca02c"}
        ax.bar(Ns, levels, color=[colors[l] for l in levels])
        thr = 3 if p == 2 else 2
        ax.set_title(f"G = Z_{p}\nrigid unless {p}|N;  fragile once v_{p}(N) >= {thr}")
        ax.set_xlabel("module  N")
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(["RIGID", "FRAGILE", "ROBUST"])
        ax.grid(axis="y", ls=":", alpha=0.4)
    axes[0].set_ylabel("phase")
    from matplotlib.patches import Patch
    axes[-1].legend(handles=[Patch(color="#d62728", label="RIGID  (p not | N)"),
                             Patch(color="#ff7f0e", label="FRAGILE (deep p-torsion)"),
                             Patch(color="#2ca02c", label="ROBUST  (shallow p-torsion)")],
                    fontsize=8, loc="upper right")
    fig.suptitle("Section 10: the v_p prime law -- generativity needs p-torsion in the "
                 "value grain,\nand becomes frame-fragile only when that p-torsion is deep",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("figures/fig23_vp_prime_law.png", dpi=130)
    plt.close(fig)
    print("wrote figures/fig23_vp_prime_law.png")


# --------------------------------------------------------------------------- #
# fig24: non-cyclic modules -- H^2 now has RANK; an action can collapse it.    #
# --------------------------------------------------------------------------- #
def fig24():
    # group by module, show |H2| per action, annotate invariants (the rank)
    mods = []
    for r in noncyc:
        mods.append((r["module"], r["action"], r["H2_order"], r["H2_invariants"]))
    modules = []
    for m, a, h, inv in mods:
        if m not in modules:
            modules.append(m)

    fig, ax = plt.subplots(figsize=(12, 6))
    xpos = 0; ticks = []; ticklabels = []
    palette = {"trivial": "#1f77b4", "swap": "#d62728", "shear": "#9467bd",
               "negate-Z4": "#2ca02c", "neg-both": "#2ca02c"}
    for m in modules:
        entries = [r for r in noncyc if r["module"] == m]
        for r in entries:
            a = r["action"]; h = r["H2_order"]; inv = r["H2_invariants"]
            c = palette.get(a, "#7f7f7f")
            ax.bar(xpos, h, color=c, edgecolor="black")
            label = "x".join(str(x) for x in inv) if inv else "trivial(1)"
            ax.text(xpos, h + 0.08, f"H2=Z_{label}" if inv else "1",
                    ha="center", va="bottom", fontsize=7, rotation=0)
            ax.text(xpos, -0.28, a, ha="center", va="top", fontsize=7, rotation=45)
            ticks.append(xpos); ticklabels.append("")
            xpos += 1
        # module separator label
        ax.text(xpos - len(entries) / 2.0 - 0.5, -1.15, m, ha="center",
                va="top", fontsize=10, fontweight="bold")
        xpos += 0.8
    ax.set_ylabel("|H^2(Z_2, M)|")
    ax.set_ylim(-1.4, 5)
    ax.set_xticks([])
    ax.set_title("Section 10: non-cyclic modules give the generative class a RANK\n"
                 "Z2xZ2 trivial -> H^2 = Z2xZ2 (a rank-2 generative core); but 'swap' "
                 "or 'shear' collapses it to 1.\nThe scalar v_p invariant is replaced by "
                 "the p-rank of p-torsion, and a single frame-change can erase whole dimensions.")
    ax.axhline(1, ls="--", color="gray", lw=0.8)
    ax.grid(axis="y", ls=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig("figures/fig24_noncyclic_rank.png", dpi=130)
    plt.close(fig)
    print("wrote figures/fig24_noncyclic_rank.png")


if __name__ == "__main__":
    fig23()
    fig24()
