---
name: "maritime-chokepoint"
description: "Classify the current tick by the state of thirteen global maritime chokepoints, using free IMF PortWatch AIS transit data, and cap delta accordingly."
---

# Maritime Chokepoint

You are reading the tick against the physical constrictions of global
trade. Thirteen straits and canals carry the majority of seaborne
commerce. When one is disrupted, supply chains reroute, freight rates
spike, energy prices move, and regional risk premia reprice. The
chokepoints are the arteries; a stenosis anywhere is a macro signal.

Your job is to classify the tick into one of four maritime states and
cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits.

## The monitored chokepoints

Thirteen chokepoints are monitored. Each has a PortWatch `portid` where
one exists. Where PortWatch does not track the chokepoint, the operator
supplies a proxy series and the skill notes the proxy.

| Chokepoint | Region | PortWatch portid | Weight |
|---|---|---|---|
| Strait of Hormuz | Persian Gulf ↔ Gulf of Oman | `chokepoint6` | critical |
| Bab el-Mandeb | Red Sea ↔ Gulf of Aden | `chokepoint4` | major |
| Suez Canal | Mediterranean ↔ Red Sea | `chokepoint1` | critical |
| Strait of Gibraltar | Atlantic ↔ Mediterranean | `chokepoint8` | major |
| Danish Straits | Baltic ↔ North Sea | `chokepoint10` (Øresund; the Great Belt is not separately tracked) | major |
| Gulf of Finland | Baltic ↔ St. Petersburg | none | minor |
| Panama Canal | Atlantic ↔ Pacific | `chokepoint2` | major |
| Cape of Good Hope | Atlantic ↔ Indian Ocean (diversion route) | `chokepoint7` | minor |
| Nine Degree Channel | Arabian Sea ↔ Lakshadweep Sea | none | minor |
| Strait of Malacca | Andaman Sea ↔ South China Sea | `chokepoint5` | critical |
| Taiwan Strait | East China Sea ↔ South China Sea | `chokepoint11` | critical |
| Jeju Strait | Yellow Sea ↔ Korea Strait (East China Sea) | none | minor |
| La Perouse (Soya) Strait | Sea of Okhotsk ↔ Sea of Japan | none | minor |

For the four chokepoints with no PortWatch `portid`, the operator
supplies a proxy series in `external_data["chokepoint_traffic"]` under
the same keys as the others. If no proxy is supplied, the chokepoint
is treated as **unmonitored** and excluded from the aggregate. The
weights are qualitative; a disruption at a critical chokepoint
dominates the state regardless of what the major and minor
chokepoints are doing.

## The two readings

Compute two readings from `snapshot.external_data["chokepoint_traffic"]`.
Use the qualitative thresholds below. Do not attempt precise
arithmetic; use the comparisons.

### Reading 1 — Per-chokepoint status

For each monitored chokepoint `c`, read two values from the fetcher:

- `c["current_7d_mean"]`: the average daily total transits over the
  trailing seven settled days.
- `c["baseline_90d_mean"]`: the average daily total transits over the
  trailing ninety settled days.

Compute the ratio `r_c = current_7d_mean / baseline_90d_mean`. Classify:

| Ratio | Status |
|---|---|
| ≥ 0.90 | **normal** |
| 0.70 to 0.90 | **below normal** |
| 0.40 to 0.70 | **disrupted** |
| < 0.40 | **severely disrupted** |

PortWatch publishes with a 3–7 day reporting lag, so "current" means
the most recent settled day's baseline, not a live count.

### Reading 2 — Diversion signal

Two chokepoints are paired by the fact that traffic diverted from one
appears in the other:

- **Suez Canal** (`chokepoint1`) and **Cape of Good Hope**
  (`chokepoint7`). Ships avoiding the Red Sea route around Africa.
- **Panama Canal** (`chokepoint2`) and the **Strait of Magellan** route
  (not monitored directly; the Cape of Good Hope serves as the
  Atlantic-side diversion proxy).

Read the pair Suez ↔ Cape of Good Hope:

| Suez status | Cape status | Diversion |
|---|---|---|
| normal | normal | **none** |
| below normal or disrupted | normal or above | **active diversion** |
| severely disrupted | above normal by ≥ 1.5× | **confirmed diversion** |
| any | any other combination | **indeterminate** |

