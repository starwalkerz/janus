#### name: "special-economic-zone-arbitrage-yardstick"
description: "Classify special economic zones (SEZs), R&D clusters, youth/payroll tax-credit regimes, municipal trade-tax enclaves, and paper-only proposals into a non-political investment yardstick: scoring enacted tax/payroll-wedge arbitrage, physical permitting and grid readiness, sovereign-capture/parastatal delisting risk (DP World precedent), and routing capital strictly to publicly listed capture vehicles (listed zone REITs/developers, Layer-1 utility tollbooths, or anchor industrial tenants)."

#### Special Economic Zone & Fiscal-Enclave Arbitrage Yardstick

You are reading the tick against the **concrete fiscal, permitting, and
infrastructure arbitrage** of Special Economic Zones (SEZs), R&D
clusters, payroll tax-credit territories, and municipal tax enclaves—and
mapping where that economic rent is captured by **publicly listed
equity tickers**. 

In Douglass C. North's *Institutions, Institutional Change and Economic
Performance* (1990), Mancur Olson's *The Rise and Decline of Nations*
(1982), and the World Bank / UNCTAD *World Investment Report* taxonomy
of Special Economic Zones, enclaves exist to bypass national regulatory
and tax sclerosis locally. However, from an underwriting perspective,
not all zones are investable: 

1. **Heterogeneous Zone Typology:** Zones range from customs-bonded
industrial ports (**Southern Italy's ZES Unica**, **Seville &
Barcelona Zona Franca**, **Abu Dhabi KEZAD / Dubai JAFZA**)
and semiconductor/deep-tech R&D campuses (**Grenoble Minatec**,
**Leuven imec**, **Bengaluru IT SEZs**), to statutory payroll-tax
credit territories (**French Outre-mer (LODEOM) youth & employer
hiring exemptions**), municipal trade-tax (*Gewerbesteuer*) holding
enclaves (**Dahme-Spreewald**, **Zug**), dense startup incubators
(**Paris Station F**, **Berlin tech districts**), and **unenacted
paper concepts** (**Imatra** border SEZ proposals) with zero enacted
tax statute or physical throughput.
2. **Publicly Listed Capture Vehicles vs. Non-Listed / Parastatal Operators:**
Most zones are administered directly by public authorities or
unlisted foundations (Minatec, Station F, ZES Unica, Port of Seville). Even when a zone operator is initially listed on a stock
exchange, it faces acute **sovereign-capture and parastatal conversion
risk**—exemplified by **DP World**, which was delisted and taken
private by its sovereign parent (Dubai World / Port & Free Zone World), turning a once-listed global port-and-zone operator into a
state-controlled parastatal. Underwriting must therefore verify
whether rent is captured by a **durable, minority-protected public
ticker** (listed industrial/SEZ REIT, Layer-1 grid/telecom/fuel
tollbooth, or anchor semiconductor/industrial tenant) rather than a
delisting-prone parastatal monopoly.

Your job is to classify the target zone and its public equity capture
channel into one of four underwriting states and cap your delta
accordingly. You do not invent trades. You do not override AGOP. You
modulate the LLM's delta within the bound the verifier already permits.
You never raise delta above the strategy cap, and you never invent an
action outside allowed_actions. 

#### The Readings

Compute three quantitative readings from
snapshot.external_data["sez_arbitrage"]. Use the qualitative tables
below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes enacted zone tax statutes, permitting timelines,
physical grid/port utilization, operator ownership/delisting status,
and listed ticker exposure into snapshot.external_data["sez_arbitrage"]: 

