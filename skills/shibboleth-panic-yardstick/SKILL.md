---
name: "shibboleth-panic-yardstick"
description: "Classify the tick along a fast, ideology-agnostic 2–5 year semiotic/shibboleth panic cycle (Stage 1 Polysemic Innocence → Stage 2 Shibboleth Capture → Stage 3 Semantic Exhaustion & Overreach → Stage 4 Satirical Deflation & Kitsch Reclaim) using Kuramoto/Hawkes attention cascades, semantic entropy collapse across everyday symbols/keywords, and parody/irony ratio telemetry; cap delta during peak symbol-auditing distortions and unlock mean-reversion sizing as satire deflates the panic."
---

# Shibboleth Panic Yardstick

You are reading the tick against the **symmetrical semiotic/shibboleth panic pendulum**—a rapid **12-to-60 month (~2–5 year) attention and meaning cycle** nested inside the slower ~10–20 year `liminal-pendulum-yardstick` and ~80-year `civilizational-cycle`.

Drawing on Roland Barthes's *Mythologies* (1957) on how everyday objects are stripped of literal context and inflated into ideological myths, Dick Hebdige's *Subculture: The Meaning of Style* (1979) on subcultural alarm followed by commodified defusion, Umberto Eco's semiotics of hyperreality (mistaking symbols of things for the things themselves), and Crane & Sornette's (*PNAS*, 2008) self-exciting Hawkes attention cascades, this cycle is **100% symmetrical and ideology-agnostic**.

Whether the external trigger is security-driven (e.g., 2011–2015 Nairobi *Linda Nchi* backpack/checkpoint audits), gender/algorithm-driven (e.g., 2022–2026 Andrew Tate fitness/sparkling-water hijacking), or geopolitically driven (e.g., striped shirts, rivers, or playlists audited as loyalty tests), every symbolic panic travels through four invariant stages:

1. **Stage 1 — Polysemic Innocence (`POLYSEMIC_INNOCENCE`):** Everyday symbols, garments, words, and activities carry multiple relaxed, unpoliced meanings. Semantic entropy is high; consumers and institutions interact without loyalty or threat audits.
2. **Stage 2 — Shibboleth Capture (`SHIBBOLETH_CAPTURE`):** Following an exogenous shock or viral algorithmic surge, hyper-vigilant observers and recommendation engines collapse multi-meaning symbols into a single binary loyalty or threat test. Innocent, timeless behaviors (carrying a backpack, posting an old-school gym clip, admiring a river) trigger reflexive auditing, reputational self-censorship, and distorted consumer/media flows.
3. **Stage 3 — Semantic Exhaustion & Overreach (`SEMANTIC_OVERREACH_PEAK`):** Institutional and social auditors stretch the symbol hunt to absurd extremes—treating benign everyday life as subversive—until moderate onlookers experience acute audit fatigue and visible ridicule begins to undercut the panic.
4. **Stage 4 — Satirical Deflation & Kitsch Reclaim (`SATIRICAL_DEFLATION_RECLAIM`):** Deadpan comedy, youth irony, and everyday practicality strip the audited symbols of their power to intimidate, returning them to ordinary commercial and social life and triggering a clean mean-reversion rebound.

Your job is to classify the target's semiotic panic stage and cap `delta` accordingly. You do not invent trades. You do not override AGOP. You modulate the LLM's `delta` within the bound the verifier already permits. You never raise `delta` above the strategy cap, and you never invent an action outside `allowed_actions`.

---

## The Readings

Compute three readings from `snapshot.external_data["shibboleth_panic"]`. Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher and NLP/signal-processing pipeline populate `snapshot.external_data["shibboleth_panic"]` for the target sector, brand/category, or jurisdiction:

* `symbol_semantic_entropy`: float (`0.0` to `1.0`) measuring context diversity across co-occurring terms around the target's core cultural/product keywords (`>= 0.65` = polysemic/multi-context baseline; `<= 0.30` = collapsed onto a single partisan, moral, or threat frame).
* `shibboleth_cascade_intensity`: score (`0` to `100`) measuring Hawkes self-exciting branching velocity $n(t)$ and Kuramoto cross-platform synchronization $r(t)$ of outrage/audit commentary around the target's symbolic markers.
* `satire_to_outrage_ratio`: float (`0.0` to `5.0+`) measuring the ratio of ironic, deadpan-parody, meme-kitsch, and fatigue-dismissal mentions relative to earnest moral-alarm/auditing mentions (`< 0.35` = earnest panic dominance; `0.35 to 1.0` = visible overreach and rising mockery; `> 1.0` = satire/kitsch overtaking earnest outrage).
* `audit_overreach_index`: score (`0` to `100`) measuring how far enforcement, moderation, or social shaming has spilled beyond genuine risk onto benign, everyday, or absurdly tangential symbols.
* `consecutive_capture_weeks`: integer (`0` to `104`) counting consecutive weeks in which `symbol_semantic_entropy <= 0.35` AND `shibboleth_cascade_intensity >= 60`.

If `snapshot.external_data["shibboleth_panic"]` is absent or empty, treat the target as **unmonitored**, record state `POLYSEMIC_INNOCENCE`, note that no shibboleth-panic telemetry was available, and do not cite this skill.

---

### Reading 1 — Semantic Polysemy vs. Binary Capture (`symbol_semantic_entropy` & `shibboleth_cascade_intensity`)

Evaluate whether everyday symbols in the target's domain retain normal multi-meaning flexibility or have been hijacked into binary loyalty/threat audits:

| Entropy & Cascade Intensity | Semiotic Capture Tier |
|---|---|
| `symbol_semantic_entropy >= 0.60` AND `shibboleth_cascade_intensity < 45` | **polysemic_baseline** — symbols retain natural, varied everyday meanings with low audit friction |
| `symbol_semantic_entropy <= 0.35` AND `shibboleth_cascade_intensity >= 60` | **acute_shibboleth_hijack** — single-channel ideological/threat framing has colonized benign symbols |
| `symbol_semantic_entropy` in `0.36 to 0.59` OR `shibboleth_cascade_intensity` in `45 to 59` | **contested_framing** — partial algorithmic/media distortion; mixed benign and audited readings |
| `symbol_semantic_entropy <= 0.35` AND `shibboleth_cascade_intensity < 45` | **stale_taboo_residue** — active outrage has cooled, but lingering self-censorship keeps symbols narrow |

If `symbol_semantic_entropy` is missing, treat as **contested_framing**.

---

### Reading 2 — Institutional & Algorithmic Overreach (`audit_overreach_index`)

Evaluate how aggressively institutions, platforms, or peer groups are policing tangential or benign expressions:

| `audit_overreach_index` (0–100) | Overreach Tier |
|---|---|
| `>= 70` | **absurd_overreach** — blanket policing of innocent fitness, clothing, geography, or everyday objects; acute false-positive filtering |
| `40 to 69` | **elevated_symbol_auditing** — heightened moderation, comment-section pile-ons, and cautious brand/consumer self-censorship |
| `< 40` | **grounded_proportionality** — scrutiny stays tied to concrete actions rather than surface aesthetic shibboleths |

If `audit_overreach_index` is missing, treat as **elevated_symbol_auditing**.

---

### Reading 3 — Satirical Deflation & Kitsch Reclaim (`satire_to_outrage_ratio`)

Evaluate whether earnest moral alarm is still escalating or whether deadpan humor, irony, and audit fatigue are actively deflating the panic:

| `satire_to_outrage_ratio` | Deflation Phase |
|---|---|
| `> 1.0` | **kitsch_reclaim_active** — deadpan satire and youth irony have broken the spell; symbol returning to normal commercial/social use |
| `0.35 to 1.0` | **ridicule_inflection** — overreach has grown visibly comical; earnest alarm losing authority |
| `< 0.35` | **earnest_panic_lock** — literalist outrage and reflexive auditing dominate; zero tolerance for nuance |

