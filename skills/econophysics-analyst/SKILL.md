---
name: "econophysics-analyst"
description: "Interpret the quantum econophysics reports from Baaquie tunneling and Ising herding."
---

# Econophysics Analyst

You receive two quantum-derived reports per tick: a tunneling probability
from the Baaquie potential-well circuit, and a magnetization order parameter
from the Ising QAOA circuit. Interpret them together.

## Tunneling

The tunneling probability `P_tunnel` is the probability that the price,
starting at its current level, ends the evolution window strictly beyond
the nearest heavy-volume barrier. High `P_tunnel` means the barrier is
porous — the wall is likely to break. Low `P_tunnel` means the wall is
likely to hold.

- `P_tunnel > 0.6` and `direction = "up"` — the resistance is fragile.
  Accept a LONG at higher `delta` if the AGOP ranking agrees.
- `P_tunnel > 0.6` and `direction = "down"` — the support is fragile.
  Accept a SHORT at higher `delta` if the AGOP ranking agrees.
- `P_tunnel < 0.2` — the barrier is solid. Treat the direction as
  rejected unless the AGOP top-ranked action points the other way.

## Herding

The magnetization `|M|` is the magnitude of the mean spin alignment
across the asset correlation graph. `|M|` close to one means the market
is in a ferromagnetic herding phase: a fragile, overcrowded consensus.
`|M|` close to zero means the market is disordered.

- `|M| > 0.7` — herding phase. Reduce `delta` by half even if the
  regime classifier says trending. Herding phases resolve violently.
- `|M| < 0.3` — disordered phase. No herding adjustment.
- The `signed_magnetization` field indicates direction: positive is
  bullish consensus, negative is bearish.

## Combining the two

- Fragile barrier plus strong herding in the same direction is a **crowded
  breakout**. Reduce size — the breakout is likely to reverse on the first
  adverse print.
- Solid barrier plus strong herding toward the barrier is a **crowded
  rejection**. Reduce size — the wall is likely to hold and the crowd is
  on the wrong side.
- Fragile barrier plus low herding is the **clean case**. Accept the AGOP
  top-ranked action at the full risk bound.
- Solid barrier plus low herding is the **no-trade case**. Return FLAT.

## Do not

- Do not compute your own tunneling probability. The value reported is
  from a quantum circuit; trust the number.
- Do not ignore the `backend` field. If it says `classical-exact`, the
  result is exact but the quantum hardware was not used; this is a
  deployment detail, not a signal-quality issue.
- Do not raise `delta` above 1.0. The verifier will reject it.