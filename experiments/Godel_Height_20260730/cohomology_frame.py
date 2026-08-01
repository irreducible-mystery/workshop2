#!/usr/bin/env python3
"""
cohomology_frame.py
===================
Circle-Five-style experiment on OUR frame-lattice.

The claim we have only gestured at so far (M4 / Fork 1 give a *discriminator*,
S<=2 vs S>2, but not a group statement) is upgraded here into an explicit
finite group-cohomology construction, following the *technique* of the external
Circle One->Five Lean build (define a gauge/coboundary action, show the
coherence equation is the cocycle equation, quotient, count classes) -- but on
our objects, and crucially in the NONTRIVIAL-action case their artifact does not
cover.

PREDICTION UNDER TEST
---------------------
  frame-resolvable paradox  ==  coboundary  ==  identity class   ("pure gauge")
  generative residue        ==  nontrivial cocycle == the generator

WHAT IS LITERAL MATH vs ANALOGY
-------------------------------
  LITERAL   : the cochain complex, d^2 = 0, cocycles Z^n, coboundaries B^n,
              H^n = Z^n / B^n, class counting, generator order. This is exact
              finite group cohomology over F_2 (and over the unit module).
  ANALOGY   : the identification "paradox <-> 2-cochain", "reachable frame-change
              <-> 1-cochain whose coboundary can cancel it", "generative <-> not
              a coboundary". This mapping is the modelling choice; it is
              internally consistent and it is what makes the discriminator a
              quotient, but it is not a theorem about real institutions.

We do everything over the group G = Z2 (frame flip) first -- so we can RECOVER
their trivial-action H = Z2 as a sanity anchor -- then turn on a NONTRIVIAL
action and watch what changes.
"""
from __future__ import annotations
import itertools
import numpy as np


# --------------------------------------------------------------------------- #
# Group and modules.                                                          #
#   G = Z2 = {0,1} under addition; 1 = "flip to the dual/conjugate frame".    #
#   Coefficient module M = Z2 = {0,1} under addition (F_2 truth-defect).      #
#   Action: g acts on m by sign; trivial action => g.m = m always;           #
#           nontrivial action => 1.m = -m = m over F_2 (so still m!) -- so to #
#   get a genuinely different action we use the module Z4 (or the unit group  #
#   {+1,-1,+i,-i}) where conjugation is a real involution.                    #
# --------------------------------------------------------------------------- #

# We use the UNIT MODULE M = Z[i]^x = {1, -1, i, -i} written multiplicatively,
# encoded as integers 0,1,2,3 for exponents of i:  k <-> i^k.
#   mul(a,b) = (a+b) mod 4 ;  inv(a) = (-a) mod 4 ;  identity e = 0.
# The nontrivial frame action is COMPLEX CONJUGATION: conj(i^k) = i^(-k),
#   i.e. act(g=1, k) = (-k) mod 4 ; act(g=0, k) = k.
# This is exactly the Galois mirror the Circle Five build uses, and over this
# module the action is genuinely nontrivial (conj swaps i <-> -i).

MOD = 4  # |M| = 4 (the four Gaussian units)


def m_mul(a, b): return (a + b) % MOD
def m_inv(a):    return (-a) % MOD
M_E = 0


def action(g, k, nontrivial):
    """g in {0,1} acts on module element k (exponent of i)."""
    if not nontrivial:
        return k
    return (-k) % MOD if g == 1 else k          # conjugation on the flip


G = [0, 1]                                       # Z2


def gadd(a, b): return (a + b) % 2               # group op on Z2


# --------------------------------------------------------------------------- #
# Cochains: C^n = functions G^n -> M.  We store them as dicts.                #
# Coboundary d^n : C^n -> C^{n+1}, INHOMOGENEOUS (bar) resolution, written    #
# multiplicatively in M (so "+" in additive M = the group law m_mul):         #
#                                                                             #
#  (d^1 f)(g1,g2) = g1 . f(g2)  *  f(g1 g2)^{-1}  *  f(g1)                     #
#  (d^2 f)(g1,g2,g3) = g1.f(g2,g3) * f(g1 g2,g3)^{-1} * f(g1,g2 g3)           #
#                        * f(g1,g2)^{-1}                                       #
#  (d^0 m)(g1) = g1.m * m^{-1}                                                 #
# --------------------------------------------------------------------------- #

