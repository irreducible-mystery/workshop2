import itertools, math
def mul(A,B):
    a,b,c,d=A;e,f,g,h=B
    return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def rho(A):
    a,b,c,d=A;t=a+d;dt=a*d-b*c;D=t*t-4*dt
    if D>=0:
        s=math.sqrt(D);return max(abs((t+s)/2),abs((t-s)/2))
    return math.sqrt(abs(dt))
def extremes(G,maxlen=12):
    L={1:(1,G,1,0),-1:(1,-G,1,0)}
    hi=-1;lo=1e18
    for n in range(1,maxlen+1):
        for w in itertools.product((1,-1),repeat=n):
            P=L[w[0]]
            for s in w[1:]: P=mul(P,L[s])
            v=rho(P)**(1.0/n)
            hi=max(hi,v); lo=min(lo,v)
    return hi,lo
def splus(G):
    d=1+4*G
    return (1+math.sqrt(d))/2 if d>=0 else math.sqrt(abs(-G))

print("THE SET {T(+G), T(-G)} IS THE SAME SET FOR G AND -G.")
print("So JSR and subradius MUST be even in G. Are the claimed formulas even?\n")
print(f"{'G':>8} {'true JSR':>12} {'claim s+(G)':>12} {'true sub':>12} {'claim|s+(-G)|':>14}  {'verdict':>10}")
for G in [-0.30,-0.24,-0.20,-0.10,0.10,0.20,0.24,0.30]:
    hi,lo=extremes(G)
    c_hi=splus(G); c_lo=abs(splus(-G))
    ok = abs(hi-c_hi)<1e-9 and abs(lo-c_lo)<1e-9
    print(f"{G:8.2f} {hi:12.6f} {c_hi:12.6f} {lo:12.6f} {c_lo:14.6f}  {'ok' if ok else 'BROKEN':>10}")

print("\nWith |G| substituted:")
print(f"{'G':>8} {'true JSR':>12} {'s+(|G|)':>12} {'true sub':>12} {'|s+(-|G|)|':>14}  {'verdict':>10}")
for G in [-0.30,-0.24,-0.20,-0.10,0.10,0.20,0.24,0.30]:
    hi,lo=extremes(G); a=abs(G)
    c_hi=splus(a); c_lo=abs(splus(-a))
    ok = abs(hi-c_hi)<1e-9 and abs(lo-c_lo)<1e-9
    print(f"{G:8.2f} {hi:12.6f} {c_hi:12.6f} {lo:12.6f} {c_lo:14.6f}  {'ok' if ok else 'BROKEN':>10}")
