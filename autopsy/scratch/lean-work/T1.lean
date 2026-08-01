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

-- Part C, target 2:  mul f f = one  <->  f = one  \/  f = neg one
theorem sq_one_iff (f : GZ) : mul f f = one ↔ (f = one ∨ f = neg one) := by
  constructor
  · intro h
    have h1 : f.re * f.re - f.im * f.im = 1 := congrArg GZ.re h
    have h2 : f.re * f.im + f.im * f.re = 0 := congrArg GZ.im h
    have h2' : 2 * (f.re * f.im) = 0 := by omega
    have him : f.re = 0 ∨ f.im = 0 := by
      rcases Int.mul_eq_zero.mp (by omega : f.re * f.im = 0) with h | h
      · exact Or.inl h
      · exact Or.inr h
    rcases him with hre | hi
    · exfalso
      rw [hre] at h1
      nlinarith [sq_nonneg f.im]
    · rw [hi] at h1
      have : f.re * f.re = 1 := by omega
      have : f.re = 1 ∨ f.re = -1 := by
        rcases Int.eq_one_or_self_of_prime with _ | _
        · exact Or.inl (by nlinarith)
        · exact Or.inl (by nlinarith)
      sorry
  · intro h
    rcases h with h | h <;> subst h <;> rfl
