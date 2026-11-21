---
name: "keystone-species-yardstick"
description: "Classify the tick into one of four ecosystem states (THRIVING, STABLE, STRESSED, COLLAPSING) using the centrality of keystone species in ecological interaction networks, their IUCN population trends, their occurrence-record proliferation, and the habitat integrity of their ranges; cap delta as ecosystem stability degrades."
---

# Keystone Species Yardstick

You are reading the tick against the structural integrity of the
planet's major ecological zones. A keystone species is a node in an
ecological interaction network whose removal triggers a cascade far
larger than its own abundance would suggest. In graph-theoretic terms,
it is a high-betweenness or high-degree vertex in the network of
predation, pollination, seed dispersal, and competition edges. In
systems-theoretic terms, it is a **systemically important node** whose
failure propagates through the network's feedback loops before any
aggregate abundance statistic registers the loss. Paine's starfish
experiment established the concept; Jordán, Liu and Davis established
that centrality measures identify the keystone nodes; Scheffer,
Dunne and Williams established that their loss produces critical
transitions rather than smooth decline.

The ecosystem is the network. The keystone species is the node that
holds the network together. Their existence and proliferation is
bullish for the ecosystem's persistence; their decline is the earliest
observable signal of cascade collapse. Your job is to classify the
tick into one of four ecosystem states and cap your `delta`
accordingly. The state is a risk gate, not a forecast. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise `delta`
above the strategy cap, and you never invent an action outside
`allowed_actions`.

## The Readings

Compute four readings from
`snapshot.external_data["keystone_species"]` and its companion
`snapshot.external_data["ecosystem_zones"]` dict. Use the qualitative
tables below. Do not compute precise arithmetic.

### The monitored zones

Five zones are monitored. Each zone aggregates the keystone species
whose range overlaps it.

| Zone Key | Coverage | Weight |
|---|---|---|
| `terrestrial` | Terrestrial vertebrate and invertebrate keystone species across biomes | critical |
| `freshwater` | Freshwater vertebrate and invertebrate keystone species | major |
| `marine` | Marine keystone species (apex predators, reef builders, forage fish) | critical |
| `pollinator` | Pollinating insect keystone species | critical |
| `soil` | Soil-ecosystem engineer species | major |

The fetcher supplies a `keystone_species` dict keyed by zone. Each
entry supplies:

- `keystone_count`: the number of identified keystone species in the
  zone's interaction network.
- `centrality_share`: the fraction of keystone species in the top
  decile of betweenness centrality in the zone's GloBI-derived network.
- `population_trend_increasing`: fraction of keystone species whose
  latest IUCN assessment reports an increasing population trend.
- `population_trend_decreasing`: fraction reporting a decreasing
  trend.
- `occurrence_ratio`: the trailing-12-month occurrence records divided
  by the trailing-5-year annual mean, effort-normalised.
- `habitat_intactness`: the mean Biodiversity Intactness Index over
  the keystone species' ranges in the zone.

If `keystone_species` is absent or empty, treat all zones as
unmonitored, record state **STABLE**, note that no ecological data was
available, and do not cite this skill. If a specific zone key is
absent, evaluate the remaining zones; the skill only requires the
`terrestrial`, `marine`, and `pollinator` zones for the
critical-dominated states.

### Reading 1 — Keystone centrality share (graph-theory)

The centrality share is the fraction of keystone species that occupy
the top decile of betweenness centrality in the zone's interaction
network. A network whose keystone species are genuinely central has a
high share; a network where the labelled keystones are peripheral has
a low share, which is itself a signal that the network has been
restructured around different hubs.

| `centrality_share` | Centrality |
|---|---|
| ≥ 0.20 | **high** — the keystone nodes still occupy the network's structural core |
| 0.10 to 0.20 | **moderate** — some keystone nodes remain central |
| < 0.10 | **low** — the network has restructured away from its keystone nodes |

If `centrality_share` is missing, treat as **moderate** and rely on the
other readings.

### Reading 2 — Population trend (IUCN)

Read `population_trend_increasing` and `population_trend_decreasing`:

| `decreasing` | `increasing` | Population trend |
|---|---|---|
| < 0.30 | ≥ 0.50 | **thriving** — most keystone species are increasing |
| < 0.30 | < 0.50 | **stable** — neither trend dominates |
| 0.30 to 0.60 | any | **stressed** — a substantial minority is declining |
| > 0.60 | any | **collapsing** — the majority is declining |

If the two values are absent, treat as **stable** and rely on the
other readings.

