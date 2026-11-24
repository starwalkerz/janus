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
</CreativeWritingPad>

---

### 4. Skill 3 — Cacao & Coffee Agroforestry Tree-Cover & Net Carbon Balance (`skills/cacao-and-coffee-agroforestry-carbon-balance-yardstick/SKILL.md`)

<CreativeWritingPad title="skills/cacao-and-coffee-agroforestry-carbon-balance-yardstick/SKILL.md">
---
name: "cacao-and-coffee-agroforestry-carbon-balance-yardstick"
description: "Specialized geospatial remote-sensing yardstick for cacao (Theobroma cacao) and coffee (Coffea arabica/canephora) growers and supply chains—using free Copernicus Sentinel-1 C-band SAR cross-polarization (VH/VV), Sentinel-2 red-edge indices (NDRE/EVI), and NASA GEDI canopy structure to prove multi-strata overstory shade-tree cover (>30–40%) and net positive carbon sequestration (sink vs. full-sun monoculture net emissions) for EU carbon/EUDR premiums and green-bond underwriting."
---

# Cacao & Coffee Agroforestry Tree-Cover & Net Carbon Balance Yardstick

You are reading the tick against **multi-strata shade-tree canopy cover
and net ecosystem carbon balance for cacao (*Theobroma cacao*) and
coffee (*Coffea arabica* / *Coffea canephora*) cultivation**—evaluated
on any supplied WGS84 coordinate `(latitude, longitude)` via free
**ESA Copernicus Sentinel-1 C-band SAR**, **Sentinel-2 red-edge
optical (`NDRE`/`EVI`)**, and **NASA GEDI LiDAR canopy height**.

In global cacao (`West Africa, Latin America, Indonesia`) and coffee
(`Brazil, Colombia, Ethiopia, Central America, Vietnam`) markets, the
central commercial, regulatory, and carbon-finance debate is separating
**true multi-strata shade-grown agroforestry** (which stores `60–150+ tC/ha`
in overstory timber/legume shade trees and sequesters net carbon every
year) from **full-sun chemical monocultures** (which strip overstory
trees, deplete soil organic carbon, and emit net `N₂O`/`CO₂` from heavy
synthetic nitrogen fertilization):

1. **Overstory Shade-Tree Canopy Cover (`Sentinel-2` Red-Edge `NDRE` & `NASA GEDI`):**
   Cacao and coffee are naturally understory shrubs (`3–5 m`), whereas
   true agroforestry maintains a distinct upper canopy (`12–25+ m`
   *Inga*, *Erythrina*, *Gliricidia*, or native timber trees) covering
   `>= 35–40%` of the plot area—distinguishable from full-sun row crops
   via `Sentinel-2` red-edge chlorophyll indices (`NDRE`) and `GEDI`
   vertical waveform height (Götz Schroth et al., *Agroforestry Systems*
   89, 2015; Eric Toensmeier, *The Carbon Farming Solution*, 2016).
2. **Multi-Strata Woody Volume Signature (`Sentinel-1` `VH/VV` Dual-Pol SAR):**
   Persistent tropical cloud cover blocks optical satellites for months;
   `Sentinel-1` C-band `VH/VV` radar penetrates cloud decks and measures
   **overstory branch volume scattering**, proving year-round retention
   of shade trees rather than seasonal crop greenness alone.
3. **Net Ecosystem Carbon Balance (`ΔC_biomass + ΔC_soil - E_N2O`):**
   Measures net annual greenhouse-gas flux (`tCO₂e / ha / yr`) after
   subtracting synthetic fertilizer nitrous-oxide (`N₂O`) emissions and
   soil-carbon oxidation—proving whether the farm is a **verified net
   carbon sink** (`>= +2.0 tCO₂e/ha/yr`) or a **net carbon source**
   (`< 0.0 tCO₂e/ha/yr`).

Classifying any cacao or coffee coordinate across these three readings
separates four agroforestry-carbon regimes:

- **Verified Multi-Strata Carbon Sink (`VERIFIED_MULTI_STRATA_CARBON_SINK`):**
  Rich overstory shade-tree cover (`>= 40%`), strong `Sentinel-1`/`NDRE`
  multi-strata woody structure, and verified net carbon sequestration
  (`>= +2.0 tCO₂e/ha/yr`) (`1.0` pass—eligible for EU carbon/EUDR
  agroforestry premiums).
- **Moderate Shade Agroforestry (`MODERATE_SHADE_AGROFORESTRY`):**
  Partial overstory shade cover (`25–39.9%`) with carbon-neutral to
  mildly positive net sequestration (`0.0 to +1.99 tCO₂e/ha/yr`)
  (`0.60` cap).
