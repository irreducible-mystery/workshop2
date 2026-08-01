#!/usr/bin/env python3
"""
cohomology_quotient.py
======================
OPTION 2: build the actual QUOTIENT TYPE, not just a class census.

Turn-3/4 (cohomology_frame / cohomology_sweep / cohomology_phase) *counted*
cohomology classes: how many cosets of B^2 in Z^2, and the order of a generator.
That is a census.  The external Lean artifact does more: it constructs a genuine
Quot type (gauge_quotient_exactly_two), equips it with a group law, and proves the
gauge map phi (1-cochain -> coboundary) is a HOMOMORPHISM (gaugePhi_comp,
gaugePhi_inv).  This script matches that on our side, as an executable object with
axioms *checked*, so that H^2 becomes a constructed group we can compute in, not
just a number.

We build, for G = Z_m acting on M = Z_N by an involution/unit u:

  1. Z2  = the abelian group of 2-cocycles (pointwise addition mod N)
  2. B2  = the subgroup of 2-coboundaries  = image of d1
  3. the canonical projection  Z2 -> H2 = Z2/B2  via a coset-normal-form
  4. H2 as a concrete finite abelian group: its elements (normal forms),
     its addition table, its identity, its inverses, its generators/order
  5. VERIFY the group axioms on H2 (closure, assoc, identity, inverse, comm)
  6. the gauge map  phi : C1 (1-cochains) -> B2 <= Z2,  f1 |-> d1(f1),
     and PROVE  phi is a homomorphism:  d1(f1 + g1) = d1(f1) + d1(g1),
     d1(0) = 0,  d1(-f1) = -d1(f1)     [the exact analogue of gaugePhi_comp/_inv]
  7. the FIRST ISOMORPHISM THEOREM, executable:  C1/ker(phi)  ~=  im(phi) = B2,
     and  H2 = Z2 / im(phi).  We check |C1| = |ker phi| * |im phi|.

Everything is literal finite group cohomology; the only analogy is the standing
paradox<->2-cochain, frame-change<->1-cochain dictionary from sections 8-9.
"""
from __future__ import annotations
import itertools, json, os, math
from collections import defaultdict

os.makedirs("results", exist_ok=True)


# --------------------------------------------------------------------------- #
# Cochain machinery for G = Z_m, M = Z_N, generator acts by mult-by-u.         #
# A 1-cochain is a function G -> M given as a tuple indexed by G.              #
# A 2-cochain is a function G^2 -> M given as a tuple indexed by G^2.          #
# We store cochains as plain tuples (canonical, hashable) in a fixed key order.#
# --------------------------------------------------------------------------- #
class CochainWorld:
    def __init__(self, m, N, u):
        assert pow(u, m, N) == 1, f"u={u} is not order-dividing-{m} mod {N}"
        self.m, self.N, self.u = m, N, u
        self.G = list(range(m))
        self.keys1 = [(g,) for g in self.G]
        self.keys2 = list(itertools.product(self.G, repeat=2))
        self.keys3 = list(itertools.product(self.G, repeat=3))
        self.idx1 = {k: i for i, k in enumerate(self.keys1)}
        self.idx2 = {k: i for i, k in enumerate(self.keys2)}

    # module arithmetic
    def gadd(self, a, b): return (a + b) % self.m
    def madd(self, a, b): return (a + b) % self.N
    def minv(self, a): return (-a) % self.N
    def act(self, g, x): return (pow(self.u, g, self.N) * x) % self.N

    # cochain addition / inverse (as tuples)
    def add(self, f, g): return tuple(self.madd(a, b) for a, b in zip(f, g))
    def neg(self, f): return tuple(self.minv(a) for a in f)
    def zero(self, n): return tuple([0] * n)

    # coboundary d1: C1 -> C2   (bar/inhomogeneous)
    def d1(self, f1):
        # build lookup g -> value
        val = {self.keys1[i]: f1[i] for i in range(len(self.keys1))}
        out = []
        for (g1, g2) in self.keys2:
            t = self.madd(self.act(g1, val[(g2,)]),
                          self.minv(val[(self.gadd(g1, g2),)]))
            t = self.madd(t, val[(g1,)])
            out.append(t)
        return tuple(out)

    # coboundary d2: C2 -> C3   (used to test the cocycle condition)
    def d2(self, f2):
        val = {self.keys2[i]: f2[i] for i in range(len(self.keys2))}
        out = []
        for (g1, g2, g3) in self.keys3:
            t = self.act(g1, val[(g2, g3)])
            t = self.madd(t, self.minv(val[(self.gadd(g1, g2), g3)]))
            t = self.madd(t, val[(g1, self.gadd(g2, g3))])
            t = self.madd(t, self.minv(val[(g1, g2)]))
            out.append(t)
        return tuple(out)

    def is_cocycle(self, f2):
        return all(v == 0 for v in self.d2(f2))


