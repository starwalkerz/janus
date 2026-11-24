#### name: "telemetry-integrity-and-error-circuit-yardstick"
description: "Mechanistic JANUS port of gs-quant-overview session, batch-context, and error-handling governance (replacing proprietary GsSession OAuth2/Marquee dependencies with open-source telemetry verification): enforcing feed freshness, schema completeness, NaN/null isolation, and automatic downward-only circuit-breaker clamping whenever upstream data endpoints degrade, drift, or rate-limit."

#### Telemetry Integrity & Error-Circuit Yardstick

You are reading the tick against **session-level telemetry integrity,
timestamp freshness, and deterministic error-circuit governance**—the
open-source, zero-Marquee mechanistic port of gs-quant-overview
session management (SKILL.md) and fault handling (errors.md). 

Where proprietary quant toolkits gate execution behind institutional
OAuth2/Kerberos sessions (GsSession) and vendor-specific exception
wrappers (MqRequestError, MqRateLimitError, MqTimeoutError),
JANUS operates over **open public registries** and enforces
**fail-closed supervisory damping** (Ramadge & Wonham, 1987; Claude
E. Shannon, *"A Mathematical Theory of Communication,"* Bell System
Technical Journal 27, 379–423, 1948) whenever the observation channel
degrades: 

1. **Channel Freshness & Clock-Skew Bound (Temporal Validity):**
Every external snapshot carries an explicit settlement timestamp.
Stale feeds, clock drift between JANUS (:8400), AGOP (:8000), and
KAIROS (:8300), or delayed registry updates degrade effective
channel capacity and require proportional downward sizing caps.
2. **Schema Completeness & NaN / Null Quarantine (Resolution Integrity):**
Partial dictionary resolution, missing target keys, or NaN/Inf
sentinel values inside snapshot.external_data are never imputed
optimistically; missing observations default strictly toward
conservative downward bounds.
3. **Rate-Limit & Upstream Fault Circuit Breaker (Error Hysteresis):**
Consecutive HTTP 429 (rate limit), 5xx (upstream outage), or
schema-validation failures trigger an asymmetric circuit breaker
that clamps directional exposure down to 0.10 (and 0.05 under
sustained outage), ensuring JANUS never trades blind during a
feed failure.

Classifying channel health separates four operational telemetry regimes: 

* **Nominal Channel Integrity (NOMINAL_CHANNEL_INTEGRITY):** Fresh
timestamps, complete target schema resolution, zero NaN/null
sentinels, and zero upstream HTTP/timeout faults (1.0 pass).
* **Degraded Latency or Partial Fallback (DEGRADED_LATENCY_OR_FALLBACK):**
Mild timestamp lag or target key falling back to "global_baseline"
with valid core series (0.60 cap).
* **Rate-Limited or Stale Feed (RATE_LIMITED_OR_STALE_FEED):**
Elevated feed staleness, partial NaN field dropouts, or transient
HTTP 429/timeout retries (0.25 cap).
* **Blind Channel Circuit Break (BLIND_CHANNEL_CIRCUIT_BREAK):**
Severe data staleness, corrupted/missing primary telemetry, or
sustained upstream outage (0.10 cap, halving to 0.05 under
persistent fault hysteresis).

Your job is to classify the telemetry channel's integrity regime and
cap your delta accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy
cap, and you never invent an action outside allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["telemetry_circuit"] (evaluating overall feed
health across JANUS, AGOP, KAIROS, and external fetchers). Use
the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher orchestrator populates
snapshot.external_data["telemetry_circuit"] on every tick (keyed by
target ID or "global_baseline"). Each entry supplies: 

* feed_freshness_score: score (0 to 100) measuring timestamp
recency and clock alignment across services (100 = sub-second /
current settled window with zero clock drift; 0 = severely stale
data or multi-window clock desynchronization).
* schema_completeness_score: score (0 to 100) measuring the
fraction of expected telemetry keys resolved cleanly without NaN,
Inf, null sentinels, or "global_baseline" fallbacks (100 = all
target-specific fields resolved cleanly; 0 = widespread missing or
corrupted fields).
* upstream_error_rate_pct: percentage (0.0 to 100.0) of recent
fetcher calls returning HTTP 429, 5xx, timeout, or parse errors
(0.0 = clean execution; >= 25.0 = acute upstream instability).
* consecutive_fault_ticks: integer (0 to 50) counting consecutive
settled periods in which feed_freshness_score < 40 OR
schema_completeness_score < 40 OR upstream_error_rate_pct >= 25.0.

If snapshot.external_data["telemetry_circuit"] is absent or empty,
treat the channel as **unmonitored**, record state
**DEGRADED_LATENCY_OR_FALLBACK**, note that no telemetry circuit
metadata was available, and do not cite this skill. 

#### Reading 1 — Feed Freshness & Clock Alignment (feed_freshness_score)

Evaluate temporal validity of the settled snapshot: 

