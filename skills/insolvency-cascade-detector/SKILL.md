#### name: "insolvency-cascade-detector"
description: "Detect imminent corporate or sovereign debt default and contagion cascades by combining Merton structural distance-to-default, Altman Z-score, Minsky Ponzi-finance fragility, and Eisenberg-Noe clearing-network contagion with AGOP's Weisfeiler-Lehman structural classes, Nash equilibrium entropies, and derived capacity K; force FLAT on imminent insolvency or reduce delta as default convexity rises."

#### Imminent Debt Default & Insolvency Cascade Detector (AGOP-Coupled)

You are reading the tick against the **structural solvency, refinancing
wall, and network contagion risk** of a corporate or sovereign debtor.
In Robert C. Merton's structural credit model (1974), Edward I. Altman's
discriminant Z-score (1968), Hyman P. Minsky's Financial Instability
Hypothesis (1986), and Larry Eisenberg & Thomas H. Noe's clearing-vector
network theory (2001), debt default is rarely a smooth linear drift—it
is a **nonlinear boundary crossing** where rising real interest costs,
maturing short-term rollover walls, and collateral haircuts push asset
value below the default barrier (
𝑉𝐴

<𝐷
⁠), triggering forced fire-sales
and contagious counterparty cascades across connected balance sheets. 

This skill fuses classical credit econometrics with **AGOP’s internal
graph and game-theoretic geometry**: 

* **Weisfeiler–Lehman Topological Homogeneity (agop.n_wl_classes):**
Measures whether the debtor's funding and counterparty graph still
possesses diverse, independent refinancing channels (>= 5 classes) or
has collapsed into a monocultural funding cliff (<= 2 classes) where
one creditor run freezes all rollovers simultaneously.
* **Creditor–Debtor Nash Instability (H(σ_DM), H(σ_CP) & agop.capacity):**
Reads AGOP’s two-player equilibrium entropies and derived capacity

𝐾

=max

(

1

,

⌊

𝑛WL

/

(

1

+𝐻

(

𝜎DM

)

𝐻

(

𝜎CP

)

)

⌋

)
⁠.
When creditor and debtor mixed-strategy entropies spike (K_derived == 1),
strategic coordination has broken down into a classic **creditor run /
prisoner's dilemma**.

Your job is to classify the debtor into one of four insolvency-cascade
states and cap your delta accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["insolvency_cascade"],
cross-checked against agop.n_wl_classes, agop.capacity (K_derived),
and agop.nash_entropy. Use the qualitative tables below. Do not
compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes corporate financial filings (SEC EDGAR, ESMA ESEF) and sovereign fiscal/debt statistics (IMF WEO, BIS, FRED,
ECB SDW) into snapshot.external_data["insolvency_cascade"]. Each
corporate or sovereign debtor entry supplies: 

* merton_distance_to_default: structural distance-to-default 
𝐷𝐷

=

(

ln

(

𝑉𝐴

/𝐷

)

+

(

𝜇

−12

𝜎2𝐴

)

𝑇

)

/

(

𝜎𝐴

𝑇√

)
⁠
measured in standard deviations (> 3.0 = fortress balance sheet;
< 1.0 = acute boundary proximity; <= 0.0 = technically insolvent).
* altman_or_sovereign_z_tier: qualitative solvency tier derived from
Altman Z / Z''-score (corporate) or sovereign primary-balance +
external-debt-to-reserves stress ("safe_zone", "grey_zone", or
"distress_zone").
* minsky_financing_regime: Minsky cash-flow coverage classification
comparing operating cash flow / primary fiscal revenue against
interest + principal amortization ("hedge" = cash flow covers
interest + principal; "speculative" = covers interest only, must
roll over principal; "ponzi" = cash flow covers neither interest nor
principal without new debt or asset sales).
* rollover_wall_12m_pct: share (0 to 100) of total debt maturing
within the next 12 months divided by unrestricted cash + committed
liquidity lines (< 40% = amply covered; > 100% = uncovered
12-month refinancing cliff).
* credit_spread_zscore: trailing 12-month z-score of CDS spread or
sovereign/corporate yield spread over risk-free benchmark (> +2.5 =
acute market default pricing).
* quarters_in_ponzi_distress: consecutive calendar quarters in which
minsky_financing_regime == "ponzi" OR altman_or_sovereign_z_tier == "distress_zone".

