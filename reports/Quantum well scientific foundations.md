# Validated models anchor quantum confinement lab

Quantum Confinement Lab should treat every reported energy as the intersection of three separate claims: a stated physical model, a tested numerical approximation, and an independently checkable reference calculation. The infinite well provides a closed-form continuum benchmark and an exact discrete-operator benchmark; the finite well adds a branch-safe parity-equation reference and an explicit test that bound states remain localized as the artificial domain expands. The semiconductor model should use the Hermitian BenDaniel–Duke (BDD) divergence operator, not a constant-mass Laplacian with a variable prefactor, and should be checked against unequal-mass interface-matching equations. A coherent material baseline is an idealized, unstrained low-temperature GaAs/Al\(_{0.30}\)Ga\(_{0.70}\)As well with \(m_w^*=0.067m_0\), \(m_b^*=0.0919m_0\), and \(V_0=0.253\) eV, while the measured band-offset uncertainty motivates a 0.244–0.261 eV sensitivity interval. These choices make the project scientifically defensible without overstating what a one-dimensional, one-band envelope model can predict.

## Two analytical references separate physics from discretization

The common starting point is the one-dimensional stationary Schrödinger equation,

\[
\left[-\frac{\hbar^2}{2m}\frac{d^2}{dx^2}+V(x)\right]\psi(x)=E\psi(x).
\]

For an infinite well of width \(L\), Dirichlet conditions at the walls give \(\psi_n(x)=\sqrt{2/L}\sin(n\pi x/L)\) and

\[
E_n=\frac{n^2\pi^2\hbar^2}{2mL^2},\qquad n=1,2,\ldots.
\]

This is more than a familiar textbook result: it provides direct tests of state ordering, \(L^{-2}\) width scaling, \(m^{-1}\) mass scaling, and continuum normalization ([MIT OpenCourseWare, Quantum Physics I, Lecture 11](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)). A uniform grid with \(N\) intervals and \(h=L/N\) supplies a second, logically distinct reference. For the centered Dirichlet second difference, the exact discrete energy is

\[
E_{n,h}=\frac{2\hbar^2}{mh^2}\sin^2\left(\frac{n\pi}{2N}\right),
\]

so the numerical eigensolver should agree with \(E_{n,h}\) nearly to its algebraic tolerance before its error against \(E_n\) is interpreted as continuum discretization error. The leading relative error is negative, \(-(n\pi)^2/(12N^2)+O(N^{-4})\), and therefore converges from below at second order for fixed low \(n\) ([MIT numerical-analysis notes, Chapter 5](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf)). **This three-way comparison—computed matrix eigenvalue, exact discrete eigenvalue, and exact continuum energy—prevents a correct eigensolver from masking an incorrectly assembled Hamiltonian.**

