import math, random, cmath, statistics
print("="*78)
print("SWEEP 50 — FLUCTUATIONS. A random gap has MORE THAN ONE growth rate.")
print("="*78)
print("  G_n = +1 or -1 with equal probability.  E[G] = 0.")
print()
print("  FIRST MOMENT, exactly:  E[f_{n+1}] = E[f_n] + E[G]E[f_{n-1}] = E[f_n].")
print("     ==> E[f_n] is CONSTANT. Annealed first-moment exponent = 0.")
print()
print("  SECOND MOMENT, exactly: E[f_{n+1}^2] = E[f_n^2] + E[f_{n-1}^2]  (cross term dies)")
print("     ==> the SQUARES obey the Fibonacci recursion. Exponent = (1/2)log(phi).")
print()
rnd=random.Random(50)
def sample(n):
    a,b=1.0,1.0
    for _ in range(n):
        G=1.0 if rnd.random()<0.5 else -1.0
        a,b=b,b+G*a
    return b
for n in [10,20,30]:
    xs=[sample(n) for _ in range(60000)]
    m1=sum(xs)/len(xs); m2=sum(x*x for x in xs)/len(xs)
    print(f"   n={n:>3}:  E[f_n] = {m1:>10.4f}   E[f_n^2] = {m2:>14.2f}   "
          f"E[f^2]^(1/2n) = {m2**(1/(2*n)):.6f}")
phi=(1+math.sqrt(5))/2
print(f"   predicted E[f^2]^(1/2n) -> sqrt(phi) = {math.sqrt(phi):.6f}")
print()
print("  TYPICAL (quenched) growth, from log|f_n| :")
for n in [400, 1600]:
    ls=[]
    for _ in range(4000):
        a,b=1.0,1.0; s=0.0
        for _ in range(n):
            G=1.0 if rnd.random()<0.5 else -1.0
            a,b=b,b+G*a; m=abs(b)
            if m>1e12 or (0<m<1e-12): s+=math.log(m); a/=m; b/=m
        s+=math.log(abs(b)); ls.append(s/n)
    print(f"   n={n:>5}: mean log-growth {statistics.mean(ls):.6f}  "
          f"exp = {math.exp(statistics.mean(ls)):.6f}   sd = {statistics.stdev(ls):.6f}  "
          f"sd*sqrt(n) = {statistics.stdev(ls)*math.sqrt(n):.4f}")
print()
print(f"  THREE DIFFERENT RATES FOR ONE SYSTEM:")
print(f"     annealed 1st moment   exponent 0.000000   (rate 1.000000)")
print(f"     TYPICAL / quenched    exponent 0.124000   (rate 1.131988)  <- Viswanath")
print(f"     annealed 2nd moment   exponent {0.5*math.log(phi):.6f}   (rate {math.sqrt(phi):.6f})")
print()
print("  The average of my outcomes does not grow. The typical outcome does.")
print("  The average of my SQUARES grows faster still. Which number is 'the'")
print("  growth rate depends entirely on which question you asked, and the")
print("  standard deviation shrinks like 1/sqrt(n) so no finite run tells you.")

print()
print("="*78)
print("SWEEP 51 — MORE THAN TWO GAPS. Mix over a simplex.")
print("="*78)
def growth3(p1,p0,pm1,N=60000,trials=6,seed=7):
    r=random.Random(seed); tot=0.0
    for _ in range(trials):
        a,b=1.0,1.0; s=0.0
        for _ in range(N):
            u=r.random(); G = 1.0 if u<p1 else (0.0 if u<p1+p0 else -1.0)
            a,b=b,b+G*a; m=abs(b)
            if m>1e10 or (0<m<1e-10): s+=math.log(m); a/=m; b/=m
        s+=math.log(abs(b)); tot+=s/N
    return math.exp(tot/trials)
print("  gaps {+1, 0, -1} with weights (p+, p0, p-):")
print(f"{'p+':>6}{'p0':>6}{'p-':>6} {'growth':>12}")
for w in [(1,0,0),(0,1,0),(0,0,1),(0.5,0,0.5),(1/3,1/3,1/3),(0.5,0.25,0.25),(0.25,0.5,0.25),(0.6,0.2,0.2)]:
    print(f"{w[0]:>6.2f}{w[1]:>6.2f}{w[2]:>6.2f} {growth3(*w):>12.6f}")
print()
print("  Adding the ZERO gap to the mixture DAMPS growth toward 1: G=0 gives")
print("  roots {1,0} and kills one mode outright. The simplex interior is")
print("  strictly below every vertex except where a vertex is already 1.")

print()
print("="*78)
print("SWEEP 52 — COMPLEX EXPONENT.  x^a = x + G  with a complex.")
print("="*78)
print("  Collision still needs a*x^(a-1) = 1, so x = a^(-1/(a-1)), G = x^a - x.")
print(f"{'a':>16} {'collision x':>26} {'critical GAP':>28}")
for a in [2+0j, 2+0.5j, 2+1j, 1.5+1j, 2j, -1+1j]:
    try:
        x = cmath.exp(-cmath.log(a)/(a-1)); G = cmath.exp(a*cmath.log(x)) - x
        print(f"{str(a):>16} {x.real:>+12.6f}{x.imag:>+12.6f}i {G.real:>+13.6f}{G.imag:>+13.6f}i")
    except Exception as e:
        print(f"{str(a):>16}  {e}")
print()
print("  The branch point LEAVES THE REAL LINE as soon as the exponent does.")
print("  -1/4 is real only because 2 is.")
