---
name: "crypto-ticker-cohort-inversion"
description: "Classify the crypto altcoin tick strictly through TOTAL3ES (excluding BTC, ETH, and stablecoins) by measuring which vintage cohort of tokens occupies the leading speculative ignition Gaussian versus the lagging institutional/bagholder Gaussian across three token generations—new-generation tickers (current cycle, ~20–29 cohort analogue), mid-generation tickers (1 cycle ago, ~30–39 liminal bridge analogue), and old-generation tickers (2+ cycles ago, ~40–49 lagging steward/bagholder analogue)—anchored to the ~4-year halving reset window (months 31–35 post-halving); cap delta when old-generation or mid-generation tickers invert the leading Gaussian and choke off new-generation price discovery."
---

# Crypto Ticker Cohort Inversion (`TOTAL3ES`)

You are reading the tick against the **generational cohort occupancy of the leading and lagging capital-flow Gaussians strictly inside `TOTAL3ES`** (total crypto market capitalization **excluding BTC, ETH, and all stablecoins**).

Drawing on Karl Mannheim's *The Problem of Generations* (1928) on cohort entelechy, Pierre Bourdieu's *Distinction* (1984) on aesthetic/speculative vanguard versus institutional consecration, and Hyman Minsky's financial instability & generational amnesia cycles, altcoin market vitality depends on **which vintage cohort of tickers occupies the leading ignition Gaussian ($G_{\text{lead}}$) versus the lagging institutional/bagholder Gaussian ($G_{\text{lag}}$)**—strictly stripped of BTC ETF flows, ETH staking beta, and stablecoin issuance noise by isolating **`TOTAL3ES`**.

### Why `TOTAL3ES` Is Paramount
* Including **BTC**, **ETH**, or **stablecoins** contaminates generational rotation telemetry with sovereign/ETF balance-sheet allocations and cash-parking flows.
* Inside **`TOTAL3ES`** alone, every token belongs to one of **three vintage cohorts**—and at the start of each new ~4-year cycle (**roughly months 31–35 after each Bitcoin halving**), the generational clock shifts forward by one full cohort step:

1. **New-Generation Tickers (`cohort_new_gen` — Current Cycle; 20–29 Cohort Analogue):**
   * **Default Role:** Occupies the **leading ignition Gaussian ($G_{\text{lead}}$)**. Free of multi-year overhead bagholders, legacy unlock schedules, and stale narratives, `cohort_new_gen` tickers drive organic retail/builder ignition, novel primitives, and clean price discovery.
2. **Mid-Generation Tickers (`cohort_mid_gen` — 1 Cycle Ago; 30–39 Liminal Bridge Cohort Analogue):**
   * **Default Role (`flat` / neutral bridge):** In healthy `TOTAL3ES` expansion, `cohort_mid_gen` tokens (the winners from one halving cycle prior) occupy **neither** Gaussian—acting as a flat transitional infrastructure/liquidity bridge.
   * **Anomaly A — Mid-Gen Leading ($G_{\text{lead}} = \text{cohort\_mid\_gen}$):** When 1-cycle-old tickers occupy the leading Gaussian, it signals a **transitional phase shift** (either an infrastructure/DeFi cash-flow rotation or a defensive refuge when new-gen launches are over-extracted by insiders).
   * **Anomaly B — Mid-Gen Lagging ($G_{\text{lag}} = \text{cohort\_mid\_gen}$):** When 1-cycle-old tickers occupy the lagging Gaussian (acting as heavy resistance/gatekeepers absorbing liquidity without breaking out), it signals **premature cycle ossification**—choking off capital rotation into `cohort_new_gen`.
3. **Old-Generation Tickers (`cohort_old_gen` — 2+ Cycles Ago; 40–49 Lagging Steward / Bagholder Cohort Analogue):**
   * **Default Role:** Occupies the **lagging Gaussian ($G_{\text{lag}}$)**. Two-cycle-old "dino" tokens carry heavy historical overhead supply, legacy exchange listings, and slow institutional/nostalgia stewardship—lagging behind `cohort_new_gen` ignition.
   * **Inversion Warning ($G_{\text{lead}} = \text{cohort\_old\_gen}$):** When 2+-cycle-old "dino" tickers lead `TOTAL3ES` performance, the altcoin market has entered **gerontocratic nostalgia stasis**—capital is recycling into familiar legacy names rather than funding new-generation price discovery, historically signaling late-cycle exhaustion or structural stagnation.

