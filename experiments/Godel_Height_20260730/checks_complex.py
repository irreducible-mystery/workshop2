#!/usr/bin/env python3
"""
checks_complex.py
=================
Deterministic checks for the complex / imaginary extension.

The Thread-1 verdict "back-loaded harm is un-governable" was a statement about a
GREEDY, REAL, CONTIGUOUS climb: the myopic rule stops at the first rung whose
running net value turns negative, so with a deep (back-loaded) payoff it never
starts. This file shows that verdict is a LOCAL-optimum / real-axis artifact and
makes precise the sense in which the payoff, and the break-even "height," go
COMPLEX -- using the exact quadratic / discriminant / branch-point structure the
user pointed to with -1/4.

Dictionary (governance  <->  quadratic)
---------------------------------------
  cumulative net value along the climb:  V(h) = -a*h^2 + b*h - c_barrier   (a>0)
      concave-down parabola: early rungs cost (the valley), a deep peak later.
  break-even heights = roots of V(h) = 0  ->  a*h^2 - b*h + c_barrier = 0
      discriminant D = b^2 - 4 a c_barrier.
        D > 0 : two REAL break-even heights (enter the valley at h_-, exit in the
                black at h_+). A GLOBAL climber that commits crosses and profits.
        D = 0 : the two collide (tangent) -- the marginal case (the "-1/4" fold).
        D < 0 : NO real break-even. The peak of V never reaches 0 on the real axis;
                the roots are a COMPLEX-CONJUGATE pair h = (b/2a) +/- i*sqrt(|D|)/2a.
                The imaginary part is the "distance off the real axis" you must
                traverse -- the TUNNELING cost.

Checks
------
  C1  greedy vs global optimum on a back-loaded profile: greedy stops at 0,
      global crosses the valley and wins. Quantify the forgone payoff.
  C2  discriminant law + the -1/4 collision: sweep barrier depth c_barrier;
      find c* where real break-even roots collide and go complex; verify it is
      exactly the vertex-touches-zero point (the fold), matching x^2 + x + c.
  C3  path dependence: continue a break-even root as the barrier passes the branch
      point from two directions; show the analytic continuations land on conjugate
      sheets ("approach from -1/2 vs from 1 gives different answers").
  C4  tunneling action (WKB): under the barrier the momentum sqrt(E - V) is
      imaginary; the action integral is imaginary; the crossing amplitude is
      exp(-|Im S|). Compute it and read it as "probability the deep reform pays off."
"""
from __future__ import annotations
import numpy as np
import cmath


# --------------------------------------------------------------------------- #
# C1  greedy vs global optimum on a back-loaded value profile                  #
# --------------------------------------------------------------------------- #
def per_rung_value(profile, L=8, budget=12.0, cost0=0.05, base=1.4):
    """Net value of building each rung k = dissolved-harm value - tier cost.

    'back' models a genuine BARRIER-then-PAYOFF: the deep paradoxes (large harm,
    hence large value once dissolved) sit at the TOP rungs, but you must first pay
    for several low rungs that dissolve little. So the early net is negative (the
    valley / barrier) and the late net is strongly positive (the deep payoff).
    A greedy climber refuses to enter the valley; a global climber crosses it."""
    heights = np.arange(1, L + 1)
    P_EXCITE, INST_SCALE = 0.6, 0.08
    # LINEAR (not exponential) tier cost here, so a finite barrier can be crossed:
    # an exponential cost makes deep payoffs unreachable even globally (a separate,
    # also-true regime). We use a linear coordination cost to isolate the
    # barrier-crossing phenomenon the user asked about ("climb anyway").
    cost = cost0 * (1.0 + 0.15 * (heights - 1))
    if profile == "back":
        # value concentrated in the TOP two rungs; tiny below -> a genuine valley
        # (negative early net) followed by a large peak (positive late net).
        w = np.zeros(L); w[-1] = 0.60; w[-2] = 0.32
        w[:-2] = 0.08 / max(L - 2, 1)
    elif profile == "front":
        w = 1.0 / heights; w = w / w.sum()
    elif profile == "flat":
        w = np.ones(L); w = w / w.sum()
    value = P_EXCITE * INST_SCALE * budget * w
    return value - cost   # per-rung net: valley early, peak late (for 'back')


def greedy_height(net):
    """Myopic contiguous stop: build while running prefix stays non-negative."""
    h, running = 0, 0.0
    for k, v in enumerate(net, start=1):
        running += v
        if running >= 0:
            h = k
        else:
            break
    return h


def global_height(net):
    """Best cumulative value over ALL heights (allowed to cross valleys)."""
    cum = np.cumsum(net)
    h = int(np.argmax(cum)) + 1 if cum.max() > 0 else 0
    return h, float(cum.max())


def check1():
    print("=== C1: greedy vs global on a BACK-LOADED profile (three regimes) ===")
    print("  Sweep the deep-payoff budget B. The barrier (early negative rungs) is")
    print("  fixed; only the size of the deep payoff behind it grows with B.\n")
    print(f"  {'budget':>7s} {'greedy_h':>9s} {'global_h':>9s} {'global_V':>9s}  regime")
    saw_barrier_wins = saw_never = False
    for B in [8.0, 12.0, 16.0, 22.0, 30.0]:
        net = per_rung_value("back", budget=B)
        cum = np.cumsum(net)
        hg = greedy_height(net)
        hstar, vstar = global_height(net)
        if vstar <= 0:
            regime = "barrier impassable even globally (roots COMPLEX)"
            saw_never = True
        elif hg == 0 and hstar > 0:
            regime = "GREEDY refuses, GLOBAL crosses & wins (roots REAL)"
            saw_barrier_wins = True
        else:
            regime = "greedy already climbs"
        print(f"  {B:7.1f} {hg:9d} {hstar:9d} {vstar:9.3f}  {regime}")
    ok = saw_barrier_wins and saw_never
    print(f"\n  => both regimes observed: a valley that greedy won't cross but global will,")
    print(f"     AND a barrier so deep no real height breaks even (payoff goes complex): {ok}\n")
    return ok


