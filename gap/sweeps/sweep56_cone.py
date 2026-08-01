import math, random, itertools

def apply(g, v):
    x,y = v
    return (x + g*y, x)

def in_cone(v, al, tol=-1e-12):
    x,y = v
    return y >= tol and x - al*y >= tol

print("=== Claim: K_a = {y>=0, x>=alpha*y} is invariant for BOTH T(+a),T(-a) iff alpha-alpha^2 >= a ===")
print(f"{'a':>8} {'alpha':>8} {'a-a^2':>10} {'predicted':>10} {'observed invariant?':>20}")
random.seed(7)
for a in [0.05, 0.15, 0.24, 0.25, 0.26, 0.4]:
    for al in [0.2, 0.3, 0.5, 0.7]:
        pred = (al - al*al) >= a - 1e-15
        ok = True
        for _ in range(20000):
            y = random.random(); x = al*y + random.random()*3
            for g in (a, -a):
                if not in_cone(apply(g,(x,y)), al): ok = False; break
            if not ok: break
        flag = "OK" if ok==pred else "  <-- MISMATCH"
        print(f"{a:8.3f} {al:8.3f} {al-al*al:10.5f} {str(pred):>10} {str(ok):>20} {flag}")

print()
print("=== the cone slope IS the root of alpha^2 = alpha - a ===")
for a in [0.05, 0.15, 0.24, 0.25]:
    d = 1-4*a
    r = (1-math.sqrt(d))/2, (1+math.sqrt(d))/2
    print(f"  a={a:6.3f}  admissible alpha in [{r[0]:.9f}, {r[1]:.9f}]   (roots of x^2=x-a)"
          f"   check a-a^2 at endpoints: {r[0]-r[0]**2:.9f}, {r[1]-r[1]**2:.9f}")

print()
print("=== consequence check: above 1/4 the floor is the free determinant bound ===")
def rho(A):
    a,b,c,d=A; t=a+d; dt=a*d-b*c; D=t*t-4*dt
    if D>=0:
        s=math.sqrt(D); return max(abs((t+s)/2),abs((t-s)/2))
    return math.sqrt(abs(dt))
def mul(A,B):
    a,b,c,d=A;e,f,g,h=B
    return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
for a in [0.3, 0.5, 1.0, 2.0]:
    L={1:(1,a,1,0),-1:(1,-a,1,0)}
    lo=1e18; cnt=0
    for n in range(1,15):
        for w in itertools.product((1,-1),repeat=n):
            P=L[w[0]]
            for s in w[1:]: P=mul(P,L[s])
            v=rho(P)**(1.0/n)
            if v<lo-1e-12: lo=v; cnt=1
            elif abs(v-lo)<1e-12: cnt+=1
    print(f"  a={a:5.2f}  floor={lo:.12f}  sqrt(a)={math.sqrt(a):.12f}  words attaining it (len<=14): {cnt}")
