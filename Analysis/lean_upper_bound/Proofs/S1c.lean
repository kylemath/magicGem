import Mathlib

open Polynomial

/-- Taylor coefficients at `1`: the `r`-th coefficient of `P_γ(t+1)` is `Σ_j C(j,r) γ_j`. -/
lemma S1c_taylor_coeff {R : Type*} [CommRing R] {n : ℕ} (γ : Fin n → R) (r : ℕ) :
    (taylor 1 (∑ j : Fin n, C (γ j) * X ^ (j : ℕ))).coeff r
      = ∑ j : Fin n, ((j : ℕ).choose r : R) * γ j := by
  rw [map_sum, finsetSum_coeff]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [taylor_mul, taylor_C, taylor_X_pow, coeff_C_mul, C_1, coeff_X_add_one_pow, mul_comm]

/-- **Step S1c (Lemma poly_form, (ii) ⇔ (iii)).** For `γ : Fin n → R` (any commutative ring,
e.g. `ℤ` or `ℚ`) with `P_γ(t) = Σ_j γ_j t^j`:
`Σ_j C(j,r) γ_j = 0` for all `r ≤ k` iff `(t − 1)^(k+1)` divides `P_γ`. -/
theorem S1c_binom_moments_iff_dvd {R : Type*} [CommRing R] {n : ℕ} (γ : Fin n → R) (k : ℕ) :
    (∀ r ≤ k, ∑ j : Fin n, ((j : ℕ).choose r : R) * γ j = 0) ↔
      (X - 1 : R[X]) ^ (k + 1) ∣ ∑ j : Fin n, C (γ j) * X ^ (j : ℕ) := by
  set P : R[X] := ∑ j : Fin n, C (γ j) * X ^ (j : ℕ)
  have hX : taylor (1 : R) ((X - 1 : R[X]) ^ (k + 1)) = X ^ (k + 1) := by
    rw [taylor_pow, map_sub, taylor_X, map_one]; simp
  rw [← map_dvd_iff (taylorEquiv (1 : R))]
  change _ ↔ taylor 1 _ ∣ taylor 1 P
  rw [hX, X_pow_dvd_iff]
  simp only [← S1c_taylor_coeff, P, Nat.lt_succ_iff]
