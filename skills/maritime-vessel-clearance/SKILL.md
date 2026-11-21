#### name: "maritime-vessel-clearance"
description: "Perform civilian commercial due diligence on a vessel's flag-state registry, International Group P&I insurance coverage, Port State Control (PSC) inspection record, and open AIS port-call/transponder continuity using free Equasis, IMO GISIS, Paris/Tokyo MoU, IG P&I, and Fintraffic Digitraffic / IMF PortWatch telemetry; cap delta or force FLAT on uninsurable or high-detention vessels."

#### Maritime Vessel Registry, Insurance & Port-Call Clearance

You are reading the tick against the **civilian commercial admissibility,
class/flag integrity, P&I liability coverage, and kinematic port-call
continuity** of the target vessel or shipping counterparty. In maritime
underwriting and cargo chartering (Stopford, *Maritime Economics*, 2009;
UNCLOS Art. 91 & 94), placing civilian freight or commodity exposure onto a
vessel lacking valid International Group Protection & Indemnity (IG P&I)
coverage, recognized IACS classification society standing, or continuous
AIS transponder provenance exposes cargo owners and charterers to
catastrophic uninsured general average, port detention, cargo seizure,
and statutory liability. 

Even where a shipping lane itself is physically open (maritime-chokepoint),
a specific vessel operating on that lane may be commercially uninsurable
due to rapid flag-hopping across low-oversight registries (Paris/Tokyo MoU
"Black List" flags), lapsed or unverifiable P&I cover, repeated Port State
Control (PSC) structural deficiencies, or unexplained AIS transponder dark
periods and open-water ship-to-ship (STS) drift anomalies. 

Your job is to classify the vessel into one of four due-diligence clearance
states and cap your delta accordingly. You do not invent trades. You do
not override AGOP. You modulate the LLM's delta within the bound the
verifier already permits. You never raise delta above the strategy cap,
and you never invent an action outside allowed_actions. 

#### The Readings

Compute three readings from snapshot.external_data["vessel_clearance"].
Use the qualitative tables below. Do not compute precise arithmetic. 

#### Monitored telemetry fields

The fetcher normalizes open vessel registry, Port State Control, P&I club
member lookup, and AIS port-call telemetry into
snapshot.external_data["vessel_clearance"]. Each vessel IMO or charter
corridor entry supplies: 

* flag_psc_tier: Port State Control flag-state performance tier from
Paris MoU / Tokyo MoU annual White-Grey-Black lists ("white_list",
"grey_list", or "black_list").
* iacs_class_valid: boolean (true or false) indicating whether the
vessel holds active, non-suspended classification with an International
Association of Classification Societies (IACS) member verified via
Equasis / IMO GISIS.
* ig_pi_insurance_verified: boolean (true or false) indicating
whether active Protection & Indemnity liability cover is verified via
public International Group P&I club vessel-search registries.
* psc_detentions_24m: integer count of Port State Control detentions
recorded across Paris MoU, Tokyo MoU, USCG PSIX, or Equasis over the
trailing 24 months (0 = clean record; >= 2 = chronic deficiency).
* ais_dark_hours_30d: cumulative unexplained AIS transponder gap hours
(outside known terrestrial coverage dead-zones) over the trailing 30
days (< 6 = continuous tracking; > 48 = extended dark-fleet gap).
* unscheduled_sts_loiter_30d: integer count of unscheduled open-water
loitering or ship-to-ship (STS) proximity events detected in
AIS / IMF PortWatch / Fintraffic Digitraffic port-call logs over the
trailing 30 days.
* flag_changes_36m: integer count of flag-state re-registrations over
the trailing 36 months (>= 3 = chronic flag-hopping).

If snapshot.external_data["vessel_clearance"] is absent or empty, treat
the instrument as **unmonitored** (not a vessel-specific booking), record
state **VERIFIED_ADMISSIBLE**, note that no vessel clearance data was
available, and do not cite this skill. 

#### Reading 1 — Registry, IACS class & P&I insurance integrity (flag_psc_tier, iacs_class_valid, ig_pi_insurance_verified)

Evaluate whether the vessel carries verifiable flag-state oversight,
IACS structural class, and International Group P&I third-party cover: 

