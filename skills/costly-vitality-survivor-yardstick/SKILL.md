---
name: "costly-vitality-survivor-yardstick"
description: "Classify whether a multi-cycle legacy asset, brand, or ticker across any valuation tranche has crossed from transient novelty into a durable multi-cycle survivor by measuring costly-to-fake original attributes (Zahavi handicap principle, Lindy survival persistence, trough organic retention, and structural liquidity/brand moat) independent of current market valuation or institutional status; cap delta on hollow/unverified nostalgia traps while preserving sizing on genuine multi-cycle costly-signal survivors."
---

# Costly Vitality & Multi-Cycle Survivor Yardstick

You are reading the tick against the **novelty-to-legacy survival filter**—identifying whether an asset, consumer brand, equity ticker, or crypto protocol has transitioned from ephemeral cycle novelty into a **durable multi-cycle survivor** across any valuation tranche.

Drawing on Amotz Zahavi's *Handicap Principle* (1975) on costly, unfalsifiable signals of underlying vitality, Nassim Nicholas Taleb's *Lindy Effect* (2012) on non-perishable survival across multiple stress cycles, Thorstein Veblen's *Theory of the Leisure Class* (1899) on status signals versus functional durability, and Thorndike/Greenblatt capital-resilience frameworks, assets that survive multiple full boom-bust cycles without vanishing share a single invariant:

**They possess original, costly-to-fake attributes that continue generating organic user/consumer vitality right through the cycle trough—strictly independent of their current market capitalization, valuation multiple, or prevailing institutional status.**

Whether observed in:
* **Multi-cycle equities & consumer staples** across large-cap and beaten-down valuation tranches (e.g., Coca-Cola, McDonald's, Levi's, Intel, AMD, Nokia),
* **Multi-cycle crypto protocols** that survive 80–95% drawdowns yet retain deep organic settlement or cultural liquidity (e.g., `SOL` as high-throughput infrastructure liquidity, `DOGE` as unforgeable multi-cycle cultural/meme liquidity), or
* **Consumer brands & cultural staples** that outlast transient trends by delivering unmistakable functional or aesthetic utility,

every multi-cycle asset falls into one of **four survival states**:

1. **COSTLY_VITALITY_STAPLE (`COSTLY_VITALITY_STAPLE`):** The asset has survived 2+ full cycles with high costly-to-fake original attributes (deep physical distribution, patent/fab/network infrastructure, unforgeable cultural mindshare, or Lindy brand equity) AND continues displaying strong organic user/consumer retention during market troughs—regardless of whether its current market valuation is high or depressed.
2. **CONTESTED_TURNAROUND_SURVIVOR (`CONTESTED_TURNAROUND_SURVIVOR`):** A multi-cycle survivor possessing genuine legacy infrastructure or brand moat, currently undergoing architectural/strategic reinvention after a severe trough (e.g., legacy semiconductor or telecom turnaround, or post-crash protocol rebuild) where costly attributes remain intact even while consensus status is depressed.
3. **UNPROVEN_NOVELTY_CYCLE (`UNPROVEN_NOVELTY_CYCLE`):** A single-cycle or newly launched asset (`< 1` full boom-bust trough survived) whose vitality has not yet been stress-tested through a complete winter; still priced on novelty rather than Lindy survival.
4. **HOLLOW_NOSTALGIA_SHELL (`HOLLOW_NOSTALGIA_SHELL`):** A multi-cycle ticker whose costly-to-fake core attributes have eroded (zero organic trough activity, decaying developer/customer base, purely financialized or zombie shell) and which only spikes on artificial exit-liquidity pumps or stale name recognition.

Your job is to classify the target's costly-vitality survival state and cap `delta` accordingly. You do not invent trades. You do not override AGOP. You modulate the LLM's `delta` within the bound the verifier already permits. You never raise `delta` above the strategy cap, and you never invent an action outside `allowed_actions`.

---

## The Readings

Compute three readings from `snapshot.external_data["costly_vitality"]`. Use the qualitative tables below. Do not compute precise arithmetic.

### Monitored telemetry fields

The fetcher and fundamental/on-chain/attention pipeline populate `snapshot.external_data["costly_vitality"]` for the target ticker or brand (across any valuation tranche):

