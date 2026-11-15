# janus/portfolio — ticker registry and portfolio calendar for Janus

A self-contained subsystem under `janus/`, structured like `janus/stirpes/`.
It does not modify any file outside its own directory. Registration is through
`Config.module_imports`.

The subsystem operates on two user-supplied data folders:

- **`tickers/`** — classifies tickers by three orthogonal axes:
  geography, sector, commodity. A ticker's classification is an
  *intersection* — a triple `(geography, sector, commodity)`. Many tickers
  can share the same intersection. A ticker can belong to more than one
  intersection.
- **`calendar/`** — records, per Gregorian year and quarter (2027–2046),
  which intersections are favored or dampened. The calendar does not know
  about tickers directly; it references intersections. The module resolves
  intersection → tickers via the tickers registry.

Cyclic and synodic analysis is out of scope for this subsystem. That is
KAIROS's job. The portfolio calendar only knows about Gregorian years and
quarters, and about the tickers the user has classified.

---

## Contents of the package

| File | Purpose |
|---|---|
| `__init__.py` | Package marker and public re-exports. Does not import the module class (would create a circular dependency during package load). |
| `tickers.py` | Axes definitions, `Intersection` type, ticker file parser, and the reverse index. No dependencies outside the standard library. |
| `calendar.py` | `CalendarEntry` type, calendar file parser, quarter lookup, wildcard matching. Imports the axes from `tickers.py`. |
| `portfolio_calendar.py` | The `Module` subclass registered under `module_imports`. Reads both folders, resolves symbol → intersections → active calendar entries, patches AGOP's axes. |
| `ibkr_broker.py` | Optional live-broker adapter implementing `PaperBroker.execute`. Not imported by the module. Requires `requests`. |
| `README.md` | This file. |

Complete filetree of the package:

```
janus/
└── portfolio/
    ├── README.md
    ├── __init__.py
    ├── tickers.py
    ├── calendar.py
    ├── portfolio_calendar.py
    └── ibkr_broker.py
```

Test file at the repository root:

```
tests/
└── test_portfolio.py
```

The test file uses `pytest.importorskip("janus")` and is skipped cleanly when
the full Janus environment is absent.

---

## The axes

Tickers are classified along three orthogonal axes. Each axis is a closed
set of string values.

### Geography (16 values)

`us`, `eu`, `uk`, `jp`, `kr`, `hk`, `sh`, `in`, `ca`, `za`, `lk`, `ng`, `ke`,
`br`, `ar`, `mx`.

### Sector (16 values)

`energy`, `power`, `nuclear`, `fusion`, `metals`, `precious`, `industrials`,
`defence`, `tech`, `semis`, `financials`, `agriculture`, `health`, `consumer`,
`infra`, `transport`.

### Commodity (15 values)

`oil`, `gas`, `coal`, `uranium`, `copper`, `lithium`, `gold`, `silver`, `pgm`,
`iron`, `aluminium`, `rare-earth`, `agri`, `cocoa`, `none`.

### Intersections

An **intersection** is a triple `(geography, sector, commodity)`. Every ticker
in the registry belongs to at least one intersection. A ticker may belong to
multiple intersections if it spans categories (e.g., a diversified energy
company may appear in both `(us, energy, oil)` and `(us, energy, gas)`).

The total number of possible intersections is 16 × 16 × 15 = 3,840. Only a
small fraction will be populated in practice. The registry only stores the
populated intersections.

---

## The `tickers/` folder

The `tickers/` folder contains one or more `.txt` files in the ticker file
format. The module concatenates all `.txt` files in lexicographic filename
order.

### Ticker file format

Each non-comment, non-blank line is either a section header or a ticker
under the current section.

**Section header** — a bracket-delimited triple:

```
[<geography> | <sector> | <commodity>]
```

All three fields must be specific values from their respective axes. No
wildcards, no omissions. The header opens a new section.

**Ticker line** — a single ticker (any non-empty string, upper-cased on
parse). One ticker per line. Duplicates within a section are deduplicated.

**Comments** — lines whose first non-whitespace character is `#`. Blank lines
are ignored.

**Example:**

```
# US uranium miners
[us | nuclear | uranium]
CCJ
UEC
NXE

# US oil producers
[us | energy | oil]
XOM
CVX
```

### File discovery

- All regular files in the folder whose suffix is exactly `.txt`.
- Sorted lexicographically by filename.
- Subfolders and non-`.txt` files are ignored.

### Invariants

| ID | Invariant |
|---|---|
| **I-T1** | Section header matches `[<geography> \| <sector> \| <commodity>]` exactly. |
| **I-T2** | Each field of the section header is a specific value from its axis. |
| **I-T3** | Each ticker line is a non-empty string, upper-cased on parse. |
| **I-T4** | A ticker may not appear before any section header. |
| **I-T5** | Duplicate sections with the same intersection are merged (accumulate). |
| **I-T6** | Duplicate tickers within a section are deduplicated. |

Any violation raises `ValueError` naming the source file, the line number, and
the offending token. There is no silent skip.

---

## The `calendar/` folder

The `calendar/` folder contains one or more `.txt` files in the calendar file
format. The module concatenates all `.txt` files in lexicographic filename
order.

