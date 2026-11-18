---
name: "older-adult-functional-capacity"
description: "Classify the current tick by the share of the 70+ population retaining full cognitive and physical functional capacity (zero ADL/IADL limitations and intact cognition) out of total 70+ population, using region-specific free longitudinal aging surveys (SHARE, HRS, ELSA, CHARLS, LASI, JSTAR, HAALSI, WHO SAGE, MHAS, ELSI-Brazil) and WHO HALE telemetry, and cap delta accordingly."
---

# Older-Adult Functional Capacity (`70+` Cohort)

You are reading the tick against the **true functional compression of
morbidity** in the `70+` population. Headline life-expectancy and
elderly-dependency ratios treat every person aged `70+` as an identical
statistical unit. In reality, an aging society's fiscal solvency,
caregiving labor drain, and senior-consumer vitality depend on one ratio:

$$\text{Functional Autonomy Share}_{70+} = \frac{\text{Population}_{70+}\text{ with full cognitive \& physical capacity}}{\text{Total Population}_{70+}}$$

In James Fries's *Compression of Morbidity* framework (1980) and
Joseph Tainter's *Collapse of Complex Societies* (1988), when medical
intervention extends chronological survival (`70+` headcount grows)
without compressing cognitive and physical disability (dementia,
frailty, ADL/IADL loss), the economy enters an **expansion of
morbidity**: working-age adults are pulled out of productive labor into
unpaid caregiving, healthcare overhead consumes public budgets, and
senior consumption shifts from discretionary goods to custodial survival.

