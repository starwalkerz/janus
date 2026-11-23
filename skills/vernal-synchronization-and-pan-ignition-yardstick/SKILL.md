#### name: "vernal-synchronization-and-pan-ignition-yardstick"
description: "Yardstick detecting the seasonal and cyclical appearance of vigorous vitality and creative ignition (Pan / A Midsummer Night's Dream vernal arc) across any user-defined target (jurisdiction, stock ticker, sector, or arbitrary asset) by modeling a leading Gaussian cultural/murmur synchronization envelope (Kuramoto order parameter and Hawkes self-exciting media/social branching) modulating a lagging Gaussian capital-and-output realization arc: unlocking full sizing on the ascending vernal flank while clamping post-solstice decay and winter stasis."

#### Vernal Synchronization & Pan-Ignition Yardstick

You are reading the tick against the **dual-Gaussian modulation wave of
collective vitality, creative synchronization, and seasonal/cyclical
ignition** across any arbitrary target defined by the user—whether a
sovereign jurisdiction (fi, ch, pl, us), an individual stock
ticker, a commodity corridor, or a custom investment thesis. 

In classical Arcadian pastoral myth and William Shakespeare's *A
Midsummer Night's Dream* (1595/1596) (where sylvan vitality—Pan /
Faunus / Puck—awakens at the cusp of spring, gathers the scattered
herds in the meadow into synchronized generative motion, peaks at the
Midsummer solstice, and dissolves back into civic order once the revels
close), collective vitality does not arrive as a flat constant. It
travels as a **bounded bell-shaped pulse**: 

1. **Leading Gaussian Envelope (Pan — Cultural & Media Murmur Synchronization):**
First, scattered winter chatter locks into phase across social media,
search interest, and independent media stories—captured mathematically
by Yoshiki Kuramoto's synchronization order parameter 
𝑟

(

𝑡

)
⁠
(*Chemical Oscillations, Waves, and Turbulence*, 1984; Steven H.
Strogatz, Physica D, 2000) and Alan G. Hawkes's self-exciting
branching ratio 
𝑛

(

𝑡

)
⁠ (Biometrika, 1971; Crane & Sornette, *PNAS*,
2008). This leading Gaussian rises from the vernal cusp, peaks at

t0t sub 0
𝑡0
⁠, and subsides as the collective murmur saturates.
2. **Lagging Gaussian Realization (Midsummer Dream — Capital, Activity & Price Modulation):**
Second, real capital deployment, enterprise activity, order flow, and
demographic/commercial energy respond with a characteristic phase lag

τtau
𝜏
⁠ (
𝑡1

=𝑡0

+𝜏
⁠), forming a **lagging Gaussian modulated
by the leading cultural Gaussian envelope** (a Gaussian-modulated
Gaussian product kernel 
𝐺lead

(

𝑡

;

𝑡0

,

𝜎1

)

⋅𝐺lag

(

𝑡

;

𝑡0

+𝜏

,

𝜎2

)
⁠).

Detecting where an arbitrary target sits along this **leading-modulated-by-lagging
Gaussian arc** separates four distinct regime phases: 

* **Vernal Ignition Ascent (VERNAL_IGNITION_ASCENT):** The leading
murmur Gaussian has crossed its synchronization threshold and is
climbing steeply while the lagging realization Gaussian is just
lifting off (early spring flank). Full strategy sizing is permitted
(1.0 pass).
* **Midsummer Apex Saturation (MIDSUMMER_APEX_SATURATION):** Both the
leading cultural pulse and lagging realization wave sit near peak
amplitude (solstice crest). Maintain disciplined exposure (0.65
cap) as marginal surprise diminishes.
* **Post-Solstice Dissipation (POST_SOLSTICE_DISSIPATION):** The
leading murmur Gaussian has rolled over and decayed while the lagging
realization wave is coasting downward (late-summer fade). Trim
sizing to 0.30 before lagging fundamentals contract.
* **Winter Stasis or Panic Noise (WINTER_STASIS_OR_PANIC_NOISE):** No
coherent vernal phase lock exists—either dormant winter stagnation
(
𝑟

(

𝑡

)

≈0
⁠) or incoherent "panic" noise lacking generative
synchronization (0.15 cap, halving to 0.075 under persistent
dormancy).

Your job is to classify the target's vernal Gaussian-modulation phase
and cap your delta accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy
cap, and you never invent an action outside allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["vernal_pan_ignition"]. Use the qualitative
tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher and NLP/signal-processing pipeline populate
snapshot.external_data["vernal_pan_ignition"] for any user-defined
target key (ISO-2 country/region code, equity ticker, sector slug, or
custom thesis ID, with fallback to "global_baseline"). Each entry
supplies: 