For the centered finite well, take \(V=0\) for \(|x|<a=L/2\) and \(V=V_0\) outside. Bound states satisfy \(0<E<V_0\), with \(k=\sqrt{2mE}/\hbar\) and \(\kappa=\sqrt{2m(V_0-E)}/\hbar\). Continuity of \(\psi\) and \(\psi'\) gives the independent constant-mass reference equations

\[
k\tan(ka)=\kappa \quad\text{(even)},\qquad
-k\cot(ka)=\kappa \quad\text{(odd)}.
\]

These equations arise from continuum interface matching, not from a grid, and thus can expose finite-difference errors rather than reproduce them ([Caltech Physics 12b finite-well notes](https://www.preskill.caltech.edu/ph12b/Ph12b-finite-well-4mar2010.pdf); [University of Texas finite-well treatment](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node181.html)). Their tangent and cotangent poles make unbracketed Newton iteration unsafe. The reference solver should search each open parity branch separately and use a sign-changing Brent bracket; SciPy documents `brentq` as a safeguarded bracketed method ([SciPy `brentq`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html)). **Only roots strictly inside \(0<E<V_0\) count as bound states.** A finite matrix also returns discrete states above \(V_0\), but those are box-discretized continuum states, not additional quantum-well levels.

## Flux-form discretization preserves heterojunction physics

A spatially varying mass changes the kinetic operator itself. For the selected single-conduction-band envelope model, the project should use

\[
H=-\frac{\hbar^2}{2}\frac{d}{dx}\left[\frac{1}{m^*(x)}\frac{d}{dx}\right]+V(x).
\]

BenDaniel and Duke introduced this junction model for simultaneous band-edge and band-curvature changes ([BenDaniel and Duke, *Physical Review* 152, 683 (1966)](https://doi.org/10.1103/PhysRev.152.683)). Across an ideal abrupt interface, the envelope \(\psi\) and flux-related derivative \((1/m^*)\psi'\) remain continuous. Those conditions conserve probability current and cancel the interface boundary term required for a Hermitian operator; they also distinguish the BDD model from the physically unjustified substitution \(-\hbar^2[2m(x)]^{-1}d^2/dx^2\).

On a uniform grid, define \(a_i=1/m_i^*\) and share one reciprocal-mass coefficient \(a_{i+1/2}\) across each face. With the harmonic face mass

\[
m_{i+1/2}^*=\frac{2m_i^*m_{i+1}^*}{m_i^*+m_{i+1}^*},\qquad
a_{i+1/2}=\frac{1}{m_{i+1/2}^*},
\]

the discrete action is

\[
(H\psi)_i=-\frac{\hbar^2}{2h^2}\left[a_{i+1/2}(\psi_{i+1}-\psi_i)-a_{i-1/2}(\psi_i-\psi_{i-1})\right]+V_i\psi_i.
\]

The main diagonal is \(\hbar^2(a_{i-1/2}+a_{i+1/2})/(2h^2)+V_i\), and the shared off-diagonal is \(-\hbar^2a_{i+1/2}/(2h^2)\). The same face coefficient therefore appears as \(H_{i,i+1}=H_{i+1,i}\), making the real symmetry visible in the data structure rather than merely assumed. Semiconductor finite-difference literature uses the same midpoint, divergence-form structure for discontinuous effective masses ([Galeriu et al., *Computer Physics Communications* 157, 147–159 (2004)](https://m3ai.wlu.ca/research/publications/EJ-67.pdf)). The implementation should store only the diagonal and first off-diagonal and solve with `scipy.linalg.eigh_tridiagonal`, whose contract is specifically a real symmetric tridiagonal eigenproblem with ascending eigenvalues and orthonormal vectors ([SciPy `eigh_tridiagonal`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html)).

The unequal-mass analytical check follows from the same physical interface conditions but uses no grid. For a symmetric well with masses \(m_w\) and \(m_b\), independently solve

\[
\frac{k}{m_w}\tan(ka)=\frac{\kappa}{m_b}\quad\text{(even)},\qquad
\frac{k}{m_w}\cot(ka)=-\frac{\kappa}{m_b}\quad\text{(odd)},
\]

where \(k=\sqrt{2m_wE}/\hbar\) and \(\kappa=\sqrt{2m_b(V_0-E)}/\hbar\). These are the BDD matching equations for the sinusoidal well solution and evanescent barrier solution ([position-dependent-mass square-well derivation](https://www.intechopen.com/chapters/59407)). Their equal-mass limit must reproduce the ordinary finite-well roots. Reporting the finite-difference-minus-matching difference in meV at several grids and domains establishes independent validation; agreement between two matrix assemblers would not.

## Convergence tests isolate numerical error sources

Grid error and domain truncation answer different questions and must never be varied together without attribution. At a fixed physical domain, the centered second derivative has \(O(h^2)\) truncation error for sufficiently smooth functions ([MIT OpenCourseWare, Introduction to Numerical Analysis, Chapter 2](https://live.ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/aab35b69b416758992779e2ad508b286_MIT18_330S12_Chapter2.pdf)). Three nested grids can estimate the observed order

\[
p_{\mathrm{obs}}=\frac{\log(|E_h-E_{h/2}|/|E_{h/2}-E_{h/4}|)}{\log 2}.
\]

Square potential and mass discontinuities reduce smoothness, so practical slopes can depart from two on coarse or inconsistently aligned grids. The interfaces should occupy the same geometric locations through refinement, and the report should present measured slopes instead of asserting ideal second-order behavior where results do not support it.

At fixed grid spacing, exterior padding controls a separate hard-wall perturbation. A true bound state decays outside the well as \(e^{-\kappa |x|}\), with penetration length \(1/\kappa\); near-threshold states therefore require much larger padding than deeply bound states ([Caltech finite-well notes](https://www.preskill.caltech.edu/ph12b/Ph12b-finite-well-4mar2010.pdf)). The domain study should increase padding while monitoring energy changes and probability in narrow boundary guard regions. It should report physical leakage, \(P_{\mathrm{out}}=\int_{|x|>a}|\psi|^2dx\), separately from boundary-guard probability: the former is genuine finite-barrier tunnelling, while the latter diagnoses artificial confinement.

Every computed state should be checked for unit integral, quadrature-weighted orthogonality, ascending energy, Dirichlet endpoint behavior, parity in symmetric cases, and a small relative eigenpair residual. SciPy eigenvectors are normalized in the Euclidean norm, so sampled wavefunctions must be rescaled using an explicit spatial integral; `numpy.trapezoid(y, x=...)` makes both the integration rule and length coordinate explicit ([NumPy `trapezoid`](https://numpy.org/doc/stable/reference/generated/numpy.trapezoid.html)). Symmetry should be verified at roundoff, and the variable-mass operator should reduce exactly to the constant-mass stencil when all masses match. **A credible bound-state label additionally requires \(E<V_0\), spatial localization, and stability under domain growth.** These checks target different failure modes; no single tolerance substitutes for the set.

## Literature-derived inputs define a bounded claim

The project baseline should be an undoped, unstrained, symmetric GaAs/Al\(_{0.30}\)Ga\(_{0.70}\)As type-I well, with zero energy at the GaAs conduction-band minimum and low-temperature bulk parameters. Vurgaftman, Meyer, and Ram-Mohan recommend \(E_g^\Gamma=1.519\) eV and \(m_e^\Gamma=0.067m_0\) for GaAs at 0 K, and \(E_g^\Gamma=3.099\) eV and \(m_e^\Gamma=0.15m_0\) for AlAs; for AlGaAs they recommend composition-dependent gap bowing, zero mass bowing, and place the low-temperature \(\Gamma\)-to-X crossover near \(x=0.38\) ([Vurgaftman et al., *Journal of Applied Physics* 89, 5815 (2001)](https://doi.org/10.1063/1.1368156)). At \(x=0.30\), their interpolation yields an AlGaAs \(\Gamma\)-gap of 1.93714 eV and a barrier mass of \(0.0919m_0\). Because \(x=0.30\) remains below the cited crossover, a single-\(\Gamma\)-valley barrier model is internally consistent.

Yi and collaborators measured the direct-gap GaAs/AlGaAs discontinuity at 4.2 K as a 60.4:39.6 conduction-to-valence split, with \(Q_c=0.604\pm0.02\) ([Yi et al., *Applied Physics Letters* 95, 112102 (2009)](https://doi.org/10.1063/1.3224914)). Applying that fraction to the 0.41814 eV interpolated gap difference gives 0.25256 eV, appropriately rounded to **\(V_0=0.253\) eV**. Propagating only the quoted offset-fraction range gives **0.244–0.261 eV**, which should be treated as a plausible assumption sensitivity, not as a complete device confidence interval. A separate room-temperature-inspired comparison can use \(m_w^*=0.063m_0\) and \(m_b^*=0.0879m_0\); the latter follows the Ioffe archive interpolation \(m^*/m_0=0.063+0.083x\) for direct-gap AlGaAs ([Ioffe NSM Archive](https://www.ioffe.ru/SVA/NSM/Semicond/AlGaAs/basic.html)). These temperature-labelled alternatives must not be mixed into a single falsely precise parameter set.

BDD is a standard, useful low-energy ordering, but it is not an exact atomistic theory or the unique quantization of every position-dependent classical-mass problem. Envelope-function theory assumes variation slow on the lattice scale even across an abrupt material boundary ([Burt, *Physical Review B* 50, 7518 (1994)](https://doi.org/10.1103/PhysRevB.50.7518)), and higher-order reductions can contain interface-localized terms absent from the elementary BDD model ([Foreman, *Physical Review B* 52, 12241 (1995)](https://doi.org/10.1103/PhysRevB.52.12241)). The project must therefore disclose that it omits nonparabolic, energy-dependent mass; multiband coupling; strain; alloy disorder and interdiffusion; interface roughness and atomistic bonding; dopants and Schrödinger–Poisson self-consistency; carrier interactions; and temperature dependence beyond the selected bulk inputs. These omissions bound the claim: the results compare idealized confinement models and numerical assumptions, not a fabricated device or an experimental measurement.

## Conclusion

The strongest implementation is not the one with the most semiconductor detail; it is the one whose claims have distinct failure detectors. Exact discrete eigenvalues diagnose matrix assembly, continuum formulas diagnose grid error, parity matching diagnoses finite- and mass-mismatched wells, and padding studies diagnose artificial domain confinement. Together they let the report state which differences are physical model effects and which are numerical approximation effects.

The literature-derived GaAs/AlGaAs case then becomes a disciplined sensitivity study rather than a claim of universal material truth. Fixing the baseline, propagating credible alternative offsets and masses, and naming the omitted physics makes the advanced model appropriate for an undergraduate research portfolio while preserving the scientific honesty needed for technical scrutiny.
