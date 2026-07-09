"""Compress a node's operating year into weighted representative days.

The full 8760-hour year of a node is clustered (k-medoids on daily demand and
resource shapes) into ``n_rep`` representative days. The medoid of each cluster
becomes a representative day with weight equal to the cluster size, so that the
weights sum to 365 days. Together with the cyclic battery closure this keeps each
node's operating sub-problem small (n_rep x 24 steps instead of 8760).

All hourly parameter arrays entering the model are produced here on the
``(rep_day, hour)`` grid: demand ``D``, specific yield ``rho``, self-discharge
``sigma``, usable-capacity factor ``f^e`` and the night-reserve floor ``R``.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..tree.tree_model import NodeData


@dataclass
class RepDays:
    """Representative-day arrays for one node (shape ``(n_rep, 24)`` unless noted)."""

    weight: np.ndarray          # (n_rep,) days per representative day; sums to 365
    demand: np.ndarray          # D_{t,h} [kW]
    pv_unit: np.ndarray         # rho_{t,h} [kW/kW]
    self_discharge: np.ndarray  # sigma_{t,h} [-]
    cap_factor: np.ndarray      # f^e_{t,h} usable-capacity factor [-]
    night_reserve: np.ndarray   # R_{t,h} [kWh] (per unit battery capacity)


def night_reserve_floor(demand_day: np.ndarray) -> np.ndarray:
    """Compute the look-ahead night-reserve R for a single representative day.

    Mirrors the uGrid ``loadLeft`` look-ahead: at each hour, the forecast demand
    remaining until the next sunrise. Returned per unit of installed battery energy
    (the model scales by ``cap_batt``). Stub for the skeleton.
    """
    raise NotImplementedError("Port the uGrid look-ahead night-reserve computation.")


def reduce_to_rep_days(node_data: NodeData, n_rep: int, seed: int = 0) -> RepDays:
    """Cluster a node's operating year into ``n_rep`` weighted representative days.

    Stub: implement k-medoids on standardised daily feature vectors (24-h demand
    shape + 24-h yield shape + daily totals); derive sigma and f^e from the medoid
    temperature series (uGrid ``batt_calcs`` formulas) and R from
    :func:`night_reserve_floor`.
    """
    raise NotImplementedError("Implement k-medoids representative-day reduction.")