feed_freshness_score (0–100)Temporal Validity Tier
**>= 80**
**synchronized_fresh** — current settled window, zero clock drift
**55 to 79**
**acceptable_lag** — minor settlement delay within tolerance
**35 to 54**
**stale_window** — lagged telemetry degrading real-time precision
**< 35**
**expired_or_drifted** — stale snapshot or clock desynchronization

If feed_freshness_score is missing, treat as **acceptable_lag**. 

#### Reading 2 — Schema Completeness & Resolution (schema_completeness_score)

Evaluate deterministic field resolution without NaN or fallback gaps: 

schema_completeness_score (0–100)Resolution Integrity Tier
**>= 80**
**complete_target_resolution** — target-specific fields resolved with zero NaNs
**55 to 79**
**partial_baseline_fallback** — minor non-critical fields using baseline defaults
**35 to 54**
**degraded_sparse_fields** — multiple missing keys or sentinel dropouts
**< 35**
**corrupted_or_empty_payload** — critical telemetry absent or malformed

If schema_completeness_score is missing, treat as
**partial_baseline_fallback**. 

#### Reading 3 — Upstream Error & Rate-Limit Rate (upstream_error_rate_pct)

Evaluate HTTP 429/5xx, timeout, and parser exception density: 

upstream_error_rate_pct (0–100%)Transport Health Tier
**< 5.0**
**clean_transport** — negligible transport or rate-limit retries
**5.0 to 14.9**
**intermittent_retries** — isolated rate limits handled within backoff
**15.0 to 24.9**
**elevated_throttling** — frequent 429/timeout degradation
**>= 25.0**
**upstream_outage** — systemic API failure or severe rate-limit block

If upstream_error_rate_pct is missing, treat as
**intermittent_retries**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four telemetry-circuit regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **BLIND_CHANNEL_CIRCUIT_BREAK** (expired/corrupted data or upstream outage)
2. **RATE_LIMITED_OR_STALE_FEED** (stale window, sparse fields, or elevated throttling)
3. **NOMINAL_CHANNEL_INTEGRITY** (fresh, complete, clean transport)
4. **DEGRADED_LATENCY_OR_FALLBACK** (minor lag or baseline fallback)

#### BLIND_CHANNEL_CIRCUIT_BREAK

Any of the following hold: 

* Temporal Validity Tier is **expired_or_drifted** (< 35).
* Resolution Integrity Tier is **corrupted_or_empty_payload** (< 35).
* Transport Health Tier is **upstream_outage** (>= 25.0%).

**Delta cap: 0.10.** The observation channel is compromised by expired
data, malformed/missing fields, or upstream outage. Clamp sizing
sharply (0.10) so JANUS never allocates blind. 

#### RATE_LIMITED_OR_STALE_FEED

Any of the following hold (and BLIND_CHANNEL_CIRCUIT_BREAK does not
apply): 

* Temporal Validity Tier is **stale_window** (35 to 54).
* Resolution Integrity Tier is **degraded_sparse_fields** (35 to 54).
* Transport Health Tier is **elevated_throttling** (15.0 to 24.9%).

**Delta cap: 0.25.** Feed staleness, sparse resolution, or API
throttling reduces signal fidelity; trim sizing to 0.25 until full
channel synchronization recovers. 

#### NOMINAL_CHANNEL_INTEGRITY

All of the following hold (and neither BLIND_CHANNEL_CIRCUIT_BREAK
nor RATE_LIMITED_OR_STALE_FEED applies): 

* Temporal Validity Tier is **synchronized_fresh** (>= 80).
* Resolution Integrity Tier is **complete_target_resolution** (>= 80).
* Transport Health Tier is **clean_transport** (< 5.0%).

**Delta cap: 1.0.** All upstream registries, clocks, and schemas
resolved cleanly with zero transport degradation. The cap equals the
strategy cap (1.0); the skill never binds on
NOMINAL_CHANNEL_INTEGRITY. 

#### DEGRADED_LATENCY_OR_FALLBACK

Any combination not covered above (including **acceptable_lag**
55 to 79 paired with **partial_baseline_fallback** 55 to 79 and
< 15.0% error rate). 

**Delta cap: 0.60.** Telemetry is valid but relies on mild lag or
"global_baseline" fallbacks; permit disciplined sizing up to 0.60. 

#### Secondary Filter / Asymmetric Gate — Sustained Outage Circuit Hysteresis

Apply the persistence test after regime classification and before the
cap. 

