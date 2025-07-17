#!/usr/bin/env python3
"""Run coverage simulations over ranges of altitudes and constellation sizes."""

import os
import numpy as np
import argparse

from src.constellation import walker_delta, walker_star
from src.propagation import propagate_keplerian
from src.coverage import instantaneous_coverage
from src.analysis import coverage_fraction, time_statistics
from src.utils import make_time_grid

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
except ImportError:
    plt = None


def build_constellation(config: str, n_sat: int, altitude_m: float, inc_deg: float) -> np.ndarray:
    """Helper to create constellation elements."""
    if config == "star":
        return walker_star(n_sat, np.deg2rad(inc_deg), altitude_m)
    else:
        # walker-delta: choose planes equal to sqrt(n_sat) rounded and f=1
        p = max(1, int(round(np.sqrt(n_sat))))
        return walker_delta(t=n_sat, p=p, f=1, a=altitude_m, inc=np.deg2rad(inc_deg))


def run_single_sim(elems: np.ndarray, tgt_elems: np.ndarray, scan_half_angle_deg: float) -> dict:
    times = make_time_grid(0.0, 5400.0, 60.0)  # 1.5 hours
    sat_pos = propagate_keplerian(elems, times)
    tgt_pos = propagate_keplerian(tgt_elems, times)

    cov_series = []
    for k, _ in enumerate(times):
        mask = instantaneous_coverage(
            sat_pos[:, k, :], tgt_pos[:, k, :],
            np.deg2rad(scan_half_angle_deg), np.deg2rad(scan_half_angle_deg)
        )
        cov_series.append(coverage_fraction(mask))
    cov_series = np.array(cov_series)
    stats = time_statistics(times, cov_series)
    return {"stats": stats, "series": cov_series}


def plot_constellation(elems: np.ndarray, outdir: str, scan_half_angle_deg: float):
    if plt is None:
        print("matplotlib not available; skipping plot")
        return
    os.makedirs(outdir, exist_ok=True)
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection="3d")
    earth_r = 6371e3
    # simple Earth sphere
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    x = earth_r * np.outer(np.cos(u), np.sin(v))
    y = earth_r * np.outer(np.sin(u), np.sin(v))
    z = earth_r * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x, y, z, color="lightblue", alpha=0.3, zorder=0)

    pos = propagate_keplerian(elems, np.array([0.0]))[:, 0, :]
    ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], color="red")
    # cones projected in +Z
    for p in pos:
        ax.plot([p[0], p[0]], [p[1], p[1]], [p[2], p[2] + 2e6], color="orange", lw=0.5)
    ax.set_title(f"Constellation snapshot (scan {scan_half_angle_deg} deg)")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_zlabel("Z [m]")
    plt.tight_layout()
    fig_path = os.path.join(outdir, "constellation.png")
    plt.savefig(fig_path)
    plt.close(fig)


def main(outdir: str, plot: bool):
    os.makedirs(outdir, exist_ok=True)

    inc_deg = 53.0
    scan_angle = 60.0  # degrees
    power_w = 30.0

    tgt_elems = np.array([[7000e3, 0.0, 0.0, 0.0, 0.0, 0.0]])

    # Sweep altitudes from 300 km up to 1000 km in 100 km steps
    altitudes_km = np.arange(300, 1001, 100)
    sat_counts = np.arange(30, 1001, 50)
    configs = ["delta", "star"]

    summary = []

    for cfg in configs:
        for alt_km in altitudes_km:
            for n in sat_counts:
                a_m = alt_km * 1e3 + 6371e3
                elems = build_constellation(cfg, n, a_m, inc_deg)
                res = run_single_sim(elems, tgt_elems, scan_angle)
                stat = res["stats"]
                stat.update({"config": cfg, "altitude_km": alt_km, "satellites": n, "power_w": power_w})
                summary.append(stat)
                if plot:
                    subdir = os.path.join(outdir, f"{cfg}_{n}sats_{alt_km}km")
                    plot_constellation(elems, subdir, scan_angle)

    # save statistics
    import json
    with open(os.path.join(outdir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("Sweep complete. Results in", outdir)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run constellation sweep simulations")
    ap.add_argument("--outdir", default="sweep_results", help="directory for results")
    ap.add_argument("--plot", action="store_true", help="save 3D constellation plots")
    args = ap.parse_args()
    main(args.outdir, args.plot)
