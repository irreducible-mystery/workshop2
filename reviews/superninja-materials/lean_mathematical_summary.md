================================================================================
CLEAN MATHEMATICAL SUMMARY
Extracted from Lean formalizations
================================================================================


## TransferWord.lean
----------------------------------------

### Structures:
  - M2

### Theorems:
  - det_T
  - det_mul
  - cayley_hamilton
  - transfer_satisfies_gap
  - p_step
  - Tpow_closed
  - det_Tpow
  - word_det
  - word_trace

### Definitions:
  - mmul
  - tr
  - det
  - idM
  - smul
  - sub
  - T
  - p
  - Tpow
  - word

## Branch.lean
----------------------------------------

### Theorems:
  - disc_zero_iff
  - double_root_at_branch
  - real_root_iff
  - no_real_root_below
  - sPlus_is_root
  - sPlus_one
  - golden_identity
  - sPlus_branch

### Definitions:
  - sPlus

## Casoratian.lean
----------------------------------------

### Theorems:
  - catalan_gf_is_root
  - catalan_radius
  - catalan_at_radius

### Definitions:
  - Obeys
  - W

## Golden.lean
----------------------------------------

### Structures:
  - Dual

### Theorems:
  - sqrt5_irrational
  - sPlus_one_irrational
  - sPlus_branch_rational
  - nilpotent_solution_at_branch

### Definitions:
  - sPlus
  - dmul
  - dadd
  - dconst

## Modulus.lean
----------------------------------------

### Theorems:
  - conj_root
  - normSq_eq_neg_gap
  - modulus_below_branch
  - gap_neg_one_cube
  - gap_neg_one_sixth
  - gap_neg_one_unit_modulus

## GeneralCeiling.lean
----------------------------------------

### Theorems:
  - bound_nonneg
  - run_le_bound
  - const_attains
  - geometric_solution

### Definitions:
  - bound
  - run
  - Mags

## ArtinSchreier.lean
----------------------------------------

### Theorems:
  - all_complete
  - F4_units
  - phi_additive
  - phi_kernel
  - half_reachable
  - two_roots_each
  - no_double_root
  - unreachable

### Definitions:
  - all
  - add
  - mul
  - phi

## ThermodynamicGap_Basic.lean
----------------------------------------

### Structures:
  - GapProbability

### Theorems:
  - collision_max_entropy
  - phase_transition_structure
  - spontaneous_symmetry_breaking
  - critical_exponent_energy
  - first_order_phase_transition
  - critical_universality

### Definitions:
  - collisionState
  - orderParameter
  - energy
  - energy_diff

## ShadowPatternTheorems.lean
----------------------------------------

### Structures:
  - ShadowPattern
  - OscillatoryPattern
  - FractalPattern
  - ConstantBasedPattern
  - MasterPattern
  - all_shadows
  - GenerativeRule
  - GenerativeSystem
  - DivinePattern

### Theorems:
  - arithmetic_pattern_verified
  - arithmetic_pattern_padic_connection
  - shadows_not_random
  - complete_generative_pattern
  - pattern_classification
  - pattern_uniqueness

### Definitions:
  - arithmetic_pattern
  - quadratic_pattern
  - find_quadratic_parameters
  - correlation_as_oscillation
  - self_similar_transformation
  - iterate_fractal
  - fundamental_constants
  - basic_operations
  - generate_from_constants
  - geometric_pattern
  - test_geometric_pattern
  - basic_generative_rules
  - generate_from_system
  - analyze_distance_pattern

## ToposGap.lean
----------------------------------------

### Theorems:
  - topos_internal_logic
  - sheaf_cohomology_obstruction
  - effective_topos_gap
  - synthetic_differential_gap
  - topos_decidability
  - locale_gap_map
  - presheaf_gap_model
  - topos_independence

### Definitions:
  - gapSheaf
  - gapToposComparison

## NoncommutativeGap.lean
----------------------------------------

### Theorems:
  - quantum_max_entropy
  - noncommutative_torus_connection
  - noncommutative_ktheory

### Definitions:
  - matrixGap
  - quantumGapProbability
  - quantumGapEntropy

## Characteristic.lean
----------------------------------------

### Theorems:
  - disc_vanishes_char5
  - golden_is_double_root_char5
  - char5_root_count
  - disc_vanishes_char3
  - neg_one_is_double_root_char3
  - four_is_sqrt_neg_one_char17
  - sixteen_is_neg_one_char17
  - disc_vanishes_char17
  - i_is_double_root_char17
  - thirteen_is_sqrt_neg_one_char17
  - disc_nonzero_at_minus_i_char17
  - minus_i_splits_char17
  - char2_additive
  - char2_only_zero_gap_reachable
  - char2_reachable_gap_has_two_roots
  - char7_golden_has_no_roots
  - char7_disc_nonzero

## CrossFrameworkTheorems.lean
----------------------------------------

