import Mathlib

open Real MeasureTheory intervalIntegral Set Interval

/-- **Step S3f.** For `β ≥ 2`, `∫_{-1/2}^{1/2} log(min(1, β|θ|)) dθ = −2/β`.
(Lean's `Real.log 0 = 0`; the integrand differs from the paper's only at `θ = 0`, a null set.) -/
theorem S3f_integral_log_min (β : ℝ) (hβ : 2 ≤ β) :
    ∫ θ in (-1/2 : ℝ)..(1/2), log (min 1 (β * |θ|)) = -2 / β := by
  have hβ0 : 0 < β := by linarith
  set b : ℝ := 1 / β with hbdef
  have hb0 : 0 < b := by positivity
  have hb2 : b ≤ 1 / 2 := by rw [hbdef, div_le_div_iff₀ hβ0 (by norm_num)]; linarith
  have hβb : β * b = 1 := by rw [hbdef]; field_simp
  set f : ℝ → ℝ := fun θ => log (min 1 (β * |θ|)) with hf
  set g : ℝ → ℝ := fun θ => log β + log θ with hg
  -- f vanishes where |θ| ≥ b
  have hzero : ∀ θ, b ≤ |θ| → f θ = 0 := by
    intro θ h
    have : 1 ≤ β * |θ| := by nlinarith
    simp [hf, min_eq_left this]
  have h1 : EqOn f (fun _ => 0) [[-1/2, -b]] := by
    intro θ hθ
    rw [Set.uIcc_of_le (by linarith)] at hθ
    exact hzero θ (by rw [abs_of_neg (by linarith [hθ.2])]; linarith [hθ.2])
  have h3 : EqOn f (fun _ => 0) [[b, 1/2]] := by
    intro θ hθ
    rw [Set.uIcc_of_le hb2] at hθ
    exact hzero θ (by rw [abs_of_pos (by linarith [hθ.1])]; exact hθ.1)
  -- on (-b, b], f = log β + log θ away from θ = 0
  have h2 : ∀ᵐ θ ∂volume, θ ∈ Ι (-b) b → f θ = g θ := by
    filter_upwards [(Set.countable_singleton (0 : ℝ)).ae_notMem volume] with θ hθ0 hθ
    have hne : θ ≠ 0 := by simpa using hθ0
    rw [Set.uIoc_of_le (by linarith)] at hθ
    have habs : |θ| ≤ b := abs_le.mpr ⟨hθ.1.le, hθ.2⟩
    have : β * |θ| ≤ 1 := by nlinarith
    simp only [hf, hg, min_eq_right this]
    rw [log_mul hβ0.ne' (abs_ne_zero.mpr hne), log_abs]
  have gint : IntervalIntegrable g volume (-b) b :=
    intervalIntegrable_const.add intervalIntegrable_log'
  have fint2 : IntervalIntegrable f volume (-b) b := by
    refine gint.congr_ae ?_
    rw [Filter.EventuallyEq, ae_restrict_iff' measurableSet_uIoc]
    filter_upwards [h2] with θ h hθ using (h hθ).symm
  have fint1 : IntervalIntegrable f volume (-1/2) (-b) :=
    (intervalIntegrable_const (c := (0 : ℝ))).congr
      (fun θ hθ => (h1 (Set.uIoc_subset_uIcc hθ)).symm)
  have fint3 : IntervalIntegrable f volume b (1/2) :=
    (intervalIntegrable_const (c := (0 : ℝ))).congr
      (fun θ hθ => (h3 (Set.uIoc_subset_uIcc hθ)).symm)
  have e1 : ∫ θ in (-1/2 : ℝ)..(-b), f θ = 0 := by rw [integral_congr h1]; simp
  have e3 : ∫ θ in b..(1/2 : ℝ), f θ = 0 := by rw [integral_congr h3]; simp
  have e2 : ∫ θ in (-b)..b, f θ = -2 / β := by
    rw [integral_congr_ae h2, hg, integral_add intervalIntegrable_const intervalIntegrable_log',
      intervalIntegral.integral_const, integral_log, log_neg_eq_log, smul_eq_mul]
    have hlb : log b = -log β := by rw [hbdef, one_div, log_inv]
    rw [hlb]
    field_simp
    rw [hbdef]; field_simp; ring
  show ∫ θ in (-1/2 : ℝ)..(1/2), f θ = -2 / β
  rw [← integral_add_adjacent_intervals fint1 (fint2.trans fint3),
    ← integral_add_adjacent_intervals fint2 fint3, e1, e2, e3]
  ring
