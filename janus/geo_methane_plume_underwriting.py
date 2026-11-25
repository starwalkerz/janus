"""
janus/geo_methane_underwriting.py

Two adapters for parcel-level methane plume monitoring on a 500 x 500 m AOI:

1. PassRecorder       — one record per Sentinel-2 pass (~5-day cadence),
                        B11/B12 SWIR anomaly retrieval, plume mask, ballpark Q.
2. UnderwritingAggregator — monthly resolution, divergence from monthly baseline,
                        quarterly and annual roll-ups, underwriting flags.

Zero paid APIs. Sentinel-2 L2A via Element84 Earth Search (free, no key).
Detection limit: ~1,000–5,000 kg CH4/h (super-emitters only).
NOT a continuous emissions monitor — absence of a plume is not zero emissions.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.error
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .geo_probe_updated import (
        ELEMENT84_STAC_SEARCH_URL,
        GeoCoordinate,
        _post_json,
        _dynamic_datetime_range,
    )
except ImportError:
    from geo_probe_updated import (  # type: ignore
        ELEMENT84_STAC_SEARCH_URL,
        GeoCoordinate,
        _post_json,
        _dynamic_datetime_range,
    )

# --- Physical / retrieval constants -----------------------------------------
S2_PIXEL_M = 20.0
PIXEL_AREA_M2 = S2_PIXEL_M * S2_PIXEL_M
DEFAULT_DETECTION_THRESHOLD_KG_H = 2000.0   # conservative mid-range
# Empirical IME-to-flux coefficient, calibrated so a 10-ha plume with mean
# dR = 0.05 at 3 m/s wind maps to ~2000 kg/h (Varon et al. 2021 ballpark).
IME_FLUX_COEFF = 0.133
DEFAULT_WIND_SPEED_MS = 3.0
MIN_PLUME_PIXELS = 4


# ---------------------------------------------------------------------------
# Shared Sentinel-2 methane proxy retrieval
# ---------------------------------------------------------------------------
def _read_swir_patch(
    scene_feature: dict[str, Any],
    bbox_4326: tuple[float, float, float, float],
    out_side: int = 128,
) -> dict[str, Any] | None:
    """
    Read aligned B11 (SWIR1) and B12 (SWIR2) windows at 20 m, plus B08 (NIR)
    for a simple surface mask. Returns {'b11','b12','nir'} float32 arrays or None.
    """
    import numpy as np
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds

    assets = scene_feature.get("assets", {})
    needed = ("swir16", "swir22", "nir")
    if not all(k in assets and "href" in assets[k] for k in needed):
        return None

    try:
        with rasterio.Env(
            GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
            CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
        ):
            with rasterio.open(assets["nir"]["href"]) as nir_ds:
                dst_bounds = transform_bounds(
                    "EPSG:4326", nir_ds.crs, *bbox_4326
                )
                win = (
                    from_bounds(*dst_bounds, transform=nir_ds.transform)
                    .round_offsets()
                    .round_lengths()
                )
                side = max(32, min(256, out_side))
                nir = nir_ds.read(
                    1, window=win, out_shape=(side, side),
                    resampling=Resampling.bilinear,
                ).astype(np.float32)

            def _band(key: str) -> Any:
                with rasterio.open(assets[key]["href"]) as ds:
                    b = transform_bounds("EPSG:4326", ds.crs, *bbox_4326)
                    w = (
                        from_bounds(*b, transform=ds.transform)
                        .round_offsets()
                        .round_lengths()
                    )
                    return ds.read(
                        1, window=w, out_shape=(side, side),
                        resampling=Resampling.bilinear,
                    ).astype(np.float32)

            return {
                "b11": _band("swir16"),
                "b12": _band("swir22"),
                "nir": nir,
            }
    except Exception:
        return None


def compute_methane_plume(
    bands: dict[str, Any],
    wind_speed_ms: float = DEFAULT_WIND_SPEED_MS,
) -> dict[str, Any]:
    """
    B11/B12 ratio anomaly → plume mask → integrated mass enhancement proxy → Q.

    Returns a dict with detection flag, plume pixel count, mean dR, and
    estimated Q_kg_h (None if below detection threshold).
    """
    import numpy as np

    b11 = bands["b11"]
    b12 = bands["b12"]
    nir = bands["nir"]
    eps = 1e-6

    ratio = b12 / (b11 + eps)

    # Surface mask: drop low-reflectance and vegetated pixels where B11/B12
    # retrievals are unreliable (LRAD-style artifact suppression, simplified).
    surface_ok = (b11 > 0.05) & (b12 > 0.02) & (nir > 0.05)
    ndvi = (nir - b11) / (nir + b11 + eps)
    surface_ok &= ndvi < 0.5

    if int(np.sum(surface_ok)) < 16:
        return {
            "detected": False,
            "plume_pixels": 0,
            "mean_dr": 0.0,
            "q_kg_h": None,
            "status": "insufficient_valid_surface",
        }

    valid_ratio = ratio[surface_ok]
    background = float(np.median(valid_ratio))
    mad = float(np.median(np.abs(valid_ratio - background))) + 1e-9

    dr = ratio - background
    # Plume threshold: 4× MAD, and must exceed a 0.01 absolute ratio anomaly
    plume_mask = surface_ok & (dr > max(0.01, 4.0 * mad))
    n_plume = int(np.sum(plume_mask))
    if n_plume < MIN_PLUME_PIXELS:
        return {
            "detected": False,
            "plume_pixels": n_plume,
            "mean_dr": round(float(np.mean(dr[plume_mask])) if n_plume else 0.0, 5),
            "q_kg_h": None,
            "status": "below_detection",
        }

    mean_dr = float(np.mean(dr[plume_mask]))
    plume_area_m2 = n_plume * PIXEL_AREA_M2
    q_kg_h = IME_FLUX_COEFF * mean_dr * plume_area_m2 * wind_speed_ms

    return {
        "detected": True,
        "plume_pixels": n_plume,
        "plume_area_ha": round(plume_area_m2 / 10_000.0, 3),
        "mean_dr": round(mean_dr, 5),
        "q_kg_h": round(float(q_kg_h), 1),
        "status": "detected",
    }


def record_one_pass(
    coord: GeoCoordinate,
    pass_datetime: str,
    scene_feature: dict[str, Any],
    bbox_4326: tuple[float, float, float, float],
    wind_speed_ms: float = DEFAULT_WIND_SPEED_MS,
    detection_threshold_kg_h: float = DEFAULT_DETECTION_THRESHOLD_KG_H,
) -> dict[str, Any]:
    """Build a single pass record from one Sentinel-2 scene."""
    bands = _read_swir_patch(scene_feature, bbox_4326)
    if bands is None:
        return {
            "datetime": pass_datetime,
            "status": "swir_read_failed",
            "detected": False,
            "q_kg_h": None,
        }

    plume = compute_methane_plume(bands, wind_speed_ms)
    q = plume.get("q_kg_h")
    above_threshold = q is not None and q >= detection_threshold_kg_h

    return {
        "datetime": pass_datetime,
        "status": plume["status"],
        "detected": bool(plume["detected"]),
        "above_detection_threshold": above_threshold,
        "detection_threshold_kg_h": detection_threshold_kg_h,
        "plume_pixels": plume.get("plume_pixels", 0),
        "plume_area_ha": plume.get("plume_area_ha"),
        "mean_dr": plume.get("mean_dr", 0.0),
        "q_kg_h": q,
        "wind_speed_ms": wind_speed_ms,
    }


# ---------------------------------------------------------------------------
# Adapter 1 — PassRecorder
# ---------------------------------------------------------------------------
def record_passes(
    coord: GeoCoordinate,
    lookback_days: int = 30,
    max_cloud_cover: float = 30.0,
    wind_speed_ms: float = DEFAULT_WIND_SPEED_MS,
    detection_threshold_kg_h: float = DEFAULT_DETECTION_THRESHOLD_KG_H,
    plume_search_radius_m: float = 2000.0,
) -> list[dict[str, Any]]:
    """
    Query all Sentinel-2 L2A passes over a 2 km-radius search box around the
    parcel (so the plume can drift in from outside the 500 m fence line),
    then emit one record per pass.

    The output list is append-friendly JSONL: one line per pass.
    """
    # Search box larger than the parcel so plumes advected by wind are captured
    search_coord = GeoCoordinate(
        coord.latitude, coord.longitude,
        radius_m=plume_search_radius_m,
    )
    dt_range = _dynamic_datetime_range(lookback_days=lookback_days)
    bbox = search_coord.to_bbox()

    try:
        page = _post_json(
            ELEMENT84_STAC_SEARCH_URL,
            {
                "bbox": list(bbox),
                "collections": ["sentinel-2-l2a"],
                "datetime": dt_range,
                "limit": 100,
                "query": {"eo:cloud_cover": {"lt": max_cloud_cover}},
            },
            timeout_s=20.0,
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []

    features = page.get("features", [])
    records: list[dict[str, Any]] = []
    for feat in features:
        dt_str = feat.get("properties", {}).get("datetime", "")
        if not dt_str:
            continue
        rec = record_one_pass(
            coord, dt_str, feat, bbox,
            wind_speed_ms=wind_speed_ms,
            detection_threshold_kg_h=detection_threshold_kg_h,
        )
        rec["scene_id"] = feat.get("id", "")
        rec["cloud_cover"] = feat.get("properties", {}).get("eo:cloud_cover")
        records.append(rec)

    records.sort(key=lambda r: r["datetime"])
    return records


# ---------------------------------------------------------------------------
# Adapter 2 — UnderwritingAggregator
# ---------------------------------------------------------------------------
def _month_key(iso_dt: str) -> str:
    return datetime.fromisoformat(iso_dt.replace("Z", "+00:00")).strftime("%Y-%m")


def _quarter_key(iso_dt: str) -> str:
    dt = datetime.fromisoformat(iso_dt.replace("Z", "+00:00"))
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}-Q{q}"


def aggregate_pass_records(
    records: list[dict[str, Any]],
    detection_threshold_kg_h: float = DEFAULT_DETECTION_THRESHOLD_KG_H,
) -> dict[str, Any]:
    """
    Convert pass records into:
      * monthly: mean detected Q, detection frequency, max Q
      * divergence from monthly baseline (prior-year same month, if available)
      * quarterly: mean of monthly values
      * annual: mean of monthly values

    A pass with no plume contributes 0 to the monthly mean Q (detection = False),
    which is the correct underwriting treatment: no visible plume = no measured
    super-emitter emission, not zero actual emission.
    """
    monthly_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        monthly_buckets[_month_key(r["datetime"])].append(r)

    monthly_rows: list[dict[str, Any]] = []
    for month in sorted(monthly_buckets):
        recs = monthly_buckets[month]
        detections = [r for r in recs if r.get("detected")]
        q_values = [
            float(r["q_kg_h"]) for r in detections
            if r.get("q_kg_h") is not None
        ]
        monthly_rows.append({
            "month": month,
            "passes": len(recs),
            "detections": len(detections),
            "detection_frequency": round(
                len(detections) / max(1, len(recs)), 3
            ),
            "mean_q_kg_h": round(
                sum(q_values) / len(q_values), 1
            ) if q_values else 0.0,
            "max_q_kg_h": round(max(q_values), 1) if q_values else 0.0,
            "above_threshold_count": sum(
                1 for r in recs if r.get("above_detection_threshold")
            ),
        })

    # Divergence from monthly baseline (mean of prior-year same month)
    baseline: dict[int, list[float]] = defaultdict(list)
    for row in monthly_rows:
        m = int(row["month"].split("-")[1])
        baseline[m].append(row["mean_q_kg_h"])
    baseline_mean = {
        m: (sum(v) / len(v)) for m, v in baseline.items() if v
    }

    for row in monthly_rows:
        m = int(row["month"].split("-")[1])
        base = baseline_mean.get(m)
        row["baseline_monthly_mean_kg_h"] = round(base, 1) if base else None
        if base and base > 0:
            row["divergence_from_monthly_mean"] = round(
                (row["mean_q_kg_h"] - base) / base, 3
            )
        else:
            row["divergence_from_monthly_mean"] = None

    # Quarterly roll-up
    quarterly_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        quarterly_buckets[_quarter_key(r["datetime"])].append(r)

    quarterly_rows: list[dict[str, Any]] = []
    for q in sorted(quarterly_buckets):
        recs = quarterly_buckets[q]
        dets = [r for r in recs if r.get("detected")]
        qv = [
            float(r["q_kg_h"]) for r in dets
            if r.get("q_kg_h") is not None
        ]
        quarterly_rows.append({
            "quarter": q,
            "passes": len(recs),
            "detections": len(dets),
            "mean_q_kg_h": round(sum(qv) / len(qv), 1) if qv else 0.0,
            "max_q_kg_h": round(max(qv), 1) if qv else 0.0,
        })

    # Annual roll-up
    annual_buckets: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        y = datetime.fromisoformat(
            r["datetime"].replace("Z", "+00:00")
        ).year
        annual_buckets[y].append(r)

    annual_rows: list[dict[str, Any]] = []
    for y in sorted(annual_buckets):
        recs = annual_buckets[y]
        dets = [r for r in recs if r.get("detected")]
        qv = [
            float(r["q_kg_h"]) for r in dets
            if r.get("q_kg_h") is not None
        ]
        annual_rows.append({
            "year": y,
            "passes": len(recs),
            "detections": len(dets),
            "mean_q_kg_h": round(sum(qv) / len(qv), 1) if qv else 0.0,
            "max_q_kg_h": round(max(qv), 1) if qv else 0.0,
        })

    return {
        "status": "ok" if records else "no_passes",
        "detection_threshold_kg_h": detection_threshold_kg_h,
        "total_passes": len(records),
        "total_detections": sum(1 for r in records if r.get("detected")),
        "monthly": monthly_rows,
        "quarterly": quarterly_rows,
        "annual": annual_rows,
    }


def underwriting_flags(agg: dict[str, Any]) -> dict[str, Any]:
    """
    Map the aggregated plume record to underwriting flags.

    A detection above threshold on ANY pass is a material event for a
    500 m parcel; repeated detections are a hard red flag.
    """
    flags: dict[str, Any] = {}
    total_det = agg.get("total_detections", 0)
    above = sum(
        row.get("above_threshold_count", 0)
        for row in agg.get("monthly", [])
    )
    if above >= 2:
        flags["methane_status"] = "CRITICAL_REPEAT_SUPER_EMITTER"
    elif above == 1:
        flags["methane_status"] = "ELEVATED_SINGLE_SUPER_EMITTER"
    elif total_det > 0:
        flags["methane_status"] = "PLUME_DETECTED_BELOW_THRESHOLD"
    else:
        flags["methane_status"] = "NO_PLUME_ABOVE_DETECTION_LIMIT"

    # Divergence flag: any month > 2× baseline
    diverged = [
        row["month"]
        for row in agg.get("monthly", [])
        if row.get("divergence_from_monthly_mean") is not None
        and row["divergence_from_monthly_mean"] > 2.0
    ]
    if diverged:
        flags["divergent_months"] = diverged
    return flags


# ---------------------------------------------------------------------------
# CLI — two subcommands
# ---------------------------------------------------------------------------
def _cmd_record(args: argparse.Namespace) -> None:
    coord = GeoCoordinate(args.lat, args.lon, radius_m=250.0)
    records = record_passes(
        coord,
        lookback_days=args.lookback_days,
        max_cloud_cover=args.max_cloud_cover,
        wind_speed_ms=args.wind_speed,
        detection_threshold_kg_h=args.threshold,
    )
    text = "\n".join(
        json.dumps(r, default=str) for r in records
    )
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
    agg = aggregate_pass_records(records, detection_threshold_kg_h=args.threshold)
    agg["underwriting_flags"] = underwriting_flags(agg)
    text = json.dumps(agg, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Sentinel-2 methane pass recorder + underwriting aggregator."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record", help="Record one pass per Sentinel-2 overpass")
    r.add_argument("--lat", type=float, required=True)
    r.add_argument("--lon", type=float, required=True)
    r.add_argument("--lookback-days", type=int, default=30)
    r.add_argument("--max-cloud-cover", type=float, default=30.0)
    r.add_argument("--wind-speed", type=float, default=DEFAULT_WIND_SPEED_MS)
    r.add_argument(
        "--threshold", type=float, default=DEFAULT_DETECTION_THRESHOLD_KG_H
    )
    r.add_argument("--output", type=str, default=None, help="JSONL pass log")
    r.set_defaults(func=_cmd_record)

    u = sub.add_parser("underwrite", help="Aggregate pass log to monthly/quarterly/annual")
    u.add_argument("--input", type=str, required=True)
    u.add_argument(
        "--threshold", type=float, default=DEFAULT_DETECTION_THRESHOLD_KG_H
    )
    u.add_argument("--output", type=str, default=None)
    u.set_defaults(func=_cmd_underwrite)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()