Your job is to classify the tick into one of four functional-aging
states and cap your `delta` accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["functional_aging_70plus"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes region-specific longitudinal aging panels and
WHO healthy-life-expectancy ratios into
`snapshot.external_data["functional_aging_70plus"]`. Each region or
country entry (keyed by ISO-2 code or regional hub such as `fi`, `eu`,
`de`, `uk`, `us`, `jp`, `kr`, `sh`, `in`, `ke`, `rw`, `et`, `za`,
`br`, `mx`, or `global_baseline`) supplies:

- `intact_70plus_share_pct`: percentage of the total `70+` population
  with **full physical and cognitive capacity** (`0` Katz ADL
  limitations, `0` Lawton IADL limitations, and intact cognitive
  screening score above dementia/MCI impairment cutoffs).
- `intact_share_5yr_change_pct`: percentage-point change in
  `intact_70plus_share_pct` over the trailing five settled years
  (positive = compression of morbidity; negative = expansion of
  morbidity).
- `pop_70plus_share_pct`: adults aged `70+` as a percentage of the total
  national population (measuring macro demographic weight).
- `source_panel`: identifier of the regional open longitudinal panel
  used (`SHARE`, `HRS`, `ELSA`, `CHARLS`, `LASI`, `JSTAR`, `HAALSI`,
  `WHO_SAGE`, `MHAS`, `ELSI_BRAZIL`, or `WHO_GHO_HALE`).
- `years_morbidity_expansion`: consecutive settled years in which
  `intact_share_5yr_change_pct < 0.0` while `pop_70plus_share_pct >= 12.0`.

If `snapshot.external_data["functional_aging_70plus"]` is absent or
empty, treat the region as **unmonitored**, record state **STABLE_COHORT**,
note that no `70+` functional capacity data was available, and do not
cite this skill.

### Reading 1 — Full cognitive & physical capacity share (`intact_70plus_share_pct`)

Evaluate the share of adults aged `70+` who remain free of ADL/IADL
limitations and cognitive impairment:

| `intact_70plus_share_pct` | Functional Autonomy |
|---|---|
| > 65% | **compressed_morbidity** — high cognitive & physical autonomy past 70 |
| 50% to 65% | **moderate_autonomy** — majority functional, rising late-life care load |
| 35% to 50% | **fragile_cohort** — half or more of `70+` require cognitive/physical support |
| < 35% | **expanded_morbidity** — severe cognitive/physical disability burden in `70+` |

### Reading 2 — Morbidity trajectory (`intact_share_5yr_change_pct`)

Evaluate whether additional years past 70 are being lived in full
capacity (compression) or prolonged disability (expansion):

| `intact_share_5yr_change_pct` | Morbidity Trajectory |
|---|---|
| > +1.5% | **compressing** — functional healthspan rising faster than lifespan |
| −0.5% to +1.5% | **stationary** — stable functional ratio |
| −2.5% to −0.5% | **eroding** — cognitive/physical impairment share creeping upward |
| < −2.5% | **expanding_disability** — rapid expansion of dependent morbidity |

If `intact_share_5yr_change_pct` is missing, treat as **stationary**.

### Reading 3 — Demographic weight of the `70+` cohort (`pop_70plus_share_pct`)

Evaluate `pop_70plus_share_pct` to determine how heavily `70+` care
requirements tax the broader working-age economy:

| `pop_70plus_share_pct` | Cohort Weight |
|---|---|
| < 6% | **youth_buffered** — small `70+` cohort relative to workforce |
| 6% to 13% | **transitioning** — growing senior share; manageable care ratio |
| > 13% | **top_heavy** — massive `70+` demographic weight; acute care multiplier |

If `pop_70plus_share_pct` is missing, treat as **transitioning**.

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four states.
Evaluate in strict priority order and select the first state whose
conditions are fully satisfied:

1. **CARE_OVERLOAD** (most severe)
2. **MORBIDITY_DRAG**
3. **STABLE_COHORT**
4. **COMPRESSED_VITALITY** (strictest adaptive fit)

### CARE_OVERLOAD

Any of the following hold:

- Functional Autonomy is **expanded_morbidity** (`< 35%`) AND Cohort
  Weight is **transitioning** or **top_heavy** (`≥ 6%`).
- Functional Autonomy is **fragile_cohort** (`35% to 50%`) AND Cohort
  Weight is **top_heavy** (`> 13%`) AND Morbidity Trajectory is
  **eroding** or **expanding_disability**.
- Functional Autonomy is **moderate_autonomy** (`50% to 65%`) AND Cohort
  Weight is **top_heavy** (`> 13%`) AND Morbidity Trajectory is
  **expanding_disability** (`< -2.5%`).

**Delta cap: 0.10.** A large `70+` demographic cohort is experiencing
falling cognitive and physical autonomy. Caregiving labor withdrawals,
dementia/long-term care costs, and fiscal transfers directly compress
domestic growth. Trade only if the AGOP ranking targets elder-care
robotics, neuro-protective biotech/nutraceutical IP, or youthful
export corridors. In most cases, return FLAT.

### MORBIDITY_DRAG

Any of the following hold (and `CARE_OVERLOAD` does not apply):

- Functional Autonomy is **expanded_morbidity** (`< 35%`) with
  **youth_buffered** cohort weight (`< 6%`).
- Functional Autonomy is **fragile_cohort** (`35% to 50%`).
- Functional Autonomy is **moderate_autonomy** (`50% to 65%`) AND Cohort
  Weight is **top_heavy** (`> 13%`) AND Morbidity Trajectory is
  **stationary** or **eroding**.

**Delta cap: 0.25.** Rising `70+` cognitive and physical impairment is
absorbing household savings and workforce hours. Reduce position size
substantially on domestic consumer-discretionary and labor-constrained
assets.

### STABLE_COHORT

Any of the following hold (and neither `CARE_OVERLOAD` nor
`MORBIDITY_DRAG` applies):

- Functional Autonomy is **moderate_autonomy** (`50% to 65%`) AND Cohort
  Weight is **youth_buffered** or **transitioning** (`≤ 13%`).
- Functional Autonomy is **compressed_morbidity** (`> 65%`) AND Cohort
  Weight is **top_heavy** (`> 13%`).
- Functional Autonomy is **compressed_morbidity** (`> 65%`) AND Morbidity
  Trajectory is **eroding** or **expanding_disability**.

**Delta cap: 0.75.** Senior functional capacity remains solid, though
demographic top-heaviness or mild erosion prevents full slack. Reduce
size relative to COMPRESSED_VITALITY.

### COMPRESSED_VITALITY

All of the following hold:

- Functional Autonomy is **compressed_morbidity** (`> 65%`).
- Morbidity Trajectory is **compressing** or **stationary** (`≥ -0.5%`).
- Cohort Weight is **youth_buffered** or **transitioning** (`≤ 13%`).

**Delta cap: 1.0.** High `70+` cognitive and physical autonomy paired with
a balanced age structure; minimal custodial overhead. The cap equals the
strategy cap; the skill never binds on COMPRESSED_VITALITY.

### Ambiguous fallback

Any combination not covered above is classified **MORBIDITY_DRAG** with
delta cap `0.25`.

## Secondary Filter / Asymmetric Gate — Morbidity Expansion Hysteresis

Apply the persistence test after state classification and before the
cap.

A region's functional decline is **structurally entrenched** if
`years_morbidity_expansion >= 3` (three or more consecutive settled
years in which `intact_share_5yr_change_pct < 0.0` while
`pop_70plus_share_pct >= 12.0`). Three consecutive years of falling
cognitive/physical autonomy inside a top-heavy `70+` population reflects
irreversible cohort aging and neurodegenerative prevalence that cannot
reverse within a business cycle.

If the decline is **structurally entrenched**, halve the state's delta
cap:

- `STABLE_COHORT` cap of `0.75` becomes **`0.375`**.
- `MORBIDITY_DRAG` cap of `0.25` becomes **`0.125`**.
- `CARE_OVERLOAD` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read functional aging dict.** From
   `snapshot.external_data["functional_aging_70plus"]`, load the target
   region's `intact_70plus_share_pct`, `intact_share_5yr_change_pct`,
   `pop_70plus_share_pct`, `source_panel`, and
   `years_morbidity_expansion`. If absent or empty, record
   **STABLE_COHORT**, note the omission, and do not cite this skill.
2. **Classify functional autonomy.** Apply Reading 1
(compressed_morbidity, moderate_autonomy, fragile_cohort, or
expanded_morbidity).
3. Classify morbidity trajectory. Apply Reading 2 (compressing,
stationary, eroding, or expanding_disability).
4. Classify cohort weight. Apply Reading 3 (youth_buffered,
transitioning, or top_heavy).
5. Classify state. Evaluate in strict priority order
(CARE_OVERLOAD → MORBIDITY_DRAG → STABLE_COHORT →
COMPRESSED_VITALITY) and select the first matching state
(fallback: MORBIDITY_DRAG).
6. Apply persistence test. If years_morbidity_expansion >= 3,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta exceeded delta_cap),
cite "older-adult-functional-capacity" in skills_cited and state
the classification and source_panel in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state, source panel, and cap
reason. Example: "CARE_OVERLOAD state; SHARE panel shows 46% intact 70+ functional capacity with -1.4% 5yr erosion across a 16.5% 70+ population for 4 years; delta capped at 0.05; older-adult-functional-capacity."
• skills_cited: list of skill names; include
"older-adult-functional-capacity" only when the cap bound.

