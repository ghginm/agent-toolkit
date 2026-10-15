<!--
L1 index card — .agent/project-map/index.md. First document agents read.
Target a few hundred tokens; hard ceiling ~150 lines. Delete template
comments in the written card.
-->

```
status: verified-static            # health of THIS index card
verified_revision: <git-sha|none>
verified_at: <YYYY-MM-DD>
```

# <project> — map index

## Project
<one paragraph: what this codebase is/does, for whom, in one breath.>

## Modules
| Card | Responsibility (one line) | Status |
|---|---|---|
| [data-ingestion](modules/data-ingestion.md) | reads raw sources, normalizes into X | verified-static |
| [training](modules/training.md) | ... | ... |

## Entrypoints
- `<src/pipelines/train.py>` — how training is actually launched (cite).
- CLI/serve/notebook entries as observed in code.

## Build & test
- `<command>` — existence verified in `<ci-config/script>`; execution status: <run on <date> / not executed>.

## Flow
<3-8 lines: data/control flow end to end, or "request → module A → B → output" bullets.>

## Task → module routing
| If the task is about… | Start here |
|---|---|
| adding a data source | [data-ingestion](modules/data-ingestion.md) → `src/ingest/registry.py::register_source` |
| changing a model metric | [evaluation](modules/evaluation.md) → `src/eval/metrics.py` + tests `tests/eval/` |
| feature changes affecting serving | [features](modules/features.md) — see contracts; shared with serving |
| ... | ... |

<!-- 10-25 rows for a mid-size repo; fewer for small. Rows must have been
verified against code, not guessed from folders. -->

## Capabilities (L3)
- [missing-value-handling](capabilities/missing-value-handling.md) — trigger: <why it exists>

## Coverage & uncertainty
- Mapped: <modules>. Lightly mapped: <...>. NOT mapped: <areas + why (budget/volatility/user choice)>.
- Known open drift: <cards flagged stale>.
- This index reflects revision `<sha>` <(+ dirty tree noted where relevant)>; cards may lag — statuses tell you which were verified when.
