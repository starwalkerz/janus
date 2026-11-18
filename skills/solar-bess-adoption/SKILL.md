---
name: "solar-bess-adoption"
description: "Classify the current tick by distributed solar PV, battery energy storage (BESS), and EV adoption against grid chokepoint exposure using free grid and energy agency telemetry, and cap delta accordingly."
---

# Solar & BESS Consumer Adoption

You are reading the tick against the decentralized energy resilience of
the target polity or market. Centralized power grids and imported
fossil fuels remain exposed to maritime chokepoints, pipeline
disruptions, and peak-load price spikes. When households and commercial
users adopt distributed solar PV, behind-the-meter battery energy
storage systems (BESS), and electric vehicles (EVs), they build
Machiavellian *virtù* ahead of the storm—converting local irradiance
and off-peak wind into resilient exergy while reducing exposure to
external fuel shocks.

Conversely, a society that refuses distributed solar, BESS, and EV
adoption despite high fuel-import dependence leaves itself exposed to
violent repricing whenever maritime arteries clog or winter peak demand
hits.

Your job is to classify the tick into one of four distributed-energy
states and cap your `delta` accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["distributed_energy"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes regional grid and adoption series into
`snapshot.external_data["distributed_energy"]`. Each region entry
(keyed by geography code such as `fi`, `eu`, `us`, `ke`, `rw`, `za`,
or `global_baseline`) supplies:

- `distributed_solar_bess_pct`: percentage of peak residential and
  commercial load backed by behind-the-meter solar PV and BESS.
- `ev_fleet_share_pct`: percentage of active light-duty vehicle fleet
  that is battery-electric (BEV/PHEV).
- `yoy_bess_growth_pct`: trailing 12-month percentage growth in
  installed behind-the-meter BESS capacity (`MWh`).
- `fuel_import_dependency_pct`: net share of primary energy imported
  via seaborne or cross-border corridors.
- `quarters_stalled`: consecutive quarters with `yoy_bess_growth_pct < 5.0`
  while `distributed_solar_bess_pct < 15.0`.

If `snapshot.external_data["distributed_energy"]` is absent or empty,
treat the region as **unmonitored**, record state **ADOPTING**, note
that no distributed energy data was available, and do not cite this
skill.

### Reading 1 — Distributed generation & storage penetration

Evaluate `distributed_solar_bess_pct` and `ev_fleet_share_pct` together
to classify structural grid defection capacity:

| `distributed_solar_bess_pct` | `ev_fleet_share_pct` | Penetration |
|---|---|---|
| > 35% | > 25% | **autonomous** — high local exergy buffer & V2G/BESS cushion |
| 20% to 35% | 12% to 25% | **resilient** — meaningful peak-shaving & fuel-shock buffer |
| 10% to 20% | 5% to 12% | **transitional** — early consumer uptake, grid still exposed |
| < 10% | < 5% | **laggard** — unhedged reliance on centralized fuel & grid |

If the two metrics fall in different rows, take the **lower** (more
cautious) classification.

### Reading 2 — Adoption velocity

Evaluate `yoy_bess_growth_pct` to determine whether the polity is
actively building dikes before the flood or stagnating in winter
denial:

| `yoy_bess_growth_pct` | Velocity |
|---|---|
| > 25% | **accelerating** — rapid consumer & C&I storage deployment |
| 10% to 25% | **steady** — organic grid-parity adoption |
| 5% to 10% | **sluggish** — bureaucratic or financing friction slowing uptake |
| < 5% | **stalled** — active refusal or regulatory lock-in |

### Reading 3 — Chokepoint exposure coupling

Read `fuel_import_dependency_pct` alongside any active maritime or
freight stress in `snapshot.external_data` (checking whether
`chokepoint_traffic` has any critical chokepoint `disrupted` or worse,
or `container_rates` is `SURGING` or `PROHIBITIVE`):

| `fuel_import_dependency_pct` | External corridor stress | Exposure |
|---|---|---|
| < 30% | any | **insulated** |
| ≥ 30% | none / normal | **moderate** |
| ≥ 30% | disrupted chokepoint or surging freight | **acute** |

If `fuel_import_dependency_pct` is missing, treat as `≥ 30%` (cautious
default).

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four states.
Evaluate in strict priority order and select the first state whose
conditions are fully satisfied:

1. **EXPOSED_LAGGARD** (most severe)
2. **STALLED**
3. **ADOPTING**
4. **AUTONOMOUS** (strictest adaptive fit)

### EXPOSED_LAGGARD

Any of the following hold:

- Penetration is **laggard** AND Exposure is **acute**.
- Penetration is **laggard** AND Velocity is **stalled**.
- Penetration is **transitional** AND Velocity is **stalled** AND
  Exposure is **acute**.

**Delta cap: 0.10.** The polity has refused distributed solar, BESS,
and EV buffering while remaining exposed to centralized fuel or grid
chokepoints. Legacy energy-dependent consumers and unhedged domestic
industries face severe margin and solvency compression. Trade only if
the AGOP ranking targets direct storage/grid-defection suppliers or
non-chokepoint energy hedges. In most cases, return FLAT.

### STALLED

Any of the following hold (and `EXPOSED_LAGGARD` does not apply):

- Penetration is **laggard** AND Velocity is **sluggish** or **steady**.
- Penetration is **transitional** AND Velocity is **stalled** or
  **sluggish**.
- Penetration is **resilient** AND Velocity is **stalled** AND
  Exposure is **acute**.

**Delta cap: 0.25.** Distributed energy adoption is lagging physical
need, leaving peak electricity pricing and imported fuel costs volatile.
Reduce position size substantially on exposed domestic assets.

### ADOPTING

Any of the following hold (and neither `EXPOSED_LAGGARD` nor `STALLED`
applies):

- Penetration is **transitional** AND Velocity is **steady** or
  **accelerating**.
- Penetration is **resilient** AND Exposure is **insulated** or
  **moderate**.
- Penetration is **autonomous** AND Velocity is **stalled** or
  **sluggish**.

**Delta cap: 0.75.** Distributed generation and storage are expanding,
moderating peak-load fragility, though full grid autonomy has not yet
been reached. Reduce size relative to AUTONOMOUS.

### AUTONOMOUS

All of the following hold:

- Penetration is **autonomous**.
- Velocity is **steady** or **accelerating**.
- Exposure is **insulated** or **moderate**.

**Delta cap: 1.0.** High behind-the-meter solar, BESS, and EV
penetration buffers the economy against external fuel shocks. The cap
equals the strategy cap; the skill never binds on AUTONOMOUS.

### Ambiguous fallback

Any combination not covered above is classified **STALLED** with delta
cap `0.25`.

## Secondary Filter / Asymmetric Gate — Refusal Hysteresis

Apply the persistence test after state classification and before the
cap.

A region's under-adoption is **entrenched** if `quarters_stalled >= 4`
(four or more consecutive quarters with `yoy_bess_growth_pct < 5.0`
while `distributed_solar_bess_pct < 15.0`). Four quarters of stagnation
proves the lag is cultural or regulatory lock-in rather than seasonal
installation timing.

If the under-adoption is **entrenched**, halve the state's delta cap:

- `ADOPTING` cap of `0.75` becomes **`0.375`**.
- `STALLED` cap of `0.25` becomes **`0.125`**.
- `EXPOSED_LAGGARD` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read distributed energy dict.** From
   `snapshot.external_data["distributed_energy"]`, load the target
   region's `distributed_solar_bess_pct`, `ev_fleet_share_pct`,
   `yoy_bess_growth_pct`, `fuel_import_dependency_pct`, and
   `quarters_stalled`. If absent or empty, record **ADOPTING**, note the
   omission, and do not cite this skill.
2. **Classify penetration.** Apply Reading 1 (`autonomous`,
   `resilient`, `transitional`, or `laggard`).
3. **Classify velocity.** Apply Reading 2 (`accelerating`, `steady`,
   `sluggish`, or `stalled`).
4. **Classify exposure.** Apply Reading 3 (`insulated`, `moderate`, or
   `acute`).
5. **Classify state.** Evaluate in strict priority order
   (`EXPOSED_LAGGARD` → `STALLED` → `ADOPTING` → `AUTONOMOUS`) and
   select the first matching state (fallback: `STALLED`).
6. **Apply persistence test.** If `quarters_stalled >= 4`, halve
   `delta_cap`.
7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If the
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
8. **Cite.** If the cap bound (intended `delta` exceeded `delta_cap`),
   cite `"solar-bess-adoption"` in `skills_cited` and state the
   classification in the rationale.

## The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:

```json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
```

- `action`: `"LONG"`, `"FLAT"`, or `"SHORT"`. Must appear in the AGOP
  ranking or be `"FLAT"` (Invariant I1).
- `delta`: floating-point number in `[0.0, 1.0]`.
- `confidence`: floating-point number in `[0.0, 1.0]`.
- `rationale`: free-form string naming the state and cap reason.
  Example: `"EXPOSED_LAGGARD state; solar/BESS 6% and EV 4% with stalled growth for 5 quarters during acute chokepoint exposure; delta capped at 0.05; solar-bess-adoption."`
- `skills_cited`: list of skill names; include `"solar-bess-adoption"`
  only when the cap bound.

## Worked Examples

### Case A — High solar/BESS & EV adoption, cap does not bind

Snapshot:
• distributed_solar_bess_pct = 38.0
• ev_fleet_share_pct = 29.0
• yoy_bess_growth_pct = 28.0
• fuel_import_dependency_pct = 22.0
• quarters_stalled = 0
Readings:
• Penetration: > 35% solar/BESS and > 25% EV → autonomous
• Velocity: > 25% YoY → accelerating
• Exposure: < 30% import dependency → insulated
State: AUTONOMOUS, delta cap 1.0. Persistence: quarters_stalled = 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "solar-bess-adoption".

Case B — Laggard grid during chokepoint stress, cap binds

Snapshot:
• distributed_solar_bess_pct = 6.5
• ev_fleet_share_pct = 4.2
• yoy_bess_growth_pct = 3.1
• fuel_import_dependency_pct = 58.0
• quarters_stalled = 5
• chokepoint_traffic["chokepoint6"] (Hormuz): severely disrupted
Readings:
• Penetration: < 10% solar/BESS and < 5% EV → laggard
• Velocity: < 5% YoY → stalled
• Exposure: ≥ 30% import dependency + disrupted critical chokepoint → acute
State: EXPOSED_LAGGARD, delta cap 0.10.
Persistence: quarters_stalled = 5 >= 4 → halve to 0.05.
AGOP ranks LONG on an unhedged domestic utility/consumer stock. LLM
intended delta = 0.70. Cap 0.05 binds. LLM returns delta = 0.05
and cites "solar-bess-adoption".

Free Data Sources

The fetcher populates snapshot.external_data["distributed_energy"]
from the following free, public endpoints:
• Fingrid Open Data API (Finland Grid & Reserve/Solar Telemetry):
https://fingrid.fi (free API registration, real-time and
historical Finnish solar generation, wind, and reserve capacity).
• ENTSO-E Transparency Platform (European Grid Generation & Load):
https://entsoe.eu (free API token, national solar PV
and storage capacity across all EU/EEA member states).
• IEA Photovoltaic Power Systems Programme (IEA PVPS) & IRENA:
https://irena.org and https://iea-pvps.org (free annual
and quarterly national PV/BESS capacity statistics globally).
• U.S. EIA Open Data API (Battery Storage & Distributed Solar):
https://eia.gov (free API key, monthly small-scale
solar and utility/commercial BESS capacity).
• European Alternative Fuels Observatory (EAFO) / IEA Global EV Data:
https://iea.org
(free public fleet share and BEV/PHEV registration data).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not penalize upstream manufacturers or IP exporters of solar,
BESS, or grid-defection hardware when a consumer market is in
EXPOSED_LAGGARD—unless the ticker itself is an unhedged domestic
utility or fuel-dependent consumer asset.
• Do not cite "solar-bess-adoption" when the cap did not bind.

Citation Mapping

• Machiavellian Virtù & Pre-Shock Infrastructure: Niccolò
Machiavelli, The Prince (1513), Ch. XXV. Building dikes and
channels before fortuna floods corresponds to installing behind-the-meter
solar and BESS before maritime fuel chokepoints close.
• Soft Energy Paths & Grid Defection: Amory B. Lovins, Soft Energy
Paths: Toward a Durable Peace (1977); Rocky Mountain Institute, The
Economics of Grid Defection (2014). Distributed end-use generation
paired with storage eliminates centralized transmission vulnerability.
• Diffusion of Innovations & Laggard Thresholds: Everett M. Rogers,
Diffusion of Innovations (1962). The < 10% threshold marks the
pre-takeoff laggard/early-adopter boundary before self-sustaining
network diffusion occurs.
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.