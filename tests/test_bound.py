"""Verification of the dispatch-relaxation bound and branch-and-simulate.

Checks the two claims the contribution rests on (Proposition 1 + the certificate):
  1. cost-optimal operating cost <= rule-based operating cost at every lattice point;
  2. branch-and-simulate returns the same optimum as full enumeration, and proves it.
"""
import numpy as np
import pytest

from microgrid_expansion.exact import dispatch as D
from microgrid_expansion.exact.branch_and_simulate import (
    branch_and_simulate, brute_force,
)


def _small_instance() -> D.ToyInstance:
    inst = D.default_instance()
    inst.n_pv_max = 10          # keep the test fast
    inst.n_batt_max = 6
    return inst


def test_relaxation_lower_bounds_rule_everywhere():
    inst = _small_instance()
    for npv in range(inst.n_pv_max + 1):
        for nb in range(inst.n_batt_max + 1):
            c_opt = D.cost_optimal_relaxation(
                inst, (npv * inst.u_pv,) * 2, (nb * inst.u_batt,) * 2,
                days=1, include_capex=False)
            c_rule = D.rule_dispatch(inst, npv * inst.u_pv, nb * inst.u_batt)
            assert c_opt <= c_rule + 1e-6, (npv, nb, c_opt, c_rule)


def test_branch_and_simulate_matches_brute_force_and_is_proven():
    inst = _small_instance()
    res = branch_and_simulate(inst)
    bf_z, bf_best = brute_force(inst)
    assert abs(res.z_B - bf_z) < 1e-6
    assert (res.n_pv, res.n_batt) == bf_best
    assert res.proven_optimal


def test_price_of_heuristic_is_nonnegative():
    inst = _small_instance()
    res = branch_and_simulate(inst)
    assert res.price_abs >= -1e-6        # z_B* >= z_A*  (Proposition 1)
    assert res.z_A <= res.z_B + 1e-6


def test_branch_and_simulate_prunes():
    inst = _small_instance()
    res = branch_and_simulate(inst)
    # branch-and-bound should evaluate fewer rule-simulations than full enumeration
    assert res.rule_sims < res.lattice_size
