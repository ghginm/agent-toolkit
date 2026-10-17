# Acceptance & Behavioral Evaluation

Unit tests prove the tools work. These scenarios prove the **skills produce useful agent behavior** (brief §19). They follow the spirit of the Anthropic creator's eval loop: fresh-context agent runs against fixtures with graded outputs; the `claude -p`-based runner scripts were unavailable in this environment (no Claude CLI), so runs are executed via generic subagents with the skill paths given explicitly — documented substitution, not silent omission. Baseline (without-skill) comparisons are included where they test an efficiency claim.

Ground truth for the flawed fixture lives in `expected-leaky-ml.json` (what was planted, where). A finding "counts" only when it cites the planted location. `score_run.py` automates the citation cross-check; semantic judgment (are the reasoning chains real? is proportionality respected?) is read by the evaluator, not scripted.

## Scenarios

**A1 — Audit all modes (architecture+ml+exploratory) on `leaky-ml`.**
Run: copy fixture to scratch (no git init — exercises the no-git path); fresh agent + `project-audit` skill; prompt: "Audit this project — architecture, ML methodology, and anything open-ended. Cite evidence."
Checks: report tree exists for all three modes only; every cited path resolves; planted defects found under the expected audit (see JSON); leakage not misfiled as architecture; `docs-vs-reality`-class items in exploratory without duplication; handoff sections name real files; anti_checks from the JSON hold (no fabricated runs — the fixture cannot even run without `data/churn.csv`); findings all `status: draft`; proportional recommendations (no enterprise infra demands).

**A2 — Audit single mode (`ml`) on `leaky-ml`.**
Checks: architecture-only artifacts (config overwrites) are NOT reported as findings (scope discipline), leakage/baseline/threshold ARE; `justified-now` vs `experiment-first` split present.

**M1 — Map create (scenario F + A combined): `leaky-ml`.**
Checks: L1 + 2-4 L2 cards, no L3 without trigger; honest statuses (nothing mass-marked `verified-executed`; the map cannot run the project); `sources:` all exist per map_check; README's "production-ready" NOT copied into current-state (docs-vs-code tension at most flagged); bootstrap snippet printed, not auto-pasted.

**M2 — Targeted change with correct map (scenario B): `map-sample`.**
Prompt: "Add average-per-invoice to the summary output." Expected route: L1 → core card → `app/core.py::summarize` + test file, without full-repo reads. Efficiency observation (qualitative): count of files the agent opened vs the repo's file count; recorded in results.

**M3 — Deliberately stale map (scenario C): `map-sample` + planted drift.**
Setup: mutate `app/core.py::load_records` to numeric-id sort and drop the float parse of `amount` (rename usage accordingly); leave the card claiming string-sort + float parsing; task: "make `write_report` output amounts with currency" (forces the agent to touch both the stale contract and report.py).
Checks: agent reads actual code, detects card-vs-code contradiction, prioritizes implementation, flags/repairs the card; behavior verified by test run; no blind trust of the card despite its `verified_at` date. Baseline arm: same task WITHOUT the map (directory `.agent/` removed) — compare files inspected & correctness, qualitative.

**M4 — Incremental update (scenario D): git'd `map-sample`.**
Setup: commit base; change `summarize` return format (interface fact) + add a new module file; run `update`.
Checks: `map_check --affected` used; core card changed; new module gets card or explicit deferral with reason; index routing updated if affected; NO untouched-card metadata rewrites (diff inspection).

**M5 — Missing map (scenario E):** coding task on `map-sample` with `.agent/` deleted — completes normally from source; optionally suggests creating a map; must not fail or hallucinate map content.

**M6 — Proportionality (scenario F):** map create on a 3-file tiny project (scratch: three ~10-line python files) vs on `leaky-ml`. Check: tiny → minimal (L1 only or L1+1 card); effort scales with repo.

**T1 — Trigger eval:** 20 mixed should/should-not queries judged from descriptions only (metadata-level), including near-misses (PR review, doc-diagram requests, "fix tests").

**E1 — Installer/validator mechanics:** covered exhaustively by `tests/test_install.py`, `test_validate.py`, `test_map_check.py` (single-skill installs, dry-run, conflict protection, unrelated files untouched, new-skill discovery via `mini-skill` fixture, Windows-path notes documented).

## How to run

Per scenario: (1) copy fixture under `/tmp/atk-accept/<scenario>/proj`; (2) spawn a fresh agent (subagent or clean CLI session) with ONLY: the project path + the skill dir path(s) installed at `<proj>/.agents/skills/` (use `tools/install.py --target <proj>`) + the task prompt verbatim from the scenario; (3) collect the outputs; (4) `python score_run.py a1 <run-dir>` for citation scoring, plus evaluator read-through for semantics; (5) append a dated section to `results.md` — pass/fail per check with evidence snippets. Failures that indicate skill defects get fixed in the skill, then the scenario re-runs (improvement iteration).

## Results

Documentation workflow checks (summary-first audit, human brief synthesis,
standalone use, freshness, incremental refresh, and description routing) live
in [documentation.md](documentation.md). Executed runs are recorded separately
in [documentation-results.md](documentation-results.md); unrun cases are not passes.

Focused checks for `agent-efficiency`, `tidy-dev`, and the optional policy live in
[extensions.md](extensions.md), with executed evidence in
[extensions-results.md](extensions-results.md). They use small supplied-session
scenarios and the existing fixture, not a new benchmark harness.

Focused overview/deep-dive and independent discussion/consolidation checks live
in [review-discussion.md](review-discussion.md), with executed evidence in
[review-discussion-results.md](review-discussion-results.md). They distinguish
description routing, packaging mechanics, and generated-document review.

The scenario-specific results files record actual executed runs with evidence.
Absence of a scenario from those records means it was NOT run; check the relevant
record before trusting a capability claim.