### Reading 3 — Occurrence proliferation (GBIF, eBird, iNaturalist)

The occurrence ratio measures whether observers are recording the
keystone species more or less often than the five-year baseline,
normalised for observation effort. The ratio is the earliest
observable proliferation signal, before population assessments catch
up.

| `occurrence_ratio` | Occurrence |
|---|---|
| ≥ 1.15 | **proliferating** — records exceed baseline |
| 0.85 to 1.15 | **steady** — records at baseline |
| 0.50 to 0.85 | **contracting** — records below baseline |
| < 0.50 | **vanishing** — records far below baseline |

If `occurrence_ratio` is missing, treat as **steady** and rely on the
other readings. The ratio is not a population estimate; it is an
observation-effort-normalised proxy, and a sudden drop can reflect an
observer-network disruption rather than a species decline. The
`pollinator` and `terrestrial` zones have the densest observer
coverage; the `soil` zone has the sparsest and should be weighted
accordingly.

### Reading 4 — Habitat integrity (PREDICTS BII, Map of Life)

The Biodiversity Intactness Index measures the proportion of the
original species assemblage still present in an area. It is the
habitat substrate on which the interaction network runs.

| `habitat_intactness` | Habitat |
|---|---|
| ≥ 0.85 | **intact** — assemblage close to the original |
| 0.65 to 0.85 | **modified** — assemblage substantially changed but functional |
| 0.40 to 0.65 | **degraded** — assemblage substantially reduced |
| < 0.40 | **collapsed** — assemblage largely lost |

If `habitat_intactness` is missing, treat as **modified** and rely on
the other readings.

## Taxonomy / Decision Matrix

Combine the four readings into one of four ecosystem states. The
states are evaluated in the following priority order and the first
state whose conditions are fully satisfied is the classification:

1. **THRIVING** (checked first; the strictest adaptive fit)
2. **COLLAPSING** (checked next; the most severe degradation)
3. **STRESSED**
4. **STABLE** (checked last; the loosest adaptive fit)

### THRIVING

All of the following hold across the critical zones (`terrestrial`,
`marine`, `pollinator`):

- Centrality: **high**
- Population trend: **thriving**
- Occurrence: **proliferating**
- Habitat: **intact**

**Delta cap: 1.0.** The keystone nodes remain central, the populations
are increasing, the observers are recording them more often than
baseline, and the habitat substrate is intact. No ecological
constraint on sizing. The cap equals the strategy cap; the skill can
never bind on a THRIVING classification because no valid `delta`
exceeds 1.0.

### COLLAPSING

Any of the following hold in any critical zone:

- Population trend: **collapsing**
- Occurrence: **vanishing**
- Habitat: **collapsed**
- Centrality: **low** AND population trend: **stressed**

**Delta cap: 0.10.** The keystone node is failing or has already
failed. The cascade is in progress. Trade only if the AGOP ranking is
unambiguously directional and the asset is unconnected to physical
supply chains in the affected zone. In most cases, return FLAT.

### STRESSED

Any of the following hold in any critical zone (and neither THRIVING
nor COLLAPSING applies):

- Population trend: **stressed**
- Occurrence: **contracting**
- Habitat: **degraded**
- Centrality: **low** AND population trend: **stable**

**Delta cap: 0.25.** The keystone node is under pressure but the
network has not yet restructured. Reduce substantially.

### STABLE

All of the following hold:

- Every critical zone: centrality **moderate** or **high**
- Every critical zone: population trend **stable** or **thriving**
- Every critical zone: occurrence **steady** or **proliferating**
- Every critical zone: habitat **intact** or **modified**

**Delta cap: 0.75.** The keystone nodes are intact but not expanding,
the populations are holding, the observations are at baseline, and the
habitat is functional but not pristine. Reduce size relative to
THRIVING.

### Ambiguous fallback

Any combination not covered by the four states above is classified
**STRESSED** with delta cap 0.25. The skill errs toward caution
because the cost of missing a keystone collapse exceeds the cost of an
unnecessary reduction, and because the graph-theoretic signal is
precisely the kind of signal that aggregate abundance statistics
register too late.

## Secondary Filter / Asymmetric Gate — Cascade Gate

Apply the cascade gate after the state classification and before the
cap. The gate exists because a keystone collapse in one zone
propagates to network-adjacent zones before their own readings
register it. Scheffer's critical-transition theory and Dunne and
Williams' cascading-extinction models both predict that the failure is
**non-linear**: the first zone to collapse is the leading indicator,
and the adjacent zones follow.

