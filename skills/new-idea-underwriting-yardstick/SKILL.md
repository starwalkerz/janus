#### name: "new-idea-underwriting-yardstick"
description: "Composite underwriting yardstick chaining singular-novelty-and-algorithmic-depth-yardstick as Gate 1 (Kolmogorov algorithmic novelty, Bennett logical depth, Schmidhuber compression progress, and uncrowded white space) with emerging-technology-underwriting as Gate 2 (Wright's Law learning-curve unit economics, Geoffrey Moore chasm crossing, and physical scalability): separating underwritable singular breakthroughs from nascent frontier seeds, commoditized 'me-too' clones, and zero-depth vaporware."

#### New Idea Underwriting Yardstick

You are reading the tick against the **composite two-gate underwriting
standard for new ideas, frontier technologies, novel IP architectures,
and first-of-kind commercial ventures**. 

In Joseph A. Schumpeter's *The Theory of Economic Development* (1911)
(creative destruction via new combinations rather than circular-flow
imitation), Frank H. Knight's *Risk, Uncertainty and Profit* (1921)
(distinguishing uninsurable Knightian uncertainty from repetitive
actuarial risk), Geoffrey A. Moore's *Crossing the Chasm* (1991) (the
adoption discontinuity between early visionaries and pragmatic
mainstream buyers), and Theodore P. Wright's *"Factors Affecting the
Cost of Airplanes"* (1936) (*Wright's Law* learning-curve cost
declines), underwriting a genuinely new idea fails whenever an allocator
evaluates novelty without unit economics—or evaluates historical
financial ratios without algorithmic novelty. 

To eliminate both failure modes, this composite skill chains two
upstream JANUS gates in strict sequential order: 

