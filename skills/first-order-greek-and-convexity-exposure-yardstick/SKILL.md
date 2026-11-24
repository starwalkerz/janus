#### name: "first-order-greek-and-convexity-exposure-yardstick"
description: "Mechanistic JANUS port of gs-quant-overview measure and risk-measures calculation (replacing proprietary Marquee instrument.calc(IRDelta, IRVega, EqDelta, EqGamma, EqVega) calls with closed-form Black-Scholes-Merton and Hull sensitivity bounds): policing first-order directional delta/duration exposure, second-order short-gamma negative convexity traps, and unhedged vega volatility sensitivity over open yield and implied-volatility feeds."

#### First-Order Greek & Convexity Exposure Yardstick

You are reading the tick against **first-order directional sensitivity
(Delta / Duration), second-order convexity exposure (Gamma /
Bond Convexity), and implied-volatility sensitivity (Vega)**—the
open-source, zero-Marquee mechanistic port of gs-quant-overview
valuation measures (measure.md) and Greek sensitivities
(risk-measures.md). 

Where proprietary quant toolkits invoke server-side risk primitives
(IRDelta, IRVega, EqDelta, EqGamma, EqVega, DollarPrice) on
Marquee clusters, JANUS evaluates **closed-form Taylor-expansion
Greeks** (Black–Scholes–Merton, 1973; John C. Hull, *Options,
Futures, and Other Derivatives*, 11th ed., 2021; Frederick R. Macaulay,
1938) directly over open option-chain, yield-curve, and implied-volatility
feeds (CBOE, Eurex, ECB SDW, FRED), complementing
instrument-ontology-and-contract-resolution-yardstick and
historical-vs-live-valuation-dispersion-yardstick: 

1. **First-Order Sensitivity (Normalized Delta / Effective Duration):**
Measures linear price response 

𝜕V𝜕Sthe fraction with numerator partial cap V and denominator partial cap S end-fraction
𝜕𝑉𝜕𝑆
⁠ or
rate sensitivity 
𝐷mod

=

−1𝑉

𝜕𝑉𝜕𝑦
⁠.
Excessive effective duration or delta leverage amplifies routine
spot/rate noise into outsized portfolio drawdown.
2. **Second-Order Convexity & Short-Gamma Acceleration (Gamma):**
Measures curvature 
Γ

=𝜕2𝑉𝜕𝑆2
⁠.
While positive convexity (long gamma) dampens downside risk,
**negative convexity (short gamma / callable or short-vol exposure)**
causes losses to accelerate non-linearly during gap moves (Nassim N.
Taleb, *Dynamic Hedging*, Wiley, 1997).
3. **Implied-Volatility Exposure (Normalized Vega):**
Measures sensitivity to implied volatility shifts

𝜈

=𝜕𝑉𝜕𝜎
⁠. Carrying heavy
short-vega exposure into elevated VIX/VSTOXX regimes invites
sharp mark-to-market squeezes when volatility spikes.

Classifying Greek and convexity exposure across these three dimensions
separates four sensitivity regimes: 

* **Linear or Positive Convexity Bounded (LINEAR_OR_POSITIVE_CONVEXITY_BOUNDED):**
Moderate effective delta/duration, non-negative gamma/convexity, and
contained vega sensitivity (1.0 pass).
* **Elevated Duration or Moderate Vega (ELEVATED_DURATION_OR_MODERATE_VEGA):**
Extended bond duration (8–14 yrs), moderate long-gamma decay, or
noticeable vega exposure within controlled bounds (0.60 cap).
* **Short-Gamma or High-Vega Exposure (SHORT_GAMMA_OR_HIGH_VEGA_EXPOSURE):**
Material negative convexity (short gamma), ultra-long duration
(15–24 yrs), or heavy implied-volatility sensitivity (0.25 cap).
* **Severe Short-Convexity Squeeze Trap (SEVERE_SHORT_CONVEXITY_SQUEEZE_TRAP):**
Extreme short-gamma acceleration, unhedged short-vega exposure during
volatility expansion, or hyper-duration leverage (0.10 cap, halving
to 0.05 under persistent convexity hazard).

Your job is to classify the position's Greek and convexity sensitivity
regime and cap your delta accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy
cap, and you never invent an action outside allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["greek_convexity"] (keyed by ticker, contract
ID, or portfolio sleeve, with fallback to "global_baseline"). Use the
qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher and local Black–Scholes–Merton / duration calculator
populate snapshot.external_data["greek_convexity"] from open market
curves and option chains. Each entry supplies: 

