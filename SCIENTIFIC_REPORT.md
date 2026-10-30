# Numerical Modelling and Validation of Semiconductor Quantum Wells

## 1. Abstract

This work investigates how well width, finite barrier height, and effective-mass assumptions affect electron states in idealized one-dimensional semiconductor quantum wells. A symmetric tridiagonal finite-difference solver was implemented for infinite and finite constant-mass wells and for a GaAs/Al₀.₃Ga₀.₇As heterostructure using the BenDaniel–Duke (BDD) position-dependent-mass operator. Three independent references separate numerical error from model effects: the continuum and exact discrete infinite-well spectra, constant-mass parity equations, and unequal-mass BDD matching equations. The executed experiments recover the expected inverse-square width scaling, quantify finite-barrier leakage, show meV-scale shifts from the barrier-mass assumption, and distinguish grid error from finite-domain error. For the 8 nm, 0.253 eV baseline, the refined BDD energies are 42.049 and 162.242 meV, differing by 0.069 and 0.244 meV from independent matching values. These are model calculations, not experimental measurements or claims of a new physical effect.

## 2. Introduction and motivation

Quantum confinement links a simple eigenvalue problem to the behavior of nanometre-scale heterostructures. It is also a useful test of scientific software practice: apparently small choices—an infinite instead of finite barrier, a constant instead of discontinuous effective mass, a short computational domain, or a grid that under-resolves an interface—can move predicted levels for different reasons. The objective was therefore not merely to plot wavefunctions, but to construct a calculation whose physical and numerical assumptions can be challenged independently.

## 3. Research questions

1. How accurately does the finite-difference method reproduce known infinite- and finite-well energies?
2. How do finite barriers change levels and spatial probability relative to infinite confinement?
3. What changes when the GaAs well and AlGaAs barrier have different electron effective masses?
4. How much error comes from grid resolution and artificial domain boundaries?
5. How sensitive are the heterostructure predictions to defensible material-parameter alternatives?

## 4. Physical background

For a constant effective mass, the one-dimensional stationary Schrödinger equation is

\[
\left[-\frac{\hbar^2}{2m}\frac{d^2}{dx^2}+V(x)\right]\psi(x)=E\psi(x).
\]

An infinite well of width \(L\) has Dirichlet walls and the exact spectrum

\[
E_n=\frac{n^2\pi^2\hbar^2}{2mL^2},\qquad n=1,2,\ldots.
\]

For a symmetric finite well with \(V=0\) inside \(|x|<a=L/2\) and \(V=V_0\) outside, bound states have \(0<E<V_0\), oscillate in the well, and decay into the barriers. Their nonzero barrier probability is physical penetration; it is not itself a numerical defect.

## 5. Mathematical formulation

For the semiconductor model, the mass varies at the heterointerface. The selected BDD Hamiltonian is

\[
H=-\frac{\hbar^2}{2}\frac{d}{dx}\left[\frac{1}{m^*(x)}\frac{d}{dx}\right]+V(x).
\]

