"""Symmetric tridiagonal finite-difference machinery.

The kinetic operator is discretized in BenDaniel--Duke divergence form,
``-d/dx[(1/m*) d/dx]``. Constant mass is an exact special case.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import eigh_tridiagonal

from .constants import HBAR2_OVER_2M0_EV_NM2

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class TridiagonalHamiltonian:
    """Interior-grid representation with homogeneous Dirichlet endpoints."""

    x_nm: FloatArray
    potential_ev: FloatArray
    mass_ratio: FloatArray
    diagonal_ev: FloatArray
    off_diagonal_ev: FloatArray

    @property
    def spacing_nm(self) -> float:
        return float(self.x_nm[1] - self.x_nm[0])

    def dense(self) -> FloatArray:
        matrix = np.diag(self.diagonal_ev)
        matrix += np.diag(self.off_diagonal_ev, 1)
        matrix += np.diag(self.off_diagonal_ev, -1)
        return matrix


def _as_positive_profile(value: float | FloatArray, size: int, name: str) -> FloatArray:
    profile = np.full(size, value, dtype=float) if np.isscalar(value) else np.asarray(value, dtype=float)
    if profile.shape != (size,):
        raise ValueError(f"{name} must be scalar or have one value per grid point")
    if not np.all(np.isfinite(profile)) or np.any(profile <= 0.0):
        raise ValueError(f"{name} must contain finite positive values")
    return profile


def assemble_hamiltonian(
    x_nm: FloatArray,
    potential_ev: FloatArray,
    mass_ratio: float | FloatArray,
) -> TridiagonalHamiltonian:
    """Assemble a Hermitian BDD Hamiltonian on a uniform full grid.

    The first and last grid values are Dirichlet boundaries and are excluded
    from the matrix. Face reciprocal masses are arithmetic averages of
    reciprocal nodal masses, equivalently harmonic averages of nodal masses.
    """

    x = np.asarray(x_nm, dtype=float)
    potential = np.asarray(potential_ev, dtype=float)
    if x.ndim != 1 or x.size < 4:
        raise ValueError("x_nm must be a one-dimensional grid with at least four points")
    if potential.shape != x.shape or not np.all(np.isfinite(potential)):
        raise ValueError("potential_ev must be finite and match x_nm")
    differences = np.diff(x)
    if not np.all(differences > 0.0) or not np.allclose(differences, differences[0], rtol=1e-10, atol=1e-13):
        raise ValueError("x_nm must be strictly increasing and uniformly spaced")

    mass = _as_positive_profile(mass_ratio, x.size, "mass_ratio")
    inverse_mass = 1.0 / mass
    face_inverse_mass = 0.5 * (inverse_mass[:-1] + inverse_mass[1:])
    coefficient = HBAR2_OVER_2M0_EV_NM2 / differences[0] ** 2
    diagonal = coefficient * (face_inverse_mass[:-1] + face_inverse_mass[1:]) + potential[1:-1]
    off_diagonal = -coefficient * face_inverse_mass[1:-1]
    return TridiagonalHamiltonian(x, potential, mass, diagonal, off_diagonal)


def solve_hamiltonian(
    hamiltonian: TridiagonalHamiltonian,
    number_of_states: int,
) -> tuple[FloatArray, FloatArray]:
    """Return low-energy eigenvalues and spatially normalized full-grid states."""

    dimension = hamiltonian.diagonal_ev.size
    if not isinstance(number_of_states, int) or number_of_states < 1 or number_of_states > dimension:
        raise ValueError("number_of_states must be between 1 and the interior grid size")
    energies, vectors = eigh_tridiagonal(
        hamiltonian.diagonal_ev,
        hamiltonian.off_diagonal_ev,
        select="i",
        select_range=(0, number_of_states - 1),
        check_finite=True,
    )
    wavefunctions = np.zeros((hamiltonian.x_nm.size, number_of_states), dtype=float)
    wavefunctions[1:-1, :] = vectors
    for index in range(number_of_states):
        norm = np.sqrt(np.trapezoid(wavefunctions[:, index] ** 2, x=hamiltonian.x_nm))
        wavefunctions[:, index] /= norm
        # Deterministic sign convention for reproducible figures and data.
        peak = int(np.argmax(np.abs(wavefunctions[:, index])))
        if wavefunctions[peak, index] < 0.0:
            wavefunctions[:, index] *= -1.0
    return energies.astype(float), wavefunctions


def tridiagonal_residuals(
    hamiltonian: TridiagonalHamiltonian,
    energies_ev: FloatArray,
    wavefunctions: FloatArray,
) -> FloatArray:
    """Compute dimensionless relative residual norms for eigenpairs."""

    residuals: list[float] = []
    for energy, full_state in zip(energies_ev, wavefunctions.T, strict=True):
        state = full_state[1:-1]
        applied = hamiltonian.diagonal_ev * state
        applied[:-1] += hamiltonian.off_diagonal_ev * state[1:]
        applied[1:] += hamiltonian.off_diagonal_ev * state[:-1]
        residual = applied - energy * state
        scale = max(np.linalg.norm(applied), abs(float(energy)) * np.linalg.norm(state), 1e-15)
        residuals.append(float(np.linalg.norm(residual) / scale))
    return np.asarray(residuals)
