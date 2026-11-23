#### name: "social-cohesion-and-associational-topology-yardstick"
description: "Classify the tick by society-wide social cohesion and associational graph topology: modeling individual non-erotic bond networks via Aristotle's tripartite taxonomy (Type A utility, Type B pleasure, Type C unconditional appreciation/for-its-own-sake as tested by Dionysius of Syracuse on Damon and Pythias and paralleled in Buddhist metta), aggregating individual graphs into a systemic topological manifold governed by Spenglerian civilizational incentive matrices, and capping delta accordingly."

#### Social Cohesion & Associational Graph Topology Yardstick

You are reading the tick against the **structural social cohesion and
associational graph topology** of the target polity. In Aristotle's
*Nicomachean Ethics* (Books VIII–IX), the historical test conducted by
Dionysius of Syracuse on the Pythagoreans Damon and Pythias (recorded by
Aristoxenus and Cicero, *De Officiis* III.10), Buddhist *metta*
(unconditional goodwill for the sake of the other without precondition),
Oswald Spengler's *The Decline of the West* (1918/1922), Ludwig von
Bertalanffy's *General System Theory* (1968), and Mark Granovetter's
*"The Strength of Weak Ties"* (1973) alongside James S. Coleman's
social-capital closure (1988), a society's resilience under shock is
determined by the **mathematical topology of its non-erotic human
association graphs**. 

#### 1. The Micro-Level Graph: Tripartite Edge Taxonomy (Respect vs. Appreciation)

Every individual sits at the center of an egocentric association graph

𝐺𝑖

=

(

𝑉𝑖

,

𝐸𝑖

)
⁠ whose non-erotic edges fall into three structural
classes: 

