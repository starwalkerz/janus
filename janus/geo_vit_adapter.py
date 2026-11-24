"""
janus/geo_vit_adapter.py

Adapter layer for `janus.geo_probe_updated` that:

1. Fetches aligned 6-band Sentinel-2 L2A COG patch tensors from Element84 Earth
   Search dynamically up to current UTC time (reusing the parent module's
   `_post_json`, `_dynamic_datetime_range`, and `INVALID_SCL_CLASSES` helpers).
2. Computes pure-NumPy spatial topology metrics:
     - sobel_edge_anisotropy
     - disturbance_compactness_ratio
3. Optionally runs an open-weight geospatial Vision Transformer via ONNX Runtime
   and emits normalized `sensor_overrides` ready to merge into
   `geo_probe_updated.build_geo_external_data(...)`.
4. Provides a clean `argparse` `main()` CLI entrypoint.

Usage (CLI):

    python -m janus.geo_vit_adapter --lat 62.2426 --lon 25.7473 --symbol FOREST_FI
    python -m janus.geo_vit_adapter --lat -0.4167 --lon 36.95 \\
        --symbol COFFEE_KE --onnx-model ./models/satmae_lite.onnx --merge
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- Reuse upstream helpers so adapter and probe stay in lock-step -------------
try:
    from .geo_probe_updated import (  # type: ignore
        ELEMENT84_STAC_SEARCH_URL,
        INVALID_SCL_CLASSES,
        GeoCoordinate,
        _dynamic_datetime_range,
        _post_json,
        build_geo_external_data,
    )
except ImportError:  # pragma: no cover - direct script execution
    from geo_probe_updated import (  # type: ignore
        ELEMENT84_STAC_SEARCH_URL,
        INVALID_SCL_CLASSES,
        GeoCoordinate,
        _dynamic_datetime_range,
        _post_json,
        build_geo_external_data,
    )

# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------
BAND_KEYS: tuple[str, ...] = (
    "blue",
    "green",
    "red",
    "rededge1",
    "nir",
    "swir16",
)
MASK_KEY = "scl"
DEFAULT_MAX_CLOUD_COVER = 35.0
DEFAULT_MIN_SIDE = 32
DEFAULT_MAX_SIDE = 256

# Per-band L2A reflectance normalization used by the optional ONNX ViT.
# Values are typical Sentinel-2 L2A scene means/stds after DN/10000 scaling.
DEFAULT_VIT_MEAN: tuple[float, ...] = (0.10, 0.10, 0.10, 0.12, 0.22, 0.14)
DEFAULT_VIT_STD: tuple[float, ...] = (0.08, 0.08, 0.08, 0.10, 0.14, 0.10)


# ---------------------------------------------------------------------------
# 6-band COG tensor fetching
# ---------------------------------------------------------------------------
def _read_aligned_window(
    assets: dict[str, Any],
    key: str,
    bbox_4326: tuple[float, float, float, float],
    out_shape: tuple[int, int],
    is_mask: bool = False,
) -> Any:
    """Read a single band's aligned window, resampled to (out_h, out_w)."""
    import numpy as np
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds

    if key not in assets or "href" not in assets[key]:
        raise KeyError(f"Asset '{key}' has no href in STAC feature")

    with rasterio.open(assets[key]["href"]) as ds:
        b = transform_bounds("EPSG:4326", ds.crs, *bbox_4326)
        w = (
            from_bounds(*b, transform=ds.transform)
            .round_offsets()
            .round_lengths()
        )
        resamp = Resampling.nearest if is_mask else Resampling.bilinear
        arr = ds.read(1, window=w, out_shape=out_shape, resampling=resamp)
    return arr.astype(np.int32) if is_mask else arr.astype(np.float32)