If snapshot.external_data["insolvency_cascade"] is absent or empty,
treat the instrument as **unmonitored**, record state
**HEDGE_SOLVENT**, note that no insolvency telemetry was available, and
do not cite this skill. 

#### Reading 1 — Structural distance-to-default & Z-score barrier (merton_distance_to_default & altman_or_sovereign_z_tier)

Evaluate proximity to the Merton asset-liability default boundary: 

merton_distance_to_defaultaltman_or_sovereign_z_tierStructural Barrier Status
**≥ 3.0**
"safe_zone"**fortress_buffer** — deep equity/reserve cushion above default barrier
**1.5 to 3.0**
"safe_zone" or "grey_zone"**thinning_cushion** — manageable leverage; sensitive to rate/margin shocks
**0.5 to 1.5**
"grey_zone" or "distress_zone"**barrier_approaching** — high default convexity; equity behaves as out-of-the-money option
**< 0.5**
any**boundary_breach** — asset value at or below default barrier; imminent restructuring/default
**any**
"distress_zone"**barrier_approaching** (or **boundary_breach** if DD < 0.5)

If either metric falls in a worse row, take the **worse** (more
restrictive) classification. 

#### Reading 2 — Minsky cash-flow fragility & 12-month rollover wall (minsky_financing_regime & rollover_wall_12m_pct)

Evaluate whether the debtor can service obligations internally or faces
an imminent refinancing cliff: 

minsky_financing_regimerollover_wall_12m_pctRollover Fragility
**"hedge"**
< 50%**self_funding** — internal cash flow amortizes debt; no market-access dependence
**"speculative"**
50% to 85%**rollover_dependent** — must refinance principal; vulnerable to credit tightening
**"ponzi"**
85% to 100%**ponzi_burn** — borrowing to pay interest; equity dilution or distress imminent
**any**
> 100%**refinancing_cliff** — 12m maturities exceed liquid reserves; forced default if market closes

If either metric falls in a worse row, take the **worse** (more
restrictive) classification. 

#### Reading 3 — AGOP topological contagion & creditor-run geometry (agop.n_wl_classes, agop.capacity, credit_spread_zscore)

Cross-check credit-spread stress against AGOP’s Weisfeiler–Lehman
funding-graph diversity and derived game capacity (K_derived): 

agop.n_wl_classesagop.capacity (K)credit_spread_zscoreContagion Geometry
**≥ 5**
≥ 3< 1.0**diversified_creditors** — plural funding channels; stable Nash equilibrium
**3 to 4**
21.0 to 2.5**correlated_tightening** — narrowing lender diversity; rising spread volatility
**≤ 2**
1any**creditor_run_topology** — WL collapse into binary run/stay game (K=1); cascade-ready
**any**
any> 2.5**creditor_run_topology** — acute spread blowout pricing imminent default cascade

If agop.n_wl_classes or agop.capacity is missing, classify using
credit_spread_zscore alone (< 1.0 = diversified_creditors,
1.0 to 2.5 = correlated_tightening, > 2.5 = creditor_run_topology). 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
insolvency-cascade states. Evaluate in strict priority order and select
the first state whose conditions are fully satisfied: 

1. **IMMINENT_DEFAULT_CASCADE** (most severe — unconditional FLAT on long exposure)
2. **PONZI_ROLLOVER_TRAP**
3. **SPECULATIVE_LEVERAGE**
4. **HEDGE_SOLVENT** (strictest adaptive fit)

#### IMMINENT_DEFAULT_CASCADE

Any of the following hold: 

