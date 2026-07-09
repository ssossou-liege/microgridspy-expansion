"""Branch-and-simulate: certified-optimal sizing under the rule-based controller.

Branch-and-bound over the discrete capacity lattice (n_pv, n_batt). At each box:

* LOWER bound  = the cost-optimal box relaxation (an LP with the capacities as
  continuous variables ranging over the box) -- Proposition 1 in
  docs/formulation/model.tex.
* UPPER bound  = Z_rule at an integer point inside the box (forward simulation of the
  rule-based controller).

A box is pruned when its lower bound is >= the incumbent (no integer point in it can
beat the best rule-based sizing found). On termination the incumbent is a certified
eps-global optimum of the rule-based sizing problem z_B*, and Delta_heur = z_B* - z_A*
is the price of the heuristic dispatch.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import dispatch as D
from .dispatch import ToyInstance


@dataclass
class BnSResult:
    n_pv: int
    n_batt: int
    z_B: float                 # certified rule-based optimum
    sizing_A: tuple            # cost-optimal-dispatch optimal sizing (n_pv, n_batt)
    z_A: float                 # cost-optimal-dispatch optimum
    price_abs: float           # z_B - z_A
    price_rel: float           # (z_B - z_A) / z_A
    proven_optimal: bool       # global lower bound meets incumbent
    boxes: int                 # boxes explored
    lp_solves: int             # lower-bound oracle calls
    rule_sims: int             # upper-bound oracle calls
    lattice_size: int          # |X|


def branch_and_simulate(inst: ToyInstance, days: int = 365,
                        tol: float = 1e-6) -> BnSResult:
    """Run branch-and-simulate; return the certified-optimal rule-based sizing."""
    NPV, NB = inst.n_pv_max, inst.n_batt_max
    PV0, B0 = inst.n_pv0, inst.n_batt0        # brownfield floor: never below existing
    u_pv, u_b = inst.u_pv, inst.u_batt

    incumbent, best = float("inf"), (PV0, B0)
    boxes = lp_solves = rule_sims = 0
    min_pruned_lb = float("inf")

    def lb(box):
        nonlocal lp_solves
        lp_solves += 1
        npv_lo, npv_hi, nb_lo, nb_hi = box
        return D.cost_optimal_relaxation(
            inst, (npv_lo * u_pv, npv_hi * u_pv),
            (nb_lo * u_b, nb_hi * u_b), days)

    def ub(npv, nb):
        nonlocal rule_sims
        rule_sims += 1
        return D.total_cost_rule(inst, npv, nb, days)

    stack = [(PV0, NPV, B0, NB)]
    while stack:
        npv_lo, npv_hi, nb_lo, nb_hi = box = stack.pop()
        boxes += 1
        bound = lb(box)
        if bound >= incumbent - tol:
            min_pruned_lb = min(min_pruned_lb, bound)
            continue

        mpv, mnb = (npv_lo + npv_hi) // 2, (nb_lo + nb_hi) // 2
        cand = ub(mpv, mnb)
        if cand < incumbent:
            incumbent, best = cand, (mpv, mnb)

        if npv_lo == npv_hi and nb_lo == nb_hi:
            continue
        if (npv_hi - npv_lo) >= (nb_hi - nb_lo):
            mid = (npv_lo + npv_hi) // 2
            stack.append((npv_lo, mid, nb_lo, nb_hi))
            stack.append((mid + 1, npv_hi, nb_lo, nb_hi))
        else:
            mid = (nb_lo + nb_hi) // 2
            stack.append((npv_lo, npv_hi, nb_lo, mid))
            stack.append((npv_lo, npv_hi, mid + 1, nb_hi))

    # global lower bound = min(incumbent, min LB over pruned boxes); pruned LBs are
    # >= incumbent by construction, so the incumbent is certified globally optimal.
    global_lb = min(incumbent, min_pruned_lb)
    proven = incumbent - global_lb <= 1e-4

    # cost-optimal-dispatch optimum z_A* over the integer lattice (reference)
    z_A, sizing_A = min(
        (D.total_cost_optimal(inst, npv, nb, days), (npv, nb))
        for npv in range(PV0, NPV + 1) for nb in range(B0, NB + 1))

    return BnSResult(
        n_pv=best[0], n_batt=best[1], z_B=incumbent,
        sizing_A=sizing_A, z_A=z_A,
        price_abs=incumbent - z_A, price_rel=(incumbent - z_A) / z_A,
        proven_optimal=proven, boxes=boxes, lp_solves=lp_solves,
        rule_sims=rule_sims, lattice_size=(NPV + 1) * (NB + 1),
    )


def brute_force(inst: ToyInstance, days: int = 365):
    """Full enumeration of the rule-based objective (for validation)."""
    NPV, NB = inst.n_pv_max, inst.n_batt_max
    return min(
        (D.total_cost_rule(inst, npv, nb, days), (npv, nb))
        for npv in range(NPV + 1) for nb in range(NB + 1))


def demo() -> BnSResult:
    """Run the prototype on the default instance and print a report."""
    inst = D.default_instance()

    # empirical check of Proposition 1: cost-optimal <= rule at every lattice point
    max_viol = 0.0
    for npv in range(inst.n_pv_max + 1):
        for nb in range(inst.n_batt_max + 1):
            co = D.cost_optimal_relaxation(
                inst, (npv * inst.u_pv,) * 2, (nb * inst.u_batt,) * 2,
                days=1, include_capex=False)
            ru = D.rule_dispatch(inst, npv * inst.u_pv, nb * inst.u_batt)
            max_viol = max(max_viol, co - ru)

    res = branch_and_simulate(inst)
    bf_z, bf_best = brute_force(inst)

    print("=== Branch-and-simulate prototype (single representative day) ===")
    print(f"lattice |X|                  : {res.lattice_size} points")
    print(f"Proposition 1 check          : max(C_opt - C_rule) = {max_viol:+.4f} "
          f"$/day  [{'OK <= 0' if max_viol <= 1e-6 else 'VIOLATED'}]")
    print(f"rule-based optimum  z_B*     : {res.z_B:9,.2f} $/yr  at "
          f"(n_pv={res.n_pv}, n_batt={res.n_batt})")
    print(f"brute-force optimum          : {bf_z:9,.2f} $/yr  at {bf_best}")
    print(f"certificate matches brute    : {abs(res.z_B - bf_z) < 1e-6}")
    print(f"proven globally optimal      : {res.proven_optimal}")
    print(f"cost-optimal optimum z_A*    : {res.z_A:9,.2f} $/yr  at "
          f"{res.sizing_A}")
    print(f"price of heuristic dispatch  : {res.price_abs:9,.2f} $/yr  "
          f"({100 * res.price_rel:.1f}% of z_A*)")
    print(f"work: B&S {res.rule_sims} rule-sims + {res.lp_solves} LPs over "
          f"{res.boxes} boxes  vs  brute force {res.lattice_size} rule-sims")
    return res


if __name__ == "__main__":
    demo()