* zone_type: string classifying the structural archetype: 

  * "TYPE_1_INDUSTRIAL_PORT_SEZ" (customs-bonded port/industrial zone:
e.g., Italy ZES Unica, Seville/Barcelona Zona Franca, KEZAD)
  * "TYPE_2_RD_AND_TECH_CLUSTER" (fab/lab R&D enclave: e.g., Grenoble
Minatec, imec, Hsinchu, Bengaluru IT SEZs)
  * "TYPE_3_PAYROLL_TAX_CREDIT_ZONE" (statutory youth/employer payroll
tax relief: e.g., French Outre-mer LODEOM credits, Decontribuzione Sud)
  * "TYPE_4_MUNICIPAL_HOLDING_AND_STARTUP_HUB" (low municipal trade
tax / startup hub: e.g., Dahme-Spreewald, Station F, Berlin hubs)
  * "TYPE_5_PAPER_CONCEPT_ONLY" (unenacted proposal lacking tax law,
permitting window, or physical infrastructure: e.g., Imatra SEZ)
* effective_tax_wedge_reduction_pct: percentage reduction (0.0 to
100.0) in effective corporate income tax (CIT), local municipal
trade tax (Gewerbesteuer), or statutory youth/specialist payroll
charges inside the zone compared with the surrounding national baseline.
* permitting_and_infra_readiness: score (0 to 100) measuring
enacted single-window permitting (<= 30 days) plus live power,
fiber, and port/logistics throughput (0 = unenacted paper concept;
100 = live single-window permitting + full physical grid/port load).
* public_capture_channel: string identifying how the target ticker
captures zone rent: 

  * "LISTED_SEZ_REIT_OR_DEVELOPER" (e.g., CY6U.SI, EMBASSY.NS,
CTPNV.AS, VGP.BR, MRL.MC, 4220.SR)
  * "LAYER1_UTILITY_OR_PIPE_TOLLBOOTH" (e.g., ENEL.MI, TRN.MI,
RED.MC, NTGY.MC, ORA.PA, RUI.PA)
  * "ANCHOR_INDUSTRIAL_OR_FAB_TENANT" (e.g., SOI.PA, STMPA.PA,
SU.PA, DTG.DE)
  * "PARASTATAL_OR_DELISTING_RISK" (state-controlled operator prone to
sovereign capture/delisting like DP World, or restricted float)
  * "NONE_UNLISTED_OR_PAPER" (no public ticker captures the zone)
* years_statute_and_grid_active: integer (0 to 40) counting
consecutive settled years of enacted statutory tax relief and active
physical throughput (0 for paper concepts or unbuilt proposals).

If snapshot.external_data["sez_arbitrage"] is absent or empty, treat
the instrument as **unmonitored**, record state **MODERATE_ENCLAVE_CAPTURE**,
note that no SEZ telemetry was available, and do not cite this skill. 

#### Reading 1 — Enacted Tax & Payroll-Wedge Arbitrage (zone_type & effective_tax_wedge_reduction_pct)

Evaluate whether the zone delivers genuine statutory tax or payroll
compression rather than a paper announcement: 

zone_type & effective_tax_wedge_reduction_pctFiscal Arbitrage Tier
**zone_type != "TYPE_5_PAPER_CONCEPT_ONLY" AND effective_tax_wedge_reduction_pct >= 35.0%**
**high_fiscal_arbitrage** — deep statutory CIT, trade-tax, or payroll-wedge relief
**zone_type != "TYPE_5_PAPER_CONCEPT_ONLY" AND 15.0% to 34.9%**
**moderate_fiscal_arbitrage** — meaningful regional tax/hiring credit advantage
**zone_type != "TYPE_5_PAPER_CONCEPT_ONLY" AND < 15.0%**
**marginal_tax_advantage** — cluster/network value without large statutory tax spread
**zone_type == "TYPE_5_PAPER_CONCEPT_ONLY" OR effective_tax_wedge_reduction_pct == 0.0%**
**paper_concept_zero_arbitrage** — unenacted proposal; zero fiscal or legal reality

If zone_type is missing, treat as **paper_concept_zero_arbitrage**. 

#### Reading 2 — Permitting Velocity & Physical Infrastructure Readiness (permitting_and_infra_readiness)

Evaluate whether the zone has live single-window permitting and
operational power, fiber, and port/lab infrastructure: 

