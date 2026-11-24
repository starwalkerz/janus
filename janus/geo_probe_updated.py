"""
janus/geo_probe.py 

Planetary WGS84 coordinate probe and free open Copernicus / Element84 Earth Search
COG remote-sensing extractor for JANUS. 

Design principles: 

* Zero paid APIs, zero API keys, and zero static regional tile downloads.
* Queries unauthenticated STAC endpoints: 

  1. ESA Copernicus Data Space Ecosystem (catalogue.dataspace.copernicus.eu/stac/search)
  2. Element84 Earth Search AWS Open Data (earth-search.aws.element84.com/v1/search)
* When rasterio and numpy are installed, performs HTTP range-request windowed
reads directly on public Sentinel-2 L2A Cloud-Optimized GeoTIFFs (COGs) to compute: 

  * SCL cloud/shadow/snow masking (SCL classes 3, 8, 9, 10, 11 excluded)
  * NDVI  = (NIR - RED) / (NIR + RED)
  * NDMI  = (NIR - SWIR16) / (NIR + SWIR16)
  * NDRE  = (NIR08 - REDEDGE1) / (NIR08 + REDEDGE1)
  * GLCM-style quantized co-occurrence entropy & contrast texture on NDVI
Falls back cleanly to stdlib-only STAC metadata when rasterio/numpy are absent.
* Includes a deterministic IPCC Tier-1 (2006 / 2019 Refinement) agroforestry net
carbon flux calculator (compute_ipcc_tier1_agroforestry_flux) requiring no external API.

Usage (CLI):
python -m janus.geo_probe --lat 62.2426 --lon 25.7473 --symbol FOREST_FI
python -m janus.geo_probe --lat -0.4167 --lon 36.9500 --symbol COFFEE_KE --crop coffee
""" 

from **future** import annotations 

import argparse
import json
import math
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any 

COPERNICUS_STAC_SEARCH_URL = "https://catalogue.dataspace.copernicus.eu/stac/search"
ELEMENT84_STAC_SEARCH_URL = "https://earth-search.aws.element84.com/v1/search" 

#### Sentinel-2 Scene Classification Layer (SCL) invalid classes:

#### 0=no_data, 1=saturated/defective, 3=cloud_shadows, 8=cloud_medium_prob,

#### 9=cloud_high_prob, 10=thin_cirrus, 11=snow/ice

INVALID_SCL_CLASSES = (0, 1, 3, 8, 9, 10, 11) 

@dataclass(frozen=True)
class GeoCoordinate:
"""Validated WGS84 planetary coordinate with bounding-box helper.""" 

latitude: float
longitude: float
radius_m: float = 500.0
label: str = ""

def **post_init**(self) -> None:
if not (-90.0 <= self.latitude <= 90.0) or math.isnan(self.latitude):
raise ValueError(f"Invalid latitude {self.latitude}: must be in [-90.0, 90.0]")
if not (-180.0 <= self.longitude <= 180.0) or math.isnan(self.longitude):
raise ValueError(f"Invalid longitude {self.longitude}: must be in [-180.0, 180.0]")
if self.radius_m <= 0.0 or math.isnan(self.radius_m):
raise ValueError(f"Invalid radius_m {self.radius_m}: must be > 0")

def to_bbox(self) -> tuple[float, float, float, float]:
"""Return (min_lon, min_lat, max_lon, max_lat) WGS84 bounding box."""
lat_deg = self.radius_m / 111_320.0
cos_lat = max(0.05, math.cos(math.radians(self.latitude)))
lon_deg = self.radius_m / (111_320.0 * cos_lat)
min_lon = max(-180.0, round(self.longitude - lon_deg, 6))
max_lon = min(180.0, round(self.longitude + lon_deg, 6))
min_lat = max(-90.0, round(self.latitude - lat_deg, 6))
max_lat = min(90.0, round(self.latitude + lat_deg, 6))
return (min_lon, min_lat, max_lon, max_lat)

@property
def is_tropical_belt(self) -> bool:
"""True if coordinate lies between Tropic of Cancer and Tropic of Capricorn (±23.436°)."""
return abs(self.latitude) <= 23.436

def _post_json(url: str, body: dict[str, Any], timeout_s: float = 8.0) -> dict[str, Any]:
"""Stdlib-only HTTPS JSON POST helper."""
payload = json.dumps(body).encode("utf-8")
req = urllib.request.Request(
url,
data=payload,
headers={
"Content-Type": "application/json",
"Accept": "application/json",
"User-Agent": "JANUS-GeoProbe/1.1",
},
method="POST",
)
with urllib.request.urlopen(req, timeout=timeout_s) as resp:
return json.loads(resp.read().decode("utf-8")) 

