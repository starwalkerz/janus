---
name: "air-quality-yardstick"
description: "Classify the current tick by fine particulate matter (PM2.5) concentration and atmospheric inversion spikes using free OpenAQ and Copernicus CAMS telemetry, and cap delta accordingly."
---

# Air Quality Yardstick

You are reading the tick against the atmospheric particulate load and
respiratory exergy tax of the target region or supply-chain hub. Fine
particulate matter (`PM2.5`, particles with aerodynamic diameter
`<= 2.5 µm`) crosses directly from lung alveoli into the bloodstream,
degrading human cognitive decision-making, slowing outdoor and factory
labor throughput, triggering emergency hospital admissions, and forcing
industrial curtailment mandates during winter thermal inversions.

Empirical labor economics (Graff Zivin & Neidell, *American Economic
Review*, 2012) demonstrates that even moderate particulate elevation—well
below official emergency thresholds—measurably depresses worker output.
When `PM2.5` spikes into acute smog episodes across manufacturing basins
(Indo-Gangetic Plain, Yangtze/North China Plain, Po Valley, or urban
East African corridors), physical throughput stalls before quarterly
financial statements reflect the loss.

Your job is to classify the tick into one of four air-quality states
and cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["air_quality"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes ground-sensor and atmospheric reanalysis series
into `snapshot.external_data["air_quality"]`. Each region or hub entry
(keyed by geography code or hub key such as `in`, `sh`, `eu`, `fi`,
`ke`, `rw`, `et`, `us`, or `global_baseline`) supplies:

- `pm25_7d_mean`: trailing 7-day settled mean `PM2.5` concentration in
  `µg/m³`.
- `pm25_24h_peak`: maximum 24-hour rolling `PM2.5` concentration (`µg/m³`)
  recorded within the trailing 7 days.
- `pm25_baseline_90d`: trailing 90-day settled mean `PM2.5` (`µg/m³`).
- `days_above_unhealthy`: consecutive settled days with daily mean
  `PM2.5 > 35.0 µg/m³`.

If `snapshot.external_data["air_quality"]` is absent or empty, treat
the region as **unmonitored**, record state **CLEAN**, note that no
air-quality data was available, and do not cite this skill.

### Reading 1 — Chronic particulate load (`pm25_7d_mean`)

Evaluate `pm25_7d_mean` against WHO Air Quality Guidelines (2021) and
epidemiological dose-response tiers:

| `pm25_7d_mean` (`µg/m³`) | Particulate Regime |
|---|---|
| < 15.0 | **clean** — within WHO interim/guideline clean-air envelope |
| 15.0 to 35.0 | **moderate** — measurable cognitive & labor productivity drag |
| 35.0 to 75.0 | **unhealthy** — acute respiratory load & industrial slowdown |
| > 75.0 | **hazardous** — severe smog; outdoor halts & curtailment risk |

### Reading 2 — Thermal inversion & surge ratio (`pm25_24h_peak / pm25_baseline_90d`)

Compare `pm25_24h_peak` against `pm25_baseline_90d` to detect sudden
thermal inversions, crop-burning plumes, or industrial stagnation spikes
that have not yet lifted the 7-day average:

| Ratio (`pm25_24h_peak / pm25_baseline_90d`) | Surge Status |
|---|---|
| < 1.5× | **normal** — routine diurnal/seasonal dispersion |
| 1.5× to 2.5× | **trapped** — boundary-layer inversion or regional plume active |
| > 2.5× | **acute_smog** — severe stagnation spike; visibility & logistics disrupted |

If `pm25_baseline_90d` is zero or missing, treat Surge Status as
**normal** and rely on Reading 1 alone.

### Reading 3 — Peak ceiling override (`pm25_24h_peak`)

Even in a region with a low baseline, a single-day extreme `PM2.5`
spike (`> 150.0 µg/m³`, e.g., wildfire smoke plume or acute industrial
event) degrades immediate operations:

| `pm25_24h_peak` (`µg/m³`) | Ceiling Signal |
|---|---|
| ≤ 75.0 | **contained** |
| 75.0 to 150.0 | **elevated_peak** |
| > 150.0 | **emergency_peak** |

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four states.
Evaluate in strict priority order and select the first state whose
conditions are fully satisfied:

1. **TOXIC_AIR** (most severe)
2. **DEGRADED**
3. **HAZY**
4. **CLEAN** (strictest adaptive fit)

### TOXIC_AIR

Any of the following hold:

- Particulate Regime is **hazardous** (`> 75.0 µg/m³`).
- Particulate Regime is **unhealthy** (`35.0 to 75.0 µg/m³`) AND Surge
  Status is **acute_smog** (`> 2.5×`).
- Ceiling Signal is **emergency_peak** (`pm25_24h_peak > 150.0 µg/m³`).

**Delta cap: 0.10.** Atmospheric particulate loading has reached acute
toxicity. Outdoor labor, port/airport visibility, and factory output
face immediate disruption or government curtailment orders. Trade only
if the AGOP ranking targets air-filtration/biotech remediation IP or
remote digital services. In most cases, return FLAT.

### DEGRADED

Any of the following hold (and `TOXIC_AIR` does not apply):

- Particulate Regime is **unhealthy** (`35.0 to 75.0 µg/m³`).
- Particulate Regime is **moderate** (`15.0 to 35.0 µg/m³`) AND Surge
  Status is **acute_smog** (`> 2.5×`).
- Ceiling Signal is **elevated_peak** (`75.0 to 150.0 µg/m³`).

**Delta cap: 0.25.** Elevated fine particulates are actively taxing
worker stamina, cognitive output, and healthcare utilization. Reduce
position size substantially on labor-intensive and domestic physical
assets.

### HAZY

Any of the following hold (and neither `TOXIC_AIR` nor `DEGRADED`
applies):

- Particulate Regime is **moderate** (`15.0 to 35.0 µg/m³`).
- Particulate Regime is **clean** (`< 15.0 µg/m³`) AND Surge Status is
  **trapped** (`1.5× to 2.5×`) or **acute_smog** (`> 2.5×`).

**Delta cap: 0.75.** Moderate particulate drag or an early boundary-layer
inversion is compressing peak productivity. Reduce size relative to
CLEAN.

### CLEAN

All of the following hold:

- Particulate Regime is **clean** (`< 15.0 µg/m³`).
- Surge Status is **normal** (`< 1.5×`).
- Ceiling Signal is **contained** (`≤ 75.0 µg/m³`).

**Delta cap: 1.0.** Clean atmospheric dispersion; zero particulate drag
on labor or logistics. The cap equals the strategy cap; the skill never
binds on CLEAN.

### Ambiguous fallback

Any combination not covered above is classified **DEGRADED** with delta
cap `0.25`.

## Secondary Filter / Asymmetric Gate — Stagnation Persistence

Apply the persistence test after state classification and before the
cap.

An air-quality degradation is **persistent** if `days_above_unhealthy >= 7`
(seven or more consecutive settled days with daily mean
`PM2.5 > 35.0 µg/m³`). Seven consecutive days of unhealthy air
exhausts respiratory recovery, drives measurable hospital admissions,
and triggers mandatory industrial production cuts.

If the degradation is **persistent**, halve the state's delta cap:

- `HAZY` cap of `0.75` becomes **`0.375`**.
- `DEGRADED` cap of `0.25` becomes **`0.125`**.
- `TOXIC_AIR` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read air quality dict.** From
   `snapshot.external_data["air_quality"]`, load the target region's
   `pm25_7d_mean`, `pm25_24h_peak`, `pm25_baseline_90d`, and
   `days_above_unhealthy`. If absent or empty, record **CLEAN**, note
   the omission, and do not cite this skill.
2. **Classify particulate regime.** Apply Reading 1 (`clean`,
   `moderate`, `unhealthy`, or `hazardous`).
3. **Classify surge status.** Apply Reading 2 (`normal`, `trapped`, or
   `acute_smog`).
4. **Classify ceiling signal.** Apply Reading 3 (`contained`,
   `elevated_peak`, or `emergency_peak`).
5. **Classify state.** Evaluate in strict priority order
   (`TOXIC_AIR` → `DEGRADED` → `HAZY` → `CLEAN`) and select the first
   matching state (fallback: `DEGRADED`).
6. **Apply persistence test.** If `days_above_unhealthy >= 7`, halve
   `delta_cap`.
7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If the
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
8. **Cite.** If the cap bound (intended `delta` exceeded `delta_cap`),
   cite `"air-quality-yardstick"` in `skills_cited` and state the
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
  Example: `"TOXIC_AIR state; PM2.5 7d mean 92 ug/m3 with 185 ug/m3 peak for 9 consecutive days; delta capped at 0.05; air-quality-yardstick."`
- `skills_cited`: list of skill names; include `"air-quality-yardstick"`
  only when the cap bound.

## Worked Examples

### Case A — Clean Nordic / Kigali dispersion, cap does not bind

Snapshot:
- `pm25_7d_mean` = `6.2`
- `pm25_24h_peak` = `8.5`
- `pm25_baseline_90d` = `6.8`
- `days_above_unhealthy` = `0`

Readings:
- Particulate Regime: `< 15.0` → **clean**
- Surge Status: `8.5 / 6.8 = 1.25×` (`< 1.5×`) → **normal**
- Ceiling Signal: `≤ 75.0` → **contained**

State: **CLEAN**, delta cap `1.0`. Persistence: `days_above_unhealthy = 0` → does not fire.
AGOP ranks `LONG`. LLM intended `delta = 0.85`. Cap `1.0` does not bind.
LLM returns `delta = 0.85` and does not cite `"air-quality-yardstick"`.


Case B — Persistent winter thermal inversion in manufacturing basin, cap binds

Snapshot:
• pm25_7d_mean = 88.0
• pm25_24h_peak = 165.0
• pm25_baseline_90d = 42.0
• days_above_unhealthy = 10
Readings:
• Particulate Regime: > 75.0 → hazardous
• Surge Status: 165.0 / 42.0 = 3.93× (> 2.5×) → acute_smog
• Ceiling Signal: > 150.0 → emergency_peak
State: TOXIC_AIR, delta cap 0.10.
Persistence: days_above_unhealthy = 10 >= 7 → halve to 0.05.
AGOP ranks LONG on a regional industrial/consumer ticker. LLM intended
delta = 0.75. Cap 0.05 binds. LLM returns delta = 0.05 and cites
"air-quality-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["air_quality"] from the
following free, public endpoints:
• OpenAQ v3 API (Global Ground-Station Air Quality Network):
https://openaq.org (free API key, aggregated real-time and
daily PM2.5 measurements from thousands of government and research
monitors worldwide).
• Copernicus Atmosphere Monitoring Service (CAMS Global Reanalysis & Forecast):
https://copernicus.eu (free registration, gridded
global surface PM2.5 and boundary-layer height data with zero
geographic coverage gaps).
• World Air Quality Index (WAQI / AQICN API):
https://waqi.info (free token, station-level daily PM2.5
and PM10 feeds across Asian, European, African, and American cities).
• Open-Meteo Air Quality API:
https://open-meteo.com (free, no-key
JSON endpoint returning hourly and daily pm2_5 derived from CAMS).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "air-quality-yardstick" when the cap did not bind.

Citation Mapping

• Particulate Labor & Cognitive Productivity Drag: Joshua Graff Zivin
and Matthew Neidell, "The Impact of Pollution on Worker Productivity,"
American Economic Review 102(7), 3652–3673 (2012). Establishes
non-linear output losses in manual and cognitive tasks from fine
particulate exposure.
• Epidemiological Dose-Response Curve: Douglas W. Dockery et al.,
"An Association between Air Pollution and Mortality in Six U.S.
Cities," New England Journal of Medicine 329(24), 1753–1759 (1993);
World Health Organization, WHO Global Air Quality Guidelines (2021)
(15 µg/m³ 24-hour guideline and Interim Target 3 37.5 µg/m³).
• Unpriced Atmospheric Externalities: Arthur C. Pigou, The
Economics of Welfare (1920). Industrial particulate emissions impose
uncompensated health and throughput costs on surrounding labor and
logistics systems.
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.