* **Baseline Precondition — Respect:** Genuine non-erotic association
requires baseline respect across all three edge types; without
respect, the edge is performative noise rather than a real tie.
* **Weak Edge Type A (Utility — *Aristotle's khresimon*):** Associations
whose primary reason for existing is mutual functional utility
(colleagues, commercial counterparties, institutional roles, or
corporate interfaces). Type A edges require baseline respect, not
appreciation, and dissolve when utility ends.
* **Weak Edge Type B (Pleasure — *Aristotle's hedu*):** Associations
whose primary reason for existing is transient shared pastime or
enjoyment (recreational acquaintances, hospitality/service settings,
casual social circles). Type B edges are transient and require
respect without deep mutual appreciation.
* **Strong Edge Type C (Unconditional Appreciation — *Aristotle's teleia philia* / Pythagorean Bond / Buddhist *Metta*):**
Associations existing **for the sake of the other itself**, without
transactional precondition. What modern vocabulary approximates as
**appreciation** (resting atop baseline respect) distinguishes Type C
from Types A and B: 

  * Type C is neither a colleague (Type A) nor a transient pastime
(Type B).
  * Type C edges are **time-invariant and state-persistent**: they can
begin, end, go on pause for years, and resume intact without
re-negotiating preconditions.
  * While humans empirically form most Type C edges during childhood,
youth, and early adulthood, **there is no biological or lifecycle
cutoff**—humans can form Type C edges up to old age and death. The
binding constraint is **association incentive**, not chronological age.
  * Under acute stress—such as Dionysius of Syracuse's capital test on
Damon and Pythias—only Type C edges refuse to defect when survival
or convenience favors abandonment.

#### 2. The Macro-Level System: Graph Topology & Spenglerian Incentive Matrices

When individual association graphs 

Gicap G sub i
𝐺𝑖
⁠ are aggregated across an
entire population, they form a **society-wide topological manifold**

ℳ

=⋃𝑖𝐺𝑖
⁠ governed by **Systems Theory**: 

* **Spenglerian Season → Incentive Matrix → Graph Topology:** Depending
on a civilization's **Spenglerian season** (*Spring/Culture* organic
bonding, *Summer/Autumn* institutional maturation, or *Winter/Zivilisation*
hyper-monetized megalopolitan atomization), the polity generates a
specific **matrix of association incentives**.
* **Spring / Vital Topology:** High density of load-bearing **Type C
cycles and closed triangles** (high clustering coefficient),
bridged cleanly by Type A and Type B edges—producing high trust,
low transaction costs, rapid informal mutual aid, and resistance to
panic or institutional extortion.
* **Late-Winter / Atomized Topology:** The incentive matrix monetizes,
bureaucratizes, or time-starves human interaction until **Type C
edges collapse into isolated singletons**, leaving almost exclusively
transactional **Type A** (corporate/state utility) and transient
**Type B** (commercialized pastime) edges. In topological terms, the
graph loses global cohesion (disconnected components / zero
load-bearing Type C bridges), forcing the state and courts to replace
organic trust with expensive surveillance, compliance bureaucracy,
and litigation (*Tainter* complexity overhead).

Your job is to classify the target polity's associational graph topology
into one of four systemic cohesion regimes and cap your delta
accordingly. You do not invent trades. You do not override AGOP. You
modulate the LLM's delta within the bound the verifier already permits.
You never raise delta above the strategy cap, and you never invent an
action outside allowed_actions. 

#### The Readings

Compute three quantitative readings from
snapshot.external_data["social_cohesion"]. Use the qualitative tables
below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes social-capital surveys, close-confidant density
indicators, civic/voluntary association persistence, interpersonal trust
scores, and transaction-cost/litigation proxies into
snapshot.external_data["social_cohesion"]. Each country or bloc entry
(keyed by ISO-2 code such as fi, eu, se, de, uk, us, jp,
kr, ke, rw, et, in, br, or global_baseline) supplies: 

* type_c_bond_density_pct: percentage (0.0 to 100.0) of adults
reporting two or more non-kin, non-transactional **Type C confidants**
(unconditional, pause-tolerant, high-trust bonds existing for their
own sake rather than workplace utility or transient pastime).
* incentive_matrix_atomization_score: score (0 to 100) measuring
how heavily the society's Spenglerian incentive matrix penalizes
unmonetized Type C association (e.g., hyper-atomized single-person
households, extreme geographic/credential churn, commercialized
socialization, and state/corporate substitution for mutual aid;
0 = organic community incentives, 100 = pure transactional/atomized
incentive matrix).
* generalized_trust_and_reciprocity_pct: percentage (0.0 to 100.0)
affirming baseline interpersonal respect, non-defection under stress,
and generalized social trust (WVS / ESS / Afrobarometer / OECD
standardized trust & mutual-aid metric).
* consecutive_atomization_years: integer (0 to 30) counting
consecutive settled years in which type_c_bond_density_pct < 42.0
OR incentive_matrix_atomization_score >= 65.

If snapshot.external_data["social_cohesion"] is absent or empty, treat
the polity as **unmonitored**, record state **TRANSACTIONAL_EQUILIBRIUM**,
note that no social-cohesion graph telemetry was available, and do not
cite this skill. 

#### Reading 1 — Load-Bearing Type C Bond Density (type_c_bond_density_pct)

Evaluate the prevalence of unconditional, pause-tolerant **Type C
edges** (the Pythagorean / Aristotelian *teleia philia* core) across
the population: 

type_c_bond_density_pctType C Graph Density Tier
**>= 62.0%**
**dense_type_c_core** — resilient non-transactional confidant triangles across cohorts
**45.0% to 61.9%**
**moderate_type_c_network** — intact core bonds with emerging cohort thinning
**30.0% to 44.9%**
**hollowed_type_c_edges** — sharp rise in zero-confidant isolation; weak ties dominate
**< 30.0%**
**atomized_singleton_graph** — collapse of Type C bonds; pure utility/pastime network

If type_c_bond_density_pct is missing, treat as
**moderate_type_c_network**. 

#### Reading 2 — Spenglerian Incentive Matrix & Topological Atomization (incentive_matrix_atomization_score)

Evaluate whether the society's institutional and economic incentive
matrix nurtures non-transactional bonds or converts all human ties
into Type A utility and Type B commercial pastime: 

incentive_matrix_atomization_score (0–100)Systemic Incentive Tier
**< 30**
**organic_culture_incentives** — Spenglerian Spring/Summer cohesion; low friction for Type C ties
**30 to 49**
**mixed_institutional_incentives** — balanced civic/familial anchors alongside market mobility
**50 to 69**
**transactional_drift_matrix** — bureaucratic and market incentives crowd out unmonetized ties
**>= 70**
**late_winter_megalopolitan_atomization** — hyper-individualized utility/pastime matrix

If incentive_matrix_atomization_score is missing, treat as
**mixed_institutional_incentives**. 

#### Reading 3 — Baseline Respect & Non-Defection Under Stress (generalized_trust_and_reciprocity_pct)

Evaluate whether baseline respect holds across Type A, B, and C edges
and whether social ties hold under crisis rather than defecting: 

generalized_trust_and_reciprocity_pctReciprocity & Respect Tier
**>= 55.0%**
**high_non_defection_trust** — strong baseline respect; low compliance/litigation overhead
**35.0% to 54.9%**
**conditional_procedural_trust** — respect mediated by formal rules rather than personal loyalty
**20.0% to 34.9%**
**low_trust_defection_bias** — defensive suspicion; high legal and administrative friction
| < 20.0% | anomic_fragmentation — pervasive defection; breakdown of baseline interpersonal respect |
If generalized_trust_and_reciprocity_pct is missing, treat as
conditional_procedural_trust.

Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four macro-topological cohesion regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied:
1. ANOMIC_GRAPH_COLLAPSE (most severe)
2. ATOMIZED_UTILITY_SOCIETY
3. TRANSACTIONAL_EQUILIBRIUM
4. COHESIVE_PYTHAGOREAN_MANIFOLD (strictest adaptive fit)

ANOMIC_GRAPH_COLLAPSE

Any of the following hold:
• Type C Graph Density Tier is atomized_singleton_graph (< 30.0%)
AND Reciprocity & Respect Tier is anomic_fragmentation (< 20.0%).
• Systemic Incentive Tier is late_winter_megalopolitan_atomization
(>= 70) AND Type C Graph Density Tier is atomized_singleton_graph
(< 30.0%).
• Reciprocity & Respect Tier is anomic_fragmentation (< 20.0%) AND
Systemic Incentive Tier is transactional_drift_matrix or
late_winter_megalopolitan_atomization (>= 50).
Delta cap: 0.15. The society's associational manifold has fractured
into disconnected singletons governed purely by short-term utility
(Type A) and transient pastime (Type B), with chronic defection
under stress and soaring bureaucratic/surveillance overhead. Restrict
domestic sovereign, credit, and consumer exposure sharply.

ATOMIZED_UTILITY_SOCIETY

Any of the following hold (and ANOMIC_GRAPH_COLLAPSE does not apply):
• Type C Graph Density Tier is hollowed_type_c_edges or
atomized_singleton_graph (< 45.0%).
• Systemic Incentive Tier is late_winter_megalopolitan_atomization
(>= 70).
• Reciprocity & Respect Tier is low_trust_defection_bias
(20.0% to 34.9%).
Delta cap: 0.35. Load-bearing Type C bonds have thinned sharply while
Spenglerian late-cycle incentives replace organic mutual aid with state
transfers, corporate HR compliance, and commercialized pastime. Cut
domestic long sizing substantially.

TRANSACTIONAL_EQUILIBRIUM

Any of the following hold (and neither ANOMIC_GRAPH_COLLAPSE nor
ATOMIZED_UTILITY_SOCIETY applies):
• Type C Graph Density Tier is moderate_type_c_network
(45.0% to 61.9%).
• Systemic Incentive Tier is transactional_drift_matrix (50 to 69).
• Reciprocity & Respect Tier is conditional_procedural_trust
(35.0% to 54.9%).
Delta cap: 0.75. Respect and procedural compliance hold, but Type A
utility and Type B pastime increasingly outweigh unconditional Type C
bonds. Trim sizing relative to COHESIVE_PYTHAGOREAN_MANIFOLD.

COHESIVE_PYTHAGOREAN_MANIFOLD

All of the following hold:
• Type C Graph Density Tier is dense_type_c_core (>= 62.0%).
• Systemic Incentive Tier is organic_culture_incentives or
mixed_institutional_incentives (< 50).
• Reciprocity & Respect Tier is high_non_defection_trust (>= 55.0%).
Delta cap: 1.0. High density of pause-tolerant, unconditional Type C
confidant triangles paired with baseline respect and low institutional
atomization—creating low transaction costs and high crisis resilience.
The cap equals the strategy cap; the skill never binds on
COHESIVE_PYTHAGOREAN_MANIFOLD.

Ambiguous fallback

Any combination not covered above is classified
ATOMIZED_UTILITY_SOCIETY with delta cap 0.35.

Secondary Filter / Asymmetric Gate — Topological Atomization Hysteresis

Apply the persistence test after regime classification and before the
cap.
Graph atomization is topologically entrenched if
consecutive_atomization_years >= 5 (five or more consecutive settled
years in which type_c_bond_density_pct < 42.0 OR
incentive_matrix_atomization_score >= 65). Five consecutive years of
Type C edge loss and atomized incentives destroys multi-generational
bridging triangles across communities, making rapid social-capital
re-formation impossible within a single business cycle.
If the condition is topologically entrenched, halve the regime's
delta cap:
• TRANSACTIONAL_EQUILIBRIUM cap of 0.75 becomes 0.375.
• ATOMIZED_UTILITY_SOCIETY cap of 0.35 becomes 0.175.
• ANOMIC_GRAPH_COLLAPSE cap of 0.15 becomes 0.075.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read social cohesion dict. From
snapshot.external_data["social_cohesion"], load
type_c_bond_density_pct, incentive_matrix_atomization_score,
generalized_trust_and_reciprocity_pct, and
consecutive_atomization_years. If absent or empty, record
TRANSACTIONAL_EQUILIBRIUM, note the omission, and do not cite
this skill.
2. Classify Type C bond density tier. Apply Reading 1.
3. Classify Spenglerian incentive matrix tier. Apply Reading 2.
4. Classify baseline respect & non-defection trust tier. Apply
Reading 3.
5. Classify regime. Evaluate in strict priority order
(ANOMIC_GRAPH_COLLAPSE → ATOMIZED_UTILITY_SOCIETY →
TRANSACTIONAL_EQUILIBRIUM → COHESIVE_PYTHAGOREAN_MANIFOLD)
(fallback: ATOMIZED_UTILITY_SOCIETY).
6. Apply persistence test. If consecutive_atomization_years >= 5,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"social-cohesion-and-associational-topology-yardstick" in
skills_cited and state the Type C bond density, Spenglerian
incentive atomization score, trust tier, and persistence years in
the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.35, "confidence": 0.78, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"ATOMIZED_UTILITY_SOCIETY regime; type_c_bond_density_pct=38.5% (hollowed_type_c_edges), incentive_matrix_atomization_score=71 (late_winter_megalopolitan_atomization), generalized_trust_and_reciprocity_pct=48.0% (conditional_procedural_trust), consecutive_atomization_years=8 (topological hysteresis halves cap from 0.35 to 0.175); capping delta at 0.175; social-cohesion-and-associational-topology-yardstick."
• skills_cited: list of skill names; include
"social-cohesion-and-associational-topology-yardstick" only when
the cap bound (intended delta > delta_cap).

Worked Examples


Case A — High Type C confidant density with organic incentives and high non-defection trust, cap does not bind

Snapshot:
• type_c_bond_density_pct = 68.0
• incentive_matrix_atomization_score = 26
• generalized_trust_and_reciprocity_pct = 61.0
• consecutive_atomization_years = 0
Readings:
• Type C Graph Density Tier: dense_type_c_core
• Systemic Incentive Tier: organic_culture_incentives
• Reciprocity & Respect Tier: high_non_defection_trust
Regime: COHESIVE_PYTHAGOREAN_MANIFOLD, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "social-cohesion-and-associational-topology-yardstick".

Case B — Hollowed Type C bonds + late-winter atomized incentives despite procedural trust, persistence halves cap

Snapshot:
• type_c_bond_density_pct = 38.5
• incentive_matrix_atomization_score = 71
• generalized_trust_and_reciprocity_pct = 52.0
• consecutive_atomization_years = 8
Readings:
• Type C Graph Density Tier: hollowed_type_c_edges
• Systemic Incentive Tier: late_winter_megalopolitan_atomization
• Reciprocity & Respect Tier: conditional_procedural_trust
Regime: ATOMIZED_UTILITY_SOCIETY, base cap 0.35. Persistence: 8 >= 5 → fires, halving cap to 0.175.
AGOP ranks LONG on a domestic consumer/credit asset. LLM intended delta = 0.75. Cap 0.175 binds.
LLM returns delta = 0.175 and cites "social-cohesion-and-associational-topology-yardstick".

Case C — Collapsed Type C confidant graph + anomic defection bias

Snapshot:
• type_c_bond_density_pct = 24.0
• incentive_matrix_atomization_score = 78
• generalized_trust_and_reciprocity_pct = 17.5
• consecutive_atomization_years = 6
Readings:
• Type C Graph Density Tier: atomized_singleton_graph
• Systemic Incentive Tier: late_winter_megalopolitan_atomization
• Reciprocity & Respect Tier: anomic_fragmentation
Regime: ANOMIC_GRAPH_COLLAPSE, base cap 0.15. Persistence: 6 >= 5 → fires, halving cap to 0.075.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.075 binds.
LLM returns delta = 0.075 and cites "social-cohesion-and-associational-topology-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["social_cohesion"] from
the following free, open social-capital, confidant-network, and trust
surveys:
• OECD Better Life Index & Social Connections / Trust Datasets (OECD.Stat):
https://oecd.org (free SDMX API measuring share of population
with close confidants to rely on in trouble, social-network support,
and interpersonal trust).
• European Social Survey (ESS) & EU-SILC Social Participation Modules (Eurostat):
https://europeansocialsurvey.org and https://europa.eu
(free wave microdata and aggregates on frequency of non-work social
meetings, intimate confidant count, civic association membership, and
social isolation across European polities).
• World Values Survey (WVS), Afrobarometer & Latinobarómetro:
https://worldvaluessurvey.org, https://afrobarometer.org, and
https://latinobarometro.org (free cross-national wave datasets on
generalized interpersonal trust, family/friend importance, and
voluntary reciprocity across Europe, East Africa, Asia, and the
Americas).
• Statistics Finland (Tilastokeskus StatFin) Living Conditions & Household Structure:
https://stat.fi (free JSON-stat tables on single-person
household share, loneliness/isolation incidence by age and sex, and
voluntary civic activity).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not conflate Type A workplace/institutional utility or Type B
commercialized pastime with unconditional Type C bonds; evaluate
pause-tolerant appreciation (Type C) separately from baseline
procedural respect.
• Do not impose an artificial age cutoff on Type C bond formation;
evaluate the society's association incentive matrix across the
entire adult lifecycle.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "social-cohesion-and-associational-topology-yardstick"
when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Tripartite Friendship Taxonomy & Pythagorean Non-Defection Test:
Aristotle, Nicomachean Ethics, Books VIII–IX (distinguishing utility
khresimon, pleasure hedu, and unconditional virtue/appreciation
teleia philia); Aristoxenus & Marcus Tullius Cicero, De Officiis
III.10 (44 BCE) (Dionysius of Syracuse's capital test on Damon and
Pythias); Metta Sutta (Sutta Nipata 1.8) (unconditional goodwill
for its own sake without precondition).
• Graph Topology, Weak Ties & Social-Capital Closure: Mark S.
Granovetter, "The Strength of Weak Ties," American Journal of
Sociology 78(6), 1360–1380 (1973); James S. Coleman, "Social Capital
in the Creation of Human Capital," American Journal of Sociology
94, S95–S120 (1988); Robert D. Putnam, Bowling Alone (Simon &
Schuster, 2000).
• Systems Theory & Spenglerian Civilizational Seasons: Ludwig von
Bertalanffy, General System Theory (George Braziller, 1968);
Oswald Spengler, The Decline of the West (Der Untergang des
Abendlandes, 1918/1922); Stafford Beer, Brain of the Firm (1972);
Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