permitting_and_infra_readiness (0–100)Operational Readiness Tier
**>= 75**
**turnkey_physical_corridor** — live single-window permitting + high grid/port/fab utilization
**45 to 74**
**developing_corridor** — active infrastructure with partial administrative bottlenecks
**20 to 44**
**early_stage_rollout** — statutory framework passed, physical buildout incomplete
**< 20**
**unbuilt_paper_zone** — lacks grid hookups, port/transit volume, or enacted permitting

If permitting_and_infra_readiness is missing, treat as **unbuilt_paper_zone**. 

#### Reading 3 — Public Equity Capture & Sovereign-Capture Guardrail (public_capture_channel)

Evaluate whether a durable publicly traded ticker captures the zone's
economic rent—or whether sovereign capture / parastatal conversion
blocks minority shareholders (**DP World delisting precedent**): 

public_capture_channelEquity Capture Tier
**"LISTED_SEZ_REIT_OR_DEVELOPER" OR "LAYER1_UTILITY_OR_PIPE_TOLLBOOTH"**
**direct_public_tollbooth** — listed REIT, logistics park, or utility captures rent directly
**"ANCHOR_INDUSTRIAL_OR_FAB_TENANT"**
**anchor_tenant_capture** — listed semiconductor/industrial operator captures tax & R&D credits
**"PARASTATAL_OR_DELISTING_RISK"**
**sovereign_capture_hazard** — state-dominated operator risks forced delisting/parastatal subordination
**"NONE_UNLISTED_OR_PAPER"**
**no_public_capture_vehicle** — municipal/state entity or paper zone with zero public ticker

If public_capture_channel is missing, treat as
**no_public_capture_vehicle**. 

#### Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four investment underwriting regimes.
Evaluate in strict priority order and select the first regime whose
conditions are fully satisfied: 

1. **UNINVESTABLE_PAPER_OR_NO_TICKER** (most severe — unconditional FLAT)
2. **SOVEREIGN_CAPTURE_OR_UNBUILT_TRAP**
3. **MODERATE_ENCLAVE_CAPTURE**
4. **VERIFIED_ENCLAVE_TOLLBOOTH** (strictest adaptive fit)

#### UNINVESTABLE_PAPER_OR_NO_TICKER

Any of the following hold: 

* Fiscal Arbitrage Tier is **paper_concept_zero_arbitrage**
(TYPE_5_PAPER_CONCEPT_ONLY, e.g., unenacted border SEZ proposals
such as Imatra).
* Operational Readiness Tier is **unbuilt_paper_zone** (< 20).
* Equity Capture Tier is **no_public_capture_vehicle**
("NONE_UNLISTED_OR_PAPER").

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT". Either the zone exists only on paper without enacted tax/permitting statutes, or no
publicly listed ticker captures its cash flows. The skill binds
unconditionally and must appear in skills_cited.

SOVEREIGN_CAPTURE_OR_UNBUILT_TRAP

Any of the following hold (and UNINVESTABLE_PAPER_OR_NO_TICKER does
not apply):
• Equity Capture Tier is sovereign_capture_hazard
("PARASTATAL_OR_DELISTING_RISK" — state-controlled operator prone to
forced delisting and parastatal conversion like DP World).
• Operational Readiness Tier is early_stage_rollout (20 to 44).
Delta cap: 0.20. High risk that sovereign intervention subordinates
minority equity holders to state industrial policy (parastatal capture)
or that physical infrastructure lags statutory promises. Restrict
sizing sharply.

MODERATE_ENCLAVE_CAPTURE

Any of the following hold (and neither UNINVESTABLE_PAPER_OR_NO_TICKER
nor SOVEREIGN_CAPTURE_OR_UNBUILT_TRAP applies):
• Fiscal Arbitrage Tier is marginal_tax_advantage (< 15.0% tax
spread, e.g., pure startup hubs without major statutory tax cuts).
• Operational Readiness Tier is developing_corridor (45 to 74).
• Equity Capture Tier is anchor_tenant_capture ("ANCHOR_INDUSTRIAL_OR_FAB_TENANT"
exposed to tenant cyclicality rather than pure infrastructure tolls).
Delta cap: 0.65. Real zone advantages exist and are captured by
listed firms, though tenant cyclicality or partial buildout prevents a
full tollbooth cap. Trim sizing relative to VERIFIED_ENCLAVE_TOLLBOOTH.

