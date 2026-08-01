#!/usr/bin/env python3
"""
SECTION 14 PART 1 driver.  Validate the generic resolution engine, then test
whether the two sec-13 structural facts survive bigger/mixed frame-bundles
G = Z2xZ2xZ2 and G = Z4xZ2.
"""
from __future__ import annotations
import itertools, json, os
import numpy as np
from cohomology_bigger import Resolution, GModule, H2, GroupRing

os.makedirs("results", exist_ok=True)


# --------------------------------------------------------------------------- #
# LHS / iterated-Kunneth associated-graded prediction of H^2(G,M), trivial      #
# action, for G = product of Z2's (elementary abelian) and for Z4xZ2.           #
# We compute H^*(Z_m, M) layer by layer (trivial action):                        #
#   H^0(Z_m,M)=M ; H^{odd}(Z_m,M)=M[m]=ker(mult m)  ; but for our purposes we    #
#   only need it as a MODULE to feed the next layer, and for m=2 both odd and    #
#   even (>=1) layers equal the group M/2M ~= M[2] (order gcd(2,.) per factor).  #
# For a clean independent check we restrict LHS-check to the ELEMENTARY-ABELIAN  #
# groups (all m=2), where H^q(Z2,N) alternates N/2N (even) and N[2] (odd), both  #
# = the 2-torsion-shaped group.  For Z4xZ2 the LHS layers differ (Z4 has         #
# H^{odd}=M[4]/... ), so we DO NOT claim an LHS number there and instead trust   #
# the engine via its d^2=0 self-check + agreement on the Z2^k family.            #
# --------------------------------------------------------------------------- #
def factors(orders):
    return [o for o in orders if o > 1]

def twotorsion_shape(orders):
    """orders of M[2] = M/2M for a product module (each factor -> gcd(2,o))."""
    return [ (2 if o % 2 == 0 else 1) for o in orders ]

def Hq_Z2(orders, q):
    if q == 0: return factors(orders)
    return factors(twotorsion_shape(orders))   # both parities are the 2-torsion shape

def lhs_H2_elem_abelian(orders_M, kfactors):
    """H^2(G,M) assoc-graded for G=(Z2)^kfactors, trivial action, iterated Kunneth.
    Contributions to total degree 2 = sum over compositions (q_1..q_k) with sum=2.
    We iterate: start module N0=M; after applying factor with degree q it becomes
    H^q(Z2,N).  Enumerate all degree-distributions across k factors summing to 2."""
    contrib = []
    # distributions of total degree 2 among k factors
    for dist in itertools.product(range(3), repeat=kfactors):
        if sum(dist) != 2: continue
        N = list(orders_M)
        for q in dist:
            N = Hq_Z2(N, q)
        contrib += N
    return sorted(contrib)


def part_A_validate():
    print("=" * 74)
    print("PART A  --  validate the generic engine")
    print("=" * 74)
    # (1) reproduce sec-13 Z2xZ2 numbers exactly
    res22 = Resolution([2, 2])
    print("  G=Z2xZ2 complex d^2=0:", res22.verify_complex(4))
    checks = [
        ("Z2",    [2],    [[[1]]], ),
    ]
    # trivial action on a few modules, compare to LHS elem-abelian prediction
    print("  -- G = Z2xZ2 (k=2), trivial action: engine vs LHS assoc-graded --")
    ok_all = True
    for name, orders in [("Z2",[2]),("Z4",[4]),("Z2xZ2",[2,2]),("Z2xZ4",[2,4]),("Z4xZ4",[4,4])]:
        k = len(orders); I = np.eye(k, dtype=np.int64)
        M = GModule(orders, [I, I], [2, 2], name+"(triv)")
        r = H2(res22, M)
        lhs = lhs_H2_elem_abelian(orders, 2)
        match = (r["H2_invariants"] == lhs)
        ok_all &= match
        print(f"     M={name:>6}: engine inv={r['H2_invariants']}  LHS inv={lhs}  "
              f"[{'MATCH' if match else 'MISMATCH!'}]")
    print("  engine == LHS on Z2xZ2 family:", ok_all)
    return ok_all


def all_order_dividing_actions(orders_M, factor_order):
    """All automorphism matrices A of M with A^{factor_order} = I (mod orders),
    A a valid module hom and a bijection.  Deduplicated by action signature."""
    k = len(orders_M)
    elems = list(itertools.product(*[range(o) for o in orders_M]))
    maxentry = max(orders_M)
    def valid_hom(mat):
        return all((orders_M[j]*mat[i][j]) % orders_M[i] == 0 for i in range(k) for j in range(k))
    def apply(mat, x):
        return tuple(int(sum(mat[i][j]*x[j] for j in range(k))) % orders_M[i] for i in range(k))
    def is_bij(mat):
        return len(set(apply(mat, x) for x in elems)) == len(elems)
    def order_divides(mat):
        # A^{factor_order} == I on all elems
        for x in elems:
            y = x
            for _ in range(factor_order):
                y = apply(mat, y)
            if y != x: return False
        return True
    autos = {}
    for flat in itertools.product(range(maxentry), repeat=k*k):
        mat = [[flat[i*k+j] for j in range(k)] for i in range(k)]
        if not valid_hom(mat): continue
        if not is_bij(mat): continue
        if not order_divides(mat): continue
        sig = tuple(apply(mat, x) for x in elems)
        if sig not in autos: autos[sig] = mat
    return list(autos.values()), elems


