---
name: "civilizational-cycle"
description: "Classify the current tick into one of four civilizational phases (Spring, Summer, Autumn, Winter) using Polybius' anacyclosis, Spengler's seasonal morphology, Machiavelli's fortuna-virtù dyad, and Ibn Khaldun's asabiyyah cycle, and cap delta accordingly."
---

# Civilizational Cycle

You are reading the tick as a polity in a cyclical phase. Polybius
described the anacyclosis as an invariable sequence: kingship decays
into tyranny, aristocracy into oligarchy, democracy into mob rule, and
the cycle begins again. Spengler described cultures as organisms with
four seasons: spring (birth of a worldview), summer (ripening of its
forms), autumn (hardening into civilization), winter (dissolution).
Machiavelli described the political life as a contest between fortuna
(the exogenous shock, the opportunity, the river in flood) and virtù
(the capacity to build dams and channels before the flood arrives).
Ibn Khaldun described dynasties as rising on asabiyyah (group
cohesion), maturing into luxury, and dissolving into senility across
roughly four generations.

Your job is to classify the current tick into one of four phases and
cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits.

## The four readings

Compute four readings from the snapshot and from the module contexts
you were given. Use the qualitative thresholds below. Do not attempt
precise arithmetic; use the comparisons.

### Reading 1 — Virtù (edge)

The signal-to-noise ratio is `|expected_return| / realized_volatility`.
Read it as the available virtù: the capacity of the current move to
impose form on fortuna.

| Range | Reading |
|---|---|
| ≥ 1.0 | **high** — ample capacity |
| 0.3 to 1.0 | **moderate** — capacity with thin margin |
| < 0.3 | **low** — capacity below the cost of exercising it |

### Reading 2 — Fortuna (feedback)

Two signals together determine whether fortune is favorable or
adverse, and whether the polity is cohesive enough to exploit it.

Compare the sign of `order_flow_imbalance` to the sign of
`expected_return`:

| Order flow | Reading |
|---|---|
| Same sign as expected_return, magnitude ≥ 0.3 | **favorable** |
| Same sign, magnitude < 0.3 | **mildly favorable** |
| Opposite sign | **adverse** |

Then read `signal_agreement` as a proxy for asabiyyah (cohesion):

| Range | Reading |
|---|---|
| > 0.5 | **cohesive** |
| -0.5 to 0.5 | **fractured** |
| < -0.5 | **dissolute** |

The pair (fortune, cohesion) defines the fortuna reading:

| Pair | Fortuna |
|---|---|
| favorable + cohesive | **triumphant** |
| favorable + fractured | **opportunistic** |
| mildly favorable + cohesive | **favorable** |
| adverse + any | **adverse** |
| any + dissolute | **adverse** |

### Reading 3 — Depletion (cycle position)

Compare the mean of the first half of `history` to the mean of the
second half. Compute a rough direction:

| History shape | Cycle position |
|---|---|
| Second-half mean well above first-half mean | **spring** (rising) |
| Means roughly equal | **summer** (peak) |
| Second-half mean well below first-half mean | **autumn** or **winter** (descending) |

If `history` has fewer than 8 samples, treat as **summer**.

Distinguish autumn from winter with Reading 4.

### Reading 4 — Corruption (environment)

Two quantities together determine the degree of institutional
corruption, following Machiavelli's account of the decay of the
republican order.

Read `venue_risk`:

| Range | Reading |
|---|---|
| < 0.3 | **sound** |
| 0.3 to 0.6 | **strained** |
| > 0.6 | **corrupt** |

Read `slippage / slippage_maximum`:

| Range | Reading |
|---|---|
| < 0.1 | **cheap** |
| 0.1 to 0.3 | **moderate** |
| > 0.3 | **expensive** |

The pair defines the corruption reading:

| Pair | Corruption |
|---|---|
| sound + cheap | **republican** |
| sound or strained venue, cheap or moderate slippage | **mixed** |
| corrupt OR expensive slippage | **decayed** |
| corrupt AND expensive slippage | **senile** |

## The phase taxonomy

Combine the four readings into one of four phases.

### SPRING

All of the following hold:

- Virtù reading: **high**
- Fortuna: **triumphant** or **favorable**
- Cycle position: **spring**
- Corruption: **republican**

**Delta cap: 1.0.** The polity is in its founding season. Virtù is
ample, fortune is favorable, cohesion is high, institutions are sound.
Accept the AGOP top-ranked action at full bound.

### SUMMER

All of the following hold:

- Virtù reading: **high** or **moderate**
- Fortuna: **favorable** or **opportunistic**
- Cycle position: **spring** or **summer**
- Corruption: **republican** or **mixed**

**Delta cap: 0.75.** The polity has ripened. The forms are mature, the
edge is still present, but the first signs of institutional strain
have appeared. Reduce size relative to SPRING.

### AUTUMN

Any of the following hold:

- Fortuna: **adverse** while the cycle position is still **spring**
  or **summer**
- Virtù reading: **low** while the cycle position is **summer**
- Corruption: **decayed** while the cycle position is **summer**

**Delta cap: 0.25.** The polity has hardened into civilization. The
forms are rigid, the edge is thinning, fortune is turning. Reduce
substantially. This is Spengler's autumn: the forms still function,
but the creative capacity has passed.

### WINTER

Any of the following hold:

- Cycle position: **autumn** or **winter** AND Virtù reading: **low**
- Cycle position: **autumn** or **winter** AND Corruption: **decayed**
  or **senile**
- Corruption: **senile** AND Fortuna: **adverse**

**Delta cap: 0.10.** The polity is in dissolution. The asabiyyah has
dissolved, the institutions are senile, fortune is adverse. Trade only
if the AGOP ranking is unambiguously directional and the LLM's
rationale is very strong. In most cases, return FLAT.

## The irreversibility test (Polybius)

Before applying the delta cap, ask one additional question: is the
move reversible?

A move is **irreversible** if the cycle position is **autumn** or
**winter** or if the corruption reading is **senile**. In these
states, the anacyclosis has turned; a mistake is not recoverable
within the tick horizon; the entropy of the polity has been spent.

A move is **reversible** otherwise.

If the move is **irreversible**, halve the delta cap. A SPRING cap of
1.0 becomes 0.5. A SUMMER cap of 0.75 becomes 0.375. An AUTUMN cap of
0.25 becomes 0.125. A WINTER cap of 0.10 becomes 0.05.

The irreversibility test is the last filter. It cannot raise the cap;
it can only lower it.

## The procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read virtù.** From `snapshot.expected_return` and
   `snapshot.realized_volatility`, compute the signal-to-noise ratio
   using the qualitative thresholds in Reading 1. Record one of:
   `high`, `moderate`, `low`.

2. **Read fortuna.** From `snapshot.order_flow_imbalance` and
   `snapshot.signal_agreement`, classify the fortuna as `triumphant`,
   `favorable`, `opportunistic`, or `adverse`. Record the pair.

3. **Read cycle position.** From `snapshot.history`, classify the
   cycle position as `spring`, `summer`, or `descending`.

4. **Read corruption.** From `snapshot.venue_risk` and the ratio
   `snapshot.slippage / snapshot.slippage_maximum`, classify as
   `republican`, `mixed`, `decayed`, or `senile`.

5. **Distinguish autumn from winter.** If the cycle position is
   `descending`, apply Reading 4: `decayed` or `senile` corruption
   makes it **winter**; `republican` or `mixed` corruption makes it
   **autumn**.

6. **Classify phase.** Apply the taxonomy above. Record one of:
   `SPRING`, `SUMMER`, `AUTUMN`, `WINTER`.

7. **Apply irreversibility test.** If the cycle position is `autumn`
   or `winter`, or corruption is `senile`, halve the phase's delta
   cap.

8. **Cap delta.** Let `delta_cap` be the value from steps 6–7. If
   your intended `delta` exceeds `delta_cap`, reduce it to
   `delta_cap`. Record the final `delta`.

9. **Cite.** If the cap bound (i.e., your intended delta was above
   the cap), cite `civilizational-cycle` in your rationale and state
   the phase.

## The output format

Your response must be a single JSON object. Do not include prose
outside the object. The object has exactly five fields, in this order:

    {"action": "LONG", "delta": 0.5, "confidence": 0.75, "rationale": "Brief justification citing applicable skills.", "skills_cited": ["skill-name"]}

The fields:

- `action`: a string. One of "LONG", "FLAT", "SHORT". Must appear in
  the AGOP ranking or be "FLAT". Invariant I1 enforces this
  independently of anything you produce; a hallucinated action is
  replaced with FLAT by the verifier.

- `delta`: a floating-point number in [0.0, 1.0]. The final position
  size is `delta` multiplied by the risk engine's upper bound. The
  phase cap in this skill restricts `delta` further; it does not
  replace the risk bound.

- `confidence`: a floating-point number in [0.0, 1.0]. Reflects your
  confidence in the rationale, not the trade. The strategy's
  confidence floor (0.40 for OPPORTUNITY, 0.45 for AGGRESSIVE, 0.65
  for CONSERVATIVE) rejects responses below the threshold.

- `rationale`: a free-form string. Names the phase and the reason
  for any cap. Example: "WINTER phase; descending cycle; senile
  corruption; delta capped at 0.05 after irreversibility halving;
  civilizational-cycle."

- `skills_cited`: a list of skill names. Include
  "civilizational-cycle" only if the phase cap bound the delta.
  Include the skills that actually drove the choice otherwise.

## Worked example

Suppose the snapshot has:

- `expected_return` = 0.012
- `realized_volatility` = 0.010
- `order_flow_imbalance` = 0.45
- `signal_agreement` = 0.6
- `venue_risk` = 0.2
- `slippage` = 1.5, `slippage_maximum` = 20.0
- `history` trending upward over the last 64 samples

Readings:

- Virtù: 0.012 / 0.010 = 1.2 → **high**
- Fortuna: order flow same sign (positive), magnitude ≥ 0.3 →
  favorable; signal_agreement 0.6 → cohesive; pair =
  **triumphant**
- Cycle position: history rising → **spring**
- Corruption: venue_risk 0.2 → sound; slippage ratio 0.075 → cheap;
  pair = **republican**

Phase: all four conditions of SPRING met → **SPRING**, delta cap
1.0. Not irreversible. Cap is 1.0.

If AGOP ranks LONG and the LLM would otherwise have chosen delta 1.0,
the cap does not bind. The LLM returns delta 1.0, cites nothing from
this skill (the cap did not fire), and cites whichever skills drove
the directional choice.

If the same tick had `venue_risk` = 0.7 and `slippage` = 8.0
(ratio 0.4):

- Corruption: venue_risk high, slippage expensive → **senile**

Phase: SPRING requires republican corruption; senile fails that
condition. If the cycle position is still rising but corruption is
senile, the phase is not SPRING. Check AUTUMN: corruption decayed
while cycle position summer → requires summer. Since position is
rising, not summer, and fortuna is triumphant, the phase is
AMBIGUOUS? No, the taxonomy has no AMBIGUOUS phase. AUTUMN requires
corruption decayed while position summer; not met. WINTER requires
descending position and senile corruption; position is rising, so not
winter. The correct classification is that the readings are
inconsistent with any phase. In this case, treat as WINTER because
senile corruption combined with any fortuna is the collapse signature
that trumps the rising price. Record **WINTER**, delta cap 0.10.
Irreversibility: corruption senile → halve to 0.05.

If AGOP ranks LONG and the LLM intended delta 0.75, the cap binds.
The LLM reduces to 0.05, cites `civilizational-cycle`, and states:
"WINTER phase; senile corruption with rising price; delta capped at
0.05 after irreversibility halving; civilizational-cycle."

## Do not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a
  replacement for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it. If the LLM intended a
  delta below the phase cap, do not raise it to the cap.

- Do not treat "SPRING" as a reason to increase size beyond the
  strategy cap. The strategy cap is the binding constraint. The
  SPRING phase means the AGOP-selected action is worth taking at the
  bound the strategy already permits.

- Do not compute precise arithmetic on any of the readings. The
  thresholds are qualitative. A 7B model cannot reliably divide
  small floats; use the comparison tables.

- Do not re-classify on the same tick. The phase is a deterministic
  function of the readings. If your first classification was
  WINTER, it stays WINTER. Do not push it to SPRING by preferring
  one reading over another.

- Do not cite this skill when the cap did not bind. If your intended
  delta was already at or below the cap, this skill did not change
  your decision, and it should not appear in `skills_cited`. Cite
  the skills that actually drove the choice.

## Citation mapping

- **Virtù thresholds (Reading 1)**: Machiavelli, *The Prince* (1513)
  and *Discourses on Livy* (1517). Virtù is the capacity to impose
  form on fortuna; it is measurable as the ratio of the return to
  the risk incurred in pursuing it.

- **Fortuna and asabiyyah (Reading 2)**: Machiavelli, *The Prince*
  (1513); Ibn Khaldun, *Muqaddimah* (1377). Fortuna is the exogenous
  shock; asabiyyah is the cohesion that determines whether the shock
  is exploited or absorbed.

- **Cycle position (Reading 3)**: Polybius, *Histories* Book VI
  (c. 150 BCE); Spengler, *The Decline of the West* (1918–1922).
  The anacyclosis is the political cycle; the seasonal morphology is
  the cultural cycle. Both rise, peak, and descend.

- **Corruption reading (Reading 4)**: Machiavelli, *Discourses on
  Livy* (1517). The decay of the republican order is the decay of
  the institutional friction that keeps virtù and fortuna in
  balance.

- **Irreversibility test**: Polybius, *Histories* Book VI (c. 150
  BCE); Spengler, *The Decline of the West* (1918–1922). Once the
  anacyclosis has turned, the descent is not recoverable within the
  cycle.

- **Phase taxonomy**: Spengler, *The Decline of the West* (1918–1922);
  Vico, *The New Science* (1725). The four seasons of a culture and
  the corsi e ricorsi are the canonical phase divisions.

- **Delta cap on SPRING**: Polybius, *Histories* Book VI (c. 150
  BCE). The polity in its spring has maximum capacity; size to the
  capacity, not above it.

- **Bounded authority**: Ibn Khaldun, *Muqaddimah* (1377). The
  asabiyyah is a homeostatic variable; the ruler who exceeds it
  accelerates the dynasty's decay. This skill is the algedonic
  channel for the civilizational phase.