* effective_duration_or_delta_equiv: normalized first-order
sensitivity (0.0 to 40.0) expressed as effective duration in
years for fixed-income/rate-sensitive assets or equivalent notional
delta multiple (1.0 = unlevered 1x equity delta; 5.0 = 5-year
duration or 5x delta; >= 25.0 = ultra-long duration or extreme
delta leverage).
* net_gamma_convexity_score: score (0 to 100) encoding second-order
curvature (100 = strong positive convexity / long gamma; 50 =
zero-curvature linear 1x spot; < 35 = acute negative convexity /
short-gamma acceleration hazard).
* vega_vol_sensitivity_score: score (0 to 100) measuring
vulnerability to implied-volatility expansion (0 = zero vega or
long-vol protection; 100 = heavy unhedged short-vega exposure).
* consecutive_convexity_hazard_ticks: integer (0 to 50) counting
consecutive settled periods in which
net_gamma_convexity_score < 35 OR
vega_vol_sensitivity_score >= 75 OR
effective_duration_or_delta_equiv >= 25.0.

If snapshot.external_data["greek_convexity"] is absent or empty,
treat the target as **unmonitored**, record state
**ELEVATED_DURATION_OR_MODERATE_VEGA**, note that no Greek/convexity
telemetry was available, and do not cite this skill. 

#### Reading 1 — First-Order Delta / Effective Duration (effective_duration_or_delta_equiv)

Evaluate linear directional and interest-rate sensitivity: 

effective_duration_or_delta_equivFirst-Order Sensitivity Tier
**<= 7.9**
**bounded_linear_or_short_duration** — standard 1x equity delta or short-to-mid duration
**8.0 to 14.9**
**moderate_duration_or_beta** — intermediate rate sensitivity or moderately high beta
**15.0 to 24.9**
**extended_duration_exposure** — long-bond / high-multiple rate sensitivity
**>= 25.0**
**extreme_first_order_leverage** — ultra-long duration or steep delta amplification

If effective_duration_or_delta_equiv is missing, treat as
**moderate_duration_or_beta**. 

#### Reading 2 — Second-Order Gamma & Convexity (net_gamma_convexity_score)

Evaluate curvature protection versus short-gamma acceleration risk: 

net_gamma_convexity_score (0–100)Convexity Curvature Tier
**>= 45**
**linear_or_positive_convexity** — zero negative gamma; linear spot or positive convexity
**35 to 44**
**mild_negative_convexity** — modest short-gamma or callable prepayment drag
**20 to 34**
**material_short_gamma** — accelerating loss curvature during adverse price gaps
**< 20**
**acute_short_gamma_cliff** — severe short-convexity trap prone to non-linear blowup

If net_gamma_convexity_score is missing, treat as
**linear_or_positive_convexity**. 

#### Reading 3 — Implied-Volatility Vega Exposure (vega_vol_sensitivity_score)

Evaluate mark-to-market vulnerability to volatility expansion: 

vega_vol_sensitivity_score (0–100)Vega Sensitivity Tier
**< 30**
**negligible_or_long_vega** — unexposed to vol spikes or protected by long vega
**30 to 54**
**moderate_vega_sensitivity** — manageable implied-volatility mark-to-market noise
**55 to 74**
**elevated_short_vega** — meaningful drawdown risk during volatility regime jumps
**>= 75**
**severe_short_vega_squeeze** — heavy unhedged short-vol exposure

If vega_vol_sensitivity_score is missing, treat as
**moderate_vega_sensitivity**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four Greek-convexity regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **SEVERE_SHORT_CONVEXITY_SQUEEZE_TRAP** (acute short gamma, severe short vega, or extreme duration)
2. **SHORT_GAMMA_OR_HIGH_VEGA_EXPOSURE** (material short gamma, elevated short vega, or extended duration)
3. **LINEAR_OR_POSITIVE_CONVEXITY_BOUNDED** (bounded first-order delta, non-negative convexity, low vega)
4. **ELEVATED_DURATION_OR_MODERATE_VEGA** (moderate duration/vega with benign convexity)

#### SEVERE_SHORT_CONVEXITY_SQUEEZE_TRAP

Any of the following hold: 

* Convexity Curvature Tier is **acute_short_gamma_cliff** (< 20).
* Vega Sensitivity Tier is **severe_short_vega_squeeze** (>= 75).
* First-Order Sensitivity Tier is **extreme_first_order_leverage**
(>= 25.0).

**Delta cap: 0.10.** The position carries acute negative convexity
(short gamma), severe unhedged short-vega exposure, or extreme
duration leverage that accelerates losses non-linearly during market
jumps. Clamp sizing sharply (0.10). 