A confirmed diversion is a stronger macro signal than a disruption
alone: the traffic has not stopped, it has moved. The cost is longer
voyages, higher freight rates, and a two-week lag on delivered goods.

## The state taxonomy

Combine the two readings into one of four maritime states.

### OPEN

All of the following hold:

- Every critical chokepoint: **normal**
- Every major chokepoint: **normal** or **below normal**
- Diversion: **none**

**Delta cap: 1.0.** The arteries are clear. No maritime constraint on
sizing.

### CONGESTED

All of the following hold:

- No critical chokepoint: **disrupted** or worse
- At least one major chokepoint: **disrupted**
- Diversion: **none** or **indeterminate**

Or:

- Every critical chokepoint: **normal**
- Diversion: **active diversion**

**Delta cap: 0.75.** One or more major chokepoints are strained, or a
diversion is active but not confirmed. The maritime system is
functioning with friction. Reduce size relative to OPEN.

### DISRUPTED

Any of the following hold:

- At least one critical chokepoint: **disrupted**
- At least two major chokepoints: **disrupted** or worse
- Diversion: **confirmed diversion**

**Delta cap: 0.25.** A critical artery is narrowed, or multiple major
ones are, or the diversion is confirmed. The macro regime is being
disturbed. Reduce substantially.

### BLOCKED

Any of the following hold:

- At least one critical chokepoint: **severely disrupted**
- At least two critical chokepoints: **disrupted** or worse
- At least one critical chokepoint: **disrupted** AND the diversion is
  **confirmed diversion**

**Delta cap: 0.10.** A critical artery is closed or nearly closed. The
macro regime is in shock. Trade only if the AGOP ranking is
unambiguously directional and the LLM's rationale is very strong. In
most cases, return FLAT.

## The persistence test (chokepoint hysteresis)

Before applying the delta cap, ask one additional question: is the
disruption persistent?

A disruption is **persistent** if the per-chokepoint `current_7d_mean`
has been below 0.70× baseline for at least fourteen consecutive settled
days. The fetcher supplies `c["days_below_threshold"]` for each
chokepoint. If the value is ≥ 14, the disruption is persistent.

A disruption is **transient** otherwise.

If the disruption is **persistent**, halve the delta cap. An OPEN cap
of 1.0 becomes 0.5. A CONGESTED cap of 0.75 becomes 0.375. A DISRUPTED
cap of 0.25 becomes 0.125. A BLOCKED cap of 0.10 becomes 0.05.

The persistence test is the last filter. It cannot raise the cap; it
can only lower it. It exists because a one-week dip is noise and a
one-month dip is a regime change. The fourteen-day threshold matches
the typical duration of the Suez and Panama disruptions in the 2021–2024
record.

## The procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read the traffic dict.** From
   `snapshot.external_data["chokepoint_traffic"]`, load each monitored
   chokepoint's `current_7d_mean`, `baseline_90d_mean`, and
   `days_below_threshold`. If the dict is absent, treat all chokepoints
   as **unmonitored** and record state **OPEN** with a note that no
   maritime data was available.

2. **Classify each chokepoint.** For each monitored chokepoint, compute
   `r_c = current_7d_mean / baseline_90d_mean` using the comparison
   tables in Reading 1. Record one of: `normal`, `below normal`,
   `disrupted`, `severely disrupted`.

3. **Read the diversion.** Apply Reading 2 to the Suez ↔ Cape pair.
   Record one of: `none`, `active diversion`, `confirmed diversion`,
   `indeterminate`.

4. **Classify state.** Apply the taxonomy above. Record one of:
   `OPEN`, `CONGESTED`, `DISRUPTED`, `BLOCKED`.

5. **Apply persistence test.** If any chokepoint whose status is
   `disrupted` or worse has `days_below_threshold >= 14`, halve the
   state's delta cap.

6. **Cap delta.** Let `delta_cap` be the value from steps 4–5. If your
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
   Record the final `delta`.

7. **Cite.** If the cap bound (i.e., your intended delta was above the
   cap), cite `maritime-chokepoint` in your rationale and state the
   state.

