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

-- ASSUMPTION 1: TASK.md calls conj "the non-trivial ring automorphism". Asserted, never proved.
theorem conj_mul (z w : GZ) : conj (mul z w) = mul (conj z) (conj w) := by
  cases z; cases w; simp [conj, mul]; omega
theorem conj_conj (z : GZ) : conj (conj z) = z := by cases z; simp [conj]
theorem conj_one : conj one = one := by simp [conj, one]
theorem conj_ne_id : conj I ≠ I := by simp [conj, I]

-- ASSUMPTION 2: mul associative. pentLhs writes mul (mul A B) C and never justifies the grouping.
theorem mul_assoc' (x y z : GZ) : mul (mul x y) z = mul x (mul y z) := by
  cases x; cases y; cases z; simp [mul]; constructor <;> ring

-- ASSUMPTION 3: one is a two-sided identity. Used implicitly everywhere.
theorem one_mul' (z : GZ) : mul one z = z := by cases z; simp [mul, one]
theorem mul_one' (z : GZ) : mul z one = z := by cases z; simp [mul, one]

-- ASSUMPTION 4: the two solutions are DISTINCT. If not, "f = one or f = neg one" is one solution.
theorem sols_distinct : (one : GZ) ≠ neg one := by simp [one, neg]

-- ASSUMPTION 5: is the `else zero` branch of Fs reachable at all, or dead code?
theorem gate_can_fail : Fs one 0 0 0 1 0 0 = zero := by decide
