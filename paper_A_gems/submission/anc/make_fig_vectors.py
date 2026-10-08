"""Figure: the Magic Gem of Duerer's square as vectors from the centroid; one row's vertical components cancel."""
from gemfig import *
S = DURER; n = 4; N = 16
h = exact_hull(S); P = h['P'] / 2.0
fig = plt.figure(figsize=(6.5, 2.9))
ax = fig.add_axes([0.0, 0.0, 0.5, 1.0], projection='3d')
draw_faces(ax, h, P, alpha=0.05, lw=0.4)
row = [i * n + j for i in [0] for j in range(n)]
for k in range(N):
    if k in row: continue
    ax.plot([0, P[k, 0]], [0, P[k, 1]], [0, P[k, 2]], color='#888888', lw=0.5)
    ax.scatter(*P[k], s=6, color='#555555', depthshade=False)
for k in row:
    c = OI['verm'] if P[k, 2] > 0 else OI['blue']
    ax.plot([0, P[k, 0]], [0, P[k, 1]], [0, P[k, 2]], color=c, lw=1.8)
    ax.scatter(*P[k], s=16, color=c, depthshade=False)
    off = 0.8 if P[k, 2] > 0 else -1.0
    ax.text(P[k, 0], P[k, 1], P[k, 2] + off, f'{P[k,2]:+.1f}', fontsize=7, ha='center', color=c)
ax.scatter([0], [0], [0], s=14, color='k', depthshade=False); ax.text(-0.6, 0, 1.2, 'O', fontsize=8)
style3d(ax, elev=18, azim=-70)
ax.text2D(0.02, 0.93, '(a)', transform=ax.transAxes, fontsize=9, weight='bold')
# (b) cancellation of vertical components along the top row
ax2 = fig.add_axes([0.58, 0.20, 0.39, 0.66])
z = P[row, 2]; s = np.cumsum(z); start = np.concatenate([[0], s[:-1]])
for j in range(n):
    c = OI['verm'] if z[j] > 0 else OI['blue']
    ax2.bar(j, z[j], bottom=start[j], width=0.55, color=c, alpha=0.85, edgecolor='k', lw=0.4)
    ax2.text(j, start[j] + z[j] / 2, f'{S[0, j]}\n({z[j]:+.1f})', ha='center', va='center', fontsize=7, color='white', weight='bold')
    if j < n - 1: ax2.plot([j + 0.275, j + 0.725], [s[j]] * 2, color='k', lw=0.5, ls=':')
ax2.axhline(0, color='k', lw=0.8)
ax2.annotate('', xy=(3.45, 0), xytext=(3.45, s[2]), arrowprops=dict(arrowstyle='->', color='k', lw=0.8))
ax2.text(2.2, 4.0, 'running total\nreturns to $0$', fontsize=7, ha='center')
ax2.set_xticks(range(n)); ax2.set_xticklabels([f'$j={j}$' for j in range(n)])
ax2.set_ylabel(r'height $z_{0j}=s_{0j}-8.5$'); ax2.set_ylim(-9.5, 9.5); ax2.set_xlim(-0.6, 3.8)
for sp in ('top', 'right'): ax2.spines[sp].set_visible(False)
ax2.set_title('(b) heights along the top row', loc='left', fontsize=9, weight='bold')
ax2.text(1.5, -8.3, r'$\sum_j z_{0j}=7.5-5.5-6.5+4.5=0$', ha='center', fontsize=8)
fig.savefig(f'{FIGDIR}/fig_vectors_row.pdf')
print('ok')