* `cycles_survived`: integer (`0` to `15+`) counting completed boom-bust market or industry cycles since inception (`0` = current cycle novelty; `1` = survived one full trough; `>= 2` = multi-cycle Lindy cohort).
* `costly_attribute_score`: score (`0` to `100`) measuring unfalsifiable, high-barrier original attributes—physical/fab/network infrastructure, multi-decade brand recall, regulatory/distribution moats, or unforgeable cultural mindshare (`>= 65` = deep costly-to-fake moat; `35 to 64` = moderate/contested moat; `< 35` = easily replicated commodity/shell).
* `trough_organic_vitality_score`: score (`0` to `100`) measuring genuine user, developer, transaction, or consumer demand retention **during price/valuation troughs** (`>= 60` = strong organic floor independent of token/share price; `35 to 59` = partial retention; `< 35` = ghost-town trough / demand vanishes when price falls).
* `valuation_tranche`: string (`"deep_value_distressed"`, `"mid_tranche_recovery"`, `"large_cap_staple"`, or `"parabolic_premium"`) recording current valuation status—used strictly to verify that trough vitality is evaluated **independent of market price**.
* `consecutive_vitality_erosion_quarters`: integer (`0` to `40`) counting consecutive quarters in which `trough_organic_vitality_score < 35` AND `costly_attribute_score < 50`.

If `snapshot.external_data["costly_vitality"]` is absent or empty, treat the target as **unmonitored**, record state `COSTLY_VITALITY_STAPLE`, note that no costly-vitality telemetry was available, and do not cite this skill.

---

### Reading 1 — Lindy Multi-Cycle Persistence (`cycles_survived`)

Evaluate whether the asset has graduated from single-cycle novelty into multi-cycle endurance:

| `cycles_survived` | Lindy Survival Tier |
|---|---|
| `>= 2` | **multi_cycle_lindy_veteran** — proven survival across two or more complete boom-bust cycles |
| `1` | **single_trough_survivor** — survived one full winter; transitioning from novelty toward legacy |
| `0` | **untested_current_novelty** — zero completed bust cycles; survival under stress unverified |

If `cycles_survived` is missing, treat as **untested_current_novelty**.

---

### Reading 2 — Costly-to-Fake Original Attributes (`costly_attribute_score`)

Evaluate the depth of unforgeable, high-barrier structural or cultural attributes (independent of current share/token price):

| `costly_attribute_score` (0–100) | Zahavi Costly-Signal Tier |
|---|---|
| `>= 65` | **unforgeable_costly_moat** — deep infrastructure, distribution, IP, or multi-decade cultural mindshare impossible to fake quickly |
| `35 to 64` | **contested_legacy_asset** — real historical foundation or brand recognition, but facing architectural or competitive pressure |
| `< 35` | **replicable_or_eroded_shell** — low switching costs, easily cloned narrative, or hollowed-out legacy wrapper |

If `costly_attribute_score` is missing, treat as **contested_legacy_asset**.

---

### Reading 3 — Trough Organic Vitality Independent of Market Status (`trough_organic_vitality_score`)

Evaluate whether real consumers, users, or liquidity persist when market status and valuation are depressed:

| `trough_organic_vitality_score` (0–100) | Trough Retention Tier |
|---|---|
| `>= 60` | **price_independent_vitality** — strong organic usage, consumer pull, or settlement liquidity even in deep valuation troughs |
| `35 to 59` | **moderate_trough_retention** — core base remains active during downturns while peripheral speculators exit |
| `< 35` | **price_dependent_ghost_town** — organic engagement collapses whenever price/hype fades |

If `trough_organic_vitality_score` is missing, treat as **moderate_trough_retention**.

---

## Taxonomy / Decision Matrix

Combine Readings 1–3 into one of four costly-vitality survival states. Evaluate in strict priority order and select the first state whose conditions are fully satisfied:

1. **HOLLOW_NOSTALGIA_SHELL** (most severe — multi-cycle name recognition with eroded costly attributes and dead trough vitality)
2. **UNPROVEN_NOVELTY_CYCLE** (zero completed bust cycles; unverified survival durability)
3. **CONTESTED_TURNAROUND_SURVIVOR** (multi-cycle or single-trough survivor rebuilding with intact costly attributes despite depressed status)
4. **COSTLY_VITALITY_STAPLE** (multi-cycle Lindy survivor with unforgeable costly attributes and price-independent trough vitality)

---

### 1. HOLLOW_NOSTALGIA_SHELL

Any of the following hold:

* Zahavi Costly-Signal Tier is **replicable_or_eroded_shell** (`costly_attribute_score < 35`) AND Trough Retention Tier is **price_dependent_ghost_town** (`trough_organic_vitality_score < 35`).
* Lindy Survival Tier is **multi_cycle_lindy_veteran** (`cycles_survived >= 2`) AND Trough Retention Tier is **price_dependent_ghost_town** (`trough_organic_vitality_score < 35`).

**Delta cap: 0.20.** The asset is a zombie or hollow nostalgia ticker: despite surviving on exchange listings or legacy name recognition, its costly-to-fake attributes have decayed and organic vitality vanishes outside speculative spikes. Cut directional sizing sharply (`0.20`).

---

### 2. UNPROVEN_NOVELTY_CYCLE

Any of the following hold (and `HOLLOW_NOSTALGIA_SHELL` does not apply):

* Lindy Survival Tier is **untested_current_novelty** (`cycles_survived == 0`).
* Trough Retention Tier is **price_dependent_ghost_town** (`trough_organic_vitality_score < 35`) on a `single_trough_survivor` (`cycles_survived == 1`).

Use code with caution.
Delta cap: 0.55. The ticker has not yet proven costly-signal survival across a full boom-bust trough. Cap sizing (0.55) to prevent over-allocating to untested cycle novelty before its organic trough floor is verified.

3. CONTESTED_TURNAROUND_SURVIVOR

Any of the following hold (and neither HOLLOW_NOSTALGIA_SHELL nor UNPROVEN_NOVELTY_CYCLE applies):
• Lindy Survival Tier is multi_cycle_lindy_veteran or single_trough_survivor (cycles_survived >= 1) paired with contested_legacy_asset (costly_attribute_score in 35 to 64) or moderate_trough_retention (trough_organic_vitality_score in 35 to 59).
• Lindy Survival Tier is single_trough_survivor (cycles_survived == 1) with unforgeable_costly_moat (>= 65) and price_independent_vitality (>= 60).
Delta cap: 0.85. The asset has survived at least one full trough and retains genuine costly-to-fake infrastructure, brand moat, or organic user retention across its valuation tranche (including deep-value turnaround candidates), while still proving multi-cycle compounding. Permit strong staged sizing (0.85 cap).

4. COSTLY_VITALITY_STAPLE

All of the following hold:
• Lindy Survival Tier is multi_cycle_lindy_veteran (cycles_survived >= 2).
• Zahavi Costly-Signal Tier is unforgeable_costly_moat (costly_attribute_score >= 65).
• Trough Retention Tier is price_independent_vitality (trough_organic_vitality_score >= 60).
Delta cap: 1.0. The asset has completed the transition from transient novelty to an enduring multi-cycle staple—retaining high costly-to-fake attributes and strong organic consumer/user vitality right through market troughs regardless of valuation tranche. The cap equals the strategy cap (1.0); the skill never binds on COSTLY_VITALITY_STAPLE.

Secondary Filter / Asymmetric Gate — Structural Moat Decay Hysteresis

Apply the persistence test after state classification and before capping delta:
• Even a historic multi-cycle staple suffers permanent structural impairment if consecutive_vitality_erosion_quarters >= 8 (two or more consecutive years in which trough_organic_vitality_score < 35 AND costly_attribute_score < 50). Multi-year erosion of both costly barriers and organic trough demand confirms irreversible obsolescence rather than a cyclical trough.
If consecutive_vitality_erosion_quarters >= 8, halve the state's delta cap:
• CONTESTED_TURNAROUND_SURVIVOR cap of 0.85 becomes 0.425.
• UNPROVEN_NOVELTY_CYCLE cap of 0.55 becomes 0.275.
• HOLLOW_NOSTALGIA_SHELL cap of 0.20 becomes 0.10.
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read costly vitality dict. From snapshot.external_data["costly_vitality"], load cycles_survived, costly_attribute_score, trough_organic_vitality_score, valuation_tranche, and consecutive_vitality_erosion_quarters. If absent or empty, record COSTLY_VITALITY_STAPLE, note the omission, and do not cite this skill.
2. Classify Lindy multi-cycle persistence. Apply Reading 1 (multi_cycle_lindy_veteran, single_trough_survivor, or untested_current_novelty).
3. Classify costly-to-fake attributes. Apply Reading 2 (unforgeable_costly_moat, contested_legacy_asset, or replicable_or_eroded_shell).
4. Classify trough organic vitality. Apply Reading 3 (price_independent_vitality, moderate_trough_retention, or price_dependent_ghost_town).
5. Classify state. Evaluate in strict priority order (HOLLOW_NOSTALGIA_SHELL → UNPROVEN_NOVELTY_CYCLE → CONTESTED_TURNAROUND_SURVIVOR → COSTLY_VITALITY_STAPLE).
6. Apply persistence test. If consecutive_vitality_erosion_quarters >= 8, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap), cite "costly-vitality-survivor-yardstick" in skills_cited and state cycles_survived, costly_attribute_score, trough_organic_vitality_score, valuation_tranche, and erosion quarters in rationale.

