#### name: "private-equity-underwriting"
description: "Underwrite private equity and collective investment vehicles via classical political economy (Karl Marx, Das Kapital Vol. III Ch. 27; Rudolf Hilferding, Finance Capital): evaluate collective capital strictly on (1) direct ownership of tangible domestic physical infrastructure, (2) high realized cash dividend yield prioritized over mark-to-model Sharpe ratios, and (3) power-law unsmoothed Sharpe and leverage discipline using free SEC EDGAR (BDC/Form D/ADV), ESMA, Companies House, PRH, and OECD data; force FLAT on leveraged LBO asset-stripping and fee-skimming paper roll-ups."

#### Private Equity & Collective Means-of-Production Underwriting

You are reading the tick against the **structural productive legitimacy
of a private equity fund, business development company (BDC),
infrastructure consortium, or collective investment vehicle**. In Karl
Marx's *Das Kapital*, Volume III, Chapter 27 (*"The Role of Credit in
Capitalist Production"*, 1894), Rudolf Hilferding's *Finance Capital*
(1910), and William Lazonick & Mary O'Sullivan's *"Maximizing
Shareholder Value: A New Ideology for Corporate Governance"* (*Economy
and Society*, 2000), pooled collective capital represents the **socialization
of the means of production within finance**—which diverges into two
irreconcilable regimes: 

1. **Productive Collective Ownership (INFRA_DIVIDEND_ANCHOR):** Pooled
capital directly owns and upgrades **tangible domestic productive
infrastructure** (grids, rail, ports, industrial plants, telecoms,
water, and base manufacturing) on conservative leverage, distributing
high, recurring **cash dividend yields** out of genuine operating
surplus—with **cash dividend yield strictly prioritized over
mark-to-model Sharpe ratios**.
2. **Parasitic Financialized LBO Extraction (LBO_ASSET_STRIPPER):**
Pooled capital acts as a debt-bloated fee siphon—loading productive
enterprises with predatory leverage (> 5.5× Debt/EBITDA), stripping
domestic real estate via sale-leasebacks, paying zero or debt-funded
dividends, and hiding behind artificially smoothed quarterly
mark-to-model "Sharpe ratios" while charging 2-and-20 management
tolls.

All three evaluation axes—domestic infrastructure share, cash dividend
yield, and unsmoothed return-to-risk—follow **power-law distributions**
across private vehicles: a tiny top decile of unlevered or modestly
levered domestic infrastructure owners generates the vast majority of
real cash dividends, while the long tail of leveraged buyout roll-ups
destroys productive capacity. 

