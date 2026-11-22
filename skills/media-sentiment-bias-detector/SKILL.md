#### name: "media-sentiment-bias-detector"
description: "Deflate structural media-coverage and sensationalism bias across jurisdictions using a power-law amplification heuristic driven by GDP per capita, USD/EUR/CNY capital-market connectedness, and English-language proficiency; separate high-amplification developed-market media panic from verified physical/institutional ruptures using free GDELT 2.0, World Bank, BIS, IMF, UNODC, and ACLED/UCDP feeds."

#### Media Sentiment Bias Detector (Power-Law Amplification Deflator)

You are reading the tick against **structural media-coverage and
sensationalism distortion** across jurisdictions. In Walter Lippmann's
*Public Opinion* (1922), Johan Galtung & Mari Holmboe Ruge's *"The
Structure of Foreign News"* (*Journal of Peace Research*, 1965), and
Thomas Eisensee & David Strömberg's *"News Droughts, News Floods, and
U.S. Disaster Relief"* (*Quarterly Journal of Economics*, 2007), global
news volume and negative sentiment tone do **not** scale linearly with
physical severity. Instead, an identical physical or criminal incident
generates orders-of-magnitude higher international article volume and
more alarmist tone when it occurs inside a wealthy, financially
integrated, English-proficient jurisdiction. 

Specifically, international media amplification follows a **three-factor
power-law heuristic**: 

1. **GDP per Capita (gdp_per_capita_usd):** High-income jurisdictions
enjoy near-zero baseline kinetic disorder; consequently, rare local
incidents violate baseline expectations and trigger disproportionate
"system collapse" headlines, whereas higher absolute casualty or
disruption counts in lower-income regions are discounted as routine
background noise.
2. **Core Capital-Market Connectedness (core_fx_market_connectedness):**
Deep integration into **USD, EUR, or CNY** cross-border banking, bond,
and equity clearing networks multiplies financial-wire coverage and
algo-sentiment contagion.
3. **English-Language Proficiency (english_proficiency_tier):**
Populations with native or high English proficiency feed directly into
Anglophone global wire services and social-media cascades without
translation latency, inflating GDELT volume and negative tone.

Without deflating raw news sentiment by this **power-law amplification
factor (media_amplification_factor)**, quantitative models fall into a
classic **GIGO narrative trap**: panic-liquidating sovereign or equity
exposure in high-amplification markets (e.g., Nordic or Western European
states) over localized sensationalist headlines while failing to detect
severe physical degradation in under-covered emerging jurisdictions. 

