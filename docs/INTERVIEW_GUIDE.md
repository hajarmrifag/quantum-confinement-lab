# Interview study guide

## The problem in one minute

The project asks how an electron’s allowed energies and spatial distribution change when it is confined in an idealized semiconductor quantum well. Three models isolate different assumptions. The infinite well gives a clean analytical benchmark. The finite well allows the wavefunction to penetrate a barrier. The GaAs/AlGaAs model also lets the electron effective mass change between materials and uses the BenDaniel–Duke (BDD) kinetic operator to preserve the appropriate interface flux condition.

The code discretizes the one-dimensional Hamiltonian as a real symmetric tridiagonal matrix, computes its low eigenpairs, normalizes each wavefunction in physical space, classifies only `E < V0` states as bound, and checks the answers against calculations that do not use the grid.

## Equations to understand

### Schrödinger eigenproblem

\[
H\psi=E\psi.
\]

`E` is an allowed energy and `ψ(x)` is the corresponding envelope wavefunction. `|ψ|² dx` is the probability of finding the electron in a small interval `dx`.

### Infinite well

\[
E_n=\frac{n^2\pi^2\hbar^2}{2mL^2}.
\]

Remember the scaling: energy grows as `n²`, decreases as `1/L²`, and decreases as `1/m`.

### Finite well

Inside the well, a bound state oscillates with `k = sqrt(2mE)/ℏ`. In the barrier it decays with `κ = sqrt(2m(V0−E))/ℏ`. Matching the two solutions gives even and odd transcendental equations. The project solves each branch with a bracketed root finder.

### Position-dependent mass

\[
H=-\frac{\hbar^2}{2}\frac{d}{dx}\left(\frac{1}{m^*(x)}\frac{d}{dx}\right)+V.
\]

At the interface, BDD matching keeps `ψ` and `(1/m*)ψ'` continuous. The latter is related to probability current. The discrete operator shares one reciprocal-mass coefficient between neighboring rows, making the matrix explicitly symmetric.

## What the program actually calculates

1. Construct a uniform spatial grid and material profiles `V(x)` and `m*(x)`.
2. Exclude the two Dirichlet endpoints from the unknown vector.
3. Assemble the main and off diagonals of the Hamiltonian.
4. Use SciPy’s symmetric tridiagonal eigensolver for the lowest requested states.
5. Restore zero endpoints and normalize with numerical integration.
6. Calculate leakage, boundary-guard probability, overlaps, residuals, and reference errors.
7. Repeat across controlled widths, barriers, masses, grid spacings, and domain sizes.

## Main findings to remember

- The infinite-well ground-state fit was `E ∝ L^-2.000000`.
- At 8 nm, the infinite-well energies were 87.694 and 350.774 meV.
- With a finite 0.253 eV barrier and constant mass, they became 45.499 and 169.185 meV; probability outside the nominal well was 5.26% and 26.22%.
- With the GaAs/AlGaAs BDD mass profile, they became 42.049 and 162.242 meV.
- Independent unequal-mass matching gave 42.118 and 162.486 meV, so the refined FD errors were −0.069 and −0.244 meV.
- The abrupt profiles showed about first-order global energy convergence in the tested nodal discretization, even though the centered stencil is second order in smooth regions.
- Increasing padding suppressed the artificial boundary probability; it did not remove the remaining grid/interface error.

## Limitations you should volunteer

This is a 1D, one-band envelope-function calculation for an ideal, abrupt, unstrained structure. It does not include nonparabolicity, valence-band or multiband coupling, strain, alloy disorder, interface roughness, atomistic bonds, dopants, self-consistent electrostatics, carrier interactions, or a full temperature model. BDD is a standard low-energy ordering, not a claim that all position-dependent-mass quantum theories are equivalent. Material inputs are literature-supported approximations, not universal constants.

## Possible interview questions and answers

### 1. Why does an infinite well have discrete energies?

The wavefunction must vanish at both walls. Only sinusoidal waves containing an integer number of half-wavelengths satisfy both boundary conditions. That restricts the allowed wave numbers to `k=nπ/L`, and the kinetic energy is proportional to `k²`.