def query_copernicus_stac_scenes(
coord: GeoCoordinate,
collections: tuple[str, ...] = ("SENTINEL-2", "SENTINEL-1"),
limit: int = 6,
timeout_s: float = 8.0,
) -> dict[str, Any]:
"""
Query the free, unauthenticated Copernicus Data Space Ecosystem STAC API
for recent Sentinel-1 (C-band SAR) and Sentinel-2 (MSI optical) scenes.
"""
try:
raw = _post_json(
COPERNICUS_STAC_SEARCH_URL,
{"bbox": list(coord.to_bbox()), "collections": list(collections), "limit": limit},
timeout_s=timeout_s,
)
features = raw.get("features", [])
scene_summaries = [
{
"id": feat.get("id", ""),
"collection": feat.get("collection", ""),
"datetime": feat.get("properties", {}).get("datetime", ""),
"cloud_cover": feat.get("properties", {}).get("eo:cloud_cover"),
}
for feat in features
]
return {
"status": "ok",
"source": "copernicus_dataspace_stac",
"scene_count": len(scene_summaries),
"scenes": scene_summaries,
}
except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
return {
"status": "offline_or_unreachable",
"source": "copernicus_dataspace_stac",
"error": str(exc),
"scene_count": 0,
"scenes": [],
} 

def _compute_glcm_texture_stats(array_2d: Any, levels: int = 16) -> tuple[float, float]:
"""
Compute horizontal + vertical quantized Gray-Level Co-occurrence Matrix (GLCM)
Shannon entropy and contrast on a 2D numpy array without needing scikit-image.
"""
import numpy as np 

valid = array_2d[np.isfinite(array_2d)]
if valid.size < 4:
return 0.0, 0.0

vmin, vmax = float(np.min(valid)), float(np.max(valid))
if vmax - vmin < 1e-9:
return 0.0, 0.0

scaled = np.clip((array_2d - vmin) / (vmax - vmin) * (levels - 1), 0, levels - 1)
q = np.where(np.isfinite(array_2d), scaled.astype(np.int32), -1)

glcm = np.zeros((levels, levels), dtype=np.float64)

#### Horizontal neighbor pairs

h_left, h_right = q[:, :-1], q[:, 1:]
h_mask = (h_left >= 0) & (h_right >= 0)
if np.any(h_mask):
np.add.at(glcm, (h_left[h_mask], h_right[h_mask]), 1.0)
np.add.at(glcm, (h_right[h_mask], h_left[h_mask]), 1.0) 

# Vertical neighbor pairs

v_top, v_bot = q[:-1, :], q[1:, :]
v_mask = (v_top >= 0) & (v_bot >= 0)
if np.any(v_mask):
np.add.at(glcm, (v_top[v_mask], v_bot[v_mask]), 1.0)
np.add.at(glcm, (v_bot[v_mask], v_top[v_mask]), 1.0)

total = float(np.sum(glcm))
if total <= 0.0:
return 0.0, 0.0

prob = glcm / total
nz = prob[prob > 0.0]
entropy = float(-np.sum(nz * np.log2(nz)))

idx = np.arange(levels, dtype=np.float64)
diff_sq = (idx[:, None] - idx[None, :]) ** 2
contrast = float(np.sum(prob * diff_sq))
return round(entropy, 4), round(contrast, 4)

def extract_element84_cog_indices(
coord: GeoCoordinate,
max_cloud_cover: float = 35.0,
timeout_s: float = 10.0,
) -> dict[str, Any]:
"""
Query Element84 Earth Search STAC (sentinel-2-l2a) and, when rasterio and
numpy are installed, perform HTTP range-request windowed COG reads for
red (B04), rededge1 (B05), nir (B08), nir08 (B8A), swir16 (B11),
and scl (Scene Classification Layer). 

Returns deterministic cloud-masked NDVI, NDMI, NDRE, and GLCM texture metrics,
or falls back cleanly when optional raster libraries or network access are absent.
"""
try:
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds
except ImportError:
return {
"status": "optional_deps_missing",
"note": "Install rasterio and numpy for direct COG band extraction; using stdlib fallback.",
}

