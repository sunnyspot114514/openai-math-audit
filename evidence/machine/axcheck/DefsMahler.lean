import ComparatorChallenges.MahlerConjecture
open MeasureTheory
#print OAI.SymmetricMahler.coordinatePolar
#check @OAI.SymmetricMahler.symmetric_mahler
-- volume on (Fin n → ℝ) is the product of Lebesgue measures
example (n : ℕ) : (volume : Measure (Fin n → ℝ)) = Measure.pi (fun _ => volume) := rfl
example : (volume : Measure ℝ) = Real.measureSpace.volume := rfl
-- sanity: unit cube has volume 1 in every dimension
example (n : ℕ) : volume (Set.Icc (0 : Fin n → ℝ) 1) = 1 := by
  simp [Real.volume_Icc_pi]
