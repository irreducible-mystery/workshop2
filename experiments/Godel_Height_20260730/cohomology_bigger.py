#!/usr/bin/env python3
"""
cohomology_bigger.py
====================
SECTION 14, PART 1 -- push the explicit-resolution engine from Z2xZ2 to BIGGER
frame-bundles: G = Z2xZ2xZ2 (three directions) and G = Z4xZ2 (mixed non-cyclic).
Tests whether the two structural facts found in sec 13 survive:
  (i)  the trivial action MAXIMIZES the generative rank, and
  (ii) there is a module-dependent FLOOR (an irreducible core no action removes).

METHOD (generic).  For a finite abelian group G = Z_{m_1} x ... x Z_{m_d}, the
resolution of Z over Z[G] is the TENSOR PRODUCT of the one-generator 2-periodic
resolutions, one per cyclic factor.  For a single factor Z_m = <t>:
   P^(a)_i is free of rank 1, differential phi_i = (t-1) if i odd, Norm=(1+t+..+t^{m-1})
   if i even>0.
The total complex in degree n has one free ZG-generator for each multi-index
(i_1,...,i_d) with sum i_r = n; the differential is the signed sum of the per-factor
differentials (Koszul sign (-1)^{i_1+..+i_{r-1}} on the r-th factor's map).

We build this over the group ring Z[G] represented as functions on G (|G| ints),
with each cyclic-factor operator realized as a left-multiplication matrix, verify
d^2 = 0 exactly, then Hom(-,M) and exact finite ker/im for H^2, exactly as in
cohomology_resolution.py.  Everything integer, exact, self-checking.
"""
from __future__ import annotations
import itertools, json, os
import numpy as np

os.makedirs("results", exist_ok=True)


# --------------------------------------------------------------------------- #
# Group ring of G = prod Z_{orders_G}.  Elements indexed by tuples.            #
# --------------------------------------------------------------------------- #
class GroupRing:
    def __init__(self, orders_G):
        self.orders = tuple(orders_G)
        self.elems = list(itertools.product(*[range(m) for m in orders_G]))
        self.idx = {g: i for i, g in enumerate(self.elems)}
        self.n = len(self.elems)
        self.zero = tuple(0 for _ in orders_G)
    def gmul(self, a, b):
        return tuple((x + y) % m for x, y, m in zip(a, b, self.orders))
    def left_mult(self, coeffs):
        """|G|x|G| integer matrix: left mult by ring element `coeffs` (len |G|)."""
        Mx = np.zeros((self.n, self.n), dtype=np.int64)
        for j, gj in enumerate(self.elems):
            for i, gi in enumerate(self.elems):
                c = coeffs[i]
                if c:
                    Mx[self.idx[self.gmul(gi, gj)], j] += c
        return Mx
    def factor_gen(self, r):
        """ring element = generator t_r of the r-th cyclic factor (as coeffs)."""
        g = list(self.zero); g[r] = 1
        v = [0] * self.n; v[self.idx[tuple(g)]] = 1
        return v
    def one(self):
        v = [0] * self.n; v[self.idx[self.zero]] = 1
        return v
    def op_t_minus(self, r):
        """(t_r - 1) as a matrix."""
        v = self.factor_gen(r); v[self.idx[self.zero]] -= 1
        return self.left_mult(v)
    def op_norm(self, r):
        """Norm_r = 1 + t_r + t_r^2 + ... + t_r^{m_r-1} as a matrix."""
        m = self.orders[r]
        v = [0] * self.n
        g = list(self.zero)
        for p in range(m):
            gg = list(self.zero); gg[r] = p
            v[self.idx[tuple(gg)]] += 1
        return self.left_mult(v)


