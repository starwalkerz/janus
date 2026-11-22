#### name: "young-male-participation-and-non-participation-yardstick"
description: "Measure future societal productivity, entrepreneurial pipeline depth, and sovereign growth potential through the active participation versus total incapacitation rate of men aged 20–29: separating productive tertiary/vocational/military/entry-level employment from youth unemployment, NEET exclusion, and deep structural incapacitation (incarceration, unexpunged criminal registries, work disabilities, substance addiction, APA/ICD-10 withdrawing/self-destructive/antisocial clinical morbidity, and untaxed grey-market opt-out)."

#### Young Male Participation & Non-Participation Yardstick (Ages 20–29)

You are reading the tick against the **structural economic participation
and incapacitation balance of men aged 20–29**. In Gary S. Becker's
*Human Capital* (1964), William Julius Wilson's *When Work Disappears*
(1996), Robert J. Sampson and John H. Laub's *Crime in the Making*
(1993), Nicholas Eberstadt's *Men Without Work* (2016), and the
American Psychiatric Association's *Diagnostic and Statistical Manual of
Mental Disorders* (*DSM-5-TR* / *ICD-10* Chapter V clinical classifications),
the 20–29 male cohort constitutes the primary developmental reservoir
of future entrepreneurial ventures, skilled technical trades, military
and civil defense readiness, and long-run total-factor productivity. 

Men in this decade are normally distributed across four constructive
channels: **accredited tertiary education**, **vocational specialist
training**, **military or civil service training and junior ranks**, and
**entry-level productive employment** where early-stage commercial ideas
germinate into future growth industries. When large fractions of this
cohort fall out of those channels—not merely into temporary job search,
but into **cumulative structural incapacitation**—official headline GDP
and credential-enrollment statistics mask an oncoming decade of
entrepreneurial stagnation, tax-base erosion, and sovereign fiscal strain. 

Your job is to classify the 20–29 male participation regime into one of
four states and cap your delta on domestic sovereign, consumer, and
long-horizon growth exposure accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute the three quantitative readings from
snapshot.external_data["young_male_participation"]. Use the
qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes national labor-force surveys, education/conscription
registries, justice/criminal-record statistics, disability/clinical
morbidity registries, and shadow-economy estimates for **males aged
20–29** into snapshot.external_data["young_male_participation"]: 

* male_20_29_active_participation_pct: percentage (0.0 to 100.0)
of men aged 20–29 actively engaged in **formal payroll employment**,
**accredited tertiary/vocational skill completion** (adjusted for
non-completion/credential parking), or **active military/civil
service**.
* male_20_29_neet_unemployment_pct: percentage (0.0 to 60.0) of
men aged 20–29 classified as **unemployed** (ILO definition) or
**NEET** (Not in Employment, Education, or Training).
* male_20_29_total_incapacitation_pct: percentage (0.0 to 50.0) of
men aged 20–29 removed from formal tax-paying and business-forming
activity across five cumulative exclusion channels: 

  1. **Active Incarceration & Custodial Supervision** (prisons, remand,
probation).
  2. **Unexpunged Criminal Registries** (active criminal-record flags
blocking security clearances, licensed trades, corporate
directorships, and formal credit).
  3. **Work Disability & Substance Addiction** (early disability
pensions, alcohol/opioid/stimulant dependence under *ICD-10*
F10–F19 / *DSM-5-TR* Substance Use Disorders).
  4. **Clinical Withdrawing, Self-Destructive & Antisocial Morbidity**
(severe social withdrawal/hikikomori syndrome, major depressive/anxiety
incapacitation, self-harm/suicidality, and Antisocial Personality
Disorder / persistent conduct pathology classified under *APA
DSM-5-TR* and *ICD-10* F20–F39, F60.2, F90–F98).
  5. **Grey-Market & Informal Opt-Out** (working-age men detached from
formal tax registries into untaxed cash/grey-economy subsistence
yielding zero fiscal revenue).
* consecutive_incapacitation_years: integer (0 to 20) counting
consecutive annual readings in which male_20_29_total_incapacitation_pct
increased or male_20_29_neet_unemployment_pct remained above its
structural warning threshold.

If snapshot.external_data["young_male_participation"] is absent or
empty, treat the jurisdiction as **unmonitored**, record state
**PRODUCTIVE_COHORT_EXPANSION**, note that no 20–29 male participation
telemetry was available, and do not cite this skill. 

