import Mathlib

/-- Step S3g: combining the three estimates.  If the circle average `I` of `log |P|`
is `≥ 0` (S3a) and `≤ log L − 2K/β` with `β = 2πe(n−1)/K` (S3e, S3f), then
`K² ≤ π e (n−1) log L`. -/
theorem S3g_combine (K n1 logL I : ℝ) (hK : 0 < K) (hn : 0 < n1)
    (hI0 : 0 ≤ I) (hI : I ≤ logL - 2 * K / (2 * Real.pi * Real.exp 1 * n1 / K)) :
    K ^ 2 ≤ Real.pi * Real.exp 1 * n1 * logL := by
  have hpe : 0 < Real.pi * Real.exp 1 * n1 := by positivity
  have h : 2 * K / (2 * Real.pi * Real.exp 1 * n1 / K) = K ^ 2 / (Real.pi * Real.exp 1 * n1) := by
    field_simp
  rw [h] at hI
  have : K ^ 2 / (Real.pi * Real.exp 1 * n1) ≤ logL := by linarith
  rwa [div_le_iff₀ hpe, mul_comm] at this
