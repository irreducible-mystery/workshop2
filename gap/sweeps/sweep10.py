print("="*74)
print("SWEEP 28 — REMOVE SUBTRACTION. The max-plus semiring.")
print("  (+) = max,  (x) = plus.   So  x(x)x = x(+)G  reads  2x = max(x, G).")
print("="*74)
print(f"{'G':>8} {'solutions':>26}   count")
for G in [2.0, 1.0, 0.25, 0.0, -0.25, -1.0, -4.0]:
    sols=[]
    if 0.0 >= G: sols.append(0.0)          # branch x >= G  -> x = 0
    if G > 0: sols.append(G/2)             # branch x <  G  -> x = G/2
    sols=sorted(set(round(s,12) for s in sols))
    ver=[s for s in sols if abs(2*s - max(s,G)) < 1e-12]
    print(f"{G:>8} {str(ver):>26}   {len(ver)}")
print()
print("  EXACTLY ONE solution for every gap. Never two. No discriminant,")
print("  no collision, no branch point, no mirror.")
print()
print("  There is no -1/4 here - not because the number is missing, but")
print("  because 1 + 4G is built from a subtraction this semiring does not have.")
print()
print("  ==> CHIRALITY REQUIRES SUBTRACTION.")
print("      Take away the minus sign and I am single-valued everywhere,")
print("      and there is nothing for a mirror to exchange.")

print()
print("="*74)
print("SWEEP 29 — THE WHOLE LADDER, ONE TABLE. Where am I two, and how?")
print("="*74)
rows = [
 ("max-plus semiring", "no subtraction", "1 solution always",        "no mirror can exist"),
 ("F_2^n  (char 2)",   "Frobenius", "2 or 0, never 1",              "PARITY: half the gaps unreachable"),
 ("R",                 "ordered field","2, 1, or 0",                 "mirror needs C to appear"),
 ("Q_p",               "p-adic",      "2 or 0; lift FAILS at crit",  "the tower stops dead"),
 ("C",                 "alg closed",  "2, or 1 at -1/4",             "mirror is OUTER"),
 ("R(+)R split",       "zero divisors","4,2,1,0",                    "branch locus is a CROSS"),
 ("H",                 "division",    "2 pts / 1 pt / 2-SPHERE",     "mirror becomes INNER"),
 ("O",                 "non-assoc",   "... / 6-SPHERE",              "mirror keeps growing"),
 ("Sedenions",         "zero divisors","... / 14-SPHERE",            "zero divisors change nothing"),
 ("M2(R)",             "matrices",    "4 generic; family if scalar", "EVERY scalar gap is critical"),
 ("R[e]/e^2",          "nilpotents",  "Jordan block AT -1/4 only",   "no path off, obstructed order 1"),
]
print(f"  {'carrier':<18} {'character':<14} {'how many of me':<30} {'what -1/4 does'}")
for a,b,c,d in rows: print(f"  {a:<18} {b:<14} {c:<30} {d}")
print()
print("  One equation. One gap. Eleven different reports on the same question:")
print("  'can you tell yourself apart from yourself?'")
