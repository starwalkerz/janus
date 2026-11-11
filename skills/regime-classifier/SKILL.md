---
name: "regime-classifier"
description: "Classify the current market regime from the KAIROS and Causalitybot reports."
---

# Regime Classifier

The KAIROS report tells you whether the current bar departs from the declared
cycle. The Causalitybot signal tells you whether the order book is showing a
causal horizon or a bottleneck.

## Procedure

1. If `kairos.flagged` is true and `kairos.amplitude` exceeds 0.10, the regime
   is `anomalous`. Under `anomalous`, prefer `FLAT` unless the AGOP ranking
   is unanimous.
2. If `causality.horizon` exceeds 0.6 and `causality.bottleneck` exceeds 0.5,
   the regime is `trending`. Under `trending`, the top-ranked action is
   acceptable at full `delta`.
3. Otherwise the regime is `neutral`. Accept the top-ranked action at
   `delta = 0.5`.

## Do not

- Do not raise `delta` above 1.0. It is a multiplier, not an absolute size.