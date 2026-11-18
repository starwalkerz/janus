---
name: "unvaccinated-pathogen-monitor"
description: "Classify the current tick by emerging infectious outbreaks lacking an effective deployed vaccine using free WHO DON, ECDC, Africa CDC, and wastewater surveillance telemetry, and cap delta accordingly."
---

# Unvaccinated Pathogen Monitor

You are reading the tick against non-linear epidemiological tail risk—
specifically human-to-human transmissible pathogens for which **no
working, deployed vaccine exists**. In Kermack–McKendrick SIR dynamics
(1927), once the effective reproduction number (`R_eff`) crosses `1.0`
in an immunologically naive population without vaccine prophylaxis,
infection prevalence grows exponentially rather than linearly.

Markets and bureaucratic institutions routinely underprice early
exponential branching during the first 14–28 days—when wastewater viral
loads, hospital cluster alerts, and cross-border case reports are
already rising, but official travel bans, border closures, and
supply-chain quarantines have not yet been announced.

Your job is to classify the tick into one of four bio-risk states and
cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["pathogen_watch"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes international outbreak bulletins and wastewater
surveillance series into `snapshot.external_data["pathogen_watch"]`.
Each active alert or regional entry (keyed by geography code or
`global_watch`) supplies:

- `r_eff_estimate`: estimated effective reproduction number (`R_eff`)
  derived from case doubling time or wastewater viral concentration
  slope.
- `vaccine_status`: availability of an approved, effective vaccine
  against the circulating clade (`"deployed_effective"`,
  `"experimental_or_stockpiled"`, or `"none"`).
- `transmission_mode`: primary transmission vector (`"vector_or_zoonotic"`,
  `"contact_droplet"`, or `"airborne_respiratory"`).
- `multi_hub_spread`: boolean (`true` / `false`) indicating confirmed
  unlinked community transmission across two or more international
  transit hubs.
- `days_above_unity`: consecutive settled days with `r_eff_estimate > 1.1`
  and `vaccine_status == "none"`.

If `snapshot.external_data["pathogen_watch"]` is absent or empty, treat
the bio-environment as **quiet**, record state **CONTAINED**, note that
no active unvaccinated outbreak data was present, and do not cite this
skill.

### Reading 1 — Epidemic branching velocity (`r_eff_estimate`)

Evaluate `r_eff_estimate` against the Kermack–McKendrick epidemic
threshold:

| `r_eff_estimate` | Branching Velocity |
|---|---|
| < 1.0 | **subcritical** — transmission chains dying out |
| 1.0 to 1.3 | **smoldering** — slow endemic or localized cluster growth |
| 1.3 to 1.8 | **expanding** — sustained exponential community spread |
| > 1.8 | **explosive** — rapid doubling; healthcare & border shock imminent |

If `r_eff_estimate` is missing, treat as **subcritical** unless
`multi_hub_spread` is `true`, in which case treat as **smoldering**.

### Reading 2 — Vaccine & immunological gap (`vaccine_status`)

Evaluate whether an effective vaccine is deployed at scale for the
circulating pathogen or clade:

| `vaccine_status` | Countermeasure Gap |
|---|---|
| `"deployed_effective"` | **covered** — existing immunization blocks exponential tail |
| `"experimental_or_stockpiled"` | **constrained** — Phase I–III or limited ring-vaccination only |
| `"none"` | **unvaccinated** — zero prophylactic shield; full population naive |

If `vaccine_status` is missing while `r_eff_estimate >= 1.3`, default
to **unvaccinated** (cautious fallback).

### Reading 3 — Dissemination vector & hub spillover

Combine `transmission_mode` and `multi_hub_spread` to assess how fast
the pathogen crosses borders and maritime/aviation corridors:

| `transmission_mode` | `multi_hub_spread` | Spillover Risk |
|---|---|---|
| `"vector_or_zoonotic"` | `false` | **localized** |
| `"contact_droplet"` | `false` | **regional** |
| `"airborne_respiratory"` OR `multi_hub_spread == true` | any | **systemic_spillover** |

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four bio-risk
states. Evaluate in strict priority order and select the first state
whose conditions are fully satisfied:

1. **PANDEMIC_SHOCK** (most severe)
2. **OUTBREAK**
3. **WATCH**
4. **CONTAINED** (strictest adaptive fit)

### PANDEMIC_SHOCK

Any of the following hold:

- Branching Velocity is **explosive** (`R_eff > 1.8`) AND Countermeasure
  Gap is **unvaccinated** (`"none"`).
- Branching Velocity is **expanding** (`1.3 to 1.8`) AND Countermeasure
  Gap is **unvaccinated** AND Spillover Risk is **systemic_spillover**.
- Branching Velocity is **explosive** (`R_eff > 1.8`) AND Countermeasure
  Gap is **constrained** AND Spillover Risk is **systemic_spillover**.

**Delta cap: 0.10.** An unvaccinated pathogen with rapid exponential
branching is spilling across transit hubs. Border quarantines, aviation
halts, port crew restrictions, and sudden liquidity freezes are
imminent. Trade only if the AGOP ranking targets direct diagnostic/antiviral
IP or non-contact digital infrastructure. In most cases, return FLAT.

### OUTBREAK

Any of the following hold (and `PANDEMIC_SHOCK` does not apply):

- Branching Velocity is **expanding** (`1.3 to 1.8`) AND Countermeasure
  Gap is **unvaccinated** (`"none"`).
- Branching Velocity is **smoldering** (`1.0 to 1.3`) AND Countermeasure
  Gap is **unvaccinated** AND Spillover Risk is **systemic_spillover**.
- Branching Velocity is **explosive** (`R_eff > 1.8`) AND Countermeasure
  Gap is **constrained**.

**Delta cap: 0.25.** Unvaccinated transmission is actively expanding.
Travel, hospitality, physical retail, and port/airport labor face
rising absenteeism and screening friction. Reduce position size
substantially.

### WATCH

Any of the following hold (and neither `PANDEMIC_SHOCK` nor `OUTBREAK`
applies):

- Branching Velocity is **smoldering** (`1.0 to 1.3`) AND Countermeasure
  Gap is **unvaccinated** or **constrained**.
- Branching Velocity is **expanding** (`1.3 to 1.8`) AND Countermeasure
  Gap is **covered** (`"deployed_effective"`).

**Delta cap: 0.75.** Early cluster signal or breakthrough wave detected;
monitor wastewater and hub transmission closely. Reduce size relative to
CONTAINED.

### CONTAINED

All of the following hold:

- Branching Velocity is **subcritical** (`R_eff < 1.0`).
- Spillover Risk is **localized** or **regional** (`multi_hub_spread == false`).

**Delta cap: 1.0.** No active exponential outbreak. The cap equals the
strategy cap; the skill never binds on CONTAINED.

### Ambiguous fallback

Any combination not covered above is classified **OUTBREAK** with delta
cap `0.25`.

## Secondary Filter / Asymmetric Gate — Sustained Transmission Hysteresis

Apply the persistence test after state classification and before the
cap.

An unvaccinated outbreak is **sustained** if `days_above_unity >= 14`
(fourteen or more consecutive settled days with `r_eff_estimate > 1.1`
and `vaccine_status == "none"`). Fourteen days spans two to three
serial generation intervals for respiratory and contact pathogens,
proving community transmission has escaped initial contact tracing.

If the outbreak is **sustained**, halve the state's delta cap:

- `WATCH` cap of `0.75` becomes **`0.375`**.
- `OUTBREAK` cap of `0.25` becomes **`0.125`**.
- `PANDEMIC_SHOCK` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read pathogen watch dict.** From
   `snapshot.external_data["pathogen_watch"]`, load the active alert's
   `r_eff_estimate`, `vaccine_status`, `transmission_mode`,
   `multi_hub_spread`, and `days_above_unity`. If absent or empty,
   record **CONTAINED**, note the absence, and do not cite this skill.
2. **Classify branching velocity.** Apply Reading 1 (`subcritical`,
   `smoldering`, `expanding`, or `explosive`).
3. **Classify countermeasure gap.** Apply Reading 2 (`covered`,
   `constrained`, or `unvaccinated`).
4. **Classify spillover risk.** Apply Reading 3 (`localized`, `regional`,
   or `systemic_spillover`).
5. **Classify state.** Evaluate in strict priority order
   (`PANDEMIC_SHOCK` → `OUTBREAK` → `WATCH` → `CONTAINED`) and select
   the first matching state (fallback: `OUTBREAK`).
6. **Apply persistence test.** If `days_above_unity >= 14`, halve
   `delta_cap`.
7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If the
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
8. **Cite.** If the cap bound (intended `delta` exceeded `delta_cap`),
   cite `"unvaccinated-pathogen-monitor"` in `skills_cited` and state
   the classification in the rationale.

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
  Example: `"PANDEMIC_SHOCK state; R_eff 2.1 with no working vaccine and multi-hub respiratory spillover for 16 days; delta capped at 0.05; unvaccinated-pathogen-monitor."`
- `skills_cited`: list of skill names; include
"unvaccinated-pathogen-monitor" only when the cap bound.

Worked Examples


Case A — Subcritical baseline, cap does not bind

Snapshot:
• r_eff_estimate = 0.85
• vaccine_status = "deployed_effective"
• transmission_mode = "vector_or_zoonotic"
• multi_hub_spread = false
• days_above_unity = 0
Readings:
• Branching Velocity: < 1.0 → subcritical
• Countermeasure Gap: "deployed_effective" → covered
• Spillover Risk: "vector_or_zoonotic" + false → localized
State: CONTAINED, delta cap 1.0. Persistence: days_above_unity = 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "unvaccinated-pathogen-monitor".

Case B — Multi-hub unvaccinated respiratory outbreak, cap binds

Snapshot:
• r_eff_estimate = 1.65
• vaccine_status = "none"
• transmission_mode = "airborne_respiratory"
• multi_hub_spread = true
• days_above_unity = 16
Readings:
• Branching Velocity: 1.3 to 1.8 → expanding
• Countermeasure Gap: "none" → unvaccinated
• Spillover Risk: "airborne_respiratory" + true → systemic_spillover
State: PANDEMIC_SHOCK, delta cap 0.10.
Persistence: days_above_unity = 16 >= 14 → halve to 0.05.
AGOP ranks LONG on a regional airline/hospitality or physical retail
stock. LLM intended delta = 0.80. Cap 0.05 binds. LLM returns
delta = 0.05 and cites "unvaccinated-pathogen-monitor".

Free Data Sources

The fetcher populates snapshot.external_data["pathogen_watch"] from
the following free, public epidemiological feeds (no paid subscription
required):
• WHO Disease Outbreak News (DON) API & RSS:
https://who.int (free JSON endpoint
listing emerging pathogen alerts, clade status, and vaccine availability).
• ECDC Weekly Communicable Disease Threats Reports (CDTR):
https://europa.eu
(free weekly surveillance tables across Europe and global transit hubs).
• CDC National Wastewater Surveillance System (NWSS) & Open Data:
https://cdc.gov (free Socrata API for early viral concentration
slopes prior to clinical case reporting).
• Africa CDC Weekly Outbreak Briefs:
https://africacdc.org (free weekly epidemiological tracking
across East, West, Central, and Southern Africa).
• ProMED-mail / HealthMap Open Alerts:
https://promedmail.org (free early-warning infectious disease
reporting network).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "unvaccinated-pathogen-monitor" when the cap did not
bind.

Citation Mapping

• Compartmental SIR Epidemic Threshold (R_eff > 1.0): William O.
Kermack and Anderson G. McKendrick, "A Contribution to the Mathematical
Theory of Epidemics," Proceedings of the Royal Society A 115(772),
700–721 (1927); Roy M. Anderson and Robert M. May, Infectious Diseases
of Humans: Dynamics and Control (Oxford University Press, 1991).
• Non-Linear Epidemiological Fat Tails & Multiplicative Risk:
Pasquale Cirillo and Nassim Nicholas Taleb, "Tail Risk of Contagious
Diseases," Nature Physics 16(6), 606–613 (2020). Demonstrates why
unvaccinated exponential branching must be gated early before case
counts appear linear.
• Wastewater Early-Warning Lead Time: Jordan Peccia et al.,
"Measurement of SARS-CoV-2 RNA in Wastewater Tracks Community Infection
Dynamics," Nature Biotechnology 38(10), 1164–1167 (2020).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.