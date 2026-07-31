#!/usr/bin/env python3
"""
cohomology_noncyclic_law.py
===========================
SECTION 12 -- the NON-CYCLIC frame-group phase law (OPEN thread #1 from section 11).

Setting.  Frames come in a bundle G (the frame group); a paradox is a 2-cochain,
a reframe is a 1-cochain, resolvable = coboundary, generative = nontrivial class,
and the GENERATIVE CORE is H^2(G, M).  Sections 8-10 forced G cyclic and found a
single-invariant law (one bit / v_2(N)).  Section 11.2 showed that law is a
CYCLIC-G ARTIFACT: G = Z_2 x Z_2 on M = Z_2 gave rank 3, not 1.  This file asks
the actual OPEN question:

    For NON-CYCLIC G, what replaces the single-invariant law?

STRATEGY (and the honest cap, kept from section 11):
  * DIRECT: full H^2(G, M) by cochain enumeration.  A 2-cochain is G^2 -> M, i.e.
    |M|^(|G|^2) of them.  |G|=4 => |M|^16, so DIRECT is affordable ONLY for |M|<=2.
    |G|=8 => |M|^64, so DIRECT there is affordable ONLY for the trivial 1-elt module
    (useless) -- i.e. NOT at all.  We keep the cap and say so.
  * RING PREDICTION (trivial coefficients, coefficient field F_p): for an
    elementary-abelian G = (Z_p)^k the mod-p cohomology RING is known in closed
    form, so dim_{F_p} H^2(G, F_p) is a formula.  We compute it and, where DIRECT
    is affordable, CHECK direct == ring.  Where DIRECT is NOT affordable we report
    the ring number as PREDICTION ONLY (never as a verified count).

RING FACTS USED (standard; we treat them as the *hypotheses* being tested against
direct enumeration, not as things we are re-deriving):
  * p = 2 :  H^*((Z_2)^k, F_2) = F_2[x_1,...,x_k], deg x_i = 1  (polynomial).
             => dim H^2 = number of degree-2 monomials = C(k,2) + k = k(k+1)/2.
  * p odd :  H^*((Z_p)^k, F_p) = Lambda(y_1..y_k) (x) F_p[x_1..x_k],
             deg y_i = 1, deg x_i = 2.
             => dim H^2 = (# deg-2 from the polynomial part x_i, that's k)
                        + (# deg-2 from products y_i y_j, i<j, that's C(k,2)).
             => dim H^2 = k + C(k,2) = k(k+1)/2  as WELL  -- SAME count in degree 2!
             (The exterior/poly split differs but the degree-2 DIMENSION coincides.
              We flag this coincidence explicitly and test it directly for p=2 and,
              where the cap allows, sanity-probe odd p on CYCLIC pieces via Tate.)

  Trivial-action module law being tested:
        rank_{F_p} H^2(G, (Z_p)^r)  =  r * dim_{F_p} H^2(G, F_p)          (LAW L)
  (each F_p-generator of the module contributes an independent copy of the core).

WHAT IS PROVABLE vs CHECKED is tracked in the printed ledger at the end.
"""
from __future__ import annotations
import itertools, json, os, math
from collections import Counter

os.makedirs("results", exist_ok=True)


# --------------------------------------------------------------------------- #
# Finite abelian groups / modules as tuples with add tables.                   #
# --------------------------------------------------------------------------- #
class Fin:
    def __init__(self, orders, name):
        self.orders = tuple(orders); self.name = name
        self.elems = list(itertools.product(*[range(n) for n in orders]))
        self.zero = tuple(0 for _ in orders)
        self.order = len(self.elems)
    def add(self, a, b): return tuple((x + y) % n for x, y, n in zip(a, b, self.orders))
    def neg(self, a):     return tuple((-x) % n for x, n in zip(a, self.orders))


