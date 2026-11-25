"""
janus/geo_district_underwriting.py

District-scale (5-50 km) agricultural commodity + compliance underwriter.

Reuses parcel-scale helpers; adds district-scale methane retrieval, crop-area
estimation, and a multi-pass variance test that detects real temporal change.

Key insight: the Sentinel-2 band-ratio detection floor is roughly constant in
absolute Q (~1,000-2,000 kg/h), NOT in emission density. So a distributed source
(rice paddy) becomes detectable at district scale because total Q grows linearly
with area while the floor stays fixed.

Sizing guidance:
  rice (0.125 kg/ha/h):  2,000 ha -> 9 months; 8,000 ha -> 3 weeks; 16,000 ha -> 1 pass
  point source > 2 t/h:  any size -> 1 pass
  point source ~ 500 kg/h: any size -> ~3 months

Reuses GeoCoordinate, _post_json, _dynamic_datetime_range from geo_probe_updated.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.error
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .geo_probe_updated import (
        ELEMENT84_STAC_SEARCH_URL,
        INVALID_SCL_CLASSES,
        GeoCoordinate,
        _dynamic_datetime_range,
        _post_json,
    )
except ImportError:
    from geo_probe_updated import (  # type: ignore
        ELEMENT84_STAC_SEARCH_URL,
        INVALID_SCL_CLASSES,
        GeoCoordinate,
        _dynamic_datetime_range,
        _post_json,
    )

# --- Physical constants -----------------------------------------------------
S2_PIXEL_M = 20.0
PIXEL_AREA_M2 = S2_PIXEL_M * S2_PIXEL_M
DEFAULT_DETECTION_THRESHOLD_KG_H = 2000.0
IME_FLUX_COEFF = 0.133
DEFAULT_WIND_SPEED_MS = 3.0
MIN_PLUME_PIXELS = 4
DEFAULT_OUT_SIDE = 512  # 10 km district at 20 m = 500 px; 512 is safe

# --- District sizing profiles ----------------------------------------------
DISTRICT_PROFILES: dict[str, dict[str, Any]] = {
    "rice": {
        "min_district_ha": 8000,
        "recommended_district_ha": 16000,
        "expected_methane_density_kg_ha_h": 0.125,
        "observables": ["crop_area", "rice_likelihood", "methane_anomaly", "methane_plume"],
    },
    "maize": {
        "min_district_ha": 500,
        "recommended_district_ha": 5000,
        "expected_methane_density_kg_ha_h": 0.0,
        "observables": ["crop_area", "yield_proxy"],
    },
    "wheat": {
        "min_district_ha": 500,
        "recommended_district_ha": 5000,
        "expected_methane_density_kg_ha_h": 0.0,
        "observables": ["crop_area", "yield_proxy"],
    },
    "soy": {
        "min_district_ha": 500,
        "recommended_district_ha": 5000,
        "expected_methane_density_kg_ha_h": 0.0,
        "observables": ["crop_area", "yield_proxy"],
    },
    "coffee": {
        "min_district_ha": 2000,
        "recommended_district_ha": 10000,
        "expected_methane_density_kg_ha_h": 0.0,
        "observables": ["crop_area", "shade_canopy"],
    },
    "cocoa": {
        "min_district_ha": 2000,
        "recommended_district_ha": 10000,
        "expected_methane_density_kg_ha_h": 0.0,
        "observables": ["crop_area", "shade_canopy"],
    },
}


# ---------------------------------------------------------------------------
# District AOI
# ---------------------------------------------------------------------------
@dataclass
class DistrictAOI:
    """District-scale AOI: center + radius, or polygon of (lon, lat) vertices."""

    center: GeoCoordinate
    polygon: list[tuple[float, float]] | None = None

    @property
    def area_ha(self) -> float:
        if self.polygon is not None:
            return _polygon_area_ha(self.polygon)
        return math.pi * (self.center.radius_m ** 2) / 10_000.0

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        if self.polygon is not None:
            lons = [p[0] for p in self.polygon]
            lats = [p[1] for p in self.polygon]
            return (min(lons), min(lats), max(lons), max(lats))
        return self.center.to_bbox()


def _polygon_area_ha(vertices: list[tuple[float, float]]) -> float:
    if len(vertices) < 3:
        return 0.0
    n = len(vertices)
    area_deg2 = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area_deg2 += x1 * y2 - x2 * y1
    area_deg2 = abs(area_deg2) / 2.0
    mean_lat = sum(p[1] for p in vertices) / n
    m2_per_deg2 = 111_320.0 ** 2 * math.cos(math.radians(mean_lat))
    return area_deg2 * m2_per_deg2 / 10_000.0


# ---------------------------------------------------------------------------
# District-scale band read
# ---------------------------------------------------------------------------
def _read_district_bands(
    scene_feature: dict[str, Any],
    bbox_4326: tuple[float, float, float, float],
    out_side: int = DEFAULT_OUT_SIDE,
) -> dict[str, Any] | None:
    """Read aligned district-scale windows for SWIR, NIR, RED, REDEDGE1, SCL."""
    import numpy as np
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds

    assets = scene_feature.get("assets", {})
    needed = ("swir16", "swir22", "nir", "red", "rededge1", "scl")
    if not all(k in assets and "href" in assets[k] for k in needed):
        return None

    side = max(64, min(1024, out_side))
    try:
        with rasterio.Env(
            GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
            CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
        ):
            def _band(key: str, is_mask: bool = False) -> Any:
                with rasterio.open(assets[key]["href"]) as ds:
                    b = transform_bounds("EPSG:4326", ds.crs, *bbox_4326)
                    w = (
                        from_bounds(*b, transform=ds.transform)
                        .round_offsets()
                        .round_lengths()
                    )
                    resamp = (
                        Resampling.nearest if is_mask else Resampling.bilinear
                    )
                    arr = ds.read(
                        1, window=w, out_shape=(side, side),
                        resampling=resamp,
                    )
                return arr.astype(np.int32) if is_mask else arr.astype(np.float32)

            return {
                "swir16": _band("swir16"),
                "swir22": _band("swir22"),
                "nir": _band("nir"),
                "red": _band("red"),
                "rededge1": _band("rededge1"),
                "scl": _band("scl", is_mask=True),
                "side": side,
            }
    except Exception:
        return None


def analyze_district_bands(
    bands: dict[str, Any],
    wind_speed_ms: float = DEFAULT_WIND_SPEED_MS,
    detection_threshold_kg_h: float = DEFAULT_DETECTION_THRESHOLD_KG_H,
) -> dict[str, Any]:
    """
    Compute district-mean methane anomaly, discrete plume detections, and
    crop-area proxies from one pass.
    """
    import numpy as np

    b11 = bands["swir16"]
    b12 = bands["swir22"]
    nir = bands["nir"]
    red = bands["red"]
    re1 = bands["rededge1"]
    scl = bands["scl"]
    eps = 1e-6

    clear = ~np.isin(scl, INVALID_SCL_CLASSES)
    valid = clear & (b11 > 0.05) & (b12 > 0.02) & (nir > 0.05)
    n_valid = int(np.sum(valid))
    if n_valid < 100:
        return {"status": "insufficient_valid_pixels", "n_valid": n_valid}

    # Methane proxy
    ratio = b12 / (b11 + eps)
    valid_ratio = ratio[valid]
    background = float(np.median(valid_ratio))
    mad = float(np.median(np.abs(valid_ratio - background))) + 1e-9
    dr = ratio - background

    # Discrete plume (point source: landfill, gas leak)
    plume_mask = valid & (dr > max(0.01, 4.0 * mad))
    n_plume = int(np.sum(plume_mask))
    plume_q = None
    if n_plume >= MIN_PLUME_PIXELS:
        mean_dr_plume = float(np.mean(dr[plume_mask]))
        plume_area_m2 = n_plume * PIXEL_AREA_M2
        plume_q = IME_FLUX_COEFF * mean_dr_plume * plume_area_m2 * wind_speed_ms

    # Distributed district anomaly
    district_mean_dr = float(np.mean(dr[valid]))
    district_std_dr = float(np.std(dr[valid]))
    district_area_ha = n_valid * PIXEL_AREA_M2 / 10_000.0
    district_total_ime = district_mean_dr * n_valid * PIXEL_AREA_M2
    district_total_q = IME_FLUX_COEFF * district_total_ime * wind_speed_ms

    # Crop proxies
    ndvi = (nir - red) / (nir + red + eps)
    ndwi = (nir - b11) / (nir + b11 + eps)
    ndre = (nir - re1) / (nir + re1 + eps)

    cropland = valid & (ndvi > 0.3) & (ndvi < 0.85) & (ndwi < 0.3)
    rice_like = cropland & ((ndwi > 0.1) | ((ndvi > 0.5) & (b11 > 0.15)))
    shade = valid & (ndvi >= 0.65) & (ndre >= 0.32)

    return {
        "status": "ok",
        "n_valid_pixels": n_valid,
        "district_area_ha": round(district_area_ha, 1),
        "district_mean_dr": round(district_mean_dr, 6),
        "district_std_dr": round(district_std_dr, 6),
        "district_total_q_kg_h": round(district_total_q, 1),
        "plume_detected": n_plume >= MIN_PLUME_PIXELS,
        "plume_pixels": n_plume,
        "plume_q_kg_h": round(plume_q, 1) if plume_q is not None else None,
        "plume_above_threshold": (
            plume_q is not None and plume_q >= detection_threshold_kg_h
        ),
        "cropland_ha": round(int(np.sum(cropland)) * PIXEL_AREA_M2 / 10_000.0, 1),
        "rice_likelihood_ha": round(int(np.sum(rice_like)) * PIXEL_AREA_M2 / 10_000.0, 1),
        "shade_canopy_ha": round(int(np.sum(shade)) * PIXEL_AREA_M2 / 10_000.0, 1),
        "ndvi_mean": round(float(np.mean(ndvi[valid])), 4),
    }


# ---------------------------------------------------------------------------
# Coverage + record
# ---------------------------------------------------------------------------
def _coverage_fraction(
    feature_bbox: tuple[float, float, float, float],
    district_bbox: tuple[float, float, float, float],
) -> float:
    """Fraction of district bbox covered by a scene bbox."""
    lo = max(feature_bbox[0], district_bbox[0])
    la = max(feature_bbox[1], district_bbox[1])
    hi = min(feature_bbox[2], district_bbox[2])
    ha = min(feature_bbox[3], district_bbox[3])
    if hi <= lo or ha <= la:
        return 0.0
    inter = (hi - lo) * (ha - la)
    dist = (
        (district_bbox[2] - district_bbox[0])
        * (district_bbox[3] - district_bbox[1])
    )
    return inter / dist if dist > 0 else 0.0


def _feature_bbox(feature: dict[str, Any]) -> tuple[float, float, float, float] | None:
    b = feature.get("bbox")
    if b and len(b) >= 4:
        return (b[0], b[1], b[2], b[3])
    geom = feature.get("geometry", {})
    coords = geom.get("coordinates")
    if not coords:
        return None
    try:
        if geom.get("type") == "Polygon":
            flat = [pt for ring in coords for pt in ring]
        else:  # MultiPolygon
            flat = [pt for poly in coords for ring in poly for pt in ring]
        lons = [p[0] for p in flat]
        lats = [p[1] for p in flat]
        return (min(lons), min(lats), max(lons), max(lats))
    except (IndexError, TypeError):
        return None


def record_district_passes(
    district: DistrictAOI,
    commodity: str = "rice",
    lookback_days: int = 90,
    max_cloud_cover: float = 30.0,
    min_coverage: float = 0.5,
    wind_speed_ms: float = DEFAULT_WIND_SPEED_MS,
    detection_threshold_kg_h: float = DEFAULT_DETECTION_THRESHOLD_KG_H,
    out_side: int = DEFAULT_OUT_SIDE,
) -> list[dict[str, Any]]:
    """
    Query Sentinel-2 over the district and emit one record per usable pass.

    Deduplicates by (MGRS tile, acquisition date) so overlapping tiles do not
    double-count the same pass.
    """
    dt_range = _dynamic_datetime_range(lookback_days=lookback_days)
    district_bbox = district.bbox

    try:
        page = _post_json(
            ELEMENT84_STAC_SEARCH_URL,
            {
                "bbox": list(district_bbox),
                "collections": ["sentinel-2-l2a"],
                "datetime": dt_range,
                "limit": 100,
                "query": {"eo:cloud_cover": {"lt": max_cloud_cover}},
            },
            timeout_s=25.0,
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []

    seen: set[tuple[str, str]] = set()
    records: list[dict[str, Any]] = []
    for feat in page.get("features", []):
        fb = _feature_bbox(feat)
        if fb is None:
            continue
        cov = _coverage_fraction(fb, district_bbox)
        if cov < min_coverage:
            continue
        dt = feat.get("properties", {}).get("datetime", "")
        tile = feat.get("properties", {}).get("grid:code", feat.get("id", ""))
        key = (tile, dt)
        if key in seen:
            continue
        seen.add(key)

        bands = _read_district_bands(feat, district_bbox, out_side=out_side)
        if bands is None:
            records.append({
                "datetime": dt,
                "status": "band_read_failed",
                "coverage_fraction": round(cov, 3),
            })
            continue

        analysis = analyze_district_bands(
            bands,
            wind_speed_ms=wind_speed_ms,
            detection_threshold_kg_h=detection_threshold_kg_h,
        )
        analysis["datetime"] = dt
        analysis["scene_id"] = feat.get("id", "")
        analysis["cloud_cover"] = feat.get("properties", {}).get("eo:cloud_cover")
        analysis["coverage_fraction"] = round(cov, 3)
        records.append(analysis)

    records.sort(key=lambda r: r["datetime"])
    return records


# ---------------------------------------------------------------------------
# Aggregation + variance test
# ---------------------------------------------------------------------------
def _month_key(iso: str) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m")


def _quarter_key(iso: str) -> str:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}-Q{q}"


def _wilson_hilferty_chi2(df: int, z: float = 1.645) -> float:
    """Approximate chi-square quantile for the given df and normal z-score."""
    if df <= 0:
        return 0.0
    term = 1.0 - 2.0 / (9.0 * df) + z * math.sqrt(2.0 / (9.0 * df))
    return df * (max(0.0, term) ** 3)


def variance_test(records: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Chi-square test: is the observed variance of district-mean dR across
    passes larger than expected from within-pass sensor noise?

    If yes, there is real temporal variability (source is not constant).
    """
    import numpy as np

    valid = [r for r in records if r.get("status") == "ok"]
    n = len(valid)
    if n < 4:
        return {
            "status": "insufficient_passes",
            "n_passes": n,
            "interpretation": "need >= 4 usable passes for the test",
        }

    means = np.array([r["district_mean_dr"] for r in valid], dtype=np.float64)
    stds = np.array([r["district_std_dr"] for r in valid], dtype=np.float64)
    n_pix = np.array([r["n_valid_pixels"] for r in valid], dtype=np.float64)

    sigma_means = stds / np.sqrt(n_pix)
    expected_var = float(np.mean(sigma_means ** 2))
    observed_var = float(np.var(means, ddof=1))

    if expected_var <= 0.0:
        return {"status": "degenerate_expected_var", "n_passes": n}

    chi2 = (n - 1) * observed_var / expected_var
    df = n - 1
    chi2_crit = _wilson_hilferty_chi2(df, z=1.645)  # 95% one-sided

    return {
        "status": "ok",
        "n_passes": n,
        "observed_var": round(observed_var, 10),
        "expected_var_from_noise": round(expected_var, 10),
        "chi2_statistic": round(chi2, 3),
        "chi2_critical_95pct": round(chi2_crit, 3),
        "variance_detected": chi2 > chi2_crit,
        "interpretation": (
            "real temporal variability detected"
            if chi2 > chi2_crit
            else "consistent with constant source + sensor noise"
        ),
    }


