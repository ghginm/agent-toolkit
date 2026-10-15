```
status: verified-static
verified_revision: none
verified_at: 2026-10-14
```

# Ledger — map index

## Project
Invoice ledger: reads CSVs of invoices, sorts by id, prints totals and reports.

## Modules
| Card | Responsibility | Status |
|---|---|---|
| [core](modules/core.md) | CSV loading, parsing, summary math | verified-static |

## Entrypoints
- `app/main.py::main` — CLI: `python -m app.main <csv>`.

## Build & test
- `pytest tests -q` — not executed during mapping (verified-static).

## Task → module routing
| Task | Start here |
|---|---|
| parsing / totals changes | [core](modules/core.md) → `app/core.py::load_records` |
| output/report format | `app/report.py` (unmapped — light area) |

## Coverage & uncertainty
- Mapped: core. Lightly mapped: report.py, main.py. No L3 cards (nothing triggers one).
