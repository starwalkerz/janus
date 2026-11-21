#### name: "mass-formation-herding"
description: "Classify the current tick by clique ossification, Asch/Janis groupthink conformity, and Le Bon/Desmet mass-formation narrative contagion using free Meta SCI, GDELT 2.0, Wikimedia Pageviews, and WVS/EVS telemetry alongside AGOP's Weisfeiler-Lehman classes and Ising magnetization; cap delta as herd synchronization locks in."

#### Mass Formation & Clique Ossification

You are reading the tick against the **social-network ossification and
collective herd contagion** of the target market or polity. In Solomon
Asch's conformity experiments (1955) and Irving Janis's *Groupthink*
(1972), tight-knit, inward-facing social cliques suppress dissenting
telemetry and enforce unanimous adherence to comforting folk myths—even
when physical or actuarial reality contradicts the consensus. 

Structurally, Georg Simmel (1908), Mark Granovetter (1973), and Damon
Centola (*How Behavior Spreads*, 2018) demonstrate that **closed,
high-clustering cliques lacking weak-tie bridges** ossify: complex,
high-commitment adaptations (such as behind-the-meter solar/BESS, EV
transition, or unorthodox risk underwriting) stall at < 1% adoption,
while free-floating anxiety attaches to a single shared narrative. In
Gustave Le Bon (*The Crowd*, 1895), René Girard (1978), and Mattias
Desmet (*The Psychology of Totalitarianism*, 2022), when narrative
entropy collapses and attention synchronizes around one dominant motif,
the crowd enters **mass formation**—trading independently calculated
judgment for hypnotic, mimetic herd alignment that resolves violently
once reality breaches the consensus. 

Your job is to classify the tick into one of four herd-contagion states
and cap your delta accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["mass_formation"],
cross-checked against agop.n_wl_classes (Weisfeiler–Lehman topological
diversity) and econophysics_herding.magnetization (|M|). Use the
qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes regional social-graph concentration, media
theme entropy, synchronized search/page attention, and cultural
conformity baselines into snapshot.external_data["mass_formation"].
Each region or market entry (keyed by ISO-2 / NUTS code or market hub
such as fi, eu, us, de, se, uk, ke, in, bd, sh, or
global_baseline) supplies: 

* clique_ossification_ratio: local-to-external tie concentration
derived from Meta Data for Good Social Connectedness Index
(
SCIself

/∑

SCIexternal
⁠,
normalized 0.0 to 1.0; > 0.65 = closed, inward-facing clique
network with sparse weak-tie bridges).
* narrative_entropy_score: normalized Shannon entropy (0 to 100)
of trailing 7-day GDELT 2.0 Global Knowledge Graph (GKG) themes (100
= diverse, pluralistic topic dispersion; < 30 = severe narrative
monoculture where media and public discourse fixate on 1–2 themes).
* attention_burst_ratio: trailing 7-day Wikimedia Pageviews & GDELT
volume spike on the dominant crisis/narrative cluster divided by its
90-day baseline (1.0 = normal baseline attention; > 3.0× = acute
synchronized herd fixation).
* conformity_baseline_pct: World Values Survey / European Values
Study (WVS/EVS) aggregate share (0 to 100) prioritizing social
obedience and consensus conformity over independent judgment.
* weeks_in_narrative_lock: consecutive settled weeks in which
narrative_entropy_score < 35 AND attention_burst_ratio >= 2.0.

If snapshot.external_data["mass_formation"] is absent or empty, treat
the region as **unmonitored**, record state **PLURALISTIC**, note that
no mass-formation data was available, and do not cite this skill. 

#### Reading 1 — Clique ossification & topological homogeneity (clique_ossification_ratio & agop.n_wl_classes)

Evaluate whether the underlying social or order-flow network is
structurally diverse or locked into closed, repetitive cliques: 

clique_ossification_ratioagop.n_wl_classesNetwork Topology
**< 0.35**
≥ 5**bridged_plural** — open weak-tie bridges; heterogeneous agents
**0.35 to 0.65**
3 to 4**clustered** — moderate regional/sector clustering; mixed priors
**> 0.65**
any**ossified_clique** — inward-facing closed cliques; Centola complex-adoption stall
**any**
≤ 2**ossified_clique** — structural collapse into two homogeneous herd camps

If agop.n_wl_classes is missing, classify using
clique_ossification_ratio alone (< 0.35 = bridged_plural,
0.35 to 0.65 = clustered, > 0.65 = ossified_clique). 

#### Reading 2 — Narrative monoculture & synchronized attention (narrative_entropy_score & attention_burst_ratio)

Evaluate whether public and market attention is dispersed or locked into
a Le Bon / Desmet narrative monoculture: 

narrative_entropy_scoreattention_burst_ratioNarrative Contagion
**≥ 55**
< 1.5×**dispersed** — independent information processing; healthy disagreement
**35 to 55**
1.5× to 2.5×**converging** — thematic narrowing; early mimetic alignment
**< 35**
1.5× to 3.0×**monoculture** — Asch/Janis groupthink lock; dissent suppressed
**< 35**
> 3.0×**hypnotic_swarm** — acute mass formation; synchronized emotional contagion

