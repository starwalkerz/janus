#### name: "clique-shibboleth-pendulum"
description: "Track the civilizational pendulum between open material-utilitarian meritocracy and arbitrary clique-shibboleth hoarding (isomorphic across linguistic markers such as Queen's English, Classical Arabic, Mandarin etiquette, German/French elite trivia, or phenotype/colorism) by querying KAIROS (:8300) cyclic baseline & null-space anomaly telemetry alongside free global social-mobility, linguistic-monopoly, and consumption registries (World Bank, UNESCO UIS, ILOSTAT, WVS, Eurostat, LIS); cap delta or force FLAT when shibboleth screening displaces productive merit."

#### Clique-Shibboleth & Materialism Pendulum (KAIROS Cyclic Regime Gate)

You are reading the tick against the **recurring socio-economic pendulum
between open material-utilitarian output and closed clique-shibboleth
hoarding**. In Pitirim A. Sorokin's *Social and Cultural Dynamics*
(1937–1941), Vilfredo Pareto's *The Mind and Society* (1916), Pierre
Bourdieu's *Distinction* (1979) and *Language and Symbolic Power*
(1991), Charles Tilly's *Durable Inequality* (1998), and Paul Fussell's
*Class* (1983), societies oscillate cyclically between two structural
poles: 

1. **Material-Utilitarian Phase (Sensate / Open Merit):** Status,
capital allocation, and leadership selection are governed by
verifiable physical production, engineering competence, and
material results. Barriers to entry are low, and diverse talent
compounds rapidly.
2. **Clique-Shibboleth Hoarding Phase (Categorical Opportunity Hoarding):**
As incumbents seek to lock in rents without competing on material
output, they erect **arbitrary, non-productive cultural shibboleths**
as gatekeeping filters. The surface marker varies by geography and
era—Yellow River court etiquette and Mandarin register in imperial
China, German/French philosophical and hobby trivia in Western Europe,
Queen's English accent and boarding-school codes in mid-century
Five Eyes elites, Classical Arabic register in Sunni hubs, or
phenotype/colorism in stratified post-colonial enclaves—but **the
underlying graph topology is 100% invariant**: an incumbent clique
hoards institutional opportunities (Tilly) by taxing outsiders on
arbitrary symbolic capital (Bourdieu).

Because this oscillation is a **multi-decade cyclic process**, JANUS
queries **KAIROS (:8300)** directly—using KAIROS's cyclic baseline
subtraction and Bayes-threshold null-space anomaly detector to measure
where the target economy sits on the **Materialism ↔ Shibboleth
Pendulum** and whether arbitrary clique-screening has decoupled from
real productivity growth. 

Your job is to classify the polity's pendulum phase into one of four
regimes and cap your delta accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["shibboleth_pendulum"]
(populated by querying KAIROS :8300 over free mobility, linguistic,
and consumption baseline series). Use the qualitative tables below. Do
not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher queries KAIROS (:8300) alongside open socio-economic
registries and normalizes the cyclic state into
snapshot.external_data["shibboleth_pendulum"]: 

* kairos_pendulum_phase: cyclic regime classification returned by
KAIROS (:8300) after seasonal/generational baseline subtraction:
"material_merit_expansion" (rising phase; productive output and
material innovation dominate status allocation),
"mid_cycle_drift" (mixed equilibrium; early prestige signaling
appearing alongside material growth),
"shibboleth_hoarding_peak" (late ossified phase; linguistic,
etiquette, ancestry, or trivia shibboleths dominate hiring, credit,
and state contracts), or
"clique_rupture_inflection" (pendulum snapping back via institutional
crisis, capital flight, or disruptive outsider bypass).
* kairos_nullspace_residual: normalized anomaly score (0.0 to 1.0)
from KAIROS's Bayes-threshold null-space detector measuring the
divergence between **symbolic shibboleth screening** (elite
language/credential/clique concentration) and **real total factor
productivity (TFP) / physical output** (< 0.25 = aligned with
material output; > 0.70 = severe symbolic rent extraction decoupling
from physical production).
* shibboleth_rent_premium_pct: estimated wage, board-seat, or
procurement premium (0.0 to 100.0) captured solely by holders of
the local clique marker (accent/language register, heritage school,
regional etiquette, or enclave ancestry) over equally productive
outsiders (< 12% = open meritocratic clearing; > 35% = severe
categorical opportunity hoarding).
* consecutive_hoarding_quarters: consecutive calendar quarters in
which kairos_pendulum_phase remains in "shibboleth_hoarding_peak"
OR kairos_nullspace_residual > 0.60.

