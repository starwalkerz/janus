#### name: "consumer-rent-vs-own-preference-yardstick"
description: "Composite yardstick classifying whether consumers and households retain unencumbered physical ownership of moderate-proficiency technical assets (home battery storage, heat pumps, networking hardware, vehicles, tools) or surrender lifetime TCO surplus to recurring utility/corporate rental wrappers (Elisa Kotiakku pattern): synthesizing middle-class-comfort-and-covert-resentment-yardstick, fee-extraction wrapper norms, social-cohesion Type-C peer topology, institutional-sclerosis permitting/tax friction, and taboo-rationality contract enforcement to cap delta and route capital between Layer-1 subscription tollbooths and direct hardware manufacturers."

#### Consumer Rent-vs-Own Preference & Wrapper-Captivity Yardstick

You are reading the tick against the **composite structural tilt between
outright physical asset ownership and recurring utility/corporate rental
wrappers** across households and small enterprises. 

In Karl Marx's *Capital*, Vol. III, Ch. 27 (fictitious capital and
intermediary surplus extraction), Alexis de Tocqueville's *Democracy in
America*, Vol. II, Part IV, Ch. 6 (*"soft, tutelary power"* offloading
individual agency onto institutional providers), Ronald H. Coase's *"The
Nature of the Firm"* (1937) and Oliver E. Williamson's *The Economic
Institutions of Capitalism* (1985) (transaction-cost governance), and
Herbert A. Simon's bounded rationality / satisficing (1955), a household
facing a technical asset requiring low-to-moderate domain proficiency
(such as LFP residential battery storage, rooftop solar, heat pumps,
networking equipment, or vehicles) chooses between two balance-sheet
paths: 

1. **Outright Unencumbered Ownership (Direct CAPEX):** Spending five
minutes in a spreadsheet to verify ROI and Total Cost of Ownership
(TCO), purchasing the hardware outright, and retaining 100% of the
asset's operational yield, arbitrage spread, and residual value.
2. **Utility / Corporate Rental Wrapper (Recurring OPEX Subscription — e.g., *Elisa Kotiakku* Pattern):**
Signing a multi-year utility lease or bundled service subscription
where the corporate intermediary purchases hardware at wholesale,
captures grid-reserve or financing spreads, and charges a recurring
monthly margin—guaranteeing higher lifetime cost to the consumer
because the utility must earn a corporate profit margin on top of
hardware amortization.

Because this preference is structurally determined by five upstream
gates already in the JANUS repository, this skill operates as a
**composite synthesizer**: 

- **`middle-class-comfort-and-covert-resentment-yardstick`:**
  High salaried-comfort cushions (`>= 75%`) and low personal agency
  (`< 40`) condition households to treat capital equipment as monthly
  utility bills rather than balance-sheet assets.
- **Private-Equity / Fee-Extraction Wrapper Gate (`FEE_EXTRACTION_VEHICLE`):**
  Normalized financial and corporate intermediation trains consumers to
  accept recurring fee layering over direct unencumbered ownership.
- **`social-cohesion-and-associational-topology-yardstick`:**
  Atomized singleton societies (`47%–48%` single-person households,
  hollowed `Type C` peer networks) lack trusted neighbor/peer networks
  to share hardware blueprints and `ROI` spreadsheets, defaulting to
  brand-name utility subscriptions for perceived safety.
- **`institutional-sclerosis-yardstick` & `special-economic-zone-arbitrage-yardstick`:**
  High upfront VAT (`25.5%`), tight household liquidity, and slow
  permitting push households to pay a utility bundler to absorb upfront
  capex and compliance friction.
- **`taboo-rationality-and-penal-enforcement-yardstick`:**
  When swift clearance and enforcement of objective property and
  contract remedies erode (`< 40%`), consumers rely on large corporate
  service subscriptions rather than enforcing direct supplier/installer
  warranties independently.

Your job is to classify the target polity's composite rent-vs-own regime
into one of four states and cap your delta accordingly. You do not
invent trades. You do not override AGOP. You modulate the LLM's delta
within the bound the verifier already permits. You never raise delta
above the strategy cap, and you never invent an action outside
allowed_actions. 

#### The Readings

