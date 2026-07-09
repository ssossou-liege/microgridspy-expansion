"""Monte-Carlo construction of scenario paths over the four uncertainty families.

See Section "Uncertainty space, scenario generation and reduction" of
``docs/formulation/model.tex``.
"""
from .assemble import ScenarioPath, AxisDraw, sample_scenario_paths

__all__ = ["ScenarioPath", "AxisDraw", "sample_scenario_paths"]
