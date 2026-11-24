#### name: "event-trigger-hysteresis-and-backtest-overfit-yardstick"
description: "Mechanistic JANUS port of gs-quant-overview event-driven backtesting architecture (replacing proprietary Marquee PeriodicTrigger, MktTrigger, StrategyRiskTrigger, AddTradeAction, HedgeAction, and GenericEngine simulation with deterministic trigger-hysteresis and out-of-sample overfit governance): policing trigger boundary chatter, execution turnover drag, and Bailey-López de Prado Probability of Backtest Overfitting (PBO) / Deflated Sharpe Ratio (DSR) to clamp curve-fitted strategies before live capital deployment."

#### Event-Trigger Hysteresis & Backtest-Overfit Yardstick

You are reading the tick against **event-trigger hysteresis, turnover
chatter, and out-of-sample backtest overfitting (PBO / DSR)**—the
open-source, zero-Marquee mechanistic port of gs-quant-overview
event-driven strategy backtesting (backtesting.md). 

Where proprietary quant toolkits wire PeriodicTrigger, MktTrigger,
and StrategyRiskTrigger to AddTradeAction and HedgeAction inside
vendor-hosted GenericEngine simulators, JANUS governs **live
trigger transitions** and **strategy statistical validity** without
vendor lock-in, complementing
open-dataset-lineage-and-series-integrity-yardstick and
singular-novelty-and-algorithmic-depth-yardstick: 

1. **Out-of-Sample Statistical Validity (Bailey–López de Prado PBO & DSR):**
Evaluating strategies across multiple parameter trials inflates
in-sample Sharpe ratios via selection bias. Using **Combinatorially
Symmetric Cross-Validation (CSCV)** to estimate the **Probability
of Backtest Overfitting (PBO)** and the **Deflated Sharpe Ratio
(DSR)** separates genuine structural edge from curve-fitted noise
(David H. Bailey, Jonathan M. Borwein, Marcos López de Prado & Qiji
Jim Zhu, *"The Probability of Backtest Overfitting,"* Journal of
Computational Finance 20(4), 39–69, 2017; Bailey & López de Prado,
2014).
2. **Trigger Hysteresis & Chatter Suppression (Schmitt-Trigger Deadband):**
Naive threshold triggers (MktTrigger / StrategyRiskTrigger)
oscillate rapidly whenever an indicator hovers near a decision
boundary, generating excessive turnover (AddTradeAction /
ExitPositionAction whip-saw) and transaction-cost bleed (Otto H.
Schmitt, 1938; Nicolae Gârleanu & Lasse Heje Pedersen, *"Dynamic
Trading with Predictable Returns and Transaction Costs,"* Journal
of Finance 68(6), 2309–2340, 2013).
3. **Trigger-Action Alignment (Risk-Trigger Priority):**
In any event-driven rule hierarchy, protective StrategyRiskTrigger
bounds must strictly dominate periodic or opportunistic entry
triggers (PeriodicTrigger / MktTrigger), guaranteeing
downward-only capital preservation (JANUS Invariants I1–I9).

Classifying trigger stability and out-of-sample validity separates four
execution-governance regimes: 

* **Out-of-Sample Verified & Hysteresis Locked (OOS_VERIFIED_HYSTERESIS_LOCKED):**
Low Probability of Backtest Overfitting (PBO < 0.25), high Deflated
Sharpe confidence, and disciplined trigger deadbands with minimal
chatter (1.0 pass).
* **Moderate Trial Selection or Turnover (MODERATE_TRIAL_SELECTION_OR_TURNOVER):**
Acceptable out-of-sample persistence (PBO 0.25–0.49) with moderate
rebalance frequency or minor threshold sensitivity (0.60 cap).
* **Trigger Chatter or Elevated Overfit (TRIGGER_CHATTER_OR_ELEVATED_OVERFIT):**
High boundary whip-saw turnover or elevated backtest selection bias
(PBO 0.50–0.69) eroding net live expectancy (0.25 cap).
* **Curve-Fitted Mirage or Runaway Churn (CURVE_FITTED_MIRAGE_OR_RUNAWAY_CHURN):**
Severe backtest overfitting (PBO >= 0.70), negative out-of-sample
Deflated Sharpe, or runaway trigger oscillation (0.10 cap, halving
to 0.05 under persistent churn/overfit hysteresis).

Your job is to classify the strategy's trigger hysteresis and
backtest-overfit regime and cap your delta accordingly. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise delta
above the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["backtest_trigger_governance"] (keyed by
strategy ID, AGOP sleeve, or target ticker, with fallback to
"global_baseline"). Use the qualitative tables below. Do not compute
precise arithmetic. 

#### Monitored telemetry fields

