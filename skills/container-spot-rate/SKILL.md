---
name: "container-spot-rate"
description: "Classify the tick into one of four container freight states (CHEAP, ELEVATED, SURGING, PROHIBITIVE) using the Freightos Baltic Index composite and lanes, the Drewry World Container Index, and the Shanghai Containerized Freight Index; cap delta as freight cost rises."
---

# Container Spot Rate

You are reading the tick against the marginal cost of moving physical
goods across the principal East-West container trade lanes. Container
spot rates in USD per forty-foot-equivalent unit (`$/FEU`) measure the
financial friction of the supply chain: carrier capacity tightness,
war-risk surcharges, port demurrage, and working-capital drag. When the
rates rise, low-margin bulk goods become uneconomical first; high-value
per kilogram cargo reaches the air-sea arbitrage crossover later. The
three most-watched indices — the Freightos Baltic Index (FBX), the
Drewry World Container Index (WCI), and the Shanghai Containerized
Freight Index (SCFI) — measure the same underlying cost from different
origins and weighting schemes, and their agreement or divergence is
itself a signal.

Your job is to classify the tick into one of four freight states and
cap your `delta` accordingly. The rate is a risk gate, not a forecast.
You do not invent trades. You do not override AGOP. You modulate the
LLM's delta within the bound the verifier already permits. You never
raise `delta` above the strategy cap, and you never invent an action
outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["container_rates"]`
and its companion `snapshot.external_data["container_indices"]` dict.
Use the qualitative tables below. Do not compute precise arithmetic.

### The monitored corridors

The fetcher normalises the three indices into a single
`container_rates` dict keyed by corridor. Each entry supplies:

- `current_spot`: the most recent settled spot rate for the corridor.
- `baseline_90d_mean`: the trailing ninety-day mean of the same series.
- `structural_median`: the trailing three-year median of the same series.
- `weeks_above_threshold`: the number of consecutive weekly prints above
  `1.15 × baseline_90d_mean`.

The corridors and their weights:

| Corridor Key | Route | Sources | Weight |
|---|---|---|---|
| `global_composite` | FBX Global Composite / WCI Composite | FBX, WCI | major |
| `asia_eu` | East Asia ↔ North Europe | FBX05/06, WCI Shanghai–Rotterdam | critical |
| `asia_med` | East Asia ↔ Mediterranean | FBX07/08, WCI Shanghai–Genoa | critical |
| `transpacific` | East Asia ↔ North America | FBX01–04, WCI Shanghai–LA / Shanghai–NY | major |
| `intra_asia` | Intra-Asia | SCFI intra-Asia / Drewry IACI | minor |

If `container_rates` is absent or empty, treat all corridors as
unmonitored, record state **CHEAP**, note that no freight data was
available, and do not cite this skill. If a specific corridor key is
absent, evaluate the remaining corridors against the taxonomy; the
skill only requires the critical corridors to be present for the
critical-dominated states, and only the global composite to be present
for the global structural check.

### Reading 1 — Spot-to-baseline ratio

For each monitored corridor `k`, compute the qualitative ratio
`current_spot / baseline_90d_mean`:

| Ratio | Status |
|---|---|
| < 1.15 | **normal** — spot pricing within the routine seasonal band |
| 1.15 to 1.50 | **elevated** — rate pressure and surcharge creep |
| 1.50 to 2.25 | **surging** — acute capacity squeeze or diversion repricing |
| > 2.25 | **prohibitive** — crisis pricing; bulk margins destroyed |

If `baseline_90d_mean` is zero or missing, treat the corridor as
**normal** and note the omission.

### Reading 2 — Structural level

A ninety-day baseline adapts upward during a prolonged freight crisis.
To prevent baseline drift from masking a structural shift, compare
`current_spot` against `structural_median`:

| Ratio (`current_spot / structural_median`) | Structural level |
|---|---|
| < 1.25 | **anchored** — consistent with normal fleet supply |
| 1.25 to 2.00 | **strained** — the structural cost floor has shifted upward |
| > 2.00 | **dislocated** — multi-year regime break; air-sea crossover active |

If `structural_median` is missing, treat the corridor as **anchored**
and rely on Reading 1 alone. The structural level for `global_composite`
is the reference for the CHEAP state; the structural level for
`asia_eu` and `asia_med` is the reference for the SURGING and
PROHIBITIVE conditions that depend on it.

### Reading 3 — Cross-index agreement

The FBX, WCI, and SCFI measure the same cost from different origins.
When they agree on direction, the signal is robust. When they diverge,
the market is in a transitional or measurement-noisy state, and the
skill errs toward caution.

The fetcher supplies a three-element vector per tick in
`external_data["container_indices"]`:

- `fbx_direction`: `up`, `flat`, or `down` over the trailing four weeks.
- `wci_direction`: same convention.
- `scfi_direction`: same convention.

The agreement reading:

| Combination | Agreement |
|---|---|
| All three agree | **consensus** |
| Two agree, one differs | **partial consensus** |
| All three differ | **divergence** |
| Any two missing | **insufficient** |

If `container_indices` is absent, treat as **insufficient** and skip
the cross-index adjustment in step 5 of the procedure.

## Taxonomy / Decision Matrix

Combine the three readings into one of four freight states. The states
are evaluated in the following priority order and the first state whose
conditions are fully satisfied is the classification:

1. **PROHIBITIVE** (most severe)
2. **SURGING**
3. **ELEVATED**
4. **CHEAP** (strictest adaptive fit)

### PROHIBITIVE

Any of the following hold:

- At least one critical corridor (`asia_eu`, `asia_med`) is
  **prohibitive**.
- At least two critical corridors are **surging** or worse.
- At least one critical corridor is **surging** AND its structural
  level is **dislocated**.

**Delta cap: 0.10.** Container spot rates are in an acute crisis. The
physical trade lane is economically severed for standard-goods
shipments. Trade only if the AGOP ranking is unambiguously directional
and the asset is weightless (software, IP) or air-freight-viable. In
most cases, return FLAT.

### SURGING

Any of the following hold (and PROHIBITIVE does not apply):

- At least one critical corridor is **surging**.
- At least two major corridors (`global_composite`, `transpacific`) are
  **surging** or worse.
- Any critical corridor is **elevated** AND its structural level is
  **dislocated**.

**Delta cap: 0.25.** Corridor pricing has broken out. Working-capital
drag and landed costs are high. Physical bulk trades suffer severe
margin erosion; high-value-per-kilogram cargo must pivot to air cargo
or regional overland routes. Reduce substantially.

### ELEVATED

Any of the following hold (and neither SURGING nor PROHIBITIVE
applies):

- At least one critical corridor is **elevated**.
- At least two major corridors are **elevated** or worse.
- Any critical corridor is **strained** while its spot status is
  **normal**.
- The `global_composite` structural level is **strained** while every
  corridor's spot status is **normal**.

**Delta cap: 0.75.** Freight surcharges and container tightness are
compressing physical trade margins. Reduce size relative to CHEAP.

### CHEAP

All of the following hold:

- Every critical corridor is **normal**.
- Every major corridor is **normal** or **elevated**.
- The `global_composite` structural level is **anchored**.

**Delta cap: 1.0.** Maritime transport costs are benign. The cap
equals the strategy cap; the skill can never bind on a CHEAP
classification because no valid `delta` exceeds 1.0.

### Ambiguous fallback

Any combination not covered by the four states above is classified
**ELEVATED** with delta cap 0.75. The skill errs toward caution
because the cost of missing a freight shock exceeds the cost of an
unnecessary reduction.

## Secondary Filter / Asymmetric Gate — Persistence

Apply the persistence test after the state classification and before
the cap.

A freight surge is **persistent** if any corridor whose spot status is
`elevated` or worse has `weeks_above_threshold >= 3`. Three
consecutive weekly prints above `1.15 ×` baseline separate
single-week blank-sailing noise from multi-week contract repricing
that flows into quarterly corporate margins.

A surge is **transient** otherwise.

If the surge is **persistent**, halve the state's delta cap:

- ELEVATED cap of 0.75 becomes **0.375**.
- SURGING cap of 0.25 becomes **0.125**.
- PROHIBITIVE cap of 0.10 becomes **0.05**.
- CHEAP cannot be persistent because CHEAP requires every critical
  corridor to be normal and every major corridor to be normal or
  elevated; an elevated corridor with `weeks_above_threshold >= 3`
  forces the state to ELEVATED first. The persistence test therefore
  never fires on CHEAP.

The gate is one-way. It can only lower the cap. It cannot raise it. It
cannot change the state classification.

### Cross-index adjustment

Apply the Reading 3 adjustment after the persistence test and before
step 7 of the procedure:

- If the agreement reading is **divergence**, raise the state by one
  level of severity: CHEAP → ELEVATED → SURGING → PROHIBITIVE.
  PROHIBITIVE stays PROHIBITIVE. If the state was already bound by
  persistence, apply the raise to the pre-halving state and then
  reapply the halving.
- If the agreement reading is **partial consensus** or **insufficient**,
  do not raise the state.
- If the agreement reading is **consensus**, do not change the state.

The cross-index adjustment cannot lower the state. It can only raise
it. It exists because measurement divergence is itself a reason to
reduce, not to expand.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read the rate dict.** From
   `snapshot.external_data["container_rates"]`, load each monitored
   corridor's `current_spot`, `baseline_90d_mean`, `structural_median`,
   and `weeks_above_threshold`. If the dict is absent or empty, record
   state **CHEAP**, note the absence, and skip to step 7 with a note
   that no cap was computed.

2. **Classify spot status.** For each monitored corridor, compute
   `current_spot / baseline_90d_mean` using Reading 1 and record
   `normal`, `elevated`, `surging`, or `prohibitive`.

3. **Classify structural level.** For each monitored corridor, compute
   `current_spot / structural_median` using Reading 2 and record
   `anchored`, `strained`, or `dislocated`.

4. **Classify state.** Evaluate in the priority order PROHIBITIVE,
   SURGING, ELEVATED, CHEAP and take the first state whose conditions
   are fully satisfied. If no state matches, record ELEVATED as the
   ambiguous fallback.

5. **Apply persistence test.** If any corridor whose spot status is
   `elevated` or worse has `weeks_above_threshold >= 3`, halve the
   state's delta cap.

6. **Apply cross-index adjustment.** Read the agreement vector from
   `external_data["container_indices"]`. If the agreement reading is
   `divergence`, raise the state one level of severity and recompute
   the cap using the persistence-test rule for the new state (halve if
   the new state's persistence condition is met, do not halve
   otherwise). If the reading is `partial consensus`, `consensus`, or
   `insufficient`, do not change the state.

7. **Cap delta.** Let `delta_cap` be the value from steps 4–6. If the
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
   Record the final `delta`.

8. **Cite.** If the cap bound (i.e., the intended delta was above the
   cap), cite `"container-spot-rate"` in `skills_cited` and state the
   freight state in the rationale. If the cap did not bind, do not
   cite the skill.

## The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this
order:

```json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
```

The fields:

- `action`: a string. One of `"LONG"`, `"FLAT"`, `"SHORT"`. Must
  appear in the AGOP ranking or be `"FLAT"`. Invariant I1 enforces
  this independently of anything you produce.

- `delta`: a floating-point number in `[0.0, 1.0]`. The final position
  size is `delta` multiplied by the risk engine's upper bound. The
  freight cap restricts `delta` further; it does not replace the risk
  bound.

- `confidence`: a floating-point number in `[0.0, 1.0]`. Reflects the
  confidence in the rationale, not the trade. The strategy's
  confidence floor (0.40 for OPPORTUNITY, 0.45 for AGGRESSIVE, 0.65
  for CONSERVATIVE) rejects responses below the threshold.

- `rationale`: a free-form string. Names the freight state and the
  reason for any cap. Example: "SURGING freight state; asia_med
  1.75× baseline with weeks_above_threshold=4; delta capped at 0.125
  after persistence halving; container-spot-rate."

- `skills_cited`: a list of skill names. Include
  `"container-spot-rate"` only if the cap bound. Include the skills
  that actually drove the choice otherwise.

## Worked Examples

### Case A — Cheap state, cap does not bind

Fetcher supplies:

- `container_rates["global_composite"]`: `current_spot` = 2100,
  `baseline_90d_mean` = 2000, `structural_median` = 1950,
  `weeks_above_threshold` = 0.
- `container_rates["asia_eu"]`: `current_spot` = 2400,
  `baseline_90d_mean` = 2300, `structural_median` = 2250,
  `weeks_above_threshold` = 0.
- `container_rates["asia_med"]`: `current_spot` = 2600,
  `baseline_90d_mean` = 2550, `structural_median` = 2500,
  `weeks_above_threshold` = 0.
- `container_rates["transpacific"]`: `current_spot` = 1900,
  `baseline_90d_mean` = 1800, `structural_median` = 1750,
  `weeks_above_threshold` = 0.
- `external_data["container_indices"]`: `fbx_direction` = `flat`,
  `wci_direction` = `flat`, `scfi_direction` = `flat`.

Readings:

- Spot statuses: global_composite 1.05 → **normal**;
  asia_eu 1.04 → **normal**; asia_med 1.02 → **normal**;
  transpacific 1.06 → **normal**.
- Structural levels: global_composite 1.08 → **anchored**;
  asia_eu 1.07 → **anchored**; asia_med 1.04 → **anchored**;
  transpacific 1.09 → **anchored**.
- Agreement: all three flat → **consensus**.

State (priority PROHIBITIVE → SURGING → ELEVATED → CHEAP):

- PROHIBITIVE? No critical corridor prohibitive; no critical surging;
  no critical surging with dislocated structural. No.
- SURGING? No critical surging; no two major surging; no critical
  elevated with dislocated structural. No.
- ELEVATED? No critical elevated; no two major elevated; no critical
  strained-normal; global structural anchored. No.
- CHEAP? All critical normal ✓; all major normal-or-elevated ✓;
  global structural anchored ✓. **CHEAP** matches.

Delta cap 1.0.

Persistence test: no corridor elevated or worse → does not fire.
Cap remains 1.0.

Cross-index adjustment: consensus → no change.

AGOP ranks LONG. LLM intended delta 0.85. Cap 1.0 does not bind. LLM
returns delta 0.85, does not cite `container-spot-rate`, and cites
whichever skills drove the directional choice.

### Case B — Surging state, cap binds

Fetcher supplies:

- `container_rates["global_composite"]`: `current_spot` = 4200,
  `baseline_90d_mean` = 2200, `structural_median` = 2000,
  `weeks_above_threshold` = 5.
- `container_rates["asia_eu"]`: `current_spot` = 5800,
  `baseline_90d_mean` = 2500, `structural_median` = 2300,
  `weeks_above_threshold` = 4.
- `container_rates["asia_med"]`: `current_spot` = 6400,
  `baseline_90d_mean` = 2600, `structural_median` = 2400,
  `weeks_above_threshold` = 6.
- `container_rates["transpacific"]`: `current_spot` = 3100,
  `baseline_90d_mean` = 1900, `structural_median` = 1800,
  `weeks_above_threshold` = 3.
- `external_data["container_indices"]`: `fbx_direction` = `up`,
  `wci_direction` = `up`, `scfi_direction` = `up`.

Readings:

- Spot statuses: global_composite 1.91 → **surging**;
  asia_eu 2.32 → **prohibitive**; asia_med 2.46 → **prohibitive**;
  transpacific 1.63 → **surging**.
- Structural levels: global_composite 2.10 → **dislocated**;
  asia_eu 2.52 → **dislocated**; asia_med 2.67 → **dislocated**;
  transpacific 1.72 → **strained**.
- Agreement: all three up → **consensus**.

State (priority PROHIBITIVE → SURGING → ELEVATED → CHEAP):

- PROHIBITIVE? At least one critical corridor prohibitive (asia_eu,
  asia_med both prohibitive). **PROHIBITIVE** matches.

Delta cap 0.10.

Persistence test: asia_eu `weeks_above_threshold = 4` ≥ 3 → fires.
Halve to **0.05**.

Cross-index adjustment: consensus → no change.

AGOP ranks LONG. LLM intended delta 0.80. Cap 0.05 binds. LLM returns
delta 0.05, cites `container-spot-rate`, and states in the rationale:
"PROHIBITIVE freight state; asia_eu 2.32× baseline and asia_med 2.46×
baseline with weeks_above_threshold 4 and 6; delta capped at 0.05
after persistence halving; container-spot-rate."

## Free data sources

The skill reads normalised values from `snapshot.external_data`. The
operator's fetcher populates the `container_rates` and
`container_indices` dicts from the following free sources. All are
publicly available; none requires a paid subscription.

| Source | Supplies | Endpoint | Access |
|---|---|---|---|
| Freightos Baltic Index (FBX) | Global composite + 12 lanes | `https://fbx.freightos.com/` | Free composite and all 12 public lanes; read from the embedded HTML ticker object on the terminal page, no JS execution and no API key required |
| Drewry World Container Index (WCI) | Composite in USD/FEU | `https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry` | Free headline composite in the page metadata; route-level data requires a free registration |
| Shanghai Containerized Freight Index (SCFI) | Composite in index points (base 1000) | `https://en.sse.sh.cn/` and `https://www.oilpriceapi.com/prices/freight-indices/scfi-shanghai-containerized-freight-index` | Free composite via OilPriceAPI free tier (50 requests/day) or the SSE page; weekly Friday publish |
| UNCTADstat Liner Shipping Connectivity Index (LSCI) | Connectivity index by economy | `https://unctadstat.unctad.org/datacentre/dataviewer/US.LSCI` | Free UNCTADstat account, Client ID and API key from the account page; monthly or quarterly |
| IMF PortWatch | Chokepoint container-transit volumes | `https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query` | Free, no auth; supplies the container component of chokepoint daily traffic to complement the rate indices |

