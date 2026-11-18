---
name: "enterprise-ai-adoption"
description: "Classify the current tick by enterprise AI production adoption using separate yardsticks for open-weights/sovereign AI versus closed-source proprietary API dependency via free Stanford HAI, OECD.AI, Eurostat ICT, and open-model telemetry, and cap delta accordingly."
---

# Enterprise AI Adoption

You are reading the tick against the structural quality and economic
sovereignty of enterprise AI deployment. Headline "AI adoption" surveys
obscure a fundamental bifurcation:

1. **Open-Weights & Sovereign AI Yardstick (`open_ai_pct`):** Enterprises
   running quantized open-weights models (`7B–70B` local/on-prem or
   sovereign cloud) capture permanent marginal-cost compression, data
   privacy, and architectural control.
2. **Closed-Source Proprietary API Yardstick (`closed_api_pct`):**
   Enterprises glued to proprietary third-party APIs suffer Oliver
   Williamson's asset-specificity hold-up: opaque token rent-extraction,
   model deprecation shocks, cross-border data compliance bottlenecks,
   and fragile gross margins when API pricing or rate limits shift.

In Carlota Perez's *Technological Revolutions and Financial Capital*
(2002) and Eric S. Raymond's *The Cathedral and the Bazaar* (1999),
general-purpose technologies only transition from speculative installation
bubbles into real deployment productivity once open, commoditized
standards replace proprietary gatekeepers.