#### SHORT_GAMMA_OR_HIGH_VEGA_EXPOSURE

Any of the following hold (and SEVERE_SHORT_CONVEXITY_SQUEEZE_TRAP
does not apply): 

* Convexity Curvature Tier is **material_short_gamma** (20 to 34).
* Vega Sensitivity Tier is **elevated_short_vega** (55 to 74).
* First-Order Sensitivity Tier is **extended_duration_exposure**
(15.0 to 24.9).

**Delta cap: 0.25.** Material short-gamma curvature, elevated short
vega, or extended duration exposes capital to sharp second-order
mark-to-market swings; trim sizing to 0.25. 

#### LINEAR_OR_POSITIVE_CONVEXITY_BOUNDED

All of the following hold (and neither
SEVERE_SHORT_CONVEXITY_SQUEEZE_TRAP nor
SHORT_GAMMA_OR_HIGH_VEGA_EXPOSURE applies): 

* First-Order Sensitivity Tier is
**bounded_linear_or_short_duration** (<= 7.9).
* Convexity Curvature Tier is **linear_or_positive_convexity**
(>= 45).
* Vega Sensitivity Tier is **negligible_or_long_vega** (< 30).
Delta cap: 1.0. First-order sensitivity is bounded, convexity is
linear or positive (gamma >= 0), and short-vega exposure is absent.
The cap equals the strategy cap (1.0); the skill never binds on
LINEAR_OR_POSITIVE_CONVEXITY_BOUNDED.

ELEVATED_DURATION_OR_MODERATE_VEGA

Any combination not covered above (including
moderate_duration_or_beta 8.0 to 14.9 paired with
linear_or_positive_convexity >= 45 and
moderate_vega_sensitivity 30 to 54).
Delta cap: 0.60. Moderate duration or implied-volatility sensitivity
without negative-convexity cliffs; permit disciplined sizing up to
0.60.

Secondary Filter / Asymmetric Gate — Sustained Short-Convexity Hysteresis

Apply the persistence test after regime classification and before the
cap.
Sensitivity risk is structurally entrenched if
consecutive_convexity_hazard_ticks >= 4 (four or more consecutive
settled periods in which net_gamma_convexity_score < 35 OR
vega_vol_sensitivity_score >= 75 OR
effective_duration_or_delta_equiv >= 25.0). Multi-period persistence
of unhedged negative convexity or extreme duration signals structural
tail vulnerability.
If the condition is structurally entrenched, halve the regime's
delta cap:
• ELEVATED_DURATION_OR_MODERATE_VEGA cap of 0.60 becomes 0.30.
• SHORT_GAMMA_OR_HIGH_VEGA_EXPOSURE cap of 0.25 becomes 0.125.
• SEVERE_SHORT_CONVEXITY_SQUEEZE_TRAP cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read Greek & convexity dict. From
snapshot.external_data["greek_convexity"], load
effective_duration_or_delta_equiv, net_gamma_convexity_score,
vega_vol_sensitivity_score, and
consecutive_convexity_hazard_ticks for the target key (falling
back to "global_baseline" if target key is absent). If the entire
dict is absent or empty, record
ELEVATED_DURATION_OR_MODERATE_VEGA, note the omission, and do
not cite this skill.
2. Classify first-order delta / effective duration. Apply Reading 1.
3. Classify second-order gamma & convexity. Apply Reading 2.
4. Classify implied-volatility vega exposure. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(SEVERE_SHORT_CONVEXITY_SQUEEZE_TRAP →
SHORT_GAMMA_OR_HIGH_VEGA_EXPOSURE →
LINEAR_OR_POSITIVE_CONVEXITY_BOUNDED →
ELEVATED_DURATION_OR_MODERATE_VEGA).
6. Apply persistence test. If
consecutive_convexity_hazard_ticks >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"first-order-greek-and-convexity-exposure-yardstick" in
skills_cited and state the effective duration/delta, convexity
score, vega score, and persistence ticks in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.25, "confidence": 0.88, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"SHORT_GAMMA_OR_HIGH_VEGA_EXPOSURE regime; effective_duration_or_delta_equiv=18.5 (extended_duration_exposure), net_gamma_convexity_score=28 (material_short_gamma), vega_vol_sensitivity_score=62 (elevated_short_vega), consecutive_convexity_hazard_ticks=1; capping delta at 0.25; first-order-greek-and-convexity-exposure-yardstick."
• skills_cited: list of skill names; include
"first-order-greek-and-convexity-exposure-yardstick" only when the
cap bound (intended delta > delta_cap).

