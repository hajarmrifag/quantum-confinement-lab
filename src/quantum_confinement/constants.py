"""Physical constants and unit conversions used by the solvers."""

from scipy.constants import electron_mass, electron_volt, hbar

# hbar^2/(2 m_e), expressed in eV nm^2. Masses elsewhere are ratios to m_e.
HBAR2_OVER_2M0_EV_NM2: float = hbar**2 / (2.0 * electron_mass * electron_volt) * 1.0e18
MEV_PER_EV: float = 1_000.0
