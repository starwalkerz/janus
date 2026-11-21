---
name: "resource-underwriting"
description: "Classify the tick into one of four resource-underwriting states (PREMIUM, PASSABLE, SPECULATIVE, AVOID) using a two-pass framework (Durrett asset-quality and Rule enterprise-quality), the Lassonde lifecycle position, and terminal repurpose value; cap delta as underwriting quality degrades."
---

# Resource Underwriting

You are reading the tick against the underwriting state of the
productive resource to which the tick is exposed. Every economically
productive resource is functionally a mine: it has a stock, a
concentration, an accessibility, an extractable fraction, a unit cost,
a productive lifetime, and a terminal state. The two analytical
traditions that this skill condenses both apply to it. Don Durrett's
published checklists establish what the resource might be worth: the
verification level of the stock, its grade or quality, its
accessibility, its unit economics. Rick Rule's published framework
establishes whether the enterprise controlling the resource can
realize that value: the management's track record at this lifecycle
stage, the balance sheet's ability to finance the next milestone, the
ownership alignment, the dilution risk. The two passes are computed
independently. The synthesis only reconciles them; it does not
conflate them.

Your job is to classify the tick into one of four underwriting states
and cap your `delta` accordingly. The state is a risk gate, not a
forecast. You do not invent trades. You do not override AGOP. You
modulate the LLM's delta within the bound the verifier already
permits. You never raise `delta` above the strategy cap, and you never
invent an action outside `allowed_actions`.

## The Readings

The fetcher supplies the underwriting assessment in
`snapshot.external_data["resource_underwriting"]`. The assessment is
computed offline by the operator's underwriting pipeline, which
performs the numerical work (NPV, IRR, AISC, EROI) and produces the
qualitative pass states that this skill reads. The skill does not
compute those figures; it classifies the state and caps the delta.

The dict contains:

- `asset_pass`: `strong`, `adequate`, `weak`, or `fail`.
- `asset_notes`: free-form text citing the specific sub-readings.
- `enterprise_pass`: `strong`, `adequate`, `weak`, or `fail`.
- `enterprise_notes`: free-form text citing the specific sub-readings.
- `lifecycle`: `EARLY`, `DEVELOPMENT`, `CONSTRUCTION`, `PRODUCTION`,
  or `DECLINE`.
- `lifecycle_stage`: the specific Lassonde stage, for audit.
- `terminal_value`: `positive`, `neutral`, `impaired`, or `negative`.
- `terminal_notes`: free-form text.
- `next_milestone_cost`: the capital required to reach the next
  value-creating milestone.
- `liquid_assets`: cash plus undrawn facilities plus non-dilutive
  sources available to the enterprise.
- `dilution_if_financed`: the estimated percentage of current shares
  outstanding that would need to be issued to raise the shortfall.

If `resource_underwriting` is absent, treat the state as **PASSABLE**
with delta cap 0.75, note that no underwriting assessment was
available, and do not cite this skill. The skill cannot cap without a
signal, and absence of an assessment is not evidence of a weak
resource.

### Reading 1 — Asset-quality pass (Durrett)

The asset pass is a composite of four sub-readings that the offline
pipeline computes. The skill reads only the composite, not the
sub-readings, but the composite must be defensible from them.

The four sub-readings:

- **Stock verification.** Whether the resource is measured and
  indicated under a recognised reporting standard (NI 43-101,
  JORC, SAMREC, SK-1300, or the equivalent for the resource class),
  or indicated only, or inferred only, or historical only.
- **Concentration and quality.** Whether the grade, quality, or
  productive density is at the top quartile of peers, at the peer
  median, at the bottom quartile, or below economic threshold.
- **Accessibility.** Whether the resource is at surface and near
  infrastructure, at depth with established access, in a remote but
  serviced location, or in a remote unserviced location or a
  restricted jurisdiction.
- **Unit economics.** Whether the all-in sustaining cost, levelized
  cost, or equivalent unit cost is in the lowest quartile of the
  cost curve, at the median, above the median but below the
  marginal producer, or above the marginal producer.

