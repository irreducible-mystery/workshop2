-- Recheck 2: is the general programme blocked by the toolbox, or by the carrier?
-- Zero imports.

-- A commutative ring, hand-rolled.  No Mathlib, no Std.
class CRing (R : Type) where
  zero : R
  one  : R
  add  : R → R → R
  neg  : R → R
  mul  : R → R → R
  add_assoc  : ∀ a b c, add (add a b) c = add a (add b c)
  add_comm   : ∀ a b, add a b = add b a
  add_zero   : ∀ a, add a zero = a
  add_neg    : ∀ a, add a (neg a) = zero
  mul_assoc  : ∀ a b c, mul (mul a b) c = mul a (mul b c)
  mul_comm   : ∀ a b, mul a b = mul b a
  mul_one    : ∀ a, mul a one = a
  left_distrib : ∀ a b c, mul a (add b c) = add (mul a b) (mul a c)

open CRing

-- Invertibility WITHOUT division: expressible in any ring.
def IsUnit {R : Type} [CRing R] (p : R) : Prop := ∃ u, mul p u = one

-- The EIGHT-parameter symbol.  This is P1's object, not P0's one-parameter slice.
def Sym (R : Type) := Int → Int → Int → R

def Fg {R : Type} [CRing R] (g : Sym R) (a b c d x y : Int) : R :=
  if x = (a + b) % 2 ∧ y = (b + c) % 2 ∧ d = (a + b + c) % 2 then g a b c
  else zero

def pentLhsG {R : Type} [CRing R] (g : Sym R) (a b c d : Int) : R :=
  let x := (a + b) % 2; let y := (x + c) % 2; let t := (y + d) % 2
  let w := (c + d) % 2; let v := (b + w) % 2; let u := (b + c) % 2
  mul (mul (Fg g a b c y x u) (Fg g a u d t y v)) (Fg g b c d v u w)

def pentRhsG {R : Type} [CRing R] (g : Sym R) (a b c d : Int) : R :=
  let x := (a + b) % 2; let y := (x + c) % 2; let t := (y + d) % 2
  let w := (c + d) % 2; let v := (b + w) % 2
  mul (Fg g x c d t y w) (Fg g a b w t x v)

def pentagonG {R : Type} [CRing R] (g : Sym R) : Prop :=
  ∀ a b c d : Int, (a = 0 ∨ a = 1) → (b = 0 ∨ b = 1) → (c = 0 ∨ c = 1) →
    (d = 0 ∨ d = 1) → pentLhsG g a b c d = pentRhsG g a b c d

-- The invertible-branch condition of the plan, stated generically.
def InvertibleBranch {R : Type} [CRing R] (g : Sym R) : Prop :=
  IsUnit (g 0 0 1) ∧ IsUnit (g 1 0 0) ∧
  mul (g 0 0 1) (g 0 1 1) = one ∧
  mul (g 1 0 0) (g 1 1 0) = one ∧
  g 1 0 1 = mul (g 0 0 1) (g 1 0 0)

-- ---------------------------------------------------------------------------
-- Carrier 1: the Gaussian integers, as an instance rather than as the type.
structure GZ where
  re : Int
  im : Int
  deriving DecidableEq

instance : CRing GZ where
  zero := ⟨0,0⟩
  one  := ⟨1,0⟩
  add z w := ⟨z.re + w.re, z.im + w.im⟩
  neg z := ⟨-z.re, -z.im⟩
  mul z w := ⟨z.re*w.re - z.im*w.im, z.re*w.im + z.im*w.re⟩
  add_assoc := by intro a b c; simp [Int.add_assoc]
  add_comm := by intro a b; simp [Int.add_comm]
  add_zero := by intro a; simp
  add_neg := by
    intro a
    have h : ∀ n : Int, n + -n = 0 := by intro n; omega
    cases a; simp [h]
  mul_assoc := by
    intro a b c; cases a; cases b; cases c
    simp [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub, Int.mul_assoc,
          Int.mul_comm, Int.mul_left_comm, Int.add_assoc, Int.add_comm,
          Int.add_left_comm, Int.neg_mul, Int.mul_neg, Int.sub_eq_add_neg,
          Int.neg_add, Int.neg_neg]
  mul_comm := by
    intro a b; cases a; cases b
    simp [Int.mul_comm, Int.add_comm]
  mul_one := by intro a; cases a; simp
  left_distrib := by
    intro a b c; cases a; cases b; cases c
    simp [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub, Int.mul_assoc,
          Int.mul_comm, Int.mul_left_comm, Int.add_assoc, Int.add_comm,
          Int.add_left_comm, Int.neg_mul, Int.mul_neg, Int.sub_eq_add_neg,
          Int.neg_add, Int.neg_neg]