### Theorems:
  - Category_Homotopy_Equivalence
  - Category_Thermodynamic_Equivalence
  - Homotopy_Thermodynamic_Equivalence
  - Quantum_Classical_Equivalence
  - Topos_Model_Equivalence
  - Six_Framework_Convergence
  - Universal_Property_All_Frameworks
  - Framework_Adjointness
  - Algorithm_Equivalence

### Definitions:
  - G_critical
  - CategoryFramework
  - HomotopyFramework
  - ThermodynamicFramework
  - NoncommutativeFramework
  - ToposFramework
  - ModelFramework
  - CategoryToHomotopyFunctor
  - HomotopyToThermoFunctor
  - ThermoToQuantumFunctor
  - GAPStructurePreservingNatTrans
  - category_theory_algorithm
  - homotopy_theory_algorithm
  - thermodynamic_algorithm
  - quantum_algorithm
  - topos_algorithm
  - model_theoretic_algorithm
  - verify_cross_framework_convergence

## Reflexive.lean
----------------------------------------

### Theorems:
  - gap_is_own_root
  - no_gap_equals_discriminant
  - branch_point_not_integral
  - collision_root_not_integral
  - five_not_square

### Definitions:
  - IsRoot

## ModelGap.lean
----------------------------------------

### Structures:
  - GapModel

### Theorems:
  - gap_model_completeness
  - gap_quantifier_elimination
  - gap_o_minimality
  - gap_categoricity
  - gap_decidability
  - gap_compactness
  - gap_interpolation
  - gap_forcing
  - gap_definable_sets
  - gap_atomic_models

### Definitions:
  - GapTheory
  - GapType

## HomotopyGap_CompleteFull.lean
----------------------------------------

### Theorems:
  - real_solution_components
  - complex_solution_components
  - parameter_space_fundamental_group
  - monodromy_from_homotopy
  - gap_two_sheets
  - gap_deck_transformations
  - higher_homotopy_vanish
  - euler_characteristic_formula
  - monodromy_exchange
  - covering_map_property
  - branch_point_analysis
  - solution_space_topology
  - fundamental_group_action
  - universal_covering_space
  - monodromy_representation
  - riemann_surface_structure
  - analytic_continuation
  - covering_transformation
  - local_trivialization
  - fiber_isomorphism
  - path_lifting_property
  - homotopy_lifting_property

### Definitions:
  - solutionSpace
  - gapCoveringSpace
  - gapEulerCharacteristic

## ExplicitShadowCasting.lean
----------------------------------------

### Structures:
  - GapEquationUniverse
  - ShadowCastingFunctor
  - MasterCastingObject

### Theorems:
  - universal_object_minus_one_quarter
  - solution_collapse_at_critical_point
  - G_projection_domain
  - variety_smoothness
  - critical_point_dynamics
  - characteristic_polynomial_is_gap
  - critical_eigenvalue_structure
  - unification_of_constructions

### Definitions:
  - GapEquationCat
  - universal_gap_object
  - ShadowCastingVariety
  - project_to_G
  - project_to_𝕩
  - quadratic_dynamics
  - gap_vector_field
  - fixed_points
  - linearization
  - gap_matrix
  - characteristic_poly
  - eigenvalues
  - GapEquationScheme

## CategoryGap.lean
----------------------------------------

### Theorems:
  - gap_preserve_id

### Definitions:
  - gapStructure
  - gapHom_id

## CategoryGap_Basic.lean
----------------------------------------

### Theorems:
  - gap_preserve_id

### Definitions:
  - gapStructure
  - gapSolutions

## InfiniteAscent.lean
----------------------------------------

### Structures:
  - Foundation
  - SelfCausing
  - CompletionGaps
  - CausalStructure
  - ExplanationSystem

### Theorems:
  - foundation_paradox
  - bootstrap_necessity
  - infinite_ascent_lemma
  - non_well_founded_infinite_ascent
  - completeness_infinite_expansion
  - reality_bootstrap

## HomotopyGap_Proofs.lean
----------------------------------------

### Theorems:
  - real_solution_solutions
  - parameter_space_fundamental_group
  - two_sheeted_structure
  - monodromy_exchange
  - deck_transformations_z2

## Shape.lean
----------------------------------------

### Theorems:
  - sq_one_Fin2
  - sq_one_Fin3
  - sq_one_Fin8
  - gap_root_counts_Fin8
  - gap_never_exceeds_degree_Fin8
  - half_the_gaps_reachable_Fin8

### Definitions:
  - IsRoot
  - gapRoots8

## Vieta.lean
----------------------------------------

### Definitions:
  - IsRoot

## ShadowCastingObject.lean
----------------------------------------

### Structures:
  - Shadow
  - ShadowCastingObject
  - GAPShadowObject
  - ShadowNetwork
  - HigherDimensionalObject
  - Superobject

### Theorems:
  - shadow_as_projection
  - p_adic_shadows_arithmetic_progression
  - shadows_as_special_curve_points
  - super_critical_exists
  - shadow_network_structure
  - verified_arithmetic_progression
  - identify_shadow_object
  - super_critical_exists_conjecture
  - shadow_network_topology
  - higher_dimensional_conjecture