The local validation harness and AGOP (:8000) / KAIROS (:8300)
telemetry populate snapshot.external_data["backtest_trigger_governance"].
Each entry supplies: 

* probability_backtest_overfit_pbo: probability (0.0 to 1.0) from
Combinatorially Symmetric Cross-Validation (CSCV) that the active
strategy configuration underperforms the median out-of-sample trial
(< 0.25 = robust out-of-sample edge; >= 0.70 = severe curve-fit
mirage).
* deflated_sharpe_confidence_score: score (0 to 100) measuring
statistical significance of returns after adjusting for trial count,
skewness, kurtosis, and sample length (>= 75 = high statistical
conviction; < 35 = indistinguishable from random trial mining).
* trigger_chatter_turnover_score: score (0 to 100) measuring
boundary whip-saw frequency and transaction-cost drag across
PeriodicTrigger, MktTrigger, and StrategyRiskTrigger state
transitions (0 = clean Schmitt-trigger hysteresis with low friction;
100 = runaway flip-flop churn bleeding execution costs).
* consecutive_overfit_or_churn_ticks: integer (0 to 50) counting
consecutive settled periods in which
probability_backtest_overfit_pbo >= 0.65 OR
trigger_chatter_turnover_score >= 75.

If snapshot.external_data["backtest_trigger_governance"] is absent or
empty, treat the strategy as **unmonitored**, record state
**MODERATE_TRIAL_SELECTION_OR_TURNOVER**, note that no backtest/trigger
telemetry was available, and do not cite this skill. 

#### Reading 1 — Probability of Backtest Overfitting (probability_backtest_overfit_pbo)

Evaluate combinatorially symmetric out-of-sample rank stability: 

probability_backtest_overfit_pbo (0.0–1.0)Overfit Risk Tier
**< 0.25**
**robust_oos_persistence** — strong out-of-sample rank stability across CSCV splits
**0.25 to 0.49**
**moderate_selection_noise** — manageable parameter sensitivity within tolerance
**0.50 to 0.69**
**elevated_overfit_hazard** — frequent out-of-sample rank degradation across trials
**>= 0.70**
**severe_curve_fit_mirage** — high probability of spurious in-sample data mining

If probability_backtest_overfit_pbo is missing, treat as
**moderate_selection_noise**. 

#### Reading 2 — Deflated Sharpe Statistical Conviction (deflated_sharpe_confidence_score)

Evaluate return significance corrected for multiple testing and
non-normality: 

deflated_sharpe_confidence_score (0–100)Deflated Sharpe Tier
**>= 75**
**statistically_significant_edge** — survives multiple-trial and kurtosis deflation
**50 to 74**
**moderate_empirical_support** — positive risk-adjusted edge with moderate trial count
**35 to 49**
**weak_deflated_signal** — borderline significance sensitive to sample window
**< 35**
**noise_indistinguishable** — fails multiple-testing significance threshold

If deflated_sharpe_confidence_score is missing, treat as
**moderate_empirical_support**. 

#### Reading 3 — Trigger Hysteresis & Chatter Churn (trigger_chatter_turnover_score)

Evaluate boundary oscillation and execution-cost drag: 

trigger_chatter_turnover_score (0–100)Trigger Stability Tier
**< 30**
**hysteresis_locked_clean** — disciplined deadbands, low turnover friction
**30 to 54**
**normal_rebalance_cadence** — expected periodic/risk-triggered adjustments
**55 to 74**
**elevated_boundary_chatter** — frequent threshold crossings eroding net alpha
**>= 75**
**runaway_whipsaw_churn** — severe oscillation bleeding transaction costs

If trigger_chatter_turnover_score is missing, treat as
**normal_rebalance_cadence**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four backtest-trigger regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **CURVE_FITTED_MIRAGE_OR_RUNAWAY_CHURN** (severe PBO overfit, noise-level DSR, or runaway churn)
2. **TRIGGER_CHATTER_OR_ELEVATED_OVERFIT** (elevated PBO, weak DSR, or boundary chatter)
3. **OOS_VERIFIED_HYSTERESIS_LOCKED** (robust OOS persistence, significant DSR, clean hysteresis)
4. **MODERATE_TRIAL_SELECTION_OR_TURNOVER** (moderate selection noise and normal rebalance cadence)

#### CURVE_FITTED_MIRAGE_OR_RUNAWAY_CHURN

Any of the following hold: 

* Overfit Risk Tier is **severe_curve_fit_mirage** (>= 0.70).
* Deflated Sharpe Tier is **noise_indistinguishable** (< 35).
* Trigger Stability Tier is **runaway_whipsaw_churn** (>= 75).

**Delta cap: 0.10.** The strategy exhibits severe out-of-sample
overfitting or runaway trigger whip-saw churn. Clamp sizing sharply
(0.10) to prevent live capital erosion from spurious backtest curves
or execution bleed. 

