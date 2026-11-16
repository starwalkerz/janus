---
name: "climate-yardstick"
description: "Classify the current tick by the state of the North Atlantic Oscillation and the Atlantic Meridional Overturning Circulation, using free meteorological indices, and cap delta accordingly."
---

# Climate Yardstick

You are reading the tick against two slow-moving physical variables
that set the European macro regime: the North Atlantic Oscillation
(NAO) and the Atlantic Meridional Overturning Circulation (AMOC),
including its subpolar branch (SMOC). The NAO oscillates on a
week-to-month timescale and governs winter temperature, storminess,
and energy demand across northern Europe. The AMOC varies on a
decadal-to-centennial timescale and governs the baseline climate
within which the NAO oscillates. Together they are the yardstick
against which a strategy's assumptions about European macro
conditions are measured.

Your job is to classify the tick into one of four climate states and
cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits.

## The two readings

Compute two readings from the snapshot's `external_data` dict. Use the
qualitative thresholds below. Do not attempt precise arithmetic; use
the comparisons.

### Reading 1 — NAO phase

Read `snapshot.external_data["nao_index"]`. The value is the monthly
or daily NAO index, a standardized anomaly of the 500-hPa height
field over the North Atlantic. The standard phase boundaries are:

| Index range | Phase |
|---|---|
| < −1.5 | **NAO−−** (strong negative) |
| −1.5 to −0.5 | **NAO−** (negative) |
| −0.5 to +0.5 | **NAO0** (neutral) |
| +0.5 to +1.5 | **NAO+** (positive) |
| ≥ +1.5 | **NAO++** (strong positive) |

If the key is absent or `None`, treat as **NAO0**.

### Reading 2 — AMOC and SMOC strength

Read `snapshot.external_data["amoc_strength_sv"]` (the RAPID 26°N
transport in Sverdrup) and `snapshot.external_data["smoc_strength_sv"]`
(the OSNAP subpolar transport in Sverdrup). If either is absent, treat
that reading as **unknown** and rely on the other.

The RAPID 26°N series has a modern baseline of approximately 17 Sv.
The OSNAP subpolar series has a baseline of approximately 16–17 Sv.
The thresholds used by the physical-oceanography literature are:

| AMOC (Sv) | Reading |
|---|---|
| ≥ 16 | **healthy** |
| 13 to 16 | **weakening** |
| 8 to 13 | **stressed** |
| < 8 | **near-collapse** |

| SMOC (Sv) | Reading |
|---|---|
| ≥ 16 | **healthy** |
| 13 to 16 | **weakening** |
| 8 to 13 | **stressed** |
| < 8 | **near-collapse** |

The AMOC reading is the worse of the two when both are present.

## The state taxonomy

Combine the two readings into one of four climate states.

### STABLE

All of the following hold:

- NAO phase: **NAO0**, **NAO+**, or **NAO++**
- AMOC reading: **healthy**

**Delta cap: 1.0.** The baseline climate is intact. The NAO is in its
non-disruptive mode. No climate constraint on sizing.

### WAVERING

All of the following hold:

- NAO phase: **NAO−**
- AMOC reading: **healthy** or **weakening**

Or:

- NAO phase: **NAO0** or **NAO+**
- AMOC reading: **weakening**

**Delta cap: 0.75.** One of the two variables is off-baseline but the
other is intact. The climate is not yet constraining, but the strategy
should not size as if conditions were stable.

### STRESSED

Any of the following hold:

- NAO phase: **NAO−−** or **NAO++** (extreme in either direction)
- AMOC reading: **stressed**

**Delta cap: 0.25.** An extreme NAO phase is associated with disrupted
European energy demand, storminess, and transport, and a stressed
AMOC is associated with a regime shift in the North Atlantic
heat transport. Reduce substantially.

### TIPPING

Any of the following hold:

- AMOC reading: **near-collapse**
- NAO phase: **NAO−−** for at least two consecutive readings AND AMOC
  reading is **stressed** or worse
- SMOC reading: **near-collapse**

**Delta cap: 0.10.** The AMOC is at or near the threshold below which
the physical-oceanography literature describes hysteresis and
non-recovery. Trade only if the AGOP ranking is unambiguously
directional and the LLM's rationale is very strong. In most cases,
return FLAT.

## The hysteresis test (Stommel)

Before applying the delta cap, ask one additional question: is the
current climate state on the reversible branch?

