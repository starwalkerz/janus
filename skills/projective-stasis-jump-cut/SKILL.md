---
name: "projective-stasis-jump-cut"
description: "Classify the tick by whether an institution, market, or demographic ensemble is trapped in projective frozen time (restorative nostalgia, legacy totem recycling, and lifestyle-induced decay masquerading as natural aging) versus embodied continuity (real biological, metabolic, and creative preservation compounding outside closed loops); optionally corroborate with cohort_role_inversion and institutional_optics telemetry; cap delta when restorative nostalgia masks structural stagnation or triggers sudden jump-cut dissonance."
---

# Projective Stasis vs. Embodied Continuity & Jump-Cut Gate

# At its absolute simplest, it measures the gap between fake stability and real vitality.

You are reading the tick against **the asymmetry between symbolic projective stasis and embodied material continuity** across offbeat synodic stress-and-nostalgia envelopes.

Drawing on Svetlana Boym's *The Future of Nostalgia* (2001) on restorative versus reflective nostalgia, Mark Fisher's *Ghosts of My Life* (2014) and Simon Reynolds's *Retromania* (2011) on cultural stasis and forensic retro, Robert Jay Lifton's *The Broken Connection* (1979) on symbolic immortality, Bernice Neugarten's *Social Clock* (1965) on role-timing violations, Leon Festinger's *Cognitive Dissonance* (1957), and Peter Turchin's *Secular Cycles* (2009) on late-cycle elite lock-in, systems degrade when entrenched cohorts surrender real physical and creative vitality to industrial/institutional decay while freezing past cultural or geopolitical totems in amber.

### The Core Structural Mechanism

1. **The Offbeat Material-vs.-Moral Gaussian Cascade (`synodic_phase_regime`):**
   * Across historical synodic beats ($T_{\text{syn}} \approx 127.07\text{ yrs}$ mean, oscillating between short ~111–115 yr beats and long ~138–143 yr beats), sharp **Material shock impulses** ($\sigma_{\text{mat}} \approx 0.075\,T_k$) lead at quarter-nodes, while fat **Moral/Nostalgia Gaussians** ($\sigma_{\text{mor}} \approx 0.165\,T_k$, lagging by $\delta_k \approx 0.14\,T_k$) absorb the aftermath—occupying $2.20\times$ more integrated historical phase space.
   * During long-beat inter-node valleys, **restorative nostalgia** reaches peak distortion ($I_{\text{mor}} / I_{\text{mat}} \approx 2.1\times\text{–}4.3\times$): entrenched gatekeepers lock cultural, media, and institutional doors, recycling 20-year-old hits and frozen historical archetypes as collective anesthesia against stagnation.
2. **Embodied Continuity & The Jump-Cut Outlier (`jump_cut_dissonance`):**
   * **Projective Stasis ($T_c \to \infty,\; T_s = \text{constant}$):** Mainstream actors accept lifestyle-induced biological decay ($T_v \approx T_c$, accelerated by ultra-processed foods, alcohol, and chronic cortisol) while enforcing rigid Social Clock boundaries ("step aside at 40") and consuming simulated retro youth on screen.
   * **Embodied Continuity ($T_c \to \infty,\; T_v \ll T_c$):** Outliers operating outside closed local loops—preserving metabolic and collagen vitality via whole-food nutrition, habitual sobriety, low bitterness, and uninterrupted creative hustle—compound across decades without paying the decay tax.
   * **Jump-Cut Collision ($\Delta = |T_c - T_v| \ge 20\text{ yrs}$):** When an embodied outlier re-enters a closed loop (spatial jump-cut) or reveals biographical age against youthful appearance (biographical jump-cut), vertical age hierarchies collapse into horizontal peer etiquette ("brother/sister rule"), triggering acute cognitive dissonance and sudden repricing of hollow legacy totems.

Your job is to classify the tick's temporal-stasis regime and cap `delta` accordingly. You do not invent trades. You do not override AGOP. You modulate the LLM's `delta` within the bound the verifier already permits. You never raise `delta` above the strategy cap, and you never invent an action outside `allowed_actions`.

---

## The Readings

Compute three core readings from `snapshot.external_data["projective_stasis"]`, plus an optional, non-mandatory check on `cohort_role_inversion` and `institutional_optics` if present. Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher and cultural/demographic pipeline populate `snapshot.external_data["projective_stasis"]` using streaming catalog-to-new ratios, media/festival lineup archival age, metabolic/consumer health proxies, and social-dissonance discourse streams:

