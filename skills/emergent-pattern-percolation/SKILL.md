#### name: "emergent-pattern-percolation"
description: "Track any slow-building emergent pattern—cultural genres, fashion aesthetics, distributed energy/BESS adoption, open-source protocols, or financial motifs—across the Rogers/Granovetter S-curve and Boyd-Richerson prestige-to-conformist phase transition using free Wikimedia, GDELT 2.0, GitHub/PyPI, OpenAlex, MusicBrainz, and ENTSO-E/EIA telemetry alongside AGOP's Weisfeiler-Lehman classes; modulate delta across incubation, crossover, cascade, and late-cycle saturation."

#### Emergent Pattern Percolation & S-Curve Diffusion

You are reading the tick against the **slow-building percolation and
threshold diffusion dynamics** of an emergent pattern—whether a musical
genre, fashion code, distributed technology (solar + BESS + EV),
open-source protocol, or market narrative. In Everett M. Rogers's
*Diffusion of Innovations* (1962), Thomas C. Schelling's *Micromotives and
Macrobehavior* (1978), and Mark Granovetter's threshold models (1978),
new behaviors rarely appear out of nowhere: they incubate quietly inside
peripheral innovator clusters (< 2.5% penetration) until an unbroken
chain of heterogeneous adoption thresholds crosses the critical
percolation tipping point (~15%–20%), triggering nonlinear S-curve
expansion. 

Structurally, Robert Boyd & Peter Richerson (1985), Joseph Henrich
(2015), and Georg Simmel (1904) demonstrate that diffusion operates
through two distinct transmission regimes: 

1. **Prestige-Biased Niche Incubation (< 15% adoption):** High-conviction
innovators and domain tastemakers adopt the pattern for functional or
aesthetic edge while the ossified majority ignores or mocks it. For
high-commitment **complex contagions** (Damon Centola, 2018)—such as
behind-the-meter solar+BESS or demanding subcultural scenes—adoption
stalls in closed cliques until redundant peer reinforcement bridges
neighboring clusters.
2. **Conformist-Biased Cascade & Saturation (> 20% → > 50% adoption):**
Once cumulative visibility crosses the threshold (Bikhchandani,
Hirshleifer & Welch, 1992; Salganik, Dodds & Watts, 2006),
frequency-dependent conformist bias flips on: the mainstream rushes
in to avoid social or economic exclusion, eventually saturating the
pattern into a crowded cliché where originators exit and late entrants
overpay.

This skill is **domain-agnostic**: by normalizing any emergent pattern
into four dimensionless observables (cumulative_adoption_pct,
prestige_to_mass_ratio, cross_cluster_bridge_velocity, and
quarters_in_diffusion_wave), it tracks any cultural, technological,
or financial S-curve and hands off to mass-formation-herding once
late-cycle conformist crowding takes over. 

Your job is to classify the pattern into one of four diffusion phases
and cap your delta accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from
snapshot.external_data["emergent_percolation"], cross-checked against
agop.n_wl_classes (Weisfeiler–Lehman structural diversity). Use the
qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes adoption penetration, creator/tastemaker-to-mass
attention ratios, cross-cluster bridge growth, and wave duration for any
configured pattern (music/fashion tag, BESS/EV grid share, open-source
repo/package velocity, or emerging thematic cluster) into
snapshot.external_data["emergent_percolation"]: 

* cumulative_adoption_pct: estimated share (0.0 to 100.0) of the
target addressable population, grid/fleet base, or market universe
that has adopted the pattern (< 2.5% = Rogers Innovators;
2.5% to 16% = Early Adopters; 16% to 50% = Early Majority;
> 50% = Late Majority / Laggard saturation).
* prestige_to_mass_ratio: ratio (0.0 to 10.0) of high-signal
specialist/creator activity (e.g., GitHub commits, specialist registry
installs, niche scene tags, patent/OpenAlex citations) divided by
mainstream mass-media/retail attention (> 2.5 = high signal, low
hype; < 0.5 = mainstream media/retail hype far outrunning real
builder/creator substance).
* cross_cluster_bridge_velocity: trailing 90-day percentage growth
(-50 to +500) in distinct geographic regions, municipal feeders,
or network clusters adopting the pattern (> +35% = active
Centola weak-tie percolation across clusters; < 0% = stalling or
retreating).
* quarters_in_diffusion_wave: consecutive calendar quarters in which
cross_cluster_bridge_velocity > +15% OR cumulative_adoption_pct
has expanded monotonically.

If snapshot.external_data["emergent_percolation"] is absent or empty,
treat the instrument as **unmonitored**, record state
**PRESTIGE_CROSSOVER**, note that no percolation data was available,
and do not cite this skill. 