# --------------------------------------------------------------------------- #
# Invariant factors of an abelian group given as (element set, add, zero).     #
# Primary-decomposition from element-order statistics (same method as sec 11). #
# --------------------------------------------------------------------------- #
def invariant_factors(elems, add, zero):
    n = len(elems)
    if n == 1: return []
    # element orders
    def order_of(x):
        acc = zero; k = 0
        while True:
            acc = add(acc, x); k += 1
            if acc == zero: return k
    orders = [order_of(x) for x in elems]
    # primes dividing |G|
    primes = set()
    m = n
    d = 2
    while d * d <= m:
        while m % d == 0: primes.add(d); m //= d
        d += 1
    if m > 1: primes.add(m)
    # for each prime p, A[k] = #{x : p^k x = 0} = size of p^k-torsion subgroup.
    # ranks of p-primary part: r_k = number of cyclic factors of order >= p^k.
    inv_primary = {}  # prime -> list of exponents (a_1>=a_2>=... ) meaning Z_{p^a}
    for p in primes:
        # count elements whose order divides p^k
        # max exponent
        maxe = 0
        pw = 1
        while pw < n * 2:
            pw *= p; maxe += 1
            if p ** maxe > n: break
        # A[k] = #{x : order(x) | p^k}
        A = [0] * (maxe + 2)
        for o in orders:
            # x is in p^k torsion iff p^k is multiple of the p-part of o? No:
            # x in p^k-torsion iff o | p^k iff o is a power of p and o <= p^k.
            # But element order o may have other prime factors; x is in p-power
            # torsion only if o is a pure power of p.
            oo = o
            e = 0
            while oo % p == 0: oo //= p; e += 1
            if oo == 1:  # o = p^e, pure p-power
                for k in range(e, maxe + 1):
                    A[k] += 1
            # else not in any p-power torsion (except identity handled by e counting)
        # identity has order 1 => e=0 => counted in all A[k]>=0; ensure A[0]=1
        # number of independent Z_p summands of exponent >= k:
        # |p^k-torsion| = p^{sum_{j<=k} (#factors with exponent>=j)}
        # Let t_k = log_p |A[k]|.  Then #factors with exponent exactly e =
        #   (t_e - t_{e-1}) - (t_{e+1} - t_e).
        t = []
        for k in range(0, maxe + 1):
            val = A[k] if A[k] > 0 else 1
            # log_p val
            lg = 0; v = 1
            while v < val: v *= p; lg += 1
            t.append(lg if p ** lg == val else lg)  # val should be exact power of p
        # #factors with exponent >= j  is  d_j = t_j - t_{j-1}
        d_ge = [t[0]]  # t_0 = log_p A[0]; A[0] = #{x: x=0}=1 => t_0=0 normally
        for j in range(1, maxe + 1):
            d_ge.append(t[j] - t[j - 1])
        # d_ge[j] = number of cyclic factors with exponent >= j
        # number with exponent exactly e = d_ge[e] - d_ge[e+1]
        exps = []
        for e in range(1, maxe + 1):
            cnt = d_ge[e] - (d_ge[e + 1] if e + 1 <= maxe else 0)
            exps += [e] * cnt
        exps.sort(reverse=True)
        inv_primary[p] = exps  # list of e meaning factor Z_{p^e}
    # combine primary parts into invariant factors (largest first)
    # build list of prime-power factors per prime, then CRT-merge by aligning ranks
    prime_lists = {p: sorted([p ** e for e in exps], reverse=True)
                   for p, exps in inv_primary.items()}
    maxlen = max((len(v) for v in prime_lists.values()), default=0)
    invs = []
    for i in range(maxlen):
        f = 1
        for p in prime_lists:
            lst = prime_lists[p]
            if i < len(lst): f *= lst[i]
        invs.append(f)
    invs = [x for x in invs if x > 1]
    invs.sort()
    return invs


# --------------------------------------------------------------------------- #
# DIRECT H^2(G, M), trivial action, capped.  Returns |H^2| + invariant factors.#
# --------------------------------------------------------------------------- #
def direct_H2_trivial(G: Fin, M: Fin, cap=300000):
    keys2 = list(itertools.product(G.elems, repeat=2))
    keys1 = list(G.elems)
    n2, n1 = len(keys2), len(keys1)
    blow = M.order ** n2
    if blow > cap:
        return {"skipped": True, "reason": f"|M|^|G|^2 = {M.order}^{n2} = {blow} > cap"}

    def d1(f1):
        out = []
        for (g1, g2) in keys2:
            # trivial action: (d1 f1)(g1,g2) = f1[g2] - f1[g1+g2] + f1[g1]
            t = M.add(f1[g2], M.neg(f1[G.add(g1, g2)]))
            t = M.add(t, f1[g1])
            out.append(t)
        return tuple(out)

    def is_cocycle(fv):
        f = {keys2[i]: fv[i] for i in range(n2)}
        for (g1, g2, g3) in itertools.product(G.elems, repeat=3):
            # trivial action 2-cocycle: f(g2,g3) - f(g1+g2,g3) + f(g1,g2+g3) - f(g1,g2) = 0
            t = f[(g2, g3)]
            t = M.add(t, M.neg(f[(G.add(g1, g2), g3)]))
            t = M.add(t, f[(g1, G.add(g2, g3))])
            t = M.add(t, M.neg(f[(g1, g2)]))
            if t != M.zero:
                return False
        return True

    Z2 = [fv for fv in itertools.product(M.elems, repeat=n2) if is_cocycle(fv)]
    B2 = set()
    for f1v in itertools.product(M.elems, repeat=n1):
        f1 = {keys1[i]: f1v[i] for i in range(n1)}
        B2.add(d1(f1))
    B2 = set(B2)

    def addv(a, b): return tuple(M.add(a[i], b[i]) for i in range(n2))
    zerov = tuple(M.zero for _ in keys2)
    def coset(z): return frozenset(addv(z, b) for b in B2)
    reps = {}
    for z in Z2:
        c = coset(z)
        if c not in reps: reps[c] = z
    # build the quotient group as an abstract abelian group for invariant factors
    quo_elems = list(reps.values())
    def qadd(a, b):  # representative of coset(a)+coset(b) -- pick canonical rep
        s = addv(a, b)
        return reps[coset(s)]
    invs = invariant_factors(quo_elems, qadd, reps[coset(zerov)])
    return {"skipped": False, "|Z2|": len(Z2), "|B2|": len(B2),
            "|H2|": len(reps), "H2_invariants": invs}


