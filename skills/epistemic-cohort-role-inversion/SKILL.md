---
name: "epistemic-cohort-role-inversion"
description: "Classify the tick by which demographic age cohort occupies the leading cultural/aesthetic Gaussian versus the lagging regulatory/consumption Gaussian across three aggregate cohorts—20–29 (default cultural generator), 30–39 (default flat liminal bridge whose lead signals phase shift and whose lag signals ossification), and 40–49 (default lagging environmental steward/regulator)—separating aggregate cohort roles from individual variance, with optional non-blocking corroboration from liminal-pendulum and shibboleth-panic telemetry; cap delta when cohort role inversion or ossification distorts natural cultural transmission."
---

# Epistemic Cohort Role Inversion

You are reading the tick against the **demographic cohort occupancy of the leading and lagging cultural Gaussians**.

Drawing on Karl Mannheim's *The Problem of Generations* (1928) on generational entelechy and formative cohort consciousness, Ronald Inglehart's *Culture Shift in Advanced Industrial Society* (1990) on generational value replacement, Pierre Bourdieu's *Distinction* (1984) on aesthetic vanguard versus institutional consecration, and Kuramoto/Hawkes synchronization envelopes, cultural and consumer vitality depends on **which age cohort occupies the leading cultural-ignition Gaussian ($G_{\text{lead}}$) versus the lagging regulatory/monetization Gaussian ($G_{\text{lag}}$)**.

Crucially, this yardstick evaluates **aggregate cohort behavior, strictly separated from individual variance**:
* An individual 40–49 year old may be a cultural innovator, and an individual 20–29 year old may be prudish or conventional—yet **in the aggregate**, statistical ensembles follow distinct structural roles:

### The Three Aggregate Cohort Roles

1. **20–29 Cohort (`cohort_20_29` — Default Cultural & Norm Generator):**
   * In any healthy, dynamic society or era, the 20–29 aggregate occupies the **leading Gaussian ($G_{\text{lead}}$)**. Free from mid-life institutional lock-in, their aggregate drives pop culture, aesthetic novelty, nightlife electricity, slang, and unpoliced social openness (the exact opposite of prudishness in the aggregate).
2. **40–49 Cohort (`cohort_40_49` — Default Lagging Regulator & Steward):**
   * In the default baseline, the 40–49 aggregate occupies the **lagging Gaussian ($G_{\text{lag}}$)**. They fund, institutionalize, monetize, and regulate the environment (licensing, zoning, corporate governance, norm-policing) roughly one decade behind 20–29 ignition.
3. **30–39 Cohort (`cohort_30_39` — The Liminal Bridge Cohort):**
   * **Default state (`flat` / neutral):** In normal equilibrium, the 30–39 aggregate occupies **neither** Gaussian—acting as a flat transitional bridge between youthful cultural generation and mid-life institutional stewardship.
   * **Anomaly A — 30–39 Leading ($G_{\text{lead}} = \text{cohort\_30\_39}$):** When 30–39s occupy the leading Gaussian, it signals an **active phase shift** (either a late-blooming counter-rebellion breaking out of stale norms, or a defensive/moralizing re-ordering when 20–29 ignition has been suppressed or gated out).
   * **Anomaly B — 30–39 Lagging ($G_{\text{lag}} = \text{cohort\_30\_39}$):** When 30–39s occupy the lagging Gaussian (prematurely acting as heavy norm-policers, `K-30` aesthetic gatekeepers, or stale cliché curators ahead of 40–49s), it signals **premature cultural ossification**—choking off the aspirational pipeline from 20–29s and turning vibrant scenes into dated clichés.

Your job is to classify the tick's cohort role configuration and cap `delta` accordingly. You do not invent trades. You do not override AGOP. You modulate the LLM's `delta` within the bound the verifier already permits. You never raise `delta` above the strategy cap, and you never invent an action outside `allowed_actions`.

---

## The Readings

Compute three core readings from `snapshot.external_data["cohort_role_inversion"]`, plus an optional, non-mandatory check on `liminal_pendulum` and `shibboleth_panic` if present. Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher and demographic/attention pipeline populate `snapshot.external_data["cohort_role_inversion"]` using cohort-stratified search, social-murmur, and consumer-activity streams:

