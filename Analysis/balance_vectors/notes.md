# Part 1: what bubbleTrinityApp.js actually computes

Source: kylemath/magicSquare_physicalSolver/js/bubbleTrinityApp.js (1912 lines).

State: each number is a "bubble" with continuous planar position (p.x, p.y) in [0,n]^2 and a fixed
charge q = centeredHeight(value, n) = value - (n^2+1)/2 (this is exactly the paper's z_ij). Bubbles
are *not* given a unit-vector / mass structure; the 3D "shell" view uses z = charge*heightScale only for display and for
the occupancy fit score.

Discrete energy (`lineEnergy`): induced square = bubbles rounded to nearest free cells; row/col/diag
residuals rho_L = sum of centred values on L; `completeEnergy = sum_L rho_L^2` over 2n+2 lines
= N^2 * E_full(S) exactly (E_full = sum Cov(1_L,Z)^2 = sum rho^2 / N^2). `lowModeEnergy` = Cov(X,Z)^2+Cov(Y,Z)^2+diag terms
(= E_low) is only displayed. `maxResidual` is displayed. SA "settle" (batch mode) is a Metropolis swap
search on `completeEnergy` of the discrete square -> this part is exactly E_full descent.

Continuous force per bubble (integrateForcesOnce), residuals rho_L frozen from the *discrete induced square* in that tick:
1. field ("line-energy gradient strength"): fx += -q * rho_col * dx/(0.35+dx^2) summed over columns; same for rows with dy;
   diagonals linear in signed distance with 0.12 prefactor. This is -grad_position of the potential
   sum_L (q rho_L/2) ln(0.35+d_L^2): a smoothed, *linearised* model of dE/dq_i = 2 rho_L(i). It is a
   force on POSITIONS using E's gradient WITH RESPECT TO CHARGE (rho_L) as a coefficient; it is not
   grad_(x,y) of E_full (E_full does not depend on continuous positions at all). Sign: q*rho>0 is *attracted*
   toward its own line (-q rho dx), i.e. heuristic, not descent of E.
2. snap ("centrifugal balance"): fy += q * rho_row * dy * exp(-dy^2/0.6) * 0.012*snap*0.18 (cols analogous, diagonals via perpendicular
   distance, 0.12). Opposite sign to (1): q*rho>0 pushed OUT of the Gaussian-weighted line, q*rho<0 pulled IN.
   Intended effect: line sums go to zero. It is a charge-weighted, residual-weighted radial/perpendicular
   push -- "centrifugal" only by analogy; no rotation, no omega^2 r term, no explicit mass-weighted centroid.
3. well (spring to source cell), containment (isotropic spring toward centre + soft wall), repulsion (1/r^2 between
   bubbles), occupancy (nudges worst-fitting bubble in a crowded cell toward the best free cell; fit = q*(rho_row+rho_col)
   penalty, so again first-order dE/dq logic), temperature (jitter scaled by snap), damped velocity.

What "balance" is targeted: all 2n+2 line residuals -> 0, i.e. E_full -> 0. The app never computes
sum q*(x,y), sum m*u, or any centroid/torque/moment balance. Forces are not gradients of E_full;
they are heuristics built from the residuals rho_L (which are 1/2 the charge-gradient of E up to constants),
acting on positions, with the discrete rounding doing the real coupling. Only the SA settle is true E_full descent.

Note: the closest genuinely physical statement is the *linear* one proven below: E_full = 0 implies the charge-weighted
position moments vanish (centre of mass, and all separable moments). The app's "balance" is the stronger line-sum condition.

# Part 2: see results.txt, theorems.md and the PNGs.