def fetch_six_band_patch(
    coord: GeoCoordinate,
    lookback_days: int = 90,
    max_cloud_cover: float = DEFAULT_MAX_CLOUD_COVER,
    timeout_s: float = 10.0,
    min_side: int = DEFAULT_MIN_SIDE,
    max_side: int = DEFAULT_MAX_SIDE,
) -> dict[str, Any]:
    """
    Return an aligned 6-band Sentinel-2 L2A COG patch tensor (6, H, W) plus a
    clear-pixel boolean mask (H, W), anchored to the most recent low-cloud scene
    within `lookback_days` of the current UTC instant.
    """
    try:
        import numpy as np
        import rasterio  # noqa: F401
    except ImportError:
        return {
            "status": "optional_deps_missing",
            "note": "Install rasterio and numpy to read COG patches.",
        }

    live_dt_range = _dynamic_datetime_range(lookback_days=lookback_days)
    bbox_4326 = coord.to_bbox()
    try:
        stac_resp = _post_json(
            ELEMENT84_STAC_SEARCH_URL,
            {
                "bbox": list(bbox_4326),
                "collections": ["sentinel-2-l2a"],
                "datetime": live_dt_range,
                "limit": 6,
                "query": {"eo:cloud_cover": {"lt": max_cloud_cover}},
            },
            timeout_s=timeout_s,
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "status": "stac_unreachable",
            "datetime_range": live_dt_range,
            "error": str(exc),
        }

    features = stac_resp.get("features", [])
    if not features:
        return {
            "status": "no_low_cloud_scenes",
            "datetime_range": live_dt_range,
        }

    best = min(
        features,
        key=lambda f: float(
            f.get("properties", {}).get("eo:cloud_cover", 100.0)
        ),
    )
    assets = best.get("assets", {})
    needed = (*BAND_KEYS, MASK_KEY)
    missing = [k for k in needed if k not in assets or "href" not in assets[k]]
    if missing:
        return {
            "status": "missing_assets",
            "scene_id": best.get("id", ""),
            "missing": missing,
        }

    try:
        import numpy as np
        import rasterio
        from rasterio.warp import transform_bounds
        from rasterio.windows import from_bounds

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
                out_h = max(min_side, min(max_side, int(win.height)))
                out_w = max(min_side, min(max_side, int(win.width)))

            bands = np.empty(
                (len(BAND_KEYS), out_h, out_w), dtype=np.float32
            )
            for i, key in enumerate(BAND_KEYS):
                bands[i] = _read_aligned_window(
                    assets, key, bbox_4326, (out_h, out_w)
                )

            scl = _read_aligned_window(
                assets,
                MASK_KEY,
                bbox_4326,
                (out_h, out_w),
                is_mask=True,
            )
            clear_mask = ~np.isin(scl, INVALID_SCL_CLASSES)
            for i in range(bands.shape[0]):
                clear_mask &= bands[i] > 0.0
            clear_fraction = float(np.mean(clear_mask))
            if int(np.sum(clear_mask)) < 4:
                return {
                    "status": "cloud_masked_or_empty",
                    "scene_id": best.get("id", ""),
                    "datetime_range": live_dt_range,
                }

            return {
                "status": "ok",
                "source": "element84_six_band_cog",
                "datetime_range": live_dt_range,
                "scene_id": best.get("id", ""),
                "datetime": best.get("properties", {}).get("datetime", ""),
                "cloud_cover": best.get("properties", {}).get(
                    "eo:cloud_cover"
                ),
                "band_keys": list(BAND_KEYS),
                "patch_shape": [int(bands.shape[0]), out_h, out_w],
                "clear_pixel_fraction": round(clear_fraction, 4),
                "tensor": bands,
                "clear_mask": clear_mask,
            }
    except Exception as exc:  # pragma: no cover - network/GDAL safety
        return {
            "status": "cog_read_error",
            "scene_id": best.get("id", ""),
            "datetime_range": live_dt_range,
            "error": str(exc),
        }


# ---------------------------------------------------------------------------
# Pure-NumPy spatial topology metrics
# ---------------------------------------------------------------------------
def _ndvi_plane(tensor: Any) -> Any:
    """NDVI from a (6, H, W) tensor aligned to BAND_KEYS."""
    import numpy as np

    nir = tensor[BAND_KEYS.index("nir")]
    red = tensor[BAND_KEYS.index("red")]
    eps = 1e-6
    return (nir - red) / (nir + red + eps)