def tuples(n):
    return list(itertools.product(G, repeat=n))


def d0(m, nontrivial):
    """d^0 : M -> C^1.  (d0 m)(g) = g.m - m."""
    return {(g,): m_mul(action(g, m, nontrivial), m_inv(m)) for g in G}


def d1(f, nontrivial):
    """d^1 : C^1 -> C^2."""
    out = {}
    for g1, g2 in tuples(2):
        t = m_mul(action(g1, f[(g2,)], nontrivial), m_inv(f[(gadd(g1, g2),)]))
        t = m_mul(t, f[(g1,)])
        out[(g1, g2)] = t
    return out


def d2(f, nontrivial):
    """d^2 : C^2 -> C^3."""
    out = {}
    for g1, g2, g3 in tuples(3):
        t = action(g1, f[(g2, g3)], nontrivial)
        t = m_mul(t, m_inv(f[(gadd(g1, g2), g3)]))
        t = m_mul(t, f[(g1, gadd(g2, g3))])
        t = m_mul(t, m_inv(f[(g1, g2)]))
        out[(g1, g2, g3)] = t
    return out


def is_zero(coch):
    return all(v == M_E for v in coch.values())


# --------------------------------------------------------------------------- #
# Enumerate cochain groups, cocycles, coboundaries, and H^2.                  #
# --------------------------------------------------------------------------- #

def all_cochains(n):
    keys = tuples(n)
    for vals in itertools.product(range(MOD), repeat=len(keys)):
        yield dict(zip(keys, vals))


def cohomology_H2(nontrivial):
    """Compute Z^2, B^2, H^2 = Z^2/B^2 for G=Z2 acting on M=Z4 units."""
    # 2-cocycles: d2 f = 0
    Z2 = [f for f in all_cochains(2) if is_zero(d2(f, nontrivial))]
    # 2-coboundaries: image of d1 over all 1-cochains
    B2_set = set()
    for f1 in all_cochains(1):
        b = d1(f1, nontrivial)
        B2_set.add(tuple(sorted(b.items())))
    def as_key(f): return tuple(sorted(f.items()))
    B2 = [dict(t) for t in B2_set]

    # classes: partition Z2 by (z * b) equivalence, i.e. z ~ z' iff z*z'^{-1} in B2
    def mul_coch(a, b):
        return {k: m_mul(a[k], b[k]) for k in a}
    def inv_coch(a):
        return {k: m_inv(a[k]) for k in a}
    B2keys = set(as_key(b) for b in B2)
    classes = []
    seen = set()
    for z in Z2:
        zk = as_key(z)
        if zk in seen:
            continue
        # build the whole coset z*B2
        coset = set()
        for b in B2:
            coset.add(as_key(mul_coch(z, b)))
        seen |= coset
        classes.append((z, coset))
    return Z2, B2, classes, B2keys


# --------------------------------------------------------------------------- #
# Encode OUR paradoxes as 2-cochains (their "frame defect").                  #
#   A frame-resolvable paradox with dissolution height h is modelled as a     #
#   2-cochain that IS a coboundary (pure gauge): pick a 1-cochain witness and #
#   set the paradox defect = d1(witness). By construction it lies in B^2 ->   #
#   identity class. (This is the modelling analogy, stated openly.)           #
#   The generative paradox is a genuine 2-cocycle that is NOT a coboundary.   #
# --------------------------------------------------------------------------- #

def true_generator(nontrivial):
    """Return a genuine nontrivial 2-cocycle (a Z^2 element NOT in B^2),
    computed from the actual cohomology rather than hand-guessed. This is the
    'associator that is not pure gauge' -- the generative defect."""
    def as_key(f): return tuple(sorted(f.items()))
    Z2, B2, classes, B2keys = cohomology_H2(nontrivial)
    reps = [z for z in Z2 if as_key(z) not in B2keys]
    return reps[0] if reps else {(g1, g2): M_E for g1, g2 in tuples(2)}


