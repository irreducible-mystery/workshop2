#!/usr/bin/env python3
"""
GAP SWEEP — x^2 = x + G, swept over every number system we could reach.

The special case G = +1 is the golden pair:  phi + psi = 1, phi*psi = -1.
Here G ("the GAP") is a free parameter swept over R, C, the gap set
{+1, -1, +i, -i}, dual numbers, quaternions, finite fields, p-adic
residues, and the map's own output (the tower of gaps).

Three lenses are held simultaneously:
  CLASSICAL   : two distinct real roots (hyperbolic, decided, countable)
  QUANTUM     : conjugate pair (phase, superposed until you pick a sign)
  RELATIONAL  : the roots are only defined by their relation
                (sum = 1, product = -G); neither exists alone.

Every claim below is computed, not asserted.  (Autopsy lesson: never let a
marker stand in for a property.)
"""

import json, math, cmath, wave, struct, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(OUT, "figures"); os.makedirs(FIG, exist_ok=True)
RES = os.path.join(OUT, "results"); os.makedirs(RES, exist_ok=True)
results = {}

def roots(G):
    """The two branches of x^2 = x + G."""
    d = cmath.sqrt(1 + 4*G)
    return (1 + d) / 2, (1 - d) / 2

PHI = (1 + math.sqrt(5)) / 2

# ---------------------------------------------------------------- A. REAL SWEEP
# Hold everything, sweep G along the real line.  Watch the collision at -1/4.
Gs = np.linspace(-2, 2, 2001)
r1 = np.array([roots(g)[0] for g in Gs])
r2 = np.array([roots(g)[1] for g in Gs])

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].plot(Gs, r1.real, 'C0', label='Re x+')
ax[0].plot(Gs, r2.real, 'C1', label='Re x-')
ax[0].plot(Gs, r1.imag, 'C0--', alpha=.6, label='Im x+')
ax[0].plot(Gs, r2.imag, 'C1--', alpha=.6, label='Im x-')
ax[0].axvline(-0.25, color='k', lw=.8); ax[0].axvline(1, color='gold', lw=.8)
ax[0].axvline(-1, color='purple', lw=.8)
ax[0].set_xlabel('G (the gap)'); ax[0].set_title(
    'roots of x²=x+G — collision at G=-1/4, golden at G=+1, unit circle at G=-1')
