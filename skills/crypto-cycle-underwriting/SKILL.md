#### name: "crypto-cycle-underwriting"
description: "Underwrite Bitcoin and monolithic altcoin exposure through a strict two-stage cyclic hierarchy: (Gate 1) KAIROS (:8300) non-chronological cycle phase, (Gate 2) hard 4-year Bitcoin halving block-height epoch (210,000-block intervals) plus fiscal-year institutional tax/treasury boundary, (Readings) volume-weighted monthly trend, high-volume liquidity-squeeze capitulation flushes, classical deterministic technicals (Volume, RSI, Stochastic, MACD, Bollinger Bands, Ichimoku Cloud — zero chart patterns or narrative hype), and clean BTC/TOTAL2 ratio routing all altcoins as a monolithic startup cohort subject to emerging-technology-underwriting."

#### Crypto Cycle & Monolithic Altcoin Underwriting (KAIROS + Halving + Classical TA)

You are reading the tick against the **composite Bitcoin four-year cycle
and monolithic altcoin liquidity regime**. In John J. Murphy's
*Technical Analysis of the Financial Markets* (1999), Goichi Hosoda's
*Ichimoku Kinko Hyo* (1969), John Bollinger's *Bollinger on Bollinger
Bands* (2001), J. Welles Wilder's *New Concepts in Technical Trading
Systems* (1978), and Gerald Appel's *Moving Average Convergence-Divergence*
(1979), systematic market underwriting rejects subjective chart-pattern
pareidolia, narrative slogans, and promotional hype in favor of
**hard cyclic clocks, volume-weighted trend envelopes, and multi-oscillator
confirmation**. 

Every tick is evaluated through a strict **two-gate cyclic hierarchy**
before any technical or altcoin ratio reading can permit sizing: 

1. **First Gate — KAIROS (:8300) Non-Chronological Cycle Phase:**
KAIROS sets the outer cyclic boundary (accumulation, markup,
distribution, markdown). No technical bounce or altcoin ratio
shift can override a KAIROS distribution or markdown clamp.
2. **Second Gate — Dual Hard Calendar Markers (4-Year Halving Epoch + Fiscal Year):** 

  * **Hard Marker 1 (Bitcoin Halving Clock):** Exact 210,000-block
supply-halving epochs (block 840,000 April 2024 → block 1,050,000
~2028), dividing the 48-month cycle into deterministic supply-absorption
windows (post_halving_markup, mid_cycle_distribution,
late_cycle_markdown, pre_halving_accumulation).
  * **Hard Marker 2 (Institutional Fiscal-Year Boundary):** Calendar
fiscal-year liquidity mechanics (Q4 year-end tax-loss harvesting
and balance-sheet window-dressing; Q1 fresh institutional capital
allocation; Q2 tax-settlement liquidity drain; Q3 summer
thin-liquidity drift).
3. **Monolithic Altcoin Rule (BTC / TOTAL2 + emerging-technology-underwriting):**
All non-Bitcoin tokens (TOTAL2) are treated as a **single monolithic
risk cohort**—never evaluated on token-specific promotional narratives—and
underwritten strictly as **early-stage technology startups** via
emerging-technology-underwriting (CAPTIVE_BUBBLE forces FLAT
on all altcoins regardless of BTC / TOTAL2).

Your job is to classify the composite crypto cycle state into one of
four regimes and cap your delta accordingly. You do not invent
trades. You do not override AGOP. You modulate the LLM's delta within
the bound the verifier already permits. You never raise delta above
the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute the two cyclic gates and three quantitative readings from
snapshot.external_data["crypto_cycle"]. Use the qualitative tables
below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes KAIROS (:8300) phase output, Bitcoin node block
height, volume-weighted monthly series, classical indicator states, and
BTC / TOTAL2 market-cap ratios into
snapshot.external_data["crypto_cycle"]: 