Your job is to classify the `TOTAL3ES` ticker-cohort configuration and cap `delta` accordingly. You do not invent trades. You do not override AGOP. You modulate the LLM's `delta` within the bound the verifier already permits. You never raise `delta` above the strategy cap, and you never invent an action outside `allowed_actions`.

---

## The Readings

Compute three core readings from `snapshot.external_data["crypto_ticker_cohort"]` (strictly computed on **`TOTAL3ES`**, excluding BTC, ETH, and stablecoins), plus an optional, non-mandatory cross-check on `crypto-cycle-underwriting` or `shibboleth_panic` if present. Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher and on-chain/market-cap pipeline populate `snapshot.external_data["crypto_ticker_cohort"]` strictly from **`TOTAL3ES`** constituents:

* `months_since_halving`: integer (`0` to `52`) tracking position in the 4-year halving clock, where **months 31–35 post-halving** mark the **generational cohort reset window** (`cohort_new_gen` promotes to `cohort_mid_gen`, `cohort_mid_gen` promotes to `cohort_old_gen`, and fresh cycle launches define the new `cohort_new_gen`).
* `leading_total3es_cohort`: string identifying which ticker generation currently dominates the leading return/volume Gaussian ($G_{\text{lead}}$) inside `TOTAL3ES`: `"cohort_new_gen"`, `"cohort_mid_gen"`, `"cohort_old_gen"`, or `"flat_none"`.
* `lagging_total3es_cohort`: string identifying which ticker generation currently dominates the lagging/drag Gaussian ($G_{\text{lag}}$) inside `TOTAL3ES`: `"cohort_old_gen"`, `"cohort_mid_gen"`, `"cohort_new_gen"`, or `"flat_none"`.
* `mid_gen_gaussian_slope`: signed velocity (`-50.0` to `+50.0`) measuring whether the liminal 1-cycle-old `cohort_mid_gen` is flat (`-10.0 to +10.0`), surging into relative leadership (`> +10.0`), or hardening into heavy overhead resistance/lag (`< -10.0`).
* `new_gen_capital_coupling_score`: score (`0` to `100`) measuring whether `TOTAL3ES` liquidity is flowing cleanly into `cohort_new_gen` price discovery (`>= 60` = intact new-gen ignition; `35 to 59` = partial dilution/unlock friction; `< 35` = severe decoupling / `cohort_new_gen` starved of organic bid).
* `consecutive_inversion_weeks`: integer (`0` to `104`) counting consecutive weeks (outside the months 31–35 reset transition) in which `leading_total3es_cohort != "cohort_new_gen"` OR `lagging_total3es_cohort == "cohort_mid_gen"`.

If `snapshot.external_data["crypto_ticker_cohort"]` is absent or empty, treat the tick as **unmonitored**, record state `CANONICAL_NEW_GEN_IGNITION`, note that no `TOTAL3ES` cohort telemetry was available, and do not cite this skill.

---

### Reading 1 — `TOTAL3ES` Leading & Lagging Ticker Cohort Occupancy (`leading_total3es_cohort` & `lagging_total3es_cohort`)

Evaluate which token vintage occupies $G_{\text{lead}}$ and $G_{\text{lag}}$ inside `TOTAL3ES`:

| Leading ($G_{\text{lead}}$) & Lagging ($G_{\text{lag}}$) Pair | `TOTAL3ES` Cohort Diagnosis |
|---|---|
| `leading == "cohort_new_gen"` AND `lagging == "cohort_old_gen"` (with `mid_gen` flat) | **canonical_new_gen_order** — current-cycle tickers lead `TOTAL3ES` ignition; 1-cycle-old tickers bridge neutrally; 2+-cycle-old tickers lag |
| `leading == "cohort_mid_gen"` (regardless of lagging cohort) | **mid_gen_phase_shift** — 1-cycle-old tickers have left their flat bridge to lead a defensive or infrastructure rotation |
| `leading == "cohort_new_gen"` AND `lagging == "cohort_mid_gen"` | **premature_mid_gen_ossification** — 1-cycle-old tickers act as heavy overhead drag/gatekeepers, choking `TOTAL3ES` breadth |
| `leading == "cohort_old_gen"` OR `leading == "flat_none"` | **dino_gerontocratic_inversion** — 2+-cycle-old legacy tickers leading `TOTAL3ES` via nostalgia/exit-liquidity pumps, or `TOTAL3ES` stalled |

