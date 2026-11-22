#### name: "societal-vitality-yardstick"
description: "Measure true societal vitality via the share of women aged 20–29 at childbirth whose household equivalized income sits at least one-third (>= 1.333x) above their country of residence's poverty threshold at birth, who deliver at least one healthy offspring, and whose household with the child remains >= 1.333x above the national poverty line for at least 5 consecutive years post-birth (marital/cohabitation status strictly irrelevant), using free global longitudinal household panels and demographic registries (EU-SILC, IPUMS, DHS, U.S. Census SIPP, LIS, Statistics Finland, World Bank); cap delta or force FLAT as young-family reproductive solvency collapses."

#### Societal Vitality Yardstick (20–29 Maternal Cohort Above-Poverty Reproduction)

You are reading the tick against the **real biological and material
reproductive vitality** of the target polity or domestic consumer/labor
base. In Gary S. Becker's *A Treatise on the Family* (1981), Richard A.
Easterlin's *Birth and Fortune* (1980), David J. P. Barker's *Fetal and
Infant Origins of Adult Disease* (1992), and Amartya Sen's *Development as
Freedom* (1999), headline GDP growth and aggregate fertility rates
conceal structural demographic decay when young adults cannot afford to
form solvent households during peak biological fecundity (ages 20–29). 

Specifically, true societal vitality is defined by a single, hard,
non-ideological actuarial yardstick: 

* **Target Cohort & Income Floor (≥ 1.333× National Poverty Line):**
Women aged **20 to 29 at the birth of their child** living in a
household (marital or cohabitation status strictly irrelevant) whose
equivalized disposable household income stands **at least one-third
(≥ 133.3%) above the country of residence's official poverty
threshold** at the time of birth.
* **Healthy Offspring Delivery:** Having **at least one healthy
offspring** (surviving infancy free of severe neonatal/malnutrition
pathology, measured via national birth-registry healthy-birth and
under-five survival rates).
* **Five-Year Post-Birth Solvency Retention (Ages 0–5):** The
household containing the mother and child **remaining at least
one-third (≥ 1.333×) above the national poverty threshold for at
least five consecutive years after childbirth**—proving that child-rearing
does not push young mothers into structural poverty, housing precarity,
or state transfer dependency.

Where this **vitality cohort share (vital_cohort_share_pct)** and its
**5-year post-birth solvency retention (five_year_solvency_retention_pct)**
collapse, the society is eating its own demographic seed corn: future
prime-age tax base, housing formation, and domestic consumption will
contract regardless of short-term credit stimulus or credential inflation
(institutional-sclerosis-yardstick + older-adult-functional-capacity). 