Your job is to classify the tick into one of four enterprise-AI states
and cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise `delta` above the strategy cap,
and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["enterprise_ai"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes enterprise survey, ICT census, and open-weights
deployment telemetry into `snapshot.external_data["enterprise_ai"]`.
Each sector or region entry (keyed by geography/sector such as `us`,
`eu`, `fi`, `in`, `sg`, `ke`, `rw`, `tech`, `listed`, or
`global_baseline`) supplies:

- `open_ai_prod_pct`: percentage of enterprises deploying open-weights
  or self-hosted models in production workflows.
- `closed_api_prod_pct`: percentage of enterprises relying exclusively
  on closed-source proprietary external APIs in production workflows.
- `open_ai_yoy_shift_pct`: trailing 12-month percentage-point change in
  `open_ai_prod_pct` (measuring migration from closed wrappers to
  sovereign open-weights stacks).
- `ai_capex_to_revenue_ratio`: enterprise AI spend / API + compute
  bill relative to realized revenue lift (`< 1.0` = accretive ROI;
  `> 2.0` = unmonetized capex/API burn).
- `quarters_unmonetized_burn`: consecutive quarters where
  `closed_api_prod_pct > 25%` and `ai_capex_to_revenue_ratio > 2.0`.

If `snapshot.external_data["enterprise_ai"]` is absent or empty, treat
the sector/region as **unmonitored**, record state **TRANSITIONAL_AI**,
note that no enterprise AI data was available, and do not cite this
skill.

### Reading 1 — Open-weights & sovereign AI yardstick (`open_ai_prod_pct`)

Evaluate genuine open-weights production deployment (`open_ai_prod_pct`
and `open_ai_yoy_shift_pct`):

| `open_ai_prod_pct` | Open-Weights Maturity |
|---|---|
| > 30% | **sovereign_scale** — broad open-weights production compounding |
| 15% to 30% | **expanding_open** — active open-source deployment & fine-tuning |
| 5% to 15% | **nascent_open** — early pilot stage; open stack still thin |
| < 5% | **open_laggard** — near-zero sovereign/open-weights capability |

### Reading 2 — Closed-source API dependency yardstick (`closed_api_prod_pct`)

Evaluate closed-source proprietary API concentration (`closed_api_prod_pct`)
separately to detect vendor lock-in and margin taxation:

| `closed_api_prod_pct` | Closed-API Dependency |
|---|---|
| < 15% | **unencumbered** — minimal third-party proprietary API rent |
| 15% to 30% | **moderate_wrapper** — bounded external API usage |
| 30% to 50% | **vendor_locked** — heavy margin exposure to proprietary APIs |
| > 50% | **captive_rent** — acute structural dependence on closed gatekeepers |

### Reading 3 — Compute-to-revenue realization (`ai_capex_to_revenue_ratio`)

Compare AI compute/API expenditure against realized commercial output
to separate productive deployment from installation-phase hype:

| `ai_capex_to_revenue_ratio` | Economic Realization |
|---|---|
| < 1.0 | **accretive** — AI deployment generating net positive unit margin |
| 1.0 to 2.0 | **breakeven** — transitional integration & training absorption |
| > 2.0 | **hollow_burn** — heavy API/capex spend without commercial payback |

If `ai_capex_to_revenue_ratio` is missing, treat as **breakeven**.

## Taxonomy / Decision Matrix

Combine Reading 1 (Open Yardstick), Reading 2 (Closed Yardstick), and
Reading 3 (Realization) into one of four states. Evaluate in strict
priority order and select the first state whose conditions are fully
satisfied:

1. **CAPTIVE_BUBBLE** (most severe)
2. **WRAPPER_DRAG**
3. **TRANSITIONAL_AI**
4. **SOVEREIGN_COMPOUNDING** (strictest adaptive fit)

### CAPTIVE_BUBBLE

Any of the following hold:

- Closed-API Dependency is **captive_rent** (`> 50%`) AND Economic
  Realization is **hollow_burn** (`> 2.0`).
- Closed-API Dependency is **vendor_locked** or **captive_rent** (`≥ 30%`)
  AND Open-Weights Maturity is **open_laggard** (`< 5%`) AND Economic
  Realization is **hollow_burn**.
- Open-Weights Maturity is **open_laggard** (`< 5%`) AND Closed-API
  Dependency is **unencumbered** (`< 15%`) AND Economic Realization is
  **hollow_burn** (stagnant bureaucracy buying hardware without workflow
  deployment).

**Delta cap: 0.10.** Enterprises are paying heavy proprietary API tolls
or capex burn without sovereign open-weights resilience or net margin
payback. Gross margins are exposed to vendor price hikes, regulatory
blocks, and post-hype capex write-downs. Trade only if the AGOP ranking
targets open-weights infrastructure/edge-inference enablers or
non-AI physical scarcity hedges. In most cases, return FLAT.

### WRAPPER_DRAG

Any of the following hold (and `CAPTIVE_BUBBLE` does not apply):

- Closed-API Dependency is **vendor_locked** or **captive_rent** (`≥ 30%`)
  AND Open-Weights Maturity is **nascent_open** or **open_laggard**
  (`< 15%`).
- Open-Weights Maturity is **open_laggard** (`< 5%`) across an
  information-intensive sector.
- Economic Realization is **hollow_burn** (`> 2.0`) while Open-Weights
  Maturity is **nascent_open** (`5% to 15%`).

**Delta cap: 0.25.** Proprietary API lock-in or slow open-weights
adoption is compressing unit economics and creating single-vendor
fragility. Reduce position size substantially.

### TRANSITIONAL_AI

Any of the following hold (and neither `CAPTIVE_BUBBLE` nor
`WRAPPER_DRAG` applies):

- Open-Weights Maturity is **expanding_open** (`15% to 30%`).
- Open-Weights Maturity is **sovereign_scale** (`> 30%`) AND Closed-API
  Dependency is **vendor_locked** or **captive_rent** (`≥ 30%`).
- Open-Weights Maturity is **nascent_open** (`5% to 15%`) AND
  Closed-API Dependency is **unencumbered** or **moderate_wrapper**
  (`< 30%`) with **accretive** or **breakeven** realization.

**Delta cap: 0.75.** Enterprises are actively migrating toward open
weights and generating real workflow ROI, though legacy proprietary
dependencies or scaling bottlenecks remain. Reduce size relative to
SOVEREIGN_COMPOUNDING.

### SOVEREIGN_COMPOUNDING

All of the following hold:

- Open-Weights Maturity is **sovereign_scale** (`> 30%`).
- Closed-API Dependency is **unencumbered** or **moderate_wrapper**
  (`< 30%`).
- Economic Realization is **accretive** (`< 1.0`).

**Delta cap: 1.0.** Broad production deployment of self-hosted /
open-weights models with accretive unit economics and zero proprietary
API hold-up. The cap equals the strategy cap; the skill never binds on
SOVEREIGN_COMPOUNDING.

### Ambiguous fallback

Any combination not covered above is classified **WRAPPER_DRAG** with
delta cap `0.25`.

## Secondary Filter / Asymmetric Gate — Unmonetized API Burn Hysteresis

Apply the persistence test after state classification and before the
cap.

An enterprise AI regime is **structurally trapped** if
`quarters_unmonetized_burn >= 4` (four or more consecutive quarters
where `closed_api_prod_pct > 25%` and `ai_capex_to_revenue_ratio > 2.0`).
Four quarters of unmonetized proprietary API spend without open-weights
migration proves the organization is subsidizing external model vendors
rather than compounding internal capability.

If the regime is **structurally trapped**, halve the state's delta cap:

- `TRANSITIONAL_AI` cap of `0.75` becomes **`0.375`**.
- `WRAPPER_DRAG` cap of `0.25` becomes **`0.125`**.
- `CAPTIVE_BUBBLE` cap of `0.10` becomes **`0.05`**.

The gate is one-way. It cannot raise the cap; it can only lower it.

## The Procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read enterprise AI dict.** From
   `snapshot.external_data["enterprise_ai"]`, load the target region or
   sector's `open_ai_prod_pct`, `closed_api_prod_pct`,
   `open_ai_yoy_shift_pct`, `ai_capex_to_revenue_ratio`, and
   `quarters_unmonetized_burn`. If absent or empty, record
   **TRANSITIONAL_AI**, note the omission, and do not cite this skill.
2. **Classify open-weights yardstick.** Apply Reading 1
   (`sovereign_scale`, `expanding_open`, `nascent_open`, or
   `open_laggard`).
3. **Classify closed-API yardstick.** Apply Reading 2 (`unencumbered`,
   `moderate_wrapper`, `vendor_locked`, or `captive_rent`).
4. **Classify economic realization.** Apply Reading 3 (`accretive`,
   `breakeven`, or `hollow_burn`).
5. **Classify state.** Evaluate in strict priority order
(CAPTIVE_BUBBLE → WRAPPER_DRAG → TRANSITIONAL_AI →
SOVEREIGN_COMPOUNDING) and select the first matching state
(fallback: WRAPPER_DRAG).
6. Apply persistence test. If quarters_unmonetized_burn >= 4,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta exceeded delta_cap),
cite "enterprise-ai-adoption" in skills_cited and state the
classification in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and cap reason.
Example: "CAPTIVE_BUBBLE state; closed_api_prod_pct 58% with hollow_burn (2.6x) and open_ai_prod_pct 4% for 5 quarters; delta capped at 0.05; enterprise-ai-adoption."
• skills_cited: list of skill names; include
"enterprise-ai-adoption" only when the cap bound.

