#!/usr/bin/env python3
"""
Fourth pass -- brute-search a large battery of clean arithmetic predicates on
the exponent multiset E against the exact oracle, and report EVERY predicate
that scores 21/21.  No hand-guessing; let the data pick the invariant.
"""
import itertools, json, math
from functools import reduce
from collections import Counter

from cohomology_prove import enumerate_involutions, H2_order, even_exponents

def min_h2(orders):
    invs = enumerate_involutions(orders)
    return min(H2_order(orders, A) for A in invs)

def build():
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
        E = tuple(even_exponents(orders))
        collapse = (min_h2(orders) == 1)
        data.append((E, collapse))
    return data

def features(E):
    c = Counter(E)
    k = len(E)                      # number of even factors (2-rank)
    m0 = min(E) if E else 0         # smallest exponent
    mult_m0 = c[m0] if E else 0     # multiplicity of the smallest
    n_deep = sum(1 for e in E if e >= 3)
    n_shallow = sum(1 for e in E if e < 3)   # exps 1 or 2
    n_odd_mult = sum(1 for e, mm in c.items() if mm % 2 == 1)
    distinct = len(c)
    sum_e = sum(E)
    max_e = max(E) if E else 0
    n1 = c.get(1, 0); n2 = c.get(2, 0)
    return dict(k=k, m0=m0, mult_m0=mult_m0, n_deep=n_deep, n_shallow=n_shallow,
                n_odd_mult=n_odd_mult, distinct=distinct, sum_e=sum_e,
                max_e=max_e, n1=n1, n2=n2)

def main():
    data = build()
    n = len(data)

    # candidate boolean predicates (collapse == True means H^2 -> 0)
    preds = {}
    # families parameterized simply
    preds["k even (P1)"] = lambda E, F: (F["k"] % 2 == 0)
    # 'shallow-defect' families: collapse unless there is an isolated shallow layer
    preds["n_shallow even"] = lambda E, F: (F["n_shallow"] % 2 == 0)
    preds["n_shallow even OR n_deep>0 with n_shallow<=... "] = \
        lambda E, F: (F["n_shallow"] % 2 == 0) or (F["n_deep"] >= 1 and F["n_shallow"] >= 1)
    # THE key family: think per-VALUE parity but shallow values (1,2) are the
    # only ones that can leave a floor; deep(>=3) always clear.
    preds["n1 even and n2 even"] = lambda E, F: (F["n1"] % 2 == 0 and F["n2"] % 2 == 0)
    preds["n1+n2 even"] = lambda E, F: ((F["n1"] + F["n2"]) % 2 == 0)
    # shallow count with a deep 'joker' that can fix ONE parity:
    preds["shallow parity fixable by one deep"] = \
        lambda E, F: (F["n_shallow"] % 2 == 0) or (F["n_deep"] >= 1)
    # the sharpest guess: collapse iff n_shallow is even, OR (n_shallow odd AND
    # there is a deep factor to absorb the lone shallow) -- but a lone shallow
    # needs a deep STRICTLY, and multiple shallows of DIFFERENT values...
    # try: collapse iff (n1 even) and (n2 + [n1 odd? no]) -- enumerate combos:
    preds["n1 even, n2 arbitrary if deep exists"] = \
        lambda E, F: (F["n1"] % 2 == 0 and (F["n2"] % 2 == 0 or F["n_deep"] >= 1)) \
                     or (F["n1"] % 2 == 1 and F["n_deep"] >= 1 and F["n2"] % 2 == 0) \
                     or False
    # brute: collapse iff we can pair up ALL shallow (value-1 with value-1,
    # value-2 with value-2) leaving 0 or (a lone shallow that a deep absorbs),
    # and deeps always clear:
    def pred_final(E, F):
        n1, n2, nd = F["n1"], F["n2"], F["n_deep"]
        # deeps always clear (self or mutual). Track a 'joker' capacity = number
        # of deep factors, each can absorb at most one leftover shallow.
        leftover = (n1 % 2) + (n2 % 2)   # 0,1,or 2 lone shallow values
        return leftover <= nd
    preds["FINAL: lone-shallow(<=nd deep jokers)"] = pred_final

    # score all
    print("modules:", n)
    winners = []
    for name, fn in preds.items():
        hits = 0
        misses = []
        for E, collapse in data:
            F = features(E)
            if fn(E, F) == collapse:
                hits += 1
            else:
                misses.append(list(E))
        tag = "  <-- 21/21" if hits == n else ""
        print("  %-45s %d/%d%s" % (name, hits, n, tag))
        if hits == n:
            winners.append(name)
        elif hits >= n - 2:
            print("        misses:", misses)

    print("\nWINNERS (21/21):", winners)

    out = {"n": n,
           "data": [{"E": list(E), "collapse": c} for E, c in data],
           "winners": winners}
    with open("results/cohomology_invariant_search4.json", "w") as fp:
        json.dump(out, fp, indent=2)

if __name__ == "__main__":
    main()
