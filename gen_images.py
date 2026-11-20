"""
Generate 4 research images for the Applied Analysis group website.
Run: python3 gen_images.py
Outputs:  images/domain_branching.png   (Knüpfer  — needle domains)
          images/ferromagnet_ellipsoid.png (Laux — Allen-Cahn / mcf)
          images/phase_separation.png    (Marciniak-Czochra — Cahn-Hilliard)
          images/hydra_pattern.png       (Fuhrmann — Turing patterns)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Ellipse, Polygon
from scipy.ndimage import gaussian_filter
import os

os.makedirs('images', exist_ok=True)
rng = np.random.default_rng(42)

# ═══════════════════════════════════════════════════════════════
# IMAGE 1 — 3D CRYSTAL CELL WITH HIERARCHICAL NEEDLE DOMAINS
# (Knüpfer — branching theory)
# 2D oblique (cabinet) projection, 3 harmonious muted colours.
# ═══════════════════════════════════════════════════════════════

C1   = '#1c4a7c'   # steel blue   — large central needle
C2   = '#1f7260'   # sea teal     — medium needles
C3   = '#8a6318'   # warm brass   — fine / surface needles
C_bg = '#f0ede6'   # warm off-white background

Lx, Ly, Lz = 4.0, 1.0, 1.35   # width × height × depth (box)

ang1 = np.radians(23)
sc1  = 0.44                     # cabinet foreshortening

def proj1(x, y, z):
    return x + z * np.cos(ang1) * sc1, y + z * np.sin(ang1) * sc1

px_max1 = Lx + Lz * np.cos(ang1) * sc1   # ≈ 4.55
py_max1 = Ly + Lz * np.sin(ang1) * sc1   # ≈ 1.24
mg1 = 0.18

fig1, ax1 = plt.subplots(figsize=(5.0, 1.8), dpi=120)
fig1.patch.set_facecolor(C_bg)
ax1.set_facecolor(C_bg)
ax1.set_xlim(-mg1, px_max1 + mg1)
ax1.set_ylim(-mg1, py_max1 + mg1)
ax1.set_aspect('equal')
ax1.axis('off')

def dpoly(pts_3d, fc, ec, zo, lw=0.7, alpha=1.0):
    pts2 = np.array([proj1(*p) for p in pts_3d])
    ax1.add_patch(Polygon(pts2, closed=True, fc=fc, ec=ec,
                          lw=lw, zorder=zo, alpha=alpha))

# ── box faces, back-to-front ──────────────────────────────────
# back face (z = Lz)
dpoly([(0,0,Lz),(Lx,0,Lz),(Lx,Ly,Lz),(0,Ly,Lz)],
      fc='#c0bdb6', ec='#908d86', zo=1, lw=0.6)
# left face (x = 0)
dpoly([(0,0,0),(0,0,Lz),(0,Ly,Lz),(0,Ly,0)],
      fc='#ccc9c2', ec='#908d86', zo=2, lw=0.6)
# bottom face (y = 0)
dpoly([(0,0,0),(Lx,0,0),(Lx,0,Lz),(0,0,Lz)],
      fc='#c8c5be', ec='#908d86', zo=2, lw=0.6)

# ── needles (sorted back → front by z) ───────────────────────
needles1 = []

# Level 1 — 1 large steel-blue needle at centre
needles1.append((Lx/2, Ly/2, Lz/2, 1.60, 0.088, C1, 0.94))

# Level 2 — 8 medium teal needles in symmetric yz grid
for fy, fz in [(0.25,0.20),(0.75,0.20),(0.25,0.80),(0.75,0.80),
               (0.30,0.22),(0.70,0.22),(0.30,0.78),(0.70,0.78)]:
    needles1.append((Lx*0.5 + rng.uniform(-0.4,0.4),
                     Ly*fy, Lz*fz, 0.65, 0.052, C2, 0.90))

# Level 3 — 16 fine brass needles near z-surfaces
cx3 = np.linspace(Lx*0.08, Lx*0.92, 8)
cy3 = rng.uniform(Ly*0.10, Ly*0.90, 8)
for i in range(8):
    cz_a = rng.uniform(Lz*0.06, Lz*0.17)
    cz_b = rng.uniform(Lz*0.83, Lz*0.94)
    needles1.append((cx3[i], cy3[i], cz_a, 0.28, 0.030, C3, 0.80))
    needles1.append((cx3[i], cy3[i], cz_b, 0.28, 0.030, C3, 0.80))

# sort by z descending (draw farthest first)
needles1.sort(key=lambda n: -n[2])

for cx, cy, cz, rx, ry, col, alpha in needles1:
    px, py = proj1(cx, cy, cz)
    # linear z-order: z=Lz → zorder≈3, z=0 → zorder≈4.8
    zo = 3.0 + (1.0 - cz / Lz) * 1.8
    # body
    ax1.add_patch(Ellipse((px, py), 2*rx, 2*ry,
                          fc=col, ec='none', zorder=zo, alpha=alpha))
    # subtle highlight
    ax1.add_patch(Ellipse((px, py + ry*0.28),
                          2*rx*0.80, ry*0.45,
                          fc='white', ec='none',
                          zorder=zo+0.05, alpha=alpha*0.13))

# ── front faces (drawn after needles so they partially occlude) ─
# top face (y = Ly)
dpoly([(0,Ly,0),(Lx,Ly,0),(Lx,Ly,Lz),(0,Ly,Lz)],
      fc='#dedad3', ec='#808078', zo=5, lw=0.7, alpha=0.80)
# right face (x = Lx)
dpoly([(Lx,0,0),(Lx,0,Lz),(Lx,Ly,Lz),(Lx,Ly,0)],
      fc='#d4d1ca', ec='#808078', zo=5, lw=0.7, alpha=0.80)

# ── wireframe edges ───────────────────────────────────────────
EW = 0.9
# front rectangle (z = 0)
for (x0,y0),(x1,y1) in [((0,0),(Lx,0)),((Lx,0),(Lx,Ly)),
                          ((Lx,Ly),(0,Ly)),((0,Ly),(0,0))]:
    p0 = proj1(x0, y0, 0); p1 = proj1(x1, y1, 0)
    ax1.plot([p0[0],p1[0]],[p0[1],p1[1]], color='#706d66', lw=EW, zorder=10)
# 4 depth edges
for x,y in [(0,0),(Lx,0),(Lx,Ly),(0,Ly)]:
    p0 = proj1(x,y,0); p1 = proj1(x,y,Lz)
    ax1.plot([p0[0],p1[0]],[p0[1],p1[1]], color='#706d66', lw=EW*0.8, zorder=10)
# back rectangle (z = Lz, lighter)
for (x0,y0),(x1,y1) in [((0,0),(Lx,0)),((Lx,0),(Lx,Ly)),
                          ((Lx,Ly),(0,Ly)),((0,Ly),(0,0))]:
    p0 = proj1(x0, y0, Lz); p1 = proj1(x1, y1, Lz)
    ax1.plot([p0[0],p1[0]],[p0[1],p1[1]], color='#908d86', lw=EW*0.65,
             zorder=10, alpha=0.55)

plt.savefig('images/domain_branching.png', dpi=120,
            bbox_inches='tight', pad_inches=0.03, facecolor=C_bg)
plt.close(fig1)
print("1/4  images/domain_branching.png  ✓")

# ═══════════════════════════════════════════════════════════════
# IMAGE 2 — ALLEN-CAHN PHASE FIELD / MEAN CURVATURE FLOW
# (Laux — geometric phase transitions)
# Multiple droplets with diffuse tanh-interfaces; muted palette.
# ═══════════════════════════════════════════════════════════════

W2, H2 = 500, 500
x2 = np.linspace(-1.25, 1.25, W2)
y2 = np.linspace(-1.25, 1.25, H2)
X2, Y2 = np.meshgrid(x2, y2)

eps2 = 0.055   # interface width

# (cx, cy, radius) — a large central inclusion + satellites
inclusions2 = [
    ( 0.00,  0.07,  0.52),
    (-0.62, -0.52,  0.27),
    ( 0.66, -0.46,  0.22),
    (-0.52,  0.65,  0.17),
    ( 0.66,  0.60,  0.14),
    (-0.86,  0.09,  0.10),
    ( 0.86,  0.09,  0.09),
    ( 0.08, -0.92,  0.08),
]

phi2 = np.full((H2, W2), -1.0)
for cx, cy, r in inclusions2:
    dist = np.sqrt((X2 - cx)**2 + (Y2 - cy)**2)
    phi2 = np.maximum(phi2, np.tanh((r - dist) / eps2))

# slight noise for organic texture
phi2 += gaussian_filter(rng.standard_normal((H2, W2)), sigma=1.2) * 0.025
phi2 = np.clip(phi2, -1.1, 1.1)

# Colormap: dark navy → cobalt → cyan (interface glow) → amber → pale gold
cmap2 = LinearSegmentedColormap.from_list('mcf', [
    (0.00, '#040c20'),
    (0.25, '#0a2d6a'),
    (0.47, '#1055a8'),
    (0.50, '#1fa8b0'),   # interface glow
    (0.53, '#c09020'),
    (0.75, '#e8c840'),
    (1.00, '#fff4a0'),
])

fig2, ax2 = plt.subplots(figsize=(4.0, 4.0), dpi=120)
fig2.patch.set_facecolor('#040c20')
ax2.imshow(phi2, cmap=cmap2, aspect='equal', vmin=-1.1, vmax=1.1,
           interpolation='lanczos', origin='lower')
ax2.axis('off')
plt.savefig('images/ferromagnet_ellipsoid.png', dpi=120,
            bbox_inches='tight', pad_inches=0.02, facecolor='#040c20')
plt.close(fig2)
print("2/4  images/ferromagnet_ellipsoid.png  ✓")

# ═══════════════════════════════════════════════════════════════
# IMAGE 3 — CAHN-HILLIARD SPINODAL DECOMPOSITION
# (Marciniak-Czochra — reaction-diffusion / phase separation)
# Spectral semi-implicit time-stepping on a periodic domain.
# Colourmap: dark blue → green → yellow → orange → red  (like uploaded ref.)
# ═══════════════════════════════════════════════════════════════

N3   = 256
dx3  = 1.0
dt3  = 0.5
eps2_3 = 0.8   # ε² in Cahn-Hilliard ∂u/∂t = Δ(u³ - u - ε²Δu)

# Initial condition: small fluctuations around 0
u3 = rng.uniform(-0.08, 0.08, (N3, N3))

# Wavenumber array
kx3 = np.fft.fftfreq(N3, d=dx3 / (2*np.pi))
KX3, KY3 = np.meshgrid(kx3, kx3)
K2_3 = KX3**2 + KY3**2

# Semi-implicit scheme:  û^{n+1} (1 + dt k² ε² k²) = û^n - dt k² F{u³-u}^n
print("   running Cahn-Hilliard simulation…")
for step in range(3200):
    uhat = np.fft.fft2(u3)
    nl   = np.fft.fft2(u3**3 - u3)
    uhat = (uhat - dt3 * K2_3 * nl) / (1.0 + dt3 * eps2_3 * K2_3**2)
    u3   = np.real(np.fft.ifft2(uhat))

# Colormap: dark-blue ⟶ bright-blue ⟶ green ⟶ yellow ⟶ orange ⟶ red
cmap3 = LinearSegmentedColormap.from_list('ch', [
    (0.00, '#0820b0'),
    (0.20, '#0888e8'),
    (0.45, '#10c840'),
    (0.65, '#c0e010'),
    (0.82, '#f0a000'),
    (1.00, '#e82010'),
])

fig3, ax3 = plt.subplots(figsize=(5.0, 3.4), dpi=120)
fig3.patch.set_facecolor('#0820b0')
p3 = np.percentile(u3, [2, 98])
ax3.imshow(u3, cmap=cmap3, aspect='equal', interpolation='lanczos',
           origin='lower', vmin=p3[0], vmax=p3[1])
ax3.axis('off')
plt.savefig('images/phase_separation.png', dpi=120,
            bbox_inches='tight', pad_inches=0.02, facecolor='#0820b0')
plt.close(fig3)
print("3/4  images/phase_separation.png  ✓")

# ═══════════════════════════════════════════════════════════════
# IMAGE 4 — SPATIAL SIR EPIDEMIC WAVE MODEL
# (Fuhrmann — mathematical epidemiology, travelling wave solutions)
# Reaction-diffusion SIR on 2-D domain: multiple infection seeds
# create glowing wave fronts that interact as they spread.
# S (susceptible) = dark navy "fuel"
# I (infected)    = bright warm wave front
# R (recovered)   = dark gray, extinguished
# ═══════════════════════════════════════════════════════════════

N4     = 300
dt4    = 0.50
beta4  = 0.46    # transmission rate
gamma4 = 0.07    # recovery rate  → thin glowing wave front
D_I4   = 0.35    # spatial diffusion of infectious density

S4 = np.ones((N4, N4))
I4 = np.zeros((N4, N4))
R4 = np.zeros((N4, N4))

# 3 seeds in an asymmetric triangle
seeds4 = [
    (N4//2,   N4//3),
    (N4//4,   2*N4//3),
    (3*N4//4, 2*N4//3),
]
for (cx, cy) in seeds4:
    yy4, xx4 = np.ogrid[0:N4, 0:N4]
    mask_s = (xx4 - cx)**2 + (yy4 - cy)**2 <= 49
    I4[mask_s] = 0.90
    S4[mask_s] = 0.10

def lap_zero_flux(A):
    """2-D Laplacian with zero-flux (Neumann) boundaries."""
    r = np.zeros_like(A)
    r[1:-1,1:-1] = (A[2:,1:-1] + A[:-2,1:-1] +
                    A[1:-1,2:] + A[1:-1,:-2] - 4.0*A[1:-1,1:-1])
    r[0,:]  = r[1,:];  r[-1,:] = r[-2,:]
    r[:,0]  = r[:,1];  r[:,-1] = r[:,-2]
    return r

print("   running spatial SIR simulation…")
# Stop at step 200: wave fronts from the 3 seeds are just meeting —
# the mathematically most interesting moment of wave-front interaction.
for step in range(200):
    inf4  = beta4  * S4 * I4
    rec4  = gamma4 * I4
    diff4 = D_I4   * lap_zero_flux(I4)
    S4 += dt4 * (-inf4)
    I4 += dt4 * ( inf4 - rec4 + diff4)
    R4 += dt4 * ( rec4)
    S4 = np.clip(S4, 0, 1)
    I4 = np.clip(I4, 0, 1)
    R4 = np.clip(R4, 0, 1)

# RGB visualisation
# S → near-black deep blue (susceptible "fuel")
# I → bright warm orange/yellow (active wave front)
# R → dim blue-gray (recovered, extinguished)
r_ch = I4 * 1.00 + R4 * 0.07 + S4 * 0.01
g_ch = I4 * 0.55 + R4 * 0.20 + S4 * 0.02
b_ch = I4 * 0.06 + R4 * 0.42 + S4 * 0.60

# Gamma correction for visual punch
r_ch = np.power(np.clip(r_ch, 0, 1), 0.58)
g_ch = np.power(np.clip(g_ch, 0, 1), 0.58)
b_ch = np.power(np.clip(b_ch, 0, 1), 0.58)

rgb4 = np.stack([r_ch, g_ch, b_ch], axis=-1)

fig4, ax4 = plt.subplots(figsize=(4.0, 4.0), dpi=120)
fig4.patch.set_facecolor('black')
ax4.set_facecolor('black')
ax4.imshow(rgb4, aspect='equal', interpolation='lanczos', origin='lower')
ax4.axis('off')
plt.savefig('images/hydra_pattern.png', dpi=120,
            bbox_inches='tight', pad_inches=0.03, facecolor='black')
plt.close(fig4)
print("4/4  images/hydra_pattern.png  ✓")
print("\nAll done.")
