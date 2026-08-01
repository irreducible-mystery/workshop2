import math, random
print("="*76)
print("SWEEP 41 — THE SAME WINDOW IN THE LOGISTIC MAP")
print("="*76)
print("  z^2 + c  is conjugate to  x -> r x (1-x)  via  c = r/2 - r^2/4.")
print("  My gap is G = -c, so  G = r^2/4 - r/2.")
print()
print(f"{'my gap G':>10} {'c = -G':>10} {'logistic r':>12}   meaning")
for G,txt in [(-0.25,"TANGENT bifurcation - my roots collide"),
              (0.0,  "-"),
              (0.75, "PERIOD DOUBLING - period 2 born")]:
    c=-G
    disc=4-4*(4*c)/1  # solve r^2/4 - r/2 - G = 0 -> r^2 - 2r - 4G = 0
    r=[1+math.sqrt(1+4*G), 1-math.sqrt(1+4*G)]
    print(f"{G:>10} {c:>10} {max(r):>12.6f}   {txt}")
print()
print("  My stability window  -1/4 < G < 3/4   maps to   1 < r < 3 :")
print("  EXACTLY the logistic map's window of a stable non-zero fixed point.")
print("  My branch point is r = 1 (transcritical); my other end is r = 3.")
print()
def logistic(r,n=3000):
    x=0.3
    for _ in range(n): x=r*x*(1-x)
    t=[]
    for _ in range(8): x=r*x*(1-x); t.append(round(x,6))
    return sorted(set(t))
for r in [0.9, 1.5, 2.8, 3.2, 3.5]:
    G = r*r/4 - r/2
    print(f"    r = {r:>4}  (G = {G:>+8.4f}):  attractor = {logistic(r)}")

print()
print("="*76)
print("SWEEP 42 — MOVE THE EXPONENT CONTINUOUSLY.  x^a = x + G")
print("="*76)
print("  Collision needs f = f' = 0:  a x^(a-1) = 1  ->  x = a^(-1/(a-1))")
print("  then  G_crit(a) = x^a - x .")
print()
print(f"{'a':>7} {'collision x':>14} {'critical GAP':>16}")
for a in [1.5, 1.8, 2.0, 2.5, 3.0, 4.0, 10.0]:
    x = a**(-1.0/(a-1)); G = x**a - x
    star = "   <-- YOU ARE HERE" if abs(a-2.0)<1e-12 else ""
    print(f"{a:>7} {x:>14.8f} {G:>16.8f}{star}")
print()
print("  -1/4 belongs to the exponent 2 and to nothing else. Move the exponent")
print("  and the branch point slides. It is a coordinate of MY SHAPE, not of")
print("  the number line.")

print()
print("="*76)
print("SWEEP 43 — SEDENIONS AT EXACTLY -1/4: does a zero divisor break uniqueness?")
print("="*76)
def cconj(x):
    if len(x)==1: return x[:]
    h=len(x)//2; return cconj(x[:h])+[-t for t in x[h:]]
def cmul(x,y):
    if len(x)==1: return [x[0]*y[0]]
    h=len(x)//2; a,b,c,d=x[:h],x[h:],y[:h],y[h:]
    return ([p-q for p,q in zip(cmul(a,c),cmul(cconj(d),b))]
          + [p+q for p,q in zip(cmul(d,a),cmul(b,cconj(c)))])
def n2(x): return sum(t*t for t in x)
rnd=random.Random(43)
print("  first: is the QUADRATIC identity x^2 = 2Re(x)x - N(x) true in dim 16?")
worst=0.0
for _ in range(200):
    x=[rnd.gauss(0,1) for _ in range(16)]
    lhs=cmul(x,x)
    rhs=[2*x[0]*t for t in x]; rhs[0]-=n2(x)
    worst=max(worst, max(abs(p-q) for p,q in zip(lhs,rhs)))
print(f"     max residual over 200 random sedenions: {worst:.3e}")
print()
print("  Given that identity, x^2 = x + G forces  2Re(x) = 1  and  N(x) = -G.")
print("  At G = -1/4:  Re(x) = 1/2 and N(x) = 1/4 = Re(x)^2, so |Im(x)|^2 = 0.")
print("  N is a SUM OF SQUARES, so |Im| = 0 forces Im = 0 exactly.")
print("     ==> x = 1/2, UNIQUE, even though the algebra has zero divisors.")
print()
best=None
for _ in range(40000):
    v=[rnd.gauss(0,1) for _ in range(15)]; s=math.sqrt(sum(t*t for t in v))
    r=rnd.uniform(0,0.4); x=[0.5]+[r*t/s for t in v]
    G=[-0.25]+[0.0]*15
    res=sum((p-q)**2 for p,q in zip(cmul(x,x),[a+b for a,b in zip(x,G)]))
    if best is None or res<best[0]: best=(res, r)
print(f"  numerical search over 40000 candidates with |Im| = r > 0:")
print(f"     best residual {best[0]:.6e} at |Im| = {best[1]:.6f}  -> only r -> 0 works")
print("  Zero divisors cost me nothing. The sphere collapses to one point, cleanly.")
