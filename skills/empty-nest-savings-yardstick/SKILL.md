#### name: "empty-nest-savings-yardstick"
description: "Measure pre-retirement capital formation capacity via the share of households aged 50–65 free of dependent children and their net savings-rate wedge relative to dependent-encumbered 50–65 peers, using free global household budget and aging panels (Eurostat HBS, Gateway to Global Aging HRS/SHARE/CHARLS/LASI, U.S. BLS CE, LIS, SCB, Statistics Finland); cap delta or force FLAT as delayed family formation cannibalizes peak-earning capital accumulation."

#### Empty-Nest Peak-Savings Yardstick (50–65 Capital Accumulation Window)

You are reading the tick against the **pre-retirement net capital
accumulation capacity** of households aged **50 to 65** in the target
polity or domestic equity/fixed-income base. In Franco Modigliani's
Life-Cycle Hypothesis (1954; Ando & Modigliani, 1963), Milton Friedman's
Permanent Income Hypothesis (1957), and Laurence Kotlikoff & Lawrence
Summers's intergenerational capital-accumulation framework (1981), ages
**50 to 65** represent the sole multi-decade window in the human life
cycle where **peak career earnings coincide with zero dependent children
in the household**. 

When a society's reproductive cohort delivers children at age 29 or
younger (societal-vitality-yardstick), those children reach legal
adulthood (age 18) by the time the parents hit **47–50**—unlocking a
full **15-year debt-free, dependent-free compounding window (50–65)**
that funds domestic equity investment, private pension buffers, and
infrastructure before 70+ frailty overhead begins
(older-adult-functional-capacity). Conversely, when first births slip
past age 30 into the mid-to-late thirties, dependent-child housing,
consumption, and education costs spill directly into the 50–65
window—compressing the household net savings rate (dependent_savings_drag)
and leaving the 65+ cohort under-capitalized and dependent on sovereign
deficit transfers. 

Keeping this gate independent of societal-vitality-yardstick allows
JANUS to separate **upstream generational renewal (20–29)** from
**current-generation capital formation (50–65)**: a country may
already suffer DEMOGRAPHIC_EXHAUSTION in its 20–29 cohort while
still enjoying a temporary 50–65 empty-nest savings dividend from
earlier cohorts—or it may suffer simultaneous collapse across both
windows. 

