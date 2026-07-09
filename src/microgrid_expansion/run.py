"""End-to-end orchestrator: sample -> reduce -> build -> solve -> report.

Run with::

    python -m microgrid_expansion.run

The pipeline mirrors the formulation: draw a Monte-Carlo ensemble over the four
uncertainty families, reduce it into a scenario tree, compress each node's operating
year into representative days, assemble and solve the deterministic-equivalent MILP,
then extract KPIs and write a report.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from .config import ModelConfig
from .scenarios import sample_scenario_paths
from .tree import build_tree
from .timedomain import reduce_to_rep_days
from .model import build_model
from .solve import solve
from .post import extract_solution, expected_npc_lcoe
from .post.report import write_report

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"


def run(cfg: ModelConfig, out_dir: Path = RESULTS_DIR) -> dict:
    """Execute the full pipeline and return the expected-cost KPIs."""
    cfg.validate()

    paths = sample_scenario_paths(cfg)
    tree = build_tree(paths, cfg)
    tree.check_probabilities()

    rep = {n: reduce_to_rep_days(tree.node_data[n], cfg.n_rep_days, cfg.seed)
           for n in tree.nodes}

    model = build_model(tree, rep, cfg)
    result = solve(model, cfg)

    solution = extract_solution(model, tree)
    kpis = expected_npc_lcoe(solution, tree)
    write_report(solution, kpis, tree, out_dir)
    return {"solve": result, "kpis": kpis}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", default="highs", choices=["highs", "gurobi"])
    parser.add_argument("--variant", default="rule_faithful",
                        choices=["rule_faithful", "baseline"])
    parser.add_argument("--rep-days", type=int, default=8)
    parser.add_argument("--mc-paths", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)

    cfg = ModelConfig(
        solver=args.solver,
        dispatch_variant=args.variant,
        n_rep_days=args.rep_days,
        n_mc_paths=args.mc_paths,
        seed=args.seed,
    )
    out = run(cfg)
    print(out)


if __name__ == "__main__":
    main()