If snapshot.external_data["shibboleth_pendulum"] is absent or empty,
treat the instrument as **unmonitored**, record state
**MATERIAL_MERIT_REGIME**, note that no pendulum telemetry was
available, and do not cite this skill. 

#### Reading 1 — KAIROS Cyclic Pendulum Phase (kairos_pendulum_phase)

Evaluate the macro-historical phase returned by KAIROS (:8300): 

kairos_pendulum_phaseCyclic Phase Tier
**"material_merit_expansion"**
**phase_material_upswing** — status and capital flow to tangible engineering & output
**"mid_cycle_drift"**
**phase_mixed_drift** — material growth intact, but symbolic status signaling rising
**"clique_rupture_inflection"**
**phase_snapback_turbulence** — ossified clique losing control; high regime transition volatility
**"shibboleth_hoarding_peak"**
**phase_clique_ossification** — arbitrary cultural/linguistic/ancestry codes block productive talent

If kairos_pendulum_phase is missing, treat as **phase_mixed_drift**. 

#### Reading 2 — KAIROS Null-Space Decoupling (kairos_nullspace_residual)

Evaluate how far symbolic clique screening has detached from physical
productivity in KAIROS's null-space projection: 

kairos_nullspace_residualDecoupling Severity
**< 0.25**
**nullspace_aligned** — rewards track measurable physical and economic output
**0.25 to 0.50**
**nullspace_mild_drift** — moderate credential/etiquette padding in white-collar sectors
**0.50 to 0.70**
**nullspace_elevated_rent** — symbolic pedigree systematically out-earns engineering execution
**> 0.70**
**nullspace_acute_decoupling** — pure shibboleth theater masking stagnant physical productivity

If kairos_nullspace_residual is missing, treat as
**nullspace_mild_drift**. 

#### Reading 3 — Categorical Opportunity-Hoarding Premium (shibboleth_rent_premium_pct)

Evaluate the economic tax imposed on productive outsiders by the local
clique marker: 

shibboleth_rent_premium_pctHoarding Tax Tier
**< 12.0%**
**open_access** — minimal clique tax; outsiders compete on equal footing
**12.0% to 22.0%**
**moderate_gatekeeping** — noticeable linguistic/social club advantage in leadership
**22.0% to 35.0%**
**heavy_opportunity_hoarding** — major capital and executive posts restricted to clique insiders
**> 35.0%**
**caste_enclosure** — closed hereditary/linguistic/cultural monopoly strangling dynamism

If shibboleth_rent_premium_pct is missing, treat as
**moderate_gatekeeping**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
pendulum regimes. Evaluate in strict priority order and select the
first regime whose conditions are fully satisfied: 

1. **SHIBBOLETH_CASTE_LOCK** (most severe — unconditional FLAT)
2. **PENDULUM_SNAPBACK_VOLATILITY**
3. **SYMBOLIC_RENT_DRAG**
4. **MATERIAL_MERIT_REGIME** (strictest adaptive fit)

#### SHIBBOLETH_CASTE_LOCK

Any of the following hold: 

* Cyclic Phase Tier is **phase_clique_ossification**
("shibboleth_hoarding_peak") AND Decoupling Severity is
**nullspace_acute_decoupling** (> 0.70).
* Hoarding Tax Tier is **caste_enclosure** (> 35.0% shibboleth rent
premium) AND Decoupling Severity is **nullspace_elevated_rent** or
**nullspace_acute_decoupling** (≥ 0.50).

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. The economy has swung to the extreme clique-hoarding
pole of the Sorokin/Pareto pendulum: arbitrary linguistic, etiquette,
trivia, or ancestry shibboleths have replaced material competence,
guaranteeing capital misallocation and brain drain. The skill binds
unconditionally and must appear in skills_cited. 

#### PENDULUM_SNAPBACK_VOLATILITY

Any of the following hold (and SHIBBOLETH_CASTE_LOCK does not apply): 

