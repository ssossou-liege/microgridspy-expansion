"""Refining the controller: named strategies, gap-minimising tuning, ranking.

Implements the parameterised rule class of the formulation (Section "Refining the
controller"). Every strategy is scored by its gap to the cost-optimal dispatch at the
same sizing -- the operating-cost analogue of the price of the heuristic dispatch. As
the rule is enriched (load-following -> cycle-charging -> tuned) that gap shrinks toward
the certified lower bound.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product

from .. import config
from . import dispatch as D
from .dispatch import ParametricRule, ToyInstance

_PHI = config.GEN_MIN_LOAD_FRAC

# Named strategies as points in the parameter class Theta. Load-following and
# cycle-charging share a common reserve (gamma) and differ only in the generator
# setpoint / hysteresis, so the comparison isolates the dispatch strategy itself.
BASELINE = ParametricRule(e_on=0.05, e_off=0.06, sigma_ge=_PHI, gamma=0.5,
                          name="baseline (uGrid-like)")
LOAD_FOLLOWING = ParametricRule(e_on=0.05, e_off=0.15, sigma_ge=_PHI, gamma=0.5,
                                name="load-following")
CYCLE_CHARGING = ParametricRule(e_on=0.15, e_off=0.70, sigma_ge=0.90, gamma=0.5,
                                name="cycle-charging")


def tune_rule(inst: ToyInstance, cap_pv: float, cap_batt: float) -> tuple[ParametricRule, float]:
    """Grid search over Theta minimising daily operating cost (equation (tune))."""
    e_on_grid = (0.05, 0.20, 0.35)
    e_off_grid = (0.30, 0.55, 0.85)
    sigma_grid = (_PHI, 0.60, 0.90, 1.0)
    gamma_grid = (0.0, 0.5, 1.0, 1.5)

    best, best_cost = None, float("inf")
    for e_on, e_off, sigma, gamma in product(e_on_grid, e_off_grid, sigma_grid, gamma_grid):
        if e_off < e_on:
            continue
        rule = ParametricRule(e_on, e_off, sigma, gamma, name="tuned")
        cost = D.rule_dispatch_param(inst, cap_pv, cap_batt, rule)
        if cost < best_cost:
            best, best_cost = rule, cost
    return best, best_cost


@dataclass
class StrategyScore:
    name: str
    daily_cost: float
    gap_abs: float             # daily_cost - cost-optimal
    gap_rel: float             # gap / cost-optimal


def rank_strategies(inst: ToyInstance, n_pv: int, n_batt: int) -> list[StrategyScore]:
    """Score each strategy by its operating-cost gap to the cost-optimal dispatch."""
    cap_pv, cap_batt = n_pv * inst.u_pv, n_batt * inst.u_batt
    opt = D.cost_optimal_dispatch_milp(inst, cap_pv, cap_batt, days=1)

    tuned, tuned_cost = tune_rule(inst, cap_pv, cap_batt)
    rows = []
    for rule in (BASELINE, LOAD_FOLLOWING, CYCLE_CHARGING, tuned):
        cost = D.rule_dispatch_param(inst, cap_pv, cap_batt, rule)
        rows.append(StrategyScore(rule.name, cost, cost - opt,
                                  (cost - opt) / opt if opt else 0.0))
    rows.append(StrategyScore("cost-optimal (bound)", opt, 0.0, 0.0))
    return rows


def plot_strategies(rows: list[StrategyScore],
                    out_path: str = "results/controller_strategies.png"):
    """Bar chart of each strategy's operating-cost gap to the cost-optimal bound."""
    from pathlib import Path
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    BLUE, RED, GREEN, GREY = "#2a6099", "#bf0041", "#2e8b57", "#6b7280"
    named = [r for r in rows if not r.name.startswith("cost-optimal")]
    names = [r.name for r in named]
    gaps = [100 * r.gap_rel for r in named]
    colors = {"baseline (uGrid-like)": GREY, "load-following": BLUE,
              "cycle-charging": "#e0a106", "tuned": GREEN}
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    bars = ax.bar(names, gaps, color=[colors.get(n, BLUE) for n in names],
                  edgecolor="white")
    ax.axhline(0, color=RED, lw=2)
    ax.text(len(names) - 0.5, 1.5, "cost-optimal bound", color=RED, ha="right", fontsize=10)
    for b, g in zip(bars, gaps):
        ax.text(b.get_x() + b.get_width() / 2, g + 1, f"+{g:.0f}%", ha="center",
                fontsize=10, color="#37474f")
    ax.set_ylabel("operating-cost gap to optimal  [%]")
    ax.set_title("Controller refinement — price of the heuristic dispatch",
                 color=BLUE, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.xticks(rotation=12, ha="right")
    p = Path(out_path); p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return p


def demo(n_pv: int = 24, n_batt: int = 8, plot: bool = True):
    """Rank strategies at a representative sizing and print a table."""
    inst = D.default_instance()
    rows = rank_strategies(inst, n_pv, n_batt)

    print(f"=== Controller strategies at sizing (n_pv={n_pv}, n_batt={n_batt}) ===")
    print(f"{'strategy':<26}{'op.cost $/day':>14}{'gap to optimal':>18}")
    for r in rows:
        tag = "" if r.name.startswith("cost-optimal") else f"  (+{100*r.gap_rel:.1f}%)"
        print(f"{r.name:<26}{r.daily_cost:>14.3f}{'' if r.gap_abs==0 else f'{r.gap_abs:>12.3f}'}{tag}")

    # feasibility / bound check: every rule >= cost-optimal
    opt = next(r for r in rows if r.name.startswith("cost-optimal")).daily_cost
    ok = all(r.daily_cost >= opt - 1e-6 for r in rows)
    print(f"Proposition 1 (all rules >= cost-optimal): {'OK' if ok else 'VIOLATED'}")
    if plot:
        print(f"wrote {plot_strategies(rows)}")
    return rows


if __name__ == "__main__":
    demo()