## The output format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:

    {"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}

The fields:

- `action`: a string. One of "LONG", "FLAT", "SHORT". Must appear in
  the AGOP ranking or be "FLAT". Invariant I1 enforces this
  independently of anything you produce; a hallucinated action is
  replaced with FLAT by the verifier.

- `delta`: a floating-point number in [0.0, 1.0]. The final position
  size is `delta` multiplied by the risk engine's upper bound. The
  state cap in this skill restricts `delta` further; it does not
  replace the risk bound.

- `confidence`: a floating-point number in [0.0, 1.0]. Reflects your
  confidence in the rationale, not the trade. The strategy's
  confidence floor (0.40 for OPPORTUNITY, 0.45 for AGGRESSIVE, 0.65
  for CONSERVATIVE) rejects responses below the threshold.

- `rationale`: a free-form string. Names the state and the reason for
  any cap. Example: "DISRUPTED state; Hormuz 0.55× baseline for 21
  days; confirmed Suez→Cape diversion; delta capped at 0.125 after
  persistence halving; maritime-chokepoint."

- `skills_cited`: a list of skill names. Include
  "maritime-chokepoint" only if the state cap bound the delta. Include
  the skills that actually drove the choice otherwise.

## Worked example

Suppose the snapshot has:

- `chokepoint_traffic["chokepoint6"]` (Hormuz): `current_7d_mean`
  = 130, `baseline_90d_mean` = 138, `days_below_threshold` = 0
- `chokepoint_traffic["chokepoint1"]` (Suez): `current_7d_mean` = 40,
  `baseline_90d_mean` = 43, `days_below_threshold` = 0
- `chokepoint_traffic["chokepoint7"]` (Cape): `current_7d_mean` = 86,
  `baseline_90d_mean` = 49, `days_below_threshold` = 0
- All other monitored chokepoints: `current_7d_mean` /
  `baseline_90d_mean` ≥ 0.90

Readings:

- Hormuz ratio: 130 / 138 = 0.94 → **normal**
- Suez ratio: 40 / 43 = 0.93 → **normal**
- Cape ratio: 86 / 49 = 1.76 → **above** (the fetcher's baseline is
  the 90-day mean, which already incorporates the diversion, so a
  ratio of 1.76 against a 90-day baseline that includes the diversion
  is a strong signal of new diverted traffic)
- All other critical chokepoints: normal

State: every critical chokepoint normal; diversion is **none** (Suez
is normal, so no traffic is being diverted). → **OPEN**, delta cap
1.0. Persistence: not applicable. Cap remains 1.0.

Now suppose:

- Hormuz: `current_7d_mean` = 76, `baseline_90d_mean` = 138,
  `days_below_threshold` = 21
- Suez: `current_7d_mean` = 26, `baseline_90d_mean` = 43,
  `days_below_threshold` = 45
- Cape: `current_7d_mean` = 95, `baseline_90d_mean` = 49,
  `days_below_threshold` = 0

Readings:

- Hormuz ratio: 76 / 138 = 0.55 → **disrupted**
- Suez ratio: 26 / 43 = 0.60 → **disrupted**
- Cape ratio: 95 / 49 = 1.94 → above, confirming diversion
- Diversion: Suez disrupted AND Cape above → **confirmed diversion**

State: one critical chokepoint (Hormuz) disrupted → **DISRUPTED**,
delta cap 0.25. Persistence: Hormuz has 21 days below threshold ≥ 14
→ halve to **0.125**.

If AGOP ranks LONG and the LLM intended delta 0.75, the cap binds.
The LLM reduces to 0.125 and cites `maritime-chokepoint`.

## Free data sources

The skill reads transit counts from `snapshot.external_data`. The
operator's fetcher populates the dict from the following free
sources. All are publicly available and require no authentication.

**IMF PortWatch.** The primary source. An open platform maintained by
the IMF and Oxford University, tracking 28 global chokepoints via
satellite AIS data from Spire. No API key, no rate limit in normal
use, 3–7 day reporting lag.

- ArcGIS FeatureServer for daily transit counts:
  `https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query`
- The `portid` values used by the skill are the PortWatch `portid`
  values listed in the table above.
- The 28 PortWatch chokepoints include the nine listed with a
  `portid` above. The four without a `portid` (Gulf of Finland, Nine
  Degree Channel, Jeju Strait, La Perouse Strait) are not tracked by
  PortWatch. The operator supplies proxies from commercial AIS
  (MarineTraffic, VesselFinder, Spire) or from national maritime
  authorities (Finnish Transport and Communications Agency for the
  Gulf of Finland; Indian Ministry of Ports for the Nine Degree
  Channel; Korea Coast Guard for the Jeju Strait; Japanese Coast
  Guard for the La Perouse Strait). If no proxy is supplied, the
  chokepoint is treated as unmonitored.

**World Bank Chokepoints Monitor.** A reference implementation of the
same data pipeline, with code showing the exact ArcGIS query:

- `https://worldbank.github.io/alternative-data-for-crisis/notebooks/disruptions-business-trade/chokepoints-monitor.html`
- The workbook uses the PortWatch `Daily_Chokepoints_Data`
  FeatureServer with the same `portid` conventions.

## Do not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a
  replacement for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it.

- Do not treat "OPEN" as a reason to increase size beyond the
  strategy cap. The strategy cap is the binding constraint. OPEN
  means the AGOP-selected action is worth taking at the bound the
  strategy already permits.

- Do not attempt to fetch PortWatch data yourself. You are the LLM;
  you read what is in `snapshot.external_data`. The fetcher is the
  operator's responsibility.

- Do not compute precise arithmetic on the ratios. The thresholds are
  qualitative. A 7B model cannot reliably divide small floats; use
  the comparison tables.

- Do not cite this skill when the cap did not bind. If your intended
  delta was already at or below the cap, this skill did not change
  your decision, and it should not appear in `skills_cited`.

## Citation mapping

- **Chokepoint enumeration and transit data**: IMF PortWatch, the
  joint IMF–Oxford platform tracking 28 chokepoints and 1,475 ports
  via satellite AIS from Spire, with daily transit counts, per-vessel-type
  breakdowns, and a 3–7 day reporting lag. Data covers 2019 to
  present; 120,000 ships tracked daily; 99% of maritime trade by
  volume covered. The chokepoint `portid` values and coordinates are
  from the PortWatch chokepoint feature dataset.

- **Per-chokepoint thresholds**: the 0.90 / 0.70 / 0.40 ratios are
  calibrated to the Red Sea crisis (October 2023 to present), in
  which Bab el-Mandeb traffic fell to roughly 28 ships per day
  against a pre-crisis baseline of roughly 74, a ratio of 0.38,
  classified as **severely disrupted**. The 0.70 boundary corresponds
  to the Suez traffic level of approximately 43 ships per day
  classified as **disrupted** in the same period. The persistence
  threshold of fourteen days matches the typical duration of the
  Suez and Panama disruptions in the 2021–2024 record.

- **Diversion signal**: the Suez ↔ Cape of Good Hope pairing follows
  the World Bank Chokepoints Monitor methodology, which tracks the
  two as a diversion pair. The confirmed-diversion criterion (Suez
  severely disrupted AND Cape above 1.5× baseline) matches the Red
  Sea pattern from January 2024 onward, in which Cape traffic
  exceeded the Suez traffic for the first time in the PortWatch
  record.

- **Chokepoint weights**: the critical/major/minor classification
  follows the trade-share estimates in the CSIS ChinaPower chokepoint
  tracker and the IMF PortWatch annual capacity data. Malacca and
  Taiwan each carry approximately 21% of world maritime trade by
  value (2024). Hormuz carries approximately 25% of seaborne oil and
  19% of LNG. Suez carries approximately 11% of global maritime
  trade by volume. Bab el-Mandeb approximately 9%. The Cape is a
  diversion route, not a chokepoint in the constriction sense, and
  is weighted minor accordingly.

- **Bounded authority**: the same design pattern as
  `biophysical-regime`, `civilizational-cycle`, and
  `climate-yardstick`. This skill is the algedonic channel for the
  maritime state; it can flag a constraint but cannot override the
  homeostatic risk bound.