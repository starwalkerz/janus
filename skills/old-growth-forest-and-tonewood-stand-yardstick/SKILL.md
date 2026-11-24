#### name: "old-growth-forest-and-tonewood-stand-yardstick"
description: "Geospatial remote-sensing yardstick evaluating arbitrary WGS84 Earth coordinates over free ESA Copernicus Sentinel-1 C-band SAR, Sentinel-2 MSI optical, JRC Primary Forest, and Hansen Global Forest Change data: distinguishing intact multi-layered old-growth and slow-grown tonewood stands (high VH/VV volume scattering, elevated NDMI/NDVI structural maturity, zero post-2000 clear-cut disturbance) from young monoculture plantations or degraded clear-cuts to govern forestry, timber, and natural-capital sizing."

#### Old-Growth Forest & Tonewood Stand Yardstick

You are reading the tick against **planetary coordinate verification of
intact old-growth forest structure and multi-layered canopy maturity**—evaluated
from free, open Earth-observation sensors (**ESA Copernicus Sentinel-1
C-band SAR**, **Sentinel-2 MSI multispectral**, **EU JRC Primary Forest
Map**, and **Hansen Global Forest Change**). 

Whether auditing a Nordic slow-grown spruce stand (*sointikuusi* /
quarter-sawn acoustic tonewood), a boreal primary forest reserve, or a
tropical intact forest landscape (IFL), surface timber labels frequently
conflate **true old-growth / multi-layered primary stands** with
**even-aged industrial pulpwood plantations or recently clear-cut
regrowth**: 

1. **Multi-Layered Canopy Structural Maturity (Sentinel-2 MSI NDVI / NDMI & JRC Forest Type):**
Old-growth stands exhibit heterogeneous gap dynamics, high canopy
moisture retention (NDMI), uneven vertical crown layering, and
elevated standing deadwood (snags and coarse woody debris) rather
than uniform single-cohort spectral signatures (Jerry F. Franklin et
al., *Ecological Applications* 12(2), 2002; Peter Potapov et al.,
*Science Advances* 3(1), 2017).
2. **C-Band Cross-Polarized Volume Backscatter (Sentinel-1 VH/VV Ratio):**
Unlike optical sensors blocked by Nordic or tropical cloud cover,
Sentinel-1 C-band synthetic aperture radar penetrates clouds and
measures **3D woody branch and stem volume scattering (VH/VV)**—cleanly
separating dense, structurally complex old-growth biomass from young
regrowth or clear-cut ground (Attila Lang et al., *Remote Sensing of
Environment*, 2023).
3. **Long-Horizon Disturbance Integrity (Hansen GFC 2000–Present):**
True old-growth forest requires multi-decade absence of stand-replacing
clear-cuts, road-grid fragmentation, or canopy-loss events.

Classifying any supplied coordinate (latitude, longitude) across these
three sensor readings separates four forest-integrity regimes: 

* **Intact Old-Growth Verified (INTACT_OLD_GROWTH_VERIFIED):** High
canopy structural maturity, strong C-band VH/VV woody volume
scattering, and near-zero (< 2%) post-2000 stand disturbance (1.0
pass—genuine old-growth / high-value tonewood or primary conservation
asset).
* **Maturing Secondary Stand (MATURING_SECONDARY_STAND):** Moderately
developed multi-cohort canopy without acute recent clear-cutting
(0.60 cap).
* **Even-Aged Plantation or Fragmented Canopy (EVEN_AGED_PLANTATION_OR_FRAGMENTED):**
Low vertical complexity, uniform monoculture radar signature, or
material historical thinning/fragmentation (0.25 cap).
* **Clear-Cut Disturbed or Non-Forest (CLEAR_CUT_DISTURBED_OR_NON_FOREST):**
Recent stand-replacing canopy loss (>= 15%), low woody radar
backscatter, or mislabeled non-forest land (0.10 cap, halving to
0.05 under persistent active logging/disturbance).

