#### name: "bureaucratic-incentive-topology"
description: "Classify the host society's bureaucratic incentive structure and facilitation-cost regime (money-toll vs. time-queue attrition vs. dual predatory extraction) by reading AGOP's counter-party Nash equilibrium, Weisfeiler-Lehman structural diversity, and regulatory axis alongside free World Bank B-READY, CPI, and WGI telemetry; cap delta as facilitation drag rises."

#### Bureaucratic Incentive Topology (AGOP-Coupled)

This skill evaluates how institutional incentive structures impose operational friction, categorizing costs into monetary tolls, time attrition, or dual extraction using AGOP telemetry and international governance indices [Niskanen 1971, Shleifer & Vishny 1998, North et al. 2009]. 

#### Core Operational Mechanics

1. **Readings & Inputs:** Combines agop state fields (agop.regulatory_score, counter-party mixed strategy σ_CP, Weisfeiler–Lehman structural classes n_wl_classes, and capacity K_derived) with snapshot.external_data["incentive_topology"] (covering fee tiers, turnaround time in weeks, gatekeeper incentives, and persistence drag) [Stigler 1971, Tullock 1967].
2. **Taxonomy States:** Evaluates the environment into four primary tiers: 

  * **GRABBING_HAND:** Severe predatory extraction (delta cap: 0.10, halved to 0.05 if entrenched) [Shleifer & Vishny 1993].
  * **QUEUE_ATTRITION:** Time-rationing and blame-avoiding delay (delta cap: 0.25, halved to 0.125 if entrenched) [De Soto 1989].
  * **TOLL_BOOTH:** Explicit fee-for-service compliance costs (delta cap: 0.75, halved to 0.375 if entrenched) [Niskanen 1971].
  * **RULE_BOUND_MARKET:** Aligned, low-friction environment (delta cap: 1.0).
3. **Execution & Capping:** Automatically caps delta when institutional friction thresholds are breached and cites "bureaucratic-incentive-topology" strictly when the cap binds [Beer 1972, Ramadge & Wonham 1987]. Full schemas, JSON formats, and open-source data sources (World Bank B-READY, WGI, Transparency International, OECD PMR) are detailed in the repository documentation.