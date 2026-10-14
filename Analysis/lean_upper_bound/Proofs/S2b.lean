import Mathlib

/-- **Step S2b (AM–GM).** For reals `a` and `N`, `a (N - a) ≤ N² / 4`.
With `a = p n` this gives `p n (N - p n) ≤ N²/4`, used for `‖γ‖₁ ≤ N²/4`. -/
theorem S2b_amgm (a N : ℝ) : a * (N - a) ≤ N ^ 2 / 4 := by
  nlinarith [sq_nonneg (N - 2 * a)]