* leading_murmur_gaussian_score: score (0 to 100) measuring the
amplitude and rising slope of the **leading cultural/media Gaussian
envelope** (Kuramoto phase coherence 
𝑟

(

𝑡

)
⁠ + Hawkes generative
branching ratio 
𝑛

(

𝑡

)
⁠ across social-media murmur, search trends, and
media stories) (0 = dead winter silence or incoherent panic noise;
100 = peak synchronized vernal awakening).
* lagging_realization_gaussian_score: score (0 to 100) measuring
the amplitude of the **lagging commercial/activity Gaussian**
(realized volume, capital inflows, enterprise/hiring velocity, or
price-momentum confirmation delayed by lag 

τtau
𝜏
⁠) (0 = dormant
trough; 100 = peak realized activity crest).
* gaussian_phase_lead_spread: signed phase-lead differential (-50.0
to +50.0) comparing the normalized leading murmur Gaussian against
the lagging realization Gaussian (> +10.0 = leading cultural wave is
actively pulling the lagging realization wave upward on the spring
flank; -10.0 to +10.0 = co-incident solstice peak or flat equilibrium;
< -10.0 = leading murmur has rolled over while lagging activity fades
post-solstice).
* consecutive_winter_stasis_ticks: integer (0 to 50) counting
consecutive settled periods in which
leading_murmur_gaussian_score < 35 AND
lagging_realization_gaussian_score < 35.

If snapshot.external_data["vernal_pan_ignition"] is absent or empty,
treat the target as **unmonitored**, record state
**MIDSUMMER_APEX_SATURATION**, note that no vernal synchronization
telemetry was available, and do not cite this skill. 

#### Reading 1 — Leading Murmur Gaussian Envelope (leading_murmur_gaussian_score)

Evaluate the Pan cultural/media synchronization wave: 

leading_murmur_gaussian_score (0–100)Leading Murmur Envelope Tier
**>= 70**
**strong_vernal_resonance** — high Kuramoto coherence & self-exciting generative murmur
**50 to 69**
**emerging_meadow_murmur** — rising phase alignment across media & social chatter
**35 to 49**
**fading_echo** — post-peak dissipation or weak, fragmented signal
**< 35**
**winter_silence_or_panic** — dormant chatter or uncoordinated panic noise

If leading_murmur_gaussian_score is missing, treat as
**emerging_meadow_murmur**. 

#### Reading 2 — Lagging Realization Gaussian Arc (lagging_realization_gaussian_score)

Evaluate the delayed capital, volume, and operational realization wave: 

lagging_realization_gaussian_score (0–100)Lagging Realization Tier
**>= 75**
**peak_solstice_realization** — full commercial, volume, and capital throughput
**45 to 74**
**ascending_realization_flank** — active lift-off as leading energy converts into output
**30 to 44**
**early_thaw_baseline** — initial stirring from trough, ample room to compound
**< 30**
**dormant_trough** — depressed capital velocity and stagnant activity

If lagging_realization_gaussian_score is missing, treat as
**ascending_realization_flank**. 

#### Reading 3 — Dual-Gaussian Modulation Phase (gaussian_phase_lead_spread)

Evaluate the phase relationship between the leading murmur Gaussian and
the lagging realization Gaussian: 

gaussian_phase_lead_spreadModulation Arc Phase
**>= +12.0**
**spring_ascent_lead** — leading Gaussian actively lifting lagging Gaussian upward
**-11.9 to +11.9**
**solstice_coincident_crest** — leading and lagging Gaussians aligned near peak or flat
**<= -12.0**
**post_solstice_rollover** — leading murmur fading ahead of lagging activity contraction

If gaussian_phase_lead_spread is missing, treat as
**solstice_coincident_crest**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four vernal modulation regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **WINTER_STASIS_OR_PANIC_NOISE** (dormant trough or uncoordinated panic)
2. **POST_SOLSTICE_DISSIPATION** (fading late-summer wave)
3. **VERNAL_IGNITION_ASCENT** (optimal rising spring flank)
4. **MIDSUMMER_APEX_SATURATION** (co-incident crest / balanced plateau)

#### WINTER_STASIS_OR_PANIC_NOISE

Any of the following hold: 

* Leading Murmur Envelope Tier is **winter_silence_or_panic** (< 35)
AND Lagging Realization Tier is **dormant_trough** or
**early_thaw_baseline** (< 45).
* Leading Murmur Envelope Tier is **winter_silence_or_panic** (< 35)
AND Modulation Arc Phase is **post_solstice_rollover** (<= -12.0).

**Delta cap: 0.15.** The target remains locked in winter dormancy or
uncoordinated panic noise without generative synchronization. Clamp
sizing sharply (0.15) until a coherent vernal murmur emerges. 