# --------------------------------------------------------------------------- #
# Build the quotient group H^2 = Z^2 / B^2 as a concrete finite abelian group. #
# --------------------------------------------------------------------------- #
def build_quotient(m, N, u):
    W = CochainWorld(m, N, u)
    n2 = len(W.keys2)   # number of G^2 keys
    n1 = len(W.keys1)   # number of G keys

    # Z^2 : all cocycles
    Z2 = [f for f in itertools.product(range(N), repeat=n2) if W.is_cocycle(f)]
    Z2set = set(Z2)

    # B^2 : image of d1
    C1 = list(itertools.product(range(N), repeat=n1))
    B2set = set(W.d1(f1) for f1 in C1)
    # sanity: every coboundary is a cocycle
    assert B2set <= Z2set, "B^2 not contained in Z^2 (bug)"

    # --- coset normal form: represent each class by the lexicographically-min
    #     element of its coset  z + B^2.  This is the canonical projection. ---
    B2list = list(B2set)

    def coset(z):
        return frozenset(W.add(z, b) for b in B2list)

    def normal_form(z):
        return min(W.add(z, b) for b in B2list)

    reps = sorted(set(normal_form(z) for z in Z2))   # the H^2 elements
    H2_elems = reps
    order = len(H2_elems)

    # group law on H^2 (add representatives, renormalize)
    def hadd(a, b):
        return normal_form(W.add(a, b))
    def hneg(a):
        return normal_form(W.neg(a))
    hzero = normal_form(W.zero(n2))

    # ------------------------------------------------------------------ #
    # VERIFY the abelian-group axioms on H^2.                             #
    # ------------------------------------------------------------------ #
    axioms = {}
    # closure
    axioms["closure"] = all(hadd(a, b) in H2_elems for a in H2_elems for b in H2_elems)
    # identity
    axioms["identity_in_group"] = hzero in H2_elems
    axioms["identity_law"] = all(hadd(a, hzero) == a and hadd(hzero, a) == a
                                 for a in H2_elems)
    # inverse
    axioms["inverse"] = all(hadd(a, hneg(a)) == hzero for a in H2_elems)
    # associativity
    axioms["associative"] = all(
        hadd(hadd(a, b), c) == hadd(a, hadd(b, c))
        for a in H2_elems for b in H2_elems for c in H2_elems)
    # commutativity
    axioms["commutative"] = all(hadd(a, b) == hadd(b, a)
                                for a in H2_elems for b in H2_elems)

    # element orders / group structure (finite abelian => product of cyclics)
    def elem_order(a):
        acc = a; k = 1
        while acc != hzero:
            acc = hadd(acc, a); k += 1
            if k > order + 1: break
        return k
    orders = {tuple(a): elem_order(a) for a in H2_elems}
    max_ord = max(orders.values())
    # is it cyclic?
    cyclic = any(o == order for o in orders.values())

    # ------------------------------------------------------------------ #
    # gauge map phi = d1 : C1 -> B2, and PROVE it is a homomorphism.      #
    #   phi(f + g) = phi(f) + phi(g)   (gaugePhi_comp analogue)           #
    #   phi(0) = 0                                                        #
    #   phi(-f) = -phi(f)              (gaugePhi_inv analogue)            #
    # ------------------------------------------------------------------ #
    hom_add = all(W.d1(W.add(f, g)) == W.add(W.d1(f), W.d1(g))
                  for f in C1 for g in C1)
    hom_zero = (W.d1(W.zero(n1)) == W.zero(n2))
    hom_neg = all(W.d1(W.neg(f)) == W.neg(W.d1(f)) for f in C1)
    gauge_is_hom = hom_add and hom_zero and hom_neg

    # first isomorphism theorem:  |C1| = |ker phi| * |im phi|            #
    ker = [f for f in C1 if W.d1(f) == W.zero(n2)]
    im = B2set
    fit = (len(C1) == len(ker) * len(im))

    # H^2 = Z^2 / im(phi):  |Z^2| = |H^2| * |B^2|                        #
    quotient_count = (len(Z2) == order * len(B2set))

    return {
        "m": m, "N": N, "u": u,
        "sizes": {"|C1|": len(C1), "|Z2|": len(Z2), "|B2|": len(B2set),
                  "|H2|": order, "|ker phi|": len(ker), "|im phi|": len(im)},
        "H2_order": order,
        "H2_element_orders": sorted(orders.values()),
        "H2_max_element_order": max_ord,
        "H2_is_cyclic": cyclic,
        "axioms": axioms,
        "all_axioms_pass": all(axioms.values()),
        "gauge_is_homomorphism": gauge_is_hom,
        "gauge_hom_detail": {"phi(f+g)=phi f+phi g": hom_add,
                             "phi(0)=0": hom_zero,
                             "phi(-f)=-phi f": hom_neg},
        "first_iso_|C1|=|ker||im|": fit,
        "quotient_|Z2|=|H2||B2|": quotient_count,
        "H2_elements": [list(a) for a in H2_elems],
        "H2_addition_table": {f"{list(a)}+{list(b)}": list(hadd(a, b))
                              for a in H2_elems for b in H2_elems},
    }