The fetcher uses FBX for `global_composite`, `asia_eu`, `asia_med`,
and `transpacific`; it uses WCI to cross-check the same corridors for
Reading 3; it uses SCFI for `intra_asia` and the cross-index
agreement vector. UNCTADstat and PortWatch are corroborative: the
LSCI confirms whether a rate spike coincides with a connectivity
collapse, and PortWatch confirms whether the physical container flow
through the principal chokepoints matches the rate signal. The skill
does not read LSCI or PortWatch directly; the fetcher decides whether
to include them in `container_indices`.

## Do Not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a
  replacement for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it.

- Do not treat CHEAP as a reason to increase size beyond the strategy
  cap. The strategy cap is the binding constraint. CHEAP means the
  AGOP-selected action is worth taking at the bound the strategy
  already permits.

- Do not compute precise arithmetic on the ratios. The thresholds
  are qualitative. A 7B model cannot reliably divide small floats;
  use the comparison tables.

- Do not re-classify on the same tick. The freight state is a
  deterministic function of the readings. If the first classification
  was SURGING, it stays SURGING. Do not push it to ELEVATED by
  preferring one reading over another.

- Do not cite this skill when the cap did not bind. If the intended
  delta was already at or below the cap, this skill did not change
  the decision, and it should not appear in `skills_cited`. Cite the
  skills that actually drove the choice.