Count the number of zones whose readings satisfy the **COLLAPSING**
conditions. Call this `N_collapsing`. Read the network-adjacency matrix
from `snapshot.external_data["ecosystem_zones"]`, which supplies
`adjacent_to` for each zone (the zones that share mobile species or
habitat corridors with it).

- If `N_collapsing >= 2`: **force FLAT** (`delta = 0.0`, `action =
  "FLAT"`). Two or more zones collapsing simultaneously is a systemic
  cascade, not a local failure. The skill binds unconditionally and
  must appear in `skills_cited`.
- If `N_collapsing == 1` AND at least one `adjacent_to` zone is
  **STRESSED**: halve the cap. COLLAPSING cap of 0.10 becomes **0.05**.
  STRESSED cap of 0.25 becomes **0.125**.
- Otherwise: do not change the cap.

The gate is one-way. It can only lower the cap or force FLAT. It
cannot raise the cap. It cannot change the state classification.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read the zone dicts.** From
   `snapshot.external_data["keystone_species"]`, load each monitored
   zone's `centrality_share`, `population_trend_increasing`,
   `population_trend_decreasing`, `occurrence_ratio`, and
   `habitat_intactness`. From
   `snapshot.external_data["ecosystem_zones"]`, load each zone's
   `adjacent_to`. If `keystone_species` is absent or empty, record
   state **STABLE**, note the absence, and skip to step 8 with a note
   that no cap was computed.

2. **Classify centrality.** For each zone, classify `centrality_share`
   using Reading 1 and record `high`, `moderate`, or `low`.

3. **Classify population trend.** For each zone, classify
   `population_trend_decreasing` and `population_trend_increasing`
   using Reading 2 and record `thriving`, `stable`, `stressed`, or
   `collapsing`.

4. **Classify occurrence.** For each zone, classify `occurrence_ratio`
   using Reading 3 and record `proliferating`, `steady`,
   `contracting`, or `vanishing`.

5. **Classify habitat.** For each zone, classify `habitat_intactness`
   using Reading 4 and record `intact`, `modified`, `degraded`, or
   `collapsed`.

6. **Classify state.** Evaluate in the priority order THRIVING,
   COLLAPSING, STRESSED, STABLE and take the first state whose
   conditions are fully satisfied. If no state matches, record
   STRESSED as the ambiguous fallback.

7. **Apply cascade gate.** Count `N_collapsing`. If `N_collapsing >=
   2`, force FLAT and record `delta = 0.0`, `action = "FLAT"`. Else if
   `N_collapsing == 1` and at least one adjacent zone is STRESSED,
   halve the cap. Else leave the cap unchanged.

8. **Cap delta.** Let `delta_cap` be the value from steps 6–7. If the
   intended `delta` exceeds `delta_cap`, reduce it to `delta_cap`. If
   the cascade gate forced FLAT, `delta = 0.0` and `action = "FLAT"`
   regardless of the AGOP ranking. Record the final `delta` and
   `action`.

9. **Cite.** If the cap bound (i.e., the intended delta was above the
   cap) or the cascade gate forced FLAT, cite
   `"keystone-species-yardstick"` in `skills_cited` and state the
   ecosystem state in the rationale. If the cap did not bind, do not
   cite the skill.

## The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:

```json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
```

The fields:

- `action`: a string. One of `"LONG"`, `"FLAT"`, `"SHORT"`. Must
  appear in the AGOP ranking or be `"FLAT"`. Invariant I1 enforces
  this independently of anything you produce. If the cascade gate
  forces FLAT, `action` must be `"FLAT"`.

- `delta`: a floating-point number in `[0.0, 1.0]`. The final
  position size is `delta` multiplied by the risk engine's upper
  bound. The ecological cap restricts `delta` further; it does not
  replace the risk bound. If the cascade gate forces FLAT, `delta`
  must be `0.0`.

- `confidence`: a floating-point number in `[0.0, 1.0]`. Reflects the
  confidence in the rationale, not the trade. The strategy's
  confidence floor (0.40 for OPPORTUNITY, 0.45 for AGGRESSIVE, 0.65
  for CONSERVATIVE) rejects responses below the threshold.

- `rationale`: a free-form string. Names the ecosystem state and the
  reason for any cap. Example: "COLLAPSING state; pollinator
  population_trend_decreasing 0.68 with occurrence_ratio 0.42;
  cascade gate halved to 0.05 because terrestrial zone adjacent and
  STRESSED; keystone-species-yardstick."

