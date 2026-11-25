"""
JANUS Geo Probe local HTTP bridge.

Place this file at janus/geo_probe_api.py beside geo_probe.py.
Run from the repository root:
    python -m janus.geo_probe_api --host 127.0.0.1 --port 8765

The bridge delegates all core probe work to janus.geo_probe. Optional LLM,
transformer, raster, or other enrichment can be attached through:
    JANUS_GEO_PROBE_ENRICHER=your_package.module:enrich

An enricher is called as:
    enrich(coord=coord, result=result, request=payload) -> dict | None

It should return a dictionary of additional result fields, or mutate result
and return None. Keep model weights and provider credentials on the Python
side; never send API keys to the browser.
"""
from __future__ import annotations

import argparse
import importlib
import json
import logging
import math
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from janus.geo_probe import GeoCoordinate, build_geo_external_data

LOG = logging.getLogger("janus.geo_probe_api")
ALLOWED_ORIGINS = {
    "https://browser.dataspace.copernicus.eu",
    "https://dataspace.copernicus.eu",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
}
MAX_BODY_BYTES = 1_000_000


def load_enricher():
    spec = os.environ.get("JANUS_GEO_PROBE_ENRICHER", "").strip()
    if not spec:
        return None
    if ":" not in spec:
        raise RuntimeError("Enricher must be specified as module:function")
    module_name, function_name = spec.split(":", 1)
    module = importlib.import_module(module_name)
    fn = getattr(module, function_name)
    if not callable(fn):
        raise RuntimeError(f"Configured enricher is not callable: {spec}")
    LOG.info("Loaded optional enrichment hook: %s", spec)
    return fn


ENRICHER = load_enricher()


class LocalBridge(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class Handler(BaseHTTPRequestHandler):
    server_version = "JANUS-GeoProbe-Bridge/0.1"

    def log_message(self, fmt, *args):
        LOG.info("%s - %s", self.address_string(), fmt % args)

    def _json(self, status: int, payload: dict[str, Any]):
        raw = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        origin = self.headers.get("Origin")
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.end_headers()
        self.wfile.write(raw)

    def _origin_ok(self) -> bool:
        origin = self.headers.get("Origin")
        # CLI/local health checks may have no Origin. Browser callers must match allowlist.
        return origin is None or origin in ALLOWED_ORIGINS

    def do_OPTIONS(self):
        if not self._origin_ok():
            return self._json(403, {"status": "error", "error": "Origin not allowed"})
        self.send_response(204)
        origin = self.headers.get("Origin")
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "600")
        self.end_headers()

    def do_GET(self):
        if not self._origin_ok():
            return self._json(403, {"status": "error", "error": "Origin not allowed"})
        path = urlparse(self.path).path
        if path == "/health":
            return self._json(200, {
                "status": "ok",
                "service": "janus-geo-probe",
                "python_enricher": ENRICHER is not None,
                "core": "janus.geo_probe.build_geo_external_data",
            })
        return self._json(404, {"status": "error", "error": "Not found"})

    def do_POST(self):
        if not self._origin_ok():
            return self._json(403, {"status": "error", "error": "Origin not allowed"})
        if urlparse(self.path).path != "/api/probe":
            return self._json(404, {"status": "error", "error": "Not found"})

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY_BYTES:
                return self._json(413, {"status": "error", "error": "Request body missing or too large"})
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("JSON body must be an object")

            lat = float(payload["latitude"])
            lon = float(payload["longitude"])
            radius = float(payload.get("radius_m", 500.0))
            if not all(math.isfinite(v) for v in (lat, lon, radius)):
                raise ValueError("Coordinates and radius must be finite numbers")

            coord = GeoCoordinate(
                latitude=lat,
                longitude=lon,
                radius_m=radius,
                label=str(payload.get("label", ""))[:200],
            )

            overrides = payload.get("sensor_overrides") or {}
            if not isinstance(overrides, dict):
                raise ValueError("sensor_overrides must be a JSON object")

            result = build_geo_external_data(
                coord=coord,
                crop_type=str(payload.get("crop_type", "generic"))[:40],
                sensor_overrides=overrides,
                query_live_stac=bool(payload.get("query_live_stac", True)),
            )

            if ENRICHER is not None and payload.get("run_enrichment", True):
                extra = ENRICHER(coord=coord, result=result, request=payload)
                if extra is not None:
                    if not isinstance(extra, dict):
                        raise TypeError("Enricher must return a dictionary or None")
                    result["enrichment"] = extra

            return self._json(200, {
                "status": "ok",
                "engine": "janus.geo_probe",
                "result": result,
            })

        except KeyError as exc:
            return self._json(400, {"status": "error", "error": f"Missing field: {exc}"})
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            return self._json(400, {"status": "error", "error": str(exc)})
        except Exception as exc:
            LOG.exception("Geo Probe request failed")
            return self._json(500, {"status": "error", "error": f"Probe failed: {exc}"})


def main():
    parser = argparse.ArgumentParser(description="Local HTTP bridge for JANUS Geo Probe")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address; keep this on loopback")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("Security: this bridge may only bind to localhost/loopback")
    server = LocalBridge((args.host, args.port), Handler)
    LOG.info("JANUS Geo Probe bridge listening at http://%s:%d", args.host, args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOG.info("Stopping bridge")
    finally:
        server.server_close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    main()
