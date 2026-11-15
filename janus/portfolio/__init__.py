"""janus.portfolio — ticker registry and portfolio calendar for Janus.

This package lives inside the existing ``janus`` package, so it is imported
as ``janus.portfolio.*``. It is structurally analogous to ``janus.stirpes``.

The subsystem operates on two user-supplied data folders:

- ``tickers/`` classifies tickers by three orthogonal axes (geography,
  sector, commodity). A ticker's classification is an *intersection*.
- ``calendar/`` records, per Gregorian year and quarter, which intersections
  are favored or dampened.

Circular-import warning
-----------------------
This package must **not** be imported at package level from
``janus/__init__.py``. Doing so would cause a circular import:
``janus/__init__.py`` → ``janus.portfolio`` → ``janus.portfolio.portfolio_calendar``
→ ``janus.contracts`` → ``janus/__init__.py``. The module is registered via
``Config.module_imports``, which imports it lazily.

Public surface
--------------
From ``janus.portfolio.tickers``:
    ``GEOGRAPHY_VALUES``, ``SECTOR_VALUES``, ``COMMODITY_VALUES``,
    ``AXIS_VALUES`` — the allowed values for each axis.
    ``Intersection`` — frozen triple ``(geography, sector, commodity)``.
    ``load_tickers`` — parse a tickers folder or file into a registry.
    ``build_reverse_index`` — invert the registry to symbol → intersections.

From ``janus.portfolio.calendar``:
    ``EFFECTS`` — the eight effect tokens.
    ``CalendarEntry`` — frozen record of one calendar line.
    ``load_calendar`` — parse a calendar folder or file into a list.
    ``entries_for_quarter`` — filter to a year/quarter.
    ``matches`` — check whether an entry's pattern matches an intersection.

The module class is not re-exported here. Import directly::

    from janus.portfolio.portfolio_calendar import PortfolioCalendarModule
"""

from __future__ import annotations

from janus.portfolio.calendar import (
    EFFECTS,
    CalendarEntry,
    entries_for_quarter,
    load_calendar,
    matches,
)
from janus.portfolio.tickers import (
    AXIS_VALUES,
    COMMODITY_VALUES,
    GEOGRAPHY_VALUES,
    Intersection,
    SECTOR_VALUES,
    build_reverse_index,
    load_tickers,
)

__all__: list[str] = [
    "AXIS_VALUES",
    "COMMODITY_VALUES",
    "CalendarEntry",
    "EFFECTS",
    "GEOGRAPHY_VALUES",
    "Intersection",
    "SECTOR_VALUES",
    "build_reverse_index",
    "entries_for_quarter",
    "load_calendar",
    "load_tickers",
    "matches",
]