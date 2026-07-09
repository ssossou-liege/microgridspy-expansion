"""Full-design certified sizing with brownfield initial capacity and generator replacement.

The photovoltaic array, battery and inverter are modular; the generator is a single unit
chosen from a catalogue and upgraded (with resale of the incumbent). The PV/battery core
is certified by :func:`branch_and_simulate`; the inverter module count and the generator
size are swept in an outer loop (few options, upgrades only), and their annualised capex /
resale is added as a per-combination offset. Because the offset is constant within each
branch-and-simulate run, the certificate is preserved and the sweep is exhaustive over the
discrete inverter/generator choices -- so the returned optimum is certified over the whole
design lattice.

Existing capacity is sunk (see :meth:`ToyInstance.capex_annualised` and the brownfield
floor in :func:`branch_and_simulate`); only additions and generator upgrades are charged.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from . import dispatch as D
from .dispatch import ToyInstance
from .branch_and_simulate import branch_and_simulate


@dataclass
class ExpansionResult:
    design_B: tuple          # rule-based optimum (n_pv, n_batt, n_inv, gen_kw)
    z_B: float
    design_A: tuple          # cost-optimal-dispatch optimum
    z_A: float
    price_abs: float
    price_rel: float


def _inv_options(inst: ToyInstance):
    lo = max(inst.n_inv0, 1)                 # at least one inverter module
    return range(lo, inst.n_inv_max + 1)


def _gen_options(inst: ToyInstance):
    return [g for g in inst.gen_catalog if g >= inst.gen_kw0 - 1e-9]  # upgrades only


def solve_expansion(inst: ToyInstance) -> ExpansionResult:
    """Certified rule-based and cost-optimal sizing over the full design lattice."""
    bestB = (float("inf"), None)
    bestA = (float("inf"), None)
    for n_inv in _inv_options(inst):
        for gen_kw in _gen_options(inst):
            inst2 = replace(inst, cap_inv=n_inv * inst.u_inv, cap_ge=gen_kw)
            res = branch_and_simulate(inst2)
            offset = (inst.inverter_capex_annualised(n_inv)
                      + inst.generator_capex_annualised(gen_kw))
            zB = res.z_B + offset
            zA = res.z_A + offset
            if zB < bestB[0]:
                bestB = (zB, (res.n_pv, res.n_batt, n_inv, gen_kw))
            if zA < bestA[0]:
                bestA = (zA, (res.sizing_A[0], res.sizing_A[1], n_inv, gen_kw))
    zB, dB = bestB
    zA, dA = bestA
    return ExpansionResult(dB, zB, dA, zA, zB - zA, (zB - zA) / zA)


def _describe(inst: ToyInstance, d: tuple) -> str:
    n_pv, n_batt, n_inv, gen_kw = d
    return (f"PV {n_pv*inst.u_pv:.1f} kW, batt {n_batt*inst.u_batt:.0f} kWh, "
            f"inv {n_inv*inst.u_inv:.1f} kW, genset {gen_kw:.0f} kW")


def demo():
    """Contrast greenfield vs brownfield certified sizing on the same instance."""
    base = D.default_instance()
    base.n_pv_max, base.n_batt_max, base.n_inv_max = 20, 10, 6

    green = replace(base, n_pv0=0, n_batt0=0, n_inv0=0, gen_kw0=0.0)
    brown = replace(base, n_pv0=10, n_batt0=4, n_inv0=2, gen_kw0=5.0)  # existing fleet

    print("=== Full-design certified sizing: greenfield vs brownfield ===")
    for label, inst in (("greenfield", green), ("brownfield", brown)):
        r = solve_expansion(inst)
        print(f"\n[{label}]  existing: PV {inst.n_pv0*inst.u_pv:.0f} kW, "
              f"batt {inst.n_batt0*inst.u_batt:.0f} kWh, "
              f"inv {inst.n_inv0*inst.u_inv:.0f} kW, genset {inst.gen_kw0:.0f} kW")
        print(f"  rule-based optimum z_B* : {r.z_B:9,.0f} $/yr  ->  {_describe(inst, r.design_B)}")
        print(f"  cost-optimal optimum z_A*: {r.z_A:9,.0f} $/yr  ->  {_describe(inst, r.design_A)}")
        print(f"  price of heuristic       : {r.price_abs:8,.0f} $/yr ({100*r.price_rel:.1f}%)")
        gen_note = ("keeps incumbent" if r.design_B[3] == inst.gen_kw0
                    else f"upgrades genset {inst.gen_kw0:.0f}->{r.design_B[3]:.0f} kW (old resold)")
        if inst.gen_kw0 > 0:
            print(f"  generator decision       : {gen_note}")
    return None


if __name__ == "__main__":
    demo()
