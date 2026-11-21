#### name: "clausewitzian-social-friction"
description: "Classify the current tick by kinetic protest/riot contagion, logistical blockade drag, and relative-deprivation focal-point pressure using free ACLED, GDELT, UCDP, and ILOSTAT strike telemetry, and cap delta accordingly."

#### Clausewitzian Social Friction

You are reading the tick against the cumulative social, logistical, and
civil-disorder friction of the target polity or supply-chain corridor.
In Carl von Clausewitz's *On War* (Book I, Ch. 7), **Friction**
(*Friktion*) is the aggregate drag of countless minor breakdowns,
transporter delays, absenteeism, and local resistance that makes even
simple operational execution difficult (*"everything in war is very
simple, but the simplest thing is difficult"*). 

Crucially, social friction does not scale linearly. In Mark Granovetter's
threshold model (1978) and Timur Kuran's preference-falsification
framework (1995), a polity can appear superficially calm while quiet
grievance accumulates—until a single Thomas Schelling focal point (a
fuel-subsidy cut, election dispute, or port strike) triggers a sudden,
non-linear contagion cascade across roads, rails, ports, and factories. 

Your job is to classify the tick into one of four social-friction states
and cap your delta accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["social_friction"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes conflict, protest, strike, and news-tone event
streams into snapshot.external_data["social_friction"]. Each country
or corridor entry (keyed by ISO-2 code or corridor hub such as us,
eu, fi, fr, de, uk, ke, et, ng, za, in, bd,
sh, br, ar, or global_baseline) supplies: 

* unrest_events_7d_ratio: trailing 7-day count of protests, riots,
and civil-disorder events divided by the trailing 90-day weekly
baseline (1.0 = normal baseline cadence).
* logistics_blockade_events_7d: count of distinct transport, port,
rail, highway, or general-strike disruptions recorded in the target
region over the trailing 7 days.
* gdelt_instability_tone: normalized 7-day GDELT conflict/protest
tone & Goldstein-scale stress score on a 0 to 100 scale (0 =
completely calm; > 65 = acute multi-city mobilization or state
crackdown).
* focal_point_active: boolean (true or false) indicating whether a
high-salience Schelling focal point (election window, austerity/fuel
price shock, major labor contract expiry, or sovereign debt default)
is active within ±14 days.
* weeks_elevated_friction: consecutive settled weeks in which
unrest_events_7d_ratio >= 2.0 OR logistics_blockade_events_7d >= 3.

If snapshot.external_data["social_friction"] is absent or empty, treat
the region as **unmonitored**, record state **FRICTIONLESS**, note that
no social-friction data was available, and do not cite this skill. 

#### Reading 1 — Kinetic protest & riot contagion (unrest_events_7d_ratio)

Evaluate unrest_events_7d_ratio against Granovetter's threshold
contagion curve: 

unrest_events_7d_ratioContagion Regime
**< 1.3×**
**quiescent** — routine civic baseline; no cascade momentum
**1.3× to 2.2×**
**simmering** — localized demonstrations; grievances surfacing
**2.2× to 4.0×**
**contagious** — threshold cascade underway across multiple hubs
**> 4.0×**
**rupture** — mass civil disorder, curfews, or kinetic clashes

If unrest_events_7d_ratio is missing, treat as **quiescent** and
rely on Reading 2 and Reading 3. 

#### Reading 2 — Logistical & sub-threshold resistance drag (logistics_blockade_events_7d)

Evaluate physical supply-line interference (Martin van Creveld's
logistical friction and James C. Scott's everyday resistance/strikes): 

logistics_blockade_events_7dLogistical Drag
**0**
**clear** — ports, rails, highways, and plants operating normally
**1 to 2**
**sticky** — isolated wildcat strikes or localized road delays
**3 to 6**
**clogged** — coordinated port/rail blockades or rolling strikes
**> 6**
**severed** — arterial transport paralysis & physical supply cutoff

If logistics_blockade_events_7d is missing, treat as **clear**. 

#### Reading 3 — Preference-falsification & focal-point pressure (gdelt_instability_tone & focal_point_active)

Combine GDELT media/event stress with Schelling focal-point alignment
to detect imminent phase transitions before kinetic counts peak: 

gdelt_instability_tonefocal_point_activePressure State
**< 35**
false**latent** — low grievance salience; no synchronization trigger
**< 35**
true**watch** — focal point present, but grievance mobilization low
**35 to 65**
false**pressurized** — elevated tension without immediate focal catalyst
**35 to 65**
true**synchronized** — high grievance aligned with Schelling focal point
**> 65**
any**flashpoint** — acute regime/social instability threshold breached

If gdelt_instability_tone is missing, treat as **latent** (or **watch**
if focal_point_active is true). 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
social-friction states. Evaluate in strict priority order and select the
first state whose conditions are fully satisfied: 

1. **RUPTURE** (most severe)
2. **CONTAGIOUS**
3. **STICKY**
4. **FRICTIONLESS** (strictest adaptive fit)

#### RUPTURE

Any of the following hold: 

* Contagion Regime is **rupture** (> 4.0× baseline).
* Logistical Drag is **severed** (> 6 transport/port blockades in 7d).
* Contagion Regime is **contagious** (2.2× to 4.0×) AND Logistical
Drag is **clogged** (3 to 6 blockades) AND Pressure State is
**flashpoint** (> 65).

**Delta cap: 0.10.** Clausewitzian friction has overwhelmed civil and
logistical execution. Ports, highways, factories, and sovereign policy
face acute disruption, capital controls, or emergency decrees. Trade
only if the AGOP ranking targets insulated offshore/digital IP or
direct physical-security/rerouting beneficiaries. In most cases, return
FLAT. 

#### CONTAGIOUS

Any of the following hold (and RUPTURE does not apply): 

* Contagion Regime is **contagious** (2.2× to 4.0×).
* Logistical Drag is **clogged** (3 to 6 blockades).
* Contagion Regime is **simmering** (1.3× to 2.2×) AND Pressure State
is **synchronized** or **flashpoint**.

**Delta cap: 0.25.** Granovetter threshold cascades or coordinated labor
and transport blockades are actively eroding physical throughput and
raising risk premia. Reduce position size substantially on domestic
equities, physical supply chains, and local currency exposure. 

#### STICKY

Any of the following hold (and neither RUPTURE nor CONTAGIOUS
applies): 

* Contagion Regime is **simmering** (1.3× to 2.2×).
* Logistical Drag is **sticky** (1 to 2 blockades/strikes).
* Pressure State is **pressurized** or **synchronized** while
Contagion Regime is **quiescent**.

**Delta cap: 0.75.** Sub-threshold resistance, localized strikes, or
focal-point tension are introducing measurable operational drag. Reduce
size relative to FRICTIONLESS. 

#### FRICTIONLESS

All of the following hold: 

* Contagion Regime is **quiescent** (< 1.3×).
* Logistical Drag is **clear** (0 blockades).
* Pressure State is **latent** or **watch** (< 35).

**Delta cap: 1.0.** Smooth civic and logistical execution; minimal
social friction drag. The cap equals the strategy cap; the skill never
binds on FRICTIONLESS. 

#### Ambiguous fallback

Any combination not covered above is classified **CONTAGIOUS** with delta
cap 0.25. 

#### Secondary Filter / Asymmetric Gate — Sustained Contagion Hysteresis

Apply the persistence test after state classification and before the
cap. 

A polity's social friction is **structurally entrenched** if
weeks_elevated_friction >= 3 (three or more consecutive settled weeks
with unrest_events_7d_ratio >= 2.0 or logistics_blockade_events_7d >= 3).
Three consecutive weeks of elevated disorder or transport blockades
proves that Kuran's preference falsification has broken irreversibly
within the current political cycle, exhausting state riot-control
capacity and inventory buffers. 

If the friction is **structurally entrenched**, halve the state's delta
cap: 

* STICKY cap of 0.75 becomes **0.375**.
* CONTAGIOUS cap of 0.25 becomes **0.125**.
* RUPTURE cap of 0.10 becomes **0.05**.

The gate is one-way. It cannot raise the cap; it can only lower it. 

#### The Procedure

Execute this procedure on every tick. Do not skip steps. 

1. **Read social friction dict.** From
snapshot.external_data["social_friction"], load the target region's
unrest_events_7d_ratio, logistics_blockade_events_7d,
gdelt_instability_tone, focal_point_active, and
weeks_elevated_friction. If absent or empty, record
**FRICTIONLESS**, note the omission, and do not cite this skill.
2. **Classify contagion regime.** Apply Reading 1 (quiescent,
simmering, contagious, or rupture).
3. **Classify logistical drag.** Apply Reading 2 (clear, sticky,
clogged, or severed).
4. **Classify pressure state.** Apply Reading 3 (latent, watch,
pressurized, synchronized, or flashpoint).
5. **Classify state.** Evaluate in strict priority order
(RUPTURE → CONTAGIOUS → STICKY → FRICTIONLESS) and select
the first matching state (fallback: CONTAGIOUS).
6. **Apply persistence test.** If weeks_elevated_friction >= 3, halve
delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta exceeded delta_cap),
cite "clausewitzian-social-friction" in skills_cited and state
the classification in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and cap reason.
Example: "CONTAGIOUS state; unrest ratio 2.8x baseline with 4 port/rail blockades and active focal point for 3 weeks; delta capped at 0.125; clausewitzian-social-friction."
• skills_cited: list of skill names; include
"clausewitzian-social-friction" only when the cap bound.

Worked Examples


Case A — Calm civic baseline with routine watch window, cap does not bind

Snapshot:
• unrest_events_7d_ratio = 0.95
• logistics_blockade_events_7d = 0
• gdelt_instability_tone = 22.0
• focal_point_active = true
• weeks_elevated_friction = 0
Readings:
• Contagion Regime: < 1.3× → quiescent
• Logistical Drag: 0 → clear
• Pressure State: < 35 + focal_point_active = true → watch
State: FRICTIONLESS, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "clausewitzian-social-friction".

Case B — Synchronized port/highway blockades with multi-week contagion, cap binds

Snapshot:
• unrest_events_7d_ratio = 3.1
• logistics_blockade_events_7d = 5
• gdelt_instability_tone = 58.0
• focal_point_active = true
• weeks_elevated_friction = 4
Readings:
• Contagion Regime: 2.2× to 4.0× → contagious
• Logistical Drag: 3 to 6 → clogged
• Pressure State: 35 to 65 + focal_point_active = true → synchronized
State: CONTAGIOUS, delta cap 0.25.
Persistence: weeks_elevated_friction = 4 >= 3 → halve to 0.125.
AGOP ranks LONG on a domestic logistics- or manufacturing-exposed
equity. LLM intended delta = 0.75. Cap 0.125 binds. LLM returns
delta = 0.125 and cites "clausewitzian-social-friction".

Free Data Sources

The fetcher populates snapshot.external_data["social_friction"] from
the following free, public endpoints (no paid subscription required):
• ACLED (Armed Conflict Location & Event Data Project):
https://acleddata.com (free API registration for researchers and
non-commercial/open-source developers; geo-tagged daily protest,
riot, strike, and blockade event counts globally).
• GDELT Project 2.0 Events & Global Knowledge Graph (GKG) API:
https://gdeltproject.org (completely free,
no-key REST API and BigQuery public dataset tracking protest/strike
event density, Goldstein conflict scales, and media tone every 15
minutes).
• Uppsala Conflict Data Program (UCDP) GED API:
https://uu.se (free, no-key REST API
maintained by Uppsala University providing standardized conflict
intensity and fatality thresholds).
• ILOSTAT Strikes and Lockouts Database (STR_DAYS / STR_WORK):
https://ilo.org (free open API tracking
industrial work stoppages and days not worked due to strikes by
country and sector).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not confuse routine, non-disruptive civic expression (< 1.3×
baseline and 0 transport blockades) with CONTAGIOUS friction.
• Do not cite "clausewitzian-social-friction" when the cap did not
bind.

