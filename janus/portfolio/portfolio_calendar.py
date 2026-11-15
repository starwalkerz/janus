"""janus.portfolio.portfolio_calendar — ticker registry + calendar as a module.

A ``Module`` subclass with ``name``, ``phase``, ``run(context) -> ModuleResult``,
and a module-level ``module`` instance that
``janus.bootstrap.build_default_registry`` registers.

The module reads two user-supplied folders (``tickers/`` and ``calendar/``)
and, on every tick, resolves ``snapshot.symbol`` to its intersections in the
ticker registry, finds the active calendar entries for the current Gregorian
quarter, and patches AGOP's axes. It does not size, execute, or override the
risk bound. It may veto only for the ``veto_all`` effect.

Precedence
----------
The calendar is the baseline. Opportunity modules (``agop_opportunity``,
``causality_opportunity``, ``kairos_opportunity``, ``opportunity_synthesizer``)
observe opportunities *within* the calendar's windows. If an opportunity
module has already patched a given ``(axis, action)`` pair, the calendar
yields to it: the calendar's patch for that pair is dropped, and the
opportunity module's value survives.

Veto is not yielded. A ``veto_all`` entry in the calendar always sets
``veto = True``. Opportunity signals can favor or dampen within the calendar
window; they cannot override the calendar's explicit prohibition.

Path resolution
---------------
Both paths are resolved on every tick:

Tickers folder:
    1. ``JANUS_PORTFOLIO_TICKERS`` environment variable.
    2. ``configuration.portfolio_tickers_path`` attribute.
    3. ``tickers`` in the current working directory.

Calendar folder:
    1. ``JANUS_PORTFOLIO_CALENDAR`` environment variable.
    2. ``configuration.portfolio_calendar_path`` attribute.
    3. ``calendar`` in the current working directory.

If the resolved path points to a single ``.txt`` file, the module reads that
file directly. If it does not exist, the module is a no-op.

Caching
-------
The parsed registry (reverse index) and calendar entries are cached in
memory. On every tick the module checks the modification time of each
source file (or the max of the modification times across ``.txt`` files in
a folder). If the modification time has changed, the module reloads.

Mathematical specification
--------------------------
Let ``T`` be the reverse index: ``symbol → tuple[Intersection, ...]``.
Let ``C`` be the list of parsed calendar entries.
Let ``today = (Y, Q)`` be the current Gregorian year and quarter.

    M = [e ∈ C : e.year = Y ∧ e.quarter = Q ∧
                 ∃ i ∈ T[symbol] : matches(e, i)]

    raw_patch  = merge([patch(e.effect) for e in M])
    covered    = {(axis, action) : prior opportunity module patched it}
    axes_patch = raw_patch \ covered
    veto       = ∃ e ∈ M : e.effect = "veto_all"

Every value in ``axes_patch`` lies in ``[0, 1]``. ``risk_multiplier`` is
exactly ``1.0``.
"""

from __future__ import annotations

import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final, Optional

from janus.contracts import ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult

from janus.portfolio.calendar import (
    CalendarEntry,
    entries_for_quarter,
    load_calendar,
    matches,
)
from janus.portfolio.tickers import (
    Intersection,
    build_reverse_index,
    load_tickers,
)

_HIGH: Final[float] = 0.85
_LOW: Final[float] = 0.15

_TICKERS_ENV: Final[str] = "JANUS_PORTFOLIO_TICKERS"
_CALENDAR_ENV: Final[str] = "JANUS_PORTFOLIO_CALENDAR"
_DEFAULT_TICKERS_DIR: Final[Path] = Path("tickers")
_DEFAULT_CALENDAR_DIR: Final[Path] = Path("calendar")

_OPPORTUNITY_MODULE_NAMES: Final[frozenset[str]] = frozenset(
    {
        "agop_opportunity",
        "causality_opportunity",
        "kairos_opportunity",
        "opportunity_synthesizer",
    }
)


