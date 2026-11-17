---
name: "institutional-sclerosis-yardstick"
description: "Classify the tick into one of five institutional-sclerosis temperature states (COOL, WARM, HOT, FEVER, CRITICAL) in ascending severity, using Olson's distributional-coalition vitality, Pareto-Michels elite circulation, Turchin-Tainter structural mobility, and Veblen-Hirsch-Collins ceremonial friction; cap delta as temperature rises."
---

# Institutional Sclerosis Yardstick

You are reading the tick as the temperature of an institutional
system. Olson's distributional coalitions accumulate over time and
reduce the system's capacity to adapt to shocks. Pareto's circulation
of elites is the mechanism by which that capacity is renewed; Michels'
iron law of oligarchy is the mechanism by which it is captured.
Turchin's structural-demographic cycle and Tainter's declining
marginal returns on complexity describe the trajectory once capture
locks in. Veblen's conspicuous consumption, Hirsch's positional goods,
and Collins' credential inflation describe the ceremonial friction
that capture produces. The yardstick measures all four; the
thermometer reads their combined temperature.

Your job is to classify the tick into one of five temperature states
and cap your `delta` accordingly. The thermometer is a risk gate, not
a forecast. A higher temperature means a tighter cap. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise `delta`
above the strategy cap, and you never invent an action outside
`allowed_actions`.

## The Readings

Compute four readings from the snapshot and the optional
`external_data["institutional_indicators"]` dict. Use the qualitative
tables below. Do not compute precise arithmetic; use the comparisons.

### Reading 1 — Vitality (Olson)

The signal-to-noise ratio is `|expected_return| / realized_volatility`.
It measures the system's capacity to convert a shock into output. Olson's
distributional coalitions reduce this capacity: the surplus is captured
by rent-seekers before it reaches productive use.

| Range | Reading |
|---|---|
| ≥ 1.0 | **high** — the system still converts shocks into output |
| 0.3 to 1.0 | **moderate** — conversion is possible with thin margin |
| < 0.3 | **low** — the surplus is captured before conversion |

If `realized_volatility` is zero or missing, treat as **moderate**.

### Reading 2 — Elite circulation (Pareto, Michels)

Two signals determine whether the elite is circulating or entrenched.

Read the sign of `order_flow_imbalance` against the sign of
`expected_return`:

| Flow | Reading |
|---|---|
| Same sign, magnitude ≥ 0.3 | **aligned** |
| Same sign, magnitude < 0.3 | **weak** |
| Opposite sign | **opposed** |

Read `signal_agreement`:

| Range | Reading |
|---|---|
| > 0.5 | **consensus** |
| −0.5 to 0.5 | **contested** |
| < −0.5 | **fractured** |

The pair determines the elite reading. The combinations are mutually
exclusive and collectively exhaustive:

| Pair | Elite reading |
|---|---|
| aligned + contested | **circulation** — healthy elite turnover |
| aligned + consensus | **consolidation** — unified elite; sclerosis risk if vitality is low |
| aligned + fractured | **contested circulation** — noisy but open |
| weak + any | **contested circulation** — low-signal but not captured |
| opposed + consensus | **lock-in** — elite is entrenched against the flow |
| opposed + contested | **lock-in** |
| opposed + fractured | **fragmentation** — no coherent elite |

### Reading 3 — Structural mobility (Turchin, Tainter)

Compare the mean of the first half of `history` to the mean of the
second half. The comparison is directional, not numerical.

| History shape | Mobility |
|---|---|
| Second-half mean well above first-half mean | **rising** |
| Means roughly equal | **peak** |
| Second-half mean slightly below first-half mean | **flattening** |
| Second-half mean well below first-half mean | **descending** |

If `history` has fewer than 8 samples, treat as **peak**. Turchin's
structural-demographic cycle places peak at the top of the expansion
and descending at the onset of the contraction; Tainter's declining
marginal returns on complexity place flattening at the point where
additional complexity no longer buys additional output.

### Reading 4 — Ceremonial friction (Veblen, Hirsch, Collins)

Two signals determine the degree of rent-seeking gatekeeping.

Read `venue_risk`:

| Range | Reading |
|---|---|
| < 0.3 | **low** |
| 0.3 to 0.6 | **moderate** |
| > 0.6 | **high** |

Read the ratio `slippage / slippage_maximum`:

| Range | Reading |
|---|---|
| < 0.1 | **cheap** |
| 0.1 to 0.3 | **moderate** |
| > 0.3 | **expensive** |

