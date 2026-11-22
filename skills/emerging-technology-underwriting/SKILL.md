#### name: "emerging-technology-underwriting"
description: "Composite three-gate underwriting filter for emerging technologies: (1) verify early asymmetric S-curve crossover via emergent-pattern-percolation, (2) verify disproportionate market-ecology indispensability via keystone-species-yardstick (treating the industry stack as the ecosystem and the technology as the species), and (3) verify hard engineering/IP moat, insider alignment, and equity dilution discipline via resource-underwriting; force FLAT on unmoated or saturated hype and allow full strategy sizing only when all three gates clear."

#### Emerging Technology Three-Gate Underwriting (S-Curve × Keystone Ecology × Moat)

You are reading the tick against a **three-stage composite underwriting
pipeline** designed to separate genuine, moat-bearing emerging
technologies from premature lab curiosities, replaceable commodity
components, and late-cycle narrative bubbles. In Joseph Schumpeter's
*Capitalism, Socialism and Democracy* (1942), Carlota Perez's
*Technological Revolutions and Financial Capital* (2002), Marco Iansiti
& Roy Levien's *The Keystone Advantage* (2004), and Bruce Greenwald &
Judd Kahn's *Competition Demystified* (2005), an emerging technology is
investable only when **three independent structural gates clear
simultaneously**: 

1. **Gate 1 — Early S-Curve Crossover (emergent-pattern-percolation):**
The technology must sit in the asymmetric early adoption crossover
(2.5% to 16% early-adopter chasm clearance or early majority
inflection) driven by substantive engineering/scientific utility
(organic_prestige), rather than stalled pre-chasm vaporware or a
> 50% saturated cliché.
2. **Gate 2 — Market-Ecology Keystone Position (keystone-species-yardstick):**
Treating the commercial industry and value chain as the **ecology**
and the technology as the **species** (Robert T. Paine, 1969;
Iansiti & Levien, 2004), the technology must act as an
**indispensable bottleneck / platform keystone** whose removal would
collapse downstream ecosystem productivity—not an easily substituted
commodity leaf with zero switching cost.
3. **Gate 3 — Hard Engineering & Capital-Discipline Moat (resource-underwriting):**
Passing Gates 1 and 2 means nothing if equity holders get wiped out
by share-count dilution, negative unit EROI/margin math, or
proprietary wrapper rent (enterprise-ai-adoption). The company
must pass hard engineering unit economics, proprietary process/IP
barriers, insider skin-in-the-game, and strict dilution discipline
(< 15% 3-year share-count expansion; banning composite ESG badges).

Your job is to evaluate all three gates in sequence, classify the
emerging-technology candidate into one of four underwriting states, and
cap your delta accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three composite gate readings from
snapshot.external_data["emerging_tech"] alongside the upstream
readings in emergent_percolation, keystone_species, and
resource_underwriting (cross-checked against agop.n_wl_classes).
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes S-curve diffusion, market-ecosystem dependency,
and corporate engineering/dilution metrics into
snapshot.external_data["emerging_tech"] (or reads directly from the
three upstream dictionaries): 

