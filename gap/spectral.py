#!/usr/bin/env python3
"""spectral.py - a spectral radius test that reports what it cannot tell you.

Usage:
    python3 spectral.py            # runs the self-test on known matrices
    from spectral import report; report(A)

Why this exists: the standard recipe (np.linalg.eigvals, take max abs) is right
but incomplete, and the two things it leaves out are the two that bite.
"""
import numpy as np


def power_iteration(A, iters=10000, tol=1e-14, seed=0):
    """Dominant eigenvalue modulus, independently of eigvals.
    If this disagrees with eigvals, something is wrong - do not average them."""
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(A.shape[0]) + 1j * rng.standard_normal(A.shape[0])
    v /= np.linalg.norm(v)
    prev = 0.0
    for _ in range(iters):
        w = A @ v
        n = np.linalg.norm(w)
        if n == 0:
            return 0.0
        v = w / n
        if abs(n - prev) < tol * max(1.0, n):
            break
        prev = n
    return float(abs(v.conj() @ (A @ v)))


def gerschgorin_bound(A):
    """A CERTIFIED upper bound on rho: no eigenvalue lies outside these discs.
    Cheap, rigorous, and independent of any eigensolver."""
    d = np.abs(np.diag(A))
    r = np.abs(A).sum(axis=1) - np.abs(np.diag(A))
    return float(np.max(d + r))


def departure_from_normality(A):
    """Henrici's measure. 0 means normal (rho tells the whole story).
    Large means rho controls only the n -> infinity rate and nothing before it."""
    fro2 = np.linalg.norm(A, 'fro') ** 2
    ev2 = float(np.sum(np.abs(np.linalg.eigvals(A)) ** 2))
    return float(np.sqrt(max(fro2 - ev2, 0.0)))


def transient_peak(A, horizon=500):
    """max_n ||A^n||_2 and where it occurs. THIS is the finite-horizon answer.
    A matrix with rho < 1 can amplify enormously before it decays."""
    P = np.eye(A.shape[0], dtype=complex)
    peak, at = 0.0, 0
    for k in range(1, horizon + 1):
        P = P @ A
        s = np.linalg.norm(P, 2)
        if s > peak:
            peak, at = float(s), k
        if s > 1e100:
            break
    return peak, at


def eigenvalue_conditioning(A):
    """1/|y*x| per eigenvalue: how much a perturbation of size eps can move it.
    Huge values mean the computed eigenvalues are not trustworthy to full
    precision, and near a coalescence the sensitivity is eps^(1/k), not eps."""
    w, V = np.linalg.eig(A)
    try:
        Vi = np.linalg.inv(V)
    except np.linalg.LinAlgError:
        return [float('inf')] * len(w)
    # cond(V) is the honest global measure. Per-eigenvalue 1/|y*x| silently
    # reports 1 for a DEFECTIVE matrix, where the true sensitivity is infinite.
    return float(np.linalg.cond(V))


