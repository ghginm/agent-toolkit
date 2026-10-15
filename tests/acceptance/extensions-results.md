# Workflow extension results — 2026-10-15

Scope: `agent-efficiency`, `tidy-dev`, and the optional `focused-changes` policy.
Cases and rerun procedure: [extensions.md](extensions.md). No native client
activation or measured efficiency improvement is claimed.

## Mechanical checks

| Check | Executed result |
|---|---|
| Baseline before additions | 40 unit tests passed; existing two skills validated |
| `python tools/validate.py` after changes | All four skills; OK, zero problems/warnings |
| Both creators' `quick_validate.py`, invoked directly per skill | All eight creator/skill combinations passed; edited tidy-dev rechecked afterward |
| `/usr/bin/python3.12 -m unittest discover -s tests` | 42 tests passed |
| `python -m unittest discover -s tests` (Python 3.14.7) | 42 tests passed |
| Independent packaging regression | Each new skill discovered, validated, and installed from a source root containing only that skill; copied bytes matched; no sibling skill, policy, artifact, or instruction change |
| Policy append | Unit check plus actual documented Bash append in scratch; original instructions preserved, policy appended verbatim |
| Resource/independence check | One SKILL.md per new skill, 113/93 lines; no runtime files, cross-skill reads, or mandatory root tooling |
| Local documentation links and `git diff --check` | Passed |
| Existing work | Nine pre-existing diff sections outside the three extended docs remained byte-identical; edits to those docs were additive, targeted patches |

At the time of the extension checks, the optional creator helper ran only the
first selected skill while labeling all selected names. Direct calls above
avoided that misleading summary. The focused correctness pass below fixes it.

### Final toolkit correctness pass — 2026-10-15

The earlier 42-test results are historical. No skill workflows or installer
code changed in this pass; no behavioral scenarios or benchmarks were rerun.

| Command / check | Executed result |
|---|---|
| `python tools/validate.py` | Four skills; OK, zero problems/warnings |
| `python tools/validate.py --creators ../skill-creator/skills` | Actual upstream scripts invoked independently; all eight creator/skill pairs PASS, exit 0 |
| `python -m unittest discover -s tests -p test_validate.py -v` | 16 tests passed, including 11 new creator regressions |
| `python -m unittest discover -s tests` (Python 3.14.7) | 53 tests passed |
| `/usr/bin/python3 -m unittest discover -s tests` (Python 3.12.3) | 53 tests passed |
| Temporary validator: project-audit passes, project-map fails | First check PASS, second FAIL, final FAILED, process exit 1; test initially reproduced false PASS / exit 0 before the fix |
| Other creator regressions | All four skills with both creators; first failure continues; mixed creator results; crash/abnormal exit/launch error/timeout; missing creator/interpreter; built-in failure preserved; no false PASS for unexecuted checks |
| Archive exclusion | Isolated Git tree with eight deliberately tracked root/nested cache paths: `git archive --format=tar.gz` excluded every cache and retained source |
| Git hygiene | No tracked Python caches; intended skills, policy, documentation, tests, and tools tracked in index; new source files staged without committing |
| `AGENTS.md` consistency and `git diff --check` | No fixed two-skill assumptions; no whitespace errors |

Creator checks remain optional. Missing tooling is SKIPPED; validation failures
and execution errors fail the run without suppressing remaining checks.

### Installer selection defaults — 2026-10-15

A later requested installer change makes no-selection installs equivalent to
`--skills all --profile all`, with the existing `generic` harness default.
Explicit selectors limit selection; supplying both combines their skill lists
without duplicates. `--profile all` alone selects all profile members, not all
unprofiled skills. README and installation examples now use the short default
command. No skill workflows or behavioral scenarios changed.

| Command / check | Executed result |
|---|---|
| `python -m unittest discover -s tests -p test_install.py -v` | 18 tests passed; eight new regressions cover defaults, explicit `all`, profile unions, limited selections, deduplication, discovery without profiles, dry-run, and unknown selections |
| `python tools/validate.py` | Four skills; OK, zero problems/warnings |
| `python -m unittest discover -s tests` (Python 3.14.7) | 61 tests passed |
| `/usr/bin/python3 -m unittest discover -s tests` (Python 3.12.3) | 61 tests passed |
| `python tools/install.py --help` and `git diff --check` | Selection defaults documented; no whitespace errors |

## Fresh-context scenario responses

Separate agents received each skill and its scenario group, formulated actual
responses, and graded against visible criteria. The parent reviewed those
responses and checked IDs, uniqueness, and pass totals programmatically. This is
scoped instruction-following evidence, not blind grading or a baseline comparison.