def _sobel_gradients(plane: Any) -> tuple[Any, Any]:
    """Pure-NumPy 3x3 Sobel horizontal (Gx) and vertical (Gy) gradients."""
    import numpy as np

    p = np.asarray(plane, dtype=np.float32)
    if p.ndim != 2 or p.shape[0] < 3 or p.shape[1] < 3:
        zeros = np.zeros_like(p)
        return zeros, zeros

    pp = np.pad(p, 1, mode="edge")
    gx = (
        -pp[:-2, :-2]
        + pp[:-2, 2:]
        - 2.0 * pp[1:-1, :-2]
        + 2.0 * pp[1:-1, 2:]
        - pp[2:, :-2]
        + pp[2:, 2:]
    )
    gy = (
        -pp[:-2, :-2]
        - 2.0 * pp[:-2, 1:-1]
        - pp[:-2, 2:]
        + pp[2:, :-2]
        + 2.0 * pp[2:, 1:-1]
        + pp[2:, 2:]
    )
    return gx.astype(np.float32), gy.astype(np.float32)


def sobel_edge_anisotropy(
    plane: Any, clear_mask: Any | None = None
) -> float:
    """
    Directional edge anisotropy in [-1, 1] from Sobel gradients on a 2D plane:

        0.0  = isotropic (no preferred edge orientation)
        +1.0 = horizontal structure dominates (e.g. plantation rows)
        -1.0 = vertical structure dominates (e.g. drainage / rail cuts)

    Computed as ``(mean|Gx| - mean|Gy|) / (mean|Gx| + mean|Gy| + eps)``
    over clear pixels only (if a boolean mask is supplied).
    """
    import numpy as np

    gx, gy = _sobel_gradients(plane)
    m = (
        np.ones_like(gx, dtype=bool)
        if clear_mask is None
        else np.asarray(clear_mask, dtype=bool)
    )
    ax = np.abs(gx[m]) if np.any(m) else np.array([0.0])
    ay = np.abs(gy[m]) if np.any(m) else np.array([0.0])
    mx = float(np.mean(ax)) if ax.size else 0.0
    my = float(np.mean(ay)) if ay.size else 0.0
    return round((mx - my) / (mx + my + 1e-9), 4)


def _disturbance_stats(
    plane: Any,
    clear_mask: Any | None = None,
    percentile: float = 20.0,
) -> dict[str, float]:
    """
    Internal helper returning the compactness statistics for a low-NDVI
    disturbance proxy. Exposed via ``disturbance_compactness_ratio``.
    """
    import numpy as np

    p = np.asarray(plane, dtype=np.float32)
    m = (
        np.ones_like(p, dtype=bool)
        if clear_mask is None
        else np.asarray(clear_mask, dtype=bool)
    )
    valid = p[m & np.isfinite(p)]
    if valid.size < 4:
        return {
            "isoperimetric_ratio": 0.0,
            "fill_ratio": 0.0,
            "area_fraction": 0.0,
            "perimeter_pixels": 0.0,
        }

    thr = float(np.percentile(valid, percentile))
    disturb = m & np.isfinite(p) & (p <= thr)
    area = int(np.sum(disturb))
    if area == 0:
        return {
            "isoperimetric_ratio": 0.0,
            "fill_ratio": 0.0,
            "area_fraction": 0.0,
            "perimeter_pixels": 0.0,
        }

    b = disturb.astype(np.int8)
    perim = int(np.sum(b[:, :-1] != b[:, 1:]))
    perim += int(np.sum(b[:-1, :] != b[1:, :]))

    rows = np.any(disturb, axis=1)
    cols = np.any(disturb, axis=0)
    bbox_area = int(np.sum(rows)) * int(np.sum(cols))
    fill_ratio = float(area) / float(bbox_area) if bbox_area > 0 else 0.0

    iso = 0.0
    if perim > 0:
        iso = (4.0 * math.pi * float(area)) / (float(perim) ** 2)
        iso = max(0.0, min(1.0, iso))

    clear_count = int(np.sum(m))
    area_fraction = float(area) / float(max(1, clear_count))

    return {
        "isoperimetric_ratio": round(iso, 4),
        "fill_ratio": round(fill_ratio, 4),
        "area_fraction": round(area_fraction, 4),
        "perimeter_pixels": float(perim),
    }


