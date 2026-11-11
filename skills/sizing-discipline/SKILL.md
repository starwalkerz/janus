---
name: "sizing-discipline"
description: "Constrain the sizing decision to the risk engine's upper bound."
---

# Sizing Discipline

The risk engine returns `risk_bound`, the maximum size the strategy permits
for this tick. Your `delta` is a multiplier on that bound, not a replacement
for it.

## Procedure

1. If your confidence in the rationale is below 0.5, return `delta = 0.0`.
2. If your confidence is between 0.5 and 0.7, return `delta = 0.5`.
3. If your confidence exceeds 0.7 and the regime is `trending`, return
   `delta = 1.0`.
4. Otherwise return `delta = 0.75`.

## Do not

- Do not return a `delta` greater than 1.0. The verifier will reject it and
  the trade will be forced flat.