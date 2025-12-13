### note.md

I woke up with the cleanest picture of what is *really* happening.

Treat the square as a function \(f(i,j)=z_{ij}\) on a discrete grid. All these “covariances” are just inner products \(\langle f,\phi\rangle\) with a few chosen test functions \(\phi\): namely \(x\), \(y\), and the two diagonal indicators.

So the paper’s energy
\[
E(S)=\langle f,x\rangle^2+\langle f,y\rangle^2+\langle f,\mathbf{1}_{\mathrm{main}}\rangle^2+\langle f,\mathbf{1}_{\mathrm{anti}}\rangle^2
\]
only checks that \(f\) is orthogonal to a *4-dimensional* subspace. Of course there is a huge nullspace for \(n\ge 4\): the row/column constraints live in an \((2n-2)\)-dimensional family, and “orthogonal to the first moment” is much weaker than “all row sums equal”.

The fix is almost embarrassingly simple and stays true to the authors’ language:

- Either test against **all row and column indicators** (or any full basis spanning them), plus the diagonals; or
- Test against a **complete orthogonal polynomial/Fourier basis** on \(\{0,\dots,n-1\}\), where the current \(x\) and \(y\) are just the *first* mode.

Then the “energy characterization” becomes a genuine theorem for all \(n\), and the current 4-term energy becomes a meaningful **low-mode relaxation** (also potentially interesting in its own right).

This also reframes the Magic Gem geometry nicely: you’re not discovering “mystical covariance”, you’re doing discrete harmonic analysis on a height function.
