# Vigdis Astrodynamics

Vigdis is a lightweight research tool for exploring simple satellite constellations and their ability to observe targets in very-low Earth orbit (VLEO).  The code is written in pure Python and uses [`tudatpy`](https://tudatpy.readthedocs.io) for basic astrodynamics calculations.

The simulator lets you:

- Create constellations with either a Walker-delta or Walker-star pattern (or provide your own list of Keplerian elements).
- Propagate satellites and targets using an analytic Keplerian model.
- Check which targets lie inside a satellite's observation cone at each timestep.
- Aggregate the instantaneous visibility into simple coverage statistics.

## Getting started

1. **Install dependencies**

   We recommend using a virtual environment.  Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   The list includes `numpy`, `pyyaml` and `tudatpy`.

2. **Run the example simulation**

   ```bash
   python run_simulation.py --config config/example.yaml --outdir demo/
   ```

   This command generates a small four-satellite Walker-delta constellation and propagates it for 1.5 hours.  CSV and JSON files will be written to `demo/` containing the coverage fraction time series and basic statistics.

The example configuration defines one target orbit and a set of simulation parameters:

```yaml
constellation:
  type: delta
  altitude: 550e3
  inc_deg: 53.0
  parameters:
    t: 4
    p: 2
    f: 1

simulation:
  duration: 5400   # seconds
  dt: 60

beams:
  divergence_half_angle: 20.0
  scan_half_angle: 20.0
```

You can edit these values or add additional target orbits to experiment with different scenarios.

## What does the code do?

1. **Constellation generation** – `src/constellation.py` builds the set of Keplerian elements for each satellite using the selected pattern.
2. **Propagation** – `src/propagation.py` propagates both satellites and targets analytically, returning their Cartesian positions at every timestep.
3. **Coverage check** – `src/coverage.py` determines whether each target falls within a satellite's viewing cone (defined by divergence and scan angles).
4. **Analysis** – `src/analysis.py` aggregates the per-epoch results into overall metrics such as mean coverage and longest gap without coverage.
5. **Simulation driver** – `run_simulation.py` ties everything together. It loads the YAML configuration, runs the propagation and coverage calculations, then writes the output files.

The repository also contains `sweep_simulation.py` which can run many simulations over ranges of altitudes and constellation sizes for trade studies.

## Project structure

- `src/` – implementation modules
- `config/` – example configuration files
- `run_simulation.py` – command line entry point
- `sweep_simulation.py` – parameter sweep utility

Future work may extend the propagator with a full TudatPy setup and add automated tests.