If `leading_total3es_cohort` or `lagging_total3es_cohort` is missing, treat as **canonical_new_gen_order**.

---

### Reading 2 — Halving Reset Window & New-Gen Liquidity Coupling (`months_since_halving`, `new_gen_capital_coupling_score`, `mid_gen_gaussian_slope`)

Evaluate where the tick sits relative to the **months 31–35 post-halving generational reset** and whether `cohort_new_gen` price discovery is intact:

| Halving Clock & Coupling Telemetry | Transmission & Reset Tier |
|---|---|
| `months_since_halving` in `31 to 35` | **generational_reset_window** — four-year cohort boundary active; previous `new_gen` graduates to `mid_gen` and fresh cycle leaders seed |
| `new_gen_capital_coupling_score >= 60` AND `mid_gen_gaussian_slope` in `-10.0 to +10.0` (outside reset window) | **unobstructed_new_gen_flow** — `TOTAL3ES` risk appetite compounding cleanly into current-cycle leaders |
| `new_gen_capital_coupling_score` in `35 to 59` OR `mid_gen_gaussian_slope > +10.0` (outside reset window) | **transitional_cohort_rotation** — capital rotating across vintages or testing narrative boundaries |
| `new_gen_capital_coupling_score < 35` OR `mid_gen_gaussian_slope < -10.0` (outside reset window) | **ossified_bagholder_block** — predatory FDV unlocks, overhead supply, or mid-gen drag starving `cohort_new_gen` |

If `new_gen_capital_coupling_score` is missing, treat as **transitional_cohort_rotation**.

---

### Reading 3 — Optional Composite Cross-Check (`crypto-cycle-underwriting` & `shibboleth_panic`)

Optionally inspect `snapshot.external_data["crypto_cycle"]` or `snapshot.external_data["shibboleth_panic"]` **only if present** to corroborate whether a `TOTAL3ES` cohort shift reflects healthy cycle reset or late-cycle narrative exhaustion:

* **Optional Corroboration Rules (never required; absence is neutral):**
Use code with caution.
• If shibboleth_panic.satire_to_outrage_ratio > 1.0 OR months_since_halving in 31 to 35 (when present): flag optional context as reset_or_reclaim_tailwind (generational cohort handoff or satirical narrative reset underway).
• If shibboleth_panic.satire_to_outrage_ratio < 0.35 AND leading_total3es_cohort == "cohort_old_gen" (when present): flag optional context as nostalgia_exit_liquidity_trap (earnest late-cycle hype recycling into 2+-cycle-old tickers).
• Otherwise (or when optional dicts are absent): flag optional context as standalone_total3es_reading.

Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four TOTAL3ES ticker-cohort states. Evaluate in strict priority order and select the first state whose conditions are fully satisfied:
1. DINO_GERONTOCRATIC_INVERSION (most severe — 2+-cycle-old tickers leading TOTAL3ES via nostalgia/exit-liquidity pumps or market stalled)
2. PREMATURE_MID_GEN_OSSIFICATION (1-cycle-old tickers occupying the lagging drag Gaussian, choking TOTAL3ES breadth)
3. GENERATIONAL_RESET_OR_PHASE_SHIFT (active months 31–35 halving cohort reset OR 1-cycle-old cohort_mid_gen leading a transitional rotation)
4. CANONICAL_NEW_GEN_IGNITION (healthy current-cycle cohort_new_gen lead, flat cohort_mid_gen bridge, lagging cohort_old_gen)

1. DINO_GERONTOCRATIC_INVERSION