#### Reading 1 — Rogers S-curve penetration tier (cumulative_adoption_pct)

Evaluate where the pattern sits along the cumulative S-curve: 

cumulative_adoption_pctS-Curve Position
**< 2.5%**
**innovator_fringe** — pre-chasm niche; high technical/execution uncertainty
**2.5% to 16.0%**
**early_adopter_chasm** — proven utility; crossing from specialists to early adopters
**16.0% to 50.0%**
**early_majority_expansion** — post-tipping-point S-curve acceleration
**> 50.0%**
**late_saturation** — mainstream consensus cliché; diminishing marginal alpha

If cumulative_adoption_pct is missing, treat as **early_adopter_chasm**. 

#### Reading 2 — Boyd–Richerson transmission balance (prestige_to_mass_ratio & agop.n_wl_classes)

Evaluate whether diffusion is driven by genuine specialist/creator
utility or hollow conformist imitation: 

prestige_to_mass_ratioagop.n_wl_classesTransmission Regime
**≥ 2.0**
≥ 4**organic_prestige** — substantive creator/engineering lead; low crowd hype
**0.8 to 2.0**
≥ 3**balanced_diffusion** — healthy bridge between tastemakers and early majority
**< 0.8**
3 to 4**conformist_bandwagon** — mass imitation outpacing underlying substance
**< 0.5**
≤ 2**hollow_mania** — late-cycle cliché; heterogeneous signal collapsed into herd noise

If agop.n_wl_classes is missing, classify using prestige_to_mass_ratio
alone (≥ 2.0 = organic_prestige, 0.8 to 2.0 = balanced_diffusion,
0.5 to 0.8 = conformist_bandwagon, < 0.5 = hollow_mania). 

#### Reading 3 — Centola cross-cluster percolation velocity (cross_cluster_bridge_velocity)

Evaluate whether the pattern is actively bridging across independent
clusters or stalling inside a closed niche: 

cross_cluster_bridge_velocityPercolation Momentum
**≥ +35%**
**active_percolation** — breaking out across independent clusters/regions
**+10% to +35%**
**steady_seeding** — consistent multi-cluster compounding
**0% to +10%**
**clique_stall** — trapped in local pocket; complex-contagion barrier
**< 0%**
**trend_decay** — originators abandoning; fading motif

If cross_cluster_bridge_velocity is missing, treat as **steady_seeding**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
percolation states. Evaluate in strict priority order and select the
first state whose conditions are fully satisfied: 

1. **SATURATED_CLICHE** (late-cycle crowding / trend exhaustion — strictest cap)
2. **PRE_CHASM_FRINGE** (unproven niche or stalled complex contagion)
3. **CONFORMIST_CASCADE** (rapid mainstream expansion; rising crowding risk)
4. **PRESTIGE_CROSSOVER** (sweet-spot S-curve inflection — full strategy cap)

#### SATURATED_CLICHE

Any of the following hold: 

* S-Curve Position is **late_saturation** (> 50%) AND Transmission
Regime is **conformist_bandwagon** or **hollow_mania**.
* Transmission Regime is **hollow_mania** (prestige_to_mass_ratio < 0.5
and n_wl_classes <= 2).
* Percolation Momentum is **trend_decay** (< 0%) after passing
16% adoption.

**Delta cap: 0.15.** The emergent pattern has completed its Simmel /
Bourdieu cycle: originators are exiting, mainstream imitation has turned
the signal into a crowded cliché, and valuation/attention is vulnerable
to abrupt reversal (defer to mass-formation-herding if active). Reduce
position size sharply. 

#### PRE_CHASM_FRINGE

Any of the following hold (and SATURATED_CLICHE does not apply): 

* S-Curve Position is **innovator_fringe** (< 2.5%).
* Percolation Momentum is **clique_stall** (0% to +10%) or
**trend_decay** (< 0%) while below 16% adoption.

**Delta cap: 0.35.** Pattern has not yet crossed the Granovetter /
Centola threshold out of its initial niche—high timing risk and
illiquidity if complex-contagion barriers keep the majority locked out.
Size conservatively as an early-stage option. 

#### CONFORMIST_CASCADE

Any of the following hold (and neither SATURATED_CLICHE nor
PRE_CHASM_FRINGE applies): 

* S-Curve Position is **early_majority_expansion** (16% to 50%) AND
Transmission Regime is **conformist_bandwagon**.
* S-Curve Position is **late_saturation** (> 50%) with
**organic_prestige** or **balanced_diffusion** (structural utility
plateau).

