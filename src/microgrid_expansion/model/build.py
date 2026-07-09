"""Assemble the deterministic-equivalent MILP.

Wires together coordinates, variables, investment and dispatch constraints and the
objective into a single :class:`linopy.Model` (Section "Deterministic equivalent" of
the formulation).
"""
from __future__ import annotations

import linopy

from ..config import ModelConfig
from ..tree.tree_model import ScenarioTree
from ..timedomain.rep_days import RepDays
from . import coords as _coords
from . import variables, investment_constraints, dispatch_constraints, economics


def _stack_params(coords, rep: dict[int, RepDays], tree: ScenarioTree):
    """Stack per-node :class:`RepDays` arrays into ``(node, rday, htod)`` DataArrays.

    Returns a dict of xarray DataArrays for D, rho, sigma, f_e, R plus per-node cost
    series. Stub for the skeleton.
    """
    raise NotImplementedError("Stack RepDays into (node, rday, htod) DataArrays.")


def build_model(
    tree: ScenarioTree,
    rep: dict[int, RepDays],
    cfg: ModelConfig,
) -> linopy.Model:
    """Build and return the assembled linopy model.

    Steps:
      1. ``coords = build_coords(tree, rep, cfg)``
      2. stack representative-day parameters onto the coordinate grid
      3. ``v = add_variables(m, coords)``
      4. ``add_investment_constraints(m, v, coords, cfg)``
      5. ``add_dispatch_constraints(m, v, coords, cfg, params)``
      6. ``add_objective(m, v, coords, cfg, params)``
    """
    cfg.validate()
    m = linopy.Model()
    coords = _coords.build_coords(tree, rep, cfg)
    params = _stack_params(coords, rep, tree)
    v = variables.add_variables(m, coords)
    investment_constraints.add_investment_constraints(m, v, coords, cfg)
    dispatch_constraints.add_dispatch_constraints(m, v, coords, cfg, params)
    economics.add_objective(m, v, coords, cfg, params)
    return m