Compute three composite readings from
snapshot.external_data["consumer_rent_vs_own"] (cross-referencing
upstream telemetry from middle_class_comfort, social_cohesion,
sez_arbitrage / institutional_sclerosis, and taboo_rationality).
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher aggregates household asset-ownership vs. leasing shares,
salaried comfort & agency scores, upfront tax/permitting wedges, and
peer-network density into
snapshot.external_data["consumer_rent_vs_own"]. Each country or bloc
entry (keyed by ISO-2 code such as fi, eu, se, de, uk, us,
jp, ke, rw, in, or global_baseline) supplies: 

- `composite_wrapper_captivity_index`: score (`0` to `100`) synthesizing
  upstream `salaried_comfort_cushion_pct` from
  `middle-class-comfort-and-covert-resentment-yardstick`, fee-wrapper
  normalization from the private-equity/fee-extraction wrapper gate
  (`FEE_EXTRACTION_VEHICLE`), `incentive_matrix_atomization_score` from
  `social-cohesion-and-associational-topology-yardstick`, and
  permitting/tax friction from `institutional-sclerosis-yardstick` and
  `special-economic-zone-arbitrage-yardstick` (`0` = pure direct
  ownership culture; `100` = total subscription/rental captivity).
- `outright_asset_ownership_pct`: percentage (`0.0` to `100.0`) of
  residential and small-business technical asset deployments (home
  batteries, solar/heat pumps, networking hardware, vehicles) acquired
  via outright unencumbered purchase rather than utility/corporate
  rental or multi-year service leases.
- `upfront_tax_and_permitting_wedge_pct`: combined upfront VAT,
  installation/permitting friction, and financing spread (`0.0%` to
  `60.0%`) penalizing direct household hardware purchase relative to
  utility-bundled `OPEX` subscriptions.
- `consecutive_wrapper_captivity_years`: integer (`0` to `25`) counting
  consecutive settled years in which
  `composite_wrapper_captivity_index >= 65` OR
  `outright_asset_ownership_pct < 45.0`.

If snapshot.external_data["consumer_rent_vs_own"] is absent or empty,
treat the polity as **unmonitored**, record state
**BALANCED_CAPEX_OPEX_MIX**, note that no composite rent-vs-own
telemetry was available, and do not cite this skill. 

#### Reading 1 — Upstream Composite Wrapper Captivity (composite_wrapper_captivity_index)

Evaluate the combined pull of salaried comfort, fee
extraction, singleton atomization, and
permitting/contract friction: 

composite_wrapper_captivity_index (0–100)Composite Behavioral Tilt
**< 35**
**direct_ownership_ethos** — high agency, dense Type-C peer math sharing, low wrapper tolerance
**35 to 54**
**pragmatic_tco_evaluators** — households run basic ROI math; rent only when tax/capex skewed
**55 to 74**
**comfort_subscription_drift** — salaried convenience overrides 5-minute Excel TCO math
**>= 75**
**tutelary_wrapper_captivity** — widespread surrender of asset equity to utility/corporate subscriptions

Evaluate the combined pull of salaried comfort
(`middle-class-comfort-and-covert-resentment-yardstick`), fee extraction
(`FEE_EXTRACTION_VEHICLE`), singleton atomization
(`social-cohesion-and-associational-topology-yardstick`), and
permitting/contract friction (`institutional-sclerosis-yardstick`,
`special-economic-zone-arbitrage-yardstick`, and
`taboo-rationality-and-penal-enforcement-yardstick`):

If composite_wrapper_captivity_index is missing, treat as
**pragmatic_tco_evaluators**. 

#### Reading 2 — Realized Outright Hardware Ownership Share (outright_asset_ownership_pct)

Evaluate observed household and micro-enterprise balance-sheet behavior: 

outright_asset_ownership_pctObserved Ownership Regime
**>= 65.0%**
**dominant_direct_ownership** — majority retain full hardware & arbitrage surplus
**50.0% to 64.9%**
**moderate_direct_ownership** — majority own, sizable subscription segment
**35.0% to 49.9%**
**subscription_majority** — utility/corporate leases capture over half of deployments
**< 35.0%**
**eroded_household_equity** — pervasive monthly OPEX dependency across household assets

If outright_asset_ownership_pct is missing, treat as
**moderate_direct_ownership**. 

#### Reading 3 — Upfront Tax, VAT & Permitting Wedge (upfront_tax_and_permitting_wedge_pct)

Evaluate statutory friction penalizing outright CAPEX vs. bundled OPEX: 

