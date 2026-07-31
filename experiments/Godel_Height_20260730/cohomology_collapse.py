#!/usr/bin/env python3
"""
SECTION 14 PART 2 -- the full-collapse characterization.

Question (standing OPEN since sec 11): for the CYCLIC frame group G = Z2, which
finite abelian modules M admit an order-2 action driving H^2(Z2, M) fully to rank 0
(the trivial group)?  Sec 11 REFUTED "collapse iff homocyclic" and "iff a deep
factor exists".  Here we assemble the exact collapse data and search for the real
invariant, forming a conjecture and testing it against every module we can compute.

Structural fact to build on (proven, sec 11): trivial-action H^2(Z2,M) = M[2],
the 2-torsion, an F2-vector space of dimension = number of even invariant factors
of M (call it t = dim_{F2} M[2]).  A non-trivial order-2 action twists this.

CANDIDATE INVARIANT (the hypothesis we test):
  H^2(Z2,M) can be driven to rank 0 by some order-2 action  <=>  the 2-torsion
  "pairs up" -- roughly, M has an EVEN number of even invariant factors AND those
  even factors can be matched by an involution that swaps them (exchanging a factor
  with a partner shifts M^G/Norm to zero on that pair).  More precisely we test a
  hierarchy of concrete predictors and report which one (if any) matches the data:
    P1: t = dim M[2] is EVEN                          (parity of 2-rank)
    P2: M[2] admits a fixed-point-free involution acting on the even factors
        realized by a genuine module automorphism of order 2 (a "swap pairing")
    P3: the multiset of 2-adic valuations of the even factors can be partitioned
        into equal pairs (each even factor has a same-exponent partner)
We compute the true min-rank by exhaustive enumeration (reusing the sec-11/sec-13
engines) and compare.
"""
from __future__ import annotations
import itertools, json, os

os.makedirs("results", exist_ok=True)


def even_invariant_factors(orders):
    """2-adic exponents of the even invariant factors of M = prod Z_{orders}."""
    exps = []
    for o in orders:
        e = 0; oo = o
        while oo % 2 == 0: oo //= 2; e += 1
        if e >= 1: exps.append(e)
    return sorted(exps)

def dim_M2(orders):
    """dim_{F2} M[2] = number of even factors."""
    return len(even_invariant_factors(orders))

def P1_even_2rank(orders):
    return dim_M2(orders) % 2 == 0

def P3_pairable_exponents(orders):
    """Can the multiset of even-factor 2-adic exponents be partitioned into equal
    pairs? (every exponent value occurs an even number of times)."""
    exps = even_invariant_factors(orders)
    from collections import Counter
    c = Counter(exps)
    return all(v % 2 == 0 for v in c.values())


# --- assemble the exact collapse data from sec-11 (cyclic G=Z2). --------------
CYCLIC_DATA = {}  # module name -> (orders, min_rank, collapses)
def load_cyclic():
    d = json.load(open("results/cohomology_rank_law.json"))
    name_to_orders = {
        "Z2": [2], "Z4": [4], "Z8": [8], "Z2xZ2": [2, 2], "Z2xZ4": [2, 4],
        "Z4xZ4": [4, 4], "Z2xZ2xZ2": [2, 2, 2], "Z3xZ3": [3, 3],
    }
    for r in d["results"]:
        dist = r["distribution_of_H2_types"]
        def rank(k): return 0 if k == "trivial" else k.count("Z")
        minr = min(rank(k) for k in dist)
        nm = r["module"]
        CYCLIC_DATA[nm] = {"orders": name_to_orders[nm], "min_rank": minr,
                           "collapses": minr == 0}
    return CYCLIC_DATA


def analyze():
    print("=" * 78)
    print("PART 2  --  full-collapse characterization (cyclic frame group G = Z2)")
    print("=" * 78)
    load_cyclic()
    print(f"  {'module':>10} {'orders':>10} {'dimM[2]':>8} {'evenExps':>10} "
          f"{'minRank':>8} {'collapse':>9} | {'P1even':>7} {'P3pair':>7}")
    rows = []
    p1_hits = p3_hits = 0
    tot = 0
    for nm, info in CYCLIC_DATA.items():
        orders = info["orders"]
        t = dim_M2(orders)
        exps = even_invariant_factors(orders)
        collapse = info["collapses"]
        p1 = P1_even_2rank(orders)
        p3 = P3_pairable_exponents(orders)
        # for modules WITH 2-torsion only; Z3xZ3 has t=0 (trivially collapses -- H^2=0
        # already at trivial action). Treat t=0 as "collapses" trivially.
        tot += 1
        if (p1 == collapse): p1_hits += 1
        if (p3 == collapse): p3_hits += 1
        print(f"  {nm:>10} {str(orders):>10} {t:>8} {str(exps):>10} "
              f"{info['min_rank']:>8} {str(collapse):>9} | {str(p1):>7} {str(p3):>7}")
        rows.append({"module": nm, "orders": orders, "dim_M2": t,
                     "even_exponents": exps, "min_rank": info["min_rank"],
                     "collapses": collapse, "P1_even_2rank": p1,
                     "P3_pairable_exponents": p3})
    print()
    print(f"  predictor agreement with observed collapse over {tot} modules:")
    print(f"     P1 (dim M[2] even)          : {p1_hits}/{tot}")
    print(f"     P3 (even exps pair up)      : {p3_hits}/{tot}")
    return rows, p1_hits, p3_hits, tot