If either metric falls in a worse row, take the **worse** (more
restrictive) classification. 

#### Reading 3 — Ferromagnetic & cultural conformity multiplier (conformity_baseline_pct & |M|)

Cross-check slow-moving cultural conformity (WVS/EVS) against real-time
Ising herd magnetization (|M| from econophysics_herding): 

| conformity_baseline_pct | Ising |M| | Conformity Lock |
|---|---|---|
| < 45% | < 0.4 | **independent** — low deference to herd consensus |
| 45% to 65% | 0.4 to 0.7 | **deferential** — strong preference falsification under peer pressure |
| > 65% | any | **rigid_orthodoxy** — intense social penalty for breaking clique unanimity |
| any | > 0.7 | **rigid_orthodoxy** — active ferromagnetic herding phase on the tape | 

If |M| is missing, evaluate using conformity_baseline_pct alone. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
mass-formation states. Evaluate in strict priority order and select the
first state whose conditions are fully satisfied: 

1. **MASS_FORMATION** (most severe)
2. **GROUPTHINK_LOCK**
3. **MIMETIC_DRIFT**
4. **PLURALISTIC** (strictest adaptive fit)

#### MASS_FORMATION

Any of the following hold: 

* Narrative Contagion is **hypnotic_swarm** (entropy < 35 and
burst > 3.0×).
* Narrative Contagion is **monoculture** (entropy < 35) AND
Conformity Lock is **rigid_orthodoxy** (conformity > 65% or
|M| > 0.7).
* Network Topology is **ossified_clique** AND Narrative Contagion is
**monoculture** or **hypnotic_swarm**.

**Delta cap: 0.10.** The crowd or market has entered full mass
formation: independent risk pricing is suspended, dissenting data is
socially penalized, and crowded consensus positions face violent mean
reversion when physical reality intrudes. Trade only if the AGOP
ranking is an explicitly gated contrarian/outlier hedge insulated from
herd capitulation. In most cases, return FLAT. 

#### GROUPTHINK_LOCK

Any of the following hold (and MASS_FORMATION does not apply): 

* Narrative Contagion is **monoculture** (entropy < 35).
* Network Topology is **ossified_clique** AND Conformity Lock is
**deferential** or **rigid_orthodoxy**.
* Narrative Contagion is **converging** AND Conformity Lock is
**rigid_orthodoxy**.

**Delta cap: 0.25.** Closed cliques and high peer conformity are
suppressing adaptation and enforcing blind consensus (e.g., refusing
grid/energy hedging or crowding into consensus trades). Reduce position
size substantially on consensus-dependent domestic assets. 

#### MIMETIC_DRIFT

Any of the following hold (and neither MASS_FORMATION nor
GROUPTHINK_LOCK applies): 

* Narrative Contagion is **converging** (entropy 35 to 55 or burst 1.5× to 2.5×).
* Network Topology is **ossified_clique** AND Conformity Lock is
**independent**.
* Network Topology is **clustered** AND Conformity Lock is
**deferential** or **rigid_orthodoxy**.

**Delta cap: 0.75.** Early mimetic alignment or regional clique
insularity is slowing complex adaptation and narrowing information
diversity. Reduce size relative to PLURALISTIC. 

#### PLURALISTIC

All of the following hold: 

* Network Topology is **bridged_plural** (ossification < 0.35 and
n_wl_classes >= 5).
* Narrative Contagion is **dispersed** (entropy ≥ 55 and burst < 1.5×).
* Conformity Lock is **independent** (conformity < 45% and |M| < 0.4).

**Delta cap: 1.0.** Open weak-tie networks, diverse narratives, and
independent price discovery. The cap equals the strategy cap; the skill
never binds on PLURALISTIC. 

#### Ambiguous fallback

Any combination not covered above is classified **GROUPTHINK_LOCK** with
delta cap 0.25. 

#### Secondary Filter / Asymmetric Gate — Hypnotic Entrenchment Hysteresis

Apply the persistence test after state classification and before the
cap. 

