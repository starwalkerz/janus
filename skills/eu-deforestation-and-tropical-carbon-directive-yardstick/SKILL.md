#### name: "eu-deforestation-and-tropical-carbon-directive-yardstick"
description: "Geospatial regulatory compliance yardstick auditing arbitrary WGS84 tropical and subtropical cultivation coordinates against EU Deforestation Regulation (EUDR, Regulation (EU) 2023/1115 — post-31 December 2020 cutoff) and EU Renewable Energy / Carbon Directive (RED III, Directive (EU) 2023/2413) land-use requirements over free Copernicus Sentinel-1/2 and JRC Global Forest Cover 2020 datasets."

#### EU Carbon & Deforestation Directive Tropical Cultivation Yardstick

You are reading the tick against **EU regulatory compliance for tropical
and subtropical agricultural cultivation (EUDR Regulation (EU)
2023/1115 and RED III Directive (EU) 2023/2413)**—verified directly on
any supplied WGS84 coordinate (latitude, longitude) using free
**ESA Copernicus Sentinel-1/2** change detection and **EU JRC Global
Forest Cover 2020 (GFC 2020)** baseline maps. 

Under EU law, tropical commodities (cacao, coffee, palm oil, soy, rubber, cattle, timber) and bio-carbon feedstocks cannot legally enter
the EU market—or claim EU carbon/sustainability credits—unless the
exact cultivation polygon passes three strict geospatial gates: 

1. **Post-31 December 2020 Deforestation-Free Cutoff (EUDR Art. 3(a)):**
Zero conversion of natural forest to agricultural use after
**31 December 2020**, verified by comparing Copernicus Sentinel-2
(2018–2020 dry-season baseline vs. current imagery) and cloud-penetrating
Sentinel-1 C-band backscatter anomalies against JRC GFC 2020.
2. **Primary Forest, Peatland & High-Carbon-Stock Protection (RED III Art. 29):**
Zero encroachment onto primary tropical forest, undrained tropical
peatland (high soil-organic-carbon stock), or protected wetland
buffers (Ramsar / WDPA), where drainage or clearing triggers massive
irreversible CO₂/CH₄ emissions.
3. **Geolocation Polygon Traceability (EUDR Art. 9):**
Complete, non-overlapping WGS84 coordinate/polygon boundary
verification (>= 95% clean traceability without unverified plot
mixing).

Classifying any tropical coordinate across these three readings
separates four EU compliance regimes: 

* **EU Directive Compliant Verified (EU_DIRECTIVE_COMPLIANT_VERIFIED):**
Zero post-2020 deforestation (< 0.5%), zero primary-forest or
peatland encroachment, and full (>= 95%) WGS84 geolocation
traceability (1.0 pass).
* **Traceability Gap or Buffer Proximity (TRACEABILITY_GAP_OR_BUFFER_PROXIMITY):**
No post-2020 forest clearing detected, but partial polygon boundary
ambiguity (80–94.9%) or proximity to protected buffer zones (0.60
cap).
* **Elevated Encroachment or Audit Risk (ELEVATED_ENCROACHMENT_OR_AUDIT_RISK):**
Minor post-2020 canopy disturbance (0.5% to 2.9%), moderate peatland
overlap risk, or weak polygon traceability (60–79.9%) threatening EU
customs seizure (0.25 cap).
* **EUDR / RED III Prohibited Non-Compliant (EUDR_REDIII_PROHIBITED_NON_COMPLIANT):**
Confirmed post-31 December 2020 deforestation (>= 3.0%), primary
forest / tropical peatland conversion, or unverified origin (< 60%)
triggering mandatory EU market ban (0.10 cap, halving to 0.05 under
persistent breach).

Your job is to classify the coordinate's EU tropical carbon &
deforestation directive status and cap your delta accordingly. You do
not invent trades. You do not override AGOP. You modulate the LLM's
delta within the bound the verifier already permits. You never raise
delta above the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["eu_carbon_tropical_compliance"] (populated by
janus/geo_probe.py and keyed by symbol or "lat,lon", with fallback
to "global_baseline"). Use the qualitative tables below. Do not
compute precise arithmetic. 