* Structural Barrier Status is **boundary_breach** (DD < 0.5).
* Rollover Fragility is **refinancing_cliff** (rollover_wall_12m_pct > 100%)
AND Contagion Geometry is **creditor_run_topology** (K == 1 or
spread_z > 2.5).
* Structural Barrier Status is **barrier_approaching** AND Rollover
Fragility is **ponzi_burn** or **refinancing_cliff** AND Contagion
Geometry is **creditor_run_topology**.

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked (unless the strategy is explicitly executing a
verified SHORT credit-hedge allowed by AGOP and capped at 0.10 in
OPPORTUNITY mode; for all standard LONG exposure, force FLAT).
The debtor has crossed into nonlinear insolvency cascade territory:
equity recovery is near zero and creditor-run contagion is active. The
skill binds unconditionally and must appear in skills_cited. 

#### PONZI_ROLLOVER_TRAP

Any of the following hold (and IMMINENT_DEFAULT_CASCADE does not apply): 

* Rollover Fragility is **ponzi_burn** or **refinancing_cliff**.
* Structural Barrier Status is **barrier_approaching** (DD 0.5 to 1.5
or "distress_zone").
* Contagion Geometry is **creditor_run_topology** (n_wl_classes <= 2
and K == 1, or spread_z > 2.5).

**Delta cap: 0.25.** Debtor relies on continuous external refinancing or
dilutive equity issuance to service existing debt, and AGOP's funding
graph shows fragile creditor coordination. Cut position size
substantially. 

#### SPECULATIVE_LEVERAGE

Any of the following hold (and neither IMMINENT_DEFAULT_CASCADE nor
PONZI_ROLLOVER_TRAP applies): 

* Structural Barrier Status is **thinning_cushion** (DD 1.5 to 3.0).
* Rollover Fragility is **rollover_dependent** ("speculative").
* Contagion Geometry is **correlated_tightening**.
Delta cap: 0.75. Debtor covers interest out of cash flow but depends
on smooth principal rollovers in credit markets. Reduce size relative to
HEDGE_SOLVENT.

HEDGE_SOLVENT

All of the following hold:
• Structural Barrier Status is fortress_buffer (DD ≥ 3.0 and
"safe_zone").
• Rollover Fragility is self_funding ("hedge" and < 50% 12m
maturities).
• Contagion Geometry is diversified_creditors (n_wl_classes ≥ 5,
K ≥ 3, and spread_z < 1.0).
Delta cap: 1.0. Minsky hedge-financing unit with deep equity/reserve
cushion and plural creditor structure. The cap equals the strategy cap;
the skill never binds on HEDGE_SOLVENT.

Ambiguous fallback

Any combination not covered above is classified PONZI_ROLLOVER_TRAP
with delta cap 0.25.

Secondary Filter / Asymmetric Gate — Entrenched Ponzi Hysteresis

