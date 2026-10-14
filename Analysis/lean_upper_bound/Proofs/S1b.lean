import Mathlib

open Polynomial

/-- The functional `ℓ_γ(Q) = Σ_j γ_j Q(j)` on `ℚ[X]`. -/
noncomputable def S1b_ell {n : ℕ} (γ : Fin n → ℚ) (Q : ℚ[X]) : ℚ :=
  ∑ j : Fin n, Q.eval (j : ℚ) * γ j

/-- If `p i` is monic of degree `i` for every `i`, then `ℓ_γ` kills `p 0, …, p k` iff it kills
every polynomial of degree `≤ k` (a triangular change of basis). -/
lemma S1b_monic_family {n : ℕ} (γ : Fin n → ℚ) (p : ℕ → ℚ[X])
    (hmon : ∀ i, (p i).Monic) (hdeg : ∀ i, (p i).natDegree = i) (k : ℕ) :
    (∀ i ≤ k, S1b_ell γ (p i) = 0) ↔ ∀ Q : ℚ[X], Q.degree < (k + 1 : ℕ) → S1b_ell γ Q = 0 := by
  constructor
  · intro h
    -- induction on the degree bound `d ≤ k + 1`
    suffices H : ∀ d ≤ k + 1, ∀ Q : ℚ[X], Q.degree < (d : ℕ) → S1b_ell γ Q = 0 from H _ le_rfl
    intro d
    induction d with
    | zero =>
      intro _ Q hQ
      have : Q = 0 := by
        ext m; exact (degree_lt_iff_coeff_zero Q 0).mp hQ m (Nat.zero_le _)
      subst this; simp [S1b_ell]
    | succ d ih =>
      intro hd Q hQ
      set a := Q.coeff d
      set Q' := Q - C a * p d
      have hQ' : Q'.degree < (d : ℕ) := by
        rw [degree_lt_iff_coeff_zero]
        intro m hm
        rcases Nat.eq_or_lt_of_le hm with rfl | hlt
        · have h1 : (p d).coeff d = 1 := by
            have := (hmon d).coeff_natDegree; rwa [hdeg] at this
          simp [Q', a, h1]
        · have h1 : Q.coeff m = 0 := (degree_lt_iff_coeff_zero Q _).mp hQ m (by omega)
          have h2 : (p d).coeff m = 0 := coeff_eq_zero_of_natDegree_lt (by rw [hdeg]; exact hlt)
          simp [Q', h1, h2]
      have e : Q = Q' + C a * p d := by simp [Q']
      have hl : S1b_ell γ Q = S1b_ell γ Q' + a * S1b_ell γ (p d) := by
        rw [e]; simp only [S1b_ell, eval_add, eval_mul, eval_C, add_mul, Finset.sum_add_distrib,
          Finset.mul_sum, mul_assoc]
      rw [hl, ih (by omega) Q' hQ', h d (by omega), mul_zero, add_zero]
  · intro h i hi
    apply h
    rw [degree_eq_natDegree (hmon i).ne_zero, hdeg]
    exact_mod_cast Nat.lt_succ_of_le hi

/-- **Step S1b (Lemma poly_form, (i) ⇔ (ii)).** For `γ : Fin n → ℚ`, any constant `c`
(the paper uses the centred coordinate `x_j = j − (n−1)/2`, i.e. `c = (n−1)/2`; `c = 0` gives
plain powers of `j`) and any `k`:
`Σ_j (j − c)^m γ_j = 0` for all `m ≤ k`  iff  `Σ_j C(j,r) γ_j = 0` for all `r ≤ k`. -/
theorem S1b_power_moments_iff_binom_moments {n : ℕ} (γ : Fin n → ℚ) (c : ℚ) (k : ℕ) :
    (∀ m ≤ k, ∑ j : Fin n, ((j : ℚ) - c) ^ m * γ j = 0) ↔
      (∀ r ≤ k, ∑ j : Fin n, ((j : ℕ).choose r : ℚ) * γ j = 0) := by
  -- family 1: (X - c)^m
  have A := S1b_monic_family γ (fun m => (X - C c) ^ m) (fun m => (monic_X_sub_C c).pow m)
    (fun m => by simp) k
  -- family 2: descending Pochhammer, `descPochhammer r (j) = r! * C(j, r)`
  have B := S1b_monic_family γ (fun r => descPochhammer ℚ r) (fun r => monic_descPochhammer ℚ r)
    (fun r => descPochhammer_natDegree ℚ r) k
  have hA : ∀ m, S1b_ell γ ((X - C c) ^ m) = ∑ j : Fin n, ((j : ℚ) - c) ^ m * γ j := by
    intro m; simp [S1b_ell]
  have hB : ∀ r, S1b_ell γ (descPochhammer ℚ r)
      = (r.factorial : ℚ) * ∑ j : Fin n, ((j : ℕ).choose r : ℚ) * γ j := by
    intro r
    simp only [S1b_ell, Finset.mul_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    have := descPochhammer_eval_eq_descFactorial ℚ (j : ℕ) r
    rw [this, Nat.descFactorial_eq_factorial_mul_choose]; push_cast; ring
  simp only [hA] at A
  simp only [hB, mul_eq_zero, Nat.cast_eq_zero, Nat.factorial_ne_zero, false_or] at B
  rw [A, B]