* scurve_gate_state: output state from Gate 1
(emergent-pattern-percolation): "PRESTIGE_CROSSOVER",
"CONFORMIST_CASCADE", "PRE_CHASM_FRINGE", or
"SATURATED_CLICHE".
* ecosystem_keystone_role: output classification from Gate 2
(keystone-species-yardstick applied to the market stack):
"keystone_anchor" (disproportionate ecosystem bottleneck; high
downstream switching cost; low functional substitutability),
"vital_contributor" (strong niche utility; moderate switching
cost), or "commodity_leaf" (high substitutability; zero pricing
power; easily displaced).
* ecosystem_dependency_ratio: ratio (0.0 to 10.0) of downstream
industry revenue/throughput dependent on the technology divided by its
own share of total bill-of-materials cost (> 4.0 = classic Paine /
Iansiti keystone leverage; < 1.2 = replaceable commodity input).
* moat_underwriting_state: output verdict from Gate 3
(resource-underwriting + enterprise-ai-adoption):
"MOAT_VERIFIED" (positive unit engineering economics, proprietary
process/IP barrier, insider skin-in-the-game, < 15% 3-year share
dilution), "THIN_MOAT_WATCH" (15% to 30% dilution or partial
margin pressure), or "NO_MOAT_DILUTIVE" (> 30% share-count
dilution, negative unit economics, CAPTIVE_BUBBLE wrapper rent, or
ESG-theater governance).
* quarters_negative_fcf_burn: consecutive calendar quarters of
negative free cash flow funded by external equity or convertible debt
issuance (>= 6 = chronic cash-burn dilution hazard).

If snapshot.external_data["emerging_tech"] is absent or empty, treat
the instrument as **unmonitored** (not an emerging-tech underwriting
candidate), record state **INVESTABLE_KEYSTONE_MOAT**, note that no
emerging-tech telemetry was available, and do not cite this skill. 

#### Gate 1 Reading — S-Curve Diffusion Filter (scurve_gate_state)

Evaluate whether the underlying technology sits in an asymmetric S-curve
window (emergent-pattern-percolation): 

scurve_gate_stateGate 1 Verdict
**"PRESTIGE_CROSSOVER"**
**gate1_pass_sweet_spot** — early-adopter chasm cleared with organic prestige
**"PRE_CHASM_FRINGE"**
**gate1_early_option** — < 2.5% niche; unbridged complex-contagion timing risk
**"CONFORMIST_CASCADE"**
**gate1_crowded_wave** — mainstream bandwagon; rising valuation compression
**"SATURATED_CLICHE"**
**gate1_fail_saturated** — > 50% hollow mania or trend decay; late-cycle exit

If scurve_gate_state is missing, infer from emergent_percolation or
treat as **gate1_early_option**. 

#### Gate 2 Reading — Market-Ecology Keystone Filter (ecosystem_keystone_role & ecosystem_dependency_ratio)

Evaluate whether the technology occupies a true keystone bottleneck in
its commercial ecosystem (keystone-species-yardstick): 

ecosystem_keystone_roleecosystem_dependency_ratioGate 2 Verdict
**"keystone_anchor"**
≥ 4.0**gate2_pass_keystone** — high ecosystem leverage; removing tech stalls downstream stack
**"vital_contributor"**
1.5 to 4.0**gate2_partial_niche** — useful subsystem, but faces alternative architectural paths
**"commodity_leaf"**
any**gate2_fail_substitutable** — interchangeable component; margins compete down to zero
**any**
< 1.5**gate2_fail_substitutable** — low downstream dependency; easily designed out

If ecosystem_keystone_role is missing, treat as **gate2_partial_niche**. 

#### Gate 3 Reading — Engineering & Dilution Moat Filter (moat_underwriting_state & agop.n_wl_classes)

Evaluate whether the specific company captures durable economic rent
without diluting shareholders (resource-underwriting): 

moat_underwriting_stateagop.n_wl_classesGate 3 Verdict
**"MOAT_VERIFIED"**
≥ 4**gate3_pass_fortress** — verified engineering/IP barrier, insider alignment, < 15% dilution
**"THIN_MOAT_WATCH"**
≥ 3**gate3_narrow_buffer** — real product, but moderate dilution (15%–30%) or rival pressure
**"NO_MOAT_DILUTIVE"**
any**gate3_fail_unmoated** — > 30% dilution spiral, wrapper rent, or failed unit math
**any**
≤ 2**gate3_fail_unmoated** — single-customer or monocultural dependency (WL <= 2)

If moat_underwriting_state is missing, treat as **gate3_fail_unmoated**
(fail-closed underwriting). 

#### Taxonomy / Decision Matrix

