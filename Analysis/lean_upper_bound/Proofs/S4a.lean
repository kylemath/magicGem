import Mathlib

open Real

/-- **Step S4a (final combination in the proof of Theorem 3.7(a)).**
Let `K = k + 1`. If Lemma `jensen` gives `K² ≤ π e (n−1) log L` with `L = ‖γ‖₁ > 0`,
Lemma `col_feasible` gives `L ≤ n⁴/4`, and `K² > π e (n−1) log(n⁴/4)`, we get a contradiction
(so `γ = 0`). -/
theorem S4a_contradiction (n K L : ℝ) (hn : 1 ≤ n) (hL : 0 < L)
    (hjensen : K ^ 2 ≤ π * exp 1 * (n - 1) * log L)
    (hLbound : L ≤ n ^ 4 / 4)
    (hk : π * exp 1 * (n - 1) * log (n ^ 4 / 4) < K ^ 2) : False := by
  have hlog : log L ≤ log (n ^ 4 / 4) := log_le_log hL hLbound
  have hc : 0 ≤ π * exp 1 * (n - 1) := by
    have := pi_pos; have := exp_pos 1
    have : 0 ≤ n - 1 := by linarith
    positivity
  have := mul_le_mul_of_nonneg_left hlog hc
  linarith