- Do not attempt to fetch FBX, WCI, SCFI, UNCTAD, or PortWatch data
  yourself. You are the LLM; you read what is in
  `snapshot.external_data`. The fetcher is the operator's
  responsibility.

- Do not treat the cross-index adjustment as an alternative to the
  persistence test. The two are applied sequentially. Divergence
  raises the state; persistence halves the cap. Both can fire on the
  same tick.

- Do not treat the ambiguous fallback as a distinct state. It is
  ELEVATED for all downstream purposes, including the persistence
  test and the cap.

## Citation Mapping

- **Reading 1 — spot-to-baseline thresholds (1.15, 1.50, 2.25)**:
  Freightos, *FBX Methodology* (2026); Drewry, *World Container Index
  Methodology* (2026); Shanghai Shipping Exchange, *SCFI Methodology*
  (2026). The 1.15 threshold corresponds to the routine seasonal
  variation band; the 1.50 threshold to the onset of surcharge-driven
  repricing observed in the 2021 and 2024 rate cycles; the 2.25
  threshold to the crisis pricing levels that destroy standard
  bulk-cargo margins.

- **Reading 2 — structural level (1.25, 2.00)**: Drewry, *Container
  Forecaster* (2026); UNCTAD, *Review of Maritime Transport* (2025).
  A 3-year median as the structural anchor, with a 1.25× upper bound
  for the routine fleet-supply range and a 2.00× threshold for the
  multi-year regime break, follows the methodology in the annual
  Review of Maritime Transport and the Drewry Container Forecaster.