* `restorative_nostalgia_index`: score (`0` to `100`) measuring how heavily mainstream media, brands, and institutions rely on recycled 20-to-30-year-old catalog totems and frozen historical archetypes over new creation (`< 35` = forward generative creation; `35 to 64` = elevated retro-curation drift; `>= 65` = acute restorative stasis / museum-exhibit lock-in).
* `moral_to_material_ratio`: floating-point ratio (`0.2` to `5.0`) comparing standing lagging moral/nostalgic narrative volume against leading material/operational velocity (`< 1.2` = material velocity leading; `1.2 to 2.4` = lagging moral plateau dominant; `> 2.4` = extreme inter-node nostalgia distortion).
* `embodied_vitality_divergence`: score (`0` to `100`) measuring the gap between mainstream lifestyle-decay indicators (UPF/alcohol dependency, sedentary/cortisol drag) and parallel whole-food/sober/high-output outlier cohorts (`< 35` = aligned baseline vitality; `35 to 69` = widening insider-vs.-outlier divergence; `>= 70` = extreme biological/creative divergence primed for jump-cut shock).
* `jump_cut_dissonance_velocity`: signed velocity (`-50.0` to `+50.0`) measuring the rate at which preserved outliers, adult-child/peer collisions, or whole-food/sovereign alternatives are puncturing legacy age scripts and retro illusions: `<= +10.0` (dormant or contained), `+10.1 to +30.0` (active social-clock short-circuits exposing legacy fragility), `> +30.0` (acute jump-cut paradigm break).

If `snapshot.external_data["projective_stasis"]` is absent or empty, treat the target as **unmonitored**, record state `GENERATIVE_MATERIAL_CONTINUITY`, note that no projective-stasis telemetry was available, and do not cite this skill.

---

### Reading 1 — Restorative Stasis & Moral Plateau (`restorative_nostalgia_index` & `moral_to_material_ratio`)

Evaluate whether the environment is generating forward material value or trapped in a lagging restorative nostalgia tail:

| Restorative Nostalgia & Moral-to-Material Ratio | Temporal Regime Diagnosis |
|---|---|
| `restorative_nostalgia_index < 35` AND `moral_to_material_ratio < 1.2` | **forward_generative_flow** — material innovation and new creation lead; low reliance on frozen totems |
| `restorative_nostalgia_index` in `35 to 64` OR `moral_to_material_ratio` in `1.2 to 2.4` | **lagging_moral_plateau** — aging gatekeepers recycling legacy catalog and historical scripts to soothe stagnation |
| `restorative_nostalgia_index >= 65` AND `moral_to_material_ratio > 2.4` | **amber_museum_lock_in** — acute restorative stasis; institutions functioning as living museum exhibits with golden handcuffs |

If `restorative_nostalgia_index` is missing, treat as **lagging_moral_plateau**.

---

### Reading 2 — Embodied Divergence & Jump-Cut Shock (`embodied_vitality_divergence` & `jump_cut_dissonance_velocity`)

Evaluate whether real biological/creative compounding outside the closed loop is destabilizing legacy assumptions:

| Embodied Divergence & Jump-Cut Velocity | Continuity Risk Tier |
|---|---|
| `embodied_vitality_divergence < 35` AND `jump_cut_dissonance_velocity <= +10.0` | **coherent_lifecycle_baseline** — biological and social timelines aligned; minimal jump-cut friction |
| `embodied_vitality_divergence` in `35 to 69` AND `jump_cut_dissonance_velocity <= +10.0` | **latent_outlier_compounding** — whole-food, sober, high-output outliers quietly compounding outside the UPF/nostalgia loop |
| `embodied_vitality_divergence >= 70` OR `jump_cut_dissonance_velocity > +10.0` | **active_jump_cut_rupture** — preserved biological/creative outliers colliding with rigid Social Clocks, shattering legacy scripts |

If `embodied_vitality_divergence` is missing, treat as **latent_outlier_compounding**.

---

### Reading 3 — Optional Composite Cross-Check (`cohort_role_inversion` & `institutional_optics`)

Optionally inspect `snapshot.external_data["cohort_role_inversion"]` and `snapshot.external_data["institutional_optics"]` **only if present** to corroborate whether projective stasis is reinforced by gerontocratic cohort lock-in or performative category conflation:

* **Optional Corroboration Rules (never required; absence is neutral):**
  * If `cohort_role_inversion.leading_gaussian_cohort == "cohort_40_49"` OR `cohort_role_inversion.lagging_gaussian_cohort == "cohort_30_39"` OR `institutional_optics.category_conflation_score >= 65` (when present): flag optional context as **corroborated_totem_ossification** (entrenched cohorts are actively freezing past scripts and policing hollow categories).
  * If `institutional_optics.satirical_deflation_velocity > +10.0` OR `cohort_role_inversion.cohort_30_39_slope > +10.0` (when present): flag optional context as **corroborated_material_reawakening** (rising material velocity is dissolving the lagging moral illusion).
  * Otherwise (or when both optional dicts are absent): flag optional context as **standalone_stasis_reading**.

---

## Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four projective-stasis states. Evaluate in strict priority order and select the first state whose conditions are fully satisfied:

1. **JUMP_CUT_PARADIGM_RUPTURE** (most severe — acute restorative stasis colliding with active jump-cut dissonance or extreme insider-vs.-outlier divergence)
2. **RESTORATIVE_AMBER_STASIS** (entrenched museum-exhibit lock-in and thick lagging moral plateau masking creative/metabolic decay)
3. **LAGGING_NOSTALGIA_DRIFT** (moderate retro-curation drift and latent outlier compounding requiring disciplined sizing)
Use code with caution.
4. GENERATIVE_MATERIAL_CONTINUITY (forward creation and embodied vitality aligned; low restorative distortion)

1. JUMP_CUT_PARADIGM_RUPTURE

Any of the following hold:
• Continuity Risk Tier is active_jump_cut_rupture (embodied_vitality_divergence >= 70 OR jump_cut_dissonance_velocity > +10.0).
• Temporal Regime Diagnosis is amber_museum_lock_in AND optional context is corroborated_totem_ossification.
Delta cap: 0.25. Legacy institutions and cohorts trapped in simulated frozen time are colliding with real embodied continuity compounding outside their closed loop. Sharp cognitive dissonance and sudden obsolescence of retro-dependent assets are underway. Trim exposure sharply (0.25).

2. RESTORATIVE_AMBER_STASIS

Any of the following hold (and JUMP_CUT_PARADIGM_RUPTURE does not apply):
• Temporal Regime Diagnosis is amber_museum_lock_in (restorative_nostalgia_index >= 65 AND moral_to_material_ratio > 2.4).
• Temporal Regime Diagnosis is lagging_moral_plateau AND Continuity Risk Tier is latent_outlier_compounding (embodied_vitality_divergence in 35 to 69).
Delta cap: 0.45. Gatekeepers are monetizing restorative nostalgia and rigid Social Clock scripts as anesthesia while real physical vitality and new creation atrophy inside the core loop. Reduce sizing (0.45) to avoid holding hollowing nostalgia-dependent assets.

3. LAGGING_NOSTALGIA_DRIFT

Any of the following hold (and neither JUMP_CUT_PARADIGM_RUPTURE nor RESTORATIVE_AMBER_STASIS applies):
• Temporal Regime Diagnosis is lagging_moral_plateau (restorative_nostalgia_index in 35 to 64 OR moral_to_material_ratio in 1.2 to 2.4).
• Continuity Risk Tier is latent_outlier_compounding (embodied_vitality_divergence in 35 to 69).
Delta cap: 0.70 (or 0.80 if optional cross-check confirms corroborated_material_reawakening). Moderate retro-recycling or early insider-vs.-outlier divergence is present without acute jump-cut rupture. Maintain disciplined sizing (0.70 base; 0.80 when rising material velocity begins clearing the moral tail).

4. GENERATIVE_MATERIAL_CONTINUITY

All of the following hold:
• Temporal Regime Diagnosis is forward_generative_flow (restorative_nostalgia_index < 35, moral_to_material_ratio < 1.2).
• Continuity Risk Tier is coherent_lifecycle_baseline (embodied_vitality_divergence < 35, jump_cut_dissonance_velocity <= +10.0).
Delta cap: 1.0. Cultural production and biological/operational vitality are compounding forward in real time rather than hiding behind frozen totems. The cap equals the strategy cap (1.0); the skill never binds on GENERATIVE_MATERIAL_CONTINUITY.