### 2. Why does the energy scale as inverse width squared?

Confinement sets a characteristic wave number of order `1/L`. Kinetic energy is `ℏ²k²/(2m)`, so it scales as `1/L²`. The numerical log–log fit recovered a slope of −2.

### 3. Why are finite-well energies lower than infinite-well energies?

A finite barrier lets the wavefunction extend beyond the nominal width. The effective spatial extent is larger, which reduces its curvature and kinetic energy. The difference is a physical consequence of the changed boundary model, not merely numerical error.

### 4. What does probability leakage mean here?

It is the integral of `|ψ|²` outside the nominal well but inside the computational domain. For a bound state it represents evanescent penetration into the barrier. It should not be confused with probability near the artificial outer boundaries, which is a numerical-domain diagnostic.

### 5. How do you know a returned matrix eigenstate is bound?

Its energy must lie below the barrier, it must be localized near the well, and it should remain stable as the outer domain grows. A finite Dirichlet box also discretizes above-barrier continuum waves, so a discrete matrix eigenvalue alone is not enough.

### 6. Why is the ordinary variable-prefactor Laplacian inadequate?

Writing `-(ℏ²/2m(x))ψ''` does not generally give the BDD divergence operator and does not enforce continuity of `(1/m*)ψ'`. The divergence form makes current conservation and Hermiticity explicit at a mass discontinuity.

### 7. What does Hermitian mean numerically, and why does it matter?

For this real discretization it means the Hamiltonian matrix equals its transpose. Hermiticity gives real eigenvalues and orthogonal eigenvectors. The code uses exactly the same face coefficient for `H[i,i+1]` and `H[i+1,i]`, then tests equality directly.

### 8. How is the finite-well result validated independently?

The reference calculation solves the continuum even/odd matching equations with branch-safe Brent root finding. It never constructs the finite-difference matrix, so agreement is evidence against errors specific to the grid assembly.

### 9. Why compare with the exact discrete infinite-well spectrum as well as the continuum formula?

The exact discrete formula tests whether the matrix and eigensolver implement the intended finite-difference operator. The continuum formula measures the approximation error of that operator. Without both checks, an assembly error and a discretization error can be confused.

### 10. Why was the observed convergence close to first rather than second order?

The centered second derivative is second order where the coefficients and solution are smooth. An abrupt potential and mass introduce nonsmooth interfaces, and their placement on a nodal grid changes slightly under refinement. In this experiment the energy error decreased approximately linearly with `h`; the report measures that behavior instead of assuming the smooth-problem rate.

### 11. What is the significance of the barrier effective mass?

It changes the decay behavior in the barrier and the derivative matching condition. For the 8 nm baseline, using the AlGaAs barrier mass lowered the two computed energies by about 3.45 and 6.94 meV relative to a constant `0.067m0` mass calculation.

### 12. Where did the 0.253 eV barrier come from?

Vurgaftman’s low-temperature parameter interpolation gives a Γ-gap difference of about 0.41814 eV at Al fraction 0.30. Yi and colleagues measured a conduction-band offset fraction `Qc=0.604±0.02`. Their product is 0.25256 eV, rounded to 0.253 eV. The quoted fraction range motivates 0.244–0.261 eV sensitivity cases.

### 13. Does agreement with the matching equations prove the model is physically exact?

No. It shows that the numerical solution correctly approximates the selected continuum model. Both can still omit real physics such as nonparabolicity, interface roughness, strain, or many-body effects. Numerical validation and physical-model validation are different claims.

### 14. What would you improve next?

First I would use an interface-fitted finite-volume grid or extrapolation to reduce the first-order interface error. Then I would add a carefully validated nonparabolic or multiband model. For a specific device, I would include self-consistent electrostatics and compare against documented experimental data.

### 15. What did you learn as a software engineering student?

The main lesson was to design separate failure detectors. Unit tests alone do not establish physical validity. Exact discrete eigenvalues test implementation; analytical matching tests the continuum approximation; grid and domain studies test numerical limits; and parameter sensitivity tests how much the conclusion depends on inputs.