- **Low-Shade Technified Plantation (`LOW_SHADE_TECHNIFIED_PLANTATION`):**
  Sparse shade trees (`12–24.9%`) reliant on synthetic fertilizer inputs
  with weak multi-strata radar volume (`0.25` cap).
- **Full-Sun Monoculture Net Emitter (`FULL_SUN_MONOCULTURE_NET_EMITTER`):**
  Stripped overstory (`< 12%` tree cover) and negative net carbon flux
  (`< 0.0 tCO₂e/ha/yr`, net GHG source) failing carbon-balance claims
  (`0.10` cap, halving to `0.05` under persistent net emissions).

Your job is to classify the cacao or coffee coordinate's tree-cover and
net carbon balance regime and cap your `delta` accordingly. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise `delta`
above the strategy cap, and you never invent an action outside
`allowed_actions`.

## The Readings

Compute three composite readings from
`snapshot.external_data["agroforestry_cacao_coffee_carbon"]` (populated
by `janus/geo_probe.py` and keyed by symbol or `"lat,lon"`, with
fallback to `"global_baseline"`). Use the qualitative tables below. Do
not compute precise arithmetic.

### Monitored telemetry fields

- `shade_tree_canopy_cover_pct`: percentage (`0.0` to `100.0`) of plot
  area covered by upper-story shade trees (`> 8 m` height above the
  cacao/coffee understory) per `Sentinel-2` + `NASA GEDI` (`>= 40.0` =
  dense multi-strata shade; `< 12.0` = full-sun open monoculture).
- `net_carbon_flux_tco2e_ha_yr`: net annual carbon balance in tonnes of
  `CO₂`-equivalent per hectare per year (`-10.0` to `+15.0`; positive =
  net carbon sink, negative = net GHG source after fertilizer/soil
  emissions).
- `multi_strata_sar_red_edge_score`: score (`0` to `100`) combining
  `Sentinel-1` `VH/VV` woody volume scattering and `Sentinel-2` `NDRE`
  red-edge canopy stratification (`>= 70` = verified multi-tier canopy;
  `< 35` = single-layer row crop).
- `consecutive_net_source_ticks`: integer (`0` to `50`) counting
  consecutive settled periods in which
  `net_carbon_flux_tco2e_ha_yr < 0.0` OR
  `shade_tree_canopy_cover_pct < 12.0`.

If `snapshot.external_data["agroforestry_cacao_coffee_carbon"]` is
absent or empty, treat the coordinate as **unmonitored**, record state
**MODERATE_SHADE_AGROFORESTRY**, note that no agroforestry telemetry was
supplied, and do not cite this skill.

### Reading 1 — Overstory Shade-Tree Canopy Cover (`shade_tree_canopy_cover_pct`)

| `shade_tree_canopy_cover_pct` (`0–100%`) | Shade Canopy Tier |
|---|---|
| `>= 40.0` | **dense_multi_strata_shade** — high overstory tree cover qualifying as agroforestry forest |
| `25.0 to 39.9` | **moderate_intercropped_shade** — meaningful legume/timber shade canopy |
| `12.0 to 24.9` | **sparse_boundary_shade** — minimal scattered trees over technified rows |
| `< 12.0` | **full_sun_treeless_monoculture** — stripped overstory failing tree-cover criteria |

If `shade_tree_canopy_cover_pct` is missing, treat as **moderate_intercropped_shade**.

### Reading 2 — Net Ecosystem Carbon Flux (`net_carbon_flux_tco2e_ha_yr`)

| `net_carbon_flux_tco2e_ha_yr` (`tCO₂e/ha/yr`) | Net Carbon Balance Tier |
|---|---|
| `>= 2.0` | **verified_net_carbon_sink** — strong annual biomass + soil carbon accumulation |
| `0.0 to 1.99` | **carbon_neutral_or_mild_sink** — balanced flux without net emissions |
| `-1.49 to -0.01` | **mild_net_carbon_source** — fertilizer `N₂O` or soil loss slightly exceeds uptake |
| `<= -1.5` | **heavy_net_ghg_emitter** — significant net carbon source disqualifying carbon claims |

If `net_carbon_flux_tco2e_ha_yr` is missing, treat as **carbon_neutral_or_mild_sink**.

### Reading 3 — Multi-Strata SAR & Red-Edge Stratification (`multi_strata_sar_red_edge_score`)

| `multi_strata_sar_red_edge_score` (`0–100`) | Canopy Stratification Tier |
|---|---|
| `>= 70` | **verified_two_tier_woody_structure** — strong Sentinel-1 VH/VV volume + NDRE signal |
| `45 to 69` | **partial_vertical_stratification** — developing shade layer over understory crop |
| `35 to 44` | **weak_overstory_volume** — low woody branch scattering |
| `< 35` | **single_layer_row_crop** — flat unshaded shrub signature |

