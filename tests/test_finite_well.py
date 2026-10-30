import numpy as np

from quantum_confinement.models import finite_square_well
from quantum_confinement.reference import finite_well_reference


def _points(width: float, padding: float, spacing: float) -> int:
    return int(round((width + 2 * padding) / spacing)) + 1


def test_finite_well_matches_independent_parity_roots() -> None:
    result = finite_square_well(8.0, 0.253, 0.067, 12.0, 5, _points(8, 12, 0.01))
    reference, parity = finite_well_reference(8.0, 0.253, 0.067)
    assert parity == ("even", "odd")
    np.testing.assert_allclose(result.energies_ev[: len(reference)], reference, atol=3e-4)


def test_above_barrier_box_states_are_not_bound() -> None:
    result = finite_square_well(6.0, 0.15, 0.067, 8.0, 7, 1101)
    assert np.array_equal(result.bound_mask, result.energies_ev < 0.15)
    assert np.any(~result.bound_mask)


def test_physical_leakage_decreases_for_higher_barrier() -> None:
    low = finite_square_well(8.0, 0.15, 0.067, 10.0, 2, 1401)
    high = finite_square_well(8.0, 0.40, 0.067, 10.0, 2, 1401)
    assert high.leakage_probability[0] < low.leakage_probability[0]


def test_domain_growth_stabilizes_ground_energy() -> None:
    reference = finite_well_reference(8.0, 0.253, 0.067)[0][0]
    short = finite_square_well(8.0, 0.253, 0.067, 2.0, 2, _points(8, 2, 0.02))
    long = finite_square_well(8.0, 0.253, 0.067, 10.0, 2, _points(8, 10, 0.02))
    assert abs(long.energies_ev[0] - reference) < abs(short.energies_ev[0] - reference)
    assert long.boundary_guard_probability[0] < short.boundary_guard_probability[0]


def test_reference_equal_mass_default_is_identical() -> None:
    implicit = finite_well_reference(9.0, 0.3, 0.067)[0]
    explicit = finite_well_reference(9.0, 0.3, 0.067, 0.067)[0]
    np.testing.assert_array_equal(implicit, explicit)
