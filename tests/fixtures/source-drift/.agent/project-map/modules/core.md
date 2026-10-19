```
module: core
status: verified-static
verified_revision: none
verified_at: 2026-10-14
sources:
  - app/core.py
  - app/main.py
  - tests/test_core.py
depends-on: []
```

# Core

## Responsibility and contract
Summarizes records as count and total_cents.

`app/core.py::summarize` returns a dictionary read by `app/main.py::main`; regression assertions exist in `tests/test_core.py::CoreTests` (not executed in this map).
