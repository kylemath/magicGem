import Mathlib

/-- **Step S4b.** For real `n ≥ 3`, `(n − 1)·log(n⁴/4) < 4 n log n`.
This gives the second inequality of Theorem 3.7(a). -/
theorem S4b_log_bound (n : ℝ) (hn : 3 ≤ n) :
    (n - 1) * Real.log (n ^ 4 / 4) < 4 * n * Real.log n := by
  have hnpos : 0 < n := by linarith
  have hlogn : 0 < Real.log n := Real.log_pos (by linarith)
  have hlog4 : 0 < Real.log 4 := Real.log_pos (by norm_num)
  rw [Real.log_div (by positivity) (by norm_num), Real.log_pow]
  push_cast
  nlinarith
