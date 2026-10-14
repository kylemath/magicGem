import Mathlib

/-- **Step S3b.** For `γ : Fin n → ℤ` and `P_γ(z) = Σ_j γ_j z^j`, if `|z| ≤ 1`
(in particular on the unit circle) then `|P_γ(z)| ≤ Σ_j |γ_j| = ‖γ‖₁`. -/
theorem S3b_norm_le_l1 {n : ℕ} (γ : Fin n → ℤ) (z : ℂ) (hz : ‖z‖ ≤ 1) :
    ‖∑ j : Fin n, (γ j : ℂ) * z ^ (j : ℕ)‖ ≤ ∑ j : Fin n, (|γ j| : ℝ) := by
  refine (norm_sum_le _ _).trans (Finset.sum_le_sum fun j _ => ?_)
  rw [norm_mul, norm_pow]
  have h1 : ‖z‖ ^ (j : ℕ) ≤ 1 := pow_le_one₀ (norm_nonneg _) hz
  have h2 : ‖(γ j : ℂ)‖ = (|γ j| : ℝ) := by
    rw [Complex.norm_intCast]
  rw [h2]
  calc (|γ j| : ℝ) * ‖z‖ ^ (j : ℕ) ≤ (|γ j| : ℝ) * 1 :=
        mul_le_mul_of_nonneg_left h1 (by positivity)
    _ = _ := mul_one _
