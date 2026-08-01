import math, random, cmath, collections
print("="*76)
print("SWEEP 44b — sitting exactly ON the branch point")
print("="*76)
cat=[1]
for n in range(1,4000): cat.append(cat[-1]*2*(2*n-1)//(n+1))
for k in (10,100,1000,3000):
    s=0.0
    for n in range(1,k+1):
        t=math.exp(math.log(cat[n-1])-n*math.log(4.0)) if cat[n-1]>0 else 0.0
        if t==0: break
        s+=t
    print(f"    partial sum of C_(n-1)/4^n up to n={k:>5}:  {s:.8f}")
print("    limit is exactly 1/2.  The series CONVERGES on its own radius,")
print("    but the derivative sum C_(n-1)*n/4^n DIVERGES:")
for k in (10,100,1000,3000):
    s=sum(math.exp(math.log(cat[n-1])+math.log(n)-n*math.log(4.0)) for n in range(1,k+1))
    print(f"    derivative partial sum up to n={k:>5}:  {s:.4f}")
print("    The critical tree is exactly reachable and infinitely sensitive.")
print("    Value finite. Slope infinite. That is what a branch point feels like")
print("    from inside the thing it is counting.")

print()
print("="*76)
print("SWEEP 45 — LET THE GAP DIFFUSE. Brownian motion in the G-plane.")
print("  Winding parity around -1/4 decides WHICH ROOT you come home holding.")
print("="*76)
rnd=random.Random(45)
def winding(T, steps, start=complex(0.75,0.0)):
    dt=T/steps; sd=math.sqrt(dt); z=start; w=0.0
    prev=cmath.phase(z+0.25)
    for _ in range(steps):
        z += complex(rnd.gauss(0,sd), rnd.gauss(0,sd))
        cur=cmath.phase(z+0.25); d=cur-prev
        while d> math.pi: d-=2*math.pi
        while d<-math.pi: d+=2*math.pi
        w+=d; prev=cur
    return w/(2*math.pi)
for T,steps,runs in [(10.0,40000,300),(200.0,200000,300)]:
    wind=[int(round(winding(T,steps))) for _ in range(runs)]
    c=collections.Counter(wind)
    odd=sum(v for k,v in c.items() if k%2)
    print(f"  T={T:>6}, {runs} paths:  windings {dict(sorted(c.items()))}")
    print(f"           SWAPPED (odd winding) = {odd}/{runs} = {odd/runs:.3f}")
print()
print("  As the gap wanders longer, the parity approaches a fair coin.")
print("  A system whose gap diffuses comes home with its chirality decided by")
print("  a flip nobody performed. G alone cannot reconstruct it - only the path can.")

print()
print("="*76)
print("SWEEP 46 — TILT THE MIXTURE. p = P(G=+1), else G=-1.")
print("="*76)
def growth(p, trials=10, N=20000, seed=1):
    r=random.Random(seed); tot=0.0
    for _ in range(trials):
        a,b=1.0,1.0; s=0.0
        for _ in range(N):
            G = 1.0 if r.random()<p else -1.0
            cc=b+G*a; a,b=b,cc; m=abs(b)
            if m>1e8 or (0<m<1e-8): s+=math.log(m); a/=m; b/=m
        s+=math.log(abs(b)); tot+=s/N
    return math.exp(tot/trials)
print(f"{'p':>6} {'growth':>12}   {'chord (1-p)*1 + p*phi':>24}   gap")
phi=(1+math.sqrt(5))/2
for p in [0.0,0.1,0.25,0.4,0.5,0.6,0.75,0.9,1.0]:
    g=growth(p); ch=(1-p)*1.0+p*phi
    print(f"{p:>6} {g:>12.6f}   {ch:>24.6f}   {g-ch:+.6f}")
print()
print("  Every interior point lies BELOW the chord. Mixing my gaps is strictly")
print("  worse than averaging them. Randomness costs growth - and at p=1/2 the")
print("  cost is exactly the gap between 1.3090 and Viswanath's 1.1320.")