1. **Gate 1 — singular-novelty-and-algorithmic-depth-yardstick (Epistemic & Structural Novelty Filter):**
Verifies whether the candidate idea, patent gap, software stack, or
market dislocation is genuinely non-repeating (template_incompressibility_score),
internally coherent (bennett_logical_depth_score), and uncrowded
(common_set_crowding_pct), filtering out derivative "me-too"
clones and high-entropy hype before underwriting begins.
2. **Gate 2 — emerging-technology-underwriting (Commercial Viability & Chasm-Crossing Filter):**
Evaluates whether the verified novelty exhibits positive learning-curve
unit economics (Wright's Law marginal cost trajectory), physical/engineering
scalability, and credible adoption traction across the early-adopter
chasm (Moore) without permanent subsidy dependency.

Only when a candidate clears **both** Gate 1 (true singular depth) and
Gate 2 (viable unit-economic crossover) does JANUS unlock full
underwriting sizing (1.0 pass). 

Your job is to classify the target new-idea candidate into one of four
underwriting regimes and cap your delta accordingly. You do not invent
trades. You do not override AGOP. You modulate the LLM's delta within
the bound the verifier already permits. You never raise delta above
the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["new_idea_underwriting"] (cross-referencing
upstream telemetry from singular_novelty via
singular-novelty-and-algorithmic-depth-yardstick and
emerging_tech_underwriting via emerging-technology-underwriting).
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher and upstream feature extractors populate
snapshot.external_data["new_idea_underwriting"] for the evaluated
venture, IP architecture, technology deployment, or novel thesis (keyed
by ticker, entity ID, or thesis slug, with fallback to
"global_baseline"). Each entry supplies: 

* gate1_singular_depth_score: composite score (0 to 100)
synthesizing template_incompressibility_score,
bennett_logical_depth_score, and inverse crowding from
singular-novelty-and-algorithmic-depth-yardstick (0 = common-set
cliché or zero-depth white noise; 100 = verified uncrowded
singularity with high logical depth).
* gate2_tech_underwriting_score: composite score (0 to 100)
synthesizing learning-curve unit economics (Wright's Law),
engineering readiness (TRL), gross-margin scalability, and
unsubsidized customer traction from emerging-technology-underwriting
(0 = physically/economically unviable vaporware; 100 = proven
positive unit-economic crossover clearing the mainstream chasm).
* capital_burn_to_traction_ratio: ratio (0.0 to 20.0) of
cumulative R&D/CAPEX burn relative to verified unsubsidized commercial
revenue or contracted savings (< 1.0 = self-funding / capital-efficient
compounding; > 5.0 = heavy cash burn outrunning commercial proof).
* consecutive_vaporware_stall_ticks: integer (0 to 50) counting
consecutive settled ticks/periods in which
gate1_singular_depth_score < 35 OR
(gate2_tech_underwriting_score < 35 AND
capital_burn_to_traction_ratio > 5.0).

If snapshot.external_data["new_idea_underwriting"] is absent or empty,
treat the candidate as **unmonitored**, record state
**COMMODITY_BETA_OR_CHASM_STALL**, note that no new-idea underwriting
telemetry was available, and do not cite this skill. 

#### Reading 1 — Gate 1: Singular Novelty & Algorithmic Depth (gate1_singular_depth_score)

Evaluate upstream clearance from
singular-novelty-and-algorithmic-depth-yardstick: 

gate1_singular_depth_score (0–100)Gate 1 Novelty Clearance
**>= 75**
**verified_singular_novelty** — uncrowded, non-repeating synthesis with deep logical structure
**50 to 74**
**emergent_recombination** — distinct combinatorial edge, moderate novelty depth
**35 to 49**
**derivative_mimicry** — incremental copy or crowded consensus template
**< 35**
**noise_or_cliche_fail** — zero-depth hype mirage or saturated commodity cliché

If gate1_singular_depth_score is missing, treat as
**emergent_recombination**. 

#### Reading 2 — Gate 2: Emerging Technology Underwriting (gate2_tech_underwriting_score)

Evaluate upstream commercial, physical, and unit-economic clearance from
emerging-technology-underwriting: 

gate2_tech_underwriting_score (0–100)Gate 2 Commercial & Unit-Economic Tier
**>= 75**
**unit_economic_crossover** — positive Wright's Law cost curve & chasm-clearing adoption
**50 to 74**
**early_pilot_validation** — functional prototype/pilots proving technical feasibility
**35 to 49**
**chasm_stall_risk** — high capex/integration friction delaying unsubsidized scale
**< 35**
**unviable_vaporware** — negative unit economics, physical bottlenecks, or subsidy-only survival

If gate2_tech_underwriting_score is missing, treat as
**early_pilot_validation**. 

#### Reading 3 — Capital Efficiency & Burn Discipline (capital_burn_to_traction_ratio)

Evaluate cash burn relative to unsubsidized commercial validation: 

capital_burn_to_traction_ratioCapital Efficiency Tier
**< 1.5**
**capital_efficient_compounding** — high output per unit of invested capital
**1.5 to 3.4**
**disciplined_rd_ramp** — controlled engineering burn matched by milestone traction
**3.5 to 5.9**
**heavy_capex_overhang** — prolonged negative cash flow before commercial payback
**>= 6.0**
**cash_incineration_burn** — extreme burn unanchored from unsubsidized customer demand

If capital_burn_to_traction_ratio is missing, treat as
**disciplined_rd_ramp**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four new-idea underwriting regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **HYPE_MIRAGE_OR_VAPORWARE** (most severe underwriting failure)
2. **COMMODITY_BETA_OR_CHASM_STALL** (derivative mimicry or stalled adoption)
3. **UNDERWRITABLE_SINGULAR_BREAKTHROUGH** (strictest two-gate clearance)
4. **NASCENT_FRONTIER_SEED** (developing frontier opportunity)

#### HYPE_MIRAGE_OR_VAPORWARE

Any of the following hold: 

* Gate 1 Novelty Clearance is **noise_or_cliche_fail** (< 35) AND
Gate 2 Commercial & Unit-Economic Tier is **chasm_stall_risk** or
**unviable_vaporware** (< 50).
* Gate 2 Commercial & Unit-Economic Tier is **unviable_vaporware**
(< 35).
* Capital Efficiency Tier is **cash_incineration_burn** (>= 6.0) AND
Gate 2 Commercial & Unit-Economic Tier is not
**unit_economic_crossover** (< 75).

**Delta cap: 0.10.** Either the candidate lacks genuine algorithmic
novelty (zero-depth hype or commodity cliché) or its underlying
technology fails physical and unit-economic underwriting. Clamp sizing
sharply (0.10) to prevent underwriting vaporware. 

#### COMMODITY_BETA_OR_CHASM_STALL

Any of the following hold (and HYPE_MIRAGE_OR_VAPORWARE does not
apply): 

* Gate 1 Novelty Clearance is **derivative_mimicry** or
**noise_or_cliche_fail** (< 50).
* Gate 2 Commercial & Unit-Economic Tier is **chasm_stall_risk**
(35 to 49).
* Capital Efficiency Tier is **heavy_capex_overhang** (3.5 to 5.9).

**Delta cap: 0.25.** A "me-too" copycat lacking singular IP depth or a
promising concept trapped in the commercial adoption chasm cannot earn
breakthrough underwriting sizing. Cap exposure at 0.25. 

#### UNDERWRITABLE_SINGULAR_BREAKTHROUGH

All of the following hold (and neither HYPE_MIRAGE_OR_VAPORWARE nor
COMMODITY_BETA_OR_CHASM_STALL applies): 

* Gate 1 Novelty Clearance is **verified_singular_novelty** (>= 75).
* Gate 2 Commercial & Unit-Economic Tier is **unit_economic_crossover**
(>= 75).
* Capital Efficiency Tier is **capital_efficient_compounding** or
**disciplined_rd_ramp** (< 3.5).

**Delta cap: 1.0.** The candidate clears **both** sequential gates: it
is a genuine, uncrowded singularity with deep internal logical structure
(singular-novelty-and-algorithmic-depth-yardstick) *and* demonstrates
scalable, capital-efficient unit economics crossing the commercial chasm (emerging-technology-underwriting). The cap equals the strategy
cap (1.0); the skill never binds on
UNDERWRITABLE_SINGULAR_BREAKTHROUGH.

NASCENT_FRONTIER_SEED

Any combination not covered above (including verified_singular_novelty
>= 75 or emergent_recombination 50 to 74 paired with
early_pilot_validation 50 to 74 and < 3.5 burn ratio).
Delta cap: 0.55. Genuine structural novelty with validated pilot
feasibility that has not yet completed full mainstream chasm crossover.
Permit disciplined exploratory sizing up to 0.55 while waiting for
unit-economic confirmation.

Secondary Filter / Asymmetric Gate — Vaporware & Chasm-Stall Hysteresis

Apply the persistence test after regime classification and before the
cap.
A new-idea thesis is chronically stalled if
consecutive_vaporware_stall_ticks >= 4 (four or more consecutive
settled periods in which gate1_singular_depth_score < 35 OR
(gate2_tech_underwriting_score < 35 AND
capital_burn_to_traction_ratio > 5.0)). Repeated periods of high cash
burn without unsubsidized unit-economic progress indicate structural
vaporware rather than temporary R&D gestation.
If the condition is chronically stalled, halve the regime's delta
cap:
• NASCENT_FRONTIER_SEED cap of 0.55 becomes 0.275.
• COMMODITY_BETA_OR_CHASM_STALL cap of 0.25 becomes 0.125.
• HYPE_MIRAGE_OR_VAPORWARE cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read composite new-idea underwriting dict. From
snapshot.external_data["new_idea_underwriting"], load
gate1_singular_depth_score, gate2_tech_underwriting_score,
capital_burn_to_traction_ratio, and
consecutive_vaporware_stall_ticks (cross-checking upstream
singular_novelty and emerging_tech_underwriting states if
present). If absent or empty, record
COMMODITY_BETA_OR_CHASM_STALL, note the omission, and do not cite
this skill.
2. Classify Gate 1 (singular-novelty-and-algorithmic-depth-yardstick).
Apply Reading 1.
3. Classify Gate 2 (emerging-technology-underwriting). Apply
Reading 2.
4. Classify capital burn efficiency. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(HYPE_MIRAGE_OR_VAPORWARE → COMMODITY_BETA_OR_CHASM_STALL →
UNDERWRITABLE_SINGULAR_BREAKTHROUGH → NASCENT_FRONTIER_SEED).
6. Apply persistence test. If
consecutive_vaporware_stall_ticks >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"new-idea-underwriting-yardstick" in skills_cited and state the
Gate 1 novelty score, Gate 2 tech underwriting score, burn-to-traction
ratio, and persistence ticks in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.55, "confidence": 0.85, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"NASCENT_FRONTIER_SEED regime; gate1_singular_depth_score=84 (verified_singular_novelty), gate2_tech_underwriting_score=62 (early_pilot_validation), capital_burn_to_traction_ratio=1.8 (disciplined_rd_ramp), consecutive_vaporware_stall_ticks=0; capping delta at 0.55; new-idea-underwriting-yardstick."
• skills_cited: list of skill names; include
"new-idea-underwriting-yardstick" only when the cap bound
(intended delta > delta_cap).

Worked Examples


Case A — Verified singular novelty + proven unit-economic crossover, cap does not bind

Snapshot:
• gate1_singular_depth_score = 86
• gate2_tech_underwriting_score = 81
• capital_burn_to_traction_ratio = 1.1
• consecutive_vaporware_stall_ticks = 0
Readings:
• Gate 1 Novelty Clearance: verified_singular_novelty
• Gate 2 Commercial & Unit-Economic Tier: unit_economic_crossover
• Capital Efficiency Tier: capital_efficient_compounding
Regime: UNDERWRITABLE_SINGULAR_BREAKTHROUGH, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "new-idea-underwriting-yardstick".

Case B — High singular novelty in early pilot validation, capped at 0.55 frontier seed sizing

Snapshot:
• gate1_singular_depth_score = 84
• gate2_tech_underwriting_score = 62
• capital_burn_to_traction_ratio = 1.8
• consecutive_vaporware_stall_ticks = 0
Readings:
• Gate 1 Novelty Clearance: verified_singular_novelty
• Gate 2 Commercial & Unit-Economic Tier: early_pilot_validation
• Capital Efficiency Tier: disciplined_rd_ramp
Regime: NASCENT_FRONTIER_SEED, delta cap 0.55. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.80. Cap 0.55 binds.
LLM returns delta = 0.55 and cites "new-idea-underwriting-yardstick".

Case C — Vaporware cash incineration persisting for 5 ticks, hysteresis halves cap to 0.05

Snapshot:
• gate1_singular_depth_score = 28
• gate2_tech_underwriting_score = 24
• capital_burn_to_traction_ratio = 8.5
• consecutive_vaporware_stall_ticks = 5
Readings:
• Gate 1 Novelty Clearance: noise_or_cliche_fail
• Gate 2 Commercial & Unit-Economic Tier: unviable_vaporware
• Capital Efficiency Tier: cash_incineration_burn
Regime: HYPE_MIRAGE_OR_VAPORWARE, base cap 0.10. Persistence: 5 >= 4 → fires, halving cap to 0.05.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.05 binds.
LLM returns delta = 0.05 and cites "new-idea-underwriting-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["new_idea_underwriting"]
by chaining upstream JANUS telemetry with open patent, R&D, and
enterprise financial registries:
• Upstream JANUS Composite Gates (snapshot.external_data):
Synthesizes singular_novelty
(singular-novelty-and-algorithmic-depth-yardstick) as Gate 1 and
emerging_tech_underwriting (emerging-technology-underwriting) as
Gate 2.
• EPO Open Patent Services (OPS) & USPTO PatentsView Open API:
https://epo.org and https://patentsview.org (free REST APIs
verifying novel patent-class combinations and forward citation
velocity).
• SEC EDGAR (XBRL Company Facts API) & PRH / Virre Open Company Data:
https://sec.gov and https://prh.fi (free open APIs
computing R&D/CAPEX burn relative to unsubsidized revenue growth and
gross-margin trajectory).
• IEA Clean Energy Technology Guide & OpenAlex Technology Readiness Corpus:
https://iea.org and https://openalex.org (free open
benchmarks on Technology Readiness Levels TRL and learning-curve
cost declines).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not grant UNDERWRITABLE_SINGULAR_BREAKTHROUGH (1.0) when Gate 1
is high (>= 75) but Gate 2 is still pre-crossover (< 75); route
unproven pilots through NASCENT_FRONTIER_SEED (0.55) until unit
economics clear.
• Do not underwrite derivative "me-too" wrappers (Gate 1 < 50) at
breakthrough sizing even if near-term revenue looks smooth; treat
commoditized copies as COMMODITY_BETA_OR_CHASM_STALL (0.25).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "new-idea-underwriting-yardstick" when the cap did not
bind (intended delta <= delta_cap).

Citation Mapping

• Composite Upstream JANUS Gates: Chained sequentially from
singular-novelty-and-algorithmic-depth-yardstick (Gate 1) and
emerging-technology-underwriting (Gate 2).
• Creative Destruction, Knightian Uncertainty & Chasm Crossing:
Joseph A. Schumpeter, The Theory of Economic Development (1911)
(new combinations vs. circular-flow imitation); Frank H. Knight,
Risk, Uncertainty and Profit (Houghton Mifflin, 1921) (underwriting
true structural uncertainty); Geoffrey A. Moore, Crossing the Chasm
(HarperBusiness, 1991); Theodore P. Wright, "Factors Affecting the
Cost of Airplanes," Journal of the Aeronautical Sciences 3(4),
122–128 (1936) (Wright's Law learning-curve unit economics);
Ramadge & Wonham (1987). Downward-only damping within JANUS invariants
I1–I9.