The Output Format

Your response must be a single JSON object. Do not include prose outside the object. The object has exactly five fields, in this order:
json {"action": "LONG", "delta": 0.85, "confidence": 0.84, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]} 
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP ranking or be "FLAT" (Invariant I1).
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state, cycles survived, costly attribute score, trough vitality, and cap reason. Example:
"CONTESTED_TURNAROUND_SURVIVOR state; cycles_survived=4, costly_attribute_score=62 (contested_legacy_asset), trough_organic_vitality_score=68 (price_independent_vitality), valuation_tranche=deep_value_distressed; capping delta at 0.85; costly-vitality-survivor-yardstick."
• skills_cited: list of skill names; include "costly-vitality-survivor-yardstick" only when the cap bound (intended delta > delta_cap).

Worked Examples


Case A — Multi-cycle costly-signal staple (cycles_survived = 6, high costly moat and trough vitality), cap does not bind

Snapshot:
• cycles_survived = 6
• costly_attribute_score = 84
• trough_organic_vitality_score = 79
• valuation_tranche = "large_cap_staple"
• consecutive_vitality_erosion_quarters = 0
Readings:
• Lindy Tier: multi_cycle_lindy_veteran (6 >= 2)
• Costly-Signal Tier: unforgeable_costly_moat (84 >= 65)
• Trough Retention Tier: price_independent_vitality (79 >= 60)
State: COSTLY_VITALITY_STAPLE, delta cap 1.0. Persistence: 0 < 8 → does not fire. AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind. LLM returns delta = 0.85 and does not cite "costly-vitality-survivor-yardstick".

Case B — Deep-value multi-cycle turnaround survivor (e.g., beaten-down fab/telecom ticker or post-trough protocol with intact costly infrastructure and organic trough demand), cap binds at 0.85

Snapshot:
• cycles_survived = 4
• costly_attribute_score = 61
• trough_organic_vitality_score = 67
• valuation_tranche = "deep_value_distressed"
• consecutive_vitality_erosion_quarters = 1
Readings:
• Lindy Tier: multi_cycle_lindy_veteran (4 >= 2)
• Costly-Signal Tier: contested_legacy_asset (61 in 35 to 64)
• Trough Retention Tier: price_independent_vitality (67 >= 60)
State: CONTESTED_TURNAROUND_SURVIVOR, delta cap 0.85. Persistence: 1 < 8 → does not fire. AGOP ranks LONG. LLM intended delta = 0.90. Cap 0.85 binds. LLM returns delta = 0.85 and cites "costly-vitality-survivor-yardstick".

Case C — Hollow multi-cycle nostalgia shell (legacy name recognition, zero organic trough vitality), cap binds at 0.20

Snapshot:
• cycles_survived = 3
• costly_attribute_score = 29
• trough_organic_vitality_score = 21
• valuation_tranche = "deep_value_distressed"
• consecutive_vitality_erosion_quarters = 5
Readings:
• Lindy Tier: multi_cycle_lindy_veteran (3 >= 2)
• Costly-Signal Tier: replicable_or_eroded_shell (29 < 35)
• Trough Retention Tier: price_dependent_ghost_town (21 < 35)
State: HOLLOW_NOSTALGIA_SHELL, delta cap 0.20. Persistence: 5 < 8 → does not fire. AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.20 binds. LLM returns delta = 0.20 and cites "costly-vitality-survivor-yardstick".

## Free Data Sources

The fetcher populates `snapshot.external_data["costly_vitality"]` from specialized open fundamental, intellectual-property, protocol-revenue, developer, news/tabloid, and social-murmur endpoints (no paid subscription required):