The AMOC has two stable equilibria, an "on" state at approximately
17 Sv and an "off" state below approximately 8 Sv, separated by a
hysteresis loop. On the "on" branch, a weakening is reversible if the
freshwater forcing is removed. Below approximately 8 Sv, the
literature describes non-recovery: the system does not return to the
"on" state without external forcing. The bifurcation analysis
estimates the collapse threshold at 0.28–0.32 Sv of anomalous
freshwater forcing, with hysteresis widths of 0.12–0.18 Sv.

A move is **irreversible** if the AMOC reading is **near-collapse**
or if the NAO phase is **NAO−−** for at least two consecutive
readings. In these states, the physical system is on or near the
lower branch, and the climate regime is not expected to recover on
the strategy's horizon.

A move is **reversible** otherwise.

If the move is **irreversible**, halve the delta cap. A STABLE cap of
1.0 becomes 0.5. A WAVERING cap of 0.75 becomes 0.375. A STRESSED
cap of 0.25 becomes 0.125. A TIPPING cap of 0.10 becomes 0.05.

The hysteresis test is the last filter. It cannot raise the cap; it
can only lower it.

## The procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read NAO.** From `snapshot.external_data["nao_index"]`, classify
   the phase as `NAO−−`, `NAO−`, `NAO0`, `NAO+`, or `NAO++` using the
   thresholds in Reading 1. If absent, record `NAO0`.

2. **Read AMOC.** From `snapshot.external_data["amoc_strength_sv"]`,
   classify as `healthy`, `weakening`, `stressed`, or `near-collapse`
   using the thresholds in Reading 2. If absent, record `unknown`.

3. **Read SMOC.** From `snapshot.external_data["smoc_strength_sv"]`,
   classify as `healthy`, `weakening`, `stressed`, or `near-collapse`.
   If absent, record `unknown`.

4. **Combine AMOC and SMOC.** If both are present, the combined
   reading is the worse of the two. If only one is present, the
   combined reading is that one. If neither is present, record
   `unknown`.

5. **Classify state.** Apply the taxonomy above. Record one of:
   `STABLE`, `WAVERING`, `STRESSED`, `TIPPING`.

6. **Apply hysteresis test.** If the combined AMOC reading is
   `near-collapse` or if the NAO phase is `NAO−−` for at least two
   consecutive readings, halve the state's delta cap.

7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If
   your intended `delta` exceeds `delta_cap`, reduce it to
   `delta_cap`. Record the final `delta`.

8. **Cite.** If the cap bound (i.e., your intended delta was above
   the cap), cite `climate-yardstick` in your rationale and state the
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

- `rationale`: a free-form string. Names the climate state and the
  reason for any cap. Example: "TIPPING state; AMOC 7.2 Sv below
  near-collapse threshold; NAO−− for three readings; delta capped at
  0.05 after hysteresis halving; climate-yardstick."

- `skills_cited`: a list of skill names. Include "climate-yardstick"
  only if the state cap bound the delta. Include the skills that
  actually drove the choice otherwise.

## Worked example

Suppose the snapshot has:

- `external_data["nao_index"] = 0.3`
- `external_data["amoc_strength_sv"] = 17.4`
- `external_data["smoc_strength_sv"] = 16.8`

Readings:

- NAO phase: 0.3 falls in −0.5 to +0.5 → **NAO0**
- AMOC: 17.4 ≥ 16 → **healthy**
- SMOC: 16.8 ≥ 16 → **healthy**
- Combined: **healthy**

State: NAO0 + healthy → **STABLE**, delta cap 1.0. Hysteresis test:
not near-collapse, NAO not NAO−− → reversible. Cap remains 1.0.

If AGOP ranks LONG and the LLM intended delta 1.0, the cap does not
bind. The LLM returns delta 1.0 and does not cite this skill.

Now suppose the snapshot has:

- `external_data["nao_index"] = −1.8`
- `external_data["amoc_strength_sv"] = 10.5`
- `external_data["smoc_strength_sv"] = 9.8`

Readings:

- NAO phase: −1.8 < −1.5 → **NAO−−**
- AMOC: 10.5 falls in 8–13 → **stressed**
- SMOC: 9.8 falls in 8–13 → **stressed**
- Combined: **stressed**

State: NAO−− → **STRESSED**, delta cap 0.25. Hysteresis test: NAO−−
for at least two consecutive readings → irreversible. Halve to
**0.125**.

If AGOP ranks LONG and the LLM intended delta 0.75, the cap binds.
The LLM reduces to 0.125 and cites `climate-yardstick`.

