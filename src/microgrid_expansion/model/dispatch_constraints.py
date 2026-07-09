"""Operating-layer constraints: the rule-based generation-balance control.

Implements equations (balance), (ge-cap)--(ge-min), (soc-dynamics)--(inv-bounds),
(night-reserve) and (slacks) of the formulation, broadcast over
``(node, rday, htod)``.

Two variants (selected by ``cfg.dispatch_variant``):

* ``"baseline"``      -- power balance + generator + storage + slacks, with the
  operating economics alone driving a cost-optimal dispatch within the envelope.
* ``"rule_faithful"`` -- additionally imposes the deterministic night-reserve floor
  ``e >= R`` (eq. night-reserve), reproducing the uGrid look-ahead controller with
  no extra binary.

The single binary per time step is the generator commitment ``y``.
"""
from __future__ import annotations

import linopy

from ..config import ModelConfig
from .coords import Coords


def add_dispatch_constraints(
    m: linopy.Model,
    v: dict,
    c: Coords,
    cfg: ModelConfig,
    params: dict,
) -> None:
    """Add the operating constraints.

    Parameters
    ----------
    params
        xarray DataArrays on ``(node, rday, htod)``: demand ``D``, specific yield
        ``rho``, self-discharge ``sigma``, usable-capacity factor ``f_e`` and
        night-reserve ``R`` (per unit battery capacity).

    Constraints added:
        balance        rho*cap_pv - q + P_ge + P_dis - P_ch == D - l
        ge_cap         P_ge <= cap_ge
        ge_on          P_ge <= M * y
        ge_min         P_ge >= phi*sum_s kappa_s z_ge - M*(1-y)
        soc_dynamics   e[h+1] == (1-sigma) e[h] + eta_c P_ch - P_dis/eta_d
        soc_cyclic     e[0] == e[24]
        soc_bounds     e_lo*cap_batt <= e <= e_hi*f_e*cap_batt
        inv_bounds     P_ch <= cap_inv ; P_dis <= cap_inv
        curtail/ens    0 <= q <= rho*cap_pv ; 0 <= l <= D
        night_reserve  e >= R*cap_batt          (rule_faithful only)
    """
    raise NotImplementedError("Encode the generation-balance dispatch constraints.")