# --------------------------------------------------------------------------- #
# Tensor-product resolution: per-factor differential phi_r(i) is (t_r - 1) if i  #
# odd, Norm_r if i even>0.  Degree-n generators = multi-indices summing to n.    #
# --------------------------------------------------------------------------- #
class Resolution:
    def __init__(self, orders_G):
        self.R = GroupRing(orders_G)
        self.d = len(orders_G)
        self.orders_G = tuple(orders_G)
        self._basis = {}   # n -> list of multi-indices (i_1..i_d), sum = n
    def basis(self, n):
        if n not in self._basis:
            idxs = []
            for combo in itertools.product(*[range(n + 1) for _ in range(self.d)]):
                if sum(combo) == n:
                    idxs.append(combo)
            idxs.sort()
            self._basis[n] = idxs
        return self._basis[n]
    def phi(self, r, i):
        """per-factor map applied in degree i of factor r (maps deg i -> i-1)."""
        if i % 2 == 1:
            return self.R.op_t_minus(r)
        else:
            return self.R.op_norm(r)
    def differential(self, n):
        """matrix of d_n : P_n -> P_{n-1} as block matrix over ZG (blocks |G|x|G|)."""
        src = self.basis(n)          # generators of P_n
        tgt = self.basis(n - 1)      # generators of P_{n-1}
        tgt_idx = {mi: k for k, mi in enumerate(tgt)}
        NG = self.R.n
        D = np.zeros((len(tgt) * NG, len(src) * NG), dtype=np.int64)
        for ci, mi in enumerate(src):
            for r in range(self.d):
                if mi[r] >= 1:
                    tmi = list(mi); tmi[r] -= 1; tmi = tuple(tmi)
                    k = tgt_idx[tmi]
                    sign = -1 if (sum(mi[:r]) % 2 == 1) else 1
                    D[k*NG:(k+1)*NG, ci*NG:(ci+1)*NG] += sign * self.phi(r, mi[r])
        return D
    def augmentation(self):
        return np.ones((1, self.R.n), dtype=np.int64)
    def verify_complex(self, maxn=4):
        ok = True
        d = {n: self.differential(n) for n in range(1, maxn + 1)}
        if not np.all(self.augmentation() @ d[1] == 0):
            ok = False; print("  eps d1 != 0 !!")
        for n in range(1, maxn):
            if not np.all(d[n] @ d[n + 1] == 0):
                ok = False
                print(f"  d{n} d{n+1} != 0 !!")
        return ok


# --------------------------------------------------------------------------- #
# G-module: abelian group (orders_M) with commuting automorphisms, one per       #
# cyclic factor of G (the images of the generators t_r), each of order dividing  #
# m_r.  Hom(-,M) coboundary as in sec 13.                                        #
# --------------------------------------------------------------------------- #
class GModule:
    def __init__(self, orders_M, gen_actions, orders_G, name=""):
        self.orders_M = list(orders_M); self.k = len(orders_M)
        self.orders_G = tuple(orders_G)
        self.acts = [np.array(a, dtype=np.int64) for a in gen_actions]  # per G-generator
        self.name = name
        self._check()
    def _eq_mod(self, A, B):
        d = A - B
        return all(np.all(d[r] % self.orders_M[r] == 0) for r in range(self.k))
    def _check(self):
        I = np.eye(self.k, dtype=np.int64)
        # each generator action must have order dividing the factor order, and commute
        for r, A in enumerate(self.acts):
            P = I.copy()
            for _ in range(self.orders_G[r]):
                P = P @ A
            assert self._eq_mod(P, I), f"{self.name}: gen {r} action^{self.orders_G[r]} != I"
        for r in range(len(self.acts)):
            for s in range(r + 1, len(self.acts)):
                assert self._eq_mod(self.acts[r] @ self.acts[s], self.acts[s] @ self.acts[r]), \
                    f"{self.name}: gen actions {r},{s} do not commute"
    def elem_action(self, g, R: GroupRing):
        """action of group element g=(a_1..a_d) = prod acts[r]^{a_r} (mod orders)."""
        Mx = np.eye(self.k, dtype=np.int64)
        for r, a in enumerate(g):
            for _ in range(a):
                Mx = Mx @ self.acts[r]
        return Mx


def coboundary(D_block, M: GModule, R: GroupRing):
    """delta from ZG differential D_block (rows=r_{n-1} blocks of |G|, cols=r_n)."""
    NG = R.n; k = M.k
    rblocks = D_block.shape[0] // NG
    cblocks = D_block.shape[1] // NG
    Delta = np.zeros((cblocks * k, rblocks * k), dtype=np.int64)
    zero_col = R.idx[R.zero]
    for kk in range(rblocks):
        for ii in range(cblocks):
            blk = D_block[kk*NG:(kk+1)*NG, ii*NG:(ii+1)*NG]
            coeffs = blk[:, zero_col]     # ring element = image of identity basis elt
            acc = np.zeros((k, k), dtype=np.int64)
            for gi, g in enumerate(R.elems):
                if coeffs[gi]:
                    acc += coeffs[gi] * M.elem_action(g, R)
            Delta[ii*k:(ii+1)*k, kk*k:(kk+1)*k] = acc
    return Delta


