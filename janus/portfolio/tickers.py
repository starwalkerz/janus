"""janus.portfolio.tickers — axes definitions and ticker registry.

Three orthogonal axes classify every ticker:

- ``geography`` — where the ticker trades / is domiciled.
- ``sector`` — what industry the ticker operates in.
- ``commodity`` — what physical commodity the ticker is exposed to (or
  ``none``).

A ticker's classification is an *intersection*: a frozen triple
``(geography, sector, commodity)``. Many tickers can share the same
intersection. A ticker can belong to more than one intersection.

The tickers file is plaintext, section-based:

    [<geography> | <sector> | <commodity>]
    <ticker>
    <ticker>
    ...

Lines whose first non-whitespace character is ``#`` are comments. Blank
lines are ignored. There is no partial acceptance and no silent skip: every
malformed line raises ``ValueError`` with the source filename, the line
number, and the offending token.

Mathematical specification
--------------------------
Let ``F(D) = sorted([ f : f is a regular file in D, suffix(f) = ".txt" ])``.
Let ``R(D) = concat([ load_tickers(f) : f in F(D) ])``, where each
``load_tickers(f)`` returns a ``dict[Intersection, tuple[str, ...]]``.

The merged registry is built by taking the union of tickers per intersection
across all files (duplicate sections are merged; duplicate tickers within a
section are deduplicated).

Let ``I: str → tuple[Intersection, ...]`` be the *reverse index* built by
``build_reverse_index``:

    I(symbol) = tuple of every intersection whose ticker set contains
                ``symbol.upper()``.

The reverse index is the only structure the module uses at tick time.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

GEOGRAPHY_VALUES: Final[frozenset[str]] = frozenset(
    {
        "us", "eu", "uk", "jp", "kr", "hk", "sh", "in", "ca",
        "za", "lk", "ng", "ke", "br", "ar", "mx",
    }
)

SECTOR_VALUES: Final[frozenset[str]] = frozenset(
    {
        "energy", "power", "nuclear", "fusion", "metals", "precious",
        "industrials", "defence", "tech", "semis", "financials",
        "agriculture", "health", "consumer", "infra", "transport",
    }
)

COMMODITY_VALUES: Final[frozenset[str]] = frozenset(
    {
        "oil", "gas", "coal", "uranium", "copper", "lithium",
        "gold", "silver", "pgm", "iron", "aluminium", "rare-earth",
        "agri", "cocoa", "none",
    }
)

AXIS_VALUES: Final[dict[str, frozenset[str]]] = {
    "geography": GEOGRAPHY_VALUES,
    "sector": SECTOR_VALUES,
    "commodity": COMMODITY_VALUES,
}

DEFAULT_TICKERS_DIR: Final[Path] = Path("tickers")
TICKER_SUFFIX: Final[str] = ".txt"

_SECTION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^\[\s*([a-z\-]+)\s*\|\s*([a-z\-]+)\s*\|\s*([a-z\-]+)\s*\]$"
)


@dataclass(frozen=True)
class Intersection:
    """A triple ``(geography, sector, commodity)`` classifying a ticker."""

    geography: str
    sector: str
    commodity: str

    def __post_init__(self) -> None:
        if self.geography not in GEOGRAPHY_VALUES:
            raise ValueError(
                f"invalid geography {self.geography!r}; "
                f"expected one of {sorted(GEOGRAPHY_VALUES)}"
            )
        if self.sector not in SECTOR_VALUES:
            raise ValueError(
                f"invalid sector {self.sector!r}; "
                f"expected one of {sorted(SECTOR_VALUES)}"
            )
        if self.commodity not in COMMODITY_VALUES:
            raise ValueError(
                f"invalid commodity {self.commodity!r}; "
                f"expected one of {sorted(COMMODITY_VALUES)}"
            )


def _parse_section_header(
    line: str, source_file: str, line_number: int
) -> Intersection:
    """Parse a ``[geography | sector | commodity]`` header."""
    m = _SECTION_PATTERN.match(line.strip())
    if not m:
        raise ValueError(
            f"tickers {source_file} line {line_number}: "
            f"invalid section header {line!r}; "
            f"expected [<geography> | <sector> | <commodity>]"
        )
    geography, sector, commodity = m.groups()
    try:
        return Intersection(geography, sector, commodity)
    except ValueError as exc:
        raise ValueError(
            f"tickers {source_file} line {line_number}: {exc}"
        ) from exc


def _load_tickers_file(path: Path) -> dict[Intersection, list[str]]:
    """Parse a single tickers file into ``{Intersection: [tickers]}``."""
    source_file = path.name
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"tickers {source_file}: not valid UTF-8: {exc}"
        ) from exc

    registry: dict[Intersection, list[str]] = {}
    current: Intersection | None = None

    for line_number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("["):
            current = _parse_section_header(
                stripped, source_file, line_number
            )
            registry.setdefault(current, [])
            continue

        if current is None:
            raise ValueError(
                f"tickers {source_file} line {line_number}: "
                f"ticker {stripped!r} appears before any section header"
            )

        ticker = stripped.upper()
        if not ticker:
            raise ValueError(
                f"tickers {source_file} line {line_number}: "
                f"empty ticker"
            )
        registry[current].append(ticker)

    return registry


def load_tickers(path: str | Path) -> dict[Intersection, tuple[str, ...]]:
    """Parse a tickers folder or file into a registry.

    - If ``path`` is a folder, parse every ``.txt`` file in lexicographic
      filename order and merge the results.
    - If ``path`` is a file, parse it directly.
    - If ``path`` does not exist, return an empty dict.

    Duplicate sections across files are merged. Duplicate tickers within a
    section are deduplicated. The returned tuples are sorted for
    determinism.
    """
    p = Path(path)

    if p.is_dir():
        merged: dict[Intersection, set[str]] = {}
        for f in sorted(p.glob(f"*{TICKER_SUFFIX}")):
            if not f.is_file():
                continue
            for intersection, tickers in _load_tickers_file(f).items():
                merged.setdefault(intersection, set()).update(tickers)
        return {
            intersection: tuple(sorted(tickers))
            for intersection, tickers in merged.items()
        }

    if p.is_file():
        registry = _load_tickers_file(p)
        return {
            intersection: tuple(sorted(set(tickers)))
            for intersection, tickers in registry.items()
        }

    return {}


def build_reverse_index(
    registry: dict[Intersection, tuple[str, ...]]
) -> dict[str, tuple[Intersection, ...]]:
    """Invert the registry to ``{ticker: tuple[Intersection, ...]}``.

    The tuple is sorted by ``(geography, sector, commodity)`` for
    determinism. A ticker that appears in multiple intersections will have
    more than one entry in its tuple.
    """
    reverse: dict[str, list[Intersection]] = {}
    for intersection, tickers in registry.items():
        for ticker in tickers:
            reverse.setdefault(ticker, []).append(intersection)
    return {
        ticker: tuple(
            sorted(
                intersections,
                key=lambda i: (i.geography, i.sector, i.commodity),
            )
        )
        for ticker, intersections in reverse.items()
    }