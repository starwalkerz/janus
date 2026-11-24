"""
janus/geo_agri_underwriting.py

Annual rainfall, key-crop harvest estimates, and rainfall-pattern divergence
for JANUS underwriting.

Zero paid APIs. Sentinel-native where possible; free keyless reanalysis fallback
(NASA POWER / Open-Meteo ERA5) when Sentinel-1 soil moisture is unavailable.

Outputs (per coordinate):
    annual_rainfall_mm
    rainfall_seasonality_divergence_index  (CV of monthly precipitation)
    monthly_rainfall_mm                    (list of 12)
    harvest_estimates_t_ha: {maize, wheat, rice, soy, coffee, cocoa}
    underwriting_flags: {water_stress, yield_confidence, ...}

All values mergeable into build_geo_external_data() via sensor_overrides.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    from .geo_probe_updated import (
        GeoCoordinate,
        _post_json,
        _dynamic_datetime_range,
    )
except ImportError:
    from geo_probe_updated import (  # type: ignore
        GeoCoordinate,
        _post_json,
        _dynamic_datetime_range,
    )

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Literature-ballpark yield coefficients: yield_t_ha = a + b * cumulative_ndvi
# cumulative_ndvi is the season integral of NDVI (unitless, range ~0–150)
CROP_YIELD_MODELS: dict[str, dict[str, float]] = {
    "maize":  {"a": 0.8, "b": 0.085, "peak_ndvi_min": 0.55, "peak_ndvi_max": 0.85},
    "wheat":  {"a": 0.5, "b": 0.070, "peak_ndvi_min": 0.50, "peak_ndvi_max": 0.80},
    "rice":   {"a": 1.2, "b": 0.075, "peak_ndvi_min": 0.60, "peak_ndvi_max": 0.85},
    "soy":    {"a": 0.4, "b": 0.055, "peak_ndvi_min": 0.45, "peak_ndvi_max": 0.75},
    "coffee": {"a": 0.2, "b": 0.035, "peak_ndvi_min": 0.55, "peak_ndvi_max": 0.80},
    "cocoa":  {"a": 0.1, "b": 0.030, "peak_ndvi_min": 0.55, "peak_ndvi_max": 0.80},
}

# Per-crop growing-season month windows (northern-hemisphere default; adjustable)
DEFAULT_SEASON_MONTHS: dict[str, tuple[int, int]] = {
    "maize": (4, 9), "wheat": (3, 7), "rice": (5, 9),
    "soy": (5, 9), "coffee": (1, 12), "cocoa": (1, 12),
}


# ---------------------------------------------------------------------------
# 1. Free keyless precipitation (NASA POWER primary, Open-Meteo fallback)
# ---------------------------------------------------------------------------
def fetch_nasa_power_daily_precip(
    lat: float, lon: float, start_date: str, end_date: str, timeout_s: float = 15.0
) -> dict[str, float] | None:
    """Return {YYYYMMDD: mm/day} from NASA POWER (no API key required)."""
    params = urllib.parse.urlencode({
        "parameters": "PRECTOTCORR",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date.replace("-", ""),
        "end": end_date.replace("-", ""),
        "format": "JSON",
    })
    url = f"{NASA_POWER_URL}?{params}"
    try:
        with urllib.request.urlopen(url, timeout=timeout_s) as r:
            raw = json.loads(r.read().decode("utf-8"))
        series = raw.get("properties", {}).get("parameter", {}).get("PRECTOTCORR", {})
        return {k: float(v) for k, v in series.items()}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None


def fetch_open_meteo_daily_precip(
    lat: float, lon: float, start_date: str, end_date: str, timeout_s: float = 15.0
) -> dict[str, float] | None:
    """Fallback: Open-Meteo ERA5 daily precipitation, no key."""
    params = urllib.parse.urlencode({
        "latitude": lat, "longitude": lon,
        "start_date": start_date, "end_date": end_date,
        "daily": "precipitation_sum",
        "timezone": "UTC",
    })
    try:
        with urllib.request.urlopen(f"{OPEN_METEO_ARCHIVE_URL}?{params}", timeout=timeout_s) as r:
            raw = json.loads(r.read().decode("utf-8"))
        times = raw.get("daily", {}).get("time", [])
        vals = raw.get("daily", {}).get("precipitation_sum", [])
        return {t.replace("-", ""): (float(v) if v is not None else 0.0) for t, v in zip(times, vals)}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None


def monthly_rainfall_from_daily(daily: dict[str, float]) -> list[float]:
    """Aggregate a {YYYYMMDD: mm} dict into 12 monthly totals (mm)."""
    monthly = [0.0] * 12
    for ymd, mm in daily.items():
        if len(ymd) >= 6:
            month = int(ymd[4:6])
            if 1 <= month <= 12:
                monthly[month - 1] += mm
    return [round(v, 1) for v in monthly]


def annual_and_seasonality(monthly_mm: list[float]) -> dict[str, Any]:
    """Annual total and coefficient-of-variation divergence index."""
    total = sum(monthly_mm)
    if total <= 0:
        return {"annual_rainfall_mm": 0.0, "divergence_index": None, "cv": None}
    mean_month = total / 12.0
    var = sum((m - mean_month) ** 2 for m in monthly_mm) / 12.0
    sd = math.sqrt(var)
    cv = sd / mean_month if mean_month > 0 else None
    return {
        "annual_rainfall_mm": round(total, 1),
        "divergence_index": round(cv, 3) if cv is not None else None,
        "cv": round(cv, 3) if cv is not None else None,
    }


# ---------------------------------------------------------------------------
# 2. Sentinel-2 NDVI yield estimation
# ---------------------------------------------------------------------------
def compute_ndvi_series(
    coord: GeoCoordinate,
    lookback_days: int = 365,
    max_cloud_cover: float = 40.0,
) -> list[dict[str, Any]]:
    """
    Fetch Sentinel-2 scenes over the lookback window, read the NDVI patch mean
    for each, and return [{datetime, ndvi_mean}] sorted ascending.
    """
    try:
        import numpy as np
        import rasterio  # noqa: F401
    except ImportError:
        return []
    try:
        from .geo_vit_adapter import fetch_six_band_patch, BAND_KEYS
    except ImportError:
        from geo_vit_adapter import fetch_six_band_patch, BAND_KEYS  # type: ignore

    patch = fetch_six_band_patch(
        coord, lookback_days=lookback_days, max_cloud_cover=max_cloud_cover
    )
    if patch.get("status") != "ok":
        return []

    tensor = patch["tensor"]
    clear = patch["clear_mask"]
    import numpy as np
    red = tensor[BAND_KEYS.index("red")]
    nir = tensor[BAND_KEYS.index("nir")]
    eps = 1e-6
    ndvi = (nir - red) / (nir + red + eps)
    ndvi_mean = float(np.nanmean(np.where(clear, ndvi, np.nan)))
    return [{
        "datetime": patch["datetime"],
        "ndvi_mean": round(ndvi_mean, 4),
    }]


def estimate_yields_from_ndvi(
    ndvi_series: list[dict[str, Any]],
    crop: str,
    season_months: tuple[int, int] | None = None,
) -> dict[str, Any]:
    """
    Ballpark yield_t_ha from a single NDVI sample using the literature
    coefficient for `crop`. With only one sample, we treat it as a peak-season
    proxy and apply the peak-NDVI branch of the model.
    """
    if not ndvi_series:
        return {"status": "no_ndvi"}
    model = CROP_YIELD_MODELS.get(crop)
    if model is None:
        return {"status": f"unknown_crop:{crop}"}

    ndvi = ndvi_series[0]["ndvi_mean"]
    peak_min, peak_max = model["peak_ndvi_min"], model["peak_ndvi_max"]
    # Convert peak NDVI to an approximate cumulative-NDVI equivalent
    # (season length ~ 120 days, triangular profile -> integral ≈ 60 * peak)
    cum_ndvi_equiv = 60.0 * max(0.0, ndvi)
    yield_t_ha = model["a"] + model["b"] * cum_ndvi_equiv
    confidence = "high" if peak_min <= ndvi <= peak_max else "low"
    return {
        "crop": crop,
        "peak_ndvi": ndvi,
        "cumulative_ndvi_equiv": round(cum_ndvi_equiv, 1),
        "yield_t_ha": round(max(0.0, yield_t_ha), 2),
        "confidence": confidence,
        "status": "ok",
    }


# ---------------------------------------------------------------------------
# 3. Top-level aggregator
# ---------------------------------------------------------------------------
def build_agri_underwriting(
    coord: GeoCoordinate,
    crops: tuple[str, ...] = ("maize", "wheat", "rice", "soy", "coffee", "cocoa"),
    lookback_days: int = 365,
    use_sentinel_rainfall: bool = False,  # SM2RAIN path is optional/heavy
    max_cloud_cover: float = 40.0,
) -> dict[str, Any]:
    """
    Return annual rainfall, monthly pattern divergence, and ballpark yields.
    """
    now = datetime.now(timezone.utc)
    end_date = now.strftime("%Y-%m-%d")
    start_date = (now - timedelta(days=max(365, lookback_days))).strftime("%Y-%m-%d")

    out: dict[str, Any] = {
        "status": "ok",
        "source": "geo_agri_underwriting",
        "queried_at_utc": now.isoformat(),
        "latitude": coord.latitude,
        "longitude": coord.longitude,
        "crops": list(crops),
        "sensor_overrides": {},
    }

    # --- Rainfall ---------------------------------------------------------
    daily = fetch_nasa_power_daily_precip(
        coord.latitude, coord.longitude, start_date, end_date
    )
    rain_source = "nasa_power"
    if not daily:
        daily = fetch_open_meteo_daily_precip(
            coord.latitude, coord.longitude, start_date, end_date
        )
        rain_source = "open_meteo_era5"

    if daily:
        monthly = monthly_rainfall_from_daily(daily)
        agg = annual_and_seasonality(monthly)
        out["rainfall"] = {
            "source": rain_source,
            "annual_rainfall_mm": agg["annual_rainfall_mm"],
            "monthly_rainfall_mm": monthly,
            "rainfall_seasonality_divergence_index": agg["divergence_index"],
        }
        out["sensor_overrides"]["annual_rainfall_mm"] = agg["annual_rainfall_mm"]
        out["sensor_overrides"]["rainfall_seasonality_divergence_index"] = (
            agg["divergence_index"]
        )
    else:
        out["rainfall"] = {"status": "no_precip_data"}

    # --- Crop yields (Sentinel-2 NDVI) ------------------------------------
    ndvi = compute_ndvi_series(
        coord, lookback_days=lookback_days, max_cloud_cover=max_cloud_cover
    )
    if ndvi:
        out["ndvi_scene"] = ndvi[0]
        harvests: dict[str, Any] = {}
        for crop in crops:
            res = estimate_yields_from_ndvi(ndvi, crop)
            harvests[crop] = res
            if res.get("status") == "ok":
                out["sensor_overrides"][f"harvest_{crop}_t_ha"] = res["yield_t_ha"]
        out["harvest_estimates_t_ha"] = harvests
    else:
        out["harvest_estimates_t_ha"] = {"status": "no_ndvi"}

    # --- Underwriting flags ----------------------------------------------
    flags: dict[str, Any] = {}
    rain = out.get("rainfall", {})
    annual = rain.get("annual_rainfall_mm")
    div = rain.get("rainfall_seasonality_divergence_index")
    if annual is not None:
        flags["water_stress"] = "low" if annual >= 800 else ("moderate" if annual >= 400 else "high")
    if div is not None:
        flags["seasonality"] = "uniform" if div < 0.5 else ("seasonal" if div < 1.0 else "monsoonal")
    out["underwriting_flags"] = flags
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    p = argparse.ArgumentParser(description="Annual rainfall + crop harvest + seasonality underwriting.")
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    p.add_argument("--radius-m", type=float, default=500.0)
    p.add_argument("--lookback-days", type=int, default=365)
    p.add_argument("--crops", type=str, default="maize,wheat,rice,soy,coffee,cocoa")
    p.add_argument("--output", type=str, default=None)
    args = p.parse_args()

    coord = GeoCoordinate(args.lat, args.lon, args.radius_m)
    crops = tuple(c.strip().lower() for c in args.crops.split(",") if c.strip())
    result = build_agri_underwriting(coord, crops=crops, lookback_days=args.lookback_days)

    text = json.dumps(result, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()