Worked Examples


Case A — High 70+ autonomy in transitioning cohort, cap does not bind

Snapshot:
• intact_70plus_share_pct = 68.5
• intact_share_5yr_change_pct = +1.8
• pop_70plus_share_pct = 10.5
• source_panel = "HRS"
• years_morbidity_expansion = 0
Readings:
• Functional Autonomy: > 65% → compressed_morbidity
• Morbidity Trajectory: > +1.5% → compressing
• Cohort Weight: 6% to 13% → transitioning
State: COMPRESSED_VITALITY, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "older-adult-functional-capacity".

Case B — Top-heavy European 70+ population with eroding functional capacity, cap binds

Snapshot:
• intact_70plus_share_pct = 47.0
• intact_share_5yr_change_pct = -1.6
• pop_70plus_share_pct = 16.8
• source_panel = "SHARE"
• years_morbidity_expansion = 4
Readings:
• Functional Autonomy: 35% to 50% → fragile_cohort
• Morbidity Trajectory: -2.5% to -0.5% → eroding
• Cohort Weight: > 13% → top_heavy
State: CARE_OVERLOAD, delta cap 0.10.
Persistence: years_morbidity_expansion = 4 >= 3 → halve to 0.05.
AGOP ranks LONG on a domestic consumer or labor-heavy equity. LLM
intended delta = 0.75. Cap 0.05 binds. LLM returns delta = 0.05
and cites "older-adult-functional-capacity".

Free & Open Regional Data Sources (Harmonized HRS-Family Panels)

