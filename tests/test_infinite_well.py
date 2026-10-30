import numpy as np

from quantum_confinement.models import infinite_square_well
from quantum_confinement.reference import discrete_infinite_well_energies, infinite_well_energies


def test_eigensolver_matches_exact_discrete_operator() -> None:
    result = infinite_square_well(8.0, 0.067, 5, 801)
    discrete = discrete_infinite_well_energies(8.0, 0.067, 800, 5)
    np.testing.assert_allclose(result.energies_ev, discrete, rtol=2e-10, atol=1e-12)


def test_continuum_agreement_for_multiple_widths_and_states() -> None:
    for width in (4.0, 8.0, 15.0):
        result = infinite_square_well(width, 0.067, 4, 1201)
        exact = infinite_well_energies(width, 0.067, 4)
        np.testing.assert_allclose(result.energies_ev, exact, rtol=1e-5)


def test_width_and_mass_scaling() -> None:
    e8 = infinite_square_well(8.0, 0.067, 1, 801).energies_ev[0]
    e16 = infinite_square_well(16.0, 0.067, 1, 801).energies_ev[0]
    heavy = infinite_square_well(8.0, 0.134, 1, 801).energies_ev[0]
    assert np.isclose(e8 / e16, 4.0, rtol=1e-10)
    assert np.isclose(e8 / heavy, 2.0, rtol=1e-10)


def test_normalization_orthogonality_boundaries_and_residuals() -> None:
    result = infinite_square_well(10.0, 0.067, 6, 1001)
    np.testing.assert_allclose(result.normalization, 1.0, atol=2e-12)
    np.testing.assert_allclose(result.overlap_matrix, np.eye(6), atol=2e-12)
    assert np.all(result.wavefunctions[[0, -1], :] == 0.0)
    assert result.residuals.max() < 5e-10


def test_infinite_well_reproducible_sign_convention() -> None:
    first = infinite_square_well(7.0, 0.067, 3, 401)
    second = infinite_square_well(7.0, 0.067, 3, 401)
    np.testing.assert_array_equal(first.energies_ev, second.energies_ev)
    np.testing.assert_array_equal(first.wavefunctions, second.wavefunctions)
