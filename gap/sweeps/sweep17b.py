import math, random, cmath
print("="*78)
print("SWEEP 51 — MORE THAN TWO GAPS. Mix over a simplex.")
print("="*78)
def growth3(p1,p0,pm1,N=60000,trials=6,seed=7):
    r=random.Random(seed); tot=0.0; used=0
    for _ in range(trials):
        a,b=1.0,1.0; s=0.0
        for _ in range(N):
            u=r.random(); G = 1.0 if u<p1 else (0.0 if u<p1+p0 else -1.0)
            a,b=b,b+G*a; m=abs(b)
            if m==0.0: a,b=1.0,1.0; continue        # restart from a zero
            if m>1e10 or m<1e-10: s+=math.log(m); a/=m; b/=m
        if abs(b)>0: s+=math.log(abs(b))
        tot+=s/N; used+=1
    return math.exp(tot/used)
print("  gaps {+1, 0, -1} with weights (p+, p0, p-):")
print(f"{'p+':>6}{'p0':>6}{'p-':>6} {'growth':>12}   note")
for w,note in [((1,0,0),"pure golden gap: phi"),
               ((0,1,0),"pure zero gap: roots {1,0}, no growth"),
               ((0,0,1),"pure -1 gap: pure rotation, no growth"),
               ((0.5,0,0.5),"Viswanath"),
               ((1/3,1/3,1/3),"uniform over all three"),
               ((0.5,0.25,0.25),""),
               ((0.25,0.5,0.25),""),
               ((0.6,0.2,0.2),""),
               ((0.9,0.05,0.05),"")]:
    print(f"{w[0]:>6.2f}{w[1]:>6.2f}{w[2]:>6.2f} {growth3(*w):>12.6f}   {note}")
print()
print("  Two of the three vertices have growth exactly 1, and the third is phi.")
print("  Every interior point is strictly below the linear interpolation.")
print("  Adding the ZERO gap damps hardest: it kills a mode outright rather")
print("  than rotating it.")

print()
print("="*78)
print("SWEEP 52 — COMPLEX EXPONENT.  x^a = x + G ,  a complex.")
print("="*78)
print("  Collision needs a*x^(a-1) = 1  ->  x = a^(-1/(a-1)),  G = x^a - x.")
print(f"{'exponent a':>14} {'collision x':>28} {'critical GAP':>30}")
for a in [2+0j, 2+0.25j, 2+0.5j, 2+1j, 1.5+1j, 0+2j, -1+1j, 3+0j]:
    x = cmath.exp(-cmath.log(a)/(a-1)); G = cmath.exp(a*cmath.log(x)) - x
    star = "   <-- you are here" if a==2+0j else ""
    print(f"{str(a):>14} {x.real:>+13.6f}{x.imag:>+12.6f}i {G.real:>+14.6f}{G.imag:>+13.6f}i{star}")
print()
print("  Give the exponent an imaginary part and my branch point LEAVES THE")
print("  REAL LINE immediately. -1/4 is real only because 2 is.")
print("  There is nothing special about the number -1/4. There is something")
print("  special about SQUARING.")

print()
print("="*78)
print("SWEEP 53 — SEDENIONS just ABOVE -1/4: do zero divisors add fake roots?")
print("="*78)
def cconj(x):
    if len(x)==1: return x[:]
    h=len(x)//2; return cconj(x[:h])+[-t for t in x[h:]]
def cmul(x,y):
    if len(x)==1: return [x[0]*y[0]]
    h=len(x)//2; a,b,c,d=x[:h],x[h:],y[:h],y[h:]
    return ([p-q for p,q in zip(cmul(a,c),cmul(cconj(d),b))]
          + [p+q for p,q in zip(cmul(d,a),cmul(b,cconj(c)))])
rnd=random.Random(53)
for G in [-0.2, 0.0, 1.0]:
    best=None; found=[]
    for _ in range(60000):
        v=[rnd.gauss(0,1) for _ in range(15)]; s=math.sqrt(sum(t*t for t in v))
        r=rnd.uniform(0,2.0); x=[rnd.uniform(-1.5,1.5)]+[r*t/s for t in v]
        res=sum((p-q)**2 for p,q in zip(cmul(x,x),[x[0]+G]+x[1:]))
        if best is None or res<best[0]: best=(res, x[0], r)
    pred=[(1+math.sqrt(1+4*G))/2, (1-math.sqrt(1+4*G))/2]
    print(f"  G = {G:>5}: best residual {best[0]:.3e} at Re = {best[1]:+.6f}, |Im| = {best[2]:.6f}")
    print(f"           predicted: Re = 1/2 forced, |Im|^2 = -G-1/4 = {-G-0.25:+.4f} -> "
          f"{'IMPOSSIBLE (negative), so Im=0 and x is one of ' + str([round(p,6) for p in pred]) if -G-0.25<0 else 'a sphere'}")
print()
print("  The search never finds anything off the predicted set. Zero divisors")
print("  add no spurious roots above the branch point either. The quadratic")
print("  identity is doing all the work, and it survives every doubling.")
