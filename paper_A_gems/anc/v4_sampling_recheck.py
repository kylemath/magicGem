"""Re-run of the order-4 sampling reported in Table 3 of arXiv:2512.09170v4.

v4 reported that 6*10^7 uniformly random arrangements of order 4 contained no
zero of the four-term (low-mode) energy E_low other than magic squares.
E_low = 0 exactly when the first moments sum_ij z_ij x_j and sum_ij z_ij y_i
vanish and both diagonals sum to 34; this script tests those four conditions in
integer arithmetic for the same number of samples and counts the zeros found.
Since 14,639,440 of the 16! arrangements are zeros (companion paper), about 42
are expected.  Usage: python3 v4_sampling_recheck.py [samples] [seed]
"""
import sys
import numpy as np

n, N = 4, 16
samples = int(float(sys.argv[1])) if len(sys.argv) > 1 else 60_000_000
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261014
rng = np.random.default_rng(seed)

idx = np.arange(N)
xw = 2 * (idx % n) - (n - 1)            # 2*x_j for cell index i*n+j
yw = (n - 1) - 2 * (idx // n)           # 2*y_i
dm = (idx // n) == (idx % n)            # main diagonal
da = (idx // n) + (idx % n) == n - 1    # anti-diagonal
M = n * (N + 1) // 2

zeros = magic = done = 0
chunk = 1_000_000
examples = []
while done < samples:
    m = min(chunk, samples - done)
    S = rng.permuted(np.tile(np.arange(1, N + 1, dtype=np.int16), (m, 1)), axis=1).astype(np.int32)
    ok = (S @ xw == 0) & (S @ yw == 0) & (S[:, dm].sum(1) == M) & (S[:, da].sum(1) == M)
    hits = S[ok]
    for s in hits:
        A = s.reshape(n, n)
        if (A.sum(0) == M).all() and (A.sum(1) == M).all():
            magic += 1
        if len(examples) < 3:
            examples.append(A.tolist())
    zeros += len(hits)
    done += m

expected = samples * 14_639_440 / 20_922_789_888_000
print(f"samples {samples}, seed {seed}: zeros of E_low found {zeros} "
      f"(of them magic {magic}); expected {expected:.1f}")
for A in examples:
    print(A)