try:
stac_resp = _post_json(
ELEMENT84_STAC_SEARCH_URL,
{
"bbox": list(coord.to_bbox()),
"collections": ["sentinel-2-l2a"],
"limit": 5,
"query": {"eo:cloud_cover": {"lt": max_cloud_cover}},
},
timeout_s=timeout_s,
)
except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
return {"status": "stac_unreachable", "error": str(exc)}

features = stac_resp.get("features", [])
if not features:
return {"status": "no_low_cloud_scenes", "max_cloud_cover": max_cloud_cover}

#### Pick lowest cloud-cover scene

best = min(
features,
key=lambda f: float(f.get("properties", {}).get("eo:cloud_cover", 100.0)),
)
assets = best.get("assets", {})
required_keys = ("red", "rededge1", "nir", "nir08", "swir16", "scl")
if not all(k in assets and "href" in assets[k] for k in required_keys):
return {
"status": "missing_expected_cog_assets",
"scene_id": best.get("id", ""),
"available_assets": sorted(assets.keys()),
} 

bbox_4326 = coord.to_bbox() 

try:
with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif"): 

#### Read 10m reference window from nir (B08)

with rasterio.open(assets["nir"]["href"]) as nir_ds:
dst_bounds = transform_bounds("EPSG:4326", nir_ds.crs, *bbox_4326)
win_10m = from_bounds(*dst_bounds, transform=nir_ds.transform).round_offsets().round_lengths()
out_h = max(4, min(256, int(win_10m.height)))

