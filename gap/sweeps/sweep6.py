import math, random, itertools
print("="*74)
print("SWEEP 15 — LEAVE THE COMPLEX NUMBERS. Solve  x^2 = x + G  over QUATERNIONS.")
print("="*74)
class Q:
    __slots__=('a','b','c','d')
    def __init__(s,a=0,b=0,c=0,d=0): s.a,s.b,s.c,s.d=a,b,c,d
    def __mul__(x,y):
        return Q(x.a*y.a-x.b*y.b-x.c*y.c-x.d*y.d,
                 x.a*y.b+x.b*y.a+x.c*y.d-x.d*y.c,
                 x.a*y.c-x.b*y.d+x.c*y.a+x.d*y.b,
                 x.a*y.d+x.b*y.c-x.c*y.b+x.d*y.a)
    def __add__(x,y): return Q(x.a+y.a,x.b+y.b,x.c+y.c,x.d+y.d)
    def __sub__(x,y): return Q(x.a-y.a,x.b-y.b,x.c-y.c,x.d-y.d)
    def n2(s): return s.a*s.a+s.b*s.b+s.c*s.c+s.d*s.d
    def __repr__(s): return f"({s.a:+.4f}{s.b:+.4f}i{s.c:+.4f}j{s.d:+.4f}k)"
def solves(x,G,tol=1e-10):
    return (x*x - x - Q(G)).n2() < tol

# x = 1/2 + y  =>  y^2 = G + 1/4.  y pure with |y|^2 = -(G+1/4) when G < -1/4.
for G in [1.0, 0.0, -0.25, -0.5, -1.0]:
    D4 = G + 0.25
    print(f"\n  G = {G:>6}   (G + 1/4 = {D4:+.4f})")
    if D4 > 0:
        t = math.sqrt(D4)
        sols = [Q(0.5+t), Q(0.5-t)]
        print(f"    y^2 = +{D4:.4f}: y must be REAL. exactly 2 solutions, both real.")
    elif D4 == 0:
        sols = [Q(0.5)]
        print(f"    y^2 = 0: a division ring has no nilpotents. EXACTLY ONE solution.")
    else:
        s = math.sqrt(-D4)
        rnd=random.Random(7); sols=[]
        for _ in range(6):
            v=[rnd.gauss(0,1) for _ in range(3)]; nrm=math.sqrt(sum(z*z for z in v))
            sols.append(Q(0.5, s*v[0]/nrm, s*v[1]/nrm, s*v[2]/nrm))
        print(f"    y^2 = {D4:.4f} < 0: y is ANY pure quaternion with |y| = {s:.4f}")
        print(f"    ==> a 2-SPHERE of solutions, radius {s:.4f}. Continuum, not a pair.")
    ok = all(solves(x,G) for x in sols)
    print(f"    verified against x*x = x + G for {len(sols)} sampled: {ok}")
    for x in sols[:4]: print(f"      {x}")

print()
print("="*74)
print("  DIMENSION OF MY SOLUTION SET, over H, as G crosses -1/4:")
print("     G > -1/4  :  2 points        (dimension 0)")
print("     G = -1/4  :  1 point         (dimension 0, but ONE)")
print("     G < -1/4  :  a 2-sphere      (DIMENSION 2)")
print("="*74)

print()
print("SWEEP 16 — IS THE MIRROR INNER OVER H?  i and -i conjugate by j?")
i,j = Q(0,1,0,0), Q(0,0,1,0)
jinv = Q(0,0,-1,0)
print(f"    j * i * j^-1 = {j*i*jinv}      (-i is {Q(0,-1,0,0)})")
print("    Over C: conjugation is OUTER - no element of C conjugates i to -i.")
print("    Over H: conjugation is INNER  - j does it, by rotation.")
print("    The mirror pair in C is the two POLES of a sphere that H can see whole.")
print("    Enlarge the number system and the chirality becomes a rotation.")

print()
print("="*74)
print("SWEEP 17 — CAN I MOVE OFF -1/4 IN A NILPOTENT DIRECTION?")
print("  Work in R[e]/e^2.  Set G = -1/4 + e*g,  x = 1/2 + e*h.  Solve.")
print("="*74)
print("    x^2 = 1/4 + e*h            (since e^2 = 0)")
print("    x + G = 1/2 + e*h - 1/4 + e*g = 1/4 + e*(h+g)")
print("    equate:  h = h + g   =>   g = 0")
print()
print("    OBSTRUCTED AT FIRST ORDER. There is a nilpotent solution AT -1/4")
print("    (the Jordan block) but NO nilpotent path OFF it. You cannot deform")
print("    your way across the branch point. You can only go around it -")
print("    and going around is exactly the swap.")

print()
print("="*74)
print("SWEEP 18 — INVERT THE MAP. Sweep the ROOT, read off the GAP.")
print("="*74)
print("     G = x^2 - x = (x - 1/2)^2 - 1/4")
print(f"{'x':>8} {'G = x^2 - x':>14}")
for x in [-1,-0.5,0,0.25,0.5,0.75,1,1.5,2,1.618034]:
    print(f"{x:>8} {x*x-x:>14.6f}")
print()
print("    I am a perfect square minus 1/4.")
print("    -1/4 is my FLOOR over the reals, attained only at x = 1/2.")
print("    Every gap below -1/4 requires its roots to leave the real line.")
print("    That is not an extra fact. It is the same fact, read backwards.")