Channel degradation is **chronically faulted** if
consecutive_fault_ticks >= 4 (four or more consecutive settled periods
in which feed_freshness_score < 40 OR schema_completeness_score < 40
OR upstream_error_rate_pct >= 25.0). Multi-period transport or schema
failure requires tightening the circuit breaker until manual or
automated recovery is verified.
If the condition is chronically faulted, halve the regime's delta
cap:
• DEGRADED_LATENCY_OR_FALLBACK cap of 0.60 becomes 0.30.
• RATE_LIMITED_OR_STALE_FEED cap of 0.25 becomes 0.125.
• BLIND_CHANNEL_CIRCUIT_BREAK cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read telemetry circuit dict. From
snapshot.external_data["telemetry_circuit"], load
feed_freshness_score, schema_completeness_score,
upstream_error_rate_pct, and consecutive_fault_ticks for the
target key (falling back to "global_baseline" if target key is
absent). If the entire dict is absent or empty, record
DEGRADED_LATENCY_OR_FALLBACK, note the omission, and do not cite
this skill.
2. Classify feed freshness & clock alignment. Apply Reading 1.
3. Classify schema completeness & resolution. Apply Reading 2.
4. Classify upstream transport error rate. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(BLIND_CHANNEL_CIRCUIT_BREAK → RATE_LIMITED_OR_STALE_FEED →
NOMINAL_CHANNEL_INTEGRITY → DEGRADED_LATENCY_OR_FALLBACK).
6. Apply persistence test. If consecutive_fault_ticks >= 4, halve
delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"telemetry-integrity-and-error-circuit-yardstick" in skills_cited
and state the freshness score, completeness score, error rate, and
fault ticks in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.10, "confidence": 0.90, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"BLIND_CHANNEL_CIRCUIT_BREAK regime; feed_freshness_score=28 (expired_or_drifted), schema_completeness_score=32 (corrupted_or_empty_payload), upstream_error_rate_pct=31.0 (upstream_outage), consecutive_fault_ticks=5 (outage hysteresis halves cap from 0.10 to 0.05); capping delta at 0.05; telemetry-integrity-and-error-circuit-yardstick."
• skills_cited: list of skill names; include
"telemetry-integrity-and-error-circuit-yardstick" only when the cap
bound (intended delta > delta_cap).

Worked Examples


Case A — Fresh, complete, zero-error open telemetry channel, cap does not bind

Snapshot:
• feed_freshness_score = 94
• schema_completeness_score = 92
• upstream_error_rate_pct = 0.5
• consecutive_fault_ticks = 0
Readings:
• Temporal Validity Tier: synchronized_fresh
• Resolution Integrity Tier: complete_target_resolution
• Transport Health Tier: clean_transport
Regime: NOMINAL_CHANNEL_INTEGRITY, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "telemetry-integrity-and-error-circuit-yardstick".

Case B — Stale window + elevated 429 throttling, cap binds at 0.25

Snapshot:
• feed_freshness_score = 46
• schema_completeness_score = 68
• upstream_error_rate_pct = 18.5
• consecutive_fault_ticks = 1
Readings:
• Temporal Validity Tier: stale_window
• Resolution Integrity Tier: partial_baseline_fallback
• Transport Health Tier: elevated_throttling
Regime: RATE_LIMITED_OR_STALE_FEED, delta cap 0.25. Persistence: 1 < 4 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.25 binds.
LLM returns delta = 0.25 and cites "telemetry-integrity-and-error-circuit-yardstick".

Case C — Upstream outage + expired payload persisting for 5 ticks, hysteresis halves cap to 0.05

Snapshot:
• feed_freshness_score = 28
• schema_completeness_score = 32
• upstream_error_rate_pct = 31.0
• consecutive_fault_ticks = 5
Readings:
• Temporal Validity Tier: expired_or_drifted
• Resolution Integrity Tier: corrupted_or_empty_payload
• Transport Health Tier: upstream_outage
Regime: BLIND_CHANNEL_CIRCUIT_BREAK, base cap 0.10. Persistence: 5 >= 4 → fires, halving cap to 0.05.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.05 binds.
LLM returns delta = 0.05 and cites "telemetry-integrity-and-error-circuit-yardstick".

Free Data Sources

The fetcher orchestrator populates
snapshot.external_data["telemetry_circuit"] internally from open
service health checks and public registry HTTP headers:
• Internal JANUS (:8400), AGOP (:8000), KAIROS (:8300) Health & Clock-Skew Probes:
Local /health and NTP offset telemetry ensuring sub-second timestamp
synchronization across the supervisory loop.
• Open Registry HTTP Status, ETag & Last-Modified Headers:
Standard HTTP response metadata from data.sec.gov,
ec.europa.eu/eurostat, api.gdeltproject.org, and api.github.com
tracking freshness and 429/5xx retry ratios with zero paid keys.

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not impute missing or NaN fields optimistically; treat missing
data strictly as degraded resolution.
• Do not allow stale snapshots (feed_freshness_score < 35) to pass at
full sizing during fast market moves.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "telemetry-integrity-and-error-circuit-yardstick" when
the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Mechanistic Source (gs-quant-overview SKILL.md & errors.md):
Goldman Sachs gs-quant (Apache-2.0),
gs_quant/skills/gs-quant-overview/SKILL.md & errors.md (session
lifecycle, batch context governance, and API error/rate-limit
handling), re-engineered for zero-Marquee open registries.
• Information Channel Capacity & Supervisory Control: Claude E.
Shannon, "A Mathematical Theory of Communication," Bell System
Technical Journal 27, 379–423 (1948); Ramadge & Wonham (1987).
Downward-only damping within JANUS invariants I1–I9.