ig_pi_insurance_verifiediacs_class_validflag_psc_tierUnderwriting Standing
**true**
true"white_list"**tier1_insured** — White-List flag, active IACS class, verified IG P&I
**true**
true"grey_list"**conditional_insured** — verified IG P&I and class, but elevated flag scrutiny
**true**
falseany**class_lapsed** — P&I listed, but IACS structural class withdrawn or unverified
**false**
anyany**uninsured_hull** — no verified International Group P&I liability cover
**any**
any"black_list"**uninsured_hull** — Black-List flag; severe port-state detention & seizure exposure

If ig_pi_insurance_verified or iacs_class_valid is missing, treat the
missing boolean as false (fail-closed due diligence). 

#### Reading 2 — Port State Control inspection & detention record (psc_detentions_24m)

Evaluate the vessel's physical safety and regulatory compliance record
from open port-state inspection logs: 

psc_detentions_24mPSC Inspection Tier
**0**
**clean_record** — zero detentions in trailing 24 months
**1**
**minor_friction** — single isolated detention; heightened port scrutiny
**2**
**repeat_offender** — multiple detentions; high risk of cargo delay or refusal
**≥ 3**
**chronic_substandard** — persistent structural/safety non-compliance; banning risk

If psc_detentions_24m is missing, treat as **minor_friction** (1). 

#### Reading 3 — Kinematic AIS continuity & port-call provenance (ais_dark_hours_30d & unscheduled_sts_loiter_30d)

Evaluate whether the vessel's observed AIS trajectory and port-call
sequence match legitimate commercial liner/tramp behavior: 

ais_dark_hours_30dunscheduled_sts_loiter_30dKinematic Provenance
**< 6**
0**continuous_track** — unbroken AIS and scheduled port-call logs
**6 to 24**
0**minor_signal_gap** — brief coastal/weather gap; port calls intact
**24 to 48**
1**anomalous_drift** — multi-day AIS gap or unscheduled offshore loiter
**> 48**
any**dark_corridor_pattern** — prolonged transponder shutoff; high provenance risk
**any**
≥ 2**dark_corridor_pattern** — repeated unscheduled offshore STS proximity events

If either metric falls in a worse row, take the **worse** (more
restrictive) classification. 

#### Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four
vessel-clearance states. Evaluate in strict priority order and select
the first state whose conditions are fully satisfied: 

1. **INADMISSIBLE_VESSEL** (most severe — unconditional FLAT)
2. **HIGH_SCRUTINY_CHARTER**
3. **CONDITIONAL_CLEARANCE**
4. **VERIFIED_ADMISSIBLE** (strictest adaptive fit)

#### INADMISSIBLE_VESSEL

Any of the following hold: 

* Underwriting Standing is **uninsured_hull** (ig_pi_insurance_verified = false
or flag_psc_tier = "black_list").
* Underwriting Standing is **class_lapsed** AND PSC Inspection Tier is
**repeat_offender** or **chronic_substandard** (>= 2).
* PSC Inspection Tier is **chronic_substandard** (>= 3 detentions).
* Kinematic Provenance is **dark_corridor_pattern** (> 48h AIS dark
gap or >= 2 unscheduled STS events) AND Underwriting Standing is not
**tier1_insured**.

**Delta cap: 0.0.** Set delta = 0.0 and action = "FLAT" regardless
of what AGOP ranked. Booking cargo or taking direct commercial exposure
on a vessel without verified IG P&I insurance, valid class, or
auditable AIS provenance violates basic maritime underwriting and
exposes capital to uninsurable loss or port detention. The skill binds
unconditionally and must appear in skills_cited. 

#### HIGH_SCRUTINY_CHARTER

Any of the following hold (and INADMISSIBLE_VESSEL does not apply): 

* Underwriting Standing is **class_lapsed**.
* PSC Inspection Tier is **repeat_offender** (2 detentions).
* Kinematic Provenance is **dark_corridor_pattern** (on an otherwise
tier1_insured hull).
* Kinematic Provenance is **anomalous_drift** AND Underwriting Standing
is **conditional_insured** ("grey_list").

**Delta cap: 0.25.** Vessel carries verified P&I insurance, but recent
detentions, Grey-List flag status, or AIS gaps create high odds of port
delays, charter-party disputes, and demurrage burn. Reduce size
substantially. 

#### CONDITIONAL_CLEARANCE

Any of the following hold (and neither INADMISSIBLE_VESSEL nor
HIGH_SCRUTINY_CHARTER applies): 

* Underwriting Standing is **conditional_insured** ("grey_list" with
verified IG P&I and IACS class).
* PSC Inspection Tier is **minor_friction** (1 detention).
* Kinematic Provenance is **minor_signal_gap** or **anomalous_drift**
on a **tier1_insured** vessel with 0 detentions.