Your job is to classify the polity into one of four pre-retirement
savings regimes and cap your delta accordingly. You do not invent
trades. You do not override AGOP. You modulate the LLM's delta within
the bound the verifier already permits. You never raise delta above
the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["empty_nest_savings"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes age-cohort household budget surveys, national
accounts saving tables, and harmonized longitudinal aging panels into
snapshot.external_data["empty_nest_savings"]: 

* empty_nest_50_65_share_pct: percentage (0.0 to 100.0) of all
households headed by adults aged **50 to 65** that have **zero
financially dependent children** living in or supported by the
household (≥ 72% = intact empty-nest window; < 48% = severe
late-birth / "boomerang-dependent" overhang into pre-retirement).
* empty_nest_net_savings_rate_pct: net household savings rate
(-10.0 to +40.0, disposable income minus consumption expenditure
divided by disposable income) of **child-free 50–65 households**
(≥ 16% = strong pre-retirement capital compounding; < 5% =
consumption-bloated or tax-squeezed pre-retirees).
* dependent_savings_penalty_pp: percentage-point drop (0.0 to 30.0)
in net savings rate between empty-nest 50–65 households and
50–65 households still supporting dependent children (< 6 pp =
mild drag; > 14 pp = severe dependent consumption cannibalization).
* consecutive_savings_compression_years: consecutive calendar years
in which empty_nest_50_65_share_pct OR
empty_nest_net_savings_rate_pct has declined monotonically.

If snapshot.external_data["empty_nest_savings"] is absent or empty,
treat the instrument as **unmonitored**, record state
**PEAK_CAPITAL_COMPOUNDING**, note that no empty-nest savings telemetry
was available, and do not cite this skill. 

#### Reading 1 — Empty-Nest Cohort Share (empty_nest_50_65_share_pct)

Evaluate what proportion of the 50–65 peak-earning cohort is actually
free of dependent-child expenditure: 

empty_nest_50_65_share_pctCohort Liberation Tier
**≥ 72.0%**
**liberated_window** — vast majority of 50–65 cohort is dependent-free
**60.0% to 72.0%**
**partial_overhang** — delayed parenting encroaching into early fifties
**48.0% to 60.0%**
**extended_dependency** — nearly half of 50–65 households still funding dependents
**< 48.0%**
**perpetual_dependency** — structural loss of the empty-nest compounding window

If empty_nest_50_65_share_pct is missing, treat as **partial_overhang**. 

#### Reading 2 — Empty-Nest Net Savings Rate (empty_nest_net_savings_rate_pct)

Evaluate whether liberated 50–65 households are actually accumulating
investable net capital rather than consuming peak earnings: 

empty_nest_net_savings_rate_pctCapital Accumulation Tier
**≥ 16.0%**
**high_compounding** — robust surplus savings feeding domestic capital & pension buffers
**10.0% to 16.0%**
**moderate_accumulation** — steady savings buffer; sensitive to inflation/tax drag
**5.0% to 10.0%**
**thin_surplus** — high living/tax costs absorbing peak-earning headroom
**< 5.0%**
**savings_depletion** — zero net pre-retirement capital formation; sovereign transfer reliance

If empty_nest_net_savings_rate_pct is missing, treat as
**moderate_accumulation**. 

#### Reading 3 — Dependent-Child Savings Drag (dependent_savings_penalty_pp)

Evaluate how severely supporting dependents inside the 50–65 bracket
cannibalizes household savings relative to empty-nest peers: 

dependent_savings_penalty_ppDependent Drag Severity
**< 6.0 pp**
**contained_drag** — minor consumption wedge from remaining dependents
**6.0 to 14.0 pp**
**material_erosion** — dependent housing/education cuts pre-retirement savings in half
**> 14.0 pp**
**acute_cannibalization** — dependent expenses wipe out 50–65 surplus accumulation

If dependent_savings_penalty_pp is missing, treat as **material_erosion**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
pre-retirement savings regimes. Evaluate in strict priority order and
select the first regime whose conditions are fully satisfied: 

1. **CAPITAL_CANNIBALIZATION** (most severe — unconditional FLAT on long-duration domestic assets)
2. **SAVINGS_COMPRESSION**
3. **LATE_NEST_DRAG**
4. **PEAK_CAPITAL_COMPOUNDING** (strictest adaptive fit)

#### CAPITAL_CANNIBALIZATION

Any of the following hold: 

* Capital Accumulation Tier is **savings_depletion** (< 5.0% net
savings rate among empty-nest 50–65 households).
* Cohort Liberation Tier is **perpetual_dependency** (< 48.0%) AND
Capital Accumulation Tier is **thin_surplus** (5.0% to 10.0%).
* Cohort Liberation Tier is **extended_dependency** or
**perpetual_dependency** (< 60.0%) AND Dependent Drag Severity is
**acute_cannibalization** (> 14.0 pp).

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked on domestic long-duration equities, real estate, and
sovereign debt. The 50–65 cohort is failing to accumulate net capital
before entering 65+ retirement, guaranteeing rising fiscal deficits
and forced asset liquidation as cohorts age. The skill binds
unconditionally and must appear in skills_cited. 

#### SAVINGS_COMPRESSION

Any of the following hold (and CAPITAL_CANNIBALIZATION does not apply): 

* Capital Accumulation Tier is **thin_surplus** (5.0% to 10.0%).
* Cohort Liberation Tier is **perpetual_dependency** (< 48.0%) with
moderate_accumulation or high_compounding.
* Cohort Liberation Tier is **extended_dependency** (48.0% to 60.0%)
AND Dependent Drag Severity is **material_erosion** (6.0 to 14.0 pp).

**Delta cap: 0.25.** Peak-earning pre-retirement savings are heavily
compressed by late-child dependency or tax/cost wedges. Reduce domestic
long exposure substantially. 

#### LATE_NEST_DRAG

Any of the following hold (and neither CAPITAL_CANNIBALIZATION nor
SAVINGS_COMPRESSION applies): 

* Cohort Liberation Tier is **partial_overhang** (60.0% to 72.0%) or
**extended_dependency** (48.0% to 60.0%) with contained_drag.
* Capital Accumulation Tier is **moderate_accumulation** (10.0% to 16.0%).
* Dependent Drag Severity is **material_erosion** (6.0 to 14.0 pp).

**Delta cap: 0.70.** The empty-nest window is intact for most of the
cohort, but delayed family formation or moderate living-cost drag trims
aggregate domestic capital formation. Reduce size relative to
PEAK_CAPITAL_COMPOUNDING. 

#### PEAK_CAPITAL_COMPOUNDING

All of the following hold: 

* Cohort Liberation Tier is **liberated_window** (≥ 72.0% of 50–65
households free of dependent children).
* Capital Accumulation Tier is **high_compounding** (≥ 16.0% net
savings rate among empty-nest 50–65 households).
* Dependent Drag Severity is **contained_drag** (< 6.0 pp).

**Delta cap: 1.0.** Full 15-year 50–65 empty-nest compounding engine
active: peak-earning households generate deep domestic investment flows
and self-funded retirement buffers. The cap equals the strategy cap;
the skill never binds on PEAK_CAPITAL_COMPOUNDING. 

#### Ambiguous fallback

Any combination not covered above is classified **SAVINGS_COMPRESSION**
with delta cap 0.25.

Secondary Filter / Asymmetric Gate — Multi-Year Savings Erosion Hysteresis

Apply the persistence test after regime classification and before the
cap.
Pre-retirement capital erosion is structurally entrenched if
consecutive_savings_compression_years >= 4 (four or more consecutive
calendar years of declining empty_nest_50_65_share_pct or
empty_nest_net_savings_rate_pct). Four consecutive years of shrinking
empty-nest share or falling net savings proves that late-birth
dependency overhang and structural tax/cost wedges are steadily eroding
national capital formation.
If the compression is structurally entrenched, halve the regime's
delta cap:
• LATE_NEST_DRAG cap of 0.70 becomes 0.35.
• SAVINGS_COMPRESSION cap of 0.25 becomes 0.125.
• CAPITAL_CANNIBALIZATION cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read empty-nest savings dict. From
snapshot.external_data["empty_nest_savings"], load
empty_nest_50_65_share_pct, empty_nest_net_savings_rate_pct,
dependent_savings_penalty_pp, and
consecutive_savings_compression_years. If absent or empty, record
PEAK_CAPITAL_COMPOUNDING, note the omission, and do not cite
this skill.
2. Classify cohort liberation tier. Apply Reading 1
(liberated_window, partial_overhang, extended_dependency, or
perpetual_dependency).
3. Classify capital accumulation tier. Apply Reading 2
(high_compounding, moderate_accumulation, thin_surplus, or
savings_depletion).
4. Classify dependent drag severity. Apply Reading 3
(contained_drag, material_erosion, or acute_cannibalization).
5. Classify regime. Evaluate in strict priority order
(CAPITAL_CANNIBALIZATION → SAVINGS_COMPRESSION →
LATE_NEST_DRAG → PEAK_CAPITAL_COMPOUNDING) and select the first
matching regime (fallback: SAVINGS_COMPRESSION).
6. Apply persistence test. If
consecutive_savings_compression_years >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
regime is CAPITAL_CANNIBALIZATION, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
regime is CAPITAL_CANNIBALIZATION, cite
"empty-nest-savings-yardstick" in skills_cited and state the
50–65 empty-nest share and net savings finding in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If CAPITAL_CANNIBALIZATION,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"CAPITAL_CANNIBALIZATION regime; empty_nest_50_65_share=54.0% (extended_dependency) with 16.5 pp dependent_savings_penalty and 4.2% net savings rate; forcing action=FLAT; empty-nest-savings-yardstick."
• skills_cited: list of skill names; include
"empty-nest-savings-yardstick" only when the cap bound or the
regime is CAPITAL_CANNIBALIZATION.

Worked Examples


Case A — Liberated 50–65 empty-nest cohort with high net savings rate, cap does not bind

Snapshot:
• empty_nest_50_65_share_pct = 76.0
• empty_nest_net_savings_rate_pct = 18.5
• dependent_savings_penalty_pp = 4.5
• consecutive_savings_compression_years = 0
Readings:
• Cohort Liberation Tier: ≥ 72.0% → liberated_window
• Capital Accumulation Tier: ≥ 16.0% → high_compounding
• Dependent Drag Severity: < 6.0 pp → contained_drag
Regime: PEAK_CAPITAL_COMPOUNDING, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "empty-nest-savings-yardstick".

Case B — Extended dependent overhang into 50–65 window over 5 declining years, cap binds

Snapshot:
• empty_nest_50_65_share_pct = 56.0
• empty_nest_net_savings_rate_pct = 11.5
• dependent_savings_penalty_pp = 10.5
• consecutive_savings_compression_years = 5
Readings:
• Cohort Liberation Tier: 48.0% to 60.0% → extended_dependency
• Capital Accumulation Tier: 10.0% to 16.0% → moderate_accumulation
• Dependent Drag Severity: 6.0 to 14.0 pp → material_erosion
Regime: SAVINGS_COMPRESSION, delta cap 0.25.
Persistence: consecutive_savings_compression_years = 5 >= 4 → halve to 0.125.
AGOP ranks LONG. LLM intended delta = 0.75. Cap 0.125 binds.
LLM returns delta = 0.125 and cites "empty-nest-savings-yardstick".

Case C — Empty-nest net savings depleted below 5%, unconditional FLAT

Snapshot:
• empty_nest_50_65_share_pct = 52.0
• empty_nest_net_savings_rate_pct = 3.8
• dependent_savings_penalty_pp = 15.2
• consecutive_savings_compression_years = 6
Readings:
• Cohort Liberation Tier: 48.0% to 60.0% → extended_dependency
• Capital Accumulation Tier: < 5.0% → savings_depletion
• Dependent Drag Severity: > 14.0 pp → acute_cannibalization
Regime: CAPITAL_CANNIBALIZATION, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "empty-nest-savings-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["empty_nest_savings"]
from the following free, open global household consumption/savings
surveys and harmonized longitudinal aging panels (no paid subscription
required):

Global Harmonized Aging & Household Savings Panels

• Gateway to Global Aging Data (g2aging.org — HRS, SHARE, ELSA, CHARLS, LASI, JSTAR, MHAS):
https://g2aging.org (free harmonized longitudinal microdata
measuring 50–65 household net savings, financial wealth, and
dependent-child consumption drag across North America, Europe, China,
India, Japan, South Korea, Mexico, and South Africa).
• Luxembourg Income Study (LIS) & Luxembourg Wealth Study (LWS):
https://lisdatacenter.org (free harmonized cross-national income,
consumption, and net-worth microdata disaggregated by household head
age 50–65 and presence of dependent children).
• OECD National Accounts & Household Dashboard (Stats.OECD):
https://oecd.org (free SDMX/REST API supplying
household net saving rates and age-group saving ratios across OECD
economies).

