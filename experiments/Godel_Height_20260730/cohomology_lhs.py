#!/usr/bin/env python3
"""
cohomology_lhs.py
=================
PUSH 2: NON-CYCLIC frame groups.  Everything before this held G cyclic (Z_2 in
sections 8-9, Z_m via Tate in section 10).  The honest gap flagged in section 10:
a non-cyclic frame group -- frames that come in a non-cyclic bundle, e.g.
G = Z_2 x Z_2 -- has NO Tate periodicity, so M^G/Norm(M) does not apply and we
must either enumerate cochains directly or use the Lyndon-Hochschild-Serre (LHS)
spectral sequence.  I do BOTH, and I am careful about the enumeration blow-up:

  * DIRECT: full H^2(G, M) by cochain enumeration.  For |G| = 4 a 2-cochain is a
    function G^2 -> M, i.e. |M|^16 of them.  |M| = 2 => 65536 (fine).  |M| = 3 =>
    ~43M (too slow) -- so DIRECT is CAPPED at |M| <= 2.  This is exactly the
    'blow-up we already avoided' generalized to non-cyclic G, and I keep the cap.

  * LHS cross-check: for G = Z_2 x Z_2 = <a> x <b> with A = <a>, G/A = <b>, the
    spectral sequence has E_2^{p,q} = H^p(G/A, H^q(A, M)) => H^{p+q}(G, M).  For
    the trivial action every H^q(Z_2, M) is computable by Tate, and the low-degree
    exact sequence + the known additive structure lets us predict |H^2(G,M)| and
    compare to the DIRECT count.  We do this only where DIRECT is affordable, as a
    consistency check, and REPORT any place we cannot close the check rather than
    papering over it.

WHAT WE EXPECT (and are testing): the clean single-invariant law of section 9
(one number v_2(N) decides the phase) is EXPECTED TO BREAK for non-cyclic G,
because non-cyclic groups have genuinely 2-dimensional cohomology and cross-terms.
The point of this file is to SEE it break, quantify how, and be explicit about
what can and cannot be concluded.
"""
from __future__ import annotations
import itertools, json, os, math
from collections import Counter

os.makedirs("results", exist_ok=True)


# --------------------------------------------------------------------------- #
# Groups as explicit element sets with an add table; modules as before.        #
# --------------------------------------------------------------------------- #
class FinGroup:
    """Finite abelian group given by cyclic orders; elements are tuples."""
    def __init__(self, orders, name):
        self.orders = tuple(orders); self.name = name
        self.elems = list(itertools.product(*[range(n) for n in orders]))
        self.zero = tuple(0 for _ in orders)
        self.order = len(self.elems)
    def add(self, a, b):
        return tuple((x + y) % n for x, y, n in zip(a, b, self.orders))
    def neg(self, a):
        return tuple((-x) % n for x, n in zip(a, self.orders))


class Mod:
    def __init__(self, orders):
        self.orders = tuple(orders)
        self.elems = list(itertools.product(*[range(n) for n in orders]))
        self.zero = tuple(0 for _ in orders)
        self.size = len(self.elems)
    def add(self, a, b): return tuple((x + y) % n for x, y, n in zip(a, b, self.orders))
    def neg(self, a): return tuple((-x) % n for x, n in zip(a, self.orders))


def trivial_action(G, M):
    """action(g, x) = x for all g (trivial module)."""
    return lambda g, x: x


# --------------------------------------------------------------------------- #
# DIRECT H^2(G, M) by cochain enumeration (capped |M| <= 2 for |G| = 4).       #
# --------------------------------------------------------------------------- #
def direct_H2(G: FinGroup, M: Mod, action):
    """Full |H^2(G, M)| and invariant factors, by enumerating 2-cochains.
    2-cochain f: G x G -> M as a dict over key list; d2=0 selects cocycles;
    image of d1 gives coboundaries; count cosets."""
    keys2 = list(itertools.product(G.elems, repeat=2))
    keys1 = list(G.elems)
    n2, n1 = len(keys2), len(keys1)
    blow = M.size ** n2
    if blow > 300000:
        return {"skipped": True, "reason": f"|M|^|G|^2 = {M.size}^{n2} = {blow} too big"}

    def d1(f1):
        # f1: G -> M as dict
        out = {}
        for (g1, g2) in keys2:
            t = M.add(action(g1, f1[g2]), M.neg(f1[G.add(g1, g2)]))
            t = M.add(t, f1[g1])
            out[(g1, g2)] = t
        return tuple(out[k] for k in keys2)

    def is_cocycle(fvals):
        f = {keys2[i]: fvals[i] for i in range(n2)}
        for (g1, g2, g3) in itertools.product(G.elems, repeat=3):
            t = action(g1, f[(g2, g3)])
            t = M.add(t, M.neg(f[(G.add(g1, g2), g3)]))
            t = M.add(t, f[(g1, G.add(g2, g3))])
            t = M.add(t, M.neg(f[(g1, g2)]))
            if t != M.zero:
                return False
        return True

    # enumerate cocycles
    Z2 = [fv for fv in itertools.product(M.elems, repeat=n2) if is_cocycle(fv)]
    # coboundaries
    B2 = set()
    for f1vals in itertools.product(M.elems, repeat=n1):
        f1 = {keys1[i]: f1vals[i] for i in range(n1)}
        B2.add(d1(f1))
    # cosets
    def addv(a, b): return tuple(M.add(a[i], b[i]) for i in range(n2))
    B2list = list(B2); seen = set(); classes = 0
    for z in Z2:
        if z in seen: continue
        coset = set(addv(z, b) for b in B2list)
        seen |= coset; classes += 1
    # invariant factors of H2 = Z2/B2
    inv = h2_invariants(M, keys2, Z2, B2, addv)
    return {"skipped": False, "|Z2|": len(Z2), "|B2|": len(B2),
            "|H2|": classes, "H2_invariants": inv}


