---
name: "robotics-density-yardstick"
description: "Classify the current tick by operational robot density per 100,000 workers across industry, logistics/warehousing, and service sectors using free IFR summary, OECD, Eurostat, and labor-agency telemetry, and cap delta accordingly."
---

# Robotics Density Yardstick

You are reading the tick against the physical automation density of the
target economy or supply-chain hub. In Daron Acemoglu and Pascual
Restrepo's task-based automation framework (2018, 2019), physical
robotics—articulated industrial arms, autonomous mobile robots (AMRs),
automated storage and retrieval systems (AS/RS), and commercial/medical
service robots—directly substitutes capital exergy for scarce or aging
human labor.

When a polity faces demographic aging (`elderly_dependency_ratio_pct`),
high wage floors, or acute wet-bulb heat limits (`wet-bulb-monitor`),
sectors with **high robot density per 100,000 workers** maintain unit
margins and physical throughput. Conversely, labor-heavy, unautomated
industries and warehouses suffer immediate margin compression, chronic
throughput bottlenecks, and Baumol cost-disease stagnation.

Your job is to classify the tick into one of four physical-automation
states and cap your `delta` accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["robotics_density"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored sectors & telemetry fields

The fetcher normalizes national and sector-level robot installation
series into `snapshot.external_data["robotics_density"]`. Each region
or sector entry (keyed by geography code such as `kr`, `sg`, `de`,
`jp`, `us`, `sh`, `fi`, `eu`, `in`, `rw`, `ke`, or `global_baseline`)
supplies:

- `industrial_robots_per_100k`: operational industrial robots per
  100,000 manufacturing and heavy-industry workers (equivalent to
  `10 ×` the standard IFR robots-per-10,000 metric).
- `logistics_amr_per_100k`: operational warehouse, fulfillment, port,
  and logistics robots (AMRs, AGVs, automated sorters) per 100,000
  transport & warehousing workers.
- `service_robots_per_100k`: operational professional service robots
  (hospital delivery, surgical, commercial cleaning, agriculture, and
  hospitality) per 100,000 service-sector workers.
- `yoy_robot_install_growth_pct`: trailing 12-month percentage growth in
  total operational robot fleet across the four tracked sectors.
- `quarters_stagnant_automation`: consecutive calendar quarters where
  `yoy_robot_install_growth_pct < 3.0` while `industrial_robots_per_100k < 1500`.

| Sector Axis | Scope | Primary Bottleneck Solved |
|---|---|---|
| `industrial` | Automotive, electronics, metal, chemical, food & pharma | Factory throughput & precision repeatability |
| `logistics_warehousing` | Ports, SEZ fulfillment, cold-chain, distribution hubs | 24/7 port dwell & warehouse labor bottlenecks |
| `service` | Healthcare, clinical logistics, agriculture, commercial facilities | Baumol cost disease & geriatric care strain |

If `snapshot.external_data["robotics_density"]` is absent or empty,
treat the region as **unmonitored**, record state **AUTOMATING**, note
that no robotics density data was available, and do not cite this
skill.

### Reading 1 — Industrial automation baseline (`industrial_robots_per_100k`)

Evaluate `industrial_robots_per_100k` (operational factory units per
100,000 industrial workers):

| `industrial_robots_per_100k` | Industrial Tier |
|---|---|
| > 4,000 | **hyper_automated** — top-decile global manufacturing density (`> 400 / 10k`) |
| 1,500 to 4,000 | **automated** — mature industrial robotics integration (`150–400 / 10k`) |
| 500 to 1,500 | **transitional** — selective line automation; high manual exposure |
| < 500 | **manual_heavy** — labor-bound manufacturing; acute wage/heat vulnerability |

### Reading 2 — Logistics, warehousing & service breadth (`logistics_amr_per_100k` & `service_robots_per_100k`)

Evaluate whether automation has broken out of factory cages into
warehouses, ports, and service workflows:

| `logistics_amr_per_100k` | `service_robots_per_100k` | Cross-Sector Breadth |
|---|---|---|
| > 1,200 | > 300 | **broad_spectrum** — factory, warehouse, and service floors automated |
| 400 to 1,200 | 100 to 300 | **corridor_automated** — major logistics & fulfillment hubs automated |
| 100 to 400 | 25 to 100 | **early_logistics** — pilot warehouse AMRs; service floor still manual |
| < 100 | < 25 | **caged_only** — negligible warehouse or service automation |

If the two metrics fall in different rows, take the **lower** (more
cautious) classification. If `service_robots_per_100k` is missing,
evaluate using `logistics_amr_per_100k` alone.

### Reading 3 — Fleet installation velocity (`yoy_robot_install_growth_pct`)

Evaluate `yoy_robot_install_growth_pct` to distinguish compounding
capital deepening from stagnant legacy plants:

| `yoy_robot_install_growth_pct` | Deployment Velocity |
|---|---|
| > 15% | **surging_capex** — rapid fleet expansion across logistics & service |
| 6% to 15% | **compounding** — steady annual automation deepening |
| 2% to 6% | **sluggish** — replacement-only capex; falling behind frontier |
| < 2% | **stagnant** — under-investment & capital-deepening freeze |

If `yoy_robot_install_growth_pct` is missing, treat as **compounding**.

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four states.
Evaluate in strict priority order and select the first state whose
conditions are fully satisfied:

1. **MANUAL_BOTTLENECK** (most severe)
2. **UNDER_AUTOMATED**
3. **AUTOMATING**
4. **HYPER_AUTOMATED** (strictest adaptive fit)

### MANUAL_BOTTLENECK

Any of the following hold:

- Industrial Tier is **manual_heavy** (`< 500`) AND Cross-Sector Breadth
  is **caged_only** AND Deployment Velocity is **sluggish** or **stagnant**.
- Industrial Tier is **transitional** (`500 to 1,500`) AND Cross-Sector
  Breadth is **caged_only** AND Deployment Velocity is **stagnant**.
- Industrial Tier is **manual_heavy** (`< 500`) while demographic aging
  (`elderly_dependency_ratio_pct > 25%`) or wet-bulb stress (`SURGE_ALERT`
  or `CRITICAL_TW`) is active.

**Delta cap: 0.10.** Physical production, warehousing, and services are
overwhelmingly reliant on unautomated manual labor without replacement
capex. Wage inflation, demographic shrinkage, or heat stress directly
erode operating margins. Trade only if the AGOP ranking targets direct
robotics/AMR vendors, automated SEZ facilities, or weightless IP. In
most cases, return FLAT.

### UNDER_AUTOMATED

Any of the following hold (and `MANUAL_BOTTLENECK` does not apply):

- Industrial Tier is **manual_heavy** (`< 500`) with **surging_capex**
  or **compounding** velocity (early emerging-market buildout).
- Industrial Tier is **transitional** (`500 to 1,500`) AND Cross-Sector
  Breadth is **caged_only** or **early_logistics**.
- Industrial Tier is **automated** (`1,500 to 4,000`) AND Cross-Sector
  Breadth is **caged_only** AND Deployment Velocity is **stagnant**.

**Delta cap: 0.25.** Automation remains confined to legacy factory lines
while warehousing, logistics, and service sectors suffer acute labor
friction. Reduce position size substantially on labor-intensive
domestic equities.

### AUTOMATING

Any of the following hold (and neither `MANUAL_BOTTLENECK` nor
`UNDER_AUTOMATED` applies):

- Industrial Tier is **automated** (`1,500 to 4,000`) AND Cross-Sector
  Breadth is **early_logistics**, **corridor_automated**, or
  **broad_spectrum**.
- Industrial Tier is **hyper_automated** (`> 4,000`) AND Cross-Sector
  Breadth is **caged_only** or **early_logistics**.
- Industrial Tier is **transitional** (`500 to 1,500`) AND Cross-Sector
  Breadth is **corridor_automated** or **broad_spectrum** with
  **surging_capex**.

**Delta cap: 0.75.** Meaningful robotics integration across factories and
logistics hubs buffers labor costs, though full cross-sector service
automation is still scaling. Reduce size relative to HYPER_AUTOMATED.

### HYPER_AUTOMATED

All of the following hold:

- Industrial Tier is **hyper_automated** (`> 4,000`).
- Cross-Sector Breadth is **corridor_automated** or **broad_spectrum**.
- Deployment Velocity is **compounding** or **surging_capex**.

**Delta cap: 1.0.** High physical robot density across manufacturing,
warehousing, and service sectors insulates throughput from labor
shortages and thermal stress. The cap equals the strategy cap; the skill
never binds on HYPER_AUTOMATED.

### Ambiguous fallback

Any combination not covered above is classified **UNDER_AUTOMATED** with
delta cap `0.25`.

## Secondary Filter / Asymmetric Gate — Automation Stagnation Hysteresis

Apply the persistence test after state classification and before the
cap.

An economy's automation lag is **entrenched** if
`quarters_stagnant_automation >= 4` (four or more consecutive quarters
with `yoy_robot_install_growth_pct < 3.0` while
`industrial_robots_per_100k < 1500`). Four consecutive quarters of
stagnant robot installation proves capital-deepening paralysis rather
than routine factory retooling cycles.

If the lag is **entrenched**, halve the state's delta cap:

- `AUTOMATING` cap of `0.75` becomes **`0.375`**.
- `UNDER_AUTOMATED` cap of `0.25` becomes **`0.125`**.
- `MANUAL_BOTTLENECK` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read robotics density dict.** From
   `snapshot.external_data["robotics_density"]`, load the target
   region's `industrial_robots_per_100k`, `logistics_amr_per_100k`,
service_robots_per_100k, yoy_robot_install_growth_pct, and
quarters_stagnant_automation. If absent or empty, record
AUTOMATING, note the omission, and do not cite this skill.
2. Classify industrial tier. Apply Reading 1 (hyper_automated,
automated, transitional, or manual_heavy).
3. Classify cross-sector breadth. Apply Reading 2
(broad_spectrum, corridor_automated, early_logistics, or
caged_only).
4. Classify deployment velocity. Apply Reading 3 (surging_capex,
compounding, sluggish, or stagnant).
5. Classify state. Evaluate in strict priority order
(MANUAL_BOTTLENECK → UNDER_AUTOMATED → AUTOMATING →
HYPER_AUTOMATED) and select the first matching state (fallback:
UNDER_AUTOMATED).
6. Apply persistence test. If quarters_stagnant_automation >= 4,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta exceeded delta_cap),
cite "robotics-density-yardstick" in skills_cited and state the
classification in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and cap reason.
Example: "MANUAL_BOTTLENECK state; industrial robots 380/100k, caged_only logistics/service, and stagnant 1.2% growth for 5 quarters; delta capped at 0.05; robotics-density-yardstick."
• skills_cited: list of skill names; include
"robotics-density-yardstick" only when the cap bound.