**Delta cap: 0.70.** The S-curve inflection is now consensus: upside
momentum remains active, but crowding and margin compression are
building. Trim size relative to the early crossover sweet spot. 

#### PRESTIGE_CROSSOVER

All of the following hold: 

* S-Curve Position is **early_adopter_chasm** (2.5% to 16%) OR
**early_majority_expansion** (16% to 50%).
* Transmission Regime is **organic_prestige** or **balanced_diffusion**
(prestige_to_mass_ratio >= 0.8 and n_wl_classes >= 3).
• Percolation Momentum is active_percolation (≥ +35%) or
steady_seeding (+10% to +35%).
Delta cap: 1.0. Asymmetric S-curve inflection: substantive creator
or engineering utility has cleared the chasm and is actively percolating
across clusters before mainstream conformist crowding peaks. The cap
equals the strategy cap; the skill never binds on PRESTIGE_CROSSOVER.

Ambiguous fallback

Any combination not covered above is classified CONFORMIST_CASCADE
with delta cap 0.70.

Secondary Filter / Asymmetric Gate — Late-Wave Exhaustion Hysteresis

Apply the persistence test after state classification and before the
cap.
A diffusion wave is over-extended if quarters_in_diffusion_wave >= 8
(eight or more consecutive calendar quarters of uninterrupted wave
expansion) AND the state is CONFORMIST_CASCADE or SATURATED_CLICHE.
Two full years of continuous mainstream bandwagon expansion indicates
that easy S-curve gains have already been harvested and late-cycle mean
reversion risk is elevated.
If the wave is over-extended, halve the state's delta cap:
• CONFORMIST_CASCADE cap of 0.70 becomes 0.35.
• SATURATED_CLICHE cap of 0.15 becomes 0.075.
The gate does not penalize PRESTIGE_CROSSOVER (where multi-quarter
steady seeding below the crowding threshold represents durable structural
adoption). The gate is one-way: it can only lower the cap.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read emergent percolation dict. From
snapshot.external_data["emergent_percolation"], load
cumulative_adoption_pct, prestige_to_mass_ratio,
cross_cluster_bridge_velocity, and quarters_in_diffusion_wave
(plus agop.n_wl_classes if present). If absent or empty, record
PRESTIGE_CROSSOVER, note the omission, and do not cite this
skill.
2. Classify S-curve position. Apply Reading 1 (innovator_fringe,
early_adopter_chasm, early_majority_expansion, or
late_saturation).
3. Classify transmission regime. Apply Reading 2
(organic_prestige, balanced_diffusion, conformist_bandwagon,
or hollow_mania).
4. Classify percolation momentum. Apply Reading 3
(active_percolation, steady_seeding, clique_stall, or
trend_decay).
5. Classify state. Evaluate in strict priority order
(SATURATED_CLICHE → PRE_CHASM_FRINGE → CONFORMIST_CASCADE →
PRESTIGE_CROSSOVER) and select the first matching state (fallback:
CONFORMIST_CASCADE).
6. Apply persistence test. If quarters_in_diffusion_wave >= 8 and
state is CONFORMIST_CASCADE or SATURATED_CLICHE, halve
delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"emergent-pattern-percolation" in skills_cited and state the
S-curve phase and cap reason in the rationale.

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
• rationale: free-form string naming the phase and cap reason.
Example:
"SATURATED_CLICHE state; 64% cumulative adoption with hollow_mania (prestige_to_mass=0.32, n_wl=2) over 9 quarters; delta capped at 0.075; emergent-pattern-percolation."
• skills_cited: list of skill names; include
"emergent-pattern-percolation" only when the cap bound.

Worked Examples


Case A — Early-adopter crossover with strong creator/engineering lead and active cross-cluster percolation, cap does not bind

Snapshot:
• cumulative_adoption_pct = 9.5
• prestige_to_mass_ratio = 2.6
• cross_cluster_bridge_velocity = 48.0
• quarters_in_diffusion_wave = 4
• agop.n_wl_classes = 5
Readings:
• S-Curve Position: 2.5% to 16% → early_adopter_chasm
• Transmission Regime: ≥ 2.0 and ≥ 4 → organic_prestige
• Percolation Momentum: ≥ +35% → active_percolation
State: PRESTIGE_CROSSOVER, delta cap 1.0. Persistence: does not apply.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "emergent-pattern-percolation".

Case B — Pre-chasm complex contagion stalled in a closed clique, cap binds