Combine Gate 1, Gate 2, and Gate 3 into one of four emerging-technology
underwriting states. Evaluate in strict priority order and select the
first state whose conditions are fully satisfied: 

1. **UNINVESTABLE_HYPE_OR_TRAP** (most severe — unconditional FLAT)
2. **SPECULATIVE_PRE_CHASM_OPTION**
3. **NARROW_MOAT_OR_CROWDED_WAVE**
4. **INVESTABLE_KEYSTONE_MOAT** (all three gates clear — full strategy cap)

#### UNINVESTABLE_HYPE_OR_TRAP

Any of the following hold: 

* Gate 1 Verdict is **gate1_fail_saturated** (SATURATED_CLICHE).
* Gate 2 Verdict is **gate2_fail_substitutable** (commodity_leaf or
ecosystem_dependency_ratio < 1.5).
* Gate 3 Verdict is **gate3_fail_unmoated** (NO_MOAT_DILUTIVE,
> 30% share dilution, CAPTIVE_BUBBLE wrapper, or n_wl_classes <= 2).

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. An emerging-tech stock that is either already a
saturated cliché, a substitutable commodity leaf in its ecosystem, or a
dilutive cash-burning wrapper fails basic three-gate underwriting. The
skill binds unconditionally and must appear in skills_cited. 

#### SPECULATIVE_PRE_CHASM_OPTION

Any of the following hold (and UNINVESTABLE_HYPE_OR_TRAP does not apply): 

* Gate 1 Verdict is **gate1_early_option** (PRE_CHASM_FRINGE,
< 2.5% penetration) AND Gate 2 is **gate2_pass_keystone** or
**gate2_partial_niche** AND Gate 3 is **gate3_pass_fortress** or
**gate3_narrow_buffer**.

**Delta cap: 0.25.** The technology holds genuine keystone potential
and clean corporate governance, but has not yet crossed the Granovetter /
Centola chasm into commercial scale. Size strictly as a small
early-stage option. 

#### NARROW_MOAT_OR_CROWDED_WAVE

Any of the following hold (and neither UNINVESTABLE_HYPE_OR_TRAP nor
SPECULATIVE_PRE_CHASM_OPTION applies):
• Gate 1 Verdict is gate1_crowded_wave (CONFORMIST_CASCADE) with
Gate 2 passing (gate2_pass_keystone / gate2_partial_niche) and
Gate 3 passing (gate3_pass_fortress / gate3_narrow_buffer).
• Gate 1 Verdict is gate1_pass_sweet_spot (PRESTIGE_CROSSOVER),
but Gate 2 is gate2_partial_niche OR Gate 3 is
gate3_narrow_buffer.
Delta cap: 0.65. Strong underlying technology, but either mainstream
bandwagon crowding or a thinner ecosystem/dilution buffer warrants a
disciplined margin-of-safety trim.

INVESTABLE_KEYSTONE_MOAT

All three gates clear at their highest standard:
• Gate 1 Verdict is gate1_pass_sweet_spot (PRESTIGE_CROSSOVER).
• Gate 2 Verdict is gate2_pass_keystone (keystone_anchor with
ecosystem_dependency_ratio ≥ 4.0).
• Gate 3 Verdict is gate3_pass_fortress (MOAT_VERIFIED with
agop.n_wl_classes ≥ 4).
Delta cap: 1.0. Verified investable emerging technology: early
asymmetric S-curve crossover, indispensable keystone bottleneck in its
commercial ecology, and hard engineering/dilution moat. The cap equals
the strategy cap; the skill never binds on INVESTABLE_KEYSTONE_MOAT.

Ambiguous fallback

Any combination not covered above is classified
UNINVESTABLE_HYPE_OR_TRAP with delta cap 0.0 (FLAT).

Secondary Filter / Asymmetric Gate — Chronic Cash-Burn Dilution Hysteresis