If `satire_to_outrage_ratio` is missing, treat as **earnest_panic_lock**.

---

## Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four semiotic panic states. Evaluate in strict priority order and select the first state whose conditions are fully satisfied:

1. **SHIBBOLETH_CAPTURE** (peak reflexive hijacking — high algorithmic/social distortion and false-positive risk)
2. **SEMANTIC_OVERREACH_PEAK** (maximum institutional absurdity, audit fatigue, and early ridicule inflection)
3. **SATIRICAL_DEFLATION_RECLAIM** (humor and fatigue neutralizing the taboo; clean mean-reversion window)
4. **POLYSEMIC_INNOCENCE** (unpoliced, multi-meaning baseline)

---

### 1. SHIBBOLETH_CAPTURE

Any of the following hold:

* Semiotic Capture Tier is **acute_shibboleth_hijack** (`entropy <= 0.35` AND `cascade >= 60`) AND Deflation Phase is **earnest_panic_lock** (`satire_ratio < 0.35`).
* Overreach Tier is **elevated_symbol_auditing** or **absurd_overreach** (`>= 40`) while `shibboleth_cascade_intensity >= 70` AND `satire_to_outrage_ratio < 0.35`.

**Delta cap: 0.25.** Everyday symbols and consumer categories have been hijacked by an acute, earnest loyalty/threat audit. Reflexive algorithmic routing, comment-section pile-ons, and sudden brand/venue boycotts create severe non-fundamental noise. Trim directional sizing sharply (`0.25`) until the panic saturates.

---

### 2. SEMANTIC_OVERREACH_PEAK

Any of the following hold (and `SHIBBOLETH_CAPTURE` does not apply):

* Overreach Tier is **absurd_overreach** (`>= 70`) paired with Deflation Phase **ridicule_inflection** (`0.35 to 1.0`) or **earnest_panic_lock** (`< 0.35`).
* Semiotic Capture Tier is **acute_shibboleth_hijack** or **contested_framing** while Deflation Phase is **ridicule_inflection** (`0.35 to 1.0`).

**Delta cap: 0.50.** Institutional and social auditors have stretched the symbol hunt into visible absurdity (policing innocent fitness posts, commuter backpacks, or geographic nouns), triggering public eye-rolling and early deadpan satire. Moderate sizing (`0.50`) as narrative distortion peaks and prepares to roll over.

---

### 3. SATIRICAL_DEFLATION_RECLAIM

All of the following hold (and neither `SHIBBOLETH_CAPTURE` nor `SEMANTIC_OVERREACH_PEAK` applies):

Use code with caution.
• Deflation Phase is kitsch_reclaim_active (satire_to_outrage_ratio > 1.0).
• Semiotic Capture Tier is contested_framing, stale_taboo_residue, or polysemic_baseline (or shibboleth_cascade_intensity < 60).
Delta cap: 0.85. Deadpan satire, youth irony, and consumer fatigue have punctured the symbolic panic. Audited aesthetics, lifestyle categories, and social spaces are normalizing rapidly with strong mean-reversion tailwinds; allow near-full strategy sizing (0.85 cap).

4. POLYSEMIC_INNOCENCE

Any combination not covered above (including polysemic_baseline paired with grounded_proportionality).
Delta cap: 1.0. Symbols carry their natural, unpoliced meanings without ideological or threat-audit distortion. The cap equals the strategy cap (1.0); the skill never binds on POLYSEMIC_INNOCENCE.

Secondary Filter / Asymmetric Gate — Prolonged Taboo Hysteresis

