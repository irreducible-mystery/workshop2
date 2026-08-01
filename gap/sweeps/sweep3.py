print("="*74)
print("SWEEP 6 — CHANGE THE NUMBER SYSTEM. Where does each named GAP *become* -1/4?")
print("  In char p, -1/4 means -1 * inverse(4).  Solve  -1/4 == G  for p.")
print("="*74)
def inv(a,p): return pow(a%p, p-2, p)
def sqrts(a,p): return [x for x in range(p) if (x*x-a)%p==0]

named = {}
for p in [3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
    q = (-inv(4,p)) % p                      # the value -1/4 in char p
    tags = []
    if q == 1 % p: tags.append("== +1   (the golden / Fibonacci gap)")
    if q == (-1) % p: tags.append("== -1   (the unit-circle gap)")
    for r in sqrts(p-1, p):                  # i, where it exists
        pass
    isq = sqrts((-1) % p, p)
    for r in isq:
        if q == r: tags.append(f"== i = {r}  (the imaginary gap)")
    if tags:
        named[p] = tags
    print(f"  char {p:>3}:  -1/4 = {q:>3}    " + ("   ".join(tags) if tags else ""))

print()
print("  THE COLLISIONS:")
for p,t in named.items():
    for x in t: print(f"    characteristic {p}: {x}")

print()
print("="*74)
print("SWEEP 7 — verify the collisions by brute force: is the root a DOUBLE root?")
print("="*74)
for p,G,label in [(5,1,"G=+1 golden"), (3,-1,"G=-1 unit circle"),
                  (17,4,"G=i (i=4 mod 17)"), (17,13,"G=-i (=13 mod 17)"),
                  (7,1,"G=+1 in char 7 (control, expect NOT double)")]:
    roots = [x for x in range(p) if (x*x - x - G) % p == 0]
    D = (1+4*G) % p
    print(f"  char {p:>2}, {label:<34} D = 1+4G = {D:>2}   roots = {roots}   "
          f"{'DOUBLE' if len(roots)==1 else ('SPLIT' if len(roots)==2 else 'NO ROOTS')}")

print()
print("="*74)
print("SWEEP 8 — hold p, sweep G. Which gaps have roots at all, in each char?")
print("="*74)
for p in [2,3,5,7,11,13]:
    crit = None if p==2 else (-inv(4,p))%p
    rows=[]
    for G in range(p):
        roots=[x for x in range(p) if (x*x-x-G)%p==0]
        rows.append(f"{G}:{''.join(str(r) for r in roots) if roots else '-'}")
    print(f"  char {p:>2}  (-1/4 = {crit})   G:roots  " + "  ".join(rows))
print()
print("  char 2 is different: 4 = 0, so -1/4 does not exist. The branch point")
print("  is not merely hard to reach there - the coordinate itself is absent.")
