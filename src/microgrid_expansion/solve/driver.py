"""Solver configuration and invocation.

Solves the assembled MILP with HiGHS (default, open source) or Gurobi. Exposes a
single interface so the choice of backend does not change calling code.
"""
from __future__ import annotations

from dataclasses import dataclass

import linopy

from ..config import ModelConfig


@dataclass
class SolveResult:
    """Outcome of a solve: status, objective, gap and wall-clock time."""

    status: str
    objective: float | None
    gap: float | None
    wall_time_s: float | None


def solve(model: linopy.Model, cfg: ModelConfig) -> SolveResult:
    """Solve ``model`` according to ``cfg`` (solver, time limit, MIP gap, threads).

    Maps ``cfg`` onto ``model.solve(...)`` keyword options for the chosen backend and
    returns a :class:`SolveResult`. Stub for the skeleton.
    """
    raise NotImplementedError("Invoke model.solve with backend-specific options.")
