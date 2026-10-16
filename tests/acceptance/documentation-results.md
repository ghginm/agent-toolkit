# Documentation workflow — executed evidence

Date: 2026-10-16. Toolkit base: `8daa24a884747fbcde79f122a39b048efa2cfddc`
plus the uncommitted documentation-workflow implementation. Tests below use
fresh generic subagents and scratch projects, not native harness invocation.
This is not a human newcomer study or a measured reading-time benchmark.

## T2 — Description-level routing

Queries and expected labels: [documentation-triggers.json](documentation-triggers.json).
A fresh agent extracted only names/descriptions and query text, saved predictions
before loading the expected labels, then compared in code. Result: **20/20**;
no mismatches. Predictions: queries 1–8 brief, 9–11 audit, 12–15 map, 16–20 none.

Raw artifact:
`/home/ghgin/.hermes/cache/scratch/t2-routing-667ca679d9344abca7a3a704ef89f9fb.json`.
The parent read the returned artifact. This is a simulated description judgment,
not proof of automatic triggering or reload behavior in any supported harness.

## Creator design review

Two independent reviewer agents read all three new brief resources, AGENTS.md,
and respectively the local OpenAI and Anthropic creator guidance. Neither found
an actionable gap. Reviewed dimensions included token cost, conditional resource
loading, standalone paths, triggering, synthesis boundaries, freshness, evidence,
visual-first structure, and proportional refresh. OpenAI UI metadata was
intentionally omitted for harness neutrality; creator code was not copied.

## B2 — Standalone source-only generation and no-op refresh

Scratch project:
`/home/ghgin/.hermes/cache/scratch/project-brief-b2-z9aegxsu/invoice-reporting`.
Detailed execution record: sibling `acceptance-report.md` in the scratch root.
The parent read the report and all three generated guide files.

- Only `project-brief` installed; no `.agent/`, map, audit, or external Atlas.
- Source inventory: README, all four application Python files, and the one test.
  Runtime synthesis used only those sources and the installed skill resources.
- Three documents produced; overview distinguishes CLI summary from the separate
  ID-file callable, static observations from test passes, unknown money/order
  requirements from proven defects, and current behavior from proposed changes.
- Checker observed 47 resolving relative link occurrences before/after update.
- A scratch-only comment in `app/report.py` left its AST unchanged. Refresh
  correctly kept all three guide files byte-identical; canonical fixture hashes
  remained unchanged. No application invocation or tests were run in this phase.
- Scope: generic fresh-agent instruction following on a small fixture, not native
  client discovery or empirical human reading speed/usability.

## B2 — Meaningful incremental refresh

The scratch invoice project then gained a third `average=…` summary line with
explicit empty-input handling and an updated existing assertion. A fresh agent
refreshed summary/capability/diagram/boundary/evidence sections and dependent
roadmap wording only, recording revision `none` and retained older section scope.
The parent read `meaningful-update-report.md` and `meaningful-update.diff` in the
B2 scratch root, then reran both verification scripts:

- `PYTHONDONTWRITEBYTECODE=1 python ../verify_meaningful_summary.py`: passed the
  existing test via a stdlib harness, empty-input and fractional-average assertions.
- `PYTHONDONTWRITEBYTECODE=1 python ../verify_meaningful_refresh.py`: **50** relative
  links resolve and **11** preservation checks pass; source/test parse, loader
  AST unchanged, ID-report prose, history, target proposals, and unrelated roadmap
  sections retained. Exact diff is recorded beside the report.
- Pytest could not start (`No module named pytest`); this was not a pytest suite
  pass. No CLI or report invocation was run. All source changes stayed in scratch.

## M1 — Agent map preserved

Project: `/home/ghgin/.hermes/cache/scratch/m1-project-map-xtmbx5yy/project`.
A fresh agent installed only `project-map`, read the eight supplied fixture files,
and produced L1 plus dataset/training/prediction L2 cards, no L3. All statuses
are `verified-static`, revision `none`; README readiness/accuracy claims remain
unverified. L0 was proposed only; project instructions and fixture source were
not edited. No application execution or dependency installation occurred.

The parent independently reran installed `map_check.py --repo PROJECT --map-dir
PROJECT/.agent/project-map`: exit 0, **cards checked: 4; problems: 0; notes: 1**.
The note correctly says git revision/dirty checks were skipped for a non-git copy.

## A1 + D-A — Summary-first audit on the mapped ML fixture

Run: `PROJECT/.agent/audits/20261016-1445-all`, using the M1 scratch project above.
Detailed execution record and raw scorer JSON are `audit-acceptance.md` and
`audit-score-run.json` in its parent scratch directory. The parent read all four
reports and independently reran the installed checker: **7 findings, 0 problems**.
Detailed findings are architecture 3, ML 3, exploratory 1; all draft, with unchanged
evidence/confidence/priority/lifecycle semantics. All three ML blocks retain the
eight numbered reasoning steps and local experiment/adoption gates.

Index and per-mode reports expose executive summaries, coverage/evidence limits,
sound areas, gated priorities, and linked details; mode glance tables give impact
and concrete action. Handoffs reference canonical findings/validation and add
touch points, observed invariants, boundaries, sequence, and approvals rather than
duplicating full methodology chains. No source or map edits; preservation hashes
match all eight input files and four map files. Historical-format compatibility
is covered separately by the parent unit suite, not asserted by this fresh run.

Actual runtime attempts were blocked: `python src/train.py` exited 1 for missing
sklearn; `python -m pytest tests/test_smoke.py` exited 1 for missing pytest. No
dependency installation, completed training, model metric, or test pass claimed.

