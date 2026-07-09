Here we establishe the probabilistic framework for estimating community electricity demand with a stochastic load profiles generator which parameters a derived from household census information by linking reference measured consumption behavior to socio-economic household categories. 

Structure and data-flow links

Core analysis scripts
- [src/microgrid_expansion/demand/build_monthly_household_clusters.py]: constructs multi-month demand archetypes, handles inactive and outlier states, and produces monthly cluster summaries.
  
- [src/microgrid_expansion/demand/build_mixture_probabilities.py]: estimates hierarchical Dirichlet-multinomial mixture probabilities by site, household type, and month, with shrinkage and uncertainty intervals.

Input data
- [data/meter_readings/household_customers.csv]: household roster with customer code, socio-economic class, site, and connection timing.
- [data/meter_readings/gbo_meter_readings.parquet]: meter time series for Gbowele.
- [data/meter_readings/sam_meter_readings.parquet]: meter time series for Samionta.

Main outputs
- [data/ramp_params/reference/gbowele_monthly_cluster_summary.csv]: monthly cluster composition and household-type shares for Gbowele.
- [data/ramp_params/reference/samionta_monthly_cluster_summary.csv]: monthly cluster composition and household-type shares for Samionta.
- [data/ramp_params/reference/global_cluster_profiles.csv]: global archetype profiles and aggregate cluster characteristics.
- [data/ramp_params/reference/mixture_probabilities_type_month.csv]: hierarchical posterior mixture probabilities with uncertainty bounds.
- [data/ramp_params/reference/monthly_household_features.csv]: monthly household-level demand indicators used before aggregation.
- [data/ramp_params/reference/monthly_household_cluster_assignments.csv]: household-month category assignments from multi-month segmentation.


The process begins with the harmonization of customer information and meter readings from the two reference localities (Samionta & Gbowele), where each monthly household trajectory is represented through three physically interpretable dimensions: 
    - average daily energy use, 
    - peak demand, and 
    - load factor. 

Because these indicators are naturally heavy-tailed and may contain rare extreme realizations, the behavioral space is regularized through robust transformations and bounded influence assumptions so that highly atypical customer monthly consumption data do not dominate the representation of ordinary consumption dynamics. Households with effectively null monthly consumption are treated as in inactive state before behavioral segmentation, thereby preventing inactivity from being conflated with low but genuine demand.

Behavioral segmentation is then performed jointly across months, rather than independently month by month, in order to produce a stable set of demand archetypes that remain comparable over time and across localities. This multi-month strategy ensures that each archetype has a persistent interpretation and can be used as a transferable latent demand category. After segmentation, each household-month observation is associated with one behavioral category (cluster from RAMP calibration), and empirical compositions are computed by month, locality, and socio-economic household type. At this stage, the analysis does not attempt to identify a deterministic mapping from a given household to a fixed archetype in all contexts; instead, it recognizes that the same socio-economic class may express heterogeneous demand behaviors, and that this heterogeneity must be represented probabilistically.

The final probabilistic layer is formulated through a hierarchical Dirichlet-multinomial construction with shrinkage. At the local level, observed monthly compositions define the multinomial evidence for each combination of locality, household type, and month. At the higher level, a balanced global reference distribution is constructed by giving equal weight to each reference locality, thereby avoiding dominance by whichever locality contributes more observations. Local monthly compositions are then regularized toward this balanced reference through adaptive shrinkage, with the effective regularization strength modulated by local sample support. Consequently, sparse strata, especially those involving household classes that are weakly represented in the observed data, receive broader posterior uncertainty intervals rather than overconfident point estimates. The resulting posterior distributions provide smoothed mixture probabilities for behavioral categories together with explicit credibility bounds, making uncertainty propagation tractable in downstream stochastic demand generation.

Taken together, this sequence transforms raw meter readings and customer socio-economic class into an inferential structure suitable for planning in data-limited environments. The approach preserves empirical realism through measurement-based archetypes, preserves transferability through cross-site balancing and time-stable segmentation, and preserves epistemic caution through hierarchical shrinkage and posterior uncertainty quantification. It is therefore designed to support pre-electrification demand assessment for new localities where only census counts are available, while maintaining a transparent statistical bridge to observed consumption behavior in reference sites.

In operational terms, the estimated mixture probabilities distribution is intended to drive Monte Carlo generation of community load trajectories, so that demand forecasting explicitly propagates uncertainty rather than relying on a single deterministic profile. For each simulation draw, monthly archetype shares are sampled from the posterior mixture probabilities and then translated into synthetic household demand realizations through the stochastic profile generator. In this workflow, RAMP serves as the profile-generation engine, and its behavioral parameters have been calibrated on the same customer and meter datasets used to build the probabilistic mixture model. The resulting ensemble of simulated load curves provides uncertainty-aware planning indicators that can be directly used for robust mini-grid sizing and risk-informed design decisions.




