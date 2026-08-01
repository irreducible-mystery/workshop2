#!/usr/bin/env python3
"""Figures for section 15 (threads 1,2,3 turned into theory)."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

with open("results/cohomology_invariant_search4.json") as f:
    search = json.load(f)
with open("results/cohomology_theorems.json") as f:
    thm = json.load(f)
with open("results/cohomology_prove.json") as f:
    prove = json.load(f)

# ---------------------------------------------------------------------------
# fig33 : the collapse map over 2-groups -- what collapses, what floors, and the
# candidate-predicate scoreboard showing NO multiset-only predicate is exact.
# ---------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.2))

rows = search["data"]  # list of {E, collapse}
# order by (#factors, exps)
rows = sorted(rows, key=lambda r: (len(r["E"]), r["E"]))
labels = ["{" + ",".join(map(str, r["E"])) + "}" for r in rows]
collapse = [r["collapse"] for r in rows]
colors = ["#2ca02c" if c else "#d62728" for c in collapse]
x = np.arange(len(rows))
ax1.bar(x, [1]*len(rows), color=colors, edgecolor="black", linewidth=0.4)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=90, fontsize=7)
ax1.set_yticks([])
ax1.set_title("Collapse map: H2(Z2, M) over ALL involutions\n"
              "(green = collapses to 0; red = keeps an irreducible floor)  "
              "M = 2-group by 2-adic exponents", fontsize=10.5)
# annotate the four proven anchors
prov = {"{1}":"floor\n(T3)", "{2}":"floor\n(T3)", "{1,2}":"floor\n(T3)",
        "{3}":"deep\ncollapse\n(T2)", "{1,1}":"hyperbolic\ncollapse\n(T1)",
        "{2,2}":"hyperbolic\n(T1)"}
for i, lab in enumerate(labels):
    if lab in prov:
        ax1.text(i, 0.5, prov[lab], ha="center", va="center", fontsize=6.5,
                 color="white", fontweight="bold")
# mark the refuting flip pairs
def idx(lbl):
    for i,l in enumerate(labels):
        if l==lbl: return i
    return None
for a,b in [("{1,2}","{1,1,2}"), ("{1,2,2}","{2,2,2}")]:
    ia, ib = idx(a), idx(b)
    if ia is not None and ib is not None:
        ax1.annotate("", xy=(ib,1.06), xytext=(ia,1.06),
                     arrowprops=dict(arrowstyle="<->", color="black", lw=1.1))
        ax1.text((ia+ib)/2, 1.12, "verdict FLIPS\nsame-ish multiset",
                 ha="center", fontsize=6.8)
ax1.set_ylim(0, 1.25)

# right: predicate scoreboard
preds = [
    ("P1: 2-rank even", 12),
    ("P3: all exps pair", 10),
    ("n_shallow even", 15),
    ("shallow<=deep jokers", 17),
    ("best multiset-only", 17),
]
names = [p[0] for p in preds]
scores = [p[1] for p in preds]
n = search["n"]
yy = np.arange(len(preds))
bars = ax2.barh(yy, scores, color="#8888cc", edgecolor="black")
bars[-1].set_color("#e6a000")
ax2.axvline(n, color="green", ls="--", lw=1.5)
ax2.text(n+0.1, len(preds)-0.5, "exact\n=%d/%d" % (n, n), color="green", fontsize=8.5)
ax2.set_yticks(yy); ax2.set_yticklabels(names, fontsize=9)
ax2.set_xlabel("modules predicted correctly (of %d)" % n, fontsize=9)
ax2.set_xlim(0, n+2)
ax2.set_title("Threads 1&2: NO exponent-multiset predicate is exact\n"
              "P1 REFUTED (12/21); best multiset-only 17/21; the true rule\n"
              "needs the realizable off-diagonal (shear) structure, not just exps",
              fontsize=10.5)
for i, s in enumerate(scores):
    ax2.text(s+0.1, i, "%d/%d" % (s, n), va="center", fontsize=8)

plt.tight_layout()
plt.savefig("figures/fig33_collapse_invariant.png", dpi=130, bbox_inches="tight")
print("wrote figures/fig33_collapse_invariant.png")
plt.close()

# ---------------------------------------------------------------------------
# fig34 : Thread 3 -- the torsion-injection / exp bound.  Left: exp(H2)|exp(G)
# proven for cyclic G (all elementary); right: engine spectra scatter showing
# Z4-in-core appears only for exp(G)=4 frame groups.
# ---------------------------------------------------------------------------
fig, (bx1, bx2) = plt.subplots(1, 2, figsize=(14.5, 6))

# left: exp bound bar (cyclic G=Z2, worst exp seen =2)
t5 = thm["T5_exp_bound"]
bx1.bar([0], [t5["worst_exp"]], width=0.5, color="#2ca02c", edgecolor="black",
        label="worst exp(H2) over ALL M & involutions")
bx1.axhline(2, color="red", ls="--", lw=1.5, label="exp(G)=2 bound")
bx1.set_xticks([0]); bx1.set_xticklabels(["G = Z2\n(cyclic frame group)"], fontsize=9)
bx1.set_ylabel("exponent of H2(G, M)", fontsize=10)
bx1.set_ylim(0, 4.5)
bx1.set_title("THREAD 3 (proven-exhaustive): exp(H2(Z2,M)) | 2\n"
              "H2 is ALWAYS elementary abelian for a Z2 frame group\n"
              "(zero violations over the full cost-capped 2-group sweep)",
              fontsize=10.5)
bx1.legend(fontsize=8.5, loc="upper right")
bx1.text(0, t5["worst_exp"]+0.12, "2", ha="center", fontsize=13, fontweight="bold")

# right: engine spectra -- exp(H2) vs exp(G), from cohomology_bigger.json
with open("results/cohomology_bigger.json") as f:
    big = json.load(f)

pts = []  # (expG, maxfactor, has4)
for gname, sub in big.items():
    if gname == "validate_ok":
        continue
    expG = 4 if "4" in gname else 2
    for mname, rec in sub.items():
        for factstr in rec.get("spectrum", {}):
            facts = json.loads(factstr)
            mx = max(facts)
            pts.append((expG, mx, gname))
# jitter
rng = np.random.default_rng(0)
xs = np.array([p[0] for p in pts]) + rng.uniform(-0.12, 0.12, len(pts))
ys = np.array([p[1] for p in pts]) + rng.uniform(-0.12, 0.12, len(pts))
cols = ["#d62728" if p[1] >= 4 else "#1f77b4" for p in pts]
bx2.scatter(xs, ys, c=cols, s=55, edgecolor="black", linewidth=0.4, alpha=0.85)
# diagonal exp(H2)=exp(G) bound line
bx2.plot([1.5, 4.5], [1.5, 4.5], color="gray", ls=":", lw=1.3,
         label="exp(H2)=exp(G) bound")
bx2.fill_between([1.5, 4.5], [1.5, 4.5], [5, 5], color="red", alpha=0.05)
bx2.set_xticks([2, 4]); bx2.set_xlabel("exp(G)  (frame-group exponent)", fontsize=10)
bx2.set_yticks([2, 4]); bx2.set_ylabel("max invariant factor of H2  (core torsion depth)", fontsize=10)
bx2.set_xlim(1.5, 4.7); bx2.set_ylim(1.5, 4.7)
bx2.set_title("Torsion injection on the section-14 engine spectra:\n"
              "a Z4 summand in the core (red) appears ONLY at exp(G)=4;\n"
              "every point stays on/below exp(H2)=exp(G) (no violations)",
              fontsize=10.5)
from matplotlib.lines import Line2D
leg = [Line2D([0],[0],marker='o',color='w',markerfacecolor='#1f77b4',
              markeredgecolor='black',markersize=9,label='elementary core (max factor 2)'),
       Line2D([0],[0],marker='o',color='w',markerfacecolor='#d62728',
              markeredgecolor='black',markersize=9,label='core has a Z4 (max factor 4)'),
       Line2D([0],[0],color='gray',ls=':',label='exp(H2)=exp(G) bound')]
bx2.legend(handles=leg, fontsize=8.3, loc="upper left")

plt.tight_layout()
plt.savefig("figures/fig34_torsion_injection.png", dpi=130, bbox_inches="tight")
print("wrote figures/fig34_torsion_injection.png")
plt.close()
