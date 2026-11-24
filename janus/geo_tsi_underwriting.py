"""
janus/geo_tsi_underwriting.py

Annual-aggregated Sentinel-2 surface solar irradiance (SSI) estimator for JANUS
solar-installation underwriting support.

Zero paid APIs, zero keys. Reuses upstream STAC/COG helpers from
`geo_probe_updated` and the (6, H, W) patch fetcher from `geo_vit_adapter`.

Outputs (per coordinate):
    total_solar_irradiance_score   [0-100], P50 clear-sky-normalised
    p50_ghi_kwh_m2_yr              annual all-sky GHI
    p90_ghi_kwh_m2_yr              conservative (1-sigma, one-sided 90%)
    capacity_factor_pct_p50
    capacity_factor_pct_p90
    specific_yield_kwh_kwp_yr_p50
    specific_yield_kwh_kwp_yr_p90
    kt_mean, kt_sigma, scene_count, seasonal_coverage

All values are mergeable into `build_geo_external_data()` via `sensor_overrides`.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from .geo_probe_updated import (
        ELEMENT84_STAC_SEARCH_URL,
        GeoCoordinate,
        _post_json,
    )
except ImportError:  # direct script execution
    from geo_probe_updated import (  # type: ignore
        ELEMENT84_STAC_SEARCH_URL,
        GeoCoordinate,
        _post_json,
    )

# Solar constant (W/m^2), Thuillier 2003 (the Sentinel-2 mission reference)
SOLAR_CONSTANT_W_M2 = 1361.0

# SCL class → cloud modification factor for GHI (empirical, mid-range).
# Derived from Heliosat/Meteosat literature and S2 SCL semantics.
SCL_TO_KT: dict[int, float] = {
    0: 0.00,   # no_data
    1: 0.00,   # saturated/defective
    2: 0.90,   # dark_area_pixels (topographic shade, but sun up)
    3: 0.60,   # cloud_shadows (transition)
    4: 0.95,   # vegetation
    5: 0.95,   # not_vegetated
    6: 0.95,   # water
    7: 0.90,   # unclassified
    8: 0.35,   # cloud_medium_probability
    9: 0.15,   # cloud_high_probability
    10: 0.75,  # thin_cirrus
    11: 0.85,  # snow
}

# Performance ratio (nameplate-independent) for modern utility PV.
# 0.80 = typical for mono-PERC or TOPCon at temperate latitude.
DEFAULT_PERFORMANCE_RATIO = 0.80

# Solar declination day-of-year formula (Cooper 1969)
def _declination_deg(day_of_year: int) -> float:
    return 23.45 * math.sin(
        math.radians(360.0 / 365.0 * (284 + day_of_year))
    )


def _sunset_hour_angle_rad(lat_deg: float, decl_deg: float) -> float:
    lat = math.radians(lat_deg)
    decl = math.radians(decl_deg)
    arg = -math.tan(lat) * math.tan(decl)
    return math.acos(max(-1.0, min(1.0, arg)))


def _eccentricity_correction(day_of_year: int) -> float:
    return 1.0 + 0.033 * math.cos(
        math.radians(360.0 * day_of_year / 365.0)
    )


def clear_sky_daily_ghi_wh_m2(
    lat_deg: float, day_of_year: int, clear_sky_transmittance: float = 0.75
) -> float:
    """
    Daily clear-sky surface GHI (Wh/m²/day) via the classic daily-insolation
    formula with a fixed broadband clear-sky transmittance (aerosol AOD ~0.15).
    """
    decl = _declination_deg(day_of_year)
    ws = _sunset_hour_angle_rad(lat_deg, decl)
    if not math.isfinite(ws) or ws <= 0.0:
        return 0.0
    lat = math.radians(lat_deg)
    decl_r = math.radians(decl)
    e0 = _eccentricity_correction(day_of_year)
    h0 = (24.0 * 3600.0 / math.pi) * SOLAR_CONSTANT_W_M2 * e0 * (
        math.cos(lat) * math.cos(decl_r) * math.sin(ws)
        + ws * math.sin(lat) * math.sin(decl_r)
    )
    return max(0.0, h0 * clear_sky_transmittance)


def annual_clear_sky_ghi_kwh_m2(lat_deg: float) -> float:
    """Annual clear-sky surface GHI (kWh/m²/yr) at a latitude."""
    return (
        sum(clear_sky_daily_ghi_wh_m2(lat_deg, d) for d in range(1, 366))
        / 1000.0
    )


def clear_sky_ghi_at_w_m2(
    lat_deg: float,
    lon_deg: float,
    utc_dt: datetime,
    clear_sky_transmittance: float = 0.75,
) -> float:
    """Instantaneous clear-sky surface GHI (W/m²) at a given UTC datetime."""
    doy = utc_dt.timetuple().tm_yday
    decl = math.radians(_declination_deg(doy))
    lat = math.radians(lat_deg)
    utc_hours = (
        utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    )
    hour_angle = math.radians((utc_hours - 12.0) * 15.0 + lon_deg)
    cos_z = (
        math.sin(lat) * math.sin(decl)
        + math.cos(lat) * math.cos(decl) * math.cos(hour_angle)
    )
    cos_z = max(0.0, min(1.0, cos_z))
    if cos_z <= 0.01:
        return 0.0
    air_mass = 1.0 / cos_z
    t = clear_sky_transmittance * math.exp(
        -0.15 * (air_mass - 1.0)
    )  # AOD ~0.15
    return SOLAR_CONSTANT_W_M2 * cos_z * t


def solar_zenith_deg(
    lat_deg: float, lon_deg: float, utc_dt: datetime
) -> float:
    """Solar zenith angle (degrees)."""
    doy = utc_dt.timetuple().tm_yday
    decl = math.radians(_declination_deg(doy))
    lat = math.radians(lat_deg)
    utc_hours = (
        utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    )
    hour_angle = math.radians((utc_hours - 12.0) * 15.0 + lon_deg)
    cos_z = (
        math.sin(lat) * math.sin(decl)
        + math.cos(lat) * math.cos(decl) * math.cos(hour_angle)
    )
    cos_z = max(-1.0, min(1.0, cos_z))
    return math.degrees(math.acos(cos_z))


# ---------------------------------------------------------------------------
# Per-scene Kt from SCL
# ---------------------------------------------------------------------------
def scene_kt_from_scl(scl_array: Any) -> tuple[float | None, float]:
    """
    Return (scene_mean_Kt, clear_fraction) from a raw SCL integer array.
    Returns (None, 0.0) if the scene has too few valid pixels.
    """
    import numpy as np

    if scl_array.size == 0:
        return None, 0.0
    valid = (scl_array != 0) & (scl_array != 1)
    n_valid = int(np.sum(valid))
    if n_valid < 4:
        return None, 0.0
    kt_per_pixel = np.zeros(scl_array.shape, dtype=np.float32)
    for cls, kt in SCL_TO_KT.items():
        kt_per_pixel[scl_array == cls] = kt
    kt_mean = float(np.mean(kt_per_pixel[valid]))
    # "Clear fraction" = SCL classes 2, 4, 5, 6, 7 (all clear-ish)
    clear_like = np.isin(scl_array, (2, 4, 5, 6, 7))
    clear_fraction = float(np.sum(clear_like)) / max(1.0, float(n_valid))
    return kt_mean, clear_fraction


def _parse_iso_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def fetch_scene_kt_sample(
    scene_feature: dict[str, Any],
    bbox_4326: tuple[float, float, float, float],
    lat_deg: float,
    lon_deg: float,
) -> dict[str, Any] | None:
    """
    Read the SCL window for one scene, compute scene-mean Kt, and attach the
    clear-sky GHI at acquisition time as the aggregation weight.
    """
    import numpy as np
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds

    assets = scene_feature.get("assets", {})
    if "scl" not in assets or "href" not in assets["scl"]:
        return None

    dt_str = scene_feature.get("properties", {}).get("datetime", "")
    if not dt_str:
        return None
    try:
        acq_dt = _parse_iso_dt(dt_str)
    except ValueError:
        return None

    try:
        with rasterio.Env(
            GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
            CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
        ):
            with rasterio.open(assets["scl"]["href"]) as ds:
                b = transform_bounds(
                    "EPSG:4326", ds.crs, *bbox_4326
                )
                w = (
                    from_bounds(*b, transform=ds.transform)
                    .round_offsets()
                    .round_lengths()
                )
                scl = ds.read(
                    1,
                    window=w,
                    out_shape=(64, 64),
                    resampling=Resampling.nearest,
                ).astype(np.int32)
    except Exception:
        return None

    kt, clear_frac = scene_kt_from_scl(scl)
    if kt is None:
        return None

    ghi_clear = clear_sky_ghi_at_w_m2(lat_deg, lon_deg, acq_dt)
    if ghi_clear <= 5.0:  # below horizon or grazing light: skip weight
        return None

    return {
        "datetime": acq_dt.isoformat(),
        "kt": kt,
        "ghi_clear_w_m2": ghi_clear,
        "cloud_cover": scene_feature.get("properties", {}).get(
            "eo:cloud_cover"
        ),
        "clear_fraction": round(clear_frac, 4),
    }


def sample_kt_across_year(
    coord: GeoCoordinate,
    lookback_days: int = 365,
    max_cloud_cover: float = 85.0,
    per_request_limit: int = 100,
    timeout_s: float = 15.0,
) -> list[dict[str, Any]]:
    """
    Query all low/mid-cloud scenes within the lookback window and compute
    (Kt, clear-sky weight) samples. Pages through STAC if needed.
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=max(30, int(lookback_days)))
    dt_range = (
        f"{start.strftime('%Y-%m-%dT%H:%M:%SZ')}/"
        f"{now.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    )
    bbox = list(coord.to_bbox())

    samples: list[dict[str, Any]] = []
    body: dict[str, Any] = {
        "bbox": bbox,
        "collections": ["sentinel-2-l2a"],
        "datetime": dt_range,
        "limit": per_request_limit,
        "query": {"eo:cloud_cover": {"lt": max_cloud_cover}},
    }

    try:
        page = _post_json(
            ELEMENT84_STAC_SEARCH_URL, body, timeout_s=timeout_s
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []

    features = list(page.get("features", []))
    # Follow the `next` link up to 3 pages (bounded, polite)
    for _ in range(2):
        next_link = next(
            (
                l.get("body")
                for l in page.get("links", [])
                if l.get("rel") == "next" and l.get("method", "POST") == "POST"
            ),
            None,
        )
        if not next_link:
            break
        try:
            page = _post_json(
                ELEMENT84_STAC_SEARCH_URL,
                next_link,
                timeout_s=timeout_s,
            )
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            break
        more = page.get("features", [])
        if not more:
            break
        features.extend(more)

    for feat in features:
        s = fetch_scene_kt_sample(
            feat, tuple(bbox), coord.latitude, coord.longitude
        )
        if s is not None:
            samples.append(s)

    return samples


# ---------------------------------------------------------------------------
# Annual aggregation + underwriting translation
# ---------------------------------------------------------------------------
def aggregate_annual_ghi(
    samples: list[dict[str, Any]], latitude: float
) -> dict[str, Any]:
    """
    Combine per-scene (Kt, ghi_clear) samples into annual all-sky GHI and
    P50/P90 confidence bands.

    Kt_annual    = Σ(Kt_i · GHI_clear_i) / Σ(GHI_clear_i)
    GHI_annual   = Kt_annual × annual_clear_sky_GHI(lat)
    P90_GtI      = (Kt_annual − 1.28 · σ_Kt) × annual_clear_sky_GHI(lat)
    """
    import numpy as np

    annual_clear = annual_clear_sky_ghi_kwh_m2(latitude)

    if not samples:
        return {
            "scene_count": 0,
            "kt_mean": None,
            "kt_sigma": None,
            "p50_ghi_kwh_m2_yr": None,
            "p90_ghi_kwh_m2_yr": None,
            "annual_clear_sky_ghi_kwh_m2_yr": round(annual_clear, 2),
            "seasonal_coverage": 0,
        }

    kt = np.array([s["kt"] for s in samples], dtype=np.float64)
    w = np.array(
        [s["ghi_clear_w_m2"] for s in samples], dtype=np.float64
    )
    total_w = float(w.sum())
    kt_weighted = float(np.sum(kt * w) / total_w) if total_w > 0 else 0.0

    # P90 Kt uses the lower bound: mean − 1.28·σ (one-sided 90%)
    kt_sigma = float(np.std(kt, ddof=1)) if kt.size > 1 else 0.05
    kt_p90 = max(0.0, kt_weighted - 1.28 * kt_sigma)

    p50 = kt_weighted * annual_clear
    p90 = kt_p90 * annual_clear

    # Seasonal coverage: number of distinct months sampled
    months = {_parse_iso_dt(s["datetime"]).month for s in samples}

    return {
        "scene_count": len(samples),
        "kt_mean": round(kt_weighted, 4),
        "kt_sigma": round(kt_sigma, 4),
        "p50_ghi_kwh_m2_yr": round(p50, 1),
        "p90_ghi_kwh_m2_yr": round(p90, 1),
        "annual_clear_sky_ghi_kwh_m2_yr": round(annual_clear, 1),
        "seasonal_coverage": len(months),
    }


def translate_to_underwriting(
    agg: dict[str, Any],
    performance_ratio: float = DEFAULT_PERFORMANCE_RATIO,
) -> dict[str, Any]:
    """Turn annual GHI into capacity factor and specific yield."""
    out: dict[str, Any] = {
        "performance_ratio": performance_ratio,
    }
    p50 = agg.get("p50_ghi_kwh_m2_yr")
    p90 = agg.get("p90_ghi_kwh_m2_yr")
    if p50 is None or p90 is None:
        return out

    # Mean irradiance (W/m^2) over the whole year (8760 h)
    mean_w_m2_p50 = p50 * 1000.0 / 8760.0
    mean_w_m2_p90 = p90 * 1000.0 / 8760.0

    # CF = mean_GtI / 1000 W/m^2 × PR
    cf_p50 = mean_w_m2_p50 / 1000.0 * performance_ratio
    cf_p90 = mean_w_m2_p90 / 1000.0 * performance_ratio

    out.update(
        {
            "capacity_factor_pct_p50": round(cf_p50 * 100.0, 2),
            "capacity_factor_pct_p90": round(cf_p90 * 100.0, 2),
            "specific_yield_kwh_kwp_yr_p50": round(cf_p50 * 8760.0, 1),
            "specific_yield_kwh_kwp_yr_p90": round(cf_p90 * 8760.0, 1),
        }
    )
    return out


def irradiance_score_100(agg: dict[str, Any]) -> int | None:
    """
    Bounded [0, 100] P50 score: fraction of clear-sky maximum actually
    received at the site. 100 = clear-sky everywhere; 0 = no data.
    """
    annual_clear = agg.get("annual_clear_sky_ghi_kwh_m2_yr")
    p50 = agg.get("p50_ghi_kwh_m2_yr")
    if not annual_clear or p50 is None or annual_clear <= 0:
        return None
    ratio = max(0.0, min(1.0, p50 / annual_clear))
    return int(round(ratio * 100.0))


# ---------------------------------------------------------------------------
# Top-level entrypoint
# ---------------------------------------------------------------------------
def build_tsi_underwriting(
    coord: GeoCoordinate,
    lookback_days: int = 365,
    max_cloud_cover: float = 85.0,
    performance_ratio: float = DEFAULT_PERFORMANCE_RATIO,
    fetch_data: bool = True,
) -> dict[str, Any]:
    """
    Full underwriting-ready TSI / SSI assessment for one coordinate.
    """
    now_utc = datetime.now(timezone.utc)
    out: dict[str, Any] = {
        "status": "skipped",
        "source": "geo_tsi_underwriting",
        "queried_at_utc": now_utc.isoformat(),
        "latitude": coord.latitude,
        "longitude": coord.longitude,
        "lookback_days": lookback_days,
        "sensor_overrides": {},
    }
    if not fetch_data:
        return out

    try:
        import numpy as np  # noqa: F401
        import rasterio  # noqa: F401
    except ImportError:
        out["status"] = "optional_deps_missing"
        return out

    samples = sample_kt_across_year(
        coord,
        lookback_days=lookback_days,
        max_cloud_cover=max_cloud_cover,
    )
    if not samples:
        out["status"] = "no_usable_scenes"
        return out

    agg = aggregate_annual_ghi(samples, coord.latitude)
    uw = translate_to_underwriting(agg, performance_ratio)
    score = irradiance_score_100(agg)

    out.update(
        {
            "status": "ok" if agg["scene_count"] >= 4 else "sparse_samples",
            "aggregate": agg,
            "underwriting": uw,
            "total_solar_irradiance_score": score,
        }
    )

    # Normalized overrides for build_geo_external_data(...)
    overrides: dict[str, Any] = {}
    if score is not None:
        overrides["total_solar_irradiance_score"] = score
    if "specific_yield_kwh_kwp_yr_p50" in uw:
        overrides["specific_yield_kwh_kwp_yr_p50"] = uw[
            "specific_yield_kwh_kwp_yr_p50"
        ]
    if "specific_yield_kwh_kwp_yr_p90" in uw:
        overrides["specific_yield_kwh_kwp_yr_p90"] = uw[
            "specific_yield_kwh_kwp_yr_p90"
        ]
    if "capacity_factor_pct_p50" in uw:
        overrides["capacity_factor_pct_p50"] = uw[
            "capacity_factor_pct_p50"
        ]
    out["sensor_overrides"] = overrides
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Annual SSI / TSI assessment for solar-installation underwriting "
            "from free Sentinel-2 data."
        )
    )
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--radius-m", type=float, default=500.0)
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=365,
        help="Sampling window; 365 is the underwriting default",
    )
    parser.add_argument(
        "--max-cloud-cover",
        type=float,
        default=85.0,
        help="Scene-level cloud-cover ceiling for sampling",
    )
    parser.add_argument(
        "--performance-ratio",
        type=float,
        default=DEFAULT_PERFORMANCE_RATIO,
        help="PV system performance ratio (0.75-0.85 typical)",
    )
    parser.add_argument("--symbol", type=str, default="")
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--no-fetch", action="store_true")
    args = parser.parse_args()

    coord = GeoCoordinate(
        latitude=args.lat,
        longitude=args.lon,
        radius_m=args.radius_m,
        label=args.symbol,
    )

    result = build_tsi_underwriting(
        coord,
        lookback_days=args.lookback_days,
        max_cloud_cover=args.max_cloud_cover,
        performance_ratio=args.performance_ratio,
        fetch_data=not args.no_fetch,
    )

    text = json.dumps(result, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


if __name__ == "__main__":
    main()