#### Reading 1 — Active Productive Participation (male_20_29_active_participation_pct)

Evaluate the share of men aged 20–29 building human capital, serving in
national defense/civil infrastructure, or working in formal entry-level
and technical roles: 

male_20_29_active_participation_pctActive Participation Tier
**>= 84.0%**
**robust_human_capital_formation** — deep entry-level, vocational, tertiary, and service pipeline
**76.0% to 83.9%**
**moderate_participation** — functional pipeline with localized friction
**68.0% to 75.9%**
**eroding_male_pipeline** — thinning entry-level and specialist formation
**< 68.0%**
**severe_cohort_hollowing** — critical loss of prime-age male productive capacity

If male_20_29_active_participation_pct is missing, treat as
**eroding_male_pipeline**. 

#### Reading 2 — Surface Economic Exclusion (male_20_29_neet_unemployment_pct)

Evaluate acute labor-market and training lockout among men aged 20–29: 

male_20_29_neet_unemployment_pctExclusion Tier
**< 9.0%**
**tight_absorption** — rapid transition from school/service into formal employment
**9.0% to 14.9%**
**elevated_youth_friction** — measurable bottleneck in entry-level hiring
**15.0% to 21.9%**
**acute_neet_lockout** — widespread idleness and stalled career launch
**>= 22.0%**
**systemic_youth_exclusion** — mass detachment of young men from formal work and training

If male_20_29_neet_unemployment_pct is missing, treat as
**elevated_youth_friction**. 

#### Reading 3 — Deep Structural Incapacitation (male_20_29_total_incapacitation_pct)

Evaluate the share of men aged 20–29 locked out by incarceration,
unexpunged criminal records, disability/addiction, APA/ICD-10
withdrawing/self-destructive/antisocial clinical morbidity, or untaxed
grey-market opt-out: 

male_20_29_total_incapacitation_pctStructural Incapacitation Tier
**< 6.0%**
**contained_incapacitation** — low carceral, clinical, and grey-market leakage
**6.0% to 10.9%**
**creeping_incapacitation** — rising disability, addiction, or informal-sector drift
**11.0% to 16.9%**
**entrenched_cohort_scarring** — heavy criminal-registry, clinical, and shadow-economy overhang
**>= 17.0%**
**terminal_cohort_incapacitation** — severe permanent loss of tax-paying and entrepreneurial men

If male_20_29_total_incapacitation_pct is missing, treat as
**creeping_incapacitation**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four macro-sociological productivity
regimes. Evaluate in strict priority order and select the first regime
whose conditions are fully satisfied: 

1. **TERMINAL_COHORT_INCAPACITATION** (most severe)
2. **ENTRENCHED_NEET_AND_SCARRING**
3. **ERODING_ENTRY_PIPELINE**
4. **PRODUCTIVE_COHORT_EXPANSION** (strictest adaptive fit)

#### TERMINAL_COHORT_INCAPACITATION

Any of the following hold: 

* Structural Incapacitation Tier is **terminal_cohort_incapacitation**
(>= 17.0%).
* Active Participation Tier is **severe_cohort_hollowing** (< 68.0%)
AND Exclusion Tier is **systemic_youth_exclusion** (>= 22.0%).

**Delta cap: 0.15.** A massive share of men aged 20–29 is locked out by
incarceration, unexpunged criminal records, disability/addiction,
APA/ICD-10 withdrawing/antisocial pathology, or grey-market opt-out.
Future business formation and tax-base solvency are severely impaired.
Restrict long domestic growth exposure sharply. 

#### ENTRENCHED_NEET_AND_SCARRING

Any of the following hold (and TERMINAL_COHORT_INCAPACITATION does
not apply): 

* Structural Incapacitation Tier is **entrenched_cohort_scarring**
(11.0% to 16.9%).
* Exclusion Tier is **acute_neet_lockout** or
**systemic_youth_exclusion** (>= 15.0%).
* Active Participation Tier is **severe_cohort_hollowing** (< 68.0%).

**Delta cap: 0.40.** High NEET rates, criminal-record barriers, clinical
withdrawal, and informal-economy leakage are starving future growth
industries of founders and skilled technical labor. Cut sizing
substantially. 

#### ERODING_ENTRY_PIPELINE

Any of the following hold (and neither TERMINAL_COHORT_INCAPACITATION
nor ENTRENCHED_NEET_AND_SCARRING applies): 