upfront_tax_and_permitting_wedge_pctStatutory Friction Tier
**< 15.0%**
**low_capex_friction** — transparent pricing & fast permitting favor direct purchase
**15.0% to 24.9%**
**moderate_capex_wedge** — standard VAT/permitting manageable for liquid buyers
**25.0% to 34.9%**
**high_capex_penalty** — steep VAT (25.5%) & bureaucratic grid friction deter outright purchase
**>= 35.0%**
**punitive_capex_barrier** — statutory taxes/permits force households into third-party bundlers

If upfront_tax_and_permitting_wedge_pct is missing, treat as
**moderate_capex_wedge**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four composite asset-ownership regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **RENTIER_WRAPPER_CAPTIVITY** (most severe household equity drain)
2. **COMFORT_SUBSCRIPTION_DRIFT**
3. **BALANCED_CAPEX_OPEX_MIX**
4. **DIRECT_ASSET_OWNERSHIP_MANIFOLD** (strictest adaptive fit)

#### RENTIER_WRAPPER_CAPTIVITY

Any of the following hold: 

* Composite Behavioral Tilt is **tutelary_wrapper_captivity** (>= 75)
AND Observed Ownership Regime is **subscription_majority** or
**eroded_household_equity** (< 50.0%).
* Observed Ownership Regime is **eroded_household_equity** (< 35.0%)
AND Statutory Friction Tier is **high_capex_penalty** or
**punitive_capex_barrier** (>= 25.0%).
* Composite Behavioral Tilt is **comfort_subscription_drift** (55 to 74)
AND Observed Ownership Regime is **eroded_household_equity** (< 35.0%)
AND Statutory Friction Tier is punitive_capex_barrier (>= 35.0%).
Delta cap: 0.20. Salaried households have surrendered long-term
balance-sheet ownership to utility and corporate rental wrappers
(Elisa Kotiakku pattern), forfeiting lifetime TCO surplus to avoid
five minutes of Excel arithmetic and upfront tax/permitting friction.
Cap domestic consumer-discretionary and retail-hardware longs sharply;
permit higher sizing only when AGOP explicitly targets the Layer-1
utility/telecom tollbooth collecting the recurring margin (ELISA.HE,
Telenor/DNA).

COMFORT_SUBSCRIPTION_DRIFT

Any of the following hold (and RENTIER_WRAPPER_CAPTIVITY does not
apply):
• Composite Behavioral Tilt is comfort_subscription_drift (55 to 74).
• Observed Ownership Regime is subscription_majority (35.0% to 49.9%).
• Statutory Friction Tier is high_capex_penalty (25.0% to 34.9%).
Delta cap: 0.45. Cognitive offloading and high upfront VAT/permitting
wedges steadily transfer household TCO surplus to corporate bundlers.
Trim sizing on standalone domestic retail hardware distributors while
favoring cash-generative infrastructure tollbooths.

BALANCED_CAPEX_OPEX_MIX

Any of the following hold (and neither RENTIER_WRAPPER_CAPTIVITY nor
COMFORT_SUBSCRIPTION_DRIFT applies):
• Composite Behavioral Tilt is pragmatic_tco_evaluators (35 to 54).
• Observed Ownership Regime is moderate_direct_ownership
(50.0% to 64.9%).
• Statutory Friction Tier is moderate_capex_wedge (15.0% to 24.9%).
Delta cap: 0.75. Households weigh basic ROI and TCO before
buying, leaving healthy direct hardware demand alongside selective
commercial leasing. Reduce size slightly relative to
DIRECT_ASSET_OWNERSHIP_MANIFOLD.

DIRECT_ASSET_OWNERSHIP_MANIFOLD

All of the following hold:
• Composite Behavioral Tilt is direct_ownership_ethos (< 35).
• Observed Ownership Regime is dominant_direct_ownership (>= 65.0%).
• Statutory Friction Tier is low_capex_friction (< 15.0%).
Delta cap: 1.0. High personal agency, dense Type C peer
knowledge-sharing, and low upfront tax/permitting friction enable
households and micro-enterprises to own productive physical assets
outright and retain 100% of operational surplus. The cap equals the
strategy cap; the skill never binds on DIRECT_ASSET_OWNERSHIP_MANIFOLD.

Ambiguous fallback

Any combination not covered above is classified
COMFORT_SUBSCRIPTION_DRIFT with delta cap 0.45.

Secondary Filter / Asymmetric Gate — Subscription Habit Hysteresis