def report(A, name="A", horizon=500):
    A = np.asarray(A, dtype=complex)
    ev = np.linalg.eigvals(A)
    rho = float(np.max(np.abs(ev)))
    rho_pi = power_iteration(A)
    gb = gerschgorin_bound(A)
    dep = departure_from_normality(A)
    peak, at = transient_peak(A, horizon)
    condV = eigenvalue_conditioning(A)
    ratio = None
    m = np.sort(np.abs(ev))[::-1]
    if len(m) > 1 and m[0] > 0:
        ratio = float(m[1] / m[0])

    print(f"=== {name} ===")
    print(f"  eigenvalues        : {np.round(np.sort_complex(ev), 6)}")
    print(f"  rho (eigvals)      : {rho:.10f}")
    ok = abs(rho - rho_pi) < 1e-6 * max(1, rho)
    print(f"  rho (power iter)   : {rho_pi:.10f}   "
          f"{'confirms eigvals' if ok else 'DID NOT CONVERGE (see below)'}")
    print(f"  Gerschgorin bound  : {gb:.10f}   (certified: rho <= this, always)")
    print(f"  verdict            : rho {'<' if rho < 1 else '>='} 1  ->  "
          f"{'converges asymptotically' if rho < 1 else 'DIVERGES'}")

    print(f"  departure from normal: {dep:.6g}")
    print(f"  cond(eigenvectors) : {condV:.6g}"
          + ("   <- DEFECTIVE: no eigenbasis, sensitivity is eps^(1/k)" if condV > 1e12 else ""))
    if ratio is not None:
        print(f"  |lambda2/lambda1|  : {ratio:.6f}"
              + ("   <- equal moduli: power iteration cannot converge here" if ratio > 0.9999 else ""))
    print(f"  peak ||A^n||       : {peak:.6g} at n = {at}")

    warn = []
    if abs(rho - 1.0) < 0.02:
        warn.append("rho is within 2% of 1 - floating point alone cannot decide "
                    "this; use interval arithmetic or a certified bound")
    if dep > 1e-8 and peak > 10:
        warn.append(f"NON-NORMAL: amplifies {peak:.3g}x at n={at} BEFORE decaying. "
                    "rho only governs the n->infinity rate. For a finite horizon "
                    "or anything with feedback, this matrix is not 'stable'")
    if condV > 1e6:
        warn.append(f"eigenvector matrix is ill-conditioned (cond {condV:.3g}) - "
                    "the digits above are not all real; at a coalescence a "
                    "perturbation eps moves rho by eps^(1/k), NOT eps")
    if not ok:
        if ratio is not None and ratio > 0.9999:
            warn.append("power iteration did not converge because the top two "
                        "eigenvalues have EQUAL MODULUS. That is a diagnosis, not "
                        "a failure: eigvals is right, and no single dominant "
                        "direction exists. Rotations and defective matrices both "
                        "land here")
        else:
            warn.append("the two methods disagree and the moduli are not equal - "
                        "investigate before trusting either")
    if warn:
        print("  WARNINGS:")
        for w in warn:
            print(f"    ! {w}")
    else:
        print("  (no warnings: normal enough that rho tells the whole story)")
    print()
    return {"rho": rho, "rho_power": rho_pi, "gerschgorin": gb,
            "departure": dep, "peak": peak, "peak_at": at, "condV": condV,
            "ratio": ratio}


def selftest():
    """Run on matrices whose answers are known independently, INCLUDING ones
    designed to break the naive test. A tool that has only been run on cases
    its author expected to pass has no evidence behind it."""
    print("#" * 70)
    print("# SELF-TEST - every case here has a known answer")
    print("#" * 70 + "\n")

    report([[0.5, 0.2, 0.1], [0.1, 0.6, 0.2], [0.3, 0.1, 0.4]],
           "the matrix from the question (rho = 0.83961, NOT 0.8122)")

    report([[0.9, 20.0], [0.0, 0.9]],
           "non-normal: rho=0.9 'stable', amplifies 77x first")

    report([[0.0, 1.0], [1.0, 1.0]],
           "the gap equation at G=1: rho = phi = 1.6180339887")

    report([[1.0, -1.0], [1.0, 0.0]],
           "the gap equation at G=-1: rho = 1 exactly, period 6")

    report([[0.5, 1.0, 0.0], [0.0, 0.5, 1.0], [1e-12, 0.0, 0.5]],
           "near-coalescence: 1e-12 perturbation moves rho by 1e-4")

    report([[0.99, 0.0], [0.0, 0.5]],
           "rho just below 1 - the decision boundary")

    print("WHAT THIS TOOL CANNOT TELL YOU:")
    print("  1. Whether rho is the right question. For a SWITCHING system -")
    print("     different matrices at different steps - the governing quantity")
    print("     is the JOINT spectral radius over all products, which is")
    print("     NP-hard to approximate and is not computed here.")
    print("  2. Whether your matrix is the matrix you meant. A correct rho of")
    print("     a mis-transcribed matrix is a correct answer to a wrong question.")
    print("  3. Certified digits. Everything above is float64. The Gerschgorin")
    print("     bound is the only rigorous number printed.")


if __name__ == "__main__":
    selftest()