* Active Participation Tier is **eroding_male_pipeline** (68.0% to 75.9%).
* Exclusion Tier is **elevated_youth_friction** (9.0% to 14.9%).
* Structural Incapacitation Tier is **creeping_incapacitation**
(6.0% to 10.9%).

**Delta cap: 0.70.** Early warning signs of entry-level hiring friction,
rising disability/addiction claims, or informal-sector drift. Trim
sizing relative to PRODUCTIVE_COHORT_EXPANSION. 

#### PRODUCTIVE_COHORT_EXPANSION

All of the following hold: 

* Active Participation Tier is **robust_human_capital_formation**
(>= 84.0%).
• Exclusion Tier is tight_absorption (< 9.0%).
• Structural Incapacitation Tier is contained_incapacitation
(< 6.0%).
Delta cap: 1.0. Men aged 20–29 are actively compounding skills across
tertiary/vocational programs, military/civil service, and formal
entry-level enterprises with minimal carceral, clinical, or
grey-market leakage. The cap equals the strategy cap; the skill never
binds on PRODUCTIVE_COHORT_EXPANSION.

Ambiguous fallback

Any combination not covered above is classified
ERODING_ENTRY_PIPELINE with delta cap 0.70.

Secondary Filter / Asymmetric Gate — Cumulative Cohort Scarring Persistence

Apply the persistence test after regime classification and before the
cap.
Cohort incapacitation is structurally scarring if
consecutive_incapacitation_years >= 3 (three or more consecutive
annual readings of rising total incapacitation or persistent NEET
lockout). Per Sampson & Laub's cumulative disadvantage theory, three
years of exclusion during ages 20–29 permanently damages lifetime
earnings, creditworthiness, and entrepreneurial formation.
If the condition is structurally scarring, halve the regime's
delta cap:
• ERODING_ENTRY_PIPELINE cap of 0.70 becomes 0.35.
• ENTRENCHED_NEET_AND_SCARRING cap of 0.40 becomes 0.20.
• TERMINAL_COHORT_INCAPACITATION cap of 0.15 becomes 0.075.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read young male participation dict. From
snapshot.external_data["young_male_participation"], load
male_20_29_active_participation_pct,
male_20_29_neet_unemployment_pct,
male_20_29_total_incapacitation_pct, and
consecutive_incapacitation_years. If absent or empty, record
PRODUCTIVE_COHORT_EXPANSION, note the omission, and do not cite
this skill.
2. Classify active participation tier. Apply Reading 1.
3. Classify surface NEET/unemployment tier. Apply Reading 2.
4. Classify deep structural incapacitation tier. Apply Reading 3
(incarceration, unexpunged criminal registries, disability/addiction,
APA/ICD-10 withdrawing/self-destructive/antisocial clinical morbidity,
and untaxed grey-market opt-out).
5. Classify regime. Evaluate in strict priority order
(TERMINAL_COHORT_INCAPACITATION → ENTRENCHED_NEET_AND_SCARRING
→ ERODING_ENTRY_PIPELINE → PRODUCTIVE_COHORT_EXPANSION)
(fallback: ERODING_ENTRY_PIPELINE).
6. Apply persistence test. If
consecutive_incapacitation_years >= 3, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"young-male-participation-and-non-participation-yardstick" in
skills_cited and state the active participation rate, NEET/unemployment
rate, total incapacitation rate, and persistence years in the
rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.4, "confidence": 0.78, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"ENTRENCHED_NEET_AND_SCARRING regime; male_20_29_active_participation_pct=71.2%, male_20_29_neet_unemployment_pct=16.8%, male_20_29_total_incapacitation_pct=12.4%, consecutive_incapacitation_years=4 (scarring persistence halves cap from 0.40 to 0.20); capping delta at 0.20; young-male-participation-and-non-participation-yardstick."
• skills_cited: list of skill names; include
"young-male-participation-and-non-participation-yardstick" only when
the cap bound (intended delta > delta_cap).

Worked Examples


Case A — High active participation, low NEET, contained incapacitation, cap does not bind

Snapshot:
• male_20_29_active_participation_pct = 86.5
• male_20_29_neet_unemployment_pct = 7.4
• male_20_29_total_incapacitation_pct = 4.8
• consecutive_incapacitation_years = 0
Readings:
• Active Participation Tier: robust_human_capital_formation
• Exclusion Tier: tight_absorption
• Structural Incapacitation Tier: contained_incapacitation
Regime: PRODUCTIVE_COHORT_EXPANSION, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.80. Cap 1.0 does not bind.
LLM returns delta = 0.80 and does not cite "young-male-participation-and-non-participation-yardstick".

