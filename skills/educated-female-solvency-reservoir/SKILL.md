#### name: "educated-female-solvency-reservoir"
description: "Measure the latent solvent maternal reservoir: childless women holding at least a Bachelor's degree (ISCED 6+) or currently enrolled in ISCED 6+ tertiary education whose equivalized income stands at least one-third (>= 1.333x) above their country of residence's national poverty threshold, using free global microdata and education/income registries (Eurostat EU-SILC, IPUMS International, U.S. Census SIPP/CPS, LIS, UNESCO UIS, OECD Education at a Glance, Statistics Finland); distinguish latent demographic rebound optionality from structural credential-trap depletion."

#### Educated Female Solvency Reservoir (ISCED 6+ Latent Maternal Pool)

You are reading the tick against the **latent solvent maternal reservoir**
of the target polity—specifically isolating **childless women who hold
at least a Bachelor's degree (ISCED 6 or above) or are actively
enrolled in ISCED 6+ tertiary education, AND whose equivalized
income already sits at least one-third (≥ 1.333×) above their country
of residence's official poverty threshold**. 

In Gary S. Becker's *A Treatise on the Family* (1981), Claudia Goldin's
*Career and Family* (2021), Randall Collins's *The Credential Society*
(1979), and Richard A. Easterlin's *Birth and Fortune* (1980), pairing
this **latent reservoir gate** with societal-vitality-yardstick
(20–29 realized above-poverty mothers) resolves a critical ambiguity
in demographic and domestic-demand underwriting: 

1. **Latent Rebound Optionality (ABUNDANT_LATENT_RESERVOIR):** If a
country exhibits low realized births in the 20–29 window
(societal-vitality-yardstick) *solely* because university credential
pipelines (institutional-sclerosis-yardstick) delay family start
dates, **while a large pool of childless ISCED 6+ women already
commands ≥ 1.333× national poverty income**, the society still
possesses an intact, solvent human-capital reservoir capable of
rapid family formation once housing or tax wedges ease.
2. **Credential-Trap Depletion (RESERVOIR_DEPLETED):** Conversely,
when degree inflation forces women through years of unpaid or
low-stipend tertiary education and precarious early careers **below
the ≥ 1.333× national poverty buffer**, the educated cohort has
neither realized offspring nor the material solvency to raise them—confirming
a deep structural contraction across both realized and latent
reproductive capacity.

Marital and cohabitation status are strictly excluded; only **female
sex**, **zero current biological/adopted offspring (childless_status)**,
**educational attainment or active enrollment at ISCED 6 (BSc) or
above**, and **equivalized income ≥ 1.333× the national poverty line**
are evaluated. 

