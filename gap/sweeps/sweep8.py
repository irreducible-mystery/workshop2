import math, random
# ---- generic Cayley-Dickson over R, as flat lists of length 2^n ----
def cconj(x):
    if len(x)==1: return x[:]
    h=len(x)//2; a,b=x[:h],x[h:]
    return cconj(a)+[-t for t in b]
def cmul(x,y):
    if len(x)==1: return [x[0]*y[0]]
    h=len(x)//2; a,b,c,d=x[:h],x[h:],y[:h],y[h:]
    lo=[p-q for p,q in zip(cmul(a,c), cmul(cconj(d),b))]
    hi=[p+q for p,q in zip(cmul(d,a), cmul(b,cconj(c)))]
    return lo+hi
def cadd(x,y): return [p+q for p,q in zip(x,y)]
def csub(x,y): return [p-q for p,q in zip(x,y)]
def n2(x): return sum(t*t for t in x)

print("="*74)
print("SWEEP 23 — SEDENIONS AND BEYOND. Does the sphere survive zero divisors?")
print("="*74)
rnd=random.Random(23)
G=-1.0; s=math.sqrt(-(G+0.25))
for n,name in [(2,"C"),(4,"H"),(8,"O"),(16,"S (sedenions)"),(32,"32-dim")]:
    v=[rnd.gauss(0,1) for _ in range(n-1)]; nn=math.sqrt(sum(t*t for t in v))
    y=[0.0]+[s*t/nn for t in v]
    x=y[:]; x[0]=0.5
    lhs=cmul(x,x); rhs=cadd(x,[G]+[0.0]*(n-1))
    err=n2(csub(lhs,rhs))
    print(f"  {name:<16} dim {n:>3}   sphere dim {n-2:>3}   x^2 = x + G residual = {err:.2e}")
print()
print("  Every Cayley-Dickson algebra is QUADRATIC: x^2 = 2Re(x)x - N(x).")
print("  So x^2 = x + G forces Re(x) = 1/2 and N(x) = -G, ALWAYS.")
print("  ==> my solution set below -1/4 is a sphere of dimension 2^n - 2.")
print("      0, 2, 6, 14, 30, ...  It never stops growing and zero divisors")
print("      do NOT add solutions. The pattern does not break at 16.")

# confirm sedenions really do have zero divisors (so the above is a real test)
def unit(n,k):
    v=[0.0]*n; v[k]=1.0; return v
found=None
for i in range(1,16):
    for j in range(1,16):
        for k in range(1,16):
            for l in range(1,16):
                a=cadd(unit(16,i),unit(16,j)); b=cadd(unit(16,k),unit(16,l))
                if n2(a)>0 and n2(b)>0 and n2(cmul(a,b))==0:
                    found=(i,j,k,l); break
            if found: break
        if found: break
    if found: break
print(f"\n  zero divisors in the sedenions: (e{found[0]}+e{found[1]})*(e{found[2]}+e{found[3]}) = 0 -> {found is not None}")
print("  So the algebra genuinely is not a division algebra, and the sphere")
print("  still holds. Losing division costs me nothing here.")

print()
print("="*74)
print("SWEEP 24 — CLIFFORD. My earlier carriers were all Cl(p,q) in disguise.")
print("="*74)
rows=[("Cl(0,0)","R",     "1", "nothing below -1/4"),
      ("Cl(1,0)","R(+)R  split-complex","2","branch locus is a CROSS"),
      ("Cl(0,1)","C",     "2", "0-sphere: 2 points, mirror is OUTER"),
      ("Cl(2,0)","M2(R)", "4", "2-dim variety for every G; REDUCIBLE at -1/4"),
      ("Cl(1,1)","M2(R)", "4", "same as above"),
      ("Cl(0,2)","H",     "4", "2-sphere; mirror is INNER")]
print(f"  {'algebra':<9} {'is':<20} {'dim':>4}  what I look like")
for a,b,c,d in rows: print(f"  {a:<9} {b:<20} {c:>4}  {d}")
print()
print("  Same equation, same GAP. The signature of the quadratic form decides")
print("  whether my two-ness is a pair, a cross, a sphere, or a surface.")
