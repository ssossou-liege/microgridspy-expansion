# data/ — provenance

Inputs in this directory are imported from the `THESIS` repository
(`/home/ssossou/THESIS`). They are copied (not symlinked) so this repository stays
self-contained and reproducible. Record each import below with its source path and
date.

| Local file | Source (THESIS) | Description | Imported |
|---|---|---|---|
| _(pending)_ `ramp_params/` | `data/calibration/ramp_params_*.csv` | Calibrated RAMP appliance parameters per (period, cluster) | — |
| _(pending)_ `irradiance/` | `data/raw/*solar_irradiance*.csv` | Hourly irradiance / specific yield (baseline + per-SSP) | — |
| _(pending)_ `demand/` | `results/tool_comparison/*/demand_8760.csv` | 8760-h measured demand profiles (SAM, GBO) | — |
| _(pending)_ `costs/` | `src/dispatch_assessment/config.py` | Economic constants and cost trajectories (ported into code) | — |

## Notes
- Climate scenarios (SSP126/245/370/585) are not yet present in THESIS; irradiance is
  currently historical TMY. SSP-downscaled irradiance is added here when available.
- Survey-derived appliance ownership / usage distributions feed the Monte-Carlo demand
  sampler via the RAMP parameter files above.
