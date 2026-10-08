"""Vectorized energies for batches of arrangements, shape (B, n, n), values 1..N.

Returns float64 arrays of shape (B,).  Definitions as in theory.py docstring.
"""
import numpy as np


def line_sums_z(arr):
    """Centered line sums: rows (B,n), cols (B,n), main diag (B,), anti diag (B,)."""
    B, n, _ = arr.shape
    N = n * n
    z = arr.astype(np.float64) - (N + 1) / 2.0
    rows = z.sum(axis=2)
    cols = z.sum(axis=1)
    idx = np.arange(n)
    dm = z[:, idx, idx].sum(axis=1)
    da = z[:, idx, n - 1 - idx].sum(axis=1)
    return z, rows, cols, dm, da


def all_energies(arr):
    """dict with E_low, E_full (symmetric), E_v4, E_asym for a batch."""
    B, n, _ = arr.shape
    N = n * n
    z, rows, cols, dm, da = line_sums_z(arr)
    x = np.arange(n) - (n - 1) / 2.0            # column coordinate
    y = (n - 1) / 2.0 - np.arange(n)            # row coordinate
    cov_x = (cols * x).sum(axis=1) / N           # Cov(X,Z) = (1/N) sum_j x_j colsum_j
    cov_y = (rows * y).sum(axis=1) / N
    cov_dm = dm / N
    cov_da = da / N
    e_xy = cov_x ** 2 + cov_y ** 2
    e_diag = cov_dm ** 2 + cov_da ** 2
    e_low = e_xy + e_diag
    e_full = ((rows ** 2).sum(axis=1) + (cols ** 2).sum(axis=1)) / N ** 2 + e_diag
    e_asym = ((rows[:, :-1] ** 2).sum(axis=1) + (cols[:, :-1] ** 2).sum(axis=1)) / N ** 2 + e_diag
    e_v4 = e_xy + N * e_diag        # (mean diag - mu)^2 = (dm/n)^2 = n^2 (dm/N)^2
    return {'E_low': e_low, 'E_full': e_full, 'E_v4': e_v4, 'E_asym': e_asym,
            'cov_x': cov_x, 'cov_y': cov_y, 'cov_dm': cov_dm, 'cov_da': cov_da}


def random_arrangements(n, B, rng):
    """B uniform random permutations of 1..N as (B,n,n) int arrays."""
    N = n * n
    keys = rng.random((B, N))
    perm = np.argsort(keys, axis=1, kind='quicksort') + 1
    return perm.reshape(B, n, n)