The existing A1 scorer returned 12/12 filename/token matches, but its whole-report
matching attributes hits to the first report and counts watch-item mentions.
This is **not** a semantic 12-defect pass. It flags `data/churn.csv`, correctly
disclosed as a missing input, not an inspected source. Parent inspection confirms
leakage/split/evaluation reasoning is in ML, artifact contracts in architecture,
and unsupported readiness in exploratory. Unproven imputation/production harms
remain unknowns rather than fabricated findings. The scorer was not changed or
used to tune the reports; its limitations remain explicit.

## B1 — Human synthesis from map and audit

Outputs: `PROJECT/docs/project-brief/{README.md,pipeline.md,roadmap.md}` in the
M1 scratch project. Execution record: parent scratch `brief-acceptance.md`;
verification: `check_brief.py`, independently read and rerun by the parent.

- Read map L1, dataset and prediction L2 only; training card deliberately skipped
  because direct training source sufficed. No L3 or whole-map loading required.
- Read audit index, then bounded finding sections, not full mode reports; rechecked
  the eight small supplied source/docs files. External Atlas was not needed.
- Generated overview **450 words**, pipeline **724**, roadmap **758**, using the
  checker’s whitespace/Markdown-inclusive counts; not measured reading times.
- **39** relative links, **15** fragment occurrences, all **7** finding anchors,
  and **28** diagram edges pass mechanical checks. Parent inspection confirms
  current edges match source/file contracts, proposed edges are separate, and
  readable text fallbacks explain training versus callable prediction.
- All **16** source/map/audit files preserve their baseline hashes; no unexpected
  files beyond installed skill and requested guide. No project execution during
  synthesis; prior failed commands are explicitly attributed to the audit.
- No invented readiness/97% result, completion percentage, accepted fix, or
  historical rationale. Three immediate workstreams explain problems and gates
  without forcing readers through full findings. Mermaid rendering was not tested.

Demonstration archive: parent scratch `project-brief-demo.zip`, containing **19**
actual source/map/audit/brief files under `churn-demo/` and no installed tooling.
The parent verified archive integrity and every member against source bytes;
extract it together to preserve relative evidence links. Scratch paths are local
run artifacts, not durable installed-skill dependencies.

## B1 — Independent newcomer-proxy review

Reader artifact:
`/home/ghgin/.hermes/cache/scratch/newcomer-comprehension-cpid0qpr.json`.
A separate fresh reader saw only the three generated documents, not skills,
maps, audits, or source. It supplied concrete answers and section/line references
for all **8** acceptance questions; none required opening audits for the basic
answer. The parent read every answer, checked the count and sufficiency fields
in code, and compared claims to the source and audit already inspected.

The reader correctly reconstructed separate training and callable prediction,
full-input scaling versus fresh inference scaling, the classifier-only artifact,
static built capabilities, absent data/artifact, unverified readiness/97%, three
problem themes, gated actions, target design, and deeper evidence locations.
Open consumer/label/cost questions remained explicit rather than invented.
This is a useful scoped agent-reader check, **not empirical human-readability
or timed newcomer validation**; native harness activation was not tested.

## B3 — Stale and mixed-revision proportional refresh

Fresh copied project:
`/home/ghgin/.hermes/cache/scratch/b3-brief-refresh-pr9gk1mx/project`.
Evidence: sibling `report.md`, `acceptance.json`, `refresh.diff`, and preservation
artifacts. Only this temporary test copy received a local git baseline commit
(`f2c6e18eae8c53c22bdb2fc43f30fe31dbc17393`); the toolkit was not committed.
Planted uncommitted source change: threshold **0.5 → 0.8** in config only.

The parent read the report, exact guide diff and verification script, then reran
`python -B /home/ghgin/.hermes/cache/scratch/b3-brief-refresh-pr9gk1mx/verify_b3.py`:
**37 checks passed**, none failed; **50** relative links, **17** anchored occurrences
resolve. Current strict `> 0.8` is static-only and unvalidated; old map/audit 0.5
claims are explicitly stale. Actual SHA/dirty scope and retained older no-git
section scope are stated. Threshold adjustment is not presented as an accepted
policy improvement or resolution of AUD-ML-003. All **8** map/audit files and
unrelated guide content remain unchanged; all seven findings stay draft. Original
M1 project and installed resources remain unchanged. No training, predictions,
model evaluation, dependency installation, or toolkit commit occurred.

## Structural and regression checks

The initial toolkit validator and both optional upstream validators passed for
all five skills with zero problems/warnings. Final post-integration validation,
unit suites, and the other behavioral scenarios are recorded below only after
execution; their absence here does not mean they passed.

Parent integration verification: `python tools/validate.py` and
`python tools/validate.py --creators ../skill-creator/skills` both returned OK,
zero problems/warnings; all ten creator/skill combinations passed (none skipped).
`python -m unittest discover -s tests -v` (Python 3.14.7) and
`/usr/bin/python3.12 -m unittest discover -s tests -v` each ran **64 tests, OK**.
Coverage includes legacy/summary-first/zero-finding reports, standalone brief
copying and exact resources, profile union/subset selection, all five harness
path mappings, conflict/force behavior, and preservation of project instructions,
policies, map artifacts, and authored briefs. These are copy/mechanics checks,
not client runtime certification. `git diff --check` returned no errors.

Final rerun after implementation/demo generation: both validators and both
64-test interpreter suites passed again. A scratch Markdown check covered
**14** changed non-template Markdown files and **45** local links/anchors with
zero problems; copy-fill template placeholders were intentionally excluded.
All named documentation scenarios above were executed; no broad cross-harness,
large-project performance, rendered-Mermaid, or human-study result is implied.
