import cmath, math
print("="*72)
print("SWEEP 3 — APPROACH -1/4 FROM DIFFERENT DIRECTIONS")
print("  G = -1/4 + eps * exp(i*theta).  Same distance. Different bearing.")
print("="*72)
eps = 0.01
print(f"{'bearing':>12} {'root+':>24} {'root-':>24}  what you see")
for deg in [0,45,90,135,180,225,270,315]:
    G = -0.25 + eps*cmath.exp(1j*math.radians(deg))
    s = cmath.sqrt(1+4*G); rp, rm = (1+s)/2, (1-s)/2
    if abs(rp.imag) < 1e-12:
        see = "TWO REAL — you can say which is bigger"
    elif abs(rp - rm.conjugate()) < 1e-12:
        see = "CONJUGATE PAIR — no bigger, only mirror"
    else:
        see = "generic pair — neither ordered nor mirrored"
    print(f"{deg:>9} deg  {rp.real:+.6f}{rp.imag:+.6f}i  {rm.real:+.6f}{rm.imag:+.6f}i  {see}")

print()
print("="*72)
print("SWEEP 4 — MONODROMY. Walk a full circle AROUND -1/4 and come home.")
print("="*72)
G0 = -0.25 + 0.01
s = cmath.sqrt(1+4*G0); start_p = (1+s)/2
cur = s
N = 2000
for k in range(1, N+1):
    G = -0.25 + 0.01*cmath.exp(2j*math.pi*k/N)
    nxt = cmath.sqrt(1+4*G)
    if abs(nxt - cur) > abs(-nxt - cur):   # follow the branch continuously
        nxt = -nxt
    cur = nxt
end_p = (1+cur)/2
print(f"  start at G = {G0:.4f}, root+ = {start_p.real:+.8f}{start_p.imag:+.8f}i")
print(f"  after ONE full loop around -1/4, continuously:")
print(f"    the SAME G, and the root you were following is now {end_p.real:+.8f}{end_p.imag:+.8f}i")
print(f"    is it back where it started? {abs(end_p-start_p) < 1e-6}")
print(f"    is it the OTHER root?        {abs(end_p-(1-start_p)) < 1e-6}")
print()
print("  Same G. Same equation. Different root. The path did it.")
print()
print("="*72)
print("SWEEP 5 — WHAT LIVES AT -1/4 THAT LIVES NOWHERE ELSE")
print("  solve the SAME equation for a 2x2 matrix instead of a number")
print("="*72)
import itertools
def mat_check(M, G):
    a,b,c,d = M
    M2 = (a*a+b*c, a*b+b*d, c*a+d*c, c*b+d*d)
    R  = (a+G,     b,       c,       d+G)
    return all(abs(x-y) < 1e-12 for x,y in zip(M2,R))

for G in [-0.25, -0.5, 0.0, 1.0]:
    s = cmath.sqrt(1+4*G); rp, rm = (1+s)/2, (1-s)/2
    diag = (rp,0,0,rm)
    jord = (rp,1,0,rp)                     # a Jordan block: eigenvalue repeated, NOT diagonalizable
    print(f"  G = {G:>6}: diagonal solution valid? {mat_check(diag,G)}   "
          f"JORDAN BLOCK valid? {mat_check(jord,G)}")
print()
print("  A Jordan block is a number plus a nilpotent: x = 1/2 + e, e*e = 0.")
print("  It solves the equation at G = -1/4 and at NO other G.")