* Cyclic Phase Tier is **phase_snapback_turbulence**
("clique_rupture_inflection" — the ossified clique order is
cracking under external competition, demographic pressure, or capital
exodus).
* Cyclic Phase Tier is **phase_clique_ossification** with
**heavy_opportunity_hoarding** (22.0% to 35.0%).

**Delta cap: 0.25.** The clique monopoly is either strangling growth or
undergoing disorderly regime reversal. Cut domestic directional exposure
sharply until material merit re-establishes price discovery. 

#### SYMBOLIC_RENT_DRAG

Any of the following hold (and neither SHIBBOLETH_CASTE_LOCK nor
PENDULUM_SNAPBACK_VOLATILITY applies): 

* Cyclic Phase Tier is **phase_mixed_drift** ("mid_cycle_drift") with
**nullspace_mild_drift** or **nullspace_elevated_rent**.
* Hoarding Tax Tier is **moderate_gatekeeping** (12.0% to 22.0%) or
**heavy_opportunity_hoarding** (22.0% to 35.0%) with
phase_material_upswing.
Delta cap: 0.70. Material output remains positive, but rising
elite trivia, linguistic-register, or social-club gatekeeping is
extracting a growing efficiency tax. Trim sizing relative to
MATERIAL_MERIT_REGIME.

MATERIAL_MERIT_REGIME

All of the following hold:
• Cyclic Phase Tier is phase_material_upswing
("material_merit_expansion").
• Decoupling Severity is nullspace_aligned (< 0.25).
• Hoarding Tax Tier is open_access (< 12.0%).
Delta cap: 1.0. Peak Sorokin/Pareto material-utilitarian phase:
capital and authority flow directly to tangible engineering and
productive execution regardless of accent, background, or social trivia.
The cap equals the strategy cap; the skill never binds on
MATERIAL_MERIT_REGIME.

Ambiguous fallback

Any combination not covered above is classified SYMBOLIC_RENT_DRAG
with delta cap 0.70.

Secondary Filter / Asymmetric Gate — Entrenched Clique Ossification Hysteresis

Apply the persistence test after regime classification and before the
cap.
Shibboleth hoarding is generationally entrenched if
consecutive_hoarding_quarters >= 8 (two or more consecutive years of
sustained "shibboleth_hoarding_peak" or kairos_nullspace_residual > 0.60).
Two years of uninterrupted symbolic rent extraction confirms that the
clique has captured institutional promotion and capital-allocation
channels rather than experiencing a transient cultural fad.
If the hoarding is generationally entrenched, halve the regime's
delta cap:
• SYMBOLIC_RENT_DRAG cap of 0.70 becomes 0.35.
• PENDULUM_SNAPBACK_VOLATILITY cap of 0.25 becomes 0.125.
• SHIBBOLETH_CASTE_LOCK cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read shibboleth pendulum dict. From
snapshot.external_data["shibboleth_pendulum"], load
kairos_pendulum_phase, kairos_nullspace_residual,
shibboleth_rent_premium_pct, and consecutive_hoarding_quarters.
If absent or empty, record MATERIAL_MERIT_REGIME, note the
omission, and do not cite this skill.
2. Classify cyclic phase tier. Apply Reading 1
(phase_material_upswing, phase_mixed_drift,
phase_snapback_turbulence, or phase_clique_ossification).
3. Classify null-space decoupling. Apply Reading 2
(nullspace_aligned, nullspace_mild_drift,
nullspace_elevated_rent, or nullspace_acute_decoupling).
4. Classify hoarding tax tier. Apply Reading 3 (open_access,
moderate_gatekeeping, heavy_opportunity_hoarding, or
caste_enclosure).
5. Classify regime. Evaluate in strict priority order
(SHIBBOLETH_CASTE_LOCK → PENDULUM_SNAPBACK_VOLATILITY →
SYMBOLIC_RENT_DRAG → MATERIAL_MERIT_REGIME) and select the first
matching regime (fallback: SYMBOLIC_RENT_DRAG).
6. Apply persistence test. If
consecutive_hoarding_quarters >= 8, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
regime is SHIBBOLETH_CASTE_LOCK, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
regime is SHIBBOLETH_CASTE_LOCK, cite
"clique-shibboleth-pendulum" in skills_cited and state the
KAIROS pendulum phase and shibboleth-hoarding finding in the
rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If SHIBBOLETH_CASTE_LOCK,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and KAIROS cyclic
finding. Example:
"SHIBBOLETH_CASTE_LOCK regime; KAIROS phase=shibboleth_hoarding_peak with nullspace_residual=0.78 and 38.0% shibboleth_rent_premium decoupling symbolic clique markers from physical output; forcing action=FLAT; clique-shibboleth-pendulum."
• skills_cited: list of skill names; include
"clique-shibboleth-pendulum" only when the cap bound or the regime
is SHIBBOLETH_CASTE_LOCK.