-- ---------------------------------------------------------------------------
-- Carrier 2: Int itself.
instance : CRing Int where
  zero := 0
  one := 1
  add := (· + ·)
  neg := (- ·)
  mul := (· * ·)
  add_assoc := Int.add_assoc
  add_comm := Int.add_comm
  add_zero := Int.add_zero
  add_neg := by intro a; omega
  mul_assoc := Int.mul_assoc
  mul_comm := Int.mul_comm
  mul_one := Int.mul_one
  left_distrib := Int.mul_add

-- ---------------------------------------------------------------------------
-- Carrier 3: Z/2, as Fin 2 — a ring where the label group and the value ring
-- are the same size.  P2 wants Z/n; this is n = 2.
instance : CRing (Fin 2) where
  zero := 0
  one := 1
  add := (· + ·)
  neg := (- ·)
  mul := (· * ·)
  add_assoc := by decide
  add_comm := by decide
  add_zero := by decide
  add_neg := by decide
  mul_assoc := by decide
  mul_comm := by decide
  mul_one := by decide
  left_distrib := by decide

-- ---------------------------------------------------------------------------
-- Carrier 4: Z/8 — the ring where x^2 = 1 has FOUR roots, which is the exact
-- place the plan predicts the solution set changes shape rather than size.
instance : CRing (Fin 8) where
  zero := 0
  one := 1
  add := (· + ·)
  neg := (- ·)
  mul := (· * ·)
  add_assoc := by decide
  add_comm := by decide
  add_zero := by decide
  add_neg := by decide
  mul_assoc := by decide
  mul_comm := by decide
  mul_one := by decide
  left_distrib := by decide

-- The shape claim, settled by the kernel rather than asserted:
theorem sq_one_Fin2 : (List.filter (fun z : Fin 2 => z * z == 1)
    [0,1]).length = 1 := by decide
theorem sq_one_Fin8 : (List.filter (fun z : Fin 8 => z * z == 1)
    [0,1,2,3,4,5,6,7]).length = 4 := by decide

-- ---------------------------------------------------------------------------
-- Carrier 5: a ring with nilpotents, R[e]/e^2 over Int.  P5b's deformation ring.
structure Dual where
  a : Int
  b : Int
  deriving DecidableEq

instance : CRing Dual where
  zero := ⟨0,0⟩
  one := ⟨1,0⟩
  add z w := ⟨z.a + w.a, z.b + w.b⟩
  neg z := ⟨-z.a, -z.b⟩
  mul z w := ⟨z.a*w.a, z.a*w.b + z.b*w.a⟩
  add_assoc := by intro a b c; simp [Int.add_assoc]
  add_comm := by intro a b; simp [Int.add_comm]
  add_zero := by intro a; simp
  add_neg := by
    intro a
    have h : ∀ n : Int, n + -n = 0 := by intro n; omega
    cases a; simp [h]
  mul_assoc := by
    intro a b c; cases a; cases b; cases c
    simp [Int.add_mul, Int.mul_add, Int.mul_assoc, Int.mul_comm,
          Int.mul_left_comm, Int.add_assoc, Int.add_comm, Int.add_left_comm]
  mul_comm := by
    intro a b; cases a; cases b; simp [Int.mul_comm, Int.add_comm]
  mul_one := by intro a; cases a; simp
  left_distrib := by
    intro a b c; cases a; cases b; cases c
    simp [Int.mul_add, Int.add_assoc, Int.add_comm, Int.add_left_comm]

-- e is nilpotent and non-zero: the carrier is genuinely not a domain.
theorem dual_nilpotent : CRing.mul (⟨0,1⟩ : Dual) ⟨0,1⟩ = CRing.zero := by decide
theorem dual_e_ne_zero : (⟨0,1⟩ : Dual) ≠ CRing.zero := by decide

-- ---------------------------------------------------------------------------
-- The pentagon statement instantiates at every one of them.
example (g : Sym GZ)    : Prop := pentagonG g
example (g : Sym Int)   : Prop := pentagonG g
example (g : Sym (Fin 2)) : Prop := pentagonG g
example (g : Sym (Fin 8)) : Prop := pentagonG g
example (g : Sym Dual)  : Prop := pentagonG g
example (g : Sym GZ)    : Prop := InvertibleBranch g

-- ---------------------------------------------------------------------------
-- The Rat probe lives in rat_probe.lean; Rat is not a core identifier.