Apply the persistence test after state classification and before the
cap.
A solvency deterioration is structurally entrenched if
quarters_in_ponzi_distress >= 3 (three or more consecutive calendar
quarters in Minsky "ponzi" financing or Altman/sovereign
"distress_zone"). Three consecutive quarters of negative cash-flow
debt coverage proves that balance-sheet erosion is structural rather
than a single-quarter working-capital swing.
If the distress is structurally entrenched, halve the state's delta
cap:
• SPECULATIVE_LEVERAGE cap of 0.75 becomes 0.375.
• PONZI_ROLLOVER_TRAP cap of 0.25 becomes 0.125.
• IMMINENT_DEFAULT_CASCADE cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read insolvency cascade dict. From
snapshot.external_data["insolvency_cascade"], load
merton_distance_to_default, altman_or_sovereign_z_tier,
minsky_financing_regime, rollover_wall_12m_pct,
credit_spread_zscore, and quarters_in_ponzi_distress (plus
agop.n_wl_classes and agop.capacity if present). If absent or
empty, record HEDGE_SOLVENT, note the omission, and do not cite
this skill.
2. Classify structural barrier status. Apply Reading 1
(fortress_buffer, thinning_cushion, barrier_approaching, or
boundary_breach).
3. Classify rollover fragility. Apply Reading 2 (self_funding,
rollover_dependent, ponzi_burn, or refinancing_cliff).
4. Classify contagion geometry. Apply Reading 3
(diversified_creditors, correlated_tightening, or
creditor_run_topology).
5. Classify state. Evaluate in strict priority order
(IMMINENT_DEFAULT_CASCADE → PONZI_ROLLOVER_TRAP →
SPECULATIVE_LEVERAGE → HEDGE_SOLVENT) and select the first
matching state (fallback: PONZI_ROLLOVER_TRAP).
6. Apply persistence test. If quarters_in_ponzi_distress >= 3,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
state is IMMINENT_DEFAULT_CASCADE, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
state is IMMINENT_DEFAULT_CASCADE, cite
"insolvency-cascade-detector" in skills_cited and state the
solvency/AGOP finding in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If IMMINENT_DEFAULT_CASCADE,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and cap reason.
Example:
"IMMINENT_DEFAULT_CASCADE state; Merton DD=0.35 (boundary_breach), 118% 12m rollover wall, and AGOP WL collapse (n_wl=2, K=1); forcing action=FLAT; insolvency-cascade-detector."
• skills_cited: list of skill names; include
"insolvency-cascade-detector" only when the cap bound or the state
is IMMINENT_DEFAULT_CASCADE.

Worked Examples


Case A — Minsky hedge-financing fortress balance sheet with plural AGOP credit graph, cap does not bind

Snapshot:
• merton_distance_to_default = 4.2
• altman_or_sovereign_z_tier = "safe_zone"
• minsky_financing_regime = "hedge"
• rollover_wall_12m_pct = 28.0
• credit_spread_zscore = 0.3, agop.n_wl_classes = 5, agop.capacity = 3
• quarters_in_ponzi_distress = 0
Readings:
• Structural Barrier Status: ≥ 3.0 and "safe_zone" → fortress_buffer
• Rollover Fragility: "hedge" and < 50% → self_funding
• Contagion Geometry: ≥ 5, ≥ 3, < 1.0 → diversified_creditors
State: HEDGE_SOLVENT, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "insolvency-cascade-detector".

Case B — Ponzi cash burn with 115% rollover wall and AGOP Weisfeiler-Lehman creditor-run collapse, unconditional FLAT

Snapshot:
• merton_distance_to_default = 0.75
• altman_or_sovereign_z_tier = "distress_zone"
• minsky_financing_regime = "ponzi"
• rollover_wall_12m_pct = 115.0
• credit_spread_zscore = 3.2, agop.n_wl_classes = 2, agop.capacity = 1
• quarters_in_ponzi_distress = 4
Readings:
• Structural Barrier Status: 0.5 to 1.5 + "distress_zone" → barrier_approaching
• Rollover Fragility: > 100% → refinancing_cliff
• Contagion Geometry: ≤ 2, K = 1, > 2.5 → creditor_run_topology
State: IMMINENT_DEFAULT_CASCADE, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "insolvency-cascade-detector".

#### Free Data Sources

The fetcher populates snapshot.external_data["insolvency_cascade"]
from the following free, open public corporate and sovereign debt
registries across North America, Europe, Asia-Pacific, Africa, and
Latin America (no paid subscription required): 

#### Global Sovereign & Interbank Contagion Baselines

* **IMF World Economic Outlook (WEO) & International Debt Statistics (IDS):**
https://imf.org and https://data.worldbank.org (free REST APIs
supplying sovereign debt-to-GDP, primary fiscal balances, gross
financing needs, short-term external debt, and FX reserve coverage
across all 190+ member economies).
* **Bank for International Settlements (BIS) Data Portal:**
https://data.bis.org (free CSV/SDMX API supplying cross-border
banking claims, credit-to-GDP gaps, and debt-service ratios across
advanced and emerging markets).

