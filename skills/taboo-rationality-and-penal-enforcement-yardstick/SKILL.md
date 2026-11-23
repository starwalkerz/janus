#### name: "taboo-rationality-and-penal-enforcement-yardstick"
description: "Classify the tick by the rational coherence and existential grounding of a polity's enforced social and legal taboos: measuring whether state and clique enforcement targets existential physical/sovereign harms (homicide, theft, physical coercion/slavery, violent assault, material treason) during Spenglerian Spring/Summer regimes or inverts into symbolic, rationally incoherent speech, tone, freeriding, and ideological lip-service taboos under late-stage clique-shibboleth hoarding and institutional sclerosis."

#### Taboo Rationality & Penal Enforcement Yardstick

You are reading the tick against the **rational coherence and existential
grounding of a polity's enforced taboos**. In Mary Douglas's *Purity
and Danger* (1966), Émile Durkheim's *The Division of Labour in Society*
(1893), Cesare Beccaria's *On Crimes and Punishments* (1764), Lon L.
Fuller's *The Morality of Law* (1964), Friedrich A. Hayek's *Law,
Legislation and Liberty* (1973), and Oswald Spengler's *The Decline of
the West* (1918/1922), every governing clique enforces taboos—offenses
that violate its core value system. However, the **content and
rationality** of those taboos shift predictably across the
civilizational lifecycle: 

1. **Existentially Coherent Taboos (Spenglerian Spring / Summer + Early-to-Mid clique-shibboleth-pendulum + Low-to-Moderate institutional-sclerosis-yardstick):**
When institutions are vital and grounded in physical reality, taboos
target **rationally coherent acts carrying direct existential
consequences** for persons, property, and sovereign survival: 

  * **Murder** (deprivation of life)
  * **Theft** (deprivation of earned property and capital)
  * **Actual practice of slavery / physical coercion** (deprivation of
bodily liberty)
  * **Violent sexual assault / rape** (severe bodily violation)
  * **Actual treason / espionage / sabotage** (material betrayal of
sovereign defense and infrastructure)
2. **Symbolic & Rationally Incoherent Taboos (Spenglerian Winter + Peak clique-shibboleth-pendulum + High institutional-sclerosis-yardstick):**
When an ossified governing clique loses competence over physical
security, property protection, and sovereign solvency, enforcement
redirects toward **symbolic, rationally incoherent taboos lacking
existential consequence**—substituting ritualistic compliance for
material protection: 

  * **Policing speech and heterodox opinion** while clearance rates
for actual violent crime and burglary stagnate
  * **Glorifying fiscal freeriding and rent-seeking** while penalizing
productive property owners
  * **Policing ill-mannered tone or etiquette infractions** in place of
confronting actual physical coercion and trafficking
  * **Expanding bureaucratic boundary-policing** while failing to
prosecute violent physical offenders swiftly
  * **Demanding performative lip-service condemnation of geopolitical
rivals** in place of tangible industrial, energy, and border defense

In economic and underwriting terms, a state that diverts judicial,
police, and regulatory capacity from **existential deterrence** into
**symbolic shibboleth enforcement** raises compliance overhead, erodes
property and personal security, and signals late-stage institutional
decay. 

Your job is to classify the taboo-enforcement regime into one of four
states and cap your delta on domestic sovereign, legal-dependent, and
consumer-stability exposure accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three quantitative readings from
snapshot.external_data["taboo_rationality"]. Use the qualitative
tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes criminal-justice clearance rates, speech/etiquette
vs. violent/property prosecution ratios, rule-of-law predictability scores,
and cross-skill civilizational/sclerosis states into
snapshot.external_data["taboo_rationality"]. Each country or bloc
entry (keyed by ISO-2 code such as fi, eu, se, de, uk, us,
jp, sg, ae, ke, rw, in, br, or global_baseline)
supplies: 

