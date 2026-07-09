"""Certified-optimal sizing under the rule-based dispatch policy.

Implements the dispatch-relaxation bound and the branch-and-simulate algorithm of
the formulation (Section "Certified-optimal sizing under the rule-based dispatch
policy" in docs/formulation/model.tex):

* :func:`dispatch.cost_optimal_relaxation` -- the LOWER-bound oracle (an LP over a
  capacity box; the exact cost-optimal value when the box is a point).
* :func:`dispatch.rule_dispatch` -- the UPPER-bound oracle (forward simulation of the
  uGrid generation-balance controller).
* :func:`branch_and_simulate.branch_and_simulate` -- branch-and-bound over the discrete
  capacity lattice returning a certified-optimal rule-based sizing and the price of the
  heuristic dispatch.
"""
from .dispatch import (
    ToyInstance,
    ParametricRule,
    cost_optimal_relaxation,
    cost_optimal_dispatch_milp,
    rule_dispatch,
    rule_dispatch_param,
    total_cost_optimal,
    total_cost_rule,
    default_instance,
)
from .branch_and_simulate import branch_and_simulate, brute_force, demo, BnSResult
from .brownfield import solve_expansion, ExpansionResult
from . import controller, brownfield

__all__ = [
    "ToyInstance",
    "ParametricRule",
    "cost_optimal_relaxation",
    "cost_optimal_dispatch_milp",
    "rule_dispatch",
    "rule_dispatch_param",
    "total_cost_optimal",
    "total_cost_rule",
    "default_instance",
    "branch_and_simulate",
    "brute_force",
    "demo",
    "BnSResult",
    "controller",
    "brownfield",
    "solve_expansion",
    "ExpansionResult",
]
