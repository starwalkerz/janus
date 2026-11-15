# calendar/

Record, per Gregorian year and quarter, which intersections are favored or
dampened. The calendar does not know about tickers directly; it references
intersections (geography, sector, commodity). The module resolves
intersection → tickers via the ticker registry.

The calendar covers **2027 through 2046**. Each year is a section header
followed by its four quarters. Within each quarter, entries specify which
intersection gets which effect.

## File format

Each non-comment, non-blank line is either a section header or an entry.

**Section header:**

```
[<YYYY>Q<n>]
```

Where `YYYY` is a four-digit Gregorian year and `n` is `1` through `4`.

**Entry line:**

```
<geography> | <sector> | <commodity> | <effect> | <event_id>
```

- **geography**, **sector**, **commodity** — a specific axis value or `*` for
  wildcard.
- **effect** — one of the eight tokens below.
- **event_id** — non-empty identifier, used for LLM citation.

**Comments:** lines whose first non-whitespace character is `#`. Blank
lines are ignored.

## Effects

| Effect | `pain` | `readiness` | `barrier` | `veto` |
|---|---|---|---|---|
| `favor_long` | `LONG=0.85` | `LONG=0.85` | `LONG=0.15` | — |
| `favor_short` | `SHORT=0.85` | `SHORT=0.85` | `SHORT=0.15` | — |
| `dampen_all` | — | — | `LONG=0.85`, `SHORT=0.85` | — |
| `dampen_long` | — | — | `LONG=0.85` | — |
| `dampen_short` | — | — | `SHORT=0.85` | — |
| `veto_long` | `LONG=0.15` | `LONG=0.15` | `LONG=1.0` | — |
| `veto_short` | `SHORT=0.15` | `SHORT=0.15` | `SHORT=1.0` | — |
| `veto_all` | — | — | — | `True` |

## Wildcards

A wildcard `*` matches any value on that axis. Examples:

- `us | energy | *` — every commodity under `us | energy`.
- `us | * | oil` — every sector under `us` with commodity `oil`.
- `* | * | *` — every intersection.

## Example

```
[2027Q1]
us | nuclear | uranium | favor_long | uranium_2027q1
us | energy | oil | favor_long | oil_2027q1
* | fusion | none | favor_long | fusion_2027q1

[2027Q2]
us | nuclear | uranium | favor_long | uranium_2027q2
```

## Merge precedence

Within a quarter, if two entries patch the same `(axis, action)`, the later
entry in file order wins. Files are concatenated in lexicographic filename
order; within each file, entries are applied in line order.

## File discovery

- Regular files in this folder whose suffix is exactly `.txt`.
- Sorted lexicographically by filename.
- Subfolders and non-`.txt` files are ignored.

To disable a file without deleting it, rename it to `.txt.disabled`.

## Path resolution

Resolved on every tick:

1. `JANUS_PORTFOLIO_CALENDAR` environment variable (folder or file).
2. `configuration.portfolio_calendar_path` attribute, if set.
3. `calendar` in the current working directory.

## See also

The calendar references intersections defined by the ticker registry. See
[`tickers/README.md`](../tickers/README.md) for the ticker format and the
axis definitions.