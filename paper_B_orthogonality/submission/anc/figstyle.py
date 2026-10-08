"""Common figure style: Okabe-Ito colour-blind-safe palette, Computer-Modern fonts, embedded Type 42 fonts."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

BLUE, VERM, GREEN, ORANGE, SKY, PINK, YELLOW = '#0072B2', '#D55E00', '#009E73', '#E69F00', '#56B4E9', '#CC79A7', '#F0E442'
GREY, DGREY, LGREY = '#8a8a8a', '#444444', '#e4e4e4'
DIV = LinearSegmentedColormap.from_list('bw_vermillion', [BLUE, '#ffffff', VERM])
TEXTWIDTH = 6.4   # inches (text block of the paper is 6.47in)

plt.rcParams.update({
    'font.family': 'cmr10', 'mathtext.fontset': 'cm', 'axes.formatter.use_mathtext': True, 'axes.unicode_minus': False,
    'font.size': 8.5, 'axes.labelsize': 8.5, 'axes.titlesize': 8.5, 'legend.fontsize': 7.5,
    'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'axes.linewidth': 0.6,
    'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
    'axes.spines.top': False, 'axes.spines.right': False, 'pdf.fonttype': 42, 'ps.fonttype': 42,
    'lines.linewidth': 1.0, 'figure.dpi': 150, 'savefig.dpi': 300, 'legend.frameon': False,
})


def panel_label(ax, text, x=-0.02, y=1.04):
    ax.text(x, y, r'$\mathbf{' + text + r'}$', transform=ax.transAxes, fontsize=9.5, va='bottom', ha='left')
