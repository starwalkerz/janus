#### name: "self-referential-simulacrum-and-narcissus-drift-yardstick"
description: "Yardstick detecting closed-loop self-referential drift and Goodhart-Campbell metric distortion across institutions, jurisdictions, asset issuers, and consensus rating frameworks—grounded in Ovid's Narcissus and Echo, Hans Christian Andersen's The Emperor's New Clothes, Charles Goodhart's Law, Donald Campbell's Law, and Jean Baudrillard's Simulacra and Simulation—clamping delta whenever self-congratulatory proxy dashboards diverge from primary empirical ground truth."

#### Self-Referential Simulacrum & Narcissus-Drift Yardstick

You are reading the tick against the **closed-loop self-referential
drift between institutional proxy dashboards (internal mirrors) and
primary empirical reality (external ground truth)**—complementing
clique-shibboleth-pendulum and
subconscious-internalization-and-sedna-sustenance-yardstick. 

In Ovid's *Metamorphoses*, Book III (8 CE) (where Narcissus wastes away
gazing into his own reflection while Echo can only repeat his final
syllables back to him), Hans Christian Andersen's *"The Emperor's New
Clothes"* (1837) (where courtiers praise invisible fabric because
admitting nakedness triggers credentialed ostracism), Charles Goodhart's
*"Problems of Monetary Management: The U.K. Experience"* (1975) (*"When a
measure becomes a target, it ceases to be a good measure"*), Donald T.
Campbell's *"Assessing the Impact of Planned Social Change"* (1979)
(quantitative social indicators corrupted by institutional pressure),
and Jean Baudrillard's *Simulacra and Simulation* (1981) (signs and
models detaching from the reality they claim to represent), institutions
and asset issuers succumb to **self-referential drift** whenever they
replace primary empirical measurement with self-congratulatory
consensus proxies: 

1. **The Narcissus Reflection (Proxy Inflation):** Bureaucracies,
corporations, and rating committees invent internal KPIs—ESG badges,
nominal degree targets, regulatory compliance checklists, or adjusted
non-GAAP EBITDA—that reflect their own policy intentions rather than
unfiltered physical and cash-flow reality.
2. **The Echo Chamber (Shibboleth Enforcement):** Credentialed peers
and consensus commentators repeat the proxy score back to its authors
as proof of enlightenment, punishing any uncredentialed observer who
points out empirical stagnation (clique-shibboleth-pendulum).
3. **The Simulacrum Divergence (Empirical Hollowing):** While the
self-referential dashboard climbs toward peak "governance and
sustainability" scores, primary registry metrics—net unsubsidized
enterprise formation, free cash flow, demographic replacement, and
swift contract enforcement—erode beneath the mirror until sudden
mean reversion shatters the illusion.

Classifying this divergence separates four structural epistemic regimes: 

* **Empirical Groundedness (EMPIRICAL_GROUNDEDNESS):** Primary
registry metrics and institutional self-reporting move in lockstep
with low proxy distortion (1.0 pass).
* **Moderate Proxy Drift (MODERATE_PROXY_DRIFT):** Noticeable
divergence between adjusted/committee metrics and raw registry
cash-flow or demographic reality (0.60 cap).
* **Echo-Chamber Shibboleth Lock (ECHO_CHAMBER_SHIBBOLETH_LOCK):**
High internal narrative and rating applause masking deteriorating
primary fundamentals (0.25 cap).
* **Narcissus Simulacrum Collapse (NARCISSUS_SIMULACRUM_COLLAPSE):**
Complete detachment of self-referential dashboards from primary
ground truth—peak institutional self-congratulation paired with severe
empirical hollowing (0.10 cap, halving to 0.05 under persistent
simulacrum hysteresis).

Your job is to classify the target's self-referential drift regime and
cap your delta accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy
cap, and you never invent an action outside allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["narcissus_simulacrum_drift"] (cross-checking
upstream signals from clique-shibboleth-pendulum and
subconscious-internalization-and-sedna-sustenance-yardstick where
present). Use the qualitative tables below. Do not compute precise
arithmetic. 

#### Monitored telemetry fields

The fetcher populates
snapshot.external_data["narcissus_simulacrum_drift"] for any evaluated
jurisdiction, corporate issuer, sector, or rating framework (keyed by
ISO-2 code, ticker, or entity slug, with fallback to
"global_baseline"). Each entry supplies: 

