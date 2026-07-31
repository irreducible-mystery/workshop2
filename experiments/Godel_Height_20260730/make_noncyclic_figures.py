#!/usr/bin/env python3
"""Figures for section 12: the non-cyclic frame-group phase law.
fig27 -- SHAPE (not order) decides the generative-core rank; the C(k+1,2) staircase.
fig28 -- LAW L (rank = r*core) with the DIRECT/cap frontier marked.
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
D = json.load(open("results/cohomology_noncyclic_law.json"))


def fig27():
    """Two panels.
    LEFT  : same order, different shape -> different rank (DIRECT-verified order 4;
            order 8 shown as ring-prediction/open, visually distinguished).
    RIGHT : the C(k+1,2) staircase for G=(Z_2)^k, trivial coeffs, DIRECT vs ring.
    """
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.2))

    # ---- LEFT: shape controls rank at fixed order -----------------------------
    labels = ["Z4\n(cyclic, |G|=4)", "Z2xZ2\n(non-cyc, |G|=4)",
              "Z8\n(cyclic, |G|=8)", "Z2xZ4\n(mixed, |G|=8)", "Z2^3\n(elem-ab, |G|=8)"]
    ranks  = [1, 3, 1, None, 6]           # order-8: Z8=1 (Tate), Z2^3=6 (ring), Z2xZ4 OPEN
    verified = [True, True, False, False, False]
    xs = np.arange(len(labels))
    for i, (rk, ver) in enumerate(zip(ranks, verified)):
        if rk is None:
            axL.bar(i, 0.0)
            axL.text(i, 0.15, "OPEN\n(neither cyclic\nnor elem-ab)",
                     ha="center", va="bottom", fontsize=8, color="#555")
            continue
        color = "#1f77b4" if ver else "#c7c7c7"
        axL.bar(i, rk, color=color, edgecolor="white",
                hatch=None if ver else "//")
        tag = "DIRECT" if ver else "ring pred."
        axL.text(i, rk + 0.12, f"rank {rk}\n({tag})", ha="center", va="bottom",
                 fontsize=8, color="black" if ver else "#666")
    axL.set_xticks(xs); axL.set_xticklabels(labels, fontsize=8)
    axL.set_ylabel("rank of generative core  H$^2$(G, Z$_2$)")
    axL.set_ylim(0, 7)
    axL.set_title("Same |G|, different SHAPE -> different rank\n"
                  "(order 4 DIRECT-verified: 1 vs 3 refutes rank = f(|G|))",
                  fontsize=10)
    axL.axhline(0, color="k", lw=0.6)
    # bracket the order-4 pair
    axL.annotate("", xy=(0, 3.6), xytext=(1, 3.6),
                 arrowprops=dict(arrowstyle="<->", color="#d62728"))
    axL.text(0.5, 3.7, "same order 4,\nrank 1 vs 3", ha="center", va="bottom",
             fontsize=8, color="#d62728")

    # ---- RIGHT: the C(k+1,2) staircase for (Z_2)^k ---------------------------
    ks = np.arange(1, 6)
    core = ks * (ks + 1) // 2               # 1,3,6,10,15
    axR.plot(ks, core, "s-", color="#2ca02c", lw=2, ms=9,
             label=r"ring:  dim H$^2$((Z$_2$)$^k$, F$_2$) = $\binom{k+1}{2}$")
    # mark which are DIRECT-verified (k=1,2) vs capped (k>=3)
    axR.plot([1, 2], [1, 3], "o", color="#1f77b4", ms=13, mfc="none", mew=2.2,
             label="DIRECT-verified (k=1,2)")
    for k, c in zip(ks, core):
        tag = "verified" if k <= 2 else "capped 2$^{64}$\n(ring only)"
        axR.annotate(f"{c}\n{tag}", (k, c), textcoords="offset points",
                     xytext=(0, 12), ha="center", fontsize=8,
                     color="black" if k <= 2 else "#888")
    axR.axvspan(2.5, 5.5, color="#f2f2f2", zorder=0)
    axR.text(4, 2, "DIRECT cap frontier\n(2$^{64}$ cochains)", ha="center",
             fontsize=9, color="#888")
    axR.set_xlabel("k  (frame group G = (Z$_2$)$^k$)")
    axR.set_ylabel("rank of generative core")
    axR.set_title("Generative-core rank is set by the GROUP SHAPE\n"
                  "cyclic (k=1) = 1 bit;  each extra frame-direction adds a step",
                  fontsize=10)
    axR.set_xticks(ks); axR.legend(fontsize=8, loc="upper left"); axR.grid(alpha=0.3)

    fig.suptitle("Section 12 -- the non-cyclic frame-group law: rank = shape, not order",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig("figures/fig27_shape_sets_rank.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote figures/fig27_shape_sets_rank.png")


def fig28():
    """LAW L: rank H^2((Z2)^k, (Z2)^r) = r * core.  Lines for k=1 (core 1) and
    k=2 (core 3); markers filled where DIRECT-verified, hollow where capped."""
    rows = D["part_B"]
    fig, ax = plt.subplots(figsize=(8.2, 5.4))
    for k, core, col in [(1, 1, "#1f77b4"), (2, 3, "#d62728")]:
        rs = [row["r"] for row in rows if row["k"] == k]
        pred = [row["predict"] for row in rows if row["k"] == k]
        ver = [row["agree"] is True for row in rows if row["k"] == k]
        ax.plot(rs, pred, "-", color=col, lw=2,
                label=f"G=(Z$_2$)$^{k}$: rank = {core}$\\cdot$r  (core={core})")
        for r, p, v in zip(rs, pred, ver):
            ax.plot(r, p, "o", color=col, ms=12,
                    mfc=col if v else "white", mew=2)
            ax.annotate("DIRECT" if v else "capped\n(predict)", (r, p),
                        textcoords="offset points", xytext=(8, -4),
                        fontsize=8, color=col if v else "#888")
    ax.set_xlabel("F$_2$-rank r of the module  M = (Z$_2$)$^r$")
    ax.set_ylabel("rank of H$^2$(G, M)")
    ax.set_title("LAW L: each module generator adds an independent copy of the core\n"
                 "rank H$^2$((Z$_2$)$^k$, (Z$_2$)$^r$) = r $\\cdot$ dim H$^2$((Z$_2$)$^k$, F$_2$)",
                 fontsize=10)
    ax.set_xticks([1, 2, 3]); ax.legend(fontsize=9); ax.grid(alpha=0.3)
    ax.text(0.98, 0.03, "filled = DIRECT-verified   hollow = capped, ring-prediction only",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color="#666")
    fig.tight_layout()
    fig.savefig("figures/fig28_law_L.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote figures/fig28_law_L.png")


if __name__ == "__main__":
    fig27()
    fig28()