Secondary Filter / Asymmetric Gate — Long-Beat Hysteresis Penalty

Apply the long-beat persistence check after state classification and before capping delta:
• When moral_to_material_ratio > 2.0 AND restorative_nostalgia_index >= 60 simultaneously (indicating an extended multi-decade inter-node Moral plateau typical of a long synodic beat where institutions have locked the doors against new creation), halve the state's delta_cap:
	• LAGGING_NOSTALGIA_DRIFT cap of 0.70 becomes 0.35 (or 0.80 becomes 0.40).
	• RESTORATIVE_AMBER_STASIS cap of 0.45 becomes 0.225.
	• JUMP_CUT_PARADIGM_RUPTURE cap of 0.25 becomes 0.125.
• The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read projective stasis dict. From snapshot.external_data["projective_stasis"], load restorative_nostalgia_index, moral_to_material_ratio, embodied_vitality_divergence, and jump_cut_dissonance_velocity. If absent or empty, record GENERATIVE_MATERIAL_CONTINUITY, note the omission, and do not cite this skill.
2. Classify temporal regime. Apply Reading 1 (forward_generative_flow, lagging_moral_plateau, or amber_museum_lock_in).
3. Classify embodied continuity & jump-cut risk. Apply Reading 2 (coherent_lifecycle_baseline, latent_outlier_compounding, or active_jump_cut_rupture).
4. Run optional composite cross-check. Inspect snapshot.external_data["cohort_role_inversion"] and snapshot.external_data["institutional_optics"] only if present (corroborated_totem_ossification, corroborated_material_reawakening, or standalone_stasis_reading).
5. Classify state. Evaluate in strict priority order (JUMP_CUT_PARADIGM_RUPTURE → RESTORATIVE_AMBER_STASIS → LAGGING_NOSTALGIA_DRIFT → GENERATIVE_MATERIAL_CONTINUITY).
6. Apply long-beat hysteresis gate. If moral_to_material_ratio > 2.0 AND restorative_nostalgia_index >= 60, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite "projective-stasis-jump-cut" in skills_cited and state the temporal regime diagnosis, continuity risk tier, moral-to-material ratio, jump-cut velocity, and any optional cross-check finding in rationale.

The Output Format