* proxy_to_primary_divergence_score: score (0 to 100) measuring
the gap between self-reported/committee proxy metrics (ESG ratings,
adjusted non-GAAP earnings, nominal policy KPIs) and raw primary
registry telemetry (XBRL operating cash flow, net business births,
real demographic replacement, and court disposition velocity) (0 =
strict empirical alignment; 100 = total Goodhart-Baudrillard
detachment).
* echo_chamber_consensus_score: score (0 to 100) measuring
closed-loop institutional self-applause and credentialed narrative
uniformity (0 = open empirical falsification and dissenting
auditability; 100 = unanimous courtier praise punishing empirical
dissent).
* primary_empirical_vitality_score: score (0 to 100) measuring
unfiltered, unadjusted registry health—real free cash flow, net
private enterprise formation, and physical output (0 = severe
primary hollowing; 100 = robust, unadjusted primary compounding).
* consecutive_simulacrum_drift_ticks: integer (0 to 50) counting
consecutive settled periods in which
proxy_to_primary_divergence_score >= 65 AND
primary_empirical_vitality_score < 40.

If snapshot.external_data["narcissus_simulacrum_drift"] is absent or
empty, treat the target as **unmonitored**, record state
**MODERATE_PROXY_DRIFT**, note that no self-referential drift
telemetry was available, and do not cite this skill. 

#### Reading 1 — Goodhart Proxy-to-Primary Divergence (proxy_to_primary_divergence_score)

Evaluate the gap between institutional self-scoring and raw registry
reality: 

proxy_to_primary_divergence_score (0–100)Proxy Divergence Tier
**< 30**
**empirically_anchored** — reported metrics track raw cash-flow & registry facts
**30 to 54**
**mild_metric_glaze** — moderate cosmetic adjustments or KPI framing
**55 to 74**
**goodhart_target_distortion** — optimized proxy KPIs visibly diverge from primary reality
**>= 75**
**baudrillard_simulacrum** — self-referential ratings detached from physical/fiscal ground truth

If proxy_to_primary_divergence_score is missing, treat as
**mild_metric_glaze**. 

#### Reading 2 — Echo-Chamber Consensus Lock (echo_chamber_consensus_score)

Evaluate closed-loop institutional applause and suppression of empirical
dissent: 

echo_chamber_consensus_score (0–100)Echo-Chamber Tier
**< 35**
**open_empirical_audit** — dissenting evidence & raw data freely challenge orthodoxy
**35 to 59**
**institutional_inertia** — standard bureaucratic preference for consensus narratives
**60 to 79**
**echo_chamber_amplification** — credentialed peer committees reinforce self-serving metrics
**>= 80**
**emperors_new_clothes_lock** — unanimous courtier praise enforces collective blind spot

If echo_chamber_consensus_score is missing, treat as
**institutional_inertia**. 

#### Reading 3 — Unadjusted Primary Empirical Vitality (primary_empirical_vitality_score)

Evaluate underlying registry health after stripping out all cosmetic
adjustments: 

primary_empirical_vitality_score (0–100)Primary Reality Tier
**>= 70**
**strong_primary_base** — genuine unadjusted cash flow, enterprise births & output
**45 to 69**
**moderate_primary_base** — positive underlying output tempered by structural drag
**30 to 44**
**eroding_primary_base** — weakening real cash flow or demographic/enterprise contraction
**< 30**
**hollowed_primary_core** — severe underlying depletion masked by surface metrics

If primary_empirical_vitality_score is missing, treat as
**moderate_primary_base**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four self-referential drift regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **NARCISSUS_SIMULACRUM_COLLAPSE** (severe Goodhart-Baudrillard detachment)
2. **ECHO_CHAMBER_SHIBBOLETH_LOCK** (closed-loop consensus masking erosion)
3. **MODERATE_PROXY_DRIFT** (cosmetic metric glaze / partial divergence)
4. **EMPIRICAL_GROUNDEDNESS** (strictest empirical alignment)

#### NARCISSUS_SIMULACRUM_COLLAPSE

Any of the following hold: 

* Proxy Divergence Tier is **baudrillard_simulacrum** (>= 75) AND
Primary Reality Tier is **eroding_primary_base** or
**hollowed_primary_core** (< 45).
* Proxy Divergence Tier is **goodhart_target_distortion** (55 to 74)
AND Echo-Chamber Tier is **emperors_new_clothes_lock** (>= 80) AND
Primary Reality Tier is **hollowed_primary_core** (< 30).

**Delta cap: 0.10.** The institution, issuer, or jurisdiction is gazing
into a Narcissus mirror: self-referential ratings and committee applause
celebrate peak compliance while primary registry fundamentals hollow
out. Clamp sizing sharply (0.10) ahead of inevitable reality
re-pricing. 

#### ECHO_CHAMBER_SHIBBOLETH_LOCK

Any of the following hold (and NARCISSUS_SIMULACRUM_COLLAPSE does not
apply): 

