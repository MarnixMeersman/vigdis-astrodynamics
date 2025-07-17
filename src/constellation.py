"""
Generate satellite constellations (Walker-delta, Walker-star, custom).
"""
import numpy as np

def walker_delta(t: int, p: int, f: int, a: float, inc: float, raan0: float=0.0):
    """Generate Walker-delta constellation.

    Args:
        t: total satellites
        p: planes
        f: phasing factor
        a: semi-major axis [m]
        inc: inclination [rad]
        raan0: initial RAAN offset [rad]

    Returns:
        elems: ndarray of shape (t,6) containing [a,e,i,raan,argp,mean_anomaly]
    """
    sats_per_plane = t // p
    elems = []
    for i in range(p):
        raan = raan0 + 2*np.pi * i/p
        for j in range(sats_per_plane):
            m0 = 2*np.pi*(j * p + i * f) / t
            elems.append([a, 0.0, inc, raan, 0.0, m0])
    return np.array(elems)


def walker_star(num: int, inc: float, a: float):
    """Generate evenly-spaced 'star' pattern."""
    elems = []
    for k in range(num):
        omega = 2*np.pi * k / num
        elems.append([a, 0.0, inc, omega, 0.0, 0.0])
    return np.array(elems)


def custom(elements_list):
    """Accept user-provided list of Keplerian tuples."""
    return np.array(elements_list)
