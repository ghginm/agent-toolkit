```
status: verified-static
verified_revision: none
verified_at: 2026-10-14
```

# Invoice batch — map

## Modules
| Card | Responsibility |
|---|---|
| [ingest](modules/ingest.md) | Load and deduplicate invoices |
| [core](modules/core.md) | Summaries |
| [delivery](modules/delivery.md) | Delivery |

## Entrypoint and routing
`app/main.py::main` loads records, summarizes, and publishes.
For money contracts start at [core](modules/core.md) and [ingest](modules/ingest.md).
For delivery start at [delivery](modules/delivery.md).

## Coverage
Mapped: ingest, core, delivery. No external transport source is bundled.