def aggregate_district_records(
    records: list[dict[str, Any]],
    detection_threshold_kg_h: float = DEFAULT_DETECTION_THRESHOLD_KG_H,
) -> dict[str, Any]:
    """Monthly, quarterly, annual aggregation plus the variance test."""
    ok = [r for r in records if r.get("status") == "ok"]
    if not ok:
        return {"status": "no_usable_passes", "variance_test": variance_test(records)}

    monthly: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in ok:
        monthly[_month_key(r["datetime"])].append(r)

    monthly_rows: list[dict[str, Any]] = []
    for m in sorted(monthly):
        recs = monthly[m]
        q_vals = [float(r["district_total_q_kg_h"]) for r in recs]
        plume_q = [
            float(r["plume_q_kg_h"]) for r in recs
            if r.get("plume_q_kg_h") is not None
        ]
        monthly_rows.append({
            "month": m,
            "passes": len(recs),
            "mean_district_q_kg_h": round(sum(q_vals) / len(q_vals), 1),
            "max_district_q_kg_h": round(max(q_vals), 1),
            "plume_detections": sum(1 for r in recs if r.get("plume_detected")),
            "max_plume_q_kg_h": round(max(plume_q), 1) if plume_q else 0.0,
            "mean_cropland_ha": round(
                sum(r["cropland_ha"] for r in recs) / len(recs), 1
            ),
            "mean_rice_likelihood_ha": round(
                sum(r["rice_likelihood_ha"] for r in recs) / len(recs), 1
            ),
            "mean_shade_canopy_ha": round(
                sum(r["shade_canopy_ha"] for r in recs) / len(recs), 1
            ),
            "mean_ndvi": round(
                sum(r["ndvi_mean"] for r in recs) / len(recs), 4
            ),
        })

    # Divergence from same-month prior-year baseline
    baseline: dict[int, list[float]] = defaultdict(list)
    for row in monthly_rows:
        m_num = int(row["month"].split("-")[1])
        baseline[m_num].append(row["mean_district_q_kg_h"])
    baseline_mean = {m: sum(v) / len(v) for m, v in baseline.items() if v}

    for row in monthly_rows:
        m_num = int(row["month"].split("-")[1])
        base = baseline_mean.get(m_num)
        row["prior_mean_district_q_kg_h"] = round(base, 1) if base else None
        if base and base > 0:
            row["divergence_from_monthly_mean"] = round(
                (row["mean_district_q_kg_h"] - base) / base, 3
            )
        else:
            row["divergence_from_monthly_mean"] = None

    # Quarterly
    q_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in ok:
        q_buckets[_quarter_key(r["datetime"])].append(r)
    quarterly_rows: list[dict[str, Any]] = []
    for q in sorted(q_buckets):
        recs = q_buckets[q]
        qv = [float(r["district_total_q_kg_h"]) for r in recs]
        quarterly_rows.append({
            "quarter": q,
            "passes": len(recs),
            "mean_district_q_kg_h": round(sum(qv) / len(qv), 1),
            "plume_detections": sum(1 for r in recs if r.get("plume_detected")),
        })

    # Annual
    a_buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for r in ok:
        y = datetime.fromisoformat(r["datetime"].replace("Z", "+00:00")).year
        a_buckets[y].append(r)
    annual_rows: list[dict[str, Any]] = []
    for y in sorted(a_buckets):
        recs = a_buckets[y]
        qv = [float(r["district_total_q_kg_h"]) for r in recs]
        annual_rows.append({
            "year": y,
            "passes": len(recs),
            "mean_district_q_kg_h": round(sum(qv) / len(qv), 1),
            "plume_detections": sum(1 for r in recs if r.get("plume_detected")),
        })

    return {
        "status": "ok",
        "detection_threshold_kg_h": detection_threshold_kg_h,
        "total_passes": len(ok),
        "total_plume_detections": sum(1 for r in ok if r.get("plume_detected")),
        "monthly": monthly_rows,
        "quarterly": quarterly_rows,
        "annual": annual_rows,
        "variance_test": variance_test(records),
    }


