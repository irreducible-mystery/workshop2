-- QUESTION 2: can core Lean express a RING-GENERIC carrier, with zero imports?
-- If yes, "vary the ring" is a parameter rather than a rewrite.

class CRing (R : Type) extends Add R, Mul R, Neg R, Sub R, OfNat R 0, OfNat R 1 where
  add_comm  : ∀ a b : R, a + b = b + a
  add_assoc : ∀ a b c : R, a + b + c = a + (b + c)
  mul_comm  : ∀ a b : R, a * b = b * a
  mul_assoc : ∀ a b c : R, a * b * c = a * (b * c)
  mul_add   : ∀ a b c : R, a * (b + c) = a * b + a * c
  add_zero  : ∀ a : R, a + 0 = a
  mul_one   : ∀ a : R, a * 1 = a
  add_neg   : ∀ a : R, a + -a = 0
  sub_eq    : ∀ a b : R, a - b = a + -b

structure GZ' (R : Type) where
  re : R
  im : R

variable {R : Type} [CRing R]

def mul' (z w : GZ' R) : GZ' R :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def conj' (z : GZ' R) : GZ' R := ⟨z.re, -z.im⟩
def one' : GZ' R := ⟨1, 0⟩

-- Int is an instance, so nothing already proved is lost
instance : CRing Int where
  add_comm := Int.add_comm; add_assoc := Int.add_assoc
  mul_comm := Int.mul_comm; mul_assoc := Int.mul_assoc
  mul_add := Int.mul_add;   add_zero := Int.add_zero
  mul_one := Int.mul_one;   add_neg := by intro a; omega
  sub_eq := by intro a b; omega

#check (mul' : GZ' Int → GZ' Int → GZ' Int)
