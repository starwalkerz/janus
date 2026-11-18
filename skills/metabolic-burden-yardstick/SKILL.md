---
name: "metabolic-burden-yardstick"
description: "Classify the current tick by population adult obesity prevalence and metabolic trajectory using free WHO GHO and NCD-RisC telemetry, and cap delta accordingly."
---

# Metabolic Burden Yardstick

You are reading the tick against the biological vitality and metabolic
overhead of the target polity's workforce and consumer base. Ibn Khaldun
observed in the *Muqaddimah* (1377) that polities rise on physical
hardiness (*asabiyyah*) and decay when urban luxury, sedentism, and
caloric excess erode bodily vitality. Joseph Tainter (*The Collapse of
Complex Societies*, 1988) demonstrated that as chronic biological
dysfunction rises, a society must divert ever-larger shares of its
economic surplus into non-productive maintenance overhead (clinical
intervention, disability transfers, and sick leave), yielding declining
marginal returns.

In modern economies, rising adult obesity prevalence (`BMI >= 30 kg/m²`)
is a direct, measurable proxy for biological sclerosis: it compresses
labor productivity, raises healthcare fiscal drag, and signals that
incumbent ultra-processed food and sedentary infrastructure are
consuming the population's energetic surplus.

Your job is to classify the tick into one of four metabolic states and
cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["metabolic_health"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes national and regional epidemiological series into
`snapshot.external_data["metabolic_health"]`. Each region entry (keyed
by ISO-2 geography code such as `us`, `uk`, `eu`, `fi`, `ke`, `rw`,
`et`, `in`, `br`, or `global_baseline`) supplies:

- `adult_obesity_pct`: age-standardized prevalence of adult obesity
  (`BMI >= 30 kg/m²`, ages 18+) as a percentage of the adult population.
- `obesity_5yr_change_pct`: percentage-point change in `adult_obesity_pct`
  over the trailing five settled years.
- `youth_obesity_pct`: prevalence of obesity among children and
  adolescents (`ages 5–19`) as a percentage, capturing forward
  generational metabolic lock-in.
- `years_above_30pct`: consecutive settled years in which
  `adult_obesity_pct >= 30.0`.

If `snapshot.external_data["metabolic_health"]` is absent or empty,
treat the region as **unmonitored**, record state **STRAINED**, note
that no metabolic health data was available, and do not cite this
skill.

### Reading 1 — Adult obesity prevalence (`adult_obesity_pct`)

Evaluate the current adult obesity rate against physiological carrying
capacity:

| `adult_obesity_pct` | Burden Level |
|---|---|
| < 15% | **lean_vital** — high physical workforce vitality; low chronic drag |
| 15% to 25% | **moderate** — emerging urban dietary transition; manageable load |
| 25% to 35% | **burdened** — heavy chronic morbidity & rising healthcare overhead |
| > 35% | **sclerotic_metabolic** — severe biological decay & fiscal/labor drag |

### Reading 2 — Five-year metabolic trajectory (`obesity_5yr_change_pct`)

Evaluate whether the metabolic burden is compounding or reversing:

| `obesity_5yr_change_pct` | Trajectory |
|---|---|
| < 0.0% | **reversing** — active dietary/metabolic recovery |
| 0.0% to +1.0% | **plateau** — stabilized prevalence |
| +1.0% to +2.5% | **rising_steady** — persistent metabolic erosion |
| > +2.5% | **accelerating** — rapid ultra-processed & sedentary lock-in |

### Reading 3 — Generational lock-in (`youth_obesity_pct`)

Evaluate `youth_obesity_pct` (ages 5–19) to determine whether metabolic
decay has already been imprinted onto the incoming cohort:

| `youth_obesity_pct` | Generational Signal |
|---|---|
| < 8% | **unimprinted** — youth cohort retains baseline physical vitality |
| 8% to 15% | **encroaching** — early adolescent metabolic drift |
| > 15% | **imprinted** — permanent multi-decade morbidity pipeline |

If `youth_obesity_pct` is missing, treat as **encroaching**.

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four metabolic
states. Evaluate in strict priority order and select the first state
whose conditions are fully satisfied:

1. **DEGENERATED** (most severe)
2. **BURDENED**
3. **STRAINED**
4. **VITAL** (strictest adaptive fit)

### DEGENERATED

Any of the following hold:

- Burden Level is **sclerotic_metabolic** (`> 35%`) AND Trajectory is
  **rising_steady** or **accelerating**.
- Burden Level is **sclerotic_metabolic** AND Generational Signal is
  **imprinted** (`> 15%` youth obesity).
- Burden Level is **burdened** (`25–35%`) AND Trajectory is
  **accelerating** AND Generational Signal is **imprinted**.

**Delta cap: 0.10.** The polity is in advanced biological and fiscal
sclerosis. Healthcare maintenance overhead consumes marginal growth
while workforce stamina and consumer discretionary resilience erode.
Trade only if the AGOP ranking targets direct metabolic-remediation IP,
functional low-sugar nutrition, or non-domestic export vehicles. In
most cases, return FLAT.

### BURDENED

Any of the following hold (and `DEGENERATED` does not apply):

- Burden Level is **sclerotic_metabolic** (`> 35%`) with **plateau** or
  **reversing** trajectory.
- Burden Level is **burdened** (`25–35%`) AND Trajectory is
  **rising_steady** or **accelerating**.
- Burden Level is **moderate** (`15–25%`) AND Trajectory is
  **accelerating** AND Generational Signal is **imprinted**.

**Delta cap: 0.25.** Chronic metabolic drag is compressing labor output
and redirecting household income toward medical overhead. Reduce
position size substantially on domestic consumer and labor-intensive
assets.

### STRAINED

Any of the following hold (and neither `DEGENERATED` nor `BURDENED`
applies):

- Burden Level is **burdened** (`25–35%`) AND Trajectory is **plateau**
  or **reversing**.
- Burden Level is **moderate** (`15–25%`) AND Trajectory is **plateau**,
  **rising_steady**, or **accelerating**.
- Burden Level is **lean_vital** (`< 15%`) AND Trajectory is
  **accelerating**.

**Delta cap: 0.75.** Early metabolic transition is underway; vitality
remains functional, but ultra-processed dietary drift is beginning to
build future overhead. Reduce size relative to VITAL.

### VITAL

All of the following hold:

- Burden Level is **lean_vital** (`< 15%`).
- Trajectory is **reversing**, **plateau**, or **rising_steady**.
- Generational Signal is **unimprinted** (`< 8%` youth obesity).

**Delta cap: 1.0.** High biological vitality and low chronic healthcare
overhead. The cap equals the strategy cap; the skill never binds on
VITAL.

### Ambiguous fallback

Any combination not covered above is classified **BURDENED** with delta
cap `0.25`.

## Secondary Filter / Asymmetric Gate — Chronic Compounding Hysteresis

Apply the persistence test after state classification and before the
cap.

A region's metabolic decay is **structurally entrenched** if
`years_above_30pct >= 5` (five or more consecutive settled years with
`adult_obesity_pct >= 30.0`). Five consecutive years above 30% marks
multi-year institutional and agricultural lock-in (subsidized refined
sugars, car-dependent zoning, and chronic pharmaceutical dependence)
that cannot reverse within a single business cycle.

If the decay is **structurally entrenched**, halve the state's delta
cap:

- `STRAINED` cap of `0.75` becomes **`0.375`**.
- `BURDENED` cap of `0.25` becomes **`0.125`**.
- `DEGENERATED` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read metabolic health dict.** From
   `snapshot.external_data["metabolic_health"]`, load the target
   region's `adult_obesity_pct`, `obesity_5yr_change_pct`,
   `youth_obesity_pct`, and `years_above_30pct`. If absent or empty,
   record **STRAINED**, note the omission, and do not cite this skill.
2. **Classify burden level.** Apply Reading 1 (`lean_vital`,
   `moderate`, `burdened`, or `sclerotic_metabolic`).
3. **Classify trajectory.** Apply Reading 2 (`reversing`, `plateau`,
   `rising_steady`, or `accelerating`).
4. **Classify generational lock-in.** Apply Reading 3 (`unimprinted`,
   `encroaching`, or `imprinted`).
5. **Classify state.** Evaluate in strict priority order
   (`DEGENERATED` → `BURDENED` → `STRAINED` → `VITAL`) and select the
   first matching state (fallback: `BURDENED`).
6. **Apply persistence test.** If `years_above_30pct >= 5`, halve
   `delta_cap`.
7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If the
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`.
8. **Cite.** If the cap bound (intended `delta` exceeded `delta_cap`),
   cite `"metabolic-burden-yardstick"` in `skills_cited` and state the
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
  Example: `"DEGENERATED metabolic state; adult obesity 39% with +2.8% 5yr acceleration and imprinted youth obesity (18%) above 30% for 8 years; delta capped at 0.05; metabolic-burden-yardstick."`
- `skills_cited`: list of skill names; include
"metabolic-burden-yardstick" only when the cap bound.

Worked Examples


Case A — Vital youth-led economy, cap does not bind

Snapshot (e.g., East African corridor rw / et / ke):
• adult_obesity_pct = 8.5
• obesity_5yr_change_pct = +0.8
• youth_obesity_pct = 3.2
• years_above_30pct = 0
Readings:
• Burden Level: < 15% → lean_vital
• Trajectory: 0.0% to +1.0% → plateau
• Generational Signal: < 8% → unimprinted
State: VITAL, delta cap 1.0. Persistence: years_above_30pct = 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "metabolic-burden-yardstick".

Case B — Sclerotic metabolic regime with generational lock-in, cap binds

Snapshot (e.g., mature Western consumer economy):
• adult_obesity_pct = 41.5
• obesity_5yr_change_pct = +2.7
• youth_obesity_pct = 19.8
• years_above_30pct = 9
Readings:
• Burden Level: > 35% → sclerotic_metabolic
• Trajectory: > +2.5% → accelerating
• Generational Signal: > 15% → imprinted
State: DEGENERATED, delta cap 0.10.
Persistence: years_above_30pct = 9 >= 5 → halve to 0.05.
AGOP ranks LONG on a domestic mass-market consumer stock. LLM intended
delta = 0.75. Cap 0.05 binds. LLM returns delta = 0.05 and cites
"metabolic-burden-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["metabolic_health"] from
the following free, public endpoints (no authentication required):
• WHO Global Health Observatory (GHO) OData API:
https://azureedge.net (age-standardized adult
obesity prevalence BMI >= 30) and
https://azureedge.net (child/adolescent
obesity prevalence ages 5–19). Free JSON/CSV OData queries by ISO-3
country code.
• NCD Risk Factor Collaboration (NCD-RisC):
https://ncdrisc.org (free global
country-level historical BMI and obesity time series from 1975 to
present, published in The Lancet).
• World Bank Health, Nutrition and Population Statistics:
https://worldbank.org and
SH.STA.OB18.FE.ZS (free CC BY-4.0 CSV/API downloads).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not treat DEGENERATED or BURDENED as a reason to penalize
export-oriented functional nutrition, low-sugar nutraceuticals, or
metabolic-remediation IP—unless the ticker relies on unhedged
domestic mass-market consumption.
• Do not cite "metabolic-burden-yardstick" when the cap did not bind.

Citation Mapping

• Sedentary Luxury & Biological Decay: Ibn Khaldun, Muqaddimah
(1377), Ch. III. Urban luxury, dietary excess, and physical
softness erode the asabiyyah and physiological vigor of mature
polities across generations.
• Healthcare Maintenance Overhead & Declining Returns: Joseph A.
Tainter, The Collapse of Complex Societies (1988). Rising chronic
morbidity forces complex societies to allocate increasing capital to
non-productive maintenance rather than net-surplus generation.
• Evolutionary Mismatch & Caloric Overload: Daniel E. Lieberman,
The Story of the Human Body: Evolution, Health, and Disease
(Pantheon, 2013). Industrial ultra-processed diets and sedentary
infrastructure produce mismatch diseases that tax workforce stamina.
• Global BMI Thresholds & Generational Trajectory: NCD Risk Factor
Collaboration (NCD-RisC), "Worldwide trends in underweight and
obesity from 1990 to 2022," The Lancet 403(10431), 1027–1050
(2024); WHO Global Health Observatory (NCD_BMI_30A).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.