* `leading_gaussian_cohort`: string identifying which aggregate cohort currently dominates the leading cultural/aesthetic ignition Gaussian ($G_{\text{lead}}$): `"cohort_20_29"`, `"cohort_30_39"`, `"cohort_40_49"`, or `"flat_none"`.
* `lagging_gaussian_cohort`: string identifying which aggregate cohort currently dominates the lagging institutional/regulatory/monetization Gaussian ($G_{\text{lag}}$): `"cohort_40_49"`, `"cohort_30_39"`, `"cohort_20_29"`, or `"flat_none"`.
* `cohort_30_39_slope`: signed velocity (`-50.0` to `+50.0`) measuring whether the liminal 30–39 cohort is flat (`-10.0 to +10.0`), surging into cultural/aesthetic leadership (`> +10.0`), or hardening into premature gatekeeping/lagging curation (`< -10.0`).
* `youth_pipeline_coupling_score`: score (`0` to `100`) measuring whether 20–29 cultural ignition is flowing naturally into commercial/social spaces (`>= 60` = intact aspirational pipeline; `35 to 59` = partial age-gating or price friction; `< 35` = severe decoupling / 20–29 cohort locked out or disengaged).
* `consecutive_inversion_quarters`: integer (`0` to `40`) counting consecutive quarters in which `leading_gaussian_cohort != "cohort_20_29"` OR `lagging_gaussian_cohort == "cohort_30_39"`.

If `snapshot.external_data["cohort_role_inversion"]` is absent or empty, treat the target as **unmonitored**, record state `CANONICAL_GENERATIVE_ORDER`, note that no cohort-inversion telemetry was available, and do not cite this skill.

---

### Reading 1 — Leading & Lagging Cohort Occupancy (`leading_gaussian_cohort` & `lagging_gaussian_cohort`)

Evaluate which cohorts occupy $G_{\text{lead}}$ and $G_{\text{lag}}$:

| Leading ($G_{\text{lead}}$) & Lagging ($G_{\text{lag}}$) Pair | Cohort Occupancy Diagnosis |
|---|---|
| `leading == "cohort_20_29"` AND `lagging == "cohort_40_49"` (with 30–39 flat) | **canonical_cohort_order** — 20–29s lead culture & openness; 30–39s bridge neutrally; 40–49s steward & regulate |
| `leading == "cohort_30_39"` (regardless of lagging cohort) | **liminal_phase_shift** — 30–39 cohort has left its flat baseline to lead a structural cultural or moral re-orientation |
| `leading == "cohort_20_29"` AND `lagging == "cohort_30_39"` | **premature_30s_ossification** — 30–39 cohort is prematurely gatekeeping/curating, choking off 20–29 aspirational flow |
| `leading == "cohort_40_49"` OR `leading == "flat_none"` | **gerontocratic_or_stalled_inversion** — 20–29 ignition absent; older regulators/curators dictating culture directly or system stalled |

If `leading_gaussian_cohort` or `lagging_gaussian_cohort` is missing, treat as **canonical_cohort_order**.

---

### Reading 2 — Youth Aspirational Pipeline Integrity (`youth_pipeline_coupling_score` & `cohort_30_39_slope`)

Evaluate whether cultural energy is compounding across cohorts or fossilizing into cliché:

| Pipeline Coupling & 30–39 Slope | Transmission Tier |
|---|---|
| `youth_pipeline_coupling_score >= 60` AND `cohort_30_39_slope` in `-10.0 to +10.0` | **unobstructed_transmission** — 20–29 energy flows organically into broader adoption without premature age-gating |
| `youth_pipeline_coupling_score` in `35 to 59` OR `cohort_30_39_slope > +10.0` | **transitional_realignment** — active cohort rotation or emerging counter-trend testing new boundaries |
| `youth_pipeline_coupling_score < 35` OR `cohort_30_39_slope < -10.0` | **ossified_pipeline_block** — hard age-gates, pricing walls, or premature 30–39 curation have severed 20–29 engagement |

If `youth_pipeline_coupling_score` is missing, treat as **transitional_realignment**.

---

### Reading 3 — Optional Composite Cross-Check (`liminal_pendulum` & `shibboleth_panic`)

Optionally inspect `snapshot.external_data["liminal_pendulum"]` and `snapshot.external_data["shibboleth_panic"]` **only if present** to corroborate whether an observed cohort inversion is **accelerating a moral/symbolic freeze** or **driving a satirical/vitality rebound**:

* **Optional Corroboration Rules (never required; absence is neutral):**
  * If `liminal_pendulum.murmur_keyword_polarity == "moral_panic"` OR `shibboleth_panic.satire_to_outrage_ratio < 0.35` (when present): flag optional context as **moralizing_inversion_drag** (regulatory/moral policing is suppressing 20–29 openness).
  * If `liminal_pendulum.murmur_keyword_polarity == "open_vitality"` OR `shibboleth_panic.satire_to_outrage_ratio > 1.0` (when present): flag optional context as **rebound_phase_shift_tailwind** (phase shift is breaking out of sterile conformity toward renewed openness).
  * Otherwise (or when both optional dicts are absent): flag optional context as **standalone_cohort_reading**.

