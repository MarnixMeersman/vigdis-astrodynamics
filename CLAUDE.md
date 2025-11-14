# CLAUDE.md - AI Assistant Guide

This document provides guidance for AI assistants working with the Vigdis Astrodynamics codebase.

## Project Overview

Vigdis Astrodynamics is a Python-based prototype simulator for exploring satellite constellations and target coverage in very-low Earth orbit (VLEO). The simulator uses Keplerian orbit propagation to analyze coverage patterns for different constellation configurations.

### Key Technologies
- **Python 3**: Primary language
- **NumPy**: Numerical computations and array operations
- **tudatpy**: Astrodynamics library for orbital mechanics
- **PyYAML**: Configuration file parsing
- **matplotlib** (optional): 3D visualization of constellations

## Repository Structure

```
vigdis-astrodynamics/
├── src/                      # Core implementation modules
│   ├── constellation.py      # Constellation generation (Walker-delta, Walker-star, custom)
│   ├── propagation.py        # Keplerian orbit propagation
│   ├── coverage.py           # Line-of-sight coverage calculations
│   ├── analysis.py           # Coverage statistics and metrics
│   └── utils.py              # I/O utilities and configuration parsing
├── config/                   # YAML configuration files
│   └── example.yaml          # Example constellation configuration
├── run_simulation.py         # Main CLI for single simulation runs
├── sweep_simulation.py       # Parameter sweep simulations
├── requirements.txt          # Python dependencies
├── LICENSE                   # Project license
└── README.md                 # User-facing documentation
```

## Code Organization & Patterns

### Module Responsibilities

1. **constellation.py** - Constellation Generation
   - `walker_delta(t, p, f, a, inc, raan0)`: Generate Walker-delta constellation
   - `walker_star(num, inc, a)`: Generate evenly-spaced star pattern
   - `custom(elements_list)`: Accept user-provided Keplerian elements
   - Returns: `(N, 6)` array of `[a, e, i, raan, argp, mean_anomaly]`

2. **propagation.py** - Orbital Mechanics
   - `solve_kepler(M, e, tol, max_iter)`: Newton-Raphson Kepler equation solver
   - `propagate_keplerian(elems, times, mu)`: Propagate orbits analytically
   - Uses `tudatpy.kernel.astro.element_conversion` for coordinate conversions
   - Returns: `(N_sat, N_time, 3)` ECI positions in meters

3. **coverage.py** - Coverage Analysis
   - `angle_between(u, v)`: Vectorized angle calculation
   - `instantaneous_coverage(sat_pos, tgt_pos, divergence, scan_angle)`: Coverage mask
   - Assumes satellite boresight is +Z in ECI frame
   - Returns: `(N_sat, N_tgt)` boolean coverage mask

4. **analysis.py** - Statistical Metrics
   - `coverage_fraction(coverage_mask)`: Fraction of targets covered
   - `time_statistics(time_series, coverage_series)`: Mean coverage and gap analysis
   - Returns: Dictionary with `mean_coverage` and `max_zero_coverage_gap_s`

5. **utils.py** - Utilities
   - `load_config(path)`: Parse YAML configuration files
   - `make_time_grid(t0, duration, dt)`: Generate time array

### Conventions & Best Practices

#### Coordinate Systems & Units
- **Positions**: Earth-Centered Inertial (ECI) frame, meters
- **Angles**: Radians internally; degrees in config files and CLI
- **Time**: Seconds since epoch (t0=0)
- **Semi-major axis**: Orbital radius in meters (altitude + 6371e3)
- **Gravitational parameter**: `tudatpy.kernel.constants.GRAVITATIONAL_PARAMETER_EARTH`

#### Array Shapes & Indexing
- Keplerian elements: `(N_objects, 6)` - `[a, e, i, Ω, ω, M]`
- Positions: `(N_objects, N_times, 3)` - `[x, y, z]` in ECI
- Coverage masks: `(N_sat, N_tgt)` boolean arrays
- Time series: `(N_times,)` 1D arrays

#### Naming Conventions
- **Variables**: Snake_case (e.g., `sat_pos`, `tgt_elems`, `cov_frac`)
- **Functions**: Snake_case verbs (e.g., `propagate_keplerian`, `coverage_fraction`)
- **Type hints**: Used in function signatures where applicable
- **Docstrings**: Google-style with Args/Returns sections
- **Angle parameters**: Suffix `_deg` or `_rad` to indicate units