VERIFIED_ENCLAVE_TOLLBOOTH

All of the following hold:
• Fiscal Arbitrage Tier is high_fiscal_arbitrage or
moderate_fiscal_arbitrage (>= 15.0% enacted tax/payroll wedge
reduction).
• Operational Readiness Tier is turnkey_physical_corridor (>= 75).
• Equity Capture Tier is direct_public_tollbooth ("LISTED_SEZ_REIT_OR_DEVELOPER"
or "LAYER1_UTILITY_OR_PIPE_TOLLBOOTH" with durable public float).
Delta cap: 1.0. Enacted tax/payroll arbitrage + live single-window
permitting + physical grid/port throughput captured by a durable
publicly listed REIT, logistics developer, or utility pipe. The cap
equals the strategy cap; the skill never binds on
VERIFIED_ENCLAVE_TOLLBOOTH.

Ambiguous fallback

Any combination not covered above is classified
SOVEREIGN_CAPTURE_OR_UNBUILT_TRAP with delta cap 0.20.

Secondary Filter / Asymmetric Gate — Unproven Statute Hysteresis

Apply the persistence test after regime classification and before the
cap.
A zone's fiscal and operational regime is statutorily unseasoned if
years_statute_and_grid_active < 2 (fewer than two settled years of
enacted tax relief and physical throughput). Newly enacted zone decrees
frequently suffer administrative implementation delays, EU state-aid
audits, or grid-connection backlogs during their first 24 months.
If the zone is statutorily unseasoned (< 2 settled years), halve
the regime's delta cap:
• MODERATE_ENCLAVE_CAPTURE cap of 0.65 becomes 0.325.
• SOVEREIGN_CAPTURE_OR_UNBUILT_TRAP cap of 0.20 becomes 0.10.
• UNINVESTABLE_PAPER_OR_NO_TICKER cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

Canonical Zone-to-Public-Ticker Reference Map


Zone / Enclave  Archetype (zone_type) Durable Public Capture Tickers (Non-Delisted)
Grenoble Minatec (FR) TYPE_2_RD_AND_TECH_CLUSTER  SOI.PA (Soitec), STMPA.PA (STMicroelectronics), SU.PA (Schneider Electric), AI.PA (Air Liquide)
Southern Italy ZES Unica (IT) TYPE_1_INDUSTRIAL_PORT_SEZ + TYPE_3 ENEL.MI (Enel), TRN.MI (Terna), PST.MI (Poste Italiane), VGP.BR (VGP), CTPNV.AS (CTP)
Seville & Barcelona Zona Franca (ES)  TYPE_1_INDUSTRIAL_PORT_SEZ  MRL.MC (Merlin Properties), RED.MC (Redeia), NTGY.MC (Naturgy), ACS.MC (ACS)
French Outre-mer (LODEOM Credits) TYPE_3_PAYROLL_TAX_CREDIT_ZONE  ORA.PA (Orange), RUI.PA (Rubis — Caribbean/Réunion fuel & solar infrastructure)
Dahme-Spreewald (DE Trade Tax)  TYPE_4_MUNICIPAL_HOLDING_AND_STARTUP_HUB  DTG.DE (Daimler Truck — Ludwigsfelde), VNA.DE (Vonovia), LEG.DE (LEG Immobilien)
Berlin Tech Zones & Paris Station F TYPE_4_MUNICIPAL_HOLDING_AND_STARTUP_HUB  SAP.DE (SAP), CAP.PA (Capgemini), URW.PA (Unibail-Rodamco-Westfield)
India IT/R&D SEZs (Bengaluru/Pune)  TYPE_1 + TYPE_2_RD_AND_TECH_CLUSTER CY6U.SI (CapitaLand India Trust), EMBASSY.NS (Embassy Office Parks REIT), INFY (Infosys)
Middle East Port SEZs (AE / SA) TYPE_1_INDUSTRIAL_PORT_SEZ  ADPORTS.AD (AD Ports Group), 4220.SR (Emaar Economic City) — Note: DP World delisted/parastatal
Imatra Proposed Border SEZ (FI) TYPE_5_PAPER_CONCEPT_ONLY None (FLAT = 0.0) — unenacted paper proposal lacking eastern transit or enacted tax statute


