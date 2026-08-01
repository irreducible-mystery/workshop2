#!/usr/bin/env python3
"""make_fork_figures.py — figures for Fork 1 (fig7) and the noise threshold (fig8)."""
from __future__ import annotations
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fork1_earn_label import ProbeParadox, chsh, confusion

os.makedirs("figures", exist_ok=True)
os.makedirs("results", exist_ok=True)

RED, BLUE, GREY, ORANGE = "#d62728", "#1f77b4", "#7f7f7f", "#ff7f0e"

paradoxes = [
    ProbeParadox("liar_two_valued",        "local",      False),
    ProbeParadox("goodhart_measurement",   "local",      False),
    ProbeParadox("order_effect",           "local",      False),
    ProbeParadox("nested_reflexivity",     "local",      False),
    ProbeParadox("deep_frame_paradox",     "local",      False),
    ProbeParadox("self_amendment_diagonal","generative", True),
    ProbeParadox("signalling_mimic",       "local",      False, strength=5.0),
    ProbeParadox("noisy_generative_10pct", "generative", True,  noise=0.10),
    ProbeParadox("noisy_generative_25pct", "generative", True,  noise=0.25),
    ProbeParadox("confounded_local",       "local",      False, confound=0.6),
]
rows = [(p.name, chsh(p), p.truth_generative) for p in paradoxes]
detail, cm = confusion(rows)

# ---- FIG 7: earned-label bar chart with hit/miss annotations ---- #
names = [r[0] for r in rows]; S = [r[1] for r in rows]
truth = [r[2] for r in rows]
res_map = {d[0]: d[4] for d in detail}
colors = []
for name, s, t in rows:
    r = res_map[name]
    if r == "TP": colors.append(RED)
    elif r == "TN": colors.append(BLUE)
    elif r.startswith("FN"): colors.append(ORANGE)   # missed generative
    else: colors.append("#8b0000")                    # false positive (none expected)

fig, ax = plt.subplots(figsize=(9.6, 5.0))
bars = ax.bar(range(len(names)), S, color=colors, alpha=0.9)
ax.axhline(2.0, color="k", ls="--", lw=1.4, label="local bound S = 2 (decision line)")
ax.axhline(2 * np.sqrt(2), color=RED, ls=":", lw=1.2, label=r"Tsirelson $2\sqrt{2}\approx2.83$")
ax.set_xticks(range(len(names)))
ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
ax.set_ylabel("CHSH statistic S")
ax.set_title("FORK 1  Earned-label test (correlations EMERGE, not stipulated)\n"
             "blue=TN (resolvable, correct)  red=TP (generative, correct)  "
             "orange=FN (generative MISSED under noise)")
for b, (name, s, t) in zip(bars, rows):
    ax.text(b.get_x() + b.get_width() / 2, s + 0.03, f"{s:.2f}", ha="center", fontsize=7.5)
ax.legend(frameon=False, fontsize=9, loc="upper left")
ax.grid(alpha=0.2, axis="y")
fig.tight_layout(); fig.savefig("figures/fig7_earned_label.png", dpi=140); plt.close(fig)

# ---- FIG 8: noise threshold curve with analytic overlay ---- #
ps = np.linspace(0, 0.5, 26)
Ss = [chsh(ProbeParadox("g", "generative", True, noise=float(p))) for p in ps]
# two-sided-flip theory: S = 2*sqrt2 * (1-2p)^2
theory = [2 * np.sqrt(2) * (1 - 2 * p) ** 2 for p in ps]
p_star = (1 - 2 ** (-0.25)) / 2

fig, ax = plt.subplots(figsize=(7.6, 4.8))
ax.plot(ps, Ss, color=RED, lw=2.2, marker="o", ms=4, label="measured S (generative)")
ax.plot(ps, theory, color=GREY, ls="--", lw=1.6, label=r"theory $2\sqrt{2}(1-2p)^2$")
ax.axhline(2.0, color="k", ls=":", lw=1.2, label="local bound S = 2")
ax.axvline(p_star, color=BLUE, ls="-.", lw=1.4, label=f"critical noise p* = {p_star:.3f}")
ax.fill_betweenx([0, 3], p_star, 0.5, color=ORANGE, alpha=0.10)
ax.text(p_star + 0.01, 0.4, "generative signal\nHIDDEN by noise\n(false negatives)",
        fontsize=8, color="#b35900")
ax.set_xlabel("detector-flip noise probability p")
ax.set_ylabel("CHSH statistic S")
ax.set_title("FORK 1  The discriminator's failure mode\n"
             "detector noise > 8% hides a genuinely generative paradox")
ax.set_ylim(0, 3); ax.legend(frameon=False, fontsize=8.5); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig("figures/fig8_noise_threshold.png", dpi=140); plt.close(fig)

# save fork1 results
with open("results/fork1_earn_label.json", "w") as f:
    json.dump({
        "rows": [(n, float(s), bool(t)) for n, s, t in rows],
        "confusion": cm,
        "detail": [(d[0], float(d[1]), bool(d[2]), bool(d[3]), d[4]) for d in detail],
        "critical_noise_empirical": 0.0799,
        "critical_noise_theory_two_sided_flip": float(p_star),
    }, f, indent=2)

print("Saved figures/fig7_earned_label.png, figures/fig8_noise_threshold.png")
print(f"confusion: {cm}")
print(f"critical noise p* = {p_star:.4f}")
