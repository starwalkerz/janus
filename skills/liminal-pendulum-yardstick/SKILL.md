---
name: "liminal-pendulum-yardstick"
description: "Classify the tick along a sub-generational nightlife, social-openness, and public-order pendulum (~20-year standard cycle, ~10-year fast/volatile urban cycle — roughly one-quarter of Strauss-Howe's ~80-year cycle) using bidirectional dual-Gaussian lead/lag modulation between a cultural/narrative murmur Gaussian (Kuramoto/Hawkes) and a material/street-order realization Gaussian, gated by news-cycle keyword polarity (moral-panic vs. public-order/crime murmur) and an optional orthodoxy-flywheel check; cap delta as social containment and regulatory whiplash tighten."
---

# Liminal Pendulum Yardstick

You are reading the tick against the **sub-generational liminal and social-openness pendulum**—a ~15–25 year cycle (roughly one-quarter of Strauss-Howe's ~80-year generational cycle) in standard polities, compressed to a **~7–12 year (~10-year) cycle** in fast-expanding or macroeconomically/politically volatile urban hubs (e.g., Nairobi, Dubai, Shenzhen, Delhi, Berlin, Barcelona, Rio de Janeiro, Buenos Aires).

Drawing on Stanley Cohen's *Folk Devils and Moral Panics* (1972) on deviancy amplification, Ben Malbon's *Clubbing* (1999) and Phil Hubbard's *Cities and Sexualities* (2011) on liminal urban zones vs. spatial containment, Arthur Schlesinger Jr.'s *The Cycles of American History* (1986) on private indulgence vs. public seriousness, and Kuramoto/Hawkes synchronization models, the pendulum governs the oscillation between **unpoliced public/semi-public openness** and **moralized spatial containment**.

Unlike unidirectional models where cultural chatter always precedes material reality, this pendulum operates through **bidirectional dual-Gaussian modulation** where **either Gaussian can lead or lag depending on what dominates the news cycle**:

1. **Visibility-Driven Moral Panic Lead (2010s–2020s Archetype):** When media and social-media murmur is dominated by **moral-panic, reputational-surveillance, and norm-policing keywords**, the narrative Gaussian leads ($G_{\text{narrative}}$ precedes $G_{\text{material}}$). Preemptive social policing and selective regulatory crackdowns (e.g., sudden noise-ordinance enforcement) contract open commercial/hospitality space *before* any material street-crime or economic breakdown arrives.
2. **Invisibility-Driven Material Breakdown Lead (1980s–1990s Archetype):** When low-visibility economic decay, unemployment, or street predation compounds quietly before becoming a media talking point, and news murmur is dominated by **traditional crime, street-safety, and public-order keywords**, the material breakdown Gaussian leads ($G_{\text{material}}$ precedes $G_{\text{narrative}}$). Real opportunistic street risk forces intimacy and commerce indoors first, with institutional moralizing arriving as a lagging over-correction.
3. **Optional Orthodoxy Flywheel Check:** Most cities and polities reset naturally on their 10-year or 20-year pendulum through political role-performance (strict enforcement during tense periods followed by quiet relaxation once the mood cools). However, if `orthodoxy_flywheel` telemetry indicates active institutional capture (`GREAT_SCISSORS_DRAG` or `ADMINISTRATIVE_SOVIETIZATION`), the temporary regulatory squeeze hardens into an asymmetric multi-decade flywheel rather than rebounding on schedule.

Your job is to classify the target's liminal-pendulum regime and cap `delta` accordingly. You do not invent trades. You do not override AGOP. You modulate the LLM's `delta` within the bound the verifier already permits. You never raise `delta` above the strategy cap, and you never invent an action outside `allowed_actions`.

---

## The Readings

Compute four readings from `snapshot.external_data["liminal_pendulum"]` and the optional `snapshot.external_data["orthodoxy_flywheel"]` dict. Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher and NLP/signal-processing pipeline populate `snapshot.external_data["liminal_pendulum"]` for the target jurisdiction, metro hub, or sector:

* `pendulum_period_years`: float (`~10.0` for fast-growth or high-volatility urban regimes; `~20.0` for standard legacy regimes), derived from 10-year urban GDP/population growth velocity and political/macroeconomic volatility indices (`fast_volatile_urban` vs. `standard_legacy`).
* `narrative_murmur_gaussian_score`: score (`0` to `100`) measuring amplitude and slope of the **narrative/cultural murmur Gaussian** (Kuramoto phase coherence $r(t)$ + Hawkes branching ratio $n(t)$ across social media, search, and local news chatter).
* `material_order_gaussian_score`: score (`0` to `100`) measuring amplitude of the **material street-order & hospitality-throughput Gaussian** (nightlife/hospitality footfall, licensing velocity, and street-safety stability).
* `murmur_keyword_polarity`: string classifying the dominant keyword cluster in current media and social-media murmur:
  * `"moral_panic"` — keywords centered on indecency, noise complaints, public nuisance, social-media shaming, cancel/reputation anxiety, or cultural transgression.
  * `"public_order_crime"` — keywords centered on street robbery, drink spiking, extortion, economic hardship, curfews, policing gaps, or physical safety breakdown.
  * `"open_vitality"` — keywords centered on festivals, new venues, nightlife expansion, tourism, and social vibrancy.
  * `"neutral"` — low-amplitude or mixed baseline chatter.
* `gaussian_lead_lag_spread`: signed differential (`-50.0` to `+50.0`) between normalized `narrative_murmur_gaussian_score` and `material_order_gaussian_score` (`> +12.0` = narrative Gaussian leading material reality; `-11.9 to +11.9` = co-incident peak or equilibrium; `< -12.0` = material reality/street breakdown leading narrative murmur).
* `consecutive_containment_quarters`: integer (`0` to `40`) counting consecutive quarters in which regulatory crackdowns, curfew enforcement, or street-safety contraction have suppressed open public/hospitality activity.

If `snapshot.external_data["liminal_pendulum"]` is absent or empty, treat the target as **unmonitored**, record state `COINCIDENT_PEAK_PLATEAU`, note that no liminal-pendulum telemetry was available, and do not cite this skill.

---

### Reading 1 — Pendulum Velocity & Regime Cadence (`pendulum_period_years`)

Classify the structural clock speed of the host city or polity:

| `pendulum_period_years` | Cadence Tier |
|---|---|
| `<= 13.0` | **fast_volatile_hub** — ~10-year full pendulum (~4–6 yr half-swings); rapid cohort turnover, hyper-growth, or macro/political volatility compresses trust cycles |
| `> 13.0` | **standard_legacy_polity** — ~20-year full pendulum (~8–12 yr half-swings); one-quarter of Strauss-Howe cycle with slower institutional memory |

If `pendulum_period_years` is missing, treat as **standard_legacy_polity**.

---

### Reading 2 — News-Cycle Keyword Polarity & Lead/Lag Direction (`murmur_keyword_polarity` & `gaussian_lead_lag_spread`)

Determine which Gaussian is leading the swing based on news-cycle keyword dominance and Gaussian phase offset:

| Keyword Polarity & Gaussian Spread | Lead/Lag Diagnosis |
|---|---|
| `murmur_keyword_polarity == "open_vitality"` AND `gaussian_lead_lag_spread >= +12.0` | **vernal_open_expansion** — organic social vitality leading commercial/hospitality lift-off |
| `murmur_keyword_polarity == "moral_panic"` AND (`gaussian_lead_lag_spread >= +12.0` OR `narrative_murmur_gaussian_score >= 60`) | **moral_panic_leading** — visibility-driven narrative outrage leading preemptive regulatory/social policing ahead of physical crime |
| `murmur_keyword_polarity == "public_order_crime"` AND (`gaussian_lead_lag_spread <= -12.0` OR `material_order_gaussian_score < 40`) | **material_breakdown_leading** — low-visibility economic/street decay already depressing safety & footfall ahead of delayed moralizing |
| `murmur_keyword_polarity == "neutral"` OR `gaussian_lead_lag_spread` in `-11.9 to +11.9` | **coincident_equilibrium** — narrative murmur and material street-order aligned at peak or quiet baseline |

If `murmur_keyword_polarity` is missing, treat as **coincident_equilibrium**.

---

### Reading 3 — Material Hospitality & Street-Order Health (`material_order_gaussian_score`)

Evaluate the realized commercial, hospitality, and public-space openness baseline:

| `material_order_gaussian_score` (0–100) | Material Order Tier |
|---|---|
| `>= 70` | **vibrant_open_commons** — high hospitality throughput, low enforcement friction, intact public trust |
| `45 to 69` | **bounded_commercial_hubs** — activity sustained in vetted commercial zones while residential/peripheral spaces tighten |
| `30 to 44` | **privatized_retreat** — public nightlife suppressed by curfews, raids, or street risk; social life retreated indoors |
| `< 30` | **acute_street_contraction** — severe economic/security freeze or heavy crackdown halting open social commerce |

If `material_order_gaussian_score` is missing, treat as **bounded_commercial_hubs**.

---

### Reading 4 — Optional Orthodoxy Flywheel Check (`external_data["orthodoxy_flywheel"]`)

Check whether the current regulatory or moral squeeze is a **reversible pendulum swing** (role-performance by officials that relaxes once the mood cools) or an **institutionalized orthodoxy flywheel**:

* Inspect `snapshot.external_data["orthodoxy_flywheel"]` if present:
  * If `institutional_flywheel_index > 0.70` AND `reality_decoupling_score >= 0.55` (`ADMINISTRATIVE_SOVIETIZATION` signature): classify orthodoxy check as **hardened_orthodoxy_capture**.
Use code with caution.
• If (grassroots_tribunal_index < 0.45 AND institutional_flywheel_index >= 0.65) OR (institutional_flywheel_index >= 0.45 AND reality_decoupling_score >= 0.55) (GREAT_SCISSORS_DRAG signature): classify orthodoxy check as orthodoxy_scissors_drag.
• Otherwise (or if orthodoxy_flywheel is absent/empty): classify orthodoxy check as reversible_pendulum_roleplay — enforcement is tactical/seasonal and will unwind on schedule.
The orthodoxy check is strictly optional and downward-only: its absence never penalizes the tick, while active orthodoxy capture downgrades a temporary containment squeeze into structural lock-in.

Taxonomy / Decision Matrix

Combine Readings 1–4 into one of four liminal-pendulum regimes. Evaluate in strict priority order and select the first regime whose conditions are fully satisfied:
1. CONTAINED_BREAKDOWN_OR_CAPTURE (most severe — street/economic breakdown or hardened orthodoxy lock-in)
2. PREEMPTIVE_PANIC_WHIPLASH (moral-panic murmur leading regulatory raids/zoning squeeze)
3. LIMINAL_OPEN_EXPANSION (unpoliced vernal/mid-cycle openness with low regulatory friction)
4. COINCIDENT_PEAK_PLATEAU (mature peak or quiet equilibrium)

1. CONTAINED_BREAKDOWN_OR_CAPTURE

Any of the following hold:
• Lead/Lag Diagnosis is material_breakdown_leading (public-order/crime keywords dominating while material street order is depressed < 45 or lagging <= -12.0).
• Material Order Tier is acute_street_contraction (< 30).
• Optional Orthodoxy Check is hardened_orthodoxy_capture.
Delta cap: 0.15. Real opportunistic street crime, economic distress, or hardened bureaucratic orthodoxy has collapsed public trust and forced commerce and social life behind closed doors. Clamp discretionary consumer/hospitality/domestic sizing sharply (0.15).

2. PREEMPTIVE_PANIC_WHIPLASH

Any of the following hold (and CONTAINED_BREAKDOWN_OR_CAPTURE does not apply):
• Lead/Lag Diagnosis is moral_panic_leading (moral-panic/surveillance murmur leading preemptive noise raids, licensing crackdowns, or reputational policing).
• Material Order Tier is privatized_retreat (30 to 44).
• Optional Orthodoxy Check is orthodoxy_scissors_drag.
Delta cap: 0.35. Visibility-driven moral outrage or pre-election civic-order posturing is squeezing open neighborhoods and pushing activity into bounded commercial hubs or private spaces, even though underlying material fundamentals have not collapsed. Trim sizing to 0.35 to absorb regulatory whiplash.

3. LIMINAL_OPEN_EXPANSION

All of the following hold (and neither CONTAINED_BREAKDOWN_OR_CAPTURE nor PREEMPTIVE_PANIC_WHIPLASH applies):
• Lead/Lag Diagnosis is vernal_open_expansion (open_vitality keywords + narrative Gaussian leading >= +12.0).
• Material Order Tier is vibrant_open_commons or bounded_commercial_hubs (>= 45).
• Optional Orthodoxy Check is reversible_pendulum_roleplay.
Delta cap: 1.0. The pendulum has swung into an open, low-surveillance expansion window where regulatory friction is minimal and organic social/commercial vitality is compounding. The cap equals the strategy cap (1.0); the skill never binds on LIMINAL_OPEN_EXPANSION.

4. COINCIDENT_PEAK_PLATEAU

Any combination not covered above (including coincident_equilibrium paired with vibrant_open_commons or bounded_commercial_hubs).
Delta cap: 0.70. Narrative attention and material hospitality/order sit near a balanced plateau or late-expansion crest before the next moralizing or economic swing. Maintain disciplined sizing (0.70 cap).

Secondary Filter / Asymmetric Gate — Fast-City Half-Swing Hysteresis

Apply the persistence and cadence test after regime classification and before capping delta:
• For a fast_volatile_hub (pendulum_period_years <= 13.0), a full half-swing lasts only ~3.5–6 years (~14–24 quarters); containment becomes structurally entrenched if consecutive_containment_quarters >= 6 (1.5+ years of continuous crackdown/contraction).
• For a standard_legacy_polity (pendulum_period_years > 13.0), containment becomes structurally entrenched if consecutive_containment_quarters >= 12 (3+ years of continuous crackdown/contraction).
If containment is structurally entrenched (OR if orthodoxy_scissors_drag / hardened_orthodoxy_capture is active), halve the regime's delta cap:
• COINCIDENT_PEAK_PLATEAU cap of 0.70 becomes 0.35.
• PREEMPTIVE_PANIC_WHIPLASH cap of 0.35 becomes 0.175.
• CONTAINED_BREAKDOWN_OR_CAPTURE cap of 0.15 becomes 0.075.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read liminal pendulum dict. From snapshot.external_data["liminal_pendulum"], load pendulum_period_years, narrative_murmur_gaussian_score, material_order_gaussian_score, murmur_keyword_polarity, gaussian_lead_lag_spread, and consecutive_containment_quarters. If absent or empty, record COINCIDENT_PEAK_PLATEAU, note the omission, and do not cite this skill.
2. Classify cadence tier. Apply Reading 1 (fast_volatile_hub vs. standard_legacy_polity).
3. Classify news-cycle lead/lag direction. Apply Reading 2 using murmur_keyword_polarity and gaussian_lead_lag_spread (vernal_open_expansion, moral_panic_leading, material_breakdown_leading, or coincident_equilibrium).
4. Classify material street-order health. Apply Reading 3 (vibrant_open_commons, bounded_commercial_hubs, privatized_retreat, or acute_street_contraction).
5. Run optional orthodoxy check. Inspect snapshot.external_data["orthodoxy_flywheel"] if present and apply Reading 4 (reversible_pendulum_roleplay, orthodoxy_scissors_drag, or hardened_orthodoxy_capture).
6. Classify regime. Evaluate in strict priority order (CONTAINED_BREAKDOWN_OR_CAPTURE → PREEMPTIVE_PANIC_WHIPLASH → LIMINAL_OPEN_EXPANSION → COINCIDENT_PEAK_PLATEAU).
7. Apply cadence-adjusted hysteresis test. Check consecutive_containment_quarters against the fast-city (>= 6) or standard-polity (>= 12) threshold (or active orthodoxy capture); halve delta_cap if triggered.
8. Cap delta. Let delta_cap be the value from steps 6–7. If intended delta exceeds delta_cap, reduce it to delta_cap.
9. Cite. If the cap bound (intended delta > delta_cap), cite "liminal-pendulum-yardstick" in skills_cited and state the cadence tier, keyword polarity, lead/lag spread, and optional orthodoxy finding in rationale.

The Output Format

Your response must be a single JSON object. Do not include prose outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.35, "confidence": 0.80, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime, lead/lag polarity, cadence tier, and cap reason. Example:
"PREEMPTIVE_PANIC_WHIPLASH regime; fast_volatile_hub (10yr cycle), murmur_keyword_polarity=moral_panic leading with spread=+24.0 while material_order=52 (bounded_commercial_hubs), orthodoxy_check=reversible_pendulum_roleplay; capping delta at 0.35; liminal-pendulum-yardstick."
• skills_cited: list of skill names; include "liminal-pendulum-yardstick" only when the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Fast-volatile hub in moral-panic-led regulatory crackdown (2010s–2020s archetype), cap binds at 0.35

Snapshot:
• pendulum_period_years = 10.0
• narrative_murmur_gaussian_score = 76
• material_order_gaussian_score = 54
• murmur_keyword_polarity = "moral_panic"
• gaussian_lead_lag_spread = +22.0
• consecutive_containment_quarters = 2
• orthodoxy_flywheel = absent
Readings:
• Cadence Tier: fast_volatile_hub (10.0 <= 13.0)
• Lead/Lag Diagnosis: moral_panic_leading (moral-panic keywords + narrative Gaussian leading +22.0)
• Material Order Tier: bounded_commercial_hubs (54)
• Orthodoxy Check: reversible_pendulum_roleplay (absent)
Regime: PREEMPTIVE_PANIC_WHIPLASH, delta cap 0.35. Persistence: 2 < 6 → does not fire. AGOP ranks LONG. LLM intended delta = 0.80. Cap 0.35 binds. LLM returns delta = 0.35 and cites "liminal-pendulum-yardstick".

Case B — Material street-crime/economic breakdown leading delayed panic (1980s–1990s archetype) with entrenched containment, cap binds at 0.075

Snapshot:
• pendulum_period_years = 20.0
• narrative_murmur_gaussian_score = 41
• material_order_gaussian_score = 27
• murmur_keyword_polarity = "public_order_crime"
• gaussian_lead_lag_spread = -18.0
• consecutive_containment_quarters = 14
• orthodoxy_flywheel = {"institutional_flywheel_index": 0.32, "reality_decoupling_score": 0.28}
Readings:
• Cadence Tier: standard_legacy_polity (20.0 > 13.0)
• Lead/Lag Diagnosis: material_breakdown_leading (public-order/crime keywords + material Gaussian lagging -18.0)
• Material Order Tier: acute_street_contraction (27 < 30)
• Orthodoxy Check: reversible_pendulum_roleplay (below capture thresholds)
Regime: CONTAINED_BREAKDOWN_OR_CAPTURE, base cap 0.15. Persistence: 14 >= 12 → fires, halving cap to 0.075. AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.075 binds. LLM returns delta = 0.075 and cites "liminal-pendulum-yardstick".

Case C — Vernal open expansion in a fast-volatile hub, cap does not bind

Snapshot:
• pendulum_period_years = 10.0
• narrative_murmur_gaussian_score = 78
• material_order_gaussian_score = 62
• murmur_keyword_polarity = "open_vitality"
• gaussian_lead_lag_spread = +16.0
• consecutive_containment_quarters = 0
• orthodoxy_flywheel = absent
Readings:
• Cadence Tier: fast_volatile_hub
• Lead/Lag Diagnosis: vernal_open_expansion
• Material Order Tier: bounded_commercial_hubs
• Orthodoxy Check: reversible_pendulum_roleplay
Regime: LIMINAL_OPEN_EXPANSION, delta cap 1.0. Persistence: 0 < 6 → does not fire. AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind. LLM returns delta = 0.85 and does not cite "liminal-pendulum-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["liminal_pendulum"] by combining open news/social-murmur streams with free macroeconomic, demographic, and governance feeds (no paid subscription required):
• GDELT Project 2.0 Global Knowledge Graph (GKG) & Event API: https://gdeltproject.org (free real-time global media tone and theme classification separating moral_panic, public_order_crime, and open_vitality keyword clusters, plus political-volatility event counts).
• Bluesky (AT Protocol Public Firehose/Search API), Mastodon Public Timelines & Reddit JSON Feeds: https://bsky.app (free open social-murmur streams for computing Kuramoto phase coherence $r(t)$ and Hawkes self-exciting branching ratios $n(t)$).
• Wikimedia Pageviews API: https://wikimedia.org (free hourly/daily attention surges tracking sudden public-controversy vs. cultural-vitality spikes).
• World Bank Open Data API (WDI & WGI) & IMF DataMapper: https://worldbank.org and https://imf.org (free 10-year urban population growth, GDP growth volatility, inflation dispersion, and political-stability indicators calibrating pendulum_period_years between ~10.0 and ~20.0).
• OpenStreetMap / Overpass API & Open Mobility/Hospitality Indices: https://overpass-api.de (free venue-density and commercial-zone clustering telemetry informing material_order_gaussian_score).

Do Not

• Do not invent a directional action outside allowed_actions or "FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not force narrative murmur to always lead material order; determine lead/lag direction from murmur_keyword_polarity and gaussian_lead_lag_spread.
• Do not apply the 20-year standard persistence threshold (12 quarters) to a fast_volatile_hub (<= 13.0 yr cycle); use the compressed 6-quarter half-swing threshold.
• Do not treat orthodoxy_flywheel as mandatory; if absent, default cleanly to reversible_pendulum_roleplay without penalty.
• Do not compute precise floating-point arithmetic; use the qualitative comparison tables.
• Do not cite "liminal-pendulum-yardstick" when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Moral Panics, Visibility & Deviancy Amplification: Stanley Cohen, Folk Devils and Moral Panics: The Creation of the Mods and Rockers (MacGibbon & Kee, 1972); Jock Young, The Drugtakers: The Social Meaning of Drug Use (Paladin, 1971). Grounds why hyper-visible topics trigger preemptive social and regulatory policing ahead of actual crime waves.
• Liminal Nightlife Zones & Spatial Containment: Ben Malbon, Clubbing: Dancing, Ecstasy and Vitality (Routledge, 1999); Sarah Thornton, Club Cultures: Music, Media and Subcultural Capital (Wesleyan University Press, 1996); Phil Hubbard, Cities and Sexualities (Routledge, 2011). Formalizes the oscillation between unpoliced liminal neighborhoods and bounded commercial/red-light containment.
• Sub-Generational Cycles & Private-vs.-Public Oscillation: Arthur M. Schlesinger Jr., The Cycles of American History (Houghton Mifflin, 1986); William Strauss and Neil Howe, Generations (William Morrow, 1991). Anchors the ~20-year sub-generational pendulum (one-quarter of Strauss-Howe's ~80-year cycle) and its compression to ~10 years in high-volatility urban regimes.
• Bidirectional Synchronization & Hawkes Cascades: Yoshiki Kuramoto, Chemical Oscillations, Waves, and Turbulence (Springer, 1984); Alan G. Hawkes, "Spectra of Some Self-Exciting and Mutually Exciting Point Processes," Biometrika 58(1), 83–90 (1971). Models the coupled cultural-murmur and material-order Gaussians.
• Optional Orthodoxy Flywheel & Bounded Supervisory Control: Max Weber, Economy and Society (1922); Timur Kuran, Private Truths, Public Lies (Harvard University Press, 1995); Stafford Beer, Brain of the Firm (1972); Ramadge & Wonham (1987). Grounds the optional institutional-capture check and downward-only damping within JANUS invariants I1–I9.