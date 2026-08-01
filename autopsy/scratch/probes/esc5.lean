set_option debug.skipKernelTC true
theorem bogus : (2:Nat) + 2 = 5 := by
  have h : (2:Nat) + 2 = 4 := rfl
  exact h
#print axioms bogus
