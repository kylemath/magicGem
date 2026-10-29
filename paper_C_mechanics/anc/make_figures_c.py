"""
make_figures_c.py — Generates all 7 multi-panel publication figures for Paper C:
1. figures/fig_hero_squares_gallery.pdf
2. figures/fig_origin_vectors_3d.pdf
3. figures/fig_ring_vectors.pdf
4. figures/fig_precession_dynamics.pdf
5. figures/fig_nested_diamonds.pdf
6. figures/fig_wireframes_and_nets.pdf
7. figures/fig_mirror_stacking.pdf
"""
import os, sys, json
from collections import Counter, deque
from fractions import Fraction
from math import sqrt, atan2, degrees, pi, sin, cos, gcd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon as MplPolygon, Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
from scipy.spatial import ConvexHull
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.abspath(os.path.join(HERE, '..', 'figures'))
os.makedirs(FIG_DIR, exist_ok=True)
ANC_A = os.path.abspath(os.path.join(HERE, '..', '..', 'paper_A_gems', 'anc'))
sys.path.insert(0, ANC_A)
from gem_geometry import scaled_points, exact_hull, _hull2d

S880 = np.loadtxt(os.path.join(ANC_A, 'squares880.txt'), dtype=int).reshape(880, 4, 4)
geom_data = json.load(open(os.path.join(ANC_A, 'results_geometry.json')))
dudeney_groups = geom_data['dudeney_group']

# Okabe-Ito palette matching Paper A (vecfig.py / gemfig.py)
VERM = '#D55E00'   # z > 0 (above origin O)
BLUE = '#0072B2'   # z < 0 (below origin O)
WARN = '#CC0099'   # resultant / imbalance warning arrow
GREEN = '#009E73'
GOLD = '#E69F00'
HALO = [pe.withStroke(linewidth=2.2, foreground='white')]
PILL_BG = dict(boxstyle='round,pad=0.15', facecolor='white', alpha=0.94, edgecolor='none')

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9.2,
    'axes.titlesize': 9.5,
    'axes.labelsize': 9.0,
    'xtick.labelsize': 8.0,
    'ytick.labelsize': 8.0,
    'legend.fontsize': 7.2,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'figure.dpi': 300
})

X4 = np.array([[2*j - 3 for j in range(4)] for i in range(4)], dtype=int)
Y4 = np.array([[3 - 2*i for j in range(4)] for i in range(4)], dtype=int)
R2_4 = X4**2 + Y4**2
mask_in = (R2_4 == 2)
mask_mid = (R2_4 == 10)
mask_out = (R2_4 == 18)

def zcol_strong(z):
    return VERM if z > 0 else BLUE

def draw_floor_3d(ax, zf, n=4, scale_xy=1.0, fc='#EEEEEE', ec='#BBBBBB'):
    for i in range(n):
        for j in range(n):
            x0 = (j - (n - 1) / 2 - 0.5) * scale_xy
            y0 = ((n - 1) / 2 - i - 0.5) * scale_xy
            s = 1.0 * scale_xy
            sq = [(x0, y0, zf), (x0 + s, y0, zf), (x0 + s, y0 + s, zf), (x0, y0 + s, zf)]
            ax.add_collection3d(Poly3DCollection([sq], facecolor=fc, edgecolor=ec, linewidths=0.45, alpha=0.45, zorder=0))

def draw_unit_sphere_wireframe(ax, rad=1.0):
    u = np.linspace(0, 2 * np.pi, 36)
    v = np.linspace(0, np.pi, 19)
    xs = rad * np.outer(np.cos(u), np.sin(v))
    ys = rad * np.outer(np.sin(u), np.sin(v))
    zs = rad * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(xs, ys, zs, color='#DCE6EC', alpha=0.14, linewidth=0, shade=False, zorder=1)
    th = np.linspace(0, 2 * np.pi, 120)
    ax.plot(rad * np.cos(th), rad * np.sin(th), np.zeros_like(th), color='#778899', lw=0.75, ls='--', alpha=0.7, zorder=2)
    for phi in [0.0, np.pi / 2]:
        ax.plot(rad * np.cos(th) * np.cos(phi), rad * np.cos(th) * np.sin(phi), rad * np.sin(th),
                color='#99AABB', lw=0.55, ls=':', alpha=0.55, zorder=2)

# ==============================================================================
# FIGURE 0 (NEW FIGURE 1): VISUAL ANATOMY OF THE SIX FLAGSHIP ORDER-FOUR SQUARES
# ==============================================================================
print("Generating New Figure 1: fig_hero_squares_gallery.pdf ...")
fig, axes = plt.subplots(2, 3, figsize=(14.4, 8.2))

def setup_grid_panel(ax, title_str, badge_str, badge_col='#1A365D'):
    ax.set_xlim(-2.22, 2.22)
    ax.set_ylim(-2.65, 2.18)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title_str, fontsize=9.3, fontweight='bold', pad=4)
    # Coordinate crosshairs through O=(0,0)
    ax.plot([-1.95, 1.95], [0, 0], color='#888888', lw=0.6, ls=':', zorder=1)
    ax.plot([0, 0], [-1.95, 1.95], color='#888888', lw=0.6, ls=':', zorder=1)
    ax.scatter([0], [0], color='black', s=24, zorder=12)
    ax.text(0.11, -0.14, '$O$', fontsize=7.6, fontweight='bold', color='black', path_effects=HALO, zorder=13)
    ax.text(0.0, -2.35, badge_str, ha='center', va='center', fontsize=7.5, fontweight='bold',
            color=badge_col, bbox=dict(boxstyle='round,pad=0.24', facecolor='#F8FAFC', edgecolor=badge_col, lw=0.85))

# (a) #175 (Durer 1514, Group III Associative)
ax = axes[0, 0]
S175 = S880[174]
v0_175 = set(exact_hull(S175)['vertices'])
setup_grid_panel(ax, '(a) Dürer #175 (1514, Group III Associative)',
                 r'Antipodal $s+s^\prime=17$: $\mathbf{V}_\beta\equiv\mathbf{0},\; Q_{xy}=0,\; \mathbf{c}_0=\mathbf{0},\; N_{\mathrm{tabs}}=11$',
                 badge_col='#0f5943')
for i in range(4):
    for j in range(4):
        idx = 4*i + j
        xc, yc = j - 1.5, 1.5 - i
        val = S175[i, j]
        is_v0 = idx in v0_175
        fc = '#D8EFE9' if is_v0 else '#FFF3CD'
        ec = '#007A53' if is_v0 else '#D97706'
        lw = 1.1 if is_v0 else 2.2
        ax.add_patch(Rectangle((xc - 0.44, yc - 0.44), 0.88, 0.88, facecolor=fc, edgecolor=ec, lw=lw, zorder=2))
        ax.text(xc, yc + 0.06, str(val), ha='center', va='center', fontsize=10.2, fontweight='bold', color='#111111', zorder=5)
        ax.text(xc, yc - 0.25, '$V_0$' if is_v0 else '$V_1$ core', ha='center', va='center',
                fontsize=6.2, fontweight='bold', color='#005A3C' if is_v0 else '#B45309', zorder=5)
# Antipodal connector rays through O
for (x1, y1), col_p in [((-1.5, 1.5), '#0072B2'), ((-0.5, 1.5), '#D55E00'), ((-0.5, 0.5), '#984ea3')]:
    ax.plot([x1, -x1], [y1, -y1], color=col_p, lw=1.15, ls='--', alpha=0.65, zorder=3)

# (b) #70 (Group VI, Pell 9/4 approx sqrt(5) Champion)
ax = axes[0, 1]
S70 = S880[69]
setup_grid_panel(ax, r'(b) Square #70 (Group VI, Pell $9/4\approx\sqrt{5}$ Champion)',
                 r'$\mathbf{d}_{\mathrm{out}}=5\mathbf{d}_{\mathrm{in}} \Rightarrow \|\mathbf{v}\|/\|\mathbf{u}\|=18/8=9/4,\; \min\|\mathbf{B}_{\mathrm{unit}}\|=0.0705$',
                 badge_col='#b30000')
for i in range(4):
    for j in range(4):
        xc, yc = j - 1.5, 1.5 - i
        val = S70[i, j]
        r2 = R2_4[i, j]
        if r2 == 2:
            fc, ec, r_lbl, tc = '#D1FAE5', '#059669', r'$R_{\mathrm{in}}$', '#065F46'
        elif r2 == 10:
            fc, ec, r_lbl, tc = '#DBEAFE', '#2563EB', r'$R_{\mathrm{mid}}$', '#1E40AF'
        else:
            fc, ec, r_lbl, tc = '#FEF3C7', '#D97706', r'$R_{\mathrm{out}}$', '#92400E'
        ax.add_patch(Rectangle((xc - 0.44, yc - 0.44), 0.88, 0.88, facecolor=fc, edgecolor=ec, lw=1.35, zorder=2))
        ax.text(xc, yc + 0.07, str(val), ha='center', va='center', fontsize=10.2, fontweight='bold', color='#111111', zorder=5)
        ax.text(xc, yc - 0.25, r_lbl, ha='center', va='center', fontsize=6.2, fontweight='bold', color=tc, zorder=5)
# Dipole arrows along +x in the center gap (y = +-0.04) with labels cleanly in the right margin
ax.add_patch(FancyArrowPatch((0, 0.04), (0.88, 0.04), arrowstyle='-|>', mutation_scale=9.5, lw=2.2, color='#059669', zorder=10))
ax.add_patch(FancyArrowPatch((0, -0.04), (1.92, -0.04), arrowstyle='-|>', mutation_scale=10.5, lw=2.4, color='#D97706', zorder=10))
ax.text(-0.98, 2.04, r'$\mathbf{d}_{\mathrm{in}}=(3,0)$', fontsize=6.8, fontweight='bold', color='#065F46', ha='center', bbox=PILL_BG, zorder=11)
ax.text(0.98, 2.04, r'$\mathbf{d}_{\mathrm{out}}=(15,0)=5\mathbf{d}_{\mathrm{in}}$', fontsize=6.8, fontweight='bold', color='#92400E', ha='center', bbox=PILL_BG, zorder=11)

# (c) #45 vs #54 (Group VI, 1-Swap Heavy-to-Hollow Core Siblings & alpha*=-1)
ax = axes[0, 2]
S45 = S880[44]
v0_45 = set(exact_hull(S45)['vertices'])
setup_grid_panel(ax, r'(c) #45 $\leftrightarrow$ #54 (1-Swap Heavy-to-Hollow Core Siblings)',
                 r'Swap $(8,9)\leftrightarrow(15,2)$: #45 ($\alpha^*=-1,\;\frac{\Delta\rho_1}{\rho_0}=+\frac{85}{61}$) $\to$ #54 (cavity $-\frac{57}{58}$)',
                 badge_col='#7C2D12')
for i in range(4):
    for j in range(4):
        idx = 4*i + j
        xc, yc = j - 1.5, 1.5 - i
        val = S45[i, j]
        is_v0 = idx in v0_45
        is_swap = (i in (1, 2) and j in (0, 3))
        fc = '#FEE2E2' if is_swap else ('#E0F2FE' if is_v0 else '#FEF3C7')
        ec = '#DC2626' if is_swap else ('#0284C7' if is_v0 else '#D97706')
        lw = 2.1 if (is_swap or not is_v0) else 1.1
        ax.add_patch(Rectangle((xc - 0.44, yc - 0.44), 0.88, 0.88, facecolor=fc, edgecolor=ec, lw=lw, zorder=2))
        ax.text(xc, yc + 0.08, str(val), ha='center', va='center', fontsize=10.2, fontweight='bold', color='#111111', zorder=5)
        if is_swap:
            alt_v = S880[53][i, j]
            ax.text(xc, yc - 0.24, f'#54: {alt_v}', ha='center', va='center', fontsize=6.1, fontweight='bold', color='#B91C1C', zorder=5)
        else:
            ax.text(xc, yc - 0.24, '$V_0$' if is_v0 else '$V_1$ core', ha='center', va='center',
                    fontsize=6.1, fontweight='bold', color='#0369A1' if is_v0 else '#B45309', zorder=5)
# Double-headed swap arrows on left and right borders between rows 2 and 3
for x_arr in (-1.5, 1.5):
    ax.add_patch(FancyArrowPatch((x_arr - 0.34 if x_arr < 0 else x_arr + 0.34, 0.45),
                                 (x_arr - 0.34 if x_arr < 0 else x_arr + 0.34, -0.45),
                                 arrowstyle='<->', mutation_scale=9.5, lw=1.8, color='#DC2626', zorder=11))

# (d) #46 (Group VI, Dzhanibekov Champion |Q_xy| = 60)
ax = axes[1, 0]
S46 = S880[45]
setup_grid_panel(ax, r'(d) Square #46 (Group VI, Dzhanibekov Champion $|Q_{xy}|=60$)',
                 r'$\max |Q_{xy}| = 60 \Rightarrow \mathrm{Fastest}\ 180^\circ\ \mathrm{Flip}$ ($I_1=110 < I_2=230 < I_3=340$)',
                 badge_col='#991B1B')
for i in range(4):
    for j in range(4):
        xc, yc = j - 1.5, 1.5 - i
        val = S46[i, j]
        q_cell = (val - 8.5) * xc * yc
        if q_cell > 5.0:
            fc, ec, tc = '#FCA5A5', '#B91C1C', '#7F1D1D'
        elif q_cell > 0:
            fc, ec, tc = '#FEE2E2', '#EF4444', '#991B1B'
        else:
            fc, ec, tc = '#DBEAFE', '#3B82F6', '#1E3A8A'
        ax.add_patch(Rectangle((xc - 0.44, yc - 0.44), 0.88, 0.88, facecolor=fc, edgecolor=ec, lw=1.25, zorder=2))
        ax.text(xc, yc + 0.08, str(val), ha='center', va='center', fontsize=10.2, fontweight='bold', color='#111111', zorder=5)
        ax.text(xc, yc - 0.24, f'{q_cell:+.1f}', ha='center', va='center', fontsize=5.9, fontweight='bold', color=tc, zorder=5)
