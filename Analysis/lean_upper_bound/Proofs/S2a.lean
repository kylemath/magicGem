import Mathlib

/-- Sum of `m` distinct elements of `{1,…,N}` is at most `m(2N−m+1)/2` (the `m` largest)
and at least `m(m+1)/2` (the `m` smallest); stated with the factor 2 cleared, in `ℤ`. -/
theorem S2a_sum_distinct_bounds (N : ℕ) (s : Finset ℕ) (hs : s ⊆ Finset.Icc 1 N) :
    (s.card : ℤ) * (s.card + 1) ≤ 2 * ∑ x ∈ s, (x : ℤ) ∧
      2 * ∑ x ∈ s, (x : ℤ) ≤ (s.card : ℤ) * (2 * N - s.card + 1) := by
  induction N generalizing s with
  | zero =>
    have : s = ∅ := Finset.subset_empty.mp (by simpa using hs)
    subst this; simp
  | succ N ih =>
    have hcard : s.card ≤ N + 1 := by
      simpa using Finset.card_le_card hs
    by_cases hN : N + 1 ∈ s
    · have hs' : s.erase (N + 1) ⊆ Finset.Icc 1 N := by
        intro x hx
        have hx1 := Finset.mem_erase.mp hx
        have := hs hx1.2
        simp only [Finset.mem_Icc] at this ⊢; omega
      obtain ⟨h1, h2⟩ := ih _ hs'
      rw [Finset.card_erase_of_mem hN] at h1 h2
      rw [← Finset.add_sum_erase s _ hN]
      have hpos : 1 ≤ s.card := Finset.card_pos.mpr ⟨_, hN⟩
      push_cast [hpos] at h1 h2 ⊢
      have : (s.card : ℤ) ≤ N + 1 := by exact_mod_cast hcard
      constructor <;> nlinarith
    · have hs' : s ⊆ Finset.Icc 1 N := by
        intro x hx
        have := hs hx
        have hne : x ≠ N + 1 := fun h => hN (h ▸ hx)
        simp only [Finset.mem_Icc] at this ⊢; omega
      obtain ⟨h1, h2⟩ := ih _ hs'
      refine ⟨h1, h2.trans ?_⟩
      push_cast
      nlinarith [(Nat.cast_nonneg s.card : (0 : ℤ) ≤ s.card)]

/-- **Step S2a (Lemma col_feasible, inequality (col_feasible)).**
Let `s : Fin n × Fin n → ℕ` be an arrangement: injective with values in `{1,…,N}`, `N = n²`.
Let `γ_j = Σ_i s(i,j) − n(N+1)/2` be its column deviations. Then for every set `J` of `p`
columns, `|Σ_{j∈J} γ_j| ≤ p n (N − p n) / 2`. -/
theorem S2a_col_feasible {n : ℕ} (s : Fin n × Fin n → ℕ) (hinj : Function.Injective s)
    (hrange : ∀ c, s c ∈ Finset.Icc 1 (n ^ 2)) (J : Finset (Fin n)) :
    |∑ j ∈ J, (∑ i : Fin n, (s (i, j) : ℚ) - n * ((n ^ 2 : ℕ) + 1) / 2)|
      ≤ (J.card * n : ℚ) * ((n ^ 2 : ℕ) - J.card * n) / 2 := by
  set N := n ^ 2
  -- the values in the columns of J
  set T : Finset ℕ := (Finset.univ ×ˢ J).image s
  have hT : T ⊆ Finset.Icc 1 N := by
    intro x hx; obtain ⟨c, -, rfl⟩ := Finset.mem_image.mp hx; exact hrange c
  have hTcard : T.card = J.card * n := by
    rw [Finset.card_image_of_injective _ hinj, Finset.card_product, Finset.card_univ,
      Fintype.card_fin, mul_comm]
  have hTsum : ∑ x ∈ T, (x : ℚ) = ∑ j ∈ J, ∑ i : Fin n, (s (i, j) : ℚ) := by
    rw [Finset.sum_image (fun a _ b _ h => hinj h), Finset.sum_product, Finset.sum_comm]
  obtain ⟨h1, h2⟩ := S2a_sum_distinct_bounds N T hT
  rw [hTcard] at h1 h2
  have h1' := (Int.cast_le (R := ℚ)).mpr h1
  have h2' := (Int.cast_le (R := ℚ)).mpr h2
  push_cast at h1' h2'
  rw [hTsum] at h1' h2'
  rw [Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul]
  rw [abs_le]; constructor <;> nlinarith