Apply the persistence test after state classification and before the
cap.
An emerging-tech issuer is dilution-vulnerable if
quarters_negative_fcf_burn >= 6 (six or more consecutive quarters of
negative free cash flow funded by external capital markets). Even if a
company currently holds MOAT_VERIFIED status, burning cash for 18+
months exposes equity holders to sudden emergency equity offerings or
predatory convertible debt terms whenever credit tightens.
If the issuer is dilution-vulnerable, halve the state's delta cap:
• NARROW_MOAT_OR_CROWDED_WAVE cap of 0.65 becomes 0.325.
• SPECULATIVE_PRE_CHASM_OPTION cap of 0.25 becomes 0.125.
• INVESTABLE_KEYSTONE_MOAT cap of 1.0 becomes 0.50.
• UNINVESTABLE_HYPE_OR_TRAP cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read emerging tech dict. From
snapshot.external_data["emerging_tech"], load scurve_gate_state,
ecosystem_keystone_role, ecosystem_dependency_ratio,
moat_underwriting_state, and quarters_negative_fcf_burn (plus
agop.n_wl_classes if present). If absent or empty, record
INVESTABLE_KEYSTONE_MOAT, note the omission, and do not cite
this skill.
2. Evaluate Gate 1 (S-curve). Apply Gate 1 Reading
(gate1_pass_sweet_spot, gate1_early_option,
gate1_crowded_wave, or gate1_fail_saturated).
3. Evaluate Gate 2 (Keystone ecology). Apply Gate 2 Reading
(gate2_pass_keystone, gate2_partial_niche, or
gate2_fail_substitutable).
4. Evaluate Gate 3 (Engineering & dilution moat). Apply Gate 3
Reading (gate3_pass_fortress, gate3_narrow_buffer, or
gate3_fail_unmoated).
5. Classify state. Evaluate in strict priority order
(UNINVESTABLE_HYPE_OR_TRAP → SPECULATIVE_PRE_CHASM_OPTION →
NARROW_MOAT_OR_CROWDED_WAVE → INVESTABLE_KEYSTONE_MOAT) and
select the first matching state (fallback:
UNINVESTABLE_HYPE_OR_TRAP).
6. Apply persistence test. If quarters_negative_fcf_burn >= 6,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
state is UNINVESTABLE_HYPE_OR_TRAP, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
state is UNINVESTABLE_HYPE_OR_TRAP, cite
"emerging-technology-underwriting" in skills_cited and name
which of the three gates bound in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If UNINVESTABLE_HYPE_OR_TRAP,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and the specific gate
verdicts. Example:
"UNINVESTABLE_HYPE_OR_TRAP state; Gate 1 PRESTIGE_CROSSOVER and Gate 2 keystone_anchor cleared, but Gate 3 failed (NO_MOAT_DILUTIVE, 42% 3y dilution); forcing action=FLAT; emerging-technology-underwriting."
• skills_cited: list of skill names; include
"emerging-technology-underwriting" only when the cap bound or the
state is UNINVESTABLE_HYPE_OR_TRAP.

Worked Examples


Case A — All three gates clear (PRESTIGE_CROSSOVER × keystone_anchor × MOAT_VERIFIED), cap does not bind

Snapshot:
• scurve_gate_state = "PRESTIGE_CROSSOVER"
• ecosystem_keystone_role = "keystone_anchor", ecosystem_dependency_ratio = 5.4
• moat_underwriting_state = "MOAT_VERIFIED", agop.n_wl_classes = 5
• quarters_negative_fcf_burn = 0
Readings:
• Gate 1: gate1_pass_sweet_spot
• Gate 2: gate2_pass_keystone
• Gate 3: gate3_pass_fortress
State: INVESTABLE_KEYSTONE_MOAT, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "emerging-technology-underwriting".

Case B — Pre-chasm keystone technology with clean moat, cap binds