# ---------------------------------------------------------------------------
# Compliance flags
# ---------------------------------------------------------------------------
def compliance_flags(
    agg: dict[str, Any],
    commodity: str,
    profile: dict[str, Any],
    detection_threshold_kg_h: float = DEFAULT_DETECTION_THRESHOLD_KG_H,
) -> list[str]:
    flags: list[str] = []

    # 1. Discrete plume detections (any commodity)
    det = agg.get("total_plume_detections", 0)
    if det >= 2:
        flags.append("PLUME_REPEAT: multiple discrete plumes detected")
    elif det == 1:
        flags.append("PLUME_SINGLE: one discrete plume detected")

    # 2. Distributed methane intensity (rice only)
    if profile.get("expected_methane_density_kg_ha_h", 0.0) > 0:
        monthly_q = [
            m["mean_district_q_kg_h"] for m in agg.get("monthly", [])
        ]
        if monthly_q:
            mx = max(monthly_q)
            if mx >= 2.0 * detection_threshold_kg_h:
                flags.append(
                    f"METHANE_HIGH: district Q peak {mx:.0f} kg/h "
                    f">= {2*detection_threshold_kg_h:.0f}"
                )
            elif mx >= detection_threshold_kg_h:
                flags.append(
                    f"METHANE_ELEVATED: district Q peak {mx:.0f} kg/h "
                    f">= {detection_threshold_kg_h:.0f}"
                )

    # 3. Variance test
    vt = agg.get("variance_test", {})
    if vt.get("variance_detected"):
        flags.append(
            f"VARIANCE_DETECTED: chi2={vt['chi2_statistic']} > "
            f"crit={vt['chi2_critical_95pct']}"
        )

    # 4. EUDR-style deforestation (needs baseline; flag placeholder)
    monthly = agg.get("monthly", [])
    if monthly:
        ndvi_vals = [m["mean_ndvi"] for m in monthly if m.get("mean_ndvi") is not None]
        if ndvi_vals:
            if max(ndvi_vals) > 0.65 and min(ndvi_vals) < 0.35:
                flags.append(
                    "EUDR_DEFORESTATION: NDVI crossed forest/non-forest threshold"
                )

    return flags