The composite:

| Composite | Conditions |
|---|---|
| **strong** | All four sub-readings at the top two levels of their scales |
| **adequate** | All four sub-readings at or above the peer median, with at most one at the third level |
| **weak** | Two or more sub-readings at the third level, or one at the fourth level with the others adequate |
| **fail** | Any sub-reading below the economic threshold, or two or more at the fourth level |

If a sub-reading is missing, the pipeline must record it as
`unknown`, and the composite cannot exceed **adequate**. The skill
reads the composite; it does not attempt to reconstruct it.

### Reading 2 — Enterprise-quality pass (Rule)

The enterprise pass is a composite of three sub-readings.

- **Management track record.** Whether the management team has
  previously built, financed, or operated a resource at the same
  lifecycle stage, at an adjacent stage, at no prior stage, or has
  a documented failure at this stage.
- **Balance sheet and financing runway.** Whether liquid assets
  cover the next milestone, cover the next two milestones, cover
  operating expenses for twelve months but not the milestone, or
  cover less than six months.
- **Ownership alignment.** Whether insiders own a substantial
  stake, insiders own a moderate stake, insiders own only option
  grants, or the ownership is dispersed with no aligned block.

The composite:

| Composite | Conditions |
|---|---|
| **strong** | All three sub-readings at the top level |
| **adequate** | All three at or above the second level, with at most one at the third |
| **weak** | Any sub-reading at the third level, with the others adequate or better |
| **fail** | Any sub-reading at the fourth level |

If a sub-reading is missing, the composite cannot exceed **adequate**.

### Reading 3 — Lifecycle position (Lassonde)

Read `lifecycle` from the assessment. The five positions map to the
Lassonde curve as follows:

| Lifecycle | Lassonde stages covered |
|---|---|
| **EARLY** | identification, discovery, resource definition |
| **DEVELOPMENT** | feasibility, permitting, financing for construction |
| **CONSTRUCTION** | detailed engineering, construction, commissioning |
| **PRODUCTION** | steady-state production and cash generation |
| **DECLINE** | declining grade or throughput, approaching obsolescence |

The lifecycle position is not a quality reading. It is a risk
category. EARLY and DECLINE carry structural risks that cap the
overall state regardless of how strong the asset and enterprise
passes are.

### Reading 4 — Terminal and alternative-use value

Read `terminal_value` from the assessment. The four levels:

| Terminal | Meaning |
|---|---|
| **positive** | A defensible repurposing pathway with positive NPV (e.g., open-pit mine to pumped hydro, patent to public domain generating secondary licensing, depleted reservoir to thermal storage) |
| **neutral** | No net liability and no net value at end of life |
| **impaired** | Decommissioning or restoration costs exceed residual value but do not threaten the enterprise |
| **negative** | Environmental or social liabilities exceed any residual value and could consume enterprise equity |

The terminal reading cannot upgrade the state. It can only confirm it
or degrade it. This asymmetry is deliberate: the terminal state is
the least observable part of the underwriting, and optimistic
repurposing assumptions have a long history of disappointing the
underwriter. The skill treats a positive terminal reading as
confirmatory evidence, never as a reason to reduce the cap.

## Taxonomy / Decision Matrix

Combine the four readings into one of four underwriting states. The
states are evaluated in the following priority order and the first
state whose conditions are fully satisfied is the classification:

1. **AVOID** (checked first; the most severe)
2. **SPECULATIVE**
3. **PASSABLE**
4. **PREMIUM** (checked last; the strictest adaptive fit)

The state is derived from the worst of the asset and enterprise
passes. Let `worst_pass = min(asset_pass, enterprise_pass)` where
`fail < weak < adequate < strong`. The lifecycle and terminal readings
are then applied as additional constraints.

### AVOID

Any of the following hold:

- `worst_pass` is **fail**.
- `terminal_value` is **negative**.