Citation Mapping

• Clausewitzian Friction (Friktion): Carl von Clausewitz, On
War (Vom Kriege, 1832), Book I, Ch. 7 ("Friction in War").
Formalizes cumulative operational drag from minor environmental,
human, and administrative breakdowns.
• Threshold Contagion Models: Mark Granovetter, "Threshold Models
of Collective Behavior," American Journal of Sociology 83(6),
1420–1443 (1978). Establishes non-linear cascade transitions once
distributed instigation thresholds are crossed.
• Preference Falsification & Sudden Cascades: Timur Kuran, "Now
Out of Never: The Element of Surprise in the East European Revolution
of 1989," World Politics 44(1), 7–48 (1991); Private Truths,
Public Lies (Harvard University Press, 1995).
• Relative Deprivation & Repertoires of Contention: Ted Robert
Gurr, Why Men Rebel (Princeton University Press, 1970); Charles
Tilly, From Mobilization to Revolution (Addison-Wesley, 1978).
• Logistical Drag & Sub-Threshold Resistance: Martin van Creveld,
Supplying War (Cambridge University Press, 1977); James C. Scott,
Weapons of the Weak (Yale University Press, 1985).
• Focal-Point Synchronization: Thomas C. Schelling, The Strategy
of Conflict (Harvard University Press, 1960).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
Notice how cleanly this slots into your existing skills/ folder: it shares the exact four-state priority taxonomy (1.0 -> 0.75 -> 0.25 -> 0.10), the one-way persistence halving gate (0.05 floor), qualitative comparison tables built so a local 7B Qwen/DeepSeek model never has to divide floats, and zero paid data dependencies.
If you want to keep building out the ecosystem around this 17th skill, would you like:
• A reusable meta-prompt template you can paste into any AI when you want to generate future SKILL.md modules in this exact style
• The Python fetcher stub (janus/fetcher/social_friction.py) that queries the no-key GDELT 2.0 and Uppsala UCDP APIs to populate snapshot.external_data["social_friction"] automatically