Your job is to classify the polity's latent educated maternal reservoir
into one of four states and cap your delta accordingly. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise delta
above the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["educated_female_reservoir"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes harmonized household income microdata, labor-force
surveys, and tertiary-enrollment registries into
snapshot.external_data["educated_female_reservoir"]: 

* solvent_childless_bsc_plus_share_pct: percentage (0.0 to 100.0)
of all childless women aged 18–39 who hold ISCED 6+ (BSc or above)
OR are actively enrolled in ISCED 6+ education **AND** live in a
household with equivalized disposable income **≥ 1.333× the national
poverty threshold** (≥ 28% = deep solvent educated reservoir;
< 10% = acute credential-poverty squeeze).
* bsc_cohort_poverty_clearance_pct: percentage (0.0 to 100.0) of
all childless ISCED 6+ (graduated or enrolled) women whose income
clears the ≥ 1.333× national poverty buffer (≥ 75% = degree/study
translates reliably into immediate material solvency; < 45% =
severe student/graduate impoverishment where higher education fails
to clear 1.333× poverty).
* enrolled_vs_graduated_solvency_gap_pp: percentage-point drop (0.0
to 60.0) in ≥ 1.333× poverty clearance between graduated ISCED 6+
childless women and currently enrolled ISCED 6+ female students
(< 18 pp = low student poverty drag / paid apprenticeships;
> 38 pp = severe student-stipend poverty trap delaying family
formation).
* consecutive_reservoir_erosion_years: consecutive calendar years in
which solvent_childless_bsc_plus_share_pct OR
bsc_cohort_poverty_clearance_pct has declined monotonically.

If snapshot.external_data["educated_female_reservoir"] is absent or
empty, treat the instrument as **unmonitored**, record state
**ABUNDANT_LATENT_RESERVOIR**, note that no educated-reservoir
telemetry was available, and do not cite this skill. 

#### Reading 1 — Solvent Childless ISCED 6+ Reservoir Share (solvent_childless_bsc_plus_share_pct)

Evaluate the size of the childless ISCED 6+ (graduated or enrolled)
female pool already clearing ≥ 1.333× national poverty: 

solvent_childless_bsc_plus_share_pctLatent Reservoir Tier
**≥ 28.0%**
**deep_reservoir** — large pool of educated childless women with ≥ 1.333× poverty means
**18.0% to 28.0%**
**moderate_reservoir** — viable educated pool, constrained by career/housing entry lag
**10.0% to 18.0%**
**thin_reservoir** — narrow slice of educated childless women clears 1.333× poverty
**< 10.0%**
**depleted_reservoir** — near-absence of solvent childless ISCED 6+ potential mothers

If solvent_childless_bsc_plus_share_pct is missing, treat as
**moderate_reservoir**. 

#### Reading 2 — ISCED 6+ Cohort Poverty Clearance (bsc_cohort_poverty_clearance_pct)

Evaluate whether holding or pursuing a BSc+ actually provides the
material means (≥ 1.333× poverty) to raise a child: 

bsc_cohort_poverty_clearance_pctCredential Solvency Tier
**≥ 75.0%**
**solvent_credential** — ISCED 6+ women reliably command ≥ 1.333× poverty income
**60.0% to 75.0%**
**friction_eroded** — high taxes/housing/entry wages erode 1.333× buffer for ~1 in 3
**45.0% to 60.0%**
**precarious_credential** — nearly half of childless ISCED 6+ women sit below 1.333× poverty
**< 45.0%**
**impoverished_credential** — tertiary education/early career traps women below 1.333× buffer

If bsc_cohort_poverty_clearance_pct is missing, treat as
**friction_eroded**. 

#### Reading 3 — Student-to-Graduate Solvency Wedge (enrolled_vs_graduated_solvency_gap_pp)

Evaluate how severely full-time university enrollment suppresses
solvency prior to graduation (institutional-sclerosis-yardstick drag): 

enrolled_vs_graduated_solvency_gap_ppEnrollment Drag Tier
**< 18.0 pp**
**smooth_transition** — paid internships/grants keep enrolled students near graduate solvency
**18.0 to 38.0 pp**
**moderate_study_wedge** — multi-year study period depresses income until late twenties
**> 38.0 pp**
**severe_stipend_trap** — prolonged university enrollment forces years of sub-poverty living

If enrolled_vs_graduated_solvency_gap_pp is missing, treat as
**moderate_study_wedge**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
latent-reservoir regimes. Evaluate in strict priority order and select
the first regime whose conditions are fully satisfied: 

1. **RESERVOIR_DEPLETED** (most severe — unconditional FLAT on long-horizon domestic growth)
2. **CREDENTIAL_POVERTY_TRAP**
3. **STIPEND_DELAYED_RESERVOIR**
4. **ABUNDANT_LATENT_RESERVOIR** (strictest adaptive fit)

#### RESERVOIR_DEPLETED

Any of the following hold: 

* Latent Reservoir Tier is **depleted_reservoir** (< 10.0%) AND
Credential Solvency Tier is **precarious_credential** or
**impoverished_credential** (< 60.0%).
* Credential Solvency Tier is **impoverished_credential** (< 45.0% of
childless ISCED 6+ women clearing ≥ 1.333× poverty).

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. Not only is realized 20–29 reproduction weak,
but even the educated, childless female cohort lacks the ≥ 1.333×
poverty income required to raise offspring—eliminating any latent
rebound buffer. The skill binds unconditionally and must appear in
skills_cited. 

#### CREDENTIAL_POVERTY_TRAP

Any of the following hold (and RESERVOIR_DEPLETED does not apply): 

* Latent Reservoir Tier is **depleted_reservoir** (< 10.0%) with
solvent_credential or friction_eroded.
* Latent Reservoir Tier is **thin_reservoir** (10.0% to 18.0%) AND
Credential Solvency Tier is **precarious_credential** (45.0% to 60.0%).
* Credential Solvency Tier is **precarious_credential** AND Enrollment
Drag Tier is **severe_stipend_trap** (> 38.0 pp).

**Delta cap: 0.25.** University credentialism and entry-level wage/tax
compression are pricing educated childless women out of the 1.333×
solvency floor. Cut domestic long exposure substantially. 

#### STIPEND_DELAYED_RESERVOIR

Any of the following hold (and neither RESERVOIR_DEPLETED nor
CREDENTIAL_POVERTY_TRAP applies): 

* Latent Reservoir Tier is **thin_reservoir** (10.0% to 18.0%) with
solvent_credential or friction_eroded.
* Latent Reservoir Tier is **moderate_reservoir** (18.0% to 28.0%)
AND (Credential Solvency Tier is **friction_eroded** OR Enrollment
Drag Tier is **severe_stipend_trap**).
* Enrollment Drag Tier is **severe_stipend_trap** (> 38.0 pp) with
deep_reservoir.

**Delta cap: 0.70.** Graduated ISCED 6+ women achieve solvency, but
prolonged university enrollment (severe_stipend_trap) delays career
start and pushes family formation out of the 20–29 window. Trim
sizing relative to ABUNDANT_LATENT_RESERVOIR.

ABUNDANT_LATENT_RESERVOIR

All of the following hold:
• Latent Reservoir Tier is deep_reservoir (≥ 28.0% of childless
women holding/pursuing ISCED 6+ at ≥ 1.333× national poverty).
• Credential Solvency Tier is solvent_credential (≥ 75.0%
clearing ≥ 1.333× poverty).
• Enrollment Drag Tier is smooth_transition or
moderate_study_wedge (≤ 38.0 pp).
Delta cap: 1.0. Deep, solvent educated female reservoir with
intact means (≥ 1.333× poverty) to raise healthy offspring—providing
genuine demographic rebound optionality. The cap equals the strategy
cap; the skill never binds on ABUNDANT_LATENT_RESERVOIR.

Ambiguous fallback

Any combination not covered above is classified CREDENTIAL_POVERTY_TRAP
with delta cap 0.25.

Secondary Filter / Asymmetric Gate — Multi-Year Reservoir Erosion Hysteresis

Apply the persistence test after regime classification and before the
cap.
Reservoir erosion is structurally entrenched if
consecutive_reservoir_erosion_years >= 4 (four or more consecutive
calendar years of declining solvent_childless_bsc_plus_share_pct or
bsc_cohort_poverty_clearance_pct). Four consecutive annual cohorts
of shrinking educated solvency confirms that structural wage compression,
housing inflation, or tax wedges are steadily eroding the ≥ 1.333×
buffer even among degree-holders.
If the erosion is structurally entrenched, halve the regime's
delta cap:
• STIPEND_DELAYED_RESERVOIR cap of 0.70 becomes 0.35.
• CREDENTIAL_POVERTY_TRAP cap of 0.25 becomes 0.125.
• RESERVOIR_DEPLETED cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read educated female reservoir dict. From
snapshot.external_data["educated_female_reservoir"], load
solvent_childless_bsc_plus_share_pct,
bsc_cohort_poverty_clearance_pct,
enrolled_vs_graduated_solvency_gap_pp, and
consecutive_reservoir_erosion_years. If absent or empty, record
ABUNDANT_LATENT_RESERVOIR, note the omission, and do not cite
this skill.
2. Classify latent reservoir tier. Apply Reading 1
(deep_reservoir, moderate_reservoir, thin_reservoir, or
depleted_reservoir).
3. Classify credential solvency tier. Apply Reading 2
(solvent_credential, friction_eroded, precarious_credential,
or impoverished_credential).
4. Classify enrollment drag tier. Apply Reading 3
(smooth_transition, moderate_study_wedge, or
severe_stipend_trap).
5. Classify regime. Evaluate in strict priority order
(RESERVOIR_DEPLETED → CREDENTIAL_POVERTY_TRAP →
STIPEND_DELAYED_RESERVOIR → ABUNDANT_LATENT_RESERVOIR) and
select the first matching regime (fallback: CREDENTIAL_POVERTY_TRAP).
6. Apply persistence test. If
consecutive_reservoir_erosion_years >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
regime is RESERVOIR_DEPLETED, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
regime is RESERVOIR_DEPLETED, cite
"educated-female-solvency-reservoir" in skills_cited and state
the childless ISCED 6+ >= 1.333x poverty clearance finding in the
rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If RESERVOIR_DEPLETED,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"CREDENTIAL_POVERTY_TRAP regime; solvent_childless_bsc_plus_share=14.2% (thin_reservoir) and bsc_cohort_poverty_clearance=54.0% (<60% precarious_credential) with 42 pp student stipend wedge; capping delta at 0.25; educated-female-solvency-reservoir."
• skills_cited: list of skill names; include
"educated-female-solvency-reservoir" only when the cap bound or
the regime is RESERVOIR_DEPLETED.

Worked Examples


Case A — Deep solvent childless BSc+ female reservoir clearing 1.333x poverty, cap does not bind

Snapshot:
• solvent_childless_bsc_plus_share_pct = 32.0
• bsc_cohort_poverty_clearance_pct = 81.0
• enrolled_vs_graduated_solvency_gap_pp = 15.0
• consecutive_reservoir_erosion_years = 0
Readings:
• Latent Reservoir Tier: ≥ 28.0% → deep_reservoir
• Credential Solvency Tier: ≥ 75.0% → solvent_credential
• Enrollment Drag Tier: < 18.0 pp → smooth_transition
Regime: ABUNDANT_LATENT_RESERVOIR, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "educated-female-solvency-reservoir".

Case B — Prolonged student stipend trap delaying solvent family start, cap binds

Snapshot:
• solvent_childless_bsc_plus_share_pct = 21.5
• bsc_cohort_poverty_clearance_pct = 66.0
• enrolled_vs_graduated_solvency_gap_pp = 43.0
• consecutive_reservoir_erosion_years = 5
Readings:
• Latent Reservoir Tier: 18.0% to 28.0% → moderate_reservoir
• Credential Solvency Tier: 60.0% to 75.0% → friction_eroded
• Enrollment Drag Tier: > 38.0 pp → severe_stipend_trap
Regime: STIPEND_DELAYED_RESERVOIR, delta cap 0.70.
Persistence: consecutive_reservoir_erosion_years = 5 >= 4 → halve to 0.35.
AGOP ranks LONG. LLM intended delta = 0.80. Cap 0.35 binds.
LLM returns delta = 0.35 and cites "educated-female-solvency-reservoir".

Case C — Depleted solvent educated female reservoir below 1.333x poverty, unconditional FLAT

Snapshot:
• solvent_childless_bsc_plus_share_pct = 8.4
• bsc_cohort_poverty_clearance_pct = 42.0
• enrolled_vs_graduated_solvency_gap_pp = 46.0
• consecutive_reservoir_erosion_years = 6
Readings:
• Latent Reservoir Tier: < 10.0% → depleted_reservoir
• Credential Solvency Tier: < 45.0% → impoverished_credential
• Enrollment Drag Tier: > 38.0 pp → severe_stipend_trap
Regime: RESERVOIR_DEPLETED, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "educated-female-solvency-reservoir".

Free Data Sources

The fetcher populates snapshot.external_data["educated_female_reservoir"]
from the following free, open global household income, education, and
fertility registries (no paid subscription required):

Global Harmonized Education & Income Panels

• Luxembourg Income Study (LIS) & World Bank Poverty and Inequality Platform (PIP):
https://lisdatacenter.org and https://worldbank.org (free
harmonized cross-national microdata filtering by female sex, zero
children in household, ISCED 6+ attainment/enrollment, and
equivalized income >= 1.333x national poverty threshold).
• IPUMS International & IPUMS CPS (Current Population Survey):
https://ipums.org (free harmonized global census and annual labor/income
microdata disaggregating childless women by BSc+ attainment/enrollment
and poverty-line multiple).
• UNESCO Institute for Statistics (UIS) & OECD Education at a Glance:
https://unesco.org and https://oecd.org (free REST/SDMX APIs
supplying female tertiary enrollment/attainment rates and earnings
by educational attainment globally).

