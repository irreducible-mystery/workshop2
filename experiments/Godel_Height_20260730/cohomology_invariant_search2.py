#!/usr/bin/env python3
"""
Second pass: instead of guessing a predicate, DERIVE the min |H^2| over
involutions as an exact function of the exponent multiset, by regression over
the exhaustive oracle data.  Then read off the collapse (min|H^2|=1) rule.

Key structural fact we will confirm: for a SINGLE cyclic factor Z_{2^a} the
Tate cohomology over involutions is
    a=1: |H^2| in {2}           (only u=+1; -1==+1 on Z2)   -> floor 2
    a=2: |H^2| in {2}           (u=+-1)                     -> floor 2
    a>=3:|H^2| in {1,2}         (u=+-1, and u=2^{a-1}+-1)   -> collapses (deep)
For PRODUCTS the norm map couples factors.  We tabulate min|H^2| and fit.
"""
import itertools, json
from functools import reduce
from collections import Counter

from cohomology_prove import (enumerate_involutions, H2_order,
                              even_exponents, v2)

def min_h2(orders):
    invs = enumerate_involutions(orders)
    return min(H2_order(orders, A) for A in invs)

def all_h2(orders):
    invs = enumerate_involutions(orders)
    return sorted({H2_order(orders, A) for A in invs})

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

    rows = []
    for orders in mods:
        E = even_exponents(orders)
        c = Counter(E)
        mh = min_h2(orders)
        rows.append({"orders": orders, "E": E, "min_h2": mh,
                     "all_h2": all_h2(orders)})

    # --- CANDIDATE for collapse, refined from the data:
    # A single unpaired SHALLOW exponent (1 or 2) can only be absorbed if there
    # is a STRICTLY DEEPER factor (exp >= that+? ) to couple it to, OR it can be
    # paired with an equal exponent.  Precisely, model the norm map contribution
    # per exponent level and test:
    #
    #   collapse  <=>  for every value m, the exponents can be arranged so that
    #                  each Z_{2^a} factor's fixed part is covered.
    #
    # After inspection the exact rule turns out to be about the SMALLEST
    # exponent's multiplicity parity coupled to whether a deeper factor exists.
    # Test the clean guess:
    #   E collapses  <=>  we can delete E to empty by the moves:
    #     (P) remove two EQUAL exponents            (hyperbolic pair)
    #     (S) remove a SINGLE exponent >= 3         (deep self-collapse)
    #     (C) remove a pair (a, b) with a < b AND b >= 3   (deep factor absorbs a
    #         strictly-shallower one; requires the ABSORBER be deep >=3)
    def collapses_pred(E):
        c = Counter(E)
        rem = list(c.elements())
        changed = True
        while changed:
            changed = False
            c = Counter(rem)
            # (P) equal pair
            for e, m in list(c.items()):
                if m >= 2:
                    c[e]-=2
                    if c[e]==0: del c[e]
                    rem=list(c.elements()); changed=True; break
            if changed: continue
            # (S) deep singleton
            for e in sorted(c, reverse=True):
                if e>=3:
                    c[e]-=1
                    if c[e]==0: del c[e]
                    rem=list(c.elements()); changed=True; break
            if changed: continue
            # (C) deep absorbs a strictly-shallower one
            keys=sorted(c)
            done=False
            for bi in range(len(keys)-1,-1,-1):
                b=keys[bi]
                if b>=3 and c[b]>=1:
                    for a in keys:
                        if a<b and c[a]>=1:
                            c[a]-=1; c[b]-=1
                            if c[a]==0: del c[a]
                            if c.get(b,0)==0 and b in c: del c[b]
                            rem=list(c.elements()); changed=True; done=True; break
                if done: break
        return len(rem)==0

    n=len(rows); hits=0
    print("E                collapse  pred   min|H2|")
    for r in rows:
        obs = (r["min_h2"]==1)
        pred = collapses_pred(r["E"])
        ok = (obs==pred)
        hits += ok
        print("  %-14s %-8s %-6s %d   %s" %
              (str(r["E"]), obs, pred, r["min_h2"], "" if ok else "<<< MISS"))
    print("\nrefined predicate agreement: %d/%d" % (hits, n))

    out={"n":n,"agreement":[hits,n],"rows":rows}
    with open("results/cohomology_invariant_search2.json","w") as f:
        json.dump(out,f,indent=2)

if __name__=="__main__":
    main()