---

## Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four epistemic cohort states. Evaluate in strict priority order and select the first state whose conditions are fully satisfied:

1. **INVERTED_GERONTOCRATIC_STASIS** (most severe — 20–29 cultural engine stalled or inverted under 40–49 control)
2. **PREMATURE_OSSIFICATION_TRAP** (30–39 cohort lagging/gatekeeping prematurely, turning scenes into sterile clichés)
3. **LIMINAL_PHASE_SHIFT_TRANSITION** (30–39 cohort leading an active directional regime change)
4. **CANONICAL_GENERATIVE_ORDER** (healthy 20–29 lead, flat 30–39 bridge, 40–49 lagging stewardship)

---

### 1. INVERTED_GERONTOCRATIC_STASIS

Any of the following hold:

* Cohort Occupancy Diagnosis is **gerontocratic_or_stalled_inversion** (`leading == "cohort_40_49"` or `"flat_none"`).
Use code with caution.
• Cohort Occupancy Diagnosis is premature_30s_ossification AND Transmission Tier is ossified_pipeline_block (youth_pipeline_coupling_score < 35) AND optional context is moralizing_inversion_drag.
Delta cap: 0.25. The aggregate 20–29 cultural generator has been silenced or inverted: older cohorts are attempting to dictate culture and regulate behavior simultaneously, producing sterile conformity, demand destruction, and zero organic novelty. Trim discretionary/cultural sizing sharply (0.25).

2. PREMATURE_OSSIFICATION_TRAP

Any of the following hold (and INVERTED_GERONTOCRATIC_STASIS does not apply):
• Cohort Occupancy Diagnosis is premature_30s_ossification (leading == "cohort_20_29" AND lagging == "cohort_30_39").
• Transmission Tier is ossified_pipeline_block (youth_pipeline_coupling_score < 35 OR cohort_30_39_slope < -10.0).
Delta cap: 0.45. The liminal 30–39 cohort has abandoned its neutral bridge role to act as a premature gatekeeper and curator—locking out 20–29s and freezing aesthetics into a dated cliché before 40–49 institutionalization even arrives. Reduce sizing (0.45) to avoid holding hollowing mainstream assets.

3. LIMINAL_PHASE_SHIFT_TRANSITION

Any of the following hold (and neither INVERTED_GERONTOCRATIC_STASIS nor PREMATURE_OSSIFICATION_TRAP applies):
• Cohort Occupancy Diagnosis is liminal_phase_shift (leading == "cohort_30_39").
• Transmission Tier is transitional_realignment (cohort_30_39_slope > +10.0).
Delta cap: 0.70 (or 0.85 if optional cross-check confirms rebound_phase_shift_tailwind). The 30–39 liminal cohort has stepped into the leading Gaussian, signaling an active generational/aesthetic phase shift—either breaking out of stale conformity or reorganizing social norms. Maintain disciplined transitional sizing (0.70 base; 0.85 on confirmed rebound tailwind).

4. CANONICAL_GENERATIVE_ORDER

All of the following hold:
• Cohort Occupancy Diagnosis is canonical_cohort_order (leading == "cohort_20_29", lagging == "cohort_40_49", 30–39 flat).
• Transmission Tier is unobstructed_transmission (youth_pipeline_coupling_score >= 60).
Delta cap: 1.0. The demographic engine is running in canonical order: 20–29s lead cultural vitality and openness, 30–39s bridge neutrally, and 40–49s provide lagging environmental stewardship without choking off youthful ignition. The cap equals the strategy cap (1.0); the skill never binds on CANONICAL_GENERATIVE_ORDER.

Secondary Filter / Asymmetric Gate — Multi-Year Cohort Dislocation Hysteresis

