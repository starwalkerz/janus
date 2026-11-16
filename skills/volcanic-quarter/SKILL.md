---
name: "volcanic-quarter"
description: "Classify the current tick by the frequency of VEI 5 and above volcanic eruptions in the trailing quarter, using free Smithsonian Global Volcanism Program data, and cap delta accordingly."
---

# Volcanic Quarter

You are reading the tick against the stratospheric aerosol load. A
volcanic eruption of Volcanic Explosivity Index (VEI) 5 or higher
injects sulfur dioxide into the stratosphere, where it converts to
sulfate aerosols and persists for one to three years. The aerosols
reflect incoming solar radiation, cool the troposphere, perturb the
jet stream, and shift regional precipitation and crop yields. The
macro consequences — commodity prices, energy demand, agricultural
output, and sovereign risk in exposed regions — are documented across
the 1815 Tambora, 1883 Krakatau, 1982 El Chichón, and 1991 Pinatubo
events.

Your job is to classify the tick into one of four volcanic states and
cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits.

## The two readings

Compute two readings from `snapshot.external_data["volcanic_activity"]`.
Use the qualitative thresholds below. Do not attempt precise
arithmetic; use the comparisons.

### Reading 1 — Trailing-quarter VEI 5+ count

Read `external_data["volcanic_activity"]["count_vei5plus_90d"]`: the
number of confirmed VEI 5 or higher eruptions whose start date falls
within the trailing ninety days. Read
`external_data["volcanic_activity"]["count_vei4_90d"]`: the number of
confirmed VEI 4 eruptions in the same window, used as a leading
indicator because the VEI 4 count often precedes a VEI 5 cluster.

The historical base rate for VEI 5+ is approximately one event every
twenty years in the modern era, which is roughly 0.0125 per quarter.
The distribution is heavily overdispersed: the 1980–2022 record
contains six VEI 5+ events clustered into three episodes (1980–1982,
1991, 2022) separated by multi-decade quiet intervals. The Poisson
assumption does not hold; the correct model is a negative binomial
with clustering.

The thresholds below are calibrated to that record:

| `count_vei5plus_90d` | Reading |
|---|---|
| 0 | **baseline** |
| 1 | **elevated** |
| 2 | **clustered** |
| ≥ 3 | **extreme** |

| `count_vei4_90d` | Reading |
|---|---|
| 0 to 1 | **baseline** |
| 2 | **elevated** |
| ≥ 3 | **clustered** |

### Reading 2 — Time since last VEI 5+

Read `external_data["volcanic_activity"]["days_since_last_vei5plus"]`:
the number of days since the start date of the most recent confirmed
VEI 5+ eruption. The stratospheric aerosol half-life is roughly one
to two years, so the impact window is:

| Days since last event | Reading |
|---|---|
| ≥ 730 | **dissipated** |
| 365 to 730 | **fading** |
| 180 to 365 | **active** |
| < 180 | **fresh** |

If the key is absent (no VEI 5+ event in the fetched record), treat as
**dissipated** and rely on Reading 1 for the state.

## The state taxonomy

Combine the two readings into one of four volcanic states.

### QUIET

All of the following hold:

- VEI 5+ count: **baseline**
- VEI 4 count: **baseline**
- Time since last: **dissipated**

**Delta cap: 1.0.** No stratospheric aerosol load from recent
eruptions. No volcanic constraint on sizing.

### ELEVATED

All of the following hold:

- VEI 5+ count: **baseline** or **elevated**
- VEI 4 count: **elevated** or less
- Time since last: **fading** or **dissipated**

Or:

- VEI 5+ count: **elevated**
- Time since last: **dissipated** (the eruption was recent enough to
  count in the trailing quarter but not recent enough to still be
  active)

**Delta cap: 0.75.** One VEI 5+ event in the trailing quarter, or a
cluster of VEI 4 events, but the stratospheric impact is fading or
absent. The macro regime is disturbed but not shocked. Reduce size
relative to QUIET.

### DISRUPTED

Any of the following hold:

- VEI 5+ count: **clustered**
- VEI 5+ count: **elevated** AND time since last: **active** or
  **fresh**
- VEI 4 count: **clustered** AND time since last: **active** or
  **fresh**

**Delta cap: 0.25.** Two or more VEI 5+ events in the trailing
quarter, or a single event with a fresh stratospheric impact. The
macro regime is being disturbed. Reduce substantially.

### SHOCKED

Any of the following hold:

- VEI 5+ count: **extreme**
- VEI 5+ count: **clustered** AND time since last: **fresh**
- Any confirmed VEI 6 or higher event in the trailing quarter

**Delta cap: 0.10.** Three or more VEI 5+ events, or any VEI 6+, or a
cluster with a fresh impact. The macro regime is in shock. Trade only
if the AGOP ranking is unambiguously directional and the LLM's
rationale is very strong. In most cases, return FLAT.

## The latitude test (aerosol injection)

Before applying the delta cap, ask one additional question: where did
the aerosol land?