Europe & Nordic Household Budget Registries

• Eurostat Household Budget Survey (HBS) & EU-SILC:
https://europa.eu (free quinquennial/annual consumption expenditure
and disposable income tables by age of reference person 45–59 /
60+ and household composition with vs. without dependent children).
• Statistics Finland (Tilastokeskus PxWeb — Household Budget & Wealth Surveys):
https://stat.fi (free open PxWeb tables comparing disposable
income, consumption expenditure, and net savings by household stage
and age bracket).
• Statistics Sweden (SCB Open Data) & Statistics Norway (SSB PxWeb):
https://scb.se and https://ssb.no (free open APIs for household
saving rates, consumption by household composition, and wealth by age).

North America, Asia-Pacific, Africa & Latin America

• U.S. Bureau of Labor Statistics (BLS) Consumer Expenditure Survey (CE) & Federal Reserve SCF:
https://bls.gov and https://federalreserve.gov (free public
tables and microdata comparing 45–54 and 55–64 income after taxes,
total expenditure, and net savings with vs. without children).
• Statistics Bureau of Japan (FIES), Korea KOSIS (HIES) & India MoSPI HCES:
https://stat.go.jp, https://kosis.kr, and https://mospi.gov.in
(free open household income-and-expenditure survey tables broken down
by householder age 50–65 and dependent household members).
• INEGI ENIGH (Mexico), IBGE POF (Brazil) & Statistics South Africa (Stats SA IES):
https://inegi.org.mx, https://ibge.gov.br, and https://statssa.gov.za
(free open household income and expenditure surveys measuring 50–65
savings compression across Latin America and Southern Africa).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not conflate gross pension contributions with voluntary household
net savings (empty_nest_net_savings_rate_pct) when disposable-income
savings data is available.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "empty-nest-savings-yardstick" when the cap did not bind
and the regime is not CAPITAL_CANNIBALIZATION.

Citation Mapping

• Life-Cycle Savings & Pre-Retirement Accumulation: Franco Modigliani
and Richard Brumberg, "Utility Analysis and the Consumption Function,"
in Post-Keynesian Economics (Rutgers University Press, 1954); Albert
Ando and Franco Modigliani, "The 'Life Cycle' Hypothesis of Saving,"
American Economic Review 53(1), 55–84 (1963).
• Permanent Income & Consumption Smoothing: Milton Friedman, A
Theory of the Consumption Function (Princeton University Press, 1957).
• Intergenerational Transfers & Capital Formation: Laurence J.
Kotlikoff and Lawrence H. Summers, "The Role of Intergenerational
Transfers in Aggregate Capital Accumulation," Journal of Political
Economy 89(4), 706–732 (1981).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