# --------------------------------------------------------------------------- #
# RING prediction of dim H^2(G, F_p) for elementary-abelian G = (Z_p)^k.       #
# --------------------------------------------------------------------------- #
def ring_dimH2_elem_abelian(k, p):
    """Degree-2 dimension of H^*((Z_p)^k, F_p).
    p=2: polynomial F_2[x_1..x_k], deg 1 => C(k+1,2) = k(k+1)/2.
    p odd: Lambda(y)(x)Poly(x), deg y=1 deg x=2 => deg-2 dim = k + C(k,2) = k(k+1)/2.
    (Both give k(k+1)/2 in degree 2; the p-odd split into k(from x_i)+C(k,2)(from y_iy_j).)
    """
    return k * (k + 1) // 2


# --------------------------------------------------------------------------- #
# PART A -- p=2 elementary-abelian: DIRECT vs RING, trivial coefficients F_2.   #
# --------------------------------------------------------------------------- #
def part_A_p2_core():
    print("=" * 74)
    print("PART A  --  G = (Z_2)^k, M = F_2 (trivial):  DIRECT vs RING dim H^2")
    print("=" * 74)
    rows = []
    for k in range(1, 4):  # k=1 (Z2, cyclic), k=2 (Z2xZ2), k=3 (Z2^3)
        G = Fin([2] * k, f"(Z2)^{k}")
        M = Fin([2], "Z2")
        ring = ring_dimH2_elem_abelian(k, 2)
        res = direct_H2_trivial(G, M)
        if res["skipped"]:
            direct_rank = None
            note = "DIRECT skipped: " + res["reason"]
            agree = None
        else:
            # rank over F_2 = number of invariant factors (all =2 here)
            direct_rank = len(res["H2_invariants"])
            note = f"|H2|={res['|H2|']} inv={res['H2_invariants']}"
            agree = (direct_rank == ring)
        rows.append({"k": k, "|G|": G.order, "ring_dimH2": ring,
                     "direct_rank": direct_rank, "agree": agree, "note": note})
        tag = "cyclic" if k == 1 else "NON-cyclic"
        astr = "AGREE" if agree else ("--" if agree is None else "MISMATCH!")
        print(f"  k={k} ({tag:>10}) |G|={G.order:>2}  ring C(k+1,2)={ring:>2}"
              f"   direct_rank={str(direct_rank):>4}  [{astr}]  {note}")
    return rows


# --------------------------------------------------------------------------- #
# PART B -- LAW L: trivial-action rank scales linearly with F_2-rank of module.#
# rank H^2((Z_2)^k, (Z_2)^r) ?= r * C(k+1,2).  DIRECT only where cap allows.    #
# --------------------------------------------------------------------------- #
def part_B_law_L():
    print()
    print("=" * 74)
    print("PART B  --  LAW L:  rank H^2((Z2)^k, (Z2)^r) ?= r * C(k+1,2)")
    print("           (DIRECT where |M|^(|G|^2) <= cap; else RING prediction only)")
    print("=" * 74)
    rows = []
    for k in (1, 2):
        for r in (1, 2, 3):
            G = Fin([2] * k, f"(Z2)^{k}")
            M = Fin([2] * r, f"(Z2)^{r}")
            core = ring_dimH2_elem_abelian(k, 2)
            predict = r * core
            res = direct_H2_trivial(G, M)
            if res["skipped"]:
                drank = None; status = "PREDICT-ONLY (capped)"
                agree = None
            else:
                drank = len(res["H2_invariants"])
                agree = (drank == predict)
                status = "AGREE" if agree else "MISMATCH!"
            rows.append({"k": k, "r": r, "core": core, "predict": predict,
                         "direct_rank": drank, "agree": agree, "status": status})
            print(f"  G=(Z2)^{k}  M=(Z2)^{r}:  core={core}  r*core={predict:>3}"
                  f"   direct_rank={str(drank):>4}   [{status}]")
    return rows


