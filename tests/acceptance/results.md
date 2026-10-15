# Acceptance Results — 2026-10-15

Executed on this machine (WSL Linux). Harness used: generic subagents (fresh context) pointed at skill copies installed by `tools/install.py --harness generic` into scratch project clones. The Anthropic creator's `claude -p`-based eval runner was unavailable (no Claude CLI installed), so runs use the documented generic-subagent substitution; grading = structured child reports + evaluator re-inspection of written files + `score_run.py`/`check_report.py`/`map_check.py` where applicable.

## Environment facts (relevant to honesty checks)

- Python: system 3.12 (/usr/bin/python3) + 3.14; **no pytest, no pandas/sklearn**; fixtures cannot fully execute → `verified-executed` claims should only cover what agents actually ran.
- Git available; leaky-ml copies left non-git on purpose.

## Scenario outcomes

### A2 — audit, `ml` mode only: **PASS**
8 findings, all citing planted defect locations:
scaler-fit-before-split (`src/data.py::build_dataset`) P0; shuffled-temporal-split P0; serving scaler refit / train-serve divergence (`src/predict.py`) P0; accuracy-only + no-baseline (`src/train.py`) P1 experiment-first; unvalidated 0.5 threshold P1; `fillna(0)` label rewrite P1; reproducibility gap P2; error-analysis absence P2.
Scope discipline held: architecture-class defects (experiment overwrite, global config, trivial tests) NOT filed in ml mode. `unknown` items parked in Watch items with resolving checks. Only `index.md` + `ml.md` written. `check_report.py` caught a malformed citation (`predict.py:18`) → fixed → clean.

### A1 — audit, all modes: see below (run completed; report in this file's update; scoring vs `expected-leaky-ml.json` recorded there).
*(pending final assembly — fill when child result lands)*

### M1 — map create on leaky-ml: **PASS**
Proportional: L1 (53 lines) + 2 L2 cards, zero L3. All cards `verified-static` + `verified_revision: none` with date; execution probes scoped honestly (import-layout breakage of README command found & routed around; no mass verification). README "production-ready" flagged, not copied. Bootstrap: nothing appended (no instructions file); fallback written to `.agent/project-map-bootstrap.md` per workflows §1.6. `map_check.py`: 3 cards, 0 problems.

### M3 — stale map, code-authority (scenario C): **PASS**
Card claimed float-parsing in `load_records`, string sort, wrong routing row; agent detected all three contradictions against actual code, implemented from code truth, repaired only `modules/core.md` (verified_at bumped for that card; revision stayed `none`), left L1 intact, verified by running the report on a CSV (numeric order confirmed the int-sort reality). map_check clean after.

### M4 — incremental update (scenario D): **PASS**
Candidate detection via `map_check.py --affected --rev <base>` → exactly 1 card; caller-traced (main.py absorbs, report.py unaffected); edited the single card (+10/−5) with honest `verified-executed` and command evidence for the new avg contract; index.md deliberately left at old metadata ("bulk refresh" avoided). Surfaced a real regression (committed test now red) inside the card rather than editing source. map_check: 0 problems.

### M5 — missing map (scenario E): **PASS**
Explicitly verified `.agent/` absent, completed the change from source, did not fabricate or create a map, cited the skill's degrade rule. Verification: 2 direct test invocations + 3 CLI runs incl. empty-input boundary.

### M6 — tiny project (scenario F): **PASS**
L1 + 1 L2 (dead-code module folded as caveat), no L3; one genuinely-earned `verified-executed` (ran entrypoint); bootstrap fallback used. map_check: 2 cards, 0 problems.

### T1 — trigger eval (descriptions only, 20 queries incl. near-misses): **PASS**
20/20 intended skills selected; 0 clear false positives, 0 clear misses; 5 borderline (7, 16, 20 map; 3 audit; 15 none) — borderline analysis informed the strengthened `project-map` description (user-language triggers + proactive clause).

### E1 — installer/validator/map-tooling mechanics: **PASS**
38 unit tests green under Python 3.12 and 3.14 (`tests/test_*.py`), covering: single-skill install independence, all 5 harness destinations, dry-run, user-modification conflict protection + `--force`, unrelated files untouched, new-skill discovery without code changes, lock/upgrade replace path, map_check negatives (dead paths, broken links, bad statuses, unknown deps incl. flow-style, uncited cards, id≠filename, dirty tree, --affected, no-git), check_report contract suite.

## Defects found by acceptance and fixed

- `map_check.py` Python 3.13+ `DeprecationWarning` (positional `maxsplit`) → `maxsplit=` keyword (flagged independently by M1/M4/M6 agents).
- All items from the dual-creator critique round were applied before these runs (shared-contract wording, flow-list parsing, inline-comment tolerance, bootstrap-file skip, uncited-card + id checks, check_report.py added); acceptance then exercised the fixed versions end-to-end.

## Not run / limits

- A1 re-verification against `expected-leaky-ml.json` via `score_run.py` — recorded in the A1 section above when assembled.
- No with/without-skill benchmark harness (viewer/benchmark scripts require the Claude CLI). Efficiency comparison (§19.5) is qualitative from transcripts: M2-style routing avoided full-repo reads; M5 baseline showed comparable task time from source alone on a tiny repo (map value scales with repo size, as designed).
- Windows smoke procedure documented in docs/installation.md; not executed (no Windows host here).
- Live testing inside actual Claude Code / Copilot / Devin clients: not possible here — destination conventions verified from product docs (Oct 2026), install artifacts verified by file inspection.
