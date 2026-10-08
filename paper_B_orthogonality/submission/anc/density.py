"""Density and CDF of a weighted sum of independent chi^2 variables  sum_j w_j chi^2_{m_j}
(the Gaussian-limit law of the energies), by characteristic-function inversion (Imhof 1961
style, numerically integrated)."""
import numpy as np
from scipy.integrate import quad


def _phi(t, weights):
    val = 1.0 + 0j
    for w, m in weights:
        val *= (1 - 2j * w * t) ** (-m / 2.0)
    return val


def mixture_pdf(x, weights):
    """f(x) = (1/pi) int_0^inf Re[phi(t) e^{-itx}] dt, evaluated pointwise."""
    weights = [(float(w), int(m)) for w, m in weights]
    x = np.atleast_1d(np.asarray(x, dtype=float))
    out = np.empty_like(x)
    for i, xi in enumerate(x):
        f = lambda t: (_phi(t, weights) * np.exp(-1j * t * xi)).real
        val, _ = quad(f, 0, np.inf, limit=4000)
        out[i] = val / np.pi
    return out


def mixture_cdf(x, weights):
    """Imhof's formula: F(x) = 1/2 - (1/pi) int_0^inf sin(theta(u)) / (u rho(u)) du."""
    weights = [(float(w), int(m)) for w, m in weights]
    x = np.atleast_1d(np.asarray(x, dtype=float))
    out = np.empty_like(x)
    for i, xi in enumerate(x):
        def g(u):
            theta = 0.5 * sum(m * np.arctan(2 * w * u) for w, m in weights) - 0.5 * xi * u
            rho = np.prod([(1 + 4 * w * w * u * u) ** (m / 4.0) for w, m in weights])
            return np.sin(theta) / (u * rho)
        val, _ = quad(g, 0, np.inf, limit=4000)
        out[i] = 0.5 - val / np.pi
    return out


def two_exponential_pdf(x, a, b):
    """Closed form for a*chi^2_2 + b*chi^2_2 (a != b): (e^{-x/2a} - e^{-x/2b}) / (2a - 2b)."""
    x = np.asarray(x, dtype=float)
    return (np.exp(-x / (2 * a)) - np.exp(-x / (2 * b))) / (2 * a - 2 * b)


if __name__ == '__main__':
    from theory import weights_closed
    for n in (3, 5):
        w = weights_closed(n, 'low')
        a, b = float(w[0][0]), float(w[1][0])
        xs = np.linspace(0.1, 6 * float(sum(ww * m for ww, m in w)), 7)
        print(n, np.max(np.abs(mixture_pdf(xs, w) - two_exponential_pdf(xs, a, b))))
    w = weights_closed(8, 'full')
    xs = np.linspace(0.5, 30, 5)
    print('n=8 full pdf', mixture_pdf(xs, w), 'cdf', mixture_cdf(xs, w))