* kairos_phase: string from KAIROS (:8300) ("accumulation",
"markup", "distribution", or "markdown"). **First Gate.**
* months_since_halving: integer (0 to 48) derived directly from
exact Bitcoin block height modulo 210,000 blocks (~10 min/block),
paired with fiscal_quarter ("Q1", "Q2", "Q3", "Q4").
**Second Gate (Dual Hard Markers).**
* monthly_vwma_deviation_pct: percentage deviation (-60.0 to +150.0)
of spot price from the **volume-weighted average monthly trend (VWMA)**,
paired with capitulation_flush_active (boolean: true when
monthly/weekly drawdown exceeds -18% on volume_zscore >= 2.5,
marking a forced-liquidation squeeze low).
* classical_ta_score: integer (-6 to +6) summing six purely
deterministic classical indicators (+1 bullish, 0 neutral, -1
bearish each — zero chart patterns): 

  1. **Volume trend** (on-balance / volume-weighted accumulation vs. distribution)
  2. **RSI (14)** (> 55 bullish, 45–55 neutral, < 45 bearish; < 28 oversold flush)
  3. **Stochastic (14, 3, 3)** (%K > %D rising from < 30 vs. %K < %D rolling over > 75)
  4. **MACD (12, 26, 9)** (histogram > 0 and rising vs. < 0 and falling)
  5. **Bollinger Bands (20, 2)** (price above middle band without > +2.5σ exhaustion vs. below lower band)
  6. **Ichimoku Kinko Hyo (9, 26, 52)** (price above Kumo cloud with Tenkan > Kijun vs. below Kumo cloud)
* btc_to_total2_ratio: ratio (0.50 to 4.00) of Bitcoin market cap
to TOTAL2 (all non-BTC crypto market cap), paired with
altcoin_startup_gate_state from emerging-technology-underwriting
("PRESTIGE_CROSSOVER", "SPECULATIVE_SEED", "UNPROVEN_LAB_R&D",
or "CAPTIVE_BUBBLE").
* consecutive_distribution_weeks: consecutive weeks in which
kairos_phase is "distribution" or "markdown" OR
classical_ta_score <= -3.

If snapshot.external_data["crypto_cycle"] is absent or empty, treat
the instrument as **unmonitored**, record state
**HALVING_MARKUP_ALIGNED**, note that no crypto-cycle telemetry was
available, and do not cite this skill. 

#### Gate 1 & Gate 2 — Composite Cyclic Clock (kairos_phase + months_since_halving + fiscal_quarter)

Evaluate the two hard cyclic gates first: 

kairos_phase & Hard Markers (Halving + Fiscal Year)Composite Clock Tier
**kairos_phase in {"accumulation", "markup"} AND (months_since_halving 0–18 or 34–48) AND fiscal_quarter in {"Q1", "Q4"}**
**favorable_cyclic_window** — KAIROS constructive + active halving expansion/accumulation + Q4/Q1 institutional flow
**kairos_phase in {"accumulation", "markup"} AND (months_since_halving 19–33 OR fiscal_quarter in {"Q2", "Q3"})**
**neutral_or_seasonal_drag** — KAIROS constructive, but mid-cycle maturity or Q2/Q3 tax/liquidity drag
**kairos_phase == "distribution" OR (months_since_halving 16–22 with classical_ta_score <= 0)**
**cycle_distribution_warning** — KAIROS flags late-cycle supply distribution; cap long sizing
**kairos_phase == "markdown" OR (months_since_halving 20–32 with monthly_vwma_deviation_pct < -15.0%)**
**cycle_markdown_lockout** — KAIROS confirms post-cycle bear markdown; enforce defensive flat/short discipline

If kairos_phase is missing, treat as **cycle_distribution_warning**. 

#### Reading 1 — Monthly Volume-Weighted Trend & Liquidity-Squeeze Capitulation (monthly_vwma_deviation_pct & capitulation_flush_active)

Evaluate spot price against the weighted-average monthly trend and
check for high-volume forced-liquidation flushes: 