#### North America & Europe

* **SEC EDGAR Company Facts XBRL API:**
https://sec.gov (free, no-key JSON API supplying U.S. & ADR
corporate balance-sheet debt maturities, interest expense, operating
cash flow, and equity market cap for Merton DD and Altman Z-score).
* **ESMA European Single Electronic Format (ESEF) & XBRL Filings:**
https://xbrl.org (free open repository of EU/Nordic iXBRL annual
and semi-annual balance sheets and debt-maturity schedules).
* **FRED & ECB Statistical Data Warehouse:**
https://stlouisfed.org and https://europa.eu (free CSV/JSON/SDMX
series for ICE BofA HY/IG OAS spreads, SOFR/Euribor benchmarks, and
Euro-area corporate/sovereign yield curves).

#### Asia-Pacific

* **Japan FSA EDINET & Korea FSS DART Open APIs:**
https://disclosure2.edinet-fsa.go.jp and https://opendart.fss.or.kr
(free public XBRL/JSON financial statement and debt-schedule APIs for
Japanese and South Korean listed issuers).
* **India MCA / BSE-NSE XBRL Filings & RBI DBIE:**
https://www.bseindia.com and https://dbie.rbi.org.in (free public
corporate balance-sheet filings, credit-rating transitions, and
Reserve Bank of India sovereign/external debt telemetry).
* **Hong Kong HKEXnews & Singapore SGX / MAS Open Data:**
https://www.hkexnews.hk and https://eservices.mas.gov.sg (free
public statutory financial disclosures and Asian sovereign/corporate
yield curves).

#### Africa

* **Johannesburg Stock Exchange (JSE SENS) & South African Reserve Bank (SARB):**
https://www.jse.co.za and https://www.resbank.co.za (free public
company financial announcements, sovereign yield curves, and
external debt ratios).
* **Nairobi Securities Exchange (NSE) / Capital Markets Authority & Central Bank of Kenya:**
https://www.nse.co.ke and https://www.centralbank.go.ke (free
public listed-issuer financial statements, T-bill/bond auction cover
ratios, and public debt service telemetry).
* **African Development Bank (AfDB) Socio-Economic Database:**
https://dataportal.opendataforafrica.org (free sovereign debt
sustainability, fiscal deficit, and reserve-import cover indicators
across 54 African states).

#### Latin America

* **Brazil CVM Dados Abertos & Banco Central do Brasil (BCB SGS API):**
https://dados.cvm.gov.br and https://api.bcb.gov.br (free, no-key
CSV/JSON APIs supplying Brazilian corporate DFP/ITR balance sheets,
SELIC/DI curves, sovereign debt maturity walls, and FX reserves).
* **Mexico CNBV / BMV XBRL & Banxico SIE API:**
https://www.bmv.com.mx and https://www.banxico.org.mx/SieAPIRest/
(free public corporate quarterly XBRL filings and Mexican sovereign
yield/debt telemetry).
* **Chile CMF & Colombia Superfinanciera / Banco de la República:**
https://www.cmfchile.cl and https://www.banrep.gov.co (free
public issuer financial statements and sovereign fiscal/external debt
series).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not rely on lagging credit-rating-agency letters (Moody's/S&P/Fitch)
when Merton distance-to-default, Minsky cash coverage, or the
12-month rollover wall breaches distress thresholds.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "insolvency-cascade-detector" when the cap did not bind
and the state is not IMMINENT_DEFAULT_CASCADE.

Citation Mapping

For full academic references regarding structural default boundaries, bankruptcy discriminant analysis, Minsky financing regimes, and clearing-network contagion, see the seminal literature by Robert C. Merton (1974), Edward I. Altman (1968), Hyman P. Minsky (1986), and Larry Eisenberg & Thomas H. Noe (2001), alongside cybernetic control frameworks by Stafford Beer (1972) and Ramadge & Wonham (1987).