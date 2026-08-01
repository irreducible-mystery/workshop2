import numpy as np, itertools, math

def T(g): return np.array([[1.0,g],[1.0,0.0]])

def sweep(G, N=18):
    A, B = T(G), T(-G)
    mats = [np.eye(2)]
    # BFS over all products up to length N, keep norms
    lo_rec, hi_rec = [], []
    cur = [np.eye(2)]
    for n in range(1, N+1):
        nxt = []
        for M in cur:
            nxt.append(A@M); nxt.append(B@M)
        cur = nxt
        norms = [np.linalg.norm(M,2) for M in cur]
        # also spectral radii for JSR lower bounds / subradius upper bounds
        rhos  = [max(abs(np.linalg.eigvals(M))) for M in cur]
        lo_rec.append((n, min(norms)**(1/n), min(rhos)**(1/n)))
        hi_rec.append((n, max(norms)**(1/n), max(rhos)**(1/n)))
        if n>=14: cur = sorted(cur, key=lambda M: np.linalg.norm(M,2))[:4000] + sorted(cur, key=lambda M: -np.linalg.norm(M,2))[:4000]
    return lo_rec, hi_rec

def spm(g):
    d = 1+4*g
    if d>=0: return (1+math.sqrt(d))/2
    return abs(complex(1, math.sqrt(-d))/2)

for G in [0.05, 0.1, 0.2, 0.24, 0.25, 0.3, 0.5, 1.0, 2.0, 5.0]:
    lo, hi = sweep(G, 18)
    n,ln,lr = lo[-1]; _,hn,hr = hi[-1]
    print(f"G={G:6}  claim_JSR={spm(G):.6f} numJSR(norm,n={n})={hn:.6f} (rho)={hr:.6f}")
    print(f"          claim_sub={spm(-G):.6f} numSUB(norm,n={n})={ln:.6f} (rho)={lr:.6f}   sqrt(G)={math.sqrt(G):.6f}")