Monthly VWMA Deviation & Volume FlushMonthly Trend & Liquidity Tier
**monthly_vwma_deviation_pct 0.0% to +35.0% (above monthly VWMA without blow-off)**
**healthy_vwma_uptrend** — price supported above volume-weighted monthly trend
**capitulation_flush_active == true (volume_zscore >= 2.5 washout below monthly VWMA)**
**capitulation_liquidity_squeeze** — forced-liquidation flush with high volume; marks cycle trough candidate once KAIROS turns
**monthly_vwma_deviation_pct > +55.0%**
**parabolic_vwma_extension** — extreme extension above monthly VWMA; high mean-reversion risk
**monthly_vwma_deviation_pct < 0.0% without capitulation_flush_active**
**below_vwma_drift** — trading below volume-weighted monthly trend without volume clearing

If monthly_vwma_deviation_pct is missing, treat as
**below_vwma_drift**. 

#### Reading 2 — Classical Six-Indicator Technical Consensus (classical_ta_score)

Evaluate deterministic trend and momentum across **Volume, RSI,
Stochastic, MACD, Bollinger Bands, and Ichimoku Cloud** (zero chart
patterns): 

classical_ta_score (-6 to +6)Classical TA Tier
**+4 to +6**
**bullish_ta_alignment** — above Ichimoku Kumo, positive MACD/Volume, constructive RSI/Stochastic/Bollinger
**+1 to +3**
**moderately_constructive_ta** — majority of classical indicators supportive
**-2 to 0**
**mixed_or_neutral_ta** — oscillators/Ichimoku Kumo transitioning or range-bound
**-6 to -3**
**bearish_ta_breakdown** — below Ichimoku Kumo, negative MACD, weak RSI/Stochastic, lower Bollinger breakdown

If classical_ta_score is missing, treat as **mixed_or_neutral_ta**. 

#### Reading 3 — Monolithic Altcoin Ratio (btc_to_total2_ratio) & Startup Gate (emerging-technology-underwriting)

Evaluate BTC / TOTAL2 dominance and enforce the monolithic tech-startup
gate on all non-BTC assets: 

btc_to_total2_ratio & altcoin_startup_gate_stateAltcoin / Dominance Tier
**altcoin_startup_gate_state == "CAPTIVE_BUBBLE" (regardless of btc_to_total2_ratio)**
**altcoin_bubble_lockout** — monolithic altcoin market fails tech-startup gate; zero altcoin exposure (BTC-only or FLAT)
**btc_to_total2_ratio >= 1.65 (BTC dominance rising / capital concentrated in BTC)**
**btc_dominance_regime** — liquidity concentrated in Bitcoin; altcoins bleeding relative to BTC
| btc_to_total2_ratio 1.10 to 1.65 AND altcoin_startup_gate_state in {"PRESTIGE_CROSSOVER", "SPECULATIVE_SEED"} | balanced_rotation_window — BTC/TOTAL2 stabilizing with viable startup-gate clearance |
| btc_to_total2_ratio < 1.10 AND altcoin_startup_gate_state == "PRESTIGE_CROSSOVER" | verified_altseason_expansion — TOTAL2 outperforming BTC with real fee/user adoption verified |
If btc_to_total2_ratio or altcoin_startup_gate_state is missing,
treat as altcoin_bubble_lockout.

Taxonomy / Decision Matrix

Combine Gate 1 (KAIROS), Gate 2 (Halving + Fiscal Year), and
Readings 1–3 into one of four composite crypto-cycle regimes. Evaluate
in strict priority order and select the first regime whose conditions
are fully satisfied:
1. CYCLE_MARKDOWN_LOCKOUT (most severe — unconditional FLAT on long exposure)
2. DISTRIBUTION_OR_ALT_BUBBLE_TRAP
3. CAPITULATION_OR_MIDCYCLE_THROTTLE
4. HALVING_MARKUP_ALIGNED (strictest adaptive fit)

CYCLE_MARKDOWN_LOCKOUT