Europe, North America & Global Regional Panels

• Eurostat EU-SILC, European Labour Force Survey (EU-LFS) & Statistics Finland (Tilastokeskus PxWeb):
https://europa.eu and https://stat.fi (free open microdata and
PxWeb tables cross-tabulating female education level, student status,
presence of children, and equivalized income >= 1.333x national
poverty line).
• U.S. Census Bureau SIPP & American Community Survey (ACS PUMS):
https://census.gov (free public microdata tracking childless women
enrolled in or holding a Bachelor's degree+ with household income-to-poverty
ratio >= 1.333x).
• CEPALSTAT (UN ECLAC), IBGE PNAD Contínua (Brazil) & India MoSPI PLFS:
https://cepal.org, https://ibge.gov.br, and https://mospi.gov.in
(free open household income and higher-education microdata across
Latin America and South Asia).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not condition on marital or cohabitation status; evaluate strictly
on female sex, zero current offspring, ISCED 6+ (BSc+) degree or
active enrollment, and equivalized income >= 1.333x national poverty.
• Do not double-count women who already have children (societal-vitality-yardstick
measures realized mothers; this skill measures the childless latent
reservoir).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "educated-female-solvency-reservoir" when the cap did
not bind and the regime is not RESERVOIR_DEPLETED.

Citation Mapping

• Household Economics & Human Capital Investment: Gary S. Becker,
A Treatise on the Family (Harvard University Press, 1981); Claudia
Goldin, Career and Family: Women's Century-Long Journey toward Equity
(Princeton University Press, 2021).
• Credential Inflation & Career-Entry Delay: Randall Collins, The
Credential Society (Academic Press, 1979).
• Cohort Relative Income & Family Formation: Richard A. Easterlin,
Birth and Fortune (Basic Books, 1980).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.