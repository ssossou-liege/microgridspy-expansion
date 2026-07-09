"""Visualise the branch-and-simulate result over the capacity lattice.

Produces a heatmap of the rule-based annualised cost Z_rule over (n_pv, n_batt), with
the rule-based optimum z_B* and the cost-optimal-dispatch optimum z_A* marked -- showing
that the heuristic controller shifts the optimal sizing (the reason the certified
rule-based method is needed).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import dispatch as D
from .branch_and_simulate import branch_and_simulate

BLUE, RED = "#2a6099", "#bf0041"


def plot_lattice(out_path: str | Path = "results/branch_and_simulate_lattice.png"):
    inst = D.default_instance()
    res = branch_and_simulate(inst)

    NPV, NB = inst.n_pv_max, inst.n_batt_max
    Z = np.empty((NB + 1, NPV + 1))
    for npv in range(NPV + 1):
        for nb in range(NB + 1):
            Z[nb, npv] = D.total_cost_rule(inst, npv, nb) / 1000.0  # k$/yr

    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    im = ax.imshow(Z, origin="lower", aspect="auto", cmap="viridis_r",
                   extent=[0, NPV, 0, NB])
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("rule-based annualised cost  Z_rule  [k$/yr]")

    ax.scatter([res.n_pv], [res.n_batt], s=190, marker="*", color=RED,
               edgecolor="white", linewidth=1.2, zorder=5,
               label=f"rule optimum z_B*  ({res.n_pv}, {res.n_batt})")
    ax.scatter([res.sizing_A[0]], [res.sizing_A[1]], s=130, marker="o",
               facecolor="none", edgecolor="white", linewidth=2.2, zorder=5,
               label=f"cost-opt optimum z_A*  {res.sizing_A}")

    ax.set_xlabel("PV panels  n_pv  (×%.2g kW)" % inst.u_pv)
    ax.set_ylabel("battery modules  n_batt  (×%.2g kWh)" % inst.u_batt)
    ax.set_title("Certified rule-based sizing  —  price of heuristic "
                 f"{100 * res.price_rel:.1f}%", color=BLUE, fontweight="bold")
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path, res


if __name__ == "__main__":
    path, res = plot_lattice()
    print(f"wrote {path}")
    print(f"z_B*={res.z_B:,.0f} at ({res.n_pv},{res.n_batt}); "
          f"z_A*={res.z_A:,.0f} at {res.sizing_A}; "
          f"price {100*res.price_rel:.1f}%")
