"""Objective: expected discounted total cost over the scenario tree.

Implements the objective (eq. objective) of the formulation:

    min  sum_n pi_n * delta_n * ( K_n + Delta_n * O_n + Delta_n * G_n )

with
    K_n  incremental capital cost of capacity added at node n,
    O_n  annual O&M of the cumulative fleet at node n,
    G_n  operating cost of the representative year (fuel + degradation + lost load).
"""
from __future__ import annotations

import linopy

from ..config import ModelConfig
from .coords import Coords


def add_objective(
    m: linopy.Model,
    v: dict,
    c: Coords,
    cfg: ModelConfig,
    params: dict,
) -> None:
    """Build and set the risk-neutral expected discounted-cost objective.

    Uses the per-node cost trajectories in ``params`` (capex per technology, fuel
    price), the representative-day weights, and the tree weights ``pi_n``,
    ``delta_n`` and ``Delta_n`` carried on :class:`Coords`.
    """
    raise NotImplementedError("Assemble K_n + Delta_n*(O_n + G_n), set m.objective.")