## Free meteorological data sources

The skill reads NAO and AMOC values from `snapshot.external_data`.
The operator's data fetcher populates those keys from the following
free sources. All are publicly available and require no
authentication.

**NAO monthly index.** NOAA Climate Prediction Center:

    https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii

**NAO daily index.** NOAA Climate Prediction Center:

    https://ftp.cpc.ncep.noaa.gov/cwlinks/norm.daily.nao.index.b500101.current.ascii

**AMOC 26°N transport.** RAPID-MOCHA-WBTS array, freely available:

    https://rapid.ac.uk/data/data-download

The current release is v2024-2, covering April 2004 to 2024, DOI
`10.5285/5c39bf4e-5140-5546-e063-7086abc027bc`. The time series is a
monthly transport in Sverdrup.

**SMOC subpolar transport.** OSNAP array, freely available:

    https://www.o-snap.org/data/

The first six years of monthly estimates cover August 2014 to June
2020; the array continues to produce monthly MOC estimates.

The fetcher writes the most recent value of each series into the
snapshot's `external_data` dict under the keys
`nao_index`, `amoc_strength_sv`, and `smoc_strength_sv`. If a series
is unavailable on a given tick, the fetcher omits the key and the
skill treats it as absent.

## Do not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a
  replacement for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it.

- Do not treat "STABLE" as a reason to increase size beyond the
  strategy cap. The strategy cap is the binding constraint. STABLE
  means the AGOP-selected action is worth taking at the bound the
  strategy already permits.

- Do not attempt to fetch the NAO or AMOC data yourself. You are the
  LLM; you read what is in `snapshot.external_data`. The fetcher is
  the operator's responsibility, not yours.

- Do not compute precise arithmetic on the readings. The thresholds
  are qualitative. A 7B model cannot reliably divide small floats;
  use the comparison tables.

- Do not cite this skill when the cap did not bind. If your intended
  delta was already at or below the cap, this skill did not change
  your decision, and it should not appear in `skills_cited`.

## Citation mapping

- **NAO phase thresholds (Reading 1)**: the standard phase boundaries
  used in the North Atlantic cyclone literature (Table 2, *Climate
  Dynamics*, 2008), which classify the monthly NAO index into
  NAO−−, NAO−, NAO0, NAO+, and NAO++. The index itself is defined by
  NOAA CPC as the rotated principal component of normalized 500-hPa
  height anomalies over the North Atlantic (CPC Monthly NAO
  teleconnection index, NCEP/NCAR Reanalysis).

- **AMOC and SMOC thresholds (Reading 2)**: the modern RAPID 26°N
  baseline of approximately 17 Sv (Smeed et al., RAPID-MOCHA-WBTS
  array, 2004–2024, DOI `10.5285/5c39bf4e-5140-5546-e063-7086abc027bc`);
  the OSNAP subpolar baseline of approximately 16–17 Sv (Lozier et
  al., *Science*, 2019); the weakening threshold at 15 Sv and the
  near-collapse threshold at 8 Sv (freshwater-hosing experiments
  cited in the CMIP6 and AMOC-tipping literature).

- **Hysteresis test**: Stommel, "Thermohaline Convection with Two
  Stable Regimes", *Tellus* 13 (1961); Rahmstorf, "Ocean Circulation
  and Climate during the Past 120,000 Years", *Nature* 419 (2002);
  the bifurcation analysis estimating a collapse threshold of
  0.28–0.32 Sv of anomalous freshwater forcing with hysteresis widths
  of 0.12–0.18 Sv (AMOC tipping-point literature, 2026).

- **Early warning**: Boers, "Observation-based early-warning signals
  for a collapse of the Atlantic Meridional Overturning
  Circulation", *Nature Climate Change* 11 (2021). The eight
  independent SST- and salinity-based AMOC indices used in that
  paper are the observational analogue of the two transport
  readings used here.

- **Economic consequences**: the climate-economics literature
  estimating follow-up costs of several trillion euros by 2100 from
  AMOC weakening (Max Planck Institute, 2025) and the tipping-point
  consumption-per-capita estimates (Keen, 2026). These establish
  that the AMOC state is a macro variable, not only a physical one.

- **Bounded authority**: the same design pattern as
  `biophysical-regime` and `civilizational-cycle`. This skill is the
  algedonic channel for the climate state; it can flag a constraint
  but cannot override the homeostatic risk bound.