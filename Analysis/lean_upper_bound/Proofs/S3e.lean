import Mathlib

open Complex

/-- **Step S3e.** For real `θ`, `|exp(2πiθ) − 1| ≤ 2π|θ|` (chord ≤ arc). -/
theorem S3e_norm_exp_sub_one_le (θ : ℝ) :
    ‖exp (2 * Real.pi * θ * I) - 1‖ ≤ 2 * Real.pi * |θ| := by
  have h := Real.norm_exp_I_mul_ofReal_sub_one_le (x := 2 * Real.pi * θ)
  have e : (2 * (Real.pi : ℂ) * θ * I) = I * ((2 * Real.pi * θ : ℝ) : ℂ) := by
    push_cast; ring
  rw [e]
  refine h.trans (le_of_eq ?_)
  rw [Real.norm_eq_abs, abs_mul, abs_mul, abs_of_pos Real.pi_pos]
  norm_num