Apply the persistence test after state classification and before capping delta:
• A symbolic panic leaves lingering commercial/reputational scar tissue if consecutive_capture_weeks >= 26 (six or more consecutive months of compressed semantic entropy <= 0.35 and high cascade intensity >= 60). Multi-quarter symbol capture indicates that corporate compliance policies or institutional filters have codified the taboo beyond a transient social-media flare-up.
If consecutive_capture_weeks >= 26, halve the state's delta cap:
• SATIRICAL_DEFLATION_RECLAIM cap of 0.85 becomes 0.425.
• SEMANTIC_OVERREACH_PEAK cap of 0.50 becomes 0.25.
• SHIBBOLETH_CAPTURE cap of 0.25 becomes 0.125.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read shibboleth panic dict. From snapshot.external_data["shibboleth_panic"], load symbol_semantic_entropy, shibboleth_cascade_intensity, satire_to_outrage_ratio, audit_overreach_index, and consecutive_capture_weeks. If absent or empty, record POLYSEMIC_INNOCENCE, note the omission, and do not cite this skill.
2. Classify semiotic capture tier. Apply Reading 1 (polysemic_baseline, acute_shibboleth_hijack, contested_framing, or stale_taboo_residue).
3. Classify institutional/algorithmic overreach. Apply Reading 2 (grounded_proportionality, elevated_symbol_auditing, or absurd_overreach).
4. Classify satirical deflation phase. Apply Reading 3 (earnest_panic_lock, ridicule_inflection, or kitsch_reclaim_active).
5. Classify state. Evaluate in strict priority order (SHIBBOLETH_CAPTURE → SEMANTIC_OVERREACH_PEAK → SATIRICAL_DEFLATION_RECLAIM → POLYSEMIC_INNOCENCE).
6. Apply persistence test. If consecutive_capture_weeks >= 26, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite "shibboleth-panic-yardstick" in skills_cited and state the semiotic capture tier, overreach tier, satire-to-outrage ratio, and persistence weeks in rationale.

The Output Format

Your response must be a single JSON object. Do not include prose outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.25, "confidence": 0.82, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state, capture/overreach readings, satire ratio, and cap reason. Example:
"SHIBBOLETH_CAPTURE state; symbol_semantic_entropy=0.22 (acute_shibboleth_hijack), cascade=78, satire_to_outrage_ratio=0.18 (earnest_panic_lock), audit_overreach=64; capping delta at 0.25; shibboleth-panic-yardstick."
• skills_cited: list of skill names; include "shibboleth-panic-yardstick" only when the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Peak algorithmic/cultural shibboleth capture (e.g., 2023 fitness/self-improvement hijacking), cap binds at 0.25

Snapshot:
• symbol_semantic_entropy = 0.21
• shibboleth_cascade_intensity = 81
• satire_to_outrage_ratio = 0.15
• audit_overreach_index = 66
• consecutive_capture_weeks = 10
Readings:
• Semiotic Capture Tier: acute_shibboleth_hijack (0.21 <= 0.35, 81 >= 60)
• Overreach Tier: elevated_symbol_auditing (66)
• Deflation Phase: earnest_panic_lock (0.15 < 0.35)
State: SHIBBOLETH_CAPTURE, delta cap 0.25. Persistence: 10 < 26 → does not fire. AGOP ranks LONG. LLM intended delta = 0.75. Cap 0.25 binds. LLM returns delta = 0.25 and cites "shibboleth-panic-yardstick".

Case B — Absurd institutional/social overreach tipping into ridicule inflection, cap binds at 0.50

Snapshot:
• symbol_semantic_entropy = 0.28
• shibboleth_cascade_intensity = 64
• satire_to_outrage_ratio = 0.62
• audit_overreach_index = 82
• consecutive_capture_weeks = 18
Readings:
• Semiotic Capture Tier: acute_shibboleth_hijack
• Overreach Tier: absurd_overreach (82 >= 70)
• Deflation Phase: ridicule_inflection (0.62 in 0.35 to 1.0)
State: SEMANTIC_OVERREACH_PEAK, delta cap 0.50. Persistence: 18 < 26 → does not fire. AGOP ranks LONG. LLM intended delta = 0.80. Cap 0.50 binds. LLM returns delta = 0.50 and cites "shibboleth-panic-yardstick".