Worked Examples


Case A — Unlevered 1x linear spot equity with zero negative convexity and negligible vega, cap does not bind

Snapshot:
• effective_duration_or_delta_equiv = 1.0
• net_gamma_convexity_score = 50
• vega_vol_sensitivity_score = 5
• consecutive_convexity_hazard_ticks = 0
Readings:
• First-Order Sensitivity Tier: bounded_linear_or_short_duration
• Convexity Curvature Tier: linear_or_positive_convexity
• Vega Sensitivity Tier: negligible_or_long_vega
Regime: LINEAR_OR_POSITIVE_CONVEXITY_BOUNDED, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "first-order-greek-and-convexity-exposure-yardstick".

Case B — Extended duration (18.5 yrs) + material short gamma (28), cap binds at 0.25

Snapshot:
• effective_duration_or_delta_equiv = 18.5
• net_gamma_convexity_score = 28
• vega_vol_sensitivity_score = 62
• consecutive_convexity_hazard_ticks = 1
Readings:
• First-Order Sensitivity Tier: extended_duration_exposure
• Convexity Curvature Tier: material_short_gamma
• Vega Sensitivity Tier: elevated_short_vega
Regime: SHORT_GAMMA_OR_HIGH_VEGA_EXPOSURE, delta cap 0.25. Persistence: 1 < 4 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.25 binds.
LLM returns delta = 0.25 and cites "first-order-greek-and-convexity-exposure-yardstick".

Case C — Acute short-gamma cliff + severe short-vega squeeze persisting for 5 ticks, hysteresis halves cap to 0.05

Snapshot:
• effective_duration_or_delta_equiv = 27.0
• net_gamma_convexity_score = 14
• vega_vol_sensitivity_score = 84
• consecutive_convexity_hazard_ticks = 5
Readings:
• First-Order Sensitivity Tier: extreme_first_order_leverage
• Convexity Curvature Tier: acute_short_gamma_cliff
• Vega Sensitivity Tier: severe_short_vega_squeeze
Regime: SEVERE_SHORT_CONVEXITY_SQUEEZE_TRAP, base cap 0.10. Persistence: 5 >= 4 → fires, halving cap to 0.05.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.05 binds.
LLM returns delta = 0.05 and cites "first-order-greek-and-convexity-exposure-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["greek_convexity"] from
open yield-curve, option-chain, and implied-volatility feeds using
closed-form Black–Scholes–Merton and Macaulay/Modified duration
formulas:
• ECB Statistical Data Warehouse (SDW) & U.S. Treasury / FRED Yield Curves:
https://europa.eu and https://stlouisfed.org
(free open APIs supplying zero-coupon and par yield curves for exact
modified duration and bond convexity calculation).
• CBOE Delayed Volatility Indices (VIX, VVIX, SKEW) & Stooq/Yahoo Option Chains:
https://cboe.com and https://yahoo.com (free
open feeds for implied-volatility surface calibration and closed-form
Delta/Gamma/Vega estimation).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not allow acute short-gamma (net_gamma_convexity_score < 20) or
severe short-vega (vega_vol_sensitivity_score >= 75) exposures to
bypass the 0.10 ceiling.
• Do not ignore effective duration (>= 15.0) on long-dated rate or
high-multiple assets during rate-volatility regimes.
• Do not compute precise floating-point arithmetic inside the LLM prompt;
use the qualitative comparison tables.
• Do not cite "first-order-greek-and-convexity-exposure-yardstick"
when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Mechanistic Source (gs-quant-overview measure.md & risk-measures.md):
Goldman Sachs gs-quant (Apache-2.0),
gs_quant/skills/gs-quant-overview/measure.md & risk-measures.md
(DollarPrice, IRDelta, IRVega, EqDelta, EqGamma, EqVega),
re-engineered for zero-Marquee closed-form Greek and duration bounds.
• Option Sensitivities & Fixed-Income Convexity: Fischer Black &
Myron Scholes, "The Pricing of Options and Corporate Liabilities,"
Journal of Political Economy 81(3), 637–654 (1973); John C. Hull,
Options, Futures, and Other Derivatives, 11th ed. (Pearson, 2021);
Frederick R. Macaulay (1938); Nassim N. Taleb, Dynamic Hedging
(Wiley, 1997); cross-referenced by slug with
instrument-ontology-and-contract-resolution-yardstick and
historical-vs-live-valuation-dispersion-yardstick; Ramadge & Wonham
(1987). Downward-only damping within JANUS invariants I1–I9.