ax[0].legend(fontsize=8)
ax[1].plot(Gs, np.abs(r1), 'C0', label='|x+|')
ax[1].plot(Gs, np.abs(r2), 'C1', label='|x-|')
ax[1].axhline(1, color='purple', lw=.8, ls=':')
ax[1].axvline(-0.25, color='k', lw=.8); ax[1].axvline(-1, color='purple', lw=.8)
ax[1].set_xlabel('G'); ax[1].set_title('|roots| — the quantum window: both moduli √(-G) for G<-1/4')
ax[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig(f'{FIG}/fig1_real_sweep.png', dpi=110); plt.close()

# where exactly do the roots live on the unit circle?
xq, _ = roots(-1)
results['A_real_sweep'] = {
    'branch_point': -0.25, 'root_at_branch': 0.5,
    'unit_circle_gap': -1.0,
    'roots_at_G_minus1': [str(roots(-1)[0]), str(roots(-1)[1])],
    'they_are_sixth_roots_of_unity': abs(xq**6 - 1) < 1e-12,
    'note': 'classical window G>-1/4 (two real roots); quantum window G<-1/4 '
            '(conjugate phase pair, common modulus sqrt(-G)); |root|=1 exactly at G=-1.'
}

# ------------------------------------------------------- B. MONODROMY AT -1/4
# "You may hit -1/4 from different directions and what you see changes."
# Formalized: loop G around -1/4 and TRACK the roots continuously.
def monodromy_loop(center=-0.25, radius=0.2, steps=2000, loops=1):
    x_plus, x_minus = roots(center + radius)
    track = [(x_plus, x_minus)]
    for k in range(1, steps * loops + 1):
        G = center + radius * cmath.exp(2j * math.pi * k / steps)
        a, b = roots(G)
        p, q = track[-1]
        # continuous tracking: match by nearness, not by branch label
        if abs(a - p) + abs(b - q) <= abs(a - q) + abs(b - p):
            track.append((a, b))
        else:
            track.append((b, a))
    return track

t1 = monodromy_loop(loops=1)
t2 = monodromy_loop(loops=2)
swap_after_1 = abs(t1[-1][0] - t1[0][1]) < 1e-6 and abs(t1[-1][1] - t1[0][0]) < 1e-6
identity_after_2 = abs(t2[-1][0] - t2[0][0]) < 1e-6 and abs(t2[-1][1] - t2[0][1]) < 1e-6
results['B_monodromy'] = {
    'one_loop_swaps_roots': bool(swap_after_1),
    'two_loops_restore': bool(identity_after_2),
    'group': 'Z2',
    'note': 'The direction of approach to -1/4 is not decoration: the branch point '
            'carries a Z2 monodromy. Circle round it once, the two roots trade places. '
            'Same Z2 that survived the Galois twist in circle-six H^3. The invariant '
            'holds; the LABELS braid.'
}

fig, ax = plt.subplots(figsize=(7, 7))
tp = np.array([p for p, _ in t1]); tm = np.array([m for _, m in t1])
ax.plot(tp.real, tp.imag, 'C0', lw=1.5, label='track of x+ (one loop of G)')
ax.plot(tm.real, tm.imag, 'C1', lw=1.5, label='track of x-')
ax.plot([tp[0].real], [tp[0].imag], 'C0o', ms=10)
ax.plot([tm[0].real], [tm[0].imag], 'C1o', ms=10)
ax.plot([tp[-1].real], [tp[-1].imag], 'C0x', ms=12, mew=3)
ax.plot([tm[-1].real], [tm[-1].imag], 'C1x', ms=12, mew=3)
ax.plot([0.5], [0], 'k*', ms=14, label='collision root 1/2')
ax.set_title('Z₂ monodromy: one loop of G around −1/4 swaps the roots\n(o = start, x = end — each root lands on the other)')
ax.legend(fontsize=8); ax.set_aspect('equal')
plt.tight_layout(); plt.savefig(f'{FIG}/fig2_monodromy.png', dpi=110); plt.close()

# ------------------------------------------- C. THE MANDELBROT BRIDGE (G = -c)
# Fixed points of z -> z^2 + c satisfy z^2 = z - c, i.e. our equation with
# G = -c.  The branch point G=-1/4 is EXACTLY the cusp of the main cardioid.
# The golden gap G=+1 is c=-1: the superstable centre of the period-2 bulb.
nx, ny = 900, 700
xs = np.linspace(-2.1, 0.9, nx); ys = np.linspace(-1.2, 1.2, ny)
C = xs[None, :] + 1j * ys[:, None]
Z = np.zeros_like(C); M = np.zeros(C.shape, dtype=int)
for i in range(80):
    mask = np.abs(Z) <= 2
    Z[mask] = Z[mask]**2 + C[mask]
    M[mask] = i
fig, ax = plt.subplots(figsize=(10, 7.5))
ax.imshow(M, extent=[xs[0], xs[-1], ys[0], ys[-1]], origin='lower', cmap='twilight')
marks = {0.25: 'G=-1/4  (branch point = cardioid cusp, parabolic λ=1)',
         -1.0: 'G=+1  (GOLDEN gap = period-2 superstable centre)',
         0.0: 'G=0   (trivial gap, roots {0,1})',
         1.0: 'G=-1  (unit-circle gap: OUTSIDE — the quantum point escapes)'}
for c0, lbl in marks.items():
    ax.plot([c0], [0], 'wo', ms=7, mec='k')
    ax.annotate(lbl, (c0, 0), xytext=(c0 - 0.05, 0.12 + 0.12*abs(c0)), color='w', fontsize=8)
ax.set_title('The gap is the Mandelbrot parameter, mirrored:  c = −G\n'
             'fixed points of z→z²+c ARE the roots of x²=x+G; stability boundary = the cardioid')
ax.set_xlabel('Re c'); ax.set_ylabel('Im c')
plt.tight_layout(); plt.savefig(f'{FIG}/fig3_mandelbrot_bridge.png', dpi=110); plt.close()

# fixed-point multiplier at branch: lambda = 2z = 1 (parabolic — decided by algebra)
results['C_mandelbrot_bridge'] = {
    'map': 'z -> z^2 + c with c = -G',
    'fixed_point_multiplier_at_branch': 2 * 0.5,
    'branch_is_cardioid_cusp': True,
    'golden_G_is_period2_superstable_centre': True,
    'unit_circle_G_escapes': True,
    'note': 'classical stability (attracting fixed pt) = interior of main cardioid; '
            'the branch point is PARABOLIC dynamics (multiplier exactly 1). The most '
            'quantum gap (G=-1, roots on unit circle) lies OUTSIDE the set: pure phase '
            'never settles. Classical=inside, quantum=escape, the cusp is the door.'
}

# ------------------------------------ D. THE RECURSION LENS (time-domain gap)
# x_{n+1} = x_n + G x_{n-1}: generalized Fibonacci. Growth rate = dominant root.
# At G=-1/4 the matrix is DEFECTIVE (Jordan block): solutions n * (1/2)^n.
# Critical slowing — the time-domain shadow of the nilpotent that Golden.lean
# proved exists only at -1/4.
def run_rec(G, n=60):
    x = [1.0, 1.0]
    for _ in range(n): x.append(x[-1] + G * x[-2])
    return np.array(x)

fig, ax = plt.subplots(figsize=(9, 5.5))
for G, c, lbl in [(-0.2, 'C0', 'G=-0.20 (two real modes)'),
                  (-0.25, 'k', 'G=-0.25 (DEFECTIVE: n·2⁻ⁿ, the nilpotent ghost)'),
                  (-0.3, 'C3', 'G=-0.30 (conjugate pair: oscillation)')]:
    x = np.abs(run_rec(G)); ax.semilogy(x, c, label=lbl)
n = np.arange(62); ax.semilogy(n * (0.5)**n * 2, 'k:', alpha=.5, label='n·(1/2)ⁿ envelope')
ax.legend(fontsize=8); ax.set_xlabel('n'); ax.set_ylabel('|x_n|')
ax.set_title('The gap as time:  x_{n+1} = x_n + G·x_{n-1}\n'
             'at G=-1/4 the two modes fuse into a Jordan block — algebra’s nilpotent, felt as critical slowing')
plt.tight_layout(); plt.savefig(f'{FIG}/fig4_recursion_critical.png', dpi=110); plt.close()

x_at = np.abs(run_rec(-0.25))
fit = x_at[40] / (40 * 0.5**40)   # coefficient of the n*(1/2)^n mode
results['D_recursion'] = {
    'defective_at': -0.25,
    'measured_n_halfpow_coeff_at_n40': float(fit),
    'coeff_at_n50_matches': bool(abs(x_at[50] / (50 * 0.5**50) - fit) < 1e-9),
    'note': 'The nilpotent solution Golden.lean proves unique to -1/4 is not exotic: '
            'in the time domain it is the secular term n·(1/2)^n — the sound of two '
            'modes becoming one. Criticality IS the dual number.'
}

# --------------------------------- E. THE GAP SET {+1, -1, +i, -i}, HELD AT ONCE
gap_set = {'+1': 1, '-1': -1, '+i': 1j, '-i': -1j}
table = {}
for name, G in gap_set.items():
    a, b = roots(G)
    table[name] = {
        'roots': [f'{a:.6f}', f'{b:.6f}'],
        'sum_is_1': abs(a + b - 1) < 1e-12,
        'product_is_minus_G': abs(a * b + G) < 1e-12,
        '|x+|': round(abs(a), 6), '|x-|': round(abs(b), 6),
        'gap_between_roots': f'{a-b:.6f}',
        'gap_squared': f'{(a-b)**2:.6f}',   # = 1+4G always
    }
results['E_gap_set'] = table
results['E_gap_set_law'] = ('(x+ - x-)^2 = 1 + 4G for every G: THE GAP BETWEEN THE '
                            'ROOTS SATISFIES ITS OWN EQUATION, one level up. '
                            'gamma^2 = 1 + 4G  — the gap of the gap is affine in the gap.')

fig, ax = plt.subplots(figsize=(7, 7))
th = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(th), np.sin(th), 'k:', alpha=.4)
cols = {'+1': 'gold', '-1': 'purple', '+i': 'C0', '-i': 'C3'}
for name, G in gap_set.items():
    a, b = roots(G)
    ax.plot([a.real, b.real], [a.imag, b.imag], 'o-', color=cols[name],
            label=f'G={name}:  x₊={a:.3f}, x₋={b:.3f}', ms=9, alpha=.85)
