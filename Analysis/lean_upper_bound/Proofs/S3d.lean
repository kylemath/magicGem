import Mathlib

/-- **Step S3d.** For `1 ≤ K`, `C(m, K) ≤ (e·m/K)^K` (applied with `m = n − 1`).
Proof: `C(m,K) ≤ m^K / K!` and `K^K / K! ≤ e^K`. -/
theorem S3d_choose_le (m K : ℕ) (hK : 1 ≤ K) :
    (m.choose K : ℝ) ≤ (Real.exp 1 * m / K) ^ K := by
  have hKpos : (0 : ℝ) < K := by exact_mod_cast hK
  have h1 : (m.choose K : ℝ) ≤ (m : ℝ) ^ K / K.factorial := Nat.choose_le_pow_div K m
  have h2 : (K : ℝ) ^ K / K.factorial ≤ Real.exp K :=
    Real.pow_div_factorial_le_exp (K : ℝ) hKpos.le K
  have hf : (0 : ℝ) < K.factorial := by exact_mod_cast K.factorial_pos
  have hKK : (0 : ℝ) < (K : ℝ) ^ K := by positivity
  -- K! ≥ K^K / e^K
  have h3 : (K : ℝ) ^ K ≤ Real.exp K * K.factorial := by
    rwa [div_le_iff₀ hf] at h2
  have hexp : Real.exp (K : ℝ) = Real.exp 1 ^ K := by
    rw [← Real.exp_nat_mul]; ring_nf
  calc (m.choose K : ℝ) ≤ (m : ℝ) ^ K / K.factorial := h1
    _ ≤ (m : ℝ) ^ K / ((K : ℝ) ^ K / Real.exp 1 ^ K) := by
        apply div_le_div_of_nonneg_left (by positivity) (by positivity)
        rw [div_le_iff₀ (by positivity)]; rw [← hexp]; linarith
    _ = (Real.exp 1 * m / K) ^ K := by
        rw [div_pow, mul_pow]; field_simp
