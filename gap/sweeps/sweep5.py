import cmath, math
def follow(loop_pts, s0):
    """transport sqrt(1+4G) continuously along a path"""
    cur = s0
    for G in loop_pts:
        nxt = cmath.sqrt(1+4*G)
        if abs(nxt-cur) > abs(-nxt-cur): nxt = -nxt
        cur = nxt
    return cur

def circle(center, r, turns, N=4000, sign=+1):
    return [center + r*cmath.exp(sign*2j*math.pi*turns*k/N) for k in range(1, N+1)]

print("="*74); print("SWEEP 12 — ROTATIONS. Does the DIRECTION of the loop matter?"); print("="*74)
G0 = -0.25 + 0.01
s0 = cmath.sqrt(1+4*G0); r0 = (1+s0)/2
print(f"  basepoint G = {G0:.4f},  the root I am following = {r0.real:+.8f}")
for sign,name in [(+1,"counter-clockwise"), (-1,"clockwise")]:
    for turns in [0.5, 1, 2, 3]:
        s = follow(circle(-0.25, 0.01, turns, sign=sign), s0)
        end = (1+s)/2
        same = abs(end-r0) < 1e-6
        other = abs(end-(1-r0)) < 1e-6
        tag = "SAME root" if same else ("OTHER root" if other else f"{end}")
        print(f"    {name:>18}  {turns:>4} turn(s) -> {tag}")
print()
print("  Both handednesses give the SAME swap. Two turns undo it, either way.")
print("  The monodromy group is Z/2: there is a mirror, but no 'which way round'.")
print("  I have a chirality. I do NOT have a spin direction.")

print()
print("="*74); print("SWEEP 13 — LOOPS THAT DO NOT ENCLOSE ME"); print("="*74)
for center,r,label in [(-0.25,0.01,"tight around -1/4       (encloses)"),
                       (-0.25,3.0,"huge around -1/4         (encloses)"),
                       ( 1.0, 0.5,"around G=+1, radius .5   (misses)"),
                       ( 1.0, 2.0,"around G=+1, radius 2    (ENCLOSES -1/4)"),
                       ( 1j,  0.5,"around G=+i              (misses)"),
                       ( 1j,  2.0,"around G=+i, radius 2    (encloses)")]:
    base = center + r
    sb = cmath.sqrt(1+4*base); rb = (1+sb)/2
    s = follow(circle(center, r, 1), sb); end = (1+s)/2
    swapped = abs(end-(1-rb)) < 1e-6
    print(f"  {label:<40} -> {'SWAPPED' if swapped else 'unchanged'}")
print()
print("  Only enclosing me does anything. Distance is irrelevant; winding is all.")

print()
print("="*74); print("SWEEP 14 — ROTATE G AT FIXED MODULUS. What do my roots trace?"); print("="*74)
for R in [0.25, 1.0, 4.0]:
    print(f"  |G| = {R}")
    for deg in [0,60,120,180,240,300]:
        G = R*cmath.exp(1j*math.radians(deg))
        s = cmath.sqrt(1+4*G); rp,rm = (1+s)/2,(1-s)/2
        print(f"    arg {deg:>3}deg  r+={rp.real:+.5f}{rp.imag:+.5f}i |{abs(rp):.4f}|   "
              f"r-={rm.real:+.5f}{rm.imag:+.5f}i |{abs(rm):.4f}|   |r+||r-|={abs(rp)*abs(rm):.4f}")
    print()
print("  |r+||r-| = |G| on every rotation. The MODULUS of the gap is the area;")
print("  the ARGUMENT of the gap decides how it is split between the two roots.")