* existential_crime_clearance_pct: percentage (0.0 to 100.0) of
reported existential felonies (homicide, aggravated physical assault,
robbery/burglary/theft, and material espionage/sabotage) resolved via
verified charge and conviction (UNODC / Eurostat / national justice
registries).
* symbolic_to_existential_enforcement_ratio: ratio (0.0 to 10.0)
of state prosecutorial, administrative-tribunal, and regulatory speech/tone/lip-service
enforcement actions relative to cleared existential physical/property
prosecutions (< 0.15 = existential focus; > 1.25 = heavy symbolic
shibboleth policing).
* coupled_cycle_and_sclerosis_stage: string summarizing the aligned
state across civilizational-cycle, clique-shibboleth-pendulum, and
institutional-sclerosis-yardstick: 

  * "SPRING_SUMMER_COHERENT" (Spring/Summer cycle + early/mid pendulum + low/moderate sclerosis)
  * "AUTUMN_PROCEDURAL_DRIFT" (late Summer/Autumn + rising shibboleth signaling + moderate sclerosis)
  * "WINTER_SYMBOLIC_INVERSION" (late-cycle Winter + peak shibboleth hoarding + entrenched sclerosis)
* consecutive_symbolic_inversion_years: integer (0 to 25)
counting consecutive settled years in which
symbolic_to_existential_enforcement_ratio >= 0.75 OR
existential_crime_clearance_pct < 35.0 alongside
"WINTER_SYMBOLIC_INVERSION".

If snapshot.external_data["taboo_rationality"] is absent or empty,
treat the polity as **unmonitored**, record state **PROCEDURAL_DRIFT**,
note that no taboo-enforcement telemetry was available, and do not cite
this skill. 

#### Reading 1 — Existential Deterrence & Clearance (existential_crime_clearance_pct)

Evaluate whether the state reliably investigates, clears, and deters
existential physical, property, and sovereign offenses: 

existential_crime_clearance_pctExistential Deterrence Tier
**>= 60.0%**
**high_existential_deterrence** — reliable protection of life, property, and sovereign security
**40.0% to 59.9%**
**moderate_deterrence** — core violent crimes cleared, rising backlog in property offenses
**25.0% to 39.9%**
**eroding_property_and_personal_security** — high unpunished theft/assault; weak deterrence
**< 25.0%**
**existential_enforcement_failure** — chronic non-clearance of physical and property crimes

If existential_crime_clearance_pct is missing, treat as
**moderate_deterrence**. 

#### Reading 2 — Symbolic vs. Existential Enforcement Ratio (symbolic_to_existential_enforcement_ratio)

Evaluate whether judicial and administrative bandwidth is spent on
existential harms or symbolic, rationally incoherent speech, tone,
freeriding, and lip-service taboos: 

symbolic_to_existential_enforcement_ratioTaboo Coherence Tier
**< 0.15**
**rationally_coherent_taboos** — law targets objective physical, property, and treason harms
**0.15 to 0.49**
**creeping_symbolic_policing** — administrative etiquette and speech rules expanding alongside law
**0.50 to 1.24**
**symbolic_overreach** — heavy state bandwidth spent on tone, speech, and ideological signaling
**>= 1.25**
**inverted_shibboleth_justice** — symbolic speech/lip-service policing eclipses existential deterrence