# Diagonal principal axes y = +x (I_1=110 stable) and y = -x (I_2=230 unstable flip axis)
ax.plot([-1.88, 1.88], [-1.88, 1.88], color='#059669', lw=1.7, ls='-', alpha=0.85, zorder=8)
ax.plot([-1.88, 1.88], [1.88, -1.88], color='#DC2626', lw=1.9, ls='--', alpha=0.9, zorder=8)
ax.text(1.18, 2.04, r'$y=+x$ ($I_1=110$)', fontsize=6.6, fontweight='bold', color='#065F46', ha='center', bbox=PILL_BG, zorder=12)
ax.text(-1.12, 2.04, r'$y=-x$ ($I_2=230$ flip)', fontsize=6.6, fontweight='bold', color='#991B1B', ha='center', bbox=PILL_BG, zorder=12)

# (e) #673 (Group VI, (8,8) Diamond-in-a-Diamond Champion)
ax = axes[1, 1]
S673 = S880[672]
v0_673 = set(exact_hull(S673)['vertices'])
setup_grid_panel(ax, r'(e) Square #673 ($(8,8)$ Diamond-in-a-Diamond Champion)',
                 r'$8$ Outer U-Cradle $V_0$ $\supset$ $8$ Inner T-Core $V_1$: $\min\frac{\Delta\rho_1}{\rho_0}=\frac{5}{4},\; \frac{d_1}{d_0}=0.793$',
                 badge_col='#065F46')
for i in range(4):
    for j in range(4):
        idx = 4*i + j
        xc, yc = j - 1.5, 1.5 - i
        val = S673[i, j]
        is_v0 = idx in v0_673
        fc = '#D1FAE5' if is_v0 else '#FEF3C7'
        ec = '#059669' if is_v0 else '#D97706'
        tc = '#065F46' if is_v0 else '#92400E'
        ax.add_patch(Rectangle((xc - 0.44, yc - 0.44), 0.88, 0.88, facecolor=fc, edgecolor=ec, lw=1.6, zorder=2))
        ax.text(xc, yc + 0.08, str(val), ha='center', va='center', fontsize=10.2, fontweight='bold', color='#111111', zorder=5)
        ax.text(xc, yc - 0.24, 'U-hull $V_0$' if is_v0 else 'T-core $V_1$', ha='center', va='center',
                fontsize=5.9, fontweight='bold', color=tc, zorder=5)
# Show opposing centroids c_0 on -y and c_1 on +y along the central vertical gutter (x = 0) with top/bottom margin labels
ax.add_patch(FancyArrowPatch((0, -0.05), (0, -0.92), arrowstyle='-|>', mutation_scale=9.5, lw=2.2, color='#059669', zorder=10))
ax.add_patch(FancyArrowPatch((0, 0.05), (0, 0.92), arrowstyle='-|>', mutation_scale=9.5, lw=2.2, color='#D97706', zorder=10))
ax.text(-0.95, 2.04, r'Outer $\mathbf{c}_0$ ($-y$)', fontsize=6.6, fontweight='bold', color='#065F46', ha='center', bbox=PILL_BG, zorder=11)
ax.text(0.95, 2.04, r'Core $\mathbf{c}_1$ ($+y$)', fontsize=6.6, fontweight='bold', color='#92400E', ha='center', bbox=PILL_BG, zorder=11)

# (f) #763 vs #756 (Group VI, Knight's-Move Tower Champion)
ax = axes[1, 2]
S763 = S880[762]
setup_grid_panel(ax, r"(f) #763 $\leftrightarrow$ #756 (Knight's-Move Tower & Balanced Sibling)",
                 r'Centred $A_{xy}=5$ facets $\{13..16\},\{1..4\}$; swap $(16,1)\leftrightarrow(4,13) \to$ #756 ($\mathbf{c}_0=\mathbf{0}$)',
                 badge_col='#1E3A8A')
for i in range(4):
    for j in range(4):
        xc, yc = j - 1.5, 1.5 - i
        val = S763[i, j]
        is_top = val in (13, 14, 15, 16)
        is_bot = val in (1, 2, 3, 4)
        is_swap = (i in (1, 2) and j in (0, 3))
        if is_top:
            fc, ec, tc, lbl = '#FEF08A', '#CA8A04', '#854D0E', '$F_+$ top'
        elif is_bot:
            fc, ec, tc, lbl = '#DBEAFE', '#2563EB', '#1E40AF', '$F_-$ bot'
        else:
            fc, ec, tc, lbl = '#F1F5F9', '#94A3B8', '#475569', 'mid'
        ax.add_patch(Rectangle((xc - 0.44, yc - 0.44), 0.88, 0.88, facecolor=fc, edgecolor=ec, lw=1.6 if (is_top or is_bot) else 1.0, zorder=2))
        ax.text(xc, yc + 0.08, str(val), ha='center', va='center', fontsize=10.2, fontweight='bold', color='#111111', zorder=5)
        if is_swap:
            alt_v = S880[755][i, j]
            ax.text(xc, yc - 0.24, f'#756: {alt_v}', ha='center', va='center', fontsize=5.9, fontweight='bold', color='#DC2626', zorder=5)
        else:
            ax.text(xc, yc - 0.24, lbl, ha='center', va='center', fontsize=6.0, fontweight='bold', color=tc, zorder=5)
# Draw the centred knight's-move upper square {13,14,15,16} and lower square {1,2,3,4}
top_km = np.array([[0.5, 1.5], [-1.5, 0.5], [-0.5, -1.5], [1.5, -0.5]])
bot_km = np.array([[-0.5, 1.5], [-1.5, -0.5], [0.5, -1.5], [1.5, 0.5]])
ax.add_patch(MplPolygon(top_km, closed=True, facecolor='none', edgecolor='#D97706', lw=2.0, ls='-', zorder=8))
ax.add_patch(MplPolygon(bot_km, closed=True, facecolor='none', edgecolor='#2563EB', lw=1.8, ls='--', zorder=8))

plt.tight_layout(pad=0.6)
plt.savefig(os.path.join(FIG_DIR, 'fig_hero_squares_gallery.pdf'), bbox_inches='tight', pad_inches=0.04)
plt.close()

# ==============================================================================
# FIGURE 2 (formerly Fig 1): 3D VECTORS FROM ORIGIN O OF VARIABLE LENGTH AND WEIGHT
# ==============================================================================
print("Generating Figure 2: fig_origin_vectors_3d.pdf ...")
fig = plt.figure(figsize=(14.2, 3.85))
S70 = S880[69]
P70 = scaled_points(S70).astype(float) / 2.0
R70 = np.linalg.norm(P70, axis=1, keepdims=True)
U70 = P70 / R70
B0_70 = U70.sum(axis=0)
w_star_70 = np.ones(16) - U70 @ np.linalg.solve(U70.T @ U70, B0_70)

ax1 = fig.add_subplot(1, 4, 1, projection='3d')
ax1.computed_zorder = False
ZF = -8.9
draw_floor_3d(ax1, ZF)
for k in range(16):
    p = P70[k]
    ax1.plot([p[0], p[0]], [p[1], p[1]], [p[2], ZF], color='#999999', lw=0.55, ls=(0, (1.5, 2)), zorder=1)
for k in np.argsort(-P70[:, 1]):
    p = P70[k]
    c = zcol_strong(p[2])
    ax1.plot([0, p[0]], [0, p[1]], [0, p[2]], color=c, lw=1.9, solid_capstyle='round', zorder=5)
    ax1.scatter([p[0]], [p[1]], [p[2]], s=26, color=c, edgecolor='k', linewidths=0.5, depthshade=False, zorder=6)
ax1.scatter([0], [0], [0], s=48, color='black', edgecolor='white', lw=0.8, depthshade=False, zorder=25)
ax1.text(-0.28, -0.2, -1.9, '$O$', fontsize=9.5, fontweight='bold', color='black', path_effects=HALO, zorder=30)
ax1.set_xlim(-2.1, 2.1); ax1.set_ylim(-2.1, 2.1); ax1.set_zlim(-9.3, 8.3)
ax1.set_box_aspect((1, 1, 1.12))
ax1.view_init(elev=24, azim=-48)
ax1.set_axis_off()
proj_ax1 = ax1.get_proj()
offset_pts_70 = {
    16: (0, 6), 15: (0, 6), 14: (-2, 6), 13: (-7, 4),
    12: (-8, 2), 11: (-6, 5), 10: (8, 3), 9: (8, 1),
    8: (-7, -5), 7: (10, -1), 6: (1, -8), 5: (9, -2),
    4: (-8, -6), 3: (9, -6), 2: (-9, 3), 1: (-5, -7)
}
for k in range(16):
    p = P70[k]
    val_k = int(S70.ravel()[k])
    c = zcol_strong(p[2])
    x2, y2, _ = proj3d.proj_transform(p[0], p[1], p[2], proj_ax1)
    ox, oy = offset_pts_70[val_k]
    ax1.annotate(str(val_k), xy=(x2, y2), xycoords='data',
                 xytext=(ox, oy), textcoords='offset points',
                 fontsize=6.8, fontweight='bold', ha='center', va='center',
                 color=c, path_effects=HALO, zorder=28)
ax1.set_title('(a) 3D radial spoke sculpture from $O$ ($\\beta=1$)\n' + r'$L_{ij}=R_{ij}$, $\sum \mathbf{p}_{ij} = \mathbf{0}$ (Square #70)', fontsize=8.8, pad=0)

ax2 = fig.add_subplot(1, 4, 2, projection='3d')
ax2.computed_zorder = False
draw_unit_sphere_wireframe(ax2, rad=1.0)
for k in np.argsort(-U70[:, 1]):
    u = U70[k]
    c = zcol_strong(P70[k, 2])
    ax2.plot([0, u[0]], [0, u[1]], [0, u[2]], color=c, lw=1.7, solid_capstyle='round', zorder=5)
    ax2.scatter([u[0]], [u[1]], [u[2]], s=24, color=c, edgecolor='k', linewidths=0.45, depthshade=False, zorder=6)
b_vis = B0_70 * 1.25
ax2.plot([0, b_vis[0]], [0, b_vis[1]], [0, b_vis[2]], color=WARN, lw=3.2, zorder=20)
ax2.scatter([b_vis[0]], [b_vis[1]], [b_vis[2]], s=55, marker='^', color=WARN, edgecolor='k', lw=0.6, depthshade=False, zorder=22)
ax2.scatter([0], [0], [0], s=42, color='black', edgecolor='white', lw=0.7, depthshade=False, zorder=24)
ax2.text(-0.24, -0.20, -0.18, '$O$', fontsize=9.0, fontweight='bold', path_effects=HALO, zorder=26)
ax2.set_xlim(-1.18, 1.18); ax2.set_ylim(-1.18, 1.18); ax2.set_zlim(-1.18, 1.18)
ax2.set_box_aspect((1, 1, 1))
ax2.view_init(elev=22, azim=-42)
ax2.set_axis_off()
x2_tip, y2_tip, _ = proj3d.proj_transform(b_vis[0], b_vis[1], b_vis[2], ax2.get_proj())
ax2.annotate(r'$\mathbf{V}_0 \neq \mathbf{0}$ ($0.773\,\mathbf{e}_y$)',
             xy=(x2_tip, y2_tip), xycoords='data',
             xytext=(0.76, 0.85), textcoords='axes fraction',
             ha='center', va='bottom', fontsize=7.3, fontweight='bold', color=WARN,
             arrowprops=dict(arrowstyle='->', lw=0.95, color=WARN, shrinkA=1, shrinkB=3),
             bbox=dict(boxstyle='round,pad=0.18', facecolor='white', alpha=0.95, edgecolor=WARN, lw=0.6), zorder=30)
ax2.set_title('(b) Unit vectors on $S^2$ ($\\beta=0, w_{ij}=1$)\n' + r'$L_{ij}=1 \Rightarrow \|\mathbf{V}_0\|=0.773$ (#70; $0$ on #175)', fontsize=8.8, pad=0)

ax3 = fig.add_subplot(1, 4, 3, projection='3d')
ax3.computed_zorder = False
draw_unit_sphere_wireframe(ax3, rad=1.0)
for k in np.argsort(-U70[:, 1]):
    u = U70[k]
    w_k = w_star_70[k]
    c = zcol_strong(P70[k, 2])
    tip_s = 54.0 * ((w_k / 0.70) ** 3.0)
    ec = GOLD if w_k > 1.02 else 'black'
    ew = 1.1 if w_k > 1.02 else 0.5
    ax3.plot([0, u[0]], [0, u[1]], [0, u[2]], color=c, lw=1.2 + 1.1 * (w_k - 0.7), solid_capstyle='round', zorder=5)
    ax3.scatter([u[0]], [u[1]], [u[2]], s=tip_s, color=c, edgecolor=ec, linewidths=ew, depthshade=False, zorder=7)
ax3.scatter([0], [0], [0], s=52, color=GREEN, edgecolor='black', lw=0.9, depthshade=False, zorder=25)
ax3.text(-0.24, -0.20, -0.18, '$O$', fontsize=9.0, fontweight='bold', color='#005A40', path_effects=HALO, zorder=28)
ax3.text2D(0.50, 0.02, r'Balanced: $\sum w_{ij}^*\hat{\mathbf{p}}_{ij}=\mathbf{0}$',
           transform=ax3.transAxes, fontsize=7.5, fontweight='bold', color='#005A40', ha='center', va='bottom',
           bbox=dict(boxstyle='round,pad=0.18', facecolor='white', alpha=0.94, edgecolor=GREEN, lw=0.6), zorder=30)