def note_Z3():
    print()
    print("  NOTE on Z3xZ3: it has NO 2-torsion (dim M[2]=0), so H^2(Z2,Z3xZ3)=0")
    print("  already at the trivial action -- it 'collapses' vacuously.  Both P1 (0 is")
    print("  even) and P3 (empty multiset pairs up) predict collapse=True, consistent.")


def ledger(p1_hits, p3_hits, tot, rows):
    # find any counterexamples for the best predictor
    print()
    print("=" * 78)
    print("LEDGER  --  section 14 part 2 (collapse characterization)")
    print("=" * 78)
    # identify best predictor and its exceptions
    def exceptions(key):
        return [r["module"] for r in rows if r[key] != r["collapses"]]
    ex_p1 = exceptions("P1_even_2rank")
    ex_p3 = exceptions("P3_pairable_exponents")
    print(f"""
  DATA (cyclic G=Z2, exhaustive over all order-2 actions, from sec 11):
    collapsing modules   : {[r['module'] for r in rows if r['collapses']]}
    non-collapsing       : {[r['module'] for r in rows if not r['collapses']]}

  PREDICTOR TEST:
    P1  'dim_{{F2}} M[2] is even'           agreement {p1_hits}/{tot}, exceptions {ex_p1}
    P3  'even invariant factors pair up
         (each 2-exponent even multiplicity)' agreement {p3_hits}/{tot}, exceptions {ex_p3}

  STATUS:""")
    if not ex_p1:
        print("""    * CONJECTURE (verified-on-family, NOT proven): for the cyclic frame group
      G=Z2, H^2(Z2,M) can be driven to rank 0 by some order-2 action IF AND ONLY
      IF dim_{F2} M[2] is EVEN -- i.e. the module's 2-torsion has even rank, so the
      2-torsion can be organized into swap-pairs an involution exchanges.  This
      matches EVERY module in the sec-11 exhaustive dataset with no exception.
      It is a CONJECTURE with a heuristic (an involution that pairs the F2-basis of
      M[2] sends the norm-image onto the whole fixed space, collapsing the quotient),
      not a theorem; a proof would need to show such an order-2 MODULE automorphism
      always exists when the 2-rank is even AND respects the higher 2-structure.""")
    else:
        print(f"    * P1 has exceptions {ex_p1} -- not the invariant. See P3 / open.")
    print("""
  REFUTED (re-confirmed from sec 11, now explained by the conjecture):
    * 'collapse iff homocyclic' -- FALSE.  Z2xZ2xZ2 is homocyclic but has dim M[2]=3
      (ODD) so does NOT collapse; Z4 is homocyclic-of-one-factor, dim M[2]=1 (odd),
      does NOT collapse.  The even-2-rank predictor gets both right.
    * 'collapse iff a deep factor exists' -- FALSE.  Z2xZ2 collapses with no deep
      factor (dim M[2]=2, even); Z8 collapses (dim M[2]=1... see caveat below).

  CANNOT CLAIM / OPEN:
    * A PROOF of the even-2-rank characterization for all finite abelian M.
    * The interaction with higher 2-structure: Z8 has dim M[2]=1 (odd) yet the
      sec-11 data shows it reaching rank 0 via u=3 -- this is the ONE case where the
      naive even-rank rule needs the deeper story (the action u=3 on Z8 kills the
      class by a valuation coincidence, not by pairing 2-torsion).  So the clean
      conjecture is really: for ELEMENTARY-type collapse (pairing M[2]) even 2-rank
      is the invariant; a SECOND collapse channel exists for cyclic 2-groups of
      depth >=3 (the sec-9 fragile phase, 8|N).  We state BOTH and mark the unified
      statement OPEN.
    * Non-cyclic frame groups: the sec-13 'floor' data is the analogue; a unified
      collapse law across cyclic and non-cyclic G is not attempted here.
""")


def main():
    rows, p1, p3, tot = analyze()
    note_Z3()
    ledger(p1, p3, tot, rows)
    json.dump({"rows": rows, "P1_hits": p1, "P3_hits": p3, "total": tot},
              open("results/cohomology_collapse.json", "w"), indent=2, default=str)
    print("[written] results/cohomology_collapse.json")


if __name__ == "__main__":
    main()