def part_B_bigger(res, orders_G, gname, modules, cap=2_000_000):
    """For each module, enumerate commuting tuples of per-factor actions (each of
    order dividing the factor order) and compute H^2 for each -> rank spectrum.
    Reports whether (i) trivial maximizes and (ii) a floor exists."""
    print()
    print("=" * 74)
    print(f"PART B  --  G = {gname}  (frame-bundle), structural facts test")
    print("=" * 74)
    R = res.R
    out = {}
    for name, orders in modules:
        k = len(orders)
        # per-factor candidate actions: order dividing m_r
        cand = []
        for m in orders_G:
            autos, elems = all_order_dividing_actions(orders, m)
            cand.append(autos)
        # all tuples of per-factor actions that pairwise commute (as maps)
        def apply(mat, x):
            return tuple(int(sum(mat[i][j]*x[j] for j in range(k))) % orders[i] for i in range(k))
        def commute(A, B):
            return all(apply(A, apply(B, x)) == apply(B, apply(A, x)) for x in elems)
        tuples = []
        for combo in itertools.product(*cand):
            good = True
            for a in range(len(combo)):
                for b in range(a+1, len(combo)):
                    if not commute(combo[a], combo[b]):
                        good = False; break
                if not good: break
            if good:
                tuples.append(combo)
        # compute H2 spectrum
        spectrum = {}; triv_inv = None; skipped = 0
        I = np.eye(k, dtype=np.int64)
        def is_identity(mat):
            return all(apply(mat, x) == x for x in elems)
        for combo in tuples:
            try:
                M = GModule(orders, [np.array(a, dtype=np.int64) for a in combo], orders_G, name)
            except AssertionError:
                continue
            r = H2(res, M, cap=cap)
            if r.get("skipped"):
                skipped += 1; continue
            invt = tuple(r["H2_invariants"])
            spectrum[invt] = spectrum.get(invt, 0) + 1
            if all(is_identity(a) for a in combo):
                triv_inv = invt
        if not spectrum:
            print(f"  M={name:>6}: ALL {len(tuples)} actions skipped (|C2|>cap)  -- cannot report")
            out[name] = {"orders": orders, "n_actions": len(tuples), "all_skipped": True}
            continue
        ranks = sorted(set(len(t) for t in spectrum))
        triv_rank = len(triv_inv) if triv_inv is not None else None
        maxr = max(ranks); minr = min(ranks)
        fact_i = (triv_rank == maxr) if triv_rank is not None else None
        print(f"  M={name:>6} ({len(tuples)} commuting action-tuples, {skipped} skipped):")
        print(f"     trivial rank = {triv_rank}   rank range = {minr}..{maxr}")
        for invt in sorted(spectrum, key=lambda t: (len(t), t)):
            print(f"        rank {len(invt):>1}  inv={str(list(invt)):>26} : {spectrum[invt]} actions")
        print(f"     FACT (i) trivial maximizes rank? {fact_i}"
              f"    FACT (ii) floor (min>0)? {minr > 0} (min rank {minr})")
        out[name] = {"orders": orders, "n_actions": len(tuples), "skipped": skipped,
                     "trivial_rank": triv_rank, "rank_min": minr, "rank_max": maxr,
                     "fact_i_trivial_maximizes": bool(fact_i) if fact_i is not None else None,
                     "spectrum": {str(list(k)): v for k, v in spectrum.items()}}
    return out


def main():
    out = {}
    out["validate_ok"] = part_A_validate()

    # G = Z2xZ2xZ2 : r2 = 6, so |C2| = |M|^6. Keep |M| small: Z2 (64), Z2xZ2 (4096),
    # Z4 (4096), Z2xZ2xZ2 (2^18 too big -> capped).
    res222 = Resolution([2, 2, 2])
    out["Z2xZ2xZ2"] = part_B_bigger(
        res222, [2, 2, 2], "Z2xZ2xZ2",
        [("Z2", [2]), ("Z4", [4]), ("Z2xZ2", [2, 2])], cap=2_000_000)

    # G = Z4xZ2 : r2 = 3, |C2|=|M|^3. Modules up to Z4xZ4 (16^3=4096) fine.
    res42 = Resolution([4, 2])
    out["Z4xZ2"] = part_B_bigger(
        res42, [4, 2], "Z4xZ2",
        [("Z2", [2]), ("Z4", [4]), ("Z2xZ2", [2, 2]), ("Z2xZ4", [2, 4]), ("Z4xZ4", [4, 4])],
        cap=2_000_000)

    with open("results/cohomology_bigger.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\n[written] results/cohomology_bigger.json")


if __name__ == "__main__":
    main()
