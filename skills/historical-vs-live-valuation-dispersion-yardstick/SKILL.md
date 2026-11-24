#### name: "historical-vs-live-valuation-dispersion-yardstick"
description: "Mechanistic JANUS port of gs-quant-overview PricingContext, HistoricalPricingContext, and PricingFuture result resolution (replacing proprietary Marquee pricing servers with open live-vs-historical distribution checks): comparing live spot quotes against historical valuation regimes, monitoring cross-venue bid-ask spread blowouts, and verifying batch pricing vector completeness to clamp exposure during flash dislocations or illiquid spread spikes."

#### Historical vs. Live Valuation Dispersion Yardstick

You are reading the tick against **live-vs-historical valuation
dispersion, cross-venue bid-ask spread stability, and batch pricing
vector completeness**—the open-source, zero-Marquee mechanistic port of
gs-quant-overview pricing contexts (pricing.md) and future result
resolution (results.md). 

Where proprietary quant toolkits evaluate instruments across
LiveMarket and HistoricalPricingContext(start, end) via vendor-hosted
PricingFuture grids, JANUS compares **real-time spot quotes**
against **settled historical valuation distributions** using open
public market feeds (Stooq, Yahoo Finance, ECB SDW, FRED, Nord Pool), complementing open-dataset-lineage-and-series-integrity-yardstick
and instrument-ontology-and-contract-resolution-yardstick: 

1. **Live Spot vs. Historical Regime Dispersion (Valuation Z-Score):**
Comparing the live quote against its trailing historical distribution
identifies whether current pricing sits inside a normal stationary
regime (|z| < 1.5) or has detached into an extreme tail dislocation
(|z| >= 3.0) where historical covariance and AGOP rankings lose
out-of-sample reliability (Robert F. Engle, *"Autoregressive
Conditional Heteroscedasticity,"* Econometrica 50(4), 987–1007,
1982; Tim Bollerslev, 1986).
2. **Bid-Ask & Cross-Venue Spread Blowout (Execution Friction):**
During liquidity air-pockets, live bid-ask spreads and cross-venue
basis widen sharply relative to trailing medians (Richard Roll,
*"A Simple Implicit Measure of the Effective Bid-Ask Spread in an
Efficient Market,"* Journal of Finance 39(4), 1127–1139, 1984;
Shane A. Corwin & Paul Schultz, 2012). Entering directional size
into a spread blowout locks in immediate execution slippage.
3. **Batch Pricing Vector Completeness (PricingFuture Resolution Analog):**
When evaluating a multi-asset basket, spread pair, or historical
window, incomplete leg resolution (NaN / unresolved legs across the
valuation vector) invalidates relative-value sizing and requires
downward clamping until the full pricing vector settles cleanly.

Classifying live-vs-historical pricing state separates four valuation
regimes: 

* **Aligned Historical Pricing (ALIGNED_HISTORICAL_PRICING):** Live
spot pricing sits within normal historical distribution bounds,
bid-ask spreads match trailing norms, and the full valuation vector
resolves cleanly (1.0 pass).
* **Moderate Valuation Stretch (MODERATE_VALUATION_STRETCH):** Mild
live-vs-historical z-score stretch or slight spread widening with
intact vector resolution (0.60 cap).
* **Spread Blowout or Regime Stretch (SPREAD_BLOWOUT_OR_REGIME_STRETCH):**
Wide bid-ask expansion (>= 2.5x normal), sharp spot-vs-historical
detachment (|z| >= 2.5), or partial missing legs in the pricing
vector (0.25 cap).
* **Flash Dislocation or Broken Quote (FLASH_DISLOCATION_OR_BROKEN_QUOTE):**
Extreme tail dislocation (|z| >= 3.5), severe spread freeze (>= 4.0x),
or corrupted/unresolved pricing vector (0.10 cap, halving to 0.05
under persistent dislocation).

Your job is to classify the target's live-vs-historical valuation
dispersion regime and cap your delta accordingly. You do not invent
trades. You do not override AGOP. You modulate the LLM's delta within
the bound the verifier already permits. You never raise delta above
the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["valuation_dispersion"] (keyed by ticker or
basket ID, with fallback to "global_baseline"). Use the qualitative
tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher populates
snapshot.external_data["valuation_dispersion"] from open live quote
snapshots and trailing historical return/spread series. Each entry
supplies: 

