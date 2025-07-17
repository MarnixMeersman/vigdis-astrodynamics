#!/usr/bin/env python3
import os
import argparse
import numpy as np

from src.constellation   import walker_delta, walker_star, custom
from src.propagation     import propagate_keplerian
from src.coverage        import instantaneous_coverage
from src.analysis        import coverage_fraction, time_statistics
from src.utils           import load_config, make_time_grid


def main(config_file, outdir):
    cfg = load_config(config_file)

    # 1) Build sats
    c = cfg['constellation']
    if c['type'] == 'delta':
        elems = walker_delta(**c['parameters'],
                             a=c['altitude']+6371e3,
                             inc=np.deg2rad(c['inc_deg']))
    elif c['type'] == 'star':
        elems = walker_star(c['parameters']['num'],
                            np.deg2rad(c['parameters']['inc_deg']),
                            c['altitude']+6371e3)
    else:
        elems = custom(c['parameters']['custom_list'])

    # 2) Build target orbits
    tgt_elems = []
    for tgt in cfg['targets']['orbits']:
        a = tgt['elements']['a']
        e = tgt['elements']['e']
        i = np.deg2rad(tgt['elements']['i'])
        raan = np.deg2rad(tgt['elements']['Ω'])
        argp = np.deg2rad(tgt['elements']['ω'])
        m0   = 0.0
        tgt_elems.append([a, e, i, raan, argp, m0])
    tgt_elems = np.array(tgt_elems)

    # 3) Time grid
    t0      = 0.0
    times   = make_time_grid(t0, cfg['simulation']['duration'], cfg['simulation']['dt'])

    # 4) Propagate
    sat_pos = propagate_keplerian(elems, times)
    tgt_pos = propagate_keplerian(tgt_elems, times)

    # 5) Coverage per epoch
    cov_frac = []
    for k, t in enumerate(times):
        mask = instantaneous_coverage(
            sat_pos[:,k,:], tgt_pos[:,k,:],
            np.deg2rad(cfg['beams']['divergence_half_angle']),
            np.deg2rad(cfg['beams']['scan_half_angle'])
        )
        cov_frac.append(coverage_fraction(mask))
    cov_frac = np.array(cov_frac)

    # 6) Stats & write out
    stats = time_statistics(times, cov_frac)
    os.makedirs(outdir, exist_ok=True)
    np.savetxt(os.path.join(outdir, 'coverage_time_series.csv'),
               np.vstack((times, cov_frac)).T,
               header='time_s,coverage_fraction', delimiter=',')
    with open(os.path.join(outdir, 'coverage_stats.json'), 'w') as f:
        import json; json.dump(stats, f, indent=2)

    print("Done. Results in", outdir)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--config',  required=True)
    p.add_argument('--outdir',  default='results/')
    args = p.parse_args()
    main(args.config, args.outdir)
