# tickers/

Classify tickers by three orthogonal axes: geography, sector, commodity.
Each classification is an *intersection* — a triple
`(geography, sector, commodity)`.

The module reads every `.txt` file in this folder and concatenates them in
lexicographic filename order. Each file uses the ticker file format below.

## File format

Each non-comment, non-blank line is either a section header or a ticker.

**Section header:**

```
[<geography> | <sector> | <commodity>]
```

All three fields must be specific values from their respective axes. The
header opens a new section.

**Ticker line:** a single ticker. One per line. Upper-cased on parse.
Duplicates within a section are deduplicated.

**Comments:** lines whose first non-whitespace character is `#`. Blank
lines are ignored.

## Axes

### Geography

`us` `eu` `uk` `jp` `kr` `hk` `sh` `in` `ca` `za` `lk` `ng` `ke` `br` `ar`
`mx`

### Sector

`energy` `power` `nuclear` `fusion` `metals` `precious` `industrials`
`defence` `tech` `semis` `financials` `agriculture` `health` `consumer`
`infra` `transport`

### Commodity

`oil` `gas` `coal` `uranium` `copper` `lithium` `gold` `silver` `pgm` `iron`
`aluminium` `rare-earth` `agri` `cocoa` `none`

## Example

```
[us | nuclear | uranium]
CCJ
UEC
NXE

[us | energy | oil]
XOM
CVX

[eu | metals | copper]
FCX
```

## Notes

- A ticker can appear in multiple intersections (e.g., a diversified
  energy company in both `[us | energy | oil]` and `[us | energy | gas]`).
- Duplicate sections are merged. Duplicate tickers within a section are
  deduplicated.
- A malformed line aborts the entire load with `ValueError` naming the
  source file, the line number, and the offending token. There is no
  silent skip.

## File discovery

- Regular files in this folder whose suffix is exactly `.txt`.
- Sorted lexicographically by filename.
- Subfolders and non-`.txt` files are ignored.

To disable a file without deleting it, rename it to `.txt.disabled`.

## Path resolution

Resolved on every tick:

1. `JANUS_PORTFOLIO_TICKERS` environment variable (folder or file).
2. `configuration.portfolio_tickers_path` attribute, if set.
3. `tickers` in the current working directory.

## See also

The calendar references intersections by axis values. See
[`calendar/README.md`](../calendar/README.md) for the calendar format.