Worked Examples


Case A — Sovereign open-weights compounding with accretive ROI, cap does not bind

Snapshot:
• open_ai_prod_pct = 36.0
• closed_api_prod_pct = 18.0
• open_ai_yoy_shift_pct = +14.0
• ai_capex_to_revenue_ratio = 0.75
• quarters_unmonetized_burn = 0
Readings:
• Open-Weights Yardstick: > 30% → sovereign_scale
• Closed-API Yardstick: 15% to 30% → moderate_wrapper
• Economic Realization: < 1.0 → accretive
State: SOVEREIGN_COMPOUNDING, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "enterprise-ai-adoption".

Case B — Closed-API captive wrapper burn without open-weights capability, cap binds

Snapshot:
• open_ai_prod_pct = 3.5
• closed_api_prod_pct = 56.0
• open_ai_yoy_shift_pct = +0.5
• ai_capex_to_revenue_ratio = 2.65
• quarters_unmonetized_burn = 5
Readings:
• Open-Weights Yardstick: < 5% → open_laggard
• Closed-API Yardstick: > 50% → captive_rent
• Economic Realization: > 2.0 → hollow_burn
State: CAPTIVE_BUBBLE, delta cap 0.10.
Persistence: quarters_unmonetized_burn = 5 >= 4 → halve to 0.05.
AGOP ranks LONG on an enterprise SaaS wrapper ticker. LLM intended
delta = 0.80. Cap 0.05 binds. LLM returns delta = 0.05 and cites
"enterprise-ai-adoption".

Free Data Sources

The fetcher populates snapshot.external_data["enterprise_ai"] from
the following free, public endpoints (no paid subscription required):
• Eurostat ICT Usage in Enterprises (isoc_eb_ai):
https://europa.eu (free
JSON/TSV API measuring enterprise AI adoption by technology type,
in-house vs. externally purchased software, and firm size across
all EU/EEA countries).
• Stanford HAI AI Index — Open vs. Closed Foundation Model & Enterprise Reports:
https://stanford.edu (free public datasets on
open-weights model share, inference cost deflation, and enterprise
ROI realization).
• OECD.AI Policy Observatory & Business ICT Diffusion:
https://oecd.ai (free cross-country enterprise AI diffusion and
compute indicators).
• U.S. Census Bureau Business Trends and Outlook Survey (BTOS):
https://census.gov (free biweekly AI production usage
series across US sectors).
• Hugging Face Open-Weights Enterprise & Download Telemetry:
https://huggingface.co (free public API tracking open-weights
enterprise model adoption velocity).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not conflate closed-source API wrappers with open-weights
sovereign deployment; evaluate both yardsticks independently.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "enterprise-ai-adoption" when the cap did not bind.

Citation Mapping

• The Cathedral and the Bazaar (Open vs. Closed Software Economics):
Eric S. Raymond, The Cathedral and the Bazaar (O'Reilly, 1999).
Open, inspectable software architectures out-iterate closed
gatekeeper models and eliminate single-vendor rent extraction.
• Asset Specificity & Vendor Hold-Up: Oliver E. Williamson, The
Economic Institutions of Capitalism (Free Press, 1985). Building
core workflows atop proprietary closed interfaces creates bilateral
dependency and margin expropriation risk.
• Installation Bubble vs. Deployment Synergy: Carlota Perez,
Technological Revolutions and Financial Capital (Edward Elgar, 2002).
General-purpose technologies only yield broad productivity once
installation-phase capital burn transitions to standardized, low-cost
deployment.
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.