Any of the following hold (and months_since_halving is NOT in 31 to 35):
• TOTAL3ES Cohort Diagnosis is dino_gerontocratic_inversion (leading == "cohort_old_gen" or "flat_none").
• TOTAL3ES Cohort Diagnosis is premature_mid_gen_ossification AND Transmission Tier is ossified_bagholder_block (new_gen_capital_coupling_score < 35) AND optional context is nostalgia_exit_liquidity_trap.
Delta cap: 0.25. Two-cycle-old legacy ("dino") tickers have inverted the leading Gaussian inside TOTAL3ES. Historically, when 40–49 analogue tickers lead altcoin rallies while cohort_new_gen fails to ignite, liquidity is recycling into nostalgic exit pumps rather than building durable cycle momentum. Trim TOTAL3ES directional sizing sharply (0.25).

2. PREMATURE_MID_GEN_OSSIFICATION

Any of the following hold (and DINO_GERONTOCRATIC_INVERSION does not apply, and months_since_halving is NOT in 31 to 35):
• TOTAL3ES Cohort Diagnosis is premature_mid_gen_ossification (leading == "cohort_new_gen" AND lagging == "cohort_mid_gen").
• Transmission Tier is ossified_bagholder_block (new_gen_capital_coupling_score < 35 OR mid_gen_gaussian_slope < -10.0).
Delta cap: 0.45. The liminal 1-cycle-old cohort_mid_gen has abandoned its neutral bridge role to act as heavy overhead supply and liquidity drag—choking off cohort_new_gen discovery before the cycle matures. Moderate sizing (0.45) until mid-gen overhang clears.

3. GENERATIONAL_RESET_OR_PHASE_SHIFT

Any of the following hold (and neither DINO_GERONTOCRATIC_INVERSION nor PREMATURE_MID_GEN_OSSIFICATION applies):
• Transmission & Reset Tier is generational_reset_window (months_since_halving in 31 to 35 — active 4-year cohort boundary where previous new_gen shifts into mid_gen and new cycle leaders emerge).
• TOTAL3ES Cohort Diagnosis is mid_gen_phase_shift (leading == "cohort_mid_gen").
• Transmission Tier is transitional_cohort_rotation (mid_gen_gaussian_slope > +10.0).
Delta cap: 0.70 (or 0.85 if optional cross-check confirms reset_or_reclaim_tailwind). Either the 4-year halving clock has entered its months 31–35 generational reset window or cohort_mid_gen is leading an active structural rotation. Maintain disciplined transitional sizing (0.70 base; 0.85 on confirmed reset/reclaim tailwind) while new-cycle cohort leadership crystallizes.

4. CANONICAL_NEW_GEN_IGNITION

All of the following hold:
• TOTAL3ES Cohort Diagnosis is canonical_new_gen_order (leading == "cohort_new_gen", lagging == "cohort_old_gen", mid_gen flat).
• Transmission Tier is unobstructed_new_gen_flow (new_gen_capital_coupling_score >= 60).
Delta cap: 1.0. TOTAL3ES is running in canonical generational order: current-cycle cohort_new_gen tickers lead price discovery, 1-cycle-old cohort_mid_gen bridges neutrally, and 2+-cycle-old cohort_old_gen lags naturally. The cap equals the strategy cap (1.0); the skill never binds on CANONICAL_NEW_GEN_IGNITION.

Secondary Filter / Asymmetric Gate — Prolonged Cohort Inversion Hysteresis