It implies continuity of the envelope \(\psi\) and the flux-related quantity \((1/m^*)\psi'\) across an ideal abrupt interface. A naive expression \(-\hbar^2[2m(x)]^{-1}\psi''\) does not enforce these interface conditions and is not the model used here.

The independent constant-mass reference solves

\[
k\tan(ka)=\kappa\quad(\text{even}),\qquad -k\cot(ka)=\kappa\quad(\text{odd}),
\]

where \(k=\sqrt{2mE}/\hbar\) and \(\kappa=\sqrt{2m(V_0-E)}/\hbar\). The BDD mass-mismatch reference instead solves

\[
\frac{k}{m_w}\tan(ka)=\frac{\kappa}{m_b},\qquad
\frac{k}{m_w}\cot(ka)=-\frac{\kappa}{m_b},
\]

with \(k\) using \(m_w\) and \(\kappa\) using \(m_b\). Branches are bracketed separately and solved with Brent’s method, so a tangent pole cannot be mistaken for a root.

## 6. Numerical methodology

All internal distances are nanometres, energies are electronvolts, and masses are ratios to the free-electron mass. The conversion coefficient \(\hbar^2/(2m_0)\) is calculated from SciPy physical constants rather than hard-coded.

On a uniform grid with spacing \(h\), the divergence-form kinetic operator uses the shared face reciprocal mass

\[
a_{i+1/2}=\tfrac12\left(\frac{1}{m_i^*}+\frac{1}{m_{i+1}^*}\right).
\]

The diagonal and off-diagonal entries are

\[
H_{ii}=\frac{\hbar^2}{2h^2}(a_{i-1/2}+a_{i+1/2})+V_i,
\qquad
H_{i,i+1}=-\frac{\hbar^2}{2h^2}a_{i+1/2}.
\]

Because a face coefficient is shared by both neighboring rows, the real tridiagonal matrix is symmetric by construction. `scipy.linalg.eigh_tridiagonal` computes the requested low states. The returned vectors are rescaled so \(\int|\psi|^2dx=1\), and their sign is fixed deterministically for reproducible output.

## 7. Model assumptions

The baseline is an idealized, undoped, unstrained, symmetric GaAs/Al₀.₃Ga₀.₇As type-I well at low temperature. Energy zero is the GaAs conduction-band minimum. Inputs are \(m_w^*=0.067m_0\), \(m_b^*=0.0919m_0\), and \(V_0=0.253\) eV. Vurgaftman *et al.* provide the low-temperature GaAs and alloy interpolation; combining the interpolated 0.41814 eV gap difference at \(x=0.30\) with Yi *et al.*’s measured \(Q_c=0.604\pm0.02\) gives the selected offset and 0.244–0.261 eV sensitivity interval.

## 8. Validation framework

- **Infinite continuum:** computed values are compared with \(E_n\) at several widths and states.
- **Exact discrete spectrum:** for \(N\) intervals, the centered Dirichlet operator has
  \[
  E_{n,h}=\frac{4}{m^*}\frac{\hbar^2}{2m_0h^2}\sin^2\left(\frac{n\pi}{2N}\right).
  \]
  This isolates matrix assembly/eigensolver correctness from continuum truncation error.
- **Finite wells:** continuum matching equations provide a grid-independent energy reference.
- **State quality:** automated checks cover normalization, quadrature-weighted orthogonality, ordering, endpoint behavior, residuals, Hermiticity, and deterministic reproduction.
- **Bound classification:** \(E<V_0\) is required. Above-barrier matrix states are labeled box-discretized continuum states, not confined levels.
- **Domain diagnosis:** physical outside-well probability is separated from probability in the outer 5% boundary guards.

## 9. Experimental design

| Experiment | Controlled variables | Main output |
|---|---|---|
| Width scaling | \(L=4\ldots20\) nm, fixed mass | energy scaling and analytical error |
| Finite vs infinite | \(L=4,6,8,10\) nm; \(V_0=0.150,0.253,0.400\) eV | shifts, leakage, parity-reference error |
| Effective-mass model | \(L=4\ldots12\) nm; fixed 0.253 eV barrier | constant-mass vs BDD shifts |
| Grid convergence | \(h=0.16\ldots0.01\) nm at fixed 8 nm padding | observed order and matching error |
| Domain convergence | padding 2–12 nm at fixed \(h=0.02\) nm | boundary and energy stabilization |
| Parameter sensitivity | offset 0.244–0.261 eV; alternative temperature-labelled masses | level and leakage changes |

Configurations are encoded in `experiments/run_all.py`; generated CSVs are stored under `results/`.

## 10. Quantitative results

### 10.1 Width scaling and infinite-well accuracy

The fitted ground-state log–log slope was **−2.000000**, matching \(E_1\propto L^{-2}\). Across three states and 4–20 nm widths on 1,201 points, the maximum continuum relative error was **5.14×10⁻⁶**. The numerical values agreed with the exact discrete spectrum to eigensolver precision in automated tests.

### 10.2 Finite versus infinite confinement

For the 8 nm, 0.253 eV constant-mass well:

| State | Infinite (meV) | Finite FD (meV) | Matching (meV) | FD − reference (meV) | Outside probability |
|---:|---:|---:|---:|---:|---:|
| 1 | 87.694 | 45.499 | 45.579 | −0.080 | 5.26% |
| 2 | 350.774 | 169.185 | 169.400 | −0.216 | 26.22% |

The finite barrier lowers the two values by **48.1%** and **51.8%** relative to the infinite approximation. The second state penetrates farther because it lies closer to the barrier.

### 10.3 Effective-mass assumption

| State | Constant-mass FD (meV) | BDD FD (meV) | BDD matching (meV) | BDD − constant (meV) |
|---:|---:|---:|---:|---:|
| 1 | 45.499 | 42.049 | 42.118 | −3.450 |
| 2 | 169.185 | 162.242 | 162.486 | −6.942 |

The heavier AlGaAs barrier mass changes both the decay constant and BDD interface matching. This meV-scale difference is a model effect. The much smaller BDD FD-to-matching differences are numerical errors.

### 10.4 Numerical accuracy

For the BDD ground state at fixed 8 nm padding, reducing \(h\) from 0.16 to 0.01 nm reduced the matching error from **−1.128 to −0.069 meV**. The fitted order from the three finest grids was **1.01**. The centered operator is formally second order in smooth regions, but the abrupt potential/mass profiles and nodal interface placement reduce global energy convergence here. This measured result is reported instead of an assumed order.

At fixed \(h=0.02\) nm, increasing padding from 2 to 12 nm changed the ground energy error from +2.460 to −0.139 meV and reduced boundary-guard probability from **6.43×10⁻⁴ to 9.86×10⁻⁹**. Beyond roughly 6–8 nm, the energy offset no longer improved because grid/interface error, not the distant boundary, dominated.

### 10.5 Material-parameter sensitivity

| Scenario | E₁ (meV) | E₂ (meV) | leakage₁ | leakage₂ |
|---|---:|---:|---:|---:|
| offset 0.244 eV | 41.574 | 160.053 | 5.38% | 24.86% |
| baseline 0.253 eV | 42.049 | 162.242 | 5.18% | 23.80% |
| offset 0.261 eV | 42.456 | 164.111 | 5.01% | 22.92% |
| 300 K-inspired masses, same offset | 43.664 | 168.206 | 5.51% | 25.50% |

The offset interval changes the ground level by 0.882 meV and the excited level by 4.057 meV across its endpoints. The alternative masses produce larger shifts, but that row is a labelled assumption comparison—not a complete finite-temperature device model.

## 11. Discussion

The experiments answer the central question in layers. Width has the strongest systematic effect through inverse-square kinetic scaling. Finite barriers substantially lower the infinite-well levels and create spatial leakage. Barrier-mass mismatch adds a smaller but resolved meV-scale correction. Independent roots then show how much of each reported FD value remains attributable to discretization.

The domain study also demonstrates why “more padding” and “finer grid” are not interchangeable. A sufficiently large domain suppresses the artificial wall, but cannot fix an under-resolved abrupt interface. Conversely, a very fine short domain still perturbs a slowly decaying near-threshold state.

## 12. Limitations

The BDD one-band envelope model is a useful low-energy approximation, not an atomistic or universally unique position-dependent-mass theory. The calculation omits nonparabolic energy-dependent mass, multiband coupling, strain, alloy disorder, interface roughness/interdiffusion, atomistic bonding, dopants, Schrödinger–Poisson self-consistency, carrier interactions, and detailed temperature dependence. Bulk parameters are applied to an ideal abrupt structure. Near-threshold states are especially sensitive to interface placement, grid spacing, and domain length; the broad experiment tables include larger errors for such states than the well-resolved 8 nm baseline.

## 13. Conclusions

The project reproduced analytical infinite-well behavior, validated finite and mass-mismatched wells against separate continuum matching calculations, and quantified both physical-model and numerical differences. For the representative 8 nm structure, finite barriers change energies by tens to hundreds of meV relative to the infinite approximation, barrier-mass mismatch changes them by several meV, and the refined BDD discretization is within sub-meV error of matching roots. The calculation supports careful comparison of idealized models; it does not establish an experimental device spectrum.

## 14. Future directions

Useful extensions include interface-fitted finite-volume grids or Richardson extrapolation, energy-dependent/nonparabolic mass, coupled-band \(k\cdot p\) models, self-consistent Schrödinger–Poisson electrostatics, and comparison with a specifically documented experimental heterostructure. Each would require its own independent validation.

## 15. References

1. D. J. BenDaniel and C. B. Duke, “Space-Charge Effects on Electron Tunneling,” *Physical Review* 152, 683 (1966). <https://doi.org/10.1103/PhysRev.152.683>
2. I. Vurgaftman, J. R. Meyer, and L. R. Ram-Mohan, “Band parameters for III–V compound semiconductors and their alloys,” *Journal of Applied Physics* 89, 5815 (2001). <https://doi.org/10.1063/1.1368156>
3. W. Yi et al., *Applied Physics Letters* 95, 112102 (2009). <https://doi.org/10.1063/1.3224914>
4. M. G. Burt, “The justification for applying the effective-mass approximation to microstructures,” *Physical Review B* 50, 7518 (1994). <https://doi.org/10.1103/PhysRevB.50.7518>
5. B. A. Foreman, “Effective-mass Hamiltonian and boundary conditions for the valence bands of semiconductor microstructures,” *Physical Review B* 52, 12241 (1995). <https://doi.org/10.1103/PhysRevB.52.12241>
6. MIT OpenCourseWare, *Quantum Physics I*, Lecture 11. <https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf>
7. Caltech Physics 12b, finite square-well notes. <https://www.preskill.caltech.edu/ph12b/Ph12b-finite-well-4mar2010.pdf>
8. SciPy documentation, `eigh_tridiagonal` and `brentq`. <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html>, <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html>
9. NumPy documentation, `trapezoid`. <https://numpy.org/doc/stable/reference/generated/numpy.trapezoid.html>
