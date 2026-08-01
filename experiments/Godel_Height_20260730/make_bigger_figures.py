#!/usr/bin/env python3
"""Figures for section 14.
fig31 -- bigger/mixed frame-bundles: the two sec-13 facts survive (trivial
         maximizes rank; module-dependent floor), across G=Z2^3 and Z4xZ2.
fig32 -- the collapse characterization: P3 (even factors pair up) predicts
         collapse 7/8, the lone miss (Z8) being the separate sec-9 deep channel.
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
BIG = json.load(open("results/cohomology_bigger.json"))
COL = json.load(open("results/cohomology_collapse.json"))


def fig31():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 5.6))
    # LEFT: trivial rank (max) vs floor (min) per (G, M)
    entries = []
    for G in ["Z2xZ2xZ2", "Z4xZ2"]:
        for name, info in BIG[G].items():
            if info.get("all_skipped"): continue
            entries.append((f"{G}\non {name}", info["trivial_rank"], info["rank_min"]))
    labels = [e[0] for e in entries]
    triv = [e[1] for e in entries]
    floor = [e[2] for e in entries]
    x = np.arange(len(entries)); w = 0.4
    axL.bar(x - w/2, triv, w, label="trivial-action rank (= MAX over all actions)",
            color="#1f77b4")
    axL.bar(x + w/2, floor, w, label="floor (MIN rank over all actions)", color="#d62728")
    for xi, (t, f) in enumerate(zip(triv, floor)):
        axL.text(xi - w/2, t + 0.15, str(t), ha="center", fontsize=7)
        axL.text(xi + w/2, f + 0.15, str(f), ha="center", fontsize=7)
    axL.set_xticks(x); axL.set_xticklabels(labels, fontsize=7, rotation=0)
    axL.set_ylabel("rank of generative core  H\u00b2(G, M)")
    axL.set_title("Bigger / mixed frame-bundles: both sec-13 facts SURVIVE\n"
                  "trivial always maximizes (blue \u2265 red always); floor > 0 always",
                  fontsize=10)
    axL.legend(fontsize=8, loc="upper right"); axL.grid(alpha=0.3, axis="y")

    # RIGHT: collapse predictor. bar per module, colored by collapse, marker for P3.
    rows = COL["rows"]
    names = [r["module"] for r in rows]
    minrank = [r["min_rank"] for r in rows]
    coll = [r["collapses"] for r in rows]
    p3 = [r["P3_pairable_exponents"] for r in rows]
    xr = np.arange(len(rows))
    colors = ["#2ca02c" if c else "#999999" for c in coll]
    axR.bar(xr, minrank, color=colors, edgecolor="white")
    for i, r in enumerate(rows):
        pred = "P3\u2713" if p3[i] else "P3\u2717"
        agree = (p3[i] == coll[i])
        axR.text(i, minrank[i] + 0.05,
                 f"{pred}\n{'ok' if agree else 'MISS'}",
                 ha="center", va="bottom", fontsize=7,
                 color="black" if agree else "#d62728")
    # mark Z8 as the deep-channel exception
    if "Z8" in names:
        j = names.index("Z8")
        axR.annotate("Z8: collapses by the\nsec-9 DEEP channel\n(8|N), not by pairing",
                     xy=(j, 0.05), xytext=(j + 0.2, 1.3), fontsize=7, color="#d62728",
                     arrowprops=dict(arrowstyle="->", color="#d62728"))
    axR.set_xticks(xr); axR.set_xticklabels(names, fontsize=8, rotation=30, ha="right")
    axR.set_ylabel("min rank of H\u00b2(Z\u2082, M) over all order-2 actions")
    axR.set_title("Collapse characterization (cyclic G=Z\u2082): P3 predicts 7/8\n"
                  "green = collapses (min rank 0);  'pair up the 2-torsion' is the invariant",
                  fontsize=10)
    axR.set_ylim(0, 3.4); axR.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig("figures/fig31_bigger_and_collapse.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote figures/fig31_bigger_and_collapse.png")


def fig32():
    """The new phenomenon: H^2 stays elementary for elementary-abelian frame
    groups, but acquires Z4 summands once the frame group has a Z4 direction."""
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    rows = []
    for G in ["Z2xZ2xZ2", "Z4xZ2"]:
        for name, info in BIG[G].items():
            if info.get("all_skipped"): continue
            has4 = any("4" in k for k in info["spectrum"])
            rows.append((f"{G}\non {name}", has4, "Z4-dir" if "4" in G else "elem-ab"))
    labels = [r[0] for r in rows]
    has4 = [1 if r[1] else 0 for r in rows]
    frame_has_z4 = ["#d62728" if r[2] == "Z4-dir" else "#1f77b4" for r in rows]
    x = np.arange(len(rows))
    ax.bar(x, has4, color=frame_has_z4, edgecolor="white")
    for i, r in enumerate(rows):
        ax.text(i, (1 if r[1] else 0) + 0.03,
                "Z\u2084 summand\nin H\u00b2" if r[1] else "elementary\n(all Z\u2082)",
                ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7)
    ax.set_yticks([0, 1]); ax.set_yticklabels(["H\u00b2 elementary", "H\u00b2 has Z\u2084"])
    ax.set_ylim(0, 1.5)
    ax.set_title("NEW (sec 14): the FRAME GROUP's torsion depth injects higher torsion\n"
                 "H\u00b2 acquires a Z\u2084 summand ONLY when G has a Z\u2084 direction (red), "
                 "never for elementary-abelian G (blue)", fontsize=9.5)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#d62728", label="frame group has a Z\u2084 direction"),
                        Patch(color="#1f77b4", label="frame group elementary-abelian")],
              fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig("figures/fig32_frame_torsion_injection.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote figures/fig32_frame_torsion_injection.png")


if __name__ == "__main__":
    fig31()
    fig32()