ax3.set_xlim(-1.18, 1.18); ax3.set_ylim(-1.18, 1.18); ax3.set_zlim(-1.18, 1.18)
ax3.set_box_aspect((1, 1, 1))
ax3.view_init(elev=22, azim=-42)
ax3.set_axis_off()
ax3.set_title('(c) Weighted unit vectors on $S^2$ ($w_{ij}^*>0$)\n' + r'$w_{ij}^*\in[0.72,1.19]$ restores $\mathbf{V}_{w^*,1}=\mathbf{0}$', fontsize=8.8, pad=0)

ax4 = fig.add_axes([0.765, 0.14, 0.22, 0.73])
betas = np.linspace(-1.2, 3.2, 240)
for idx_sq, lbl_sq, col_sq, ls_sq in [
    (69,  r'#70 ($\|\mathbf{V}_\beta\|$: zeros $1, 2.24$)', '#e41a1c', '-'),
    (44,  r'#45 ($\|\mathbf{V}_\beta\|$: zeros $0.96, 1$)', GREEN, '--'),
    (375, r'#376 ($\|\mathbf{V}_\beta\|$: zeros $-0.01, 1$)', BLUE, '-.'),
    (6,   r'#7 ($\|\mathbf{V}_\beta\|$: max at $\beta=0$)', '#984ea3', ':'),
    (174, r'Dürer #175 ($\equiv 0$ all $\beta$)', 'black', '-')
]:
    P_sq = scaled_points(S880[idx_sq]).astype(float) / 2.0
    R_sq = np.linalg.norm(P_sq, axis=1, keepdims=True)
    R_mean = float(np.mean(R_sq))
    norms = [float(np.linalg.norm((R_sq**(b - 1.0) * P_sq).sum(axis=0))) / (R_mean**(b - 1.0)) for b in betas]
    ax4.plot(betas, norms, color=col_sq, ls=ls_sq, lw=1.55, label=lbl_sq)

P_63 = scaled_points(S880[62]).astype(float) / 2.0
R_63 = np.linalg.norm(P_63, axis=1, keepdims=True)
Rm_63 = float(np.mean(R_63))
vz_63 = [5.0 * abs(float((R_63**(b - 1.0) * P_63[:, 2:3]).sum())) / (Rm_63**(b - 1.0)) for b in betas]
ax4.plot(betas, vz_63, color=GOLD, ls='--', lw=1.7, label=r'#63 $5|(\mathbf{V}_\beta)_z|/\bar{R}^{\beta-1}$ ($0$ at $\beta=1,3$)')

ax4.axvline(0.0, color='gray', lw=0.8, ls='--', alpha=0.65)
ax4.axvline(1.0, color='black', lw=0.9, ls=':', alpha=0.8)
ax4.axvline(3.0, color='#666666', lw=0.8, ls='--', alpha=0.55)
ax4.scatter([1.0, 2.2379, -0.0076], [0.0, 0.0, 0.0], color='#e41a1c', s=28, zorder=7)
ax4.scatter([3.0], [0.0], color=GOLD, edgecolor='black', lw=0.7, s=38, zorder=8)
ax4.annotate(r'Universal $\beta=1$', xy=(1.0, 0.04), xytext=(0.95, 1.52),
             arrowprops=dict(arrowstyle='->', lw=0.75), fontsize=6.6, bbox=PILL_BG, zorder=12)
ax4.annotate(r'$(\mathbf{V}_3)_z \equiv 0$' + '\n(all 880)', xy=(3.0, 0.0), xytext=(1.82, 1.18),
             arrowprops=dict(arrowstyle='->', lw=0.85, color='#8c5c00'), fontsize=6.6, fontweight='bold',
             color='#704800', bbox=PILL_BG, zorder=12)
ax4.set_xlabel(r'3D vector length exponent $\beta$ ($L_{ij} = R_{ij}^\beta$)')
ax4.set_ylabel(r'Normalized 3D resultant $\|\mathbf{V}_\beta\|_2 / \bar{R}^{\beta-1}$')
ax4.set_xlim(-1.2, 3.2); ax4.set_ylim(-0.12, 3.1)
ax4.set_title(r'(d) 3D power-law vector balance vs. $\beta$', fontsize=8.9)
ax4.legend(loc='upper left', framealpha=0.92, fontsize=6.0)
ax4.grid(True, alpha=0.25)

plt.savefig(os.path.join(FIG_DIR, 'fig_origin_vectors_3d.pdf'), bbox_inches='tight', pad_inches=0.04)
plt.close()

# ==============================================================================
# FIGURE 3 (formerly Fig 2): PLANAR RADIAL VECTORS, POLYGONS & PELL LAW
# ==============================================================================
print("Generating Figure 3: fig_ring_vectors.pdf ...")
fig, axes = plt.subplots(1, 4, figsize=(15.4, 3.95))

ax = axes[0]
x_grid = X4 / 2.0
y_grid = Y4 / 2.0
Z70_real = S70 - 8.5
theta = np.linspace(0, 2*np.pi, 200)
for rad, col, lbl in [(sqrt(2)/2, '#d95f02', r'$R_{\mathrm{in}}$ ($\frac{\sqrt{2}}{2}$)'),
                      (sqrt(10)/2, '#7570b3', r'$R_{\mathrm{mid}}$ ($\frac{\sqrt{10}}{2}$)'),
                      (3*sqrt(2)/2, '#1b9e77', r'$R_{\mathrm{out}}$ ($\frac{3\sqrt{2}}{2}$)')]:
    ax.plot(rad*np.cos(theta), rad*np.sin(theta), '--', color=col, lw=1.05, alpha=0.75, label=lbl)

vec_scale = 0.132
for i in range(4):
    for j in range(4):
        xv, yv = x_grid[i, j], y_grid[i, j]
        zv = Z70_real[i, j]
        wx, wy = zv * xv * vec_scale, zv * yv * vec_scale
        c_arr = zcol_strong(zv)
        ax.add_patch(FancyArrowPatch((0, 0), (wx, wy), arrowstyle='-|>', mutation_scale=8.0,
                                     lw=1.2, color=c_arr, alpha=0.78, shrinkA=0, shrinkB=0, zorder=3))
        r2 = R2_4[i, j]
        col_ring = '#d95f02' if r2 == 2 else ('#7570b3' if r2 == 10 else '#1b9e77')
        ax.scatter(xv, yv, color=col_ring, s=92, zorder=5, edgecolors='black', linewidth=0.6)
        ax.text(xv, yv, str(S70[i, j]), ha='center', va='center', fontsize=6.9, fontweight='bold', color='white', zorder=6)

ax.add_patch(FancyArrowPatch((0, 0.14), (3*vec_scale, 0.14), arrowstyle='-|>', mutation_scale=8.5, lw=2.1, color='#d95f02', zorder=8))
ax.add_patch(FancyArrowPatch((0, -0.14), (15*vec_scale, -0.14), arrowstyle='-|>', mutation_scale=9.5, lw=2.3, color='#1b9e77', zorder=8))
ax.add_patch(FancyArrowPatch((0, 0.0), (-18*vec_scale, 0.0), arrowstyle='-|>', mutation_scale=9.5, lw=2.3, color='#7570b3', zorder=8))
ax.text(0.46, 0.25, r'$\mathbf{d}_{\mathrm{in}}=(3,0)$', fontsize=6.1, color='#d95f02', fontweight='bold', ha='left', bbox=PILL_BG, zorder=10)
ax.text(1.02, -0.34, r'$\mathbf{d}_{\mathrm{out}}=(15,0)$', fontsize=6.2, color='#1b9e77', fontweight='bold', ha='center', bbox=PILL_BG, zorder=10)
ax.text(-1.02, -0.32, r'$\mathbf{d}_{\mathrm{mid}}=(-18,0)$', fontsize=6.2, color='#7570b3', fontweight='bold', ha='center', bbox=PILL_BG, zorder=10)
ax.scatter([0], [0], color='black', s=38, zorder=9)
ax.text(-0.22, 0.22, '$O$', fontsize=8.0, fontweight='bold', bbox=PILL_BG, zorder=10)

ax.axhline(0, color='#888888', lw=0.45, zorder=1)
ax.axvline(0, color='#888888', lw=0.45, zorder=1)
ax.set_xlim(-2.55, 2.55); ax.set_ylim(-2.95, 2.35)
ax.set_aspect('equal')
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_title('(a) 16 radial vectors from $O$ (#70)')
ax.legend(loc='lower center', framealpha=0.94, fontsize=6.3, ncol=3, handlelength=1.3, columnspacing=0.7)

ax = axes[1]
x_f = x_grid.ravel()
y_f = y_grid.ravel()
r_f = np.hypot(x_f, y_f)
u_x, u_y = x_f / r_f, y_f / r_f

z70_f = (S70 - 8.5).ravel()
W_lin = np.stack([z70_f * x_f, z70_f * y_f], axis=1)
ang = np.arctan2(W_lin[:, 1], W_lin[:, 0])
order = np.argsort(np.round(ang, 9), kind='stable')
V_lin = np.vstack([[0, 0], np.cumsum(W_lin[order], axis=0)])

S635 = S880[634]
z635_f = (S635 - 8.5).ravel()
W_u635 = np.stack([z635_f * u_x, z635_f * u_y], axis=1) * 1.35
ang635 = np.arctan2(W_u635[:, 1], W_u635[:, 0])
ord635 = np.argsort(np.round(ang635, 9), kind='stable')
V_u635 = np.vstack([[0, 0], np.cumsum(W_u635[ord635], axis=0)])

S45 = S880[44]
z45_f = (S45 - 8.5).ravel()
W_inv45 = np.stack([z45_f * (u_x / r_f), z45_f * (u_y / r_f)], axis=1) * 1.25
ang45 = np.arctan2(W_inv45[:, 1], W_inv45[:, 0])
ord45 = np.argsort(np.round(ang45, 9), kind='stable')
V_inv45 = np.vstack([[0, 0], np.cumsum(W_inv45[ord45], axis=0)])

for k in range(16):
    p0, p1 = V_lin[k], V_lin[k + 1]
    c = zcol_strong(z70_f[order[k]])
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=9.0, lw=1.6,
                                 color=c, shrinkA=0, shrinkB=0, zorder=4))
ax.plot([], [], color=VERM, lw=1.6, label=r'$\alpha=1$ (#70 closes on $O$)')
ax.plot(V_inv45[:, 0], V_inv45[:, 1], ls='-.', lw=1.25, color=GREEN, alpha=0.85, zorder=3,
        label=r'$\alpha^*=-1$ (#45 closes on $O$)')
ax.plot(V_u635[:, 0], V_u635[:, 1], ls='--', lw=1.15, color='#555555', alpha=0.78, zorder=2,
        label=r'$\alpha=0$ (#635 open gap $11.98$)')
ax.add_patch(FancyArrowPatch((0, 0), tuple(V_u635[-1]), arrowstyle='-|>', mutation_scale=10.5,
                             lw=2.4, color=WARN, shrinkA=0, shrinkB=0, zorder=8))
ax.text(V_u635[-1, 0] + 0.5, V_u635[-1, 1] + 2.2, r'$\mathbf{B}_{\mathrm{unit}}\neq\mathbf{0}$',
        fontsize=7.2, fontweight='bold', color=WARN, ha='left', bbox=PILL_BG, zorder=10)
ax.scatter(V_lin[:-1, 0], V_lin[:-1, 1], s=8, color='#333333', zorder=5)
ax.scatter([0], [0], s=42, color='black', zorder=9)
ax.annotate(r'$O$ (closed)', xy=(0, 0), xytext=(8, 6), textcoords='offset points',
            fontsize=7.1, fontweight='bold', color='black', path_effects=HALO, bbox=PILL_BG, zorder=12)
ax.set_xlim(min(V_lin[:, 0].min(), V_u635[:, 0].min(), V_inv45[:, 0].min()) - 3.5,
            max(V_lin[:, 0].max(), V_u635[:, 0].max(), V_inv45[:, 0].max()) + 4.0)
ax.set_ylim(min(V_lin[:, 1].min(), V_u635[:, 1].min(), V_inv45[:, 1].min()) - 8.5,
            max(V_lin[:, 1].max(), V_u635[:, 1].max(), V_inv45[:, 1].max()) + 5.5)
ax.set_aspect('equal')
ax.set_xlabel(r'Cumulative $\sum z_{ij}\ell(r_{ij})u_{ij,x}$')
ax.set_ylabel(r'Cumulative $\sum z_{ij}\ell(r_{ij})u_{ij,y}$')
ax.set_title(r'(b) Head-to-tail polygon ($\alpha=1, -1$ vs. $0$)')
ax.legend(loc='lower left', framealpha=0.92, fontsize=6.2)
ax.grid(True, alpha=0.22)