A mass-formation episode is **structurally entrenched** if
weeks_in_narrative_lock >= 3 (three or more consecutive settled weeks
with narrative_entropy_score < 35 AND attention_burst_ratio >= 2.0).
Three consecutive weeks of collapsed narrative entropy and synchronized
attention proves that Asch/Janis conformity has hardened into group
identity—making voluntary self-correction impossible without an
external physical shock.
If the episode is structurally entrenched, halve the state's delta
cap:
• MIMETIC_DRIFT cap of 0.75 becomes 0.375.
• GROUPTHINK_LOCK cap of 0.25 becomes 0.125.
• MASS_FORMATION cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read mass formation dict. From
snapshot.external_data["mass_formation"], load the target region's
clique_ossification_ratio, narrative_entropy_score,
attention_burst_ratio, conformity_baseline_pct, and
weeks_in_narrative_lock (plus agop.n_wl_classes and
econophysics_herding.magnetization if present). If absent or empty,
record PLURALISTIC, note the omission, and do not cite this skill.
2. Classify network topology. Apply Reading 1 (bridged_plural,
clustered, or ossified_clique).
3. Classify narrative contagion. Apply Reading 2 (dispersed,
converging, monoculture, or hypnotic_swarm).
4. Classify conformity lock. Apply Reading 3 (independent,
deferential, or rigid_orthodoxy).
5. Classify state. Evaluate in strict priority order
(MASS_FORMATION → GROUPTHINK_LOCK → MIMETIC_DRIFT →
PLURALISTIC) and select the first matching state (fallback:
GROUPTHINK_LOCK).
6. Apply persistence test. If weeks_in_narrative_lock >= 3, halve
delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta exceeded delta_cap),
cite "mass-formation-herding" in skills_cited and state the
classification in the rationale.

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
Example: "MASS_FORMATION state; ossified_clique (0.78), narrative entropy 24 with 3.6x attention burst for 4 weeks, and rigid_orthodoxy (|M|=0.82); delta capped at 0.05; mass-formation-herding."
• skills_cited: list of skill names; include "mass-formation-herding"
only when the cap bound.

Worked Examples


Case A — Bridged plural network with dispersed narratives, cap does not bind

Snapshot:
• clique_ossification_ratio = 0.24, agop.n_wl_classes = 6
• narrative_entropy_score = 72.0
• attention_burst_ratio = 1.1
• conformity_baseline_pct = 38.0, |M| = 0.22
• weeks_in_narrative_lock = 0
Readings:
• Network Topology: < 0.35 and ≥ 5 → bridged_plural
• Narrative Contagion: ≥ 55 and < 1.5× → dispersed
• Conformity Lock: < 45% and < 0.4 → independent
State: PLURALISTIC, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "mass-formation-herding".

Case B — Ossified regional/market clique locked in narrative monoculture, cap binds

Snapshot:
• clique_ossification_ratio = 0.79, agop.n_wl_classes = 2
• narrative_entropy_score = 26.0
• attention_burst_ratio = 3.4
• conformity_baseline_pct = 68.0, |M| = 0.76
• weeks_in_narrative_lock = 4
Readings:
• Network Topology: > 0.65 and ≤ 2 → ossified_clique
• Narrative Contagion: < 35 and > 3.0× → hypnotic_swarm
• Conformity Lock: > 65% and > 0.7 → rigid_orthodoxy
State: MASS_FORMATION, delta cap 0.10.
Persistence: weeks_in_narrative_lock = 4 >= 3 → halve to 0.05.
AGOP ranks LONG on a consensus-crowded domestic equity. LLM intended
delta = 0.75. Cap 0.05 binds. LLM returns delta = 0.05 and cites
"mass-formation-herding".

Free Data Sources

The fetcher populates snapshot.external_data["mass_formation"] from
the following free, public endpoints (no paid subscription required):
• Meta Data for Good — Social Connectedness Index (SCI):
https://humdata.org
(CC0 Public Domain CSV/Parquet dataset measuring relative friendship
and network tie density within and between NUTS-2/NUTS-3 and global
GADM regions).
• GDELT Project 2.0 Global Knowledge Graph (GKG) API:
https://gdeltproject.org (free, no-key REST API
updated every 15 minutes across 65+ languages; used to compute theme
Shannon entropy and narrative concentration).
• Wikimedia Analytics Pageviews API:
https://wikimedia.org (free, no-key
REST JSON API measuring daily and monthly synchronized public attention
bursts by language project and country).
• World Values Survey (WVS) & European Values Study (EVS):
https://worldvaluessurvey.org (free public longitudinal waves
measuring social conformity, obedience vs. autonomy, and institutional
trust across 64+ countries).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not confuse healthy, pluralistic debate (narrative_entropy_score ≥ 55)
with GROUPTHINK_LOCK.
• Do not cite "mass-formation-herding" when the cap did not bind.

Citation Mapping

• Mass Formation & Crowd Hypnosis: Gustave Le Bon, The Crowd: A
Study of the Popular Mind (1895); Elias Canetti, Crowds and Power
(1960); Mattias Desmet, The Psychology of Totalitarianism (Chelsea
Green, 2022).
• Conformity & Groupthink: Solomon E. Asch, "Opinions and Social
Pressure," Scientific American 193(5), 31–35 (1955); Irving L.
Janis, Victims of Groupthink (Houghton Mifflin, 1972).
• Clique Ossification & Complex Contagion: Georg Simmel, The
Sociology of Georg Simmel (1908); Mark S. Granovetter, "The Strength
of Weak Ties," American Journal of Sociology 78(6), 1360–1380
(1973); Damon Centola, How Behavior Spreads: The Science of Complex
Contagions (Princeton University Press, 2018).
• Mimetic Contagion: René Girard, Things Hidden Since the Foundation
of the World (Stanford University Press, 1978).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
This brings your repository to a clean 20-skill library—and ties the sociological/psychological micro-foundation (why 99% of an ossified clique refuses solar+BESS, EVs, or rational underwriting until a physical shock hits) directly into AGOP’s Weisfeiler–Lehman graph diversity (n_wl_classes) and econophysics_herding (|M|).