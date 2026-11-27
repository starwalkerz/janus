
name: "civic-emancipation-pendulum-yardstick"
description: "Classify the tick by ~150-year civic-emancipation and labor-incorporation pendulum phase (~75-year broad civic expansion nodes vs. ~75-year mid-cycle oligarchic/coercive contraction troughs) across slavery/unfree labor, women's civic participation, working-class/guild organization, and minority/religious pluralism by querying KAIROS (:8300) alongside free V-Dem, ILO, Clio Infra, WVS, Walk Free GSI, and World Bank registries; cap delta or force FLAT when coercive labor lock-in or mid-pendulum civic contraction threatens institutional stability and human-capital velocity."


Civic Emancipation Pendulum Yardstick

You are reading the tick against the ~150-year civic-emancipation and labor-incorporation pendulum—a long-wave macro-historical oscillation (~75-year expansion half-cycles punctuated by ~75-year mid-pendulum contraction troughs) governing the legal and material incorporation of four structural cohorts: unfree/coerced labor, women, the working classes, and ethnic/religious minorities.
Empirically visible across ~150-year nodes—from late-13th/14th-century guild formalization, heterodox religious assertion, and Islamicate civic-commercial zenith; to ~1500s early modern serfdom dismantling paired with externalized overseas indenture; to the ~1600s/1610s royal prohibitions on Indigenous enslavement (e.g., Philip III's Ordenanzas / Crown decrees curbing encomienda bondage); to the ~1860s–1870s global emancipation cluster (U.S. abolition of slavery, Russian emancipation of the serfs, Finnish republican Fennomania and kansakoulu enlightenment, French Third Republic civic consolidation, Prussian Bildung and early social welfare, Ottoman Tanzimat citizenship reforms, and late-Qing Tongzhi/Xianfeng-era forced self-strengthening)—the cycle alternates between broad civic-incorporation waves and mid-pendulum coercive contractions (the Counter-Reformation / 17th-century crisis, the early-1800s post-Napoleonic reaction and industrial enclosure, and the early-1900s Jim Crow, colonial high-imperialism, and cartelized labor-suppression trough).
Drawing on Karl Polanyi's The Great Transformation (1944) on the double movement between market/coercive disembedding and social protection, W. E. B. Du Bois's Black Reconstruction (1935) on abolition-democracy and counter-revolution, Barrington Moore Jr.'s Social Origins of Dictatorship and Democracy (1966) on labor-repressive vs. civic-incorporating modernization, Albert O. Hirschman's The Rhetoric of Reaction (1991) on counter-emancipatory backlash waves, and T. H. Marshall's Citizenship and Social Class (1950) on civil, political, and social rights sequencing, JANUS queries KAIROS (:8300) directly alongside free longitudinal human-rights, labor-union, gender-parity, and modern-slavery registries to identify whether the target polity or sector is riding an expansion node, entering a mid-pendulum contraction trough, or trapped in coercive labor/oligarchic sclerosis.
Your job is to classify the tick into one of four civic-pendulum states and cap your delta accordingly. You do not invent trades. You do not override AGOP. You modulate the LLM's delta within the bound the verifier already permits. You never raise delta above the strategy cap, and you never invent an action outside allowed_actions.

The Readings

Compute three readings from snapshot.external_data["civic_emancipation_pendulum"] (populated by querying KAIROS :8300 over free multi-century and contemporary civic, gender, labor, and minority-rights registries). Use the qualitative tables below. Do not compute precise arithmetic.

Monitored telemetry fields

The fetcher queries KAIROS (:8300) and open longitudinal datasets and normalizes the target polity or supply-chain jurisdiction into snapshot.external_data["civic_emancipation_pendulum"]:
• unfree_labor_and_coercion_index: normalized intensity (0.0 to 1.0) of forced labor, debt bondage, convict/prison-labor reliance, and statutory movement restrictions derived from Walk Free Global Slavery Index (GSI), ILO Forced Labour indicators, and V-Dem freedom from forced labor (< 0.20 = free contractual mobility; > 0.60 = systemic unfree/coerced labor regime).
• womens_civic_participation_index: normalized index (0.0 to 1.0) of women's property rights, labor-force autonomy, political representation, and civil liberties derived from V-Dem Women's Political Empowerment Index (v2x_gender), World Bank Women, Business and the Law (WBL), and WVS gender-egalitarianism waves (> 0.70 = full civic/economic incorporation; < 0.35 = acute legal/civic exclusion).
• working_class_bargaining_index: normalized index (0.0 to 1.0) of independent labor union density, collective bargaining coverage, guild/cooperative autonomy, and social-wage floors derived from ILOSTAT union density / collective bargaining series, ICTWSS/OECD-AIAS database, and Clio Infra historical real-wage/union series (> 0.65 = institutionalized bargaining & cooperative voice; < 0.30 = atomized/suppressed labor).
• minority_pluralism_and_emancipation_index: normalized index (0.0 to 1.0) of religious/ethnic minority equal protection, anti-discrimination enforcement, and postcolonial/post-imperial self-determination derived from V-Dem Equal Protection (v2xeg_eqprotec), Minorities at Risk / EPR (Ethnic Power Relations), and Pew Government Restrictions on Religion (> 0.70 = pluralist civic parity; < 0.35 = caste/sectarian stratification or minority disenfranchisement).
• kairos_pendulum_phase_deg: phase angle (0° to 360°) returned by KAIROS (:8300) fitting the ~150-year civic pendulum (315°–45° = expansion crest / emancipation reform node; 45°–135° = post-reform consolidation & drift; 135°–225° = mid-pendulum contraction trough / oligarchic & coercive reaction; 225°–315° = pre-emancipation agitation & reform pressure).
• pendulum_velocity_slope: 10-year composite rate of change (-1.0 to +1.0) across the four civic indices (> +0.15 = active broadening of civic participation; < -0.15 = active rollback of labor, women's, or minority rights).
• contraction_trough_quarters: consecutive calendar quarters in which pendulum_velocity_slope <= -0.15 AND at least two of the four civic indices sit in their contracted/excluded tiers.
If snapshot.external_data["civic_emancipation_pendulum"] is absent or empty, treat the instrument as unmonitored, record state PLURALIST_EXPANSION_NODE, note that no civic-pendulum telemetry was available, and do not cite this skill.

Reading 1 — Four-Pillar Civic Incorporation Composite (Women, Working Class, Minorities, Free Labor)

Evaluate the breadth of civic and economic participation across the four structural pillars:

Pillar Alignment	Conditions
broad_civic_incorporation
	unfree_labor_and_coercion_index < 0.25 AND at least two of (womens_civic_participation_index, working_class_bargaining_index, minority_pluralism_and_emancipation_index) are ≥ 0.65, with none < 0.45
partial_or_uneven_emancipation
	unfree_labor_and_coercion_index between 0.25 and 0.45, OR one pillar < 0.45 while the remaining pillars hold ≥ 0.45 (e.g., formal abolition without working-class or minority parity)
mid_pendulum_contraction
	Two or more pillars < 0.40, OR unfree_labor_and_coercion_index between 0.45 and 0.65 (guild/union suppression, rollback of women's or minority civic status)
coercive_caste_lock_in
	unfree_labor_and_coercion_index > 0.65 OR three or more pillars < 0.30 (systemic forced labor, disenfranchised majority, or rigid sectarian/colonial caste hierarchy)

If individual pillar fields are missing, evaluate from available fields and cap the reading at partial_or_uneven_emancipation.

Reading 2 — ~150-Year KAIROS Pendulum Phase (kairos_pendulum_phase_deg & pendulum_velocity_slope)

Evaluate where the target polity sits on the ~150-year oscillation (~75-year expansion vs. ~75-year contraction):

Phase / Slope	Pendulum Regime Reading
315°–45° OR (225°–315° with slope > +0.15)
	emancipatory_crest — active ~150-year reform wave broadening suffrage, free labor, education (Bildung), and minority rights
45°–135° with slope in [-0.15, +0.15]
	post_reform_plateau — civic institutions operational; reform momentum slowing toward bureaucratic stasis
135°–225° OR (45°–135° with slope < -0.15)
	mid_pendulum_trough — ~75-year counter-wave; oligarchic concentration, union busting, nationalist/sectarian exclusion, and coercive labor creep
225°–315° with slope in [-0.15, +0.15]
	pre_reform_bottleneck — acute social friction and strike/suffrage/abolition pressure building against ossified elites

If kairos_pendulum_phase_deg is missing, infer from pendulum_velocity_slope (> +0.15 → emancipatory_crest; < -0.15 → mid_pendulum_trough; otherwise post_reform_plateau).

Reading 3 — Coercive Labor & Supply-Chain Externalization Check (unfree_labor_and_coercion_index)

Evaluate whether the polity or supply chain is dismantling coercion or externalizing bondage onto peripheral/overseas units:

unfree_labor_and_coercion_index	Labor Regime Tier
< 0.20
	free_contractual_mobility — transparent wage bargaining, cooperative ownership, and zero forced-labor taint
0.20 to 0.40
	precarious_informality — subcontracted/gig or migrant labor vulnerability without statutory bondage
0.40 to 0.65
	externalized_coercion_creep — domestic rights paired with offshore/supply-chain debt bondage or captive labor

| > 0.65 | systemic_unfree_bondage — direct forced labor, state-mandated conscription/prison labor, or chattel/serf equivalents |
If unfree_labor_and_coercion_index is missing, treat as precarious_informality.

Taxonomy / Decision Matrix

Combine Reading 1, Reading 2, and Reading 3 into one of four civic-pendulum states. Evaluate in strict priority order and select the first state whose conditions are fully satisfied:
1. COERCIVE_CASTE_LOCK_IN (most severe — unconditional FLAT)
2. MID_PENDULUM_CONTRACTION
3. UNEVEN_EMANCIPATION_DRIFT
4. PLURALIST_EXPANSION_NODE (strictest adaptive fit)

COERCIVE_CASTE_LOCK_IN

Any of the following hold:
• Pillar Alignment is coercive_caste_lock_in (unfree_labor_and_coercion_index > 0.65 or ≥ 3 pillars < 0.30).
• Labor Regime Tier is systemic_unfree_bondage (> 0.65).
• Pillar Alignment is mid_pendulum_contraction AND Pendulum Regime Reading is mid_pendulum_trough with pendulum_velocity_slope < -0.30 (acute authoritarian/oligarchic rollback).
Delta cap: 0.0. Set delta = 0.0 and action = "FLAT" regardless of what AGOP ranked. Coercive labor regimes and severe civic disenfranchisement destroy long-run total factor productivity, invite sanctions/trade interdiction (EUDR / forced-labor import bans), and signal structural instability. The skill binds unconditionally and must appear in skills_cited.

MID_PENDULUM_CONTRACTION

Any of the following hold (and COERCIVE_CASTE_LOCK_IN does not apply):
• Pillar Alignment is mid_pendulum_contraction (two or more pillars < 0.40 or coercion 0.45–0.65).
• Pendulum Regime Reading is mid_pendulum_trough (135°–225° or slope < -0.15) AND Labor Regime Tier is externalized_coercion_creep (0.40–0.65).
Delta cap: 0.25. The polity has swung into the ~75-year mid-pendulum trough (analogous to the early-1800s reaction or early-1900s oligarchic/colonial contraction): labor unions are weakened, women's or minority civic protections are eroding, and capital relies on coercive extraction rather than broad human-capital productivity. Cut directional exposure sharply.

UNEVEN_EMANCIPATION_DRIFT

Any of the following hold (and neither COERCIVE_CASTE_LOCK_IN nor MID_PENDULUM_CONTRACTION applies):
• Pillar Alignment is partial_or_uneven_emancipation (formal rights in one domain offset by exclusion or precarious labor in another).
• Pendulum Regime Reading is post_reform_plateau or pre_reform_bottleneck with pendulum_velocity_slope < 0.0.
• Labor Regime Tier is precarious_informality (0.20–0.40) or externalized_coercion_creep (0.40–0.65).
Delta cap: 0.75. Civic institutions function, but asymmetrical incorporation or reform fatigue creates strike risk, supply-chain audit exposure, or demographic under-utilization. Reduce size relative to PLURALIST_EXPANSION_NODE.

PLURALIST_EXPANSION_NODE

All of the following hold:
• Pillar Alignment is broad_civic_incorporation.
• Pendulum Regime Reading is emancipatory_crest or post_reform_plateau with pendulum_velocity_slope >= 0.0.
• Labor Regime Tier is free_contractual_mobility (< 0.20).
Delta cap: 1.0. The polity sits on an expansion node of the ~150-year pendulum: free mobile labor, strong cooperative/union bargaining, high female civic and economic participation, and equal minority protection reinforce institutional trust and broad-based productivity. The cap equals the strategy cap; the skill never binds on PLURALIST_EXPANSION_NODE.

Ambiguous fallback

Any combination not covered above is classified UNEVEN_EMANCIPATION_DRIFT with delta cap 0.75.

Secondary Filter / Asymmetric Gate — Multi-Quarter Contraction Persistence

Apply the persistence test after state classification and before the cap.
A civic contraction is structurally entrenched if contraction_trough_quarters >= 8 (two or more consecutive years of pendulum_velocity_slope <= -0.15 alongside two or more contracted civic pillars). Sustained multi-year rollback confirms that the swing is not transient electoral noise but a durable ~75-year mid-pendulum contraction wave.
If the contraction is structurally entrenched, halve the state's delta cap:
• UNEVEN_EMANCIPATION_DRIFT cap of 0.75 becomes 0.375.
• MID_PENDULUM_CONTRACTION cap of 0.25 becomes 0.125.
• COERCIVE_CASTE_LOCK_IN cap remains 0.0 (FLAT).
The gate is one-way. It cannot raise the cap; it can only lower it.

The Procedure

Execute this procedure on every tick. Do not skip steps.
1. Read the civic-pendulum dict. From snapshot.external_data["civic_emancipation_pendulum"], load unfree_labor_and_coercion_index, womens_civic_participation_index, working_class_bargaining_index, minority_pluralism_and_emancipation_index, kairos_pendulum_phase_deg, pendulum_velocity_slope, and contraction_trough_quarters. If absent or empty, record PLURALIST_EXPANSION_NODE, note the omission, and do not cite this skill.
2. Classify four-pillar alignment. Apply Reading 1 (broad_civic_incorporation, partial_or_uneven_emancipation, mid_pendulum_contraction, or coercive_caste_lock_in).
3. Classify ~150-year pendulum regime. Apply Reading 2 (emancipatory_crest, post_reform_plateau, mid_pendulum_trough, or pre_reform_bottleneck).
4. Classify labor regime tier. Apply Reading 3 (free_contractual_mobility, precarious_informality, externalized_coercion_creep, or systemic_unfree_bondage).
5. Classify state. Evaluate in strict priority order (COERCIVE_CASTE_LOCK_IN → MID_PENDULUM_CONTRACTION → UNEVEN_EMANCIPATION_DRIFT → PLURALIST_EXPANSION_NODE) and select the first matching state (fallback: UNEVEN_EMANCIPATION_DRIFT).
6. Apply persistence test. If contraction_trough_quarters >= 8, halve delta_cap.
7. Cap delta. Let delta_cap be the value from steps 5–6. If the state is COERCIVE_CASTE_LOCK_IN, set delta = 0.0 and action = "FLAT" regardless of AGOP. Otherwise, if intended delta exceeds delta_cap, reduce it to delta_cap.
8. Cite. If the cap bound (intended delta > delta_cap) or the state is COERCIVE_CASTE_LOCK_IN, cite "civic-emancipation-pendulum-yardstick" in skills_cited and state the pillar alignment, KAIROS ~150-year pendulum phase, and labor-regime finding in the rationale.

The Output Format

Your response must be a single JSON object. Do not include prose outside the object. The object has exactly five fields, in this order:
json
{"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}
Use code with caution.
• action: "LONG", "FLAT", or "SHORT". Must appear in the AGOP ranking or be "FLAT" (Invariant I1). If COERCIVE_CASTE_LOCK_IN, action must be "FLAT".
• delta: floating-point number in [0.0, 1.0].
• confidence: floating-point number in [0.0, 1.0].
• rationale: free-form string naming the state, four-pillar reading, and ~150-year pendulum phase. Example: "MID_PENDULUM_CONTRACTION state; working_class_bargaining=0.28 and minority_pluralism=0.34 in mid_pendulum_trough (178 deg, slope=-0.21) for 10 quarters; delta capped at 0.125; civic-emancipation-pendulum-yardstick."
• skills_cited: list of skill names; include "civic-emancipation-pendulum-yardstick" only when the cap bound or the state is COERCIVE_CASTE_LOCK_IN.

Worked Examples


Case A — Broad civic incorporation on an expansion node, cap does not bind

Snapshot:
• unfree_labor_and_coercion_index = 0.08
• womens_civic_participation_index = 0.86
• working_class_bargaining_index = 0.78
• minority_pluralism_and_emancipation_index = 0.81
• kairos_pendulum_phase_deg = 14.0
• pendulum_velocity_slope = +0.09
• contraction_trough_quarters = 0
Readings:
• Pillar Alignment: coercion < 0.25, all three civic pillars ≥ 0.65 → broad_civic_incorporation
• Pendulum Regime: 14.0° (315°–45°) → emancipatory_crest
• Labor Regime: 0.08 < 0.20 → free_contractual_mobility
State: PLURALIST_EXPANSION_NODE, delta cap 1.0. Persistence: 0 → does not fire.
AGOP ranks LONG. LLM intended delta = 0.85. Cap 1.0 does not bind.
LLM returns delta = 0.85 and does not cite "civic-emancipation-pendulum-yardstick".

Case B — Mid-pendulum contraction trough with entrenched union and minority rollback, cap binds

Snapshot:
• unfree_labor_and_coercion_index = 0.44
• womens_civic_participation_index = 0.56
• working_class_bargaining_index = 0.27
• minority_pluralism_and_emancipation_index = 0.33
• kairos_pendulum_phase_deg = 182.0
• pendulum_velocity_slope = -0.22
• contraction_trough_quarters = 10
Readings:
• Pillar Alignment: two pillars < 0.40 (0.27, 0.33) → mid_pendulum_contraction
• Pendulum Regime: 182.0° (135°–225°) with negative slope → mid_pendulum_trough
• Labor Regime: 0.44 (0.40–0.65) → externalized_coercion_creep
State: MID_PENDULUM_CONTRACTION, delta cap 0.25.
Persistence: contraction_trough_quarters = 10 >= 8 → halve to 0.125.
AGOP ranks LONG. LLM intended delta = 0.70. Cap 0.125 binds.
LLM returns delta = 0.125, cites "civic-emancipation-pendulum-yardstick", and states in rationale: "MID_PENDULUM_CONTRACTION state; working_class_bargaining=0.27 and minority_pluralism=0.33 in mid_pendulum_trough (182 deg, slope=-0.22) entrenched for 10 quarters; delta capped at 0.125; civic-emancipation-pendulum-yardstick."

Free Data Sources

The fetcher populates snapshot.external_data["civic_emancipation_pendulum"] by routing free longitudinal human-rights, gender, labor, anti-slavery, and minority-inclusion registries through KAIROS (:8300) for ~150-year phase estimation (no paid subscription required):
• KAIROS Cyclic & Phase-Lag Engine (http://localhost:8300): Local starwalkerz/kairos service estimating the ~150-year harmonic phase angle (kairos_pendulum_phase_deg) and 10-year velocity slope (pendulum_velocity_slope) across multi-century civic series.
• V-Dem (Varieties of Democracy) Historical & Contemporary Dataset (https://v-dem.net): Free 1789–present country-year indicators including Women's Political Empowerment (v2x_gender), Freedom from Forced Labor (v2clslavef / v2clslavem), Equal Protection & Equal Access across social groups (v2xeg_eqprotec, v2xeg_eqaccess), Civil Society Participation (v2x_cspart), and Exclusion by Socio-Economic Group (v2xpe_exlecon).
• ILOSTAT & OECD/AIAS ICTWSS Database (https://ilo.org and https://oecd.org): Free global series on trade-union density (ILR_TUMT_NOC_RT), collective bargaining coverage (ILR_CBCT_NOC_RT), labor rights compliance, and forced-labor/child-labor incidence.
• Walk Free Global Slavery Index (GSI) & U.S. DOL / State TIP Open Reports (https://walkfree.org and https://dol.gov): Free country-level prevalence estimates of modern slavery, debt bondage, and supply-chain forced-labor risk.
• World Bank Women, Business and the Law (WBL) & WDI (https://worldbank.org and https://worldbank.org): Free APIs tracking statutory gender parity across mobility, workplace, pay, marriage, parenthood, entrepreneurship, assets, and pension laws (1970–present).
• Clio Infra & Maddison Historical Labour/Guild Series (https://clio-infra.eu): Free multi-century historical datasets covering real wages, guild/union formation, educational attainment (Bildung / mass literacy), and colonial/postcolonial institutional transitions.
• World Values Survey (WVS) & European Social Survey (ESS) (https://worldvaluessurvey.org and https://europeansocialsurvey.org): Free longitudinal microdata on emancipative values, gender-role norms, class solidarity, and tolerance toward religious/ethnic minorities.
• Ethnic Power Relations (EPR) & Pew Government Restrictions on Religion Index (https://ethz.ch and https://pewresearch.org): Free datasets measuring minority access to executive/civic power, postcolonial self-determination, and state restrictions on religious practice.

Do Not

• Do not invent a directional action outside allowed_actions or "FLAT" (Invariant I1).
• Do not raise delta above the strategy cap or above 1.0 (Invariant I5).
• Do not treat formal statutory abolition on paper as broad_civic_incorporation if unfree_labor_and_coercion_index remains elevated via debt bondage, prison/conscript labor, or offshore supply-chain externalization.
• Do not compute precise floating-point arithmetic; use the qualitative comparison tables.
• Do not cite "civic-emancipation-pendulum-yardstick" when the cap did not bind and the state is not COERCIVE_CASTE_LOCK_IN.

Citation Mapping

• Double Movement & Labor Commodification: Karl Polanyi, The Great Transformation: The Political and Economic Origins of Our Time (Farrar & Rinehart, 1944). Grounding the recurring oscillation between coercive/laissez-faire labor disembedding and protective civic/union/welfare re-embedding.
• Abolition-Democracy & Mid-Cycle Counter-Revolution: W. E. B. Du Bois, Black Reconstruction in America (Harcourt, Brace, 1935); Eric Foner, Reconstruction: America's Unfinished Revolution (Harper & Row, 1988). Establishing the ~1860s–1870s emancipation crest followed by the early-1900s Jim Crow and oligarchic contraction trough.
• Labor-Repressive vs. Civic-Incorporating Modernization: Barrington Moore Jr., Social Origins of Dictatorship and Democracy: Lord and Peasant in the Making of the Modern World (Beacon Press, 1966). Anchoring the structural divergence between serf/peasant emancipation (1861 Russia, Prussian Bildung/welfare, Tanzimat, late-Qing reforms) and coercive landlord/cartel lock-in.
• Backlash Cycles & Counter-Emancipatory Waves: Albert O. Hirschman, The Rhetoric of Reaction: Perversity, Futility, Jeopardy (Harvard University Press, 1991). Formalizing the mid-pendulum contraction phase (~75-year offset) following major civic expansion waves.
• Sequencing of Civil, Political & Social Citizenship: T. H. Marshall, Citizenship and Social Class (Cambridge University Press, 1950). Grounding the four-pillar integration of free labor, working-class bargaining, women's civic participation, and minority equal protection.
• Bounded Algedonic Authority: Stafford Beer, Brain of the Firm (1972); Ramadge and Wonham, Supervisory Control of a Class of Discrete-Event Processes (1987). Downward-only damping within JANUS invariants I1–I9.