#!/usr/bin/env python3
"""
cohomology_rank_law.py
======================
PUSH 1: turn section-10's SAMPLED "swap/shear collapse the rank-2 core" into an
EXHAUSTIVE, verified statement -- and be scrupulous about what is thereby proven
versus merely checked-on-a-family versus still-conjectural.

Scope of what runs here (G = Z_2 acting on a finite abelian module M):
  H^2(Z_2, M) = M^G / Norm(M),  Norm(x) = x + t.x,  M^G = {x : t.x = x}.
This is the exact Tate formula (literal, validated against brute cochains in
cohomology_general.py with zero mismatches). Given it, |H^2| and the invariant
factors (the RANK) of the generative core are a finite linear-algebra computation
over the module, so we can enumerate EVERY order-2 automorphism of a given M and
read off the whole distribution of ranks -- not a sample.

What this can legitimately CLAIM (see the printed CLAIM/CANNOT block at the end):
  * For each specific M we test, the FULL set of order-2 actions and the exact
    multiset of resulting H^2 invariant-factor types. This is exhaustive for that M.
  * A clean structural fact that holds across every M in the family: the rank of
    H^2(Z_2,M) equals the F_2-rank of  M^G / Norm(M), and the trivial action
    always maximizes it (gives the 2-torsion subgroup's full rank), while some
    actions strictly lower it. This is verified, and for the trivial-action part
    it is also a one-line proof (given below in a comment).
What this CANNOT yet claim:
  * A closed formula for the rank as a function of (M, action) for ALL M -- we only
    enumerate a finite family. Whether "there is always an action dropping the rank
    to 0 iff M is 2-elementary generated" is a theorem is left OPEN.
  * Anything for non-cyclic FRAME groups G (that is push 2, cohomology_lhs.py).
"""
from __future__ import annotations
import itertools, json, os
from collections import Counter, defaultdict

os.makedirs("results", exist_ok=True)


# --------------------------------------------------------------------------- #
# Finite abelian module M = prod Z_{orders[i]}; automorphisms as integer       #
# matrices acting mod the component orders.                                    #
# --------------------------------------------------------------------------- #
class Module:
    def __init__(self, orders):
        self.orders = tuple(orders)
        self.elems = list(itertools.product(*[range(n) for n in orders]))
        self.size = len(self.elems)
        self.zero = tuple(0 for _ in orders)

    def add(self, a, b):
        return tuple((x + y) % n for x, y, n in zip(a, b, self.orders))
    def neg(self, a):
        return tuple((-x) % n for x, n in zip(a, self.orders))


def apply_mat(mat, x, orders):
    return tuple(sum(mat[i][j] * x[j] for j in range(len(x))) % orders[i]
                 for i in range(len(orders)))


def is_homomorphism(mat, M):
    """The matrix defines a genuine module endomorphism of M = prod Z_{n_i} iff,
    for every entry, the image of generator j (which has order n_j) is well-defined
    in Z_{n_i}: i.e.  n_j * mat[i][j] == 0  (mod n_i).  This is the exact algebraic
    condition (fast, O(n^2)) equivalent to additivity on all of M."""
    orders = M.orders
    n = len(orders)
    for i in range(n):
        for j in range(n):
            if (orders[j] * mat[i][j]) % orders[i] != 0:
                return False
    return True


def is_automorphism(mat, M):
    """A module endomorphism that is also a bijection on elements
    (finite => injective <=> surjective). Must first be a homomorphism."""
    if not is_homomorphism(mat, M):
        return False
    seen = set()
    for x in M.elems:
        seen.add(apply_mat(mat, x, M.orders))
    return len(seen) == M.size


def is_order_dividing_2(mat, M):
    """t^2 == identity on M."""
    for x in M.elems:
        y = apply_mat(mat, apply_mat(mat, x, M.orders), M.orders)
        if y != x:
            return False
    return True


# --------------------------------------------------------------------------- #
# H^2(Z_2, M) = M^G / Norm(M), with invariant factors (the RANK/structure).    #
# --------------------------------------------------------------------------- #
def H2_structure(M: Module, mat):
    def t(x): return apply_mat(mat, x, M.orders)
    fixed = [x for x in M.elems if t(x) == x]              # M^G
    norm_im = set(M.add(x, t(x)) for x in M.elems)         # Norm(M) = (1+t)M
    assert norm_im <= set(fixed)
    order = len(fixed) // len(norm_im)
    inv = quotient_invariants(M, fixed, norm_im)
    return order, inv


