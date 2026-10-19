```
module: ingest
status: verified-static
verified_revision: none
verified_at: 2026-10-14
sources:
  - app/ingest.py
  - app/main.py
depends-on: []
```

# Ingest

## Responsibility and contract
Loads a list of deduplicated rows with float amounts in currency units.

`app/ingest.py::load_records` is consumed by `app/main.py::main`.
