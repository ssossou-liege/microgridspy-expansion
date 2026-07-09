"""Monte-Carlo sampling of complete uncertainty paths.

Draws ``cfg.n_mc_paths`` independent paths. Each path assigns, at every stage, a
draw from each of the four uncertainty families. The heavy hourly arrays (demand,
specific yield) are attached by :mod:`microgrid_expansion.scenarios.assemble`.
"""
from __future__ import annotations

import numpy as np

from ..config import ModelConfig
from .uncertainty_space import UncertaintySpace


def draw_axis_values(
    space: UncertaintySpace,
    stage_year: int,
    rng: np.random.Generator,
) -> dict:
    """Draw one realisation of the four families at a single stage."""
    resource = rng.choice(space.resource.pathways, p=space.resource.probabilities)
    policy = rng.choice(space.policy.penetration_levels, p=space.policy.probabilities)
    return {
        "stage_year": stage_year,
        "resource": str(resource),
        "policy": float(policy),
        # demand and economic draws are resolved lazily in assemble.py
    }


def sample_paths(cfg: ModelConfig, space: UncertaintySpace) -> list[list[dict]]:
    """Return ``n_mc_paths`` paths, each a list of per-stage axis draws."""
    rng = np.random.default_rng(cfg.seed)
    paths = []
    for _ in range(cfg.n_mc_paths):
        path = [draw_axis_values(space, y, rng) for y in cfg.stage_years]
        paths.append(path)
    return paths
