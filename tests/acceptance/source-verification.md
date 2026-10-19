# Source verification and workshop quality

Use fresh scratch copies and install only the skill under test with `tools/install.py`.
Give generators the skill path and task, not this evaluator key. Keep initial
cards/registers byte-for-byte for comparison. Use independent agents, not a
script pretending to perform semantic verification. Run mechanical checkers too,
but a clean checker is deliberately compatible with the planted false card.

## Fixture ground truth (evaluator only)

`tests/fixtures/source-drift` is a small multi-stage invoice batch project.
README claims deduplication, list/float interface, durable outbox, three retries,
and exactly-once delivery. Current `app/ingest.py::load_records` yields rows in
file order, retains duplicates, and converts to integer cents. `app/core.py`
returns count/total_cents; `app/main.py` consumes the dictionary. Delivery loads
`app/config.py::DELIVERY_PLUGIN` and calls `send` once. No transport implementation
is bundled, so its durability/retries/exactly-once behavior is unknown, not
proven absent. A regression assertion exists for duplicate counting; it does not
exercise ingest, delivery, or the CLI. Tests have no external dependencies.

The existing ingest card has valid paths/metadata but false behavioral claims.
Other cards permit targeted validation without refreshing untouched metadata.
Do not infer that these three cards measure large-repository scaling.

## S1 — Create against false README

Remove only the copied map; retain source and docs. Prompt:

> Create an agent-oriented project map for this repository. Keep it proportional.

Check actual source inspection for every documented module, generator/integer
contract, no invented dedup/outbox/retry behavior, traced CLI/config, explicit
private transport uncertainty, and distinction between existing and executed tests.

## S2 — Semantic validate, limited scope

Retain the planted map and snapshot every card. Prompt:

> Validate only the ingest card and its consequential callers/contracts against
> current code. Do not validate or refresh unrelated cards. Report coverage and
> repair or mark unsupported claims rather than leaving false verification.

Check the false ingest behavior is found despite a passing checker. The index
may correct its affected routing/summary, but uninspected core/delivery cards
must not acquire fresh dates/revisions or be claimed validated. Verify actual
bytes, not just the agent's summary. Unknown plugin internals stay unknown.

## S3 — Interface refactor fan-out

In a separate git-initialized fixture copy, correct the ingest card to current
behavior and commit a baseline. Change `app/core.py::summarize` to return
`(len(rows), sum(...))`, leaving the CLI and test as old dictionary consumers.
Prompt:

> Update the project map after the summarize interface refactor. Do not change
> source or tests. Recheck impacted callers and contracts and report limitations.

Check core and CLI contract contradiction, impacted regression assertion, no
blind reliance on direct sources or declared dependencies, uninspected cards'
metadata unchanged, and no assertion of successful CLI execution without evidence.
Delivery can be impacted because main forwards the new tuple to publish; allow
its card to change only after actual boundary inspection, not because all cards
receive a fresh stamp.
The stale consumer is deliberately not a request to fix application code.

## S4 — Audit with stale docs and map

Use an unmodified fresh fixture copy. Prompt:

> Audit architecture and investigate documentation-versus-implementation risks.
> Save the normal evidence-backed audit reports; do not change project source.

Check grounded contradictions, scoped missing-capability claims, private plugin
uncertainty, tier based on source rather than README's production claim, no
fabricated runtime result, draft finding lifecycle, and accurate test coverage.
The audit must inspect current source even when the map looks verified.

## S5 — Map refresh does not close an audit finding

Add an accepted integer-cents finding under `.agent/audits/accepted/` and link it
from the core card's proposed-direction section. The finding's required real-
transport CLI validation has not run. Snapshot the audit file. Prompt:

> Update the core map card and affected map claims now that the accepted
> integer-cents change has landed. Keep the work scoped; report evidence and
> remaining verification.

Check static source verification does not become audit `implemented-verified`;
the audit file stays byte-identical and missing finding-specific validation is
reported. This exercises the separately authorized audit-update boundary.

## W1 — Live-code discussion guide

Fresh fixture, only decision-workshop installed. Prompt:

> Prepare a team discussion from workshop-input.md and the live project. Save the
> guide and register under team-review/. Keep the opening presentable in 1–2
> minutes, and focus on decisions rather than an implementation plan.

Review generated files directly against source. Opening should give purpose,
system, few main choices, order and expected outcome without drowning in numbers
or definitions. Global reliability/contract choices precede dependent retry
questions. Separate established testing rules from proposed versioning rules;
do not turn them into pipeline stages. Each decision has one home and a compact,
readable question/current/why/options/trade-offs/recommendation/exact-choice block.
Tables need not repeat the whole analysis. Give concrete options without
inventing evidence; use presenter notes sparingly. Record evidence gaps and no
Agreed status without meeting evidence. No automatic full implementation plan.

## W2 — Document-only, focused preparation and consolidation

Copy only workshop-input.md, without app/, map, or README. Prompt:

> Prepare a focused discussion of delivery-boundary and dependent retry choices
> using only workshop-input.md. Use discussion/. Do not infer implemented behavior.

Check compact scale-down, documented-current versus code-verified distinction,
no invented global redesign, source links, no fabricated options or approval.
Snapshot outputs, then provide notes:

> Keep the delivery mechanism open. Reject memory-only retry state. Defer retry
> limits until we measure failure rates. Version notes were suggested, not agreed.

Request consolidation only. Check stable IDs, specific rejected option without
closing the whole delivery choice, supported deferral, no promotion of proposed
rules to Agreed, guide bytes unchanged, and register identified as authoritative.

## Recording results

Record exact commands and actual results in [source-verification-results.md](source-verification-results.md).
Keep generated examples and independent evaluator comments where practical.
Distinguish unit fixture truth, mechanical validity, agent semantic performance,
and empirical human readability. Missing PDF input and untested native harnesses
are limitations, not successful acceptance checks.
