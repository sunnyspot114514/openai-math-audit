import ComparatorChallenges.SymmetricPolar
set_option pp.notation false in
#print OAI.SymmetricPolar.HasSymplecticEmbedding
#print OAI.SymmetricPolar.HasSymplecticEmbedding
#print OAI.SymmetricPolar.gromovWidth
#print OAI.SymmetricPolar.capacityBall
#print OAI.SymmetricPolar.omega0
#print OAI.SymmetricPolar.polar
#print OAI.SymmetricPolar.polarProduct
#print OAI.SymmetricPolar.IsSymmetricConvexBody
#print OAI.SymmetricPolar.Phase
#print OAI.SymmetricPolar.Position
#check @OAI.SymmetricPolar.symmetric_polar_main
open scoped ContDiff in
example : (∞ : WithTop ℕ∞) = ((⊤ : ℕ∞) : WithTop ℕ∞) := rfl
-- ∞ (C^∞) is strictly below ω (analytic) in WithTop ℕ∞
open scoped ContDiff in
example : (∞ : WithTop ℕ∞) < ω := WithTop.coe_lt_top _
-- omega0 is the standard form Σ dq_j ∧ dp_j : value on (e_q1, e_p1) is 1 in dimension 1
example : OAI.SymmetricPolar.omega0 (n := 1)
    (EuclideanSpace.single 0 1, 0) (0, EuclideanSpace.single 0 1) = 1 := by
  simp [OAI.SymmetricPolar.omega0]