**Delta cap: 0.75.** Vessel is legally admissible and insured, but minor
registry, inspection, or routing anomalies warrant a modest demurrage and
delay buffer. Reduce size relative to VERIFIED_ADMISSIBLE. 

#### VERIFIED_ADMISSIBLE

All of the following hold: 

* Underwriting Standing is **tier1_insured** (ig_pi_insurance_verified = true,
iacs_class_valid = true, flag_psc_tier = "white_list").
* PSC Inspection Tier is **clean_record** (0 detentions).
* Kinematic Provenance is **continuous_track** (< 6h gap, 0 STS).

**Delta cap: 1.0.** Clean White-List registry, active IACS class,
verified International Group P&I cover, zero detentions, and continuous
AIS port-call history. The cap equals the strategy cap; the skill never
binds on VERIFIED_ADMISSIBLE. 

#### Ambiguous fallback

Any combination not covered above is classified **HIGH_SCRUTINY_CHARTER**
with delta cap 0.25.

Secondary Filter / Asymmetric Gate — Flag-Hopping Persistence Hysteresis

Apply the persistence test after state classification and before the
cap.
A vessel's registry profile is structurally evasive if
flag_changes_36m >= 3 (three or more flag-state re-registrations within
36 months). Rapid serial re-flagging across jurisdictions is the classic
empirical indicator of regulatory arbitrage to evade Port State Control
banning orders or ownership transparency.
If the vessel is structurally evasive, halve the state's delta cap:
• CONDITIONAL_CLEARANCE cap of 0.75 becomes 0.375.
• HIGH_SCRUTINY_CHARTER cap of 0.25 becomes 0.125.
• INADMISSIBLE_VESSEL cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read vessel clearance dict. From
snapshot.external_data["vessel_clearance"], load flag_psc_tier,
iacs_class_valid, ig_pi_insurance_verified, psc_detentions_24m,
ais_dark_hours_30d, unscheduled_sts_loiter_30d, and
flag_changes_36m. If absent or empty, record
VERIFIED_ADMISSIBLE, note the omission, and do not cite this
skill.
2. Classify underwriting standing. Apply Reading 1 (tier1_insured,
conditional_insured, class_lapsed, or uninsured_hull).
3. Classify PSC inspection tier. Apply Reading 2 (clean_record,
minor_friction, repeat_offender, or chronic_substandard).
4. Classify kinematic provenance. Apply Reading 3 (continuous_track,
minor_signal_gap, anomalous_drift, or dark_corridor_pattern).
5. Classify state. Evaluate in strict priority order
(INADMISSIBLE_VESSEL → HIGH_SCRUTINY_CHARTER →
CONDITIONAL_CLEARANCE → VERIFIED_ADMISSIBLE) and select the
first matching state (fallback: HIGH_SCRUTINY_CHARTER).
6. Apply persistence test. If flag_changes_36m >= 3, halve
delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the
state is INADMISSIBLE_VESSEL, set delta = 0.0 and
action = "FLAT" regardless of AGOP. Otherwise, if intended delta
exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the
state is INADMISSIBLE_VESSEL, cite "maritime-vessel-clearance"
in skills_cited and state the due-diligence finding in the
rationale.

The Output Format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP
ranking or be "FLAT" (Invariant I1). If INADMISSIBLE_VESSEL,
action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state and due-diligence
finding. Example:
"INADMISSIBLE_VESSEL state; ig_pi_insurance_verified=false, black_list flag, and 62h AIS dark gap; refusing commercial cargo exposure; action=FLAT; maritime-vessel-clearance."
• skills_cited: list of skill names; include
"maritime-vessel-clearance" only when the cap bound or the state is
INADMISSIBLE_VESSEL.

Worked Examples


Case A — Tier-1 White-List liner vessel with verified IG P&I and clean AIS, cap does not bind

Snapshot:
• flag_psc_tier = "white_list"
• iacs_class_valid = true
• ig_pi_insurance_verified = true
• psc_detentions_24m = 0
• ais_dark_hours_30d = 1.5
• unscheduled_sts_loiter_30d = 0
• flag_changes_36m = 0
Readings:
• Underwriting Standing: tier1_insured
• PSC Inspection Tier: clean_record
• Kinematic Provenance: continuous_track
State: VERIFIED_ADMISSIBLE, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "maritime-vessel-clearance".