| Case | Response evidence (condensed) | Result |
|---|---|---|
| E2 | Weekly reconstruction justifies considering reuse; inspect existing conventions first; compare verification/maintenance costs; no assessment-only edits | Pass |
| E3 | Use supplied `make validate ENV=staging CONFIG=local.toml`; do not create duplicate script | Pass |
| E4 | Tests after meaningful edits and refreshed source reads are not waste | Pass |
| E5 | Stop equivalent retries; inspect interpreter, environment, import resolution before another fix | Pass |
| E6 | Whole-session tokens/cost unknown; visible sample cannot establish totals; offer bounded behavioral diagnosis | Pass |
| E7 | Preserve 2.5 ACUs, 18 tool calls, 40% context utilization; no token/cost/quota conversion | Pass |
| E8 | No efficiency activation for a condition change and before/after tests | Pass |
| E9 | Keep measured 1200 input/300 output; 200 cache-read included in input; 90-token sample estimated, omitted context explicit; no extrapolation | Pass |
| D1 | No tidy; assessment makes no edits; recommend direct condition and focused tests when authorized | Pass |
| D2 | Tidy first: extract local parsing once, preserve errors/order, test extraction before third branch | Pass |
| D3 | Happy-path tests do not prove equivalence; authorization/side-effect order needs coverage or deferral | Pass |
| D4 | Leave unrelated module duplication outside the bug fix; propose separately | Pass |
| D5 | Read-only mixed-diff assessment; no commits, resets, or reconstruction losing user edits | Pass |
| D6 | Keep explicit functions, unittest and existing Make conventions; no strategy registry or forced commit format | Pass |
| D7 | Fix and verify urgent validation first; optional tidy afterward or defer | Pass |

Totals: efficiency **8/8**, tidy **7/7**. Policy review passed: concise directly
usable instructions, no numeric limits/dependencies/enforcement, and explicit
allowance for security, realistic failures, tests, useful modularity, and justified
complexity.

## Trigger checks

A separate agent classified Q1–Q20 using names/descriptions, not skill bodies.
Stored classifications matched the grading key **20/20**: Q1–Q5 efficiency,
Q6–Q10 tidy, Q11–Q20 neither. This tests model-judged metadata suitability, not
native harness discovery, invocation probabilities, or interactions with every
other skill in a client's catalog.

## Operational coding check

Scratch project: `/home/ghgin/.hermes/cache/scratch/atk-tidy-dev-1let53e4`.
Only `tidy-dev` was installed; map artifacts were absent. The agent chose **no
tidy**, changed only `app/core.py` and its test, and added `average_per_invoice`
with two-decimal formatting and an empty-input guard. No new abstractions.

The copied fixture originally used a pytest-style function: initial Python 3.14
unittest discovery ran **zero tests**, exit 5, not a passing baseline. The agent
adapted that scratch test to stdlib unittest, established one passing baseline,
observed failing average/empty-input regressions, then obtained two passing tests.
CLI checks returned `average_per_invoice=7.50` and `average_per_invoice=0.00`.
This fixture adaptation is an evaluation limitation, not evidence that changing
a real project's test framework is desirable.

The parent inspected the complete diff, updated the isolated installation to the
final skill version, reran both tests successfully, matched installed skill bytes,
verified the unrelated note's SHA-256 stayed unchanged, and confirmed canonical
fixture source/test bytes still match HEAD. Scratch evidence can expire; this
page retains the commands, decisions, results, and limitations.

## Creator review and refinements

| Guidance | Review / applied refinement |
|---|---|
| OpenAI creator | Single-file scope and contextual freedom accepted; qualified the behavioral classification as algorithm **behavior**, not every algorithm replacement |
| Anthropic creator | Explanation, selective triggers and honest usage accepted; clarified D1 criteria to recommend implementation while remaining read-only |

Descriptions were unchanged by these refinements. The recorded D1 response
already explicitly made no edits and meets the clarified criterion; its response
was re-reviewed. Final validators, unit suites, and operational tests ran after
the changes. Creator scaffolds were generated only in scratch; harness-specific
presentation files were not shipped. Upstream tidy-first README, skill, catalog,
and MIT license were reviewed; new skill prose is independently written.

## Limitations

- Native Codex/Claude/Devin/Copilot discovery and activation were not exercised.
- Supplied-session scenarios do not establish whole-session telemetry accuracy,
  measured token savings, or comparative efficiency gains.
- Authorized automation creation is covered by decision/authorization guidance
  and scenario responses, not by a separate generated-script operational run.
- Existing architecture and audit/map workflows were not behaviorally rerun;
  this task left their content/tools untouched and ran their unit regressions.
