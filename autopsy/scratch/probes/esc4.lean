opaque hidden : Nat
#print axioms hidden
axiom planted : (2:Nat) + 2 = 5
theorem uses_axiom : (2:Nat) + 2 = 5 := planted
#print axioms uses_axiom
theorem uses_sorry : (1:Nat) = 1 := by sorry
#print axioms uses_sorry
theorem uses_native : (2:Nat) + 2 = 4 := by native_decide
#print axioms uses_native
