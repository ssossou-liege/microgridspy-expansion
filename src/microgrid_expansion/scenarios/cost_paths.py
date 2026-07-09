"""Economic-trajectory realisations: fuel price and per-technology investment cost.

Given the economic-axis draw, returns the diesel price ``c^fuel`` and the investment
costs ``C^inv_g`` for each technology at a stage. Central values are taken from
:mod:`microgrid_expansion.config`; trajectories apply fuel-price growth and capex
learning multipliers sampled per path.
"""
from __future__ import annotations

import numpy as np

from .. import config
from .uncertainty_space import EconomicAxis


def stage_costs(
    economic_axis: EconomicAxis,
    stage_year: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    """Return a dict with ``fuel_price`` and ``capex_{pv,batt,ge,inv}`` for the stage.

    Stub: currently returns central values; replace with sampled trajectories.
    """
    return {
        "fuel_price": config.DIESEL_PRICE_USD_L,
        "capex_pv": config.PV_COST_USD_KW,
        "capex_batt": config.BATT_COST_USD_KWH,
        "capex_ge": config.GEN_COST_USD_KVA,
        "capex_inv": config.INV_COST_USD_KW,
    }