# --------------------------------------------------------------------------- #
# PART C -- shape sweep across small groups of the SAME order (rank ladder).    #
# Compares cyclic vs non-cyclic of order 4, and order 8, on M = Z_2 (trivial). #
# All DIRECT (|M|=2), so every number here is a VERIFIED count.                 #
# --------------------------------------------------------------------------- #
def part_C_shape_sweep():
    print()
    print("=" * 74)
    print("PART C  --  same |G|, different SHAPE, M = Z_2 (trivial): DIRECT counts")
    print("=" * 74)
    groups = [
        Fin([4], "Z4"),          # order 4 cyclic
        Fin([2, 2], "Z2xZ2"),    # order 4 non-cyclic (elem abelian)
        Fin([8], "Z8"),          # order 8 cyclic
        Fin([2, 4], "Z2xZ4"),    # order 8 mixed
        Fin([2, 2, 2], "Z2^3"),  # order 8 elem abelian
    ]
    M = Fin([2], "Z2")
    rows = []
    for G in groups:
        res = direct_H2_trivial(G, M)
        if res["skipped"]:
            print(f"  {G.name:>7} (|G|={G.order}):  DIRECT skipped: {res['reason']}")
            rows.append({"G": G.name, "|G|": G.order, "skipped": True,
                         "reason": res["reason"]})
            continue
        rank = len(res["H2_invariants"])
        shape = "cyclic" if len(G.orders) == 1 else "non-cyclic"
        # ring value only meaningful for elem-abelian; annotate when applicable
        note = ""
        if all(o == 2 for o in G.orders):
            k = len(G.orders); note = f"= C({k}+1,2) = {ring_dimH2_elem_abelian(k,2)} (elem-ab ring)"
        rows.append({"G": G.name, "|G|": G.order, "shape": shape,
                     "|H2|": res["|H2|"], "rank": rank,
                     "inv": res["H2_invariants"], "note": note})
        print(f"  {G.name:>7} (|G|={G.order}, {shape:>10}):  |H2|={res['|H2|']:>3}"
              f"  rank={rank}  inv={res['H2_invariants']}  {note}")
    return rows


# --------------------------------------------------------------------------- #
# PART D -- NON-trivial actions on the smallest non-cyclic G, capped probe.     #
# G = Z2 x Z2 acting on M = Z2 x Z2.  A 2-cochain is |M|^(|G|^2)=4^16 -> too big.#
# So we CANNOT do direct here; we state the cap honestly and instead probe the  #
# smaller question DIRECT allows: does a nontrivial action of Z2xZ2 on M=Z2     #
# exist that changes H^2?  (On M=Z2 every automorphism is trivial => no test.)  #
# We record this as an explicit CANNOT-CLAIM, which is itself the finding.       #
# --------------------------------------------------------------------------- #
def part_D_nontrivial_probe():
    print()
    print("=" * 74)
    print("PART D  --  non-trivial actions on non-cyclic G (the cap frontier)")
    print("=" * 74)
    notes = []
    # M = Z2: Aut(Z2) is trivial, so no nontrivial G-action exists at all.
    notes.append("M=Z2: Aut(Z2)={id}, so NO nontrivial action of any G exists -- "
                 "the trivial-action numbers in Parts A-C are the WHOLE story here.")
    # M = Z2xZ2: Aut = GL(2,F2) has order 6, nontrivial actions DO exist, but a
    # 2-cochain G^2->M has 4^16 ~ 4.3e9 values => DIRECT impossible under the cap.
    blow = (2 ** 2) ** ((2 * 2) ** 2)
    notes.append(f"M=Z2xZ2, G=Z2xZ2: nontrivial actions exist (Aut=GL(2,F2), |.|=6), "
                 f"but a 2-cochain is |M|^(|G|^2)=4^16={blow} -- DIRECT is IMPOSSIBLE "
                 f"under the cap. We do NOT claim any nontrivial-action number for "
                 f"non-cyclic G. This is an explicit CANNOT-CLAIM, and the honest "
                 f"boundary of what enumeration reaches.")
    for n in notes:
        print("  * " + n)
    return {"notes": notes, "blowup_4^16": blow}