out_w = max(4, min(256, int(win_10m.width)))
nir = nir_ds.read(1, window=win_10m, out_shape=(out_h, out_w), resampling=Resampling.bilinear).astype(np.float32)
def _read_aligned(asset_key: str, is_mask: bool = False) -> Any:
with rasterio.open(assets[asset_key]["href"]) as ds:
b = transform_bounds("EPSG:4326", ds.crs, *bbox_4326)
w = from_bounds(*b, transform=ds.transform).round_offsets().round_lengths()
resamp = Resampling.nearest if is_mask else Resampling.bilinear
arr = ds.read(1, window=w, out_shape=(out_h, out_w), resampling=resamp)
return arr.astype(np.int32) if is_mask else arr.astype(np.float32)
red = _read_aligned("red")
rededge1 = _read_aligned("rededge1")
nir08 = _read_aligned("nir08")
swir16 = _read_aligned("swir16")
scl = _read_aligned("scl", is_mask=True)
clear_mask = ~np.isin(scl, INVALID_SCL_CLASSES) & (nir > 0.0) & (red > 0.0)
clear_fraction = float(np.mean(clear_mask))
if int(np.sum(clear_mask)) < 4:
return {
"status": "cloud_masked_insufficient_pixels",
"scene_id": best.get("id", ""),
"clear_pixel_fraction": round(clear_fraction, 4),
}
eps = 1e-6
ndvi_2d = np.where(clear_mask, (nir - red) / (nir + red + eps), np.nan)
ndmi_2d = np.where(clear_mask, (nir - swir16) / (nir + swir16 + eps), np.nan)
ndre_2d = np.where(clear_mask, (nir08 - rededge1) / (nir08 + rededge1 + eps), np.nan)
ndvi_mean = float(np.nanmean(ndvi_2d))
ndmi_mean = float(np.nanmean(ndmi_2d))
ndre_mean = float(np.nanmean(ndre_2d))
glcm_entropy, glcm_contrast = _compute_glcm_texture_stats(ndvi_2d)
# Deterministic 0-100 mapping for downstream SKILL.md qualitative tables
maturity_score = int(
round(
max(
0.0,
min(
100.0,
45.0 * max(0.0, ndvi_mean)
+ 35.0 * max(0.0, ndmi_mean + 0.2)
+ 8.0 * min(4.0, glcm_entropy),
),
)
)
)
multi_strata_score = int(
round(
max(
0.0,
min(
100.0,
75.0 * max(0.0, ndre_mean)
+ 40.0 * max(0.0, ndvi_mean)
+ 5.0 * min(4.0, glcm_entropy),
),
)
)
)
return {
"status": "ok",
"source": "element84_earth_search_cog",
"scene_id": best.get("id", ""),
"datetime": best.get("properties", {}).get("datetime", ""),
"scene_cloud_cover": best.get("properties", {}).get("eo:cloud_cover"),
"clear_pixel_fraction": round(clear_fraction, 4),
"ndvi_mean": round(ndvi_mean, 4),
"ndmi_mean": round(ndmi_mean, 4),
"ndre_mean": round(ndre_mean, 4),
"glcm_entropy": glcm_entropy,
"glcm_contrast": glcm_contrast,
"derived_canopy_structural_maturity_score": maturity_score,
"derived_multi_strata_red_edge_score": multi_strata_score,
}
except Exception as exc:  # pragma: no cover - network/GDAL runtime safety
return {
"status": "cog_read_error",
"scene_id": best.get("id", ""),
"error": str(exc),
}
def compute_ipcc_tier1_agroforestry_flux(
shade_tree_canopy_cover_pct: float,
canopy_height_m: float = 14.0,
synthetic_n_fertilizer_kg_ha_yr: float = 40.0,
soil_carbon_gain_tc_ha_yr: float = 0.35,
) -> float:
"""
Deterministic IPCC Tier-1 (2006 / 2019 Refinement) agroforestry net annual
GHG flux calculator in tCO2e / ha / yr (positive = net sink, negative = net source).
Formula:
- Above-ground woody biomass increment scales with overstory shade fraction
and mean tree height (tropical agroforestry benchmark ~1.2–3.5 tC/ha/yr at
full multi-strata cover), plus root-to-shoot ratio R = 0.24 (IPCC Table 4.4).
- Soil organic carbon accumulation scales with shade cover (0.35 tC/ha/yr at
100% shade, -0.40 tC/ha/yr tillage/oxidation penalty when shade < 12%).
- Carbon-to-CO2e conversion factor = 44 / 12.
- Direct synthetic nitrogen N2O emissions: EF1 = 0.01 kg N2O-N / kg N,
N2O-N -> N2O = 44 / 28, IPCC AR6 GWP100(N2O) = 273.
"""
shade_frac = max(0.0, min(1.0, shade_tree_canopy_cover_pct / 100.0))
height_factor = max(0.2, min(2.0, canopy_height_m / 15.0))
aboveground_tc_ha_yr = 2.6 * shade_frac * height_factor
belowground_tc_ha_yr = aboveground_tc_ha_yr * 0.24
if shade_tree_canopy_cover_pct < 12.0:
soc_tc_ha_yr = -0.40
else:
soc_tc_ha_yr = soil_carbon_gain_tc_ha_yr * shade_frac
gross_sequestration_tco2e = (aboveground_tc_ha_yr + belowground_tc_ha_yr + soc_tc_ha_yr) * (44.0 / 12.0)
n2o_n_kg = max(0.0, synthetic_n_fertilizer_kg_ha_yr) * 0.01
n2o_kg = n2o_n_kg * (44.0 / 28.0)
n2o_emissions_tco2e = (n2o_kg * 273.0) / 1000.0
return round(gross_sequestration_tco2e - n2o_emissions_tco2e, 3)
def build_geo_external_data(
coord: GeoCoordinate,
crop_type: str = "generic",
sensor_overrides: dict[str, Any] | None = None,
query_live_stac: bool = True,
extract_cogs: bool = True,
) -> dict[str, Any]:
"""
Build normalized snapshot.external_data keys:
- geo_coordinate
- old_growth_forest
- eu_carbon_tropical_compliance
- agroforestry_cacao_coffee_carbon
"""
overrides = dict(sensor_overrides or {})
stac_meta = (
query_copernicus_stac_scenes(coord)
if query_live_stac
else {"status": "skipped", "source": "copernicus_dataspace_stac", "scene_count": 0, "scenes": []}
)
cog_meta = (
extract_element84_cog_indices(coord)
if (query_live_stac and extract_cogs)
else {"status": "skipped"}
)
if cog_meta.get("status") == "ok":
overrides.setdefault(
"canopy_structural_maturity_score",
cog_meta["derived_canopy_structural_maturity_score"],
)
overrides.setdefault(
"multi_strata_sar_red_edge_score",
cog_meta["derived_multi_strata_red_edge_score"],
)
shade_pct = float(overrides.get("shade_tree_canopy_cover_pct", 42.0))
if "net_carbon_flux_tco2e_ha_yr" not in overrides:
overrides["net_carbon_flux_tco2e_ha_yr"] = compute_ipcc_tier1_agroforestry_flux(
shade_tree_canopy_cover_pct=shade_pct,
canopy_height_m=float(overrides.get("canopy_height_m", 14.0)),
synthetic_n_fertilizer_kg_ha_yr=float(overrides.get("synthetic_n_fertilizer_kg_ha_yr", 40.0)),
)
key = coord.label.strip() or f"{coord.latitude:.5f},{coord.longitude:.5f}"
old_growth_entry = {
"latitude": coord.latitude,
"longitude": coord.longitude,
"canopy_structural_maturity_score": overrides.get("canopy_structural_maturity_score", 55),
"sar_vh_vv_volume_backscatter_score": overrides.get("sar_vh_vv_volume_backscatter_score", 55),
"post_2000_disturbance_loss_pct": overrides.get("post_2000_disturbance_loss_pct", 4.0),
"consecutive_disturbance_ticks": overrides.get("consecutive_disturbance_ticks", 0),
}
eu_tropical_entry = {
"latitude": coord.latitude,
"longitude": coord.longitude,
"is_tropical_belt": coord.is_tropical_belt,
"post_2020_deforestation_pct": overrides.get("post_2020_deforestation_pct", 0.0),
"primary_or_peat_encroachment_score": overrides.get("primary_or_peat_encroachment_score", 10),
"polygon_traceability_completeness_pct": overrides.get("polygon_traceability_completeness_pct", 95.0),
"consecutive_eudr_breach_ticks": overrides.get("consecutive_eudr_breach_ticks", 0),
}
agroforestry_entry = {
"latitude": coord.latitude,
"longitude": coord.longitude,
"crop_species": crop_type.lower(),
"shade_tree_canopy_cover_pct": shade_pct,
"net_carbon_flux_tco2e_ha_yr": overrides["net_carbon_flux_tco2e_ha_yr"],
"multi_strata_sar_red_edge_score": overrides.get("multi_strata_sar_red_edge_score", 68),
"consecutive_net_source_ticks": overrides.get("consecutive_net_source_ticks", 0),
}
return {
"geo_coordinate": {
"key": key,
"latitude": coord.latitude,
"longitude": coord.longitude,
"radius_m": coord.radius_m,
"bbox": list(coord.to_bbox()),
"is_tropical_belt": coord.is_tropical_belt,
"queried_at_utc": datetime.now(timezone.utc).isoformat(),
"copernicus_stac": stac_meta,
"element84_cog": cog_meta,
},
"old_growth_forest": {
key: old_growth_entry,
"global_baseline": old_growth_entry,
},
"eu_carbon_tropical_compliance": {
key: eu_tropical_entry,
"global_baseline": eu_tropical_entry,
},
"agroforestry_cacao_coffee_carbon": {
key: agroforestry_entry,
"global_baseline": agroforestry_entry,
},
}
def main() -> None:
parser = argparse.ArgumentParser(
description="Query free Copernicus / Element84 STAC COGs and build JANUS geo-coordinate external_data."
)
parser.add_argument("--lat", type=float, required=True, help="WGS84 latitude in [-90.0, 90.0]")
parser.add_argument("--lon", type=float, required=True, help="WGS84 longitude in [-180.0, 180.0]")
parser.add_argument("--radius-m", type=float, default=500.0, help="Bounding-box radius in meters")
parser.add_argument("--symbol", type=str, default="", help="Optional ticker or asset key")
parser.add_argument(
"--crop",
type=str,
default="generic",
choices=["generic", "cacao", "coffee"],
help="Optional tropical agroforestry crop focus",
)
parser.add_argument("--shade-pct", type=float, default=42.0, help="Overstory shade-tree canopy cover percent")
parser.add_argument("--canopy-height-m", type=float, default=14.0, help="Mean overstory canopy height in meters")
parser.add_argument("--n-fertilizer", type=float, default=40.0, help="Synthetic N fertilizer (kg N / ha / yr)")
parser.add_argument("--no-live-stac", action="store_true", help="Skip live STAC HTTP queries")
parser.add_argument("--no-cogs", action="store_true", help="Skip Element84 COG windowed raster reads")
args = parser.parse_args()
coord = GeoCoordinate(
latitude=args.lat,
longitude=args.lon,
radius_m=args.radius_m,
label=args.symbol,
)
ext = build_geo_external_data(
coord=coord,
crop_type=args.crop,
sensor_overrides={
"shade_tree_canopy_cover_pct": args.shade_pct,
"canopy_height_m": args.canopy_height_m,
"synthetic_n_fertilizer_kg_ha_yr": args.n_fertilizer,
},
query_live_stac=not args.no_live_stac,
extract_cogs=not args.no_cogs,
)
print(json.dumps(ext, indent=2))
if name == "main":
main()