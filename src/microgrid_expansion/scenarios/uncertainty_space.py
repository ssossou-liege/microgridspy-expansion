"""Declarative specification of the four uncertainty families and their marginals.

The four families (formulation, Section "Uncertainty space"):

* **demand**    -- RAMP trajectories: connections per customer type, appliance
  stock (name, count, rated power) and usage patterns (functioning time, time per
  event, time-of-use windows, occasional-use probability).
* **resource**  -- climate pathway in {ssp126, ssp245, ssp370, ssp585}.
* **economic**  -- diesel-price and per-technology investment-cost trajectories.
* **policy**    -- minimum solar-penetration target.

Each entry describes how a value is drawn at a given stage; the concrete
distributions are calibrated from surveys and meter readings.
"""
from __future__ import annotations

from dataclasses import dataclass, field

SSP_PATHWAYS = ("ssp126", "ssp245", "ssp370", "ssp585")


@dataclass
class DemandAxis:
    """Demand uncertainty: parameters handed to the RAMP generator per stage."""

    customer_types: tuple[str, ...] = ("residential", "commercial", "productive")
    # Distribution handles (filled by calibration); placeholders for the skeleton.
    connections_dist: dict = field(default_factory=dict)
    appliance_stock_dist: dict = field(default_factory=dict)
    usage_pattern_dist: dict = field(default_factory=dict)


@dataclass
class ResourceAxis:
    """Renewable-resource uncertainty: a categorical draw over SSP pathways."""

    pathways: tuple[str, ...] = SSP_PATHWAYS
    probabilities: tuple[float, ...] = (0.25, 0.25, 0.25, 0.25)


@dataclass
class EconomicAxis:
    """Economic uncertainty: fuel-price and cost-trajectory drivers."""

    fuel_price_growth_dist: dict = field(default_factory=dict)
    capex_learning_dist: dict = field(default_factory=dict)  # per technology


@dataclass
class PolicyAxis:
    """Policy uncertainty: minimum renewable-penetration target."""

    penetration_levels: tuple[float, ...] = (0.0, 0.5, 0.7)
    probabilities: tuple[float, ...] = (0.34, 0.33, 0.33)


@dataclass
class UncertaintySpace:
    """Container bundling the four families."""

    demand: DemandAxis = field(default_factory=DemandAxis)
    resource: ResourceAxis = field(default_factory=ResourceAxis)
    economic: EconomicAxis = field(default_factory=EconomicAxis)
    policy: PolicyAxis = field(default_factory=PolicyAxis)