* **SEC EDGAR CompanyFacts XBRL API (`data.sec.gov/api/xbrl/companyfacts`):** `https://sec.gov` (free multi-decade R&D expenditure, gross-margin stability across historical recessions, tangible property/plant/equipment capex, and balance-sheet survivability across valuation tranches).
* **USPTO PatentsView API & EPO Open Patent Services:** `https://patentsview.org` (free historical patent-grant counts, forward citation velocity, and technical moat depth verifying costly-to-fake engineering barriers for legacy tech, semiconductor, telecom, and industrial tickers like `INTC`, `AMD`, and `NOK`).
* **DefiLlama Protocol Fees, Revenue & DEX Volume API (`api.llama.fi/summary/fees`):** `https://defillama.com` (free real protocol fee generation, DEX settlement throughput, and active-user retention **during bear-market price troughs**—separating genuine settlement engines like `SOL` from zero-fee zombie shells).
* **CoinGecko Public Markets & Historical Trough API (`://coingecko.com`):** `https://coingecko.com` (free multi-cycle listing history, circulating-to-FDV supply structure, and trough-period spot trading volume floors verifying organic liquidity persistence for multi-cycle survivors like `SOL` and `DOGE`).
* **GitHub REST/GraphQL API & Open-Source Commit Telemetry (`://github.com`):** `https://github.com` (free multi-year contributor retention, core repository commit frequency, and ecosystem fork/star growth during crypto winters—confirming active engineering commitment independent of token price).
* **Blockchair / Mempool.space Open On-Chain Explorers:** `https://blockchair.com` (free daily active addresses, non-zero balance wallet counts, and UTXO/account longevity distributions measuring unforced grassroots network persistence across cycles).
* **GDELT Project 2.0 Global Knowledge Graph & News Tone Streams:** `https://gdeltproject.org` (free 15-minute global news, financial press, and regional media coverage streams measuring whether legacy brands or tickers retain continuous mainstream press relevance during market troughs).
* **Tabloid, Pop-Culture & Mass-Market RSS / News Feeds (Google News RSS, Daily Mail / NY Post / Regional Tabloid RSS):** `https://google.com` (free unauthenticated RSS search feeds capturing mainstream tabloid, celebrity, and street-level pop-culture mentions—verifying whether consumer staples like Levi's, `KO`, `MCD`, or cultural icons like `DOGE` remain embedded in everyday mass culture rather than confined to niche financial terminals).
* **Bluesky AT Protocol Public Search, Mastodon Public Timelines & Reddit JSON Feeds:** `https://bsky.app` (free open social-media firehose/search endpoints measuring grassroots organic user chatter, meme velocity, and unprompted consumer mentions during bear markets when paid marketing budgets are turned off).
* **Wikimedia Pageviews REST API (`wikimedia.org/api/rest_v1/metrics/pageviews`):** `https://wikimedia.org` (free non-financialized baseline encyclopedic lookup floors during bear markets—measuring unforced brand and cultural recall independent of speculative price spikes).


Do Not

• Do not confuse depressed market valuation (deep_value_distressed) with eroded costly attributes; evaluate costly_attribute_score and trough_organic_vitality_score strictly independent of current price or market rank.
• Do not treat untested current-cycle launches (cycles_survived == 0) as COSTLY_VITALITY_STAPLE regardless of hype or market cap.
• Do not invent a directional action outside allowed_actions or "FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not compute precise floating-point arithmetic; use the qualitative comparison tables.
• Do not cite "costly-vitality-survivor-yardstick" when the cap did not bind (intended delta <= delta_cap).

Citation Mapping

• Costly Signaling & Unforgeable Attributes: Amotz Zahavi, "Mate Selection—A Selection for a Handicap," Journal of Theoretical Biology 53(1), 205–214 (1975); Amotz Zahavi & Avishag Zahavi, The Handicap Principle: A Missing Piece of Darwin's Puzzle (Oxford University Press, 1997). Formalizes why high-cost, unforgeable attributes reliably signal underlying vitality across biological, social, consumer, and market domains.
• Lindy Survival Persistence & Non-Perishable Endurance: Nassim Nicholas Taleb, Antifragile: Things That Gain from Disorder (Random House, 2012); Benoit Mandelbrot, The Fractal Geometry of Nature (1982). Grounds why survival across multiple full stress troughs increases expected future durability.
• Conspicuous Status vs. Enduring Functional Utility: Thorstein Veblen, The Theory of the Leisure Class (Macmillan, 1899); Pierre Bourdieu, Distinction (Harvard University Press, 1984). Separates transient status/valuation rank from intrinsic costly vitality.
• Bounded Supervisory Control: Stafford Beer, Brain of the Firm (1972); Peter J. Ramadge & W. Murray Wonham (1987). Downward-only damping within JANUS invariants I1–I9.