#### name: "urban-arterial-gridlock"
description: "Detect urban and inter-city arterial traffic gridlock using dimensionless velocity-drop ratios and graph detour redundancy abstracted across any city or corridor via free OpenStreetMap topology and open municipal/highway loop-detector feeds (Fintraffic Digitraffic Road, TfL, NYC DOT, Eurostat); cap delta or force FLAT as arterial throughput seizes."

#### Urban Arterial Gridlock & Detour Topology

You are reading the tick against the **physical land-transit throughput
and arterial network redundancy** of the target metropolitan hub,
industrial logistics corridor, or retail-catchment city. In Bruce
Greenshields's fundamental traffic-flow theory (1935), William Vickrey's
bottleneck congestion model (1969), and Dietrich Braess's network
paradox (1968), urban road networks exhibit a sharp **nonlinear phase
transition (jamming)** once vehicle density crosses critical capacity:
travel velocity collapses asymptotically toward zero, freight delivery
windows miss just-in-time connections, and labor productivity bleeds
out in stationary queues. 

Tracking every street in every city directly creates an intractable
data explosion. To solve this cleanly without paid commercial GPS
firehoses, this skill **abstracts away city and street names into two
dimensionless topological invariants**: 

1. **Normalized Passage Velocity Ratio (velocity_ratio)** — observed
vehicle passage speed along the target city's primary freight/commuter
arteries divided by free-flow baseline speed (
𝑣obs

/𝑣free_flow

∈

[

0

,

1

]
⁠).
2. **Arterial Detour Redundancy (detour_redundancy_index)** — graph
path-diversity and spare parallel-corridor capacity derived from open
OpenStreetMap (Overpass / OSRM) road topology (measuring whether
traffic can reroute around a blocked bridge, tunnel, or ring road, or
whether the city is bottlenecked by single-point choke structures).