ax = axes[2]
u_norms, v_norms, b_norms, is_pell = [], [], [], []
for k in range(880):
    Z = 2 * S880[k] - 17
    din = np.array([int(np.sum(Z[mask_in] * X4[mask_in])) // 4, int(np.sum(Z[mask_in] * Y4[mask_in])) // 4], dtype=float)
    dout = np.array([int(np.sum(Z[mask_out] * X4[mask_out])) // 4, int(np.sum(Z[mask_out] * Y4[mask_out])) // 4], dtype=float)
    u = din + dout / 3.0
    v = din + dout
    u_norms.append(np.linalg.norm(u))
    v_norms.append(np.linalg.norm(v))
    b_norms.append(sqrt(2) * np.linalg.norm(u - v / sqrt(5)))
    is_pell.append((k + 1) in [70, 76, 121, 188, 452, 459, 490, 574])

u_norms = np.array(u_norms)
v_norms = np.array(v_norms)
b_norms = np.array(b_norms)
is_pell = np.array(is_pell)

sc = ax.scatter(u_norms[~is_pell], v_norms[~is_pell], c=b_norms[~is_pell], cmap='viridis', s=16, alpha=0.82, label='880 magic squares')
ax.scatter(u_norms[is_pell], v_norms[is_pell], color='#e41a1c', s=80, marker='*', zorder=6, edgecolors='black', lw=0.5, label='Pell min (#70, $v/u=9/4$)')
u_line = np.linspace(0, 21.5, 100)
ax.plot(u_line, sqrt(5)*u_line, 'r--', lw=1.25, label=r'Irrational line $\|\mathbf{v}\| = \sqrt{5}\,\|\mathbf{u}\|$')
ax.annotate('Pell min $(8,18)$:\n' + r'$\|\mathbf{v}\|/\|\mathbf{u}\|=9/4$',
            xy=(8.0, 18.0), xytext=(11.2, 3.8),
            arrowprops=dict(arrowstyle='->', lw=0.85, color='#e41a1c'),
            fontsize=6.8, fontweight='bold', color='#b30000',
            bbox=dict(boxstyle='round,pad=0.18', facecolor='white', alpha=0.95, edgecolor='#e41a1c', lw=0.5), zorder=10)
cb = plt.colorbar(sc, ax=ax, pad=0.02)
cb.set_label(r'$\|\mathbf{B}_{\mathrm{unit}}(S)\|$', fontsize=8)
ax.set_xlabel(r'$\|\mathbf{u}\| = \|\mathbf{d}_{\mathrm{in}} + \frac{1}{3}\mathbf{d}_{\mathrm{out}}\|$')
ax.set_ylabel(r'$\|\mathbf{v}\| = \|\mathbf{d}_{\mathrm{in}} + \mathbf{d}_{\mathrm{out}}\|$')
ax.set_title(r'(c) Diophantine Pell line $\|\mathbf{v}\| = \sqrt{5}\,\|\mathbf{u}\|$')
ax.legend(loc='upper left', framealpha=0.92, fontsize=6.6)
ax.grid(True, alpha=0.25)

ax = axes[3]
alphas = np.linspace(-1.25, 3.25, 300)
r1, r2, r3 = sqrt(2)/2, sqrt(10)/2, 3*sqrt(2)/2

for idx_sq, lbl_sq, col_sq, ls_sq in [
    (69,  r'#70 ($\kappa=+5$: zeros $\alpha=-0.05, 1$)', '#e41a1c', '-'),
    (44,  r'#45 ($\kappa=+9$: exact zeros $\alpha=-1, 1$)', '#1b9e77', '--'),
    (285, r'#286 ($\kappa=+1$: exact zeros $\alpha=1, 3$)', '#377eb8', '-.'),
    (45,  r'#46 ($\kappa=-9$: zero only at $\alpha=1$)', '#984ea3', ':')
]:
    Z = 2 * S880[idx_sq] - 17
    din = np.array([int(np.sum(Z[mask_in] * X4[mask_in])) // 4, int(np.sum(Z[mask_in] * Y4[mask_in])) // 4], dtype=float)
    dout = np.array([int(np.sum(Z[mask_out] * X4[mask_out])) // 4, int(np.sum(Z[mask_out] * Y4[mask_out])) // 4], dtype=float)
    vals = []
    for a in alphas:
        c1 = r1**(a - 1) - r2**(a - 1)
        c3 = r3**(a - 1) - r2**(a - 1)
        bvec = c1 * din + c3 * dout
        vals.append(np.linalg.norm(bvec))
    ax.plot(alphas, vals, color=col_sq, ls=ls_sq, lw=1.6, label=lbl_sq)

ax.axvline(1.0, color='black', lw=1.0, ls=':', alpha=0.8)
ax.axvline(0.0, color='gray', lw=0.85, ls='--', alpha=0.6)
ax.scatter([-1.0, -0.0496, 1.0, 3.0], [0.0, 0.0, 0.0, 0.0], color=['#1b9e77', '#e41a1c', 'black', '#377eb8'], s=30, zorder=7)
ax.annotate(r'$\alpha^*=-1$' + '\n(25 sqs)', xy=(-1.0, 0.3), xytext=(-0.92, 9.2),
            arrowprops=dict(arrowstyle='->', lw=0.75, color='#1b9e77'), fontsize=6.9, bbox=PILL_BG)
ax.annotate(r'$\alpha^*=+3$' + '\n(25 sqs)', xy=(3.0, 0.3), xytext=(1.15, 7.8),
            arrowprops=dict(arrowstyle='->', lw=0.75, color='#377eb8'), fontsize=6.9, bbox=PILL_BG)
ax.set_xlabel(r'Planar radial exponent $\alpha$ ($\ell(r) = r^\alpha$)')
ax.set_ylabel(r'Resultant norm $\|\mathbf{B}_{z, r^\alpha}(S)\|_2$')
ax.set_xlim(-1.25, 3.25); ax.set_ylim(-0.6, 26)
ax.set_title(r'(d) Planar power-law roots $\alpha^* \in \{-1, 1, 3\}$')
ax.legend(loc='upper center', framealpha=0.92, fontsize=6.5)
ax.grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig_ring_vectors.pdf'), bbox_inches='tight')
plt.close()

# ==============================================================================
# FIGURE 4 (formerly Fig 3): 4-PANEL 3D INERTIA ELLIPSOIDS, POINSOT & PRECESSION
# ==============================================================================
print("Generating Rebuilt Figure 4: fig_precession_dynamics.pdf (4 panels) ...")
fig = plt.figure(figsize=(15.4, 3.95))

# Panel (a): Universal Inertia Ratio I_perp(lambda)/I_zz + 3D Inertia Ellipsoid Insets
ax1 = fig.add_subplot(1, 4, 1)
lams = np.linspace(0, 1.05, 300)
for n_ord, col, ls in [(3, '#7570b3', '--'), (4, '#1b9e77', '-'), (5, '#d95f02', '-.')]:
    ratio = 0.5 * (1.0 + (n_ord**2 + 1) * lams**2)
    ax1.plot(lams, ratio, color=col, ls=ls, lw=1.7, label=f'$n={n_ord}$ ($b_n/a_n = {n_ord**2+1}$)')

ax1.axhline(1.0, color='black', lw=0.85, ls=':')
lam_cube = 0.20
lam_iso = 1.0 / sqrt(17)
ax1.scatter([lam_cube, lam_iso, 1.0], [21/25, 1.0, 9.0], color='#e41a1c', s=42, zorder=6)
BOX_OPAQUE = dict(boxstyle='round,pad=0.16', facecolor='white', alpha=0.96, edgecolor='#cccccc', lw=0.5)

th_el = np.linspace(0, 2*np.pi, 100)
ax1.annotate('$\\lambda_{\\mathrm{cube}}=1/5$: oblate\n($I_\\perp/I_{zz}=21/25$)',
             xy=(lam_cube, 0.84), xytext=(0.02, 4.1),
             arrowprops=dict(arrowstyle='->', lw=0.75, color='#e41a1c'), fontsize=6.4, bbox=BOX_OPAQUE, zorder=12)
ax1.annotate('Spherical top $\\lambda_{\\mathrm{iso}}=\\frac{1}{\\sqrt{17}}$\n(exact sphere $I_{xx}=I_{yy}=I_{zz}$)',
             xy=(lam_iso, 1.0), xytext=(0.27, 1.85),
             arrowprops=dict(arrowstyle='->', lw=0.75, color='#007A53'), fontsize=6.4, fontweight='bold',
             color='#005A3C', bbox=dict(boxstyle='round,pad=0.16', facecolor='#F0FDF4', edgecolor='#009E73', lw=0.7), zorder=12)
ax1.annotate('Canonical $\\lambda=1$: $I_\\perp/I_{zz}=9$\n(9:1 closed polhode cone)',
             xy=(1.0, 9.0), xytext=(0.40, 10.7),
             arrowprops=dict(arrowstyle='->', lw=0.75, color='#e41a1c'), fontsize=6.4, bbox=BOX_OPAQUE, zorder=12)

# Inset showing all 3 co-rotating 3D inertia ellipsoids on #46: lam=0.20 (oblate), lam_iso=1/sqrt(17) (exact sphere), lam=1.0 (prolate)
ax1_in = ax1.inset_axes([0.03, 0.53, 0.42, 0.39], projection='3d')
ax1_in.computed_zorder = False
u_sp = np.linspace(0, 2*np.pi, 24)
v_sp = np.linspace(0, np.pi, 13)
ax1_in.plot_surface(np.outer(np.cos(u_sp), np.sin(v_sp)),
                    np.outer(np.sin(u_sp), np.sin(v_sp)),
                    np.outer(np.ones_like(u_sp), np.cos(v_sp)),
                    color='#009E73', alpha=0.16, linewidth=0)
# Outer oblate-mass / prolate-inertia shell at lam=0.20 (dashed blue) and inner prolate-mass / oblate-inertia shell at lam=1 (dotted purple)
ax1_in.plot(np.cos(th_el), np.sin(th_el), np.zeros_like(th_el), color='#007A53', lw=0.95, ls='-')
ax1_in.plot(np.cos(th_el), np.zeros_like(th_el), np.sin(th_el), color='#007A53', lw=0.95, ls='-')
ax1_in.plot(1.09*np.cos(th_el), np.zeros_like(th_el), 0.72*np.sin(th_el), color='#2563EB', lw=0.8, ls='--')
ax1_in.plot(0.55*np.cos(th_el), np.zeros_like(th_el), 1.15*np.sin(th_el), color='#7C3AED', lw=0.8, ls=':')
P46_iso = scaled_points(S880[45]).astype(float) / 2.0
P46_iso[:, 2] *= lam_iso
P46_iso /= 2.35
h46_iso = ConvexHull(P46_iso)
for simp in h46_iso.simplices:
    ax1_in.add_collection3d(Poly3DCollection([P46_iso[simp]], facecolor='#D55E00', edgecolor='#7F1D1D', lw=0.25, alpha=0.48))
ax1_in.set_xlim(-1.12, 1.12); ax1_in.set_ylim(-1.12, 1.12); ax1_in.set_zlim(-1.12, 1.12)
ax1_in.set_box_aspect((1, 1, 1))
ax1_in.view_init(elev=20, azim=-40)
ax1_in.set_axis_off()
ax1_in.set_title(r'#46 Ellipsoids ($\lambda_{\mathrm{cube}}, \lambda_{\mathrm{iso}}, 1$)', fontsize=5.8, pad=-4, color='#005A3C', fontweight='bold')

ax1.set_xlabel(r'Vertical lift scale $\lambda$')
ax1.set_ylabel(r'Principal inertia ratio $I_\perp(\lambda)/I_{zz}$')
ax1.set_ylim(0, 14.2)
ax1.set_title('(a) Universal symmetric-top inertia law', fontsize=8.9)
ax1.legend(loc='lower right', framealpha=0.92, fontsize=6.3)
ax1.grid(True, alpha=0.25)

# Panel (b): 3D Triaxial Poinsot Ellipsoid (I1=110 < I2=230 < I3=340) & Unstable Flip Trajectory of #46
ax2 = fig.add_subplot(1, 4, 2, projection='3d')
ax2.computed_zorder = False
I1_p, I2_p, I3_p = 110.0, 230.0, 340.0
a1 = 1.12
a2 = a1 * sqrt(I1_p / I2_p)
a3 = a1 * sqrt(I1_p / I3_p)
u_p = np.linspace(0, 2*np.pi, 40)
v_p = np.linspace(0, np.pi, 22)
Xp = a1 * np.outer(np.cos(u_p), np.sin(v_p))
Yp = a2 * np.outer(np.sin(u_p), np.sin(v_p))
Zp = a3 * np.outer(np.ones_like(u_p), np.cos(v_p))
ax2.plot_surface(Xp, Yp, Zp, color='#DCE6EC', alpha=0.22, linewidth=0, shade=False, zorder=1)
th_p = np.linspace(0, 2*np.pi, 160)
ax2.plot(a1*np.cos(th_p), a2*np.sin(th_p), np.zeros_like(th_p), color='#64748B', lw=0.7, ls=':', zorder=2)
ax2.plot(a1*np.cos(th_p), np.zeros_like(th_p), a3*np.sin(th_p), color='#64748B', lw=0.7, ls=':', zorder=2)
ax2.plot(np.zeros_like(th_p), a2*np.cos(th_p), a3*np.sin(th_p), color='#64748B', lw=0.7, ls=':', zorder=2)

sep_ratio = sqrt((I3_p * (I3_p - I2_p)) / (I1_p * (I2_p - I1_p)))
z_sep_max = 1.0 / sqrt(1.0 + sep_ratio**2)
for sgn_branch in (-1.0, 1.0):
    z_norm = z_sep_max * np.sin(th_p)
    x_norm = sgn_branch * sep_ratio * z_norm
    y_norm = np.cos(th_p)
    ax2.plot(a1 * x_norm, a2 * y_norm, a3 * z_norm, color='#1E293B', lw=1.15, ls='--', alpha=0.82, zorder=6)

def euler_rhs(t, w, I1, I2, I3):
    return [
        ((I2 - I3) / I1) * w[1] * w[2],
        ((I3 - I1) / I2) * w[2] * w[0],
        ((I1 - I2) / I3) * w[0] * w[1]
    ]

t_span = (0, 54)
t_eval = np.linspace(0, 54, 1800)
sol_dzh = solve_ivp(euler_rhs, t_span, [0.02, 1.0, 0.02], args=(110.0, 230.0, 340.0), t_eval=t_eval, rtol=1e-9, atol=1e-11)
sol_mag = solve_ivp(euler_rhs, t_span, [0.25, 0.96, 0.25], args=(170.0, 170.0, 340.0), t_eval=t_eval, rtol=1e-9, atol=1e-11)

E2_dzh = I1_p*sol_dzh.y[0]**2 + I2_p*sol_dzh.y[1]**2 + I3_p*sol_dzh.y[2]**2
scale_poinsot = a2 / np.sqrt(E2_dzh / I2_p)
ax2.plot(sol_dzh.y[0]*scale_poinsot, sol_dzh.y[1]*scale_poinsot, sol_dzh.y[2]*scale_poinsot,
         color='#e41a1c', lw=2.0, zorder=10, label=r'Dzhanibekov flip orbit $\boldsymbol{\omega}(t)$')
ax2.scatter([0, 0], [a2, -a2], [0, 0], color='#e41a1c', edgecolor='black', s=46, lw=0.7, depthshade=False, zorder=15)
ax2.scatter([a1, -a1], [0, 0], [0, 0], color='#059669', edgecolor='black', s=36, lw=0.6, depthshade=False, zorder=14)
ax2.text(0.0, a2 + 0.14, 0.12, r'$+\mathbf{e}_2$ ($y=-x$)', fontsize=6.6, fontweight='bold', color='#b30000', ha='center', bbox=PILL_BG, zorder=20)
ax2.text(0.0, -a2 - 0.16, -0.15, r'$-\mathbf{e}_2$ ($180^\circ$ flip)', fontsize=6.6, fontweight='bold', color='#b30000', ha='center', bbox=PILL_BG, zorder=20)
ax2.text(a1 + 0.08, 0.0, 0.08, r'$\mathbf{e}_1$ ($I_1=110$)', fontsize=6.3, fontweight='bold', color='#065F46', ha='left', bbox=PILL_BG, zorder=20)
ax2.set_xlim(-1.18, 1.18); ax2.set_ylim(-0.95, 0.95); ax2.set_zlim(-0.78, 0.78)
ax2.set_box_aspect((1.15, 0.92, 0.76))
ax2.view_init(elev=22, azim=-36)
ax2.set_axis_off()
ax2.set_title('(b) 3D Poinsot ellipsoid & separatrix (#46)\n' + r'$I_1=110 < I_2=230 < I_3=340$ ($|Q_{xy}|=60$)', fontsize=8.8, pad=0)

# Panel (c): Time-series curves w2(t)
ax3 = fig.add_subplot(1, 4, 3)
ax3.plot(sol_dzh.t, sol_dzh.y[1], color='#e41a1c', lw=1.6, label=r'#46 ($|Q_{xy}|=60$): Dzhanibekov $\omega_2(t)$')
ax3.plot(sol_mag.t, sol_mag.y[1], color='#1b9e77', lw=1.45, ls='--', label=r'Dürer #175 ($Q_{xy}=0$): Harmonic $\omega_2(t)$')
ax3.plot(sol_mag.t, np.hypot(sol_mag.y[0], sol_mag.y[1]), color='#377eb8', lw=1.45, label=r'Axisymmetric rotor: Constant $|\boldsymbol{\omega}_\perp|$')
ax3.set_xlabel('Dimensionless time $t$')
ax3.set_ylabel('Body angular velocity component')
ax3.set_xlim(0, 54); ax3.set_ylim(-1.18, 1.58)
ax3.set_title('(c) Precession vs. $180^\\circ$ Dzhanibekov flips', fontsize=8.9)
ax3.legend(loc='upper right', framealpha=0.94, fontsize=6.1)
ax3.grid(True, alpha=0.25)

# Panel (d): Entry-weighted quadrupole census |Q_xy(S)| across 880 squares
ax4 = fig.add_subplot(1, 4, 4)
q_vals = [abs(int(np.sum((2 * S880[k] - 17) * X4 * Y4)) // 8) for k in range(880)]
q_counts = Counter(q_vals)
qs_sorted = sorted(q_counts.keys())
counts_sorted = [q_counts[q] for q in qs_sorted]

ax4.bar(qs_sorted, counts_sorted, width=1.1, color='#377eb8', edgecolor='black', lw=0.4, alpha=0.85, label='880 magic squares')
ax4.bar([0], [q_counts[0]], width=1.5, color='#1b9e77', edgecolor='black', lw=0.6, label='$Q_{xy}=0$ (56 axisymmetric)')
ax4.bar([60], [q_counts[60]], width=1.5, color='#e41a1c', edgecolor='black', lw=0.6, label='$|Q_{xy}|=60$ (max: #46, #71, #253, #286)')
ax4.set_xlabel(r'Quadrupole $|Q_{xy}(S)| = \frac{1}{2}(I_2 - I_1)$')
ax4.set_ylabel('Number of $D_4$-classes (out of 880)')
ax4.set_title(r'(d) Quadrupole inertia split $I_{1,2} = 170 \mp |Q_{xy}|$', fontsize=8.9)
ax4.legend(loc='upper right', framealpha=0.92, fontsize=6.3)
ax4.grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig_precession_dynamics.pdf'), bbox_inches='tight')
plt.close()

# ==============================================================================
# FIGURE 5 (formerly Fig 4): NESTED CONVEX LAYERS (#673 vs HOLLOW-CAVITY #54)
# ==============================================================================
print("Generating Rebuilt Figure 5: fig_nested_diamonds.pdf (#673 vs Hollow-Cavity #54 + Fulcrum Levers) ...")
fig = plt.figure(figsize=(14.2, 4.35))

def plot_nested_gem_with_lever(fig_obj, sub_idx, S, title_str, rho_str, c0_y_vis, c1_y_vis, is_cavity=False):
    ax3d = fig_obj.add_subplot(1, 3, sub_idx, projection='3d')
    ax3d.computed_zorder = False
    P = scaled_points(S).astype(float) / 2.0
    lam_disp = 0.25
    P_disp = P.copy()
    P_disp[:, 2] *= lam_disp

    h0 = ConvexHull(P_disp)
    for simp in h0.simplices:
        tri = P_disp[simp]
        poly = Poly3DCollection([tri], alpha=0.15, facecolor='#1b9e77', edgecolor='#0f5943', linewidths=0.45, zorder=2)
        ax3d.add_collection3d(poly)

    v0_set = set(exact_hull(S)['vertices'])
    inner_idx = [i for i in range(16) if i not in v0_set]
    Q_disp = P_disp[inner_idx]
    h1 = ConvexHull(Q_disp)
    core_fc = '#93C5FD' if is_cavity else '#e6ab02'
    core_ec = '#1D4ED8' if is_cavity else '#8c6800'
    for simp in h1.simplices:
        tri = Q_disp[simp]
        poly = Poly3DCollection([tri], alpha=0.40 if is_cavity else 0.46, facecolor=core_fc,
                                edgecolor=core_ec, linewidths=0.8, ls='--' if is_cavity else '-', zorder=4)
        ax3d.add_collection3d(poly)

    ax3d.scatter(P_disp[list(v0_set), 0], P_disp[list(v0_set), 1], P_disp[list(v0_set), 2],
                 color='#1b9e77', s=20, edgecolors='black', lw=0.4, depthshade=False, zorder=6)
    ax3d.scatter(Q_disp[:, 0], Q_disp[:, 1], Q_disp[:, 2],
                 color='#2563EB' if is_cavity else '#d95f02', s=28, edgecolors='black', lw=0.55, depthshade=False, zorder=8)

    ax3d.plot([0, 0], [-1.72, 1.72], [0, 0], 'k--', lw=1.15, alpha=0.78, zorder=15)
    ax3d.scatter([0], [0], [0], color='black', s=58, marker='+', lw=1.8, depthshade=False, zorder=25)
    ax3d.scatter([0], [c0_y_vis], [0], color='#007A53', edgecolor='white', lw=0.8, s=52, marker='o', depthshade=False, zorder=26)
    ax3d.scatter([0], [c1_y_vis], [0], color='#2563EB' if is_cavity else '#D55E00', edgecolor='white', lw=0.8, s=54, marker='D', depthshade=False, zorder=26)
    if is_cavity:
        ax3d.scatter([0], [-0.55], [0], color='#6B7280', edgecolor='white', lw=0.7, s=42, marker='s', depthshade=False, zorder=26)
        ax3d.text(0.0, -0.62, 0.28, r'$\overline{\mathbf{p}}_{\mathrm{out}}$ ($-y$)', fontsize=6.8, fontweight='bold', color='#374151', ha='center', va='bottom', bbox=PILL_BG, zorder=28)
        ax3d.text(0.0, c0_y_vis - 0.05, -0.58, r'$\mathbf{c}_0$ ($+y$!)', fontsize=7.1, fontweight='bold', color='#005A3C', ha='center', va='top', bbox=PILL_BG, zorder=28)
        ax3d.text(0.0, c1_y_vis + 0.18, 0.28, r'$\mathbf{c}_1$ ($+y$)', fontsize=7.1, fontweight='bold', color='#1E40AF', ha='center', va='bottom', bbox=PILL_BG, zorder=28)
    else:
        ax3d.text(0.0, 0.0, 0.28, '$O$', fontsize=7.4, fontweight='bold', color='black', ha='center', va='bottom', bbox=PILL_BG, zorder=28)
        ax3d.text(0.0, c0_y_vis - 0.14, 0.28, r'$\mathbf{c}_0$ ($-y$)', fontsize=7.2, fontweight='bold', color='#005A3C', ha='center', va='bottom', bbox=PILL_BG, zorder=28)
        ax3d.text(0.0, c1_y_vis + 0.14, 0.28, r'$\mathbf{c}_1$ ($+y$)', fontsize=7.2, fontweight='bold', color='#B34700', ha='center', va='bottom', bbox=PILL_BG, zorder=28)

    ax3d.set_xlim(-1.62, 1.62); ax3d.set_ylim(-1.62, 1.62); ax3d.set_zlim(-2.35, 1.85)
    ax3d.set_box_aspect((1, 1, 1.08))
    ax3d.view_init(elev=22, azim=-38)
    ax3d.set_axis_off()
    ax3d.set_title(title_str + '\n(' + rho_str + ')', fontsize=8.8, pad=0)

    # Bottom 2D fulcrum lever inset diagram on a crisp rounded card
    ax_lev = ax3d.inset_axes([0.03, 0.00, 0.94, 0.23])
    ax_lev.set_xlim(-1.35, 1.35); ax_lev.set_ylim(-0.56, 0.62)
    ax_lev.axis('off')
    ax_lev.add_patch(Rectangle((-1.32, -0.54), 2.64, 1.12, facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=0.7, zorder=0))
    ax_lev.plot([-1.12, 1.12], [0, 0], color='#1F2937', lw=2.0, zorder=2)
    ax_lev.add_patch(MplPolygon([[-0.10, -0.34], [0.10, -0.34], [0.0, 0.0]], closed=True, facecolor='#111111', edgecolor='black', zorder=3))
    ax_lev.text(0.0, -0.45, '$O$ ($y=0$)', ha='center', va='center', fontsize=6.4, fontweight='bold')
    if not is_cavity:
        ax_lev.add_patch(FancyArrowPatch((-0.68, 0.0), (-0.68, -0.40), arrowstyle='-|>', mutation_scale=8, lw=1.8, color='#007A53'))
        ax_lev.add_patch(FancyArrowPatch((0.68, 0.0), (0.68, -0.40), arrowstyle='-|>', mutation_scale=8, lw=1.8, color='#D55E00'))
        ax_lev.text(-0.68, 0.26, r'$V_0 c_{0,y}=-20/3$', ha='center', va='center', fontsize=6.3, fontweight='bold', color='#005A3C', bbox=PILL_BG)
        ax_lev.text(0.68, 0.26, r'$\frac{\Delta\rho_1}{\rho_0}V_1 c_{1,y}=+\frac{20}{3}$', ha='center', va='center', fontsize=6.3, fontweight='bold', color='#B34700', bbox=PILL_BG)
    else:
        ax_lev.add_patch(FancyArrowPatch((-0.78, 0.0), (-0.78, -0.34), arrowstyle='-|>', mutation_scale=7.5, lw=1.3, ls='--', color='#6B7280'))
        ax_lev.add_patch(FancyArrowPatch((0.26, 0.0), (0.26, -0.40), arrowstyle='-|>', mutation_scale=8, lw=1.8, color='#007A53'))
        ax_lev.add_patch(FancyArrowPatch((0.88, 0.0), (0.88, 0.44), arrowstyle='-|>', mutation_scale=8.5, lw=1.9, color='#2563EB'))
        ax_lev.text(-0.78, 0.26, r'$\overline{\mathbf{p}}_{\mathrm{out}}=-\frac{3}{10}$', ha='center', va='center', fontsize=6.0, color='#374151', bbox=PILL_BG)
        ax_lev.text(0.22, 0.26, r'$\mathbf{c}_0=+\frac{19}{324}$', ha='center', va='center', fontsize=6.0, fontweight='bold', color='#005A3C', bbox=PILL_BG)
        ax_lev.text(0.88, -0.25, r'Cavity $\Delta\rho_1<0$' + '\n' + r'(buoyancy at $\mathbf{c}_1$)', ha='center', va='center', fontsize=5.8, fontweight='bold', color='#1E40AF', bbox=PILL_BG)

plot_nested_gem_with_lever(
    fig, 1, S880[672],
    r'(a) Opposing Centroids: Gem #673 ($V_0=8, V_1=8$)',
    r'Denser core $\Delta\rho_1/\rho_0 = +5/4 = 1.25$',
    c0_y_vis=-0.45, c1_y_vis=0.52, is_cavity=False
)

plot_nested_gem_with_lever(
    fig, 2, S880[53],
    r'(b) Same-Side Paradox: Hollow-Cavity Gem #54 ($10,6$)',
    r'$\mathbf{c}_0,\mathbf{c}_1$ both on $+y \Rightarrow$ cavity $\Delta\rho_1/\rho_0 = -57/58$',
    c0_y_vis=0.22, c1_y_vis=0.68, is_cavity=True
)

ax3 = fig.add_subplot(1, 3, 3)
categories = [
    'All order-4\nmagic gems',
    'Non-empty\ninner $P_S^{(1)}$',
    'Cone-balanced\nby $P_S^{(1)}$ + natural',
    '3D inner core\ngem $\\mathcal{G}_1(S)$',
    'Naturally\nbalanced ($\\mathbf{c}_0=\\mathbf{0}$)',
    '2-density solid\nbalanced ($\\mathcal{G}_0,\\mathcal{G}_1$)',
    'Depth-3 onion\n($\\mathcal{G}_0\\supset\\mathcal{G}_1\\supset\\mathcal{G}_2$)'
]
counts = [880, 862, 528, 511, 51, 35, 20]
colors = ['#4d4d4d', '#377eb8', '#1b9e77', '#e6ab02', '#7570b3', '#d95f02', '#e7298a']
y_pos = np.arange(len(categories))
bars = ax3.barh(y_pos, counts, color=colors, edgecolor='black', lw=0.6, height=0.62)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(categories, fontsize=8)
ax3.invert_yaxis()
ax3.set_xlabel('Number of order-4 magic squares (out of 880)')
ax3.set_xlim(0, 1240)
for bar, c in zip(bars, counts):
    lbl_txt = '35 (4.0%: 33 denser + 2 cavity)' if c == 35 else f'{c} ({100*c/880:.1f}%)'
    ax3.text(c + 14, bar.get_y() + bar.get_height()/2, lbl_txt,
             va='center', ha='left', fontsize=7.5 if c == 35 else 8, fontweight='bold')
ax3.set_title('(c) Order-4 nested core & balance census', fontsize=9.0)
ax3.grid(True, axis='x', alpha=0.25)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig_nested_diamonds.pdf'), bbox_inches='tight')
plt.close()

# ==============================================================================
# FIGURE 6: BALL-AND-ROD WIREFRAMES, COMPLETE K_16 & PAPERCRAFT NET WITH a-k TABS
# ==============================================================================
print("Generating Rebuilt Figure 6: fig_wireframes_and_nets.pdf (with a-k gluing labels & root ★) ...")
fig = plt.figure(figsize=(15.4, 4.2))

def get_inner_edges_3d(Q_int):
    M = len(Q_int)
    hull = ConvexHull(Q_int.astype(float))
    planes = {}
    for s in hull.simplices:
        p0, p1, p2 = Q_int[s[0]], Q_int[s[1]], Q_int[s[2]]
        nrm = np.cross(p1 - p0, p2 - p0)
        a, b, c = int(nrm[0]), int(nrm[1]), int(nrm[2])
        g = gcd(gcd(abs(a), abs(b)), abs(c))
        a, b, c = a // g, b // g, c // g
        d = -(a * int(p0[0]) + b * int(p0[1]) + c * int(p0[2]))
        val = a * int(Q_int[:, 0].sum()) + b * int(Q_int[:, 1].sum()) + c * int(Q_int[:, 2].sum()) + d * M
        if val > 0:
            a, b, c, d = -a, -b, -c, -d
        planes[(a, b, c, d)] = True
    edges = set()
    Pi = [tuple(int(t) for t in p) for p in Q_int]
    for key in planes:
        a, b, c, d = key
        vals = a * Q_int[:, 0] + b * Q_int[:, 1] + c * Q_int[:, 2] + d
        pts = [int(k) for k in np.nonzero(vals == 0)[0]]
        drop = next(i for i in (2, 0, 1) if key[i] != 0)
        cyc = _hull2d([tuple(Pi[k][i] for i in range(3) if i != drop) + (k,) for k in pts])
        for i in range(len(cyc)):
            u, v = cyc[i], cyc[(i + 1) % len(cyc)]
            edges.add((min(u, v), max(u, v)))
    return sorted(edges)

ax1 = fig.add_subplot(1, 4, 1, projection='3d')
ax1.computed_zorder = False
S673 = S880[672]
h673 = exact_hull(S673)
P673_disp = h673['P'].astype(float) / 2.0
P673_disp[:, 2] *= 0.25
v0_673 = set(h673['vertices'])
inner_673 = [i for i in range(16) if i not in v0_673]
Q673_int = h673['P'][inner_673]
Q673_disp = P673_disp[inner_673]
edges1_673 = get_inner_edges_3d(Q673_int)

for u, v in h673['edges']:
    pu, pv = P673_disp[u], P673_disp[v]
    ax1.plot([pu[0], pv[0]], [pu[1], pv[1]], [pu[2], pv[2]],
             color='#0072B2', lw=2.1, solid_capstyle='round', alpha=0.88, zorder=4)
for u, v in edges1_673:
    qu, qv = Q673_disp[u], Q673_disp[v]
    ax1.plot([qu[0], qv[0]], [qu[1], qv[1]], [qu[2], qv[2]],
             color='#D55E00', lw=1.9, solid_capstyle='round', alpha=0.95, zorder=7)
P0_pts = P673_disp[list(v0_673)]
ax1.scatter(P0_pts[:, 0], P0_pts[:, 1], P0_pts[:, 2],
            color='#0072B2', s=38, edgecolors='white', lw=0.6, depthshade=False, zorder=6)
ax1.scatter(Q673_disp[:, 0], Q673_disp[:, 1], Q673_disp[:, 2],
            color='#E69F00', s=42, edgecolors='black', lw=0.6, depthshade=False, zorder=9)

ax1.plot([0, 0], [-1.72, 1.72], [0, 0], 'k--', lw=1.0, alpha=0.7, zorder=12)
ax1.scatter([0], [0], [0], color='black', s=52, marker='+', lw=1.7, depthshade=False, zorder=20)
ax1.scatter([0], [-0.42], [0], color='#0072B2', edgecolor='white', lw=0.8, s=48, marker='o', depthshade=False, zorder=22)
ax1.scatter([0], [0.58], [0], color='#D55E00', edgecolor='white', lw=0.8, s=50, marker='D', depthshade=False, zorder=22)
ax1.text(0.0, 0.0, 0.30, '$O$', fontsize=7.4, fontweight='bold', ha='center', va='bottom', bbox=PILL_BG, zorder=25)
ax1.text(0.0, -0.62, -0.46, r'$\mathbf{c}_{\mathrm{wire},0}$', fontsize=7.1, fontweight='bold', color='#005282', ha='center', va='top', bbox=PILL_BG, zorder=25)
ax1.text(0.0, 0.72, 0.28, r'$\mathbf{c}_{\mathrm{wire},1}$', fontsize=7.1, fontweight='bold', color='#A34400', ha='center', va='bottom', bbox=PILL_BG, zorder=25)
ax1.text2D(0.50, 0.01, r'Diam. ratio $d_1/d_0=0.793$ ($\lambda=1$) $\Rightarrow \mathbf{c}_{\mathrm{wire}}=\mathbf{0}$',
           transform=ax1.transAxes, fontsize=6.7, fontweight='bold', color='#004D40', ha='center', va='bottom',
           bbox=dict(boxstyle='round,pad=0.16', facecolor='white', alpha=0.94, edgecolor='#0072B2', lw=0.55), zorder=30)
ax1.set_xlim(-1.65, 1.65); ax1.set_ylim(-1.65, 1.65); ax1.set_zlim(-1.95, 1.95)
ax1.set_box_aspect((1, 1, 1.05))
ax1.view_init(elev=22, azim=-38)
ax1.set_axis_off()
ax1.set_title('(a) Nested ball-and-rod wireframe\n' + r'$G(\mathcal{G}_0)\cup G(\mathcal{G}_1)$ (Gem #673, $17+17$ rods)', fontsize=8.6, pad=0)

ax2 = fig.add_subplot(1, 4, 2, projection='3d')
ax2.computed_zorder = False
S175 = S880[174]
h175 = exact_hull(S175)
P175_disp = h175['P'].astype(float) / 2.0
P175_disp[:, 2] *= 0.25
hull_edges_175 = set(h175['edges'])

for u in range(16):
    for v in range(u + 1, 16):
        pu, pv = P175_disp[u], P175_disp[v]
        if (u, v) in hull_edges_175:
            ax2.plot([pu[0], pv[0]], [pu[1], pv[1]], [pu[2], pv[2]],
                     color='#009E73', lw=1.65, solid_capstyle='round', alpha=0.92, zorder=6)
        else:
            ax2.plot([pu[0], pv[0]], [pu[1], pv[1]], [pu[2], pv[2]],
                     color='#4B5D8E', lw=0.62, solid_capstyle='round', alpha=0.38, zorder=3)

for k in range(16):
    p = P175_disp[k]
    c_node = VERM if p[2] > 0 else BLUE
    ax2.scatter([p[0]], [p[1]], [p[2]], s=34, marker='s', color=c_node,
                edgecolor='black', linewidths=0.55, depthshade=False, zorder=10)

ax2.scatter([0], [0], [0], s=52, color='black', edgecolor='white', lw=0.8, depthshade=False, zorder=20)
ax2.text(0.0, 0.0, 0.28, r'$O=\mathbf{c}(K_{16})$', fontsize=7.2, fontweight='bold', color='black',
         ha='center', va='bottom', bbox=PILL_BG, zorder=25)
ax2.text2D(0.50, 0.01, r'Equal-mass: $\mathbf{c}=\mathbf{0}$, $\Sigma_{\mathrm{rods}}=\frac{29}{45}\Sigma(\lambda)$ (all 880)',
           transform=ax2.transAxes, fontsize=6.7, fontweight='bold', color='#1A2B5C', ha='center', va='bottom',
           bbox=dict(boxstyle='round,pad=0.16', facecolor='white', alpha=0.94, edgecolor='#4B5D8E', lw=0.55), zorder=30)
ax2.set_xlim(-1.65, 1.65); ax2.set_ylim(-1.65, 1.65); ax2.set_zlim(-1.95, 1.95)
ax2.set_box_aspect((1, 1, 1.05))
ax2.view_init(elev=22, azim=-42)
ax2.set_axis_off()
ax2.set_title('(b) Complete $K_{16}$ strut network (Dürer #175)\n' + r'$\binom{16}{2}=120$ rods ($24$ hull + $96$ internal)', fontsize=8.6, pad=0)

# Panel (c): Unfolded 2D Papercraft Cutout Net with Edge-Pair Gluing Letters (a-k) and Root Facet ★
ax3 = fig.add_subplot(1, 4, 3)
lam_net = 0.20
P175_net = h175['P'].astype(float) / 2.0
P175_net[:, 2] *= lam_net
s175_flat = S175.ravel()

facets_175 = []
for key, fv in h175['faces'].items():
    a, b, c, d = key
    n_vec = np.array([a * lam_net, b * lam_net, float(c)], dtype=float)
    n_hat = n_vec / np.linalg.norm(n_vec)
    tmp = np.array([1.0, 0.0, 0.0]) if abs(n_hat[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = np.cross(tmp, n_hat); e1 /= np.linalg.norm(e1)
    e2 = np.cross(n_hat, e1)
    pts_idx = list(fv)
    origin = P175_net[pts_idx[0]]
    uv = np.array([[np.dot(P175_net[idx] - origin, e1), np.dot(P175_net[idx] - origin, e2)] for idx in pts_idx])
    ctr = uv.mean(axis=0)
    order = np.argsort(np.arctan2(uv[:, 1] - ctr[1], uv[:, 0] - ctr[0]))
    cyc = [pts_idx[i] for i in order]
    uv_ord = uv[order]
    area = 0.5 * abs(sum(uv_ord[i, 0] * uv_ord[(i + 1) % len(cyc), 1] - uv_ord[(i + 1) % len(cyc), 0] * uv_ord[i, 1] for i in range(len(cyc))))
    facets_175.append({'key': key, 'cyc': cyc, 'uv_local': uv_ord, 'area': area})

facets_175.sort(key=lambda f: (-round(f['area'], 6), f['key']))
F175 = len(facets_175)
edge_to_facet_175 = {}
for fi, f in enumerate(facets_175):
    cyc = f['cyc']
    m = len(cyc)
    for i in range(m):
        edge_to_facet_175[(cyc[i], cyc[(i + 1) % m])] = (fi, i)

placed_175 = {0: facets_175[0]['uv_local'].copy()}
tree_edges_175 = set()
q_bfs = deque([0])
while q_bfs:
    fi = q_bfs.popleft()
    cyc = facets_175[fi]['cyc']
    uv_parent = placed_175[fi]
    m = len(cyc)
    for i in range(m):
        u, v = cyc[i], cyc[(i + 1) % m]
        nj, j_pos = edge_to_facet_175[(v, u)]
        if nj in placed_175:
            continue
        uv_nj = facets_175[nj]['uv_local']
        m_nj = len(uv_nj)
        p_v_local = uv_nj[j_pos]
        p_u_local = uv_nj[(j_pos + 1) % m_nj]
        target_u, target_v = uv_parent[i], uv_parent[(i + 1) % m]
        vec_local, vec_target = p_v_local - p_u_local, target_v - target_u
        L2 = float(np.dot(vec_local, vec_local))
        cos_t = float(np.dot(vec_local, vec_target)) / L2
        sin_t = float(vec_local[0] * vec_target[1] - vec_local[1] * vec_target[0]) / L2
        R_mat = np.array([[cos_t, -sin_t], [sin_t, cos_t]])
        placed_175[nj] = (uv_nj - p_u_local) @ R_mat.T + target_u
        tree_edges_175.add((min(u, v), max(u, v)))
        q_bfs.append(nj)

all_uv_pts = np.vstack([placed_175[fi] for fi in range(F175)])
uv_mean = all_uv_pts.mean(axis=0)
all_uv_centered = all_uv_pts - uv_mean
_, _, Vt_net = np.linalg.svd(all_uv_centered, full_matrices=False)
R_align = Vt_net
if np.linalg.det(R_align) < 0:
    R_align[1, :] *= -1
for fi in range(F175):
    placed_175[fi] = (placed_175[fi] - uv_mean) @ R_align.T

def make_tab_trapezoid(pa, pb, poly_own):
    ed = pb - pa
    L_e = float(np.linalg.norm(ed))
    t_hat = ed / L_e
    n_out = np.array([t_hat[1], -t_hat[0]])
    if np.dot(n_out, 0.5 * (pa + pb) - poly_own.mean(axis=0)) < 0:
        n_out = -n_out
    h_tab = min(0.24, 0.18 * L_e)
    bevel = min(0.22 * L_e, 1.15 * h_tab)
    return np.array([
        pa,
        pa + bevel * t_hat + h_tab * n_out,
        pb - bevel * t_hat + h_tab * n_out,
        pb
    ]), n_out

def poly_overlaps_2d(p1, p2, eps=1e-4):
    for poly in (p1, p2):
        m = len(poly)
        for i in range(m):
            edge = poly[(i + 1) % m] - poly[i]
            axis = np.array([-edge[1], edge[0]])
            norm = np.linalg.norm(axis)
            if norm < 1e-12:
                continue
            axis /= norm
            proj1, proj2 = p1 @ axis, p2 @ axis
            if proj1.max() <= proj2.min() + eps or proj2.max() <= proj1.min() + eps:
                return False
    return True

# Draw trapezoidal glue tabs and matching lowercase letters a..k on each of the 11 cut-edge pairs!
tab_drawn_for_edge = {}
all_face_centers = np.array([placed_175[fi].mean(axis=0) for fi in range(F175)])
letter_idx = 0
for fi in range(F175):
    cyc = facets_175[fi]['cyc']
    uv_f = placed_175[fi]
    m = len(cyc)
    for i in range(m):
        u, v = cyc[i], cyc[(i + 1) % m]
        ekey = (min(u, v), max(u, v))
        if ekey in tree_edges_175 or ekey in tab_drawn_for_edge:
            continue
        pa1, pb1 = uv_f[i], uv_f[(i + 1) % m]
        trap1, n_out1 = make_tab_trapezoid(pa1, pb1, uv_f)
        ov1 = sum(1 for fo in range(F175) if fo != fi and poly_overlaps_2d(trap1, placed_175[fo]))

        nj, j_pos = edge_to_facet_175[(v, u)]
        uv_nj = placed_175[nj]
        m_nj = len(uv_nj)
        pa2, pb2 = uv_nj[j_pos], uv_nj[(j_pos + 1) % m_nj]
        trap2, n_out2 = make_tab_trapezoid(pa2, pb2, uv_nj)
        ov2 = sum(1 for fo in range(F175) if fo != nj and poly_overlaps_2d(trap2, placed_175[fo]))

        if ov2 < ov1:
            use_second = True
        elif ov1 < ov2:
            use_second = False
        else:
            d1 = min(np.linalg.norm(trap1.mean(axis=0) - fc) for fc in all_face_centers)
            d2 = min(np.linalg.norm(trap2.mean(axis=0) - fc) for fc in all_face_centers)
            use_second = (d2 > d1)

        ch_lbl = chr(ord('a') + letter_idx)
        letter_idx += 1
        tab_drawn_for_edge[ekey] = ch_lbl
        if not use_second:
            trap, mate_pa, mate_pb, mate_n_out = trap1, pa2, pb2, n_out2
        else:
            trap, mate_pa, mate_pb, mate_n_out = trap2, pa1, pb1, n_out1

        ax3.add_patch(plt.Polygon(trap, facecolor='#D0D5DD', edgecolor='#555555', lw=0.65, zorder=2))
        tab_ctr = trap.mean(axis=0)
        ax3.text(tab_ctr[0], tab_ctr[1], ch_lbl, ha='center', va='center', fontsize=5.3,
                 fontweight='bold', color='#7F1D1D', path_effects=HALO, zorder=11)
        mate_mid = 0.5 * (mate_pa + mate_pb) + 0.14 * mate_n_out
        ax3.text(mate_mid[0], mate_mid[1], ch_lbl, ha='center', va='center', fontsize=5.3,
                 fontweight='bold', color='#1E3A8A', path_effects=HALO, zorder=11)

assert len(tab_drawn_for_edge) == 11

for fi in range(F175):
    cyc = facets_175[fi]['cyc']
    uv_f = placed_175[fi]
    m = len(cyc)
    fcol = '#FFF2CC' if m == 4 else '#D8EFE9'
    ax3.add_patch(plt.Polygon(uv_f, facecolor=fcol, edgecolor='none', alpha=0.92, zorder=3))
    if fi == 0:
        fc0 = uv_f.mean(axis=0)
        ax3.text(fc0[0], fc0[1], r'$\bigstar F_0$', ha='center', va='center', fontsize=6.2,
                 fontweight='bold', color='#B45309', path_effects=HALO, zorder=10)
    for i in range(m):
        u, v = cyc[i], cyc[(i + 1) % m]
        ekey = (min(u, v), max(u, v))
        pa, pb = uv_f[i], uv_f[(i + 1) % m]
        if ekey in tree_edges_175:
            ax3.plot([pa[0], pb[0]], [pa[1], pb[1]], color='#007A53', ls='--', lw=1.05, zorder=5)
        else:
            ax3.plot([pa[0], pb[0]], [pa[1], pb[1]], color='#111111', ls='-', lw=1.25, zorder=6)

uv_vert_clusters = []
for fi in range(F175):
    cyc = facets_175[fi]['cyc']
    uv_f = placed_175[fi]
    fc = uv_f.mean(axis=0)
    for i, v_idx in enumerate(cyc):
        pt = uv_f[i]
        val = int(s175_flat[v_idx])
        matched = False
        for cl in uv_vert_clusters:
            if np.linalg.norm(pt - cl['pts'][0]) < 0.22:
                cl['pts'].append(pt)
                cl['fcs'].append(fc)
                matched = True
                break
        if not matched:
            uv_vert_clusters.append({'pts': [pt], 'fcs': [fc], 'val': val})

for cl in uv_vert_clusters:
    mean_pt = np.mean(cl['pts'], axis=0)
    mean_fc = np.mean(cl['fcs'], axis=0)
    inward = mean_fc - mean_pt
    inward_norm = float(np.linalg.norm(inward))
    u_inw = inward / max(inward_norm, 1e-9)
    if len(cl['pts']) == 1:
        lbl_pt = mean_pt + min(0.46, 0.42 * inward_norm) * u_inw
    elif len(cl['pts']) == 2:
        lbl_pt = mean_pt + min(0.32, 0.34 * inward_norm) * u_inw
    else:
        lbl_pt = mean_pt + 0.02 * u_inw
    ax3.scatter([lbl_pt[0]], [lbl_pt[1]], s=42, color='white', edgecolor='#222222', lw=0.6, zorder=8)
    ax3.text(lbl_pt[0], lbl_pt[1], str(cl['val']), ha='center', va='center', fontsize=5.0, fontweight='bold', color='#111111', zorder=9)

ax3.plot([], [], color='#007A53', ls='--', lw=1.2, label=r'Mountain folds ($f_2-1=13$, $\bar{\theta}_{\mathrm{fold}}=141.2^\circ$)')
ax3.plot([], [], color='#111111', ls='-', lw=1.3, label=r'Cut perimeter ($2f_0-2=22$, pairs $\mathbf{a}$–$\mathbf{k}$)')
ax3.add_patch(Rectangle((0, 0), 0.01, 0.01, facecolor='#D0D5DD', edgecolor='#555555', lw=0.65, label=r'Glue tabs ($N_{\mathrm{tabs}}=f_0-1=11$, root $\bigstar F_0$)'))
ax3.set_aspect('equal')
ax3.autoscale_view()
xlim3, ylim3 = ax3.get_xlim(), ax3.get_ylim()
ax3.set_xlim(xlim3[0] - 0.38, xlim3[1] + 0.38)
ax3.set_ylim(ylim3[0] - 1.62, ylim3[1] + 0.35)
ax3.set_axis_off()
ax3.legend(loc='lower center', framealpha=0.96, fontsize=5.6, ncol=1, handlelength=1.4, borderpad=0.25, labelspacing=0.18)
ax3.set_title('(c) Buildable 2D papercraft net (pairs a–k)\n' + r'(Dürer #175, $\lambda=0.20$, $f=(12,24,14)$)', fontsize=8.6, pad=0)

ax4 = fig.add_subplot(1, 4, 4)
realizations = [
    'Equal-mass $K_{16}$\n/ point cloud',
    'Length-weighted\n$K_{16}$ (120 rods)',
    'Uniform solid\npolyhedron $\\mathcal{G}_0$',
    'Hollow papercraft\nshell $\\partial\\mathcal{G}_0$',
    'Outer hull\nwireframe $G(\\mathcal{G}_0)$'
]
mean_lam1 = [0.0000, 0.0717, 0.1087, 0.1357, 0.1940]
mean_lam02 = [0.0000, 0.0247, 0.0888, 0.0907, 0.0879]
tags_lam1 = ['880/880 (100%)', '48/880 (assoc.)', '51/880 (+3 VI)', '48 (+80 VI*)', '48 (+158 VI*)']
tags_lam02 = ['880/880 (100%)', '48/880 (assoc.)', '51/880 (+3 VI)', '48 (+87 VI*)', '48 (+164 VI*)']

y_pos = np.arange(len(realizations))
bar_h = 0.34
ax4.barh(y_pos - bar_h/2, mean_lam1, height=bar_h, color='#377eb8', edgecolor='black', lw=0.55, label=r'Canonical lift $\lambda=1.0$')
ax4.barh(y_pos + bar_h/2, mean_lam02, height=bar_h, color='#1b9e77', edgecolor='black', lw=0.55, label=r'Cubic print $\lambda=0.20$')

for i in range(len(realizations)):
    if i == 0:
        ax4.text(0.005, y_pos[i] + 0.06, r'$\|\mathbf{c}\|_2 \equiv 0$ (880/880 exact)', va='center', ha='left', fontsize=6.6, fontweight='bold', color='#005A3C')
    elif i in (1, 2):
        ax4.text(mean_lam1[i] + 0.004, y_pos[i] - bar_h/2, f'{mean_lam1[i]:.3f}', va='center', ha='left', fontsize=6.5, fontweight='bold', color='#1f4e78')
        ax4.text(mean_lam02[i] + 0.004, y_pos[i] + bar_h/2, f'{mean_lam02[i]:.3f} [{tags_lam02[i]}]', va='center', ha='left', fontsize=6.1, color='#0f5943')
    else:
        ax4.text(mean_lam1[i] + 0.004, y_pos[i] - bar_h/2, f'{mean_lam1[i]:.3f} [{tags_lam1[i]}]', va='center', ha='left', fontsize=6.1, fontweight='bold', color='#1f4e78')
        ax4.text(mean_lam02[i] + 0.004, y_pos[i] + bar_h/2, f'{mean_lam02[i]:.3f} [{tags_lam02[i]}]', va='center', ha='left', fontsize=6.1, color='#0f5943')

ax4.set_yticks(y_pos)
ax4.set_yticklabels(realizations, fontsize=7.5)
ax4.invert_yaxis()
ax4.set_xlabel(r'Mean centroid drift $\|\mathbf{c}(S)\|_2$ across $880$ squares')
ax4.set_xlim(0, 0.345)
ax4.set_title('(d) Centroid drift by physical realization\n(*Group VI restored via inner $\\mathcal{G}_1$)', fontsize=8.6)
ax4.legend(loc='upper right', framealpha=0.95, fontsize=6.4)
ax4.grid(True, axis='x', alpha=0.25)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig_wireframes_and_nets.pdf'), bbox_inches='tight')
plt.close()

# ==============================================================================
# FIGURE 7 (formerly Fig 5): MIRROR-TWIN STACKING (#763) + 2D SIDE ELEVATION
# ==============================================================================
print("Generating Rebuilt Figure 7: fig_mirror_stacking.pdf (4 panels with 2D side-elevation schematic) ...")
fig = plt.figure(figsize=(15.4, 4.15))

ax1 = fig.add_subplot(1, 4, 1, projection='3d')
S762 = S880[762]  # Square #763 (1-indexed)
lam = 0.20
P_base = scaled_points(S762).astype(float) / 2.0
P_base[:, 2] *= lam

for blk_idx in range(4):
    pts_blk = (P_base.copy() if blk_idx % 2 == 0 else -P_base.copy())
    pts_blk[:, 2] += blk_idx * 2.4
    ch = ConvexHull(pts_blk)
    fcol = '#1b9e77' if blk_idx % 2 == 0 else '#3b528b'
    ecol = '#0c4735' if blk_idx % 2 == 0 else '#1f2c4d'
    for simp in ch.simplices:
        tri = pts_blk[simp]
        poly = Poly3DCollection([tri], alpha=0.72, facecolor=fcol, edgecolor=ecol, linewidths=0.45)
        ax1.add_collection3d(poly)

s_flat = S762.ravel()
top4_idx = [i for i in range(16) if s_flat[i] in (13, 14, 15, 16)]
bot4_idx = [i for i in range(16) if s_flat[i] in (1, 2, 3, 4)]

def order_ccw(pts):
    ang = np.arctan2(pts[:, 1], pts[:, 0])
    return pts[np.argsort(ang)]

for j_idx, z_sh in enumerate([0.0, 2.4, 4.8]):
    if j_idx % 2 == 0:
        quad = order_ccw(P_base[top4_idx].copy())
        quad[:, 2] += z_sh
    else:
        quad = order_ccw((-P_base[bot4_idx]).copy())
        quad[:, 2] += z_sh
    poly_j = Poly3DCollection([quad], alpha=0.95, facecolor='#ffd92f', edgecolor='#b38f00', linewidths=1.5)
    ax1.add_collection3d(poly_j)

ax1.plot([0, 0], [0, 0], [-1.5, 8.7], 'r--', lw=1.3, zorder=20)
ax1.set_xlim(-1.9, 1.9); ax1.set_ylim(-1.9, 1.9); ax1.set_zlim(-1.6, 8.8)
ax1.set_xticks([-1, 0, 1]); ax1.set_yticks([-1, 0, 1]); ax1.set_zticks([0, 2, 4, 6, 8])
ax1.set_box_aspect((1, 1, 1.85))
ax1.view_init(elev=16, azim=-52)
ax1.set_xlabel('$x$', labelpad=-6); ax1.set_ylabel('$y$', labelpad=-6); ax1.set_zlabel('$z$', labelpad=1)
ax1.tick_params(pad=-2, labelsize=7.3)
ax1.set_title('(a) Alternating Mirror-Twin Tower\n(Square #763, $\\lambda=0.20$)', fontsize=8.8)

# Panel (b): Top-down (x,y) footprint of Square #763
ax2 = fig.add_subplot(1, 4, 2)
pts_xy = P_base[:, :2]
top_quad_xy = order_ccw(pts_xy[top4_idx])
bot_quad_xy = order_ccw(pts_xy[bot4_idx])

poly_top = plt.Polygon(top_quad_xy, facecolor='#ffd92f', alpha=0.45, edgecolor='#d95f02', lw=2.0, label=r'Upper $F_+$ $\{13..16\}$ ($A_{xy}=5$)')
poly_bot = plt.Polygon(bot_quad_xy, facecolor='none', edgecolor='#3b528b', lw=1.8, ls='--', label=r'Lower $F_-$ $\{1..4\}$ ($A_{xy}=5$)')
ax2.add_patch(poly_top)
ax2.add_patch(poly_bot)

theta_c = np.linspace(0, 2*np.pi, 200)
r_inscribed = sqrt(5) / 2.0
ax2.plot(r_inscribed*np.cos(theta_c), r_inscribed*np.sin(theta_c), ':', color='#1b9e77', lw=1.35, label=r'2D inradius $r=\sqrt{5}/2\approx 1.12$')
ax2.scatter([0], [0], color='red', marker='+', s=90, lw=2.0, zorder=10, label='Centroid $(0,0)$ ($d_{\\mathrm{stab}}=0.969$)')

for i in range(4):
    for j in range(4):
        val = S762[i, j]
        xv, yv = X4[i, j]/2.0, Y4[i, j]/2.0
        is_t = val in (13, 14, 15, 16)
        is_b = val in (1, 2, 3, 4)
        c_bg = '#d95f02' if is_t else ('#3b528b' if is_b else '#cccccc')
        c_fg = 'white' if (is_t or is_b) else 'black'
        ax2.scatter(xv, yv, color=c_bg, s=115, zorder=6, edgecolors='black', lw=0.7)
        ax2.text(xv, yv, str(val), ha='center', va='center', fontsize=7.6, fontweight='bold', color=c_fg, zorder=7)

ax2.set_xlim(-2.15, 2.15); ax2.set_ylim(-2.95, 2.05)
ax2.set_aspect('equal')
ax2.set_xlabel('$x$'); ax2.set_ylabel('$y$')
ax2.set_title("(b) Centred knight's-move facets ($A_{xy}=5$)", fontsize=8.8)
ax2.legend(loc='lower center', framealpha=0.94, fontsize=6.1, ncol=2)
ax2.grid(True, alpha=0.25)

# Panel (c): NEW 2D Side-Elevation Joint & Tipping Schematic (Same-Gem Mismatch vs. Mirror-Twin Locking)
ax3 = fig.add_subplot(1, 4, 3)
ax3.set_xlim(-2.65, 2.75)
ax3.set_ylim(-1.65, 4.35)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title('(c) Side-elevation joint & tipping mechanics\n' + r'(Same-gem mismatch vs. mirror-twin locking)', fontsize=8.8)

# Left sub-diagram (x centered at -1.35): Same-gem stacking S on S (22.6 deg wedge gap!)
xL = -1.38
w_b = 0.88
sl = 0.20  # tan(11.31 deg) = 0.20
# Block B0 (same gem): bottom slopes up-right (+sl), top slopes down-right (-sl)
b0_L = np.array([
    [xL - w_b, -1.2 - sl*w_b],
    [xL + w_b, -1.2 + sl*w_b],
    [xL + w_b,  1.2 - sl*w_b],
    [xL - w_b,  1.2 + sl*w_b]
])
ax3.add_patch(MplPolygon(b0_L, closed=True, facecolor='#D1FAE5', edgecolor='#059669', lw=1.3, zorder=3))
# Block B1 (unrotated copy of same gem S): its bottom slopes up-right (+sl), mismatching B0's top (-sl) by 2*11.31 = 22.62 deg!
gap_y = 0.36
b1_L = np.array([
    [xL - w_b, 1.2 + sl*w_b + (0.0)],
    [xL + w_b, 1.2 + sl*w_b + 2*sl*w_b + 0.12],
    [xL + w_b - 0.15, 3.35 - sl*w_b],
    [xL - w_b - 0.15, 3.35 + sl*w_b]
])
ax3.add_patch(MplPolygon(b1_L, closed=True, facecolor='#FEE2E2', edgecolor='#DC2626', lw=1.3, ls='--', zorder=3))
# Draw mismatched normal arrows n_+ and n_-
ax3.add_patch(FancyArrowPatch((xL + 0.05, 1.2), (xL + 0.25, 1.95), arrowstyle='-|>', mutation_scale=8, lw=1.6, color='#059669', zorder=8))
ax3.add_patch(FancyArrowPatch((xL - 0.05, 1.55), (xL + 0.22, 0.82), arrowstyle='-|>', mutation_scale=8, lw=1.6, color='#DC2626', zorder=8))
ax3.text(xL, 0.0, r'$\mathcal{G}_\lambda(S)$', ha='center', va='center', fontsize=7.2, fontweight='bold', color='#065F46')
ax3.text(xL - 0.05, 2.45, r'$\mathcal{G}_\lambda(S)$' + '\n(tilts/gaps!)', ha='center', va='center', fontsize=6.5, fontweight='bold', color='#991B1B')
ax3.text(xL, 3.82, 'Same-Gem Stack\n' + r'$\mathbf{n}_+\nparallel -\mathbf{n}_-$ ($22.6^\circ$ gap)', ha='center', va='center',
         fontsize=6.4, fontweight='bold', color='#991B1B', bbox=dict(boxstyle='round,pad=0.18', facecolor='#FEF2F2', edgecolor='#DC2626', lw=0.6))

# Divider line
ax3.plot([0.0, 0.0], [-1.5, 4.1], color='#CBD5E1', lw=1.0, ls=':', zorder=1)

# Right sub-diagram (x centered at +1.35): Alternating mirror-twin stack S and S*=-S on base plinth
xR = 1.38
# Base wedge plinth on flat table z = -1.45
plinth = np.array([
    [xR - w_b, -1.45],
    [xR + w_b, -1.45],
    [xR + w_b, -1.2 + sl*w_b],
    [xR - w_b, -1.2 - sl*w_b]
])
ax3.add_patch(MplPolygon(plinth, closed=True, facecolor='#E2E8F0', edgecolor='#475569', lw=1.1, zorder=2))
ax3.text(xR, -1.34, 'Plinth', ha='center', va='center', fontsize=5.8, fontweight='bold', color='#334155')

b0_R = np.array([
    [xR - w_b, -1.2 - sl*w_b],
    [xR + w_b, -1.2 + sl*w_b],
    [xR + w_b,  1.2 - sl*w_b],
    [xR - w_b,  1.2 + sl*w_b]
])
b1_R = np.array([
    [xR - w_b,  1.2 + sl*w_b],
    [xR + w_b,  1.2 - sl*w_b],
    [xR + w_b,  3.4 + sl*w_b],
    [xR - w_b,  3.4 - sl*w_b]
])
ax3.add_patch(MplPolygon(b0_R, closed=True, facecolor='#D1FAE5', edgecolor='#059669', lw=1.35, zorder=3))
ax3.add_patch(MplPolygon(b1_R, closed=True, facecolor='#DBEAFE', edgecolor='#1D4ED8', lw=1.35, zorder=3))
# Highlight the flush golden joint F_+ = -F_+ + 2c(F_+) at z = 1.2
ax3.plot([xR - w_b, xR + w_b], [1.2 + sl*w_b, 1.2 - sl*w_b], color='#EAB308', lw=3.0, zorder=6)
# Vertical z-axis alignment line x = xR
ax3.plot([xR, xR], [-1.45, 3.6], color='#DC2626', lw=1.2, ls='--', zorder=5)
# Tipping triangle from B0 centroid (xR, 0.0) to pivot corner (xR + w_b, -1.2 + sl*w_b)
ax3.plot([xR, xR + w_b], [0.0, -1.2 + sl*w_b], color='#B45309', lw=1.2, ls='-.', zorder=7)
ax3.scatter([xR, xR], [0.0, 2.3], color='#DC2626', s=24, zorder=8)
ax3.text(xR - 0.36, -0.05, r'$\mathbf{c}_0$', fontsize=6.6, fontweight='bold', color='#991B1B', bbox=PILL_BG, zorder=9)
ax3.text(xR + 0.42, -0.52, r'$\theta_{\mathrm{tip}}^{(1)}=39.4^\circ$', fontsize=6.0, fontweight='bold', color='#B45309', ha='center', bbox=PILL_BG, zorder=9)
ax3.text(xR, 1.28, r'$\theta_{\mathrm{joint}}=11.3^\circ$ ($\mu_s\geq 0.2$)', fontsize=6.0, fontweight='bold', color='#854D0E', ha='center', bbox=PILL_BG, zorder=10)
ax3.text(xR, 2.45, r'$\mathcal{G}_\lambda(S^*)=-\mathcal{G}_\lambda(S)$', ha='center', va='center', fontsize=6.5, fontweight='bold', color='#1E3A8A')
ax3.text(xR, 3.82, 'Mirror-Twin Lock\n' + r'$100\%$ Flush + Vertical $z$', ha='center', va='center',
         fontsize=6.4, fontweight='bold', color='#065F46', bbox=dict(boxstyle='round,pad=0.18', facecolor='#F0FDF4', edgecolor='#059669', lw=0.6))

# Panel (d): Distribution of critical tipping angles across all 14,824 facets
ax4 = fig.add_subplot(1, 4, 4)

def quick_solid_centroid(pts_int):
    h = ConvexHull(pts_int.astype(float))
    v0 = pts_int[0].astype(float) / 2.0
    vol = 0.0
    mom = np.zeros(3)
    for s in h.simplices:
        v1, v2, v3 = pts_int[s[0]]/2.0, pts_int[s[1]]/2.0, pts_int[s[2]]/2.0
        vt = abs(np.linalg.det([v1 - v0, v2 - v0, v3 - v0])) / 6.0
        vol += vt
        mom += vt * (v0 + v1 + v2 + v3) / 4.0
    return mom / vol

def facet_tip_deg(P_real_unscaled, face_v_indices, plane_abcd, com_unscaled, lam=1.0):
    P_lam = P_real_unscaled.copy()
    P_lam[:, 2] *= lam
    com_lam = np.array([com_unscaled[0], com_unscaled[1], com_unscaled[2] * lam])
    a, b, c, d = plane_abcd
    n_vec = np.array([a * lam, b * lam, float(c)], dtype=float)
    n_hat = n_vec / np.linalg.norm(n_vec)
    tmp = np.array([1.0, 0.0, 0.0]) if abs(n_hat[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = np.cross(tmp, n_hat); e1 /= np.linalg.norm(e1)
    e2 = np.cross(n_hat, e1)
    pts_f = P_lam[list(face_v_indices)]
    origin_f = pts_f[0]
    uv = np.array([[np.dot(p - origin_f, e1), np.dot(p - origin_f, e2)] for p in pts_f])
    ctr = uv.mean(axis=0)
    order = np.argsort(np.arctan2(uv[:, 1] - ctr[1], uv[:, 0] - ctr[0]))
    uv = uv[order]
    m = len(uv)
    h_com = -np.dot(com_lam - origin_f, n_hat)
    com_uv = np.array([np.dot(com_lam - origin_f, e1), np.dot(com_lam - origin_f, e2)])
    min_dist = min(
        ((uv[(i+1)%m, 0] - uv[i, 0])*(com_uv[1] - uv[i, 1]) - (uv[(i+1)%m, 1] - uv[i, 1])*(com_uv[0] - uv[i, 0]))
        / np.linalg.norm(uv[(i+1)%m] - uv[i])
        for i in range(m)
    )
    return degrees(atan2(min_dist, h_com)) if min_dist > 1e-9 else 0.0

tips_02, tips_10 = [], []
for k in range(880):
    h = exact_hull(S880[k])
    P_real = h['P'].astype(float) / 2.0
    c_sol = quick_solid_centroid(h['P'])
    for plane_key, fv in h['faces'].items():
        t02 = facet_tip_deg(P_real, fv, plane_key, c_sol, lam=0.20)
        t10 = facet_tip_deg(P_real, fv, plane_key, c_sol, lam=1.00)
        if t02 > 0:
            tips_02.append(t02)
        if t10 > 0:
            tips_10.append(t10)

ax4.hist(tips_02, bins=35, alpha=0.65, color='#1b9e77', edgecolor='black', lw=0.4, label=f'Cubic $\\lambda=0.20$ ({len(tips_02)} stable, 74.5%)')
ax4.hist(tips_10, bins=35, alpha=0.65, color='#7570b3', edgecolor='black', lw=0.4, label=f'Canonical $\\lambda=1.0$ ({len(tips_10)} stable, 43.0%)')
ax4.axvline(39.35, color='#e41a1c', lw=1.6, ls='--', label="#763 knight's-move ($39.35^\\circ$)")
ax4.set_xlabel(r'Critical tipping angle $\theta_{\mathrm{tip}}$ (degrees)')
ax4.set_ylabel('Number of stable facets (out of 14,824)')
ax4.set_title('(d) Resting gravitational stability census', fontsize=8.8)
ax4.legend(loc='upper right', framealpha=0.92, fontsize=6.4)
ax4.grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig_mirror_stacking.pdf'), bbox_inches='tight')
plt.close()

print("All 7 figures cleanly regenerated in", FIG_DIR)