* live_vs_historical_zscore_abs: absolute standard-deviation
distance (0.0 to 10.0) between current live valuation/price
level and its settled trailing historical distribution (< 1.5 =
normal historical range; >= 3.5 = extreme tail dislocation).
* bid_ask_spread_expansion_multiple: ratio (1.0 to 15.0) of
current live bid-ask or cross-venue spread divided by trailing
30-day median spread (1.0 = normal liquidity spread; >= 4.0 =
acute liquidity air-pocket / spread blowout).
* pricing_vector_resolution_pct: percentage (0.0 to 100.0) of
required instrument/historical pricing nodes resolved cleanly without
missing or stale legs (100.0 = complete batch pricing vector;
< 75.0 = partial/broken pricing vector).
* consecutive_dislocation_ticks: integer (0 to 50) counting
consecutive settled periods in which
live_vs_historical_zscore_abs >= 3.0 OR
bid_ask_spread_expansion_multiple >= 3.5 OR
pricing_vector_resolution_pct < 75.0.

If snapshot.external_data["valuation_dispersion"] is absent or empty,
treat the target as **unmonitored**, record state
**MODERATE_VALUATION_STRETCH**, note that no valuation dispersion
telemetry was available, and do not cite this skill. 

#### Reading 1 — Live vs. Historical Distribution Distance (live_vs_historical_zscore_abs)

Evaluate how far live pricing has stretched from its settled historical
context: 

live_vs_historical_zscore_absHistorical Dispersion Tier
**< 1.5**
**within_historical_band** — live quote inside normal stationary range
**1.5 to 2.4**
**moderate_regime_stretch** — elevated directional extension requiring caution
**2.5 to 3.4**
**acute_tail_extension** — outer-tail stretch beyond normal historical calibration
**>= 3.5**
**extreme_flash_dislocation** — violent price detachment from historical regime

If live_vs_historical_zscore_abs is missing, treat as
**moderate_regime_stretch**. 

#### Reading 2 — Bid-Ask & Cross-Venue Spread Expansion (bid_ask_spread_expansion_multiple)

Evaluate live execution friction relative to trailing median spreads: 

bid_ask_spread_expansion_multipleSpread Friction Tier
**< 1.5**
**normal_tight_spread** — live spread aligned with trailing 30-day median
**1.5 to 2.4**
**mild_spread_widening** — modest execution friction during active volatility
**2.5 to 3.9**
**wide_liquidity_gap** — significant spread expansion penalizing market entry
**>= 4.0**
**frozen_spread_blowout** — severe order-book withdrawal / cross-venue fracture

If bid_ask_spread_expansion_multiple is missing, treat as
**mild_spread_widening**. 

#### Reading 3 — Batch Pricing Vector Completeness (pricing_vector_resolution_pct)

Evaluate deterministic resolution across all required pricing legs and
historical dates: 

pricing_vector_resolution_pct (0–100%)Vector Resolution Tier
**>= 98.0**
**complete_pricing_vector** — all live and historical legs resolved cleanly
**85.0 to 97.9**
**minor_leg_omission** — isolated non-critical historical point missing
**75.0 to 84.9**
**partial_vector_degradation** — multiple missing pricing points weakening comparability
**< 75.0**
**broken_pricing_vector** — critical pricing legs unresolved or corrupted

If pricing_vector_resolution_pct is missing, treat as
**minor_leg_omission**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four valuation-dispersion regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **FLASH_DISLOCATION_OR_BROKEN_QUOTE** (extreme z-score, spread blowout, or broken vector)
2. **SPREAD_BLOWOUT_OR_REGIME_STRETCH** (acute tail extension, wide spread, or partial vector)
3. **ALIGNED_HISTORICAL_PRICING** (normal band, tight spread, complete vector)
4. **MODERATE_VALUATION_STRETCH** (mild stretch or minor leg omission)

#### FLASH_DISLOCATION_OR_BROKEN_QUOTE

Any of the following hold: 

* Historical Dispersion Tier is **extreme_flash_dislocation** (>= 3.5).
* Spread Friction Tier is **frozen_spread_blowout** (>= 4.0).
* Vector Resolution Tier is **broken_pricing_vector** (< 75.0).

**Delta cap: 0.10.** Live quotes have detached violently from
historical calibration, bid-ask spreads have blown out, or the batch
pricing vector failed to resolve. Clamp sizing sharply (0.10). 

#### SPREAD_BLOWOUT_OR_REGIME_STRETCH