def pretty(res):
    s = res["sizes"]
    print(f"  G=Z{res['m']}  M=Z{res['N']}  action u={res['u']}"
          f"{'  (trivial)' if res['u']==1 else ''}")
    print(f"    |C1|={s['|C1|']}  |Z2|={s['|Z2|']}  |B2|={s['|B2|']}  "
          f"|H2|={s['|H2|']}  |ker phi|={s['|ker phi|']}  |im phi|={s['|im phi|']}")
    print(f"    H2 order={res['H2_order']}  cyclic={res['H2_is_cyclic']}  "
          f"element orders={res['H2_element_orders']}")
    ax = "PASS" if res["all_axioms_pass"] else "FAIL"
    print(f"    abelian-group axioms on H2: {ax}  "
          f"({', '.join(k for k,v in res['axioms'].items() if v)})")
    print(f"    gauge map phi=d1 is a HOMOMORPHISM: {res['gauge_is_homomorphism']}  "
          f"{res['gauge_hom_detail']}")
    print(f"    first iso |C1|=|ker||im|: {res['first_iso_|C1|=|ker||im|']}   "
          f"quotient |Z2|=|H2||B2|: {res['quotient_|Z2|=|H2||B2|']}")


if __name__ == "__main__":
    print("=" * 74)
    print("OPTION 2: H^2 as a CONSTRUCTED quotient group (axioms + gauge hom checked)")
    print("=" * 74)

    # (A) the Circle-Five anchor: G=Z2, M = Gaussian units as Z4, trivial + conj
    #     and the Z8 fragile case, and an odd rigid case -- one from each phase.
    configs = [
        (2, 4, 1),   # ROBUST GENERATIVE, trivial action (Gaussian-units anchor)
        (2, 4, 3),   # ROBUST GENERATIVE, conjugation action
        (2, 8, 1),   # FRAGILE: trivial action keeps the class
        (2, 8, 3),   # FRAGILE: this action DESTROYS the class
        (2, 3, 1),   # RIGID (odd)
        (2, 2, 1),   # smallest generative
    ]
    results = []
    for (m, N, u) in configs:
        res = build_quotient(m, N, u)
        pretty(res); print()
        results.append(res)

    # summary assertions -- the whole point is these must all hold
    allpass = all(r["all_axioms_pass"] and r["gauge_is_homomorphism"]
                  and r["first_iso_|C1|=|ker||im|"] and r["quotient_|Z2|=|H2||B2|"]
                  for r in results)
    print("=" * 74)
    print(f"ALL configs: group axioms + gauge-homomorphism + first-iso + quotient "
          f"identities hold: {allpass}")
    print("=" * 74)

    # trim tables for the two anchor cases only (keep JSON small)
    for r in results:
        if not (r["m"] == 2 and r["N"] == 4):
            r.pop("H2_addition_table", None)
            r.pop("H2_elements", None)

    with open("results/cohomology_quotient.json", "w") as f:
        json.dump({"configs": results, "all_pass": allpass}, f, indent=2)
    print("wrote results/cohomology_quotient.json")