Worked Examples


Case A — Material-utilitarian expansion phase with aligned KAIROS null-space, cap does not bind

Snapshot:
• kairos_pendulum_phase = "material_merit_expansion"
• kairos_nullspace_residual = 0.18
• shibboleth_rent_premium_pct = 8.5
• consecutive_hoarding_quarters = 0
Readings:
• Cyclic Phase Tier: phase_material_upswing
• Decoupling Severity: < 0.25 → nullspace_aligned
• Hoarding Tax Tier: < 12.0% → open_access
Regime: MATERIAL_MERIT_REGIME, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "clique-shibboleth-pendulum".

Case B — Ossified clique hoarding with acute KAIROS null-space decoupling, unconditional FLAT

Snapshot:
• kairos_pendulum_phase = "shibboleth_hoarding_peak"
• kairos_nullspace_residual = 0.76
• shibboleth_rent_premium_pct = 37.5
• consecutive_hoarding_quarters = 10
Readings:
• Cyclic Phase Tier: phase_clique_ossification
• Decoupling Severity: > 0.70 → nullspace_acute_decoupling
• Hoarding Tax Tier: > 35.0% → caste_enclosure
Regime: SHIBBOLETH_CASTE_LOCK, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "clique-shibboleth-pendulum".

Free Data Sources

The fetcher populates snapshot.external_data["shibboleth_pendulum"] by
routing free socio-economic, linguistic, and intergenerational mobility
time series through KAIROS (:8300) for cyclic baseline subtraction
and null-space anomaly detection (no paid subscription required):
• KAIROS Cyclic & Null-Space Engine (http://localhost:8300):
Local starwalkerz/kairos service computing seasonal/generational
baseline residuals and Bayes-threshold null-space divergence between
symbolic clique concentration and real TFP/industrial output.
• World Bank Global Database on Intergenerational Mobility (GDIM) & WDI:
https://worldbank.org (free global mobility elasticity, income
concentration, and productivity series across 150+ economies).
• Luxembourg Income Study (LIS) & World Inequality Database (WID.world):
https://lisdatacenter.org and https://wid.world (free open
microdata and APIs measuring top-decile/percentile wage premia by
linguistic, regional, educational, and demographic group).
• World Values Survey (WVS) & European Social Survey (ESS):
https://worldvaluessurvey.org and https://europeansocialsurvey.org
(free longitudinal waves measuring shifts between materialist/utilitarian
values, trust in outsiders, and rigid cultural/ingroup gatekeeping).
• ILOSTAT & UNESCO Institute for Statistics (UIS):
https://ilo.org and https://unesco.org (free open
APIs for occupation-by-background wage gaps, language-of-instruction
monopolies, and executive credential stratification).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not treat one specific surface marker (language, accent, etiquette,
or phenotype) as unique; evaluate the invariant structural ratio of
clique-marker rent to physical productivity via KAIROS.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "clique-shibboleth-pendulum" when the cap did not bind
and the regime is not SHIBBOLETH_CASTE_LOCK.

Citation Mapping

• Civilizational Sensate vs. Ideational Cycles: Pitirim A. Sorokin,
Social and Cultural Dynamics, Vols. 1–4 (American Book Company,
1937–1941); Vilfredo Pareto, The Mind and Society (Trattato di
Sociologia Generale, 1916).
• Symbolic Capital, Linguistic Markets & Class Shibboleths: Pierre
Bourdieu, Distinction: A Social Critique of the Judgement of Taste
(Harvard University Press, 1979); Pierre Bourdieu, Language and
Symbolic Power (Harvard University Press, 1991); Paul Fussell,
Class: A Guide Through the American Status System (Summit Books,
1983).
• Categorical Opportunity Hoarding: Charles Tilly, Durable
Inequality (University of California Press, 1998).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.