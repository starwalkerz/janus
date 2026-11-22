#### name: "wartime-coverage-sanitizer-detector"
description: "Mirror image of media-sentiment-bias-detector: detect wartime coverage sanitization, dampened casualty/attrition volume, and victory-bias inversion across active conflict zones filtered through (1) host-government martial/legal censorship gates, (2) allied media statutory and social-clique enforcement, and (3) reverse power-law sensationalism (allied audiences rewarding 'winning' narratives over kinetic reality); cross-check sanitized GDELT sentiment against physical telemetry (UCDP, ACLED, NASA FIRMS, ENTSO-E, IMF PortWatch) and force FLAT when kinetic war is masked by sanitized coverage."

#### Wartime Coverage Sanitizer & Victory-Bias Detector (Reverse Power-Law Filter)

You are reading the tick against **wartime information sanitization,
dampened kinetic reporting, and victory-bias inversion**. While
media-sentiment-bias-detector corrects peacetime clickbait inflation in
stable core markets, active war zones exhibit the **exact opposite
distortion**: severe, high-intensity kinetic warfare—characterized by
artillery duels, drone/missile strikes, grid destruction, and heavy
attrition—is systematically presented to allied and domestic publics in a
**sanitized format with artificially dampened volume and optimistic
"winning" tone**. 

In Philip Knightley's *The First Casualty* (1975), Paul Fussell's
*Wartime: Understanding and Behavior in the Second World War* (1989),
and Irving Janis's *Groupthink* (1972), wartime coverage passes through
three sequential throttling gates before reaching global financial
wires: 

1. **Gate 1 — Host-Government Martial & Legal Censorship (legal_censorship_tier):**
The local belligerent government enforces martial law, criminalizes
unauthorized filming or geolocation of frontline positions, air-defense
impacts, and energy-grid damage, and restricts press accreditation to
approved pool dispatches.
2. **Gate 2 — Allied Media Legal & Social-Clique Enforcement (allied_clique_enforcement):**
Allied foreign broadcasters and wire services operate under statutory
national-security/sanctions compliance constraints reinforced by tight
editorial clique conformity (mass-formation-herding), penalizing
reporters or analysts who break consensus framing.
3. **Gate 3 — Reverse Power-Law Sensationalism / Victory-Bias Inversion (reverse_sentiment_bias):**
In peacetime, high GDP/capita, USD/EUR/CNY financial integration, and
English-language proximity magnify negative headlines; in an allied
war effort, **that exact same power-law engine runs in reverse**.
Because domestic publics and allied capital markets find it far more
believable and palatable that *"their side is winning"* regardless of
actual territorial or attrition dynamics on the ground, Anglophone
wires suppress raw attrition volume and amplify sanitized resilience
narratives.

Without detecting this **three-gate sanitization filter**, models
relying on GDELT sentiment or mainstream headlines misclassify an
active, high-intensity war economy as a recovering peacetime market—exposing
capital to sudden kinetic, grid, currency, or sovereign-restructuring
ruptures (VERIFIED_SANITIZED_WAR → FLAT). 

