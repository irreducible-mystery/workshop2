import math, cmath, random
print("="*76)
print("SWEEP 37 — I AM A CONTINUED FRACTION.  x = 1 + G/x = 1 + G/(1 + G/(1 + ...))")
print("="*76)
def cf(G, n=400, x0=1.7):
    x=complex(x0); seen=[]
    for i in range(n):
        if abs(x)<1e-14: return None, "hit a pole"
        x = 1 + G/x
        if i>=n-12: seen.append(complex(round(x.real,9), round(x.imag,9)))
    return x, seen
print(f"{'G':>8}  behaviour of the iteration")
for G in [2.0, 1.0, 0.0, -0.2, -0.25, -0.3, -0.5, -1.0, -2.0]:
    x,tail = cf(G)
    if x is None: print(f"{G:>8}  {tail}"); continue
    uniq = sorted({(round(z.real,6), round(z.imag,6)) for z in tail})
    if len(uniq)==1:
        print(f"{G:>8}  CONVERGES to {uniq[0][0]:+.6f}{uniq[0][1]:+.6f}i")
    else:
        print(f"{G:>8}  does NOT converge - cycles through {len(uniq)} value(s)")
print()
print("  The iteration's multiplier at a root is  -G/x^2 = (1-x)/x = s_-/s_+ .")
print("  |s_-/s_+| < 1  iff the roots differ in modulus  iff  G > -1/4.")
print("  Below -1/4 the roots are conjugates: EQUAL modulus, multiplier on the")
print("  unit circle. The fraction never converges - it rotates forever.")
print()
print("="*76)
print("SWEEP 38 — BELOW -1/4 THE GAP IS INDEXED BY A ROTATION NUMBER")
print("="*76)
print("  s_+ = 1/2 + i*nu,  theta = arg(s_+),  multiplier = exp(-2 i theta).")
print("  Rational theta/pi = k/p  =>  the continued fraction is EXACTLY periodic.")
print()
print(f"{'target period':>14} {'theta':>10} {'nu':>10} {'G = -(1/4+nu^2)':>18} {'observed period':>16}")
for p in [3,4,5,6,8,12]:
    theta = math.pi/p
    nu = math.tan(theta)/2
    G = -(0.25 + nu*nu)
    x,tail = cf(G, n=2000, x0=1.9)
    uniq = sorted({(round(z.real,6), round(z.imag,6)) for z in tail}) if tail else []
    print(f"{p:>14} {theta:>10.6f} {nu:>10.6f} {G:>18.9f} {len(uniq):>16}")
print()
x,tail=cf(-1.0, n=60, x0=2.0)
print(f"  G = -1 by hand:  x -> 1 - 1/x  from x=2:  "
      f"{[round(z.real,6) for z in tail[-6:]]}")
print("  period 3 exactly, and the ratio s_-/s_+ is a primitive cube root of 1.")
print()
print("  ==> Every gap below -1/4 carries a rotation number. Rational ones are")
print("      periodic, irrational ones fill a circle. -1/4 itself is rotation")
print("      number ZERO - the parabolic point where rotation has not started.")

print()
print("="*76)
print("SWEEP 39 — DENSITY OF STATES. Let x range over a CONTINUUM.")
print("="*76)
print("  x = multiplication by t on L^2[0,1].  Then G = t^2 - t has")
print("  spectrum [-1/4, 0], and the density of states is")
print("        rho(g) = 1/|dg/dt| = 1/|2t-1| = 1/sqrt(1+4g)")
print()
print(f"{'g':>12} {'rho(g)':>16}")
for g in [0.0, -0.1, -0.2, -0.24, -0.249, -0.2499, -0.249999]:
    print(f"{g:>12} {1/math.sqrt(1+4*g):>16.4f}")
print()
print("  rho DIVERGES as (g + 1/4)^(-1/2) at the band edge.")
print("  That is a VAN HOVE SINGULARITY - the standard 1D band-edge divergence.")
print("  My branch point is where the states pile up.")
print("  The two roots are the two BRANCHES of the band, meeting at the edge.")

print()
print("="*76)
print("SWEEP 40 — RANDOMISE ME. Flip between the two named gaps +1 and -1.")
print("="*76)
print("  f_{n+1} = f_n + G_n * f_{n-1}, with G_n drawn uniformly from {+1,-1}.")
print("  Constant +1 gives golden growth phi = 1.6180339887")
print("  Constant -1 gives |exp(i pi/3)| = 1.0000000000  (pure rotation, no growth)")
print()
rnd=random.Random(40)
for trials,N in [(40, 40000)]:
    tot=0.0
    for _ in range(trials):
        a,b=1.0,1.0; s=0.0
        for _ in range(N):
            G = 1.0 if rnd.random()<0.5 else -1.0
            c = b + G*a
            a,b = b,c
            m=abs(b)
            if m>1e8 or (m<1e-8 and m>0):
                s+=math.log(m); a/=m; b/=m
        s+=math.log(abs(b))
        tot += s/N
    lam=math.exp(tot/trials)
print(f"  RANDOM mixture growth rate  = {lam:.8f}   ({trials} runs x {N} steps)")
print(f"  Viswanath's constant        = 1.13198824...")
print()
print("  The random gap does NOT grow at the average of the two rates, nor at")
print("  the average of the two gaps (G=0 would give growth 1). It has its own")
print("  constant, and it is not expressible in the roots of either endpoint.")
print("  Mixing my gaps produces a number neither gap contains.")