def district_decision(flags: list[str], commodity: str) -> str:
    if any(f.startswith("PLUME_REPEAT") for f in flags):
        return "NON_COMPLIANT"
    if any(f.startswith("METHANE_HIGH") for f in flags):
        return "NON_COMPLIANT"
    if any(f.startswith(("EUDR_DEFORESTATION", "METHANE_ELEVATED")) for f in flags):
        return "CONDITIONAL"
    if any(f.startswith("VARIANCE_DETECTED") for f in flags):
        return "CONDITIONAL"
    if any(f.startswith("PLUME_SINGLE") for f in flags):
        return "CONDITIONAL"
    return "COMPLIANT" if flags is not None else "INSUFFICIENT_DATA"


# ---------------------------------------------------------------------------
# Top-level entrypoint
# ---------------------------------------------------------------------------
def build_district_underwriting(
    district: DistrictAOI,
    commodity: str = "rice",
    lookback_days: int = 90,
    max_cloud_cover: float = 30.0,
    min_coverage: float = 0.5,
    wind_speed_ms: float = DEFAULT_WIND_SPEED_MS,
    detection_threshold_kg_h: float = DEFAULT_DETECTION_THRESHOLD_KG_H,
    fetch_data: bool = True,
) -> dict[str, Any]:
    """Full district underwriting assessment for one commodity."""
    now_utc = datetime.now(timezone.utc)
    profile = DISTRICT_PROFILES.get(commodity, DISTRICT_PROFILES["rice"])

    out: dict[str, Any] = {
        "status": "skipped",
        "source": "geo_district_underwriting",
        "queried_at_utc": now_utc.isoformat(),
        "commodity": commodity,
        "district_area_ha": round(district.area_ha, 1),
        "min_district_ha_recommended": profile["min_district_ha"],
        "lookback_days": lookback_days,
        "sensor_overrides": {},
    }

    if district.area_ha < profile["min_district_ha"]:
        out["status"] = "district_too_small_for_commodity"
        out["note"] = (
            f"District {district.area_ha:.0f} ha < {profile['min_district_ha']} ha "
            f"recommended for {commodity}; detection floor may be unreachable."
        )
        return out

    if not fetch_data:
        out["status"] = "skipped_by_flag"
        return out

    try:
        import numpy as np  # noqa: F401
        import rasterio  # noqa: F401
    except ImportError:
        out["status"] = "optional_deps_missing"
        return out

    records = record_district_passes(
        district,
        commodity=commodity,
        lookback_days=lookback_days,
        max_cloud_cover=max_cloud_cover,
        min_coverage=min_coverage,
        wind_speed_ms=wind_speed_ms,
        detection_threshold_kg_h=detection_threshold_kg_h,
    )
    if not records:
        out["status"] = "no_passes"
        return out

    agg = aggregate_district_records(
        records, detection_threshold_kg_h=detection_threshold_kg_h
    )
    flags = compliance_flags(
        agg, commodity, profile,
        detection_threshold_kg_h=detection_threshold_kg_h,
    )
    decision = district_decision(flags, commodity)

    out.update({
        "status": "ok" if agg.get("status") == "ok" else agg.get("status"),
        "record_count": len(records),
        "aggregate": agg,
        "compliance_flags": flags,
        "underwriting_decision": decision,
    })

    # Normalized overrides for build_geo_external_data(...)
    overrides: dict[str, Any] = {
        "district_area_ha": round(district.area_ha, 1),
        "district_compliance_decision": decision,
    }
    if agg.get("monthly"):
        last = agg["monthly"][-1]
        overrides["district_last_month_q_kg_h"] = last["mean_district_q_kg_h"]
        overrides["district_last_month_cropland_ha"] = last["mean_cropland_ha"]
        overrides["district_last_month_ndvi"] = last["mean_ndvi"]
        if commodity == "rice":
            overrides["district_last_month_rice_likelihood_ha"] = last[
                "mean_rice_likelihood_ha"
            ]
        if commodity in ("coffee", "cocoa"):
            overrides["district_last_month_shade_canopy_ha"] = last[
                "mean_shade_canopy_ha"
            ]
    vt = agg.get("variance_test", {})
    if vt.get("status") == "ok":
        overrides["district_variance_detected"] = vt["variance_detected"]
    out["sensor_overrides"] = overrides
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _cmd_record(args: argparse.Namespace) -> None:
    center = GeoCoordinate(
        latitude=args.lat, longitude=args.lon, radius_m=args.radius_m
    )
    district = DistrictAOI(center=center)
    records = record_district_passes(
        district,
        commodity=args.commodity,
        lookback_days=args.lookback_days,
        max_cloud_cover=args.max_cloud_cover,
        wind_speed_ms=args.wind_speed,
        detection_threshold_kg_h=args.threshold,
    )
    text = "\n".join(json.dumps(r, default=str) for r in records)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