- `skills_cited`: a list of skill names. Include
  `"keystone-species-yardstick"` only if the cap bound or the cascade
  gate forced FLAT. Include the skills that actually drove the choice
  otherwise.

## Worked Examples

### Case A — Thriving state, cap does not bind

Fetcher supplies:

- `keystone_species["terrestrial"]`: `centrality_share` = 0.24,
  `population_trend_increasing` = 0.55, `population_trend_decreasing`
  = 0.12, `occurrence_ratio` = 1.22, `habitat_intactness` = 0.88.
- `keystone_species["marine"]`: `centrality_share` = 0.22,
  `population_trend_increasing` = 0.58, `population_trend_decreasing`
  = 0.10, `occurrence_ratio` = 1.18, `habitat_intactness` = 0.86.
- `keystone_species["pollinator"]`: `centrality_share` = 0.26,
  `population_trend_increasing` = 0.61, `population_trend_decreasing`
  = 0.11, `occurrence_ratio` = 1.30, `habitat_intactness` = 0.87.
- `ecosystem_zones`: every zone `adjacent_to` the others.

Readings:

- Centrality: 0.24, 0.22, 0.26 → **high** in all three critical zones.
- Population trend: increasing 0.55–0.61, decreasing 0.10–0.12 →
  **thriving** in all three.
- Occurrence: 1.18–1.30 → **proliferating** in all three.
- Habitat: 0.86–0.88 → **intact** in all three.

State (priority THRIVING → COLLAPSING → STRESSED → STABLE):

- THRIVING? Centrality high ✓, population thriving ✓, occurrence
  proliferating ✓, habitat intact ✓. **THRIVING** matches.

Delta cap 1.0.

Cascade gate: `N_collapsing` = 0 → does not fire.

AGOP ranks LONG. LLM intended delta 0.90. Cap 1.0 does not bind. LLM
returns delta 0.90, does not cite `keystone-species-yardstick`, and
cites whichever skills drove the directional choice.

### Case B — Collapsing state, cascade gate binds

Fetcher supplies:

- `keystone_species["terrestrial"]`: `centrality_share` = 0.08,
  `population_trend_increasing` = 0.10, `population_trend_decreasing`
  = 0.72, `occurrence_ratio` = 0.38, `habitat_intactness` = 0.36.
- `keystone_species["marine"]`: `centrality_share` = 0.21,
  `population_trend_increasing` = 0.30, `population_trend_decreasing`
  = 0.35, `occurrence_ratio` = 0.92, `habitat_intactness` = 0.72.
- `keystone_species["pollinator"]`: `centrality_share` = 0.12,
  `population_trend_increasing` = 0.22, `population_trend_decreasing`
  = 0.48, `occurrence_ratio` = 0.71, `habitat_intactness` = 0.58.
- `ecosystem_zones`: `terrestrial` `adjacent_to` `["pollinator",
  "freshwater"]`; `pollinator` `adjacent_to` `["terrestrial"]`.

Readings:

- Centrality: terrestrial 0.08 → **low**; marine 0.21 → **high**;
  pollinator 0.12 → **moderate**.
- Population trend: terrestrial decreasing 0.72, increasing 0.10 →
  **collapsing**; marine decreasing 0.35 → **stressed**; pollinator
  decreasing 0.48 → **stressed**.
- Occurrence: terrestrial 0.38 → **vanishing**; marine 0.92 →
  **steady**; pollinator 0.71 → **contracting**.
- Habitat: terrestrial 0.36 → **collapsed**; marine 0.72 →
  **modified**; pollinator 0.58 → **degraded**.

State (priority THRIVING → COLLAPSING → STRESSED → STABLE):

- THRIVING? No — terrestrial fails every condition. No.
- COLLAPSING? Terrestrial population collapsing ✓ (also occurrence
  vanishing ✓, habitat collapsed ✓). **COLLAPSING** matches.

Delta cap 0.10.

Cascade gate: `N_collapsing` = 1 (terrestrial). Terrestrial is
adjacent to `pollinator`, which is **STRESSED** (population stressed,
occurrence contracting, habitat degraded). Gate fires → halve to
**0.05**.

AGOP ranks LONG. LLM intended delta 0.80. Cap 0.05 binds. LLM returns
delta 0.05, cites `keystone-species-yardstick`, and states in the
rationale: "COLLAPSING state; terrestrial centrality 0.08 with
population_trend_decreasing 0.72, occurrence_ratio 0.38, and
habitat_intactness 0.36; cascade gate halved to 0.05 because
pollinator adjacent and STRESSED; keystone-species-yardstick."

