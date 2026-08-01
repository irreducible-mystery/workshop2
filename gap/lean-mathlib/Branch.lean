import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic.Ring.RingNF
import Mathlib.Tactic.Linarith.Frontend
import Mathlib.Tactic.NormNum.Basic

/- -1/4 AS AN ACTUAL NUMBER: the branch point over the reals. -/

/-- The discriminant vanishes at exactly one gap. -/
theorem disc_zero_iff (G : ℝ) : 1 + 4*G = 0 ↔ G = -1/4 := by
  constructor <;> intro h <;> linarith

/-- AT THAT GAP THE TWO ROOTS ARE ONE. The equation has the unique root 1/2. -/
theorem double_root_at_branch (x : ℝ) : x*x = x + (-1/4) ↔ x = 1/2 := by
  constructor
  · intro h; nlinarith [sq_nonneg (x - 1/2)]
  · intro h; subst h; norm_num

/-- The squared difference of the roots IS the discriminant, over ℝ. -/
theorem disc_is_squared_gap (G x y : ℝ) (hx : x*x = x + G) (hy : y*y = y + G)
    (hne : x ≠ y) : (x - y)^2 = 1 + 4*G := by
  have hs : x + y = 1 := by
    have key : (x - y) * (x + y - 1) = 0 := by nlinarith
    rcases mul_eq_zero.mp key with h | h
    · exact absurd (by linarith : x = y) hne
    · linarith
  nlinarith

/-- REAL ROOTS EXIST EXACTLY ABOVE THE BRANCH POINT. -/
theorem real_root_iff (G : ℝ) : (∃ x : ℝ, x*x = x + G) ↔ -1/4 ≤ G := by
  constructor
  · intro ⟨x, hx⟩; nlinarith [sq_nonneg (2*x - 1)]
  · intro h
    refine ⟨(1 + Real.sqrt (1+4*G))/2, ?_⟩
    have hd : (0:ℝ) ≤ 1 + 4*G := by linarith
    have hs : Real.sqrt (1+4*G) ^ 2 = 1 + 4*G := Real.sq_sqrt hd
    nlinarith [hs]

/-- BELOW IT, NOTHING REAL. -/
theorem no_real_root_below (G : ℝ) (h : G < -1/4) : ¬ ∃ x : ℝ, x*x = x + G := by
  intro ⟨x, hx⟩; nlinarith [sq_nonneg (2*x - 1)]

/-- THE CEILING, as an explicit number: the larger root at gap G. -/
noncomputable def sPlus (G : ℝ) : ℝ := (1 + Real.sqrt (1+4*G))/2

theorem sPlus_is_root (G : ℝ) (h : -1/4 ≤ G) : sPlus G * sPlus G = sPlus G + G := by
  have hd : (0:ℝ) ≤ 1 + 4*G := by linarith
  have hs : Real.sqrt (1+4*G) ^ 2 = 1 + 4*G := Real.sq_sqrt hd
  unfold sPlus; nlinarith [hs]

/-- At the golden gap it is the golden ratio. -/
theorem sPlus_one : sPlus 1 = (1 + Real.sqrt 5)/2 := by
  unfold sPlus; norm_num

theorem golden_identity : sPlus 1 * sPlus 1 = sPlus 1 + 1 :=
  sPlus_is_root 1 (by norm_num)

/-- At the branch point it is 1/2 - and so is the other root. -/
theorem sPlus_branch : sPlus (-1/4) = 1/2 := by
  unfold sPlus; norm_num

#print axioms disc_zero_iff
#print axioms double_root_at_branch
#print axioms disc_is_squared_gap
#print axioms real_root_iff
#print axioms no_real_root_below
#print axioms golden_identity
#print axioms sPlus_branch
