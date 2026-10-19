# Source verification and workshop quality — executed results

Run date: October 18, 2026 (local EDT; source attachment uses October 19 UTC).
Working-tree implementation based on `main`; no commit or push was requested.
Procedure and evaluator key: [source-verification.md](source-verification.md).

## Environment and evidence boundaries

Fresh generic subagents received a scratch project, one independently installed
skill, and the task prompt—not the evaluator key. The fixture uses stdlib Python
and an unavailable private transport. These are supplied-skill agent runs, not
native client discovery or cross-harness certification. Source application/tests
were not changed by generators (S3's tuple refactor was evaluator setup).

Scratch root: `/home/ghgin/.hermes/cache/scratch/source-verification-4216uioa`.
Durable raw outputs, snapshots, checks, and evaluation notes are retained in
[source-verification-evidence.json](source-verification-evidence.json); relative
artifact paths in those snapshots refer to their original scenario project.
The JSON is evidence data, not a new runner, schema, index, or runtime dependency.

`prompt3.pdf` was not supplied/discoverable in the available attachments. The
workshop changes use the user's detailed extracted requirements, not a claimed
reading or evaluation of that PDF.

## Executed source-verification scenarios

| Scenario | Actual result | Evidence and limits |
|---|---|---|
| S1 create, false README | Pass | L1 plus two L2 cards; generator/integer-cents contract and duplicate-preserving flow; all local app bodies read; plugin guarantees unknown. One existing regression passes, explicitly not ingestion/delivery coverage. |
| S2 semantic validate | Pass | Repaired false ingest despite valid metadata/paths; traced main/core consumer; scoped probes support ingest claims. Original core/delivery cards remain byte-identical; index retains its older baseline after partial repair. |
| S3 interface fan-out | Pass against source-based scope; initial evaluator qualification below | Detected tuple return versus dictionary CLI/test; documented the one expected test failure and mocked CLI TypeError. Traced forwarded tuple into delivery. Ingest card preserved byte-for-byte; inspected downstream delivery card updated. |
| S4 audit, stale docs/map | Pass within fixture scope | Two distinct draft findings on duplicate semantics and wrong ingest interface, grounded in current source and a saved mock-boundary probe. Missing private transport guarantees remain unknown rather than declared absent. All 21 pre-existing files unchanged. |
| S5 map/audit lifecycle | Pass | Accepted audit record remains byte-identical (387 bytes). Map distinguishes present cents implementation from the required real-transport CLI validation that has not run; no audit lifecycle promotion. |

S3's initial rubric incorrectly assumed delivery was unrelated and expected it
unchanged. The independent evaluator flagged that literal criterion. Reading
`main` establishes that the refactored summary is passed unchanged to `publish`,
so delivery is a consequential consumer and was actually inspected. The rubric
now permits that grounded update; this is an evaluator correction, not a hidden
regeneration or parent edit to the output. The real invariant—no refreshing
uninspected cards—holds; S2 separately demonstrates exact untouched-card preservation.

Mechanical map/report checkers were also run by the generators and independent
evaluator. Clean structure does not establish semantic truth. No unsupported
new `verified-*` claims were found by the independent semantic evaluator within
the declared scopes. The planted original ingest label is deliberately false.

## Executed workshop scenarios and iterations

- **W1 live-code preparation:** Both initial broad runs correctly distinguish
  inspected local behavior, executed one-test coverage, and private-plugin
  unknowns. They put delivery architecture before dependent retries, isolate
  established regression discipline from proposed version notes, and use only
  Open/Proposed decisions. Explicit `team-review/` destination is respected.
- **Independent readability review:** The second broad guide has a 189-word
  opening (about 1.1–1.5 minutes at illustrative 130–170 words/minute), correct
  ordering and evidence, but its 1,707-word guide and dense register remain
  verbose. Compound exact-choice questions were also flagged. This triggered
  another skill revision: one primary choice per block, shared caveats once,
  optional secondary evidence, and short five-column register defaults.
- **W1 fresh compact rerun: pass with readability limits.** The parent read both
  actual outputs against source: four concise primary choices, global-before-local
  order, separate general practices, no invented approvals, and no implementation
  plan. The guide is 1,364 words versus 1,707 (20.1% shorter); register 242 versus
  481 (49.7% shorter). Its 214-word opening is compatible with about 1.3–1.6
  minutes at illustrative 130–170 words/minute. All 33 file/anchor links resolve;
  all seven app/test files remain byte-identical. This final compact sample was
  parent-reviewed after the earlier independent reviewers' feedback; it did not
  receive another independent reader or human study. Repeated uncertainty reminders
  remain, but exact-choice questions no longer bundle the evidence checklist.
- **W2 initial focused preparation: failed scope discipline.** It truthfully
  labeled document-only design but expanded delivery/retry into money/version-note
  decisions. The parent did not edit it into a pass. Added an explicit rule that
  extra questions in inputs do not expand a focused user request.
- **W2 fresh rerun: pass.** Only D-001 boundary and D-002 dependent retry decisions;
  money/version-note items explicitly out of scope. Document-only claims remain
  unverified implementation, including the outbox/inline ambiguity. No code,
  measurements, threshold, or team approval was invented.
- **W2 consolidation: pass.** D-001 stays Open. Memory-only state is a Rejected
  option without closing all retry-state choices; limits are Deferred until
  failure rates are measured. Stable two IDs, original and meeting-note
  provenance retained. Proposed version notes do not become Agreed. Guide bytes
  are unchanged; the register explicitly becomes authoritative for meeting outcomes.

The wide and focused examples are independent generations, not successive
parent rewrites of a single guide. Reviewers read the actual artifacts and
source. Timing/readability assessments are agent review and word-count estimates,
not a timed presentation or human comprehension study.
No generated guide or register was parent-edited to manufacture a pass; skill
changes were followed by fresh generation. Consolidation edits were generated
from the supplied meeting notes and checked against the saved preparation snapshot.

## Concrete mechanical regression found during acceptance

The S4 generator encountered `check_report.py` stripping the leading dot from
`.agent/project-map/...` citations. It honestly recorded a notation workaround.
A new test reproduced the failure before the fix. The checker now preserves
literal citation paths; the same test verifies both an existing hidden path and
its deletion. Other added regressions demonstrate that a false but validly cited
map/report can pass a structural checker, execute the fixture's actual ground
truth, and check workshop discovery/profile/catalog integration. Independent
installation/resource copying is exercised for map and audit as well as workshop.

## Commands actually executed after implementation

- `python tools/validate.py` → `result: OK (0 problems, 0 warnings)`.
- `python -m unittest discover -s tests -v`, Python 3.14.7 → **72 passed**.
- `/usr/bin/python3 -m unittest discover -s tests -v`, Python 3.12.3 → **72 passed**.
- `/usr/bin/python3 tools/validate.py --creators ../skill-creator/skills` → both
  actual creator validators pass for all six discovered skills; zero problems/warnings.
- `git diff --check` → clean. The validator checks bundled references and top-level
  skill length; the unit suite checks standalone copying and installer lifecycles.

The fixture has one passing test normally. S3 intentionally has one failing test
after the evaluator's interface change; that observed failure is expected scenario
evidence, not a failure of the toolkit's 72-test suite. No real external transport
or end-to-end production delivery was exercised.

## Remaining limitations

No PDF inspection, native client activation, production transport, large-map
scaling measurement, or empirical human study. Scoped validation was exercised on
a small map, not claimed as whole-map proof after sampling. There is no no-skill
baseline or statistical estimate of reliability across models. Agent instructions
cannot mechanically guarantee that every future execution inspects the right
source; the behavioral evidence here is finite and explicitly scoped.
