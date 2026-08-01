#!/usr/bin/env python3
"""
Find the EXACT combinatorial collapse invariant for H^2(Z2, M), M a finite
abelian 2-group, over ALL involutions u.  We already have the exact oracle
(min |H^2| over involutions == 1  <=>  collapse) from cohomology_prove.py.
Here we mine the exhaustive data for the true rule on the exponent multiset,
testing several candidate predicates against the oracle.

We enumerate every 2-group M = Z_{2^{a1}} x ... (invariant-factor form,
a1<=...<=ak) within a cost cap, compute the oracle, and score candidates.
"""
import itertools, json
from functools import reduce
from collections import Counter

from cohomology_prove import (elements, enumerate_involutions, H2_order,
                              even_exponents, v2)

def oracle_collapses(orders):
    invs = enumerate_involutions(orders)
    return min(H2_order(orders, A) for A in invs) == 1

# ---- candidate predicates on the exponent multiset E = sorted exps ----

def cand_A_all_pairable(E):
    """P3: every exponent has even multiplicity."""
    return all(m % 2 == 0 for m in Counter(E).values())

def cand_B_partition_pairs_or_deep(E):
    """previous P_partition: pair equal exps, leftover singletons must be >=3."""
    left = [e for e, m in Counter(E).items() if m % 2 == 1]
    return all(e >= 3 for e in left)

def cand_C_no_isolated_shallow_min(E):
    """Hypothesis: collapse fails iff there is an UNPAIRED exponent that is the
    unique minimum and is shallow.  Try: the number of odd-multiplicity classes
    that are 'not coverable'."""
    # coverable if you can pair unequal exps by the 'staircase' rule:
    # an exponent a can be absorbed by a strictly larger exponent b>a (the
    # larger cyclic factor's norm map covers the smaller fixed part).
    # Greedy: sort exps; repeatedly pair equal, else absorb a smaller into a
    # strictly larger; a value with v2>=3 can self-absorb (deep channel).
    exps = sorted(E)
    remaining = exps[:]
    changed = True
    while changed:
        changed = False
        c = Counter(remaining)
        # remove equal pairs
        for e, m in list(c.items()):
            if m >= 2:
                c[e] -= 2
                if c[e] == 0: del c[e]
                remaining = list(c.elements())
                changed = True
                break
        if changed: continue
        # self-absorb a deep singleton
        for e in sorted(c):
            if e >= 3:
                c[e] -= 1
                if c[e] == 0: del c[e]
                remaining = list(c.elements())
                changed = True
                break
        if changed: continue
        # absorb a smaller into a strictly larger (norm of the larger factor
        # surjects onto the fixed part of the smaller)
        keys = sorted(c)
        if len(keys) >= 2:
            a, b = keys[0], keys[-1]
            if b > a:
                c[a] -= 1; c[b] -= 1
                if c[a] == 0: del c[a]
                if b in c and c[b] == 0: del c[b]
                remaining = list(c.elements())
                changed = True
    return len(remaining) == 0

def cand_D_pairs_or_any_deep_present_and_rest_pairs(E):
    """collapse iff after removing equal-pairs, the leftover set is either empty
    or consists ENTIRELY of values, at least one of which is >=3 AND the count
    of leftovers is ... (try: leftovers all absorbable = at most one shallow if a
    deep exists)."""
    left = sorted(e for e, m in Counter(E).items() if m % 2 == 1)
    if not left: return True
    # if there is any deep (>=3) leftover, it can pull in one shallow partner
    deeps = [e for e in left if e >= 3]
    shallows = [e for e in left if e < 3]
    # each deep can absorb itself and optionally one shallow; each pair of
    # shallows already removed. So collapse iff #shallows <= #deeps.
    return len(shallows) <= len(deeps)

def main():
    # exhaustive over 2-groups, cost-capped
    mods = []
    for k in range(1, 4):
        for combo in itertools.combinations_with_replacement(range(1, 5), k):
            orders = [2**a for a in combo]
            search = reduce(lambda x, y: x*y, orders, 1) ** k
            elem = reduce(lambda x, y: x*y, orders, 1)
            if search > 300000 or elem > 512:
                continue
            mods.append(orders)

    cands = {
        "A_P3_all_pairable": cand_A_all_pairable,
        "B_pairs_or_deep_leftover": cand_B_partition_pairs_or_deep,
        "C_staircase_absorb": cand_C_no_isolated_shallow_min,
        "D_shallows_le_deeps": cand_D_pairs_or_any_deep_present_and_rest_pairs,
    }
    scores = {k: 0 for k in cands}
    rows = []
    for orders in mods:
        E = even_exponents(orders)
        obs = oracle_collapses(orders)
        row = {"orders": orders, "E": E, "collapse": obs}
        for name, fn in cands.items():
            pred = fn(E)
            row[name] = pred
            if pred == obs:
                scores[name] += 1
        rows.append(row)
    n = len(rows)

    print("modules tested:", n)
    for name in cands:
        print("  %-26s %d/%d" % (name, scores[name], n))
    print()
    # show the exact table with any misses of the best candidate
    best = max(scores, key=scores.get)
    print("BEST:", best, "%d/%d" % (scores[best], n))
    for r in rows:
        flags = " ".join("%s=%s" % (k[0], "T" if r[k] else "F") for k in cands)
        miss = "" if r[best] == r["collapse"] else "   <<< %s MISS" % best
        print("  %-16s E=%-14s collapse=%-5s  %s%s" %
              (str(r["orders"]), str(r["E"]), r["collapse"], flags, miss))

    out = {"n": n, "scores": scores, "best": best, "rows": rows}
    with open("results/cohomology_invariant_search.json", "w") as f:
        json.dump(out, f, indent=2)

if __name__ == "__main__":
    main()
