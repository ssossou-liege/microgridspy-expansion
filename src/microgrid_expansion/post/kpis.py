"""Key performance indicators: net present cost and levelised cost of electricity.

Reuses the THESIS net-present-cost accounting (``src/dispatch_assessment/stage2.py``):
capital cost, O&M, fuel, periodic battery replacement and end-of-horizon salvage,
annualised through the capital recovery factor. KPIs are reported per node and as the
probability-weighted expectation over the tree.
"""
from __future__ import annotations

from .. import config
from ..tree.tree_model import ScenarioTree


def node_kpis(solution: dict, node: int, tree: ScenarioTree) -> dict:
    """Return NPC, LCOE, renewable penetration, diesel dependency and LPSP for a node.

    Stub: implement using the extracted solution and the ported NPC/LCOE math,
    including battery replacement (every ``config.BATT_LIFETIME_Y`` years) and salvage.
    """
    raise NotImplementedError("Compute per-node NPC/LCOE/REP/DD/LPSP.")


def expected_npc_lcoe(solution: dict, tree: ScenarioTree) -> dict:
    """Return probability-weighted expected NPC and LCOE over the leaves."""
    raise NotImplementedError("Aggregate node KPIs by leaf probability pi_n.")