Case B — Rising NEET and creeping disability/grey-market drift for 3 consecutive years, persistence halves cap

Snapshot:
• male_20_29_active_participation_pct = 73.5
• male_20_29_neet_unemployment_pct = 13.2
• male_20_29_total_incapacitation_pct = 9.4
• consecutive_incapacitation_years = 3
Readings:
• Active Participation Tier: eroding_male_pipeline
• Exclusion Tier: elevated_youth_friction
• Structural Incapacitation Tier: creeping_incapacitation
Regime: ERODING_ENTRY_PIPELINE, base cap 0.70. Persistence: 3 >= 3 → fires, halving cap to 0.35.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.35 binds.
LLM returns delta = 0.35 and cites "young-male-participation-and-non-participation-yardstick".

Case C — Entrenched NEET lockout + criminal-registry/clinical/grey-market scarring over 4 years

Snapshot:
• male_20_29_active_participation_pct = 69.0
• male_20_29_neet_unemployment_pct = 17.5
• male_20_29_total_incapacitation_pct = 13.8
• consecutive_incapacitation_years = 4
Readings:
• Active Participation Tier: eroding_male_pipeline
• Exclusion Tier: acute_neet_lockout
• Structural Incapacitation Tier: entrenched_cohort_scarring
Regime: ENTRENCHED_NEET_AND_SCARRING, base cap 0.40. Persistence: 4 >= 3 → fires, halving cap to 0.20.
AGOP ranks LONG. LLM intended delta = 0.75. Cap 0.20 binds.
LLM returns delta = 0.20 and cites "young-male-participation-and-non-participation-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["young_male_participation"]
from the following free, open national and international statistical
registries:
• Statistics Finland (Tilastokeskus StatFin) Open API:
https://stat.fi (free JSON-stat API for Labour Force Survey
employment/unemployment by sex and 5-year age group 20–24 and
25–29, educational attainment/completion, justice/prison/criminal-record
statistics, and Kela/ETK early work-disability pension awards).
• Eurostat & ILOSTAT Free Statistical APIs:
https://europa.eu and https://ilo.org (free
REST endpoints for harmonised NEET rates edat_lfse_20, youth
unemployment une_rt_a, and informal-economy indicators).
• Finnish Institute for Health and Welfare (THL Sotkanet) & WHO Global Health Observatory:
https://sotkanet.fi and https://who.int (free REST APIs for
substance-use and psychiatric morbidity incidence by age/sex under
ICD-10 Chapter V / APA DSM-5-TR categories).
• OECD & World Bank Open Data APIs:
https://oecd.org and https://worldbank.org (cross-country
youth labor-force participation and shadow-economy benchmarks).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not conflate passive university enrollment without degree/skill
completion with productive human-capital formation when NEET or
incapacitation metrics are rising.
• Do not omit unexpunged criminal-registry exclusions, APA/ICD-10
withdrawing/self-destructive/antisocial clinical morbidity, or
untaxed grey-market opt-out when evaluating total male incapacitation.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "young-male-participation-and-non-participation-yardstick"
when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Human Capital, Entrepreneurial Formation & Labor Attachment:
Gary S. Becker, Human Capital: A Theoretical and Empirical Analysis
(University of Chicago Press, 1964); William Julius Wilson, When Work
Disappears: The World of the New Urban Poor (Knopf, 1996); Nicholas
Eberstadt, Men Without Work: America's Invisible Crisis (Templeton
Press, 2016).
• Life-Course Criminology, Cumulative Disadvantage & Registry Scarring:
Robert J. Sampson & John H. Laub, Crime in the Making: Pathways and
Turning Points Through Life (Harvard University Press, 1993); Devah
Pager, Marked: Race, Crime, and Finding Work in an Era of Mass
Incarceration (University of Chicago Press, 2007).
• Clinical Taxonomy of Withdrawing, Self-Destructive & Antisocial Morbidity:
American Psychiatric Association, Diagnostic and Statistical Manual of
Mental Disorders, Fifth Edition, Text Revision (DSM-5-TR, 2022);
World Health Organization, International Statistical Classification of
Diseases and Related Health Problems, 10th Revision (ICD-10 Chapter
V: Mental and Behavioural Disorders F10–F99).
• Bounded Supervisory Control: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.