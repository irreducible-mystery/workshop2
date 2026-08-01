import math, random
print("="*74)
print("SWEEP 19 — KEEP ENLARGING. Cayley-Dickson: R, C, H, O.")
print("="*74)
class Q:
    def __init__(s,*v): s.v=list(v)+[0]*(4-len(v))
    def conj(s): return Q(s.v[0],-s.v[1],-s.v[2],-s.v[3])
    def __mul__(x,y):
        a,b,c,d=x.v; e,f,g,h=y.v
        return Q(a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g, a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)
    def __add__(x,y): return Q(*[p+q for p,q in zip(x.v,y.v)])
    def __sub__(x,y): return Q(*[p-q for p,q in zip(x.v,y.v)])
    def n2(s): return sum(z*z for z in s.v)
class O:   # octonion = pair of quaternions
    def __init__(s,a,b): s.a,s.b=a,b
    def __mul__(x,y): return O(x.a*y.a - y.b.conj()*x.b, y.b*x.a + x.b*y.a.conj())
    def __add__(x,y): return O(x.a+y.a, x.b+y.b)
    def __sub__(x,y): return O(x.a-y.a, x.b-y.b)
    def n2(s): return s.a.n2()+s.b.n2()

def rand_pure_oct(rnd, r):
    v=[rnd.gauss(0,1) for _ in range(7)]; n=math.sqrt(sum(z*z for z in v))
    v=[r*z/n for z in v]
    return O(Q(0,v[0],v[1],v[2]), Q(v[3],v[4],v[5],v[6]))

rnd=random.Random(11)
print(f"{'algebra':>10} {'dim':>4} {'imaginary units':>16} {'solution set for G < -1/4':>34}")
for name,dim,imag,desc in [("R",1,0,"NO solution (needs sqrt of a negative)"),
                           ("C",2,1,"2 points  (a conjugate pair)"),
                           ("H",4,3,"a 2-sphere"),
                           ("O",8,7,"a 6-sphere")]:
    print(f"{name:>10} {dim:>4} {imag:>16} {desc:>34}")
print()
G=-1.0; s=math.sqrt(-(G+0.25))
ok=True
for _ in range(8):
    y=rand_pure_oct(rnd,s); x=O(Q(0.5)+y.a, y.b)
    ok &= (x*x - x - O(Q(G),Q(0))).n2() < 1e-16
print(f"  octonion check at G = {G}: sampled 8 points of the 6-sphere, all solve x^2 = x + G: {ok}")
print()
print("  My mirror is a 0-sphere in C, a 2-sphere in H, a 6-sphere in O.")
print("  CHIRALITY IS WHAT A 2-DIMENSIONAL OBSERVER CALLS A SPHERE IT CANNOT TURN.")

print()
print("="*74)
print("SWEEP 20 — SPLIT-COMPLEX  R[j]/(j^2=+1) = R (+) R.  Zero divisors.")
print("="*74)
print("  Componentwise: each coordinate is its own gap.")
print(f"{'G = (g1,g2)':>18} {'roots':>10}   branch structure")
for g1,g2 in [(1,1),(1,-1),(-0.25,1),(-0.25,-0.25),(-0.5,1),(-0.5,-0.5)]:
    n1 = 2 if 1+4*g1>0 else (1 if 1+4*g1==0 else 0)
    n2 = 2 if 1+4*g2>0 else (1 if 1+4*g2==0 else 0)
    tag = []
    if 1+4*g1==0: tag.append("g1 critical")
    if 1+4*g2==0: tag.append("g2 critical")
    print(f"{str((g1,g2)):>18} {n1*n2:>10}   {', '.join(tag) if tag else ''}")
print()
print("  The branch locus is no longer a POINT. It is a CROSS: two lines,")
print("  g1 = -1/4 and g2 = -1/4, meeting at (-1/4,-1/4).")
print("  Split the number system and the branch point splits with it.")

print()
print("="*74)
print("SWEEP 21 — 2x2 MATRICES. Does the solution set see -1/4 at all?")
print("="*74)
print("  x^2 = x + G  <=>  trace = 1 and det = -G.  Two conditions on four")
print("  parameters, so the solution set is 2-DIMENSIONAL FOR EVERY G.")
print("  The dimension does NOT jump. What jumps is IRREDUCIBILITY:")
print()
for G,txt in [(1.0,"eigenvalues 1.618, -0.618 distinct -> ONE conjugacy class, 2-dim"),
              (0.0,"eigenvalues 1, 0 distinct        -> ONE conjugacy class, 2-dim"),
              (-0.25,"eigenvalues 1/2, 1/2 EQUAL      -> TWO classes: the scalar (1/2)I,"),
              (-0.5,"eigenvalues 1/2 +- i/2 distinct  -> ONE conjugacy class, 2-dim")]:
    print(f"   G = {G:>6}: {txt}")
    if G==-0.25: print(f"   {'':>13}  which is ONE point, and the Jordan block, a 2-dim family.")
print()
print("  Over a field, -1/4 is where my roots collide.")
print("  Over matrices, -1/4 is where my solution VARIETY becomes REDUCIBLE.")
print("  Same point. Different symptom. The dimension count is blind to it.")

print()
print("="*74)
print("SWEEP 22 — p-ADIC. Does a root mod p lift to mod p^2, p^3, ...?")
print("  Hensel: a simple root lifts uniquely. Lifting needs f'(x) = 2x-1 invertible.")
print("="*74)
def roots_mod(G,m): return [x for x in range(m) if (x*x-x-G)%m==0]
for p,G,label in [(5,1,"G=+1, char 5   (the critical gap there)"),
                  (11,1,"G=+1, char 11  (a split gap)"),
                  (3,-1,"G=-1, char 3   (the critical gap there)"),
                  (7,5,"G=5=-1/4 char 7 (the critical gap there)")]:
    r1 = roots_mod(G,p); r2 = roots_mod(G,p*p); r3 = roots_mod(G,p**3)
    dprime = [(2*x-1)%p for x in r1]
    print(f"  {label:<38} mod p: {str(r1):>9}  f'={str(dprime):>7}  "
          f"mod p^2: {len(r2)} root(s)  mod p^3: {len(r3)} root(s)")
print()
print("  Where I am critical, f' = 2*(1/2) - 1 = 0: Hensel FAILS and the root")
print("  does not lift. The branch point is exactly where the p-adic tower stops.")
print("  Same obstruction as the nilpotent one, in a different number system.")