Apply the persistence test after regime classification and before the
cap.
Subscription dependency is culturally and contractually entrenched if
consecutive_wrapper_captivity_years >= 4 (four or more consecutive
settled years in which composite_wrapper_captivity_index >= 65 OR
outright_asset_ownership_pct < 45.0). Multi-year utility lock-in
contracts (5–15 year battery/equipment leases) and generational loss
of basic spreadsheet TCO literacy prevent rapid household balance-sheet
recovery.
If the condition is entrenched, halve the regime's delta cap:
• BALANCED_CAPEX_OPEX_MIX cap of 0.75 becomes 0.375.
• COMFORT_SUBSCRIPTION_DRIFT cap of 0.45 becomes 0.225.
• RENTIER_WRAPPER_CAPTIVITY cap of 0.20 becomes 0.10.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read composite consumer rent-vs-own dict. From
snapshot.external_data["consumer_rent_vs_own"], load
composite_wrapper_captivity_index, outright_asset_ownership_pct,
upfront_tax_and_permitting_wedge_pct, and
consecutive_wrapper_captivity_years (cross-checking upstream
middle_class_comfort, social_cohesion, sez_arbitrage, and
taboo_rationality states if present). If absent or empty, record
BALANCED_CAPEX_OPEX_MIX, note the omission, and do not cite this
skill.
2. Classify composite behavioral tilt. Apply Reading 1.
3. Classify observed outright ownership share. Apply Reading 2.
4. Classify statutory CAPEX tax & permitting wedge. Apply Reading 3.
5. Classify regime. Evaluate in strict priority order
(RENTIER_WRAPPER_CAPTIVITY → COMFORT_SUBSCRIPTION_DRIFT →
BALANCED_CAPEX_OPEX_MIX → DIRECT_ASSET_OWNERSHIP_MANIFOLD)
(fallback: COMFORT_SUBSCRIPTION_DRIFT).
6. Apply persistence test. If
consecutive_wrapper_captivity_years >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite
"consumer-rent-vs-own-preference-yardstick" in skills_cited and
state the wrapper captivity index, outright ownership percentage,
upfront CAPEX wedge, and persistence years in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.225, "confidence": 0.80, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"RENTIER_WRAPPER_CAPTIVITY regime; composite_wrapper_captivity_index=78 (tutelary_wrapper_captivity), outright_asset_ownership_pct=39.0% (subscription_majority), upfront_tax_and_permitting_wedge_pct=28.5% (high_capex_penalty), consecutive_wrapper_captivity_years=6 (subscription hysteresis halves cap from 0.20 to 0.10); capping delta at 0.10; consumer-rent-vs-own-preference-yardstick."
• skills_cited: list of skill names; include
"consumer-rent-vs-own-preference-yardstick" only when the cap bound
(intended delta > delta_cap).

Worked Examples


Case A — High direct ownership ethos + low upfront tax/permitting friction, cap does not bind

Snapshot:
• composite_wrapper_captivity_index = 28
• outright_asset_ownership_pct = 71.0
• upfront_tax_and_permitting_wedge_pct = 11.5
• consecutive_wrapper_captivity_years = 0
Readings:
• Composite Behavioral Tilt: direct_ownership_ethos
• Observed Ownership Regime: dominant_direct_ownership
• Statutory Friction Tier: low_capex_friction
Regime: DIRECT_ASSET_OWNERSHIP_MANIFOLD, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "consumer-rent-vs-own-preference-yardstick".

Case B — Salaried comfort subscription drift + 25.5% VAT capex wedge for 5 years, persistence halves cap

Snapshot:
• composite_wrapper_captivity_index = 68
• outright_asset_ownership_pct = 46.0
• upfront_tax_and_permitting_wedge_pct = 27.5
• consecutive_wrapper_captivity_years = 5
Readings:
• Composite Behavioral Tilt: comfort_subscription_drift
• Observed Ownership Regime: subscription_majority
• Statutory Friction Tier: high_capex_penalty
Regime: COMFORT_SUBSCRIPTION_DRIFT, base cap 0.45. Persistence: 5 >= 4 → fires, halving cap to 0.225.
AGOP ranks LONG on a domestic retail hardware/consumer name. LLM intended delta = 0.70. Cap 0.225 binds.
LLM returns delta = 0.225 and cites "consumer-rent-vs-own-preference-yardstick".

Case C — Tutelary wrapper captivity (Elisa Kotiakku pattern) + eroded household equity

