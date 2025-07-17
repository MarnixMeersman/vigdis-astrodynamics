"""
Aggregate instantaneous results into time-integrated metrics.
"""
import numpy as np


def coverage_fraction(coverage_mask: np.ndarray) -> float:
    """Return fraction of targets covered by at least one satellite."""
    tgt_covered = np.any(coverage_mask, axis=0)
    return np.sum(tgt_covered) / tgt_covered.size


def time_statistics(
    time_series: np.ndarray,
    coverage_series: np.ndarray
) -> dict:
    """Compute mean coverage and maximum zero-coverage gap."""
    mean_cov = np.mean(coverage_series)
    zeros = np.where(coverage_series == 0)[0]
    if zeros.size > 1:
        gaps = np.diff(time_series[zeros])
        max_gap = np.max(gaps)
    else:
        max_gap = 0.0
    return {
        "mean_coverage": mean_cov,
        "max_zero_coverage_gap_s": max_gap
    }