Your job is to classify the coordinate's old-growth forest regime and cap
your delta accordingly. You do not invent trades. You do not override
AGOP. You modulate the LLM's delta within the bound the verifier
already permits. You never raise delta above the strategy cap, and you
never invent an action outside allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["old_growth_forest"] (populated by
janus/geo_probe.py and keyed by symbol or "lat,lon", with fallback
to "global_baseline"). Use the qualitative tables below. Do not
compute precise arithmetic. 

#### Monitored telemetry fields

* canopy_structural_maturity_score: score (0 to 100) derived from
Sentinel-2 NDVI/NDMI textural heterogeneity and JRC primary
forest layers (>= 75 = complex uneven-aged old-growth canopy; < 35
= uniform young regrowth or bare ground).
* sar_vh_vv_volume_backscatter_score: score (0 to 100) derived
from Sentinel-1 C-band VH/VV cross-polarization woody volume
scattering (>= 70 = dense multi-story woody biomass; < 35 = sparse
canopy or clear-cut soil).
* post_2000_disturbance_loss_pct: percentage (0.0 to 100.0) of
polygon area experiencing stand-replacing tree-cover loss since year
2000 per Hansen GFC / Copernicus change detection (< 2.0 =
undisturbed; >= 15.0 = heavily logged or clear-cut).
* consecutive_disturbance_ticks: integer (0 to 50) counting
consecutive settled periods in which
post_2000_disturbance_loss_pct >= 10.0 OR
sar_vh_vv_volume_backscatter_score < 35.

If snapshot.external_data["old_growth_forest"] is absent or empty,
treat the coordinate as **unmonitored**, record state
**MATURING_SECONDARY_STAND**, note that no geospatial telemetry was
supplied, and do not cite this skill. 

#### Reading 1 — Canopy Structural Maturity (canopy_structural_maturity_score)

canopy_structural_maturity_score (0–100)Canopy Maturity Tier
**>= 75**
**old_growth_multi_layered** — uneven-aged canopy, high moisture retention (NDMI), deadwood heterogeneity
**50 to 74**
**maturing_mixed_stand** — developing multi-cohort stand with partial structural complexity
**35 to 49**
**uniform_young_plantation** — homogeneous single-cohort spectral texture
**< 35**
**degraded_or_non_canopy** — open clear-cut, scrub, or non-forest land

If canopy_structural_maturity_score is missing, treat as
**maturing_mixed_stand**. 

#### Reading 2 — Sentinel-1 SAR Woody Volume Backscatter (sar_vh_vv_volume_backscatter_score)

sar_vh_vv_volume_backscatter_score (0–100)Radar Volume Tier
**>= 70**
**dense_old_growth_biomass** — strong C-band cross-polarized volume scattering
**45 to 69**
**moderate_woody_biomass** — established mid-rotation timber volume
**35 to 44**
**thin_monoculture_volume** — low structural branch complexity
**< 35**
**clear_cut_surface_scatter** — flat ground or early seedling stage

If sar_vh_vv_volume_backscatter_score is missing, treat as
**moderate_woody_biomass**. 

#### Reading 3 — Post-2000 Disturbance Integrity (post_2000_disturbance_loss_pct)

post_2000_disturbance_loss_pct (0–100%)Disturbance Tier
**< 2.0**
**intact_undisturbed** — zero stand-replacing harvesting or road-grid fragmentation
**2.0 to 6.9**
**minor_natural_gap_turnover** — localized windthrow or selective single-stem extraction
**7.0 to 14.9**
**material_thinning_footprint** — significant historical harvesting impact
**>= 15.0**
**acute_clear_cut_disturbance** — widespread stand-replacing deforestation/logging

If post_2000_disturbance_loss_pct is missing, treat as
**minor_natural_gap_turnover**. 

#### Taxonomy / Decision Matrix

Evaluate in strict priority order: 

