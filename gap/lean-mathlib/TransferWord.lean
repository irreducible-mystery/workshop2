import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring.RingNF
import Mathlib.Tactic.Linarith.Frontend
import Mathlib.Tactic.NormNum.Basic

/- THE CLOSED FORM for the optimal asymmetric word  + T^m,  T = -b.
   Proved through Cayley-Hamilton for 2x2, which needs no spectral API. -/

structure M2 where
  a : ℝ
  b : ℝ
  c : ℝ
  d : ℝ

def mmul (X Y : M2) : M2 :=
  ⟨X.a*Y.a + X.b*Y.c, X.a*Y.b + X.b*Y.d, X.c*Y.a + X.d*Y.c, X.c*Y.b + X.d*Y.d⟩
def tr (X : M2) : ℝ := X.a + X.d
def det (X : M2) : ℝ := X.a*X.d - X.b*X.c
def idM : M2 := ⟨1,0,0,1⟩
def smul (k : ℝ) (X : M2) : M2 := ⟨k*X.a, k*X.b, k*X.c, k*X.d⟩
def sub (X Y : M2) : M2 := ⟨X.a-Y.a, X.b-Y.b, X.c-Y.c, X.d-Y.d⟩

/-- The transfer matrix of one step at gap g. -/
def T (g : ℝ) : M2 := ⟨1, g, 1, 0⟩

theorem det_T (g : ℝ) : det (T g) = -g := by simp [det, T]

/-- THE DETERMINANT IS MULTIPLICATIVE, so a word's determinant is the product
    of minus its gaps - no cancellation is ever possible. -/
theorem det_mul (X Y : M2) : det (mmul X Y) = det X * det Y := by
  simp [det, mmul]; ring

/-- CAYLEY-HAMILTON for 2x2: every transfer matrix satisfies its own
    characteristic equation, which IS the gap equation in disguise. -/
theorem cayley_hamilton (X : M2) :
    mmul X X = sub (smul (tr X) X) (smul (det X) idM) := by
  cases X; simp [mmul, sub, smul, tr, det, idM]; refine ⟨?_, ?_, ?_, ?_⟩ <;> ring

/-- For the one-step matrix that reads: M^2 = M + g*I, the gap equation. -/
theorem transfer_satisfies_gap (g : ℝ) :
    mmul (T g) (T g) = sub (smul 1 (T g)) (smul (-g) idM) := by
  have := cayley_hamilton (T g)
  rwa [show tr (T g) = 1 by simp [tr, T], det_T] at this

/-- The auxiliary sequence of the closed form: p_{k+1} = p_k - b*p_{k-1}. -/
def p (b : ℝ) : Nat → ℝ
  | 0 => 0
  | 1 => 1
  | k+2 => p b (k+1) - b * p b k

theorem p_step (b : ℝ) (k : Nat) : p b (k+2) = p b (k+1) - b * p b k := rfl

/-- POWERS OF THE NEGATIVE-GAP MATRIX, in closed form. -/
def Tpow (b : ℝ) : Nat → M2
  | 0 => idM
  | m+1 => mmul (Tpow b m) (T (-b))

theorem Tpow_closed (b : ℝ) (m : Nat) :
    Tpow b (m+1) = ⟨p b (m+2), -b * p b (m+1), p b (m+1), -b * p b m⟩ := by
  induction m with
  | zero => simp [Tpow, mmul, idM, T, p]
  | succ k ih =>
    show mmul (Tpow b (k+1)) (T (-b)) = _
    rw [ih]
    simp [mmul, T, p_step]
    refine ⟨?_, ?_, ?_, ?_⟩ <;> ring

/-- THE WORD  + T^m , and its trace and determinant - the closed form from the
    sweep, now proved. -/
def word (b : ℝ) (m : Nat) : M2 := mmul (T 1) (Tpow b m)

theorem det_Tpow (b : ℝ) (m : Nat) : det (Tpow b m) = b^m := by
  induction m with
  | zero => simp [Tpow, det, idM]
  | succ k ih =>
    show det (mmul (Tpow b k) (T (-b))) = _
    rw [det_mul, det_T, ih]
    ring

theorem word_det (b : ℝ) (m : Nat) : det (word b m) = -(b^m) := by
  unfold word
  rw [det_mul, det_T, det_Tpow]
  ring

theorem word_trace (b : ℝ) (m : Nat) :
    tr (word b (m+1)) = (2 - b) * p b (m+1) - b * p b m := by
  unfold word
  rw [Tpow_closed]
  simp [tr, mmul, T, p_step]
  ring

#print axioms det_T
#print axioms det_mul
#print axioms cayley_hamilton
#print axioms transfer_satisfies_gap
#print axioms Tpow_closed
#print axioms det_Tpow
#print axioms word_det
#print axioms word_trace
