"""Write solution summaries and figures to the results directory."""
from __future__ import annotations

from pathlib import Path

from ..tree.tree_model import ScenarioTree


def write_report(solution: dict, kpis: dict, tree: ScenarioTree, out_dir: Path) -> None:
    """Write CSV/JSON summaries and dispatch/capacity figures under ``out_dir``.

    Summaries (per-node capacities, expected KPIs, scenario-reduction error) are
    written so they survive the results ``.gitignore`` (filenames beginning with
    ``summary``). Stub for the skeleton.
    """
    raise NotImplementedError("Emit summary CSV/JSON and figures.")