def paradox_cochain(kind, seed, nontrivial):
    """kind in {'resolvable','generative'}.
       resolvable -> a coboundary d1(witness) (identity class, pure gauge).
       generative -> the TRUE nontrivial 2-cocycle for this action (not gauge).
    """
    rng = np.random.default_rng(seed)
    if kind == "resolvable":
        # a random 1-cochain witness; its coboundary is the (pure-gauge) defect.
        # Whatever reachable frame-change we pick, the defect is a coboundary,
        # so a frame-resolvable paradox is identity-class BY CONSTRUCTION.
        witness = {(g,): int(rng.integers(0, MOD)) for g in G}
        return d1(witness, nontrivial)
    # generative: the associator that no reachable frame-change can cancel.
    return true_generator(nontrivial)


# --------------------------------------------------------------------------- #
# The paradox bag (same names/heights as checks.py), tagged resolvable/gen.   #
# --------------------------------------------------------------------------- #
PARADOXES = [
    ("liar_two_valued",        "resolvable", 1),
    ("goodhart_measurement",   "resolvable", 1),
    ("order_effect",           "resolvable", 2),
    ("nested_reflexivity",     "resolvable", 3),
    ("deep_frame_paradox",     "resolvable", 5),
    ("self_amendment_diagonal","generative", None),
]


def classify_paradox(defect, B2keys, classes):
    """Return 'identity' if defect is a coboundary, else the nontrivial class id."""
    def as_key(f): return tuple(sorted(f.items()))
    if as_key(defect) in B2keys:
        return "identity"
    # find which nonidentity class it lands in
    for idx, (z, coset) in enumerate(classes):
        if as_key(defect) in coset:
            return f"class_{idx}"
    return "OUTSIDE_H2 (not a cocycle)"


# --------------------------------------------------------------------------- #
# Deterministic checks.                                                       #
# --------------------------------------------------------------------------- #
def check_complex_closes(nontrivial):
    """d1 o d0 = 0 and d2 o d1 = 0 for all inputs (the complex is a complex)."""
    ok = True
    for m in range(MOD):
        if not is_zero(d1(d0(m, nontrivial), nontrivial)):
            ok = False
    for f1 in all_cochains(1):
        if not is_zero(d2(d1(f1, nontrivial), nontrivial)):
            ok = False
    return ok


def run(nontrivial):
    tag = "NONTRIVIAL (conjugation)" if nontrivial else "TRIVIAL"
    print(f"\n{'='*70}\nACTION: {tag}   G = Z2,  M = Gaussian units Z[i]^x (|M|=4)\n{'='*70}")

    closes = check_complex_closes(nontrivial)
    print(f"  complex closes (d1.d0=0 and d2.d1=0): {closes}")

    Z2, B2, classes, B2keys = cohomology_H2(nontrivial)
    print(f"  |Z^2| (2-cocycles)     = {len(Z2)}")
    print(f"  |B^2| (2-coboundaries) = {len(B2)}")
    print(f"  |H^2| = |Z^2/B^2|      = {len(classes)}   "
          f"(classes: identity + {len(classes)-1} nontrivial)")

    # order of the nontrivial generator (if any): smallest n with g^n in B2
    gen_order = None
    def as_key(f): return tuple(sorted(f.items()))
    def mul_coch(a, b): return {k: m_mul(a[k], b[k]) for k in a}
    for z, coset in classes:
        if as_key(z) in B2keys:
            continue                     # identity class
        # power it up
        acc = {k: z[k] for k in z}
        for n in range(1, 8):
            if as_key(acc) in B2keys:
                gen_order = n
                break
            acc = mul_coch(acc, z)
        break
    print(f"  order of nontrivial generator: {gen_order}  "
          f"=> H^2 ~ Z{gen_order if gen_order else 1}")

    # classify every paradox
    print("  paradox -> cohomology class:")
    hits = {"identity": [], "nontrivial": [], "outside": []}
    for name, kind, height in PARADOXES:
        defect = paradox_cochain(kind, seed=abs(hash(name)) % (2**31), nontrivial=nontrivial)
        cls = classify_paradox(defect, B2keys, classes)
        bucket = ("identity" if cls == "identity"
                  else "outside" if "OUTSIDE" in cls else "nontrivial")
        hits[bucket].append(name)
        print(f"    {name:26s} [{kind:10s} h={str(height):4s}] -> {cls}")

    # PREDICTION CHECK
    resolvable_all_identity = all(
        classify_paradox(paradox_cochain("resolvable", abs(hash(n)) % (2**31), nontrivial),
                         B2keys, classes) == "identity"
        for n, k, h in PARADOXES if k == "resolvable")
    gen_nontrivial = all(
        classify_paradox(paradox_cochain("generative", abs(hash(n)) % (2**31), nontrivial),
                         B2keys, classes) != "identity"
        for n, k, h in PARADOXES if k == "generative")
    print(f"  PREDICTION: resolvable == identity class : {resolvable_all_identity}")
    print(f"  PREDICTION: generative == nontrivial     : {gen_nontrivial}")
    return {
        "action": tag, "closes": closes, "nZ2": len(Z2), "nB2": len(B2),
        "nH2": len(classes), "gen_order": gen_order,
        "resolvable_identity": resolvable_all_identity,
        "generative_nontrivial": gen_nontrivial, "hits": hits,
    }


