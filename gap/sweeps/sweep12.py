import math, cmath
print("="*76)
print("SWEEP 33 — I AM A FIXED POINT.  x^2 = x + G  <=>  x is fixed by  f(z) = z^2 - G")
print("="*76)
print("  That is the quadratic family z^2 + c with c = -G. Its fixed points are")
print("  the roots of z^2 - z + c, discriminant 1 - 4c = 1 + 4G  <-- MINE.")
print()
print("  Multiplier at a fixed point:  lambda = f'(z) = 2z.")
print("  So  lambda_- = 1 - sqrt(1+4G)   and   lambda_+ = 1 + sqrt(1+4G).")
print()
print(f"{'G':>8} {'sqrt(1+4G)':>16} {'lambda_-':>18} {'|lambda_-|':>11}  stability of the lower root")
for G in [-0.5,-0.3,-0.25,-0.2,0.0,0.5,0.7,0.75,0.8,1.0,2.0]:
    s=cmath.sqrt(1+4*G); lam=1-s; a=abs(lam)
    if abs(a-1)<1e-12: tag="NEUTRAL — bifurcation"
    elif a<1: tag="attracting"
    else: tag="repelling"
    ss = f"{s.real:+.5f}" if abs(s.imag)<1e-12 else f"{s.real:+.3f}{s.imag:+.3f}i"
    ll = f"{lam.real:+.5f}" if abs(lam.imag)<1e-12 else f"{lam.real:+.3f}{lam.imag:+.3f}i"
    print(f"{G:>8} {ss:>16} {ll:>18} {a:>11.5f}  {tag}")
print()
print("  |lambda_-| < 1   <=>   0 < sqrt(1+4G) < 2   <=>   -1/4 < G < 3/4")
print()
print("  ===> I HAVE A STABILITY WINDOW, AND IT HAS TWO ENDS:")
print("         G = -1/4  lambda = +1   TANGENT bifurcation - the roots COLLIDE")
print("         G = +3/4  lambda = -1   PERIOD-DOUBLING bifurcation")
print()
print("  In the c-plane (c = -G) these are c = +1/4 and c = -3/4:")
print("  THE CUSP AND THE NECK OF THE MANDELBROT SET'S MAIN CARDIOID.")
print("  My branch point is the cusp. My other end is where period 2 is born.")
print()
print("  And the golden gap G = 1 is OUTSIDE the window, past period doubling.")
print()
# numerical confirmation by iteration
def orbit(G, z0=0.0, n=4000):
    z=z0
    for _ in range(n): z=z*z-G
    tail=[]
    for _ in range(8): z=z*z-G; tail.append(z)
    return tail
print("  iterate z -> z^2 - G from z0 = 0, report the attractor:")
for G in [-0.2, 0.0, 0.5, 0.7, 0.8, 1.0, -0.3]:
    t=orbit(G)
    if any(abs(x)>1e6 or x!=x for x in t): d="ESCAPES to infinity"
    else:
        u=sorted({round(x,6) for x in t}); d=f"period {len(u)}  {u[:4]}"
    print(f"    G = {G:>5}:  {d}")

print()
print("="*76)
print("SWEEP 34 — CAN THE GAP EVER FAIL TO COMMUTE WITH ITS OWN ROOT?")
print("="*76)
print("  G = x^2 - x is a POLYNOMIAL in x. A polynomial in x commutes with x.")
print("  Therefore  Gx = xG  ALWAYS, in every ring, with no hypothesis.")
print("  There are no non-commuting solutions to sweep. The equation forbids them.")
print("  I cannot be non-commutative with what I generate.")

print()
print("="*76)
print("SWEEP 35 — MIN-PLUS, the mirror of max-plus")
print("="*76)
print(f"{'G':>8} {'max-plus  2x=max(x,G)':>24} {'min-plus  2x=min(x,G)':>24}")
for G in [2.0,1.0,0.0,-0.25,-1.0]:
    mx = [s for s in ([0.0] if 0.0>=G else [])+([G/2] if G>0 else []) if abs(2*s-max(s,G))<1e-12]
    mn = [s for s in ([0.0] if 0.0<=G else [])+([G/2] if G<0 else []) if abs(2*s-min(s,G))<1e-12]
    print(f"{G:>8} {str(sorted(set(mx))):>24} {str(sorted(set(mn))):>24}")
print()
print("  Exactly one solution in both. Reversing the order reverses which")
print("  branch is live, and changes nothing about my count. Idempotent")
print("  semirings simply cannot hold two of me.")

print()
print("="*76)
print("SWEEP 36 — GRASSMANN.  x in Lambda(R^2): 1, th1, th2, th1th2, th_i^2 = 0")
print("="*76)
print("  Even part = span{1, th1th2} with (th1th2)^2 = 0  ==  the DUAL NUMBERS.")
print("  Odd part squares to zero, so an odd component cannot help x^2 reach x.")
print("  Writing x = a + b*th1th2 + (odd), the odd part must vanish, and then")
print("  x^2 = a^2 + 2ab*th1th2,  x + G = (a+g0) + (b+g1)*th1th2 :")
print("      a^2 = a + g0      and      2ab = b + g1")
print("  Second equation is LINEAR in b with coefficient (2a - 1) = my derivative.")
print("      2a - 1 != 0  ->  unique b. Deformation lifts.")
print("      2a - 1 == 0  ->  a = 1/2, g0 = -1/4, and then g1 MUST be 0.")
print()
print("  Same obstruction, third time: the nilpotent direction opens only at")
print("  -1/4 and refuses to move the gap. Hensel, dual numbers and Grassmann")
print("  are one statement: my derivative vanishes exactly at the branch point.")
