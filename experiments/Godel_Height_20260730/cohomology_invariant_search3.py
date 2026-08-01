#!/usr/bin/env python3
"""
Third pass -- stop guessing, DERIVE the collapse rule from the actual optimal
involution structure.  For each 2-group M we already have the exact oracle
min|H^2|.  Here we ALSO extract, for a min-achieving involution, its rational
canonical structure, and we fit a closed form for min|H^2| as a function of the
exponent multiset by a principled layer-by-layer (2-adic filtration) argument,
then TEST the resulting predicate exhaustively.

The layer argument: filter M by 2^j M.  On each layer the involution acts, and
|H^2| = |coker(1+u on M) restricted...|.  Empirically min|H^2| = 2^{f} where f
is the number of 'unpaired shallow slots'.  We compute f directly from the
oracle (f = log2 min|H^2|) and search for the closed form of f over E.
"""
import itertools, json, math
from functools import reduce
from collections import Counter

from cohomology_prove import (enumerate_involutions, H2_order, even_exponents)

def min_h2(orders):
    invs = enumerate_involutions(orders)
    return min(H2_order(orders, A) for A in invs)

def f_from_oracle(orders):
    mh = min_h2(orders)
    return int(round(math.log2(mh)))

def main():
    mods = []
    for k in range(1, 4):
        for combo in itertools.combinations_with_replacement(range(1, 5), k):
            orders = [2**a for a in combo]
            search = reduce(lambda x, y: x*y, orders, 1) ** k
            elem = reduce(lambda x, y: x*y, orders, 1)
            if search > 300000 or elem > 512:
                continue
            mods.append(orders)

    data = []
    for orders in mods:
        E = even_exponents(orders)
        f = f_from_oracle(orders)
        data.append((tuple(E), f))

    print("E                 f=log2 min|H2|")
    for E, f in data:
        print("  %-16s %d" % (str(list(E)), f))
    print()

    # ---- CLOSED-FORM HYPOTHESIS for f ----
    # From the table: f is 0 (collapse) or 1 (floor of order 2).  Never >1 in
    # this range.  So collapse <=> f==0.  The task is a clean boolean rule.
    #
    # DERIVED RULE (read off, then tested):  consider the exponents as a multiset.
    # Sort ascending.  A collapse-blocking 'defect' is created by the SMALLEST
    # exponent ONLY when it cannot be matched.  Matching moves, in order:
    #   1. two equal exponents annihilate       (hyperbolic pair)
    #   2. an exponent >=3 annihilates by itself (deep self-collapse)
    #   3. a value v is annihilated by ANY other value w != v with max(v,w)>=... ?
    # Retest a SHARPER move-3: a value v<3 can be annihilated by pairing with a
    # STRICTLY GREATER value (regardless of that value's depth), because the
    # larger cyclic factor's (1+u) image reaches the smaller factor's fixed line
    # through an off-diagonal (shear) involution.  Deep(>=3) values can ALSO
    # self-annihilate.  Only a leftover set of EQUAL shallow(<3) values with ODD
    # total count survives -- and actually a single shallow value alone survives.
    def rule(E):
        c = Counter(E)
        rem = sorted(c.elements())
        changed = True
        while changed:
            changed = False
            c = Counter(rem)
            keys = sorted(c)
            # move 1: equal pair
            for e in keys:
                if c[e] >= 2:
                    c[e] -= 2
                    rem = sorted(c.elements()); changed = True; break
            if changed: continue
            # move 3: pair a smaller with a strictly larger (shear), ANY depth
            keys = sorted(k for k in c if c[k] > 0)
            if len(keys) >= 2:
                a, b = keys[0], keys[-1]   # smallest and largest, a<b
                c[a] -= 1; c[b] -= 1
                rem = sorted(e for e in c.elements()); changed = True; continue
            # move 2: deep self-collapse of a lone value
            keys = sorted(k for k in c if c[k] > 0)
            if len(keys) == 1:
                e = keys[0]
                if e >= 3:
                    c[e] -= 1
                    rem = sorted(c.elements()); changed = True; continue
        return len(rem) == 0   # True => collapse

    n = len(data); hits = 0
    print("E                 collapse  rule   ")
    for E, f in data:
        obs = (f == 0)
        pred = rule(list(E))
        ok = obs == pred
        hits += ok
        print("  %-16s %-8s %-6s %s" % (str(list(E)), obs, pred, "" if ok else "<<< MISS"))
    print("\nSHARPER RULE agreement: %d/%d" % (hits, n))

    out = {"n": n, "agreement": [hits, n],
           "data": [{"E": list(E), "f": f} for E, f in data]}
    with open("results/cohomology_invariant_search3.json", "w") as fp:
        json.dump(out, fp, indent=2)

if __name__ == "__main__":
    main()