* Proxy Divergence Tier is **goodhart_target_distortion** or
**baudrillard_simulacrum** (>= 55).
* Echo-Chamber Tier is **echo_chamber_amplification** or emperors_new_clothes_lock (>= 60) AND Primary Reality Tier is
eroding_primary_base or hollowed_primary_core (< 45).
Delta cap: 0.25. Credentialed consensus and adjusted KPIs are
actively masking underlying empirical erosion. Trim sizing to 0.25 so
the allocator never mistakes committee applause for durable value.

MODERATE_PROXY_DRIFT

Any of the following hold (and neither NARCISSUS_SIMULACRUM_COLLAPSE
nor ECHO_CHAMBER_SHIBBOLETH_LOCK applies):
• Proxy Divergence Tier is mild_metric_glaze (30 to 54).
• Echo-Chamber Tier is institutional_inertia (35 to 59).
• Primary Reality Tier is moderate_primary_base (45 to 69).
Delta cap: 0.60. Moderate cosmetic metric framing or bureaucratic
inertia exists alongside viable underlying fundamentals; cap exposure at
0.60 relative to empirically transparent peers.

EMPIRICAL_GROUNDEDNESS

All of the following hold:
• Proxy Divergence Tier is empirically_anchored (< 30).
• Echo-Chamber Tier is open_empirical_audit (< 35).
• Primary Reality Tier is strong_primary_base (>= 70).
Delta cap: 1.0. Reported metrics, auditability, and unfiltered
primary registry fundamentals align without Goodhart distortion or
courtier self-applause. The cap equals the strategy cap (1.0); the
skill never binds on EMPIRICAL_GROUNDEDNESS.

Ambiguous fallback

Any combination not covered above is classified MODERATE_PROXY_DRIFT
with delta cap 0.60.

Secondary Filter / Asymmetric Gate — Prolonged Simulacrum Hysteresis

Apply the persistence test after regime classification and before the
cap.
Self-referential drift is institutionally ossified if
consecutive_simulacrum_drift_ticks >= 4 (four or more consecutive
settled periods in which proxy_to_primary_divergence_score >= 65 AND
primary_empirical_vitality_score < 40). Multi-period commitment to
cosmetic proxy KPIs while primary cash flow or demographic vitality
erodes indicates structural capture by the simulacrum.
If the condition is institutionally ossified, halve the regime's
delta cap:
• MODERATE_PROXY_DRIFT cap of 0.60 becomes 0.30.
• ECHO_CHAMBER_SHIBBOLETH_LOCK cap of 0.25 becomes 0.125.
• NARCISSUS_SIMULACRUM_COLLAPSE cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read Narcissus-simulacrum drift dict. From
snapshot.external_data["narcissus_simulacrum_drift"], load
proxy_to_primary_divergence_score, echo_chamber_consensus_score,
primary_empirical_vitality_score, and
consecutive_simulacrum_drift_ticks for the target key (falling
back to "global_baseline" if target key is absent). If the entire
dict is absent or empty, record MODERATE_PROXY_DRIFT, note the
omission, and do not cite this skill.
2. Classify Goodhart proxy-to-primary divergence. Apply Reading 1.
3. Classify echo-chamber consensus lock. Apply Reading 2.
4. Classify unadjusted primary empirical vitality. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(NARCISSUS_SIMULACRUM_COLLAPSE → ECHO_CHAMBER_SHIBBOLETH_LOCK →
MODERATE_PROXY_DRIFT → EMPIRICAL_GROUNDEDNESS) (fallback:
MODERATE_PROXY_DRIFT).
6. Apply persistence test. If
consecutive_simulacrum_drift_ticks >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"self-referential-simulacrum-and-narcissus-drift-yardstick" in
skills_cited and state the proxy divergence score, echo-chamber
score, primary empirical vitality score, and persistence ticks in
the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.10, "confidence": 0.87, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"NARCISSUS_SIMULACRUM_COLLAPSE regime; proxy_to_primary_divergence_score=82 (baudrillard_simulacrum), echo_chamber_consensus_score=84 (emperors_new_clothes_lock), primary_empirical_vitality_score=29 (hollowed_primary_core), consecutive_simulacrum_drift_ticks=6 (simulacrum hysteresis halves cap from 0.10 to 0.05); capping delta at 0.05; self-referential-simulacrum-and-narcissus-drift-yardstick."
• skills_cited: list of skill names; include
"self-referential-simulacrum-and-narcissus-drift-yardstick" only
when the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Empirically anchored issuer/polity with open auditability and strong primary base, cap does not bind

