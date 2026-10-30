# Position-dependent effective mass heterostructures

## What operator and interface conditions are physically standard for abrupt semiconductor heterojunctions?

### Takeaway
For the project's one-band conduction-envelope model, use the BenDaniel–Duke (BDD) divergence-form Hamiltonian
\(H=-\frac{\hbar^2}{2}\frac{d}{dx}[m^{*-1}(x)\frac{d}{dx}]+V(x)\). At an ideal abrupt interface its domain is defined by continuity of \(\psi\) and of \(m^{*-1}\psi'\); the latter is the current/flux matching condition.

### Cited Findings
- BenDaniel and Duke's original 1966 paper formulated one-electron tunnelling for junctions in which both band curvature (electron mass) and band-edge position vary across the junction. The stable primary citation is D. J. BenDaniel and C. B. Duke, *Physical Review* **152**, 683 (1966), DOI 10.1103/PhysRev.152.683. — [APS/DOI](https://doi.org/10.1103/PhysRev.152.683)
- A modern derivation states the BDD Hamiltonian explicitly as \(-\hbar^2/2\,d/dx\,[m^{-1}(x)d/dx]+V\), and states continuity of the envelope and of \((1/m)d\psi/dx\) at the interface. — [IntechOpen chapter, equations 1–4](https://www.intechopen.com/chapters/59407)
- Lévy-Leblond derived a position-dependent-mass Hamiltonian and abrupt-heterojunction boundary conditions from instantaneous Galilean invariance, providing independent theoretical support rather than only empirical convention. — [Physical Review A 52, 1845 (1995), DOI 10.1103/PhysRevA.52.1845](https://doi.org/10.1103/PhysRevA.52.1845)
- Burt's effective-mass derivation for atomically abrupt microstructures identifies the central envelope-function assumption: the envelope varies slowly on the lattice-period scale; unlike elementary treatments, it does not assume the band-edge Bloch functions are identical on both sides. — [Physical Review B 50, 7518 (1994), DOI 10.1103/PhysRevB.50.7518](https://doi.org/10.1103/PhysRevB.50.7518)
- Foreman's exact heterostructure analysis finds an infinite-order differential equation; its finite second-order reduction is related to the BDD model but can also contain a localized interface delta term. This is a warning that the elementary BDD model is a controlled low-order model, not an exact atomic-interface theory. — [Physical Review B 52, 12241 (1995), DOI 10.1103/PhysRevB.52.12241](https://doi.org/10.1103/PhysRevB.52.12241)

### Inferences
- Integrating the divergence-form equation over an infinitesimal interval around a finite potential/mass jump gives continuity of \(m^{-1}\psi'\); together with continuity of \(\psi\), this also makes the boundary term in \(\langle\phi,H\psi\rangle-\langle H\phi,\psi\rangle\) vanish. Thus the selected operator and matching conditions are mutually consistent and Hermitian.
- In code and documentation call \(\psi\) a conduction-band *envelope function*, not the microscopic crystal wavefunction. Treat the barrier edge as the zero-reference plus \(V_0\), and require positive masses for the type-I GaAs/AlGaAs model.

### Gaps
- The single-band project will not determine Foreman's interface delta term from microscopic first principles. It should explicitly set such interface terms to zero and identify that as a BDD modelling assumption.

## How can the operator be discretized as a symmetric tridiagonal Hamiltonian?

### Takeaway
Discretize the divergence form as a difference of face fluxes, sharing the same positive reciprocal-mass coefficient on both sides of each grid edge. This produces a real symmetric tridiagonal matrix by construction; do not expand the operator into a naïve variable coefficient times a constant-mass Laplacian.

### Cited Findings
- Published semiconductor finite-difference work writes the BDD equation in divergence form and applies central differences on a grid with midpoint quantities, which is the appropriate numerical structure for discontinuous material coefficients. — [Galeriu et al., *Computer Physics Communications* 157, 147–159 (2004)](https://m3ai.wlu.ca/research/publications/EJ-67.pdf)
- A finite-difference quantum-well derivation uses half-grid effective masses in the discretized divergence, producing a tridiagonal Hamiltonian; it notes that a uniform grid makes the displayed matrix symmetric. — [Band-scheme modelling thesis, equations 5.9–5.10](https://citeseerx.ist.psu.edu/document?doi=e77928e4dc892991124d282b2244881b30d7e10f&repid=rep1&type=pdf)
- A numerical BDD quantum-dot study independently uses the Hamiltonian \(-\hbar^2\nabla(m^{-1}\nabla)/2+V\), finite differences, and verifies against a separate analytical interface-matching solution. — [Woon and Yung, *Sains Malaysiana* 40, 55–58 (2011)](https://www.ukm.edu.my/jsm/pdf_files/SM-PDF-40-1-2011/12%20Woon.pdf)
- The BDD operator is also the explicit confinement Hamiltonian used for electron and hole states in a peer-reviewed GaAs/AlGaAs coupled-quantum-well calculation. — [Wilkes and Muljarov, *New Journal of Physics* 18, 023032 (2016), DOI 10.1088/1367-2630/18/2/023032](https://doi.org/10.1088/1367-2630/18/2/023032)

### Inferences
- On a uniform interior grid \(x_i\) with spacing \(h\), define \(a_i=1/m_i^*\) and one shared face coefficient \(a_{i+1/2}\). If the implementation requirement is expressed as a harmonic face mass, use
  \[
  m_{i+1/2}^{*}=\frac{2m_i^*m_{i+1}^*}{m_i^*+m_{i+1}^*},\qquad
  a_{i+1/2}=\frac{1}{m_{i+1/2}^{*}}=\tfrac12(a_i+a_{i+1}).
  \]
  The discrete action is
  \[
  (H\psi)_i=-\frac{\hbar^2}{2h^2}
  [a_{i+1/2}(\psi_{i+1}-\psi_i)-a_{i-1/2}(\psi_i-\psi_{i-1})]+V_i\psi_i.
  \]
  Therefore
  \(H_{ii}=\frac{\hbar^2}{2h^2}(a_{i-1/2}+a_{i+1/2})+V_i\) and
  \(H_{i,i+1}=H_{i+1,i}=-\frac{\hbar^2}{2h^2}a_{i+1/2}\). This algebra proves real symmetry because each face coefficient is literally shared.
- Dirichlet endpoints can be excluded from the unknown vector. Store only the main and first off-diagonal arrays and solve with a symmetric tridiagonal eigensolver.
- Required automated checks: (1) `max(abs(H-H.T))` at roundoff; (2) constant-mass reduction to the standard three-point Laplacian; (3) positive kinetic quadratic form; (4) normalized orthogonal eigenvectors; (5) eigenpair residuals; (6) convergence to the independent parity roots below; and (7) convergence of one-sided \((1/m)\psi'\) at each interface.
- There is a subtle placement convention at a discontinuity: averaging reciprocal mass at a node-to-node face (equivalently a harmonic mean of nodal masses) and a finite-volume harmonic average of the *coefficient* \(a=1/m\) correspond to different assumptions about whether the material jump lies on a node or within a cell. The project should align well edges consistently, document its convention, and demonstrate convergence under grid refinement rather than claim that one interpolation is atomically exact.

### Gaps
- The cited literature supports face-based divergence discretization, but there is no universal interface-averaging formula independent of grid/material placement. The implementation must therefore document and test its chosen harmonic-face-mass convention.

## What independent analytical matching solution validates unequal-mass bound states?

### Takeaway
For a symmetric well of width \(L=2a\), well mass \(m_w\), barrier mass \(m_b\), and barrier \(V_0\), independently root-solve the BDD parity equations for every \(0<E<V_0\). This calculation shares only the physical boundary conditions with the finite-difference solver, not its grid or matrix algorithm.

### Cited Findings
- For the symmetric mass-mismatched finite well, the literature defines \(k=\sqrt{2m_wE}/\hbar\), \(\kappa=\sqrt{2m_b(V_0-E)}/\hbar\), constructs cosine/sine states in the well and decaying exponentials outside, and derives the BDD transcendental equations. — [IntechOpen chapter, equations 5–28](https://www.intechopen.com/chapters/59407)
- In the equal-mass limit these equations reduce to the familiar finite-square-well even and odd quantization conditions, giving an immediate limiting-case check. — [IntechOpen chapter, equations 23–30](https://www.intechopen.com/chapters/59407)
- A separate study of position-dependent-mass square wells likewise derives transcendental eigenvalue equations by applying interface matching, supporting analytical matching as a genuinely distinct reference method. — [Dekar, *Journal of Mathematical Physics* preprint, arXiv:quant-ph/0608102](https://arxiv.org/abs/quant-ph/0608102)
- Transfer-matrix accuracy for both constant and position-dependent effective mass has been compared directly with finite differences in the numerical literature. — [Jirauschek, *IEEE Journal of Quantum Electronics* 45, 1059 (2009), arXiv:1106.3201](https://arxiv.org/abs/1106.3201)

### Inferences
- With \(a=L/2\), solve the two independent residuals
  \[
  f_{\rm even}(E)=\frac{k}{m_w}\tan(ka)-\frac{\kappa}{m_b}=0,
  \]
  \[
  f_{\rm odd}(E)=\frac{k}{m_w}\cot(ka)+\frac{\kappa}{m_b}=0,
  \]
  or algebraically equivalent nonsingular residuals. The corresponding wavefunctions are \(A\cos(kx)\) and \(A\sin(kx)\) inside, joined to decaying exponentials outside. These formulas follow directly from the cited BDD conditions.
- Bracket roots separately between tangent/cotangent poles; never let a root finder cross a pole. Reject endpoints and accept only \(0<E<V_0\). Deduplicate roots at tight tolerance and sort them. In the limit \(m_w=m_b\), compare against the constant-mass reference; in the limit \(V_0\to\infty\), the roots approach infinite-well values.
- A general transfer-matrix reference can propagate the BDD state vector \(y=[\psi,(1/m)\psi']^T\). In a constant region of mass \(m\), width \(d\), and real wave number \(q\),
  \[
  y(x+d)=\begin{bmatrix}\cos qd&(m/q)\sin qd\\-(q/m)\sin qd&\cos qd\end{bmatrix}y(x).
  \]
  For an evanescent region set \(q=i\kappa\), yielding the corresponding cosh/sinh matrix. Because both components of \(y\) are continuous at a BDD interface, no ad hoc interface matrix is needed. Requiring decay in both outer barriers gives an independent scalar determinant/root condition for asymmetric extensions.
- Validation should report finite-difference minus matching energy in meV and relative terms for every bound state, then show that disagreement shrinks under both grid and domain refinement. A state is bound only when its reference or numerical energy is below \(V_0\) and its density is localized; box-discretized states above the barrier are not bound states.

### Gaps
- The parity equations are exact only for the ideal symmetric piecewise-constant, one-band BDD model. They do not independently validate graded alloys, electric fields, nonparabolic mass, or microscopic interface terms.

## What limitations and operator-ordering caveats must be disclosed?

### Takeaway
BDD is a defensible, standard single-band envelope model for this portfolio investigation, but it is not a unique exact quantization of an arbitrary position-dependent classical mass and it omits atomic-scale interface physics, multiband coupling, strain, charge self-consistency, and energy-dependent nonparabolicity.

### Cited Findings
- The position-dependent-mass literature contains multiple Hermitian operator orderings; calculations for a GaAs/AlGaAs well can depend on which Hermitian Hamiltonian is selected. — [Morrow and Brownstein, *Physical Review B* 30, 678 (1984) context; ordering dependence demonstrated in *Physical Review B* 47, 12760 (1993), DOI 10.1103/PhysRevB.47.12760](https://doi.org/10.1103/PhysRevB.47.12760)
- Burt identifies slowly varying envelope functions as the principal approximation even when the material boundary is atomically abrupt. — [Physical Review B 50, 7518 (1994), DOI 10.1103/PhysRevB.50.7518](https://doi.org/10.1103/PhysRevB.50.7518)
- Foreman's exact theory shows that interface-localized terms can survive when reducing the exact heterostructure problem to a second-order model. — [Physical Review B 52, 12241 (1995), DOI 10.1103/PhysRevB.52.12241](https://doi.org/10.1103/PhysRevB.52.12241)
- For GaAs/AlGaAs wells, a peer-reviewed study found that both mass magnitude and conduction-band nonparabolicity can significantly affect confinement energy, particularly in narrow wells. — [Chen and Andersson, *Physical Review B* 44, 9068 (1991), DOI 10.1103/PhysRevB.44.9068](https://doi.org/10.1103/PhysRevB.44.9068)
- The widely used III–V parameter review tabulates composition- and temperature-dependent gaps, effective masses, bowing, and heterostructure band offsets, emphasizing that material parameters are model inputs with stated conditions rather than universal constants. — [Vurgaftman, Meyer, and Ram-Mohan, *Journal of Applied Physics* 89, 5815 (2001), DOI 10.1063/1.1368156](https://doi.org/10.1063/1.1368156)
- A readily inspectable 300 K AlGaAs compilation gives the direct-valley electron-mass interpolation \(m_\Gamma^*/m_0=0.063+0.083x\) for \(x<0.45\), illustrating both composition and temperature specificity. — [Ioffe NSM Archive: AlGaAs basic parameters](https://www.ioffe.ru/SVA/NSM/Semicond/AlGaAs/basic.html)

### Inferences
- The report should describe BDD as the explicitly selected operator ordering for a low-energy, single-conduction-band envelope model. It should not say that BDD is the uniquely correct Hamiltonian for all position-dependent-mass quantum mechanics.
- A clean reference case is an undoped, strain-free, symmetric GaAs/Al\(_x\)Ga\(_{1-x}\)As type-I well at an explicitly stated temperature, with zero energy at the GaAs conduction-band edge. State \(x\), \(m_w\), \(m_b(x)\), \(V_0=\Delta E_c\), and the source/formula for each. Sensitivity analysis should vary the band-offset fraction and mass within defensible alternatives instead of presenting a single parameter set as exact.
- Important omissions to disclose: energy-dependent/nonparabolic mass; multiband \(k\cdot p\) coupling; electron–electron and electron–hole interactions; dopants and Schrödinger–Poisson self-consistency; strain; alloy disorder/interdiffusion; atomistic interface bonding; and temperature dependence beyond the chosen bulk parameters.

### Gaps
- This research pass did not select the project's final Al fraction, temperature, and conduction-band-offset formula; those should be fixed by the separate material-parameter review and recorded in the scientific specification before experiments run.
