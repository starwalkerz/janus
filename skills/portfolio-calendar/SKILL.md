---
name: portfolio-calendar
description: Consult the ticker registry and calendar before sizing a trade. The registry classifies tickers by three orthogonal axes (geography, sector, commodity). The calendar records, per Gregorian year and quarter, which intersections are favored or dampened. The module resolves symbol → intersections → active entries and patches AGOP's axes.
---

# Portfolio Calendar

The portfolio has two data folders:

- **`tickers/`** — classifies tickers by three orthogonal axes (geography,
  sector, commodity). A ticker's classification is an *intersection* — a
  triple `(geography, sector, commodity)`.
- **`calendar/`** — records, per Gregorian year and quarter, which
  intersections are favored or dampened.

The deterministic `portfolio_calendar` module reads both folders on every
tick. It resolves the current symbol to its intersections, finds the active
calendar entries for the current Gregorian quarter, and patches AGOP's axes.

Before approving a trade, check whether the current date falls inside a
quarter that has active entries for the symbol's intersections. If it does,
weigh the entry's effect against the AGOP ranking and the risk bound. The
ticker registry and calendar are **context**, not a mandate.

## Reading the module's context

The module exposes active entries in `context["events"]`. Each entry is a
dict with keys `event_id`, `year`, `quarter`, `geography`, `sector`,
`commodity`, `effect`, and `source_file`.

`context["year"]`, `context["quarter"]`, and `context["intersections"]` are
also provided. `context["intersections"]` is a list of dicts with keys
`geography`, `sector`, `commodity`.

## Effects

| Effect | Meaning |
|---|---|
| `favor_long` | The calendar favors long exposure to this intersection. |
| `favor_short` | The calendar favors short exposure. |
| `dampen_all` | The calendar dampens both long and short. |
| `dampen_long` | The calendar dampens long exposure. |
| `dampen_short` | The calendar dampens short exposure. |
| `veto_long` | The calendar blocks long exposure. |
| `veto_short` | The calendar blocks short exposure. |
| `veto_all` | The calendar forces FLAT before intent construction. |

## Wildcards

A calendar entry may use `*` on any axis. A wildcard matches any value on
that axis. For example, `us | energy | *` matches every commodity under
`us | energy`. The module checks whether the entry's pattern matches any of
the symbol's intersections.

## How to cite

Cite `portfolio-calendar` in `skills_cited` and name the event ID, axes, and
source file in the rationale. Examples:

> "Entry `uranium_2027q1` (us, nuclear, uranium; from `calendar.txt`) is
> active in 2027Q1; AGOP ranks LONG first; calendar favors accumulation."

> "Entry `fusion_2028q3` (multi, fusion, none; from `calendar.txt`) is
> active in 2028Q3; AGOP ranks LONG first; calendar dampens longs."

When the calendar has no active entries for the symbol, do not cite it. Do
not invent events. Read them from `context["events"]`.