#### TRIGGER_CHATTER_OR_ELEVATED_OVERFIT

Any of the following hold (and
CURVE_FITTED_MIRAGE_OR_RUNAWAY_CHURN does not apply): 

* Overfit Risk Tier is **elevated_overfit_hazard** (0.50 to 0.69).
* Deflated Sharpe Tier is **weak_deflated_signal** (35 to 49).
* Trigger Stability Tier is **elevated_boundary_chatter** (55 to 74).

**Delta cap: 0.25.** Elevated parameter selection bias or frequent
trigger boundary chatter weakens live net expectancy; trim sizing to
0.25. 

#### OOS_VERIFIED_HYSTERESIS_LOCKED

All of the following hold (and neither CURVE_FITTED_MIRAGE_OR_RUNAWAY_CHURN nor
TRIGGER_CHATTER_OR_ELEVATED_OVERFIT applies):
• Overfit Risk Tier is robust_oos_persistence (< 0.25).
• Deflated Sharpe Tier is statistically_significant_edge (>= 75).
• Trigger Stability Tier is hysteresis_locked_clean (< 30).
Delta cap: 1.0. Out-of-sample rank persistence is verified via
CSCV, Deflated Sharpe survives multiple-trial adjustment, and
Schmitt-trigger deadbands prevent whip-saw churn. The cap equals the
strategy cap (1.0); the skill never binds on
OOS_VERIFIED_HYSTERESIS_LOCKED.

MODERATE_TRIAL_SELECTION_OR_TURNOVER

Any combination not covered above (including
moderate_selection_noise 0.25 to 0.49 paired with
moderate_empirical_support 50 to 74 and
normal_rebalance_cadence 30 to 54).
Delta cap: 0.60. Moderate trial selection variance or standard
rebalance turnover; permit disciplined sizing up to 0.60.

Secondary Filter / Asymmetric Gate — Sustained Overfit or Churn Hysteresis

Apply the persistence test after regime classification and before the
cap.
Strategy degradation is structurally entrenched if
consecutive_overfit_or_churn_ticks >= 4 (four or more consecutive
settled periods in which probability_backtest_overfit_pbo >= 0.65 OR
trigger_chatter_turnover_score >= 75). Multi-period persistence of
out-of-sample rank collapse or runaway trigger oscillation requires
halving maximum exposure until strategy parameters are recalibrated.
If the condition is structurally entrenched, halve the regime's
delta cap:
• MODERATE_TRIAL_SELECTION_OR_TURNOVER cap of 0.60 becomes
0.30.
• TRIGGER_CHATTER_OR_ELEVATED_OVERFIT cap of 0.25 becomes
0.125.
• CURVE_FITTED_MIRAGE_OR_RUNAWAY_CHURN cap of 0.10 becomes
0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read backtest & trigger governance dict. From
snapshot.external_data["backtest_trigger_governance"], load
probability_backtest_overfit_pbo,
deflated_sharpe_confidence_score,
trigger_chatter_turnover_score, and
consecutive_overfit_or_churn_ticks for the target key (falling
back to "global_baseline" if target key is absent). If the entire
dict is absent or empty, record
MODERATE_TRIAL_SELECTION_OR_TURNOVER, note the omission, and do
not cite this skill.
2. Classify Probability of Backtest Overfitting (PBO). Apply
Reading 1.
3. Classify Deflated Sharpe (DSR) statistical conviction. Apply
Reading 2.
4. Classify trigger hysteresis & chatter churn. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(CURVE_FITTED_MIRAGE_OR_RUNAWAY_CHURN →
TRIGGER_CHATTER_OR_ELEVATED_OVERFIT →
OOS_VERIFIED_HYSTERESIS_LOCKED →
MODERATE_TRIAL_SELECTION_OR_TURNOVER).
6. Apply persistence test. If
consecutive_overfit_or_churn_ticks >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"event-trigger-hysteresis-and-backtest-overfit-yardstick" in
skills_cited and state the PBO, Deflated Sharpe score, chatter
turnover score, and persistence ticks in the rationale.

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
"TRIGGER_CHATTER_OR_ELEVATED_OVERFIT regime; probability_backtest_overfit_pbo=0.56 (elevated_overfit_hazard), deflated_sharpe_confidence_score=58 (moderate_empirical_support), trigger_chatter_turnover_score=64 (elevated_boundary_chatter), consecutive_overfit_or_churn_ticks=1; capping delta at 0.25; event-trigger-hysteresis-and-backtest-overfit-yardstick."
• skills_cited: list of skill names; include
"event-trigger-hysteresis-and-backtest-overfit-yardstick" only
when the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Low PBO (0.14), high Deflated Sharpe conviction (84), and clean trigger hysteresis, cap does not bind