Your job is to classify the private equity vehicle or sector exposure
into one of four underwriting regimes and cap your delta accordingly.
You do not invent trades. You do not override AGOP. You modulate the
LLM's delta within the bound the verifier already permits. You never
raise delta above the strategy cap, and you never invent an action
outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["private_equity"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes regulatory filings (SEC EDGAR Form N-2/10-K/ADV,
Companies House, ESMA, PRH), infrastructure registries, and
cash-distribution series into snapshot.external_data["private_equity"]: 

* domestic_infra_ownership_share_pct: percentage (0.0 to 100.0) of
fund net asset value (NAV) invested directly in **tangible domestic
productive infrastructure and physical means of production** (energy
grids, transport/ports, industrial manufacturing, water, fiber/telecom)
rather than offshore holding shells, software roll-ups, or financial
intermediaries (≥ 65% = true domestic infrastructure steward;
< 20% = financialized paper/offshore roll-up).
* realized_cash_dividend_yield_pct: trailing 12-month **cash dividend
yield** (0.0 to 25.0) funded strictly from **operating free cash
flow** (excluding debt-funded dividend recapitalizations and return-of-capital
accounting tricks; ≥ 7.0% = high productive cash distribution;
< 2.0% = cash-starved / fee-skimmed vehicle).
* unsmoothed_sharpe_ratio: de-smoothed (Geltner-adjusted) power-law
return-to-volatility ratio (-1.0 to 3.0) paired with portfolio
net leverage (portfolio_net_debt_to_ebitda). Cash dividend yield
always outranks Sharpe ratio in the decision matrix (dividend_over_sharpe_priority).
* consecutive_cash_starvation_quarters: consecutive calendar quarters
in which operating cash dividend yield sits < 3.0% OR portfolio
leverage exceeds 5.0× Net Debt/EBITDA.

If snapshot.external_data["private_equity"] is absent or empty, treat
the instrument as **unmonitored**, record state **INFRA_DIVIDEND_ANCHOR**,
note that no private-equity telemetry was available, and do not cite
this skill. 

#### Reading 1 — Domestic Physical Infrastructure Share (domestic_infra_ownership_share_pct)

Evaluate whether collective capital actually owns tangible domestic
means of production: 

domestic_infra_ownership_share_pctMeans-of-Production Tier
**≥ 65.0%**
**domestic_infra_core** — majority direct ownership of tangible domestic physical infrastructure
**40.0% to 65.0%**
**mixed_industrial** — substantial domestic physical assets paired with commercial holdings
**20.0% to 40.0%**
**financialized_tilt** — minority physical infrastructure; heavy service/software/offshore weighting
**< 20.0%**
**paper_rollup_shell** — virtually zero domestic physical infrastructure; pure financial engineering

If domestic_infra_ownership_share_pct is missing, treat as
**financialized_tilt**. 

#### Reading 2 — Operating Cash Dividend Yield (realized_cash_dividend_yield_pct) — Primary Financial Criterion

Evaluate hard operating cash yield distributed to collective owners
(strictly prioritized over Sharpe ratio): 

realized_cash_dividend_yield_pctCash Yield Tier (Primary)
**≥ 7.0%**
**high_cash_dividend** — strong, recurring operating-surplus cash distribution (≥ 7.0%)
**4.5% to 7.0%**
**moderate_cash_dividend** — respectable operating cash yield; covers inflation and cost of capital
**2.0% to 4.5%**
**thin_cash_yield** — management fees and debt service absorbing most operating surplus
**< 2.0%**
**dividend_starved** — zero or negligible operating cash yield; J-curve fee/leverage extraction

If realized_cash_dividend_yield_pct is missing, treat as
**thin_cash_yield**. 

#### Reading 3 — Unsmoothed Sharpe & Leverage Discipline (unsmoothed_sharpe_ratio & portfolio_net_debt_to_ebitda) — Secondary Financial Criterion

Evaluate power-law risk-adjusted efficiency after stripping mark-to-model
appraisal smoothing (secondary to Cash Dividend Yield): 

unsmoothed_sharpe_ratio & LeverageSharpe & Leverage Tier (Secondary)
**Sharpe ≥ 1.10 AND Debt/EBITDA ≤ 3.0×**
**high_sharpe_conservative** — genuine power-law surplus with unbloated balance sheet
**Sharpe 0.60 to 1.10 AND Debt/EBITDA ≤ 4.5×**
**solid_sharpe_moderate_debt** — healthy risk-adjusted output with manageable leverage
**Sharpe < 0.60 OR Debt/EBITDA 4.5× to 5.5×**
**weak_sharpe_or_levered** — appraisal smoothing masking volatility or heavy debt burden
**Sharpe < 0.25 OR Debt/EBITDA > 5.5×**
**predatory_lbo_leverage** — debt-loaded asset stripping; severe insolvency tail risk

If unsmoothed_sharpe_ratio or leverage is missing, treat as
**weak_sharpe_or_levered**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
private-equity underwriting regimes—enforcing **Cash Dividend Yield >
Sharpe Ratio** priority at every step. Evaluate in strict priority order
and select the first regime whose conditions are fully satisfied: 

1. **LBO_ASSET_STRIPPER** (most severe — unconditional FLAT)
2. **FEE_EXTRACTION_VEHICLE**
3. **SHARPE_WITHOUT_DIVIDEND_DRAG**
4. **INFRA_DIVIDEND_ANCHOR** (strictest adaptive fit)

#### LBO_ASSET_STRIPPER

Any of the following hold: 

* Sharpe & Leverage Tier is **predatory_lbo_leverage** (Debt/EBITDA > 5.5×
or unsmoothed_sharpe_ratio < 0.25).
* Means-of-Production Tier is **paper_rollup_shell** (< 20.0% domestic
infrastructure) AND Cash Yield Tier is **dividend_starved** (< 2.0%).
* Cash Yield Tier is **dividend_starved** (< 2.0%) AND Sharpe &
Leverage Tier is **weak_sharpe_or_levered**.

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. The vehicle is a debt-bloated LBO or fee-skimming
shell that starves collective owners of operating cash dividends while
hollowing out physical production. The skill binds unconditionally and
must appear in skills_cited. 

#### FEE_EXTRACTION_VEHICLE

Any of the following hold (and LBO_ASSET_STRIPPER does not apply): 

* Cash Yield Tier is **dividend_starved** (< 2.0%) even if smoothed
Sharpe looks high (enforcing **Cash Dividend Yield > Sharpe Ratio**).
* Cash Yield Tier is **thin_cash_yield** (2.0% to 4.5%) AND
Means-of-Production Tier is **paper_rollup_shell** or
**financialized_tilt** (< 40.0%).

**Delta cap: 0.20.** High GP fee layers or offshore paper financialization
are intercepting the surplus before it reaches collective owners as
cash dividends. Cut exposure sharply. 

#### SHARPE_WITHOUT_DIVIDEND_DRAG

Any of the following hold (and neither LBO_ASSET_STRIPPER nor
FEE_EXTRACTION_VEHICLE applies): 

* Cash Yield Tier is **moderate_cash_dividend** (4.5% to 7.0%) OR
**thin_cash_yield** (2.0% to 4.5%) with domestic_infra_core or
mixed_industrial (≥ 40.0% domestic physical infrastructure).
* Cash Yield Tier is **high_cash_dividend** (≥ 7.0%) AND
Means-of-Production Tier is **financialized_tilt** or
**paper_rollup_shell** (< 40.0% domestic infrastructure).
Delta cap: 0.65. Solid productive cash flow or Sharpe discipline,
but either cash dividend yield falls short of the ≥ 7.0% elite power-law
tier or assets sit outside domestic physical infrastructure. Trim sizing
relative to INFRA_DIVIDEND_ANCHOR.

INFRA_DIVIDEND_ANCHOR

All of the following hold:
• Means-of-Production Tier is domestic_infra_core (≥ 65.0% direct
ownership of tangible domestic productive infrastructure).
• Cash Yield Tier is high_cash_dividend (≥ 7.0% operating-surplus
cash dividend yield — primary criterion satisfied).
• Sharpe & Leverage Tier is high_sharpe_conservative or
solid_sharpe_moderate_debt (unsmoothed_sharpe_ratio >= 0.60 and
Debt/EBITDA <= 4.5×).
Delta cap: 1.0. True productive collective ownership of the domestic
means of production: unbloated leverage, tangible national infrastructure,
and high operating cash dividends outranking paper Sharpe metrics. The
cap equals the strategy cap; the skill never binds on
INFRA_DIVIDEND_ANCHOR.

Ambiguous fallback

Any combination not covered above is classified FEE_EXTRACTION_VEHICLE
with delta cap 0.20.

Secondary Filter / Asymmetric Gate — Sustained Cash-Starvation Hysteresis

Apply the persistence test after regime classification and before the
cap.
Surplus extraction is structurally entrenched if
consecutive_cash_starvation_quarters >= 4 (four or more consecutive
quarters with operating cash dividend yield < 3.0% or portfolio
leverage > 5.0× Net Debt/EBITDA). A full year of withholding operating
cash distributions while running elevated LBO debt confirms that GP
fees and creditors are permanently expropriating the collective surplus.
If the extraction is structurally entrenched, halve the regime's
delta cap:
• SHARPE_WITHOUT_DIVIDEND_DRAG cap of 0.65 becomes 0.325.
• FEE_EXTRACTION_VEHICLE cap of 0.20 becomes 0.10.
• LBO_ASSET_STRIPPER cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read private equity dict. From
snapshot.external_data["private_equity"], load
domestic_infra_ownership_share_pct,
realized_cash_dividend_yield_pct, unsmoothed_sharpe_ratio,
portfolio_net_debt_to_ebitda, and
consecutive_cash_starvation_quarters. If absent or empty, record
INFRA_DIVIDEND_ANCHOR, note the omission, and do not cite this
skill.
2. Classify means-of-production tier. Apply Reading 1
(domestic_infra_core, mixed_industrial, financialized_tilt, or
paper_rollup_shell).
3. Classify cash yield tier (Primary). Apply Reading 2
(high_cash_dividend, moderate_cash_dividend, thin_cash_yield,
or dividend_starved).
4. Classify Sharpe & leverage tier (Secondary). Apply Reading 3
(high_sharpe_conservative, solid_sharpe_moderate_debt,
weak_sharpe_or_levered, or predatory_lbo_leverage).
5. Classify regime. Evaluate in strict priority order
(LBO_ASSET_STRIPPER → FEE_EXTRACTION_VEHICLE →
SHARPE_WITHOUT_DIVIDEND_DRAG → INFRA_DIVIDEND_ANCHOR) enforcing
Cash Dividend Yield > Sharpe Ratio priority (fallback:
FEE_EXTRACTION_VEHICLE).
6. Apply persistence test. If
consecutive_cash_starvation_quarters >= 4, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
regime is LBO_ASSET_STRIPPER, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
regime is LBO_ASSET_STRIPPER, cite
"private-equity-underwriting" in skills_cited and state the
domestic infrastructure share, cash dividend yield, and leverage
finding in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If LBO_ASSET_STRIPPER,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the regime and cap reason.
Example:
"LBO_ASSET_STRIPPER regime; domestic_infra_share=14.0% (paper_rollup_shell), cash_dividend_yield=1.1% (dividend_starved), and 6.4x Debt/EBITDA predatory leverage; forcing action=FLAT; private-equity-underwriting."
• skills_cited: list of skill names; include
"private-equity-underwriting" only when the cap bound or the
regime is LBO_ASSET_STRIPPER.

Worked Examples


Case A — Domestic infrastructure consortium with 8.2% operating cash dividend yield and low leverage, cap does not bind

Snapshot:
• domestic_infra_ownership_share_pct = 78.0
• realized_cash_dividend_yield_pct = 8.2
• unsmoothed_sharpe_ratio = 1.15
• portfolio_net_debt_to_ebitda = 2.6
• consecutive_cash_starvation_quarters = 0
Readings:
• Means-of-Production Tier: ≥ 65.0% → domestic_infra_core
• Cash Yield Tier (Primary): ≥ 7.0% → high_cash_dividend
• Sharpe & Leverage Tier (Secondary): ≥ 1.10 & ≤ 3.0× → high_sharpe_conservative
Regime: INFRA_DIVIDEND_ANCHOR, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "private-equity-underwriting".

Case B — High mark-to-model Sharpe (1.40) but 1.2% cash dividend yield (dividend_starved), cash yield priority binds

Snapshot:
• domestic_infra_ownership_share_pct = 45.0
• realized_cash_dividend_yield_pct = 1.2
• unsmoothed_sharpe_ratio = 1.40
• portfolio_net_debt_to_ebitda = 3.8
• consecutive_cash_starvation_quarters = 5
Readings:
• Means-of-Production Tier: 40.0% to 65.0% → mixed_industrial
• Cash Yield Tier (Primary): < 2.0% → dividend_starved
• Sharpe & Leverage Tier (Secondary): solid_sharpe_moderate_debt
Regime: FEE_EXTRACTION_VEHICLE, delta cap 0.20 (Cash Dividend Yield
prioritized over smoothed Sharpe). Persistence: 5 >= 4 → halve to
0.10. AGOP ranks LONG. LLM intended delta = 0.80. Cap 0.10
binds. LLM returns delta = 0.10 and cites "private-equity-underwriting".

Case C — Debt-loaded LBO paper roll-up at 6.3x Debt/EBITDA, unconditional FLAT

Snapshot:
• domestic_infra_ownership_share_pct = 15.0
• realized_cash_dividend_yield_pct = 0.5
• unsmoothed_sharpe_ratio = 0.40
• portfolio_net_debt_to_ebitda = 6.3
• consecutive_cash_starvation_quarters = 6
Readings:
• Means-of-Production Tier: < 20.0% → paper_rollup_shell
• Cash Yield Tier (Primary): < 2.0% → dividend_starved
• Sharpe & Leverage Tier (Secondary): > 5.5× → predatory_lbo_leverage
Regime: LBO_ASSET_STRIPPER, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "private-equity-underwriting".

Free Data Sources

The fetcher populates snapshot.external_data["private_equity"] from
the following free, open public fund-filing, corporate-registry, and
infrastructure-yield sources (no paid PitchBook/Preqin subscription
required):
• U.S. SEC EDGAR (BDC Forms 10-K/10-Q/N-2, Form ADV & Form D APIs):
https://sec.gov (free JSON/XBRL APIs for publicly traded Business
Development Companies, listed private-equity/infrastructure funds,
debt-to-equity ratios, portfolio company schedules, and cash dividend
distributions).
• ESMA AIFMD Registers & European Long-Term Investment Fund (ELTIF) Database:
https://europa.eu (free open registers and aggregate leverage/asset-class
reports for EU Alternative Investment Funds and domestic infrastructure
vehicles).
• UK Companies House API & London Stock Exchange Listed Infrastructure/PE Filings:
https://service.gov.uk (free REST API for UK
investment trusts, infrastructure funds, balance-sheet debt, and
dividend histories).
• Finnish Patent and Registration Office (PRH Open Data) & Nordic Listed PE/Infra Filings:
https://prh.fi (free open company and annual-account
registries verifying domestic infrastructure ownership and operating
cash payouts).
• OECD Pension Markets in Focus & Infrastructure Investment Indicators:
https://oecd.org (free open datasets tracking institutional
allocations to domestic physical infrastructure vs. leveraged buyouts).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not let a high mark-to-model Sharpe ratio override a low or
debt-funded operating cash dividend yield (Cash Dividend Yield > Sharpe Ratio is mandatory).
• Do not count debt-funded dividend recapitalizations as operating cash
dividend yield (realized_cash_dividend_yield_pct).
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "private-equity-underwriting" when the cap did not bind
and the regime is not LBO_ASSET_STRIPPER.

Citation Mapping

• Socialization of Capital & Collective Means of Production: Karl
Marx, Das Kapital: A Critique of Political Economy, Volume III,
Chapter 27 ("The Role of Credit in Capitalist Production", 1894);
Rudolf Hilferding, Finance Capital: A Study of the Latest Phase of
Capitalist Development (1910).
• Financialization vs. Productive Reinvestment: William Lazonick and
Mary O'Sullivan, "Maximizing Shareholder Value: A New Ideology for
Corporate Governance," Economy and Society 29(1), 13–35 (2000).
• Private-Equity Appraisal Smoothing & De-Smoothed Sharpe: David
Geltner, "Estimating Market Values from Appraised Values without
Assuming an Efficient Market," Journal of Real Estate Research 8(3),
325–345 (1993).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
