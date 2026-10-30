"""Independent continuum and discrete reference calculations."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import brentq

from .constants import HBAR2_OVER_2M0_EV_NM2

FloatArray = NDArray[np.float64]


def _positive(value: float, name: str) -> float:
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return float(value)


def infinite_well_energies(width_nm: float, mass_ratio: float, number_of_states: int) -> FloatArray:
    """Continuum infinite-square-well energies in eV."""

    width = _positive(width_nm, "width_nm")
    mass = _positive(mass_ratio, "mass_ratio")
    if not isinstance(number_of_states, int) or number_of_states < 1:
        raise ValueError("number_of_states must be a positive integer")
    n = np.arange(1, number_of_states + 1, dtype=float)
    return HBAR2_OVER_2M0_EV_NM2 * (np.pi * n / width) ** 2 / mass


def discrete_infinite_well_energies(
    width_nm: float,
    mass_ratio: float,
    number_of_intervals: int,
    number_of_states: int,
) -> FloatArray:
    """Exact eigenvalues of the centered Dirichlet second-difference matrix."""

    width = _positive(width_nm, "width_nm")
    mass = _positive(mass_ratio, "mass_ratio")
    if number_of_intervals < 2 or number_of_states < 1 or number_of_states >= number_of_intervals:
        raise ValueError("require intervals >= 2 and 1 <= states < intervals")
    h = width / number_of_intervals
    n = np.arange(1, number_of_states + 1, dtype=float)
    return 4.0 * HBAR2_OVER_2M0_EV_NM2 / (mass * h**2) * np.sin(n * np.pi / (2 * number_of_intervals)) ** 2


def finite_well_reference(
    width_nm: float,
    barrier_ev: float,
    well_mass_ratio: float,
    barrier_mass_ratio: float | None = None,
) -> tuple[FloatArray, tuple[str, ...]]:
    """Bound energies from independent parity matching equations.

    Supports both ordinary constant-mass matching and BDD mass-mismatched
    matching. The search is branch-aware and never brackets across a pole.
    """

    width = _positive(width_nm, "width_nm")
    barrier = _positive(barrier_ev, "barrier_ev")
    well_mass = _positive(well_mass_ratio, "well_mass_ratio")
    barrier_mass = well_mass if barrier_mass_ratio is None else _positive(barrier_mass_ratio, "barrier_mass_ratio")
    half_width = width / 2.0
    z0 = half_width * np.sqrt(barrier * well_mass / HBAR2_OVER_2M0_EV_NM2)

    def decay_coordinate(z: float) -> float:
        return float(np.sqrt(max(0.0, (barrier_mass / well_mass) * (z0**2 - z**2))))

    def even_equation(z: float) -> float:
        return (z / well_mass) * np.tan(z) - decay_coordinate(z) / barrier_mass

    def odd_equation(z: float) -> float:
        return (z / well_mass) / np.tan(z) + decay_coordinate(z) / barrier_mass

    roots: list[tuple[float, str]] = []
    epsilon = 1e-10
    branch = 0
    while branch * np.pi < z0:
        even_left = branch * np.pi + (epsilon if branch else epsilon)
        even_right = min(branch * np.pi + np.pi / 2.0, z0) - epsilon
        if even_right > even_left:
            f_left, f_right = even_equation(even_left), even_equation(even_right)
            if np.isfinite(f_left) and np.isfinite(f_right) and f_left * f_right < 0.0:
                roots.append((brentq(even_equation, even_left, even_right, xtol=1e-13), "even"))
        odd_left = branch * np.pi + np.pi / 2.0 + epsilon
        odd_right = min((branch + 1) * np.pi, z0) - epsilon
        if odd_right > odd_left:
            f_left, f_right = odd_equation(odd_left), odd_equation(odd_right)
            if np.isfinite(f_left) and np.isfinite(f_right) and f_left * f_right < 0.0:
                roots.append((brentq(odd_equation, odd_left, odd_right, xtol=1e-13), "odd"))
        branch += 1

    roots.sort(key=lambda item: item[0])
    energies = np.asarray(
        [HBAR2_OVER_2M0_EV_NM2 * (z / half_width) ** 2 / well_mass for z, _ in roots],
        dtype=float,
    )
    return energies, tuple(parity for _, parity in roots)
