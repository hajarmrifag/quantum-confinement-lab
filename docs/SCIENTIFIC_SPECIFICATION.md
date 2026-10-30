# Scientific specification

This document fixes the theory and inputs before interpreting the advanced model. The longer research synthesis is retained in `reports/Quantum well scientific foundations.md`; source notes are under `research_notes/`.

## Coordinate and energy conventions

- One spatial dimension; symmetric well centered at `x = 0`.
- Width `L`; half-width `a = L/2`.
- Energy zero at the well conduction-band edge.
- Finite barriers have `V(x)=V0` outside the nominal well.
- Internal distance unit: nm. Internal energy unit: eV. Effective masses are ratios to `m0`.
- Dirichlet endpoints are artificial computational boundaries for finite wells and must be separated from the physical interface.

## Model definitions

### A. Infinite square well

Constant mass, `V=0` between hard walls, and `ψ=0` at the walls. Validate against both the continuum spectrum and exact centered-difference spectrum.

### B. Finite square well

Constant mass across well and barriers. A state is physically bound only if `0 < E < V0`; matrix states above the barrier are discretized continuum states. Validate against parity-resolved continuum matching roots and test exterior-domain sensitivity.

### C. GaAs/AlGaAs heterostructure

Use the BenDaniel–Duke divergence operator

`H = -(ℏ²/2) d/dx [(1/m*(x)) d/dx] + V(x)`.

Discretize with one reciprocal-mass coefficient shared by each face. This makes the tridiagonal Hamiltonian explicitly symmetric and corresponds to continuity of `ψ` and `(1/m*)ψ'` at an ideal abrupt interface. Validate against independent unequal-mass parity equations.

## Baseline material inputs

| Quantity | Baseline | Rationale |
|---|---:|---|
| structure | GaAs/Al₀.₃Ga₀.₇As | direct-gap Γ-valley regime at low temperature |
| well mass | 0.067 m₀ | Vurgaftman et al. GaAs recommendation |
| barrier mass | 0.0919 m₀ | zero-bowing interpolation at x=0.30 |
| Γ gap difference | 0.41814 eV | Vurgaftman alloy interpolation |
| conduction offset fraction | 0.604 ± 0.02 | Yi et al. 4.2 K measurement |
| barrier | 0.253 eV | 0.604 × 0.41814 eV, rounded |
| sensitivity interval | 0.244–0.261 eV | propagation of quoted offset-fraction range only |

The interval is an assumption sensitivity, not a device confidence interval. A separate row using masses `0.063/0.0879 m₀` is labelled “300 K-inspired”; it is not mixed with the low-temperature baseline.

## Required diagnostics

1. spatial normalization and quadrature-weighted orthogonality;
2. ascending eigenvalues and zero endpoint values;
3. relative eigenpair residual;
4. exact matrix symmetry;
5. analytical/reference energy error;
6. physical outside-well probability;
7. outer boundary-guard probability;
8. grid refinement at a fixed domain;
9. domain growth at fixed spacing.

## Claim boundary

The model compares idealized confinement assumptions. It does not include nonparabolicity, multiband coupling, strain, alloy disorder, interface roughness, atomistic bonding, dopants, self-consistent electrostatics, carrier interactions, or full temperature dependence. It is not an experimental validation or original physical discovery.