def _resolve_tickers_path(configuration: Any) -> Path:
    env = os.environ.get(_TICKERS_ENV)
    if env:
        return Path(env)
    configured = getattr(configuration, "portfolio_tickers_path", None)
    if configured:
        return Path(configured)
    return _DEFAULT_TICKERS_DIR


def _resolve_calendar_path(configuration: Any) -> Path:
    env = os.environ.get(_CALENDAR_ENV)
    if env:
        return Path(env)
    configured = getattr(configuration, "portfolio_calendar_path", None)
    if configured:
        return Path(configured)
    return _DEFAULT_CALENDAR_DIR


def _safe_mtime(path: Path) -> Optional[float]:
    """Return the max mtime of ``.txt`` files at ``path``, or ``None``."""
    try:
        if path.is_file():
            return path.stat().st_mtime
        if path.is_dir():
            mtimes = [
                f.stat().st_mtime
                for f in path.glob("*.txt")
                if f.is_file()
            ]
            return max(mtimes) if mtimes else None
    except OSError:
        pass
    return None


def _patch_for_effect(effect: str) -> dict[str, dict[str, float]]:
    """Map a calendar effect to an axis patch. Every value in ``[0, 1]``."""
    if effect == "favor_long":
        return {
            "pain": {"LONG": _HIGH},
            "readiness": {"LONG": _HIGH},
            "barrier": {"LONG": _LOW},
        }
    if effect == "favor_short":
        return {
            "pain": {"SHORT": _HIGH},
            "readiness": {"SHORT": _HIGH},
            "barrier": {"SHORT": _LOW},
        }
    if effect == "dampen_all":
        return {"barrier": {"LONG": _HIGH, "SHORT": _HIGH}}
    if effect == "dampen_long":
        return {"barrier": {"LONG": _HIGH}}
    if effect == "dampen_short":
        return {"barrier": {"SHORT": _HIGH}}
    if effect == "veto_long":
        return {
            "pain": {"LONG": _LOW},
            "readiness": {"LONG": _LOW},
            "barrier": {"LONG": 1.0},
        }
    if effect == "veto_short":
        return {
            "pain": {"SHORT": _LOW},
            "readiness": {"SHORT": _LOW},
            "barrier": {"SHORT": 1.0},
        }
    if effect == "veto_all":
        return {}
    return {}


def _merge_patches(
    patches: list[dict[str, dict[str, float]]],
) -> dict[str, dict[str, float]]:
    """Merge axis patches. Later patches win per (axis, action) pair."""
    merged: dict[str, dict[str, float]] = {}
    for patch in patches:
        for axis, actions in patch.items():
            merged.setdefault(axis, {}).update(actions)
    return merged


def _covered_by_opportunity(
    prior_results: dict[str, ModuleResult],
) -> dict[str, frozenset[str]]:
    """Return, per axis, the set of actions already patched by an opportunity module.

    Any ``(axis, action)`` pair in the returned mapping is considered covered
    by a higher-precedence module. The calendar yields to it.
    """
    covered: dict[str, set[str]] = {}
    for module_name, result in prior_results.items():
        if module_name not in _OPPORTUNITY_MODULE_NAMES:
            continue
        axes_patch = getattr(result, "axes_patch", None) or {}
        for axis, actions in axes_patch.items():
            covered.setdefault(axis, set()).update(actions.keys())
    return {axis: frozenset(actions) for axis, actions in covered.items()}


def _drop_covered(
    patch: dict[str, dict[str, float]],
    covered: dict[str, frozenset[str]],
) -> dict[str, dict[str, float]]:
    """Remove any ``(axis, action)`` pair present in ``covered`` from ``patch``."""
    if not covered:
        return patch
    result: dict[str, dict[str, float]] = {}
    for axis, actions in patch.items():
        covered_actions = covered.get(axis, frozenset())
        kept = {a: v for a, v in actions.items() if a not in covered_actions}
        if kept:
            result[axis] = kept
    return result