## Free data sources

The skill reads normalised values from `snapshot.external_data`. The
operator's fetcher populates the `keystone_species` and
`ecosystem_zones` dicts from the following free sources. All are
publicly available; none requires a paid subscription. Two carry
non-commercial clauses that the operator is responsible for
respecting.

| Source | Supplies | Endpoint | Access |
|---|---|---|---|
| IUCN Red List API v4 | Population trend (increasing, stable, decreasing, unknown) per keystone species | `https://api.iucnredlist.org/api/v4` | Free token at `https://api.iucnredlist.org/users/sign_up`; conservation, education, and research use only; commercial use prohibited |
| GBIF API | Occurrence records per species and zone | `https://api.gbif.org/v1/` | Fully free, no key; open data licences |
| GloBI (Global Biotic Interactions) | Species interaction edges for the centrality network | `https://api.globalbioticinteractions.org/` | Fully free REST API; open data |
| Living Planet Index (ZSL) | Population time series for vertebrate keystone species | `https://www.livingplanetindex.org/latest_results` and `http://stats.livingplanetindex.org/` | Free download; non-commercial use per ZSL Data Use Policy |
| Map of Life | Expert-validated range maps for 450,000+ species | `https://mol.org` | Free for non-commercial use by researchers, governments, NGOs, and educators |
| PREDICTS / Biodiversity Intactness Index | Site-level biodiversity intactness | `https://data.nhm.ac.uk/` (PREDICTS release November 2022) and the BII GitHub release | CC-NC licence; free for non-commercial use |
| eBMS / EU Grassland Butterfly Index | Pollinator abundance and diversity trends | `https://butterfly-monitoring.net/ebms` | Raw data open and freely available for Finland; upon request for other member states |
| Large carnivore distribution maps for Europe | Apex predator range and trend | `https://research.wur.nl/` (2017–2022/23 release) | Free shapefiles |
| NatureServe | Keystone species raster and feature layers | `https://geodata.natureserve.org/` | Free for non-commercial use |

The fetcher constructs the centrality network from GloBI edges for the
keystone species list in each zone, computes betweenness centrality,
and reports the fraction of keystone species in the top decile as
`centrality_share`. It reads `population_trend_*` from the IUCN
assessments, `occurrence_ratio` from GBIF (or eBird and iNaturalist
via the `spocc` interface for the terrestrial and pollinator zones),
and `habitat_intactness` from PREDICTS BII. The Living Planet Index
supplies the vertebrate population time series used to cross-check the
IUCN trend reading. Map of Life supplies the range maps that define
which species belong to which zone. eBMS supplies the pollinator
abundance trends for the pollinator zone. The large carnivore maps
supply the apex-predator range data for the terrestrial and marine
zones. NatureServe supplies the keystone species raster layers for the
terrestrial zone.

## Do Not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a
  replacement for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it.

- Do not treat THRIVING as a reason to increase size beyond the
  strategy cap. The strategy cap is the binding constraint. THRIVING
  means the AGOP-selected action is worth taking at the bound the
  strategy already permits.

- Do not compute precise arithmetic on the shares or ratios. The
  thresholds are qualitative. A 7B model cannot reliably compute
  betweenness centrality or divide small floats; use the comparison
  tables.

- Do not re-classify on the same tick. The ecosystem state is a
  deterministic function of the readings. If the first classification
  was COLLAPSING, it stays COLLAPSING. Do not push it to STRESSED by
  preferring one zone's reading over another.

- Do not cite this skill when the cap did not bind. If the intended
  delta was already at or below the cap, this skill did not change
  the decision, and it should not appear in `skills_cited`. Cite the
  skills that actually drove the choice.

- Do not attempt to fetch IUCN, GBIF, GloBI, LPI, Map of Life,
  PREDICTS, eBMS, WUR, or NatureServe data yourself. You are the LLM;
  you read what is in `snapshot.external_data`. The fetcher is the
  operator's responsibility.

- Do not treat the cascade gate as an alternative to the state
  classification. The two are applied sequentially. The state is
  classified first; the cascade gate then adjusts the cap. Both can
  fire on the same tick.

- Do not treat the ambiguous fallback as a distinct state. It is
  STRESSED for all downstream purposes, including the cascade gate
  and the cap.

- Do not treat the occurrence ratio as a population estimate. It is an
  observation-effort-normalised proxy. A sudden drop can reflect an
  observer-network disruption. Weight it accordingly, and never let it
  alone override a habitat or population reading in the opposite
  direction unless the state taxonomy explicitly permits it.