**Delta cap: 0.0.** Set `delta = 0.0` and `action = "FLAT"`
regardless of what AGOP ranked. The skill binds unconditionally on an
AVOID classification and must appear in `skills_cited`.

### SPECULATIVE

Any of the following hold (and AVOID does not apply):

- `worst_pass` is **weak**.
- `lifecycle` is **EARLY**.
- `lifecycle` is **DECLINE**.
- `terminal_value` is **impaired**.

**Delta cap: 0.25.** The underwriting is not yet defensible for a
sized position. The asset may be strong and the enterprise weak, or
the enterprise strong and the asset weak, or the asset and enterprise
acceptable but the lifecycle at a stage where most value destruction
occurs. Trade only at reduced size; in most cases the AGOP ranking
will not justify a position here without a specific catalyst that the
underwriting pipeline has already captured.

### PASSABLE

All of the following hold:

- `worst_pass` is **adequate**.
- `lifecycle` is **DEVELOPMENT**, **CONSTRUCTION**, or **PRODUCTION**.
- `terminal_value` is **positive** or **neutral**.

**Delta cap: 0.75.** The asset and enterprise are both adequate; the
lifecycle is in a stage where the enterprise can execute; the terminal
position is not a liability. Reduce size relative to PREMIUM.

### PREMIUM

All of the following hold:

- `asset_pass` is **strong**.
- `enterprise_pass` is **strong**.
- `lifecycle` is **DEVELOPMENT**, **CONSTRUCTION**, or **PRODUCTION**.
- `terminal_value` is **positive** or **neutral**.

**Delta cap: 1.0.** The asset, the enterprise, and the lifecycle are
all aligned. No underwriting constraint on sizing. The cap equals the
strategy cap; the skill can never bind on a PREMIUM classification
because no valid `delta` exceeds 1.0.

### Ambiguous fallback

Any combination not covered by the four states above is classified
**SPECULATIVE** with delta cap 0.25. The skill errs toward caution
because the cost of underwriting a broken resource enterprise exceeds
the cost of declining a working one.

## Secondary Filter / Asymmetric Gate — Milestone-Financing Test

Apply the milestone-financing test after the state classification and
before the cap. The gate codifies Rule's pre-revenue resource process:
the enterprise must be able to finance the next milestone without
unacceptable dilution, or the analyst must have identified a
non-dilutive source.

Read `next_milestone_cost`, `liquid_assets`, and
`dilution_if_financed` from the assessment.

Define `shortfall = max(0, next_milestone_cost - liquid_assets)`.

- If `shortfall > 0` AND `dilution_if_financed > 30`: **force AVOID**
  (`delta = 0.0`, `action = "FLAT"`). The financing gap is severe
  enough that the existing equity would be materially destroyed in
  the raise, which converts a marginally acceptable underwriting into
  an unacceptable one.
- If `shortfall > 0` AND `dilution_if_financed ≤ 30`: **halve the
  cap**. PASSABLE cap of 0.75 becomes **0.375**. SPECULATIVE cap of
  0.25 becomes **0.125**. PREMIUM cap of 1.0 becomes **0.5** (this
  case is rare and only arises when the enterprise pass was strong
  but the next milestone is outside the twelve-month window).
- If `shortfall ≤ 0`: do not change the cap.

The gate is one-way. It can only lower the cap or force AVOID. It
cannot raise the cap. It cannot change the state classification.

If `next_milestone_cost` or `liquid_assets` is missing, the gate does
not fire and the state's cap applies unmodified. The operator's
underwriting pipeline is responsible for supplying these fields when
the lifecycle is DEVELOPMENT or CONSTRUCTION.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read the underwriting dict.** From
   `snapshot.external_data["resource_underwriting"]`, load the eight
   fields listed in the Readings section. If the dict is absent,
   record state **PASSABLE**, note the absence, and skip to step 7
   with a note that no underwriting assessment was available.

