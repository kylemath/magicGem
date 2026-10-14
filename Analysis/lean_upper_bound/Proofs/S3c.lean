import Mathlib

open Polynomial

/-- Taylor coefficients at `1` (as in S1c): the `r`-th coefficient of `P_γ(t+1)` is
`Σ_j C(j,r) γ_j`. -/
lemma S3c_taylor_coeff {n : ℕ} (γ : Fin n → ℂ) (r : ℕ) :
    (taylor 1 (∑ j : Fin n, C (γ j) * X ^ (j : ℕ))).coeff r
      = ∑ j : Fin n, ((j : ℕ).choose r : ℂ) * γ j := by
  rw [map_sum, finsetSum_coeff]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [taylor_mul, taylor_C, taylor_X_pow, coeff_C_mul, C_1, coeff_X_add_one_pow, mul_comm]

/-- `(X-1)^K ∣ P_γ` gives vanishing binomial moments `Σ_j C(j,r) γ_j = 0` for `r < K`. -/
lemma S3c_moments_of_dvd {n : ℕ} (γ : Fin n → ℂ) (K : ℕ)
    (h : (X - 1 : ℂ[X]) ^ K ∣ ∑ j : Fin n, C (γ j) * X ^ (j : ℕ)) :
    ∀ r < K, ∑ j : Fin n, ((j : ℕ).choose r : ℂ) * γ j = 0 := by
  have hX : taylor (1 : ℂ) ((X - 1 : ℂ[X]) ^ K) = X ^ K := by
    rw [taylor_pow, map_sub, taylor_X, map_one]; simp
  rw [← map_dvd_iff (taylorEquiv (1 : ℂ))] at h
  change taylor 1 _ ∣ taylor 1 _ at h
  rw [hX, X_pow_dvd_iff] at h
  intro r hr; rw [← S3c_taylor_coeff]; exact h r hr

/-- One step of Pascal's rule for truncated binomial expansions. -/
lemma S3c_pascal (w : ℂ) (j K : ℕ) :
    (1 + w) * ∑ r ∈ Finset.range (K + 1), (j.choose r : ℂ) * w ^ r
      = ∑ r ∈ Finset.range (K + 1), ((j + 1).choose r : ℂ) * w ^ r
        + (j.choose K : ℂ) * w ^ (K + 1) := by
  induction K with
  | zero => simp
  | succ K ih =>
    rw [Finset.sum_range_succ, mul_add, ih, Finset.sum_range_succ (n := K + 1),
      Nat.choose_succ_succ]
    push_cast; ring

