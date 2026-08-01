#!/usr/bin/env python3
"""
complex_climb_sim.py
====================
The complex / imaginary extension, simulated.

Three climbers face the SAME back-loaded lattice (the "un-governable" case from
Thread 1: a value-valley of early rungs guarding a deep payoff):

  GREEDY (real, myopic)   -- builds a rung only while the running net stays >= 0.
                             On a back-loaded lattice it stops at 0 (Thread 1's verdict).

  GLOBAL (real, commit)   -- computes the best cumulative height and, IF a real
                             break-even exists (discriminant >= 0), commits to the
                             whole climb, eating the valley to reach the peak.
                             When no real break-even exists it correctly declines.

  QUANTUM (complex, tunnel)-- attempts the climb even when there is NO real break-even,
                             by "tunnelling": it crosses the forbidden valley with a
                             probability equal to the WKB amplitude exp(-2|Im S|), and
                             while under the barrier it pays a REACTIVE (imaginary) cost
                             -- a trust/volatility drawdown that dissipates nothing if it
                             makes it across (like reactive power) but can cause RUIN if
                             the drawdown exceeds a survival buffer mid-crossing.

The point: "climb anyway" is not one thing. If the payoff is real-reachable, GLOBAL
can beat GREEDY -- but now pays a real ruin risk on the drawdown, not for free. If it is only complex-reachable, QUANTUM can still win -- but
now pays an imaginary cost and takes on real ruin risk. We measure when each wins.

Perspectives held at once:
  classical    : real cost accounting; greedy vs global; complex ROOTS show up as
                 overshoot/oscillation in the committed climb's transient.
  quantum      : tunnelling amplitude; imaginary action; ruin under the barrier.
  complex/AC   : reactive cost |X| paid to move real value past the barrier; only the
                 resistive part R dissipates; power factor = crossings that pay off.
"""
from __future__ import annotations
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("figures", exist_ok=True)
os.makedirs("results", exist_ok=True)

L = 8
P_EXCITE, INST_SCALE = 0.6, 0.08


def back_loaded_net(budget, cost0=0.05):
    heights = np.arange(1, L + 1)
    cost = cost0 * (1.0 + 0.15 * (heights - 1))
    w = np.zeros(L); w[-1] = 0.60; w[-2] = 0.32; w[:-2] = 0.08 / (L - 2)
    value = P_EXCITE * INST_SCALE * budget * w
    return value - cost


def greedy_h(net):
    h, run = 0, 0.0
    for k, v in enumerate(net, 1):
        run += v
        if run >= 0: h = k
        else: break
    return h


def global_h(net):
    cum = np.cumsum(net)
    return (int(np.argmax(cum)) + 1, float(cum.max())) if cum.max() > 0 else (0, 0.0)


def barrier_imag_action(net):
    """|Im S| for the value-valley: integral of sqrt(max(0, -net)) over the valley.
    Larger, deeper valley -> larger imaginary action -> smaller tunnelling amplitude."""
    forbidden = np.clip(-np.cumsum(net), 0, None)      # depth of the value deficit
    return float(np.sum(np.sqrt(forbidden)))


def tunnel_amplitude(net):
    return float(np.exp(-2 * barrier_imag_action(net) / L))


def _drawdown_path(net, rng, vol):
    """Simulate reserves being depleted while crossing the value-valley.

    A climber that COMMITS to the full height carries a running reserve that
    starts at 0 and moves by the (real) per-rung net each step PLUS a mean-zero
    volatility shock of scale `vol`. The transient low-water mark is what
    threatens ruin -- even a climb whose *final* value is positive can dip so
    deep mid-crossing that reserves are exhausted first. Returns (low_water,
    final) where low_water <= 0 is the worst cumulative deficit along the path.
    """
    reserve = 0.0
    low = 0.0
    for v in net:
        reserve += v + rng.normal(0.0, vol)
        low = min(low, reserve)
    return low, reserve


