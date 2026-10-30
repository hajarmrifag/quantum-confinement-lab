"""Interactive scientific companion for the Quantum Confinement Lab."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from quantum_confinement.models import finite_square_well, infinite_square_well, semiconductor_well
from quantum_confinement.reference import finite_well_reference, infinite_well_energies

st.set_page_config(page_title="Quantum Confinement Lab", page_icon="◈", layout="wide")

st.markdown(
    """
<style>
:root { --ink:#17242d; --muted:#5b6c76; --blue:#135a8a; --cyan:#38a6a5; --paper:#f5f7f6; }
.stApp { background: linear-gradient(180deg,#f7f9f8 0,#eef3f3 100%); color:var(--ink); }
[data-testid="stSidebar"] { background:#102a38; }
[data-testid="stSidebar"] * { color:#f4f8f8 !important; }
[data-testid="stSidebar"] input { color:#102a38 !important; }
.hero { padding:2.1rem 0 1.15rem; border-bottom:1px solid #cbd7db; margin-bottom:1.1rem; }
.eyebrow { color:#247b86; font:700 .74rem/1.2 system-ui; letter-spacing:.16em; text-transform:uppercase; }
.hero h1 { font:600 clamp(2rem,4vw,3.5rem)/1.04 Georgia,serif; letter-spacing:-.035em; margin:.4rem 0 .65rem; color:#102a38; }
.hero p { max-width:850px; color:#50636d; font-size:1.03rem; line-height:1.6; }
.model-note { padding:.85rem 1rem; border-left:3px solid #38a6a5; background:#fff; color:#42545e; margin:.4rem 0 1rem; }
[data-testid="stMetric"] { background:#fff; border:1px solid #d8e1e4; padding:.8rem 1rem; border-radius:4px; }
[data-testid="stMetricLabel"] { color:#5b6c76; }
.smallcap { color:#5b6c76; font-size:.82rem; line-height:1.45; }
@media (max-width: 700px) { .hero {padding-top:1rem}.hero h1{font-size:2rem} }
</style>
<div class="hero">
  <div class="eyebrow">Computational physics · validated models</div>
  <h1>Quantum Confinement Lab</h1>
  <p>Explore how well width, barrier height, and effective-mass assumptions change electron states—and keep physical-model differences separate from numerical approximation error.</p>
</div>
""",
    unsafe_allow_html=True,
)


def point_count(width: float, padding: float, spacing: float) -> int:
    intervals = max(80, int(round((width + 2 * padding) / spacing)))
    return intervals + (intervals % 2) + 1


@st.cache_data(show_spinner=False)
def calculate(model: str, width: float, barrier: float, mass: float, padding: float, spacing: float, states: int):
    if model == "Infinite square well":
        return infinite_square_well(width, mass, states, max(101, int(round(width / spacing)) + 1))
    points = point_count(width, padding, spacing)
    if model == "Finite square well":
        return finite_square_well(width, barrier, mass, padding, states, points)
    return semiconductor_well(width, padding_nm=padding, number_of_states=states, points=points)


with st.sidebar:
    st.markdown("### Model controls")
    model = st.selectbox("Physical model", ["GaAs / AlGaAs heterostructure", "Finite square well", "Infinite square well"])
    width = st.slider("Well width L (nm)", 3.0, 20.0, 8.0, 0.5)
    barrier = st.slider("Barrier height V₀ (eV)", 0.05, 0.50, 0.253, 0.005, disabled=model != "Finite square well")
    mass = st.slider("Effective mass m*/m₀", 0.04, 0.20, 0.067, 0.001, disabled=model == "GaAs / AlGaAs heterostructure")
    padding = st.slider("Exterior padding per side (nm)", 2.0, 16.0, 8.0, 1.0, disabled=model == "Infinite square well")
    spacing = st.select_slider("Grid spacing target (nm)", [0.20, 0.10, 0.05, 0.025], value=0.05)
    requested_states = st.slider("Computed low-energy states", 2, 8, 5)
    st.markdown("---")
    st.caption("All energies are recomputed from the symmetric tridiagonal Hamiltonian when a control changes.")

result = calculate(model, width, barrier, mass, padding, spacing, requested_states)
bound_indices = np.flatnonzero(result.bound_mask)
display_indices = np.arange(result.energies_ev.size) if model == "Infinite square well" else bound_indices

if model == "Infinite square well":
    reference = infinite_well_energies(width, mass, requested_states)
    reference_name = "continuum analytical"
elif model == "Finite square well":
    reference, _ = finite_well_reference(width, barrier, mass)
    reference_name = "parity matching"
else:
    reference, _ = finite_well_reference(width, 0.253, 0.067, 0.0919)
    reference_name = "BDD parity matching"

tab_explore, tab_compare, tab_accuracy, tab_methods = st.tabs(["State explorer", "Model comparison", "Numerical QA", "Methods & scope"])

with tab_explore:
    if not len(display_indices):
        st.warning("No bound state was resolved below the selected barrier on this domain.")
    else:
        first = display_indices[0]
        error = abs(result.energies_ev[first] - reference[first]) * 1e3 if len(reference) > first else float("nan")
        cols = st.columns(4)
        cols[0].metric("Bound states", len(display_indices))
        cols[1].metric("Ground energy", f"{result.energies_ev[first] * 1e3:.3f} meV")
        cols[2].metric(f"Error vs {reference_name}", f"{error:.3f} meV")
        cols[3].metric("Ground-state leakage", f"{result.leakage_probability[first] * 100:.2f}%")

        if model == "GaAs / AlGaAs heterostructure":
            st.markdown('<div class="model-note"><strong>Baseline:</strong> idealized low-temperature GaAs/Al₀.₃Ga₀.₇As; m<sub>w</sub>*=0.067m₀, m<sub>b</sub>*=0.0919m₀, V₀=0.253 eV. The kinetic operator is BenDaniel–Duke divergence form.</div>', unsafe_allow_html=True)

        potential = go.Figure()
        potential.add_trace(go.Scatter(x=result.x_nm, y=result.potential_ev * 1e3, name="Potential", line=dict(color="#17242d", width=2)))
        amplitude = max(8.0, float((result.potential_ev.max() if result.barrier_ev else result.energies_ev[-1]) * 1e3 * 0.10))
        palette = ["#135a8a", "#d97732", "#38a6a5", "#835f95", "#9b8b3b", "#556b77"]
        for color, idx in zip(palette, display_indices, strict=False):
            base = result.energies_ev[idx] * 1e3
            potential.add_trace(go.Scatter(x=result.x_nm, y=base + amplitude * result.wavefunctions[:, idx], name=f"ψ{idx + 1} offset from {base:.1f} meV", line=dict(color=color)))
            potential.add_hline(y=base, line_width=1, line_dash="dot", line_color=color, opacity=0.45)
        potential.update_layout(title="Potential energy, eigenlevels, and offset wavefunctions", xaxis_title="Position x (nm)", yaxis_title="Energy (meV)", height=480, margin=dict(l=20, r=20, t=55, b=30), legend=dict(orientation="h", y=-0.20), template="plotly_white")
        st.plotly_chart(potential, width="stretch")
        st.caption(f"Wavefunction display convention: Eₙ + {amplitude:.1f} ψₙ. The vertical wavefunction scale is intentionally artificial; energies and probability densities retain physical units.")

        density = go.Figure()
        for color, idx in zip(palette, display_indices, strict=False):
            density.add_trace(go.Scatter(x=result.x_nm, y=result.probability_densities_per_nm[:, idx], name=f"|ψ{idx + 1}|²", line=dict(color=color), fill="tozeroy" if idx == first else None, opacity=0.88))
        density.add_vrect(x0=-width / 2, x1=width / 2, fillcolor="#38a6a5", opacity=0.07, line_width=0)
        density.update_layout(title="Normalized probability densities", xaxis_title="Position x (nm)", yaxis_title="Probability density (nm⁻¹)", height=390, margin=dict(l=20, r=20, t=55, b=30), template="plotly_white")
        st.plotly_chart(density, width="stretch")

        count = min(len(display_indices), len(reference))
        table = pd.DataFrame(
            {
                "state n": display_indices[:count] + 1,
                "finite-difference E (meV)": result.energies_ev[display_indices[:count]] * 1e3,
                f"{reference_name} E (meV)": reference[:count] * 1e3,
                "difference (meV)": (result.energies_ev[display_indices[:count]] - reference[:count]) * 1e3,
                "outside probability (%)": result.leakage_probability[display_indices[:count]] * 100,
                "relative residual": result.residuals[display_indices[:count]],
            }
        )
        st.dataframe(table.style.format(precision=5), width="stretch", hide_index=True)

with tab_compare:
    widths = np.linspace(4.0, 18.0, 15)
    infinite_ground = np.array([infinite_well_energies(value, 0.067, 1)[0] for value in widths])
    finite_ground = np.array([finite_well_reference(value, 0.253, 0.067)[0][0] for value in widths])
    bdd_ground = np.array([finite_well_reference(value, 0.253, 0.067, 0.0919)[0][0] for value in widths])
    comparison = go.Figure()
    comparison.add_trace(go.Scatter(x=widths, y=infinite_ground * 1e3, name="Infinite, m*=0.067m₀", line=dict(color="#17242d", dash="dash")))
    comparison.add_trace(go.Scatter(x=widths, y=finite_ground * 1e3, name="Finite, constant mass", line=dict(color="#135a8a")))
    comparison.add_trace(go.Scatter(x=widths, y=bdd_ground * 1e3, name="Finite, BDD mass mismatch", line=dict(color="#d97732")))
    comparison.update_layout(title="Ground-state energy versus confinement width", xaxis_title="Well width (nm)", yaxis_title="Energy (meV)", height=480, template="plotly_white", margin=dict(l=20, r=20, t=55, b=30))
    st.plotly_chart(comparison, width="stretch")
    shift = (bdd_ground - finite_ground) * 1e3
    st.markdown(f"At **8 nm**, replacing the constant barrier mass by the GaAs/AlGaAs BDD mass profile changes the matching-reference ground energy by **{np.interp(8, widths, shift):.3f} meV**. This is a model-assumption difference, not a grid error.")

with tab_accuracy:
    st.markdown("### Grid refinement at fixed physical domain")
    if model == "Infinite square well":
        spacings = np.array([0.20, 0.10, 0.05, 0.025])
        values = np.array([calculate(model, width, barrier, mass, padding, float(h), 2).energies_ev[0] for h in spacings])
        target = infinite_well_energies(width, mass, 1)[0]
    else:
        spacings = np.array([0.20, 0.10, 0.05, 0.025])
        values = np.array([calculate(model, width, barrier, mass, padding, float(h), 2).energies_ev[0] for h in spacings])
        target = reference[0]
    convergence = go.Figure(go.Scatter(x=spacings, y=np.abs(values - target) * 1e3, mode="lines+markers", line=dict(color="#135a8a")))
    convergence.update_xaxes(type="log", autorange="reversed", title="Target grid spacing h (nm)")
    convergence.update_yaxes(type="log", title=f"|FD − {reference_name}| (meV)")
    convergence.update_layout(title="Reference error under grid refinement", height=390, template="plotly_white", margin=dict(l=20, r=20, t=55, b=30))
    st.plotly_chart(convergence, width="stretch")
    c1, c2, c3 = st.columns(3)
    c1.metric("Max normalization error", f"{np.max(np.abs(result.normalization - 1)):.2e}")
    c2.metric("Max orthogonality error", f"{np.max(np.abs(result.overlap_matrix - np.eye(requested_states))):.2e}")
    c3.metric("Max eigenpair residual", f"{result.residuals.max():.2e}")
    st.info("For abrupt square potentials and discontinuous masses, interface placement can make the observed energy convergence close to first order. The report measures this behavior rather than assuming ideal second order.")

with tab_methods:
    st.markdown(
        """
### What is calculated

The code solves the one-dimensional time-independent Schrödinger eigenproblem on a uniform grid. Infinite and ordinary finite wells use the constant-mass operator. The semiconductor model uses

$$H=-\frac{\hbar^2}{2}\frac{d}{dx}\left[\frac{1}{m^*(x)}\frac{d}{dx}\right]+V(x),$$

with shared reciprocal-mass face coefficients, so the discrete tridiagonal Hamiltonian is explicitly real symmetric. At an abrupt interface this corresponds to continuity of the envelope $\psi$ and of $(1/m^*)\,d\psi/dx$.

### Independent checks

- Infinite-well results are compared with both the continuum spectrum and exact eigenvalues of the discrete Dirichlet Laplacian.
- Finite constant-mass states are compared with even/odd transcendental matching equations.
- GaAs/AlGaAs states are compared with unequal-mass BenDaniel–Duke matching equations.
- Bound states require $E<V_0$; above-barrier box states are never labelled confined states.

### Scope

This is a one-band, one-dimensional envelope-function model of an idealized, abrupt, unstrained structure. It omits nonparabolicity, multiband coupling, strain, alloy disorder, roughness, electrostatics, carrier interactions, and temperature dependence beyond selected bulk inputs. It is a numerical investigation—not experimental verification or a device prediction.
"""
    )