Your job is to classify the tick into one of four gridlock states and
cap your delta accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["urban_gridlock"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes open municipal inductive-loop detectors, highway
traffic-management cameras/sensors, and OpenStreetMap graph-redundancy
metrics into snapshot.external_data["urban_gridlock"]. Each abstracted
city or logistics hub entry supplies: 

* velocity_ratio: dimensionless ratio 
𝑣obs

/𝑣free_flow
⁠
(0.0 to 1.0) comparing current rolling 24-hour / peak-window
passage speed across primary arteries to the 90-day uncongested
baseline (>= 0.85 = free-flow; < 0.35 = severe kinematic jamming).
* detour_redundancy_index: normalized 0.0 to 1.0 graph-topology
score computed from OpenStreetMap road networks (ratio of independent
alternate arterial paths within +25% distance penalty; > 0.65 =
dense grid/ring redundancy; < 0.25 = island, fjord, bridge, or
single-corridor choke topology with no viable detour).
* incident_blockage_pct: percentage (0 to 100) of primary
arterial lane-kilometers closed or restricted by roadworks, weather
snow/ice accumulation, protest blockades, or structural closures.
* consecutive_gridlock_days: consecutive calendar days in which
velocity_ratio < 0.50 across the abstracted city hub.

If snapshot.external_data["urban_gridlock"] is absent or empty, treat
the hub as **unmonitored**, record state **FREE_FLOW**, note that no
urban gridlock data was available, and do not cite this skill. 

#### Reading 1 — Normalized passage velocity drop (velocity_ratio)

Evaluate how severely vehicle throughput speed has degraded relative to
uncongested baseline: 

velocity_ratioKinematic Flow Regime
**≥ 0.80**
**free_flow** — uncongested baseline transit velocity
**0.60 to 0.80**
**synchronized_drag** — peak-hour slowing; predictable schedule buffer
**0.35 to 0.60**
**congested_breakdown** — stop-and-go instability; freight SLA slippage
**< 0.35**
**kinematic_jam** — near-stationary gridlock; physical transit stall

If velocity_ratio is missing, treat as **synchronized_drag**. 

#### Reading 2 — Graph detour redundancy & lane blockage (detour_redundancy_index & incident_blockage_pct)

Evaluate whether the abstracted road graph can absorb disruption via
alternate routes or is trapped in a topological choke: 

detour_redundancy_indexincident_blockage_pctNetwork Bypass Capacity
**≥ 0.60**
< 10%**redundant_mesh** — multiple parallel arterials absorb local shocks
**0.30 to 0.60**
< 20%**constrained_bypass** — limited ring/bypass routes; high spillover
**< 0.30**
any**choke_topology** — bridge/tunnel/peninsula bottleneck; zero viable detour
**any**
≥ 20%**choke_topology** — widespread lane closures severing bypass paths

If either metric falls in a worse row, take the **worse** (more
restrictive) classification. 

#### Reading 3 — Gridlock persistence (consecutive_gridlock_days)

Evaluate whether congestion is a single-day transient event or a
multi-day structural paralysis: 

consecutive_gridlock_daysPersistence Tier
**0 to 1**
**transient** — single-shift weather or accident spike
**2 to 4**
**multi_day** — compounding freight backlog and shift disruption
**≥ 5**
**chronic_paralysis** — entrenched urban logistics seizure

If consecutive_gridlock_days is missing, treat as **transient** (0). 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
urban-gridlock states. Evaluate in strict priority order and select the
first state whose conditions are fully satisfied: 

1. **ARTERIAL_SEIZURE** (most severe — unconditional FLAT)
2. **GRIDLOCK_DRAG**
3. **CORRIDOR_FRICTION**
4. **FREE_FLOW** (strictest adaptive fit)

#### ARTERIAL_SEIZURE

Any of the following hold: 

* Kinematic Flow Regime is **kinematic_jam** (velocity_ratio < 0.35)
AND Network Bypass Capacity is **choke_topology**.
* Kinematic Flow Regime is **kinematic_jam** (velocity_ratio < 0.35)
AND Persistence Tier is **chronic_paralysis** (>= 5 days).
* Network Bypass Capacity is **choke_topology** with
incident_blockage_pct >= 35% AND Kinematic Flow Regime is
**congested_breakdown** or **kinematic_jam**.

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. Urban road throughput has seized without viable
detour routes: local logistics, retail footfall, and just-in-time
industrial deliveries are physically stalled. The skill binds
unconditionally and must appear in skills_cited. 

#### GRIDLOCK_DRAG

Any of the following hold (and ARTERIAL_SEIZURE does not apply): 

* Kinematic Flow Regime is **kinematic_jam** (velocity_ratio < 0.35).
* Kinematic Flow Regime is **congested_breakdown** (0.35 to 0.60)
AND Network Bypass Capacity is **choke_topology**.
* Kinematic Flow Regime is **congested_breakdown** AND Persistence Tier
is **multi_day** or **chronic_paralysis** (>= 2 days).

**Delta cap: 0.25.** Severe congestion and scarce detour routes are
eroding delivery margins and commuter productivity. Reduce position size
substantially on locally exposed retail, transport, and industrial
tickers. 

#### CORRIDOR_FRICTION

Any of the following hold (and neither ARTERIAL_SEIZURE nor
GRIDLOCK_DRAG applies): 

* Kinematic Flow Regime is **congested_breakdown** (0.35 to 0.60)
with **redundant_mesh** or **constrained_bypass**.
* Kinematic Flow Regime is **synchronized_drag** (0.60 to 0.80) AND
Network Bypass Capacity is **choke_topology**.

**Delta cap: 0.75.** Moderate arterial slowing or tight bypass capacity
creates manageable scheduling friction. Reduce size relative to
FREE_FLOW. 

#### FREE_FLOW

All of the following hold: 

* Kinematic Flow Regime is **free_flow** (velocity_ratio ≥ 0.80).
* Network Bypass Capacity is **redundant_mesh** or **constrained_bypass**.
* Persistence Tier is **transient** (0 to 1 day).

**Delta cap: 1.0.** Normal uncongested arterial velocity and intact
detour capacity. The cap equals the strategy cap; the skill never binds
on FREE_FLOW. 

#### Ambiguous fallback

Any combination not covered above is classified **GRIDLOCK_DRAG** with
delta cap 0.25. 

#### Secondary Filter / Asymmetric Gate — Chronic Seizure Hysteresis

Apply the persistence test after state classification and before the
cap. 

An urban gridlock event is **structurally entrenched** if
consecutive_gridlock_days >= 5 (chronic_paralysis — five or more
consecutive days with velocity_ratio < 0.50). Five consecutive days of
sub-50% passage velocity proves that municipal traffic control, snow/ice
clearance, or infrastructure repair cannot clear the queue within a
normal workweek. 

If the gridlock is **structurally entrenched**, halve the state's delta
cap: 

* CORRIDOR_FRICTION cap of 0.75 becomes **0.375**.
* GRIDLOCK_DRAG cap of 0.25 becomes **0.125**.
* ARTERIAL_SEIZURE cap remains **0.0** (FLAT).

The gate is one-way. It cannot raise the cap; it can only lower it. 

#### The Procedure

Execute this procedure on every tick. Do not skip steps. 

1. **Read urban gridlock dict.** From
snapshot.external_data["urban_gridlock"], load velocity_ratio,
detour_redundancy_index, incident_blockage_pct, and
consecutive_gridlock_days. If absent or empty, record
**FREE_FLOW**, note the omission, and do not cite this skill.
2. **Classify kinematic flow regime.** Apply Reading 1 (free_flow,
synchronized_drag, congested_breakdown, or kinematic_jam).
3. Classify network bypass capacity. Apply Reading 2 (redundant_mesh,
constrained_bypass, or choke_topology).
4. Classify persistence tier. Apply Reading 3 (transient,
multi_day, or chronic_paralysis).
5. Classify state. Evaluate in strict priority order
(ARTERIAL_SEIZURE → GRIDLOCK_DRAG → CORRIDOR_FRICTION →
FREE_FLOW) and select the first matching state (fallback:
GRIDLOCK_DRAG).
6. Apply persistence test. If consecutive_gridlock_days >= 5,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
state is ARTERIAL_SEIZURE, set delta = 0.0 and action = "FLAT"
regardless of AGOP. Otherwise, if intended delta exceeds
delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
state is ARTERIAL_SEIZURE, cite "urban-arterial-gridlock" in
skills_cited and state the abstracted velocity/detour finding in
the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If ARTERIAL_SEIZURE,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and abstracted metrics.
Example:
"GRIDLOCK_DRAG state; velocity_ratio=0.42 (congested_breakdown) with choke_topology (detour=0.22) for 6 days; delta capped at 0.125; urban-arterial-gridlock."
• skills_cited: list of skill names; include
"urban-arterial-gridlock" only when the cap bound or the state is
ARTERIAL_SEIZURE.

Worked Examples


Case A — Normal arterial speed with dense ring/grid detour redundancy, cap does not bind

Snapshot:
• velocity_ratio = 0.88
• detour_redundancy_index = 0.72
• incident_blockage_pct = 3.0
• consecutive_gridlock_days = 0
Readings:
• Kinematic Flow Regime: ≥ 0.80 → free_flow
• Network Bypass Capacity: ≥ 0.60 and < 10% → redundant_mesh
• Persistence Tier: 0 → transient
State: FREE_FLOW, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "urban-arterial-gridlock".

Case B — Severe velocity collapse on a choke-topology peninsula/bridge city, unconditional FLAT

Snapshot:
• velocity_ratio = 0.28
• detour_redundancy_index = 0.19
• incident_blockage_pct = 25.0
• consecutive_gridlock_days = 3
Readings:
• Kinematic Flow Regime: < 0.35 → kinematic_jam
• Network Bypass Capacity: < 0.30 → choke_topology
• Persistence Tier: 3 → multi_day
State: ARTERIAL_SEIZURE, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "urban-arterial-gridlock".

#### Free Data Sources

The fetcher abstracts any city and artery into dimensionless ratios
(velocity_ratio and detour_redundancy_index) from the following
free, open public traffic, transit-speed, and map-topology sources: 

* **OpenStreetMap (Overpass API & OSRM Public Routing Graph):**
https://overpass-api.de (free, no-key ODbL road network graph used
globally to compute detour_redundancy_index via betweenness
centrality and parallel-path ratios for any city).
* **Mobility Database / OpenMobilityData GTFS-Realtime Feeds:**
https://mobilitydatabase.org (free open catalog of live GTFS-RT
vehicle-position feeds across 1,000+ cities worldwide; surface-bus
corridor speeds provide a direct, zero-cost kinematic proxy for
arterial velocity_ratio where inductive loops are absent).
* **Fintraffic Digitraffic Road API (Finland National & Urban TMS Loops):**
https://digitraffic.fi (free, no-key real-time JSON/REST API
exposing induction-loop vehicle speeds, congestion alerts, and road
closures across Helsinki, Tampere, Turku, and national arteries).
* **Transport for London (TfL) Unified API & UK National Highways:**
https://tfl.gov.uk (free open corridor travel times, road
disruptions, and bus/arterial speed feeds).
* **NYC DOT Open Traffic Speeds & U.S. FHWA NPMRDS / State 511 Feeds:**
https://cityofnewyork.us (free Socrata open-data endpoints for
real-time arterial segment velocities and bridge/tunnel bottlenecks).
* **Eurostat Urban Transport & TomTom Open Traffic Index Summaries:**
https://europa.eu (free municipal commute-time and urban congestion
baselines).
* **Singapore LTA DataMall (Traffic Speed Bands & Incidents):**
https://datamall.lta.gov.sg (free API-key JSON endpoint exposing
real-time expressway and arterial speed bands across Singapore).
* **Taiwan TDX (Transport Data eXchange) & Japan JARTIC / ODPT:**
https://tdx.transportdata.tw and https://www.odpt.org (free open
government APIs supplying live highway/urban vehicle-detector speeds
and congestion status across Taipei, Kaohsiung, and Tokyo).
* **India Open Government Data (data.gov.in) & Delhi/Bengaluru Open Transit:**
https://data.gov.in and https://otd.delhi.gov.in (free public
transit and arterial corridor telemetry for Indian metropolitan hubs).
* **DigitalTransport4Africa (DT4A) & South Africa Open Mobility:**
https://digitaltransport4africa.org and https://www.transport.gov.za
(free open GTFS/GTFS-RT and municipal corridor datasets for Nairobi,
Addis Ababa, Accra, Lagos, Cairo, Johannesburg, and Cape Town).
* **World Bank Open Data & African Development Bank (AfDB) Transport Portal:**
https://data.worldbank.org (free corridor freight transit-time and
urban infrastructure bottleneck indicators).
* **São Paulo CET / SPTrans Olho Vivo & Rio de Janeiro Data.Rio:**
https://dados.prefeitura.sp.gov.br and https://www.data.rio (free
open municipal traffic-jam length, arterial corridor speed, and
real-time bus-corridor GPS feeds).
* **Buenos Aires BA Data (Transporte) & Bogotá Datos Abiertos (Movilidad):**
https://data.buenosaires.gob.ar and https://datosabiertos.bogota.gov.co
(free open-data portals exposing real-time arterial speeds, road
closures, and SITP/TransMilenio corridor velocities).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not hard-code city-specific street exceptions; always evaluate via
the abstracted velocity_ratio and detour_redundancy_index.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "urban-arterial-gridlock" when the cap did not bind and
the state is not ARTERIAL_SEIZURE.

Citation Mapping

For full academic references underlying traffic flow theory, bottleneck queueing, and network routing, consult the foundational works by Bruce D. Greenshields (1935), William S. Vickrey (1969), and Dietrich Braess (1968), alongside cybernetic authority principles by Stafford Beer (1972) and Ramadge & Wonham (1987).