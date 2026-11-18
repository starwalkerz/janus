---
name: "skilled-immigration-bottleneck"
description: "Classify the current tick by administrative permitting bottlenecks throttling qualified vocational, bachelor, specialist-qualification, master's, and lower-to-middle managerial professionals—including next-of-kin reunification and spousal work permits for citizens/residents married to foreign professionals—using free OECD, Eurostat, Fragomen/MPI, and national immigration agency telemetry, and cap delta accordingly."
---

# Skilled Immigration Bottleneck

You are reading the tick against the **human-capital permeability and
family-reunification friction** of the target economy. Aging, low-fertility
polities cannot sustain industrial, clinical, or engineering throughput
without importing qualified working-age staff across the core productive
band: **post-secondary vocational specialists, bachelor's and master's
degree holders, technical professionals, and lower-to-middle managers**.

Crucially, skilled human capital does not move as isolated atomized
units. A regime that throttles **next-of-kin reunification**—or
subjects a **citizen or legal resident who has married a foreign
professional** to multi-month income-threshold traps, permit queues, and
spousal work bans when returning home to work—commits acute self-sabotage.
It blocks dual-income skilled households at the border, drives domestic
talent abroad to join their spouses, and compounds demographic shrinkage.

In Albert O. Hirschman's *Exit, Voice, and Loyalty* (1970) and Mancur
Olson's *The Rise and Decline of Nations* (1982), credentialed guild
protectionism and bureaucratic permit queues force productive couples
and mid-tier professionals to choose **Exit** over **Loyalty**, leaving
domestic employers starved of operational talent.

Your job is to classify the tick into one of four human-capital
permeability states and cap your `delta` accordingly. You do not invent
trades. You do not override AGOP. You modulate the LLM's delta within
the bound the verifier already permits. You never raise `delta` above
the strategy cap, and you never invent an action outside `allowed_actions`.

## The Readings

Compute three readings from `snapshot.external_data["skilled_immigration"]`.
Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher normalizes national residence-permit processing times,
salary/credential threshold ratios, and family-reunification rules into
`snapshot.external_data["skilled_immigration"]`. Each country or bloc
entry (keyed by ISO-2 code such as `fi`, `eu`, `de`, `se`, `uk`, `us`,
`ca`, `sg`, `ae`, `rw`, `ke`, or `global_baseline`) supplies:

- `permit_processing_weeks`: median end-to-end processing time in weeks
  for qualified work and family-reunification residence permits (vocational
  specialists, bachelor/master's holders, and lower-to-middle managers).
- `salary_threshold_to_median_wage`: minimum statutory salary required for
  skilled/specialist work or spousal reunification permits divided by the
  national median full-time wage (`1.0` = equal to median wage; `> 1.3`
  excludes lower-to-middle managers, vocational specialists, and early-career
  bachelor/master's staff).
- `next_of_kin_friction`: qualitative administrative barrier level for
  spouses and dependent next of kin—specifically covering both dependents
  of incoming skilled staff AND foreign spouses of returning citizens or
  residents (`"seamless"`, `"delayed"`, `"income_gated"`, or `"obstructive"`).
- `quarters_permit_backlog`: consecutive calendar quarters in which
  `permit_processing_weeks > 12` OR `next_of_kin_friction` is
  `"income_gated"` or `"obstructive"`.

If `snapshot.external_data["skilled_immigration"]` is absent or empty,
treat the region as **unmonitored**, record state **MODERATE_FRICTION**,
note that no immigration permitting data was available, and do not cite
this skill.

### Reading 1 — Mid-tier & specialist permitting gate (`permit_processing_weeks` & `salary_threshold_to_median_wage`)

Evaluate whether qualified vocational, bachelor/master's, and
lower-to-middle managerial staff can actually enter and start work
within commercial hiring timelines:

| `permit_processing_weeks` | `salary_threshold_to_median_wage` | Permitting Gate |
|---|---|---|
| ≤ 4 weeks | ≤ 0.90× | **fluid** — fast-track entry across vocational, bachelor/master's & mid-management |
| 4 to 10 weeks | 0.90× to 1.15× | **workable** — standard administrative queue; mid-tier roles accessible |
| 10 to 20 weeks | 1.15× to 1.40× | **throttled** — slow queues & inflated pay floors block mid-tier/vocational staff |
| > 20 weeks | > 1.40× | **gridlocked** — de facto exclusion of vocational, bachelor/master's & mid-managers |

If the two metrics fall in different rows, take the **worse** (more
restrictive) classification.

### Reading 2 — Next-of-kin & citizen/resident spousal reunification (`next_of_kin_friction`)

Evaluate administrative treatment of **next of kin**—including both
family members accompanying qualified workers AND foreign spouses of
citizens or residents relocating to work in the destination country:

| `next_of_kin_friction` | Family & Spousal Permeability |
|---|---|
| `"seamless"` | **open_family** — immediate concurrent spousal work rights; no punitive income trap |
| `"delayed"` | **queued_family** — spousal work rights granted, but sequential 2–4 month lag |
| `"income_gated"` | **income_trapped** — punitive income thresholds or language/residency rules block citizen/resident spousal return |
| `"obstructive"` | **severed_family** — multi-month separation, spousal work bans, or arbitrary rejections |

If `next_of_kin_friction` is missing, treat as **queued_family**.

### Reading 3 — Domestic demographic labor need (`elderly_dependency_ratio_pct`)

Cross-check `elderly_dependency_ratio_pct` (from `specialist_density` or
`skilled_immigration` context) to measure how severely permitting
bottlenecks starve domestic operations:

| `elderly_dependency_ratio_pct` | Domestic Labor Hunger |
|---|---|
| < 18% | **self_buffered** — abundant domestic youth cohort |
| 18% to 28% | **tightening** — growing replacement need for skilled staff |
| > 28% | **acute_shortage** — shrinking workforce; permit friction directly caps GDP |

If `elderly_dependency_ratio_pct` is missing, treat as **tightening**.

## Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four states.
Evaluate in strict priority order and select the first state whose
conditions are fully satisfied:

1. **TALENT_EXCLUSION** (most severe)
2. **PERMIT_CHOKE**
3. **MODERATE_FRICTION**
4. **PERMEABLE** (strictest adaptive fit)

### TALENT_EXCLUSION

Any of the following hold:

- Permitting Gate is **gridlocked** (`> 20 weeks` or `> 1.40×` median wage)
  AND Family & Spousal Permeability is **income_trapped** or
  **severed_family**.
- Permitting Gate is **throttled** or **gridlocked** AND Family &
  Spousal Permeability is **severed_family** (`"obstructive"`).
- Permitting Gate is **throttled** (`10–20 weeks` or `1.15–1.40×`) AND
  Family & Spousal Permeability is **income_trapped** AND Domestic Labor
  Hunger is **acute_shortage** (`> 28%`).

**Delta cap: 0.10.** Bureaucratic permitting and next-of-kin hostility
actively block qualified vocational, bachelor/master's, and
lower-to-middle managerial staff while driving bi-national citizen/resident
couples to exit the country. Domestic employers face chronic skill
shortages, project delays, and rising wage-to-output drag. Trade only
if the AGOP ranking targets remote/offshore SEZ execution corridors or
fully automated IP. In most cases, return FLAT.

### PERMIT_CHOKE

Any of the following hold (and `TALENT_EXCLUSION` does not apply):

- Permitting Gate is **gridlocked** (`> 20 weeks` or `> 1.40×`).
- Permitting Gate is **throttled** (`10–20 weeks` or `1.15–1.40×`).
- Family & Spousal Permeability is **income_trapped** or
  **severed_family** (even if individual work permits appear fast,
  blocking spouses/next of kin repels settled professionals and
  returning citizens).

**Delta cap: 0.25.** Mid-tier professional permitting or next-of-kin
reunification rules create severe hiring friction and talent attrition.
Reduce position size substantially on labor- and management-dependent
domestic sectors.

### MODERATE_FRICTION

Any of the following hold (and neither `TALENT_EXCLUSION` nor
`PERMIT_CHOKE` applies):

- Permitting Gate is **workable** (`4 to 10 weeks` and `0.90× to 1.15×`).
- Permitting Gate is **fluid** AND Family & Spousal Permeability is
  **queued_family** (`"delayed"`).

**Delta cap: 0.75.** Qualified professionals and their families can
enter and work, though administrative processing lags slow rapid
team scaling. Reduce size relative to PERMEABLE.

### PERMEABLE

All of the following hold:

- Permitting Gate is **fluid** (`≤ 4 weeks` and `≤ 0.90×` median wage).
- Family & Spousal Permeability is **open_family** (`"seamless"`
  concurrent spousal work rights for incoming staff and returning
  citizens/residents).

**Delta cap: 1.0.** Fast, transparent permitting for vocational,
bachelor/master's, and mid-managerial staff plus immediate next-of-kin
work rights. The cap equals the strategy cap; the skill never binds on
PERMEABLE.

### Ambiguous fallback

Any combination not covered above is classified **PERMIT_CHOKE** with
delta cap `0.25`.

## Secondary Filter / Asymmetric Gate — Bureaucratic Backlog Hysteresis

Apply the persistence test after state classification and before the
cap.

A country's immigration bottleneck is **structurally entrenched** if
`quarters_permit_backlog >= 4` (four or more consecutive quarters with
`permit_processing_weeks > 12` or `next_of_kin_friction` in
`{"income_gated", "obstructive"}`). Four consecutive quarters of
permitting backlog or spousal income-gating proves the friction is
embedded in statutory rules and institutional culture rather than
seasonal summer visa volume.

If the bottleneck is structurally entrenched, halve the state's
delta cap:
• MODERATE_FRICTION cap of 0.75 becomes 0.375.
• PERMIT_CHOKE cap of 0.25 becomes 0.125.
• TALENT_EXCLUSION cap of 0.10 becomes 0.05.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read skilled immigration dict. From
snapshot.external_data["skilled_immigration"], load the target
country's permit_processing_weeks, salary_threshold_to_median_wage,
next_of_kin_friction, and quarters_permit_backlog (plus
elderly_dependency_ratio_pct if available). If absent or empty,
record MODERATE_FRICTION, note the omission, and do not cite this
skill.
2. Classify permitting gate. Apply Reading 1 (fluid, workable,
throttled, or gridlocked).
3. Classify family & spousal permeability. Apply Reading 2
(open_family, queued_family, income_trapped, or
severed_family).
4. Classify domestic labor hunger. Apply Reading 3 (self_buffered,
tightening, or acute_shortage).
5. Classify state. Evaluate in strict priority order
(TALENT_EXCLUSION → PERMIT_CHOKE → MODERATE_FRICTION →
PERMEABLE) and select the first matching state (fallback:
PERMIT_CHOKE).
6. Apply persistence test. If quarters_permit_backlog >= 4,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta exceeded delta_cap),
cite "skilled-immigration-bottleneck" in skills_cited and state
the classification in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and cap reason.
Example: "TALENT_EXCLUSION state; 18-week permit queue, 1.25x median wage threshold, and income-trapped next-of-kin/spousal reunification for 5 quarters amid 37% elderly dependency; delta capped at 0.05; skilled-immigration-bottleneck."
• skills_cited: list of skill names; include
"skilled-immigration-bottleneck" only when the cap bound.

Worked Examples


Case A — Fast-track skilled permitting with immediate spousal work rights, cap does not bind

Snapshot (e.g., open SEZ / talent-hub regime):
• permit_processing_weeks = 3.0
• salary_threshold_to_median_wage = 0.75
• next_of_kin_friction = "seamless"
• quarters_permit_backlog = 0
• elderly_dependency_ratio_pct = 14.0
Readings:
• Permitting Gate: ≤ 4 weeks and ≤ 0.90× → fluid
• Family & Spousal Permeability: "seamless" → open_family
• Domestic Labor Hunger: < 18% → self_buffered
State: PERMEABLE, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "skilled-immigration-bottleneck".

Case B — Throttled mid-tier permitting & income-trapped spousal reunification in aging economy, cap binds

Snapshot (e.g., aging European economy with strict income/permit rules):
• permit_processing_weeks = 16.0
• salary_threshold_to_median_wage = 1.25
• next_of_kin_friction = "income_gated"
• quarters_permit_backlog = 5
• elderly_dependency_ratio_pct = 37.5
Readings:
• Permitting Gate: 10 to 20 weeks and 1.15× to 1.40× → throttled
• Family & Spousal Permeability: "income_gated" → income_trapped
• Domestic Labor Hunger: > 28% → acute_shortage
State: TALENT_EXCLUSION, delta cap 0.10.
Persistence: quarters_permit_backlog = 5 >= 4 → halve to 0.05.
AGOP ranks LONG on a domestic labor- or management-dependent stock.
LLM intended delta = 0.75. Cap 0.05 binds. LLM returns delta = 0.05
and cites "skilled-immigration-bottleneck".

Free & Open Data Sources

The fetcher populates snapshot.external_data["skilled_immigration"]
from the following free, public endpoints (no paid subscription
required):
• OECD Indicators of Talent Attractiveness & International Migration Database:
https://oecd.org (free SDMX API covering skilled
worker visa conditions, family-reunification scores, spousal work
rights, and bilateral migration flows).
• Eurostat First Residence Permits by Reason & Duration (migr_resfirst / migr_resfam / migr_resocc):
https://europa.eu (free JSON/TSV API
tracking employment and family-reunification residence permit volumes
and processing backlogs across EU/EEA states).
• MIPEX (Migrant Integration Policy Index — Labour Market Mobility & Family Reunion):
https://mipex.eu (free public country-by-country
policy scores on family reunification income thresholds, waiting
periods, and spousal labor-market access across 56 countries).
• National Immigration Service Open Statistics (Migri Finland / Migrationsverket Sweden / BAMF Germany / RDB Rwanda):
https://migri.fi (free public monthly/quarterly processing
time medians and decision statistics by permit category—work-based,
specialist, and family ties).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not evaluate executive/C-suite visas in isolation; always evaluate
the vocational, bachelor/master's, and lower-to-middle managerial
band AND next-of-kin / citizen-spousal reunification rules.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "skilled-immigration-bottleneck" when the cap did not
bind.

Citation Mapping

• Exit, Voice, and Loyalty (Talent Flight Under Institutional Friction):
Albert O. Hirschman, Exit, Voice, and Loyalty: Responses to Decline
in Firms, Organizations, and States (Harvard University Press, 1970).
When bureaucratic rules block productive households and bi-national
couples from working locally, mobile human capital exits to more
permeable jurisdictions.
• Guild Protectionism & Distributional Coalitions: Mancur Olson,
The Rise and Decline of Nations (Yale University Press, 1982).
Credential and salary-floor gatekeeping protects narrow domestic
incumbents at the expense of aggregate economic dynamism.
• Global Talent & Family-Reunification Policy Benchmarks: OECD,
Indicators of Talent Attractiveness (2023–2025); Migrant Integration
Policy Index (MIPEX), Family Reunion & Labour Market Mobility
Strands.
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.