# One-dimensional quantum wells and finite-difference validation

## What equations and boundary conditions independently validate infinite and finite square wells?

### Takeaway
Use two genuinely independent continuum references: the closed-form infinite-well spectrum and parity-resolved transcendental equations for the finite well. Express the finite well with its bottom at (0) and barrier at (V_0), so a physical bound state is exactly one with (0<E<V_0); this is the same problem as the common (-V_0<E'<0) convention after the constant shift (E=E'+V_0).

### Cited Findings
- The stationary one-dimensional problem is
  \[
  \left[-\frac{\hbar^2}{2m}\frac{d^2}{dx^2}+V(x)\right]\psi(x)=E\psi(x).
  \]
  For an infinite well on (0<x<L), the wavefunction obeys the Dirichlet conditions (psi(0)=\psi(L)=0); the acceptable states are
  \[
  \psi_n(x)=\sqrt{\frac{2}{L}}\sin\!\left(\frac{n\pi x}{L}\right),\qquad
  E_n=\frac{n^2\pi^2\hbar^2}{2mL^2},\quad n=1,2,\ldots.
  \]
  MIT's derivation explicitly gives the endpoint conditions, normalization, and spectrum. — [MIT OpenCourseWare, Quantum Physics I, Lecture 11](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)
- For a centered finite well of full width (L=2a), use (V(x)=0) for (|x|<a) and (V(x)=V_0) outside. For (0<E<V_0), define
  \[
  k=\sqrt{2mE}/\hbar,\qquad \kappa=\sqrt{2m(V_0-E)}/\hbar.
  \]
  The wavefunction is sinusoidal inside and exponentially decaying outside; for constant mass, continuity of both (psi) and (d\psi/dx) at (x=\pm a) yields
  \[
  \text{even: } k\tan(ka)=\kappa,
  \qquad
  \text{odd: }-k\cot(ka)=\kappa.
  \]
  These are the parity-resolved quantization equations for a separate reference solver. — [Caltech Physics 12b finite-well notes](https://www.preskill.caltech.edu/ph12b/Ph12b-finite-well-4mar2010.pdf); [MIT OpenCourseWare, Lecture 11](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)
- A convenient dimensionless form is
  \[
  z=ka,\quad z_0=a\sqrt{2mV_0}/\hbar,\quad y=\kappa a=\sqrt{z_0^2-z^2},
  \]
  with (0<z<z_0), giving (z\tan z=y) for even states and (-z\cot z=y) for odd states. The University of Texas treatment gives the equivalent even and odd equations and restricts the dimensionless root to the bound-state energy interval. — [University of Texas, Particle in Finite Square Potential Well](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node181.html)
- The finite-well roots must be bracketed separately between tangent/cotangent poles. An implementation-safe scheme is to intersect (0<z<z_0) with the open intervals
  \[
  \text{even: }(j\pi,\,j\pi+\pi/2),\qquad
  \text{odd: }(j\pi+\pi/2,\,(j+1)\pi),\quad j=0,1,\ldots,
  \]
  shrink each endpoint by a small scale-aware amount, confirm a sign change, and then call a bracketed solver. SciPy documents that `root_scalar(..., method="brentq", bracket=[a,b])` uses a bracket; this avoids Newton iterates jumping across poles. — [SciPy `root_scalar` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root_scalar.html); equations and pole structure from [University of Texas finite-well treatment](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node181.html)
- A one-dimensional attractive square well always has at least one even bound state, whereas the first odd state requires sufficient depth/width; the cited dimensionless convention gives no odd state for (lambda<(\pi/2)^2). This is a useful state-count regression test for the reference root solver. — [University of Texas, Particle in Finite Square Potential Well](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node181.html)
- For implementation with the well bottom at zero, energies from a source using the well at (-V_0) and the exterior at zero must be shifted by (+V_0). MIT explicitly warns that the energy origin must be handled when comparing finite- and infinite-well results. — [MIT OpenCourseWare, Lecture 11](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)
- The finite-difference Hamiltonian on (N-1) interior nodes of a uniform (N)-interval grid is real symmetric tridiagonal for constant (m):
  \[
  H_{ii}=\frac{\hbar^2}{m h^2}+V_i,\qquad
  H_{i,i\pm1}=-\frac{\hbar^2}{2mh^2},\qquad h=L/N.
  \]
  SciPy's `eigh_tridiagonal` is specifically defined for real symmetric tridiagonal matrices, returns ascending eigenvalues and right eigenvectors, and allows selection by index or value. — [SciPy `eigh_tridiagonal` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html)

### Inferences
- The infinite-well validation should compare the same computed eigenvalue three ways: (1) the numerical eigensolver output, (2) the exact eigenvalue of the *discrete* tridiagonal operator, and (3) the continuum (E_n). Agreement with (2) tests assembly/eigensolver correctness, while the gap from (3) measures discretization error; the source-backed formulas for both spectra make these logically distinct checks. — [MIT numerical-analysis notes](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf); [MIT quantum notes](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)
- The finite-well reference solver should share only physical inputs and units with the matrix solver, not its grid, Hamiltonian assembly, or eigenvectors. Solving the branch-wise transcendental equations with `brentq` is therefore an independent algorithmic validation. — [SciPy `root_scalar` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root_scalar.html); [Caltech finite-well notes](https://www.preskill.caltech.edu/ph12b/Ph12b-finite-well-4mar2010.pdf)

### Gaps
- The exact number of bound states is sensitive to the convention used for the dimensionless depth parameter and to whether a threshold state at (E=V_0) is counted; avoid a memorized closed-form count. Count only roots strictly inside (0<E<V_0), with explicit tolerance and branch tests. The cited sources support root counting graphically but do not provide one convention-independent integer formula. — [University of Texas finite-well treatment](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node181.html)

## How should bound states be distinguished from box-discretized continuum states?

### Takeaway
Classify by the asymptotic barrier, not by the fact that a finite matrix returns a discrete eigenvalue. For the present potential with exterior (V_0), require (E<V_0) (with a documented numerical margin), spatial localization, and stability as exterior padding grows; states above (V_0) are box-discretized continuum states and must not be reported as quantum-well bound states.

### Cited Findings
- A bound state on the infinite line must be normalizable and decay as (|x|\to\infty). In the energy convention with exterior zero and well bottom (-V_0), the bound-state interval is (-V_0<E<0), while (E>0) produces exterior plane waves that are not normalizable. Shifting the energy zero to the well bottom converts this to (0<E<V_0). — [MIT OpenCourseWare, Lecture 11](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)
- The physical bound-state tail is exponential: outside a constant barrier, (psi\propto e^{-\kappa |x|}) with (kappa=\sqrt{2m(V_0-E)}/\hbar), and the characteristic penetration depth is (1/\kappa). — [Caltech finite-well notes](https://www.preskill.caltech.edu/ph12b/Ph12b-finite-well-4mar2010.pdf); [Modern Physics for Scientists and Engineers, finite-well section hosted by University of Cincinnati](https://www.eng.uc.edu/~beaucag/Classes/AdvancedMaterialsThermodynamics/Books/Modern%20Physics%20for%20Scientists%20and%20Engineers.pdf)
- Finite barriers therefore give a nonzero probability outside the nominal well; the finite-well wavefunction joins smoothly at the interfaces and approaches zero exponentially, and the number of physical bound levels is finite. — [University of Texas finite-well treatment](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node181.html); [Modern Physics for Scientists and Engineers](https://www.eng.uc.edu/~beaucag/Classes/AdvancedMaterialsThermodynamics/Books/Modern%20Physics%20for%20Scientists%20and%20Engineers.pdf)
- `eigh_tridiagonal` returns the eigenpairs of the finite tridiagonal matrix supplied to it; on a truncated domain all of those matrix eigenvalues are discrete. The API does not attach physical bound/continuum labels, so classification must occur after solving. — [SciPy `eigh_tridiagonal` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html)
- A robust numerical acceptance set is: (i) (E<V_0-\tau_E); (ii) normalized probability (int |\psi|^2dx=1) within tolerance; (iii) small amplitude/probability in boundary guard regions; and (iv) energy stability under increased exterior padding at fixed grid spacing. Conditions (i) and exponential localization follow from the continuum bound-state definition; conditions (iii)–(iv) test whether imposed Dirichlet walls are perturbing that tail. — bound-state definition and tail: [MIT OpenCourseWare, Lecture 11](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)
- For a uniform grid, SciPy eigenvectors are Euclidean-normalized ((v^Tv=1)); a continuum-normalized sampled wavefunction is therefore (psi_i=v_i/\sqrt{h}) for the rectangle-rule inner product, or should be explicitly rescaled using the chosen numerical quadrature. MIT's numerical notes explain the weighted discrete norm (\|u\|_{2,h}=(h\sum_i|u_i|^2)^{1/2}), while the quantum notes impose (int |\psi|^2dx=1). — [MIT numerical-analysis notes](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf); [MIT quantum notes](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf); [SciPy `eigh_tridiagonal` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html)
- Since a real symmetric matrix has orthogonal eigenvectors, verify the quadrature-weighted overlap matrix (S_{mn}=\sum_i\psi_{m,i}\psi_{n,i}h) against the identity after continuum normalization. Also compute the relative eigenpair residual
  \[
  r_n=\frac{\|H\psi_n-E_n\psi_n\|_2}{\max(\|H\psi_n\|_2,|E_n|\|\psi_n\|_2,\epsilon)}.
  \]
  SciPy states the defining relations (Av_i=w_i v_i) and (V^HV=I), which these tests check rather than assume. — [SciPy `eigh_tridiagonal` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html)

### Inferences
- Choose padding in units of the weakest-decaying retained state's penetration depth: if the nearest reported state has (kappa_{\min}), the unperturbed tail amplitude at a wall a padding distance (p) away scales as (e^{-\kappa_{\min}p}). This directly motivates padding until both boundary probability and successive-domain energy changes meet declared tolerances. — exponential tail from [Caltech finite-well notes](https://www.preskill.caltech.edu/ph12b/Ph12b-finite-well-4mar2010.pdf)
- A near-threshold state ((E\lesssim V_0)) has small (kappa), long penetration depth, and correspondingly slower domain convergence. It should receive a larger domain and a stricter domain-sensitivity warning than a deeply bound state. — (1/\kappa) penetration depth from [Modern Physics for Scientists and Engineers](https://www.eng.uc.edu/~beaucag/Classes/AdvancedMaterialsThermodynamics/Books/Modern%20Physics%20for%20Scientists%20and%20Engineers.pdf)
- Report the outside-well probability (P_{\rm out}=\int_{|x|>a}|\psi|^2dx) as a physical observable, but separately report the probability in a narrow boundary guard band as a domain-truncation diagnostic; conflating them would incorrectly treat genuine tunnelling leakage as numerical error. — finite outside-well probability from [University of Texas finite-well treatment](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node181.html)

### Gaps
- No simple universal finite-padding error bound was identified in the authoritative pedagogical sources reviewed. The project should therefore present measured domain-convergence deltas rather than claim an exact exponential energy-error order; the exponential *tail* is established, but the prefactor and energy perturbation from a hard numerical wall depend on the state and setup. — tail behavior from [MIT OpenCourseWare, Lecture 11](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)

## What convergence behavior is expected from a centered second-order finite-difference operator, and how do finite-domain errors differ?

### Takeaway
At fixed physical domain, the centered three-point kinetic operator is second-order accurate for sufficiently smooth eigenfunctions, so low-state energy errors should scale approximately as (h^2). Domain truncation is a separate error source controlled by exterior padding; test it at fixed (h), and test grid convergence at fixed domain, rather than changing both simultaneously.

### Cited Findings
- The centered second derivative is
  \[
  \psi''(x_i)=\frac{\psi_{i+1}-2\psi_i+\psi_{i-1}}{h^2}+O(h^2),
  \]
  with leading local term (h^2\psi^{(4)}(\xi)/12) when the needed smoothness holds. — [MIT OpenCourseWare, Introduction to Numerical Analysis, Chapter 2](https://live.ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/aab35b69b416758992779e2ad508b286_MIT18_330S12_Chapter2.pdf)
- For the Dirichlet negative second derivative on a length-(L) interval split into (N) equal subintervals ((h=L/N), (N-1) interior unknowns), the exact discrete eigenpairs are
  \[
  v^{(n)}_j=\sin\!\left(\frac{n\pi j}{N}\right),\qquad
  \lambda_n^{(h)}=\frac{4}{h^2}\sin^2\!\left(\frac{n\pi}{2N}\right),
  \quad n,j=1,\ldots,N-1.
  \]
  MIT's numerical notes derive these eigenvectors/eigenvalues and establish second-order convergence for the Dirichlet finite-difference problem. — [MIT numerical-analysis notes, Chapter 5](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf)
- Multiplying by (hbar^2/(2m)) gives the exact infinite-well *discrete* energies
  \[
  E_{n,h}=\frac{2\hbar^2}{mh^2}\sin^2\!\left(\frac{n\pi}{2N}\right).
  \]
  Relative to the continuum (E_n=\hbar^2n^2\pi^2/(2mL^2)), Taylor expansion gives
  \[
  \frac{E_{n,h}-E_n}{E_n}=-\frac{(n\pi)^2}{12N^2}+O(N^{-4}),
  \]
  so at fixed low (n) the standard second-difference energy approaches from below with (O(h^2)) error. This follows directly from the source's exact discrete formula and the continuum spectrum. — discrete formula: [MIT numerical-analysis notes](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf); continuum formula: [MIT quantum notes](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf)
- The MIT numerical notes also state near the formula that the (O(h^2)) correction to the minimum eigenvalue is positive; this conflicts with both the displayed sine formula and (sin x<x) for (x>0). The project should trust the exact displayed formula and verify it computationally; the correct leading relative correction for the stated stencil is negative. — [MIT numerical-analysis notes](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf)
- Observed order from three successively refined grids can be estimated as
  \[
  p_{\rm obs}=\frac{\log(|E_h-E_{h/2}|/|E_{h/2}-E_{h/4}|)}{\log 2},
  \]
  which should approach (2) in the asymptotic regime for this centered stencil. MIT establishes the (O(h^2)) scheme; the ratio is the standard consequence of an error model (E_h=E_*+Ch^p+o(h^p)). — [MIT numerical-analysis notes](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf)
- The expected second-order result assumes adequate smoothness. A square potential makes the wavefunction and its first derivative continuous for constant mass, but higher derivatives change across the interface; therefore fitted orders can deviate from an ideal value on coarse grids or when the discontinuity is not represented consistently across refinements. — continuity conditions: [University of Texas finite-well treatment](https://farside.ph.utexas.edu/teaching/355/Surveyhtml/node181.html); smoothness requirement for the truncation derivation: [MIT Introduction to Numerical Analysis](https://live.ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/aab35b69b416758992779e2ad508b286_MIT18_330S12_Chapter2.pdf)

### Inferences
- Grid study: fix the physical domain and potential/interface locations, use nested grids whose nodes represent interfaces consistently, compute (E_h), exact/reference energy, absolute and relative errors, and (p_{\rm obs}). For the infinite well, also assert agreement with (E_{n,h}) close to floating-point/eigensolver tolerance before interpreting continuum error. — exact formulas from [MIT numerical-analysis notes](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf)
- Domain study: hold (h) approximately identical and increase only the exterior padding (p); compare each bound-state energy to the largest-domain value and monitor boundary-guard probability. If changing domain requires an integer node count, record the actual (h) so residual grid effects remain visible. — physical tail from [Caltech finite-well notes](https://www.preskill.caltech.edu/ph12b/Ph12b-finite-well-4mar2010.pdf)
- A useful automated validation matrix includes: positive ordered energies; exact state count below (V_0) versus reference roots; (int|\psi_n|^2dx\approx1); overlap matrix near identity; Dirichlet endpoints; finite-well parity; small relative residuals; infinite-well (L^{-2}) and (m^{-1}) scaling; second-order grid trend; and fixed-(h) domain stability. Each check targets a different failure mode supported by the cited analytical, numerical, or physical constraints. — [MIT quantum notes](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/a565b327f85c7721b18f1074dbd69ede_MIT8_04S16_LecNotes11.pdf); [SciPy `eigh_tridiagonal`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html); [MIT numerical-analysis notes](https://math.mit.edu/icg/resources/teaching/18.330/18.330-Apr-2014.pdf)

### Gaps
- Interface discontinuities can reduce or obscure the asymptotic order on practical grids. The reviewed sources establish the stencil's smooth-function order but do not provide a square-well-specific theorem for the eigenvalue order; the project should report measured slopes and avoid asserting exactly second-order behavior where the data do not support it. — [MIT Introduction to Numerical Analysis](https://live.ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/aab35b69b416758992779e2ad508b286_MIT18_330S12_Chapter2.pdf)