If symbolic_to_existential_enforcement_ratio is missing, treat as
**creeping_symbolic_policing**. 

   - **Criminalizing ritual contact via pollution etymology (`kajoaminen` —
     from Finnish *kajota*, "to touch or tamper with a forbidden/sacred
     object")**—substituting Mary Douglas's archaic ritual-pollution logic
     for Cesare Beccaria's tangible physical-harm standard, flooding dockets
     with low-threshold harassment and groping disputes while violent
     physical rape and coercion cases sit in multi-year backlogs.


#### Reading 3 — Coupled Civilizational & Sclerosis Alignment (coupled_cycle_and_sclerosis_stage)

Cross-check civilizational-cycle, clique-shibboleth-pendulum, and
institutional-sclerosis-yardstick: 

coupled_cycle_and_sclerosis_stageStructural Alignment Tier
**"SPRING_SUMMER_COHERENT"**
**vital_existential_order** — meritocratic clique norms aligned with physical survival
**"AUTUMN_PROCEDURAL_DRIFT"**
**procedural_transition** — rising formalism and credential signaling
**"WINTER_SYMBOLIC_INVERSION"**
**late_winter_shibboleth_inversion** — ossified clique substitutes symbolic orthodoxy for competence

If coupled_cycle_and_sclerosis_stage is missing, treat as
**procedural_transition**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four legal-sociological regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **INVERTED_SHIBBOLETH_TYRANNY** (most severe)
2. **SYMBOLIC_OVERREACH_DECAY**
3. **PROCEDURAL_DRIFT**
4. **EXISTENTIALLY_COHERENT_ORDER** (strictest adaptive fit)

#### INVERTED_SHIBBOLETH_TYRANNY

Any of the following hold: 

* Taboo Coherence Tier is **inverted_shibboleth_justice** (>= 1.25)
AND Existential Deterrence Tier is
**eroding_property_and_personal_security** or
**existential_enforcement_failure** (< 40.0%).
* Structural Alignment Tier is **late_winter_shibboleth_inversion** AND
Taboo Coherence Tier is **inverted_shibboleth_justice** (>= 1.25).
* Existential Deterrence Tier is **existential_enforcement_failure**
(< 25.0%) AND Structural Alignment Tier is
**late_winter_shibboleth_inversion**.

**Delta cap: 0.15.** The governing clique has inverted legal rationality:
symbolic speech, tone, freeriding glorification, and geopolitical
lip-service taboos are aggressively policed while existential
protections for life, earned property, and tangible defense erode.
Arbitrary regulatory risk is high and property security is compromised.
Restrict domestic exposure sharply. 

#### SYMBOLIC_OVERREACH_DECAY
Any of the following hold (and INVERTED_SHIBBOLETH_TYRANNY does not
apply):
• Taboo Coherence Tier is symbolic_overreach (0.50 to 1.24).
• Existential Deterrence Tier is
eroding_property_and_personal_security (25.0% to 39.9%).
• Structural Alignment Tier is late_winter_shibboleth_inversion AND
Taboo Coherence Tier is creeping_symbolic_policing.
Delta cap: 0.35. Judicial and administrative capacity is visibly
diverted from existential deterrence into symbolic shibboleth
enforcement, raising compliance friction and eroding trust in legal
impartiality. Cut domestic long sizing substantially.

PROCEDURAL_DRIFT

Any of the following hold (and neither INVERTED_SHIBBOLETH_TYRANNY
nor SYMBOLIC_OVERREACH_DECAY applies):
• Taboo Coherence Tier is creeping_symbolic_policing
(0.15 to 0.49).
• Existential Deterrence Tier is moderate_deterrence (40.0% to 59.9%).
• Structural Alignment Tier is procedural_transition.
Delta cap: 0.75. Core existential laws remain enforced, though
symbolic speech and etiquette regulations are beginning to accumulate.
Trim sizing relative to EXISTENTIALLY_COHERENT_ORDER.

EXISTENTIALLY_COHERENT_ORDER

All of the following hold:
• Existential Deterrence Tier is high_existential_deterrence
(>= 60.0%).
• Taboo Coherence Tier is rationally_coherent_taboos (< 0.15).
• Structural Alignment Tier is vital_existential_order
("SPRING_SUMMER_COHERENT").
Delta cap: 1.0. Enforced taboos align strictly with rational,
existential protections of life, property, bodily liberty, and
sovereign security; negligible bandwidth wasted on symbolic speech or
lip-service rituals. The cap equals the strategy cap; the skill never
binds on EXISTENTIALLY_COHERENT_ORDER.

Ambiguous fallback

Any combination not covered above is classified
SYMBOLIC_OVERREACH_DECAY with delta cap 0.35.

Secondary Filter / Asymmetric Gate — Symbolic Inversion Hysteresis

Apply the persistence test after regime classification and before the
cap.
Symbolic taboo inversion is institutionally entrenched if
consecutive_symbolic_inversion_years >= 4 (four or more consecutive
settled years in which symbolic_to_existential_enforcement_ratio >= 0.75
OR existential_crime_clearance_pct < 35.0 inside a late-cycle
sclerotic regime). Four consecutive years of prioritizing symbolic
orthodoxy over existential deterrence embeds selective, arbitrary
enforcement into courts and regulators (Lon L. Fuller breakdown of the
inner morality of law).
If the condition is institutionally entrenched, halve the regime's
delta cap:
• PROCEDURAL_DRIFT cap of 0.75 becomes 0.375.
• SYMBOLIC_OVERREACH_DECAY cap of 0.35 becomes 0.175.
• INVERTED_SHIBBOLETH_TYRANNY cap of 0.15 becomes 0.075.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read taboo rationality dict. From
snapshot.external_data["taboo_rationality"], load
existential_crime_clearance_pct,
symbolic_to_existential_enforcement_ratio,
coupled_cycle_and_sclerosis_stage, and
consecutive_symbolic_inversion_years. If absent or empty, record
PROCEDURAL_DRIFT, note the omission, and do not cite this skill.
2. Classify existential deterrence tier. Apply Reading 1.
3. Classify taboo coherence tier. Apply Reading 2.
4. Classify coupled civilizational & sclerosis alignment tier.
Apply Reading 3 (civilizational-cycle +
clique-shibboleth-pendulum + institutional-sclerosis-yardstick).
5. Classify regime. Evaluate in strict priority order
(INVERTED_SHIBBOLETH_TYRANNY → SYMBOLIC_OVERREACH_DECAY →
PROCEDURAL_DRIFT → EXISTENTIALLY_COHERENT_ORDER) (fallback:
SYMBOLIC_OVERREACH_DECAY).
6. Apply persistence test. If
consecutive_symbolic_inversion_years >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"taboo-rationality-and-penal-enforcement-yardstick" in
skills_cited and state the existential clearance rate, symbolic
enforcement ratio, coupled cycle/sclerosis stage, and persistence
years in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.35, "confidence": 0.78, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"INVERTED_SHIBBOLETH_TYRANNY regime; existential_crime_clearance_pct=31.0%, symbolic_to_existential_enforcement_ratio=1.65, coupled_cycle_and_sclerosis_stage=WINTER_SYMBOLIC_INVERSION, consecutive_symbolic_inversion_years=5 (inversion hysteresis halves cap from 0.15 to 0.075); capping delta at 0.075; taboo-rationality-and-penal-enforcement-yardstick."
• skills_cited: list of skill names; include
"taboo-rationality-and-penal-enforcement-yardstick" only when the
cap bound (intended delta > delta_cap).

Worked Examples


Case A — Spring/Summer vital order with high existential clearance and low symbolic policing, cap does not bind

Snapshot:
• existential_crime_clearance_pct = 74.0
• symbolic_to_existential_enforcement_ratio = 0.08
• coupled_cycle_and_sclerosis_stage = "SPRING_SUMMER_COHERENT"
• consecutive_symbolic_inversion_years = 0
Readings:
• Existential Deterrence Tier: high_existential_deterrence
• Taboo Coherence Tier: rationally_coherent_taboos
• Structural Alignment Tier: vital_existential_order
Regime: EXISTENTIALLY_COHERENT_ORDER, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "taboo-rationality-and-penal-enforcement-yardstick".

Case B — Symbolic overreach with eroding property-crime clearance for 4 years, persistence halves cap

Snapshot:
• existential_crime_clearance_pct = 36.5
• symbolic_to_existential_enforcement_ratio = 0.85
• coupled_cycle_and_sclerosis_stage = "AUTUMN_PROCEDURAL_DRIFT"
• consecutive_symbolic_inversion_years = 4
Readings:
• Existential Deterrence Tier: eroding_property_and_personal_security
• Taboo Coherence Tier: symbolic_overreach
• Structural Alignment Tier: procedural_transition
Regime: SYMBOLIC_OVERREACH_DECAY, base cap 0.35. Persistence: 4 >= 4 → fires, halving cap to 0.175.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.175 binds.
LLM returns delta = 0.175 and cites "taboo-rationality-and-penal-enforcement-yardstick".

Case C — Late-Winter shibboleth inversion: speech/lip-service policing eclipses existential deterrence

Snapshot:
• existential_crime_clearance_pct = 29.0
• symbolic_to_existential_enforcement_ratio = 1.80
• coupled_cycle_and_sclerosis_stage = "WINTER_SYMBOLIC_INVERSION"
• consecutive_symbolic_inversion_years = 6
Readings:
• Existential Deterrence Tier: eroding_property_and_personal_security
• Taboo Coherence Tier: inverted_shibboleth_justice
• Structural Alignment Tier: late_winter_shibboleth_inversion
Regime: INVERTED_SHIBBOLETH_TYRANNY, base cap 0.15. Persistence: 6 >= 4 → fires, halving cap to 0.075.
AGOP ranks LONG. LLM intended delta = 0.75. Cap 0.075 binds.
LLM returns delta = 0.075 and cites "taboo-rationality-and-penal-enforcement-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["taboo_rationality"]
from the following free, open criminal-justice, rule-of-law, and
prosecution endpoints:
• UNODC Data Portal (dataunodc.un.org):
https://un.org (free open datasets covering intentional
homicide, violent assault, burglary/theft rates, and criminal-justice
conviction/clearance counts globally).
• Eurostat Crime & Criminal Justice Statistics (crim_off_cat, crim_just_job):
https://europa.eu (free JSON/TSV API tracking recorded
offenses, solved/cleared offenses, and prosecution workloads across
EU/EEA states).
• World Justice Project (WJP) Rule of Law Index Open Data:
https://worldjusticeproject.org (free downloadable factor scores
for Factor 5 Order and Security, Factor 8 Criminal Justice, and
Factor 4 Fundamental Rights — measuring impartial, non-arbitrary
legal enforcement).
• Statistics Finland (Tilastokeskus StatFin) Justice & Court Statistics (Rikokset ja pakkokeinot / Syytetyt, tuomitut ja rangaistukset):
https://stat.fi (free JSON-stat tables breaking down
reported vs. solved/prosecuted offenses by penal-code chapter—separating
homicide, robbery/theft, and treason/espionage from speech/defamation/public-order
infractions).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not treat high regulatory conviction counts on speech, tone, or
etiquette infractions as evidence of strong law and order when
existential physical and property crime clearance is falling.
• Do not evaluate taboo rationality in isolation from
civilizational-cycle, clique-shibboleth-pendulum, and
institutional-sclerosis-yardstick.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "taboo-rationality-and-penal-enforcement-yardstick" when
the cap did not bind (intended delta <= delta_cap).

