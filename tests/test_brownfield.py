"""Verification of brownfield expansion, modular inverter and generator replacement.

Checks the properties the brownfield/replacement formulation relies on:
  1. the price of the heuristic stays non-negative (Proposition 1) for greenfield and
     brownfield alike -- i.e. the incremental (sunk-adjusted) capex is consistent between
     the cost-optimal and rule oracles;
  2. an existing fleet is sunk, so brownfield total cost <= greenfield total cost;
  3. the generator obeys upgrades-only (never below the incumbent size).
"""
from dataclasses import replace

import pytest

from microgrid_expansion.exact import dispatch as D
from microgrid_expansion.exact.brownfield import solve_expansion


def _small():
    base = D.default_instance()
    base.n_pv_max, base.n_batt_max, base.n_inv_max = 8, 5, 3
    base.gen_catalog = (5.0, 10.0)
    return base


def test_price_nonnegative_greenfield_and_brownfield():
    base = _small()
    green = replace(base, n_pv0=0, n_batt0=0, n_inv0=0, gen_kw0=0.0)
    brown = replace(base, n_pv0=4, n_batt0=2, n_inv0=1, gen_kw0=5.0)
    for inst in (green, brown):
        r = solve_expansion(inst)
        assert r.price_abs >= -1e-6, (inst.gen_kw0, r.price_abs)   # z_B* >= z_A*


def test_existing_fleet_is_sunk():
    base = _small()
    green = replace(base, n_pv0=0, n_batt0=0, n_inv0=0, gen_kw0=0.0)
    brown = replace(base, n_pv0=4, n_batt0=2, n_inv0=1, gen_kw0=5.0)
    rg, rb = solve_expansion(green), solve_expansion(brown)
    assert rb.z_B <= rg.z_B + 1e-6           # existing capacity can only help


def test_generator_upgrades_only():
    base = _small()
    brown = replace(base, n_pv0=4, n_batt0=2, n_inv0=1, gen_kw0=5.0)
    r = solve_expansion(brown)
    assert r.design_B[3] >= brown.gen_kw0 - 1e-9   # never downsize the genset