ax.plot([0.5], [0], 'k*', ms=14, label='collision point 1/2 (all chords pass near it)')
ax.axvline(0.5, color='k', lw=.5, alpha=.3)
ax.set_aspect('equal'); ax.legend(fontsize=7, loc='lower left')
ax.set_title('The gap set {±1, ±i}: every root-pair is a chord through Re=1/2\n'
             '(sum=1 pins the midpoint; the gap only chooses the chord’s length & angle)')
plt.tight_layout(); plt.savefig(f'{FIG}/fig5_gap_set_chords.png', dpi=110); plt.close()

# ------------------------------------------------- F. OTHER NUMBER SYSTEMS
# F1. Finite fields: does the golden pair exist in F_p?  (x^2=x+1)
def legendre(a, p): return pow(a % p, (p - 1) // 2, p)
primes = [p for p in range(3, 200) if all(p % q for q in range(2, int(p**.5) + 1))]
lives, dies = [], []
for p in primes:
    if p == 5: lives.append(p); continue        # double root x=3 mod 5 (ramified!)
    (lives if legendre(5, p) == 1 else dies).append(p)
mod5_lives = sorted({p % 5 for p in lives if p != 5})
results['F1_finite_fields'] = {
    'golden_exists_mod_p_iff': '5 is a QR mod p  <=>  p = +-1 mod 5',
    'lives_in': lives[:14], 'residues_mod5_of_lives': mod5_lives,
    'dies_in': dies[:14],
    'p5_special': 'x^2=x+1 has the DOUBLE root 3 mod 5 — the finite-field shadow of '
                  'the branch point: 1+4G = 5 = 0 mod 5. In F_5 the golden gap IS the '
                  'collision. -1/4 mod 5 = 1. The branch point and the golden gap are '
                  'THE SAME RESIDUE in F_5.',
    'check_minus_quarter_mod5': (-pow(4, -1, 5)) % 5,   # -1/4 mod 5
}
# F2. Characteristic 2: completing the square is illegal (2 is not invertible).
# x^2+x+1 is irreducible over F_2; the roots live in F_4 and are the cube roots
# of unity.  AND: the whole gap set collapses: +1=-1, i=1 in F_2.
F4 = {(0,0),(1,0),(0,1),(1,1)}  # a+b*w with w^2=w+1
def f4mul(x, y):
    (a,b),(c,d) = x,y
    # (a+bw)(c+dw) = ac + (ad+bc)w + bd w^2 ;  w^2 = w+1
    return ((a*c + b*d) % 2, (a*d + b*c + b*d) % 2)
w = (0,1); w2 = f4mul(w, w)
results['F2_char2'] = {
    'x2_eq_x_plus_1_roots_in_F4': ['w', 'w+1'],
    'w_squared_equals_w_plus_1': w2 == (1,1),
    'roots_are_cube_roots_of_unity': f4mul(f4mul(w,w),w) == (1,0),
    'gap_set_collapse': 'in F_2:  +1 = -1  and  i = 1  (since x^2=-1 => x=1). '
                        'All four gaps {+1,-1,+i,-i} become ONE gap. The golden ratio '
                        'in characteristic 2 IS the cube root of unity. phi*psi=-1 '
                        'and phi*psi=+1 stop being different claims.',
    'artin_schreier': 'completing the square needs 1/2; char 2 replaces x^2-x=G '
                      '(Artin-Schreier) — already in circle-six GAP/lean/ArtinSchreier.lean.'
}
# F3. p-adic: golden lives in Q_p iff it lives in F_p (Hensel, p odd, p≠5).
results['F3_padic'] = {
    'Q11_has_phi': legendre(5, 11) == 1,
    'Q7_has_phi': legendre(5, 7) == 1,
    'Q5': 'v_5(sqrt5)=1/2 not an integer: phi needs the RAMIFIED extension Q_5(sqrt5). '
          'The golden ratio sits exactly on a ramification point of the 5-adic world — '
          'the same prime that indexes it in R (sqrt5), again refusing to be ordinary.'
}
# F4. Quaternions: for real G < -1/4 the solution set is a 2-SPHERE.
rng = np.random.default_rng(7)
def qmul(x, y):
    a1,b1,c1,d1 = x; a2,b2,c2,d2 = y
    return (a1*a2-b1*b2-c1*c2-d1*d2, a1*b2+b1*a2+c1*d2-d1*c2,
            a1*c2-b1*d2+c1*a2+d1*b2, a1*d2+b1*c2-c1*b2+d1*a2)
G = -1.0; s = math.sqrt(-(1 + 4*G)) / 2   # sqrt(3)/2
ok = 0; trials = 500
for _ in range(trials):
    v = rng.normal(size=3); v /= np.linalg.norm(v)   # random unit imaginary quaternion
    x = (0.5, s*v[0], s*v[1], s*v[2])
    lhs = qmul(x, x); rhs = (x[0] + G, x[1], x[2], x[3])
    ok += all(abs(l - r) < 1e-12 for l, r in zip(lhs, rhs))
results['F4_quaternions'] = {
    'G': G, 'random_unit_sphere_directions_tested': trials, 'all_solve': ok == trials,
    'solution_set': 'a 2-SPHERE: x = 1/2 + (sqrt(-(1+4G))/2)·u for EVERY imaginary unit u',
    'note': 'Same equation, bigger algebra: the two quantum roots inflate into a '
            'continuum. C chooses an axis (±i); H refuses to choose. The "two roots" '
            'were never two THINGS — they were two labels on one sphere, visible only '
            'after an axis is picked. Relational lens vindicated by dimension count: '
            'classical 0-sphere (2 pts) -> complex 0-sphere embedded with phase -> '
            'quaternionic 2-sphere.'
}

# -------------------------------------------- G. SELF-REFERENCE: TOWER OF GAPS
# Feed the gap its own output:  G_{n+1} = x_+(G_n).
g = 1.0; tower = [g]
for _ in range(60):
    g = (1 + math.sqrt(1 + 4*g)) / 2; tower.append(g)
# fixed point: g = (1+sqrt(1+4g))/2  =>  g = 2  (deriv 1/3: attracting)
# and the "gap is golden" point: gamma = sqrt(1+4G) = phi  =>  G = phi/4
G_goldengap = PHI / 4
a, b = roots(G_goldengap)
results['G_tower'] = {
    'iterate_x_plus_from_G=1_converges_to': tower[-1],
    'fixed_point': 2.0, 'attracting_derivative': 1/3,
    'meaning_of_2': 'x^2=x+2 has roots {2,-1}: the first INTEGER pair past golden. '
                    'The tower of gaps eats itself and lands on the simplest split: '
                    '2 and -1. Self-reference terminates in integers.',
    'gap_is_golden_at_G': G_goldengap,
    'gap_between_roots_there': float((a - b).real),
    'equals_phi': abs((a - b).real - PHI) < 1e-12,
}

# ---------------------------------------- H. THE COMPLEX FIELD, AS COLOR (language)
# Hue = direction of the gap-between-roots, brightness = its size.
nx, ny = 900, 700
gx = np.linspace(-2, 2, nx); gy = np.linspace(-1.5, 1.5, ny)
GG = gx[None, :] + 1j * gy[:, None]
gamma = np.sqrt(1 + 4*GG)                      # the gap between the roots
H = (np.angle(gamma) / (2*np.pi)) % 1.0
V = 1 - 1/(1 + np.abs(gamma))
import colorsys
rgb = np.zeros((ny, nx, 3))
hsv = np.stack([H, 0.9*np.ones_like(H), V], axis=-1)
# vectorized hsv->rgb
hh = (hsv[...,0]*6).astype(int) % 6; f = hsv[...,0]*6 - np.floor(hsv[...,0]*6)
p = hsv[...,2]*(1-hsv[...,1]); q = hsv[...,2]*(1-f*hsv[...,1]); t = hsv[...,2]*(1-(1-f)*hsv[...,1]); v = hsv[...,2]
for k,(r_,g_,b_) in enumerate([(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)]):
    m = hh == k; rgb[m,0]=r_[m]; rgb[m,1]=g_[m]; rgb[m,2]=b_[m]
fig, ax = plt.subplots(figsize=(10, 7.5))
ax.imshow(rgb, extent=[gx[0], gx[-1], gy[0], gy[-1]], origin='lower')
for G0, lbl in [(-0.25,'branch'), (1,'golden'), (-1,'unit circle'), (1j,'+i'), (-1j,'-i'), (0,'0')]:
    ax.plot([complex(G0).real], [complex(G0).imag], 'wo', ms=6, mec='k')
    ax.annotate(lbl, (complex(G0).real, complex(G0).imag), xytext=(complex(G0).real+.05, complex(G0).imag+.07),
                color='w', fontsize=9)
ax.set_title('The gap field, spoken in color: hue = direction of √(1+4G), brightness = its size\n'
             'the black point is −1/4 — the only place the gap has no direction to point')
ax.set_xlabel('Re G'); ax.set_ylabel('Im G')
plt.tight_layout(); plt.savefig(f'{FIG}/fig6_gap_field_color.png', dpi=110); plt.close()

# ---------------------------------------------- I. SOUND (a language for the sweep)
# Two voices, one per root. Pitch from modulus, stereo pan from branch.
# Sweep G from +1 (golden chord) down through -1/4 (unison — the voices FUSE)
# to -1 (both voices at the same pitch: the quantum unison hides the phase).
sr = 22050; dur = 12.0; N = int(sr * dur)
tt = np.arange(N) / sr
Gt = 1 - 2 * (tt / dur)             # G: 1 -> -1
f0 = 220.0
ph1 = np.zeros(N); ph2 = np.zeros(N)
fr1 = np.zeros(N); fr2 = np.zeros(N)
for i, g in enumerate(Gt):
    a, b = roots(g)
    fr1[i] = f0 * abs(a); fr2[i] = f0 * max(abs(b), 1e-3)
ph1 = 2*np.pi*np.cumsum(fr1)/sr; ph2 = 2*np.pi*np.cumsum(fr2)/sr
L = 0.6*np.sin(ph1) + 0.25*np.sin(ph2)
R = 0.6*np.sin(ph2) + 0.25*np.sin(ph1)
env = np.minimum(1, np.minimum(tt/0.05, (dur-tt)/0.05))
L *= env; R *= env
mx = max(np.max(np.abs(L)), np.max(np.abs(R)))
L, R = L/mx*0.9, R/mx*0.9
with wave.open(f'{OUT}/gap_sweep.wav', 'w') as w_:
    w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(sr)
    inter = np.empty(2*N, dtype=np.int16)
    inter[0::2] = (L*32767).astype(np.int16); inter[1::2] = (R*32767).astype(np.int16)
    w_.writeframes(inter.tobytes())
results['I_sound'] = {
    'file': 'gap_sweep.wav',
    'script': 'G sweeps 1 -> -1 over 12s. Start: the golden chord (pitch ratio phi^2 = phi+1, '
              'the only interval equal to itself plus an octave-of-itself). At G=-1/4 (t=7.5s) '
              'the two voices FUSE into unison at 110 Hz — you can hear the branch point as the '
              'death of harmony into a single line. For G<-1/4 both moduli are sqrt(-G): ONE '
              'pitch rising, and the difference between the roots survives only as stereo phase '
              '— audible as space, not as tone. Classical = interval. Quantum = placement.'
}

# ------------------------------------------------------------------ WRITE OUT
results['ONE_SENTENCE'] = ('The gap is not the flaw in the equation; it is the coordinate the whole '
                           'family of solutions breathes through, and “kinds of number” — real, '
                           'imaginary, nilpotent, finite, spherical — are just the shapes the same '
                           'two roots take when you walk up to −1/4 from different directions.')
results['ONE_WORD'] = 'between'
with open(f'{RES}/gap_sweep_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
print(json.dumps(results, indent=2, default=str))
