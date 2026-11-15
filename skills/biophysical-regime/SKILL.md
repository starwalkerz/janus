---
name: "biophysical-regime"
description: "Classify the current biophysical regime and cap delta accordingly, using EROI-like edge, feedback-loop reading, depletion-curve position, and throughput bounds."
---

# Biophysical Regime

You are reading the tick as a biophysical system. The available edge is
a low-entropy resource. The market's feedback loops determine whether
that edge is being amplified or dissipated. The depletion curve tells
you whether you are on the rising limb, the peak, or the descending
limb. The execution environment tells you whether you are operating
within throughput bounds or beyond them.

Your job is to classify the current tick into one of five regimes and
cap your `delta` accordingly. You do not invent trades. You do not
override AGOP. You modulate the LLM's delta within the bound the
verifier already permits.

## The four readings

Compute four readings from the snapshot and from the module contexts
you were given. Use the qualitative thresholds below. Do not attempt
precise arithmetic; use the comparisons.

### Reading 1 — Edge (EROI proxy)

The signal-to-noise ratio is `|expected_return| / realized_volatility`.
Read it as the EROI of the current move: how much energy is returned
per unit of risk energy expended.

| Range | Reading |
|---|---|
| ≥ 1.0 | **high** — edge comfortably exceeds risk |
| 0.3 to 1.0 | **moderate** — edge covers risk with thin margin |
| < 0.3 | **low** — edge is below the cost of carrying it |

### Reading 2 — Feedback (Meadows / Forrester)

Two signals together determine whether the current move is being
amplified by a reinforcing loop or damped by a balancing loop.

Compare the sign of `order_flow_imbalance` to the sign of
`expected_return`:

| Order flow | Reading |
|---|---|
| Same sign as expected_return, magnitude ≥ 0.3 | **reinforcing** |
| Same sign, magnitude < 0.3 | **mildly reinforcing** |
| Opposite sign | **balancing** |

Then read `signal_agreement`:

| Range | Reading |
|---|---|
| > 0.5 | **agreement** |
| -0.5 to 0.5 | **mixed** |
| < -0.5 | **disagreement** |

The pair (order flow, agreement) defines the loop reading:

| Pair | Loop |
|---|---|
| reinforcing + agreement | **runaway reinforcing** |
| reinforcing + mixed | **reinforcing** |
| mildly reinforcing + agreement | **reinforcing** |
| balancing + any | **balancing** |
| any + disagreement | **balancing** |

### Reading 3 — Depletion (Hubbert)

Compare the mean of the first half of `history` to the mean of the
second half. Compute a rough direction:

| History shape | Curve position |
|---|---|
| Second-half mean well above first-half mean | **rising limb** |
| Means roughly equal | **peak** |
| Second-half mean well below first-half mean | **descending limb** |

If `history` has fewer than 8 samples, treat as **peak**.

### Reading 4 — Environment (Daly / Beer)

Two quantities together determine whether you are within throughput
bounds.

Read `venue_risk`:

| Range | Reading |
|---|---|
| < 0.3 | **low** |
| 0.3 to 0.6 | **moderate** |
| > 0.6 | **high** |

Read `slippage / slippage_maximum`:

| Range | Reading |
|---|---|
| < 0.1 | **cheap** |
| 0.1 to 0.3 | **moderate** |
| > 0.3 | **expensive** |

The pair defines the environment:

| Pair | Environment |
|---|---|
| low + cheap | **within bounds** |
| low or moderate venue, cheap or moderate slippage | **near bounds** |
| high venue OR expensive slippage | **beyond bounds** |
| high venue AND expensive slippage | **far beyond bounds** |

## The regime taxonomy

Combine the four readings into one of five regimes.

### EXPANDING

All of the following hold:

- Edge reading: **high**
- Loop: **runaway reinforcing** or **reinforcing**
- Curve: **rising limb**
- Environment: **within bounds**

**Delta cap: 1.0.** The system is in maximum-power flow. The edge is
genuine, the loop is amplifying, the curve is rising, the environment
is benign. Accept the AGOP top-ranked action at full bound.

### MATURE

All of the following hold:

- Edge reading: **high** or **moderate**
- Loop: **reinforcing** or **mildly reinforcing**
- Curve: **rising limb** or **peak**
- Environment: **within bounds** or **near bounds**

**Delta cap: 0.75.** The system is still productive but no longer in
runaway expansion. The curve is flattening or near the peak. Reduce
size relative to the EXPANDING case.

### OVERSHOOT

Any of the following hold:

- Loop: **balancing** while the curve is still **rising limb**
- Edge reading: **low** while the curve is **rising limb**
- Environment: **beyond bounds** while the curve is **peak**

**Delta cap: 0.25.** The system is being asked to consume more than it
produces. The balancing loop has started. Reduce substantially.

### CONTRACTING

Any of the following hold:

- Curve: **descending limb** AND Edge reading: **low**
- Curve: **descending limb** AND Environment: **beyond bounds** or
  **far beyond bounds**
- Environment: **far beyond bounds** AND Loop: **balancing**

**Delta cap: 0.10.** The entropy has been spent. The system is in
throughput contraction. Trade only if the AGOP ranking is unambiguously
directional and the LLM's rationale is very strong. In most cases,
return FLAT.

### AMBIGUOUS

Everything that does not satisfy the above conditions.

**Delta cap: 0.50.** The readings conflict. Treat with the same
caution as the sizing-discipline skill's "moderate confidence" tier.

## The irreversibility test (Georgescu-Roegen)

Before applying the delta cap, ask one additional question: is the
move reversible?

A move is **irreversible** if the curve reading is **descending limb**
or if the environment reading is **far beyond bounds**. In these
states, a mistake is not recoverable within the tick horizon; the
entropy has been spent.

A move is **reversible** otherwise.

If the move is **irreversible**, halve the delta cap. An EXPANDING cap
of 1.0 becomes 0.5. A MATURE cap of 0.75 becomes 0.375. An OVERSHOOT
cap of 0.25 becomes 0.125. A CONTRACTING cap of 0.10 becomes 0.05.

The irreversibility test is the last filter. It cannot raise the cap;
it can only lower it.

## The procedure

Execute this procedure on every tick. Do not skip steps.

1. **Read edge.** From `snapshot.expected_return` and
   `snapshot.realized_volatility`, compute the signal-to-noise ratio
   using the qualitative thresholds in Reading 1. Record one of:
   `high`, `moderate`, `low`.

2. **Read loop.** From `snapshot.order_flow_imbalance` and
   `snapshot.signal_agreement`, classify the loop as `runaway
   reinforcing`, `reinforcing`, `mildly reinforcing`, or `balancing`.
   Record the pair.

3. **Read curve.** From `snapshot.history`, classify the curve position
   as `rising limb`, `peak`, or `descending limb`.

4. **Read environment.** From `snapshot.venue_risk` and the ratio
   `snapshot.slippage / snapshot.slippage_maximum`, classify as
   `within bounds`, `near bounds`, `beyond bounds`, or `far beyond
   bounds`.

5. **Classify regime.** Apply the taxonomy above. Record one of:
   `EXPANDING`, `MATURE`, `OVERSHOOT`, `CONTRACTING`, `AMBIGUOUS`.

6. **Apply irreversibility test.** If the curve is `descending limb`
   or the environment is `far beyond bounds`, halve the regime's
   delta cap.

7. **Cap delta.** Let `delta_cap` be the value from steps 5–6. If
   your intended `delta` exceeds `delta_cap`, reduce it to
   `delta_cap`. Record the final `delta`.

8. **Cite.** If the cap bound (i.e., your intended delta was above
   the cap), cite `biophysical-regime` in your rationale and state
   the regime.

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
  regime cap in this skill restricts `delta` further; it does not
  replace the risk bound.

- `confidence`: a floating-point number in [0.0, 1.0]. Reflects your
  confidence in the rationale, not the trade. The strategy's
  confidence floor (0.40 for OPPORTUNITY, 0.45 for AGGRESSIVE, 0.65
  for CONSERVATIVE) rejects responses below the threshold.

- `rationale`: a free-form string. Names the regime and the reason
  for any cap. Example: "OVERSHOOT regime; balancing loop with
  rising curve; environment far beyond bounds; delta capped at
  0.125 after irreversibility halving; biophysical-regime."

- `skills_cited`: a list of skill names. Include "biophysical-regime"
  only if the regime cap bound the delta. Include the skills that
  actually drove the choice otherwise.

If you applied a cap, the rationale names the regime and the reason.
Example: "EXPANDING regime; loop reinforcing; edge high; delta 1.0
accepted at AGOP bound." Or: "OVERSHOOT regime; balancing loop with
rising curve; delta capped at 0.25; biophysical-regime."

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

- Edge: 0.012 / 0.010 = 1.2 → **high**
- Loop: order flow same sign (positive), magnitude ≥ 0.3 → reinforcing;
  signal_agreement 0.6 → agreement; pair = **runaway reinforcing**
