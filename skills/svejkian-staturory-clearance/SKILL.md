#### name: "svejkian-statutory-clearance"
description: "Detect conflicting or overlapping governing authorities, international treaties, statutes, and regulations; apply a hyper-literal Svejkian interpretation to select the cleanest, minimal-liability execution path and cap delta as statutory collision severity rises."

#### Švejkian Statutory Clearance

You are reading the tick against the **jurisdictional overlap and
statutory collision** surrounding the target asset, venue, or cross-border
corridor. In Lon L. Fuller's *The Morality of Law* (1964) and Guido
Calabresi's *A Common Law for the Age of Statutes* (1982), overlapping
or mutually contradictory treaties, statutes, and regulatory agencies
destroy legal predictability, expose capital to arbitrary selective
enforcement, and create compliance deadlocks. 

When two or more governing authorities or statutory regimes collide,
standard discretionary negotiation invites discretionary retaliation.
Following Jaroslav Hašek's *The Good Soldier Švejk* (1923)—where
**hyper-literal, deadpan obedience to the exact text of the rulebook**
exposes bureaucratic contradictions and leaves the actor completely
unassailable—the cleanest, lowest-liability resolution is a **strict
Švejkian statutory interpretation**: 

1. **Take every binding statutory constraint verbatim** without informal
workarounds, unwritten gentlemen's agreements, or discretionary waivers.
2. **Enforce the strict intersection (most restrictive floor)** of all
overlapping rules so every authority's literal text is satisfied
simultaneously.
3. **If two binding rules are mutually exclusive** (obeying Statute A
literally violates Treaty/Statute B), **refuse execution (FLAT)**
immediately rather than gambling on administrative forbearance.