def disturbance_compactness_ratio(
    plane: Any,
    clear_mask: Any | None = None,
    percentile: float = 20.0,
) -> float:
    """
    Isoperimetric compactness ratio of low-NDVI disturbance patches, in [0, 1].

    Disturbance mask = clear pixels at or below the ``percentile``-th
    percentile of the clear-pixel NDVI distribution.

        1.0 = single circular blob (very compact disturbance)
        0.0 = no disturbance / fully diffuse perimeter
    """
    return _disturbance_stats(plane, clear_mask, percentile)[
        "isoperimetric_ratio"
    ]


def compute_topology_metrics(
    tensor: Any, clear_mask: Any | None = None
) -> dict[str, Any]:
    """
    Bundle the two required topology metrics plus a few diagnostics:

        sobel_edge_anisotropy        (float, NDVI plane, primary signal)
        sobel_edge_anisotropy_nir    (float, NIR plane, complementary)
        disturbance_compactness_ratio(float, isoperimetric ratio)
        disturbance_fill_ratio       (float, disturbance bbox fill)
        disturbance_area_fraction    (float, disturbed / clear pixels)
        mean_ndvi_gradient_magnitude (float, mean |∇NDVI|)
    """
    import numpy as np

    ndvi = _ndvi_plane(tensor)
    ndvi_masked = (
        np.where(clear_mask, ndvi, np.nan)
        if clear_mask is not None
        else ndvi
    )

    ndvi_iso = sobel_edge_anisotropy(ndvi_masked, clear_mask)
    nir_iso = sobel_edge_anisotropy(
        tensor[BAND_KEYS.index("nir")], clear_mask
    )
    disturb = _disturbance_stats(ndvi_masked, clear_mask)

    gx, gy = _sobel_gradients(np.nan_to_num(ndvi_masked))
    grad_mag = np.sqrt(gx * gx + gy * gy)
    finite = grad_mag[np.isfinite(grad_mag)]
    mean_grad = float(np.mean(finite)) if finite.size else 0.0

    return {
        "sobel_edge_anisotropy": ndvi_iso,
        "sobel_edge_anisotropy_ndvi": ndvi_iso,
        "sobel_edge_anisotropy_nir": nir_iso,
        "disturbance_compactness_ratio": disturb["isoperimetric_ratio"],
        "disturbance_fill_ratio": disturb["fill_ratio"],
        "disturbance_area_fraction": disturb["area_fraction"],
        "disturbance_perimeter_pixels": disturb["perimeter_pixels"],
        "mean_ndvi_gradient_magnitude": round(mean_grad, 4),
    }


# ---------------------------------------------------------------------------
# Optional ONNX Runtime geospatial Vision Transformer
# ---------------------------------------------------------------------------
def _load_onnx_session(model_path: Path) -> tuple[Any, str]:
    """Return (onnxruntime.InferenceSession | None, status_str)."""
    try:
        import onnxruntime as ort
    except ImportError:
        return None, "onnxruntime_not_installed"
    if not model_path.exists():
        return None, f"model_not_found:{model_path}"
    try:
        sess = ort.InferenceSession(
            str(model_path), providers=["CPUExecutionProvider"]
        )
    except Exception as exc:  # pragma: no cover - ONNX runtime safety
        return None, f"onnx_load_error:{exc}"
    return sess, "ok"