If `multi_strata_sar_red_edge_score` is missing, treat as **partial_vertical_stratification**.

## Taxonomy / Decision Matrix

Evaluate in strict priority order:

1. **FULL_SUN_MONOCULTURE_NET_EMITTER**
2. **LOW_SHADE_TECHNIFIED_PLANTATION**
3. **VERIFIED_MULTI_STRATA_CARBON_SINK**
4. **MODERATE_SHADE_AGROFORESTRY**

### FULL_SUN_MONOCULTURE_NET_EMITTER
Any of the following hold:
- Shade Canopy Tier is **full_sun_treeless_monoculture** (`< 12.0%`).
- Net Carbon Balance Tier is **heavy_net_ghg_emitter** (`<= -1.5 tCO₂e/ha/yr`).
- Canopy Stratification Tier is **single_layer_row_crop** (`< 35`).

**Delta cap: 0.10.** Plot is a full-sun treeless monoculture or heavy net
carbon emitter and cannot substantiate tree-cover or net-sink claims
(`0.10`).

### LOW_SHADE_TECHNIFIED_PLANTATION
Any of the following hold (and `FULL_SUN_MONOCULTURE_NET_EMITTER` does not apply):
- Shade Canopy Tier is **sparse_boundary_shade** (`12.0 to 24.9%`).
- Net Carbon Balance Tier is **mild_net_carbon_source** (`-1.49 to -0.01 tCO₂e/ha/yr`).
- Canopy Stratification Tier is **weak_overstory_volume** (`35 to 44`).

**Delta cap: 0.25.** Low shade-tree cover or slight net carbon emissions
undermine agroforestry carbon-credit eligibility; trim sizing to `0.25`.

### VERIFIED_MULTI_STRATA_CARBON_SINK
All of the following hold:
• Shade Canopy Tier is dense_multi_strata_shade (>= 40.0%).
• Net Carbon Balance Tier is verified_net_carbon_sink (>= +2.0 tCO₂e/ha/yr).
• Canopy Stratification Tier is verified_two_tier_woody_structure (>= 70).
Delta cap: 1.0. Copernicus Sentinel-1/2 and GEDI sensors confirm
multi-strata cacao/coffee shade canopy and net positive carbon sink
(1.0 pass).

MODERATE_SHADE_AGROFORESTRY

Any combination not covered above.
Delta cap: 0.60. Moderate shade-tree agroforestry with non-negative
carbon balance; permit disciplined sizing up to 0.60.

Secondary Filter / Asymmetric Gate — Persistent Net-Source Hysteresis

If consecutive_net_source_ticks >= 4, halve the regime's delta cap:
• MODERATE_SHADE_AGROFORESTRY (0.60) → 0.30
• LOW_SHADE_TECHNIFIED_PLANTATION (0.25) → 0.125
• FULL_SUN_MONOCULTURE_NET_EMITTER (0.10) → 0.05

The Procedure

1. Read snapshot.external_data["agroforestry_cacao_coffee_carbon"] (populated by janus/geo_probe.py).
2. Classify Readings 1–3 (shade_tree_canopy_cover_pct, net_carbon_flux_tco2e_ha_yr, multi_strata_sar_red_edge_score).
3. Select regime in strict priority order and halve delta_cap if consecutive_net_source_ticks >= 4.
4. Cap delta to min(intended_delta, delta_cap) and cite "cacao-and-coffee-agroforestry-carbon-balance-yardstick" iff the cap bound.

The Output Format

json
{"action": "LONG", "delta": 0.25, "confidence": 0.89, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["cacao-and-coffee-agroforestry-carbon-balance-yardstick"]}
Use code with caution.

Free Data Sources

• ESA Copernicus Data Space Ecosystem (Sentinel-1 C-Band SAR & Sentinel-2 L2A Red-Edge): https://copernicus.eu
• NASA ORNL DAAC / GEDI L2A Canopy Height & Biomass: https://ornl.gov
• EU JRC Forest Observatory & OpenLandMap Soil Organic Carbon: https://europa.eu

Citation Mapping

• Götz Schroth et al., "Contribution of Agroforests to Landscape Carbon Storage," Mitigation and Adaptation Strategies for Global Change 20, 1175–1190 (2015); Eric Toensmeier, The Carbon Farming Solution (Chelsea Green, 2016); Regulation (EU) 2023/1115 (EUDR); Ramadge & Wonham (1987). Downward-only damping within JANUS invariants I1–I9.