Your job is to classify the tick into one of four statutory-clearance
states and cap your delta accordingly. You do not invent trades. You
do not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["statutory_clearance"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher and legal-registry parser normalize applicable treaty,
statutory, and agency overlap metadata into
snapshot.external_data["statutory_clearance"]. Each ticker, venue, or
corridor entry supplies: 

* overlapping_authorities_count: integer count of distinct national,
supranational, or treaty authorities asserting concurrent regulatory
or licensing jurisdiction over the instrument or corridor.
* statutory_conflict_level: qualitative text-collision state derived
from primary statute/treaty comparison ("harmonized", "layered",
"ambiguous_overlap", or "mutually_exclusive").
* svejkian_literal_path_exists: boolean (true or false) indicating
whether a strictly literal, zero-discretion compliance path exists
that satisfies all overlapping texts simultaneously without relying on
official forbearance or informal interpretation.
* enforcement_arbitrariness_index: normalized 0 to 100 score
measuring retroactive rule changes, selective enforcement actions, or
contradictory agency guidance in the target jurisdiction (< 25 =
predictable text-bound rule of law; > 65 = high arbitrary scrutiny).
* quarters_unresolved_conflict: consecutive calendar quarters in
which statutory_conflict_level has remained "ambiguous_overlap" or
"mutually_exclusive" without statutory harmonization.

If snapshot.external_data["statutory_clearance"] is absent or empty,
treat the instrument as **unmonitored**, record state **CLEAR_TEXT**,
note that no statutory overlap data was available, and do not cite this
skill. 

#### Reading 1 — Jurisdictional overlap density (overlapping_authorities_count)

Evaluate how many separate governing authorities claim concurrent
jurisdiction over the trade, asset, or supply corridor: 

overlapping_authorities_countAuthority Stack
**1**
**unitary** — single clear statutory authority
**2**
**bilateral** — dual-agency or home/host treaty overlap
**3 to 4**
**multi_layered** — stacked national, bloc, and treaty regimes
**≥ 5**
**fragmented_web** — dense multi-jurisdictional turf collision

If overlapping_authorities_count is missing, treat as **bilateral**. 

#### Reading 2 — Textual collision & Švejkian literal path (statutory_conflict_level & svejkian_literal_path_exists)

Evaluate whether the overlapping treaties, statutes, and regulations
can be satisfied simultaneously by strict, literal obedience to the text: 

statutory_conflict_levelsvejkian_literal_path_existsŠvejkian Clearance
**"harmonized"**
true**verbatim_clear** — single unambiguous text; literal compliance trivial
**"layered"**
true**strict_intersection** — additive rules; taking the strictest bound satisfies all texts
**"ambiguous_overlap"**
true**defensive_literal** — vague or overlapping text, but a safe literal safe-harbor exists
**"ambiguous_overlap"**
false**discretionary_trap** — compliance requires informal agency blessing or selective forbearance
**"mutually_exclusive"**
any**irreconcilable** — literal obedience to Rule A violates Rule B

If svejkian_literal_path_exists is missing, treat as false whenever
statutory_conflict_level is "ambiguous_overlap" or "mutually_exclusive". 

#### Reading 3 — Arbitrary scrutiny exposure (enforcement_arbitrariness_index)

Evaluate whether authorities enforce the written text literally or
weaponize statutory ambiguity for selective scrutiny: 

enforcement_arbitrariness_indexScrutiny Regime
**< 25**
**text_bound** — predictable, literal administrative adjudication
**25 to 45**
**procedural** — heavy documentation, but bound by written rules
**45 to 65**
**discretionary** — selective audits and broad interpretive leeway
**> 65**
**arbitrary** — retroactive enforcement, shifting goalposts, or political targeting

If enforcement_arbitrariness_index is missing, treat as **procedural**. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
statutory-clearance states. Evaluate in strict priority order and select
the first state whose conditions are fully satisfied: 

1. **IRRECONCILABLE_CONFLICT** (most severe — unconditional FLAT)
2. **ARBITRARY_EXPOSURE**
3. **LITERAL_INTERSECTION**
4. **CLEAR_TEXT** (strictest adaptive fit)

#### IRRECONCILABLE_CONFLICT

Any of the following hold: 

* Švejkian Clearance is **irreconcilable** ("mutually_exclusive").
* Švejkian Clearance is **discretionary_trap** AND Scrutiny Regime is
**arbitrary** (> 65).
* Authority Stack is **fragmented_web** (≥ 5) AND Švejkian Clearance
is **discretionary_trap** AND Scrutiny Regime is **discretionary** or
**arbitrary** (≥ 45).

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. No hyper-literal, minimal-liability execution path
exists: obeying one authority triggers statutory liability under another,
or exposes capital to uninsurable arbitrary scrutiny. The skill binds
unconditionally and must appear in skills_cited. 

#### ARBITRARY_EXPOSURE

Any of the following hold (and IRRECONCILABLE_CONFLICT does not apply): 

* Švejkian Clearance is **discretionary_trap** (svejkian_literal_path_exists = false).
* Scrutiny Regime is **arbitrary** (> 65).
* Švejkian Clearance is **defensive_literal** AND Scrutiny Regime is
**discretionary** (45 to 65).

**Delta cap: 0.25.** Overlapping statutes leave gray zones where literal
text alone does not guarantee immunity from discretionary scrutiny or
facilitation demands. Execute strictly within the narrowest literal
safe-harbor and reduce position size substantially. 

#### LITERAL_INTERSECTION

Any of the following hold (and neither IRRECONCILABLE_CONFLICT nor
ARBITRARY_EXPOSURE applies): 

* Švejkian Clearance is **strict_intersection** ("layered" + literal path).
* Švejkian Clearance is **defensive_literal** AND Scrutiny Regime is
**text_bound** or **procedural** (< 45).
* Authority Stack is **multi_layered** (3 to 4) with **verbatim_clear**
or **strict_intersection** clearance.

**Delta cap: 0.75.** Multiple authorities or treaties overlap, but a
clean, hyper-literal Švejkian compliance path satisfies every written
text simultaneously without relying on official favors. Reduce size
relative to CLEAR_TEXT to absorb documentation overhead. 

#### CLEAR_TEXT

All of the following hold: 

* Authority Stack is **unitary** or **bilateral** (1 to 2).
* Švejkian Clearance is **verbatim_clear**.
* Scrutiny Regime is **text_bound** (< 25).

**Delta cap: 1.0.** Single or harmonized statutory regime with literal,
predictable enforcement. The cap equals the strategy cap; the skill
never binds on CLEAR_TEXT. 

#### Ambiguous fallback

Any combination not covered above is classified **ARBITRARY_EXPOSURE**
with delta cap 0.25. 

#### Secondary Filter / Asymmetric Gate — Statutory Deadlock Hysteresis

Apply the persistence test after state classification and before the
cap. 

A statutory collision is **structurally entrenched** if
quarters_unresolved_conflict >= 3 (three or more consecutive quarters
in which statutory_conflict_level remained "ambiguous_overlap" or
"mutually_exclusive"). Three consecutive quarters without legislative
or treaty harmonization proves that authorities are intentionally
preserving jurisdictional ambiguity as a discretionary lever. 

If the collision is **structurally entrenched**, halve the state's delta
cap:
• LITERAL_INTERSECTION cap of 0.75 becomes 0.375.
• ARBITRARY_EXPOSURE cap of 0.25 becomes 0.125.
• IRRECONCILABLE_CONFLICT cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read statutory clearance dict. From
snapshot.external_data["statutory_clearance"], load
overlapping_authorities_count, statutory_conflict_level,
svejkian_literal_path_exists, enforcement_arbitrariness_index,
and quarters_unresolved_conflict. If absent or empty, record
CLEAR_TEXT, note the omission, and do not cite this skill.
2. Classify authority stack. Apply Reading 1 (unitary,
bilateral, multi_layered, or fragmented_web).
3. Classify Švejkian clearance. Apply Reading 2 (verbatim_clear,
strict_intersection, defensive_literal, discretionary_trap, or
irreconcilable).
4. Classify scrutiny regime. Apply Reading 3 (text_bound,
procedural, discretionary, or arbitrary).
5. Classify state. Evaluate in strict priority order
(IRRECONCILABLE_CONFLICT → ARBITRARY_EXPOSURE →
LITERAL_INTERSECTION → CLEAR_TEXT) and select the first matching
state (fallback: ARBITRARY_EXPOSURE).
6. Apply persistence test. If quarters_unresolved_conflict >= 3,
halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
state is IRRECONCILABLE_CONFLICT, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
state is IRRECONCILABLE_CONFLICT, cite
"svejkian-statutory-clearance" in skills_cited and state the
literal compliance constraint in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If IRRECONCILABLE_CONFLICT,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state, overlapping regime,
and minimal-liability instruction. Example:
"ARBITRARY_EXPOSURE state; 4 overlapping authorities with ambiguous_overlap and discretionary scrutiny (54) for 4 quarters; execute only via literal safe-harbor; delta capped at 0.125; svejkian-statutory-clearance."
• skills_cited: list of skill names; include
"svejkian-statutory-clearance" only when the cap bound or the state
is IRRECONCILABLE_CONFLICT.

Worked Examples


Case A — Additive cross-border rules with clean Švejkian intersection, cap binds mildly

Snapshot:
• overlapping_authorities_count = 3
• statutory_conflict_level = "layered"
• svejkian_literal_path_exists = true
• enforcement_arbitrariness_index = 20.0
• quarters_unresolved_conflict = 0
Readings:
• Authority Stack: 3 → multi_layered
• Švejkian Clearance: "layered" + true → strict_intersection
• Scrutiny Regime: < 25 → text_bound
State: LITERAL_INTERSECTION, delta cap 0.75. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.90. Cap 0.75 binds.
LLM returns delta = 0.75 and cites "svejkian-statutory-clearance".

Case B — Mutually exclusive treaty/sanction rules, unconditional FLAT

Snapshot:
• overlapping_authorities_count = 4
• statutory_conflict_level = "mutually_exclusive"
• svejkian_literal_path_exists = false
• enforcement_arbitrariness_index = 72.0
• quarters_unresolved_conflict = 3
Readings:
• Authority Stack: 4 → multi_layered
• Švejkian Clearance: "mutually_exclusive" → irreconcilable
• Scrutiny Regime: > 65 → arbitrary
State: IRRECONCILABLE_CONFLICT, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "svejkian-statutory-clearance".

Free Data Sources

• EUR-Lex & N-Lex (EU & National Statutory Repositories):
https://europa.eu (free, no-key SPARQL/REST endpoints for
EU directives, regulations, and national transposition conflicts).
• UN Treaty Collection & UNCTAD International Investment Agreements Navigator:
https://unctad.org (free public database of bilateral
investment treaties, arbitration clauses, and overlapping treaty rules).
• U.S. Federal Register & eCFR API:
https://federalregister.gov and
https://ecfr.gov (free, no-key
JSON APIs tracking agency rule overlaps and effective dates).
• WTO / UNCTAD TRAINS Non-Tariff Measures (NTM) Database:
https://unctad.org (free open portal mapping overlapping
customs, licensing, and technical-barrier regulations across corridors).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not recommend informal workarounds, discretionary waivers, or
off-text shortcuts; always select the hyper-literal Švejkian path.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "svejkian-statutory-clearance" when the cap did not bind.

Citation Mapping

• Hyper-Literal Bureaucratic Compliance: Jaroslav Hašek, The Good
Soldier Švejk (Osudy dobrého vojáka Švejka za světové války,
1921–1923). Literal, unembellished execution of written rules neutralizes
contradictory authority without incurring personal or legal liability.
• Internal Morality of Law & Statutory Collision: Lon L. Fuller,
The Morality of Law (Yale University Press, 1964), Ch. 2 (identifying
contradictory rules and non-congruence between declared rule and
official action as systemic legal failures); Guido Calabresi, A Common
Law for the Age of Statutes (Harvard University Press, 1982).
• Legal Indeterminacy & Regulatory Arbitrage: H. L. A. Hart, The
Concept of Law (Oxford University Press, 1961) ("penumbra of
uncertainty" vs. settled core of literal text).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