#### Configuration Files (YAML)
```yaml
constellation:
  type: delta|star|custom          # Constellation type
  altitude: <float>                 # meters above Earth
  inc_deg: <float>                  # degrees
  parameters:
    t: <int>                        # total satellites (delta)
    p: <int>                        # planes (delta)
    f: <int>                        # phasing factor (delta)
    num: <int>                      # satellites (star)

targets:
  orbits:
    - elements:                     # Keplerian elements (degrees)
        a: <float>                  # semi-major axis [m]
        e: <float>                  # eccentricity
        i: <float>                  # inclination [deg]
        Ω: <float>                  # RAAN [deg]
        ω: <float>                  # argument of periapsis [deg]

simulation:
  duration: <float>                 # seconds
  dt: <float>                       # timestep [s]

beams:
  divergence_half_angle: <float>    # degrees
  scan_half_angle: <float>          # degrees
```

## Development Workflows

### Git Workflow
- **Feature branches**: Use descriptive prefixes (e.g., `codex/feature-name`)
- **Pull requests**: All changes merged via PRs to main branch
- **Commits**: Clear, descriptive messages
- **Current branch**: `claude/claude-md-mhyxcclqxmr0q280-018qUm5LSwMuUebMhgLaeEmm`

### Running Simulations

#### Single Configuration
```bash
python run_simulation.py --config config/example.yaml --outdir demo/
```

#### Parameter Sweeps
```bash
python sweep_simulation.py --outdir sweep_results --plot
```

#### Expected Outputs
- **CSV files**: `coverage_time_series.csv` with columns `[time_s, coverage_fraction]`
- **JSON files**: `coverage_stats.json` with metrics
- **PNG files**: `constellation.png` 3D visualization (if matplotlib available)

### Testing & Validation
- Currently no automated test suite (future work)
- Manual validation via configuration files in `config/`
- Verify outputs by checking:
  - Coverage fractions in range [0, 1]
  - ECI positions have realistic magnitudes (~7000 km from Earth center)
  - Time series matches configured duration and timestep

## Common Tasks for AI Assistants

### Adding New Constellation Types
1. Add generation function to `src/constellation.py`
2. Update `run_simulation.py` to handle new type in config parsing
3. Add example configuration to `config/`
4. Test with known constellation patterns

### Modifying Coverage Algorithms
1. Edit `src/coverage.py` for new coverage models
2. Consider boresight pointing (currently fixed +Z)
3. Maintain `(N_sat, N_tgt)` boolean mask output
4. Update docstrings with algorithm details

### Adding Analysis Metrics
1. Add functions to `src/analysis.py`
2. Return dictionary format for JSON serialization
3. Include units in dictionary keys (e.g., `_s`, `_deg`, `_km`)
4. Update output writing in `run_simulation.py`

### Implementing Full Numerical Propagation
- Replace `propagate_keplerian()` with tudatpy numerical propagator
- Maintain interface: `(elems, times)` → `(N, T, 3)` positions
- Add perturbation models (J2, drag, etc.) as configuration options
- Consider performance for large constellations

## Important Notes for AI Assistants

### Performance Considerations
- Vectorized NumPy operations preferred over loops
- Large parameter sweeps can be CPU-intensive
- Keplerian propagation is fast but limited accuracy
- Consider chunking for very large constellations (>10,000 satellites)

### Known Limitations
- **Simplified coverage model**: Fixed +Z boresight, no attitude dynamics
- **Keplerian propagation**: No perturbations (J2, drag, solar pressure)
- **No occlusion**: Earth shadow not considered in coverage
- **Single target orbit type**: Only circular/elliptical targets
- **No communication constraints**: Power, data rate, link budget not modeled

### Future Enhancements Mentioned
- Replace Keplerian propagator with full tudatpy numerical propagation
- Add automated test suite
- Support for more complex target patterns
- Attitude dynamics and beam steering
- Link budget analysis

### Code Quality Standards
- **Type hints**: Add to new functions
- **Docstrings**: Include Args, Returns, and brief description
- **Error handling**: Validate inputs (positive altitudes, valid angles, etc.)
- **Comments**: Explain non-obvious physics or mathematical operations
- **Consistency**: Match existing naming and structure patterns

## Quick Reference

### Key Files by Use Case
- **Understanding constellation types**: `src/constellation.py`
- **Orbital mechanics**: `src/propagation.py`
- **Coverage logic**: `src/coverage.py`
- **Adding metrics**: `src/analysis.py`
- **CLI changes**: `run_simulation.py`, `sweep_simulation.py`
- **Configuration format**: `config/example.yaml`

### External Dependencies
- **tudatpy docs**: https://tudatpy.readthedocs.io
- **NumPy**: Standard numerical Python library
- **PyYAML**: YAML parsing

### Contact & Contributions
- Check README.md for project-specific contribution guidelines
- Follow existing code patterns for consistency
- Test changes with example configurations before committing

---

**Document Version**: 1.0
**Last Updated**: 2025-11-14
**Codebase State**: Main simulation framework complete, parameter sweeps functional