Snapshot:
• cumulative_adoption_pct = 1.4
• prestige_to_mass_ratio = 1.8
• cross_cluster_bridge_velocity = 3.0
• quarters_in_diffusion_wave = 2
• agop.n_wl_classes = 3
Readings:
• S-Curve Position: < 2.5% → innovator_fringe
• Transmission Regime: 0.8 to 2.0 and ≥ 3 → balanced_diffusion
• Percolation Momentum: 0% to +10% → clique_stall
State: PRE_CHASM_FRINGE, delta cap 0.35. Persistence: does not fire.
AGOP ranks LONG. LLM intended delta = 0.80. Cap 0.35 binds.
LLM returns delta = 0.35 and cites "emergent-pattern-percolation".

Case C — Over-extended late-cycle cliché with conformist bandwagon crowding, cap binds

Snapshot:
• cumulative_adoption_pct = 62.0
• prestige_to_mass_ratio = 0.38
• cross_cluster_bridge_velocity = 18.0
• quarters_in_diffusion_wave = 9
• agop.n_wl_classes = 2
Readings:
• S-Curve Position: > 50% → late_saturation
• Transmission Regime: < 0.5 and ≤ 2 → hollow_mania
• Percolation Momentum: +10% to +35% → steady_seeding
State: SATURATED_CLICHE, delta cap 0.15.
Persistence: quarters_in_diffusion_wave = 9 >= 8 → halve to 0.075.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.075 binds.
LLM returns delta = 0.075 and cites "emergent-pattern-percolation".

Free Data Sources

The fetcher populates snapshot.external_data["emergent_percolation"]
for any cultural, technological, or thematic pattern from the following
free, open public telemetry endpoints (no paid subscription required):
• Wikimedia Analytics Pageviews & EventStreams API:
https://wikimedia.org (free, no-key REST API measuring multi-language
page creation, editor concentration vs. mass reader traffic, and
cross-regional article percolation).
• GDELT Project 2.0 Global Knowledge Graph (GKG) API:
https://gdeltproject.org (free, no-key 15-minute global media and
theme co-occurrence feed used to track emerging motifs across 65+
languages and countries).
• GitHub REST API & PyPI / HuggingFace Public Stats:
https://github.com and https://pypistats.org (free open APIs
measuring developer commit/fork velocity vs. mainstream hype for
software, protocol, and AI adoption S-curves).
• OpenAlex Scientific & Patent Citation Graph:
https://openalex.org (free, no-key CC0 scholarly graph tracking
pre-commercial R&D velocity across energy, materials, and biotech).
• MusicBrainz & ListenBrainz Open Cultural Telemetry:
https://musicbrainz.org and https://listenbrainz.org (free CC0/open
APIs tracking underground genre tag emergence, artist-to-listener
dispersion, and scene crossover).
• ENTSO-E Transparency Platform, Fingrid & U.S. EIA Open Data:
https://entsoe.eu, https://fingrid.fi, and
https://eia.gov (free open grid registries tracking distributed
solar PV, battery storage BESS, and EV charging load penetration).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not extrapolate linear growth past 50% cumulative adoption when
prestige_to_mass_ratio drops below 0.5 (hollow_mania).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "emergent-pattern-percolation" when the cap did not bind.

Citation Mapping

• Diffusion of Innovations & Threshold Models: Everett M. Rogers,
Diffusion of Innovations (Free Press, 1962); Thomas C. Schelling,
Micromotives and Macrobehavior (W. W. Norton, 1978); Mark S.
Granovetter, "Threshold Models of Collective Behavior," American
Journal of Sociology 83(6), 1420–1443 (1978).
• Cultural Evolution & Prestige/Conformist Bias: Robert Boyd and
Peter J. Richerson, Culture and the Evolutionary Process (University
of Chicago Press, 1985); Joseph Henrich, The Secret of Our Success
(Princeton University Press, 2015); Dan Sperber, Explaining Culture
(Blackwell, 1996).
• Fashion Cycles & Subcultural Capital: Georg Simmel, "Fashion,"
International Quarterly 10, 130–155 (1904); Pierre Bourdieu,
Distinction (Harvard University Press, 1979); Dick Hebdige,
Subculture: The Meaning of Style (Methuen, 1979).
• Informational Cascades & Cumulative Advantage: Sushil Bikhchandani,
David Hirshleifer, and Ivo Welch, "A Theory of Fads, Fashion, Custom,
and Cultural Change as Informational Cascades," Journal of Political
Economy 100(5), 992–1026 (1992); Matthew J. Salganik, Peter Sheridan
Dodds, and Duncan J. Watts, Science 311(5762), 854–856 (2006).
• Complex Contagion & Bounded Authority: Damon Centola, How
Behavior Spreads (Princeton University Press, 2018); Stafford Beer,
Brain of the Firm (1972); Ramadge & Wonham (1987). Downward-only
damping within JANUS invariants I1–I9.