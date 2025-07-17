"""
I/O, config parsing, helpers.
"""
import yaml
import numpy as np


def load_config(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def make_time_grid(t0: float, duration: float, dt: float) -> np.ndarray:
    """Return array of times [s] from 0 to duration, step dt."""
    return np.arange(0.0, duration+dt/2, dt)