Your job is to classify the polity into one of four societal-vitality
regimes and cap your delta accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["societal_vitality"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes longitudinal household income panels, birth
registries, and maternal-child poverty follow-ups into
snapshot.external_data["societal_vitality"]. Marital and cohabitation
fields are explicitly ignored; only **mother's age at birth (20–29)**,
**household equivalized income relative to national poverty threshold
(≥ 1.333×)**, **healthy offspring delivery**, and **5-year post-birth
household income retention** are evaluated: 

* vital_cohort_share_pct: percentage (0.0 to 100.0) of all women
aged 20–29 in the country who have at least one healthy child AND
whose household equivalized income is ≥ 1.333× the national poverty
line (≥ 22% = robust young-family formation above the poverty buffer;
< 8% = acute demographic & economic sterilization of the 20–29 cohort).
* five_year_solvency_retention_pct: percentage (0.0 to 100.0) of
mothers aged 20–29 who entered childbirth at ≥ 1.333× the national
poverty line and **remained at or above 1.333× the poverty line for
all five consecutive years post-birth** (≥ 80% = durable child-rearing
solvency; < 55% = severe "motherhood penalty" pushing young families
below the 1.333× buffer within 5 years).
* healthy_offspring_survival_pct: percentage (0.0 to 100.0) of
births to 20–29 mothers meeting healthy term/birthweight and 5-year
child survival benchmarks (≥ 94% = intact maternal-child health;
< 85% = severe biological/nutritional stress).
* consecutive_vitality_decline_years: consecutive calendar years in
which vital_cohort_share_pct OR five_year_solvency_retention_pct
has declined monotonically.

If snapshot.external_data["societal_vitality"] is absent or empty,
treat the instrument as **unmonitored**, record state
**GENERATIVE_VITALITY**, note that no societal vitality data was
available, and do not cite this skill. 

#### Reading 1 — 20–29 Above-Poverty Maternal Cohort Share (vital_cohort_share_pct)

Evaluate what share of women aged 20–29 are actually having healthy
children while maintaining a ≥ 1.333× buffer above national poverty: 

vital_cohort_share_pctCohort Formation Tier
**≥ 22.0%**
**abundant_formation** — broad solvent family formation in prime 20–29 window
**14.0% to 22.0%**
**moderate_formation** — viable but housing/wage friction delaying births
**8.0% to 14.0%**
**compressed_cohort** — majority of 20–29 cohort priced out of solvent parenthood
**< 8.0%**
**sterilized_cohort** — structural collapse of above-poverty 20–29 reproduction

If vital_cohort_share_pct is missing, treat as **moderate_formation**. 

#### Reading 2 — Five-Year Post-Birth Solvency Retention (five_year_solvency_retention_pct)

Evaluate whether households with a 20–29 mother stay ≥ 1.333× above
the national poverty line through the child's first five years: 

five_year_solvency_retention_pctPost-Birth Solvency Tier
**≥ 80.0%**
**durable_solvency** — child-rearing preserves household economic buffer over 5y
**68.0% to 80.0%**
**fragile_buffer** — childcare/housing costs erode margin for ~1 in 4 families
**55.0% to 68.0%**
**poverty_slippage** — > 1 in 3 young families fall below 1.333× poverty within 5y
**< 55.0%**
**motherhood_impoverishment** — having a child in 20s systematically triggers poverty

If five_year_solvency_retention_pct is missing, treat as **fragile_buffer**. 

#### Reading 3 — Offspring Health & Survival Integrity (healthy_offspring_survival_pct)

Evaluate biological offspring health and early-childhood survival for
the 20–29 maternal cohort: 

healthy_offspring_survival_pctOffspring Health Tier
**≥ 94.0%**
**healthy_baseline** — high term/birthweight integrity and 5y child survival
**88.0% to 94.0%**
**moderate_maternal_stress** — elevated prematurity/low-birthweight or care gaps
**< 88.0%**
**biological_attrition** — severe neonatal, nutritional, or pediatric health deficit

If healthy_offspring_survival_pct is missing, treat as **healthy_baseline**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
societal-vitality regimes. Evaluate in strict priority order and select
the first regime whose conditions are fully satisfied: 

1. **DEMOGRAPHIC_EXHAUSTION** (most severe — unconditional FLAT on domestic-demand exposure)
2. **REPRODUCTIVE_SQUEEZE**
3. **DELAYED_FORMATION_DRAG**
4. **GENERATIVE_VITALITY** (strictest adaptive fit)

#### DEMOGRAPHIC_EXHAUSTION

Any of the following hold: 

* Cohort Formation Tier is **sterilized_cohort** (< 8.0%) AND
Post-Birth Solvency Tier is **poverty_slippage** or
**motherhood_impoverishment** (< 68.0%).
* Post-Birth Solvency Tier is **motherhood_impoverishment** (< 55.0%
5-year retention above 1.333× poverty).
* Offspring Health Tier is **biological_attrition** (< 88.0%) AND
Cohort Formation Tier is **compressed_cohort** or **sterilized_cohort**.

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked on domestic consumer, housing, and long-horizon
sovereign/equity exposure. A society where women aged 20–29 either
cannot afford children at ≥ 1.333× poverty or systematically fall
below that buffer within five years of giving birth faces irreversible
base erosion. The skill binds unconditionally and must appear in
skills_cited. 

#### REPRODUCTIVE_SQUEEZE

Any of the following hold (and DEMOGRAPHIC_EXHAUSTION does not apply): 

* Cohort Formation Tier is **sterilized_cohort** (< 8.0%) with
durable_solvency or fragile_buffer.
* Cohort Formation Tier is **compressed_cohort** (8.0% to 14.0%) AND
Post-Birth Solvency Tier is **poverty_slippage** (55.0% to 68.0%).
* Offspring Health Tier is **biological_attrition** (< 88.0%).

**Delta cap: 0.25.** Young adults are heavily priced out of solvent
parenthood or experiencing sharp post-birth income slippage. Cut
domestic long exposure substantially. 

#### DELAYED_FORMATION_DRAG

Any of the following hold (and neither DEMOGRAPHIC_EXHAUSTION nor
REPRODUCTIVE_SQUEEZE applies): 

* Cohort Formation Tier is **compressed_cohort** (8.0% to 14.0%) with
durable_solvency or fragile_buffer.
* Cohort Formation Tier is **moderate_formation** (14.0% to 22.0%)
AND Post-Birth Solvency Tier is **fragile_buffer** or
**poverty_slippage**.
* Offspring Health Tier is **moderate_maternal_stress** (88.0% to 94.0%).
Delta cap: 0.70. Family formation is intact for financially buffered
households, but housing/tax wedges are pushing births out of the 20–29
window. Trim domestic growth sizing relative to GENERATIVE_VITALITY.

GENERATIVE_VITALITY

All of the following hold:
• Cohort Formation Tier is abundant_formation (≥ 22.0% of women
20–29 having ≥ 1 healthy child at ≥ 1.333× national poverty).
• Post-Birth Solvency Tier is durable_solvency (≥ 80.0% staying
≥ 1.333× above poverty for 5 consecutive years post-birth).
• Offspring Health Tier is healthy_baseline (≥ 94.0%).
Delta cap: 1.0. Deep, self-sustaining generational renewal: young
mothers and children maintain a durable ≥ 1/3 income buffer above
poverty across early childhood. The cap equals the strategy cap; the
skill never binds on GENERATIVE_VITALITY.

Ambiguous fallback

Any combination not covered above is classified REPRODUCTIVE_SQUEEZE
with delta cap 0.25.

Secondary Filter / Asymmetric Gate — Multi-Year Cohort Sterilization Hysteresis

Apply the persistence test after regime classification and before the
cap.
A societal vitality contraction is structurally entrenched if
consecutive_vitality_decline_years >= 5 (five or more consecutive
calendar years of declining vital_cohort_share_pct or
five_year_solvency_retention_pct). Five consecutive annual cohorts
losing above-poverty reproductive capacity proves that structural
housing, tax, or wage barriers are compounding across the entire 20–29
generation rather than reflecting a single-year recession.
If the vitality decline is structurally entrenched, halve the
regime's delta cap:
• DELAYED_FORMATION_DRAG cap of 0.70 becomes 0.35.
• REPRODUCTIVE_SQUEEZE cap of 0.25 becomes 0.125.
• DEMOGRAPHIC_EXHAUSTION cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read societal vitality dict. From
snapshot.external_data["societal_vitality"], load
vital_cohort_share_pct, five_year_solvency_retention_pct,
healthy_offspring_survival_pct, and
consecutive_vitality_decline_years. If absent or empty, record
GENERATIVE_VITALITY, note the omission, and do not cite this
skill.
2. Classify cohort formation tier. Apply Reading 1
(abundant_formation, moderate_formation, compressed_cohort, or
sterilized_cohort).
3. Classify post-birth solvency tier. Apply Reading 2
(durable_solvency, fragile_buffer, poverty_slippage, or
motherhood_impoverishment).
4. Classify offspring health tier. Apply Reading 3
(healthy_baseline, moderate_maternal_stress, or
biological_attrition).
5. Classify regime. Evaluate in strict priority order
(DEMOGRAPHIC_EXHAUSTION → REPRODUCTIVE_SQUEEZE →
DELAYED_FORMATION_DRAG → GENERATIVE_VITALITY) and select the
first matching regime (fallback: REPRODUCTIVE_SQUEEZE).
6. Apply persistence test. If
consecutive_vitality_decline_years >= 5, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
regime is DEMOGRAPHIC_EXHAUSTION, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
regime is DEMOGRAPHIC_EXHAUSTION, cite
"societal-vitality-yardstick" in skills_cited and state the
20–29 cohort formation and 5-year post-birth solvency finding in the
rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If DEMOGRAPHIC_EXHAUSTION,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"DEMOGRAPHIC_EXHAUSTION regime; vital_cohort_share=6.8% (<8% sterilized_cohort) and 5y post-birth >=1.333x poverty retention=52.0% (<55%); forcing action=FLAT; societal-vitality-yardstick."
• skills_cited: list of skill names; include
"societal-vitality-yardstick" only when the cap bound or the regime
is DEMOGRAPHIC_EXHAUSTION.

Worked Examples


Case A — High 20–29 above-poverty birth cohort with durable 5-year post-birth solvency, cap does not bind

Snapshot:
• vital_cohort_share_pct = 24.5
• five_year_solvency_retention_pct = 84.0
• healthy_offspring_survival_pct = 97.5
• consecutive_vitality_decline_years = 0
Readings:
• Cohort Formation Tier: ≥ 22.0% → abundant_formation
• Post-Birth Solvency Tier: ≥ 80.0% → durable_solvency
• Offspring Health Tier: ≥ 94.0% → healthy_baseline
Regime: GENERATIVE_VITALITY, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "societal-vitality-yardstick".

Case B — Compressed 20–29 cohort with multi-year decline, cap binds

Snapshot:
• vital_cohort_share_pct = 11.2
• five_year_solvency_retention_pct = 71.0
• healthy_offspring_survival_pct = 96.8
• consecutive_vitality_decline_years = 6
Readings:
• Cohort Formation Tier: 8.0% to 14.0% → compressed_cohort
• Post-Birth Solvency Tier: 68.0% to 80.0% → fragile_buffer
• Offspring Health Tier: ≥ 94.0% → healthy_baseline
Regime: DELAYED_FORMATION_DRAG, delta cap 0.70.
Persistence: consecutive_vitality_decline_years = 6 >= 5 → halve to 0.35.
AGOP ranks LONG. LLM intended delta = 0.80. Cap 0.35 binds.
LLM returns delta = 0.35 and cites "societal-vitality-yardstick".

Case C — Sterilized 20–29 cohort and <55% 5-year post-birth solvency above 1.333x poverty, unconditional FLAT

Snapshot:
• vital_cohort_share_pct = 6.4
• five_year_solvency_retention_pct = 51.5
• healthy_offspring_survival_pct = 96.0
• consecutive_vitality_decline_years = 7
Readings:
• Cohort Formation Tier: < 8.0% → sterilized_cohort
• Post-Birth Solvency Tier: < 55.0% → motherhood_impoverishment
• Offspring Health Tier: ≥ 94.0% → healthy_baseline
Regime: DEMOGRAPHIC_EXHAUSTION, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "societal-vitality-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["societal_vitality"]
from the following free, open global longitudinal household panels,
income-distribution microdata, and birth/child-survival registries
(no paid subscription required):

Global Harmonized Household & Demographic Panels

• Luxembourg Income Study (LIS) & World Bank Poverty and Inequality Platform (PIP):
https://lisdatacenter.org and https://worldbank.org (free
harmonized cross-national microdata and APIs measuring equivalized
household income relative to national poverty thresholds by mother's
age and presence of children under 5).
• IPUMS International & IPUMS DHS (Demographic and Health Surveys):
https://ipums.org and https://dhsprogram.com (free
open census microdata and 90+ country maternal/childbirth panels
tracking women aged 20–29, household wealth/income quintiles, infant
health, and 5-year child survival across Africa, Asia, and Latin America).
• UNICEF Data Warehouse & WHO Global Health Observatory (GHO):
https://unicef.org and https://who.int (free
REST/SDMX APIs supplying maternal-age-specific fertility, low
birthweight, neonatal health, and under-five survival rates globally).