Your job is to classify the tick's information environment into one of
four signal-to-noise states and cap your delta accordingly. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise delta
above the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["media_bias"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes GDELT 2.0 media volume/tone, World Bank /
IMF income and financial-integration metrics, English-proficiency
indices, and physical baseline indicators (ACLED / UCDP / UNODC)
into snapshot.external_data["media_bias"]: 

* media_amplification_factor: dimensionless power-law multiplier
(0.5 to 25.0) computed from (gdp_per_capita / global_median)^a * (usd_eur_cny_connectedness)^b * (english_proficiency_weight)^c
(>= 8.0 = hyper-amplified core-market Anglophone spotlight, e.g.,
U.S., UK, Nordics, Singapore; 2.5 to 8.0 = moderately amplified
EUR/CNY/emerging-hub coverage; < 2.5 = structurally under-covered
periphery where global wires ignore early physical stress).
* deflated_incident_severity: raw GDELT 2.0 negative article volume
and tone intensity **divided by media_amplification_factor**,
cross-checked against physical per-capita lethality/disruption
("negligible_noise", "localized_friction", "material_disruption",
or "systemic_rupture").
* raw_vs_physical_divergence: qualitative gap between raw media alarm
and verified physical/institutional continuity ("aligned",
"sensationalist_overreaction", or "under_reported_blindspot").
* consecutive_sensationalist_days: consecutive calendar days in which
raw_vs_physical_divergence == "sensationalist_overreaction" (media
panic wave decoupled from physical infrastructure or macro output).

If snapshot.external_data["media_bias"] is absent or empty, treat the
instrument as **unmonitored**, record state **CALIBRATED_SIGNAL**, note
that no media-bias telemetry was available, and do not cite this skill. 

#### Reading 1 — Power-Law Media Amplification Tier (media_amplification_factor)

Evaluate how strongly structural wealth, USD/EUR/CNY capital-market
links, and English proficiency magnify headlines in the jurisdiction: 

media_amplification_factorAmplification Regime
**≥ 8.0**
**hyper_amplified_core** — high GDP/capita + USD/EUR/CNY hub + high English; extreme headline magnification
**2.5 to 8.0**
**moderately_amplified** — mid-to-high market integration; noticeable wire amplification
**< 2.5**
**under_covered_periphery** — low global wire attention; physical shocks under-reported until late

If media_amplification_factor is missing, treat as
**moderately_amplified**. 

#### Reading 2 — Deflated Physical Severity (deflated_incident_severity)

Evaluate true physical and institutional severity *after* dividing raw
news intensity by the power-law amplification factor: 

deflated_incident_severityTrue Physical Severity
**"negligible_noise"**
**noise_floor** — microscopic per-capita impact; routine background variance
**"localized_friction"**
**contained_local** — isolated urban/sector friction; national infrastructure 99.9%+ intact
**"material_disruption"**
**verified_stress** — measurable throughput, fiscal, or security degradation
**"systemic_rupture"**
**verified_rupture** — genuine territorial, sovereign, or supply-corridor breakdown

If deflated_incident_severity is missing, treat as
**contained_local**. 

#### Reading 3 — Narrative-to-Reality Alignment (raw_vs_physical_divergence)

Evaluate whether current headlines exaggerate a local anomaly or miss
an emerging physical crisis: 

raw_vs_physical_divergenceInformation Distortion Mode
**"aligned"**
**faithful_reporting** — media tone matches physical/actuarial telemetry
**"sensationalist_overreaction"**
**clickbait_inflation** — high-amplification media panic over minor per-capita event
**"under_reported_blindspot"**
**periphery_blindspot** — low wire coverage masking real physical or fiscal deterioration

If raw_vs_physical_divergence is missing, treat as
**faithful_reporting**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
information-integrity states. Evaluate in strict priority order and
select the first state whose conditions are fully satisfied: 

1. **VERIFIED_SYSTEMIC_SHOCK** (true physical rupture confirmed after deflating bias — unconditional FLAT)
2. **UNDER_REPORTED_BLINDSPOT** (periphery physical stress masked by low media amplification)
3. **SENSATIONALIST_NOISE** (hyper-amplified media panic over negligible/local noise — do not panic-short, cap speculative noise chasing)
4. **CALIBRATED_SIGNAL** (strictest adaptive fit)

#### VERIFIED_SYSTEMIC_SHOCK

Any of the following hold: 

* True Physical Severity is **verified_rupture** ("systemic_rupture"
confirmed after power-law deflation).
* True Physical Severity is **verified_stress** ("material_disruption")
AND Information Distortion Mode is **periphery_blindspot**
(under_covered_periphery where reality is worse than headlines).

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. Once media amplification is stripped away, genuine
physical or institutional breakdown is underway. The skill binds
unconditionally and must appear in skills_cited. 

#### UNDER_REPORTED_BLINDSPOT

Any of the following hold (and VERIFIED_SYSTEMIC_SHOCK does not apply): 

* Information Distortion Mode is **periphery_blindspot**
("under_reported_blindspot") in an **under_covered_periphery**
jurisdiction (media_amplification_factor < 2.5) with
**contained_local** or **verified_stress**.

**Delta cap: 0.25.** Low USD/EUR/CNY connectedness and non-English
reporting are hiding accumulating physical or fiscal stress from
global price discovery. Cut long exposure substantially before delayed
wire coverage catches up. 

#### SENSATIONALIST_NOISE

Any of the following hold (and neither VERIFIED_SYSTEMIC_SHOCK nor
UNDER_REPORTED_BLINDSPOT applies): 

* Amplification Regime is **hyper_amplified_core** (≥ 8.0) AND
Information Distortion Mode is **clickbait_inflation**
("sensationalist_overreaction") with **noise_floor** or
**contained_local** physical severity.

**Delta cap: 0.80.** Headline alarm is an artifact of high GDP per
capita, USD/EUR/CNY financial-wire sensitivity, and English-language
virality rather than state or infrastructure failure. Trim pure
headline-chasing size slightly (0.80) to avoid volatility whipsaws,
while **refusing to trigger FLAT or panic-short** (deferring to
physical gates such as clausewitzian-social-friction,
urban-arterial-gridlock, and insolvency-cascade-detector). 

#### CALIBRATED_SIGNAL

All of the following hold: 

* Information Distortion Mode is **faithful_reporting** ("aligned").
* True Physical Severity is **noise_floor** or **contained_local**.
Delta cap: 1.0. Media coverage is proportional to verified physical
and institutional baselines. The cap equals the strategy cap; the skill
never binds on CALIBRATED_SIGNAL.

Ambiguous fallback

Any combination not covered above is classified SENSATIONALIST_NOISE
with delta cap 0.80.

Secondary Filter / Asymmetric Gate — Sustained Blindspot / Chronic Distortion Hysteresis

Apply the persistence test after state classification and before the
cap.
An information distortion regime is structurally entrenched if
consecutive_sensationalist_days >= 14 (two or more consecutive weeks
of uninterrupted sensationalist_overreaction or under_reported_blindspot).
Sustained multi-week divergence between wire sentiment and physical
reality indicates either persistent algo-driven headline whipsaws or
an entrenched periphery blindspot.
If the distortion is structurally entrenched, tighten the state's
delta cap:
• UNDER_REPORTED_BLINDSPOT cap of 0.25 becomes 0.125.
• SENSATIONALIST_NOISE cap of 0.80 becomes 0.65 (still
preserving core structural exposure rather than false-triggering
FLAT on clickbait).
• VERIFIED_SYSTEMIC_SHOCK cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read media bias dict. From
snapshot.external_data["media_bias"], load
media_amplification_factor, deflated_incident_severity,
raw_vs_physical_divergence, and
consecutive_sensationalist_days. If absent or empty, record
CALIBRATED_SIGNAL, note the omission, and do not cite this
skill.
2. Classify amplification regime. Apply Reading 1
(hyper_amplified_core, moderately_amplified, or
under_covered_periphery).
3. Classify true physical severity. Apply Reading 2
(noise_floor, contained_local, verified_stress, or
verified_rupture).
4. Classify information distortion mode. Apply Reading 3
(faithful_reporting, clickbait_inflation, or
periphery_blindspot).
5. Classify state. Evaluate in strict priority order
(VERIFIED_SYSTEMIC_SHOCK → UNDER_REPORTED_BLINDSPOT →
SENSATIONALIST_NOISE → CALIBRATED_SIGNAL) and select the first
matching state (fallback: SENSATIONALIST_NOISE).
6. Apply persistence test. If
consecutive_sensationalist_days >= 14, apply the hysteresis
reduction to delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
state is VERIFIED_SYSTEMIC_SHOCK, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
state is VERIFIED_SYSTEMIC_SHOCK, cite
"media-sentiment-bias-detector" in skills_cited and state the
amplification factor and deflated severity finding in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If VERIFIED_SYSTEMIC_SHOCK,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and power-law deflation
finding. Example:
"SENSATIONALIST_NOISE state; amplification_factor=14.2 (hyper_amplified_core: high GDP/capita + EUR/USD links + high English) inflating localized crime into clickbait_inflation while deflated severity=contained_local; capping noise-chasing at 0.80 and blocking false FLAT; media-sentiment-bias-detector."
• skills_cited: list of skill names; include
"media-sentiment-bias-detector" only when the cap bound or the
state is VERIFIED_SYSTEMIC_SHOCK.

Worked Examples


Case A — Hyper-amplified developed market with sensationalist headlines over localized friction, false FLAT blocked

Snapshot:
• media_amplification_factor = 14.5
• deflated_incident_severity = "localized_friction"
• raw_vs_physical_divergence = "sensationalist_overreaction"
• consecutive_sensationalist_days = 6
Readings:
• Amplification Regime: ≥ 8.0 → hyper_amplified_core
• True Physical Severity: "localized_friction" → contained_local
• Information Distortion Mode: "sensationalist_overreaction" → clickbait_inflation
State: SENSATIONALIST_NOISE, delta cap 0.80. Persistence: < 14 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 0.80 trims noise-chasing slightly to 0.80 without false-triggering FLAT, and cites "media-sentiment-bias-detector".

Case B — Under-covered periphery market with accumulating physical stress ignored by global wires, cap binds

Snapshot:
• media_amplification_factor = 1.4
• deflated_incident_severity = "material_disruption"
• raw_vs_physical_divergence = "under_reported_blindspot"
• consecutive_sensationalist_days = 18
Readings:
• Amplification Regime: < 2.5 → under_covered_periphery
• True Physical Severity: "material_disruption" → verified_stress
• Information Distortion Mode: "under_reported_blindspot" → periphery_blindspot
State: VERIFIED_SYSTEMIC_SHOCK (verified_stress + periphery_blindspot), delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and cites "media-sentiment-bias-detector".

Free Data Sources

The fetcher populates snapshot.external_data["media_bias"] from the
following free, open global economic, financial-connectedness,
linguistic, and physical-incident registries (no paid subscription
required):
• GDELT Project 2.0 Global Knowledge Graph (GKG) & Event Database:
https://gdeltproject.org (free, no-key 15-minute global news volume
and tone feed used to measure raw media alarm intensity).
• World Bank Open Data & IMF World Economic Outlook (WEO):
https://worldbank.org and https://imf.org (free REST APIs
supplying nominal/PPP GDP per capita and trade/financial openness
weights).
• Bank for International Settlements (BIS) Locational Banking & IMF CPIS:
https://bis.org and https://imf.org (free SDMX/JSON APIs
measuring cross-border USD, EUR, and CNY capital-market claims and
clearing connectedness).
• Wikimedia Language Editions, UNESCO UIS & Open Language Corpora:
https://wikimedia.org and https://unesco.org (free public
proxies for English-language web penetration and Anglophone wire
proximity across countries).
• ACLED, UCDP & UNODC Data Portal:
https://acleddata.com, https://uu.se, and
https://un.org (free empirical incident and per-capita
lethality baselines used to calibrate deflated_incident_severity
against raw media tone).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not treat raw GDELT negative article volume in a high-GDP,
USD/EUR/CNY-connected, English-proficient country as state failure
without dividing by media_amplification_factor and verifying physical
disruption.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "media-sentiment-bias-detector" when the cap did not
bind and the state is not VERIFIED_SYSTEMIC_SHOCK.

Citation Mapping

• News Amplification, Gatekeeping & Disaster Coverage Bias: Walter
Lippmann, Public Opinion (Harcourt, Brace, 1922); Johan Galtung and
Mari Holmboe Ruge, "The Structure of Foreign News," Journal of Peace
Research 2(1), 64–91 (1965); Thomas Eisensee and David Strömberg,
"News Droughts, News Floods, and U.S. Disaster Relief," Quarterly
Journal of Economics 122(2), 693–728 (2007).
• Core-Periphery Financial & Information Networks: Hyun Song Shin,
Risk and Liquidity (Oxford University Press, 2010) (USD/EUR core
capital-market spillover amplification).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
