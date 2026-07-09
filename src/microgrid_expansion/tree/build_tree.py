"""Nest per-stage reduced outcomes into a branching scenario tree.

A node at one stage gives rise to several children at the next; the path probability
of a node is the product of the conditional branch probabilities along its path.
A two-stage program is recovered as a tree with a single decision node at the first
stage (``cfg.branching == (1, ...)`` with a star of leaves).
"""
from __future__ import annotations

from ..config import ModelConfig
from ..scenarios.assemble import ScenarioPath
from .tree_model import ScenarioTree, NodeData
from . import reduce as _reduce


def build_tree(paths: list[ScenarioPath], cfg: ModelConfig) -> ScenarioTree:
    """Build the scenario tree from the Monte-Carlo ensemble.

    Skeleton outline:
      1. For each stage, call :func:`reduce.reduce_stage` with the stage branching
         factor to obtain representative outcomes and their probability mass.
      2. Nest the representatives stage by stage, creating child nodes and assigning
         conditional branch probabilities.
      3. Attach :class:`NodeData` (reduced hourly arrays + cost/resource/policy) and
         fill ``prob``, ``disc`` (= (1+r)^-year) and ``n_years`` (= span to next stage).
      4. Validate that leaf probabilities sum to 1.

    Implemented as a stub; the reduction and nesting logic is pending.
    """
    cfg.validate()
    raise NotImplementedError("Nest per-stage reductions into a ScenarioTree.")
