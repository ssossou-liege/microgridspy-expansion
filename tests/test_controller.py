"""Verification of the parameterised controller and gap-minimising tuning.

Checks the properties the controller-refinement subsection relies on:
  1. every parameterised rule is feasible, so its cost is >= the cost-optimal dispatch
     with the same cost structure (Proposition 1, controller-invariance);
  2. gap-minimising tuning does no worse than the named strategies (it can only help).
"""
import pytest

from microgrid_expansion.exact import dispatch as D
from microgrid_expansion.exact import controller as C


def _inst():
    return D.default_instance()


def test_every_rule_dominated_by_cost_optimal():
    inst = _inst()
    cap_pv, cap_batt = 24 * inst.u_pv, 8 * inst.u_batt
    opt = D.cost_optimal_dispatch_milp(inst, cap_pv, cap_batt, days=1)
    for rule in (C.BASELINE, C.LOAD_FOLLOWING, C.CYCLE_CHARGING):
        cost = D.rule_dispatch_param(inst, cap_pv, cap_batt, rule)
        assert cost >= opt - 1e-6, (rule.name, cost, opt)


def test_tuning_beats_named_strategies():
    inst = _inst()
    cap_pv, cap_batt = 24 * inst.u_pv, 8 * inst.u_batt
    _, tuned_cost = C.tune_rule(inst, cap_pv, cap_batt)
    named = [D.rule_dispatch_param(inst, cap_pv, cap_batt, r)
             for r in (C.BASELINE, C.LOAD_FOLLOWING, C.CYCLE_CHARGING)]
    assert tuned_cost <= min(named) + 1e-6


def test_tuned_gap_is_nonnegative():
    inst = _inst()
    cap_pv, cap_batt = 24 * inst.u_pv, 8 * inst.u_batt
    opt = D.cost_optimal_dispatch_milp(inst, cap_pv, cap_batt, days=1)
    _, tuned_cost = C.tune_rule(inst, cap_pv, cap_batt)
    assert tuned_cost >= opt - 1e-6
