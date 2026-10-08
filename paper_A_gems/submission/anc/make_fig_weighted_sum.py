"""Figure 3: the height-weighted vector sum  sum_ij z_ij (x_ij, y_ij) = (0,0)  for two magic squares (Duerer and square #45):
the 16 'moment arms' w_ij = z_ij (x_ij, y_ij), laid head to tail in order of direction, close up for both squares (weighted balance),
while the quadrant totals of z x y (right) add to 0 for Duerer and to 60 for #45 (mixed moment not forced)."""
from vecfig import *
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.5, foreground='white')]
S_LIST = [('Dürer', DURER), ('square #45', SQ[45])]
def pts(S):
    P = coords(S); return P[:, 0], P[:, 1], P[:, 2]
fig = plt.figure(figsize=(6.5, 3.35))
for col, (nm, S) in enumerate(S_LIST):
    assert (S.sum(0) == 34).all() and (S.sum(1) == 34).all() and np.trace(S) == 34 and np.trace(S[::-1]) == 34   # magic
    x, y, z = pts(S)
    W = np.stack([z * x, z * y], 1)                                   # moment arms w_ij = z_ij (x_ij, y_ij)
    assert abs(W.sum(0)).max() < 1e-12                                # sum z x = sum z y = 0
    ang = np.arctan2(W[:, 1], W[:, 0]); order = np.argsort(np.round(ang, 9), kind='stable')
    V = np.vstack([[0, 0], np.cumsum(W[order], 0)]); assert np.abs(V[-1]).max() < 1e-12     # head-to-tail chain closes
    quad = {(sx, sy): float((z * x * y)[(np.sign(x) == sx) & (np.sign(y) == sy)].sum()) for sx in (-1, 1) for sy in (-1, 1)}
    tot = sum(quad.values()); assert abs(tot - (z * x * y).sum()) < 1e-12
    print(nm, 'quadrants', quad, 'total', tot); assert tot == (0 if col == 0 else 60)
    ax = fig.add_axes([col * 0.5 + 0.0, 0.08, 0.34, 0.74]); ax.set_aspect('equal'); ax.axis('off')
    for k in range(16):
        p0, p1 = V[k], V[k + 1]; c = zcol_strong(z[order[k]])
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=11, lw=1.7, color=c, shrinkA=0, shrinkB=0, zorder=3))
    ax.scatter(V[:-1, 0], V[:-1, 1], s=7, color='#444444', zorder=4)
    ax.scatter([0], [0], s=38, color='k', zorder=6)
    ax.text(0.6, -0.8, '$O$', fontsize=10, ha='left', va='top', path_effects=HALO, zorder=7)
    ax.plot([-1, 1], [0, 0], lw=0)   # keep limits
    L = 14.5; ax.set_xlim(V[:, 0].min() - 2.5, V[:, 0].max() + 2.5); ax.set_ylim(V[:, 1].min() - 2.5, V[:, 1].max() + 2.5)
    fig.text(col * 0.5 + 0.015, 0.975, f'({"ab"[col]})  {nm}', fontsize=9.5, weight='bold', va='top')
    fig.text(col * 0.5 + 0.015, 0.915, r'$16$ arrows $z_{ij}(x_{ij},y_{ij})$ head to tail:' + '\n' + r'they close up, $\sum z\,(x,y)=(0,0)$', fontsize=7.8, va='top', color='#333333')
    # quadrant totals of z x y
    qa = fig.add_axes([col * 0.5 + 0.345, 0.30, 0.14, 0.28]); qa.set_xlim(0, 2); qa.set_ylim(0, 2); qa.axis('off'); qa.set_aspect('equal')
    qn = Normalize(-20, 20)
    for (sx, sy), v in quad.items():
        cx, cy = (sx + 1) / 2, (sy + 1) / 2
        c = CMAP(qn(v)); lum = np.mean(c[:3])
        qa.add_patch(Rectangle((cx, cy), 1, 1, facecolor=c, edgecolor='white', lw=1.5))
        qa.text(cx + .5, cy + .5, (f'{v:+.1f}' if v else '0'), ha='center', va='center', fontsize=7.5, weight='bold', color='white' if lum < 0.55 else '#222222')
    qa.text(1, 2.12, r'$\sum z\,xy$ by quadrant', ha='center', va='bottom', fontsize=7)
    fig.text(col * 0.5 + 0.415, 0.235, (r'total $=0$' if tot == 0 else rf'total $=+{tot:.0f}$'), ha='center', va='top', fontsize=9, weight='bold', color='k' if tot == 0 else WARN)
fig.text(0.5, 0.012, r'edge colour: orange $z>0$, blue $z<0$; arrows are sorted by direction, so each chain is a closed convex polygon', ha='center', fontsize=7.8, color='#333333')
fig.savefig(f'{FIGDIR}/fig_weighted_sum.pdf'); print('ok')
