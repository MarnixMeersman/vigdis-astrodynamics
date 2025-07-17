"""
Analytical (Keplerian) propagator using mean elements + Newton-Raphson.
"""
import numpy as np
from tudatpy.kernel import constants
from tudatpy.kernel.astro import element_conversion


def solve_kepler(M, e, tol=1e-8, max_iter=50):
    E = M.copy()
    for _ in range(max_iter):
        f = E - e*np.sin(E) - M
        f_prime = 1 - e*np.cos(E)
        dE = -f / f_prime
        E += dE
        if np.all(np.abs(dE) < tol):
            break
    return E


def propagate_keplerian(elems: np.ndarray, times: np.ndarray,
                        mu: float = constants.GRAVITATIONAL_PARAMETER_EARTH) -> np.ndarray:
    """Propagate keplerian orbits using mean elements.

    Args:
        elems: (N,6) array of [a,e,i,raan,argp,m0] at t0=0
        times: (T,) array of seconds since t0
        mu: gravitational parameter [m^3/s^2]

    Returns:
        positions: (N, T, 3) ECI positions [m]
    """
    a, e, i, raan, argp, m0 = elems.T
    n = np.sqrt(mu / a**3)
    positions = np.zeros((elems.shape[0], times.size, 3))
    for idx, t in enumerate(times):
        M = m0 + n * t
        E = solve_kepler(M, e)
        # convert each sat
        for sat in range(elems.shape[0]):
            r_ijk = element_conversion.keplerian_to_cartesian(
                a[sat], e[sat], i[sat], raan[sat], argp[sat], E[sat], mu
            )
            positions[sat, idx, :] = r_ijk
    return positions