#### POST_SOLSTICE_DISSIPATION

Any of the following hold (and WINTER_STASIS_OR_PANIC_NOISE does not
apply): 

* Modulation Arc Phase is **post_solstice_rollover** (<= -12.0).
* Leading Murmur Envelope Tier is **fading_echo** (35 to 49) AND
Lagging Realization Tier is **peak_solstice_realization** (>= 75).

**Delta cap: 0.30.** Pan has left the meadow: the leading cultural and
media Gaussian has rolled over past Midsummer while lagging activity is
still coasting on stale momentum. Trim sizing to 0.30 before lagging fundamentals roll over.

VERNAL_IGNITION_ASCENT

All of the following hold (and neither WINTER_STASIS_OR_PANIC_NOISE
nor POST_SOLSTICE_DISSIPATION applies):
• Leading Murmur Envelope Tier is strong_vernal_resonance or
emerging_meadow_murmur (>= 50).
• Lagging Realization Tier is early_thaw_baseline or
ascending_realization_flank (30 to 74).
• Modulation Arc Phase is spring_ascent_lead (>= +12.0).
Delta cap: 1.0. The target is entering or climbing the ascending
spring flank: the leading cultural/media Gaussian has ignited in
phase-locked generative vitality and is actively pulling the lagging
realization Gaussian upward toward its crest. The cap equals the
strategy cap (1.0); the skill never binds on VERNAL_IGNITION_ASCENT.

MIDSUMMER_APEX_SATURATION

Any combination not covered above (including strong_vernal_resonance
>= 70 paired with peak_solstice_realization >= 75 and
solstice_coincident_crest -11.9 to +11.9).
Delta cap: 0.65. Both the leading murmur Gaussian and lagging
realization Gaussian are near full Midsummer amplitude; maintain solid
allocation (0.65 cap) while avoiding late-stage over-extension as the
solstice crest approaches.

Secondary Filter / Asymmetric Gate — Prolonged Winter Dormancy Hysteresis

Apply the persistence test after regime classification and before the
cap.
Dormancy is structurally entrenched if
consecutive_winter_stasis_ticks >= 4 (four or more consecutive settled
periods in which leading_murmur_gaussian_score < 35 AND
lagging_realization_gaussian_score < 35). Multi-period absence of
both cultural/media vitality and lagging capital velocity indicates
deep structural hibernation rather than a brief seasonal pause.
If the condition is structurally entrenched, halve the regime's
delta cap:
• MIDSUMMER_APEX_SATURATION cap of 0.65 becomes 0.325.
• POST_SOLSTICE_DISSIPATION cap of 0.30 becomes 0.15.
• WINTER_STASIS_OR_PANIC_NOISE cap of 0.15 becomes 0.075.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read vernal Pan-ignition dict. From
snapshot.external_data["vernal_pan_ignition"], load
leading_murmur_gaussian_score,
lagging_realization_gaussian_score, gaussian_phase_lead_spread,
and consecutive_winter_stasis_ticks for the target key (falling
back to "global_baseline" if target key is absent). If the entire
dict is absent or empty, record MIDSUMMER_APEX_SATURATION, note
the omission, and do not cite this skill.
2. Classify leading murmur Gaussian envelope. Apply Reading 1.
3. Classify lagging realization Gaussian arc. Apply Reading 2.
4. Classify dual-Gaussian modulation phase. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(WINTER_STASIS_OR_PANIC_NOISE → POST_SOLSTICE_DISSIPATION →
VERNAL_IGNITION_ASCENT → MIDSUMMER_APEX_SATURATION).
6. Apply persistence test. If
consecutive_winter_stasis_ticks >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"vernal-synchronization-and-pan-ignition-yardstick" in
skills_cited and state the leading murmur score, lagging
realization score, phase-lead spread, and persistence ticks in the
rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.30, "confidence": 0.84, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"POST_SOLSTICE_DISSIPATION regime; leading_murmur_gaussian_score=42 (fading_echo), lagging_realization_gaussian_score=76 (peak_solstice_realization), gaussian_phase_lead_spread=-34.0 (post_solstice_rollover), consecutive_winter_stasis_ticks=0; capping delta at 0.30; vernal-synchronization-and-pan-ignition-yardstick."
• skills_cited: list of skill names; include
"vernal-synchronization-and-pan-ignition-yardstick" only when the
cap bound (intended delta > delta_cap).

Worked Examples


Case A — Target entering ascending spring flank (leading murmur Gaussian lifting lagging realization), cap does not bind