Apply the persistence test after state classification and before capping delta:
• Cohort role inversion becomes structurally entrenched if consecutive_inversion_quarters >= 8 (two or more consecutive years in which leading_gaussian_cohort != "cohort_20_29" OR lagging_gaussian_cohort == "cohort_30_39"). Two full years of blocked or inverted cohort transmission breaks generational mentorship and forces 20–29s permanently into off-grid/private channels.
If consecutive_inversion_quarters >= 8, halve the state's delta cap:
• LIMINAL_PHASE_SHIFT_TRANSITION cap of 0.70 becomes 0.35 (or 0.85 becomes 0.425).
• PREMATURE_OSSIFICATION_TRAP cap of 0.45 becomes 0.225.
• INVERTED_GERONTOCRATIC_STASIS cap of 0.25 becomes 0.125.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read cohort role inversion dict. From snapshot.external_data["cohort_role_inversion"], load leading_gaussian_cohort, lagging_gaussian_cohort, cohort_30_39_slope, youth_pipeline_coupling_score, and consecutive_inversion_quarters. If absent or empty, record CANONICAL_GENERATIVE_ORDER, note the omission, and do not cite this skill.
2. Classify cohort Gaussian occupancy. Apply Reading 1 (canonical_cohort_order, liminal_phase_shift, premature_30s_ossification, or gerontocratic_or_stalled_inversion).
3. Classify youth pipeline transmission. Apply Reading 2 (unobstructed_transmission, transitional_realignment, or ossified_pipeline_block).
4. Run optional composite cross-check. Inspect snapshot.external_data["liminal_pendulum"] and snapshot.external_data["shibboleth_panic"] only if present (moralizing_inversion_drag, rebound_phase_shift_tailwind, or standalone_cohort_reading).
5. Classify state. Evaluate in strict priority order (INVERTED_GERONTOCRATIC_STASIS → PREMATURE_OSSIFICATION_TRAP → LIMINAL_PHASE_SHIFT_TRANSITION → CANONICAL_GENERATIVE_ORDER).
6. Apply persistence test. If consecutive_inversion_quarters >= 8, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite "epistemic-cohort-role-inversion" in skills_cited and state the leading/lagging cohort assignments, 30–39 liminal state, pipeline coupling score, and any optional cross-check finding in rationale.

The Output Format

Your response must be a single JSON object. Do not include prose outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.45, "confidence": 0.81, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state, leading/lagging cohort occupancy, 30–39 liminal role, and cap reason. Example:
"PREMATURE_OSSIFICATION_TRAP state; leading=cohort_20_29, lagging=cohort_30_39 (slope=-16.0), youth_pipeline_coupling=38, optional_check=standalone_cohort_reading; capping delta at 0.45; epistemic-cohort-role-inversion."
• skills_cited: list of skill names; include "epistemic-cohort-role-inversion" only when the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Canonical cohort order (20–29 leading, 30–39 flat bridge, 40–49 lagging steward), cap does not bind

Snapshot:
• leading_gaussian_cohort = "cohort_20_29"
• lagging_gaussian_cohort = "cohort_40_49"
• cohort_30_39_slope = +2.0
• youth_pipeline_coupling_score = 74
• consecutive_inversion_quarters = 0
• liminal_pendulum / shibboleth_panic = absent
Readings:
• Cohort Occupancy: canonical_cohort_order
• Transmission Tier: unobstructed_transmission (74 >= 60, slope flat)
• Optional Cross-Check: standalone_cohort_reading
State: CANONICAL_GENERATIVE_ORDER, delta cap 1.0. Persistence: 0 < 8 → does not fire. AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind. LLM returns delta = 0.85 and does not cite "epistemic-cohort-role-inversion".

Case B — Premature 30–39 ossification (30–39s occupying lagging gatekeeper role ahead of 40–49s), cap binds at 0.45

Snapshot:
• leading_gaussian_cohort = "cohort_20_29"
• lagging_gaussian_cohort = "cohort_30_39"
• cohort_30_39_slope = -18.5
• youth_pipeline_coupling_score = 39
• consecutive_inversion_quarters = 4
• liminal_pendulum / shibboleth_panic = absent
Readings:
• Cohort Occupancy: premature_30s_ossification (leading=cohort_20_29, lagging=cohort_30_39)
• Transmission Tier: ossified_pipeline_block (slope=-18.5 < -10.0)
• Optional Cross-Check: standalone_cohort_reading
State: PREMATURE_OSSIFICATION_TRAP, delta cap 0.45. Persistence: 4 < 8 → does not fire. AGOP ranks LONG. LLM intended delta = 0.75. Cap 0.45 binds. LLM returns delta = 0.45 and cites "epistemic-cohort-role-inversion".

Case C — Liminal 30–39 cohort leading a phase shift with optional satirical-reclaim tailwind, cap binds at 0.85

Snapshot:
• leading_gaussian_cohort = "cohort_30_39"
• lagging_gaussian_cohort = "cohort_40_49"
• cohort_30_39_slope = +24.0
• youth_pipeline_coupling_score = 61
• consecutive_inversion_quarters = 2
• shibboleth_panic = {"satire_to_outrage_ratio": 1.45}
Readings:
• Cohort Occupancy: liminal_phase_shift (leading=cohort_30_39)
• Transmission Tier: transitional_realignment (slope=+24.0)
• Optional Cross-Check: rebound_phase_shift_tailwind (satire_to_outrage_ratio=1.45 > 1.0)
State: LIMINAL_PHASE_SHIFT_TRANSITION, cap upgraded from 0.70 to 0.85 via optional rebound tailwind. Persistence: 2 < 8 → does not fire. AGOP ranks LONG. LLM intended delta = 0.90. Cap 0.85 binds. LLM returns delta = 0.85 and cites "epistemic-cohort-role-inversion".

