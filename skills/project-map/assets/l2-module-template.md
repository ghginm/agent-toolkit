<!--
L2 module card — .agent/project-map/modules/<module>.md (~60-120 lines).
One card per substantial module. Cite claims; keep honest statuses.
Delete template comments in the written card.
-->

```
module: <kebab-id>
# status: verified-static | verified-executed | inferred | proposed | stale — pick exactly ONE token after 'status:'
status: verified-static
verified_revision: <git-sha|none>
verified_at: <YYYY-MM-DD>
# sources/tests/config/depends-on: paths must exist / ids must name known cards; block-list style shown
sources:
  - src/<path>.py
tests:
  - tests/<path>.py
config:
  - configs/<file>.yaml
depends-on:
  - <other-module-id>
depended-on-by:
  - <...>
```

# <Module name>

## Responsibility
<2-4 sentences: what this module owns; what it deliberately does not own. Cite the
code that shows the boundary (a function, a registration point, a caller).>

## Key entrypoints & symbols
| Symbol | File | Role |
|---|---|---|
| `run()` | `src/pipelines/train.py::run` | process entry; called by CLI + CI |
| `build_features()` | `src/features/builder.py::build_features` | sole feature path for train AND serving (cite serving caller) |

## Upstream / downstream
- Reads: <inputs + source contract, cited> — verified|inferred.
- Consumed by: <modules/scripts that import or call these entrypoints> — verified by reading imports (list files) or marked inferred.

## Contracts
- <data shape crossing the boundary: keys/types/units/ordering assumptions; where the schema is defined (path::symbol)>
- <API/config contract: keys read, defaults, who sets them>

## Configuration & tests
<keys this module reads; test files that cover it. One line each.>

## Caveats & invariants
- <sharp edge: e.g. "assumes rows sorted by (entity, ts) — enforced nowhere but `ingest.py::write_parquet` sorts (cite)"; break here and features silently shift>
- <undocumented why: "binary encoding here rather than at serving — inferred rationale (not documented): serving runs on trimmed schema">

## Decisions & proposed direction (optional)
- <accepted-but-unimplemented plan, linked: AUD-ARCH-003 (see .agent/audits/<run>/architecture.md). NOT current state.>

## Where to look for X
| Change… | Touch |
|---|---|
| adding feature F | `src/features/builder.py` + `tests/features/test_builder.py`; check contract with serving (capabilities/<name> if present) |
| ... | ... |

## Verification (when status is verified-executed)
- `<command>` → <observed result>, <date>. Covers: <which claims>.