Any of the following hold (and FLASH_DISLOCATION_OR_BROKEN_QUOTE does
not apply): 

* Historical Dispersion Tier is **acute_tail_extension** (2.5 to 3.4).
* Spread Friction Tier is **wide_liquidity_gap** (2.5 to 3.9).
* Vector Resolution Tier is **partial_vector_degradation**
(75.0 to 84.9%).

**Delta cap: 0.25.** Elevated tail dispersion, wide bid-ask spreads, or
incomplete pricing legs erode execution edge; trim sizing to 0.25. 

#### ALIGNED_HISTORICAL_PRICING

All of the following hold (and neither
FLASH_DISLOCATION_OR_BROKEN_QUOTE nor
SPREAD_BLOWOUT_OR_REGIME_STRETCH applies): 

* Historical Dispersion Tier is **within_historical_band** (< 1.5).
* Spread Friction Tier is **normal_tight_spread** (< 1.5).
* Vector Resolution Tier is **complete_pricing_vector** (>= 98.0%).

**Delta cap: 1.0.** Live spot pricing sits comfortably within its
settled historical distribution with tight spreads and 100% vector resolution. The cap equals the strategy cap (1.0); the skill never
binds on ALIGNED_HISTORICAL_PRICING.

MODERATE_VALUATION_STRETCH

Any combination not covered above (including moderate_regime_stretch
1.5 to 2.4 paired with mild_spread_widening 1.5 to 2.4 and
minor_leg_omission 85.0 to 97.9%).
Delta cap: 0.60. Moderate live-vs-historical extension or slight
spread widening; permit disciplined sizing up to 0.60.

Secondary Filter / Asymmetric Gate — Sustained Dislocation Hysteresis

Apply the persistence test after regime classification and before the
cap.
Valuation dislocation is structurally entrenched if
consecutive_dislocation_ticks >= 4 (four or more consecutive settled
periods in which live_vs_historical_zscore_abs >= 3.0 OR
bid_ask_spread_expansion_multiple >= 3.5 OR
pricing_vector_resolution_pct < 75.0). Multi-period quote dislocation
or chronic spread blowout indicates structural regime fracture.
If the condition is structurally entrenched, halve the regime's
delta cap:
• MODERATE_VALUATION_STRETCH cap of 0.60 becomes 0.30.
• SPREAD_BLOWOUT_OR_REGIME_STRETCH cap of 0.25 becomes 0.125.
• FLASH_DISLOCATION_OR_BROKEN_QUOTE cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read valuation dispersion dict. From
snapshot.external_data["valuation_dispersion"], load
live_vs_historical_zscore_abs,
bid_ask_spread_expansion_multiple, pricing_vector_resolution_pct,
and consecutive_dislocation_ticks for the target key (falling back
to "global_baseline" if target key is absent). If the entire dict is
absent or empty, record MODERATE_VALUATION_STRETCH, note the
omission, and do not cite this skill.
2. Classify live-vs-historical distribution distance. Apply Reading 1.
3. Classify bid-ask & cross-venue spread expansion. Apply Reading 2.
4. Classify batch pricing vector completeness. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(FLASH_DISLOCATION_OR_BROKEN_QUOTE →
SPREAD_BLOWOUT_OR_REGIME_STRETCH → ALIGNED_HISTORICAL_PRICING →
MODERATE_VALUATION_STRETCH).
6. Apply persistence test. If
consecutive_dislocation_ticks >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"historical-vs-live-valuation-dispersion-yardstick" in
skills_cited and state the z-score, spread expansion multiple,
vector resolution percentage, and persistence ticks in the rationale.

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
"SPREAD_BLOWOUT_OR_REGIME_STRETCH regime; live_vs_historical_zscore_abs=2.8 (acute_tail_extension), bid_ask_spread_expansion_multiple=2.9 (wide_liquidity_gap), pricing_vector_resolution_pct=99.0 (complete_pricing_vector), consecutive_dislocation_ticks=1; capping delta at 0.25; historical-vs-live-valuation-dispersion-yardstick."
• skills_cited: list of skill names; include
"historical-vs-live-valuation-dispersion-yardstick" only when the
cap bound (intended delta > delta_cap).

Worked Examples


Case A — Live quote aligned with historical regime, tight spread, and 100% vector resolution, cap does not bind

