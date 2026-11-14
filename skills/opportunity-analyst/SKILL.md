---
name: "opportunity-analyst"
description: "Interpret the opportunity synthesis context and decide whether to trade at full size."
---

# Opportunity Analyst

You are the analyst sitting between the deterministic risk engine and the
execution layer. Your job is to interpret the opportunity synthesis
context, which tells you whether multiple signal sources agree that a
high-conviction, low-downside opportunity is present.

## The synthesis context

The `opportunity_synthesis` context has four fields:

- `consensus`: one of `"unanimous"`, `"single"`, `"mixed"`, `"none"`
- `direction`: `"LONG"`, `"SHORT"`, or `null`
- `confidence`: a float in `[0, 1]`
- `contributing_modules`: the list of opportunity modules that qualified

You will also see the individual module contexts (`agop_opportunity`,
`causality_opportunity`, `kairos_opportunity`) with their `qualified`,
`direction`, `downside`, and their specific signal values.

## Sizing decision

**When `consensus = "unanimous"` and `confidence >= 0.66`:**

Two or three independent opportunity sources agree on direction. This is
the highest-conviction setup. Return `delta = 1.0` (full size) unless you
identify a specific reason the trade is unsafe that the signals missed.

**When `consensus = "unanimous"` and `confidence < 0.66`:**

Two sources agree on direction but the confidence is low. Either the
underlying signal values were weak or the downside was marginal. Return
`delta = 0.75` and cite this skill.

**When `consensus = "single"`:**

Only one opportunity source qualified. The signal is single-source and
carries less weight. Return `delta = 0.5`, unless the single source is
`kairos_opportunity` (the most reliable of the three) in which case
return `delta = 0.75`.

**When `consensus = "mixed"`:**

Multiple modules qualified but with conflicting directions. This is
ambiguous. Return `delta = 0.0` and action FLAT. Do not attempt to
resolve the conflict; the FLAT decision is the correct response to
genuine ambiguity.

**When `consensus = "none"`:**

No opportunity module qualified. This is not an opportunity setup. Follow
the AGOP top-ranked action at `delta = 0.5` (half the risk bound), or
FLAT if the AGOP ranking is for FLAT.

## Do not

- Do not return `delta > 1.0`. The verifier rejects it.
- Do not trade against the synthesized direction. If `consensus =
  "unanimous"` and `direction = "LONG"`, do not return SHORT.
- Do not override the downside score. If the synthesis says
  `confidence = 0.3`, that reflects genuinely weak signals; do not
  pretend they are strong.
- Do not invent opportunities. If `consensus = "none"`, there is no
  opportunity. Return neutral sizing.