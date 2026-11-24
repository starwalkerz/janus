"""
janus/geo_tsi_adapter.py

Total Solar Irradiance (TSI) score adapter on top of janus.geo_probe_updated.

Reuses upstream STAC/COG helpers. Two estimator backends:
  * "physics" : compact clear-sky + cloud-index model (no external deps beyond NumPy)
  * "onnx"    : optional pre-trained irradiance regressor
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- Reuse upstream ----------------------------------------------------------
try:
    from .geo_probe_updated import (
        ELEMENT84_STAC_SEARCH_URL,
        INVALID_SCL_CLASSES,
        GeoCoordinate,
        _dynamic_datetime_range,
        _post_json,
        build_geo_external_data,
    )
    from .geo_vit_adapter import (
        BAND_KEYS,
        fetch_six_band_patch,
        _preprocess_for_vit,
        _load_onnx_session,
    )
except ImportError:  # direct script execution
    from geo_probe_updated import (  # type: ignore
        ELEMENT84_STAC_SEARCH_URL,
        INVALID_SCL_CLASSES,
        GeoCoordinate,
        _dynamic_datetime_range,
        _post_json,
        build_geo_external_data,
    )
    from geo_vit_adapter import (  # type: ignore
        BAND_KEYS,
        fetch_six_band_patch,
        _preprocess_for_vit,
        _load_onnx_session,
    )

# Solar constant (W m^-2) at 1 AU, Thuillier 2003 (Sentinel-2 mission model)
SOLAR_CONSTANT_W_M2 = 1361.0
DEFAULT_MAX_CLOUD_COVER = 35.0


# ---------------------------------------------------------------------------
# 1. Cloud / atmosphere feature extraction
# ---------------------------------------------------------------------------
def compute_solar_zenith_deg(
    scene_datetime: str,
    latitude: float,
    longitude: float,
) -> float:
    """Rough solar zenith angle from scene timestamp + coordinate (no ephem dep)."""
    # Parse ISO timestamp
    dt = datetime.fromisoformat(scene_datetime.replace("Z", "+00:00"))
    day_of_year = dt.timetuple().tm_yday
    # Solar declination (Cooper's equation, degrees)
    decl = 23.45 * math.sin(
        math.radians(360.0 / 365.0 * (284 + day_of_year))
    )
    # Hour angle from UTC time (approximate solar noon at longitude 0)
    utc_hours = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    hour_angle = (utc_hours - 12.0) * 15.0 + longitude
    lat_r = math.radians(latitude)
    decl_r = math.radians(decl)
    ha_r = math.radians(hour_angle)
    cos_zen = (
        math.sin(lat_r) * math.sin(decl_r)
        + math.cos(lat_r) * math.cos(decl_r) * math.cos(ha_r)
    )
    cos_zen = max(-1.0, min(1.0, cos_zen))
    return math.degrees(math.acos(cos_zen))


def compute_cloud_features(tensor: Any, clear_mask: Any) -> dict[str, float]:
    """Cloud fraction, shadow fraction, cirrus proxy, and clear-pixel NDVI."""
    import numpy as np

    total = float(clear_mask.size)
    clear = float(np.sum(clear_mask))
    cloud_fraction = 1.0 - clear / max(1.0, total)

    # Cirrus proxy: B10 (cirrus) is not in BAND_KEYS; use SWIR16/NIR ratio as a
    # thin-cloud / haze indicator when B10 is unavailable.
    swir16 = tensor[BAND_KEYS.index("swir16")]
    nir = tensor[BAND_KEYS.index("nir")]
    eps = 1e-6
    cirrus_proxy = float(
        np.nanmean(np.where(clear_mask, swir16 / (nir + eps), np.nan))
    )

    # Clear-pixel NDVI (for vegetation context)
    red = tensor[BAND_KEYS.index("red")]
    ndvi = (nir - red) / (nir + red + eps)
    ndvi_clear = float(np.nanmean(np.where(clear_mask, ndvi, np.nan)))

    return {
        "cloud_fraction": round(cloud_fraction, 4),
        "cirrus_proxy": round(cirrus_proxy, 4),
        "clear_ndvi_mean": round(ndvi_clear, 4),
        "clear_pixel_count": int(clear),
    }


# ---------------------------------------------------------------------------
# 2a. Physics-based irradiance estimator
# ---------------------------------------------------------------------------
def clear_sky_ghi_w_m2(
    solar_zenith_deg: float,
    elevation_m: float = 0.0,
    aerosol_optical_depth: float = 0.15,
) -> float:
    """
    Compact clear-sky GHI model (Haurwitz / simple broadband).
    GHI_clear ≈ S0 * cos(θz) * exp(-τ / cos(θz)) * altitude_correction
    """
    cos_z = max(0.0, math.cos(math.radians(solar_zenith_deg)))
    if cos_z <= 0.01:
        return 0.0
    air_mass = 1.0 / cos_z
    transmittance = math.exp(-aerosol_optical_depth * air_mass)
    alt_corr = math.exp(elevation_m / 8434.0)  # barometric approx
    return SOLAR_CONSTANT_W_M2 * cos_z * transmittance * alt_corr


def all_sky_ghi_w_m2(
    clear_ghi: float,
    cloud_fraction: float,
    cloud_attenuation: float = 0.75,
) -> float:
    """Simple cloud attenuation: GHI_all = GHI_clear * (1 - k * CF)."""
    cf = max(0.0, min(1.0, cloud_fraction))
    return max(0.0, clear_ghi * (1.0 - cloud_attenuation * cf))


def irradiance_score(
    all_sky_ghi: float,
    clear_sky_ghi: float,
) -> int:
    """Normalised TSI score in [0, 100] relative to clear-sky maximum."""
    if clear_sky_ghi <= 1.0:
        return 0
    ratio = max(0.0, min(1.0, all_sky_ghi / clear_sky_ghi))
    return int(round(ratio * 100.0))


# ---------------------------------------------------------------------------
# 2b. ONNX surrogate path
# ---------------------------------------------------------------------------
def run_onnx_irradiance(
    tensor: Any,
    model_path: str | Path,
    input_size: int = 224,
) -> dict[str, Any]:
    """Run an ONNX irradiance regressor over the (6, H, W) patch."""
    path = Path(model_path)
    sess, status = _load_onnx_session(path)
    if sess is None:
        return {"status": status}
    try:
        import numpy as np

        x = _preprocess_for_vit(tensor, input_size=input_size)
        input_meta = sess.get_inputs()[0]
        outputs = sess.run(None, {input_meta.name: x.astype(np.float32)})
        raw = np.asarray(outputs[0]).ravel()
        # Assume the model outputs GHI in W m^-2 (or a normalised value).
        ghi = float(raw[0])
        if 0.0 <= ghi <= 1.0:
            # Model returned a fraction of solar constant
            ghi *= SOLAR_CONSTANT_W_M2
        return {
            "status": "ok",
            "model": str(path),
            "estimated_ghi_w_m2": round(ghi, 2),
            "raw_output_shape": list(np.asarray(outputs[0]).shape),
        }
    except Exception as exc:
        return {"status": "onnx_run_error", "error": str(exc)}


# ---------------------------------------------------------------------------
# 3. Top-level adapter
# ---------------------------------------------------------------------------
def build_tsi_adapter(
    coord: GeoCoordinate,
    lookback_days: int = 90,
    max_cloud_cover: float = DEFAULT_MAX_CLOUD_COVER,
    estimator: str = "physics",          # "physics" | "onnx"
    onnx_model: str | Path | None = None,
    vit_input_size: int = 224,
    fetch_cogs: bool = True,
) -> dict[str, Any]:
    """
    Return a dict with:
      status, source, queried_at_utc, latitude, longitude,
      scene_id, datetime, cloud_cover,
      cloud_features: {...},
      solar_zenith_deg,
      clear_sky_ghi_w_m2, all_sky_ghi_w_m2,
      total_solar_irradiance_score (0-100),
      sensor_overrides: {...}   # mergeable into build_geo_external_data
    """
    now_utc = datetime.now(timezone.utc)
    out: dict[str, Any] = {
        "status": "skipped",
        "source": "geo_tsi_adapter",
        "queried_at_utc": now_utc.isoformat(),
        "latitude": coord.latitude,
        "longitude": coord.longitude,
        "lookback_days": lookback_days,
        "cloud_features": {},
        "sensor_overrides": {},
    }
    if not fetch_cogs:
        return out

    patch = fetch_six_band_patch(
        coord,
        lookback_days=lookback_days,
        max_cloud_cover=max_cloud_cover,
    )
    if patch.get("status") != "ok":
        out.update(
            {
                "status": patch.get("status"),
                "error": patch.get("error"),
                "datetime_range": patch.get("datetime_range"),
            }
        )
        return out

    tensor = patch["tensor"]
    clear_mask = patch["clear_mask"]
    scene_dt = patch["datetime"]

    # 1. Features
    cloud_feats = compute_cloud_features(tensor, clear_mask)
    solar_zenith = compute_solar_zenith_deg(
        scene_dt, coord.latitude, coord.longitude
    )

    out.update(
        {
            "status": "ok",
            "scene_id": patch["scene_id"],
            "datetime": scene_dt,
            "cloud_cover": patch["cloud_cover"],
            "cloud_features": cloud_feats,
            "solar_zenith_deg": round(solar_zenith, 2),
        }
    )

    # 2. Irradiance estimate
    if estimator == "onnx" and onnx_model is not None:
        irr = run_onnx_irradiance(tensor, onnx_model, vit_input_size)
        if irr.get("status") == "ok":
            ghi_all = irr["estimated_ghi_w_m2"]
            clear_ghi = clear_sky_ghi_w_m2(solar_zenith)
            out["estimator"] = "onnx"
            out["clear_sky_ghi_w_m2"] = round(clear_ghi, 2)
            out["all_sky_ghi_w_m2"] = round(ghi_all, 2)
            out["total_solar_irradiance_score"] = irradiance_score(
                ghi_all, clear_ghi
            )
            out["sensor_overrides"][
                "total_solar_irradiance_score"
            ] = out["total_solar_irradiance_score"]
            return out

    # Fallback / default: physics
    clear_ghi = clear_sky_ghi_w_m2(solar_zenith)
    ghi_all = all_sky_ghi_w_m2(
        clear_ghi, cloud_feats["cloud_fraction"]
    )
    score = irradiance_score(ghi_all, clear_ghi)

    out.update(
        {
            "estimator": "physics",
            "clear_sky_ghi_w_m2": round(clear_ghi, 2),
            "all_sky_ghi_w_m2": round(ghi_all, 2),
            "total_solar_irradiance_score": score,
        }
    )
    out["sensor_overrides"]["total_solar_irradiance_score"] = score
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute a total solar irradiance (TSI) score from Sentinel-2."
    )
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--radius-m", type=float, default=500.0)
    parser.add_argument("--lookback-days", type=int, default=90)
    parser.add_argument("--max-cloud-cover", type=float, default=35.0)
    parser.add_argument("--symbol", type=str, default="")
    parser.add_argument(
        "--estimator",
        choices=["physics", "onnx"],
        default="physics",
        help="Irradiance estimator backend",
    )
    parser.add_argument("--onnx-model", type=str, default=None)
    parser.add_argument("--merge", action="store_true")
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--no-cogs", action="store_true")
    args = parser.parse_args()

    coord = GeoCoordinate(
        latitude=args.lat,
        longitude=args.lon,
        radius_m=args.radius_m,
        label=args.symbol,
    )

    result = build_tsi_adapter(
        coord,
        lookback_days=args.lookback_days,
        max_cloud_cover=args.max_cloud_cover,
        estimator=args.estimator,
        onnx_model=args.onnx_model,
        fetch_cogs=not args.no_cogs,
    )

    payload: Any = result
    if args.merge:
        snapshot = build_geo_external_data(
            coord=coord,
            sensor_overrides=result.get("sensor_overrides", {}),
            query_live_stac=True,
            extract_cogs=True,
        )
        payload = {"tsi_adapter": result, "snapshot": snapshot}

    text = json.dumps(payload, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()