Snapshot:
• live_vs_historical_zscore_abs = 0.7
• bid_ask_spread_expansion_multiple = 1.1
• pricing_vector_resolution_pct = 100.0
• consecutive_dislocation_ticks = 0
Readings:
• Historical Dispersion Tier: within_historical_band
• Spread Friction Tier: normal_tight_spread
• Vector Resolution Tier: complete_pricing_vector
Regime: ALIGNED_HISTORICAL_PRICING, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "historical-vs-live-valuation-dispersion-yardstick".

Case B — Outer-tail z-score stretch (2.8) + wide liquidity gap (2.9x), cap binds at 0.25

Snapshot:
• live_vs_historical_zscore_abs = 2.8
• bid_ask_spread_expansion_multiple = 2.9
• pricing_vector_resolution_pct = 99.0
• consecutive_dislocation_ticks = 1
Readings:
• Historical Dispersion Tier: acute_tail_extension
• Spread Friction Tier: wide_liquidity_gap
• Vector Resolution Tier: complete_pricing_vector
Regime: SPREAD_BLOWOUT_OR_REGIME_STRETCH, delta cap 0.25. Persistence: 1 < 4 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.25 binds.
LLM returns delta = 0.25 and cites "historical-vs-live-valuation-dispersion-yardstick".

Case C — Flash dislocation + frozen spread blowout persisting for 5 ticks, hysteresis halves cap to 0.05

Snapshot:
• live_vs_historical_zscore_abs = 4.3
• bid_ask_spread_expansion_multiple = 5.1
• pricing_vector_resolution_pct = 68.0
• consecutive_dislocation_ticks = 5
Readings:
• Historical Dispersion Tier: extreme_flash_dislocation
• Spread Friction Tier: frozen_spread_blowout
• Vector Resolution Tier: broken_pricing_vector
Regime: FLASH_DISLOCATION_OR_BROKEN_QUOTE, base cap 0.10. Persistence: 5 >= 4 → fires, halving cap to 0.05.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.05 binds.
LLM returns delta = 0.05 and cites "historical-vs-live-valuation-dispersion-yardstick".

Free Data Sources

The fetcher populates
snapshot.external_data["valuation_dispersion"] by comparing real-time
open market quotes against trailing historical distributions with zero
Marquee keys:
• Stooq & Yahoo Finance Open Quote / OHLCV Feeds:
https://stooq.com and https://yahoo.com (free
endpoints supplying live bid/ask/last quotes alongside trailing
historical OHLCV bars for z-score and Corwin-Schultz spread
estimation).
• ECB Statistical Data Warehouse (SDW) & FRED Daily Yield/FX Series:
https://europa.eu and https://stlouisfed.org
(free APIs anchoring sovereign yield, credit spread, and FX spot-vs-history
dispersion).
• Nord Pool / ENTSO-E Transparency Platform:
https://entsoe.eu (free open API tracking live intraday
power price spikes against historical seasonal distributions).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not enter full-size directional positions during a live bid-ask
spread blowout (bid_ask_spread_expansion_multiple >= 2.5) or extreme
flash dislocation (live_vs_historical_zscore_abs >= 3.5).
• Do not trust partial batch pricing vectors (pricing_vector_resolution_pct < 75.0%)
for relative-value or multi-leg sizing.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "historical-vs-live-valuation-dispersion-yardstick" when
the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Mechanistic Source (gs-quant-overview pricing.md & results.md):
Goldman Sachs gs-quant (Apache-2.0),
gs_quant/skills/gs-quant-overview/pricing.md & results.md
(PricingContext, HistoricalPricingContext, LiveMarket, and
PricingFuture batch result extraction), re-engineered for open
live-vs-historical distribution governance.
• Conditional Volatility & Effective Bid-Ask Spread Econometrics:
Robert F. Engle, "Autoregressive Conditional Heteroscedasticity
with Estimates of the Variance of United Kingdom Inflation,"
Econometrica 50(4), 987–1007 (1982); Richard Roll, "A Simple
Implicit Measure of the Effective Bid-Ask Spread in an Efficient
Market," Journal of Finance 39(4), 1127–1139 (1984); Shane A. Corwin
& Paul Schultz, "A Simple Way to Estimate Bid-Ask Spreads from Daily
High and Low Prices," Journal of Finance 67(2), 719–760 (2012);
cross-referenced by slug with
open-dataset-lineage-and-series-integrity-yardstick and
instrument-ontology-and-contract-resolution-yardstick; Ramadge &
Wonham (1987). Downward-only damping within JANUS invariants I1–I9.