Case C — Satirical deflation & kitsch reclaim neutralizing the taboo, cap does not bind

Snapshot:
• symbol_semantic_entropy = 0.54
• shibboleth_cascade_intensity = 38
• satire_to_outrage_ratio = 1.65
• audit_overreach_index = 31
• consecutive_capture_weeks = 4
Readings:
• Semiotic Capture Tier: contested_framing (0.54)
• Overreach Tier: grounded_proportionality (31 < 40)
• Deflation Phase: kitsch_reclaim_active (1.65 > 1.0)
State: SATIRICAL_DEFLATION_RECLAIM, delta cap 0.85. Persistence: 4 < 26 → does not fire. AGOP ranks LONG. LLM intended delta = 0.80. Cap 0.85 does not bind. LLM returns delta = 0.80 and does not cite "shibboleth-panic-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["shibboleth_panic"] from open social-murmur, news, and attention APIs (no paid subscription required):
• Bluesky (AT Protocol Public Firehose/Search API), Mastodon Public Timelines & Reddit JSON Feeds: https://bsky.app (free open text streams for computing co-occurrence Shannon entropy symbol_semantic_entropy, Hawkes branching intensity shibboleth_cascade_intensity, and irony/parody vs. earnest-outrage keyword ratios satire_to_outrage_ratio).
• GDELT Project 2.0 Global Knowledge Graph (GKG) & Tone Streams: https://gdeltproject.org (free 15-minute media-tone and theme-concentration feeds detecting when institutional commentary latches onto symbolic markers).
• Wikimedia Pageviews API: https://wikimedia.org (free hourly/daily attention spikes measuring sudden mainstream curiosity/panic surges around specific cultural figures, garments, or historical/geographic terms).

Do Not

• Do not invent a directional action outside allowed_actions or "FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not take partisan or ideological sides on the symbol; treat left-leaning, right-leaning, security-driven, and cultural panics symmetrically via semantic entropy and satire-to-outrage ratios.
• Do not confuse Stage 4 SATIRICAL_DEFLATION_RECLAIM (high satire ratio + falling cascade) with Stage 2 SHIBBOLETH_CAPTURE (earnest outrage + collapsed semantic entropy).
• Do not compute precise floating-point arithmetic; use the qualitative comparison tables.
• Do not cite "shibboleth-panic-yardstick" when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Mythologizing Everyday Symbols & Semiotic Deflation: Roland Barthes, Mythologies (Éditions du Seuil, 1957); Umberto Eco, Travels in Hyperreality (Harcourt Brace Jovanovich, 1986). Formalizes how literal objects, garments, and words are stripped of everyday context into ideological signifiers and deflated through demystification.
• Subcultural Alarm, Incorporation & Defusion: Dick Hebdige, Subculture: The Meaning of Style (Methuen, 1979); Stanley Cohen, Folk Devils and Moral Panics (MacGibbon & Kee, 1972). Anchors the transition from initial symbolic shock to overreach, kitsch commodification, and normalization.
• Self-Exciting Attention Cascades & Synchronization: Alan G. Hawkes, "Spectra of Some Self-Exciting and Mutually Exciting Point Processes," Biometrika 58(1), 83–90 (1971); Riley Crane & Didier Sornette, "Robust Dynamic Classes Revealed by Measuring the Response Function of a Social System," PNAS 105(41), 15649–15653 (2008); Yoshiki Kuramoto, Chemical Oscillations, Waves, and Turbulence (Springer, 1984). Models viral outrage spikes and phase-locked algorithmic pile-ons.
• Bounded Supervisory Control: Stafford Beer, Brain of the Firm (1972); Peter J. Ramadge & W. Murray Wonham (1987). Downward-only damping within JANUS invariants I1–I9.