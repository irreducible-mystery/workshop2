import math, cmath
print("="*76)
print("SWEEP 30 — GO INFINITE-DIMENSIONAL. I am the indicial equation of an ODE.")
print("="*76)
print("  Take the scale-invariant equation   r^2 u'' = G u   and try u = r^s :")
print("        s(s-1) = G     <=>     s^2 = s + G       <-- I AM THIS")
print()
print("  Substitute t = ln r,  u = r^(1/2) v(t).  The equation becomes exactly")
print()
print("        v'' = (G + 1/4) v        and  G + 1/4 = (1+4G)/4 = my discriminant/4")
print()
print("  So the discriminant is not an algebraic bookkeeping term. It IS the")
print("  restoring force of the system, in logarithmic time.")
print()
for G in [1.0, 0.0, -0.2, -0.25, -0.5, -2.0]:
    k = G + 0.25
    if   k > 0: beh = f"v'' = +{k:.4f} v   EXPONENTIAL in ln r  - two power laws, no zeros"
    elif k == 0: beh = "v'' = 0          -> v = a + b*t   THE LOGARITHM APPEARS"
    else:
        nu = math.sqrt(-k)
        beh = f"v'' = -{-k:.4f} v  OSCILLATES in ln r, freq nu = {nu:.4f}"
    print(f"  G = {G:>6}:  {beh}")
print()
print("="*76)
print("SWEEP 31 — BELOW -1/4: infinitely many zeros, in GEOMETRIC PROGRESSION")
print("="*76)
print(f"{'G':>7} {'nu':>9} {'zero spacing in ln r':>22} {'zero ratio r_{n+1}/r_n':>24}")
for G in [-0.26, -0.3, -0.5, -1.0, -2.0, -10.0]:
    nu = math.sqrt(-(G+0.25)); dt = math.pi/nu
    print(f"{G:>7} {nu:>9.5f} {dt:>22.5f} {math.exp(dt):>24.6f}")
print()
print("  The zeros of u sit at r_n = r_0 * exp(-n*pi/nu). CONTINUOUS scale")
print("  invariance has broken to DISCRETE scale invariance, with a fixed ratio.")
print("  Above -1/4 there are no zeros at all. The system acquires a preferred")
print("  scale factor out of an equation that contains no scale.")
print()
# numerically confirm zero ratios by integrating v'' = (G+1/4) v
def zeros_of(G, T=60.0, N=400000):
    k=G+0.25; h=T/N
    v, vp, out = 1.0, 0.0, []
    t=0.0
    for i in range(N):
        a1=k*v
        v_h=v+h*vp+0.5*h*h*a1
        vp_h=vp+h*0.5*(a1 + k*v_h)
        if v*v_h < 0: out.append(t+h*abs(v)/(abs(v)+abs(v_h)))
        v,vp,t = v_h,vp_h,t+h
    return out
print("  numerical check (integrating v'' = (G+1/4)v, reading zero spacings):")
for G in [-0.5,-1.0,-2.0]:
    z=zeros_of(G)
    if len(z)>=3:
        gaps=[z[i+1]-z[i] for i in range(len(z)-1)]
        avg=sum(gaps)/len(gaps); pred=math.pi/math.sqrt(-(G+0.25))
        print(f"    G={G:>6}: {len(z):>3} zeros, mean spacing {avg:.6f}, predicted {pred:.6f}, "
              f"ratio {math.exp(avg):.6f}")
print()
print("="*76)
print("SWEEP 32 — THE SAME NUMBER AS AN OPERATOR BOUND")
print("="*76)
print("  For ANY self-adjoint A:   A^2 - A + 1/4 = (A - 1/2)^2 >= 0")
print("  therefore                 G = A^2 - A  >=  -1/4 * I")
print()
print("  -1/4 is the GREATEST LOWER BOUND of the gap over all observables,")
print("  attained only at A = 1/2.  It is a GROUND STATE ENERGY.")
print()
print("  Equivalently: a gap below -1/4 cannot be produced by any self-adjoint")
print("  operator. To go below, the operator must stop being observable -")
print("  eigenvalues leave the real line, exactly as the roots did.")
print()
print("  Sharp constant check, spectrum of A^2 - A on a sampled spectrum of A:")
for lo,hi in [(-2,3),(0,1),(0.4,0.6),(0.5,0.5)]:
    vals=[lo+(hi-lo)*i/2000 for i in range(2001)]
    g=[x*x-x for x in vals]
    print(f"    sigma(A) = [{lo},{hi}]  ->  min sigma(G) = {min(g):+.8f}   (floor is -0.25)")