The pair determines the friction reading:

| Pair | Friction |
|---|---|
| low + cheap | **low friction** — no ceremonial gatekeeping |
| low or moderate venue, cheap or moderate slippage | **ceremonial** — positional costs are present but not binding |
| high venue OR expensive slippage | **rent-seeking** — gatekeeping is extracting from the trade |
| high venue AND expensive slippage | **senescent** — the gatekeeping structure is fully captured |

If `slippage_maximum` is zero or missing, use the venue reading alone
and treat slippage as **moderate**.

#### Optional corroboration from public governance data

Reading 4 is computed from snapshot fields. The optional
`external_data["institutional_indicators"]` dict corroborates the
friction reading with country-level governance data. The fetcher
normalizes each source to a single `governance_percentile` field on a
0–100 scale, where 0 is the most sclerotic country-year in the sample
and 100 is the most adaptive. The skill reads only
`governance_percentile`, not the raw source scores.

If `governance_percentile` is present and below 25, and the snapshot
friction reading is **ceremonial**, **rent-seeking**, or
**senescent**, raise the friction label by one level. Ceremonial
becomes rent-seeking; rent-seeking becomes senescent; senescent stays
senescent. If `governance_percentile` is 25 or above, do nothing. The
corroboration can only raise the friction label; it can never lower it,
and it can never raise it by more than one level.

If the dict is absent, or `governance_percentile` is missing, the skill
uses the snapshot-only friction reading and ignores the corroboration.

The six free sources the fetcher normalizes from:

| Source | Endpoint |
|---|---|
| World Bank Worldwide Governance Indicators | `https://api.worldbank.org/v2/country/{ISO3}/indicator/GE.EST?format=json` (and `RL.EST`, `RQ.EST`, `CC.EST`) |
| V-Dem | `https://v-dem.net/data/the-v-dem-dataset/` (country-year CSV, version 16) |
| Heritage Index of Economic Freedom | `https://www.heritage.org/index/explore` (annual raw data CSV) |
| Fraser Economic Freedom of the World | `https://www.fraserinstitute.org/economic-freedom/dataset` |
| Transparency International Corruption Perceptions Index | `https://images.transparencycdn.org/images/CPI2025_Results.zip` |
| OECD-WBG Product Market Regulation | `https://data360.worldbank.org/en/dataset/OECD_WB_PMR` |

## Taxonomy / Decision Matrix

Combine the four readings into one of five temperature states. The
temperature is a label, not a number. Higher temperature means more
sclerosis and a tighter cap.

The states are evaluated in the following priority order and the first
state whose conditions are fully satisfied is the classification:

1. **COOL** (checked first; the strictest adaptive fit)
2. **CRITICAL** (checked next; the most severe degradation)
3. **FEVER** (checked next; the second-most severe)
4. **HOT** (checked next; the third-most severe)
5. **WARM** (checked last; the loosest adaptive fit)

Checking COOL before WARM is necessary because WARM's conditions are a
superset of COOL's; checking CRITICAL and FEVER before WARM is
necessary because degradation overrides the adaptive classification.
If no state matches, the readings are classified **HOT** as the
ambiguous fallback.

### COOL

All of the following hold:

- Vitality: **high**
- Elite: **circulation** or **contested circulation**
- Mobility: **rising** or **peak**
- Friction: **low friction**

**Delta cap: 1.0.** The system is in its adaptive phase. No sclerosis
constraint on sizing. The cap equals the strategy cap; the skill can
never bind on a COOL classification because no valid delta exceeds 1.0.

### CRITICAL

Any of the following hold:

- Elite: **fragmentation** AND friction is **senescent**
- Friction: **senescent** AND mobility is **descending**
- Elite: **lock-in** AND mobility is **descending** AND vitality is
  **low**

**Delta cap: 0.0.** The institutional system is fully sclerotic. Set
`delta = 0.0` and `action = "FLAT"` regardless of what AGOP ranked.
The skill binds unconditionally on a CRITICAL classification and must
appear in `skills_cited`.

### FEVER

Any of the following hold:

- Elite: **lock-in** AND mobility is **flattening** or **descending**
- Vitality: **low** AND mobility is **flattening** or **descending**
- Friction: **rent-seeking** or **senescent** AND mobility is
  **flattening** or **descending**

**Delta cap: 0.10.** The system is in Tainter's declining-returns
phase. Trade only if the AGOP ranking is unambiguously directional and
the LLM's rationale is very strong. In most cases, return FLAT.

### HOT

Any of the following hold:

- Vitality: **low** while mobility is **peak**
- Elite: **lock-in** while mobility is **rising** or **peak**
- Friction: **rent-seeking** while mobility is **peak**

**Delta cap: 0.25.** The sclerosis is measurable but the mobility
reading has not yet degraded. The system is still moving.

### WARM

All of the following hold:

- Vitality: **high** or **moderate**
- Elite: **circulation**, **contested circulation**, or
  **consolidation**
- Mobility: **rising** or **peak**
- Friction: **low friction** or **ceremonial**

**Delta cap: 0.75.** One or more readings show the first signs of
entrenchment, but the system is still adaptive. Reduce size relative
to COOL.

### Ambiguous fallback

Any combination not covered by the five states above is classified
**HOT** with delta cap 0.25. The skill errs toward caution because its
purpose is to cap when structure is brittle; an ambiguous reading is
not a license to size as if the system were adaptive.

## Secondary Filter / Asymmetric Gate

Apply the irreversibility test after the temperature classification
and before the cap.

A move is **irreversible** if both of the following hold:

- Mobility is **descending**
- Friction is **rent-seeking** or **senescent**

In this state, Tainter's declining marginal returns on complexity and
Olson's institutional sclerosis have both locked in. The entropy of
the institutional system has been spent; a mistake is not recoverable
within the tick horizon.

A move is **reversible** otherwise.

The gate can only fire on states whose mobility reading is
`descending`. In this taxonomy, only FEVER and the ambiguous fallback
HOT can have a descending mobility reading; COOL and WARM require
mobility rising or peak, and HOT requires mobility rising or peak.
CRITICAL forces delta to zero, so halving has no additional effect
there.

If the move is irreversible:

- FEVER cap of 0.10 becomes **0.05**
- Ambiguous fallback HOT cap of 0.25 becomes **0.125**

The gate is one-way. It can only lower the cap. It cannot raise it. It
cannot change the temperature classification.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read vitality.** From `snapshot.expected_return` and
   `snapshot.realized_volatility`, classify as `high`, `moderate`, or
   `low` using Reading 1. Record the reading.

2. **Read elite circulation.** From
   `snapshot.order_flow_imbalance` and `snapshot.signal_agreement`,
   classify as `circulation`, `consolidation`, `contested circulation`,
   `lock-in`, or `fragmentation` using Reading 2. Record the reading.

3. **Read structural mobility.** From `snapshot.history`, classify as
   `rising`, `peak`, `flattening`, or `descending` using Reading 3. If
   `history` has fewer than 8 samples, record `peak`. Record the
   reading.

4. **Read ceremonial friction.** From `snapshot.venue_risk` and the
   ratio `snapshot.slippage / snapshot.slippage_maximum`, classify as
   `low friction`, `ceremonial`, `rent-seeking`, or `senescent` using
   Reading 4. If `external_data["institutional_indicators"]` contains
   `governance_percentile < 25` and the friction reading is
   `ceremonial`, `rent-seeking`, or `senescent`, raise the friction
   label by one level. Never lower it. Record the reading.

5. **Classify temperature.** Evaluate in the priority order COOL,
   CRITICAL, FEVER, HOT, WARM and take the first state whose
   conditions are fully satisfied. If no state matches, record `HOT`
   as the ambiguous fallback.

6. **Apply irreversibility gate.** If mobility is `descending` AND
   friction is `rent-seeking` or `senescent`, halve the temperature's
   delta cap. Record the final cap.

7. **Cap delta.** Let `delta_cap` be the value from step 6. If the
   temperature is `CRITICAL`, set `delta = 0.0` and `action =
   "FLAT"` regardless of the AGOP ranking. Otherwise, if the intended
   `delta` exceeds `delta_cap`, reduce it to `delta_cap`. Record the
   final `delta` and `action`.

8. **Cite.** If the cap bound (i.e., the intended delta was above the
   cap) or the temperature is `CRITICAL`, include
   `"institutional-sclerosis-yardstick"` in `skills_cited` and state
   the temperature in the rationale. If the cap did not bind, do not
   cite the skill.

## The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:

```json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
```

The fields:

- `action`: a string. One of `"LONG"`, `"FLAT"`, `"SHORT"`. Must
  appear in the AGOP ranking or be `"FLAT"`. Invariant I1 enforces
  this independently of anything you produce; a hallucinated action is
  replaced with FLAT by the verifier. If the temperature is
  `CRITICAL`, `action` must be `"FLAT"`.

