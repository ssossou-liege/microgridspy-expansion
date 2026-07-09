"""Demand realisations from the calibrated RAMP generator.

Wraps the THESIS RAMP calibration (``src/demand_modeling/ramp_models.py``,
``ramp_evolution_extension.py``) to draw a stochastic 8760-hour demand profile for
each stage of a scenario path, given the demand-axis draw (connections, appliance
stock, usage patterns) and the Markov tier-transition growth between stages.

Produces, per stage, the array ``D`` [kW] entering the formulation (parameter
``D_{n,t,h}`` after time-domain reduction).
"""
from __future__ import annotations

import numpy as np

from .uncertainty_space import DemandAxis


def simulate_stage_demand(
    demand_axis: DemandAxis,
    stage_year: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Return an 8760-hour demand profile [kW] for one stage.

    Intended to call ``CalibratedModels.simulate(period, cluster, seed=...)`` from
    THESIS, applying the evolution scaling for ``stage_year``. Stub for the skeleton.
    """
    raise NotImplementedError(
        "Wire to THESIS CalibratedModels / ramp_evolution_extension."
    )