/-- Discrete Taylor formula with remainder for `z^j` at `1`:
`z^j = Σ_{r<K} C(j,r)(z−1)^r + (z−1)^K · Σ_{i<j} C(i,K−1) z^{j−1−i}` (here `K = K'+1`). -/
lemma S3c_monomial_taylor (z : ℂ) (K j : ℕ) :
    z ^ j = ∑ r ∈ Finset.range (K + 1), (j.choose r : ℂ) * (z - 1) ^ r
      + (z - 1) ^ (K + 1) * ∑ i ∈ Finset.range j, (i.choose K : ℂ) * z ^ (j - 1 - i) := by
  induction j with
  | zero => simp [Finset.sum_range_succ']
  | succ j ih =>
    have hR : ∑ i ∈ Finset.range (j + 1), (i.choose K : ℂ) * z ^ (j + 1 - 1 - i)
        = z * ∑ i ∈ Finset.range j, (i.choose K : ℂ) * z ^ (j - 1 - i) + (j.choose K : ℂ) := by
      rw [Finset.sum_range_succ, Finset.mul_sum]
      simp only [Nat.add_sub_cancel, Nat.sub_self, pow_zero, mul_one]
      congr 1
      refine Finset.sum_congr rfl fun i hi => ?_
      have hi := Finset.mem_range.mp hi
      rw [show j - i = (j - 1 - i) + 1 by omega, pow_succ]; ring
    have hp := S3c_pascal (z - 1) j K
    rw [show (1 : ℂ) + (z - 1) = z by ring] at hp
    rw [pow_succ, ih, hR]
    linear_combination hp

/-- Hockey stick: `Σ_{i<j} C(i,K) = C(j,K+1)`. -/
lemma S3c_hockey (K j : ℕ) : ∑ i ∈ Finset.range j, i.choose K = j.choose (K + 1) := by
  induction j with
  | zero => simp
  | succ j ih => rw [Finset.sum_range_succ, ih, Nat.choose_succ_succ, add_comm]

/-- **Step S3c (Taylor bound in Lemma jensen).** Let `γ : Fin n → ℂ`, `P_γ(z) = Σ_j γ_j z^j`,
`L = Σ_j |γ_j|`, and `K ≥ 1` with `(X − 1)^K ∣ P_γ`. Then for `|z| ≤ 1`,
`|P_γ(z)| ≤ L · C(n−1, K) · |z − 1|^K`.
Proved algebraically (no integrals): `P_γ = (X−1)^K Q` with
`Q(z) = Σ_j γ_j Σ_{i<j} C(i,K−1) z^{j−1−i}` and `|Q(z)| ≤ Σ_j |γ_j| C(j,K)` on the disc. -/
theorem S3c_taylor_bound {n : ℕ} (γ : Fin n → ℂ) (K : ℕ) (hK : 1 ≤ K)
    (hdiv : (X - 1 : ℂ[X]) ^ K ∣ ∑ j : Fin n, C (γ j) * X ^ (j : ℕ))
    (z : ℂ) (hz : ‖z‖ ≤ 1) :
    ‖∑ j : Fin n, γ j * z ^ (j : ℕ)‖
      ≤ (∑ j : Fin n, ‖γ j‖) * ((n - 1).choose K : ℝ) * ‖z - 1‖ ^ K := by
  obtain ⟨K, rfl⟩ : ∃ K', K = K' + 1 := ⟨K - 1, by omega⟩
  have hmom := S3c_moments_of_dvd γ (K + 1) hdiv
  set R : Fin n → ℂ := fun j =>
    ∑ i ∈ Finset.range (j : ℕ), (i.choose K : ℂ) * z ^ ((j : ℕ) - 1 - i)
  -- P(z) = (z-1)^(K+1) * Σ_j γ_j R_j
  have hP : ∑ j : Fin n, γ j * z ^ (j : ℕ) = (z - 1) ^ (K + 1) * ∑ j : Fin n, γ j * R j := by
    rw [Finset.sum_congr rfl fun j _ => by rw [S3c_monomial_taylor z K (j : ℕ)]]
    simp only [mul_add, Finset.sum_add_distrib, Finset.mul_sum]
    have h0 : ∑ j : Fin n, ∑ r ∈ Finset.range (K + 1),
        γ j * ((((j : ℕ).choose r : ℕ) : ℂ) * (z - 1) ^ r) = 0 := by
      rw [Finset.sum_comm]
      refine Finset.sum_eq_zero fun r hr => ?_
      have := hmom r (Finset.mem_range.mp hr)
      calc _ = (∑ j : Fin n, ((j : ℕ).choose r : ℂ) * γ j) * (z - 1) ^ r := by
              rw [Finset.sum_mul]; exact Finset.sum_congr rfl fun j _ => by ring
        _ = 0 := by rw [this, zero_mul]
    rw [h0, zero_add]
    exact Finset.sum_congr rfl fun j _ => by simp only [R, Finset.mul_sum]; ring_nf
  -- |R_j| ≤ C(j, K+1) ≤ C(n-1, K+1)
  have hR : ∀ j : Fin n, ‖R j‖ ≤ ((n - 1).choose (K + 1) : ℝ) := by
    intro j
    calc ‖R j‖ ≤ ∑ i ∈ Finset.range (j : ℕ), ‖(i.choose K : ℂ) * z ^ ((j : ℕ) - 1 - i)‖ :=
          norm_sum_le _ _
      _ ≤ ∑ i ∈ Finset.range (j : ℕ), (i.choose K : ℝ) := by
          refine Finset.sum_le_sum fun i _ => ?_
          rw [norm_mul, norm_pow, Complex.norm_natCast]
          exact mul_le_of_le_one_right (by positivity) (pow_le_one₀ (norm_nonneg _) hz)
      _ = ((j : ℕ).choose (K + 1) : ℝ) := by exact_mod_cast S3c_hockey K j
      _ ≤ ((n - 1).choose (K + 1) : ℝ) := by
          exact_mod_cast Nat.choose_le_choose _ (by omega)
  rw [hP, norm_mul, norm_pow, mul_comm]
  gcongr
  calc ‖∑ j : Fin n, γ j * R j‖ ≤ ∑ j : Fin n, ‖γ j‖ * ‖R j‖ := by
        refine (norm_sum_le _ _).trans (le_of_eq ?_); simp
    _ ≤ ∑ j : Fin n, ‖γ j‖ * ((n - 1).choose (K + 1) : ℝ) :=
        Finset.sum_le_sum fun j _ => mul_le_mul_of_nonneg_left (hR j) (norm_nonneg _)
    _ = _ := by rw [Finset.sum_mul]
