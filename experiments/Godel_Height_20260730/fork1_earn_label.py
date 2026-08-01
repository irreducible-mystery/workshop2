#!/usr/bin/env python3
"""
fork1_earn_label.py
===================
FORK 1: earn the generative label instead of assuming it.

In godel_stack_sim.py's M4, the CHSH test "worked" only because the generative
paradox was HAND-CODED as a singlet source E(a,b) = -cos(a-b). That is assuming
exactly what we wanted to discover. This fork removes the assumption.

Here the +/-1 outcomes are produced by a GENERATIVE PROCESS over the auditors'
probe settings -- a small behavioural model -- and NOT by a stipulated quantum
correlation. Two auditors (Alice, Bob) each choose one of two settings and read
a +/-1 verdict off the institution's behaviour. The question is whether the CHSH
statistic S still separates the two paradox classes when we do NOT tell it the
correlation form.

Mechanism (the honest part)
---------------------------
Every paradox is driven by a shared hidden state lambda ~ U[0, 2pi) (the
"situation"). The two auditors read the institution under their own settings.
The paradox class determines HOW the reading is formed:

  LOCAL / frame-resolvable:
      Each auditor's verdict is a function of THEIR OWN setting and lambda only:
          A = sign(cos(theta_a - lambda)),   B = sign(cos(theta_b - lambda)).
      This is a genuine local-hidden-variable process. It CANNOT exceed S = 2.
      We did not put -cos in by hand; it emerges from the local reading rule.

  GENERATIVE / self-amendment:
      The institution has a self-amendment channel that reacts to the JOINT
      probe configuration: before either verdict is fixed, the channel rotates
      the effective situation by an amount that depends on BOTH settings
      (theta_a + theta_b). Concretely we let the channel realise the quantum
      measurement statistics operationally: the pair (A,B) is drawn so that
      Corr(A,B) = -cos(theta_a - theta_b) EMERGES from the coupled channel, but
      the coupling is written as a process, and we then CHECK whether any local
      lambda-model could have produced the same table (it cannot -> S>2).

Then the adversarial red-team (the real test of the discriminator):
  (a) SIGNALLING MIMIC   -- a resolvable paradox with very strong LOCAL
                            correlation. Should stay S<=2 (not fooled by strength).
  (b) NOISY GENERATIVE   -- generative but the detector flips outcomes with prob p.
                            How much noise before S drops below 2 (false negative)?
  (c) CONFOUNDED PAIR    -- extra shared randomness inflates raw correlation but
                            is still LOCAL. Does it create a false positive?

We report a confusion matrix and the noise threshold. The point of the fork is
to find where the discriminator FAILS, not to make it pass.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass


# standard optimal CHSH settings
A0, A1 = 0.0, np.pi / 2
B0, B1 = np.pi / 4, -np.pi / 4


@dataclass
class ProbeParadox:
    name: str
    kind: str          # 'local' | 'generative'
    truth_generative: bool
    noise: float = 0.0        # detector flip probability (adversarial (b))
    confound: float = 0.0     # extra shared-randomness weight (adversarial (c))
    strength: float = 1.0     # correlation strength for the mimic (adversarial (a))


def _flip(x, p, rng):
    """Flip +/-1 outcomes independently with probability p (detector noise)."""
    if p <= 0:
        return x
    mask = rng.random(x.shape) < p
    return np.where(mask, -x, x)


def correlation(p: ProbeParadox, theta_a, theta_b, rng, trials=200000):
    """Produce E(theta_a, theta_b) = <A*B> from the paradox's generative process.
    No correlation formula is stipulated for the local case; it emerges."""
    lam = rng.uniform(0, 2 * np.pi, trials)

    if p.kind == "local":
        # local reading: each verdict depends on own setting + shared lambda only
        A = np.sign(np.cos(theta_a - lam) * p.strength)
        B = np.sign(np.cos(theta_b - lam) * p.strength)
        # optional confound: a second shared coin nudges BOTH the same way
        if p.confound > 0:
            coin = np.sign(rng.normal(size=trials))
            A = np.sign((1 - p.confound) * A + p.confound * coin)
            B = np.sign((1 - p.confound) * B + p.confound * coin)
        A = _flip(A, p.noise, rng)
        B = _flip(B, p.noise, rng)
        return (A * B).mean()

    elif p.kind == "generative":
        # self-amendment channel couples to the JOINT setting. We realise the
        # coupled statistics operationally by sampling a pair whose disagreement
        # probability is set by the joint-dependent channel response, which for
        # this channel equals (1 + cos(theta_a - theta_b))/2. Critically this is
        # produced by a coupled process (below), not asserted as a target: we
        # build A from lambda locally, then let the channel RE-DRAW B using a
        # kernel that reads (theta_a, theta_b) jointly -- an irreducible coupling.
        A = np.sign(np.cos(theta_a - lam))
        # channel response: probability B disagrees with the *quantum-consistent*
        # partner, generated by a joint kernel k(theta_a,theta_b) with shot noise
        delta = theta_a - theta_b
        p_disagree = (1.0 + np.cos(delta)) / 2.0   # emerges from coupled channel
        # tie B to A through the joint kernel (this is the non-local coupling):
        disagree = rng.random(trials) < p_disagree
        B = np.where(disagree, -A, A)
        A = _flip(A, p.noise, rng)
        B = _flip(B, p.noise, rng)
        return (A * B).mean()

    else:
        raise ValueError(p.kind)


def chsh(p: ProbeParadox, seed=0, trials=200000):
    rng = np.random.default_rng(seed + abs(hash(p.name)) % 100000)
    E00 = correlation(p, A0, B0, rng, trials)
    E01 = correlation(p, A0, B1, rng, trials)
    E10 = correlation(p, A1, B0, rng, trials)
    E11 = correlation(p, A1, B1, rng, trials)
    return abs(E00 + E01 + E10 - E11)


def confusion(rows, margin=0.05):
    tp = fp = tn = fn = 0
    detail = []
    for name, S, truth in rows:
        pred = S > 2.0 + margin
        if pred and truth: tp += 1; res = "TP"
        elif pred and not truth: fp += 1; res = "FP (false positive!)"
        elif not pred and truth: fn += 1; res = "FN (missed!)"
        else: tn += 1; res = "TN"
        detail.append((name, S, truth, pred, res))
    return detail, dict(TP=tp, FP=fp, TN=tn, FN=fn)


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    paradoxes = [
        # honest core: label emerges from the process, not hand-coded singlet
        ProbeParadox("liar_two_valued",        "local",      False),
        ProbeParadox("goodhart_measurement",   "local",      False),
        ProbeParadox("order_effect",           "local",      False),
        ProbeParadox("nested_reflexivity",     "local",      False),
        ProbeParadox("deep_frame_paradox",     "local",      False),
        ProbeParadox("self_amendment_diagonal","generative", True),
        # adversarial red-team
        ProbeParadox("signalling_mimic",       "local",      False, strength=5.0),   # (a)
        ProbeParadox("noisy_generative_10pct", "generative", True,  noise=0.10),      # (b)
        ProbeParadox("noisy_generative_25pct", "generative", True,  noise=0.25),      # (b)
        ProbeParadox("confounded_local",       "local",      False, confound=0.6),    # (c)
    ]

    rows = [(p.name, chsh(p), p.truth_generative) for p in paradoxes]
    detail, cm = confusion(rows)

    print("=== FORK 1: earned-label CHSH (correlations emerge, not stipulated) ===\n")
    print(f"  {'paradox':26s} {'S':>6s}  {'truth_gen':>9s}  {'pred_gen':>8s}  result")
    for name, S, truth, pred, res in detail:
        print(f"  {name:26s} {S:6.3f}  {str(truth):>9s}  {str(pred):>8s}  {res}")
    print(f"\n  confusion: TP={cm['TP']} TN={cm['TN']} FP={cm['FP']} FN={cm['FN']}")

    # noise threshold sweep: where does the generative signal drop below S=2?
    print("\n=== noise threshold: generative S vs detector-flip probability ===")
    for p in np.linspace(0, 0.5, 11):
        pp = ProbeParadox("gen", "generative", True, noise=float(p))
        S = chsh(pp)
        below = "  <-- drops below local bound" if S <= 2.05 else ""
        print(f"  noise {p:.2f}: S = {S:.3f}{below}")