def _cmd_underwrite(args: argparse.Namespace) -> None:
    path = Path(args.input)
    if not path.exists():
        raise SystemExit(f"Pass log not found: {path}")
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    agg = aggregate_district_records(
        records, detection_threshold_kg_h=args.threshold
    )
    profile = DISTRICT_PROFILES.get(
        args.commodity, DISTRICT_PROFILES["rice"]
    )
    flags = compliance_flags(
        agg, args.commodity, profile, detection_threshold_kg_h=args.threshold
    )
    payload = {
        "commodity": args.commodity,
        "aggregate": agg,
        "compliance_flags": flags,
        "underwriting_decision": district_decision(flags, args.commodity),
    }
    text = json.dumps(payload, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "District-scale (5-50 km) agricultural commodity + compliance "
            "underwriter. Detects distributed methane (rice), point-source "
            "plumes (landfill, gas leak), crop area, and deforestation."
        )
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record", help="Record one line per Sentinel-2 pass")
    r.add_argument("--lat", type=float, required=True)
    r.add_argument("--lon", type=float, required=True)
    r.add_argument(
        "--radius-m", type=float, default=5000.0,
        help="District radius (m); 5000 = ~7,850 ha",
    )
    r.add_argument(
        "--commodity", type=str, default="rice",
        choices=list(DISTRICT_PROFILES),
    )
    r.add_argument("--lookback-days", type=int, default=90)
    r.add_argument("--max-cloud-cover", type=float, default=30.0)
    r.add_argument("--wind-speed", type=float, default=DEFAULT_WIND_SPEED_MS)
    r.add_argument(
        "--threshold", type=float, default=DEFAULT_DETECTION_THRESHOLD_KG_H
    )
    r.add_argument("--output", type=str, default=None, help="JSONL pass log")
    r.set_defaults(func=_cmd_record)

    u = sub.add_parser(
        "underwrite",
        help="Aggregate a pass log to monthly/quarterly/annual with variance test",
    )
    u.add_argument("--input", type=str, required=True)
    u.add_argument(
        "--commodity", type=str, default="rice",
        choices=list(DISTRICT_PROFILES),
    )
    u.add_argument(
        "--threshold", type=float, default=DEFAULT_DETECTION_THRESHOLD_KG_H
    )
    u.add_argument("--output", type=str, default=None)
    u.set_defaults(func=_cmd_underwrite)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()