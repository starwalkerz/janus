---
name: "specialist-physician-density"
description: "Classify the current tick by resident specialist physician density per 100,000 population (counting only board-certified/advanced-degree specialists, excluding generalists and administrative staff) using free WHO GHO, OECD, and Eurostat telemetry, and cap delta accordingly."
---

# Specialist Physician Density

You are reading the tick against the true acute-care clinical capacity
of the target polity. Headline "physicians per capita" figures frequently
mask clinical fragility by lumping in non-practicing administrators,
generalists, or transient contractors. Only **resident specialist
physicians holding advanced post-graduate medical degrees** (surgeons,
anesthesiologists, intensivists, oncologists, cardiologists, and
emergency/infectious-disease specialists) represent genuine clinical
throughput during demographic aging, wet-bulb surges, or pathogen
shocks.

In William Baumol's cost-disease framework (1966) and Joseph Tainter's
complexity model (1988), when specialist clinical capacity falls behind
demographic demand—or stagnates behind credentialing bottlenecks—waiting
lists lengthen, preventable morbidity compounds into workforce exit, and
fiscal budgets are consumed by emergency triage overhead.

Your job is to classify the tick into one of four clinical-capacity
states and cap your `delta` accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["specialist_density"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes national and regional medical workforce series
into `snapshot.external_data["specialist_density"]`. Each region entry
(keyed by ISO-2 geography code such as `fi`, `eu`, `de`, `us`, `uk`,
`ke`, `rw`, `et`, `in`, or `global_baseline`) supplies:

- `specialists_per_100k`: active resident specialist physicians holding
  advanced post-graduate specialist degrees per 100,000 population
  (excluding general practitioners, interns, and non-clinical staff).
- `specialist_5yr_net_change_pct`: net percentage change in
  `specialists_per_100k` over the trailing five settled years (accounting
  for retirements and emigration vs. new specialist graduations).
- `elderly_dependency_ratio_pct`: population aged 65+ as a percentage
  of the working-age population (`15–64`), measuring clinical demand
  load.
- `years_declining`: consecutive settled years in which
  `specialists_per_100k` fell or grew slower than the 65+ population.

If `snapshot.external_data["specialist_density"]` is absent or empty,
treat the region as **unmonitored**, record state **ADEQUATE**, note
that no specialist workforce data was available, and do not cite this
skill.

### Reading 1 — Resident specialist supply (`specialists_per_100k`)

Evaluate `specialists_per_100k` (counting strictly credentialed resident
specialists):

| `specialists_per_100k` | Supply Tier |
|---|---|
| > 220 | **deep_bench** — high specialist reserve & acute-care redundancy |
| 140 to 220 | **sufficient** — functional specialist coverage under normal load |
| 60 to 140 | **thin** — tight specialist bottlenecks & multi-month triage queues |
| < 60 | **depleted** — acute specialist scarcity; systemic clinical fragility |

### Reading 2 — Pipeline & retention trajectory (`specialist_5yr_net_change_pct`)

Evaluate whether resident specialist capacity is expanding or hollowing
out via retirement and brain drain:

| `specialist_5yr_net_change_pct` | Pipeline Status |
|---|---|
| > +5.0% | **expanding** — specialist graduations outpace retirements |
| 0.0% to +5.0% | **stagnant** — barely replacing retiring cohorts |
| −5.0% to 0.0% | **eroding** — net attrition or emigration draining specialist pool |
| < −5.0% | **hollowing** — acute specialist flight or retirement cliff |

If `specialist_5yr_net_change_pct` is missing, treat as **stagnant**.

### Reading 3 — Demographic clinical load (`elderly_dependency_ratio_pct`)

Compare `elderly_dependency_ratio_pct` to determine whether clinical
demand is outstripping specialist supply:

| `elderly_dependency_ratio_pct` | Demand Load |
|---|---|
| < 18% | **youthful_load** — low chronic specialist utilization |
| 18% to 30% | **moderate_load** — rising geriatric & surgical demand |
| > 30% | **heavy_geriatric_load** — intense multi-morbidity specialist strain |

If `elderly_dependency_ratio_pct` is missing, treat as **moderate_load**.

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four states.
Evaluate in strict priority order and select the first state whose
conditions are fully satisfied:

1. **CLINICAL_BOTTLENECK** (most severe)
2. **STRAINED_BENCH**
3. **ADEQUATE**
4. **DEEP_RESERVE** (strictest adaptive fit)

### CLINICAL_BOTTLENECK

Any of the following hold:

- Supply Tier is **depleted** (`< 60`) AND Pipeline Status is
  **eroding** or **hollowing**.
- Supply Tier is **thin** (`60 to 140`) AND Pipeline Status is
  **hollowing** (`< -5.0%`).
- Supply Tier is **thin** (`60 to 140`) AND Demand Load is
  **heavy_geriatric_load** (`> 30%`) AND Pipeline Status is not
  **expanding**.

**Delta cap: 0.10.** Resident specialist capacity cannot absorb acute
clinical or demographic shocks. Workforce absenteeism, prolonged
morbidity, and emergency healthcare rationing threaten domestic
productivity and fiscal stability. Trade only if the AGOP ranking
targets medical-automation/diagnostic IP or insulated export corridors.
In most cases, return FLAT.

### STRAINED_BENCH

Any of the following hold (and `CLINICAL_BOTTLENECK` does not apply):

- Supply Tier is **depleted** (`< 60`) with **expanding** or **stagnant**
  pipeline (e.g., youthful economy actively building specialist cohorts).
- Supply Tier is **thin** (`60 to 140`).
- Supply Tier is **sufficient** (`140 to 220`) AND Demand Load is
  **heavy_geriatric_load** (`> 30%`) AND Pipeline Status is
  **stagnant**, **eroding**, or **hollowing**.

**Delta cap: 0.25.** Specialist capacity is stretched against demographic
or structural demand; triage queues and healthcare cost inflation
compress domestic margins. Reduce position size substantially.

### ADEQUATE

Any of the following hold (and neither `CLINICAL_BOTTLENECK` nor
`STRAINED_BENCH` applies):

- Supply Tier is **sufficient** (`140 to 220`).
- Supply Tier is **deep_bench** (`> 220`) AND Pipeline Status is
  **eroding** or **hollowing**.
- Supply Tier is **deep_bench** (`> 220`) AND Demand Load is
  **heavy_geriatric_load** (`> 30%`).

**Delta cap: 0.75.** Functional specialist coverage, though aging
demographics or pipeline friction prevent full slack. Reduce size
relative to DEEP_RESERVE.

### DEEP_RESERVE

All of the following hold:

- Supply Tier is **deep_bench** (`> 220`).
- Pipeline Status is **expanding** or **stagnant**.
- Demand Load is **youthful_load** or **moderate_load** (`≤ 30%`).

**Delta cap: 1.0.** Ample resident specialist redundancy relative to
demographic load. The cap equals the strategy cap; the skill never
binds on DEEP_RESERVE.

### Ambiguous fallback

Any combination not covered above is classified **STRAINED_BENCH** with
delta cap `0.25`.

## Secondary Filter / Asymmetric Gate — Specialist Attrition Hysteresis

Apply the persistence test after state classification and before the
cap.

A region's specialist deficit is **structurally entrenched** if
`years_declining >= 3` (three or more consecutive settled years in which
`specialists_per_100k` declined or lagged 65+ cohort growth). Training a
board-certified specialist requires 10–14 years of post-secondary
education and residency; a 3-year decline locks in an unavoidable
multi-year clinical deficit.

If the deficit is **structurally entrenched**, halve the state's delta
cap:

- `ADEQUATE` cap of `0.75` becomes **`0.375`**.
- `STRAINED_BENCH` cap of `0.25` becomes **`0.125`**.
- `CLINICAL_BOTTLENECK` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read specialist density dict.** From
   `snapshot.external_data["specialist_density"]`, load the target
   region's `specialists_per_100k`, `specialist_5yr_net_change_pct`,
   `elderly_dependency_ratio_pct`, and `years_declining`. If absent or
   empty, record **ADEQUATE**, note the omission, and do not cite this
   skill.
2. **Classify supply tier.** Apply Reading 1 (`deep_bench`,
   `sufficient`, `thin`, or `depleted`).
3. **Classify pipeline status.** Apply Reading 2 (`expanding`,
   `stagnant`, `eroding`, or `hollowing`).
4. **Classify demand load.** Apply Reading 3 (`youthful_load`,
   `moderate_load`, or `heavy_geriatric_load`).
5. **Classify state.** Evaluate in strict priority order
   (`CLINICAL_BOTTLENECK` → `STRAINED_BENCH` → `ADEQUATE` →
   `DEEP_RESERVE`) and select the first matching state (fallback:
   `STRAINED_BENCH`).
6. **Apply persistence test.** If `years_declining >= 3`, halve
   `delta_cap`.
7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If the
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
8. **Cite.** If the cap bound (intended `delta` exceeded `delta_cap`),
   cite `"specialist-physician-density"` in `skills_cited` and state
   the classification in the rationale.

## The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:

```json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
```

• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and cap reason.
Example: "STRAINED_BENCH state; 175 resident specialists per 100k against 36% elderly dependency ratio and 4 years of relative decline; delta capped at 0.125; specialist-physician-density."
• skills_cited: list of skill names; include
"specialist-physician-density" only when the cap bound.

Worked Examples


Case A — Deep specialist reserve with moderate demographic load, cap does not bind

Snapshot:
• specialists_per_100k = 245.0
• specialist_5yr_net_change_pct = +6.2
• elderly_dependency_ratio_pct = 24.0
• years_declining = 0
Readings:
• Supply Tier: > 220 → deep_bench
• Pipeline Status: > +5.0% → expanding
• Demand Load: 18% to 30% → moderate_load
State: DEEP_RESERVE, delta cap 1.0. Persistence: years_declining = 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "specialist-physician-density".

Case B — Sufficient specialists overwhelmed by heavy geriatric load and attrition, cap binds

Snapshot:
• specialists_per_100k = 168.0
• specialist_5yr_net_change_pct = -1.8
• elderly_dependency_ratio_pct = 37.5
• years_declining = 4
Readings:
• Supply Tier: 140 to 220 → sufficient
• Pipeline Status: -5.0% to 0.0% → eroding
• Demand Load: > 30% → heavy_geriatric_load
State: STRAINED_BENCH, delta cap 0.25.
Persistence: years_declining = 4 >= 3 → halve to 0.125.
AGOP ranks LONG on a domestic healthcare-exposed or labor-intensive
stock. LLM intended delta = 0.75. Cap 0.125 binds. LLM returns
delta = 0.125 and cites "specialist-physician-density".

Free Data Sources

The fetcher populates snapshot.external_data["specialist_density"]
from the following free, public endpoints (no paid subscription
required):
• WHO Global Health Observatory (GHO) — Medical Specialists Density:
https://azureedge.net (specialist medical
practitioners per 10,000 population, scaled ×10 to per 100,000; free
OData JSON/CSV by ISO-3 country code).
• OECD Health Statistics — Practising Specialists by Category:
https://oecd.org (free SDMX API, practising specialist
physicians per 1,000 population excluding generalists and
administrators).
• Eurostat Healthcare Personnel Statistics (hlth_rs_spec):
https://europa.eu (free
JSON/TSV API breaking down practising medical specialists by specialty
across EU/EEA states).
• World Bank Age Dependency Ratio (SP.POP.DPND.OL):
https://worldbank.org
(free CC BY-4.0 API for population ages 65+ as % of working-age
population).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not include general practitioners, interns, or administrative
medical staff when evaluating specialists_per_100k.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "specialist-physician-density" when the cap did not bind.

Citation Mapping

• Cost Disease in Labor-Intensive Clinical Care: William J. Baumol
and William G. Bowen, Performing Arts: The Economic Dilemma (Twentieth
Century Fund, 1966); William J. Baumol, The Cost Disease (Yale
University Press, 2012). Highly credentialed specialist clinical care
cannot be trivially automated without capital substitution.
• Complexity Overhead & Training Lag: Joseph A. Tainter, The
Collapse of Complex Societies (1988). Multi-decade specialist training
pipelines create rigid supply bottlenecks when geriatric morbidity
accelerates.
• Global Specialist Workforce Benchmarks: World Health Organization,
National Health Workforce Accounts (NHWA) (HWF_0002); OECD,
Health at a Glance (Practising Specialists Indicator).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.