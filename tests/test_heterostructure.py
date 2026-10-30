import numpy as np

from quantum_confinement.models import GAAS_ALGAAS_BASELINE, semiconductor_well
from quantum_confinement.numerics import assemble_hamiltonian
from quantum_confinement.reference import finite_well_reference


def _points(width: float, padding: float, spacing: float) -> int:
    return int(round((width + 2 * padding) / spacing)) + 1


def test_bdd_model_matches_independent_mass_mismatch_roots() -> None:
    result = semiconductor_well(8.0, padding_nm=12.0, number_of_states=4, points=_points(8, 12, 0.01))
    reference, parity = finite_well_reference(8.0, 0.253, 0.067, 0.0919)
    assert parity == ("even", "odd")
    np.testing.assert_allclose(result.energies_ev[: len(reference)], reference, atol=3e-4)


def test_bdd_tridiagonal_is_exactly_symmetric() -> None:
    x = np.linspace(-7.0, 7.0, 701)
    inside = np.abs(x) <= 3.0
    potential = np.where(inside, 0.0, 0.253)
    mass = np.where(inside, 0.067, 0.0919)
    hamiltonian = assemble_hamiltonian(x, potential, mass)
    dense = hamiltonian.dense()
    np.testing.assert_array_equal(dense, dense.T)


def test_shared_face_coefficient_uses_harmonic_face_mass() -> None:
    x = np.linspace(-0.2, 0.2, 5)
    mass = np.array([0.067, 0.067, 0.0919, 0.0919, 0.0919])
    hamiltonian = assemble_hamiltonian(x, np.zeros_like(x), mass)
    expected_inverse_face = 0.5 * (1 / mass[1] + 1 / mass[2])
    coefficient = -hamiltonian.off_diagonal_ev[0] * (x[1] - x[0]) ** 2
    from quantum_confinement.constants import HBAR2_OVER_2M0_EV_NM2

    assert np.isclose(coefficient / HBAR2_OVER_2M0_EV_NM2, expected_inverse_face)


def test_constant_mass_limit_matches_equal_mass_reference() -> None:
    parameters = GAAS_ALGAAS_BASELINE.__class__(0.3, 0.067, 0.067, 0.253, "test", "test")
    result = semiconductor_well(8.0, parameters, 10.0, 3, _points(8, 10, 0.01))
    reference = finite_well_reference(8.0, 0.253, 0.067)[0]
    np.testing.assert_allclose(result.energies_ev[: len(reference)], reference, atol=3e-4)


def test_mass_mismatch_changes_prediction_beyond_numerical_tolerance() -> None:
    equal = finite_well_reference(8.0, 0.253, 0.067)[0]
    mismatch = finite_well_reference(8.0, 0.253, 0.067, 0.0919)[0]
    assert abs(mismatch[0] - equal[0]) > 0.003


def test_heterostructure_state_checks() -> None:
    result = semiconductor_well(10.0, padding_nm=10.0, number_of_states=5, points=1501)
    np.testing.assert_allclose(result.normalization, 1.0, atol=2e-12)
    np.testing.assert_allclose(result.overlap_matrix, np.eye(5), atol=2e-12)
    assert np.all(np.diff(result.energies_ev) > 0)
    assert result.residuals.max() < 1e-9
