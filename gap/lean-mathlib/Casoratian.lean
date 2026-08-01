import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic.Ring.RingNF
import Mathlib.Tactic.Linarith.Frontend
import Mathlib.Tactic.NormNum.Basic

/- THE DETERMINANT, in sequence form, and what it forbids. -/

/-- Two sequences obeying the SAME gap schedule. -/
def Obeys (s f : Nat → ℝ) : Prop := ∀ n, f (n+2) = f (n+1) + s n * f n

/-- The Casoratian - the determinant of the transfer matrix, as a sequence. -/
def W (f g : Nat → ℝ) (n : Nat) : ℝ := f (n+1) * g n - f n * g (n+1)

/-- IT SCALES BY EXACTLY MINUS THE GAP, EVERY STEP. This is
    det(M_n) = -s_n, with no matrix machinery. -/
theorem casoratian_step (s f g : Nat → ℝ) (hf : Obeys s f) (hg : Obeys s g)
    (n : Nat) : W f g (n+1) = -(s n) * W f g n := by
  unfold W
  rw [hf n, hg n]; ring

/-- FOR UNIT GAPS THE CASORATIAN NEVER CHANGES SIZE. -/
theorem casoratian_unit (s f g : Nat → ℝ) (hf : Obeys s f) (hg : Obeys s g)
    (hs : ∀ n, |s n| = 1) (n : Nat) : |W f g n| = |W f g 0| := by
  induction n with
  | zero => rfl
  | succ k ih =>
    rw [casoratian_step s f g hf hg k, abs_mul, abs_neg, hs k, one_mul, ih]

/-- SO TWO INDEPENDENT SOLUTIONS CANNOT BOTH VANISH IN THE LIMIT: if the
    Casoratian starts non-zero it stays non-zero, forever, whatever the
    schedule does. Growth and decay are locked together. -/
theorem independent_forever (s f g : Nat → ℝ) (hf : Obeys s f) (hg : Obeys s g)
    (hs : ∀ n, |s n| = 1) (h0 : W f g 0 ≠ 0) (n : Nat) : W f g n ≠ 0 := by
  intro hz
  have := casoratian_unit s f g hf hg hs n
  rw [hz] at this
  simp at this
  exact h0 (abs_eq_zero.mp this.symm)

/- ---------------------------------------------------------------------------
   THE COUNTING SERIES. Its radius of convergence IS the branch point. -/

/-- The Catalan generating function is a root of the gap equation at G = -x. -/
theorem catalan_gf_is_root (x : ℝ) (h : x ≤ 1/4) :
    ((1 - Real.sqrt (1-4*x))/2) * ((1 - Real.sqrt (1-4*x))/2)
      = ((1 - Real.sqrt (1-4*x))/2) + (-x) := by
  have hd : (0:ℝ) ≤ 1 - 4*x := by linarith
  have hs : Real.sqrt (1-4*x) ^ 2 = 1 - 4*x := Real.sq_sqrt hd
  nlinarith [hs]

/-- AND IT IS REAL EXACTLY UP TO x = 1/4. The tree-counting series' radius of
    convergence is the gap equation's branch point, reflected. -/
theorem catalan_radius (x : ℝ) : (∃ y : ℝ, y*y = y + (-x)) ↔ x ≤ 1/4 := by
  constructor
  · intro ⟨y, hy⟩; nlinarith [sq_nonneg (2*y - 1)]
  · intro h; exact ⟨(1 - Real.sqrt (1-4*x))/2, catalan_gf_is_root x h⟩

/-- At the radius itself the two roots coincide at 1/2 - the critical tree. -/
theorem catalan_at_radius : ((1 - Real.sqrt (1-4*(1/4)))/2 : ℝ) = 1/2 := by
  norm_num

#print axioms casoratian_step
#print axioms casoratian_unit
#print axioms independent_forever
#print axioms catalan_gf_is_root
#print axioms catalan_radius
#print axioms catalan_at_radius
