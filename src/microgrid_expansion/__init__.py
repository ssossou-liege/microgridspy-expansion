"""Multi-stage stochastic capacity-expansion model for off-grid microgrid sizing.

The package is organised to mirror the formulation in
``docs/formulation/model.tex``:

* :mod:`microgrid_expansion.scenarios` -- Monte-Carlo sampling of the four
  uncertainty families (demand, renewable resource, economics, policy).
* :mod:`microgrid_expansion.tree` -- scenario reduction and scenario-tree
  construction (Section "Uncertainty space" of the formulation).
* :mod:`microgrid_expansion.timedomain` -- representative-day time-domain
  reduction.
* :mod:`microgrid_expansion.model` -- linopy variables, constraints, economics
  and assembly of the deterministic-equivalent MILP.
* :mod:`microgrid_expansion.solve` -- solver driver.
* :mod:`microgrid_expansion.post` -- solution extraction, KPIs and reporting.
"""

__version__ = "0.1.0"
