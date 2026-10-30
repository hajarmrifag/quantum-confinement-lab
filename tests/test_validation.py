import numpy as np
import pytest

from quantum_confinement.models import finite_square_well, infinite_square_well, semiconductor_well
from quantum_confinement.numerics import assemble_hamiltonian
from quantum_confinement.reference import finite_well_reference, infinite_well_energies


@pytest.mark.parametrize(
    ("function", "args"),
    [
        (infinite_square_well, (-1.0,)),
        (infinite_square_well, (8.0, -0.1)),
        (finite_square_well, (8.0, -0.2)),
        (finite_square_well, (8.0, 0.2, 0.067, -1.0)),
        (infinite_well_energies, (8.0, 0.067, 0)),
        (finite_well_reference, (8.0, 0.2, -0.1)),
    ],
)
def test_invalid_physical_parameters_raise(function, args) -> None:
    with pytest.raises(ValueError):
        function(*args)


def test_nonuniform_grid_is_rejected() -> None:
    x = np.array([0.0, 0.1, 0.21, 0.3])
    with pytest.raises(ValueError, match="uniform"):
        assemble_hamiltonian(x, np.zeros_like(x), 0.067)


def test_infinite_grid_convergence_reduces_continuum_error() -> None:
    exact = infinite_well_energies(8.0, 0.067, 1)[0]
    coarse = infinite_square_well(8.0, 0.067, 1, 101).energies_ev[0]
    fine = infinite_square_well(8.0, 0.067, 1, 401).energies_ev[0]
    assert abs(fine - exact) < abs(coarse - exact) / 10.0


def test_semiconductor_reproducibility() -> None:
    first = semiconductor_well(8.0, points=801, number_of_states=3)
    second = semiconductor_well(8.0, points=801, number_of_states=3)
    np.testing.assert_array_equal(first.energies_ev, second.energies_ev)