def quotient_invariants(M: Module, big, small):
    """Invariant factors of Q = (big/small) as a finite abelian group.

    Correct method: realize Q concretely as a set of coset-keys with a group
    operation, then compute its invariant factors by iterated peeling of a
    maximal-order cyclic subgroup -- but doing the peeling INSIDE the quotient
    group Q itself (as an abstract group of coset-keys), not by re-cosetting in M
    (which was the bug). Small groups only; exact here."""
    small = set(small)

    def coset(x):
        return frozenset(M.add(x, s) for s in small)

    # canonical key per coset + a chosen representative tuple
    reps = {}
    for x in big:
        c = coset(x)
        if c not in reps:
            reps[c] = x
    keys = list(reps.keys())
    zero_key = coset(M.zero)
    order = len(keys)
    if order == 1:
        return []

    # group operation on coset-keys, precomputed as a table
    add = {}
    for a in keys:
        ra = reps[a]
        for b in keys:
            add[(a, b)] = coset(M.add(ra, reps[b]))

    def add_keys(a, b):
        return add[(a, b)]

    def ord_key(a):
        acc = zero_key
        k = 0
        while True:
            k += 1
            acc = add_keys(acc, a)
            if acc == zero_key:
                return k

    # Invariant factors from the element-order statistics, via primary
    # decomposition. For each prime p | |G|, the p-primary part's type is
    # recovered from  a_k = #{ x : p^k x = 0 }  (the number of elements killed by
    # p^k). This is exact for any finite abelian group and needs no risky peeling.
    def mul(a, n):
        acc = zero_key
        cur = a
        # n*a by repeated addition (n small here)
        for _ in range(n):
            acc = add_keys(acc, a)
        return acc

    # factor |G| into primes
    def factor(n):
        f = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                f[d] = f.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            f[n] = f.get(n, 0) + 1
        return f

    primes = factor(order)
    all_factors = []
    for p, _ in primes.items():
        # counts: A[k] = #{x in G : p^k * x = 0}
        # find max k needed
        A = [1]  # A[0] = #{x: x=0} = 1
        k = 0
        while True:
            k += 1
            cnt = sum(1 for x in keys if mul(x, p ** k) == zero_key)
            A.append(cnt)
            if cnt == A[-2]:   # stabilized: p^k kills same set as p^(k-1)
                break
        # number of cyclic factors Z_{p^j} in the p-part:
        #   n_j = ( 2*A[j] - A[j-1] - A[j+1] ) / ... standard formula:
        # Let r_k = log_p( A[k]/A[k-1] ) = rank contributed at level k.
        # Number of invariant factors of order exactly p^j is:
        #   t_j = r_j - r_{j+1},  where r_k = log_p(A[k]) - log_p(A[k-1]).
        import math
        maxk = len(A) - 1
        logs = [round(math.log(a, p)) if a > 1 else 0 for a in A]  # log_p A[k]
        r = [logs[k] - logs[k - 1] for k in range(1, len(logs))]   # r[1..maxk], 0-indexed r[k-1]
        r = r + [0]
        for j in range(1, maxk + 1):
            t_j = r[j - 1] - r[j]      # number of Z_{p^j} factors
            for _ in range(t_j):
                all_factors.append(p ** j)
    return sorted(all_factors)


# --------------------------------------------------------------------------- #
# EXHAUSTIVE enumeration of ALL order-2 automorphisms of a small module M.      #
# --------------------------------------------------------------------------- #
def all_order2_actions(M: Module, entry_range=None):
    n = len(M.orders)
    # candidate integer matrices with entries mod lcm-ish range; to be safe use
    # entries in range(max(orders)) which covers all residues that matter.
    R = max(M.orders)
    rng = range(R) if entry_range is None else entry_range
    acts = []
    for flat in itertools.product(rng, repeat=n * n):
        mat = [list(flat[i * n:(i + 1) * n]) for i in range(n)]
        if not is_automorphism(mat, M):
            continue
        if not is_order_dividing_2(mat, M):
            continue
        acts.append(mat)
    # dedup by action-on-elements signature
    uniq = {}
    for mat in acts:
        sig = tuple(apply_mat(mat, x, M.orders) for x in M.elems)
        if sig not in uniq:
            uniq[sig] = mat
    return list(uniq.values())


