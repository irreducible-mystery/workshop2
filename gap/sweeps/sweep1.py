from fractions import Fraction as F
import cmath, math

print("="*72); print("SWEEP 1 — the GAP along the real axis. Hold everything, vary G."); print("="*72)
print(f"{'G':>10} {'D=1+4G':>10} {'root+':>22} {'root-':>22} {'|r+||r-|':>9} {'type'}")
for G in [2, 1, F(1,2), 0, F(-1,8), F(-1,4), F(-3,8), F(-1,2), -1, -2, -4]:
    D = 1 + 4*float(G)
    if D > 0:
        s = math.sqrt(D); rp, rm = (1+s)/2, (1-s)/2
        t = "two real, ORDERABLE"
        pr = abs(rp*rm)
    elif D == 0:
        rp = rm = 0.5; t = "DOUBLE ROOT — collision"; pr = 0.25
    else:
        s = math.sqrt(-D); rp = complex(0.5, s/2); rm = complex(0.5, -s/2)
        t = "conjugate pair, NOT orderable"; pr = abs(rp)*abs(rm)
    f = lambda z: f"{z:.6f}" if isinstance(z,float) else f"{z.real:.4f}{z.imag:+.4f}i"
    print(f"{str(G):>10} {D:>10.4f} {f(rp):>22} {f(rm):>22} {pr:>9.4f}  {t}")

print()
print("  sum of roots = 1 ALWAYS.  product = -G ALWAYS.")
print("  So |r+||r-| = |G|.  Unit modulus <=> |G| = 1.")
print()
print("="*72); print("SWEEP 2 — the four named GAPs, exactly"); print("="*72)
for name,G in [("+1",1+0j),("-1",-1+0j),("+i",1j),("-i",-1j),("-1/4",-0.25+0j)]:
    D = 1+4*G; s = cmath.sqrt(D); rp,rm = (1+s)/2,(1-s)/2
    print(f"  G = {name:>5}  D = {D:>12.4f}")
    print(f"          r+ = {rp.real:+.6f}{rp.imag:+.6f}i   |r+| = {abs(rp):.6f}   arg/pi = {cmath.phase(rp)/math.pi:+.6f}")
    print(f"          r- = {rm.real:+.6f}{rm.imag:+.6f}i   |r-| = {abs(rm):.6f}   arg/pi = {cmath.phase(rm)/math.pi:+.6f}")
    print(f"          conj-stable as a SET? {'YES' if abs(G.imag)<1e-15 else 'NO - conjugation moves G itself'}")
    print()