Your response must be a single JSON object. Do not include prose outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.45, "confidence": 0.81, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["projective-stasis-jump-cut"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state, temporal regime diagnosis, continuity risk tier, moral-to-material ratio, and cap reason. Example:
"RESTORATIVE_AMBER_STASIS state; regime=lagging_moral_plateau (nostalgia=62, moral_material_ratio=2.12), continuity=latent_outlier_compounding (divergence=58, jump_cut_vel=+6.5), optional_check=standalone_stasis_reading; long_beat_gate fired; capping delta at 0.225; projective-stasis-jump-cut."
• skills_cited: list of skill names; include "projective-stasis-jump-cut" only when the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Forward generative continuity, cap does not bind

• Snapshot: restorative_nostalgia_index = 24, moral_to_material_ratio = 0.85, embodied_vitality_divergence = 22, jump_cut_dissonance_velocity = +1.5, optional dicts absent.
• Readings: Temporal Regime = forward_generative_flow; Continuity Tier = coherent_lifecycle_baseline; Optional Check = standalone_stasis_reading.
• State: GENERATIVE_MATERIAL_CONTINUITY, delta_cap = 1.0. Long-beat gate does not fire. AGOP ranks LONG, intended delta = 0.85. Cap 1.0 does not bind. Return delta = 0.85 and omit "projective-stasis-jump-cut" from skills_cited.

Case B — Lagging moral plateau with long-beat hysteresis gate firing, cap binds at 0.225

• Snapshot: restorative_nostalgia_index = 63, moral_to_material_ratio = 2.12, embodied_vitality_divergence = 56, jump_cut_dissonance_velocity = +7.0, optional dicts absent.
• Readings: Temporal Regime = lagging_moral_plateau (63 in 35..64, ratio 2.12 in 1.2..2.4); Continuity Tier = latent_outlier_compounding (56 in 35..69); Optional Check = standalone_stasis_reading.
• State: RESTORATIVE_AMBER_STASIS, base delta_cap = 0.45. Long-beat gate fires (2.12 > 2.0 AND 63 >= 60), halving delta_cap to 0.225. AGOP ranks LONG, intended delta = 0.70. Cap 0.225 binds. Return delta = 0.225 and cite "projective-stasis-jump-cut".

Case C — Active jump-cut rupture colliding with museum lock-in, cap binds at 0.125

• Snapshot: restorative_nostalgia_index = 74, moral_to_material_ratio = 2.65, embodied_vitality_divergence = 78, jump_cut_dissonance_velocity = +18.4, cohort_role_inversion = {"leading_gaussian_cohort": "cohort_40_49"}.
• Readings: Temporal Regime = amber_museum_lock_in; Continuity Tier = active_jump_cut_rupture; Optional Check = corroborated_totem_ossification.
• State: JUMP_CUT_PARADIGM_RUPTURE, base delta_cap = 0.25. Long-beat gate fires (2.65 > 2.0 AND 74 >= 60), halving delta_cap to 0.125. AGOP ranks LONG, intended delta = 0.60. Cap 0.125 binds. Return delta = 0.125 and cite "projective-stasis-jump-cut".

Free Data Sources

The fetcher populates snapshot.external_data["projective_stasis"] from open cultural-catalog, metabolic-health, and social-discourse streams (no paid subscription required):
• MusicBrainz, Wikimedia Pageviews & Open Library APIs: https://musicbrainz.org and https://wikimedia.org (free release-year metadata and attention series measuring catalog-to-new consumption ratios and restorative nostalgia concentration).
• FAOSTAT, WHO Global Health Observatory & Open Food Facts API: https://worldbank.org and https://openfoodfacts.org (free national dietary composition, NOVA ultra-processed food share, and per-capita alcohol consumption series calibrating insider metabolic decay vs. whole-food continuity).
• GDELT Project 2.0 Global Knowledge Graph (GKG): https://gdeltproject.org (free real-time media tone and historical-archetype frequency streams measuring lagging moral plateau intensity).
• Bluesky (AT Protocol Public Firehose), Mastodon & Reddit Public JSON Feeds: https://bsky.app (free open discourse streams tracking Social Clock role-timing violations, ID-drop/age-perception dissonance spikes, and jump-cut outlier narratives).

Do Not

• Do not invent a directional action outside allowed_actions or "FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not conflate simulated retro performance on stage ($T_s = \text{constant}$) with real biological and creative continuity ($T_v \ll T_c$).
• Do not treat cohort_role_inversion or institutional_optics as mandatory inputs; if absent, execute cleanly on projective_stasis alone (standalone_stasis_reading).
• Do not compute precise floating-point arithmetic during tick inference; use the qualitative comparison tables.
• Do not cite "projective-stasis-jump-cut" when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Restorative vs. Reflective Nostalgia & Cultural Stasis: Svetlana Boym, The Future of Nostalgia (Basic Books, 2001); Mark Fisher, Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures (Zero Books, 2014); Simon Reynolds, Retromania: Pop Culture's Addiction to Its Own Past (Faber & Faber, 2011). Grounds why late-cycle institutions freeze past totems in amber while suppressing new creation.
• Symbolic Immortality & Terror Management: Robert Jay Lifton, The Broken Connection: On Death and the Continuity of Life (Simon & Schuster, 1979); Ernest Becker, The Denial of Death (Free Press, 1973). Models projective timelessness as collective anesthesia against mortality and aging.
• The Social Clock, Role-Timing Violations & Perceptual Dissonance: Bernice L. Neugarten, Joan W. Moore, and John C. Lowe, "Age Norms, Age Constraints, and Adult Socialization," American Journal of Sociology 70(6), 710–717 (1965); Leon Festinger, A Theory of Cognitive Dissonance (Stanford University Press, 1957); Hélène Dehon and Serge Brédart, "An 'Other-Race' Effect in Age Estimation from Faces," Perception 30(9), 1107–1113 (2001). Formalizes bystander short-circuits when biological preservation violates visual age heuristics.
• Offbeat Synodic Cycles & Secular Elite Lock-In: Peter Turchin and Sergey A. Nefedov, Secular Cycles (Princeton University Press, 2009); Richard Tarnas, Cosmos and Psyche (Viking, 2006). Grounds the asymmetric leading-material / lagging-moral Gaussian envelope across ~127-year synodic beats.
• Bounded Supervisory Control: Stafford Beer, Brain of the Firm (1972); Peter J. Ramadge & W. Murray Wonham (1987). Downward-only damping within JANUS invariants I1–I9.
