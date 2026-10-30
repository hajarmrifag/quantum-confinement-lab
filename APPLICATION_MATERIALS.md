# Application materials

## CV entry

**Quantum Confinement Lab — Numerical Modelling and Validation of Semiconductor Quantum Wells**  
GitHub: <https://github.com/hajarmrifag/quantum-confinement-lab>

- Built a Python/SciPy finite-difference eigensolver for infinite, finite, and GaAs/Al₀.₃Ga₀.₇As quantum wells, including a Hermitian BenDaniel–Duke operator for discontinuous effective mass and a tested Streamlit exploration interface.
- Independently validated finite-well states with parity-matching equations; for an 8 nm, 0.253 eV well, resolved BDD levels at 42.049 and 162.242 meV within 0.069 and 0.244 meV of matching references, with explicit grid and domain convergence analysis.

## nanoGUNE motivation paragraph

I explored quantum confinement because I wanted to test whether the habits I developed in scientific Python and performance-oriented software work—breaking a computation into assumptions, numerical methods, and measurable error—would transfer to a physical problem outside my degree. Building the project made the distinction between “the code converged” and “the model is justified” much more concrete: I had to compare finite and infinite barriers, implement the correct flux-form operator when the effective mass changes at an interface, and validate the results against separate analytical matching equations. I also learned how strongly a prediction can depend on an idealized material parameter or an artificial computational boundary. That experience has made me more interested in the point where models meet real structures, and I want to attend the nanoGUNE Winter School to learn how nanofabrication and experimental measurements constrain, challenge, and improve the kinds of simulations I can currently build.

## Accuracy note for the applicant

Review `SCIENTIFIC_REPORT.md`, run the application, and work through `docs/INTERVIEW_GUIDE.md` before using these statements. The values are computed results of an idealized one-dimensional model, not experimental measurements.