## Citation Mapping

- **Reading 1 — centrality share (graph-theory)**: Robert T. Paine,
  "A Note on Trophic Complexity and Community Stability", *The
  American Naturalist* 103 (1969) — the keystone species concept.
  Jordán, Liu, and Davis, "Centrality measures and the importance of
  generalist species in pollination networks", *Ecological
  Complexity* 7 (2010) — the identification of keystone species by
  degree and betweenness centrality. Linton C. Freeman, "A Set of
  Measures of Centrality Based on Betweenness", *Sociometry* 40
  (1977) — the betweenness definition. The 0.20 and 0.10 thresholds
  are calibrated to the betweenness distributions reported in the
  Jordán et al. pollination networks.

- **Reading 2 — population trend (IUCN)**: IUCN, *Guidelines for
  Using the IUCN Red List Categories and Criteria* (Standards and
  Petitions Committee, 2024) — the population-trend criterion. Stuart
  Butchart et al., "Improvements to the Red List Index", *PLoS ONE*
  2 (2007) — the aggregation of species trends into an index. The
  0.30 and 0.60 thresholds separate a substantial minority from a
  majority decline, matching the IUCN's own "significant decline"
  language.

- **Reading 3 — occurrence proliferation (GBIF, eBird, iNaturalist)**:
  GBIF Secretariat, *GBIF API* (2026); eBird, *eBird API* (2026);
  iNaturalist, *iNaturalist API* (2026). The effort-normalisation
  follows the `spocc` interface (Owens et al., 2026) and the
  occurrence-trend methodology in the Living Planet Index's
  supplementary materials. The 1.15 and 0.50 thresholds are
  calibrated to the observation-effort band reported in the eBMS
  pollinator dataset.

- **Reading 4 — habitat integrity (PREDICTS, Map of Life)**: Tim
  Newbold et al., "Has land use pushed terrestrial biodiversity
  beyond the planetary boundary?", *Science* 353 (2016) — the
  Biodiversity Intactness Index. Walter Jetz et al., "The Map of
  Life: integrating global biodiversity data", *Trends in Ecology &
  Evolution* 27 (2012). The 0.85 and 0.40 thresholds correspond to
  the planetary-boundary "safe" and "high-risk" levels.

- **State taxonomy**: Donella H. Meadows, *Thinking in Systems: A
  Primer* (2008) — reinforcing and balancing loops. Marten Scheffer
  et al., "Early-warning signals for critical transitions", *Nature*
  461 (2009) — the non-linear regime shift. The priority order
  THRIVING, COLLAPSING, STRESSED, STABLE reflects the fact that
  degradation overrides the adaptive classification when its
  conditions are met, while THRIVING is checked before STABLE
  because THRIVING is the strictest fit for the adaptive state.

- **Cascade gate**: Marten Scheffer et al., "Catastrophic shifts in
  ecosystems", *Nature* 413 (2001) — the critical-transition
  framework. Jennifer A. Dunne and Richard J. Williams,
  "Cascading extinctions and community collapse in model food
  webs", *Philosophical Transactions of the Royal Society B* 364
  (2009) — the cascading-extinction model. The network-adjacency
  reading follows the graph-theoretic propagation logic in the same
  literature.

- **Optional corroboration**: Zoological Society of London, *Living
  Planet Index* (2024 release) — vertebrate population time series;
  European Butterfly Monitoring Scheme, *EU Grassland Butterfly
  Index* (2026) — a 47 % decline since 1991 in the EU; Large
  Carnivore Distribution Maps for Europe (WUR, 2017–2022/23);
  NatureServe keystone species layers (2026). These are
  corroborative only; the readings are computed from the
  `keystone_species` dict.

- **Ambiguous fallback (STRESSED, cap 0.25)**: Scheffer et al.
  (2009). The skill errs toward caution because the cost of missing
  a keystone collapse exceeds the cost of an unnecessary reduction,
  and because the graph-theoretic signal is precisely the kind of
  signal that aggregate abundance statistics register too late.

- **Bounded algedonic authority**: Stafford Beer, *Brain of the
  Firm* (1972); Ramadge and Wonham, *Supervisory Control of a Class
  of Discrete-Event Processes* (1987). The skill operates strictly as
  a downward-only algedonic damper within JANUS invariants I1–I9. It
  can flag an ecosystem state and cap delta; it cannot override the
  homeostatic risk bound or invent an action outside the AGOP
  ranking.