The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read SEZ arbitrage dict. From
snapshot.external_data["sez_arbitrage"], load zone_type,
effective_tax_wedge_reduction_pct,
permitting_and_infra_readiness, public_capture_channel, and
years_statute_and_grid_active. If absent or empty, record
MODERATE_ENCLAVE_CAPTURE, note the omission, and do not cite this
skill.
2. Classify fiscal arbitrage tier. Apply Reading 1.
3. Classify permitting & infrastructure readiness tier. Apply
Reading 2.
4. Classify public equity capture & sovereign-capture tier. Apply
Reading 3 (enforcing the DP World delisting/parastatal guardrail).
5. Classify regime. Evaluate in strict priority order
(UNINVESTABLE_PAPER_OR_NO_TICKER →
SOVEREIGN_CAPTURE_OR_UNBUILT_TRAP → MODERATE_ENCLAVE_CAPTURE →
VERIFIED_ENCLAVE_TOLLBOOTH) (fallback:
SOVEREIGN_CAPTURE_OR_UNBUILT_TRAP).
6. Apply persistence test. If years_statute_and_grid_active < 2,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
regime is UNINVESTABLE_PAPER_OR_NO_TICKER and action == "LONG",
set delta = 0.0 and action = "FLAT" regardless of AGOP.
Otherwise, if intended delta exceeds delta_cap, reduce it to
delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
regime is UNINVESTABLE_PAPER_OR_NO_TICKER, cite
"special-economic-zone-arbitrage-yardstick" in skills_cited and
state the zone type, fiscal arbitrage tier, readiness score, and
public capture vehicle in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.65, "confidence": 0.80, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If
UNINVESTABLE_PAPER_OR_NO_TICKER and AGOP ranks LONG, action must
be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime, capture vehicle,
and cap reason. Example:
"UNINVESTABLE_PAPER_OR_NO_TICKER regime; zone_type=TYPE_5_PAPER_CONCEPT_ONLY (Imatra proposed border SEZ), effective_tax_wedge_reduction_pct=0.0%, permitting_and_infra_readiness=10, public_capture_channel=NONE_UNLISTED_OR_PAPER; forcing FLAT (0.0); special-economic-zone-arbitrage-yardstick."
• skills_cited: list of skill names; include
"special-economic-zone-arbitrage-yardstick" only when the cap bound
or the regime is UNINVESTABLE_PAPER_OR_NO_TICKER.

Worked Examples


Case A — Active industrial/port SEZ REIT or utility tollbooth with enacted tax relief, cap does not bind

Snapshot (e.g., CY6U.SI India IT SEZ REIT or MRL.MC / RED.MC Spanish port/free-zone corridor):
• zone_type = "TYPE_1_INDUSTRIAL_PORT_SEZ"
• effective_tax_wedge_reduction_pct = 42.0
• permitting_and_infra_readiness = 84
• public_capture_channel = "LISTED_SEZ_REIT_OR_DEVELOPER"
• years_statute_and_grid_active = 9
Readings:
• Fiscal Arbitrage Tier: high_fiscal_arbitrage
• Operational Readiness Tier: turnkey_physical_corridor
• Equity Capture Tier: direct_public_tollbooth
Regime: VERIFIED_ENCLAVE_TOLLBOOTH, delta cap 1.0. Persistence: 9 >= 2 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "special-economic-zone-arbitrage-yardstick".