Europe & Nordic Longitudinal Registries

• Eurostat EU-SILC Longitudinal Panel & Statistics Finland (Tilastokeskus PxWeb):
https://europa.eu and https://stat.fi (free
4-year rotating longitudinal income-and-living-conditions microdata
and open Nordic birth/income tables tracking household equivalized
income transitions before and after childbirth irrespective of marital
status).

North America, Asia-Pacific & Latin America

• U.S. Census Bureau SIPP (Survey of Income and Program Participation) & IPUMS CPS:
https://census.gov and
https://ipums.org (free multi-year longitudinal panels tracking
household income-to-poverty ratios (>= 1.333x) for mothers aged
20–29 across 5 consecutive years post-birth).
• CEPALSTAT (UN ECLAC Latin America) & IBGE PNAD Contínua (Brazil):
https://cepal.org and https://ibge.gov.br (free
longitudinal household income and maternal/child poverty panels across
Latin America).
• India NFHS / MoSPI Periodic Labour Force Survey & China CFPS / NBS Open Data:
https://mospi.gov.in and https://pku.edu.cn
(free open household income and maternal-child longitudinal surveys).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not condition on marital or cohabitation status; evaluate strictly
on mother's age (20–29 at birth), household equivalized income
(>= 1.333x national poverty line), healthy offspring delivery, and
5-year post-birth retention.
• Do not substitute headline GDP per capita or aggregate Total Fertility
Rate (TFR) when vital_cohort_share_pct or
five_year_solvency_retention_pct is available.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "societal-vitality-yardstick" when the cap did not bind
and the regime is not DEMOGRAPHIC_EXHAUSTION.

Citation Mapping

• Household Economics & Quality-Quantity Trade-Off: Gary S. Becker,
A Treatise on the Family (Harvard University Press, 1981), Ch. 5
(household income constraints and investment in healthy offspring).
• Cohort Economic Headroom & Generational Fertility: Richard A.
Easterlin, Birth and Fortune: The Impact of Numbers on Personal
Welfare (Basic Books, 1980) (relative income of young adults aged
20–29 and family formation).
• Developmental Origins of Health & Capability Floor: David J. P.
Barker, Fetal and Infant Origins of Adult Disease (BMJ Publishing,
1992); Amartya Sen, Development as Freedom (Anchor, 1999) (early
childhood material security above the poverty line).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.