def simulate(budget, seeds=4000, buffer_frac=0.6, vol=0.03):
    """Run the three climbers on a back-loaded lattice of given payoff budget.

    RUIN is now a real, stressed outcome for BOTH committing climbers:
      * survival_buffer is set to `buffer_frac` of the deterministic valley
        depth, so it always bites (buffer_frac < 1 => the buffer is shallower
        than the valley and ruin is possible);
      * the drawdown path is stochastic (volatility `vol`), so ruin fires even
        when the mean path would have survived;
      * a climber that is ruined loses its committed reserves (-buffer) and
        collects NO payoff -- there is no free tunnel bonus any more.
    """
    net = back_loaded_net(budget)
    cum = np.cumsum(net)
    hg = greedy_h(net)
    hgl, vgl = global_h(net)
    real_reachable = vgl > 0
    amp = tunnel_amplitude(net)

    valley_depth = float(max(-cum.min(), 0.0))          # deterministic worst deficit
    survival_buffer = buffer_frac * valley_depth if valley_depth > 0 else 1e9

    rng = np.random.default_rng(int(budget * 1000))
    deep = float(np.sum(net))                            # payoff of full commit

    # ----- GLOBAL (real, commit): only attempts when a real bank exists ------
    g_vals = []
    g_ruin = 0
    for _ in range(seeds):
        if not real_reachable:
            g_vals.append(0.0); continue               # correctly declines
        low, final = _drawdown_path(net, rng, vol)
        if low < -survival_buffer:
            g_ruin += 1; g_vals.append(-survival_buffer)   # reserves exhausted mid-climb
        else:
            g_vals.append(max(final, 0.0))
    g_vals = np.array(g_vals)

    # ----- QUANTUM (complex, tunnel): attempts even with no real bank --------
    q_pay, q_ruin, q_decline = 0, 0, 0
    q_vals = []
    for _ in range(seeds):
        if real_reachable:
            # a real bank exists: quantum crosses like global, same ruin risk
            low, final = _drawdown_path(net, rng, vol)
            if low < -survival_buffer:
                q_ruin += 1; q_vals.append(-survival_buffer)
            else:
                q_pay += 1; q_vals.append(max(final, 0.0))
            continue
        # no real break-even: must tunnel. First: does it tunnel at all?
        if rng.random() >= amp:
            q_decline += 1; q_vals.append(0.0)             # reflected
            continue
        # tunnelled: still must survive the reactive drawdown to bank the payoff
        low, final = _drawdown_path(net, rng, vol)
        if low < -survival_buffer:
            q_ruin += 1; q_vals.append(-survival_buffer)   # crossed but ruined
        else:
            q_pay += 1; q_vals.append(max(deep, 0.0))      # no bonus: bare payoff
    q_vals = np.array(q_vals)

    return {
        "budget": budget, "net": net.tolist(), "cum": cum.tolist(),
        "greedy_h": hg, "global_h": hgl, "global_V": vgl,
        "real_reachable": bool(real_reachable), "tunnel_amp": amp,
        "valley_depth": valley_depth, "survival_buffer": survival_buffer,
        "buffer_frac": buffer_frac, "vol": vol,
        "q_mean": float(q_vals.mean()), "global_mean": float(g_vals.mean()),
        "q_pay_frac": q_pay / seeds, "q_ruin_frac": q_ruin / seeds,
        "q_decline_frac": q_decline / seeds,
        "global_ruin_frac": g_ruin / seeds,
    }


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    budgets = [8, 10, 12, 13, 14, 15, 16, 20, 26, 34]
    # For the budget sweep use a buffer where ruin is REAL but survivable
    # (~1.1x valley depth => ~20-40% ruin), so budget-dependence stays visible.
    rows = [simulate(b, buffer_frac=1.1) for b in budgets]
    print("  RUIN NOW STRESSED (buffer = 1.1 x valley depth, volatility 0.03):")
    for r in rows:
        tag = "REAL path" if r["real_reachable"] else "complex-only (tunnel)"
        print(f"  B={r['budget']:>3}: amp={r['tunnel_amp']:.3f}  "
              f"Gmean={r['global_mean']:+.3f} Gruin={r['global_ruin_frac']:.2f}  "
              f"Qmean={r['q_mean']:+.3f} Qpay={r['q_pay_frac']:.2f} "
              f"Qruin={r['q_ruin_frac']:.2f}  [{tag}]")

    # ---- buffer-fraction sweep: the §7.4 seam, closed -----------------------
    # At a fixed deep budget, lower the survival buffer below the valley depth
    # and watch the quantum advantage collapse toward amp*payoff - ruin loss.
    B_FIX = 20
    fracs = [1.20, 1.00, 0.80, 0.60, 0.45, 0.35, 0.25, 0.15]
    buf_rows = [simulate(B_FIX, buffer_frac=bf) for bf in fracs]
    print(f"\n  BUFFER SWEEP at B={B_FIX} (real path exists; ruin bites as buffer shrinks):")
    for bf, r in zip(fracs, buf_rows):
        print(f"    buffer={bf:.2f}x valley: Gmean={r['global_mean']:+.3f} "
              f"Gruin={r['global_ruin_frac']:.2f}   Qmean={r['q_mean']:+.3f} "
              f"Qruin={r['q_ruin_frac']:.2f}")

    out = {"budget_sweep": rows, "buffer_sweep": {
        "B_fix": B_FIX, "fracs": fracs, "rows": buf_rows}}
    with open("results/complex_climb_sim.json", "w") as f:
        json.dump(out, f, indent=2)

    BLUE, GREEN, RED, PURPLE, GREY = "#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#7f7f7f"

    # FIG 14: cumulative value with the valley; greedy-stop vs global-opt (B=20)
    net = np.array(simulate(20)["net"]); cum = np.cumsum(net)
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    hh = np.arange(1, L + 1)
    ax.axhline(0, color="k", lw=0.8)
    ax.fill_between(hh, cum, 0, where=(cum < 0), color=RED, alpha=0.12,
                    label="value-valley (classically forbidden)")
    ax.plot(hh, cum, color=BLUE, lw=2.4, marker="o", label="cumulative value V(h)")
    ax.axvline(greedy_h(net) + 0.02, color=GREY, ls="--", lw=1.6,
               label=f"greedy stops at h={greedy_h(net)}")
    gh, gv = global_h(net)
    ax.plot([gh], [gv], marker="*", ms=18, color=GREEN,
            label=f"global optimum h={gh} (climb anyway)")
    ax.set_xlabel("Godel height h"); ax.set_ylabel("cumulative net value V(h)")
    ax.set_title("COMPLEX §7  Climb anyway: a value-valley guards a deep payoff\n"
                 "greedy refuses the valley; the global climber crosses it")
    ax.legend(frameon=False, fontsize=8.5, loc="lower left"); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig("figures/fig14_valley_greedy_vs_global.png", dpi=140); plt.close(fig)

    # FIG 15: the -1/4 root locus (real roots collide and go complex)
    cs = np.linspace(-0.5, 1.0, 400)
    re, im_p, im_m = [], [], []
    for c in cs:
        d = 1 - 4 * c
        s = np.sqrt(d) if d >= 0 else 1j * np.sqrt(-d)
        r1 = (-1 + s) / 2
        re.append(r1.real if d >= 0 else -0.5)
        im_p.append(0.0 if d >= 0 else float((( -1 + s)/2).imag))
        im_m.append(0.0 if d >= 0 else float((( -1 - s)/2).imag))
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    # real branch(es)
    real_mask = cs <= 0.25
    ax.plot(cs[real_mask], [((-1+np.sqrt(1-4*c))/2) for c in cs[real_mask]],
            color=BLUE, lw=2.2, label="real root h+ (break-even, upper)")
    ax.plot(cs[real_mask], [((-1-np.sqrt(1-4*c))/2) for c in cs[real_mask]],
            color=BLUE, lw=2.2, ls="--", label="real root h- (break-even, lower)")
    comp = cs > 0.25
    ax.plot(cs[comp], np.array(im_p)[comp], color=RED, lw=2.2,
            label="Im part (tunnel cost), +sheet")
    ax.plot(cs[comp], np.array(im_m)[comp], color=RED, lw=2.2, ls="--",
            label="Im part, -sheet (conjugate)")
    ax.axvline(0.25, color=PURPLE, lw=1.6, ls="-.", label="fold at c = 1/4")
    ax.plot([0.25], [-0.5], marker="o", ms=9, color=PURPLE)
    ax.annotate("roots collide at -1/2\nthen leave the real axis",
                xy=(0.25, -0.5), xytext=(0.35, -1.15), fontsize=8,
                arrowprops=dict(arrowstyle="->", color=PURPLE))
    ax.set_xlabel("barrier depth  c   (break-even eqn  h² + h + c = 0)")
    ax.set_ylabel("break-even height  h")
    ax.set_title("COMPLEX §7  The −1/4 fold: real break-even roots collide and go complex\n"
                 "past c=1/4 the break-even height is imaginary = the tunnelling cost")
    ax.legend(frameon=False, fontsize=8, loc="upper right"); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig("figures/fig15_root_locus.png", dpi=140); plt.close(fig)

    # FIG 16: tunnelling amplitude vs payoff budget, with the real/complex regime split
    b_arr = np.array([r["budget"] for r in rows])
    amp_arr = np.array([r["tunnel_amp"] for r in rows])
    real_arr = np.array([r["real_reachable"] for r in rows])
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    ax.plot(b_arr, amp_arr, color=RED, lw=2.2, marker="o",
            label="tunnelling amplitude exp(-2|Im S|/L)")
    # shade real-reachable region
    if real_arr.any():
        b_split = b_arr[real_arr].min()
        ax.axvspan(b_split, b_arr.max(), color=GREEN, alpha=0.08)
        ax.axvline(b_split, color=GREEN, lw=1.6, ls="--",
                   label=f"real break-even appears (B≈{b_split}); real path opens (still ruin-risked)")
    ax.set_xlabel("deep-payoff budget B")
    ax.set_ylabel("tunnelling amplitude / payoff-probability")
    ax.set_title("COMPLEX §7  When the payoff is only complex-reachable,\n"
                 "the quantum climber crosses with amplitude exp(-2|Im S|)")
    ax.legend(frameon=False, fontsize=8.5); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig("figures/fig16_tunnel_amplitude.png", dpi=140); plt.close(fig)

    # FIG 17: sim outcomes — greedy vs global vs quantum, RISK-DISCOUNTED
    greedy_val, global_val, quantum_val = [], [], []
    for r in rows:
        greedy_val.append(0.0)                     # greedy builds nothing here
        global_val.append(max(r["global_mean"], 0.0))
        quantum_val.append(r["q_mean"])
    b_split = b_arr[real_arr].min() if real_arr.any() else None
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.plot(b_arr, greedy_val, color=GREY, lw=2.2, marker="s", label="GREEDY (real, myopic)")
    ax.plot(b_arr, np.array(quantum_val), color=PURPLE, lw=3.0, marker="o",
            label="QUANTUM (complex, tunnel) — risk-discounted", zorder=2)
    ax.plot(b_arr, np.array(global_val) + 0.012, color=GREEN, lw=2.0, marker="^",
            ls="--", label="GLOBAL (real, commit) — with ruin", zorder=3)
    if b_split is not None:
        ax.axvline(b_split, color=GREEN, ls=":", lw=1.4)
        ax.axvspan(b_arr.min(), b_split, color=PURPLE, alpha=0.06)
        ax.text((b_arr.min() + b_split) / 2.0, 0.06,
                "complex-only gap:\nonly QUANTUM lifts it\n(now ruin-discounted)",
                ha="center", va="bottom", fontsize=8.0, color=PURPLE)
    ax.set_xlabel("deep-payoff budget B")
    ax.set_ylabel("expected realised value (after ruin)")
    ax.set_title("COMPLEX §7.4  Ruin stressed: quantum advantage in the complex-only gap\n"
                 "now trades payoff against real ruin (no free tunnel bonus)")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left"); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig("figures/fig17_three_climbers.png", dpi=140); plt.close(fig)

    # FIG 18: the seam closed — buffer-fraction sweep at fixed B
    fr = np.array(fracs)
    gm = np.array([r["global_mean"] for r in buf_rows])
    gr = np.array([r["global_ruin_frac"] for r in buf_rows])
    qm = np.array([r["q_mean"] for r in buf_rows])
    qr = np.array([r["q_ruin_frac"] for r in buf_rows])
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.2, 4.6))
    axL.plot(fr, gm, color=GREEN, lw=2.2, marker="^", label="GLOBAL mean value")
    axL.plot(fr, qm, color=PURPLE, lw=2.2, marker="o", label="QUANTUM mean value")
    axL.axvline(1.0, color=GREY, ls=":", lw=1.2)
    axL.invert_xaxis()
    axL.set_xlabel("survival buffer  (x valley depth)  — shrinking to the right")
    axL.set_ylabel(f"expected realised value  (B={B_FIX})")
    axL.set_title("Value collapses as the buffer drops below the valley")
    axL.legend(frameon=False, fontsize=9); axL.grid(alpha=0.25)
    axR.plot(fr, 100*gr, color=GREEN, lw=2.2, marker="^", label="GLOBAL ruin %")
    axR.plot(fr, 100*qr, color=PURPLE, lw=2.2, marker="o", label="QUANTUM ruin %")
    axR.axvline(1.0, color=GREY, ls=":", lw=1.2)
    axR.invert_xaxis()
    axR.set_xlabel("survival buffer  (x valley depth)  — shrinking to the right")
    axR.set_ylabel("ruin probability (%)")
    axR.set_title("Ruin now fires (the §7.4 seam, closed)")
    axR.legend(frameon=False, fontsize=9); axR.grid(alpha=0.25)
    fig.suptitle("COMPLEX §7.4  Lowering the survival buffer below valley depth: "
                 "ruin becomes real and the free-option illusion disappears", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig("figures/fig18_ruin_buffer_sweep.png", dpi=140); plt.close(fig)

    print("\nSaved figures/fig14..fig18 and results/complex_climb_sim.json")