A tropical eruption (latitude between 23.5°S and 23.5°N) injects
aerosols into the tropical stratosphere, where the Brewer–Dobson
circulation spreads them globally within weeks. The global cooling
effect is strongest for tropical eruptions.

A high-latitude eruption (latitude above 60°) injects aerosols into
the polar stratosphere, where they remain confined to the hemisphere
and have weaker global effect. The 2011 Nabro (Eritrea, 13°N) and the
2022 Hunga Tonga (20°S, but submarine and water-vapor-dominated)
illustrate the range.

Read `external_data["volcanic_activity"]["max_vei5plus_latitude_abs"]`:
the absolute latitude of the most equatorward VEI 5+ event in the
trailing quarter. If the value is ≤ 23.5, the event is tropical; if
> 23.5, it is extratropical.

If the most equatorward VEI 5+ event is **tropical**, halve the delta
cap. A QUIET cap of 1.0 becomes 0.5. An ELEVATED cap of 0.75 becomes
0.375. A DISRUPTED cap of 0.25 becomes 0.125. A SHOCKED cap of 0.10
becomes 0.05.

If the event is **extratropical**, do not halve.

The latitude test is the last filter. It cannot raise the cap; it can
only lower it. It exists because a tropical eruption is the case with
global macro consequences; an extratropical one is a regional event.

## The procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read the activity dict.** From
   `snapshot.external_data["volcanic_activity"]`, load
   `count_vei5plus_90d`, `count_vei4_90d`,
   `days_since_last_vei5plus`, and
   `max_vei5plus_latitude_abs`. If the dict is absent, treat all
   counts as zero and record state **QUIET** with a note that no
   volcanic data was available.

2. **Classify VEI 5+ count.** Apply the thresholds in Reading 1.
   Record one of: `baseline`, `elevated`, `clustered`, `extreme`.

3. **Classify VEI 4 count.** Apply the thresholds in Reading 1.
   Record one of: `baseline`, `elevated`, `clustered`.

4. **Classify time since last.** Apply the thresholds in Reading 2.
   Record one of: `fresh`, `active`, `fading`, `dissipated`.

5. **Classify state.** Apply the taxonomy above. Record one of:
   `QUIET`, `ELEVATED`, `DISRUPTED`, `SHOCKED`.

6. **Apply latitude test.** If `max_vei5plus_latitude_abs <= 23.5`,
   halve the state's delta cap.

7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If your
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
   Record the final `delta`.

8. **Cite.** If the cap bound (i.e., your intended delta was above the
   cap), cite `volcanic-quarter` in your rationale and state the
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
  any cap. Example: "DISRUPTED state; VEI 5+ count 2 in trailing
  quarter; tropical event at 13°N; delta capped at 0.125 after
  latitude halving; volcanic-quarter."

- `skills_cited`: a list of skill names. Include "volcanic-quarter"
  only if the state cap bound the delta. Include the skills that
  actually drove the choice otherwise.

## Worked example

Suppose the snapshot has:

- `count_vei5plus_90d` = 1
- `count_vei4_90d` = 1
- `days_since_last_vei5plus` = 410
- `max_vei5plus_latitude_abs` = 41.0 (Mt. St. Helens, 1980, if the
  event were recent)

Readings:

- VEI 5+ count: 1 → **elevated**
- VEI 4 count: 1 → **baseline**
- Time since last: 410 → **fading**

State: VEI 5+ elevated, time since last fading → **ELEVATED**, delta
cap 0.75. Latitude test: 41.0 > 23.5 → extratropical, do not halve.
Cap remains 0.75.

If AGOP ranks LONG and the LLM intended delta 1.0, the cap binds. The
LLM reduces to 0.75 and cites `volcanic-quarter`.

Now suppose:

- `count_vei5plus_90d` = 2
- `count_vei4_90d` = 3
- `days_since_last_vei5plus` = 45
- `max_vei5plus_latitude_abs` = 13.0 (tropical)

Readings:

- VEI 5+ count: 2 → **clustered**
- VEI 4 count: 3 → **clustered**
- Time since last: 45 → **fresh**

State: VEI 5+ clustered, time since last fresh → **DISRUPTED**, delta
cap 0.25. Latitude test: 13.0 ≤ 23.5 → tropical, halve to **0.125**.

If AGOP ranks LONG and the LLM intended delta 0.75, the cap binds.
The LLM reduces to 0.125 and cites `volcanic-quarter`.

## Free data sources

The skill reads eruption counts from `snapshot.external_data`. The
operator's fetcher populates the dict from the following free
sources. All are publicly available and require no authentication.

**Smithsonian Global Volcanism Program (GVP).** The authoritative
database of Holocene volcanism, maintained by the Smithsonian
National Museum of Natural History. The Volcanoes of the World (VOTW)
database contains approximately 1,200 Holocene volcanoes and 10,000
recorded eruptions, updated weekly. VEI is recorded for historical
eruptions; the modern era (since 1500) is the best-covered window.

- GeoServer WFS endpoint:
  `https://webservices.volcano.si.edu/geoserver/GVP-VOTW/wfs`
