"""Tests for ticker registry, calendar parser, and the module.

Every test constructs its own synthetic data. No fixture contains
production-specific content. Tests for the module use
``pytest.importorskip("janus")`` and are skipped cleanly when the full
Janus environment is absent.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from janus.portfolio.calendar import (
    EFFECTS,
    CalendarEntry,
    entries_for_quarter,
    load_calendar,
    matches,
)
from janus.portfolio.tickers import (
    COMMODITY_VALUES,
    GEOGRAPHY_VALUES,
    SECTOR_VALUES,
    Intersection,
    build_reverse_index,
    load_tickers,
)


# ─── fixtures ────────────────────────────────────────────────────────────


@pytest.fixture()
def write_file(tmp_path: Path):
    """Factory: write a file under ``tmp_path``."""

    def _make(name: str, lines: list[str]) -> Path:
        path = tmp_path / name
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    return _make


@pytest.fixture()
def make_folder(tmp_path: Path):
    """Factory: write a folder of files under ``tmp_path``."""
    counter = {"n": 0}

    def _make(files: dict[str, list[str]]) -> Path:
        counter["n"] += 1
        folder = tmp_path / f"folder_{counter['n']}"
        folder.mkdir()
        for name, lines in files.items():
            (folder / name).write_text(
                "\n".join(lines), encoding="utf-8"
            )
        return folder

    return _make


# ─── tickers: axes ───────────────────────────────────────────────────────


def test_intersection_validates_geography() -> None:
    with pytest.raises(ValueError, match="invalid geography"):
        Intersection("zz", "energy", "oil")


def test_intersection_validates_sector() -> None:
    with pytest.raises(ValueError, match="invalid sector"):
        Intersection("us", "zz", "oil")


def test_intersection_validates_commodity() -> None:
    with pytest.raises(ValueError, match="invalid commodity"):
        Intersection("us", "energy", "zz")


def test_intersection_accepts_valid_values() -> None:
    i = Intersection("us", "energy", "oil")
    assert i.geography == "us"
    assert i.sector == "energy"
    assert i.commodity == "oil"


# ─── tickers: parser ─────────────────────────────────────────────────────


def test_load_tickers_empty(tmp_path: Path) -> None:
    assert load_tickers(tmp_path / "absent") == {}


def test_load_tickers_single_section(write_file) -> None:
    path = write_file(
        "tickers.txt",
        [
            "[us | energy | oil]",
            "XOM",
            "CVX",
        ],
    )
    registry = load_tickers(path)
    key = Intersection("us", "energy", "oil")
    assert registry[key] == ("CVX", "XOM")


def test_load_tickers_multiple_sections(write_file) -> None:
    path = write_file(
        "tickers.txt",
        [
            "[us | energy | oil]",
            "XOM",
            "[us | nuclear | uranium]",
            "CCJ",
        ],
    )
    registry = load_tickers(path)
    assert registry[Intersection("us", "energy", "oil")] == ("XOM",)
    assert registry[Intersection("us", "nuclear", "uranium")] == ("CCJ",)


def test_load_tickers_upper_cases_tickers(write_file) -> None:
    path = write_file(
        "tickers.txt",
        ["[us | energy | oil]", "xom", "Cvx"],
    )
    registry = load_tickers(path)
    assert registry[Intersection("us", "energy", "oil")] == ("CVX", "XOM")


def test_load_tickers_deduplicates(write_file) -> None:
    path = write_file(
        "tickers.txt",
        ["[us | energy | oil]", "XOM", "XOM", "CVX"],
    )
    registry = load_tickers(path)
    assert registry[Intersection("us", "energy", "oil")] == ("CVX", "XOM")


def test_load_tickers_comments_ignored(write_file) -> None:
    path = write_file(
        "tickers.txt",
        [
            "# comment",
            "",
            "[us | energy | oil]",
            "XOM",
        ],
    )
    registry = load_tickers(path)
    assert registry[Intersection("us", "energy", "oil")] == ("XOM",)


def test_load_tickers_rejects_bad_header(write_file) -> None:
    path = write_file("tickers.txt", ["[us | energy]"])
    with pytest.raises(ValueError, match="invalid section header"):
        load_tickers(path)


def test_load_tickers_rejects_bad_axis_value(write_file) -> None:
    path = write_file("tickers.txt", ["[zz | energy | oil]"])
    with pytest.raises(ValueError, match="invalid geography"):
        load_tickers(path)


def test_load_tickers_rejects_ticker_before_section(write_file) -> None:
    path = write_file("tickers.txt", ["XOM"])
    with pytest.raises(ValueError, match="before any section"):
        load_tickers(path)


def test_load_tickers_ignores_blank_lines(write_file) -> None:
    path = write_file(
        "tickers.txt",
        ["[us | energy | oil]", "   "],
    )
    registry = load_tickers(path)
    assert registry[Intersection("us", "energy", "oil")] == ()


def test_load_tickers_folder_concatenates(make_folder) -> None:
    folder = make_folder(
        {
            "01.txt": ["[us | energy | oil]", "XOM"],
            "02.txt": ["[us | nuclear | uranium]", "CCJ"],
        }
    )
    registry = load_tickers(folder)
    assert registry[Intersection("us", "energy", "oil")] == ("XOM",)
    assert registry[Intersection("us", "nuclear", "uranium")] == ("CCJ",)


def test_load_tickers_folder_merges_duplicate_sections(make_folder) -> None:
    folder = make_folder(
        {
            "01.txt": ["[us | energy | oil]", "XOM"],
            "02.txt": ["[us | energy | oil]", "CVX"],
        }
    )
    registry = load_tickers(folder)
    assert registry[Intersection("us", "energy", "oil")] == ("CVX", "XOM")


def test_build_reverse_index(write_file) -> None:
    path = write_file(
        "tickers.txt",
        [
            "[us | energy | oil]",
            "XOM",
            "[us | energy | gas]",
            "XOM",
            "[us | nuclear | uranium]",
            "CCJ",
        ],
    )
    registry = load_tickers(path)
    reverse = build_reverse_index(registry)
    xom_intersections = reverse["XOM"]
    assert len(xom_intersections) == 2
    sectors = {i.sector for i in xom_intersections}
    assert sectors == {"energy"}
    commodities = {i.commodity for i in xom_intersections}
    assert commodities == {"oil", "gas"}
    assert reverse["CCJ"] == (
        Intersection("us", "nuclear", "uranium"),
    )


# ─── calendar: parser ────────────────────────────────────────────────────


def test_load_calendar_empty(tmp_path: Path) -> None:
    assert load_calendar(tmp_path / "absent") == []


def test_load_calendar_single_quarter(write_file) -> None:
    path = write_file(
        "calendar.txt",
        [
            "[2027Q1]",
            "us | nuclear | uranium | favor_long | U2027Q1",
        ],
    )
    entries = load_calendar(path)
    assert len(entries) == 1
    e = entries[0]
    assert isinstance(e, CalendarEntry)
    assert e.year == 2027
    assert e.quarter == 1
    assert e.geography == "us"
    assert e.sector == "nuclear"
    assert e.commodity == "uranium"
    assert e.effect == "favor_long"
    assert e.event_id == "U2027Q1"


def test_load_calendar_multiple_quarters(write_file) -> None:
    path = write_file(
        "calendar.txt",
        [
            "[2027Q1]",
            "us | nuclear | uranium | favor_long | A",
            "[2027Q2]",
            "us | nuclear | uranium | favor_long | B",
        ],
    )
    entries = load_calendar(path)
    assert [e.event_id for e in entries] == ["A", "B"]


def test_load_calendar_wildcard_supported(write_file) -> None:
    path = write_file(
        "calendar.txt",
        [
            "[2027Q1]",
            "* | fusion | none | favor_long | F",
        ],
    )
    entries = load_calendar(path)
    e = entries[0]
    assert e.geography == "*"
    assert e.sector == "fusion"
    assert e.commodity == "none"


def test_load_calendar_comments_ignored(write_file) -> None:
    path = write_file(
        "calendar.txt",
        [
            "# comment",
            "",
            "[2027Q1]",
            "us | nuclear | uranium | favor_long | A",
        ],
    )
    entries = load_calendar(path)
    assert len(entries) == 1


def test_load_calendar_rejects_bad_section(write_file) -> None:
    path = write_file("calendar.txt", ["[2027Q5]"])
    with pytest.raises(ValueError, match="invalid section header"):
        load_calendar(path)


def test_load_calendar_rejects_bad_axis(write_file) -> None:
    path = write_file(
        "calendar.txt",
        ["[2027Q1]", "zz | nuclear | uranium | favor_long | A"],
    )
    with pytest.raises(ValueError, match="invalid geography"):
        load_calendar(path)


def test_load_calendar_rejects_unknown_effect(write_file) -> None:
    path = write_file(
        "calendar.txt",
        ["[2027Q1]", "us | nuclear | uranium | zz | A"],
    )
    with pytest.raises(ValueError, match="unknown effect"):
        load_calendar(path)


def test_load_calendar_rejects_empty_event_id(write_file) -> None:
    path = write_file(
        "calendar.txt",
        ["[2027Q1]", "us | nuclear | uranium | favor_long | "],
    )
    with pytest.raises(ValueError, match="empty event ID"):
        load_calendar(path)


def test_load_calendar_rejects_wrong_field_count(write_file) -> None:
    path = write_file(
        "calendar.txt",
        ["[2027Q1]", "us | nuclear | favor_long | A"],
    )
    with pytest.raises(ValueError, match="expected 5 pipe-separated"):
        load_calendar(path)


def test_load_calendar_rejects_entry_before_section(write_file) -> None:
    path = write_file(
        "calendar.txt",
        ["us | nuclear | uranium | favor_long | A"],
    )
    with pytest.raises(ValueError, match="before any section"):
        load_calendar(path)


def test_entries_for_quarter(write_file) -> None:
    path = write_file(
        "calendar.txt",
        [
            "[2027Q1]",
            "us | nuclear | uranium | favor_long | A",
            "[2027Q2]",
            "us | nuclear | uranium | favor_long | B",
            "[2028Q1]",
            "us | nuclear | uranium | favor_long | C",
        ],
    )
    entries = load_calendar(path)
    q1_2027 = entries_for_quarter(entries, 2027, 1)
    assert [e.event_id for e in q1_2027] == ["A"]
    q2_2027 = entries_for_quarter(entries, 2027, 2)
    assert [e.event_id for e in q2_2027] == ["B"]
    q1_2028 = entries_for_quarter(entries, 2028, 1)
    assert [e.event_id for e in q1_2028] == ["C"]


def test_matches_exact() -> None:
    entry = CalendarEntry(
        year=2027, quarter=1,
        geography="us", sector="energy", commodity="oil",
        effect="favor_long", event_id="A",
        line_number=1, source_file="x.txt",
    )
    assert matches(entry, Intersection("us", "energy", "oil"))
    assert not matches(entry, Intersection("eu", "energy", "oil"))


def test_matches_wildcard_on_commodity() -> None:
    entry = CalendarEntry(
        year=2027, quarter=1,
        geography="us", sector="energy", commodity="*",
        effect="favor_long", event_id="A",
        line_number=1, source_file="x.txt",
    )
    assert matches(entry, Intersection("us", "energy", "oil"))
    assert matches(entry, Intersection("us", "energy", "gas"))
    assert not matches(entry, Intersection("eu", "energy", "oil"))


def test_matches_wildcard_all() -> None:
    entry = CalendarEntry(
        year=2027, quarter=1,
        geography="*", sector="*", commodity="*",
        effect="favor_long", event_id="A",
        line_number=1, source_file="x.txt",
    )
    assert matches(entry, Intersection("us", "energy", "oil"))
    assert matches(entry, Intersection("eu", "nuclear", "uranium"))


# ─── module ──────────────────────────────────────────────────────────────


janus = pytest.importorskip("janus")
from janus.contracts import MarketSnapshot, ModulePhase  # noqa: E402
from janus.modules.base import (  # noqa: E402
    Module,
    ModuleContext,
    ModuleResult,
)
from janus.modules.registry import validate_result  # noqa: E402

from janus.portfolio.portfolio_calendar import (  # noqa: E402
    PortfolioCalendarModule,
    module as registered_module,
)


def _snapshot(symbol: str) -> MarketSnapshot:
    return MarketSnapshot(
        symbol=symbol,
        price=100.0,
        expected_return=0.01,
        realized_volatility=0.02,
        slippage=1.0,
        slippage_maximum=10.0,
        venue_risk=0.1,
        signal_agreement=0.5,
        order_flow_imbalance=0.0,
        history=(),
        timestamps=(),
        external_data={},
    )


def _context(
    symbol: str,
    prior: dict[str, ModuleResult] | None = None,
) -> ModuleContext:
    return ModuleContext(
        snapshot=_snapshot(symbol),
        configuration=None,
        strategy=None,
        phase=ModulePhase.PRE_AGOP,
        prior_results=prior or {},
    )


def _freeze_today(target: date):
    fixed = datetime(
        target.year, target.month, target.day, tzinfo=timezone.utc
    )

    class _FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed

    return patch(
        "janus.portfolio.portfolio_calendar.datetime", _FixedDatetime
    )


def test_module_is_registered_instance() -> None:
    assert isinstance(registered_module, Module)
    assert registered_module.name == "portfolio_calendar"
    assert registered_module.phase is ModulePhase.PRE_AGOP


def test_module_no_tickers_returns_neutral(make_folder) -> None:
    tickers_folder = make_folder({})
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | favor_long | A"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM"))

    assert result.axes_patch == {}
    assert result.veto is False
    assert result.risk_multiplier == 1.0
    validate_result(result)


def test_module_no_calendar_returns_neutral(make_folder) -> None:
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder({})
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM"))

    assert result.axes_patch == {}
    assert result.veto is False
    validate_result(result)


def test_module_favor_long_patches(make_folder) -> None:
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | favor_long | A"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM"))

    assert result.axes_patch["pain"]["LONG"] == 0.85
    assert result.axes_patch["barrier"]["LONG"] == 0.15
    assert result.veto is False
    validate_result(result)


def test_module_quarter_mismatch_returns_neutral(make_folder) -> None:
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q3]", "us | energy | oil | favor_long | A"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM"))

    assert result.axes_patch == {}
    validate_result(result)


def test_module_wildcard_entry(make_folder) -> None:
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | fusion | none]", "OKLO"]}
    )
    calendar_folder = make_folder(
        {
            "calendar.txt": [
                "[2027Q1]",
                "* | fusion | * | favor_long | F",
            ]
        }
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("OKLO"))

    assert result.axes_patch["pain"]["LONG"] == 0.85
    validate_result(result)


def test_module_veto_all(make_folder) -> None:
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | veto_all | V"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM"))

    assert result.veto is True
    validate_result(result)


def test_module_later_entry_wins_on_collision(make_folder) -> None:
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {
            "calendar.txt": [
                "[2027Q1]",
                "us | energy | oil | favor_long | A",
                "us | energy | oil | dampen_long | B",
            ]
        }
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM"))

    assert result.axes_patch["barrier"]["LONG"] == 0.85
    assert result.axes_patch["pain"]["LONG"] == 0.85
    validate_result(result)


def test_module_context_contains_events(make_folder) -> None:
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | favor_long | A"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM"))

    assert result.context["year"] == 2027
    assert result.context["quarter"] == 1
    assert len(result.context["events"]) == 1
    event = result.context["events"][0]
    assert event["event_id"] == "A"
    assert event["effect"] == "favor_long"
    assert event["source_file"] == "calendar.txt"
    validate_result(result)


# ─── precedence: portfolio_calendar yields to opportunity ────────────────


def test_module_yields_to_prior_opportunity_on_collision(make_folder) -> None:
    """Portfolio drops patches for (axis, action) pairs already patched by an opportunity module."""
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | dampen_long | A"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    prior = {
        "agop_opportunity": ModuleResult(
            name="agop_opportunity",
            phase=ModulePhase.PRE_AGOP,
            axes_patch={
                "pain": {"LONG": 0.90},
                "barrier": {"LONG": 0.10},
            },
        ),
    }

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM", prior=prior))

    # dampen_long only patches barrier[LONG]; opportunity already covered it.
    # The entire calendar patch is dropped.
    assert result.axes_patch == {}
    validate_result(result)


def test_module_preserves_patches_not_covered_by_opportunity(make_folder) -> None:
    """Portfolio keeps patches for (axis, action) pairs that opportunity did not touch."""
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | favor_long | A"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    prior = {
        "agop_opportunity": ModuleResult(
            name="agop_opportunity",
            phase=ModulePhase.PRE_AGOP,
            axes_patch={"pain": {"SHORT": 0.90}},
        ),
    }

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM", prior=prior))

    # favor_long patches pain[LONG], readiness[LONG], barrier[LONG].
    # opportunity only patched pain[SHORT]. No collision.
    assert result.axes_patch["pain"]["LONG"] == 0.85
    assert result.axes_patch["readiness"]["LONG"] == 0.85
    assert result.axes_patch["barrier"]["LONG"] == 0.15
    validate_result(result)


def test_module_partial_yield_on_mixed_collision(make_folder) -> None:
    """If opportunity covers some but not all of the calendar's patches, only covered pairs are dropped."""
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | favor_long | A"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    prior = {
        "agop_opportunity": ModuleResult(
            name="agop_opportunity",
            phase=ModulePhase.PRE_AGOP,
            axes_patch={"pain": {"LONG": 0.90}},
        ),
    }

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM", prior=prior))

    # opportunity covers pain[LONG]. favor_long also patches readiness[LONG]
    # and barrier[LONG]. Those survive.
    assert "pain" not in result.axes_patch or "LONG" not in result.axes_patch.get("pain", {})
    assert result.axes_patch["readiness"]["LONG"] == 0.85
    assert result.axes_patch["barrier"]["LONG"] == 0.15
    validate_result(result)


