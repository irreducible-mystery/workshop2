/-
  Core.lean — the definitions this repository is about.

  Zero imports by design: this file compiles with `lean lean/Core.lean` and no
  project, no lakefile and no dependency. Nothing here may be redesigned.
-/

structure GZ where
  re : Int
  im : Int
  deriving DecidableEq

def zero : GZ := ⟨0, 0⟩
def one  : GZ := ⟨1, 0⟩
def I    : GZ := ⟨0, 1⟩

def add (z w : GZ) : GZ := ⟨z.re + w.re, z.im + w.im⟩
def neg (z : GZ) : GZ := ⟨-z.re, -z.im⟩
def mul (z w : GZ) : GZ :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def conj (z : GZ) : GZ := ⟨z.re, -z.im⟩

/-- The symbol. One free parameter `f`, carried on a single index pattern;
    `one` on the other admissible patterns; `zero` off the gate. -/
def Fs (f : GZ) (a b c d x y : Int) : GZ :=
  if x = (a + b) % 2 ∧ y = (b + c) % 2 ∧ d = (a + b + c) % 2 then
    (if a = 1 ∧ b = 1 ∧ c = 1 then f else one)
  else zero

def pentLhs (f : GZ) (a b c d : Int) : GZ :=
  let x := (a + b) % 2; let y := (x + c) % 2; let t := (y + d) % 2
  let w := (c + d) % 2; let v := (b + w) % 2; let u := (b + c) % 2
  mul (mul (Fs f a b c y x u) (Fs f a u d t y v)) (Fs f b c d v u w)

def pentRhs (f : GZ) (a b c d : Int) : GZ :=
  let x := (a + b) % 2; let y := (x + c) % 2; let t := (y + d) % 2
  let w := (c + d) % 2; let v := (b + w) % 2
  mul (Fs f x c d t y w) (Fs f a b w t x v)

def pentagonHolds (f : GZ) : Prop :=
  ∀ a b c d : Int, (a = 0 ∨ a = 1) → (b = 0 ∨ b = 1) → (c = 0 ∨ c = 1) →
    (d = 0 ∨ d = 1) → pentLhs f a b c d = pentRhs f a b c d

theorem sq_self_eq_one (a : Int) (h : a * a = 1) : a = 1 ∨ a = -1 := by
  rcases Int.lt_or_le a 0 with hneg | hpos
  · right
    have h' : (-a) * (-a) = 1 := by rw [Int.neg_mul_neg]; exact h
    have : (-a) = 1 := Int.eq_one_of_mul_eq_one_right (by omega) h'
    omega
  · left
    exact Int.eq_one_of_mul_eq_one_right hpos h

theorem sq_self_nonneg (a : Int) : 0 ≤ a * a := by
  rcases Int.lt_or_le a 0 with h | h
  · have : 0 ≤ (-a) * (-a) := Int.mul_nonneg (by omega) (by omega)
    rw [Int.neg_mul_neg] at this; exact this
  · exact Int.mul_nonneg h h

theorem sq_one_iff (f : GZ) : mul f f = one ↔ (f = one ∨ f = neg one) := by
  constructor
  · intro h
    have h1 : f.re * f.re - f.im * f.im = 1 := congrArg GZ.re h
    have h2 : f.re * f.im + f.im * f.re = 0 := congrArg GZ.im h
    have hz : f.re * f.im = 0 := by
      have : f.im * f.re = f.re * f.im := Int.mul_comm _ _
      omega
    rcases Int.mul_eq_zero.mp hz with hre | him
    · exfalso
      have := sq_self_nonneg f.im
      rw [hre] at h1
      omega
    · rw [him] at h1
      have hre1 : f.re * f.re = 1 := by omega
      rcases sq_self_eq_one _ hre1 with h' | h'
      · left;  cases f; simp_all [one]
      · right; cases f; simp_all [neg, one]
  · intro h
    rcases h with h | h <;> subst h <;> rfl

-- Part A, one assignment, to see how the gate reduces
example (f : GZ) : Fs f 1 1 1 1 0 0 = f := by decide +kernel
example (f : GZ) : Fs f 1 1 1 1 0 0 = f := by simp [Fs]

-- Part C target 1, forward direction at the single constraining assignment
example (f : GZ) (h : pentagonHolds f) : mul f f = one := by
  have := h 1 1 1 1 (Or.inr rfl) (Or.inr rfl) (Or.inr rfl) (Or.inr rfl)
  simp [pentLhs, pentRhs, Fs, mul, one] at this
  exact this
