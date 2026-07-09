"""Configuration: stage calendar, technology catalogues, economic constants and
solver settings.

Economic and technical constants are ported from the THESIS dispatch-assessment
configuration (``src/dispatch_assessment/config.py``) so this repository is
self-contained. Symbols map onto the formulation in
``docs/formulation/model.tex`` as annotated.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Economic constants (ported from THESIS dispatch_assessment/config.py)
# ---------------------------------------------------------------------------
DISCOUNT_RATE = 0.12          # r   -- annual discount rate
PROJECT_YEARS = 25            # planning horizon [yr]

PV_COST_USD_KW = 500.0        # C^inv_pv   [$/kW]
BATT_COST_USD_KWH = 450.0     # C^inv_batt [$/kWh]  (BYD LV Flex LFP)
GEN_COST_USD_KVA = 800.0      # C^inv_ge   [$/kVA]
INV_COST_USD_KW = 150.0       # C^inv_inv  [$/kW]   (placeholder; refine from catalogue)

PV_OM_RATE = 0.018            # O_pv   -- annual O&M as fraction of CAPEX
BATT_OM_RATE = 0.060          # O_batt
GEN_OM_RATE = 0.080           # O_ge
INV_OM_RATE = 0.020           # O_inv

DIESEL_PRICE_USD_L = 1.29     # c^fuel -- central benchmark [$/L]
VOLL_USD_KWH = 2.00           # v      -- value of lost load [$/kWh]

# Generator fuel characteristic (linear): F = F0*y + F1*P_ge  [L/h]
FUEL_F0 = 1.10                # F_0 -- no-load intercept [L/h]
FUEL_F1 = 0.252               # F_1 -- incremental slope [L/kWh]

# Battery degradation cost [$/kWh discharged] = replacement / lifetime throughput
BATT_CYCLES = 6000
BATT_LIFETIME_Y = 16

# ---------------------------------------------------------------------------
# Battery technical parameters
# ---------------------------------------------------------------------------
ETA_CHARGE = 0.975            # eta^c
ETA_DISCHARGE = 0.975         # eta^d
SOC_MIN_FRAC = 0.05           # underline{e}  -- protective discharge trip
SOC_MAX_FRAC = 0.95           # overline{e}   -- protective charge trip

# Generator
GEN_MIN_LOAD_FRAC = 0.30      # phi^ge -- minimum stable loading fraction

# ---------------------------------------------------------------------------
# Capacity increments and discrete catalogues
# ---------------------------------------------------------------------------
PV_UNIT_KW = 0.5              # u^pv   -- rated power of one PV panel [kW]
BATT_UNIT_KWH = 5.0           # u^batt -- usable energy of one battery module [kWh]

# kappa^ge_s, kappa^inv_s -- discrete catalogue ratings [kW]
GEN_CATALOG_KW = (5.0, 10.0, 18.0, 30.0)
INV_CATALOG_KW = (5.0, 10.0, 20.0, 40.0)


@dataclass
class ModelConfig:
    """Top-level configuration for one model run."""

    # --- Stage calendar (milestone years, relative to commissioning) ---
    stage_years: tuple[int, ...] = (0, 5, 10, 15, 20)

    # --- Scenario-tree shape ---
    n_mc_paths: int = 1000               # Monte-Carlo paths drawn before reduction
    branching: tuple[int, ...] = (1, 3, 2, 2, 2)  # children per stage (root first)
    seed: int = 0

    # --- Time-domain reduction ---
    n_rep_days: int = 8                  # representative days per node

    # --- Operating layer encoding ---
    # "rule_faithful" adds the night-reserve floor (eq. night-reserve);
    # "baseline" uses cost-optimal dispatch within the operating envelope.
    dispatch_variant: str = "rule_faithful"

    # --- Solver ---
    solver: str = "highs"
    time_limit_s: int = 3600
    mip_gap: float = 0.01
    threads: int = 0                     # 0 = solver default

    # --- Economics (frozen copies for convenience) ---
    discount_rate: float = DISCOUNT_RATE
    pv_unit_kw: float = PV_UNIT_KW
    batt_unit_kwh: float = BATT_UNIT_KWH
    gen_catalog_kw: tuple[float, ...] = GEN_CATALOG_KW
    inv_catalog_kw: tuple[float, ...] = INV_CATALOG_KW

    def validate(self) -> None:
        """Check internal consistency (stage count vs branching, etc.)."""
        if len(self.branching) != len(self.stage_years):
            raise ValueError(
                "branching must have one entry per stage in stage_years"
            )
        if self.dispatch_variant not in {"rule_faithful", "baseline"}:
            raise ValueError("dispatch_variant must be 'rule_faithful' or 'baseline'")


def crf(r: float = DISCOUNT_RATE, n: int = PROJECT_YEARS) -> float:
    """Capital recovery factor r(1+r)^n / ((1+r)^n - 1)."""
    return r * (1 + r) ** n / ((1 + r) ** n - 1)


def battery_degradation_cost() -> float:
    """Battery throughput-degradation cost c^deg [$/kWh discharged]."""
    throughput = BATT_CYCLES * (SOC_MAX_FRAC - SOC_MIN_FRAC)  # per kWh of capacity
    return BATT_COST_USD_KWH / throughput
