class CRing (R : Type) where
  add : R → R → R
  mul : R → R → R
  neg : R → R
  zer : R
  unit : R
  add_comm  : ∀ a b, add a b = add b a
  add_assoc : ∀ a b c, add (add a b) c = add a (add b c)
  mul_comm  : ∀ a b, mul a b = mul b a
  mul_assoc : ∀ a b c, mul (mul a b) c = mul a (mul b c)
  mul_add   : ∀ a b c, mul a (add b c) = add (mul a b) (mul a c)
  add_zer   : ∀ a, add a zer = a
  mul_unit   : ∀ a, mul a unit = a
  add_neg   : ∀ a, add a (neg a) = zer

structure GZ' (R : Type) where
  re : R
  im : R

variable {R : Type} [C : CRing R]
open CRing

def sub' (a b : R) : R := add a (neg b)
def gmul (z w : GZ' R) : GZ' R :=
  ⟨sub' (mul z.re w.re) (mul z.im w.im), add (mul z.re w.im) (mul z.im w.re)⟩
def gconj (z : GZ' R) : GZ' R := ⟨z.re, neg z.im⟩
def gone : GZ' R := ⟨unit, zer⟩

instance : CRing Int where
  add := Int.add; mul := Int.mul; neg := Int.neg; zer := 0; unit := 1
  add_comm := Int.add_comm; add_assoc := Int.add_assoc
  mul_comm := Int.mul_comm; mul_assoc := Int.mul_assoc
  mul_add := Int.mul_add; add_zer := Int.add_zero
  mul_unit := Int.mul_one; add_neg := by intro a; omega

#check (gmul : GZ' Int → GZ' Int → GZ' Int)
#check (gconj : GZ' Int → GZ' Int)

-- and the ring-generic proof goes through for ANY carrier
theorem gconj_gconj (z : GZ' R) : gconj (gconj z) = z := by
  cases z; simp [gconj]