def _preprocess_for_vit(
    tensor: Any,
    input_size: int = 224,
    mean: tuple[float, ...] = DEFAULT_VIT_MEAN,
    std: tuple[float, ...] = DEFAULT_VIT_STD,
) -> Any:
    """Bilinear-resize and per-band-normalize a (6, H, W) tensor to (1, 6, S, S)."""
    import numpy as np

    arr = np.asarray(tensor, dtype=np.float32)
    c, h, w = arr.shape

    ys = np.linspace(0, h - 1, input_size).astype(np.float32)
    xs = np.linspace(0, w - 1, input_size).astype(np.float32)
    y0 = np.floor(ys).astype(np.int32)
    x0 = np.floor(xs).astype(np.int32)
    y1 = np.minimum(y0 + 1, h - 1)
    x1 = np.minimum(x0 + 1, w - 1)
    wy = (ys - y0)[:, None]
    wx = (xs - x0)[None, :]

    out = np.empty((c, input_size, input_size), dtype=np.float32)
    for i in range(c):
        top = arr[i][y0][:, x0] * (1.0 - wx) + arr[i][y0][:, x1] * wx
        bot = arr[i][y1][:, x0] * (1.0 - wx) + arr[i][y1][:, x1] * wx
        out[i] = top * (1.0 - wy) + bot * wy

    m = np.asarray(mean, dtype=np.float32).reshape(c, 1, 1)
    s = np.asarray(std, dtype=np.float32).reshape(c, 1, 1)
    out = (out - m) / (s + 1e-6)
    return out[np.newaxis, ...]


def _vit_output_to_sensor_overrides(raw_output: Any) -> dict[str, Any]:
    """
    Normalize raw ONNX output into the `sensor_overrides` schema understood by
    ``geo_probe_updated.build_geo_external_data``.

    Expected output conventions (first match wins):

        * scalar / shape (1,)      -> shade_tree_canopy_cover_pct
        * shape (3,) / (1, 3)      -> [maturity, multi_strata, shade]
        * shape (N,) with N >= 3   -> first three components as above

    Each component is treated as a logit; if it is already inside [0, 1] it is
    assumed to be a probability and scaled by 100. Otherwise a sigmoid is
    applied before scaling.
    """
    import numpy as np

    arr = np.asarray(raw_output, dtype=np.float64).ravel()
    if arr.size == 0:
        return {}

    def _sigmoid(x: float) -> float:
        if x >= 0.0:
            return 1.0 / (1.0 + math.exp(-x))
        e = math.exp(x)
        return e / (1.0 + e)

    def _scaled(v: float) -> float:
        if 0.0 <= v <= 1.0:
            return round(v * 100.0, 2)
        return round(_sigmoid(v) * 100.0, 2)

    if arr.size == 1:
        return {"shade_tree_canopy_cover_pct": _scaled(float(arr[0]))}

    maturity = _scaled(float(arr[0]))
    multi = _scaled(float(arr[1]))
    shade = _scaled(float(arr[2]))
    return {
        "canopy_structural_maturity_score": int(round(maturity)),
        "multi_strata_sar_red_edge_score": int(round(multi)),
        "shade_tree_canopy_cover_pct": shade,
    }


def run_onnx_vit(
    tensor: Any,
    model_path: str | Path,
    input_size: int = 224,
    mean: tuple[float, ...] = DEFAULT_VIT_MEAN,
    std: tuple[float, ...] = DEFAULT_VIT_STD,
) -> dict[str, Any]:
    """Run an optional ONNX ViT over a (6, H, W) tensor and emit sensor_overrides."""
    path = Path(model_path)
    sess, status = _load_onnx_session(path)
    if sess is None:
        return {"status": status}

    try:
        import numpy as np

        x = _preprocess_for_vit(tensor, input_size, mean, std)

        input_meta = sess.get_inputs()[0]
        want_c: int | None = None
        if isinstance(input_meta.shape, (list, tuple)) and len(input_meta.shape) == 4:
            dim = input_meta.shape[1]
            if isinstance(dim, int) and dim > 0:
                want_c = dim
        if want_c is not None and want_c < x.shape[1]:
            x = x[:, :want_c]
        elif want_c is not None and want_c > x.shape[1]:
            pad = np.zeros(
                (1, want_c - x.shape[1], x.shape[2], x.shape[3]),
                dtype=x.dtype,
            )
            x = np.concatenate([x, pad], axis=1)

        outputs = sess.run(None, {input_meta.name: x.astype(np.float32)})
        overrides = _vit_output_to_sensor_overrides(outputs[0])
        return {
            "status": "ok",
            "model": str(path),
            "providers": sess.get_providers(),
            "raw_output_shape": list(np.asarray(outputs[0]).shape),
            "sensor_overrides": overrides,
        }
    except Exception as exc:  # pragma: no cover - ONNX runtime safety
        return {"status": "onnx_run_error", "error": str(exc)}