### Calendar file format

Each non-comment, non-blank line is either a section header or an entry
under the current section.

**Section header** — a bracket-delimited year and quarter:

```
[<YYYY>Q<n>]
```

Where `YYYY` is a four-digit Gregorian year and `n` is `1` through `4`. The
section opens a new quarter.

**Entry line** — five pipe-separated fields:

```
<geography> | <sector> | <commodity> | <effect> | <event_id>
```

- **`geography`**, **`sector`**, **`commodity`** — either a specific axis value
  or `*` for wildcard. A wildcard matches any value on that axis.
- **`effect`** — one of eight effect tokens (see below).
- **`event_id`** — non-empty identifier used for citation.

**Example:**

```
[2027Q1]
us | nuclear | uranium | favor_long | uranium_2027q1
us | energy | oil | favor_long | oil_2027q1
* | fusion | none | favor_long | fusion_2027q1

[2027Q2]
us | nuclear | uranium | favor_long | uranium_2027q2
```

### Wildcards

A wildcard `*` in any of the three axis fields matches any value on that
axis. The parser accepts `*` only in calendar entries, not in ticker section
headers.

- `us | energy | *` matches `(us, energy, oil)`, `(us, energy, gas)`, etc.
- `us | * | oil` matches `(us, energy, oil)`, `(us, semis, oil)`, etc.
- `* | * | *` matches every intersection.

### File discovery

- All regular files in the folder whose suffix is exactly `.txt`.
- Sorted lexicographically by filename.
- Subfolders and non-`.txt` files are ignored.

### Invariants

| ID | Invariant |
|---|---|
| **I-C1** | Section header matches `[<YYYY>Q<n>]` exactly, with `YYYY` a 4-digit year and `n` ∈ {1,2,3,4}. |
| **I-C2** | Entry line has exactly five pipe-separated fields. |
| **I-C3** | Each axis field is a specific value from its axis or `*`. |
| **I-C4** | The effect is one of the eight tokens. |
| **I-C5** | The event ID is non-empty. |
| **I-C6** | An entry may not appear before any section header. |
| **I-C7** | Duplicate sections with the same `[YYYYQn]` are merged (accumulate). |

Any violation raises `ValueError` naming the source file, the line number, and
the offending token.

---

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

Every axis value lies in `[0, 1]`. `risk_multiplier` is always exactly `1.0`.

---

## The module's resolution logic

On each tick, with `symbol` from `context.snapshot.symbol` and `today` from
`datetime.now(timezone.utc).date()`:

1. **Resolve symbol to intersections.** Look up `symbol` (upper-cased) in the
   reverse index built from the tickers registry. Get the tuple of
   intersections the ticker belongs to. If empty, return a neutral
   `ModuleResult`.
2. **Compute the current quarter.** `year = today.year`,
   `quarter = (today.month - 1) // 3 + 1`.
3. **Filter calendar entries.** Keep only entries whose `(year, quarter)`
   matches. If empty, return neutral.
4. **Match patterns.** For each entry in the current quarter, check whether
   its pattern (with possible wildcards) matches *any* of the ticker's
   intersections. Keep the matching entries.
5. **Merge effects.** Apply `patch(effect)` for each matching entry. On any
   `(axis, action)` collision, the later entry in file order wins (deterministic).
6. **Veto.** `veto = True` if any matching entry has effect `veto_all`.
7. **Return** a `ModuleResult` with the merged `axes_patch`, the veto flag,
   and a structured `context` describing the symbol, intersections, and
   active entries.

### Formal specification

Let `T` be the reverse index: `T[symbol] → tuple[Intersection, ...]`.
Let `C` be the list of all parsed calendar entries.
Let `today = (Y, Q)` be the current Gregorian year and quarter.

Define:

```
M = [e ∈ C : e.year = Y ∧ e.quarter = Q ∧ ∃ i ∈ T[symbol] : matches(e, i)]
```

where `matches(e, i)` is `(e.geography ∈ {"*", i.geography}) ∧ (e.sector ∈
{"*", i.sector}) ∧ (e.commodity ∈ {"*", i.commodity})`.

Then:

```
axes_patch = merge([patch(e.effect) for e in M])
veto      = ∃ e ∈ M : e.effect = "veto_all"
```

`merge` applies `dict.update` in sequence order (`M`'s order, which is file
order). Every `axes_patch` value lies in `[0, 1]`.

---

## Path resolution

Both folder paths are resolved on every tick in this order:

**Tickers folder:**

1. `JANUS_PORTFOLIO_TICKERS` environment variable.
2. `configuration.portfolio_tickers_path` attribute, if present.
3. `tickers` in the current working directory.

**Calendar folder:**

1. `JANUS_PORTFOLIO_CALENDAR` environment variable.
2. `configuration.portfolio_calendar_path` attribute, if present.
3. `calendar` in the current working directory.

Re-resolving on every tick means env changes after import are honoured. If a
path points to a single `.txt` file rather than a folder, the module reads
that file directly.

If neither folder exists, the module is a no-op: no axes patched, no veto, no
error. Operators who want strictness set `on_error = "fail_closed"` in
`config.toml`.

