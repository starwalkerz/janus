#### name: "open-dataset-lineage-and-series-integrity-yardstick"
description: "Mechanistic JANUS port of gs-quant-overview time-series dataset queries (replacing proprietary Marquee Dataset.get_data() calls with verified open registries—FRED, ECB SDW, Eurostat, SEC EDGAR XBRL, and national statistical offices): enforcing primary-source provenance, observation continuity without missing-bar gaps, and point-in-time vintage immunity against retroactive data revisions and look-ahead bias."

#### Open Dataset Lineage & Series Integrity Yardstick

You are reading the tick against **time-series provenance, observation
continuity, and point-in-time vintage integrity**—the open-source,
zero-Marquee mechanistic port of gs-quant-overview dataset ingestion
(datasets.md). 

Where proprietary quant toolkits query vendor-hosted data catalogs
(Dataset("EDRVOL_PERCENT_INTRADAY").get_data(...)) behind institutional
subscriptions, JANUS sources all historical and macro-financial time
series directly from **primary public statistical authorities** (FRED,
ECB SDW, Eurostat, SEC EDGAR XBRL, Tilastokeskus, Fingrid),
complementing telemetry-integrity-and-error-circuit-yardstick and
self-referential-simulacrum-and-narcissus-drift-yardstick: 

1. **Primary-Source Provenance (Authoritative Lineage):**
Every series must trace directly to its primary issuing registry or
central bank rather than unverified secondary aggregators or
synthetically interpolated proxies (Clive W. J. Granger & Paul
Newbold, *Forecasting Economic Time Series*, 1977).
2. **Observation Continuity & Gap Density (Sampling Integrity):**
Missing trading bars, irregular sampling intervals, or unannounced
series discontinuations distort rolling volatility, covariance, and
causal discovery inside AGOP (:8000), KAIROS (:8300), and
Causalitybot (Donald B. Rubin, *"Inference and Missing Data,"*
Biometrika 63(3), 581–592, 1976).
3. **Point-in-Time Vintage & Revision Immunity (Look-Ahead Guard):**
Macroeconomic and corporate accounting series frequently undergo
retroactive restatements (ALFRED vintage revisions, SEC
restated filings). Evaluating signals on revised historical numbers
unavailable at the time of decision introduces severe look-ahead
bias (Dean Croushore & Tom Stark, *"A Real-Time Data Set for
Macroeconomists,"* Journal of Econometrics 105(1), 111–130, 2001).

Classifying time-series quality across these three dimensions separates
four dataset-integrity regimes: 

* **Primary Vintage Verified (PRIMARY_VINTAGE_VERIFIED):** Direct
authoritative registry lineage, continuous gap-free observation
window, and point-in-time vintage lock with minimal restatement drift
(1.0 pass).
* **Minor Gap or Revision Lag (MINOR_GAP_OR_REVISION_LAG):** Valid
primary series with minor holiday/calendar alignment gaps or routine
small statistical revisions (0.65 cap).
* **Secondary Proxy or Gapped Series (SECONDARY_PROXY_OR_GAPPED_SERIES):**
Reliance on secondary scraped mirrors, >5% missing observations, or
material retroactive restatements (0.25 cap).
* **Unverified or Look-Ahead Corrupted (UNVERIFIED_OR_LOOKAHEAD_CORRUPTED):**
Unattributed synthetic series, broken/discontinued feed, or severe
restatement distortion (0.10 cap, halving to 0.05 under
persistent series corruption).

Your job is to classify the underlying dataset lineage and series
integrity regime and cap your delta accordingly. You do not invent
trades. You do not override AGOP. You modulate the LLM's delta within
the bound the verifier already permits. You never raise delta above
the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["dataset_lineage"] (keyed by target ID or
dataset slug, with fallback to "global_baseline"). Use the
qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher populates snapshot.external_data["dataset_lineage"] from
open-registry metadata and stirpes_lens provenance checks. Each
entry supplies: 

* primary_provenance_score: score (0 to 100) measuring direct
cryptographic/HTTPS provenance from an official issuing authority
(SEC, ECB, FRED, Eurostat, Fingrid, Tilastokeskus) versus
unverified third-party mirrors or synthetic proxies (100 = direct
primary issuing authority with immutable series ID; 0 = unattributed
or synthetically backfilled series).
* series_missing_gap_pct: percentage (0.0 to 100.0) of expected
scheduled observations missing, duplicated, or NaN-padded across the
lookback window (0.0 = continuous, gap-free series; >= 10.0 =
severely fragmented time series).
* vintage_revision_drift_score: score (0 to 100) measuring
point-in-time stability versus retroactive restatement magnitude
(0 = immutable point-in-time vintage with zero retroactive drift;
100 = heavy retroactive restatements creating look-ahead distortion).
* consecutive_series_corruption_ticks: integer (0 to 50)
counting consecutive settled periods in which
primary_provenance_score < 40 OR series_missing_gap_pct >= 10.0
OR vintage_revision_drift_score >= 70.

If snapshot.external_data["dataset_lineage"] is absent or empty,
treat the dataset as **unmonitored**, record state
**MINOR_GAP_OR_REVISION_LAG**, note that no dataset lineage metadata
was available, and do not cite this skill. 

#### Reading 1 — Primary-Source Provenance (primary_provenance_score)

Evaluate issuing-authority authenticity and lineage depth: 

primary_provenance_score (0–100)Provenance Lineage Tier
**>= 80**
**official_primary_registry** — direct feed from central bank, statistical office, or SEC
**55 to 79**
**curated_open_aggregator** — verified open mirror (FRED, DBnomics) preserving source IDs
**35 to 54**
**unverified_secondary_scrape** — third-party scrape or interpolated proxy lacking source audit
**< 35**
**opaque_or_synthetic_series** — unattributed feed or synthetically backfilled history

If primary_provenance_score is missing, treat as
**curated_open_aggregator**. 

#### Reading 2 — Observation Continuity & Gap Density (series_missing_gap_pct)

Evaluate sampling completeness across the active estimation window: 

series_missing_gap_pct (0–100%)Series Continuity Tier
**< 1.0**
**continuous_gap_free** — complete scheduled observations with clean calendar alignment
**1.0 to 4.9**
**minor_calendar_gaps** — isolated holiday or timezone alignment gaps
**5.0 to 9.9**
**material_missing_bars** — recurring observation dropouts degrading rolling estimators
**>= 10.0**
**fragmented_or_discontinued** — severe data holes or discontinued series

If series_missing_gap_pct is missing, treat as
**minor_calendar_gaps**. 

#### Reading 3 — Point-in-Time Vintage & Revision Stability (vintage_revision_drift_score)

Evaluate immunity against retroactive restatements and look-ahead bias: 

vintage_revision_drift_score (0–100)Vintage Stability Tier
**< 25**
**immutable_point_in_time** — finalized market/registry prints with negligible restatement
**25 to 49**
**routine_benchmark_revision** — standard seasonal or preliminary-to-final adjustment
**50 to 69**
**elevated_restatement_drift** — frequent retroactive revisions shifting historical signals
**>= 70**
**severe_lookahead_distortion** — heavy ex-post restatements invalidating historical calibration

If vintage_revision_drift_score is missing, treat as
**routine_benchmark_revision**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four dataset-lineage regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **UNVERIFIED_OR_LOOKAHEAD_CORRUPTED** (opaque source, fragmented series, or severe restatement)
2. **SECONDARY_PROXY_OR_GAPPED_SERIES** (unverified scrape, material gaps, or elevated restatements)
3. **PRIMARY_VINTAGE_VERIFIED** (official registry, gap-free continuity, immutable vintage)
4. **MINOR_GAP_OR_REVISION_LAG** (curated open mirror with minor gaps or routine revisions)

#### UNVERIFIED_OR_LOOKAHEAD_CORRUPTED

Any of the following hold: 

* Provenance Lineage Tier is **opaque_or_synthetic_series** (< 35).
* Series Continuity Tier is **fragmented_or_discontinued** (>= 10.0%).
* Vintage Stability Tier is **severe_lookahead_distortion** (>= 70).

**Delta cap: 0.10.** The underlying dataset lacks verified primary
provenance, suffers severe missing-bar fragmentation, or exhibits
heavy retroactive restatement bias. Clamp sizing sharply (0.10). 

#### SECONDARY_PROXY_OR_GAPPED_SERIES

Any of the following hold (and UNVERIFIED_OR_LOOKAHEAD_CORRUPTED does
not apply): 

* Provenance Lineage Tier is **unverified_secondary_scrape**
(35 to 54).
* Series Continuity Tier is **material_missing_bars** (5.0 to 9.9%).
* Vintage Stability Tier is **elevated_restatement_drift** (50 to 69).

**Delta cap: 0.25.** Secondary scraped proxies, recurring missing bars,
or elevated restatement drift degrade statistical confidence; trim
sizing to 0.25. 

#### PRIMARY_VINTAGE_VERIFIED

All of the following hold (and neither
UNVERIFIED_OR_LOOKAHEAD_CORRUPTED nor
SECONDARY_PROXY_OR_GAPPED_SERIES applies): 

* Provenance Lineage Tier is **official_primary_registry** (>= 80).
* Series Continuity Tier is **continuous_gap_free** (< 1.0%).
* Vintage Stability Tier is **immutable_point_in_time** (< 25).

**Delta cap: 1.0.** Direct authoritative open-registry lineage,
continuous gap-free bars, and point-in-time vintage lock are verified.
The cap equals the strategy cap (1.0); the skill never binds on
PRIMARY_VINTAGE_VERIFIED. 

#### MINOR_GAP_OR_REVISION_LAG
Any combination not covered above (including curated_open_aggregator
55 to 79 paired with minor_calendar_gaps 1.0 to 4.9% and
routine_benchmark_revision 25 to 49).
Delta cap: 0.65. Valid open-data series with minor calendar gaps or
routine statistical revisions; permit disciplined sizing up to 0.65.

Secondary Filter / Asymmetric Gate — Chronic Series Degradation Hysteresis

Apply the persistence test after regime classification and before the
cap.
Dataset corruption is structurally entrenched if
consecutive_series_corruption_ticks >= 4 (four or more consecutive
settled periods in which primary_provenance_score < 40 OR
series_missing_gap_pct >= 10.0 OR
vintage_revision_drift_score >= 70). Multi-period series gaps or
unverified feed persistence requires halving exposure until primary
series continuity is restored.
If the condition is structurally entrenched, halve the regime's
delta cap:
• MINOR_GAP_OR_REVISION_LAG cap of 0.65 becomes 0.325.
• SECONDARY_PROXY_OR_GAPPED_SERIES cap of 0.25 becomes 0.125.
• UNVERIFIED_OR_LOOKAHEAD_CORRUPTED cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read dataset lineage dict. From
snapshot.external_data["dataset_lineage"], load
primary_provenance_score, series_missing_gap_pct,
vintage_revision_drift_score, and
consecutive_series_corruption_ticks for the target key (falling
back to "global_baseline" if target key is absent). If the entire
dict is absent or empty, record MINOR_GAP_OR_REVISION_LAG, note
the omission, and do not cite this skill.
2. Classify primary-source provenance. Apply Reading 1.
3. Classify observation continuity & gap density. Apply Reading 2.
4. Classify point-in-time vintage stability. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(UNVERIFIED_OR_LOOKAHEAD_CORRUPTED →
SECONDARY_PROXY_OR_GAPPED_SERIES → PRIMARY_VINTAGE_VERIFIED →
MINOR_GAP_OR_REVISION_LAG).
6. Apply persistence test. If
consecutive_series_corruption_ticks >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"open-dataset-lineage-and-series-integrity-yardstick" in
skills_cited and state the provenance score, missing gap
percentage, vintage drift score, and persistence ticks in the
rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.25, "confidence": 0.87, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"SECONDARY_PROXY_OR_GAPPED_SERIES regime; primary_provenance_score=48 (unverified_secondary_scrape), series_missing_gap_pct=6.4 (material_missing_bars), vintage_revision_drift_score=32 (routine_benchmark_revision), consecutive_series_corruption_ticks=0; capping delta at 0.25; open-dataset-lineage-and-series-integrity-yardstick."
• skills_cited: list of skill names; include
"open-dataset-lineage-and-series-integrity-yardstick" only when the
cap bound (intended delta > delta_cap).

Worked Examples


Case A — Official primary registry with gap-free continuity and immutable vintage, cap does not bind

Snapshot:
• primary_provenance_score = 95
• series_missing_gap_pct = 0.0
• vintage_revision_drift_score = 8
• consecutive_series_corruption_ticks = 0
Readings:
• Provenance Lineage Tier: official_primary_registry
• Series Continuity Tier: continuous_gap_free
• Vintage Stability Tier: immutable_point_in_time
Regime: PRIMARY_VINTAGE_VERIFIED, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "open-dataset-lineage-and-series-integrity-yardstick".

Case B — Secondary scraped feed with 6.4% missing bars, cap binds at 0.25

Snapshot:
• primary_provenance_score = 48
• series_missing_gap_pct = 6.4
• vintage_revision_drift_score = 32
• consecutive_series_corruption_ticks = 0
Readings:
• Provenance Lineage Tier: unverified_secondary_scrape
• Series Continuity Tier: material_missing_bars
• Vintage Stability Tier: routine_benchmark_revision
Regime: SECONDARY_PROXY_OR_GAPPED_SERIES, delta cap 0.25. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.25 binds.
LLM returns delta = 0.25 and cites "open-dataset-lineage-and-series-integrity-yardstick".

Case C — Discontinued/fragmented series with severe look-ahead restatements for 5 ticks, hysteresis halves cap to 0.05

Snapshot:
• primary_provenance_score = 29
• series_missing_gap_pct = 14.2
• vintage_revision_drift_score = 78
• consecutive_series_corruption_ticks = 5
Readings:
• Provenance Lineage Tier: opaque_or_synthetic_series
• Series Continuity Tier: fragmented_or_discontinued
• Vintage Stability Tier: severe_lookahead_distortion
Regime: UNVERIFIED_OR_LOOKAHEAD_CORRUPTED, base cap 0.10. Persistence: 5 >= 4 → fires, halving cap to 0.05.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.05 binds.
LLM returns delta = 0.05 and cites "open-dataset-lineage-and-series-integrity-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["dataset_lineage"] from
open primary statistical authorities with full ALFRED/XBRL vintage
auditability:
• ALFRED / FRED (ArchivaL Federal Reserve Economic Data):
https://stlouisfed.org (free JSON API providing exact
point-in-time vintage dates realtime_start / realtime_end to
eliminate look-ahead revision bias).
• ECB Statistical Data Warehouse (SDW) & Eurostat:
https://europa.eu and https://europa.eu
(free SDMX/JSON APIs for eurozone yield curves, inflation, and
macroeconomic time series).
• SEC EDGAR (XBRL Company Facts API) & Tilastokeskus (PxWeb):
https://sec.gov and
https://stat.fi (free open JSON APIs preserving original
filing accession dates and statistical release timestamps).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not trust backfilled or retroactively revised macro/accounting
series (vintage_revision_drift_score >= 70) at full position size.
• Do not allow fragmented series (series_missing_gap_pct >= 10.0%) to
pass un-clamped into downstream covariance or causal estimators.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "open-dataset-lineage-and-series-integrity-yardstick"
when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Mechanistic Source (gs-quant-overview datasets.md):
Goldman Sachs gs-quant (Apache-2.0),
gs_quant/skills/gs-quant-overview/datasets.md (catalog series
discovery, date-range queries, and time-series validation),
re-engineered for open ALFRED/FRED, ECB SDW, Eurostat, and
SEC EDGAR XBRL registries.
• Time-Series Econometrics, Missing Data & Point-in-Time Vintages:
Clive W. J. Granger & Paul Newbold, Forecasting Economic Time
Series (Academic Press, 1977); Donald B. Rubin, "Inference and
Missing Data," Biometrika 63(3), 581–592 (1976); Dean Croushore &
Tom Stark, "A Real-Time Data Set for Macroeconomists," Journal of
Econometrics 105(1), 111–130 (2001); cross-referenced by slug with
telemetry-integrity-and-error-circuit-yardstick and
self-referential-simulacrum-and-narcissus-drift-yardstick; Ramadge &
Wonham (1987). Downward-only damping within JANUS invariants I1–I9.