2. **Read the asset pass.** Record `asset_pass` as `strong`,
   `adequate`, `weak`, or `fail`. Record `asset_notes` for the
   rationale.

3. **Read the enterprise pass.** Record `enterprise_pass` as
   `strong`, `adequate`, `weak`, or `fail`. Record
   `enterprise_notes` for the rationale.

4. **Read the lifecycle position.** Record `lifecycle` as `EARLY`,
   `DEVELOPMENT`, `CONSTRUCTION`, `PRODUCTION`, or `DECLINE`.

5. **Read the terminal value.** Record `terminal_value` as
   `positive`, `neutral`, `impaired`, or `negative`.

6. **Classify state.** Evaluate in the priority order AVOID,
   SPECULATIVE, PASSABLE, PREMIUM and take the first state whose
   conditions are fully satisfied. If no state matches, record
   SPECULATIVE as the ambiguous fallback.

7. **Apply milestone-financing gate.** Read `next_milestone_cost`,
   `liquid_assets`, and `dilution_if_financed`. If `shortfall > 0` and
   `dilution_if_financed > 30`, force AVOID and record `delta = 0.0`,
   `action = "FLAT"`. Else if `shortfall > 0` and
   `dilution_if_financed ≤ 30`, halve the cap. Else leave the cap
   unchanged.

8. **Cap delta.** Let `delta_cap` be the value from steps 6–7. If
   the intended `delta` exceeds `delta_cap`, reduce it to
   `delta_cap`. If the gate forced AVOID, `delta = 0.0` and
   `action = "FLAT"` regardless of the AGOP ranking. Record the final
   `delta` and `action`.

9. **Cite.** If the cap bound (i.e., the intended delta was above
   the cap) or the gate forced AVOID, cite `"resource-underwriting"`
   in `skills_cited` and state the underwriting state in the
   rationale. If the cap did not bind, do not cite the skill.

## The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this
order:

```json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
```

The fields:

- `action`: a string. One of `"LONG"`, `"FLAT"`, `"SHORT"`. Must
  appear in the AGOP ranking or be `"FLAT"`. Invariant I1 enforces
  this independently of anything you produce. If the milestone-
  financing gate forces AVOID, `action` must be `"FLAT"`.

- `delta`: a floating-point number in `[0.0, 1.0]`. The final
  position size is `delta` multiplied by the risk engine's upper
  bound. The underwriting cap restricts `delta` further; it does not
  replace the risk bound. If the gate forces AVOID, `delta` must be
  `0.0`.

- `confidence`: a floating-point number in `[0.0, 1.0]`. Reflects the
  confidence in the rationale, not the trade. The strategy's
  confidence floor (0.40 for OPPORTUNITY, 0.45 for AGGRESSIVE, 0.65
  for CONSERVATIVE) rejects responses below the threshold.

- `rationale`: a free-form string. Names the underwriting state and
  the reason for any cap. Example: "SPECULATIVE state; asset_pass
  adequate with inferred-only stock, enterprise_pass weak because
  dilution_if_financed 62 % on next milestone; delta capped at
  0.125; resource-underwriting."

- `skills_cited`: a list of skill names. Include
  `"resource-underwriting"` only if the cap bound or the gate forced
  AVOID. Include the skills that actually drove the choice otherwise.

## Worked Examples

### Case A — Premium state, cap does not bind

Fetcher supplies:

- `asset_pass` = **strong** (`asset_notes`: NI 43-101 measured and
  indicated reserve, grade at peer top quartile, surface access with
  established infrastructure, AISC at 30th percentile of the cost
  curve).
- `enterprise_pass` = **strong** (`enterprise_notes`: management has
  built three mines at this scale, cash covers the next two
  milestones, insiders own 15 % on a fully diluted basis).
- `lifecycle` = **PRODUCTION** (`lifecycle_stage`: steady-state
  production year 4 of an 18-year mine life).
- `terminal_value` = **positive** (`terminal_notes`: pit lake already
  studied for pumped-hydro repurposing with positive NPV).
