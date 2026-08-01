-- what nonlinear Int facts exist in core, with ZERO imports?
#check @Int.mul_eq_zero
#check @Int.mul_self_nonneg
#check @Int.eq_one_of_mul_eq_one_right
#check @Int.mul_le_mul
#check @Int.le_of_mul_le_mul_left
example (a : Int) (h : a * a = 1) : a = 1 ∨ a = -1 := by omega