- `delta`: a floating-point number in `[0.0, 1.0]`. The final position
  size is `delta` multiplied by the risk engine's upper bound. The
  temperature cap restricts `delta` further; it does not replace the
  risk bound. If the temperature is `CRITICAL`, `delta` must be `0.0`.

- `confidence`: a floating-point number in `[0.0, 1.0]`. Reflects the
  confidence in the rationale, not the trade. The strategy's
  confidence floor (0.40 for OPPORTUNITY, 0.45 for AGGRESSIVE, 0.65
  for CONSERVATIVE) rejects responses below the threshold.

- `rationale`: a free-form string. Names the temperature and the
  reason for any cap. Example: "FEVER state; lock-in elite with
  descending mobility; rent-seeking friction; delta capped at 0.05
  after irreversibility halving;
  institutional-sclerosis-yardstick."

- `skills_cited`: a list of skill names. Include
  `"institutional-sclerosis-yardstick"` only if the cap bound or the
  temperature is `CRITICAL`. Include the skills that actually drove
  the choice otherwise. Do not include a skill whose cap was already
  at or above the intended delta.

## Worked Examples

### Case A — Favorable state, cap does not bind

Snapshot:

- `expected_return` = 0.015, `realized_volatility` = 0.010
- `order_flow_imbalance` = 0.20 (same sign as expected_return)
- `signal_agreement` = 0.1
- `venue_risk` = 0.2
- `slippage` = 1.0, `slippage_maximum` = 20.0
- `history` rising over the last 64 samples
- `external_data` absent (no corroboration)

Readings:

- Vitality: 0.015 / 0.010 = 1.5 → **high**
- Elite: flow weak (magnitude 0.20 < 0.3); signal_agreement 0.1
  → contested; pair = weak + any → **contested circulation**
- Mobility: **rising**
- Friction: venue_risk 0.2 → low; slippage ratio 0.05 → cheap; pair =
  **low friction**

Temperature (priority order COOL, CRITICAL, FEVER, HOT, WARM):

- COOL? Vitality high ✓, elite contested circulation ✓, mobility
  rising ✓, friction low friction ✓. COOL matches.

Temperature is **COOL**, delta cap 1.0.

Irreversibility gate: mobility is rising, not descending → gate does
not fire. Cap remains 1.0.

AGOP ranks LONG. LLM intended delta 0.8. Cap 1.0 does not bind. LLM
returns delta 0.8, does not cite `institutional-sclerosis-yardstick`,
and cites whichever skills drove the directional choice.

### Case B — Adverse state, cap binds

Snapshot:

- `expected_return` = 0.005, `realized_volatility` = 0.010
- `order_flow_imbalance` = −0.45 (opposed to expected_return sign)
- `signal_agreement` = 0.4
- `venue_risk` = 0.7
- `slippage` = 4.0, `slippage_maximum` = 20.0
- `history` descending over the last 64 samples
- `external_data` absent (no corroboration)

Readings:

- Vitality: 0.005 / 0.010 = 0.5 → **moderate**
- Elite: flow opposed; signal_agreement 0.4 → contested; pair =
  opposed + contested → **lock-in**
- Mobility: **descending**
- Friction: venue_risk 0.7 → high; slippage ratio 0.2 → moderate; pair
  = **rent-seeking**

Temperature (priority order COOL, CRITICAL, FEVER, HOT, WARM):

- COOL? Vitality moderate — no. COOL fails.
- CRITICAL?
  - Elite fragmentation AND friction senescent → elite is lock-in,
    not fragmentation. No.
  - Friction senescent AND mobility descending → friction is
    rent-seeking, not senescent. No.
  - Elite lock-in AND mobility descending AND vitality low →
    vitality is moderate, not low. No.
  CRITICAL fails.
- FEVER? Elite lock-in AND mobility descending → matches. FEVER
  matches.

Temperature is **FEVER**, delta cap 0.10.

Irreversibility gate: mobility is descending ✓ AND friction is
rent-seeking ✓ → gate fires. Halve to **0.05**.

AGOP ranks LONG. LLM intended delta 0.75. Cap 0.05 binds. LLM returns
delta 0.05, cites `institutional-sclerosis-yardstick`, and states in
the rationale: "FEVER state; lock-in elite with descending mobility;
rent-seeking friction; delta capped at 0.05 after irreversibility
halving; institutional-sclerosis-yardstick."

## Do Not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a replacement
  for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it. If the LLM intended a
  delta below the temperature cap, do not raise it to the cap.