def check_same_cochain_two_verdicts():
    """THE HEADLINE: one and the same frame-defect cochain (f(1,1)=2, else e)
    is PURE GAUGE (a coboundary => identity class) under the trivial action, but
    a GENERATOR (not a coboundary => nontrivial class) under conjugation. So
    'is this paradox generative?' is not a property of the paradox alone -- it
    is a property of the paradox TOGETHER WITH how the frame group acts."""
    def as_key(f): return tuple(sorted(f.items()))
    same = {(g1, g2): M_E for g1, g2 in tuples(2)}
    same[(1, 1)] = 2
    print(f"\n{'='*70}\nHEADLINE CHECK: same cochain f(1,1)=2, two actions\n{'='*70}")
    res = {}
    for nontrivial, name in [(False, "trivial"), (True, "conjugation")]:
        Z2, B2, classes, B2keys = cohomology_H2(nontrivial)
        is_cocycle = is_zero(d2(same, nontrivial))
        is_cobound = as_key(same) in B2keys
        verdict = ("identity (pure gauge)" if is_cobound
                   else "GENERATOR (load-bearing)" if is_cocycle
                   else "not even a cocycle")
        print(f"  action={name:12s}: cocycle={is_cocycle}  coboundary={is_cobound}"
              f"  -> {verdict}")
        res[name] = verdict
    flipped = res["trivial"] != res["conjugation"]
    print(f"  => SAME defect, DIFFERENT verdict across the frame action: {flipped}")
    return flipped, res


if __name__ == "__main__":
    r_triv = run(nontrivial=False)
    r_non = run(nontrivial=True)
    flipped, verdicts = check_same_cochain_two_verdicts()

    print(f"\n{'='*70}\nSUMMARY\n{'='*70}")
    print(f"  trivial action    : H^2 has {r_triv['nH2']} classes, generator order "
          f"{r_triv['gen_order']}  (anchor: should match Circle Five's Z2)")
    print(f"  nontrivial action : H^2 has {r_non['nH2']} classes, generator order "
          f"{r_non['gen_order']}")
    print(f"  prediction holds (trivial)    : "
          f"{r_triv['resolvable_identity'] and r_triv['generative_nontrivial']}")
    print(f"  prediction holds (nontrivial) : "
          f"{r_non['resolvable_identity'] and r_non['generative_nontrivial']}")
    if r_triv['nH2'] != r_non['nH2'] or r_triv['gen_order'] != r_non['gen_order']:
        print("  => the NONTRIVIAL action CHANGES the group -- the case their "
              "artifact does not cover. This difference is the finding.")
    else:
        print("  => trivial and nontrivial actions give the same H^2 here.")
