# Vigdis Astrodynamics

This repository contains a small prototype simulator for exploring satellite constellations and target coverage in very-low Earth orbit (VLEO).

The code is pure Python and relies only on `numpy`, `pyyaml` and [`tudatpy`](https://tudatpy.readthedocs.io) for basic astrodynamics routines.  It provides tools to generate constellations, propagate simple Keplerian orbits and estimate line-of-sight coverage of user defined targets.

## Quick start

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Run the demo simulation using the provided configuration:

```bash
python run_simulation.py --config config/example.yaml --outdir demo/
```

This produces CSV and JSON files under `demo/` describing the time history of coverage fraction and some simple statistics.

## Project structure

- `src/` – implementation modules (constellation generation, propagation, coverage checks, etc.)
- `config/` – example YAML configuration files
- `run_simulation.py` – command line interface to run a simulation

Future iterations may replace the simple propagator with a full TudatPy setup and include automated tests.

