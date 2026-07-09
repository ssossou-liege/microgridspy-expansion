# Roadmap — microgrid-expansion

Next moves for the multi-stage stochastic capacity-expansion model and its core
contribution: **certified-optimal sizing under the fixed rule-based dispatch controller**
(dispatch-relaxation lower bound + branch-and-simulate; the "price of the heuristic
dispatch"). See [docs/formulation/model.tex](formulation/model.tex), section
*Certified-optimal sizing under the rule-based dispatch policy*.

Priorities: **P0** = critical path to a thesis result · **P1** = important · **P2** = nice-to-have.
Each task lists target files and a *Done when* acceptance criterion.

---

## Current state (2026-06-30)

- ✅ Formulation document (`docs/formulation/model.tex`) — sets, parameters, variables,
  constraints, objective, scenario construction, **+ the certified-optimality section**
  (Assumption 1, Proposition 1, branch-and-simulate, price of heuristic). Compiles.
- ✅ Code skeleton under `src/microgrid_expansion/` (`scenarios → tree → timedomain →
  model → solve → post`) — **all stubs raise `NotImplementedError`**.
- ✅ Working prototype of the contribution: `src/microgrid_expansion/exact/`
  (`dispatch.py`, `branch_and_simulate.py`, `plot.py`) + `tests/test_bound.py`.
  Toy single-day result: `z_B* = (30 PV, 10 batt)` vs `z_A* = (29, 8)`, price 3.3 %,
  proven optimal, ~83 % fewer simulations. Figure `results/branch_and_simulate_lattice.png`.
- ✅ Presentation deck `docs/model_formulation.odp` (22 slides, 7 figures).
- ✅ Literature scan: contribution confirmed novel (see memory + model.tex prior-work paragraph).
- ✅ Initial commit done and pushed to github remote repo
- ⬜ No real data imported; conda env not yet created.

---

## Phase 0 — Foundations & housekeeping (P0, ~0.5 day)

- [ ] ✅ **Create the environment.** `conda env create -f environment.yml`, then
  `pip install -e .`; confirm `linopy`, `highspy`, `scikit-learn-extra`, `rampdemand`
  import. *Done when* `python -m pytest tests/ -q` runs (config + bound tests pass).
- [ ] ✅ **Commit the current work.** Branch off `main`; commit `exact/`, the formulation
  section, deck, tests and figure with a clear message. *Done when* `git status` is clean
  and history shows the contribution.
- [ ] **Import data from THESIS** into `data/` per `data/README.md` (RAMP params,
  `*solar_irradiance*.csv`, `demand_8760.csv` for SAM and GBO), recording provenance.
  *Done when* the provenance table in `data/README.md` is filled and files load.
- [ ] **Save the deck/figure generators** into the repo (`docs/build_slides.py`,
  `docs/figs.py`) so the presentation is reproducible. *Done when* re-running them
  regenerates `docs/model_formulation.odp`.

---

## Phase 1 — Make the exact method real on ONE site (P0, ~1–2 weeks)

Goal: replace the toy with the real oracles and produce a certified rule-based sizing +
`Δ_heur` on actual Benin (SAM or GBO) data, single scenario. This is the minimum
publishable result.

- [ ] **Real rule-based simulator (UB oracle).** Port uGrid `GenControl()` faithfully into
  `exact/dispatch.py` (or a new `exact/simulator.py`): `batt_calcs` temperature + self-
  discharge, `fuel_calcs` quadratic genset efficiency, the `loadLeft` night-reserve
  look-ahead. Source: `THESIS/external/uGrid/uGrid/technical_tools_PC_3_alt.py`.
  *Done when* it reproduces uGrid's dispatch on a shared 8760 within tolerance.
- [ ] **Real cost-optimal dispatch (LB oracle).** Port `THESIS/src/dispatch_assessment/
  stage3.py` MILP to linopy over representative days, with capacities as box-bounded
  variables. Expose two modes: **LP relaxation** (drop commitment binary → fast, valid LB)
  and **MILP** (tight LB). *Done when* both return values and LP ≤ MILP ≤ rule at sample
  points.
- [ ] **Real economics.** Reuse `THESIS/src/dispatch_assessment/stage2.py` NPC/LCOE/CRF/
  replacement/salvage in `post/kpis.py`; feed annualised cost into the oracles instead of
  the toy capex. *Done when* a single sizing reproduces the THESIS benchmark
  (PV 8.2 kW, batt 17.2 kWh, gen 5.85 kW, LCOE 0.3211).
- [ ] **Generalise the lattice** to (PV panels, battery modules, genset size, inverter
  size) in `exact/branch_and_simulate.py`; branch on all integer/catalog dimensions.
  *Done when* B&S certifies the optimum on a ≥3-D lattice and matches enumeration on a
  coarse grid.
- [ ] **Validate on real single-site data** (8760 → representative days via
  `timedomain/rep_days.py`). Report `z_B*`, `z_A*`, `Δ_heur` (abs + %), certified gap,
  runtime, and #oracle calls vs enumeration. *Done when* a results table + figure are
  written under `results/` and `tests/test_benchmark.py` passes.

**Risk:** Assumption 1 (rule trajectory feasible for the cost-optimal set). Verify the
ported `GenControl` never violates `F(x)` (no simultaneous charge/discharge, respects
min-load / SOC trips). If it can, document the correction or restrict `F(x)` accordingly.

---

## Phase 2 — Stochastic multi-scenario / tree extension (P1, ~2–3 weeks)

Goal: expected `Δ_heur` across a reduced scenario tree on Benin data (the full thesis
result). Fills the skeleton.

- [ ] **Scenario generation** — implement `scenarios/{demand_paths,pv_paths,cost_paths,
  mc_sampler,assemble}.py`: RAMP demand draws (wrap THESIS `CalibratedModels` +
  `ramp_evolution_extension`), SSP PV profiles, fuel/capex trajectories, policy draws.
  *Done when* `sample_scenario_paths(cfg)` returns resolved `ScenarioPath`s with 8760 arrays.
- [ ] **Scenario reduction + tree** — implement `tree/{reduce,build_tree}.py` (per-stage
  k-medoids / fast-forward → branching tree; path probabilities; report reduction error).
  *Done when* `build_tree` returns a `ScenarioTree` with `check_probabilities()` passing.
- [ ] **Time-domain reduction** — implement `timedomain/rep_days.py` (weighted k-medoids
  representative days; derive `σ`, `f_e`, `R` per the formulation). *Done when* rep-day
  costs match full-8760 within ~5 %.
- [ ] **Full LB = deterministic-equivalent MILP relaxation** — fill `model/{coords,
  variables,investment_constraints,dispatch_constraints,economics,build}.py` (the linopy
  model). The relaxed solve is the tree-wide lower bound. *Done when* `build_model` solves
  and reproduces the single-node case from Phase 1.
- [ ] **Branch-and-simulate over the tree** — outer branch over the per-node capacity
  plan; LB = tree MILP relaxation on the capacity box; UB = rule simulation per
  (node, scenario, rep-day). Wire through `run.py`. *Done when* `python -m
  microgrid_expansion.run` returns expected NPC/LCOE + expected `Δ_heur` with a certificate.

---

## Phase 3 — Theory hardening & the open question (P1, ongoing)

- [ ] **Prove Assumption 1 for the uGrid controller** rigorously (feasibility within
  `F(x)`); enumerate and dispatch edge cases. *Done when* a lemma + proof are in model.tex.
- [ ] **Tighten / accelerate the bound.** Add monotonicity-based pruning (operating cost
  ↓ in capacity, capex ↑), size-specific big-M, and an LP-vs-MILP LB trade-off study.
  *Done when* node counts drop measurably on the real lattice and the effect is tabulated.
- [ ] **Multi-stage SDDiP angle (open research).** Test the conjecture that a fixed
  (non-optimising) rule-based recourse removes the integer recourse that obstructs SDDP/
  SDDiP, making exact multi-stage decomposition possible. Start with a proof sketch + a
  targeted literature check. *Done when* either a proof/counterexample exists or it is
  scoped out with justification.
- [ ] **Complexity / convergence note** for branch-and-simulate (finite lattice ⇒
  finite termination; gap behaviour vs bound tightness). *Done when* stated in model.tex.

---

## Phase 4 — Dissemination (P2)

- [ ] **Deck slide(s)** for the contribution: the bound inequality, branch-and-simulate
  schematic, and `results/branch_and_simulate_lattice.png`. Add to `docs/build_slides.py`.
- [ ] **Paper / chapter outline** centred on the method + the price-of-heuristic result,
  positioned against HOMER/iHOGA (no certificate) and the MILP camp (cost-optimal only).
- [ ] **Reproducibility**: CI running `pytest`; pin solver versions; seed all stochastic
  steps. *Done when* a fresh clone reproduces the headline numbers.

---

## Open questions / watch-list

- Does the lower-bound inequality hold under *all* the diesel min-load / reserve / unit-
  commitment rules, or can the rule sometimes leave `F(x)`? (Assumption 1 — Phase 3.)
- Multi-stage adaptivity with a *fixed* policy: open-loop plan vs a parameterised decision
  rule for the UB simulation (the LB/certificate are unaffected).
- The rule-based-sizing space is active (Nespoli & Medici, Nov 2025) — re-scan before
  submission to confirm novelty still holds.
- Tightness of `Δ_heur`: a small gap justifies the heuristic's simplicity; a large gap is
  itself the headline result. Either way it is reportable.
