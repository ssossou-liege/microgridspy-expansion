"""Build the xarray coordinate system shared by all model variables.

Dimensions (formulation, Section "Sets and indices"):

* ``node``  -- scenario-tree node n.
* ``rday``  -- representative day t within a node.
* ``htod``  -- hour-of-day h in 0..23.
* ``gsize`` -- generator catalogue option s (single active unit; the PV array, battery
  and inverter are modular integer counts, not catalogue dimensions).

Because the number of representative days is uniform across nodes in the skeleton,
dispatch variables live on the dense ``(node, rday, htod)`` grid. Per-node scalars
(stage, parent, prob, disc, n_years) are carried as aligned coordinates, not extra
dimensions.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..config import ModelConfig
from ..tree.tree_model import ScenarioTree
from ..timedomain.rep_days import RepDays


@dataclass
class Coords:
    """Coordinate arrays and aligned per-node attributes for model construction."""

    node: np.ndarray
    rday: np.ndarray
    htod: np.ndarray
    gsize: np.ndarray
    parent: dict[int, int | None]
    prob: pd.Series          # indexed by node
    disc: pd.Series
    n_years: pd.Series


def build_coords(
    tree: ScenarioTree,
    rep: dict[int, RepDays],
    cfg: ModelConfig,
) -> Coords:
    """Assemble the coordinate system from the tree, representative days and config."""
    nodes = np.array(tree.nodes)
    return Coords(
        node=nodes,
        rday=np.arange(cfg.n_rep_days),
        htod=np.arange(24),
        gsize=np.arange(len(cfg.gen_catalog_kw)),
        parent=tree.parent,
        prob=pd.Series(tree.prob),
        disc=pd.Series(tree.disc),
        n_years=pd.Series(tree.n_years),
    )
