# GaAs AlGaAs material parameters and scientific software

## Which well/barrier electron effective masses and conduction-band offsets are defensible for a stated Al fraction and temperature?

### Takeaway
A coherent baseline is an idealized, unstrained GaAs/Al\(_{0.30}\)Ga\(_{0.70}\)As well at low temperature (nominally 0 K material interpolation, compared with a 4.2 K band-offset measurement): \(m_w^*=0.067m_0\), \(m_b^*=0.0919m_0\), and a \(\Gamma\)-conduction-band barrier \(V_0\approx0.253\) eV. The barrier alloy remains on the direct-gap side of the low-temperature \(\Gamma\)-to-X crossover, so a single-\(\Gamma\)-valley effective-mass model is defensible at \(x=0.30\).

### Cited Findings
- Vurgaftman, Meyer, and Ram-Mohan's peer-reviewed compilation recommends, at 0 K, \(E_g^\Gamma=1.519\) eV and \(m_e^\Gamma=0.067m_0\) for GaAs; it gives the measured mass ranges as 0.065–0.070 at 0 K and 0.0635–0.067 at 300 K (Table I, p. 5825). — [Vurgaftman et al., *J. Appl. Phys.* 89, 5815 (2001), DOI 10.1063/1.1368156](https://doi.org/10.1063/1.1368156); [accessible PDF, Table I](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)
- The same compilation recommends for AlAs \(E_g^\Gamma=3.099\) eV and \(m_e^\Gamma=0.15m_0\) (Table II, p. 5826). It notes that the AlAs \(\Gamma\)-mass is difficult to measure and that 0.15 is supported by AlGaAs extrapolations and calculations, while the reported range extends down to 0.06. — [Vurgaftman et al., Table II and discussion](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)
- For a ternary \(A_{1-x}B_x\), Vurgaftman et al. use \(E_g=(1-x)E_g(A)+xE_g(B)-x(1-x)C\). For AlGaAs they recommend the composition-dependent \(\Gamma\)-gap bowing \(C_\Gamma=-0.127+1.310x\) eV, zero effective-mass bowing (linear endpoint interpolation), and report a low-temperature \(\Gamma\)-X crossover at \(x=0.38\) (0.39 at 300 K) (Eq. 4.1, Table XII, pp. 5837–5839). — [Vurgaftman et al., alloy interpolation and AlGaAs section](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)
- A direct, model-independent ballistic-carrier measurement on GaAs/Al\(_x\)Ga\(_{1-x}\)As at 4.2 K found the \(\Gamma\)-band-gap discontinuity split to be 60.4:39.6 between conduction and valence bands, with ±2% uncertainty. — [Yi et al., *Appl. Phys. Lett.* 95, 112102 (2009), DOI 10.1063/1.3224914](https://doi.org/10.1063/1.3224914); [Harvard open-access copy](https://dash.harvard.edu/server/api/core/bitstreams/3638b704-7321-437c-9e63-d8877d180cd1/content)
- Published parameter practice is not unique: Vurgaftman's reference-energy tables imply a GaAs-to-AlAs valence offset of 0.53 eV (VBO entries −0.80 and −1.33 eV), while direct GaAs/AlGaAs experiments have also reported conduction offset fractions around 0.60–0.62. — [Vurgaftman et al., Tables I–II](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf); [Yi et al. 2009](https://doi.org/10.1063/1.3224914); [Fujiwara et al., conduction fraction \(Q_c=0.62\)](https://cir.nii.ac.jp/crid/1360016869467699200)

### Inferences
- At \(x=0.30\), Vurgaftman's bowing is \(C_\Gamma=0.266\) eV. The interpolated low-temperature barrier gap is therefore \(0.7(1.519)+0.3(3.099)-0.3(0.7)(0.266)=1.93714\) eV, so \(\Delta E_g=0.41814\) eV. Applying Yi et al.'s measured \(Q_c=0.604\) gives \(\Delta E_c=0.25256\) eV; rounding the model input to **0.253 eV** avoids false precision. These calculations derive directly from the cited Vurgaftman formula/endpoints and Yi offset fraction.
- Zero mass bowing gives \(m_b^*/m_0=0.7(0.067)+0.3(0.15)=0.0919\). Thus the recommended baseline configuration is `al_fraction=0.30`, `temperature_assumption="low-temperature (0 K interpolation; 4.2 K offset measurement)"`, `well_mass=0.067`, `barrier_mass=0.0919`, `barrier_eV=0.253`, and the GaAs conduction-band minimum as the zero of energy.
- The measured ±0.02 uncertainty in \(Q_c\) alone maps to approximately 0.244–0.261 eV for this calculated gap discontinuity. This is a useful, honest offset-sensitivity interval rather than a claim that 0.253 eV is universal.

### Gaps
- The scalar one-band model neglects energy-dependent nonparabolicity, strain, alloy disorder, interface roughness, electrostatics, dopants, temperature-dependent wavefunction interactions, and many-body effects; bulk band-edge masses and offsets are model inputs, not exact device properties.
- The 4.2 K offset experiment spans multiple Al compositions and supports a common direct-gap offset ratio, but it is not a dedicated uncertainty determination for only \(x=0.30\). The project should label its 0.253 eV value as an idealized literature-derived choice.

## Where do literature values disagree or depend on conventions, temperature, and composition?

### Takeaway
The largest defensible variations for this project are the conduction-band offset partition and the band-edge effective masses. Temperature, composition, valley choice, energy nonparabolicity, and the convention used to align valence bands all matter, so parameter sensitivity should be reported separately from numerical convergence.

### Cited Findings
- Vurgaftman et al. list a 0 K GaAs \(\Gamma\)-mass range of 0.065–0.070 and a 300 K range of 0.0635–0.067 rather than a single temperature-independent truth. — [Vurgaftman et al., Table I](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)
- Vurgaftman et al. report proposed AlGaAs \(\Gamma\)-gap bowing parameters from 0.14 to 0.66 eV, choose the composition-dependent Aspnes form for better accuracy, and state that the temperature dependence of bowing is insufficiently determined. — [Vurgaftman et al., AlGaAs discussion, pp. 5837–5838](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)
- Their review says several studies for \(x<0.33\) fitted nonlinear \(\Gamma\)-mass composition dependence but the narrow composition range and data spread make accuracy hard to judge; they recommend zero mass bowing and note a linear approximation is adequate at small \(x\). — [Vurgaftman et al., AlGaAs effective-mass discussion](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)
- A 300 K materials archive uses \(m_e^*/m_0=0.063+0.083x\) for direct-gap AlGaAs (\(x<0.45\)); at \(x=0.30\) this gives 0.0879, lower than the 0 K endpoint interpolation 0.0919. — [Ioffe Institute NSM Archive, AlGaAs basic parameters](https://www.ioffe.ru/SVA/NSM/Semicond/AlGaAs/basic.html)
- Experiments do not all encode exactly the same offset fraction: Yi et al. measured \(Q_c=0.604\pm0.02\), while an excitation-spectroscopy study reports \(Q_c=0.62\pm0.01\). — [Yi et al. 2009](https://doi.org/10.1063/1.3224914); [Fujiwara et al. record](https://cir.nii.ac.jp/crid/1360016869467699200)
- The direct-gap, single-\(\Gamma\)-valley picture ceases to describe the lowest barrier valley beyond the AlGaAs crossover (about \(x=0.38\) at low temperature in Vurgaftman's recommended interpolation). — [Vurgaftman et al., p. 5838](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)

### Inferences
- A transparent sensitivity experiment can vary \(Q_c\) over **0.584–0.624** (Yi central value ± quoted uncertainty), compare the common **0.60 and 0.62** conventions, and vary the barrier mass between **0.0879** (Ioffe 300 K formula) and **0.0919** (Vurgaftman 0 K linear interpolation). It should not mix these endpoints while claiming one precisely defined temperature; they are explicitly alternative assumption sets.
- A second scientifically useful sensitivity is Al fraction, e.g. \(x=0.20,0.25,0.30,0.35\), recomputing both gap discontinuity and mass from the cited formulas. Staying below 0.38 keeps the lowest barrier valley direct under the low-temperature interpolation and avoids silently changing the physics model.
- Numerical grid/domain sweeps must hold the material set fixed. Parameter sensitivity should then be compared against converged numerical results so input-model uncertainty is not mislabeled as discretization error.

### Gaps
- The cited data do not justify a single probability distribution for all material parameters; sensitivity ranges should be presented as plausible assumption alternatives, not statistical confidence intervals.
- A rigorous finite-temperature, energy-dependent nonparabolic mass model is outside the intended one-band undergraduate scope and would require additional band-structure parameters and validation.

## Which parameter sensitivities are scientifically honest to investigate?

### Takeaway
The most defensible study varies Al composition, the conduction-offset fraction, and well/barrier mass assumptions one at a time, always recomputing dependent quantities and clearly labelling the baseline versus alternatives.

### Cited Findings
- Alloy gaps in the Vurgaftman framework depend jointly on composition, endpoint gaps, and bowing, while the recommended AlGaAs \(\Gamma\)-mass approximation is linear in composition. — [Vurgaftman et al., Eq. 4.1 and Table XII](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)
- The experimental direct-gap offset fractions 0.604±0.02 and 0.62±0.01 demonstrate that an offset-ratio sensitivity is evidence-based rather than arbitrary. — [Yi et al. 2009](https://doi.org/10.1063/1.3224914); [Fujiwara et al.](https://cir.nii.ac.jp/crid/1360016869467699200)
- Vurgaftman explicitly warns that alloy mass data are spread and composition-limited, even though linear interpolation is an adequate small-\(x\) approximation. — [Vurgaftman et al., AlGaAs section](https://www.physik.uni-wuerzburg.de/fileadmin/11000000/03_Studium/03_Master/F-Praktikum/_imported/fileadmin/11999999/OS/Vurgaftman_-_Band_Parameters.pdf)

### Inferences
- Recommended experiment matrix: baseline \((x,Q_c,m_w,m_b)=(0.30,0.604,0.067,0.0919)\); composition sweep \(x=0.20\)–0.35 with all dependent properties recomputed; offset sweep \(Q_c=0.584,0.604,0.624\); and a clearly separate room-temperature-inspired mass comparison \((0.063,0.0879)\). Report shifts in bound energies and leakage, not a claim of discovering new material behavior.
- A useful attribution sequence is: (1) keep \(m=0.067m_0\) everywhere and use the same 0.253 eV potential; (2) introduce \(m_b=0.0919m_0\) with the BenDaniel–Duke operator; (3) vary the literature-based offset. This isolates mass-operator effects from barrier-height effects.

### Gaps
- Changing Al composition also changes dielectric and phonon properties that this one-electron, one-band model omits. The study can still isolate confinement sensitivity, but must not imply a complete device prediction.

## Which official SciPy and NumPy APIs support constants, tridiagonal eigensolution, root finding, and integration?

### Takeaway
Use `scipy.constants` for SI constants and conversions, `scipy.linalg.eigh_tridiagonal` for the real symmetric tridiagonal Hamiltonian, `scipy.optimize.brentq` for independently bracketed transcendental roots, and `numpy.trapezoid` for spatial normalization/probability integrals.

### Cited Findings
- SciPy's constants module exposes `hbar` in J·s, `electron_mass`/`m_e` in kg, and `electron_volt`/`eV` in joules; its database uses the 2022 CODATA recommended values in the current documentation. — [SciPy Constants documentation](https://docs.scipy.org/doc/scipy/reference/constants.html)
- `scipy.linalg.eigh_tridiagonal(d, e, ...)` solves the eigenproblem for a **real symmetric tridiagonal** matrix whose diagonal is `d` and off-diagonal is `e`; returned eigenvectors satisfy \(v^H v=I\). It supports selecting only an index or value range of eigenpairs. — [SciPy `eigh_tridiagonal` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html)
- `scipy.optimize.brentq` finds a scalar root on a sign-changing bracket and combines bracketing/bisection with inverse quadratic extrapolation; the official documentation describes it as a safe Brent method and exposes absolute/relative tolerances. — [SciPy `brentq` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html)
- `numpy.trapezoid(y, x=...)` computes a composite-trapezoidal approximation to \(\int y(x)\,dx\); supplying `x` makes the spatial units explicit. It was added in NumPy 2.0. — [NumPy `trapezoid` documentation](https://numpy.org/doc/stable/reference/generated/numpy.trapezoid.html)

### Inferences
- The implementation can remain SI internally: construct positions in metres, masses as a dimensionless ratio times `scipy.constants.electron_mass`, kinetic entries in joules using `hbar`, add potentials converted by `electron_volt`, solve, then divide returned energies by `electron_volt` for eV/meV reporting.
- Because `eigh_tridiagonal` normalizes vectors in the discrete Euclidean norm rather than the continuum integral norm, each eigenvector should be rescaled by `sqrt(np.trapezoid(abs(psi)**2, x))`; continuum overlap and outside-well probability should be evaluated with the same explicit-`x` quadrature.
- Pinning NumPy >=2.0 permits `np.trapezoid`; supporting older NumPy would require the older `np.trapz` spelling or SciPy integration. Pinning current compatible NumPy/SciPy versions is preferable for reproducibility.

### Gaps
- CODATA uncertainty is negligible compared with semiconductor parameter/model uncertainty here. The project should not confuse precision in fundamental constants with accuracy of the effective-mass approximation.