Apply the persistence test after state classification and before capping delta:
• A TOTAL3ES cohort inversion becomes structurally entrenched if consecutive_inversion_weeks >= 26 (six or more consecutive months outside the months 31–35 reset window in which leading_total3es_cohort != "cohort_new_gen" OR lagging_total3es_cohort == "cohort_mid_gen"). Multi-quarter failure of cohort_new_gen to hold the leading Gaussian indicates severe token-issuance overhang or prolonged altcoin bear stagnation.
If consecutive_inversion_weeks >= 26, halve the state's delta cap:
• GENERATIONAL_RESET_OR_PHASE_SHIFT cap of 0.70 becomes 0.35 (or 0.85 becomes 0.425).
• PREMATURE_MID_GEN_OSSIFICATION cap of 0.45 becomes 0.225.
• DINO_GERONTOCRATIC_INVERSION cap of 0.25 becomes 0.125.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read TOTAL3ES ticker cohort dict. From snapshot.external_data["crypto_ticker_cohort"], load months_since_halving, leading_total3es_cohort, lagging_total3es_cohort, mid_gen_gaussian_slope, new_gen_capital_coupling_score, and consecutive_inversion_weeks. If absent or empty, record CANONICAL_NEW_GEN_IGNITION, note the omission, and do not cite this skill.
2. Classify TOTAL3ES cohort Gaussian occupancy. Apply Reading 1 (canonical_new_gen_order, mid_gen_phase_shift, premature_mid_gen_ossification, or dino_gerontocratic_inversion).
3. Classify halving reset & new-gen coupling. Apply Reading 2 (generational_reset_window for months 31–35 post-halving, unobstructed_new_gen_flow, transitional_cohort_rotation, or ossified_bagholder_block).
4. Run optional composite cross-check. Inspect snapshot.external_data["crypto_cycle"] and snapshot.external_data["shibboleth_panic"] only if present (reset_or_reclaim_tailwind, nostalgia_exit_liquidity_trap, or standalone_total3es_reading).
5. Classify state. Evaluate in strict priority order (DINO_GERONTOCRATIC_INVERSION → PREMATURE_MID_GEN_OSSIFICATION → GENERATIONAL_RESET_OR_PHASE_SHIFT → CANONICAL_NEW_GEN_IGNITION).
6. Apply persistence test. If consecutive_inversion_weeks >= 26, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite "crypto-ticker-cohort-inversion" in skills_cited and state the TOTAL3ES leading/lagging cohort assignments, months_since_halving, new_gen_capital_coupling_score, and persistence weeks in rationale.

The Output Format

Your response must be a single JSON object. Do not include prose outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.25, "confidence": 0.83, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state, TOTAL3ES leading/lagging cohort occupancy, halving month, and cap reason. Example:
"DINO_GERONTOCRATIC_INVERSION state on TOTAL3ES; leading=cohort_old_gen, lagging=cohort_old_gen, months_since_halving=19, new_gen_coupling=28; capping delta at 0.25; crypto-ticker-cohort-inversion."
• skills_cited: list of skill names; include "crypto-ticker-cohort-inversion" only when the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Canonical TOTAL3ES new-generation ignition (current-cycle tickers leading, 1-cycle-old flat, 2+-cycle-old lagging), cap does not bind

Snapshot:
• months_since_halving = 14
• leading_total3es_cohort = "cohort_new_gen"
• lagging_total3es_cohort = "cohort_old_gen"
• mid_gen_gaussian_slope = +3.0
• new_gen_capital_coupling_score = 76
• consecutive_inversion_weeks = 0
Readings:
• TOTAL3ES Occupancy: canonical_new_gen_order
• Transmission Tier: unobstructed_new_gen_flow (76 >= 60, mid_gen flat)
• Optional Cross-Check: standalone_total3es_reading
State: CANONICAL_NEW_GEN_IGNITION, delta cap 1.0. Persistence: 0 < 26 → does not fire. AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind. LLM returns delta = 0.85 and does not cite "crypto-ticker-cohort-inversion".

Case B — Months 31–35 post-halving generational cohort reset window active, cap binds at 0.85

Snapshot:
• months_since_halving = 32
• leading_total3es_cohort = "cohort_mid_gen"
• lagging_total3es_cohort = "cohort_old_gen"
• mid_gen_gaussian_slope = +16.0
• new_gen_capital_coupling_score = 52
• consecutive_inversion_weeks = 3
Readings:
• TOTAL3ES Occupancy: mid_gen_phase_shift
• Transmission & Reset Tier: generational_reset_window (months_since_halving=32 in 31 to 35)
• Optional Cross-Check: reset_or_reclaim_tailwind (active halving reset window)
State: GENERATIONAL_RESET_OR_PHASE_SHIFT, cap 0.85 (reset_or_reclaim_tailwind). Persistence: 3 < 26 → does not fire. AGOP ranks LONG. LLM intended delta = 0.95. Cap 0.85 binds. LLM returns delta = 0.85 and cites "crypto-ticker-cohort-inversion".