- `next_milestone_cost` = 0 (the enterprise is in production; there
  is no next value-creating milestone requiring external capital).
- `liquid_assets` = 200,000,000.
- `dilution_if_financed` = 0.

Readings:

- Asset pass: **strong**.
- Enterprise pass: **strong**.
- Lifecycle: **PRODUCTION**.
- Terminal: **positive**.

State (priority AVOID → SPECULATIVE → PASSABLE → PREMIUM):

- AVOID? `worst_pass` is strong; terminal is positive. No.
- SPECULATIVE? `worst_pass` is strong; lifecycle is PRODUCTION;
  terminal is positive. No.
- PASSABLE? `worst_pass` is strong, not adequate. No (the PASSABLE
  condition requires the worst pass to be adequate, and strong
  exceeds that; the priority order means we check PASSABLE's
  conditions next, then PREMIUM's).
- PREMIUM? Asset strong ✓, enterprise strong ✓, lifecycle PRODUCTION
  ✓, terminal positive ✓. **PREMIUM** matches.

Delta cap 1.0.

Milestone-financing gate: `next_milestone_cost` = 0, shortfall = 0 →
gate does not fire. Cap remains 1.0.

AGOP ranks LONG. LLM intended delta 0.90. Cap 1.0 does not bind. LLM
returns delta 0.90, does not cite `resource-underwriting`, and cites
whichever skills drove the directional choice.

### Case B — Speculative state, milestone-financing gate forces AVOID

Fetcher supplies:

- `asset_pass` = **adequate** (`asset_notes`: inferred resource only
  pending feasibility, grade at peer median, remote but serviced
  access, AISC at 65th percentile).
- `enterprise_pass` = **weak** (`enterprise_notes`: management has
  never built at this scale, cash covers three months of G&A but not
  the feasibility study, insiders own only option grants).
- `lifecycle` = **DEVELOPMENT** (`lifecycle_stage`: feasibility
  study not yet funded).
- `terminal_value` = **neutral** (`terminal_notes`: standard
  reclamation obligation, no alternative-use pathway identified).
- `next_milestone_cost` = 150,000,000 (feasibility study and
  permitting).
- `liquid_assets` = 30,000,000.
- `dilution_if_financed` = 62.

Readings:

- Asset pass: **adequate**.
- Enterprise pass: **weak**.
- Lifecycle: **DEVELOPMENT**.
- Terminal: **neutral**.

State (priority AVOID → SPECULATIVE → PASSABLE → PREMIUM):

- AVOID? `worst_pass` = min(adequate, weak) = **weak**, not fail.
  Terminal is neutral, not negative. No.
- SPECULATIVE? `worst_pass` is weak → matches. **SPECULATIVE**.

Delta cap 0.25.

Milestone-financing gate: `shortfall` = 150,000,000 − 30,000,000 =
120,000,000 > 0. `dilution_if_financed` = 62 % > 30 % → **force
AVOID**. Set `delta = 0.0`, `action = "FLAT"`.

AGOP ranks LONG. LLM intended delta 0.70. Gate forces FLAT. LLM
returns delta 0.0, action FLAT, cites `resource-underwriting`, and
states in the rationale: "SPECULATIVE state; asset_pass adequate but
enterprise_pass weak because dilution_if_financed 62 % on
next milestone cost 150,000,000 against liquid_assets 30,000,000;
milestone-financing gate forces AVOID; resource-underwriting."

## Free data sources

The skill reads the underwriting assessment from
`snapshot.external_data`. The operator's underwriting pipeline
populates it from the following public sources. All are free; the
resource-filing repositories and the ESG standards are open access.

| Source | Supplies | Endpoint | Access |
|---|---|---|---|
| SEDAR+ (Canadian Securities Administrators) | NI 43-101 technical reports, MD&A, financial statements, insider filings | `https://www.sedarplus.ca/` | Free account; full-text search; documents downloadable |
| SEC EDGAR | 10-K, 10-Q, 8-K, SK-1300 technical summary reports, Form 4 insider filings | `https://www.sec.gov/edgar/search/` | Free, no key; bulk downloads available |
| ASX Announcements | JORC 2012 reports, quarterly activities, Appendix 5B | `https://www.asx.com.au/asx/statistics/announcements.do` | Free |
| LSE RNS (Regulatory News Service) | UK-listed resource announcements | `https://www.londonstockexchange.com/news?tab=news-explorer` | Free |
| TMX Money | TSX and TSXV filings | `https://money.tmx.com/` | Free |
| Resource Capital Funds — Phases of Mining | Lifecycle reference for the `lifecycle_stage` field | `https://www.rcf.com/` (publications) | Free |
| SASB Standards | Measurable ESG outcome factors (environmental, social, governance) | `https://sasb.ifrs.org/standards/` | Free to access; the standards themselves are the measured-outcome layer, not the composite ratings |
| GRI Standards | Measurable ESG disclosure factors | `https://www.globalreporting.org/standards/` | Free to access |
| EU CSRD / ESRS | Measurable sustainability reporting factors, including double materiality | `https://www.efrag.org/lab6` | Free to access |
| Hall, Cleveland, and Kaufmann (1986); Hall (2017) | EROI methodology | Book references | Reference only |

The underwriting pipeline uses SEDAR+, SEC EDGAR, ASX, LSE RNS, or
TMX depending on where the enterprise is listed, and reads the
technical reports directly. For ESG, it reads SASB and GRI standards
as the **measured-outcome** layer, and it discards composite ratings
from MSCI, Sustainalytics, and similar agencies because those
agencies mix measured outcomes with qualitative judgements the
actuary cannot audit. The premise holds: the ESG factors that
measure measurable outcomes are useful; the ones that encode
compromises are not.

The `terminal_value` field draws on the same filings (closure plans,
reclamation bonds, environmental assessments) and on independent
sources for the specific repurposing pathway when one is claimed
(pumped-hydro studies, thermal-storage assessments, spectrum
reassignment schedules, patent expiry calendars).

## Do Not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a
  replacement for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it.

- Do not treat PREMIUM as a reason to increase size beyond the
  strategy cap. The strategy cap is the binding constraint. PREMIUM
  means the AGOP-selected action is worth taking at the bound the
  strategy already permits.

- Do not compute NPV, IRR, AISC, or EROI yourself. Those are
  offline computations the underwriting pipeline performs and
  records. You read the qualitative pass states and classify.

- Do not re-classify on the same tick. The underwriting state is a
  deterministic function of the readings. If the first
  classification was SPECULATIVE, it stays SPECULATIVE. Do not push
  it to PASSABLE by preferring one pass over another.

- Do not cite this skill when the cap did not bind. If the intended
  delta was already at or below the cap, this skill did not change
  the decision, and it should not appear in `skills_cited`. Cite the
  skills that actually drove the choice.

- Do not treat a positive `terminal_value` as a reason to upgrade
  the state. The terminal reading can only confirm or degrade. It
  cannot raise.

- Do not use composite ESG ratings (MSCI, Sustainalytics, or
  similar) as inputs to the underwriting. Only the measured-outcome
  factors from SASB, GRI, or ESRS count. A high composite rating is
  not evidence of low operational risk.

- Do not conflate the following pairs, each of which the skill
  treats as distinct:
  - Resource stock versus recoverable reserves.
  - Installed capacity versus utilized capacity.
  - Revenue versus free cash flow.
  - Market capitalisation versus enterprise value.
  - Technical feasibility versus commercial feasibility.
  - A good resource versus a good enterprise.
  - A good enterprise versus a good investment.
  - A low valuation versus undervaluation.
  - A high ESG rating versus low operational risk.
  - A lifecycle stage versus guaranteed appreciation.

- Do not treat the ambiguous fallback as a distinct state. It is
  SPECULATIVE for all downstream purposes, including the
  milestone-financing gate and the cap.

- Do not attempt to fetch SEDAR+, EDGAR, ASX, LSE RNS, TMX, or the
  SASB, GRI, or ESRS standards yourself. You are the LLM; you read
  what is in `snapshot.external_data`. The underwriting pipeline is
  the operator's responsibility.

## Citation Mapping

- **Reading 1 — asset-quality pass**: Don Durrett, *Appendix E:
  Getting an Edge*, which explicitly separates producer, developer,
  and exploration checklists; Don Durrett, *How to Value Mining
  Stocks*, for the detailed valuation methodology. The four
  sub-readings (verification, concentration, accessibility, unit
  economics) correspond to Durrett's producer screen and to the
  feasibility-stage criteria that determine whether a resource is
  economically recoverable.

- **Reading 2 — enterprise-quality pass**: Rick Rule, "How I
  Interview Junior Mining Management", for the management track
  record, ownership alignment, and the interview-based assessment
  of technical and financial competence; Rick Rule, "Pre-Revenue
  Resource Investing Process and Due Diligence", for the
  milestone-based capital allocation and the failure-criteria
  discipline; Rick Rule, Global Resource Investments, for the
  contrarian sector and jurisdiction selection that underpins the
  three sub-readings.

- **Reading 3 — lifecycle position**: Pierre Lassonde, the Lassonde
  Curve / two-stage discovery curve, for the generalized lifecycle
  stages from identification through production to decline; Resource
  Capital Funds, *Phases of Mining*, for the operational
  specification of the stages.

- **Reading 4 — terminal value**: the premise that every resource is
  functionally a mine implies that every resource has a terminal
  state. The examples the premise gives — open-pit mine to pumped
  hydro, patent to public domain, radio frequency to reassignment —
  are the reference cases. The reclamation and closure-cost
  obligations trace to the same technical reports that supply
  Reading 1.

- **Milestone-financing gate**: Rick Rule, "Pre-Revenue Resource
  Investing Process and Due Diligence". The gate encodes the
  pre-revenue discipline: the enterprise must be able to finance
  the next milestone without unacceptable dilution, or the analyst
  must have identified a non-dilutive source.

- **ESG as measurable underwriting**: SASB Standards, GRI Standards,
  EU CSRD / ESRS. The premise that only the factors measuring
  measurable outcomes are useful to the actuary, and the corollary
  that composite ratings mix measured and unmeasured judgements,
  traces to the design of these standards versus the design of the
  rating agencies.

- **EROI**: Charles A. S. Hall, Cutler J. Cleveland, and Robert
  Kaufmann, *Energy and Resource Quality: The Ecology of the
  Economic Process* (1986); Charles A. S. Hall, *Energy Return on
  Investment* (2017). The distinction between financial ROI and
  EROI is the reason the underwriting pipeline computes both.

- **Two-pass independence**: Don Durrett, *Appendix E: Getting an
  Edge*, and Rick Rule, "Pre-Revenue Resource Investing Process and
  Due Diligence". The asset pass establishes what the resource
  might be worth; the enterprise pass establishes whether the
  people, capital structure, and circumstances permit that value
  to be realized. The skill keeps them separately identifiable
  before the synthesis, so that agreement, disagreement, and
  unresolved uncertainty are visible in the rationale.

- **Ambiguous fallback (SPECULATIVE, cap 0.25)**: Durrett (Appendix
  E) and Rule (Pre-Revenue Process). The skill errs toward caution
  because underwriting a broken resource enterprise exceeds the
  cost of declining a working one.

- **Bounded algedonic authority**: Stafford Beer, *Brain of the
  Firm* (1972); Ramadge and Wonham, *Supervisory Control of a Class
  of Discrete-Event Processes* (1987). The skill operates strictly
  as a downward-only algedonic damper within JANUS invariants
  I1–I9. It can flag an underwriting state and cap delta; it cannot
  override the homeostatic risk bound or invent an action outside
  the AGOP ranking.