- Do not treat COOL as a reason to increase size beyond the strategy
  cap. The strategy cap is the binding constraint. COOL means the
  AGOP-selected action is worth taking at the bound the strategy
  already permits.

- Do not compute precise arithmetic on the readings. The thresholds
  are qualitative. A 7B model cannot reliably divide small floats; use
  the comparison tables.

- Do not re-classify on the same tick. The temperature is a
  deterministic function of the four readings. If the first
  classification was HOT, it stays HOT. Do not push it to WARM by
  preferring one reading over another.

- Do not cite this skill when the cap did not bind. If the intended
  delta was already at or below the cap, this skill did not change
  the decision, and it should not appear in `skills_cited`. Cite the
  skills that actually drove the choice.

- Do not use the optional `external_data["institutional_indicators"]`
  dict to lower the friction label. It can only raise it, by at most
  one level, and only when `governance_percentile` is below 25.

- Do not treat the ambiguous fallback as a distinct state. It is HOT
  for all downstream purposes, including the irreversibility gate
  and the cap.

## Citation Mapping

- **Vitality thresholds (Reading 1)**: Mancur Olson, *The Rise and
  Decline of Nations* (1982). Distributional coalitions accumulate
  over time and reduce the system's capacity to convert shocks into
  output. The signal-to-noise ratio is the analogue of that
  conversion capacity.

- **Elite circulation and lock-in (Reading 2)**: Vilfredo Pareto,
  *The Mind and Society* (1916); Robert Michels, *Political Parties*
  (1911). Pareto's circulation of elites is healthy turnover;
  Michels' iron law of oligarchy is the capture that produces
  lock-in. Signal agreement without flow is the empirical signature
  of consolidation; opposed flow is the signature of lock-in.

- **Structural mobility (Reading 3)**: Peter Turchin, *Ages of
  Discord* (2016); Joseph Tainter, *The Collapse of Complex
  Societies* (1988). Turchin's structural-demographic cycle places
  peak at the top of the expansion and descending at the onset of the
  contraction. Tainter's declining marginal returns on complexity
  place flattening at the point where additional complexity no longer
  buys additional output.

- **Ceremonial friction (Reading 4)**: Thorstein Veblen, *The Theory
  of the Leisure Class* (1899); Fred Hirsch, *Social Limits to
  Growth* (1976); Randall Collins, *The Credential Society* (1979).
  Veblen's conspicuous consumption, Hirsch's positional goods, and
  Collins' credential inflation are the ceremonial forms whose
  market-microstructure analogue is gatekeeping friction. Venue risk
  and slippage are the empirical signature.

- **Optional corroboration**: World Bank Worldwide Governance
  Indicators (Kaufmann, Kraay, and Mastruzzi, 2010); V-Dem (Coppedge
  et al., 2026, version 16); Heritage Index of Economic Freedom
  (Heritage Foundation, 2026); Fraser Economic Freedom of the World
  (Gwartney, Lawson, and Hall, 2026); Transparency International
  Corruption Perceptions Index (Transparency International, 2025);
  OECD-WBG Product Market Regulation indicators (OECD and World Bank,
  2024). These are corroborative only; the friction reading is
  computed from the snapshot.

- **Irreversibility gate**: Joseph Tainter, *The Collapse of Complex
  Societies* (1988); Mancur Olson, *The Rise and Decline of Nations*
  (1982). Once both declining marginal returns and institutional
  sclerosis have locked in, the entropy of the institutional system
  has been spent; the move is not recoverable within the tick horizon.

- **Ambiguous fallback**: Olson, *The Rise and Decline of Nations*
  (1982). The skill errs toward HOT because an ambiguous reading is
  not a license to size as if the system were adaptive.

- **Taxonomy priority order**: Olson (1982), Pareto (1916), Michels
  (1911), Turchin (2016), Tainter (1988). The priority order COOL,
  CRITICAL, FEVER, HOT, WARM reflects the fact that degradation
  (CRITICAL, FEVER) overrides the adaptive classification when its
  conditions are met, while COOL is checked before WARM because COOL
  is the strictest fit for the adaptive state.

- **Bounded algedonic authority**: Stafford Beer, *Brain of the Firm*
  (1972); Ramadge and Wonham, *Supervisory Control of a Class of
  Discrete-Event Processes* (1987). The skill operates strictly as a
  downward-only algedonic damper within JANUS invariants I1–I9. It
  can flag a temperature and cap delta; it cannot override the
  homeostatic risk bound or invent an action outside the AGOP
  ranking.