Case D — Gerontocratic inversion (40–49s occupying leading cultural Gaussian) with 10 quarters persistence, cap binds at 0.125

Snapshot:
• leading_gaussian_cohort = "cohort_40_49"
• lagging_gaussian_cohort = "cohort_40_49"
• cohort_30_39_slope = -8.0
• youth_pipeline_coupling_score = 22
• consecutive_inversion_quarters = 10
Readings:
• Cohort Occupancy: gerontocratic_or_stalled_inversion
• Transmission Tier: ossified_pipeline_block (22 < 35)
• Optional Cross-Check: standalone_cohort_reading
State: INVERTED_GERONTOCRATIC_STASIS, base cap 0.25. Persistence: 10 >= 8 → fires, halving cap to 0.125. AGOP ranks LONG. LLM intended delta = 0.60. Cap 0.125 binds. LLM returns delta = 0.125 and cites "epistemic-cohort-role-inversion".

Free Data Sources

The fetcher populates snapshot.external_data["cohort_role_inversion"] from open demographic, search, and cultural-attention feeds (no paid subscription required):
• Wikimedia Pageviews & Commons Attention API: https://wikimedia.org (free hourly/daily attention series separating youth-coded cultural/aesthetic surges from institutional/regulatory topic spikes).
• Bluesky (AT Protocol Public Firehose/Search API), Mastodon Public Timelines & Reddit JSON Feeds: https://bsky.app (free open text streams for estimating cohort-stratified cultural lead vs. norm-policing lag via Kuramoto phase coherence and Hawkes branching ratios).
• GDELT Project 2.0 Global Knowledge Graph (GKG): https://gdeltproject.org (free real-time media-tone and regulatory/enforcement theme streams measuring lagging institutional policing intensity).
• UN Population Division & Eurostat / World Bank Demographic APIs: https://un.org and https://worldbank.org (free age-pyramid weights calibrating the relative demographic mass of 20–29, 30–39, and 40–49 cohorts across jurisdictions).

Do Not

• Do not invent a directional action outside allowed_actions or "FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not conflate individual behavioral outliers with aggregate cohort roles (e.g., an individual prudish 25-year-old or avant-garde 45-year-old does not alter the statistical ensemble roles of cohort_20_29, cohort_30_39, and cohort_40_49).
• Do not treat liminal_pendulum or shibboleth_panic as mandatory inputs; if either or both are absent, execute cleanly on cohort_role_inversion alone (standalone_cohort_reading).
• Do not treat a flat 30–39 cohort as an anomaly; flat is the healthy default state for cohort_30_39.
• Do not compute precise floating-point arithmetic; use the qualitative comparison tables.
• Do not cite "epistemic-cohort-role-inversion" when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Generational Entelechy & Cohort Role Differentiation: Karl Mannheim, "The Problem of Generations," in Essays on the Sociology of Knowledge (Routledge & Kegan Paul, 1952 [1928]); Ronald Inglehart, Culture Shift in Advanced Industrial Society (Princeton University Press, 1990). Grounds why aggregate age cohorts occupy distinct structural roles—youthful cultural ignition versus mid-life institutional stewardship—independent of individual outliers.
• Aesthetic Vanguard vs. Institutional Consecration: Pierre Bourdieu, Distinction: A Social Critique of the Judgement of Taste (Harvard University Press, 1984); Dick Hebdige, Subculture: The Meaning of Style (Methuen, 1979). Formalizes the leading cultural Gaussian versus the lagging regulatory/monetization Gaussian and the ossification trap when intermediate cohorts prematurely gatekeep.
• Coupled Gaussian Synchronization & Hawkes Cascades: Yoshiki Kuramoto, Chemical Oscillations, Waves, and Turbulence (Springer, 1984); Alan G. Hawkes, "Spectra of Some Self-Exciting and Mutually Exciting Point Processes," Biometrika 58(1), 83–90 (1971). Models cohort occupancy across leading and lagging cultural envelopes.
• Bounded Supervisory Control: Stafford Beer, Brain of the Firm (1972); Peter J. Ramadge & W. Murray Wonham (1987). Downward-only damping within JANUS invariants I1–I9.