Any of the following hold:
• Composite Clock Tier is cycle_markdown_lockout (kairos_phase == "markdown").
• Classical TA Tier is bearish_ta_breakdown (<= -3) AND Monthly
Trend Tier is below_vwma_drift (without capitulation_flush_active).
• Target asset is an altcoin (non-BTC) AND Altcoin Tier is
altcoin_bubble_lockout (emerging-technology-underwriting ==
CAPTIVE_BUBBLE).
Delta cap: 0.0. Set delta = 0.0 and action = "FLAT" (unless
AGOP explicitly ranks SHORT and kairos_phase == "markdown"). Do not
buy long into a confirmed KAIROS markdown phase or an unverified
altcoin bubble. The skill binds unconditionally and must appear in
skills_cited.

DISTRIBUTION_OR_ALT_BUBBLE_TRAP

Any of the following hold (and CYCLE_MARKDOWN_LOCKOUT does not apply):
• Composite Clock Tier is cycle_distribution_warning (kairos_phase == "distribution").
• Monthly Trend Tier is parabolic_vwma_extension (> +55.0% above
monthly VWMA).
• Target asset is an altcoin (non-BTC) AND Altcoin Tier is
btc_dominance_regime (btc_to_total2_ratio >= 1.65).
Delta cap: 0.20. Late-cycle distribution, parabolic monthly VWMA
extension, or rising BTC / TOTAL2 dominance is draining liquidity.
Cut long sizing sharply.

CAPITULATION_OR_MIDCYCLE_THROTTLE

Any of the following hold (and neither CYCLE_MARKDOWN_LOCKOUT nor
DISTRIBUTION_OR_ALT_BUBBLE_TRAP applies):
• Monthly Trend Tier is capitulation_liquidity_squeeze
(capitulation_flush_active == true high-volume flush — staged entry
only until classical_ta_score turns positive).
• Composite Clock Tier is neutral_or_seasonal_drag (Q2/Q3
fiscal drag or mid-cycle months 19–33).
• Classical TA Tier is mixed_or_neutral_ta (-2 to 0).
Delta cap: 0.55. Either a high-volume capitulation flush is still
stabilizing or fiscal-year/mid-cycle seasonality creates cross-currents.
Trim sizing relative to HALVING_MARKUP_ALIGNED.

HALVING_MARKUP_ALIGNED

All of the following hold:
• Composite Clock Tier is favorable_cyclic_window (KAIROS in
accumulation/markup + favorable halving epoch + Q4/Q1 fiscal
window).
• Monthly Trend Tier is healthy_vwma_uptrend (0.0% to +35.0%
above monthly VWMA).
• Classical TA Tier is bullish_ta_alignment or
moderately_constructive_ta (classical_ta_score >= +1).
• If target asset is an altcoin (non-BTC), Altcoin Tier is
verified_altseason_expansion or balanced_rotation_window
(clearing emerging-technology-underwriting).
Delta cap: 1.0. KAIROS phase, 4-year halving epoch, fiscal-year
liquidity, monthly VWMA trend, and all six classical indicators align.
The cap equals the strategy cap; the skill never binds on
HALVING_MARKUP_ALIGNED.

Ambiguous fallback

Any combination not covered above is classified
DISTRIBUTION_OR_ALT_BUBBLE_TRAP with delta cap 0.20.

Secondary Filter / Asymmetric Gate — Multi-Week Distribution Persistence