Your job is to evaluate the three wartime throttling gates against
independent physical conflict telemetry (UCDP, ACLED, NASA FIRMS
thermal anomalies, ENTSO-E grid telemetry, IMF PortWatch), classify
the information regime, and cap your delta accordingly. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise delta
above the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["wartime_sanitizer"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes martial-law/press-freedom indices, allied wire
framing divergence, raw GDELT tone/volume, and physical satellite/grid
conflict telemetry into snapshot.external_data["wartime_sanitizer"]: 

* legal_censorship_tier: host-government statutory control over
frontline, infrastructure-strike, and casualty reporting ("open_press",
"selective_restrictions", or "martial_law_blackout" — criminal
penalties for publishing strike coordinates, grid damage, or
unapproved casualty figures).
* allied_clique_enforcement: degree to which allied international
media exhibits synchronized framing, low source entropy, and
legal/social conformity ("independent_pluralism",
"soft_editorial_alignment", or "clique_enforced_orthodoxy").
* kinetic_vs_sentiment_inversion: gap between verified physical war
intensity (UCDP/ACLED battles/explosions, NASA FIRMS thermal
fire anomalies, ENTSO-E generation/grid drops) and sanitized media
tone ("aligned", "dampened_attrition", or "victory_bias_inversion"
— severe physical kinetic escalation paired with upbeat/sanitized
"winning" media sentiment).
* consecutive_sanitized_weeks: consecutive calendar weeks in which
physical kinetic telemetry (UCDP/ACLED/FIRMS) remains at war
intensity while GDELT volume/tone shows dampened_attrition or
victory_bias_inversion.

If snapshot.external_data["wartime_sanitizer"] is absent or empty,
treat the instrument as **unmonitored**, record state
**UNFILTERED_REPORTING**, note that no wartime-sanitizer telemetry was
available, and do not cite this skill. 

#### Reading 1 — Gate 1: Host-Government Legal Censorship (legal_censorship_tier)

Evaluate statutory information throttling at the conflict source: 

legal_censorship_tierGate 1 Censorship Status
**"open_press"**
**gate1_open** — unrestricted frontline and infrastructure reporting
**"selective_restrictions"**
**gate1_throttled** — military accreditation rules and delayed strike disclosure
**"martial_law_blackout"**
**gate1_blackout** — criminalized strike/casualty/grid telemetry; state-curated dispatches only

If legal_censorship_tier is missing, treat as **gate1_throttled**. 

#### Reading 2 — Gate 2: Allied Media Legal & Social-Clique Enforcement (allied_clique_enforcement)

Evaluate downstream legal and conformity enforcement across allied wires: 

allied_clique_enforcementGate 2 Allied Framing Status
**"independent_pluralism"**
**gate2_pluralist** — diverse field reporting and dissenting strategic analysis
**"soft_editorial_alignment"**
**gate2_aligned** — shared alliance framing; uncomfortable attrition downplayed
**"clique_enforced_orthodoxy"**
**gate2_locked** — legal/sanctions guardrails + ossified_clique ostracism enforce uniform narrative

If allied_clique_enforcement is missing, treat as **gate2_aligned**. 

#### Reading 3 — Gate 3: Reverse Sensationalism / Victory-Bias Inversion (kinetic_vs_sentiment_inversion)

Evaluate whether physical satellite/conflict telemetry contradicts
sanitized "winning" media narratives: 

kinetic_vs_sentiment_inversionGate 3 Physical-vs-Narrative Gap
**"aligned"**
**gate3_transparent** — media volume and tone match physical conflict telemetry
**"dampened_attrition"**
**gate3_dampened** — kinetic strikes and grid/port damage under-reported in volume
**"victory_bias_inversion"**
**gate3_inverted** — heavy kinetic warfare masked by sanitized "winning/resilient" headlines

If kinetic_vs_sentiment_inversion is missing, treat as
**gate3_dampened**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four wartime
information states. Evaluate in strict priority order and select the
first state whose conditions are fully satisfied: 

1. **SANITIZED_WAR_FOG** (active kinetic war masked by censorship & victory bias — unconditional FLAT)
2. **COALITION_NARRATIVE_LOCK** (allied clique conformity obscuring material attrition)
3. **SELECTIVE_FOG_WATCH** (localized operational security throttling; partial transparency)
4. **UNFILTERED_REPORTING** (strictest adaptive fit)

#### SANITIZED_WAR_FOG

Any of the following hold: 

* Gate 3 is **gate3_inverted** ("victory_bias_inversion" — physical
war/grid/thermal telemetry proves severe kinetic conflict while
sanitized headlines claim victory or routine stability).
* Gate 1 is **gate1_blackout** ("martial_law_blackout") AND Gate 3
is **gate3_dampened** or **gate3_inverted**.
* Gate 2 is **gate2_locked** ("clique_enforced_orthodoxy") AND Gate 3
is **gate3_dampened** or **gate3_inverted**.

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. Media sentiment is running in reverse victory-bias
mode behind martial-law and allied-clique gates, concealing genuine
kinetic warfare (Baghdad / Mogadishu / Ukraine / Sahel physical
force posture) and severe sovereign/infrastructure tail risk. The skill
binds unconditionally and must appear in skills_cited. 

#### COALITION_NARRATIVE_LOCK

Any of the following hold (and SANITIZED_WAR_FOG does not apply): 

* Gate 1 is **gate1_throttled** ("selective_restrictions") AND Gate 2
is **gate2_locked** ("clique_enforced_orthodoxy").
* Gate 2 is **gate2_aligned** or **gate2_locked** AND Gate 3 is
**gate3_dampened** ("dampened_attrition").

**Delta cap: 0.20.** Allied narrative conformity and selective wartime
restrictions are systematically muting attrition and logistics friction.
Cut long exposure sharply. 

#### SELECTIVE_FOG_WATCH

Any of the following hold (and neither SANITIZED_WAR_FOG nor
COALITION_NARRATIVE_LOCK applies): 

* Gate 1 is **gate1_throttled** ("selective_restrictions") with
gate2_pluralist and gate3_transparent.
* Gate 2 is **gate2_aligned** ("soft_editorial_alignment") with
gate1_open and gate3_transparent.
Delta cap: 0.65. Operational security rules or soft editorial
alignment create partial blind spots around localized deployments,
though macro physical telemetry remains transparent. Trim position size
for fog-of-war uncertainty.

UNFILTERED_REPORTING

All of the following hold:
• Gate 1 is gate1_open ("open_press").
• Gate 2 is gate2_pluralist ("independent_pluralism").
• Gate 3 is gate3_transparent ("aligned").
Delta cap: 1.0. No wartime censorship, clique enforcement, or
victory-bias inversion detected. The cap equals the strategy cap; the
skill never binds on UNFILTERED_REPORTING.

Ambiguous fallback

Any combination not covered above is classified COALITION_NARRATIVE_LOCK
with delta cap 0.20.

Secondary Filter / Asymmetric Gate — Prolonged Fog-of-War Desensitization Hysteresis

Apply the persistence test after state classification and before the
cap.
A wartime information environment is chronically desensitized if
consecutive_sanitized_weeks >= 8 (eight or more consecutive weeks of
sustained dampened_attrition or victory_bias_inversion). After two
months of sanitized coverage, allied audiences and financial algorithms
habituate to ongoing kinetic destruction as "normal background," creating
acute blindness to sudden front-line, grid, or fiscal collapse.
If the environment is chronically desensitized, halve the state's
delta cap:
• SELECTIVE_FOG_WATCH cap of 0.65 becomes 0.325.
• COALITION_NARRATIVE_LOCK cap of 0.20 becomes 0.10.
• SANITIZED_WAR_FOG cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read wartime sanitizer dict. From
snapshot.external_data["wartime_sanitizer"], load
legal_censorship_tier, allied_clique_enforcement,
kinetic_vs_sentiment_inversion, and consecutive_sanitized_weeks.
If absent or empty, record UNFILTERED_REPORTING, note the
omission, and do not cite this skill.
2. Evaluate Gate 1 (Host legal censorship). Apply Reading 1
(gate1_open, gate1_throttled, or gate1_blackout).
3. Evaluate Gate 2 (Allied legal & clique enforcement). Apply
Reading 2 (gate2_pluralist, gate2_aligned, or gate2_locked).
4. Evaluate Gate 3 (Reverse sensationalism / victory bias). Apply
Reading 3 (gate3_transparent, gate3_dampened, or
gate3_inverted).
5. Classify state. Evaluate in strict priority order
(SANITIZED_WAR_FOG → COALITION_NARRATIVE_LOCK →
SELECTIVE_FOG_WATCH → UNFILTERED_REPORTING) and select the first
matching state (fallback: COALITION_NARRATIVE_LOCK).
6. Apply persistence test. If consecutive_sanitized_weeks >= 8,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
state is SANITIZED_WAR_FOG, set delta = 0.0 and action = "FLAT"
regardless of AGOP. Otherwise, if intended delta exceeds
delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
state is SANITIZED_WAR_FOG, cite
"wartime-coverage-sanitizer-detector" in skills_cited and name
which of the three throttling gates bound in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If SANITIZED_WAR_FOG,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and the active
censorship/victory-bias gates. Example:
"SANITIZED_WAR_FOG state; Gate 1 martial_law_blackout + Gate 2 clique_enforced_orthodoxy + Gate 3 victory_bias_inversion masking kinetic grid/artillery attrition behind upbeat wire tone over 12 weeks; forcing action=FLAT; wartime-coverage-sanitizer-detector."
• skills_cited: list of skill names; include
"wartime-coverage-sanitizer-detector" only when the cap bound or the
state is SANITIZED_WAR_FOG.

Worked Examples


Case A — Active war zone masked by martial law, allied clique orthodoxy, and victory-bias inversion, unconditional FLAT

Snapshot:
• legal_censorship_tier = "martial_law_blackout"
• allied_clique_enforcement = "clique_enforced_orthodoxy"
• kinetic_vs_sentiment_inversion = "victory_bias_inversion"
• consecutive_sanitized_weeks = 14
Readings:
• Gate 1: gate1_blackout
• Gate 2: gate2_locked
• Gate 3: gate3_inverted
State: SANITIZED_WAR_FOG, delta cap 0.0 → forces FLAT.
AGOP ranks LONG based on upbeat sanitized headlines. LLM overrides
to action = "FLAT", delta = 0.0, and cites
"wartime-coverage-sanitizer-detector".

Case B — Selective wartime press restrictions with allied editorial alignment dampening attrition, cap binds

Snapshot:
• legal_censorship_tier = "selective_restrictions"
• allied_clique_enforcement = "soft_editorial_alignment"
• kinetic_vs_sentiment_inversion = "dampened_attrition"
• consecutive_sanitized_weeks = 9
Readings:
• Gate 1: gate1_throttled
• Gate 2: gate2_aligned
• Gate 3: gate3_dampened
State: COALITION_NARRATIVE_LOCK, delta cap 0.20.
Persistence: consecutive_sanitized_weeks = 9 >= 8 → halve to 0.10.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.10 binds.
LLM returns delta = 0.10 and cites
"wartime-coverage-sanitizer-detector".

Free Data Sources

The fetcher populates snapshot.external_data["wartime_sanitizer"] by
contrasting sanitized media feeds against unvarnished physical,
satellite, and conflict-event telemetry from the following free, open
public sources (no paid subscription required):
• Uppsala Conflict Data Program (UCDP) & ACLED:
https://uu.se and https://acleddata.com (free georeferenced
armed-conflict battle, shelling, drone/missile strike, and fatality
datasets used to measure true kinetic intensity).
• NASA FIRMS (Fire Information for Resource Management System):
https://nasa.gov (free, open MODIS/VIIRS
satellite thermal anomaly API detecting artillery, refinery, and
infrastructure fires in real time independent of press censorship).
• ENTSO-E Transparency Platform & IEA Open Energy Data:
https://entsoe.eu and https://iea.org (free grid
frequency, cross-border interconnect flow, and generation outage
telemetry exposing physical power-grid destruction).
• IMF PortWatch & AIS Maritime Traffic Feeds:
https://imf.org (free satellite-derived port-call and
chokepoint vessel-transit counts verifying physical trade disruption).
• GDELT Project 2.0 Global Knowledge Graph (GKG):
https://gdeltproject.org (free, no-key 15-minute global news feed
used to measure raw wire volume, source concentration, and
victory-bias tone divergence against UCDP/FIRMS ground truth).
• RSF World Press Freedom Index & Freedom House Open Data:
https://rsf.org and https://freedomhouse.org (free statutory
press-restriction and martial-law censorship indicators).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not treat dampened GDELT negative volume or upbeat allied wire
headlines as peacetime stability when UCDP, ACLED, NASA FIRMS,
or ENTSO-E confirm active kinetic warfare.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "wartime-coverage-sanitizer-detector" when the cap did
not bind and the state is not SANITIZED_WAR_FOG.

Citation Mapping

• Wartime Censorship & Propaganda Filtering: Philip Knightley, The
First Casualty: The War Correspondent as Hero and Myth-Maker from the
Crimea to Iraq (Harcourt, 1975); Paul Fussell, Wartime:
Understanding and Behavior in the Second World War (Oxford University
Press, 1989).
• Editorial Clique Conformity & Mass Framing: Irving L. Janis,
Victims of Groupthink (Houghton Mifflin, 1972); Walter Lippmann,
Public Opinion (1922).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