def h2_invariants(M, keys2, Z2, B2, addv):
    """Invariant factors of Z2/B2 (an abelian group) via the element-order method."""
    B2 = set(B2)
    def coset(z): return frozenset(addv(z, b) for b in B2)
    reps = {}
    for z in Z2:
        c = coset(z)
        if c not in reps: reps[c] = z
    keys = list(reps.keys())
    order = len(keys)
    if order == 1: return []
    zero = coset(tuple(M.zero for _ in keys2))
    def mul(z, n):
        acc = tuple(M.zero for _ in keys2)
        for _ in range(n): acc = addv(acc, z)
        return acc
    # factor order
    def factor(nn):
        f = {}; d = 2
        while d*d <= nn:
            while nn % d == 0: f[d]=f.get(d,0)+1; nn//=d
            d += 1
        if nn>1: f[nn]=f.get(nn,0)+1
        return f
    facs = []
    for p in factor(order):
        A=[1]; k=0
        while True:
            k+=1
            cnt=sum(1 for c in keys if coset(mul(reps[c], p**k))==zero)
            A.append(cnt)
            if cnt==A[-2]: break
        logs=[round(math.log(a,p)) if a>1 else 0 for a in A]
        r=[logs[i]-logs[i-1] for i in range(1,len(logs))]+[0]
        for j in range(1,len(A)):
            for _ in range(r[j-1]-r[j]): facs.append(p**j)
    return sorted(facs)


# --------------------------------------------------------------------------- #
# LHS prediction for G = Z2 x Z2, TRIVIAL module M (finite abelian).           #
# For the trivial Z2xZ2-module M, the cohomology ring is known:                #
#   H^*(Z2xZ2, F_2) = F_2[x, y]  (poly ring, |x|=|y|=1), so                     #
#   dim_{F_2} H^n(Z2xZ2, F_2) = n + 1.  In particular dim H^2 = 3.             #
# For M = (Z2)^r trivial:  H^2(Z2xZ2, (Z2)^r) = (Z2)^{3r},  |H^2| = 2^{3r}.    #
# For M = Z4 trivial: use the Bockstein/coefficient sequence; we instead just   #
# report the F_2 case as the clean LHS-backed prediction and CROSS-CHECK it     #
# against DIRECT for M = Z2.                                                    #
# --------------------------------------------------------------------------- #
def lhs_prediction_trivial_F2(r):
    """|H^2(Z2xZ2, (Z2)^r)| under trivial action = 2^{3r}; invariants = [2]*3r."""
    return {"|H2|": 2 ** (3 * r), "H2_invariants": [2] * (3 * r),
            "basis": "H^*(Z2xZ2,F2)=F2[x,y], dim H^2 = 3 => 3r copies of Z2"}