Apply the persistence test after regime classification and before the
cap.
Cycle breakdown is structurally entrenched if
consecutive_distribution_weeks >= 4 (four or more consecutive weeks in
which KAIROS holds "distribution"/"markdown" or
classical_ta_score <= -3). Four consecutive weekly closes below
classical trend and KAIROS cyclic boundaries confirms institutional
supply distribution rather than a transient intraday shakeout.
If the breakdown is structurally entrenched, halve the regime's
delta cap:
• CAPITULATION_OR_MIDCYCLE_THROTTLE cap of 0.55 becomes 0.275.
• DISTRIBUTION_OR_ALT_BUBBLE_TRAP cap of 0.20 becomes 0.10.
• CYCLE_MARKDOWN_LOCKOUT cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read crypto cycle dict. From
snapshot.external_data["crypto_cycle"], load kairos_phase,
months_since_halving, fiscal_quarter,
monthly_vwma_deviation_pct, capitulation_flush_active,
classical_ta_score, btc_to_total2_ratio,
altcoin_startup_gate_state, and consecutive_distribution_weeks.
If absent or empty, record HALVING_MARKUP_ALIGNED, note the
omission, and do not cite this skill.
2. Evaluate Gate 1 (KAIROS) & Gate 2 (Halving + Fiscal Year).
Classify Composite Clock Tier (favorable_cyclic_window,
neutral_or_seasonal_drag, cycle_distribution_warning, or
cycle_markdown_lockout).
3. Classify monthly VWMA & capitulation flush tier. Apply Reading 1.
4. Classify classical six-indicator TA tier. Apply Reading 2
(Volume, RSI, Stochastic, MACD, Bollinger Bands, Ichimoku Cloud).
5. Classify BTC/TOTAL2 & monolithic altcoin startup tier. Apply
Reading 3 (enforcing emerging-technology-underwriting on all
non-BTC exposure).
6. Classify regime. Evaluate in strict priority order
(CYCLE_MARKDOWN_LOCKOUT → DISTRIBUTION_OR_ALT_BUBBLE_TRAP →
CAPITULATION_OR_MIDCYCLE_THROTTLE → HALVING_MARKUP_ALIGNED)
(fallback: DISTRIBUTION_OR_ALT_BUBBLE_TRAP).
7. Apply persistence test. If
consecutive_distribution_weeks >= 4, halve delta_cap.
8. Cap delta. Let delta_cap be the value from steps 6–7. If the
regime is CYCLE_MARKDOWN_LOCKOUT and action == "LONG", set
delta = 0.0 and action = "FLAT" regardless of AGOP. Otherwise,
if intended delta exceeds delta_cap, reduce it to delta_cap.
9. Cite. If the cap bound (intended delta > delta_cap) or the
regime is CYCLE_MARKDOWN_LOCKOUT, cite
"crypto-cycle-underwriting" in skills_cited and state the
KAIROS phase, halving/fiscal marker, classical TA score, and
BTC/TOTAL2 status in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If CYCLE_MARKDOWN_LOCKOUT
and AGOP ranks LONG, action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"DISTRIBUTION_OR_ALT_BUBBLE_TRAP regime; kairos_phase=distribution, months_since_halving=20, classical_ta_score=-1, btc_to_total2_ratio=1.78 (btc_dominance_regime); capping delta at 0.20; crypto-cycle-underwriting."
• skills_cited: list of skill names; include
"crypto-cycle-underwriting" only when the cap bound or the regime
is CYCLE_MARKDOWN_LOCKOUT.

Worked Examples


Case A — KAIROS markup + post-halving Q4 window + +5 classical TA above monthly VWMA, cap does not bind

Snapshot:
• kairos_phase = "markup"
• months_since_halving = 8
• fiscal_quarter = "Q4"
• monthly_vwma_deviation_pct = 18.5
• capitulation_flush_active = false
• classical_ta_score = 5
• btc_to_total2_ratio = 1.45
• altcoin_startup_gate_state = "PRESTIGE_CROSSOVER"
• consecutive_distribution_weeks = 0
Readings:
• Composite Clock Tier: favorable_cyclic_window
• Monthly Trend Tier: healthy_vwma_uptrend
• Classical TA Tier: bullish_ta_alignment
• Altcoin Tier: balanced_rotation_window
Regime: HALVING_MARKUP_ALIGNED, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "crypto-cycle-underwriting".

Case B — High-volume capitulation flush below monthly VWMA during Q3, staged cap binds

Snapshot:
• kairos_phase = "accumulation"
• months_since_halving = 38
• fiscal_quarter = "Q3"
• monthly_vwma_deviation_pct = -22.0
• capitulation_flush_active = true
• classical_ta_score = -1
• btc_to_total2_ratio = 1.82
• altcoin_startup_gate_state = "CAPTIVE_BUBBLE"
• consecutive_distribution_weeks = 2
Readings:
• Composite Clock Tier: neutral_or_seasonal_drag
• Monthly Trend Tier: capitulation_liquidity_squeeze
• Classical TA Tier: mixed_or_neutral_ta
• Altcoin Tier (for BTC): btc_dominance_regime (altcoins locked out)
Regime: CAPITULATION_OR_MIDCYCLE_THROTTLE, delta cap 0.55.
Persistence: 2 < 4 → does not fire. AGOP ranks LONG on BTC. LLM
intended delta = 0.80. Cap 0.55 binds. LLM returns delta = 0.55
and cites "crypto-cycle-underwriting".