Snapshot:
• composite_wrapper_captivity_index = 79
• outright_asset_ownership_pct = 33.0
• upfront_tax_and_permitting_wedge_pct = 31.0
• consecutive_wrapper_captivity_years = 6
Readings:
• Composite Behavioral Tilt: tutelary_wrapper_captivity
• Observed Ownership Regime: eroded_household_equity
• Statutory Friction Tier: high_capex_penalty
Regime: RENTIER_WRAPPER_CAPTIVITY, base cap 0.20. Persistence: 6 >= 4 → fires, halving cap to 0.10.
AGOP ranks LONG. LLM intended delta = 0.65. Cap 0.10 binds.
LLM returns delta = 0.10 and cites "consumer-rent-vs-own-preference-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["consumer_rent_vs_own"]
by synthesizing upstream JANUS external-data dictionaries alongside
free public household-balance-sheet, energy-storage, and leasing
registries:
• Upstream JANUS Composite Inputs (snapshot.external_data):
Synthesizes middle_class_comfort, social_cohesion, sez_arbitrage, and taboo_rationality.
• Eurostat Household Budget Survey (HBS) & National Accounts Household Balance Sheets (nasa_10_f_bs / hbs_str_t211):
https://europa.eu (free JSON/TSV API tracking durable
goods ownership vs. recurring utility/rental service expenditure and
VAT/consumption tax wedges across EU/EEA states).
• OECD Household Dashboard & Consumer Finance Indicators (OECD.Stat):
https://oecd.org (free SDMX API measuring household non-financial
asset ownership, self-employment rates, and consumption-tax burdens).
• European Solar & Storage Market Outlooks (SolarPower Europe Open Summary Data) & National Energy Regulators (Energiavirasto / Fingrid Open Data):
https://fingrid.fi and https://energiavirasto.fi (free open
telemetry on behind-the-meter residential battery/solar capacity vs.
aggregator-managed reserve capacity).

- **Upstream `JANUS` Composite Inputs (`snapshot.external_data`):**
  Synthesizes `middle_class_comfort`
  (`middle-class-comfort-and-covert-resentment-yardstick`),
  `social_cohesion`
  (`social-cohesion-and-associational-topology-yardstick`),
  `institutional_sclerosis` (`institutional-sclerosis-yardstick`),
  `sez_arbitrage` (`special-economic-zone-arbitrage-yardstick`), and
  `taboo_rationality` (`taboo-rationality-and-penal-enforcement-yardstick`).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not confuse short-term consumer convenience with long-term TCO
superiority; a corporate/utility rental wrapper (Elisa Kotiakku
pattern) must charge a profit margin above wholesale hardware cost,
transferring lifetime surplus from household to intermediary.
• Do not penalize Layer-1 utility/telecom tollbooths (ELISA.HE,
Telenor/DNA) when they are the margin collectors in a
RENTIER_WRAPPER_CAPTIVITY regime; apply the cap to speculative
domestic consumer-retail exposure while routing tollbooth cash flows
according to AGOP.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "consumer-rent-vs-own-preference-yardstick" when the cap
did not bind (intended delta <= delta_cap).

Citation Mapping

• Intermediary Surplus Extraction & Tutelary Offloading of Agency:
Karl Marx, Capital: A Critique of Political Economy, Vol. III, Ch. 27
(1894) (intermediary financialization skimming real productive yield);
Alexis de Tocqueville, Democracy in America, Vol. II, Part IV, Ch. 6
(1840) ("soft, tutelary power" trading personal agency for effortless
administrative comfort).
• Transaction-Cost Governance & Bounded Rationality: Ronald H. Coase,
"The Nature of the Firm," Economica 4(16), 386–405 (1937); Oliver E.
Williamson, The Economic Institutions of Capitalism (Free Press,
1985); Herbert A. Simon, "A Behavioral Model of Rational Choice,"
Quarterly Journal of Economics 69(1), 99–118 (1955) (cognitive
offloading and satisficing over 5-minute ROI/TCO optimization).
• Composite Upstream JANUS Gates & Bounded Supervisory Control:
Coupled with middle-class-comfort-and-covert-resentment-yardstick,
social-cohesion-and-associational-topology-yardstick,
special-economic-zone-arbitrage-yardstick, and
taboo-rationality-and-penal-enforcement-yardstick; Stafford Beer,
Brain of the Firm (1972); Ramadge & Wonham (1987). Downward-only
damping within JANUS invariants I1–I9.