- Curve: history rising → **rising limb**
- Environment: venue_risk 0.2 → low; slippage ratio 0.075 → cheap;
  pair = **within bounds**

Regime: all four conditions of EXPANDING met → **EXPANDING**,
delta cap 1.0. Not irreversible. Cap is 1.0.

If AGOP ranks LONG and the LLM would otherwise have chosen delta 1.0,
the cap does not bind. The LLM returns delta 1.0, cites nothing from
this skill (the cap did not fire), and cites whichever skills drove
the directional choice.

If the same tick had `venue_risk` = 0.7 and `slippage` = 8.0
(ratio 0.4):

- Environment: venue_risk high, slippage expensive → **far beyond
  bounds**

Regime: EXPANDING requires within bounds; far beyond bounds fails
that condition. If loop is balancing instead, OVERSHOOT. If loop is
still reinforcing, check the other OVERSHOOT conditions. Suppose the
loop has flipped to balancing while history is still rising → the
classic overshoot signature. Regime = **OVERSHOOT**, delta cap 0.25.
Then irreversibility: environment far beyond bounds → halve.
Final delta cap: **0.125**.

If AGOP ranks LONG and the LLM intended delta 0.75, the cap binds.
The LLM reduces to 0.125, cites `biophysical-regime`, and states:
"OVERSHOOT regime; balancing loop with rising curve; environment far
beyond bounds; delta capped at 0.125 after irreversibility halving;
biophysical-regime."

## Do not

- Do not invent a directional action the AGOP ranking does not
  contain. Your action must be in `allowed_actions` or FLAT. This
  skill never overrides invariant I1.

- Do not exceed the risk engine's upper bound. The cap computed here
  is a further restriction on top of the risk bound, not a
  replacement for it. Invariant I5 still applies.

- Do not raise delta above the strategy cap. The cap here can only
  lower the final delta; it never raises it. If the LLM intended a
  delta below the regime cap, do not raise it to the cap.

- Do not treat "EXPANDING" as a reason to increase size beyond the
  strategy cap. The strategy cap is the binding constraint. The
  EXPANDING regime means the AGOP-selected action is worth taking at
  the bound the strategy already permits.

- Do not compute precise arithmetic on any of the readings. The
  thresholds are qualitative. A 7B model cannot reliably divide
  small floats; use the comparison tables.

- Do not re-classify on the same tick. The regime is a deterministic
  function of the readings. If your first classification was
  AMBIGUOUS, it stays AMBIGUOUS. Do not push it to EXPANDING by
  preferring one reading over another.

- Do not cite this skill when the cap did not bind. If your intended
  delta was already at or below the cap, this skill did not change
  your decision, and it should not appear in `skills_cited`. Cite
  the skills that actually drove the choice.

## Citation mapping

- **Edge thresholds (Reading 1)**: Hall, Cleveland & Kaufmann, *Energy
  and Resource Quality* (1986); Hall, *Energy Return on Investment*
  (2017). The EROI below which a resource cannot sustain its own
  extraction is the analogue of the signal-to-noise ratio below
  which a move cannot cover its execution cost.
- **Feedback loops (Reading 2)**: Forrester, *Industrial Dynamics*
  (1961); Meadows et al., *Limits to Growth* (1972). Reinforcing and
  balancing loops determine whether a signal is amplified or damped.
- **Depletion curve (Reading 3)**: Hubbert, "Nuclear Energy and the
  Fossil Fuels" (1956). The logistic curve rises, peaks, and
  descends; extrapolation is only safe on the rising limb.
- **Throughput bounds (Reading 4)**: Daly, *Steady-State Economics*
  (1977); Schumacher, *Small Is Beautiful* (1973). Activity beyond
  bounds consumes more than it produces.
- **Irreversibility test**: Georgescu-Roegen, *The Entropy Law and the
  Economic Process* (1971). Irreversible moves spend low-entropy
  capital; they cannot be recovered.
- **Maximum power principle (delta cap on EXPANDING)**: Odum,
  *Environment, Power, and Society* (1971). Size to the available
  flow, not above it.
- **Regime taxonomy**: Smil, *Energy and Civilization* (2017);
  Ayres & Warr, *The Economic Growth Engine* (2009). Regime
  transitions follow power-conversion and exergy-efficiency shifts,
  not smooth interpolations.
- **Bounded authority**: Beer, *Brain of the Firm* (1972). The VSM
  algedonic channel can flag a regime but cannot override the
  homeostatic bound.