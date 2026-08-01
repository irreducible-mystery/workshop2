import cmath, math
from fractions import Fraction as F
print("="*74)
print("SWEEP 9 — HOLD G, VARY THE OTHER COEFFICIENT.  x^2 = A*x + G")
print("  You fixed A = 1 when you wrote  phi + psi = 1.")
print("="*74)
print(f"{'A':>6} {'critical G = -A^2/4':>22}   collision root = A/2")
for A in [F(1),F(2),F(1,2),F(-1),F(3),F(0)]:
    print(f"{str(A):>6} {str(F(-1,4)*A*A):>22}   {str(A/2):>10}")
print()
print("  -1/4 is the branch point ONLY because the sum of the roots is 1.")
print("  The '1' in phi + psi = 1 and the '-1/4' are the SAME NUMBER, twice.")
print("  Critical locus in (A,G) space is a parabola.  You are sitting on it at A=1.")

print()
print("="*74)
print("SWEEP 10 — CHANGE DEGREE.  x^n = x + G.  Where do roots collide?")
print("="*74)
import numpy as np
for n in [2,3,4,5]:
    # collision <=> discriminant 0 <=> x^n - x - G and its derivative share a root
    # n x^(n-1) = 1  ->  x = (1/n)^(1/(n-1));  then G = x^n - x
    xs = [ (1/n)**(1/(n-1)) * cmath.exp(2j*math.pi*k/(n-1)) for k in range(n-1) ]
    gs = sorted({complex(round((x**n - x).real,10), round((x**n-x).imag,10)) for x in xs}, key=lambda z:(z.real,z.imag))
    print(f"  degree {n}: {len(gs)} critical GAP value(s):  " +
          "  ".join(f"{g.real:+.6f}{g.imag:+.6f}i" for g in gs))
print()
print("  degree 2 has ONE branch point. Higher degree has several, and they")
print("  leave the real line. -1/4 is the whole branch locus only at degree 2.")

print()
print("="*74)
print("SWEEP 11 — THE ASYMMETRY IN CHAR 17, stated honestly")
print("="*74)
p=17
print(f"  both 4 and 13 square to -1 mod {p}:  4^2={4*4%p}, 13^2={13*13%p}")
print(f"  -1/4 mod {p} = {(-pow(4,p-2,p))%p}")
print("  So exactly ONE of the two square roots of -1 is the critical GAP.")
print("  Which one is called 'i' is a labelling choice with no internal witness.")
print("  Choose i=4  -> the gap +i is critical, -i is not.")
print("  Choose i=13 -> the gap -i is critical, +i is not.")
print("  The chirality is real; WHICH one you are is not determinable from inside.")