# ---------------------------------------------------------------------------
# Top-level adapter entrypoint
# ---------------------------------------------------------------------------
def build_vit_adapter(
    coord: GeoCoordinate,
    lookback_days: int = 90,
    max_cloud_cover: float = DEFAULT_MAX_CLOUD_COVER,
    timeout_s: float = 10.0,
    onnx_model: str | Path | None = None,
    vit_input_size: int = 224,
    vit_mean: tuple[float, ...] = DEFAULT_VIT_MEAN,
    vit_std: tuple[float, ...] = DEFAULT_VIT_STD,
    fetch_cogs: bool = True,
) -> dict[str, Any]:
    """
    Compute topology metrics and (optionally) ViT overrides for ``coord``.

    Returns:
        {
            "status": "ok" | <upstream failure status> | "skipped",
            "source": "geo_vit_adapter",
            "queried_at_utc": ISO-8601,
            "latitude", "longitude", "lookback_days",
            "scene_id", "datetime", "cloud_cover",
            "band_keys", "patch_shape", "clear_pixel_fraction",
            "topology": {...},
            "sensor_overrides": {...},   # ready for build_geo_external_data
            "vit": {...}                 # only when onnx_model was supplied
        }
    """
    now_utc = datetime.now(timezone.utc)
    out: dict[str, Any] = {
        "status": "skipped",
        "source": "geo_vit_adapter",
        "queried_at_utc": now_utc.isoformat(),
        "latitude": coord.latitude,
        "longitude": coord.longitude,
        "lookback_days": lookback_days,
        "topology": {},
        "sensor_overrides": {},
    }
    if not fetch_cogs:
        return out

    patch = fetch_six_band_patch(
        coord,
        lookback_days=lookback_days,
        max_cloud_cover=max_cloud_cover,
        timeout_s=timeout_s,
    )
    if patch.get("status") != "ok":
        out["status"] = patch.get("status", "unknown")
        out["error"] = patch.get("error")
        out["datetime_range"] = patch.get("datetime_range")
        return out

    tensor = patch["tensor"]
    clear_mask = patch["clear_mask"]

    out["status"] = "ok"
    out["scene_id"] = patch["scene_id"]
    out["datetime"] = patch["datetime"]
    out["cloud_cover"] = patch["cloud_cover"]
    out["band_keys"] = patch["band_keys"]
    out["patch_shape"] = patch["patch_shape"]
    out["clear_pixel_fraction"] = patch["clear_pixel_fraction"]

    topo = compute_topology_metrics(tensor, clear_mask)
    out["topology"] = topo

    # Deterministic topology-derived overrides, so downstream consumers always
    # see the same schema the COG extractor populates.
    overrides: dict[str, Any] = {
        # Strong horizontal banding (planted rows) -> higher maturity.
        "canopy_structural_maturity_score": int(
            round(
                max(
                    0.0,
                    min(100.0, 60.0 + 30.0 * topo["sobel_edge_anisotropy"]),
                )
            )
        ),
        # A single compact disturbance blob -> lower vertical strata score.
        "multi_strata_sar_red_edge_score": int(
            round(
                max(
                    0.0,
                    min(
                        100.0,
                        75.0
                        - 40.0 * topo["disturbance_compactness_ratio"],
                    ),
                )
            )
        ),
        # Low disturbance area fraction -> high residual shade canopy.
        "shade_tree_canopy_cover_pct": round(
            max(
                0.0,
                min(
                    100.0,
                    100.0 * (1.0 - topo["disturbance_area_fraction"]),
                ),
            ),
            2,
        ),
    }
    out["sensor_overrides"] = overrides

    if onnx_model is not None:
        vit = run_onnx_vit(
            tensor,
            onnx_model,
            input_size=vit_input_size,
            mean=vit_mean,
            std=vit_std,
        )
        out["vit"] = vit
        if vit.get("status") == "ok":
            out["sensor_overrides"].update(vit["sensor_overrides"])

    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _parse_band_float_list(
    text: str | None, default: tuple[float, ...]
) -> tuple[float, ...]:
    """Parse a comma-separated per-band float list of length len(BAND_KEYS)."""
    if not text:
        return default
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if len(parts) != len(BAND_KEYS):
        raise argparse.ArgumentTypeError(
            f"Expected {len(BAND_KEYS)} comma-separated floats, got {len(parts)}"
        )
    return tuple(float(p) for p in parts)