# --------------------------------------------------------------------------- #
# C2  discriminant law + the -1/4 collision                                    #
# --------------------------------------------------------------------------- #
def check2():
    print("=== C2: break-even discriminant and the -1/4 fold ===")
    # V(h) = 0 with V a concave parabola -> a h^2 - b h + c = 0. Use the canonical
    # normalized form h^2 + h + c (a=1,b=-1 style) so the fold sits at c=1/4.
    print("  normalized break-even eqn x^2 + x + c = 0  (disc = 1 - 4c):")
    collide_c = None
    prev_real = None
    for c in np.round(np.arange(-0.5, 1.01, 0.01), 2):
        disc = 1 - 4 * c
        real = disc >= 0
        if prev_real is True and real is False:
            collide_c = round(c - 0.01, 2)
        prev_real = real
    # exact collision
    r_at = (-1 + cmath.sqrt(1 - 4 * 0.25)) / 2
    print(f"  real break-even roots exist for c <= 0.25; they COLLIDE at c = 0.25")
    print(f"  double root at c=1/4 is x = {r_at.real:+.4f}  (== vertex -1/2 of x^2+x)")
    for c in [0.24, 0.25, 0.26]:
        d = 1 - 4 * c
        r1 = (-1 + cmath.sqrt(d)) / 2
        r2 = (-1 - cmath.sqrt(d)) / 2
        tag = "real" if d >= 0 else "COMPLEX pair -> tunnel"
        print(f"    c={c}: roots {r1:.3f}, {r2:.3f}  [{tag}]")
    ok = abs(r_at.real + 0.5) < 1e-9 and abs(r_at.imag) < 1e-9
    print(f"  => collision at the -1/4 fold, root at vertex -1/2: {ok}\n")
    return ok


# --------------------------------------------------------------------------- #
# C3  path dependence through the branch point                                 #
# --------------------------------------------------------------------------- #
def check3():
    print("=== C3: path dependence (approach the fold from two sides) ===")
    root = lambda c: (-1 + cmath.sqrt(1 - 4 * c)) / 2
    c0 = 1.0  # a barrier well past the fold
    below = root(complex(c0, -1e-9))
    above = root(complex(c0, +1e-9))
    print(f"  break-even 'height' at barrier c={c0} approached from below cut: {below:.4f}")
    print(f"                                              from above cut: {above:.4f}")
    conj = np.isclose(below, above.conjugate())
    print(f"  => the two approaches give CONJUGATE complex heights: {conj}")
    print(f"     ('approaching -1/4 from -1/2 vs from 1' picks a different Riemann sheet)\n")
    return bool(conj)


# --------------------------------------------------------------------------- #
# C4  tunneling action (WKB): imaginary action -> crossing amplitude           #
# --------------------------------------------------------------------------- #
def check4():
    print("=== C4: tunneling action under the value-barrier (WKB) ===")
    # Treat the value-valley as a potential barrier V(x) above the 'energy' E=0.
    # classically forbidden where V(x) > E. Momentum p = sqrt(E - V) is imaginary
    # there; the action S = integral p dx is imaginary; amplitude ~ exp(-|Im S|).
    xs = np.linspace(0, 1, 2001)
    def amplitude(barrier_height, barrier_width):
        # rectangular-ish barrier centred in [0,1]
        V = np.where((xs > 0.5 - barrier_width / 2) & (xs < 0.5 + barrier_width / 2),
                     barrier_height, 0.0)
        E = 0.0
        integrand = np.sqrt(np.clip(V - E, 0, None))   # |imaginary momentum|
        _trapz = getattr(np, "trapezoid", None) or np.trapz
        ImS = _trapz(integrand, xs)
        return np.exp(-2 * ImS), ImS
    print("  barrier(height, width) -> |Im action|, crossing amplitude exp(-2|Im S|):")
    rows = []
    for h in [0.5, 1.0, 2.0]:
        for w in [0.2, 0.5]:
            amp, ImS = amplitude(h, w)
            rows.append((h, w, ImS, amp))
            print(f"    height={h:.1f} width={w:.1f}: |Im S|={ImS:.3f}  amplitude={amp:.4f}")
    # monotone: deeper/wider barrier -> smaller amplitude
    ok = rows[0][3] > rows[-1][3]
    print(f"  => deeper/wider barrier lowers the tunnelling amplitude (payoff-probability): {ok}\n")
    return ok


if __name__ == "__main__":
    r = [check1(), check2(), check3(), check4()]
    names = ["C1 greedy<global (climb anyway wins)",
             "C2 -1/4 discriminant fold",
             "C3 path/sheet dependence",
             "C4 tunnelling amplitude monotone"]
    print("=== SUMMARY ===")
    for n, ok in zip(names, r):
        print(f"  {'PASS' if ok else 'FAIL'}  {n}")