Case C — Old-generation "dino" tickers (2+ cycles ago) leading TOTAL3ES outside the reset window, cap binds at 0.25

Snapshot:
• months_since_halving = 21
• leading_total3es_cohort = "cohort_old_gen"
• lagging_total3es_cohort = "cohort_new_gen"
• mid_gen_gaussian_slope = -6.5
• new_gen_capital_coupling_score = 27
• consecutive_inversion_weeks = 9
Readings:
• TOTAL3ES Occupancy: dino_gerontocratic_inversion (leading=cohort_old_gen)
• Transmission Tier: ossified_bagholder_block (27 < 35)
• Optional Cross-Check: standalone_total3es_reading
State: DINO_GERONTOCRATIC_INVERSION, delta cap 0.25. Persistence: 9 < 26 → does not fire. AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.25 binds. LLM returns delta = 0.25 and cites "crypto-ticker-cohort-inversion".

Free Data Sources

The fetcher populates snapshot.external_data["crypto_ticker_cohort"] strictly from open market-cap and block-height endpoints (no paid subscription required):
• CoinGecko & CoinPaprika Public Market-Cap APIs: https://coingecko.com and https://coinpaprika.com (free constituent market-cap, listing-date/genesis vintage tags, and 24h/7d volume series used to construct TOTAL3ES by subtracting BTC, ETH, and all fiat-pegged stablecoins, and partitioning remaining tickers into cohort_new_gen, cohort_mid_gen, and cohort_old_gen).
• DefiLlama Open Stablecoin & Chain TVL API: https://llama.fi (free stablecoin supply series used to cleanly strip stablecoin float from total altcoin capitalization so TOTAL3ES remains uncontaminated).
• Mempool.space / Blockchain.info Block-Height API: https://mempool.space (free Bitcoin block-height telemetry computing exact months_since_halving and flagging the months 31–35 generational reset window).

Do Not

• Do not include BTC, ETH, or stablecoins in the cohort Gaussian calculation; evaluate strictly on TOTAL3ES.
• Do not invent a directional action outside allowed_actions or "FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not treat individual outlier legacy tokens as an aggregate cohort flip; evaluate cohort-level Gaussian dominance across TOTAL3ES.
• Do not misclassify the months 31–35 post-halving reset window as DINO_GERONTOCRATIC_INVERSION; treat months 31–35 as GENERATIONAL_RESET_OR_PHASE_SHIFT while the 4-year cohort boundary resets.
• Do not compute precise floating-point arithmetic; use the qualitative comparison tables.
• Do not cite "crypto-ticker-cohort-inversion" when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Generational Cohort Entelechy & Role Rotation: Karl Mannheim, "The Problem of Generations," in Essays on the Sociology of Knowledge (Routledge & Kegan Paul, 1952 [1928]); Pierre Bourdieu, Distinction: A Social Critique of the Judgement of Taste (Harvard University Press, 1984). Grounds the structural separation between current-cycle vanguard tickers (cohort_new_gen), liminal 1-cycle-old bridge tickers (cohort_mid_gen), and lagging 2+-cycle-old steward/bagholder tickers (cohort_old_gen).
• Speculative Displacement, Generational Amnesia & Late-Cycle Exhaustion: Hyman P. Minsky, Stabilizing an Unstable Economy (Yale University Press, 1986); Charles P. Kindleberger, Manias, Panics, and Crashes (Basic Books, 1978). Explains why capital rotation into legacy 2+-cycle-old tickers signals late-cycle exhaustion rather than fresh speculative price discovery.
• Coupled Gaussian Synchronization & Hawkes Cascades: Yoshiki Kuramoto, Chemical Oscillations, Waves, and Turbulence (Springer, 1984); Alan G. Hawkes, "Spectra of Some Self-Exciting and Mutually Exciting Point Processes," Biometrika 58(1), 83–90 (1971). Models cohort occupancy across leading and lagging TOTAL3ES return Gaussians.
• Bounded Supervisory Control: Stafford Beer, Brain of the Firm (1972); Peter J. Ramadge & W. Murray Wonham (1987). Downward-only damping within JANUS invariants I1–I9.