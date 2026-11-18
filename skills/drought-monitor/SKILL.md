---
name: "drought-monitor"
description: "Classify the current tick by meteorological/agricultural drought severity (SPEI/SPI) and hydroelectric reservoir depletion using free Copernicus GDO, USDM, and FEWS NET telemetry, and cap delta accordingly."
---

# Drought Monitor

You are reading the tick against the hydrological balance and
soil-moisture carrying capacity of the target region or commodity
basin. Water is the primary bottleneck of both agricultural exergy
(`cocoa`, `coffee`, grains, oilseeds) and hydroelectric baseload power
(Nordics, Brazil, East Africa, Yangtze, Pacific Northwest). Unlike
sudden storms, drought is a slow-compounding thermodynamic deficit:
soil moisture depletion and falling reservoir levels quietly erode crop
yields and grid reserve margins months before spot commodity prices or
rationing mandates spike.

Your job is to classify the tick into one of four hydrological states
and cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["drought_status"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes regional drought and reservoir telemetry into
`snapshot.external_data["drought_status"]`. Each region or basin entry
(keyed by geography code or basin key such as `eu`, `fi`, `se`, `br`,
`ke`, `et`, `tz`, `ug`, `rw`, `ng`, `us`, `in`, or `global_baseline`)
supplies:

- `spei_3m`: 3-month Standardized Precipitation-Evapotranspiration Index
  (or `spi_3m` / USDM equivalent numeric scale), capturing acute
  agricultural soil-moisture balance.
- `spei_12m`: 12-month Standardized Precipitation-Evapotranspiration
  Index, capturing multi-season groundwater and hydrological deficit.
- `reservoir_fill_pct`: regional hydroelectric/water reservoir storage
  as a percentage of seasonal normal (`100%` = normal seasonal fill).
- `quarters_in_severe_drought`: consecutive calendar quarters with
  `spei_3m <= -1.3` or `spei_12m <= -1.3`.

If `snapshot.external_data["drought_status"]` is absent or empty, treat
the region as **unmonitored**, record state **HYDRATED**, note that no
drought data was available, and do not cite this skill.

### Reading 1 — Agricultural soil-moisture balance (`spei_3m`)

Evaluate `spei_3m` against the standard McKee / Vicente-Serrano / USDM
drought classification boundaries:

| `spei_3m` | Soil Moisture Status |
|---|---|
| > −0.8 | **normal** — adequate root-zone moisture |
| −0.8 to −1.3 | **abnormally_dry** (`D0/D1`) — early yield compression |
| −1.3 to −2.0 | **severe_drought** (`D2/D3`) — acute crop stress & irrigation rationing |
| < −2.0 | **exceptional_drought** (`D4`) — harvest failure & acute supply shock |

If `spei_3m` is missing, treat as **normal** and rely on Reading 2 and
Reading 3.

### Reading 2 — Hydrological & reservoir storage (`reservoir_fill_pct`)

Evaluate `reservoir_fill_pct` (percentage of seasonal normal storage)
to measure hydroelectric generation and river-barge capacity:

| `reservoir_fill_pct` | Hydrological Storage |
|---|---|
| ≥ 85% | **full** — normal hydro baseload & waterway draft |
| 65% to 85% | **drawn** — tightening hydro dispatch; thermal backup rising |
| < 65% | **depleted** — power rationing risk & low-water barge bottlenecks |

If `reservoir_fill_pct` is missing, treat as **full**.

### Reading 3 — Multi-season aquifer & basin deficit (`spei_12m`)

Compare `spei_12m` to detect deep structural water deficits that cannot
be cured by a single rain event:

| `spei_12m` | Basin Depth |
|---|---|
| > −1.0 | **recharged** |
| −1.0 to −1.6 | **drawing_down** |
| < −1.6 | **structural_deficit** |

If `spei_12m` is missing, treat as **recharged**.

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four states.
Evaluate in strict priority order and select the first state whose
conditions are fully satisfied:

1. **MEGA_DROUGHT** (most severe)
2. **SEVERE_DROUGHT**
3. **DRYING**
4. **HYDRATED** (strictest adaptive fit)

### MEGA_DROUGHT

Any of the following hold:

- Soil Moisture Status is **exceptional_drought** (`spei_3m < -2.0`).
- Soil Moisture Status is **severe_drought** (`-1.3 to -2.0`) AND
  Hydrological Storage is **depleted** (`< 65%`).
- Basin Depth is **structural_deficit** (`spei_12m < -1.6`) AND
  Hydrological Storage is **depleted** (`< 65%`).

**Delta cap: 0.10.** Acute hydrological collapse. Agricultural yields,
hydroelectric power generation, and inland waterway logistics are
severely impaired. Trade only if the AGOP ranking targets direct
water-desalination/irrigation IP or hedged non-affected supply basins.
In most cases, return FLAT.

### SEVERE_DROUGHT

Any of the following hold (and `MEGA_DROUGHT` does not apply):

- Soil Moisture Status is **severe_drought** (`-1.3 to -2.0`).
- Hydrological Storage is **depleted** (`< 65%`).
- Soil Moisture Status is **abnormally_dry** (`-0.8 to -1.3`) AND Basin
  Depth is **structural_deficit** (`spei_12m < -1.6`).

**Delta cap: 0.25.** Significant soil-moisture or reservoir drawdown is
compressing agricultural output and raising electricity costs. Reduce
position size substantially on `agri`, `cocoa`, `coffee`, hydro-reliant
utilities, and consumer staples exposed to food inflation.

### DRYING

Any of the following hold (and neither `MEGA_DROUGHT` nor
`SEVERE_DROUGHT` applies):

- Soil Moisture Status is **abnormally_dry** (`-0.8 to -1.3`).
- Hydrological Storage is **drawn** (`65% to 85%`).
- Basin Depth is **drawing_down** (`spei_12m` `-1.0 to -1.6`).

**Delta cap: 0.75.** Early moisture deficit is emerging; yield and
reservoir margins are thinning. Reduce size relative to HYDRATED.

### HYDRATED

All of the following hold:

- Soil Moisture Status is **normal** (`> -0.8`).
- Hydrological Storage is **full** (`≥ 85%`).
- Basin Depth is **recharged** (`> -1.0`).

**Delta cap: 1.0.** Healthy soil moisture and full hydrological
reserves. The cap equals the strategy cap; the skill never binds on
HYDRATED.

### Ambiguous fallback

Any combination not covered above is classified **SEVERE_DROUGHT** with
delta cap `0.25`.

## Secondary Filter / Asymmetric Gate — Multi-Quarter Soil Hysteresis

Apply the persistence test after state classification and before the
cap.

A drought is **entrenched** if `quarters_in_severe_drought >= 2` (two
or more consecutive quarters with `spei_3m <= -1.3` or
`spei_12m <= -1.3`). Two consecutive quarters of severe moisture
deficit spans across planting and harvesting cycles, depleting carry-over
grain/cocoa stocks and forcing multi-year tree-crop or herd liquidation.

If the drought is **entrenched**, halve the state's delta cap:

- `DRYING` cap of `0.75` becomes **`0.375`**.
- `SEVERE_DROUGHT` cap of `0.25` becomes **`0.125`**.
- `MEGA_DROUGHT` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read drought dict.** From
   `snapshot.external_data["drought_status"]`, load the target region's
   `spei_3m`, `spei_12m`, `reservoir_fill_pct`, and
   `quarters_in_severe_drought`. If absent or empty, record
   **HYDRATED**, note the omission, and do not cite this skill.
2. **Classify soil moisture.** Apply Reading 1 (`normal`,
   `abnormally_dry`, `severe_drought`, or `exceptional_drought`).
3. **Classify hydrological storage.** Apply Reading 2 (`full`, `drawn`,
   or `depleted`).
4. **Classify basin depth.** Apply Reading 3 (`recharged`,
   `drawing_down`, or `structural_deficit`).
5. **Classify state.** Evaluate in strict priority order
   (`MEGA_DROUGHT` → `SEVERE_DROUGHT` → `DRYING` → `HYDRATED`) and
   select the first matching state (fallback: `SEVERE_DROUGHT`).
6. **Apply persistence test.** If `quarters_in_severe_drought >= 2`,
   halve `delta_cap`.
7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If the
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
8. **Cite.** If the cap bound (intended `delta` exceeded `delta_cap`),
   cite `"drought-monitor"` in `skills_cited` and state the
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
  Example: `"MEGA_DROUGHT state; SPEI-3m -2.2 and reservoir fill 58% for 3 consecutive quarters; delta capped at 0.05; drought-monitor."`
- `skills_cited`: list of skill names; include `"drought-monitor"` only
  when the cap bound.

## Worked Examples

### Case A — Recharged Nordic / East African basin, cap does not bind

Snapshot:
- `spei_3m` = `+0.4`
- `spei_12m` = `+0.2`
- `reservoir_fill_pct` = `94.0`
- `quarters_in_severe_drought` = `0`

Readings:
- Soil Moisture: `> -0.8` → **normal**
- Hydrological Storage: `≥ 85%` → **full**
- Basin Depth: `> -1.0` → **recharged**

State: **HYDRATED**, delta cap `1.0`. Persistence: `quarters_in_severe_drought = 0` → does not fire.
AGOP ranks `LONG`. LLM intended `delta = 0.85`. Cap `1.0` does not bind.
LLM returns `delta = 0.85` and does not cite `"drought-monitor"`.

### Case B — Persistent West African cocoa / hydro drought, cap binds

Snapshot:
- `spei_3m` = `-1.75`
- `spei_12m` = `-1.80`
• reservoir_fill_pct = 61.0
• quarters_in_severe_drought = 3
Readings:
• Soil Moisture: -1.3 to -2.0 → severe_drought
• Hydrological Storage: < 65% → depleted
• Basin Depth: < -1.6 → structural_deficit
State: MEGA_DROUGHT, delta cap 0.10.
Persistence: quarters_in_severe_drought = 3 >= 2 → halve to 0.05.
AGOP ranks LONG on a cocoa-dependent consumer or hydro-exposed utility
ticker. LLM intended delta = 0.70. Cap 0.05 binds. LLM returns
delta = 0.05 and cites "drought-monitor".

Free Data Sources

The fetcher populates snapshot.external_data["drought_status"] from
the following free, public endpoints (no paid subscription required):
• Copernicus Global Drought Observatory (GDO) & European Drought Observatory (EDO):
https://copernicus.eu (free global gridded
SPI, SPEI, soil moisture anomaly, and low-flow indicators).
• U.S. Drought Monitor (USDM / NDMC Data Download & API):
https://unl.edu (free weekly
CSV/JSON/GeoJSON D0–D4 drought intensity tables).
• FEWS NET (Famine Early Warning Systems Network — East & West Africa):
https://fews.net (free agro-climatology, rainfall anomaly, and
crop-condition datasets across ke, et, tz, ug, rw, bi, ng).
• Nord Pool / ENTSO-E Hydro Reservoir Filling Data (Nordics & EU):
https://entsoe.eu (free weekly stored hydro energy
fill levels in GWh vs. historical median for Norway, Sweden,
Finland, and Alpine basins).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "drought-monitor" when the cap did not bind.

Citation Mapping

• Standardized Precipitation Index (SPI) & Thresholds: Thomas B.
McKee, Nolan J. Doesken, and John Kleist, "The Relationship of Drought
Frequency and Duration to Time Scales," Proceedings of the 8th
Conference on Applied Climatology, 179–184 (1993). Establishes the
-0.8, -1.3, -1.6, and -2.0 standard-deviation drought tiers.
• Standardized Precipitation-Evapotranspiration Index (SPEI):
Sergio M. Vicente-Serrano, Santiago Beguería, and Juan I. López-Moreno,
"A Multiscalar Drought Index Sensitive to Global Warming: The
Standardized Precipitation Evapotranspiration Index," Journal of
Climate 23(7), 1696–1718 (2010). Incorporates potential
evapotranspiration so heat-driven soil desiccation is captured.
• Hydraulic Infrastructure & Water Bottlenecks: Karl A. Wittfogel,
Oriental Despotism: A Comparative Study of Total Power (Yale
University Press, 1957); FAO, The State of Food and Agriculture:
Overcoming Water Challenges in Agriculture (2020).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.