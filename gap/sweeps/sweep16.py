import math, cmath
from fractions import Fraction as F
print("="*78)
print("SWEEP 47 — REFLEXIVE FIXED POINTS. Where does the GAP equal something of its own?")
print("="*78)
def roots(G):
    s=cmath.sqrt(1+4*G); return (1+s)/2,(1-s)/2
tests=[]
print("  My roots always satisfy   s+ + s- = 1   and   s+ * s- = -G .")
print()
print("  (a) GAP = SUM of its roots      ->   G = 1")
print("      the sum is always 1, so this is one equation with one answer.")
sp,sm=roots(1.0); print(f"      G = 1: roots {sp.real:.6f}, {sm.real:.6f}, sum {sp.real+sm.real:.6f}")
print("      ==> THE GOLDEN GAP IS THE SELF-REFERENTIAL ONE.")
print("          phi + psi = 1 is not a side fact. It is the equation G = s+ + s-.")
print()
print("  (b) GAP = PRODUCT of its roots  ->   G = -G   ->   G = 0")
sp,sm=roots(0.0); print(f"      G = 0: roots {sp.real:.6f}, {sm.real:.6f}, product {(sp*sm).real:.6f}")
print()
print("  (c) GAP IS one of its own roots ->   G^2 = G + G   ->   G = 0 or G = 2")
for G in [0.0,2.0]:
    sp,sm=roots(G)
    print(f"      G = {G}: roots {sp.real:+.6f}, {sm.real:+.6f}   is G a root? "
          f"{abs(G-sp.real)<1e-12 or abs(G-sm.real)<1e-12}")
print()
print("  (d) GAP = DIFFERENCE of its roots = sqrt(1+4G) ->  G^2 = 1+4G -> G = 2 +- sqrt5")
phi=(1+math.sqrt(5))/2
for G in [2+math.sqrt(5), 2-math.sqrt(5)]:
    d=cmath.sqrt(1+4*G)
    print(f"      G = {G:+.6f}:  sqrt(1+4G) = {d.real:+.6f}{d.imag:+.6f}i   G-difference = {abs(G-d.real):.2e}")
print(f"      and 2+sqrt(5) = {2+math.sqrt(5):.6f} = phi^3 = {phi**3:.6f}")
print()
print("  (e) GAP = its own DISCRIMINANT 1+4G  ->  G = -1/3")
G=-1/3.0; print(f"      G = -1/3: 1+4G = {1+4*G:+.6f}   equal? {abs(G-(1+4*G))<1e-12}")
print("      and -1/3 is the ROTATION-NUMBER-6 gap from sweep 38.")
print()
print("  (f) GAP = my branch point  ->  G = -1/4, the only place I cannot tell")
print("      my two roots apart at all.")
print()
print("  THE REFLEXIVE LADDER:   -1/3   -1/4   0   1   2   phi^3")
print("  and G = 1 - the one you handed me - is exactly 'the gap is the sum of")
print("  what it produces'.")

print()
print("="*78)
print("SWEEP 48 — TRIGONOMETRIC. Force the root to be a quantum dimension 2cos(theta).")
print("="*78)
print("  d = 2cos(theta),  G = d^2 - d = 4cos^2 - 2cos.  Put u = cos(theta) in [-1,1]:")
print(f"{'theta/pi':>10} {'d = 2cos':>10} {'G':>12}")
for k in [0, 1/6, 1/5, 1/4, 1/3, 0.4193, 1/2, 2/3, 4/5, 1]:
    th=k*math.pi; d=2*math.cos(th); G=d*d-d
    tag = "  <-- G minimal = -1/4" if abs(math.cos(th)-0.25)<2e-3 else ("  <-- Fibonacci, G=1" if abs(G-1)<1e-6 else "")
    print(f"{k:>10.4f} {d:>10.6f} {G:>12.6f}{tag}")
print()
print("  G(u) = 4u^2 - 2u has its vertex at u = 1/4, value 4/16 - 1/2 = -1/4.")
print("  The floor arrives again, now from trigonometry, and the minimising")
print("  angle is arccos(1/4) - a number that is not a rational multiple of pi.")
print("  My branch point is not at any root of unity. It sits between them.")

print()
print("="*78)
print("SWEEP 49 — INTEGER GAPS ARE SHIFT SPACES. Entropy.")
print("="*78)
print("  Adjacency matrix M = [[1,1],[G,0]] has characteristic polynomial x^2 - x - G.")
print("  So my larger root is the growth rate of a walk, and log(root) is its entropy.")
print(f"{'G':>4} {'s+':>12} {'entropy log s+':>16}   shift")
for G,name in [(1,"golden mean shift - no two consecutive 1s"),
               (2,"                                        "),
               (3,"                                        "),
               (6,"                                        ")]:
    sp,_=roots(float(G))
    print(f"{G:>4} {sp.real:>12.8f} {math.log(sp.real):>16.8f}   {name}")
print()
print("  G = 1 gives entropy log(phi) = 0.4812118251, the golden mean shift.")
print("  Non-integer or negative G has no such counting model: below -1/4 the")
print("  'growth rate' is complex and there is nothing to count.")
print("  ==> ABOVE -1/4 I CAN BE A COUNTING PROBLEM. BELOW IT I CANNOT.")
