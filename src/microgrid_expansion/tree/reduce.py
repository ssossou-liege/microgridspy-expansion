"""Per-stage scenario reduction.

Condenses the Monte-Carlo ensemble at each stage to a small set of representative
outcomes, each carrying the probability mass of its cluster. A medoid-based method
(k-medoids on a feature representation of the paths, or fast-forward selection) is
used so that representatives are actual sampled outcomes.

The reduction error relative to the full ensemble is returned so that the compression
stays transparent (no silent truncation).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..scenarios.assemble import ScenarioPath


@dataclass
class StageReduction:
    """Result of reducing one stage's outcomes."""

    representatives: list[int]          # indices of representative paths
    assignment: np.ndarray              # path -> representative index
    weights: np.ndarray                 # probability mass per representative
    error: float                        # distortion vs full ensemble


def reduce_stage(
    paths: list[ScenarioPath],
    stage_year: int,
    n_repr: int,
    seed: int = 0,
) -> StageReduction:
    """Reduce the ensemble of stage-``stage_year`` outcomes to ``n_repr`` medoids.

    Stub: implement k-medoids / fast-forward selection on a feature vector built from
    each path's stage demand shape, specific yield and cost draw.
    """
    raise NotImplementedError("Implement medoid-based stage reduction.")
