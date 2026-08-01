from fractions import Fraction as F
import math, random, cmath
print("="*76)
print("SWEEP 44 — I AM A COUNTING SERIES.  Expand my root as a power series in G.")
print("="*76)
# y = (1 - sqrt(1+4G))/2 ,  put x = -G  ->  y = (1 - sqrt(1-4x))/2
N=14
# binomial series for sqrt(1-4x) = sum_k C(1/2,k) (-4x)^k
def binom_half(k):
    r=F(1)
    for i in range(k): r*= (F(1,2)-i)/(i+1)
    return r
coef=[ -binom_half(k)*F((-4)**k)/2 for k in range(N+1) ]
coef[0]= (F(1)-F(1))/2 + (1-1)/2  # constant term of y is 0
coef[0]=F(0)
print("  y = (1 - sqrt(1 - 4x))/2   expanded in x = -G :")
print("   ", "  ".join(str(coef[k]) for k in range(1,N)))
cat=[1]
for n in range(1,N): cat.append(cat[-1]*2*(2*n-1)//(n+1))
print("  Catalan numbers C_0..C_%d:"%(N-2))
print("   ", "  ".join(str(c) for c in cat[:N-1]))
ok = all(coef[n]==cat[n-1] for n in range(1,N))
print(f"\n  do my series coefficients equal the Catalan numbers?  {ok}")
print()
print("  ==> MY ROOT IS THE GENERATING FUNCTION THAT COUNTS BINARY TREES.")
print("      x*C(x) where C = 1 + x C^2.  The gap G is minus the tree weight.")
print()
print("  Radius of convergence = distance to my branch point = 1/4.")
print(f"  coefficient ratios C_n/C_(n-1):  " +
      "  ".join(f"{cat[n]/cat[n-1]:.4f}" for n in range(6,N-1)))
print("  -> 4 = 1/(1/4).  THE 4^n IN THE CATALAN ASYMPTOTIC *IS* MY BRANCH POINT.")
print("  And the square-root branch is why the correction is n^(-3/2).")
print()
print("  At G = -1/4 exactly (x = 1/4) the series sits ON its radius:")
s=sum(F(cat[n-1],4**n) for n in range(1,400)) if False else None
tot=0.0
for n in range(1,200001):
    pass
part=[sum(cat[n-1]/4**n for n in range(1,k+1)) for k in (10,100,1000)]
print(f"     partial sums at x=1/4: {part[0]:.6f}, {part[1]:.6f}, {part[2]:.6f}  -> 1/2")
print("     it CONVERGES, but only just, and its derivative blows up.")
print("     The critical tree is exactly reachable and infinitely sensitive.")

print()
print("="*76)
print("SWEEP 45 — LET THE GAP DIFFUSE. Brownian motion in the G-plane.")
print("="*76)
print("  G(t) is 2D Brownian. Count how many times it winds around -1/4.")
print("  Winding parity decides WHICH ROOT you come back holding.")
print()
rnd=random.Random(45)
def winding(T=40.0, steps=200000, start=complex(0.75,0.0)):
    dt=T/steps; sd=math.sqrt(dt); z=start; w=0.0
    prev=cmath.phase(z-(-0.25))
    for _ in range(steps):
        z += complex(rnd.gauss(0,sd), rnd.gauss(0,sd))
        cur=cmath.phase(z-(-0.25))
        d=cur-prev
        while d> math.pi: d-=2*math.pi
        while d<-math.pi: d+=2*math.pi
        w+=d; prev=cur
    return w/(2*math.pi)
runs=[winding() for _ in range(400)]
wind=[int(round(w)) for w in runs]
even=sum(1 for k in wind if k%2==0); odd=len(wind)-even
import collections
c=collections.Counter(wind)
print(f"  400 Brownian gap-paths, T=40:")
print(f"    winding numbers seen: {dict(sorted(c.items()))}")
print(f"    EVEN winding (root preserved): {even}   ODD winding (root SWAPPED): {odd}")
print(f"    fraction swapped = {odd/len(wind):.3f}")
print()
print("  A gap that wanders comes home with its chirality decided by a coin")
print("  it never saw flipped. The parity is the coin. Nothing measured it,")
print("  nothing chose it, and the system cannot reconstruct it from G alone.")

print()
print("="*76)
print("SWEEP 46 — TILT THE RANDOM MIXTURE. p = P(G = +1), else G = -1.")
print("="*76)
def growth(p, trials=12, N=20000, seed=1):
    r=random.Random(seed); tot=0.0
    for _ in range(trials):
        a,b=1.0,1.0; s=0.0
        for _ in range(N):
            G = 1.0 if r.random()<p else -1.0
            c=b+G*a; a,b=b,c; m=abs(b)
            if m>1e8 or (0<m<1e-8): s+=math.log(m); a/=m; b/=m
        s+=math.log(abs(b)); tot+=s/N
    return math.exp(tot/trials)
print(f"{'p':>6} {'growth rate':>14}")
for p in [0.0,0.1,0.25,0.4,0.5,0.6,0.75,0.9,1.0]:
    print(f"{p:>6} {growth(p):>14.6f}")
print()
print("  p=0 -> 1.0 (pure rotation), p=1 -> phi. Monotone in between, and it")
print("  passes through Viswanath at p = 1/2. The curve is not a chord: mixing")
print("  gaps is not averaging gaps.")