### Definitions:
  - SpecialCurve
  - SuperCriticalParameter
  - GAPShadowNetwork

## Ceiling.lean
----------------------------------------

### Theorems:
  - step_bound
  - step_tight
  - fib_step
  - run_zero
  - run_succ
  - run_bound
  - plus_is_fib
  - ceiling_sharp
  - plus_is_signs

### Definitions:
  - fib
  - run
  - Signs
  - plus

## HomotopyGap_Basic.lean
----------------------------------------

### Theorems:
  - branch_point_detection
  - two_sheeted_structure
  - monodromy_exchange
  - deck_transformations_z2
  - higher_homotopy_vanish
  - topology_change
  - realline_removed_point_fundamental

### Definitions:
  - solutionSpace

## ThermodynamicGap_CompleteFull.lean
----------------------------------------

### Structures:
  - GapProbabilitySpace
  - CollisionState

### Theorems:
  - collision_max_entropy
  - entropy_phase_transition
  - spontaneous_symmetry_breaking
  - critical_exponent_analysis
  - partition_function_zeros
  - free_energy_landscape
  - correlation_length
  - renormalization_group
  - critical_opalescence
  - order_parameter_proof
  - susceptibility_proof
  - specific_heat_proof
  - fluctuation_dissipation
  - lee_yang_theorem
  - universality_class

### Definitions:
  - gapEntropy

## HomotopyGap_Complete.lean
----------------------------------------

### Theorems:
  - real_solution_analysis
  - parameter_space_fundamental_group_complete
  - two_sheeted_structure_complete
  - monodromy_exchange_complete
  - deck_transformations_z2_complete

## Quadratic.lean
----------------------------------------

### Structures:
  - H

### Theorems:
  - hmul_self
  - factor
  - i_never_solves

### Definitions:
  - hmul
  - hone
  - hadd
  - hsmul

## Tropical.lean
----------------------------------------

### Theorems:
  - tropical_solutions
  - tropical_witness_nonpos
  - tropical_witness_pos

## HomotopyGap.lean
----------------------------------------

### Theorems:
  - real_solution_components
  - complex_solution_components
  - parameter_space_fundamental_group
  - monodromy_from_homotopy
  - gap_two_sheets
  - gap_deck_transformations
  - higher_homotopy_vanish
  - euler_characteristic_formula
  - cohomology_calculation
  - obstruction_detected_at_collision
  - fiber_is_two_points
  - branch_point_homotopy_detection
  - chirality_from_homotopy

### Definitions:
  - solutionSpace
  - gapFundamentalGroup
  - gapCoveringSpace
  - gapEulerCharacteristic
  - gapBettiNumbers
  - gapSingularCohomology
  - gapSingularHomology
  - gapObstruction
  - gapFiberBundle

## ThermodynamicGap.lean
----------------------------------------

### Structures:
  - GapProbabilitySpace

### Theorems:
  - probabilities_normalize
  - thermodynamic_identity
  - collision_max_entropy
  - entropy_phase_transition
  - first_order_phase_transition
  - critical_exponent_energy
  - spontaneous_symmetry_breaking
  - specific_heat_divergence
  - ising_universality
  - rg_fixed_point_theorem
  - thermodynamic_foundation

### Definitions:
  - energy
  - partitionFunction
  - probability₁
  - probability₂
  - freeEnergy
  - entropy
  - averageEnergy
  - collisionState
  - orderParameter
  - specificHeat
  - susceptibility
  - correlationFunction
  - rgFixedPoint

## Schedules.lean
----------------------------------------

### Theorems:
  - run_succ
  - minus_period_six
  - minus_orbit
  - minus_shift
  - minus_bounded
  - alternation_is_golden
  - alt_char_poly

### Definitions:
  - run
  - minus
  - altTrace
  - altDet

## SuperCriticalPoint.lean
----------------------------------------

### Structures:
  - UniversalFramework

### Theorems:
  - intersection_conventional_frameworks

### Definitions:
  - FrameworkIdentifier
  - conventional_frameworks
  - framework_convergence_conventional
  - p_adic_framework
  - modular_framework
  - transcendental_framework
  - intersection_super_critical
  - majority_vote_super_critical
  - count_votes
  - weighted_consensus
  - find_special
  - harmonic_mean_super_critical
  - find_all_special_values
  - all_possible_frameworks
  - sequential_illumination
  - shadow_projection_union
  - meta_framework
  - appears_in_multiple_frameworks
  - part_of_meaningful_structure
  - connected_to_fundamental_constants
  - experimental_super_critical

## ThermodynamicGap_Proofs.lean
----------------------------------------

### Theorems:
  - collision_max_entropy
  - entropy_phase_analysis
  - spontaneous_symmetry_breaking
  - first_order_phase_transition
  - critical_exponent_energy