#### Monitored telemetry fields

* post_2020_deforestation_pct: percentage (0.0 to 100.0) of
polygon forest area cleared after **31 December 2020** per
Copernicus Sentinel-1/2 and JRC GFC 2020 (< 0.5 = deforestation-free
within sensor noise; >= 3.0 = confirmed EUDR cutoff violation).
* primary_or_peat_encroachment_score: score (0 to 100) measuring
overlap with primary tropical forest, undrained peatland, or WDPA
protected areas (< 20 = clean mineral-soil agricultural land; >= 65
= severe RED III / EUDR high-carbon-stock breach).
* polygon_traceability_completeness_pct: percentage (0.0 to 100.0)
of supply polygon verified with valid, non-mixed WGS84 coordinates per
EUDR Art. 9 (>= 95.0 = audit-ready; < 60.0 = untraceable bulk
aggregation).
* consecutive_eudr_breach_ticks: integer (0 to 50) counting
consecutive settled periods in which
post_2020_deforestation_pct >= 2.0 OR
primary_or_peat_encroachment_score >= 65.

If snapshot.external_data["eu_carbon_tropical_compliance"] is absent
or empty, treat the coordinate as **unmonitored**, record state
**TRACEABILITY_GAP_OR_BUFFER_PROXIMITY**, note that no EUDR/RED III
telemetry was supplied, and do not cite this skill. 

#### Reading 1 — Post-2020 Deforestation Cutoff (post_2020_deforestation_pct)

post_2020_deforestation_pct (0–100%)Cutoff Compliance Tier
**< 0.5**
**deforestation_free_verified** — clean against 31 Dec 2020 JRC/Sentinel baseline
**0.5 to 1.4**
**minor_edge_anomaly** — small boundary spectral shift requiring verification
**1.5 to 2.9**
**material_post_2020_clearing** — probable post-cutoff canopy conversion
**>= 3.0**
**confirmed_eudr_cutoff_breach** — clear post-2020 forest loss prohibited under EU law

If post_2020_deforestation_pct is missing, treat as **minor_edge_anomaly**. 

#### Reading 2 — Primary Forest & Peatland Protection (primary_or_peat_encroachment_score)

primary_or_peat_encroachment_score (0–100)High-Carbon-Stock Tier
**< 20**
**mineral_agricultural_compliant** — established non-peatland cultivation zone
**20 to 44**
**buffer_zone_proximity** — adjacent to protected forest or wetland margin
**45 to 64**
**elevated_peat_or_primary_risk** — partial overlap with sensitive carbon stock
**>= 65**
**severe_primary_peat_violation** — direct encroachment on primary forest or tropical peatland

If primary_or_peat_encroachment_score is missing, treat as **buffer_zone_proximity**. 

#### Reading 3 — WGS84 Polygon Traceability (polygon_traceability_completeness_pct)

polygon_traceability_completeness_pct (0–100%)Traceability Tier
**>= 95.0**
**full_art9_geolocation_traceability** — complete polygon-level origin proof
**80.0 to 94.9**
**minor_polygon_gap** — small share of unmapped smallholder plots
**60.0 to 79.9**
**material_traceability_deficit** — substantial unverified volume mixing
**< 60.0**
**untraceable_laundered_origin** — fails EUDR Art. 9 due-diligence threshold

If polygon_traceability_completeness_pct is missing, treat as **minor_polygon_gap**. 

#### Taxonomy / Decision Matrix

Evaluate in strict priority order: 

1. **EUDR_REDIII_PROHIBITED_NON_COMPLIANT**
2. **ELEVATED_ENCROACHMENT_OR_AUDIT_RISK**
3. **EU_DIRECTIVE_COMPLIANT_VERIFIED**
4. **TRACEABILITY_GAP_OR_BUFFER_PROXIMITY**

