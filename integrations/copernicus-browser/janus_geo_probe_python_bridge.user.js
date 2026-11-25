
// ==UserScript==
// @name         JANUS Geo Probe — Python Bridge for Copernicus Browser
// @namespace    https://github.com/starwalkerz/janus
// @version      0.2.0
// @description  Copernicus Browser UI for the original local Python JANUS Geo Probe
// @match        https://browser.dataspace.copernicus.eu/*
// @match        https://dataspace.copernicus.eu/browser/*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-idle
// ==/UserScript==

(() => {
  "use strict";

  if (window.__JANUS_GEO_PROBE_PY__) return;
  window.__JANUS_GEO_PROBE_PY__ = true;

  const API = "http://127.0.0.1:8765";
  const $ = (s, root = document) => root.querySelector(s);

  const css = document.createElement("style");

  css.textContent = `
  #janus-py {
    position:fixed;
    z-index:999999;
    right:18px;
    top:90px;
    width:min(390px,calc(100vw - 24px));
    max-height:calc(100vh - 110px);
    overflow:auto;
    background:#101923;
    color:#eaf1f6;
    border:1px solid #526a7c;
    border-radius:12px;
    box-shadow:0 12px 40px #0009;
    font:13px/1.45 system-ui,sans-serif
  }

  #janus-py * {
    box-sizing:border-box
  }

  #janus-py header {
    padding:12px;
    background:#1b2b39;
    display:flex;
    justify-content:space-between;
    cursor:move
  }

  #janus-py .body {
    padding:12px
  }

  #janus-py .grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px
  }

  #janus-py label {
    display:block;
    color:#aec0cc;
    font-size:11px
  }

  #janus-py input,
  #janus-py select,
  #janus-py button {
    width:100%;
    padding:8px;
    border-radius:7px;
    border:1px solid #536a7b;
    background:#1b2b39;
    color:inherit;
    font:inherit
  }

  #janus-py button {
    cursor:pointer
  }

  #janus-py .full {
    grid-column:1/-1
  }

  #janus-py .run {
    margin-top:10px;
    background:#146f64;
    font-weight:700
  }

  #janus-py .status {
    margin:10px 0;
    padding:9px;
    background:#1b2b39;
    border-radius:7px;
    overflow-wrap:anywhere
  }

  #janus-py pre {
    white-space:pre-wrap;
    overflow-wrap:anywhere;
    max-height:300px;
    overflow:auto;
    background:#0b1219;
    padding:9px;
    border-radius:7px;
    font-size:10px
  }

  #janus-py .actions {
    display:flex;
    gap:7px
  }

  #janus-py .actions > * {
    flex:1
  }
  `;

  document.head.appendChild(css);

  const panel = document.createElement("section");

  panel.id = "janus-py";

  panel.innerHTML = `
    <header id="jpy-drag">
      <strong>🌍 JANUS GEO PROBE · PYTHON</strong>
      <button id="jpy-close" style="width:auto">×</button>
    </header>

    <div class="body">

      <div class="grid">

        <div>
          <label>Latitude WGS84</label>
          <input id="jpy-lat"
                 type="number"
                 step="any"
                 placeholder="Latitude">
        </div>

        <div>
          <label>Longitude WGS84</label>
          <input id="jpy-lon"
                 type="number"
                 step="any"
                 placeholder="Longitude">
        </div>

        <div>
          <label>Radius (m)</label>
          <input id="jpy-radius"
                 type="number"
                 min="1"
                 value="500">
        </div>

        <div>
          <label>Crop focus</label>
          <select id="jpy-crop">
            <option>generic</option>
            <option>cacao</option>
            <option>coffee</option>
          </select>
        </div>

        <div class="full">
          <label>Label / asset key</label>
          <input id="jpy-label"
                 placeholder="Optional site or parcel name">
        </div>

      </div>

      <button class="run" id="jpy-run">
        Run original Python Geo Probe
      </button>

      <div class="status" id="jpy-status">
        Checking local Python bridge…
      </div>

      <pre id="jpy-output">No probe results yet.</pre>

      <div class="actions">
        <button id="jpy-copy" disabled>Copy JSON</button>
        <button id="jpy-save" disabled>Download JSON</button>
      </div>

      <p style="font-size:10px;color:#9db0bf">
        Calls janus.geo_probe on your machine.
        Optional Python-side LLM/transformer enrichment
        stays local to the Python environment.
      </p>

    </div>
  `;

  document.body.appendChild(panel);

  const status = $("#jpy-status", panel);
  const output = $("#jpy-output", panel);

  let latest = null;

  // HTTP communication with the local Python bridge.

  function request(method, path, data) {

    return new Promise((resolve, reject) => {

      GM_xmlhttpRequest({

        method,
        url: API + path,

        headers: {
          "Content-Type": "application/json"
        },

        data: data === undefined
          ? undefined
          : JSON.stringify(data),

        timeout: 120000,

        onload: response => {

          let json;

          try {
            json = JSON.parse(response.responseText);
          } catch {
            return reject(
              new Error("Invalid JSON from Python bridge")
            );
          }

          if (
            response.status >= 200 &&
            response.status < 300
          ) {
            resolve(json);
          } else {
            reject(
              new Error(
                json.error || `HTTP ${response.status}`
              )
            );
          }

        },

        onerror: () => reject(
          new Error(
            "Cannot reach local Python bridge at " + API
          )
        ),

        ontimeout: () => reject(
          new Error("Python bridge request timed out")
        )

      });

    });

  }

  // Import coordinates from URL parameters if present.

  function readUrlCoords() {

    const params = new URLSearchParams(location.search);

    const lat =
      params.get("lat") ??
      params.get("latitude");

    const lon =
      params.get("lng") ??
      params.get("lon") ??
      params.get("longitude");

    if (lat !== null && lon !== null) {

      $("#jpy-lat", panel).value = lat;
      $("#jpy-lon", panel).value = lon;

    }

  }

  readUrlCoords();

  // Check Python service availability.

  request("GET", "/health")
    .then(result => {

      status.textContent =
        `Python bridge connected · ${result.core} · ` +
        `enrichment ${
          result.python_enricher
            ? "configured"
            : "not configured"
        }`;

    })
    .catch(error => {

      status.textContent =
        error.message +
        " — start the Python bridge first.";

    });

  // Execute the original Python Geo Probe.

  $("#jpy-run", panel).addEventListener(
    "click",
    async () => {

      const payload = {

        latitude: Number(
          $("#jpy-lat", panel).value
        ),

        longitude: Number(
          $("#jpy-lon", panel).value
        ),

        radius_m: Number(
          $("#jpy-radius", panel).value
        ),

        label: $("#jpy-label", panel).value,

        crop_type: $("#jpy-crop", panel).value,

        query_live_stac: true,

        run_enrichment: true

      };

      status.textContent =
        "Running original Python Geo Probe…";

      output.textContent = "";

      $("#jpy-copy", panel).disabled = true;
      $("#jpy-save", panel).disabled = true;

      try {

        const response = await request(
          "POST",
          "/api/probe",
          payload
        );

        latest = response.result;

        output.textContent = JSON.stringify(
          response,
          null,
          2
        );

        status.textContent =
          "Python probe completed · " +
          (
            latest.geo_coordinate
              ?.copernicus_stac
              ?.scene_count ?? 0
          ) +
          " STAC scene(s)";

        $("#jpy-copy", panel).disabled = false;
        $("#jpy-save", panel).disabled = false;

      } catch (error) {

        status.textContent =
          "Probe error: " + error.message;

      }

    }
  );

  // Copy result JSON.

  $("#jpy-copy", panel).addEventListener(
    "click",
    async () => {

      if (!latest) return;

      try {

        await navigator.clipboard.writeText(
          JSON.stringify(latest, null, 2)
        );

        status.textContent = "JSON copied.";

      } catch {

        status.textContent =
          "Clipboard permission unavailable.";

      }

    }
  );

  // Download result JSON.

  $("#jpy-save", panel).addEventListener(
    "click",
    () => {

      if (!latest) return;

      const blob = new Blob(
        [JSON.stringify(latest, null, 2)],
        {type: "application/json"}
      );

      const link = document.createElement("a");

      link.href = URL.createObjectURL(blob);
      link.download = "janus-geo-probe.json";

      link.click();

      URL.revokeObjectURL(link.href);

    }
  );

  // Close panel.

  $("#jpy-close", panel).addEventListener(
    "click",
    () => panel.remove()
  );

  // Draggable panel.

  const bar = $("#jpy-drag", panel);

  let drag = null;

  bar.addEventListener("pointerdown", event => {

    if (event.target.closest("button")) return;

    const rect = panel.getBoundingClientRect();

    drag = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };

    bar.setPointerCapture(event.pointerId);

  });

  bar.addEventListener("pointermove", event => {

    if (!drag) return;

    panel.style.left =
      Math.max(0, event.clientX - drag.x) + "px";

    panel.style.top =
      Math.max(0, event.clientY - drag.y) + "px";

    panel.style.right = "auto";

  });

  bar.addEventListener("pointerup", () => {
    drag = null;
  });

})();
