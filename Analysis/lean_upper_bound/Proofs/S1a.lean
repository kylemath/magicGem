import Mathlib

/-- **Step S1a (Lemma poly_form, first statement).**
If a weight `φ` depends only on the column index `j`, then summing `φ j * f i j` over all
cells equals summing `φ j * γ j`, where `γ j = Σ_i f i j` is the `j`-th column sum.
(The paper's normalisation `1/N` of the inner product is a constant factor and is omitted.) -/
theorem S1a_sum_col_weight {n : ℕ} (f : Fin n → Fin n → ℝ) (φ : Fin n → ℝ) :
    ∑ i, ∑ j, φ j * f i j = ∑ j, φ j * ∑ i, f i j := by
  rw [Finset.sum_comm]
  simp [Finset.mul_sum]