1. **CLEAR_CUT_DISTURBED_OR_NON_FOREST**
2. **EVEN_AGED_PLANTATION_OR_FRAGMENTED**
3. **INTACT_OLD_GROWTH_VERIFIED**
4. **MATURING_SECONDARY_STAND**

#### CLEAR_CUT_DISTURBED_OR_NON_FOREST

Any of the following hold: 

* Disturbance Tier is **acute_clear_cut_disturbance** (>= 15.0%).
* Canopy Maturity Tier is **degraded_or_non_canopy** (< 35).
* Radar Volume Tier is **clear_cut_surface_scatter** (< 35).

**Delta cap: 0.10.** Coordinate exhibits clear-cut disturbance or lacks
standing forest structure; clamp sizing sharply (0.10). 

#### EVEN_AGED_PLANTATION_OR_FRAGMENTED

Any of the following hold (and CLEAR_CUT_DISTURBED_OR_NON_FOREST does not apply): 

* Disturbance Tier is **material_thinning_footprint** (7.0 to 14.9%).
* Canopy Maturity Tier is **uniform_young_plantation** (35 to 49).
* Radar Volume Tier is **thin_monoculture_volume** (35 to 44).

**Delta cap: 0.25.** Coordinate represents an even-aged plantation or
fragmented stand rather than intact old-growth; trim sizing to 0.25. 

#### INTACT_OLD_GROWTH_VERIFIED

All of the following hold: 

* Canopy Maturity Tier is **old_growth_multi_layered** (>= 75).
* Radar Volume Tier is **dense_old_growth_biomass** (>= 70).
* Disturbance Tier is **intact_undisturbed** (< 2.0%).

**Delta cap: 1.0.** Copernicus Sentinel-1/2 and historical disturbance
sensors confirm intact multi-layered old-growth forest (1.0 pass). 

#### MATURING_SECONDARY_STAND

Any combination not covered above. 

**Delta cap: 0.60.** Maturing secondary stand without acute disturbance;
permit disciplined sizing up to 0.60. 

#### Secondary Filter / Asymmetric Gate — Active Logging & Disturbance Hysteresis

If consecutive_disturbance_ticks >= 4, halve the regime's delta cap: 

* MATURING_SECONDARY_STAND (0.60) → **0.30**
* EVEN_AGED_PLANTATION_OR_FRAGMENTED (0.25) → **0.125**
* CLEAR_CUT_DISTURBED_OR_NON_FOREST (0.10) → **0.05**

#### The Procedure

1. Read snapshot.external_data["old_growth_forest"] (populated by janus/geo_probe.py).
2. Classify Readings 1–3 (canopy_structural_maturity_score, sar_vh_vv_volume_backscatter_score, post_2000_disturbance_loss_pct).
3. Select regime in strict priority order and halve delta_cap if consecutive_disturbance_ticks >= 4.
4. Cap delta to min(intended_delta, delta_cap) and cite "old-growth-forest-and-tonewood-stand-yardstick" iff the cap bound.

The Output Format

json
{"action": "LONG", "delta": 0.25, "confidence": 0.88, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["old-growth-forest-and-tonewood-stand-yardstick"]}
Use code with caution.

Free Data Sources

• ESA Copernicus Data Space Ecosystem (Sentinel-1 GRD & Sentinel-2 L2A STAC API): https://copernicus.eu
• EU JRC Global Forest Observatory & Primary Forest Datasets: https://europa.eu
• Hansen / UMD Global Forest Change (2000–Present): https://googleapis.com

Citation Mapping

• Jerry F. Franklin et al., "Disturbances and Structural Development of Natural Forest Ecosystems with Silvicultural Implications," Forest Ecology and Management 155, 399–423 (2002); Peter Potapov et al., "The Last Frontiers of Wilderness," Science Advances 3(1) (2017); Ramadge & Wonham (1987). Downward-only damping within JANUS invariants I1–I9.