def _neutral_result(
    name: str,
    phase: ModulePhase,
    year: int,
    quarter: int,
    intersections: tuple[Intersection, ...],
    note: str,
) -> ModuleResult:
    return ModuleResult(
        name=name,
        phase=phase,
        context={
            "year": year,
            "quarter": quarter,
            "intersections": [asdict(i) for i in intersections],
            "events": [],
        },
        notes=note,
    )


class PortfolioCalendarModule(Module):
    """PRE_AGOP module reading the ticker registry and calendar."""

    name: str = "portfolio_calendar"
    phase: ModulePhase = ModulePhase.PRE_AGOP

    def __init__(self) -> None:
        self._tickers_path: Optional[Path] = None
        self._tickers_mtime: Optional[float] = None
        self._tickers_reverse: Optional[dict[str, tuple[Intersection, ...]]] = None
        self._calendar_path: Optional[Path] = None
        self._calendar_mtime: Optional[float] = None
        self._calendar_entries: Optional[list[CalendarEntry]] = None

    def _get_reverse(
        self, configuration: Any
    ) -> dict[str, tuple[Intersection, ...]]:
        path = _resolve_tickers_path(configuration)
        mtime = _safe_mtime(path)
        if self._tickers_path != path or self._tickers_mtime != mtime:
            registry = load_tickers(path)
            self._tickers_reverse = build_reverse_index(registry)
            self._tickers_path = path
            self._tickers_mtime = mtime
        return self._tickers_reverse or {}

    def _get_entries(self, configuration: Any) -> list[CalendarEntry]:
        path = _resolve_calendar_path(configuration)
        mtime = _safe_mtime(path)
        if self._calendar_path != path or self._calendar_mtime != mtime:
            self._calendar_entries = load_calendar(path)
            self._calendar_path = path
            self._calendar_mtime = mtime
        return self._calendar_entries or []

    def run(self, context: ModuleContext) -> ModuleResult:
        symbol = context.snapshot.symbol.upper()
        today = datetime.now(timezone.utc).date()
        year = today.year
        quarter = (today.month - 1) // 3 + 1

        reverse = self._get_reverse(context.configuration)
        intersections = reverse.get(symbol, ())

        if not intersections:
            return _neutral_result(
                self.name,
                self.phase,
                year,
                quarter,
                (),
                f"calendar: no intersection for {symbol}",
            )

        entries = self._get_entries(context.configuration)
        quarter_entries = entries_for_quarter(entries, year, quarter)
        matching = [
            e
            for e in quarter_entries
            if any(matches(e, i) for i in intersections)
        ]

        if not matching:
            return _neutral_result(
                self.name,
                self.phase,
                year,
                quarter,
                intersections,
                f"calendar: no active entries for {symbol} in {year}Q{quarter}",
            )

        patches = [_patch_for_effect(e.effect) for e in matching]
        merged = _merge_patches(patches)

        covered = _covered_by_opportunity(context.prior_results or {})
        merged = _drop_covered(merged, covered)

        veto = any(e.effect == "veto_all" for e in matching)

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            axes_patch=merged,
            veto=veto,
            context={
                "year": year,
                "quarter": quarter,
                "intersections": [asdict(i) for i in intersections],
                "events": [
                    {
                        "event_id": e.event_id,
                        "year": e.year,
                        "quarter": e.quarter,
                        "geography": e.geography,
                        "sector": e.sector,
                        "commodity": e.commodity,
                        "effect": e.effect,
                        "source_file": e.source_file,
                    }
                    for e in matching
                ],
            },
            notes=(
                f"calendar: {','.join(e.event_id for e in matching)} "
                f"for {symbol} in {year}Q{quarter}"
            ),
        )


# Janus's ``module_imports`` loader expects a ``module`` attribute that is a
# Module instance.
module: PortfolioCalendarModule = PortfolioCalendarModule()