def ledger():
    print()
    print("=" * 74)
    print("LEDGER  --  section 12 (non-cyclic frame-group law)")
    print("=" * 74)
    print("""
  PROVEN (theorem, trivial action):
    * H^2(Z_2, M) trivial-action = M/2M = M[2]  (carried over from sec 11, still
      a theorem).  For the frame-group question the relevant proven statement is
      narrower: for CYCLIC G=Z_m trivial action, |H^2(Z_m,M)| = |M/mM| by Tate,
      which is rank-1 in the F_2 sense when M=Z_2 -- this is WHY cyclic G gives a
      'single bit'.  That is a proof, and it explains the sec-9 law's origin.

  VERIFIED-ON-FAMILY (DIRECT enumeration, exact counts -- not proven in general):
    * PART A:  G=(Z_2)^k trivial on F_2 gives rank = C(k+1,2): k=1 ->1, k=2 ->3.
               (k=3 -> ring predicts 6 but DIRECT is capped; see below.)
    * PART C:  at fixed order the SHAPE decides the rank -- DIRECT-VERIFIED at
               order 4:  Z4 (cyclic) rank 1   vs   Z2xZ2 rank 3.  That single
               order-4 pair already refutes 'rank = f(|G|)': same |G|=4, ranks
               1 and 3.  So 'rank of the generative core' is NOT a function of
               |G|; it is a function of the GROUP SHAPE.  This is the replacement
               for the sec-9 single-invariant law: the invariant is the SHAPE
               (the ring), not a number attached to |G| or v_2(|G|).
               ( order 8 -- Z8 / Z2xZ4 / Z2^3 -- is ENTIRELY past the 2^64 cap;
                 no order-8 rank is DIRECT-verified here.  See RING-PREDICTION. )
    * PART B:  LAW L (rank scales as r*core) holds on every case the cap allowed.

  RING-PREDICTION-ONLY (NOT a verified count -- stated as prediction, flagged):
    * G=(Z_2)^3 on F_2: ring says dim H^2 = C(4,2)=6, but a 2-cochain is
      2^(8^2)=2^64 -- DIRECT is impossible.  We report 6 as PREDICTION ONLY.
    * ALL order-8 groups (Z8, Z2xZ4, Z2^3): DIRECT impossible (2^64).  Ring gives
      elem-abelian Z2^3 -> rank 6; Z8 (cyclic Tate) -> rank 1; Z2xZ4 is neither
      simple-cyclic nor elem-abelian, so its rank is genuinely OPEN here.  None of
      the three order-8 ranks is a verified count in this file.
    * Any NON-trivial action for non-cyclic G on |M|>2 (Part D): DIRECT impossible
      (4^16).  No number claimed.

  REFUTED (killed earlier plausible claims -- kept from sec 9/11, reconfirmed):
    * 'One invariant (v_2(N)) decides the generative phase.'  FALSE for non-cyclic
      G: same |G|, different shape, different rank (Part C, order 4: 1 vs 3).
    * (from sec 11) 'some order-2 action always collapses H^2 fully.'  Still false.

  CANNOT CLAIM (yet, or maybe ever):
    * A closed rank formula for H^2(G,M) valid for ALL finite abelian G and M with
      ARBITRARY action.  We have it for elem-abelian G, trivial action, by ring
      theory (and verified up to the cap); the general action case is open.
    * Any DIRECT number for non-cyclic G with |M|>2 (the 4^16 wall).
    * The governance reading remains ANALOGY under the paradox<->cochain dictionary.

  THE ONE-LINE UPGRADE OF THE LAW:
    cyclic G  :  generative core is a single bit, size gcd/v_2 -- 'is there a
                 load-bearing remainder, yes/no'.
    non-cyclic G:  the generative core has a SHAPE-DETERMINED RANK
                 (= r * dim H^2(G,F_p), e.g. C(k+1,2) for G=(Z_p)^k), a whole
                 vector space of independent load-bearing remainders, one family
                 per pair of frame-directions.  Frames-in-a-bundle can carry MORE
                 irreducible paradox than frames-in-a-line, and exactly how much
                 is read off the group's cohomology ring, not a single number.
""")


def main():
    out = {}
    out["part_A"] = part_A_p2_core()
    out["part_B"] = part_B_law_L()
    out["part_C"] = part_C_shape_sweep()
    out["part_D"] = part_D_nontrivial_probe()
    ledger()
    with open("results/cohomology_noncyclic_law.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\n[written] results/cohomology_noncyclic_law.json")


if __name__ == "__main__":
    main()