The fetcher populates snapshot.external_data["functional_aging_70plus"]
using each global region's own free, open, academically harmonized
longitudinal aging study (each measuring Katz ADL, Lawton IADL, and
cognitive recall/orientation in 70+ respondents) alongside WHO/UN
demographic denominators:

Global Region Regional Data Source  Endpoint / Access (Free & Open)
Europe & Nordics (eu, fi, se, de, fr, it, es) SHARE (Survey of Health, Ageing and Retirement in Europe) + Eurostat Healthy Life Years (hlth_hlye) https://share-eric.eu (free scientific registration; harmonized waves 1–9 covering ADL, IADL, and cognitive scores for 70+ across 28 European countries) & https://europa.eu (free open API).
United Kingdom (uk) ELSA (English Longitudinal Study of Ageing) https://elsa-project.ac.uk & UK Data Service (https://ukdataservice.ac.uk, free academic/research download of waves 1–10 functional & cognitive batteries).
North America (us, ca)  HRS (Health and Retirement Study — University of Michigan) & CLSA (Canadian Longitudinal Study on Aging)  https://umich.edu (free registration, RAND HRS Longitudinal File with harmonized 70+ ADL/IADL and cognitive impairment indices).
China & East Asia (sh, hk, jp, kr)  CHARLS (China Health and Retirement Longitudinal Study), JSTAR (Japanese Study of Aging and Retirement), & KLoSA (Korean Longitudinal Study of Aging) https://pku.edu.cn (free Peking University data portal), https://rieti.go.jp (free RIETI application), & https://keis.or.kr (free KEIS public data).
India & South Asia (in) LASI (Longitudinal Ageing Study in India) https://iipsindia.ac.in & Gateway to Global Aging (https://g2aging.org, free harmonized 70+ ADL/IADL and cognition datasets).
Sub-Saharan Africa (za, ke, rw, et, ng, ug, tz) HAALSI (Health and Aging in Africa: A Longitudinal Study of an INDEPTH Community), WHO SAGE (Study on Global AGEing and Adult Health), & DHS Disability/Functioning Modules https://haalsi.org (free Harvard Dataverse public datasets), https://who.int (free WHO microdata catalog), & https://dhsprogram.com (free Demographic and Health Surveys).
Latin America (br, mx, ar)  ELSI-Brazil (Brazilian Longitudinal Study of Aging) & MHAS (Mexican Health and Aging Study) https://fiocruz.br (free Fiocruz data portal) & https://mhasweb.org (free NIH/UTMB public dataset).
Cross-Regional Harmonization & Denominators Gateway to Global Aging Data (g2aging.org), WHO GHO (WHOSIS_000002 HALE), & UN World Population Prospects (70+ Cohort Share)  https://g2aging.org (free cross-study harmonized codebooks across HRS, SHARE, ELSA, CHARLS, LASI, JSTAR, KLoSA, MHAS, ELSI), https://azureedge.net, & https://un.org.


Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not use raw life expectancy or total 70+ headcount alone; always
evaluate the ratio of 70+ adults retaining full cognitive and
physical capacity out of total 70+ population.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "older-adult-functional-capacity" when the cap did not
bind.

Citation Mapping

• Compression of Morbidity Hypothesis: James F. Fries, "Aging,
Natural Death, and the Compression of Morbidity," New England
Journal of Medicine 303(3), 130–135 (1980). Defines healthy aging as
delaying the onset of cognitive and physical disability closer to the
end of life rather than prolonging dependent morbidity.
• Katz ADL & Lawton IADL Functional Autonomy Scales: Sidney Katz et
al., "Studies of Illness in the Aged: The Index of ADL," JAMA
185(12), 914–919 (1963); M. Powell Lawton and Elaine M. Brody,
"Assessment of Older People: Self-Maintaining and Instrumental
Activities of Daily Living," The Gerontologist 9(3), 179–186
(1969).
• Cross-National HRS-Family Longitudinal Harmonization: Drystan
Phillips et al. / Gateway to Global Aging Data (USC Schaeffer Center /
NIA), Harmonized Aging Surveys Across Europe, the Americas, Asia, and
Africa (SHARE, HRS, ELSA, CHARLS, LASI, JSTAR, KLoSA, MHAS, ELSI,
HAALSI).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.