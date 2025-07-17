"""
Check whether each target point lies within any sat's beam cone.
"""
import numpy as np


def angle_between(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Elementwise angle between vectors (rad)."""
    cosang = np.einsum('...i,...i', u, v) / (
        np.linalg.norm(u, axis=-1) * np.linalg.norm(v, axis=-1)
    )
    return np.arccos(np.clip(cosang, -1.0, 1.0))


def instantaneous_coverage(
    sat_pos: np.ndarray,       # (N_sat,3)
    tgt_pos: np.ndarray,       # (N_tgt,3)
    divergence: float,         # half-angle [rad]
    scan_angle: float          # half-angle [rad]
) -> np.ndarray:
    """Returns boolean mask (N_sat, N_tgt) indicating coverage."""
    # LOS vectors: (N_sat,1,3) - (1,N_tgt,3) → (N_sat, N_tgt,3)
    los = sat_pos[:, None, :] - tgt_pos[None, :, :]
    # assume sat boresight is +Z in ECI for now
    boresight = np.array([0, 0, 1.0])
    boresight = boresight[None, None, :]  # broadcast
    ang = angle_between(los, boresight)  # (N_sat, N_tgt)
    return ang <= np.minimum(divergence, scan_angle)

