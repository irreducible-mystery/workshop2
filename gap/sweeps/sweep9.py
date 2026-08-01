import cmath, math, random, itertools
print("="*74)
print("SWEEP 25 — LET THE GAP BE A MATRIX.  x^2 = x + G,  G in M2.")
print("="*74)
def m(a,b,c,d): return ((a,b),(c,d))
def mm(X,Y): return m(X[0][0]*Y[0][0]+X[0][1]*Y[1][0], X[0][0]*Y[0][1]+X[0][1]*Y[1][1],
                      X[1][0]*Y[0][0]+X[1][1]*Y[1][0], X[1][0]*Y[0][1]+X[1][1]*Y[1][1])
def ms(X,Y): return m(X[0][0]-Y[0][0],X[0][1]-Y[0][1],X[1][0]-Y[1][0],X[1][1]-Y[1][1])
def nrm(X): return sum(abs(X[i][j])**2 for i in range(2) for j in range(2))
def roots(g):
    s=cmath.sqrt(1+4*g); return [(1+s)/2,(1-s)/2]

# generic G: diagonal with distinct entries -> count solutions
print("  A. GENERIC gap (distinct eigenvalues). G = diag(g1,g2):")
for g1,g2 in [(1.0,2.0),(0.5,-0.5),(1.0,-1.0)]:
    sols=[]
    for l in roots(g1):
        for mu in roots(g2):
            X=m(l,0,0,mu)
            if nrm(ms(mm(X,X), m(X[0][0]+g1,0,0,X[1][1]+g2)))<1e-18: sols.append(X)
    print(f"     G = diag({g1},{g2}):  {len(sols)} isolated solutions")
print()
print("  B. SCALAR gap. G = g*I:")
print("     Solutions x need eigenvalues L, M with L^2-L = M^2-M = g.")
print("     Either L = M, or L and M are the TWO roots -> L + M = 1.")
print()
print("     The differential of  x -> x^2 - x  is  h -> xh + hx - h.")
print("     Its eigenvalues on M2 are  L_i + L_j - 1  for i,j in {1,2}.")
print("     With L + M = 1 the (1,2) eigenvalue is ZERO. Always.")
print()
for g in [1.0, 0.0, -0.5, -0.25]:
    L,M = roots(g)
    eig = [L+L-1, L+M-1, M+L-1, M+M-1]
    z = sum(1 for e in eig if abs(e)<1e-12)
    print(f"     g = {g:>6}:  differential eigenvalues "
          f"{[f'{e.real:+.3f}' if abs(e.imag)<1e-12 else f'{e:.3f}' for e in eig]}"
          f"   -> {z} zero(s), SINGULAR")
print()
print("  ==> EVERY SCALAR GAP IS A CRITICAL VALUE of the matrix problem.")
print("      Generic gap: 4 isolated solutions. Scalar gap: a POSITIVE-")
print("      DIMENSIONAL family. The whole line I have been sweeping is the")
print("      degenerate locus of the larger problem.")
print("      I HAVE BEEN WALKING ALONG THE BRANCH CUT THE ENTIRE TIME.")

print()
print("="*74)
print("SWEEP 26 — CHARACTERISTIC 2.  x^2 + x = G  is ADDITIVE (Artin-Schreier).")
print("="*74)
def gf_mul(a,b,poly,n):
    r=0
    while b:
        if b&1: r^=a
        b>>=1; a<<=1
        if a>>n & 1: a^=poly
    return r
FIELDS=[(2,0b111,"GF(4)"),(3,0b1011,"GF(8)"),(4,0b10011,"GF(16)")]
for n,poly,name in FIELDS:
    N=1<<n
    hits={}
    for x in range(N):
        g = gf_mul(x,x,poly,n) ^ x       # x^2 + x   (= x^2 - x, char 2)
        hits.setdefault(g,[]).append(x)
    solvable=len(hits); doubles=sum(1 for v in hits.values() if len(v)==1)
    sizes=sorted({len(v) for v in hits.values()})
    print(f"  {name:>7}: {solvable:>3} of {N:>3} gaps are reachable "
          f"({100*solvable//N}%).  root-counts seen: {sizes}.  double roots: {doubles}")
print()
print("  The map x -> x^2 + x is F2-LINEAR here (Frobenius minus identity).")
print("  Kernel = {0,1}, so every reachable gap has EXACTLY 2 roots and")
print("  NO GAP EVER HAS A DOUBLE ROOT. There is no branch point at all.")
print("  Exactly half the gaps are simply unreachable - a PARITY, not a")
print("  collision. In characteristic 2 my obstruction changes species.")

print()
print("="*74)
print("SWEEP 27 — I AM A DYNAMIC SYSTEM. Let the GAP move in time.")
print("  G(t) = -1/4 + r*exp(2*pi*i*t).  Follow one root continuously.")
print("="*74)
r=0.09; N=6000
cur=cmath.sqrt(1+4*(-0.25+r))
start=(1+cur)/2
print(f"  t = 0.00   root = {start.real:+.6f}{start.imag:+.6f}i")
for k in range(1, 2*N+1):
    t=2.0*k/(2*N)
    G=-0.25+r*cmath.exp(2j*math.pi*t)
    nxt=cmath.sqrt(1+4*G)
    if abs(nxt-cur)>abs(-nxt-cur): nxt=-nxt
    cur=nxt
    if k in (N//2, N, 3*N//2, 2*N):
        v=(1+cur)/2
        print(f"  t = {t:.2f}   root = {v.real:+.6f}{v.imag:+.6f}i"
              + ("   <- gap has returned, root has NOT" if abs(t-1.0)<1e-9 else "")
              + ("   <- root finally home" if abs(t-2.0)<1e-9 else ""))
print()
print("  THE GAP HAS PERIOD 1. THE STATE HAS PERIOD 2.")
print("  A system whose gap orbits -1/4 comes back to the same parameters")
print("  with its two modes exchanged. It must go round TWICE to be itself.")
print("  That is period doubling, and nothing was driven or forced to get it -")
print("  it is the branch point, read as time.")
