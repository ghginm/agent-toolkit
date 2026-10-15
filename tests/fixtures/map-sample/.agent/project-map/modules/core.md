```
module: core
status: verified-static
verified_revision: none
verified_at: 2026-10-14
sources:
  - app/core.py
  - app/main.py
  - tests/test_core.py
tests:
  - tests/test_core.py
depends-on: []
```

# Core

## Responsibility
Reads invoice CSV rows, sorts them by `id`, parses `amount` to float, and computes count/total summaries. Does NOT write reports.

## Key entrypoints & symbols
| Symbol | File | Role |
|---|---|---|
| `load_records()` | `app/core.py::load_records` | sole loader; called by `app/main.py` and `app/report.py` |
| `summarize()` | `app/core.py::summarize` | total math |

## Contracts
- Input CSV columns: `id`, `amount` (string→float). Amount parsing: `float(r["amount"])` — currency units assumed plain floats (inferred rationale: no unit code anywhere in repo).

## Configuration & tests
- No config. Tests: `tests/test_core.py`.

## Caveats & invariants
- Sort order by `id` is string sort, not numeric — ids are zero-padded by convention (inferred).

## Where to look for X
| Change | Touch |
|---|---|
| totals logic | `app/core.py::summarize` |
| amount parsing rules | `app/core.py::load_records` |
