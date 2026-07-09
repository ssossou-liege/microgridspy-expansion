"""Investment-layer constraints: capacity accumulation and non-anticipativity.

Implements equations (cap-pv)--(cap-inv), (cap-ge), (ge-monotone) and (ge-transition)
of the formulation. The PV array, battery and inverter are modular and accumulate from
the parent; the generator is a single active unit (a catalogue state) that is replaced
on upgrade. Non-anticipativity is structural (variables are indexed by node), so no
explicit coupling constraints are needed -- only the parent-referencing recursions
below, built by iterating the tree.

Brownfield: the root's parent capacity is the existing fleet C^g_0 (zero for greenfield)
and the root's parent generator state is the incumbent size s_0.
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
    """Add capacity-accumulation and generator-state constraints (per node, vs parent).

    Modular technologies (g in {pv, batt, inv}):
        cap_g[n] == cap_g[parent(n)] + u_g * b_g[n]         (parent(root) = C^g_0)
    Generator (single active unit):
        cap_ge[n] == sum_s kappa_s * z_ge[n,s] ,  sum_s z_ge[n,s] == 1
        cap_ge[n] >= cap_ge[parent(n)]                       (upgrades only)
        ins_ge[n,s] >= z_ge[n,s] - z_ge[parent(n),s]
        ret_ge[n,s] <= z_ge[parent(n),s] ,  ret_ge[n,s] <= 1 - z_ge[n,s]
    with the root's parent state fixed to the incumbent size s_0 (brownfield) or the
    smallest catalogue size (greenfield).
    """
    raise NotImplementedError("Build per-node capacity + generator-state recursion.")