Snapshot:
• probability_backtest_overfit_pbo = 0.14
• deflated_sharpe_confidence_score = 84
• trigger_chatter_turnover_score = 18
• consecutive_overfit_or_churn_ticks = 0
Readings:
• Overfit Risk Tier: robust_oos_persistence
• Deflated Sharpe Tier: statistically_significant_edge
• Trigger Stability Tier: hysteresis_locked_clean
Regime: OOS_VERIFIED_HYSTERESIS_LOCKED, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "event-trigger-hysteresis-and-backtest-overfit-yardstick".

Case B — Elevated PBO (0.56) + boundary trigger chatter (64), cap binds at 0.25

Snapshot:
• probability_backtest_overfit_pbo = 0.56
• deflated_sharpe_confidence_score = 58
• trigger_chatter_turnover_score = 64
• consecutive_overfit_or_churn_ticks = 1
Readings:
• Overfit Risk Tier: elevated_overfit_hazard
• Deflated Sharpe Tier: moderate_empirical_support
• Trigger Stability Tier: elevated_boundary_chatter
Regime: TRIGGER_CHATTER_OR_ELEVATED_OVERFIT, delta cap 0.25. Persistence: 1 < 4 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.25 binds.
LLM returns delta = 0.25 and cites "event-trigger-hysteresis-and-backtest-overfit-yardstick".

Case C — Curve-fit mirage (PBO 0.81) + runaway trigger churn persisting for 5 ticks, hysteresis halves cap to 0.05

Snapshot:
• probability_backtest_overfit_pbo = 0.81
• deflated_sharpe_confidence_score = 24
• trigger_chatter_turnover_score = 83
• consecutive_overfit_or_churn_ticks = 5
Readings:
• Overfit Risk Tier: severe_curve_fit_mirage
• Deflated Sharpe Tier: noise_indistinguishable
• Trigger Stability Tier: runaway_whipsaw_churn
Regime: CURVE_FITTED_MIRAGE_OR_RUNAWAY_CHURN, base cap 0.10. Persistence: 5 >= 4 → fires, halving cap to 0.05.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.05 binds.
LLM returns delta = 0.05 and cites "event-trigger-hysteresis-and-backtest-overfit-yardstick".

Free Data Sources

The local validation engine and AGOP (:8000) / KAIROS (:8300)
diagnostics populate
snapshot.external_data["backtest_trigger_governance"] from internal
simulation logs and open historical series:
• Internal AGOP (:8000) & KAIROS (:8300) Walk-Forward / CSCV Logs:
Local combinatorial cross-validation splits and trigger transition
counters computed directly on settled open market bars (Stooq,
FRED, ECB SDW).
• stirpes_lens Audit Trail:
Lineage and turnover verification logs tracking historical signal
flip frequency and realized transaction slippage.

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not deploy full size behind high in-sample Sharpe ratios when
probability_backtest_overfit_pbo >= 0.50 or
deflated_sharpe_confidence_score < 50.
• Do not allow boundary-chattering MktTrigger loops
(trigger_chatter_turnover_score >= 55) to bleed capital through
uncontrolled turnover.
• Do not compute precise floating-point arithmetic inside the LLM prompt;
use the qualitative comparison tables.
• Do not cite "event-trigger-hysteresis-and-backtest-overfit-yardstick"
when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Mechanistic Source (gs-quant-overview backtesting.md):
Goldman Sachs gs-quant (Apache-2.0),
gs_quant/skills/gs-quant-overview/backtesting.md (PeriodicTrigger,
MktTrigger, StrategyRiskTrigger, AddTradeAction, HedgeAction,
and GenericEngine event-driven backtest loop), re-engineered for
zero-Marquee trigger hysteresis and out-of-sample overfit defense.
• Backtest Overfitting, Deflated Sharpe & Dynamic Trading Costs:
David H. Bailey, Jonathan M. Borwein, Marcos López de Prado & Qiji
Jim Zhu, "The Probability of Backtest Overfitting," Journal of
Computational Finance 20(4), 39–69 (2017); David H. Bailey & Marcos
López de Prado, "The Deflated Sharpe Ratio: Correcting for Selection
Bias, Backtest Overfitting, and Non-Normality," Journal of Portfolio
Management 40(5), 94–107 (2014); Nicolae Gârleanu & Lasse Heje
Pedersen (2013); Otto H. Schmitt (1938); cross-referenced by slug with
open-dataset-lineage-and-series-integrity-yardstick and
singular-novelty-and-algorithmic-depth-yardstick; Ramadge & Wonham
(1987). Downward-only damping within JANUS invariants I1–I9.