# data/ — provenance

Inputs in this directory are copied (not symlinked) so this repository stays
self-contained and reproducible. Record each import below with its source path and
date.

| Local file | Source | Description | Imported |
|---|---|---|---|
| _(Done)_ `ramp_params/` | `calibration results` | Calibrated RAMP appliance parameters per cluster | Yes |
| _(pending)_ `irradiance/` | `Climate Data Store (CDS) Copernic` | Hourly irradiance / specific yield (baseline + per-SSP) | — |
| _(pending)_ `demand/` | `results/tool_comparison/*/demand_8760.csv` | 8760-h measured demand profiles (SAM, GBO) | — |
| _(pending)_ `costs/` | `src/dispatch_assessment/config.py` | Economic constants and cost trajectories (ported into code) | — |

## Notes
- Climate scenarios (SSP126/245/370/585) are not yet generated; irradiance is
  currently historical TMY. SSP-downscaled irradiance is added here when available.
- Survey-derived appliance ownership / usage distributions feed the Monte-Carlo demand
  sampler via the RAMP parameter files above.
