"""Execute the complete deterministic experiment suite and write artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from quantum_confinement.constants import MEV_PER_EV
from quantum_confinement.models import (
    HeterostructureParameters,
    finite_square_well,
    infinite_square_well,
    semiconductor_well,
)
from quantum_confinement.reference import finite_well_reference, infinite_well_energies

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

BLUE = "#135A8A"
CYAN = "#38A6A5"
ORANGE = "#D97732"
INK = "#17242D"
GRID = "#D8E1E6"


def points_for(width_nm: float, padding_nm: float, spacing_nm: float) -> int:
    """Return an odd number of points with the requested approximate spacing."""

    intervals = int(round((width_nm + 2.0 * padding_nm) / spacing_nm))
    if intervals % 2:
        intervals += 1
    return intervals + 1


def configure_plots() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 145,
            "savefig.dpi": 180,
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "axes.edgecolor": "#8A9AA5",
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "grid.color": GRID,
            "grid.linewidth": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save_frame(frame: pd.DataFrame, name: str) -> None:
    frame.to_csv(RESULTS / name, index=False, float_format="%.12g")


def width_scaling() -> tuple[pd.DataFrame, float]:
    rows: list[dict[str, float]] = []
    widths = np.arange(4.0, 20.1, 1.0)
    for width in widths:
        result = infinite_square_well(width, points=1201, number_of_states=3)
        exact = infinite_well_energies(width, 0.067, 3)
        for state in range(3):
            rows.append(
                {
                    "width_nm": width,
                    "state_n": state + 1,
                    "numerical_energy_mev": result.energies_ev[state] * MEV_PER_EV,
                    "analytical_energy_mev": exact[state] * MEV_PER_EV,
                    "absolute_error_uev": abs(result.energies_ev[state] - exact[state]) * 1e6,
                    "relative_error": abs(result.energies_ev[state] / exact[state] - 1.0),
                }
            )
    frame = pd.DataFrame(rows)
    ground = frame[frame.state_n == 1]
    slope = float(np.polyfit(np.log(ground.width_nm), np.log(ground.numerical_energy_mev), 1)[0])

    fig, ax = plt.subplots(figsize=(7.6, 4.7))
    for state, color in zip((1, 2, 3), (BLUE, CYAN, ORANGE), strict=True):
        subset = frame[frame.state_n == state]
        ax.plot(subset.width_nm, subset.numerical_energy_mev, "o", ms=4, color=color, label=f"FD, n={state}")
        ax.plot(subset.width_nm, subset.analytical_energy_mev, "-", lw=1.4, color=color, alpha=0.75)
    ax.set(yscale="log", xscale="log", xlabel="Well width, L (nm)", ylabel="Energy (meV)", title="Infinite-well confinement follows inverse-square scaling")
    ax.grid(True, which="both")
    ax.legend(frameon=False, ncol=3)
    ax.text(0.03, 0.05, f"Fitted ground-state log slope = {slope:.6f}", transform=ax.transAxes)
    fig.tight_layout()
    fig.savefig(FIGURES / "width_scaling.png")
    plt.close(fig)
    return frame, slope


def finite_comparison() -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []
    for width in (4.0, 6.0, 8.0, 10.0):
        infinite = infinite_well_energies(width, 0.067, 6)
        for barrier in (0.150, 0.253, 0.400):
            result = finite_square_well(
                width,
                barrier,
                padding_nm=10.0,
                points=points_for(width, 10.0, 0.01),
                number_of_states=6,
            )
            reference, _ = finite_well_reference(width, barrier, 0.067)
            comparable_count = min(len(reference), int(result.bound_mask.sum()))
            for state, ref_energy in enumerate(reference[:comparable_count]):
                rows.append(
                    {
                        "width_nm": width,
                        "barrier_ev": barrier,
                        "state_n": state + 1,
                        "finite_fd_mev": result.energies_ev[state] * MEV_PER_EV,
                        "finite_reference_mev": ref_energy * MEV_PER_EV,
                        "fd_reference_error_mev": (result.energies_ev[state] - ref_energy) * MEV_PER_EV,
                        "infinite_energy_mev": infinite[state] * MEV_PER_EV,
                        "finite_shift_percent": (result.energies_ev[state] / infinite[state] - 1.0) * 100.0,
                        "leakage_percent": result.leakage_probability[state] * 100.0,
                    }
                )
    frame = pd.DataFrame(rows)
    focus = frame[(frame.width_nm == 8.0) & (frame.state_n <= 2)]
    fig, (left, right) = plt.subplots(1, 2, figsize=(10.5, 4.4))
    for state, color in ((1, BLUE), (2, ORANGE)):
        subset = focus[focus.state_n == state]
        left.plot(subset.barrier_ev, subset.finite_fd_mev, "o-", color=color, label=f"Finite, n={state}")
        left.axhline(subset.infinite_energy_mev.iloc[0], color=color, ls="--", alpha=0.6)
        right.plot(subset.barrier_ev, subset.leakage_percent, "o-", color=color, label=f"n={state}")
    left.set(xlabel="Barrier height (eV)", ylabel="Energy (meV)", title="Finite barriers lower bound-state energies")
    right.set(xlabel="Barrier height (eV)", ylabel="Probability outside well (%)", title="Barrier penetration is physical leakage")
    for axis in (left, right):
        axis.grid(True)
        axis.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "finite_vs_infinite.png")
    plt.close(fig)
    return frame


def state_profiles() -> None:
    result = semiconductor_well(8.0, padding_nm=8.0, points=1201, number_of_states=4)
    bound = np.flatnonzero(result.bound_mask)
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 7.1), sharex=True)
    axes[0].plot(result.x_nm, result.potential_ev * MEV_PER_EV, color=INK, lw=1.5, label="Conduction-band profile")
    amplitude_scale = 20.0
    for idx, color in zip(bound, (BLUE, ORANGE), strict=False):
        axes[0].axhline(result.energies_ev[idx] * MEV_PER_EV, color=color, lw=1.0, alpha=0.65)
        axes[0].plot(
            result.x_nm,
            result.energies_ev[idx] * MEV_PER_EV + amplitude_scale * result.wavefunctions[:, idx],
            color=color,
            label=f"n={idx + 1}: E={result.energies_ev[idx] * 1e3:.2f} meV",
        )
        axes[1].plot(result.x_nm, result.probability_densities_per_nm[:, idx], color=color, label=f"n={idx + 1}")
    axes[0].set(ylabel="Energy (meV)", title="GaAs/Al₀.₃Ga₀.₇As potential, levels, and offset wavefunctions")
    axes[0].text(0.01, 0.03, f"Display convention: E + {amplitude_scale:.0f}·ψ; ψ in nm⁻¹ᐟ²", transform=axes[0].transAxes, fontsize=8)
    axes[1].set(xlabel="Position x (nm)", ylabel="Probability density (nm⁻¹)", title="Spatial probability densities")
    for axis in axes:
        axis.axvspan(-4.0, 4.0, color=CYAN, alpha=0.08)
        axis.grid(True)
        axis.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "state_profiles.png")
    plt.close(fig)


def mass_comparison() -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []
    for width in np.arange(4.0, 12.1, 1.0):
        points = points_for(width, 10.0, 0.01)
        constant = finite_square_well(width, 0.253, mass_ratio=0.067, padding_nm=10.0, points=points, number_of_states=6)
        variable = semiconductor_well(width, padding_nm=10.0, points=points, number_of_states=6)
        reference, _ = finite_well_reference(width, 0.253, 0.067, 0.0919)
        count = min(int(variable.bound_mask.sum()), len(reference), int(constant.bound_mask.sum()))
        for state in range(count):
            rows.append(
                {
                    "width_nm": width,
                    "state_n": state + 1,
                    "constant_mass_mev": constant.energies_ev[state] * MEV_PER_EV,
                    "variable_mass_mev": variable.energies_ev[state] * MEV_PER_EV,
                    "matching_reference_mev": reference[state] * MEV_PER_EV,
                    "mass_model_shift_mev": (variable.energies_ev[state] - constant.energies_ev[state]) * MEV_PER_EV,
                    "bdd_reference_error_mev": (variable.energies_ev[state] - reference[state]) * MEV_PER_EV,
                }
            )
    frame = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(7.6, 4.7))
    for state, color in ((1, BLUE), (2, ORANGE)):
        subset = frame[frame.state_n == state]
        ax.plot(subset.width_nm, subset.mass_model_shift_mev, "o-", color=color, label=f"n={state}")
    ax.axhline(0.0, color=INK, lw=0.8)
    ax.set(xlabel="Well width (nm)", ylabel="BDD variable − constant mass (meV)", title="Barrier-mass mismatch changes predicted confinement energies")
    ax.grid(True)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "effective_mass_comparison.png")
    plt.close(fig)
    return frame


def numerical_accuracy() -> tuple[pd.DataFrame, pd.DataFrame, float]:
    width, padding, barrier = 8.0, 8.0, 0.253
    reference = finite_well_reference(width, barrier, 0.067, 0.0919)[0][0]
    grid_rows: list[dict[str, float | int]] = []
    for spacing in (0.16, 0.08, 0.04, 0.02, 0.01):
        result = semiconductor_well(width, padding_nm=padding, points=points_for(width, padding, spacing), number_of_states=2)
        grid_rows.append(
            {
                "spacing_nm": spacing,
                "points": result.x_nm.size,
                "ground_energy_mev": result.energies_ev[0] * MEV_PER_EV,
                "matching_error_mev": (result.energies_ev[0] - reference) * MEV_PER_EV,
                "residual": result.residuals[0],
            }
        )
    grid = pd.DataFrame(grid_rows)
    errors = np.abs(grid.matching_error_mev.to_numpy())
    observed_order = float(np.polyfit(np.log(grid.spacing_nm.iloc[-3:]), np.log(errors[-3:]), 1)[0])

    domain_rows: list[dict[str, float | int]] = []
    for pad in (2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 12.0):
        result = semiconductor_well(width, padding_nm=pad, points=points_for(width, pad, 0.02), number_of_states=2)
        domain_rows.append(
            {
                "padding_nm": pad,
                "points": result.x_nm.size,
                "ground_energy_mev": result.energies_ev[0] * MEV_PER_EV,
                "matching_error_mev": (result.energies_ev[0] - reference) * MEV_PER_EV,
                "boundary_guard_probability": result.boundary_guard_probability[0],
            }
        )
    domain = pd.DataFrame(domain_rows)

    fig, (left, right) = plt.subplots(1, 2, figsize=(10.5, 4.4))
    left.loglog(grid.spacing_nm, np.abs(grid.matching_error_mev), "o-", color=BLUE)
    left.set(xlabel="Grid spacing h (nm)", ylabel="|FD − matching| (meV)", title=f"Grid error; fitted fine-grid order {observed_order:.2f}")
    right.semilogy(domain.padding_nm, np.abs(domain.matching_error_mev), "o-", color=ORANGE, label="Energy error")
    right.semilogy(domain.padding_nm, domain.boundary_guard_probability, "s--", color=CYAN, label="Boundary-guard probability")
    right.set(xlabel="Exterior padding per side (nm)", ylabel="Error / probability", title="Domain truncation decays with padding")
    for axis in (left, right):
        axis.grid(True, which="both")
    right.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "numerical_convergence.png")
    plt.close(fig)
    return grid, domain, observed_order


def parameter_sensitivity() -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    scenarios = [
        ("offset low", 0.067, 0.0919, 0.244),
        ("baseline", 0.067, 0.0919, 0.253),
        ("offset high", 0.067, 0.0919, 0.261),
        ("300 K-inspired masses", 0.063, 0.0879, 0.253),
    ]
    for label, well_mass, barrier_mass, offset in scenarios:
        parameters = HeterostructureParameters(0.30, well_mass, barrier_mass, offset, label, "sensitivity scenario")
        result = semiconductor_well(8.0, parameters, padding_nm=10.0, points=2801, number_of_states=4)
        for state in np.flatnonzero(result.bound_mask):
            rows.append(
                {
                    "scenario": label,
                    "well_mass_ratio": well_mass,
                    "barrier_mass_ratio": barrier_mass,
                    "offset_ev": offset,
                    "state_n": int(state + 1),
                    "energy_mev": result.energies_ev[state] * MEV_PER_EV,
                    "leakage_percent": result.leakage_probability[state] * 100.0,
                }
            )
    frame = pd.DataFrame(rows)
    pivot = frame.pivot(index="scenario", columns="state_n", values="energy_mev").reindex([s[0] for s in scenarios])
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    pivot.plot.bar(ax=ax, color=[BLUE, ORANGE], width=0.7)
    ax.set(ylabel="Bound-state energy (meV)", xlabel="", title="Sensitivity to literature-supported parameter assumptions")
    ax.legend(title="State n", frameon=False)
    ax.tick_params(axis="x", rotation=12)
    ax.grid(True, axis="y")
    fig.tight_layout()
    fig.savefig(FIGURES / "parameter_sensitivity.png")
    plt.close(fig)
    return frame


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    configure_plots()
    width, slope = width_scaling()
    finite = finite_comparison()
    state_profiles()
    mass = mass_comparison()
    grid, domain, order = numerical_accuracy()
    sensitivity = parameter_sensitivity()
    save_frame(width, "width_scaling.csv")
    save_frame(finite, "finite_vs_infinite.csv")
    save_frame(mass, "effective_mass_comparison.csv")
    save_frame(grid, "grid_convergence.csv")
    save_frame(domain, "domain_convergence.csv")
    save_frame(sensitivity, "parameter_sensitivity.csv")

    focus_finite = finite[(finite.width_nm == 8.0) & (finite.barrier_ev == 0.253)]
    focus_mass = mass[(mass.width_nm == 8.0)]
    baseline_sensitivity = sensitivity[sensitivity.scenario == "baseline"]
    summary = {
        "generated_by": "experiments/run_all.py",
        "width_scaling_ground_state_log_slope": slope,
        "grid_observed_order_last_three": order,
        "infinite_well_max_relative_error": float(width.relative_error.max()),
        "finite_reference_max_abs_error_mev": float(finite.fd_reference_error_mev.abs().max()),
        "bdd_reference_max_abs_error_mev": float(mass.bdd_reference_error_mev.abs().max()),
        "eight_nm_253mev": focus_finite.to_dict(orient="records"),
        "eight_nm_mass_model": focus_mass.to_dict(orient="records"),
        "baseline_heterostructure": baseline_sensitivity.to_dict(orient="records"),
        "domain_12nm_error_mev": float(domain.iloc[-1].matching_error_mev),
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