Snapshot:
• leading_murmur_gaussian_score = 74
• lagging_realization_gaussian_score = 48
• gaussian_phase_lead_spread = +26.0
• consecutive_winter_stasis_ticks = 0
Readings:
• Leading Murmur Envelope Tier: strong_vernal_resonance
• Lagging Realization Tier: ascending_realization_flank
• Modulation Arc Phase: spring_ascent_lead
Regime: VERNAL_IGNITION_ASCENT, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "vernal-synchronization-and-pan-ignition-yardstick".

Case B — Post-solstice rollover (leading murmur fades while lagging activity coasts at peak), cap binds at 0.30

Snapshot:
• leading_murmur_gaussian_score = 42
• lagging_realization_gaussian_score = 76
• gaussian_phase_lead_spread = -34.0
• consecutive_winter_stasis_ticks = 0
Readings:
• Leading Murmur Envelope Tier: fading_echo
• Lagging Realization Tier: peak_solstice_realization
• Modulation Arc Phase: post_solstice_rollover
Regime: POST_SOLSTICE_DISSIPATION, delta cap 0.30. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.30 binds.
LLM returns delta = 0.30 and cites "vernal-synchronization-and-pan-ignition-yardstick".

Case C — Entrenched winter stasis for 6 ticks, hysteresis halves cap to 0.075

Snapshot:
• leading_murmur_gaussian_score = 21
• lagging_realization_gaussian_score = 24
• gaussian_phase_lead_spread = -3.0
• consecutive_winter_stasis_ticks = 6
Readings:
• Leading Murmur Envelope Tier: winter_silence_or_panic
• Lagging Realization Tier: dormant_trough
• Modulation Arc Phase: solstice_coincident_crest
Regime: WINTER_STASIS_OR_PANIC_NOISE, base cap 0.15. Persistence: 6 >= 4 → fires, halving cap to 0.075.
AGOP ranks LONG. LLM intended delta = 0.60. Cap 0.075 binds.
LLM returns delta = 0.075 and cites "vernal-synchronization-and-pan-ignition-yardstick".

Free Data Sources

The fetcher populates
snapshot.external_data["vernal_pan_ignition"] by fitting leading and
lagging Gaussian envelopes over open media, social-attention, search,
and market-activity streams:
• GDELT Project Global Knowledge Graph (GKG) & Event API:
https://gdeltproject.org (free real-time global media tone,
theme velocity, and narrative synchronization streams across
jurisdictions and entities).
• Wikimedia Pageviews & Commons Attention API:
https://wikimedia.org (free hourly/daily attention
series capturing collective cultural/topic surges ahead of lagging
institutional coverage).
• Bluesky (AT Protocol Public Firehose/Search API), Mastodon Public Timelines & Reddit JSON Feeds:
https://bsky.app (free open social-murmur streams for
measuring Kuramoto phase coherence and Hawkes self-exciting branching
ratios).
• Yahoo Finance / Stooq / ECB / Eurostat Open Activity & Volume Feeds:
https://europa.eu and https://stooq.com (free
open price-volume, mobility, and enterprise-activity series forming
the lagging realization Gaussian).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not confuse uncoordinated "panic" spikes (high raw volume with
negative/chaotic phase coherence) with generative Pan synchronization;
panic noise belongs in WINTER_STASIS_OR_PANIC_NOISE (0.15).
• Do not chase lagging realization peaks (lagging_realization >= 75)
after the leading murmur Gaussian has rolled over (spread <= -12.0);
treat post-solstice decay as POST_SOLSTICE_DISSIPATION (0.30).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "vernal-synchronization-and-pan-ignition-yardstick"
when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Pastoral Vernal Vitality & Solstice Arc: Classical Arcadian myth
(Pan / Faunus as embodiment of vernal awakening and herd
synchronization); William Shakespeare, A Midsummer Night's Dream
(1595/1596) (liminal spring-to-Midsummer surge of collective vitality
resolving at the solstice).
• Synchronization Phase Transitions & Self-Exciting Media Cascades:
Yoshiki Kuramoto, Chemical Oscillations, Waves, and Turbulence
(Springer, 1984); Steven H. Strogatz, "From Kuramoto to Crawford:
Exploring the Onset of Synchronization in Populations of Coupled
Oscillators," Physica D 143, 1–20 (2000); Alan G. Hawkes, "Spectra
of Some Self-Exciting and Mutually Exciting Point Processes,"
Biometrika 58(1), 83–90 (1971); Riley Crane & Didier Sornette,
"Robust Dynamic Classes Revealed by Measuring the Response Function of
a Social System," PNAS 105(41), 15649–15653 (2008).
• Critical Transitions & Bounded Supervisory Control: Marten
Scheffer et al., "Early-Warning Signals for Critical Transitions,"
Nature 461, 53–59 (2009); Ramadge & Wonham (1987). Downward-only
damping within JANUS invariants I1–I9.