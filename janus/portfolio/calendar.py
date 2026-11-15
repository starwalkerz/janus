"""janus.portfolio.calendar — calendar file parser.

The calendar records, per Gregorian year and quarter, which intersections
are favored or dampened. It does not know about tickers; it references
intersections by axis values (with optional wildcards).

Format, section-based:

    [<YYYY>Q<n>]
    <geography> | <sector> | <commodity> | <effect> | <event_id>
    <geography> | <sector> | <commodity> | <effect> | <event_id>
    ...

Lines whose first non-whitespace character is ``#`` are comments. Blank
lines are ignored. Any malformed line raises ``ValueError`` naming the
source file, the line number, and the offending token.

Axis fields in an entry may be a specific value from the axis or ``*`` for
wildcard. ``*`` matches any value on that axis.

Mathematical specification
--------------------------
Let ``F(D) = sorted([ f : f is a regular file in D, suffix(f) = ".txt" ])``.
Let ``E(D) = concat([ load_calendar(f) : f in F(D) ])``.

``entries_for_quarter(E, y, q)`` returns the subsequence of ``E`` whose
``year = y`` and ``quarter = q``.

``matches(e, i)`` is::

    (e.geography == "*" or e.geography == i.geography)
    and (e.sector == "*" or e.sector == i.sector)
    and (e.commodity == "*" or e.commodity == i.commodity)

which returns ``True`` iff the entry's pattern matches the intersection.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from janus.portfolio.tickers import (
    COMMODITY_VALUES,
    GEOGRAPHY_VALUES,
    SECTOR_VALUES,
    Intersection,
)

DEFAULT_CALENDAR_DIR: Final[Path] = Path("calendar")
CALENDAR_SUFFIX: Final[str] = ".txt"

EFFECTS: Final[frozenset[str]] = frozenset(
    {
        "favor_long",
        "favor_short",
        "dampen_all",
        "dampen_long",
        "dampen_short",
        "veto_long",
        "veto_short",
        "veto_all",
    }
)

_SECTION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^\[(\d{4})Q([1-4])\]$"
)


@dataclass(frozen=True)
class CalendarEntry:
    """One calendar line.

    Attributes
    ----------
    year, quarter
        Gregorian year and quarter. ``quarter`` is 1 through 4.
    geography, sector, commodity
        Pattern fields. Each is either a specific axis value or ``"*"``.
    effect
        One of the eight tokens in ``EFFECTS``.
    event_id
        Non-empty identifier, used for LLM citation.
    line_number
        1-based line number within the source file.
    source_file
        Basename of the source file.
    """

    year: int
    quarter: int
    geography: str
    sector: str
    commodity: str
    effect: str
    event_id: str
    line_number: int
    source_file: str


def _parse_section_header(
    line: str, source_file: str, line_number: int
) -> tuple[int, int]:
    """Parse a ``[YYYYQn]`` header into ``(year, quarter)``."""
    m = _SECTION_PATTERN.match(line.strip())
    if not m:
        raise ValueError(
            f"calendar {source_file} line {line_number}: "
            f"invalid section header {line!r}; "
            f"expected [<YYYY>Q<1-4>]"
        )
    year = int(m.group(1))
    quarter = int(m.group(2))
    return year, quarter


def _parse_axis_field(
    token: str,
    allowed: frozenset[str],
    axis_name: str,
    source_file: str,
    line_number: int,
) -> str:
    """Validate a calendar axis field. Wildcard ``*`` is allowed."""
    value = token.strip()
    if value == "*":
        return value
    if value not in allowed:
        raise ValueError(
            f"calendar {source_file} line {line_number}: "
            f"invalid {axis_name} {value!r}; "
            f"expected one of {sorted(allowed)} or '*'"
        )
    return value


def _parse_entry_line(
    line: str,
    year: int,
    quarter: int,
    source_file: str,
    line_number: int,
) -> CalendarEntry:
    """Parse a calendar entry line."""
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 5:
        raise ValueError(
            f"calendar {source_file} line {line_number}: "
            f"expected 5 pipe-separated fields, got {len(parts)}: {line!r}"
        )
    geography, sector, commodity, effect, event_id = parts

    geography = _parse_axis_field(
        geography, GEOGRAPHY_VALUES, "geography", source_file, line_number
    )
    sector = _parse_axis_field(
        sector, SECTOR_VALUES, "sector", source_file, line_number
    )
    commodity = _parse_axis_field(
        commodity, COMMODITY_VALUES, "commodity", source_file, line_number
    )

    effect = effect.strip().lower()
    if effect not in EFFECTS:
        raise ValueError(
            f"calendar {source_file} line {line_number}: "
            f"unknown effect {effect!r}; "
            f"expected one of {sorted(EFFECTS)}"
        )

    if not event_id:
        raise ValueError(
            f"calendar {source_file} line {line_number}: empty event ID"
        )

    return CalendarEntry(
        year=year,
        quarter=quarter,
        geography=geography,
        sector=sector,
        commodity=commodity,
        effect=effect,
        event_id=event_id,
        line_number=line_number,
        source_file=source_file,
    )


def _load_calendar_file(path: Path) -> list[CalendarEntry]:
    """Parse a single calendar file."""
    source_file = path.name
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"calendar {source_file}: not valid UTF-8: {exc}"
        ) from exc

    entries: list[CalendarEntry] = []
    current: tuple[int, int] | None = None

    for line_number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("["):
            current = _parse_section_header(
                stripped, source_file, line_number
            )
            continue

        if current is None:
            raise ValueError(
                f"calendar {source_file} line {line_number}: "
                f"entry appears before any section header"
            )

        year, quarter = current
        entries.append(
            _parse_entry_line(
                stripped, year, quarter, source_file, line_number
            )
        )

    return entries


def load_calendar(path: str | Path) -> list[CalendarEntry]:
    """Parse a calendar folder or file into a list of entries.

    - If ``path`` is a folder, parse every ``.txt`` file in lexicographic
      filename order and concatenate.
    - If ``path`` is a file, parse it directly.
    - If ``path`` does not exist, return an empty list.
    """
    p = Path(path)

    if p.is_dir():
        entries: list[CalendarEntry] = []
        for f in sorted(p.glob(f"*{CALENDAR_SUFFIX}")):
            if not f.is_file():
                continue
            entries.extend(_load_calendar_file(f))
        return entries

    if p.is_file():
        return _load_calendar_file(p)

    return []


def entries_for_quarter(
    entries: list[CalendarEntry], year: int, quarter: int
) -> list[CalendarEntry]:
    """Return entries whose ``(year, quarter)`` matches."""
    return [
        e for e in entries
        if e.year == year and e.quarter == quarter
    ]


def matches(entry: CalendarEntry, intersection: Intersection) -> bool:
    """Return ``True`` iff ``entry``'s pattern matches ``intersection``."""
    return (
        (entry.geography == "*" or entry.geography == intersection.geography)
        and (entry.sector == "*" or entry.sector == intersection.sector)
        and (entry.commodity == "*" or entry.commodity == intersection.commodity)
    )