"""Investment-layer constraints: capacity accumulation and non-anticipativity.

Implements equations (cap-pv)--(cap-inv) of the formulation. Capacity at a node is
the capacity inherited from its parent plus the increment added at the node; the
root's parent capacity is zero. Non-anticipativity is structural (variables are
indexed by node), so no explicit coupling constraints are needed -- only the
parent-referencing recursion below, built by iterating the tree.
"""
from __future__ import annotations

import linopy

from ..config import ModelConfig
from .coords import Coords


def add_investment_constraints(
    m: linopy.Model,
    v: dict,
    c: Coords,
    cfg: ModelConfig,
) -> None:
    """Add capacity-accumulation constraints (one per node, referencing the parent).

    For each node n and technology g:
        cap_g[n] == cap_g[parent(n)] + increment_g[n]
    with cap_g[parent(root)] == 0. Increments are u^pv*b_pv, u^batt*b_batt, and the
    catalogue-weighted sums sum_s kappa_s * x_{n,s}; also enforces
    sum_s x_ge[n,s] <= 1 and sum_s x_inv[n,s] <= 1.
    """
    raise NotImplementedError("Build per-node capacity recursion over the tree.")