Case B — Grey-List vessel with verified P&I but repeated flag-hopping and AIS gap, cap binds

Snapshot:
• flag_psc_tier = "grey_list"
• iacs_class_valid = true
• ig_pi_insurance_verified = true
• psc_detentions_24m = 1
• ais_dark_hours_30d = 30.0
• unscheduled_sts_loiter_30d = 1
• flag_changes_36m = 4
Readings:
• Underwriting Standing: conditional_insured
• PSC Inspection Tier: minor_friction
• Kinematic Provenance: anomalous_drift
State: HIGH_SCRUTINY_CHARTER, delta cap 0.25.
Persistence: flag_changes_36m = 4 >= 3 → halve to 0.125.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.125 binds.
LLM returns delta = 0.125 and cites "maritime-vessel-clearance".

Case C — Unverified P&I insurance and Black-List registry, unconditional FLAT

Snapshot:
• flag_psc_tier = "black_list"
• iacs_class_valid = false
• ig_pi_insurance_verified = false
• psc_detentions_24m = 2
• ais_dark_hours_30d = 64.0
• unscheduled_sts_loiter_30d = 2
• flag_changes_36m = 3
Readings:
• Underwriting Standing: uninsured_hull
• PSC Inspection Tier: repeat_offender
• Kinematic Provenance: dark_corridor_pattern
State: INADMISSIBLE_VESSEL, delta cap 0.0 → forces FLAT.
AGOP ranks LONG. LLM returns action = "FLAT", delta = 0.0, and
cites "maritime-vessel-clearance".

Free Data Sources

The fetcher populates snapshot.external_data["vessel_clearance"] from
the following free, open public maritime registries and AIS telemetry
feeds (no paid subscription required):
• Equasis Public Maritime Safety Database:
https://equasis.org (free public vessel lookup providing IMO
number, flag history, IACS classification society status, P&I club
entries, and Port State Control inspection summaries).
• IMO Global Integrated Shipping Information System (GISIS):
https://imo.org (free public UN International Maritime
Organization portal for ship particulars, registered owners, and
flag-state administration records).
• Paris MoU & Tokyo MoU Port State Control Inspection & Flag Lists:
https://parismou.org and https://tokyo-mou.org (free
public detention search portals and annual White-Grey-Black flag-state
performance tables).
• International Group of P&I Clubs (IG P&I) Public Vessel Search:
https://igpandi.org (free directory linking to the 12 member
P&I clubs' open vessel-entry search tools to verify active third-party
and pollution liability insurance).
• Fintraffic Digitraffic Marine API & IMF PortWatch:
https://digitraffic.fi (free, no-key real-time Baltic/Finnish
AIS vessel positions, port calls, and metadata) and
https://imf.org (free global port-call and chokepoint AIS
telemetry).

Do Not

• Do not invent a directional action outside allowed_actions or
"FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not rely on self-reported charterer claims when ig_pi_insurance_verified
or iacs_class_valid is unverified in open registries.
• Do not compute precise floating-point arithmetic; use the qualitative
comparison tables.
• Do not cite "maritime-vessel-clearance" when the cap did not bind
and the state is not INADMISSIBLE_VESSEL.

Citation Mapping

• Maritime Economics & Chartering Risk: Martin Stopford, Maritime
Economics, 3rd ed. (Routledge, 2009), Ch. 5 & 15 (freight market risk,
classification societies, P&I liability, and Port State Control
enforcement).
• Flag-State Jurisdiction & Genuine Link: United Nations Convention on
the Law of the Sea (UNCLOS, 1982), Articles 91, 94 & 217 (nationality
of ships, duties of the flag state, and port-state enforcement).
• Information Asymmetry & Counterparty Screening: George A. Akerlof,
"The Market for 'Lemons'," Quarterly Journal of Economics 84(3),
488–500 (1970) (adverse selection in substandard hull and uninsured
counterparty markets).
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm
(1972); Ramadge & Wonham (1987). Downward-only damping within JANUS
invariants I1–I9.
This pairs cleanly with maritime-chokepoint and svejkian-statutory-clearance: maritime-chokepoint checks whether the sea lane is open and profitable, svejkian-statutory-clearance checks whether the treaty/sanctions intersection permits the cargo, and maritime-vessel-clearance verifies that the specific ship is White-List registered, IACS-classed, IG P&I insured, detention-clean, and continuously tracked on open AIS.