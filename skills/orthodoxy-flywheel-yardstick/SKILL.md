#### name: "orthodoxy-flywheel-yardstick"
description: "Classify the tick by two-stage puritanical/orthodoxy cycle phase—separating fast-decaying bottom-up peer/status tribunals from ~80-year institutional flywheels (20-year codification climb + 60-year asymmetric unwind)—by querying KAIROS (:8300) phase-lag telemetry alongside free WVS, ESS, V-Dem, World Bank WGI, and GDELT registries; cap delta or force FLAT when institutionalized orthodoxy detaches from material reality."

#### Orthodoxy Flywheel Yardstick

You are reading the tick against the **two-stage puritanical orthodoxy cycle**—an invariant sociopolitical mechanism in which a bottom-up grassroots boundary/status shield (e.g., 1972 Cairo University *al-zayy al-Islami*, 2013–2017 #MeToo/campus checklists) is captured by administrative councils and hardened into an **~80-year institutional flywheel** (roughly a 20-year climb to statutory/clerical saturation followed by a 50–60-year asymmetric unwind). 

Drawing on Erving Goffman's *The Presentation of Self in Everyday Life* (1959) on frontstage/backstage collapse, Max Weber's *Economy and Society* (1922) on bureaucratic routinization, Alexis de Tocqueville's *Democracy in America* (1835) on administrative tutelage, and Timur Kuran's *Private Truths, Public Lies* (1995) on ritual preference falsification, the cycle operates through two coupled waves: 

1. **Leading Grassroots Wave (Fast Cohort Burnout, ~10–15 yrs):** Starts peer-to-peer as a defensive shield against social disorder or status anxiety. Individuals internalize a "phantom audience" (collapsing private backstage space into a permanent moral courtroom), penalizing unperformed material competence while rewarding theatrical compliance. Informal cohorts exhaust themselves and re-privatize daily life once the external crisis passes.
2. **Lagging Institutional Flywheel (~80-Year Three-Generation Cycle):** Roughly 5–10 years after grassroots ignition, administrative councils (clerical boards, university compliance committees, corporate HR, or centralized public-order bureaucracies) capture the mood and codify moving-goalpost orthodoxies into permanent rules. Because councils renew their cadres automatically and lack a constitutional or spatial buffer (unlike federalized or neighborhood-compartmentalized polities), **institutional policing continues climbing even after grassroots culture has burned out**—creating a "Great Scissors" divergence followed by decades of hollow ritual compliance ("administrative Sovietization") and brain drain.

Because this process exhibits a measurable **phase offset between informal social norms and formal institutional enforcement**, JANUS queries **KAIROS (:8300)** directly alongside open longitudinal social-values and governance registries to detect whether the target polity is in adaptive equilibrium, mid-scissors codification, or terminal institutional orthodoxy lock-in. 

Your job is to classify the tick into one of four orthodoxy-flywheel states and cap your delta accordingly. You do not invent trades. You do not override AGOP. You modulate the LLM's delta within the bound the verifier already permits. You never raise delta above the strategy cap, and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["orthodoxy_flywheel"] (populated by querying KAIROS :8300 over free values, regulatory-burden, and media-tone time series). Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher queries KAIROS (:8300) and open sociometric/governance registries and normalizes the target polity or sector into snapshot.external_data["orthodoxy_flywheel"]: 

* grassroots_tribunal_index: normalized intensity (0.0 to 1.0) of bottom-up peer/digital status-policing and interpersonal distrust derived from WVS/ESS social-trust waves and GDELT cultural-grievance tone (< 0.25 = re-privatized/grounded; > 0.65 = peak peer courtroom).
* institutional_flywheel_index: normalized intensity (0.0 to 1.0) of top-down bureaucratic, speech, academic, or public-order compliance codification derived from V-Dem academic/expression freedom sub-indices, World Bank WGI regulatory rigidity, and GDELT administrative-enforcement tone (< 0.25 = pragmatic/bounded; > 0.70 = captured compliance state).
* kairos_phase_lag_years: estimated phase offset (in years) returned by KAIROS (:8300) cross-correlating the leading grassroots curve against the lagging institutional curve (< 3.0 = coupled/baseline; 3.0 to 8.0 = active institutional capture; > 8.0 = late-stage flywheel persistence after grassroots burnout).
* reality_decoupling_score: normalized score (0.0 to 1.0) measuring divergence between administrative orthodoxy enforcement and material/economic execution—e.g., declining TFP/R&D output, capital/talent flight, or failing basic bread-and-butter governance metrics (< 0.30 = grounded in material results; > 0.70 = severe narrative-over-reality decoupling).
* entrenched_flywheel_quarters: consecutive calendar quarters in which institutional_flywheel_index >= 0.65 AND reality_decoupling_score >= 0.50.

If snapshot.external_data["orthodoxy_flywheel"] is absent or empty, treat the instrument as **unmonitored**, record state **PRAGMATIC_BASELINE**, note that no orthodoxy-flywheel telemetry was available, and do not cite this skill. 

#### Reading 1 — Grassroots vs. Institutional Phase Split (grassroots_tribunal_index & institutional_flywheel_index)

Evaluate the coupling between the fast leading wave and the slow lagging flywheel: 

Grassroots IndexInstitutional IndexPhase Split Reading
**< 0.35**
< 0.35**baseline_equilibrium** — private backstage intact; institutions bounded to material tasks
**≥ 0.35**
< 0.45**grassroots_ignition** — peer/campus tribunal rising; state/corporate capture still early
**≥ 0.35**
0.45 to 0.70**synchronized_capture** — grassroots mood hardening into formal HR/academic/legal codes
**< 0.45**
≥ 0.65**great_scissors_lag** — grassroots cohort burned out, but captured council keeps ramping rules
**any**
> 0.70**institutional_lock_in** — full administrative orthodoxy flywheel decoupled from grassroots life

If either index is missing, treat as **baseline_equilibrium** and rely on Reading 2 and Reading 3. 

#### Reading 2 — Material Reality Decoupling (reality_decoupling_score)

Evaluate how severely orthodoxy enforcement has displaced basic material competence ("failing the price of bread" / penalizing empirical candor): 

reality_decoupling_scoreReality Alignment Tier
**< 0.30**
**materially_grounded** — institutions audited by physical output, truth, and reciprocity
**0.30 to 0.55**
**ceremonial_drag** — rising compliance overhead and self-censorship in elite hubs
**0.55 to 0.75**
**sovietized_ritual** — hollow boilerplate compliance; builders and researchers exiting
**> 0.75**
**acute_reality_breach** — ideological narration openly overrides material survival and facts

If reality_decoupling_score is missing, treat as **ceremonial_drag**. 

#### Reading 3 — Spatial & Constitutional Buffer (kairos_phase_lag_years)

Evaluate whether spatial compartmentalization (center vs. neighborhood), federalism, or constitutional speech protections are containing the flywheel: 

kairos_phase_lag_yearsContainment Tier
**< 3.0**
**buffered_containment** — spatial/legal boundaries prevent tribunal from colonizing private life
**3.0 to 8.0**
**porous_capture** — institutional flywheels forming in elite hubs while periphery resists
**> 8.0**
**unbuffered_saturation** — multi-decade administrative flywheel operating without external check

If kairos_phase_lag_years is missing, treat as **porous_capture**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four orthodoxy-flywheel states. Evaluate in strict priority order and select the first state whose conditions are fully satisfied: 

1. **ADMINISTRATIVE_SOVIETIZATION** (most severe — unconditional FLAT)
2. **GREAT_SCISSORS_DRAG**
3. **GRASSROOTS_TRIBUNAL_FRICTION**
4. **PRAGMATIC_BASELINE** (strictest adaptive fit)

#### ADMINISTRATIVE_SOVIETIZATION

Any of the following hold: 

* Phase Split Reading is **institutional_lock_in** (institutional_flywheel_index > 0.70) AND Reality Alignment Tier is **sovietized_ritual** or **acute_reality_breach** (≥ 0.55).
* Reality Alignment Tier is **acute_reality_breach** (> 0.75) AND Containment Tier is **unbuffered_saturation** (> 8.0 yrs).

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless of what AGOP ranked. The polity has entered late-stage institutional orthodoxy lock-in: administrative councils enforce ever-shifting compliance rituals while hollowing out scientific candor, productive capital, and social trust. The skill binds unconditionally and must appear in skills_cited. 

#### GREAT_SCISSORS_DRAG

Any of the following hold (and ADMINISTRATIVE_SOVIETIZATION does not apply): 

* Phase Split Reading is **great_scissors_lag** (grassroots cohort burned out while institutional flywheel ≥ 0.65 keeps climbing).
* Phase Split Reading is **synchronized_capture** with Reality Alignment Tier **sovietized_ritual** (0.55 to 0.75).

**Delta cap: 0.25.** Informal culture is attempting to normalize, but captured state, university, or corporate bureaucracies are still ramping up compliance overhead and driving talent flight. Cut directional domestic exposure sharply. 

#### GRASSROOTS_TRIBUNAL_FRICTION

Any of the following hold (and neither ADMINISTRATIVE_SOVIETIZATION nor GREAT_SCISSORS_DRAG applies):

• Phase Split Reading is grassroots_ignition or synchronized_capture with Reality Alignment Tier ceremonial_drag (0.30 to 0.55).
• Containment Tier is porous_capture (3.0 to 8.0 yrs) while Reality Alignment Tier is materially_grounded.
Delta cap: 0.75. Bottom-up peer/status policing or early institutional compliance is introducing measurable friction in consumer, media, or white-collar sectors, though core material production remains intact. Reduce size relative to PRAGMATIC_BASELINE.

PRAGMATIC_BASELINE

All of the following hold:
• Phase Split Reading is baseline_equilibrium.
• Reality Alignment Tier is materially_grounded (< 0.30).
• Containment Tier is buffered_containment (< 3.0 yrs).
Delta cap: 1.0. Clean boundary between public civic etiquette and unpoliced private/productive life; institutions are judged by material results rather than ideological orthodoxy. The cap equals the strategy cap; the skill never binds on PRAGMATIC_BASELINE.

Ambiguous fallback

Any combination not covered above is classified GRASSROOTS_TRIBUNAL_FRICTION with delta cap 0.75.

Secondary Filter / Asymmetric Gate — Multi-Generation Flywheel Hysteresis

Apply the persistence test after state classification and before the cap.
An orthodoxy flywheel is generationally entrenched if entrenched_flywheel_quarters >= 12 (three or more consecutive years of institutional_flywheel_index >= 0.65 and reality_decoupling_score >= 0.50). Three consecutive years of decoupled institutional enforcement confirms that the administrative council has survived an initial cohort turnover and locked into a multi-decade (~60-year) asymmetric unwinding trajectory.
If the flywheel is generationally entrenched, halve the state's delta cap:
• GRASSROOTS_TRIBUNAL_FRICTION cap of 0.75 becomes 0.375.
• GREAT_SCISSORS_DRAG cap of 0.25 becomes 0.125.
• ADMINISTRATIVE_SOVIETIZATION cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read orthodoxy flywheel dict. From snapshot.external_data["orthodoxy_flywheel"], load grassroots_tribunal_index, institutional_flywheel_index, kairos_phase_lag_years, reality_decoupling_score, and entrenched_flywheel_quarters. If absent or empty, record PRAGMATIC_BASELINE, note the omission, and do not cite this skill.
2. Classify phase split. Apply Reading 1 (baseline_equilibrium, grassroots_ignition, synchronized_capture, great_scissors_lag, or institutional_lock_in).
3. Classify reality alignment. Apply Reading 2 (materially_grounded, ceremonial_drag, sovietized_ritual, or acute_reality_breach).
4. Classify containment tier. Apply Reading 3 (buffered_containment, porous_capture, or unbuffered_saturation).
5. Classify state. Evaluate in strict priority order (ADMINISTRATIVE_SOVIETIZATION → GREAT_SCISSORS_DRAG → GRASSROOTS_TRIBUNAL_FRICTION → PRAGMATIC_BASELINE) and select the first matching state (fallback: GRASSROOTS_TRIBUNAL_FRICTION).
6. Apply persistence test. If entrenched_flywheel_quarters >= 12, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the state is ADMINISTRATIVE_SOVIETIZATION, set delta = 0.0 and action = "FLAT" regardless of AGOP. Otherwise, if intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the state is ADMINISTRATIVE_SOVIETIZATION, cite "orthodoxy-flywheel-yardstick" in skills_cited and state the phase split and reality-decoupling finding in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP ranking or be "FLAT" (Invariant I1). If ADMINISTRATIVE_SOVIETIZATION, action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and phase-lag finding. Example: "ADMINISTRATIVE_SOVIETIZATION state; institutional_flywheel=0.81 with reality_decoupling=0.68 and 11.5yr KAIROS phase lag indicating locked-in compliance bureaucracy; forcing action=FLAT; orthodoxy-flywheel-yardstick."
• skills_cited: list of skill names; include "orthodoxy-flywheel-yardstick" only when the cap bound or the state is ADMINISTRATIVE_SOVIETIZATION.

Worked Examples


Case A — Re-privatized, materially grounded polity with buffered containment, cap does not bind

Snapshot:
• grassroots_tribunal_index = 0.18
• institutional_flywheel_index = 0.21
• kairos_phase_lag_years = 1.5
• reality_decoupling_score = 0.19
• entrenched_flywheel_quarters = 0
Readings:
• Phase Split: < 0.35 and < 0.35 → baseline_equilibrium
• Reality Alignment: < 0.30 → materially_grounded
• Containment Tier: < 3.0 → buffered_containment
State: PRAGMATIC_BASELINE, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "orthodoxy-flywheel-yardstick".

Case B — Great Scissors divergence with entrenched institutional flywheel, cap binds

Snapshot:
• grassroots_tribunal_index = 0.38
• institutional_flywheel_index = 0.68
• kairos_phase_lag_years = 6.5
• reality_decoupling_score = 0.52
• entrenched_flywheel_quarters = 14
Readings:
• Phase Split: grassroots < 0.45 + institutional ≥ 0.65 → great_scissors_lag
• Reality Alignment: 0.30 to 0.55 → ceremonial_drag
• Containment Tier: 3.0 to 8.0 → porous_capture
State: GREAT_SCISSORS_DRAG, delta cap 0.25.
Persistence: entrenched_flywheel_quarters = 14 >= 12 → halve to 0.125.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.125 binds.
LLM returns delta = 0.125, cites "orthodoxy-flywheel-yardstick", and states in rationale: "GREAT_SCISSORS_DRAG state; grassroots cohort unwinding while institutional_flywheel=0.68 remains entrenched for 14 quarters; delta capped at 0.125; orthodoxy-flywheel-yardstick."

Free Data Sources

The fetcher populates snapshot.external_data["orthodoxy_flywheel"] by routing free longitudinal values, governance, and event-tone series through KAIROS (:8300) for leading/lagging curve phase-offset estimation (no paid subscription required):
• KAIROS Cyclic & Phase-Lag Engine (http://localhost:8300): Local starwalkerz/kairos service computing cross-correlation phase offsets (kairos_phase_lag_years) between leading grassroots trust/grievance curves and lagging institutional compliance series.
• World Values Survey (WVS), European Social Survey (ESS) & Arab Barometer: https://worldvaluessurvey.org, https://europeansocialsurvey.org, and https://arabbarometer.org (free multi-wave microdata measuring interpersonal trust, privatization of moral/religious norms, and generational cohort turnover).
• V-Dem (Varieties of Democracy) Dataset: https://v-dem.net (free country-year indices tracking freedom of academic and cultural expression, public-space surveillance, and institutional orthodoxy enforcement).
• World Bank Worldwide Governance Indicators (WGI) & WDI: https://worldbank.org (free APIs for Regulatory Quality RQ.EST, Government Effectiveness GE.EST, and Total Factor Productivity / R&D output baselines).
• GDELT Project 2.0 Global Knowledge Graph (GKG): https://gdeltproject.org (free, no-key 15-minute event and tone streams separating grassroots social-grievance spikes from state/administrative enforcement actions).

Do Not

• Do not invent a directional action outside allowed_actions or "FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not conflate fast-decaying grassroots peer trends with ~80-year institutionalized flywheels; always evaluate both indices and the KAIROS phase lag.
• Do not compute precise floating-point arithmetic; use the qualitative comparison tables.
• Do not cite "orthodoxy-flywheel-yardstick" when the cap did not bind and the state is not ADMINISTRATIVE_SOVIETIZATION.

Citation Mapping

• Frontstage / Backstage Collapse & Phantom Audience: Erving Goffman, The Presentation of Self in Everyday Life (Anchor Books, 1959). Formalizes the boundary between public impression management and unpoliced private sanctuary.
• Preference Falsification & Ritual Compliance: Timur Kuran, Private Truths, Public Lies: The Social Consequences of Preference Falsification (Harvard University Press, 1995). Explains why public compliance persists long after private conviction has evaporated.
• Bureaucratic Routinization & Administrative Tutelage: Max Weber, Economy and Society (1922); Alexis de Tocqueville, Democracy in America, Vol. 2 (1840). Establishes how grassroots moral movements harden into self-perpetuating administrative councils.
• Generational Cohort Cycles & Institutional Half-Life: Ibn Khaldun, Muqaddimah (1377); Peter Turchin, Ages of Discord (Beresta Books, 2016). Anchors the ~20-year institutional capture climb and ~75–80-year three-generation exhaustion lifecycle.
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm (1972); Ramadge and Wonham, Supervisory Control of a Class of Discrete-Event Processes (1987). Downward-only damping within JANUS invariants I1–I9.