- Eruption layer: `GVP-VOTW:Smithsonian_VOTW_Holocene_Eruptions`
- Volcano layer: `GVP-VOTW:E3WebApp_HoloceneVolcanoes`
- Bulk downloads in XML and Excel are also available from the GVP
  website.
- AI usage policy: non-commercial, educational, and research use
  permitted with attribution. Commercial use requires prior written
  Smithsonian permission. The operator is responsible for
  compliance.

**The fetcher query.** A WFS GetFeature request for eruptions with
`vei >= 5` and `start_date` within the trailing 90 days returns the
events for `count_vei5plus_90d`. A parallel query with
`vei = 4` returns `count_vei4_90d`. The most recent event's
`start_date` gives `days_since_last_vei5plus`. The event's
`latitude` (absolute value) gives `max_vei5plus_latitude_abs`.

The reference implementation from the `volcanoes` R package
(`https://github.com/moderndive/volcanoes`) demonstrates the WFS
query pattern and the field names.

## Do not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a
  replacement for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it.

- Do not treat "QUIET" as a reason to increase size beyond the
  strategy cap. The strategy cap is the binding constraint. QUIET
  means the AGOP-selected action is worth taking at the bound the
  strategy already permits.

- Do not attempt to fetch GVP data yourself. You are the LLM; you
  read what is in `snapshot.external_data`. The fetcher is the
  operator's responsibility.

- Do not compute precise arithmetic on the counts. The thresholds are
  qualitative. A 7B model cannot reliably model a negative binomial;
  use the comparison tables.

- Do not cite this skill when the cap did not bind. If your intended
  delta was already at or below the cap, this skill did not change
  your decision, and it should not appear in `skills_cited`.

## Citation mapping

- **VEI 5+ base rate and clustering**: the Smithsonian Global
  Volcanism Program's Volcanoes of the World database records 28
  VEI 5+ eruptions since 1500, 8 VEI 6, and 1 VEI 7 (Tambora 1815).
  The mean inter-VEI-6 interval is 58.7 years, and the 1815–1991
  stretch had 5 VEI 6 events at roughly 35-year cadence. The modern
  era's VEI 5+ events cluster into three episodes: 1980–1982 (St.
  Helens, El Chichón), 1991 (Pinatubo, Cerro Hudson), and 2022
  (Hunga Tonga). The modern-era rate of one VEI 5+ per twenty years
  is a long-run average that masks the clustering; the negative
  binomial is the correct model. The reference catalogue
  `https://github.com/Biblejustin/volcanic-eruptions` documents the
  clustering and reports a post-1900 decadal trend of
  +0.002 eruptions/decade [95% CI +0.000, +0.003], consistent with a
  steady-state rate on the century scale.

- **Per-quarter thresholds**: the 1, 2, and 3+ thresholds are
  calibrated to the historical record. A single VEI 5+ in a quarter
  is approximately 80× the base rate of 0.0125; two is roughly 160×;
  three is the threshold at which the record shows a cluster (the
  1991 episode had two VEI 5+ and one VEI 6 within six months). The
  VEI 4 count is used as a leading indicator because the 1980–1982
  and 1991 clusters both had elevated VEI 4 activity in the months
  preceding the VEI 5+ events.

- **Time-since thresholds**: the 180, 365, and 730 day boundaries
  correspond to the stratospheric aerosol residence time. The e-folding
  decay for sulfate aerosols is approximately 12–18 months, so a
  "fading" event (365–730 days) still has roughly 15–40% of its
  initial aerosol load, an "active" event (180–365 days) has 40–70%,
  and a "fresh" event (<180 days) has 70–100%. The 730-day boundary
  is where the impact is indistinguishable from background.

- **Latitude test**: the tropical-vs-extratropical distinction follows
  the aerosol-injection literature. Tropical eruptions inject into
  the tropical stratosphere, where the Brewer–Dobson circulation
  spreads the aerosol globally within 2–3 weeks. Extratropical
  eruptions inject into the polar stratosphere, where the aerosol
  remains confined to the hemisphere and has weaker global effect.
  The 23.5° boundary is the Tropic of Cancer/Capricorn.

- **Economic consequences**: the macro-channel from eruption to
  commodity prices is documented for Tambora 1815 (the "Year Without
  a Summer" of 1816, with subsequent harvest failures and food
  riots in Europe), Krakatau 1883 (regional cooling and crop
  failures in the Dutch East Indies), El Chichón 1982 (a
  stratospheric aerosol layer that persisted for two years), and
  Pinatubo 1991 (a global mean cooling of approximately 0.5°C for
  two years, with documented effects on agricultural output and
  energy demand). The skill's purpose is to cap sizing during the
  impact window of any new event in that class.

- **Bounded authority**: the same design pattern as
  `biophysical-regime`, `civilizational-cycle`, `climate-yardstick`,
  and `maritime-chokepoint`. This skill is the algedonic channel for
  the volcanic state; it can flag a constraint but cannot override
  the homeostatic risk bound.