Worked Examples


Case A — Hyper-automated industrial & logistics corridor, cap does not bind

Snapshot (e.g., South Korea / Singapore / automated SEZ hub):
• industrial_robots_per_100k = 6800.0
• logistics_amr_per_100k = 1450.0
• service_robots_per_100k = 380.0
• yoy_robot_install_growth_pct = 12.5
• quarters_stagnant_automation = 0
Readings:
• Industrial Tier: > 4,000 → hyper_automated
• Cross-Sector Breadth: > 1,200 logistics and > 300 service →
broad_spectrum
• Deployment Velocity: 6% to 15% → compounding
State: HYPER_AUTOMATED, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "robotics-density-yardstick".

Case B — Labor-heavy economy with stagnant logistics/service automation, cap binds

Snapshot:
• industrial_robots_per_100k = 420.0
• logistics_amr_per_100k = 75.0
• service_robots_per_100k = 18.0
• yoy_robot_install_growth_pct = 1.5
• quarters_stagnant_automation = 5
Readings:
• Industrial Tier: < 500 → manual_heavy
• Cross-Sector Breadth: < 100 logistics and < 25 service →
caged_only
• Deployment Velocity: < 2% → stagnant
State: MANUAL_BOTTLENECK, delta cap 0.10.
Persistence: quarters_stagnant_automation = 5 >= 4 → halve to 0.05.
AGOP ranks LONG on a labor-intensive domestic manufacturing or
warehousing ticker. LLM intended delta = 0.75. Cap 0.05 binds. LLM
returns delta = 0.05 and cites "robotics-density-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["robotics_density"] from
the following free, public endpoints (no paid subscription required):
• International Federation of Robotics (IFR) World Robotics Press & Executive Summaries:
https://ifr.org (free annual country-by-country
industrial robot density per 10,000 employees—multiplied by 10 for
per 100,000—plus logistics AMR and service robotics installation
summaries).
• OECD Science, Technology and Industry / Industrial Robotics Diffusion:
https://oecd.org (free SDMX API covering robot stock,
sectoral capital deepening, and manufacturing employment denominators).
• Eurostat ICT & Robotics Usage in Enterprises (isoc_eb_p3d / isoc_r_cuse):
https://europa.eu (free JSON/TSV API
measuring industrial and service robot adoption across EU/EEA
enterprises).
• ILOSTAT / World Bank Sectoral Employment Denominators (SL.IND.EMPL.ZS, SL.SRV.EMPL.ZS):
https://worldbank.org (free CC BY-4.0 API providing industry,
logistics, and service workforce counts for per-100,000 normalization).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not evaluate manufacturing robots alone; always incorporate
logistics_amr_per_100k and service_robots_per_100k per Reading 2.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "robotics-density-yardstick" when the cap did not bind.

Citation Mapping

• Task-Based Automation & Factor Substitution: Daron Acemoglu and
Pascual Restrepo, "The Race between Man and Machine: Implications of
Technology for Growth, Factor Shares, and Employment," American
Economic Review 108(6), 1488–1542 (2018); "Automation and New Tasks:
How Technology Displaces and Reinstates Labor," Journal of Economic
Perspectives 33(2), 3–30 (2019).
• Escape From Baumol's Cost Disease: William J. Baumol, The Cost
Disease (Yale University Press, 2012). Substituting robotics in
logistics, warehousing, and clinical/commercial services breaks the
stagnant-productivity cost spiral.
• Global Robot Density Benchmarks: International Federation of
Robotics (IFR), World Robotics — Industrial Robots & Service Robots
(annual benchmark series normalizing operational stock per 10,000
manufacturing employees, scaled here to per 100,000 workers).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.