def module_elements(orders):
    return list(itertools.product(*[range(o) for o in orders]))

def H2(res: Resolution, M: GModule, cap=2_000_000):
    R = res.R
    d2 = res.differential(2)  # P2->P1
    d3 = res.differential(3)  # P3->P2
    delta1 = coboundary(d2, M, R)   # C1 -> C2
    delta2 = coboundary(d3, M, R)   # C2 -> C3
    r1 = len(res.basis(1)); r2 = len(res.basis(2)); r3 = len(res.basis(3))
    k = M.k
    orders1 = M.orders_M * r1
    orders2 = M.orders_M * r2
    orders3 = M.orders_M * r3
    size_C2 = 1
    for o in orders2: size_C2 *= o
    if size_C2 > cap:
        return {"skipped": True, "reason": f"|C2|={size_C2} > cap"}
    mod2 = np.array(orders2, dtype=np.int64); mod3 = np.array(orders3, dtype=np.int64)
    C1 = module_elements(orders1); C2 = module_elements(orders2)
    z3 = tuple(0 for _ in orders3)
    def ap(mat, vec, mod):
        return tuple(int(x) % int(m) for x, m in zip(mat @ np.array(vec, dtype=np.int64), mod))
    ker2 = set(c for c in C2 if ap(delta2, c, mod3) == z3)
    im1 = set(ap(delta1, c, mod2) for c in C1)
    assert im1 <= ker2, f"{M.name}: im(delta1) not <= ker(delta2) -- complex broken"
    def addv(a, b): return tuple((x+y) % m for x, y, m in zip(a, b, orders2))
    def coset(x): return frozenset(addv(x, b) for b in im1)
    reps = {}
    for z in ker2:
        c = coset(z)
        if c not in reps: reps[c] = z
    inv = invariant_factors(list(reps.values()),
                            lambda a, b: reps[coset(addv(a, b))],
                            reps[coset(tuple(0 for _ in orders2))])
    return {"skipped": False, "|H2|": len(reps), "H2_invariants": inv,
            "|ker2|": len(ker2), "|im1|": len(im1)}


def invariant_factors(elems, add, zero):
    n = len(elems)
    if n == 1: return []
    def order_of(x):
        acc = zero; k = 0
        while True:
            acc = add(acc, x); k += 1
            if acc == zero: return k
    orders = [order_of(x) for x in elems]
    primes = set(); m = n; d = 2
    while d*d <= m:
        while m % d == 0: primes.add(d); m //= d
        d += 1
    if m > 1: primes.add(m)
    prime_lists = {}
    for p in primes:
        maxe = 0
        while p**(maxe+1) <= n: maxe += 1
        A = [0]*(maxe+2)
        for o in orders:
            oo = o; e = 0
            while oo % p == 0: oo //= p; e += 1
            if oo == 1:
                for kk in range(e, maxe+1): A[kk] += 1
        A[0] = max(A[0], 1)
        t = []
        for kk in range(maxe+1):
            val = A[kk] if A[kk] > 0 else 1
            lg = 0; v = 1
            while v < val: v *= p; lg += 1
            t.append(lg)
        d_ge = [t[0]] + [t[j]-t[j-1] for j in range(1, maxe+1)]
        exps = []
        for e in range(1, maxe+1):
            cnt = d_ge[e] - (d_ge[e+1] if e+1 <= maxe else 0)
            exps += [e]*cnt
        prime_lists[p] = sorted([p**e for e in exps], reverse=True)
    maxlen = max((len(v) for v in prime_lists.values()), default=0)
    invs = []
    for i in range(maxlen):
        f = 1
        for p in prime_lists:
            lst = prime_lists[p]
            if i < len(lst): f *= lst[i]
        if f > 1: invs.append(f)
    invs.sort()
    return invs


if __name__ == "__main__":
    for og in [[2,2],[2,2,2],[4,2]]:
        r = Resolution(og)
        print(f"G={og}: ranks P0..P3 =",
              [len(r.basis(n)) for n in range(4)],
              " complex d^2=0:", r.verify_complex(4))