- **Reading 3 — cross-index agreement**: Freightos, *FBX Methodology*
  (2026); Drewry, *WCI Methodology* (2026); Shanghai Shipping
  Exchange, *SCFI Methodology* (2026). The three indices use
  different origins, weighting, and unit systems (FBX index points,
  WCI USD/FEU, SCFI index points). Directional agreement is the
  minimum condition for a robust signal; divergence is a
  measurement-noise signal that warrants caution.

- **Corridor weights**: UNCTAD, *Review of Maritime Transport* (2025);
  PortWatch, *Global Chokepoints Data* (2026). The critical
  designation for `asia_eu` and `asia_med` reflects the concentration
  of Nordic and EU import flows on these lanes; the major
  designation for `global_composite` and `transpacific` reflects
  their role as the global capacity-absorption proxy.

- **Persistence threshold (3 weeks)**: Drewry, *Container
  Forecaster* (2026); the 2021–2024 rate-cycle case studies. Three
  consecutive weekly prints above the elevated threshold separate
  single-week blank-sailing noise from multi-week contract repricing.

- **Cross-index adjustment (divergence → raise one severity level)**:
  Freightos, *FBX Methodology* (2026); Drewry, *WCI Methodology*
  (2026); Shanghai Shipping Exchange, *SCFI Methodology* (2026). The
  design principle is that measurement uncertainty is a reason to
  reduce, not to expand; the adjustment can only raise the state,
  never lower it.

- **Ambiguous fallback (ELEVATED, cap 0.75)**: Drewry, *World
  Container Index* (2026). The skill errs toward caution because the
  cost of missing a freight shock exceeds the cost of an unnecessary
  reduction.

- **Bounded algedonic authority**: Stafford Beer, *Brain of the Firm*
  (1972); Ramadge and Wonham, *Supervisory Control of a Class of
  Discrete-Event Processes* (1987). The skill operates strictly as a
  downward-only algedonic damper within JANUS invariants I1–I9. It
  can flag a freight state and cap delta; it cannot override the
  homeostatic risk bound or invent an action outside the AGOP
  ranking.