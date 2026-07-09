"""Extract a tidy view of the optimal solution from a solved linopy model."""
from __future__ import annotations

import linopy

from ..tree.tree_model import ScenarioTree


def extract_solution(model: linopy.Model, tree: ScenarioTree) -> dict:
    """Return per-node capacities and dispatch time-series from the solved model.

    Produces, per node: installed capacities (pv, batt, ge, inv), the capacity
    increments decided there, and the operating arrays (P_ge, P_ch, P_dis, e, q, l,
    y) on the representative-day grid. Stub for the skeleton.
    """
    raise NotImplementedError("Read solution values from model.variables.")
