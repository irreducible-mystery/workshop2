import numpy as np, math

def T(g): return np.array([[1.0,g],[1.0,0.0]])
def spm(g):
    d=1+4*g
    return (1+math.sqrt(d))/2 if d>=0 else abs(complex(1,math.sqrt(-d))/2)

# 1) NEGATIVE G: family {T(G),T(-G)} is literally the same SET as for -G.
print("=== negative G: set symmetry ===")
for G in [-0.1,-0.2,-0.24]:
    A,B=T(G),T(-G)
    cur=[np.eye(2)]
    best_hi=0; best_lo=1e9
    for n in range(1,17):
        cur=[X@M for M in cur for X in (A,B)]
        rh=[max(abs(np.linalg.eigvals(M))) for M in cur]
        best_hi=max(best_hi,max(rh)**(1/n)); best_lo=min(best_lo,min(rh)**(1/n))
        if n>=13: cur=sorted(cur,key=lambda M:np.linalg.norm(M,2))[:3000]+sorted(cur,key=lambda M:-np.linalg.norm(M,2))[:3000]
    print(f" G={G}: claimed JSR s+(G)={spm(G):.6f}  TRUE JSR~{best_hi:.6f}  = s+(|G|)={spm(abs(G)):.6f}")
    print(f"        claimed sub |s+(-G)|={spm(-G):.6f}  TRUE sub~{best_lo:.6f} = s+(-|G|)={spm(-abs(G)):.6f}")

# 2) cone argument check: K_c={x>=c y>=0} invariant under both iff c(1-c)>=G, needs G<=1/4
print("\n=== invariant cone x >= c*y >= 0, c = s+(-G) ===")
for G in [0.05,0.1,0.2,0.25]:
    c=spm(-G)
    x,y=1.0,0.0
    ok=True; worst=1e9
    rng=np.random.default_rng(0)
    for trial in range(200):
        x,y=1.0,1.0/c*0.999  # on the cone edge-ish; x>=c y
        for n in range(1,60):
            s=G*(1 if rng.random()<0.5 else -1)
            x,y=x+s*y, x
            if x < c*y - 1e-12: ok=False
            worst=min(worst, x/ (c**n) if c**n>0 else 1e9)
    print(f" G={G}: cone c={c:.6f} invariant under all random schedules: {ok}; min x_n/s+^n over runs = {worst:.4f}")