Case B — Deep-tech R&D cluster (Minatec / SOI.PA) or parastatal delisting risk (DP World pattern), cap binds

Snapshot (e.g., SOI.PA at Grenoble Minatec):
• zone_type = "TYPE_2_RD_AND_TECH_CLUSTER"
• effective_tax_wedge_reduction_pct = 24.0
• permitting_and_infra_readiness = 88
• public_capture_channel = "ANCHOR_INDUSTRIAL_OR_FAB_TENANT"
• years_statute_and_grid_active = 15
Readings:
• Fiscal Arbitrage Tier: moderate_fiscal_arbitrage
• Operational Readiness Tier: turnkey_physical_corridor
• Equity Capture Tier: anchor_tenant_capture
Regime: MODERATE_ENCLAVE_CAPTURE, delta cap 0.65. Persistence: 15 >= 2 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 0.65 binds.
LLM returns delta = 0.65 and cites "special-economic-zone-arbitrage-yardstick".

Case C — Paper-only border SEZ proposal (Imatra) or unlisted municipal enclave without public capture ticker

Snapshot:
• zone_type = "TYPE_5_PAPER_CONCEPT_ONLY"
• effective_tax_wedge_reduction_pct = 0.0
• permitting_and_infra_readiness = 12
• public_capture_channel = "NONE_UNLISTED_OR_PAPER"
• years_statute_and_grid_active = 0
Readings:
• Fiscal Arbitrage Tier: paper_concept_zero_arbitrage
• Operational Readiness Tier: unbuilt_paper_zone
• Equity Capture Tier: no_public_capture_vehicle
Regime: UNINVESTABLE_PAPER_OR_NO_TICKER, delta cap 0.0 → forces FLAT on
LONG. AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0,
and cites "special-economic-zone-arbitrage-yardstick".

Free Data Sources

The fetcher populates snapshot.external_data["sez_arbitrage"] from
the following free, open statutory, municipal-tax, and exchange-filing
endpoints:
• UNCTAD World Investment Report & World Bank SEZ Open Database:
https://unctad.org and https://worldbank.org (free
global catalog of enacted Special Economic Zones, Freeports, and
industrial corridors).
• National Tax & Zone Registries (EU State Aid Transparency / Destatis Hebesätze / ZES Unica / INSEE):
https://europa.eu (free EU
State Aid award registry verifying enacted ZES Unica, Outre-mer LODEOM, and R&D tax credits), https://regionalstatistik.de (free
German municipal Gewerbesteuer trade-tax multipliers for enclaves
like Dahme-Spreewald), and https://insee.fr.
• Public Exchange & REIT Filings (SEC EDGAR, ESMA ESEF, SGX, NSE, ADX, Tadawul):
Verifying active public float, delisting/take-private notices (such
as DP World’s delisting into Dubai World), and asset concentration
inside zone perimeters.

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not treat political speeches or proposed zone studies (e.g.,
Imatra border SEZ concepts) as enacted fiscal arbitrage; classify them
unconditionally as TYPE_5_PAPER_CONCEPT_ONLY (FLAT = 0.0).
• Do not treat delisted or sovereign-captured operators (such as DP World)
as liquid public equities; enforce the PARASTATAL_OR_DELISTING_RISK
cap whenever state control threatens minority shareholders.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "special-economic-zone-arbitrage-yardstick" when the cap
did not bind and the regime is not UNINVESTABLE_PAPER_OR_NO_TICKER.

Citation Mapping

• Institutional Enclaves & Transaction-Cost Reduction: Douglass C.
North, Institutions, Institutional Change and Economic Performance
(Cambridge University Press, 1990); Mancur Olson, The Rise and
Decline of Nations (Yale University Press, 1982).
• Global SEZ Typology, Fiscal Incentives & Parastatal Governance:
UNCTAD, World Investment Report: Special Economic Zones (United
Nations); World Bank Group, Special Economic Zones: An Operational
Review of Their Impacts (World Bank).
• Bounded Supervisory Control: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
