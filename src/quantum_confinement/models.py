"""Physical model constructors and state diagnostics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .numerics import assemble_hamiltonian, solve_hamiltonian, tridiagonal_residuals

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class HeterostructureParameters:
    """Idealized bulk inputs for an abrupt symmetric heterostructure."""

    alloy_fraction: float
    well_mass_ratio: float
    barrier_mass_ratio: float
    conduction_offset_ev: float
    temperature_label: str
    source_note: str


GAAS_ALGAAS_BASELINE = HeterostructureParameters(
    alloy_fraction=0.30,
    well_mass_ratio=0.067,
    barrier_mass_ratio=0.0919,
    conduction_offset_ev=0.253,
    temperature_label="low-temperature bulk parameters",
    source_note="Vurgaftman et al. (2001) interpolation; Yi et al. (2009) Qc=0.604",
)


@dataclass(frozen=True)
class SolveResult:
    """Eigenstates plus numerical and physical diagnostics."""

    model: str
    x_nm: FloatArray
    potential_ev: FloatArray
    mass_ratio: FloatArray
    energies_ev: FloatArray
    wavefunctions: FloatArray
    residuals: FloatArray
    bound_mask: NDArray[np.bool_]
    well_width_nm: float
    barrier_ev: float | None

    @property
    def probability_densities_per_nm(self) -> FloatArray:
        return self.wavefunctions**2

    @property
    def normalization(self) -> FloatArray:
        return np.asarray([np.trapezoid(state**2, x=self.x_nm) for state in self.wavefunctions.T])

    @property
    def overlap_matrix(self) -> FloatArray:
        states = self.wavefunctions
        return np.asarray(
            [[np.trapezoid(states[:, i] * states[:, j], x=self.x_nm) for j in range(states.shape[1])] for i in range(states.shape[1])]
        )

    @property
    def leakage_probability(self) -> FloatArray:
        outside = np.abs(self.x_nm) > self.well_width_nm / 2.0
        if self.model == "infinite":
            return np.zeros(self.energies_ev.size)
        return np.asarray(
            [np.trapezoid(np.where(outside, state**2, 0.0), x=self.x_nm) for state in self.wavefunctions.T]
        )

    @property
    def boundary_guard_probability(self) -> FloatArray:
        domain_width = self.x_nm[-1] - self.x_nm[0]
        guard = (self.x_nm < self.x_nm[0] + 0.05 * domain_width) | (self.x_nm > self.x_nm[-1] - 0.05 * domain_width)
        return np.asarray(
            [np.trapezoid(np.where(guard, state**2, 0.0), x=self.x_nm) for state in self.wavefunctions.T]
        )


def _validate_common(width_nm: float, mass_ratio: float, number_of_states: int, points: int) -> None:
    if not np.isfinite(width_nm) or width_nm <= 0.0:
        raise ValueError("width_nm must be finite and positive")
    if not np.isfinite(mass_ratio) or mass_ratio <= 0.0:
        raise ValueError("mass_ratio must be finite and positive")
    if not isinstance(number_of_states, int) or number_of_states < 1:
        raise ValueError("number_of_states must be a positive integer")
    if not isinstance(points, int) or points < number_of_states + 3:
        raise ValueError("points must be an integer large enough for the requested states")


def _result(
    model: str,
    x: FloatArray,
    potential: FloatArray,
    mass: FloatArray,
    states: int,
    width: float,
    barrier: float | None,
) -> SolveResult:
    hamiltonian = assemble_hamiltonian(x, potential, mass)
    energies, wavefunctions = solve_hamiltonian(hamiltonian, states)
    residuals = tridiagonal_residuals(hamiltonian, energies, wavefunctions)
    bound = np.ones(states, dtype=bool) if barrier is None else energies < barrier
    return SolveResult(model, x, potential, mass, energies, wavefunctions, residuals, bound, width, barrier)


def infinite_square_well(
    width_nm: float,
    mass_ratio: float = 0.067,
    number_of_states: int = 4,
    points: int = 801,
) -> SolveResult:
    """Solve an infinite well centered on zero with Dirichlet walls."""

    _validate_common(width_nm, mass_ratio, number_of_states, points)
    x = np.linspace(-width_nm / 2.0, width_nm / 2.0, points)
    potential = np.zeros_like(x)
    mass = np.full_like(x, mass_ratio)
    return _result("infinite", x, potential, mass, number_of_states, width_nm, None)


def finite_square_well(
    width_nm: float,
    barrier_ev: float,
    mass_ratio: float = 0.067,
    padding_nm: float = 10.0,
    number_of_states: int = 6,
    points: int = 1401,
) -> SolveResult:
    """Solve a symmetric constant-mass finite well on a padded domain."""

    _validate_common(width_nm, mass_ratio, number_of_states, points)
    if not np.isfinite(barrier_ev) or barrier_ev <= 0.0:
        raise ValueError("barrier_ev must be finite and positive")
    if not np.isfinite(padding_nm) or padding_nm <= 0.0:
        raise ValueError("padding_nm must be finite and positive")
    half_domain = width_nm / 2.0 + padding_nm
    x = np.linspace(-half_domain, half_domain, points)
    potential = np.where(np.abs(x) <= width_nm / 2.0, 0.0, barrier_ev)
    mass = np.full_like(x, mass_ratio)
    return _result("finite", x, potential, mass, number_of_states, width_nm, barrier_ev)


def semiconductor_well(
    width_nm: float,
    parameters: HeterostructureParameters = GAAS_ALGAAS_BASELINE,
    padding_nm: float = 10.0,
    number_of_states: int = 6,
    points: int = 1401,
) -> SolveResult:
    """Solve an idealized abrupt GaAs/AlGaAs well with the BDD operator."""

    _validate_common(width_nm, parameters.well_mass_ratio, number_of_states, points)
    if parameters.barrier_mass_ratio <= 0.0 or parameters.conduction_offset_ev <= 0.0:
        raise ValueError("heterostructure masses and offset must be positive")
    if padding_nm <= 0.0:
        raise ValueError("padding_nm must be positive")
    half_domain = width_nm / 2.0 + padding_nm
    x = np.linspace(-half_domain, half_domain, points)
    inside = np.abs(x) <= width_nm / 2.0
    potential = np.where(inside, 0.0, parameters.conduction_offset_ev)
    mass = np.where(inside, parameters.well_mass_ratio, parameters.barrier_mass_ratio)
    return _result(
        "heterostructure",
        x,
        potential,
        mass,
        number_of_states,
        width_nm,
        parameters.conduction_offset_ev,
    )
