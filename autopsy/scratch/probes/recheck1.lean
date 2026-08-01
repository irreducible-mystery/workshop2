-- Recheck 1: the structural fact about conj and Fs.
structure GZ where
  re : Int
  im : Int
  deriving DecidableEq

def zero : GZ := ⟨0, 0⟩
def one  : GZ := ⟨1, 0⟩

def neg (z : GZ) : GZ := ⟨-z.re, -z.im⟩
def mul (z w : GZ) : GZ :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
def conj (z : GZ) : GZ := ⟨z.re, -z.im⟩

def Fs (f : GZ) (a b c d x y : Int) : GZ :=
  if x = (a + b) % 2 ∧ y = (b + c) % 2 ∧ d = (a + b + c) % 2 then
    (if a = 1 ∧ b = 1 ∧ c = 1 then f else one)
  else zero

-- conj is trivial on the two constants the gate can return.
theorem conj_zero : conj zero = zero := by decide
theorem conj_one  : conj one  = one  := by decide

-- The structural fact, for every f and every index tuple, with no side conditions.
theorem conj_Fs (f : GZ) (a b c d x y : Int) :
    conj (Fs f a b c d x y) = Fs (conj f) a b c d x y := by
  unfold Fs
  by_cases h : x = (a + b) % 2 ∧ y = (b + c) % 2 ∧ d = (a + b + c) % 2
  · rw [if_pos h, if_pos h]
    by_cases k : a = 1 ∧ b = 1 ∧ c = 1
    · rw [if_pos k, if_pos k]
    · rw [if_neg k, if_neg k]; exact conj_one
  · rw [if_neg h, if_neg h]; exact conj_zero

-- Negative control on the same shape: conj does NOT commute past mul's first
-- argument alone.  If this were provable the theorem above would be vacuous
-- in the sense that everything commutes with conj.
theorem conj_not_free : conj (mul ⟨0,1⟩ ⟨0,1⟩) ≠ mul (conj ⟨0,1⟩) ⟨0,1⟩ := by decide

-- Live-instance witness: Fs genuinely returns f somewhere, so conj_Fs is not
-- a statement only about constants.
theorem Fs_hits_f (f : GZ) : Fs f 1 1 1 1 0 0 = f := by
  unfold Fs
  rw [if_pos (by decide : (0:Int) = (1 + 1) % 2 ∧ (0:Int) = (1 + 1) % 2 ∧
                          (1:Int) = (1 + 1 + 1) % 2)]
  rw [if_pos (by decide : (1:Int) = 1 ∧ (1:Int) = 1 ∧ (1:Int) = 1)]

#print axioms conj_Fs
#print axioms conj_not_free
#print axioms Fs_hits_f