---

## Caching

The module caches the parsed tickers registry (or reverse index) and the
parsed calendar entries in memory. On every tick it checks the modification
time of each source file (or the max of the modification times across `.txt`
files, if the path is a folder). If the modification time has changed since
the last parse, the module reloads and re-parses.

This means the module picks up user edits within one tick without a restart.
If the files are unchanged, the module performs only a `stat()` call per
tick.

---

## Register

Append the import path to `[modules].imports` in `config.toml`:

```toml
[modules]
imports = ["janus.portfolio.portfolio_calendar"]

[modules.portfolio_calendar]
enabled = true
on_error = "fail_closed"
```

`on_error = "fail_closed"` means a malformed ticker or calendar file vetoes
the tick.

---

## Structured context

The module exposes, in `context["events"]`, one dict per active entry:

```python
{
    "event_id": "uranium_2027q1",
    "year": 2027,
    "quarter": 1,
    "geography": "us",
    "sector": "nuclear",
    "commodity": "uranium",
    "effect": "favor_long",
    "source_file": "calendar.txt",
}
```

Plus `context["year"]`, `context["quarter"]`, and `context["intersections"]`
(a list of dicts with `geography`, `sector`, `commodity` for the ticker).

The LLM can cite any of these:

> "Window `uranium_2027q1` (us, nuclear, uranium; from `calendar.txt`) is
> active in 2027Q1; AGOP ranks LONG first; calendar favors accumulation."

---

## Optional broker adapter

`janus/portfolio/ibkr_broker.py` implements `PaperBroker.execute` from
`janus/execution.py`:

```python
def execute(
    self,
    intent: TradeIntent,
    symbol: str,
    price: float,
) -> Fill | None:
```

Semantics match `PaperBroker`:

- `FLAT` — flatten (long or short); return `None`.
- `LONG` — buy `position_size × equity / price` shares; return a `Fill`.
- `SHORT` — buy inverse-ETF proxy in `SHORT_PROXIES`; log and return `None` if
  no proxy.

**Known limitations**, documented in the module:

- `self.equity` is captured at construction; set `broker.equity` before
  `execute` if it has changed.
- `Fill.action` uses `intent.action.value`; verify against
  `janus/execution.py` if `PaperBroker` uses the `Action` enum.
- On `SHORT`, `Fill` records intent symbol, not the proxy.

Requires `requests` (only for the broker adapter, not for the module).

---

## Install

Module: no new install. Broker adapter:

```bash
pip install "requests>=2.32"
```

---

## Testing

```bash
pytest tests/test_portfolio.py
```

Tests cover:

- Ticker file parsing: sections, multiple sections, deduplication, error cases.
- Calendar file parsing: quarters, entries, wildcards, error cases.
- Reverse index construction and lookup.
- Quarter filtering.
- Pattern matching (exact and wildcard).
- Module behavior: no tickers, no calendar, active entry, wildcard match,
  merge precedence, veto, `validate_result` compliance.
- Context contents and `notes` format.

---

## Design notes

**Why three axes, not a taxonomy.** A taxonomy would require a stable
classification that the user maintains. Three orthogonal axes let the user
classify independently: a ticker is `(us, energy, oil)` or `(eu, nuclear,
uranium)`. A company that spans multiple categories appears in multiple
intersections. No hierarchy, no reclassification when a ticker is added.

**Why the calendar is year/quarter, not date ranges.** Date ranges invite
drift: the same event gets encoded as `2027-01-01 → 2028-06-30` in one file
and `2027-03-15 → 2028-07-10` in another, and now the module needs to resolve
overlapping intervals. Quarters are a fixed grid. Every entry snaps to a
quarter. Overlap is impossible by construction.

**Why cycles are outsourced to KAIROS.** The portfolio calendar has one job:
encode which intersections the user wants favored or dampened in which
quarters. Cyclic analysis (synodic periods, seasonal patterns, business-cycle
phases) is a different function with its own inputs and its own outputs.
KAIROS already performs that analysis. Duplicating it inside the portfolio
calendar would create two sources of truth for the same signal, and the
module's patches would conflict with KAIROS's.

**Why the ticker registry is not a database.** A JSON or SQLite file would
work, but the user edits the file by hand, and hand-editing structured data
invites format errors. The section-based plaintext format is the simplest
schema that supports grouping without requiring a schema. The parser is
strict because the module runs inside the trading pipeline; a malformed
section aborts the load with a `ValueError` naming the file, line, and
token.

**Why the module re-checks mtimes.** During development and editing, the
user needs changes to take effect without restarting Janus. The mtime check
costs one `stat()` per file per tick, which is negligible. When files change,
the module re-parses. When they don't, it uses the cached parse.

**Why `janus/__init__.py` must not import `janus.portfolio`.** Importing the
subpackage at package level would cause a circular import:
`janus/__init__.py` → `janus.portfolio` → `janus.portfolio.portfolio_calendar`
→ `janus.contracts` → `janus/__init__.py`. The module is registered via
`Config.module_imports`, which imports it lazily. This matches the existing
`janus/stirpes/` convention.