- Do not treat high prosecution counts on ritual-contact (*kajoaminen*),
  harassment, speech, or etiquette infractions as evidence of strong law
  and order when swift clearance of violent physical coercion, homicide,
  and property theft is falling.


Citation Mapping

• Taboo Systems, Symbolic Pollution & Boundary Maintenance: Mary
Douglas, Purity and Danger: An Analysis of Concepts of Pollution and
Taboo (Routledge, 1966); Émile Durkheim, The Division of Labour in
Society (1893) (repressive vs. restitutive law and collective
conscience). *(Etymological note: Finnish statutory `kajoaminen` derives directly
  from `kajota`—"to touch a forbidden object"—illustrating Douglas's
  ritual-pollution taboo replacing Beccaria's tangible-harm test.)*

• Proportionality, Rational Deterrence & Inner Morality of Law:
Cesare Beccaria, On Crimes and Punishments (Dei delitti e delle
pene, 1764) (measuring crimes strictly by tangible harm to society
rather than ideological offense); Lon L. Fuller, The Morality of Law
(Yale University Press, 1964); Friedrich A. Hayek, Law, Legislation
and Liberty (University of Chicago Press, 1973).
• Civilizational Seasons, Shibboleth Hoarding & Sclerosis Coupling:
Oswald Spengler, The Decline of the West (1918/1922); coupled with
civilizational-cycle, clique-shibboleth-pendulum, and
institutional-sclerosis-yardstick; Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.