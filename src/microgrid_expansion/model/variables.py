"""Declare the linopy decision variables on the coordinate system.

Investment layer (per node) and operating layer (per node, representative day,
hour), matching Section "Decision variables" of the formulation. The only integer
operating variable is the generator commitment ``y`` (one per time step).
"""
from __future__ import annotations

import linopy

from .coords import Coords


def add_variables(m: linopy.Model, c: Coords) -> dict:
    """Add all variables to ``m`` and return a name -> Variable mapping.

    Investment:
        b_pv[node], b_batt[node], b_inv[node]   integer >= 0  (modular modules added)
        z_ge[node, gsize]                        binary        (single active genset size)
        ins_ge[node, gsize], ret_ge[node, gsize] in [0,1]      (install / retire transition)
        cap_pv, cap_batt, cap_ge, cap_inv [node] continuous >= 0
    Operating (node, rday, htod):
        P_ge, P_ch, P_dis, e, q (curtail), l (ens)   continuous >= 0
        y   binary (generator on/off)
    """
    raise NotImplementedError(
        "Declare investment and operating variables via m.add_variables(...)."
    )