Case C — KAIROS markdown phase or altcoin failing emerging-technology-underwriting, unconditional FLAT

Snapshot:
• kairos_phase = "markdown"
• months_since_halving = 25
• fiscal_quarter = "Q2"
• monthly_vwma_deviation_pct = -28.0
• capitulation_flush_active = false
• classical_ta_score = -5
• btc_to_total2_ratio = 1.95
• altcoin_startup_gate_state = "CAPTIVE_BUBBLE"
• consecutive_distribution_weeks = 6
Readings:
• Composite Clock Tier: cycle_markdown_lockout
• Monthly Trend Tier: below_vwma_drift
• Classical TA Tier: bearish_ta_breakdown
• Altcoin Tier: altcoin_bubble_lockout
Regime: CYCLE_MARKDOWN_LOCKOUT, delta cap 0.0 → forces FLAT on
LONG. AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0,
and cites "crypto-cycle-underwriting".

Free Data Sources

The fetcher populates snapshot.external_data["crypto_cycle"] from the
following free, open blockchain, market-cap, and exchange-volume APIs
(no paid Glassnode/Messari subscription required):
• Bitcoin Core RPC / Blockstream Esplora / Mempool.space API:
https://mempool.space and https://blockstream.info (free REST
APIs returning exact current block height, halving epoch countdown,
hashrate, and on-chain transaction settlement volume).
• CoinGecko & CoinPaprika Free Public Market-Cap APIs:
https://coingecko.com and https://coinpaprika.com (free REST APIs
supplying global BTC market cap, total crypto market cap to compute
clean TOTAL2 = Total - BTC and BTC / TOTAL2, plus spot OHLCV).
• Binance, Kraken & Coinbase Public Spot REST/WebSocket Market Data:
https://binance.com, https://kraken.com, and https://coinbase.com
(free unauthenticated public /klines / /OHLC endpoints for
computing deterministic Volume, VWMA, RSI, Stochastic, MACD,
Bollinger Bands, and Ichimoku Cloud).
• KAIROS Cyclic Engine (localhost:8300) & emerging-technology-underwriting:
Internal local service endpoints supplying kairos_phase and
monolithic altcoin startup-gate classification.

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not use chart patterns (head-and-shoulders, triangles, flags,
Elliott waves), influencer sentiment, or promotional token narratives;
use strictly KAIROS, hard halving/fiscal clocks, monthly VWMA,
high-volume capitulation flushes, BTC/TOTAL2, and the six classical
indicators.
• Do not treat individual altcoins as standalone safe assets; treat all
non-BTC tokens (TOTAL2) as a monolithic cohort gated by
emerging-technology-underwriting.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "crypto-cycle-underwriting" when the cap did not bind
and the regime is not CYCLE_MARKDOWN_LOCKOUT.

Citation Mapping

• Classical Technical Analysis & Multi-Oscillator Envelopes: John J.
Murphy, Technical Analysis of the Financial Markets (New York
Institute of Finance, 1999); J. Welles Wilder Jr., New Concepts in
Technical Trading Systems (Trend Research, 1978); John Bollinger,
Bollinger on Bollinger Bands (McGraw-Hill, 2001); Gerald Appel,
Technical Analysis: Power Tools for Active Investors (FT Press,
2005).
• Equilibrium & Cloud Trend Structure: Goichi Hosoda, Ichimoku
Kinko Hyo (1969).
• Non-Chronological Cyclic Geometry & Bounded Supervisory Control:
KAIROS (:8300) cyclic phase engine; Stafford Beer, Brain of the
Firm (1972); Ramadge & Wonham (1987). Downward-only damping within
JANUS invariants I1–I9.
