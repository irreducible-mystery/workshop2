-- Can a compiler-only definition reach a kernel-checked proof?
unsafe def cheat : Nat := 0
theorem uses_it : cheat = 0 := rfl
