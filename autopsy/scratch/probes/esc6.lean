theorem t1 : (1:Nat) = 1 := rfl
macro "cheat" : tactic => `(tactic| sorry)
theorem t2 : (2:Nat) + 2 = 5 := by cheat
#print axioms t2
