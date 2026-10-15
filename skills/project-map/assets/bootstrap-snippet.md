<!--
L0 bootstrap snippet — the pointer block for the project's agent-instructions
file. PASTE RULES (do not paste these): keep everything between the markers
verbatim and ≤15 lines; append into AGENTS.md / CLAUDE.md / harness equivalent
only with explicit user permission, only when no equivalent pointer exists,
never overwriting existing content (canonical rules: references/workflows.md §1 step 6).

===== paste below this line =====

## Project map (.agent/project-map/)

- `index.md` is the entry point: project overview + task→module routing. Consult it before exploring an unfamiliar part of this repo.
- Cards cite sources (`path::symbol`) and carry `status`/`verified_revision`. They are navigation aids, NOT authority: always read the actual code and tests you are about to change, even when the map looks fresh. If map and code disagree, code wins — then fix or flag the card (`status: stale`).
- After a change that alters module responsibilities, interfaces, entrypoints, or contracts, update the affected cards (and only those).
- If the map is missing, incomplete, or misleading, search the repository directly; use the `project-map` skill to create/refresh it when worthwhile.
- Audit reports (if any) live in `.agent/audits/`; findings are proposals (`status: draft`) until reviewed.

===== paste above this line =====
-->