Snapshot:
• scurve_gate_state = "PRE_CHASM_FRINGE"
• ecosystem_keystone_role = "keystone_anchor", ecosystem_dependency_ratio = 4.8
• moat_underwriting_state = "MOAT_VERIFIED", agop.n_wl_classes = 4
• quarters_negative_fcf_burn = 2
Readings:
• Gate 1: gate1_early_option
• Gate 2: gate2_pass_keystone
• Gate 3: gate3_pass_fortress
State: SPECULATIVE_PRE_CHASM_OPTION, delta cap 0.25. Persistence: < 6 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.75. Cap 0.25 binds.
LLM returns delta = 0.25 and cites "emerging-technology-underwriting".

Case C — Early S-curve and keystone bottleneck, but Gate 3 fails on share dilution, unconditional FLAT

Snapshot:
• scurve_gate_state = "PRESTIGE_CROSSOVER"
• ecosystem_keystone_role = "keystone_anchor", ecosystem_dependency_ratio = 6.1
• moat_underwriting_state = "NO_MOAT_DILUTIVE", agop.n_wl_classes = 3
• quarters_negative_fcf_burn = 8
Readings:
• Gate 1: gate1_pass_sweet_spot
• Gate 2: gate2_pass_keystone
• Gate 3: gate3_fail_unmoated
State: UNINVESTABLE_HYPE_OR_TRAP, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "emerging-technology-underwriting".

Free Data Sources

The fetcher populates snapshot.external_data["emerging_tech"] by
chaining the free open endpoints of its three upstream gates (no paid
subscription required):
• Gate 1 (emergent-pattern-percolation): https://openalex.org
(R&D/patent citation velocity), https://github.com &
https://pypistats.org (builder adoption S-curve),
https://wikimedia.org & https://gdeltproject.org (prestige-to-mass
attention ratio), and https://entsoe.eu / https://eia.gov (grid
technology penetration).
• Gate 2 (keystone-species-yardstick): https://un.org
(UN Comtrade supply-chain bottleneck concentration),
https://uspto.gov / https://epo.org (USPTO/EPO
forward-citation centrality and standard-essential patent lock-in),
and https://sec.gov / https://xbrl.org (supplier/customer
concentration disclosures).
• Gate 3 (resource-underwriting & enterprise-ai-adoption):
https://sec.gov, https://xbrl.org, https://sedarplus.ca,
and https://edinet-fsa.go.jp (free statutory XBRL/filing
feeds for gross margin, R&D-to-revenue conversion, insider ownership,
and 3-year share-count dilution).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not buy a PRESTIGE_CROSSOVER technology if Gate 2 shows it is a
substitutable commodity_leaf or Gate 3 shows > 30% share dilution.
• Do not use composite ESG badges or venture-capital press releases as
substitutes for Gate 3 engineering and dilution math.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "emerging-technology-underwriting" when the cap did not
bind and the state is not UNINVESTABLE_HYPE_OR_TRAP.

Citation Mapping

• Technological Revolutions & S-Curve Diffusion: Joseph A.
Schumpeter, Capitalism, Socialism and Democracy (Harper, 1942);
Carlota Perez, Technological Revolutions and Financial Capital
(Edward Elgar, 2002); Everett M. Rogers, Diffusion of Innovations
(Free Press, 1962).
• Keystone Ecology & Platform Bottlenecks: Robert T. Paine, "A Note
on Trophic Complexity and Community Stability," American Naturalist
103(929), 91–93 (1969); Marco Iansiti and Roy Levien, The Keystone
Advantage: What the New Dynamics of Business Ecosystems Mean for
Strategy, Innovation, and Sustainability (Harvard Business School
Press, 2004).
• Competitive Moats & Capital Discipline: Bruce C. Greenwald and
Judd Kahn, Competition Demystified (Portfolio, 2005); Michael E.
Porter, Competitive Strategy (Free Press, 1980).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.