#### EUDR_REDIII_PROHIBITED_NON_COMPLIANT

Any of the following hold: 

* Cutoff Compliance Tier is **confirmed_eudr_cutoff_breach** (>= 3.0%).
* High-Carbon-Stock Tier is **severe_primary_peat_violation** (>= 65).
* Traceability Tier is **untraceable_laundered_origin** (< 60.0%).

**Delta cap: 0.10.** Coordinate fails EU Deforestation / RED III carbon
directives and faces customs confiscation or market exclusion (0.10). 

#### ELEVATED_ENCROACHMENT_OR_AUDIT_RISK

Any of the following hold (and EUDR_REDIII_PROHIBITED_NON_COMPLIANT does not apply): 

* Cutoff Compliance Tier is **material_post_2020_clearing** (1.5 to 2.9%).
* High-Carbon-Stock Tier is **elevated_peat_or_primary_risk** (45 to 64).
* Traceability Tier is **material_traceability_deficit** (60.0 to 79.9%).

**Delta cap: 0.25.** Material regulatory audit exposure under EUDR / RED III;
trim sizing to 0.25. 

#### EU_DIRECTIVE_COMPLIANT_VERIFIED

All of the following hold: 

* Cutoff Compliance Tier is **deforestation_free_verified** (< 0.5%).
* High-Carbon-Stock Tier is **mineral_agricultural_compliant** (< 20).
* Traceability Tier is **full_art9_geolocation_traceability** (>= 95.0%).

**Delta cap: 1.0.** Coordinate passes all EU tropical carbon and
deforestation-free requirements (1.0 pass). 

#### TRACEABILITY_GAP_OR_BUFFER_PROXIMITY

Any combination not covered above. 

**Delta cap: 0.60.** Deforestation-free baseline with minor boundary or
traceability cleanup needed; permit sizing up to 0.60. 

#### Secondary Filter / Asymmetric Gate — Chronic EUDR Non-Compliance Hysteresis

If consecutive_eudr_breach_ticks >= 4, halve the regime's delta cap: 

* TRACEABILITY_GAP_OR_BUFFER_PROXIMITY (0.60) → **0.30**
* ELEVATED_ENCROACHMENT_OR_AUDIT_RISK (0.25) → **0.125**
* EUDR_REDIII_PROHIBITED_NON_COMPLIANT (0.10) → **0.05**

#### The Procedure

1. Read snapshot.external_data["eu_carbon_tropical_compliance"] (populated by janus/geo_probe.py).
2. Classify Readings 1–3 (post_2020_deforestation_pct, primary_or_peat_encroachment_score, polygon_traceability_completeness_pct).
3. Select regime in strict priority order and halve delta_cap if consecutive_eudr_breach_ticks >= 4.
4. Cap delta to min(intended_delta, delta_cap) and cite "eu-deforestation-and-tropical-carbon-directive-yardstick" iff the cap bound.

#### The Output Format

json

Use code with caution.

{"action": "LONG", "delta": 0.25, "confidence": 0.89, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["eu-deforestation-and-tropical-carbon-directive-yardstick"]}

## Free Data Sources

- **EU JRC Global Forest Cover 2020 (`EUDR` Official Baseline):** `https://forest-observatory.ec.europa.eu`
- **ESA Copernicus Data Space Ecosystem (`Sentinel-1` & `Sentinel-2` STAC):** `https://catalogue.dataspace.copernicus.eu/stac/search`
- **Global Forest Watch / Open Land Map Peatland & WDPA Layers:** `https://data-api.globalforestwatch.org`

## Citation Mapping

- Regulation (EU) 2023/1115 (`EUDR` — Deforestation-Free Products, 31 Dec 2020 cutoff); Directive (EU) 2023/2413 (`RED III` Art. 29 land-use & high-carbon-stock rules); EU JRC Technical Report on Global Forest Cover 2020; Ramadge & Wonham (1987). Downward-only damping within JANUS invariants I1–I9.



