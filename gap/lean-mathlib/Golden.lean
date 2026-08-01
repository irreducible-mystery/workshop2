import Mathlib.Data.Real.Irrational
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic.Ring.RingNF
import Mathlib.Tactic.Linarith.Frontend
import Mathlib.Tactic.NormNum.Basic

/- The golden gap, and the one thing that exists ONLY at the branch point. -/

noncomputable def sPlus (G : ℝ) : ℝ := (1 + Real.sqrt (1+4*G))/2

theorem sqrt5_irrational : Irrational (Real.sqrt 5) := by
  have hp : Nat.Prime 5 := by decide
  simpa using hp.irrational_sqrt

/-- THE GOLDEN GAP'S ROOT IS IRRATIONAL. -/
theorem sPlus_one_irrational : Irrational (sPlus 1) := by
  unfold sPlus
  have h : (1:ℝ) + 4*1 = 5 := by norm_num
  rw [h]
  rintro ⟨q, hq⟩
  apply sqrt5_irrational
  refine ⟨2*q - 1, ?_⟩
  have : ((2*q - 1 : ℚ) : ℝ) = 2*(q:ℝ) - 1 := by
    simp [Rat.cast_sub, Rat.cast_mul]
  rw [this, hq]; ring

/-- THE BRANCH POINT'S ROOT IS NOT. It is exactly 1/2 - the collision is the
    one gap whose root is rational. -/
theorem sPlus_branch_rational : sPlus (-1/4) = 1/2 := by
  unfold sPlus; norm_num

/- ---------------------------------------------------------------------------
   THE NILPOTENT SOLUTION EXISTS AT -1/4 AND NOWHERE ELSE.
   Work in the dual numbers R[e]/(e^2), written as pairs. -/

structure Dual where
  re : ℝ
  ep : ℝ

def dmul (x y : Dual) : Dual := ⟨x.re*y.re, x.re*y.ep + x.ep*y.re⟩
def dadd (x y : Dual) : Dual := ⟨x.re+y.re, x.ep+y.ep⟩
def dconst (r : ℝ) : Dual := ⟨r, 0⟩

/-- At the branch point there is a solution with a NON-ZERO nilpotent part. -/
theorem nilpotent_solution_at_branch :
    dmul ⟨1/2, 1⟩ ⟨1/2, 1⟩ = dadd ⟨1/2, 1⟩ (dconst (-1/4)) := by
  simp [dmul, dadd, dconst]; norm_num

/-- AND NOWHERE ELSE: a solution with non-zero nilpotent part forces the gap to
    be exactly -1/4 and the real part to be exactly 1/2. -/
theorem nilpotent_forces_branch (x : Dual) (G : ℝ)
    (h : dmul x x = dadd x (dconst G)) (hep : x.ep ≠ 0) :
    x.re = 1/2 ∧ G = -1/4 := by
  have h1 : x.re * x.re = x.re + G := by
    have := congrArg Dual.re h; simpa [dmul, dadd, dconst] using this
  have h2 : x.re * x.ep + x.ep * x.re = x.ep := by
    have := congrArg Dual.ep h; simpa [dmul, dadd, dconst] using this
  have hre : x.re = 1/2 := by
    have : x.ep * (2*x.re - 1) = 0 := by nlinarith [h2]
    rcases mul_eq_zero.mp this with hz | hz
    · exact absurd hz hep
    · linarith
  refine ⟨hre, ?_⟩
  rw [hre] at h1; linarith

#print axioms sqrt5_irrational
#print axioms sPlus_one_irrational
#print axioms sPlus_branch_rational
#print axioms nilpotent_solution_at_branch
#print axioms nilpotent_forces_branch