def test_module_ignores_non_opportunity_prior_results(make_folder) -> None:
    """Only modules in _OPPORTUNITY_MODULE_NAMES cause yielding."""
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | favor_long | A"]}
    )
    module = PortfolioCalendarModule()
    module._tickers_path = tickers_folder
    module._calendar_path = calendar_folder

    prior = {
        "regime": ModuleResult(
            name="regime",
            phase=ModulePhase.PRE_AGOP,
            axes_patch={"pain": {"LONG": 0.20}},
        ),
        "sentiment": ModuleResult(
            name="sentiment",
            phase=ModulePhase.PRE_AGOP,
            axes_patch={"barrier": {"LONG": 0.50}},
        ),
    }

    with _freeze_today(date(2027, 2, 1)):
        result = module.run(_context("XOM", prior=prior))

    # Non-opportunity modules do not trigger yielding. Portfolio overrides
    # both regime's and sentiment's prior patches.
    assert result.axes_patch["pain"]["LONG"] == 0.85
    assert result.axes_patch["barrier"]["LONG"] == 0.15
    validate_result(result)


def test_module_yields_to_each_opportunity_module(make_folder) -> None:
    """Each of the four opportunity modules can trigger yielding."""
    tickers_folder = make_folder(
        {"tickers.txt": ["[us | energy | oil]", "XOM"]}
    )
    calendar_folder = make_folder(
        {"calendar.txt": ["[2027Q1]", "us | energy | oil | dampen_long | A"]}
    )

    for module_name in (
        "agop_opportunity",
        "causality_opportunity",
        "kairos_opportunity",
        "opportunity_synthesizer",
    ):
        module = PortfolioCalendarModule()
        module._tickers_path = tickers_folder
        module._calendar_path = calendar_folder

        prior = {
            module_name: ModuleResult(
                name=module_name,
                phase=ModulePhase.PRE_AGOP,
                axes_patch={"barrier": {"LONG": 0.10}},
            ),
        }

        with _freeze_today(date(2027, 2, 1)):
            result = module.run(_context("XOM", prior=prior))

        assert result.axes_patch == {}, f"{module_name} did not trigger yield"
        validate_result(result)