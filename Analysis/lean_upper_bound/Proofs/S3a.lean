import Mathlib

open Polynomial

/-- **Step S3a (Mahler measure / Jensen).** For a nonzero integer polynomial `P`, the
average of `log |P|` over the unit circle is `≥ 0`, i.e. `log 𝓜(P) ≥ 0`.
Stated with Mathlib's `Real.circleAverage` over the circle of radius 1 centred at 0
(the paper's `∫_{-1/2}^{1/2} log|P(e^{2πiθ})| dθ` is the same average, reparametrised). -/
theorem S3a_circleAverage_log_nonneg {P : ℤ[X]} (hP : P ≠ 0) :
    0 ≤ Real.circleAverage (fun z => Real.log ‖eval z (P.map (Int.castRingHom ℂ))‖) 0 1 := by
  rw [← logMahlerMeasure_def, logMahlerMeasure_eq_log_MahlerMeasure]
  exact Real.log_nonneg (one_le_mahlerMeasure_of_ne_zero hP)