# --------------------------------------------------------------------------- #
def run():
    print("=" * 78)
    print("PUSH 2: non-cyclic frame group G = Z2 x Z2 (no Tate periodicity)")
    print("=" * 78)

    G = FinGroup((2, 2), "Z2xZ2")
    results = []

    # (1) DIRECT vs LHS on M = Z2 (trivial): the affordable exact case.
    print("\n  [A] DIRECT vs LHS cross-check, trivial action")
    for mname, morders, r in [("Z2", (2,), 1), ("Z2xZ2", (2, 2), 2)]:
        M = Mod(morders)
        act = trivial_action(G, M)
        direct = direct_H2(G, M, act)
        lhs = lhs_prediction_trivial_F2(r)
        row = {"G": "Z2xZ2", "M": mname, "action": "trivial",
               "direct": direct, "lhs": lhs}
        results.append(row)
        if direct.get("skipped"):
            print(f"    M={mname:6s}: DIRECT skipped ({direct['reason']}); "
                  f"LHS predicts |H2|={lhs['|H2|']} inv={lhs['H2_invariants']}")
        else:
            agree = (direct["|H2|"] == lhs["|H2|"]
                     and sorted(direct["H2_invariants"]) == sorted(lhs["H2_invariants"]))
            print(f"    M={mname:6s}: DIRECT |H2|={direct['|H2|']} inv={direct['H2_invariants']}"
                  f"  ||  LHS |H2|={lhs['|H2|']} inv={lhs['H2_invariants']}  "
                  f"=> {'AGREE' if agree else 'DISAGREE'}")

    # (2) the KEY comparison: cyclic Z4 vs non-cyclic Z2xZ2 as frame groups, same
    #     module M = Z2 trivial. Section-9 (cyclic) gave |H2(Z2,Z2)|=2 and
    #     |H2(Z4,Z2)|=2 (one bit). Non-cyclic gives 2^3 = 8 (THREE bits). This is
    #     the clean break: a non-cyclic frame group multiplies the generative rank.
    print("\n  [B] cyclic vs non-cyclic frame group on the SAME module M=Z2 (trivial):")
    M = Mod((2,))
    # cyclic references via direct on Z2 and Z4
    for gname, gorders in [("Z2", (2,)), ("Z4", (4,))]:
        Gc = FinGroup(gorders, gname)
        d = direct_H2(Gc, M, trivial_action(Gc, M))
        print(f"    G={gname:6s} (cyclic):     |H2(G,Z2)|={d['|H2|']}  inv={d['H2_invariants']}")
    d4 = direct_H2(G, M, trivial_action(G, M))
    print(f"    G=Z2xZ2 (non-cyclic): |H2(G,Z2)|={d4['|H2|']}  inv={d4['H2_invariants']}")
    print(f"    => NON-CYCLIC frame group gives rank {len(d4['H2_invariants'])} "
          f"(a THREE-dimensional generative core) vs rank 1 for the cyclic groups.")
    results.append({"comparison": "cyclic_vs_noncyclic_on_Z2",
                    "H2_Z2xZ2_on_Z2": d4})

    # (3) does the section-9 SINGLE-INVARIANT (v2) law survive? -- NO, and here is
    #     the explicit statement of the break.
    print("\n  [C] does the section-9 single-invariant (v2) phase law survive? NO.")
    print("      For cyclic G=Z2, |H2(Z2,Z_N)| in {1,2}: a BIT (phase = v2(N)).")
    print("      For non-cyclic G=Z2xZ2 (trivial), |H2(G,(Z2)^r)| = 2^{3r}: the")
    print("      generative core has rank 3r -- NOT captured by any single v2 number.")
    print("      The scalar phase law is a CYCLIC-G artifact; non-cyclic frame")
    print("      groups need the whole cohomology-ring rank, not one invariant.")

    with open("results/cohomology_lhs.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 78)
    print("CLAIM / CANNOT-CLAIM LEDGER (push 2)")
    print("=" * 78)
    print("""
  CAN CLAIM:
    * DIRECT enumeration for G=Z2xZ2 on M=Z2 (trivial) is EXACT and gives
      |H^2| = 8, H^2 = (Z2)^3 -- a rank-3 generative core.  It AGREES with the
      LHS/cohomology-ring prediction dim H^2(Z2xZ2, F2) = 3.  (Cross-checked.)
    * The section-9 single-number (v2) phase law is SPECIFIC TO CYCLIC G.  For a
      non-cyclic frame group the generative rank grows (3 per F2-generator of M),
      so no single invariant classifies the phase.  This is the expected break,
      now made explicit and exact for one case.

  CANNOT CLAIM (yet, or ever):
    * DIRECT beyond |M| <= 2 for |G|=4 (the |M|^16 enumeration blows up); the
      M=Z2xZ2 trivial case is predicted by LHS (|H^2|=2^6=64) but only the M=Z2
      case is DIRECT-verified here.  We DO NOT claim the M=Z2xZ2 direct number.
    * A general non-cyclic phase law.  We have one exact data point + a ring-
      theoretic prediction, not a classification.  Whether there is a clean
      'non-cyclic generativity law' is OPEN and may have no tidy form.
    * Non-TRIVIAL actions of Z2xZ2: not enumerated here (would need direct, capped).
    * Governance reading stays ANALOGY, as everywhere in this project.
""")


if __name__ == "__main__":
    run()
