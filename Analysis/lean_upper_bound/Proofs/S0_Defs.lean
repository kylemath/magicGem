import Mathlib

open Polynomial BigOperators

/-! Step S0: the objects of Theorem 3.7(a). -/

/-- An arrangement of order `n`: the grid filled with `1, …, n²`, each value once
(stored as values `0, …, n² - 1` shifted by one). -/
abbrev Arrangement (n : ℕ) := Fin n × Fin n ≃ Fin (n ^ 2)

/-- The entry `s i j ∈ {1, …, n²}`. -/
def Arrangement.entry {n : ℕ} (S : Arrangement n) (i j : Fin n) : ℤ := (S (i, j) : ℤ) + 1

/-- The magic constant `M(n) = n (n² + 1) / 2`, written as `2 M(n) = n (n² + 1)`. -/
def twiceMagic (n : ℕ) : ℤ := n * (n ^ 2 + 1)

/-- Twice the column deviation, `2 γ_j = 2 Σ_i s_ij − 2 M(n)` (doubling keeps it integral). -/
def Arrangement.twiceGamma {n : ℕ} (S : Arrangement n) (j : Fin n) : ℤ :=
  2 * ∑ i, S.entry i j - twiceMagic n

/-- `P_γ(t) = Σ_j γ_j t^j` for an integer vector `γ`. -/
noncomputable def Pgamma {n : ℕ} (γ : Fin n → ℤ) : ℤ[X] := ∑ j, C (γ j) * X ^ (j : ℕ)

/-- Sanity check: the order-5 witness of Appendix C has `γ = (1, −4, 6, −4, 1)`,
so `P_γ = (1 − t)^4`. -/
example : (Pgamma ![(1 : ℤ), -4, 6, -4, 1]) = (1 - X) ^ 4 := by
  simp [Pgamma, Fin.sum_univ_five]; ring
