#### name: "instrument-ontology-and-contract-resolution-yardstick"
description: "Mechanistic JANUS port of gs-quant-overview instrument ontology and contract resolution (replacing proprietary Marquee Instrument.resolve() symbology calls with open OpenFIGI, ESMA FIRDS, SEC EDGAR, and GLEIF verification): classifying contract settlement clarity, embedded leverage/convexity complexity, and primary-venue liquidity depth to clamp sizing on opaque OTC wrappers, leveraged traps, and thinly traded tickers."

#### Instrument Ontology & Contract Resolution Yardstick

You are reading the tick against **contract-level ontology, symbology
resolution, embedded leverage, and primary-venue liquidity depth**—the
open-source, zero-Marquee mechanistic port of gs-quant-overview
instrument specification and resolution (instruments.md). 

Where proprietary quant toolkits bind instrument parameters (asset_class,
notional, expiration, payoff_type) via vendor-locked symbology
servers (Instrument.resolve()), JANUS decomposes any tradable
contract into its **irreducible legal and payoff primitives** over open
public registries (OpenFIGI, ESMA FIRDS, SEC EDGAR, GLEIF),
complementing reductio-ad-absurdum-and-first-principles-yardstick and
telemetry-integrity-and-error-circuit-yardstick: 

1. **Symbology & Settlement Clarity (Contractual Determinism):**
Every instrument must resolve unambiguously to a standardized
identifier (FIGI / ISIN / LEI), transparent clearing venue,
and deterministic settlement rule (Ronald H. Coase, *"The Nature of
the Firm,"* 1937; Oliver E. Williamson, *The Economic Institutions of
Capitalism*, 1985). Unresolved OTC wrappers, complex multi-leg
structured notes, or ambiguous synthetic trackers carry severe
counterparty and basis risk.
2. **Embedded Leverage & Payoff Non-Linearity (Tail-Exposure Bound):**
Linear spot equities, unlevered ETFs, and plain-vanilla sovereign
bills exhibit bounded 1x delta response. Embedded derivative
leverage (2x/3x daily-reset ETPs, short-volatility structures,
deep-OTM options, or callable structured products) introduces path
decay and discontinuous jump risk (Fischer Black & Myron Scholes,
1973; Nassim N. Taleb, *Dynamic Hedging*, 1997).
3. **Primary-Venue Liquidity & Market-Impact Depth (Kyle's Lambda):**
Even a clean linear equity becomes hazardous when daily turnover and
order-book depth cannot absorb execution without adverse price
impact (Albert S. Kyle, *"Continuous Auctions and Insider Trading,"*
Econometrica 53(6), 1315–1335, 1985; Yakov Amihud, *"Illiquidity
and Stock Returns,"* Journal of Financial Markets 5(1), 31–56,
2002).

Classifying contract resolution across these three dimensions separates
four instrument-ontology regimes: 

* **Resolved Linear Liquid (RESOLVED_LINEAR_LIQUID):** Unambiguous
FIGI/ISIN resolution on a regulated primary exchange, 1x linear
payoff structure, and deep institutional liquidity (1.0 pass).
* **Listed Convex or Moderate Liquidity (LISTED_CONVEX_OR_MODERATE_LIQUIDITY):**
Cleanly resolved exchange-traded option, moderate-leverage ETP
(<= 2x), or mid-cap equity with adequate but finite book depth
(0.60 cap).
* **Complex Structured or Thin Book (COMPLEX_STRUCTURED_OR_THIN_BOOK):**
Multi-leg structured product, >= 3x daily-reset leveraged ETP,
or thinly traded small-cap with high Amihud illiquidity impact
(0.25 cap).
* **Unresolved or Opaque OTC Trap (UNRESOLVED_OR_OPAQUE_OTC_TRAP):**
Failed FIGI/ISIN resolution, bespoke opaque OTC derivative, or
frozen/halted primary venue (0.10 cap, halving to 0.05 under
persistent resolution/liquidity impairment).

Your job is to classify the target instrument's contract resolution and
structural payoff regime and cap your delta accordingly. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise delta
above the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["instrument_ontology"] (keyed by ticker,
FIGI, or ISIN, with fallback to "global_baseline"). Use the
qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher populates snapshot.external_data["instrument_ontology"]
from open symbology and venue-transparency registries. Each entry
supplies: 

* symbology_settlement_clarity_score: score (0 to 100) measuring
unambiguous OpenFIGI/ISIN/LEI resolution, regulated central
clearing, and transparent contractual terms (100 = primary-listed
standard security with verified FIGI and LEI; 0 = unresolved
ticker or opaque bespoke OTC contract).
* embedded_leverage_factor: numeric multiplier (1.0 to 20.0)
capturing effective notional leverage or non-linear jump sensitivity
(1.0 = unlevered linear spot equity/bond; 2.0 = 2x ETP or
standard delta-one margin; >= 3.0 = 3x+ daily-reset ETP,
short-vol structure, or high-gamma derivative).
* venue_liquidity_depth_score: score (0 to 100) measuring
primary-exchange average daily turnover, bid-ask tightness, and low
Amihud price-impact resilience (100 = Tier-1 deep order book;
0 = halted, delisted, or severely illiquid micro-float).
* consecutive_illiquid_or_unresolved_ticks: integer (0 to 50)
counting consecutive settled periods in which
symbology_settlement_clarity_score < 40 OR
venue_liquidity_depth_score < 35.

If snapshot.external_data["instrument_ontology"] is absent or empty,
treat the instrument as **unmonitored**, record state
**LISTED_CONVEX_OR_MODERATE_LIQUIDITY**, note that no instrument
ontology telemetry was available, and do not cite this skill. 

#### Reading 1 — Symbology & Settlement Clarity (symbology_settlement_clarity_score)

Evaluate deterministic identifier resolution and clearing transparency: 

symbology_settlement_clarity_score (0–100)Contract Resolution Tier
**>= 80**
**unambiguous_cleared_security** — verified FIGI/ISIN/LEI on regulated venue
**55 to 79**
**listed_derivative_or_wrapper** — standardized exchange option or plain ETP
**35 to 54**
**complex_structured_note** — multi-leg payoff, callable wrapper, or cross-listed ADR friction
**< 35**
**unresolved_or_bespoke_otc** — missing registry match or opaque bilateral OTC contract

If symbology_settlement_clarity_score is missing, treat as
**listed_derivative_or_wrapper**. 

#### Reading 2 — Embedded Leverage & Payoff Convexity (embedded_leverage_factor)

Evaluate structural leverage and path-dependent convexity amplification: 

embedded_leverage_factorPayoff Complexity Tier
**<= 1.2**
**linear_unlevered** — 1x direct spot ownership with zero reset decay
**1.3 to 2.4**
**moderate_convex_or_2x** — listed option or 2x structured exposure
**2.5 to 4.9**
**high_leverage_decay** — 3x+ daily-reset ETP or steep short-gamma exposure
**>= 5.0**
**extreme_tail_convexity** — hyper-leveraged derivative prone to discontinuous wipeout

If embedded_leverage_factor is missing, treat as
**moderate_convex_or_2x**. 

#### Reading 3 — Primary-Venue Liquidity Depth (venue_liquidity_depth_score)

Evaluate execution depth and Kyle/Amihud market-impact resilience: 

venue_liquidity_depth_score (0–100)Liquidity Depth Tier
**>= 75**
**deep_tier1_book** — tight spreads, high daily turnover, negligible market impact
**45 to 74**
**moderate_exchange_book** — tradable depth requiring disciplined slice sizing
**30 to 44**
**thin_order_book** — wide spreads and elevated Amihud slippage risk
**< 30**
**illiquid_or_halted** — severely impaired book, trading halt, or delisting risk

If venue_liquidity_depth_score is missing, treat as
**moderate_exchange_book**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four instrument-ontology regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **UNRESOLVED_OR_OPAQUE_OTC_TRAP** (unresolved contract, extreme leverage, or halted book)
2. **COMPLEX_STRUCTURED_OR_THIN_BOOK** (high leverage decay, structured note, or thin liquidity)
3. **RESOLVED_LINEAR_LIQUID** (unambiguous 1x linear security with deep liquidity)
4. **LISTED_CONVEX_OR_MODERATE_LIQUIDITY** (standardized convex/2x or mid-depth listed instrument)

#### UNRESOLVED_OR_OPAQUE_OTC_TRAP

Any of the following hold: 

* Contract Resolution Tier is **unresolved_or_bespoke_otc** (< 35).
* Payoff Complexity Tier is **extreme_tail_convexity** (>= 5.0).
* Liquidity Depth Tier is **illiquid_or_halted** (< 30).

**Delta cap: 0.10.** The contract fails open registry resolution, embeds
extreme tail leverage, or lacks executable market liquidity. Clamp
sizing sharply (0.10) to prevent basis or liquidity traps. 

#### COMPLEX_STRUCTURED_OR_THIN_BOOK

Any of the following hold (and UNRESOLVED_OR_OPAQUE_OTC_TRAP does not
apply): 

* Contract Resolution Tier is **complex_structured_note** (35 to 54).
* Payoff Complexity Tier is **high_leverage_decay** (2.5 to 4.9).
* Liquidity Depth Tier is **thin_order_book** (30 to 44).

**Delta cap: 0.25.** Multi-leg complexity, daily-reset volatility drag,
or thin order-book depth erodes net execution efficiency; trim sizing to
0.25. 

#### RESOLVED_LINEAR_LIQUID

All of the following hold (and neither UNRESOLVED_OR_OPAQUE_OTC_TRAP
nor COMPLEX_STRUCTURED_OR_THIN_BOOK applies): 

* Contract Resolution Tier is **unambiguous_cleared_security**
(>= 80).
* Payoff Complexity Tier is **linear_unlevered** (<= 1.2).
* Liquidity Depth Tier is **deep_tier1_book** (>= 75).
Delta cap: 1.0. The instrument resolves cleanly to a regulated 1x
linear security with deep Tier-1 liquidity. The cap equals the strategy
cap (1.0); the skill never binds on RESOLVED_LINEAR_LIQUID.

LISTED_CONVEX_OR_MODERATE_LIQUIDITY

Any combination not covered above (including
listed_derivative_or_wrapper 55 to 79 paired with
moderate_convex_or_2x 1.3 to 2.4 and moderate_exchange_book
45 to 74).
Delta cap: 0.60. Standardized exchange-traded contract with
moderate convexity or mid-tier liquidity; permit disciplined sizing up
to 0.60.

Secondary Filter / Asymmetric Gate — Sustained Illiquidity or Resolution Failure Hysteresis

Apply the persistence test after regime classification and before the
cap.
Contract impairment is structurally entrenched if
consecutive_illiquid_or_unresolved_ticks >= 4 (four or more
consecutive settled periods in which
symbology_settlement_clarity_score < 40 OR
venue_liquidity_depth_score < 35). Multi-period symbology ambiguity or
chronic illiquidity signals structural delisting or counterparty hazard.
If the condition is structurally entrenched, halve the regime's
delta cap:
• LISTED_CONVEX_OR_MODERATE_LIQUIDITY cap of 0.60 becomes 0.30.
• COMPLEX_STRUCTURED_OR_THIN_BOOK cap of 0.25 becomes 0.125.
• UNRESOLVED_OR_OPAQUE_OTC_TRAP cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read instrument ontology dict. From
snapshot.external_data["instrument_ontology"], load
symbology_settlement_clarity_score, embedded_leverage_factor,
venue_liquidity_depth_score, and
consecutive_illiquid_or_unresolved_ticks for the target key
(falling back to "global_baseline" if target key is absent). If
the entire dict is absent or empty, record
LISTED_CONVEX_OR_MODERATE_LIQUIDITY, note the omission, and do
not cite this skill.
2. Classify symbology & settlement clarity. Apply Reading 1.
3. Classify embedded leverage & payoff convexity. Apply Reading 2.
4. Classify primary-venue liquidity depth. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(UNRESOLVED_OR_OPAQUE_OTC_TRAP → COMPLEX_STRUCTURED_OR_THIN_BOOK
→ RESOLVED_LINEAR_LIQUID → LISTED_CONVEX_OR_MODERATE_LIQUIDITY).
6. Apply persistence test. If
consecutive_illiquid_or_unresolved_ticks >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"instrument-ontology-and-contract-resolution-yardstick" in
skills_cited and state the clarity score, leverage factor,
liquidity depth score, and persistence ticks in the rationale.

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
"COMPLEX_STRUCTURED_OR_THIN_BOOK regime; symbology_settlement_clarity_score=68 (listed_derivative_or_wrapper), embedded_leverage_factor=3.0 (high_leverage_decay), venue_liquidity_depth_score=62 (moderate_exchange_book), consecutive_illiquid_or_unresolved_ticks=0; capping delta at 0.25; instrument-ontology-and-contract-resolution-yardstick."
• skills_cited: list of skill names; include
"instrument-ontology-and-contract-resolution-yardstick" only when
the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Primary-listed 1x equity with verified FIGI/LEI and deep Tier-1 liquidity, cap does not bind

Snapshot:
• symbology_settlement_clarity_score = 96
• embedded_leverage_factor = 1.0
• venue_liquidity_depth_score = 91
• consecutive_illiquid_or_unresolved_ticks = 0
Readings:
• Contract Resolution Tier: unambiguous_cleared_security
• Payoff Complexity Tier: linear_unlevered
• Liquidity Depth Tier: deep_tier1_book
Regime: RESOLVED_LINEAR_LIQUID, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "instrument-ontology-and-contract-resolution-yardstick".

Case B — 3x daily-reset leveraged ETP with volatility decay, cap binds at 0.25

Snapshot:
• symbology_settlement_clarity_score = 68
• embedded_leverage_factor = 3.0
• venue_liquidity_depth_score = 62
• consecutive_illiquid_or_unresolved_ticks = 0
Readings:
• Contract Resolution Tier: listed_derivative_or_wrapper
• Payoff Complexity Tier: high_leverage_decay
• Liquidity Depth Tier: moderate_exchange_book
Regime: COMPLEX_STRUCTURED_OR_THIN_BOOK, delta cap 0.25. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.25 binds.
LLM returns delta = 0.25 and cites "instrument-ontology-and-contract-resolution-yardstick".

Case C — Unresolved OTC structure with chronic illiquidity persisting for 5 ticks, hysteresis halves cap to 0.05

Snapshot:
• symbology_settlement_clarity_score = 24
• embedded_leverage_factor = 6.5
• venue_liquidity_depth_score = 21
• consecutive_illiquid_or_unresolved_ticks = 5
Readings:
• Contract Resolution Tier: unresolved_or_bespoke_otc
• Payoff Complexity Tier: extreme_tail_convexity
• Liquidity Depth Tier: illiquid_or_halted
Regime: UNRESOLVED_OR_OPAQUE_OTC_TRAP, base cap 0.10. Persistence: 5 >= 4 → fires, halving cap to 0.05.
AGOP ranks LONG. LLM intended delta = 0.60. Cap 0.05 binds.
LLM returns delta = 0.05 and cites "instrument-ontology-and-contract-resolution-yardstick".

Free Data Sources

The fetcher populates
snapshot.external_data["instrument_ontology"] from open global
symbology and regulatory transparency endpoints with zero Marquee keys:
• OpenFIGI API (Bloomberg Open Symbology):
https://openfigi.com (free REST API resolving
tickers, ISIN, CUSIP, and SEDOL to canonical FIGI, security
type, and primary exchange codes).
• ESMA Financial Instruments Reference Data System (FIRDS):
https://europa.eu (free open EU MiFID II registry
verifying ISIN, CFI classification codes, leverage/derivative flags,
and regulated trading venues).
• GLEIF Legal Entity Identifier (LEI) API & SEC EDGAR Submissions:
https://gleif.org and https://sec.gov (free open APIs
verifying corporate issuer legal structure and security registration).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not treat a 3x daily-reset ETP or opaque structured note as
equivalent to 1x linear spot equity; enforce COMPLEX_STRUCTURED_OR_THIN_BOOK
(0.25) or UNRESOLVED_OR_OPAQUE_OTC_TRAP (0.10).
• Do not ignore thin order-book liquidity (venue_liquidity_depth_score < 45)
when sizing directional positions.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "instrument-ontology-and-contract-resolution-yardstick"
when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Mechanistic Source (gs-quant-overview instruments.md):
Goldman Sachs gs-quant (Apache-2.0),
gs_quant/skills/gs-quant-overview/instruments.md (instrument class
taxonomy, parameter specification, and symbology resolution),
re-engineered for open OpenFIGI / ESMA FIRDS / GLEIF registries.
• Contract Theory, Market Microstructure & Option Convexity: Ronald
H. Coase, "The Nature of the Firm," Economica 4(16), 386–405
(1937); Albert S. Kyle, "Continuous Auctions and Insider Trading,"
Econometrica 53(6), 1315–1335 (1985); Yakov Amihud, "Illiquidity
and Stock Returns," Journal of Financial Markets 5(1), 31–56 (2002);
Fischer Black & Myron Scholes (1973); Nassim N. Taleb (1997);
cross-referenced by slug with
reductio-ad-absurdum-and-first-principles-yardstick and
telemetry-integrity-and-error-circuit-yardstick; Ramadge & Wonham
(1987). Downward-only damping within JANUS invariants I1–I9.