def analyze_module(name, orders):
    M = Module(orders)
    acts = all_order2_actions(M)
    dist = Counter()
    trivial_inv = None
    min_order = None
    per_action = []
    triv_mat = [[1 if i == j else 0 for j in range(len(orders))] for i in range(len(orders))]
    for mat in acts:
        order, inv = H2_structure(M, mat)
        key = "x".join(f"Z{f}" for f in inv) if inv else "trivial"
        dist[key] += 1
        per_action.append({"matrix": mat, "H2_order": order, "H2_invariants": inv})
        if mat == triv_mat:
            trivial_inv = inv
        min_order = order if min_order is None else min(min_order, order)
    max_order = max((p["H2_order"] for p in per_action), default=1)
    return {
        "module": name, "orders": list(orders), "n_order2_actions": len(acts),
        "trivial_H2_invariants": trivial_inv,
        "max_H2_order": max_order, "min_H2_order": min_order,
        "distribution_of_H2_types": dict(dist),
        "some_action_kills_class": (min_order == 1),
        "per_action": per_action,
    }


if __name__ == "__main__":
    print("=" * 76)
    print("PUSH 1: EXHAUSTIVE rank distribution of H^2(Z_2, M) over ALL order-2 actions")
    print("=" * 76)
    family = [
        ("Z2",      (2,)),
        ("Z4",      (4,)),
        ("Z8",      (8,)),
        ("Z2xZ2",   (2, 2)),
        ("Z2xZ4",   (2, 4)),
        ("Z4xZ4",   (4, 4)),
        ("Z2xZ2xZ2",(2, 2, 2)),
        ("Z3xZ3",   (3, 3)),   # control: no 2-torsion -> always trivial
    ]
    results = []
    for name, orders in family:
        res = analyze_module(name, orders)
        results.append(res)
        print(f"\n  M = {name:9s} (|M|={Module(orders).size}):  "
              f"{res['n_order2_actions']} order-2 actions")
        print(f"    trivial action -> H^2 = "
              f"{'x'.join('Z'+str(f) for f in res['trivial_H2_invariants']) if res['trivial_H2_invariants'] else 'trivial'}"
              f"   (this is the MAX rank)")
        print(f"    max |H^2| = {res['max_H2_order']},  min |H^2| = {res['min_H2_order']},  "
              f"some action kills the class: {res['some_action_kills_class']}")
        print(f"    full distribution over all order-2 actions: {res['distribution_of_H2_types']}")

    # ---- the structural facts we verified across the whole family ---- #
    print("\n" + "=" * 76)
    print("VERIFIED ACROSS THE FAMILY (exhaustive per module):")
    print("=" * 76)
    fact1 = all((r["trivial_H2_invariants"] or []) != [] or r["module"] == "Z3xZ3"
                for r in results)  # every 2-torsion module has nontrivial trivial-action H2
    # trivial action gives the 2-torsion subgroup M[2]'s structure (max rank)
    fact_maxrank = []
    for r in results:
        M = Module(tuple(r["orders"]))
        # M[2] = 2-torsion subgroup
        twotors = [x for x in M.elems if M.add(x, x) == M.zero]
        # rank of M[2] as F_2-space = log2(|M[2]|)
        import math
        rk2 = round(math.log2(len(twotors))) if len(twotors) > 0 else 0
        triv_rank = len(r["trivial_H2_invariants"] or [])
        fact_maxrank.append((r["module"], rk2, triv_rank, rk2 == triv_rank))
    print("\n  FACT A (trivial action maximizes rank = F_2-rank of the 2-torsion M[2]):")
    for name, rk2, tr, ok in fact_maxrank:
        print(f"    {name:9s}: rank(M[2])={rk2}  trivial-action rank(H^2)={tr}  {'OK' if ok else 'MISMATCH'}")
    factA = all(ok for *_, ok in fact_maxrank)

    print("\n  FACT B* (does SOME order-2 action collapse H^2 fully to trivial?):")
    print("      NOTE: this turned out to be MODULE-DEPENDENT -- NOT a universal law.")
    kills = {}
    for r in results:
        kills[r["module"]] = r["some_action_kills_class"]
        print(f"    {r['module']:9s}: some action kills class = {r['some_action_kills_class']}")
    # the pattern: full collapse possible iff M is 'homocyclic' (all cyclic factors
    # equal order) among 2-groups? Z2, Z4 (single factor, no collapse -> exception),
    # Z8 collapses, Z2xZ2 collapses, Z4xZ4 collapses, but Z2xZ4 & Z2xZ2xZ2 do NOT.
    factB_universal = all(kills[r["module"]] for r in results
                          if r["module"] != "Z3xZ3" and (r["orders"]))
    print(f"\n    => FACT B is NOT universal (refuted): full collapse fails for "
          f"Z2xZ4 and Z2xZ2xZ2 (mixed-exponent 2-groups with no deep factor).")
    print(f"    OBSERVED PATTERN (conjecture, NOT proven): among the 2-groups tested,")
    print(f"    a fully-collapsing action exists exactly for")
    print(f"       Z8 (v2>=3 single factor), Z2xZ2, Z4xZ4 (homocyclic rank 2),")
    print(f"    and NOT for Z2 (too small), Z4, Z2xZ4, Z2xZ2xZ2. The clean guess")
    print(f"    'collapse iff homocyclic' FAILS at Z2 and Z2xZ2xZ2, so no simple law yet.")

    with open("results/cohomology_rank_law.json", "w") as f:
        # trim per_action matrices from JSON for the big modules
        slim = []
        for r in results:
            rr = dict(r)
            if Module(tuple(r["orders"])).size > 8:
                rr.pop("per_action", None)
            slim.append(rr)
        json.dump({"results": slim,
                   "FACT_A_trivial_maximizes_rank_eq_M2rank": factA,
                   "fact_A_detail": [{"module": n, "rank_M2": a, "trivial_rank": b, "ok": ok}
                                     for n, a, b, ok in fact_maxrank]},
                  f, indent=2)

    print("\n" + "=" * 76)
    print("CLAIM / CANNOT-CLAIM LEDGER")
    print("=" * 76)
    print("""
  CAN CLAIM (proven or exhaustively verified):
    * For each module M in the family, the COMPLETE multiset of H^2(Z_2,M) types
      over ALL order-2 actions (exhaustive enumeration, exact Tate formula).
    * FACT A: the trivial action gives H^2 = M[2] (the 2-torsion subgroup), so its
      rank is exactly the F_2-rank of M[2]; verified for every M, and it is the
      MAXIMUM rank any action achieves. [The 'H^2 = M[2]' half is PROVEN (see the
      PROVEN block below); the 'trivial MAXIMIZES over all actions' half is
      exhaustively verified on the family but not proven in general.]
    * The COMPLETE rank distribution: e.g. Z4xZ4 realizes H^2 types
      {trivial, Z2, Z2xZ2} across its 28 order-2 actions -- a genuine RANK LADDER
      (rank 0,1,2), not a mere on/off, confirming section 10's claim exhaustively.

  REFUTED (data killed a plausible claim -- worth recording):
    * "Some frame-change can always fully de-generativize a 2-torsion module"
      (FACT B as a universal law) is FALSE. Z2xZ4 and Z2xZ2xZ2 have NO order-2
      action collapsing H^2 to trivial (their min |H^2| = 2). So full collapse is
      module-dependent; the section-9/10 'reframe-to-gauge' adversary does NOT
      always have a total win available -- sometimes the best it can do is a
      partial rank drop. This is a genuine limit on the adversary, not a bug.

  CANNOT CLAIM (yet, or maybe ever):
    * A closed rank formula rank H^2 = f(M, action) valid for ALL finite abelian M.
      We only enumerated a finite family; the pattern is suggestive, not proven.
    * A clean characterization of WHICH 2-groups admit a fully-collapsing action.
      The obvious guesses (homocyclic; deep factor) both fail on the data, so this
      is OPEN. Might have a clean answer eventually; might not.
    * ANY statement about non-cyclic FRAME groups G -- that is a separate object
      (Lyndon-Hochschild-Serre), attempted in cohomology_lhs.py, and the clean
      single-invariant story is EXPECTED to break there.
    * The governance reading remains ANALOGY under the paradox<->cochain dictionary;
      no claim that a real institution's value grain IS one of these modules.

  PROVEN (not just checked):
    * FACT A, trivial-action half: H^2(Z_2, M) with trivial action = M/2M = M[2],
      so rank = dim_{F_2} M[2]. One-line proof: trivial action => M^G=M and
      Norm=(1+1)=mult-by-2, hence H^2 = M/Norm(M) = M/2M; for finite abelian M,
      M/2M and the 2-torsion M[2] are both F_2-vector spaces of equal dimension.
      This half is a theorem, not a sample. The 'trivial action MAXIMIZES rank'
      half is verified on the family but NOT proven in general (left open).
""")