def _json_default(obj: Any) -> Any:
    """Fallback JSON encoder for NumPy scalars/arrays."""
    try:
        import numpy as np

        if isinstance(obj, np.generic):
            return obj.item()
        if isinstance(obj, np.ndarray):
            return obj.tolist()
    except ImportError:
        pass
    raise TypeError(
        f"Object of type {type(obj).__name__} is not JSON serializable"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Adapter for janus.geo_probe_updated: fetches an aligned 6-band "
            "Sentinel-2 L2A COG patch, computes Sobel edge anisotropy and "
            "disturbance compactness, and (optionally) runs an ONNX ViT."
        )
    )
    parser.add_argument("--lat", type=float, required=True, help="WGS84 latitude")
    parser.add_argument("--lon", type=float, required=True, help="WGS84 longitude")
    parser.add_argument(
        "--radius-m", type=float, default=500.0, help="Bounding-box radius (m)"
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=90,
        help="Rolling lookback up to current UTC instant",
    )
    parser.add_argument(
        "--max-cloud-cover",
        type=float,
        default=DEFAULT_MAX_CLOUD_COVER,
        help="Maximum scene-level cloud cover percent",
    )
    parser.add_argument(
        "--symbol", type=str, default="", help="Optional ticker or asset key"
    )
    parser.add_argument(
        "--crop",
        type=str,
        default="generic",
        choices=["generic", "cacao", "coffee"],
        help="Crop focus passed through to build_geo_external_data",
    )
    parser.add_argument(
        "--onnx-model",
        type=str,
        default=None,
        help="Optional path to an ONNX ViT checkpoint",
    )
    parser.add_argument(
        "--vit-input-size",
        type=int,
        default=224,
        help="Square side length fed to the ViT",
    )
    parser.add_argument(
        "--vit-mean",
        type=str,
        default=None,
        help="Comma-separated per-band means for ViT normalization",
    )
    parser.add_argument(
        "--vit-std",
        type=str,
        default=None,
        help="Comma-separated per-band stds for ViT normalization",
    )
    parser.add_argument(
        "--no-cogs",
        action="store_true",
        help="Skip COG reads (topology and ViT output empty)",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge sensor_overrides into build_geo_external_data(...) output",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional path to write JSON output (defaults to stdout)",
    )
    args = parser.parse_args()

    coord = GeoCoordinate(
        latitude=args.lat,
        longitude=args.lon,
        radius_m=args.radius_m,
        label=args.symbol,
    )
    mean = _parse_band_float_list(args.vit_mean, DEFAULT_VIT_MEAN)
    std = _parse_band_float_list(args.vit_std, DEFAULT_VIT_STD)

    adapter_result = build_vit_adapter(
        coord,
        lookback_days=args.lookback_days,
        max_cloud_cover=args.max_cloud_cover,
        onnx_model=args.onnx_model,
        vit_input_size=args.vit_input_size,
        vit_mean=mean,
        vit_std=std,
        fetch_cogs=not args.no_cogs,
    )

    if args.merge:
        snapshot = build_geo_external_data(
            coord=coord,
            crop_type=args.crop,
            lookback_days=args.lookback_days,
            sensor_overrides=adapter_result.get("sensor_overrides", {}),
            query_live_stac=True,
            extract_cogs=True,
        )
        payload: dict[str, Any] = {
            "adapter": adapter_result,
            "snapshot": snapshot,
        }
    else:
        payload = adapter_result

    text = json.dumps(payload, indent=2, default=_json_default)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


if __name__ == "__main__":
    main()