Snapshot:
• proxy_to_primary_divergence_score = 18
• echo_chamber_consensus_score = 24
• primary_empirical_vitality_score = 81
• consecutive_simulacrum_drift_ticks = 0
Readings:
• Proxy Divergence Tier: empirically_anchored
• Echo-Chamber Tier: open_empirical_audit
• Primary Reality Tier: strong_primary_base
Regime: EMPIRICAL_GROUNDEDNESS, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "self-referential-simulacrum-and-narcissus-drift-yardstick".

Case B — Goodhart target distortion + echo-chamber amplification masking eroding primary base, cap binds at 0.25

Snapshot:
• proxy_to_primary_divergence_score = 64
• echo_chamber_consensus_score = 72
• primary_empirical_vitality_score = 38
• consecutive_simulacrum_drift_ticks = 1
Readings:
• Proxy Divergence Tier: goodhart_target_distortion
• Echo-Chamber Tier: echo_chamber_amplification
• Primary Reality Tier: eroding_primary_base
Regime: ECHO_CHAMBER_SHIBBOLETH_LOCK, delta cap 0.25. Persistence: 1 < 4 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.25 binds.
LLM returns delta = 0.25 and cites "self-referential-simulacrum-and-narcissus-drift-yardstick".

Case C — Baudrillard simulacrum + Emperor's New Clothes lock persisting for 6 ticks, hysteresis halves cap to 0.05

Snapshot:
• proxy_to_primary_divergence_score = 82
• echo_chamber_consensus_score = 84
• primary_empirical_vitality_score = 29
• consecutive_simulacrum_drift_ticks = 6
Readings:
• Proxy Divergence Tier: baudrillard_simulacrum
• Echo-Chamber Tier: emperors_new_clothes_lock
• Primary Reality Tier: hollowed_primary_core
Regime: NARCISSUS_SIMULACRUM_COLLAPSE, base cap 0.10. Persistence: 6 >= 4 → fires, halving cap to 0.05.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.05 binds.
LLM returns delta = 0.05 and cites "self-referential-simulacrum-and-narcissus-drift-yardstick".

Free Data Sources

The fetcher populates
snapshot.external_data["narcissus_simulacrum_drift"] by contrasting
self-reported institutional ratings and narrative consensus against
raw, unadjusted primary registries:
• SEC EDGAR (XBRL GAAP Operating Cash Flow vs. Non-GAAP Adjusted Metrics):
https://sec.gov (free JSON API measuring divergence between
headline adjusted earnings and unadjusted cash generation).
• Eurostat & OECD Primary Structural Registries (bd_9bd_sz_cl_r2, demo_frate, gov_10dd_edpt1):
https://europa.eu and https://oecd.org (free
open APIs supplying raw enterprise birth/death rates, fertility, and
public-debt baselines unmediated by committee governance scores).
• GDELT Project Global Knowledge Graph (GKG) & Media Tone Concentration:
https://gdeltproject.org (free real-time media narrative
uniformity vs. dissenting coverage dispersion).
• CEPEJ European Judicial Systems & World Justice Project Open Indicators:
https://coe.int and https://worldjusticeproject.org
(free open data contrasting formal constitutional self-ratings
against actual judicial disposition times).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not accept committee-issued ESG ratings, self-reported governance
scores, or non-GAAP adjusted earnings at face value when raw primary
registry cash flow or demographic baselines are deteriorating.
• Do not confuse unanimous institutional applause (echo_chamber_consensus_score >= 80)
with empirical safety; treat unchallenged consensus paired with proxy
divergence as ECHO_CHAMBER_SHIBBOLETH_LOCK (0.25) or
NARCISSUS_SIMULACRUM_COLLAPSE (0.10).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "self-referential-simulacrum-and-narcissus-drift-yardstick"
when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Classical & Literary Self-Referential Archetypes: Ovid,
Metamorphoses, Book III, lines 339–510 (8 CE) (Narcissus and Echo
closed-loop reflection trap); Hans Christian Andersen, "Kejserens nye
Klæder" ("The Emperor's New Clothes," 1837) (credentialed
courtier consensus enforcing collective empirical blindness).
• Metric Corruption, Simulacra & Related JANUS Gates: Charles A. E.
Goodhart, "Problems of Monetary Management: The U.K. Experience," in
Papers in Monetary Economics, Vol. I (Reserve Bank of Australia,
1975); Donald T. Campbell, "Assessing the Impact of Planned Social
Change," Evaluation and Program Planning 2(1), 67–90 (1979); Jean
Baudrillard, Simulacra and Simulation (Éditions Galilée, 1981);
cross-referenced with clique-shibboleth-pendulum and
subconscious-internalization-and-sedna-sustenance-yardstick;
Ramadge & Wonham (1987). Downward-only damping within JANUS invariants
I1–I9.