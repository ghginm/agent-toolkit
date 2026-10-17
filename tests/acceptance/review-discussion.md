# Deep review and decision workshop acceptance

Use the fresh-context scratch/installed-skill procedure in [README](README.md).
Do not treat unit string assertions or file-copy checks as generation quality.
Keep generated outputs and initial-register snapshots for evaluator inspection.
These scenarios test behavior with supplied skills, not native client discovery.

## R1 — Overview compatibility and standalone source synthesis

Copy `tests/fixtures/leaky-ml` into scratch and install only `project-brief`.
Prompt: "Give a quick human-readable overview of this project: purpose, current
pipeline, status, problems, and immediate priorities."

Check compact README/pipeline/roadmap outputs, high-level flow and priorities,
source evidence versus execution limits, and no prerequisite audit/map creation.
The existing overview template should remain unchanged.

## R2 — Explicit and natural deep-dive

Use two fresh copies of the same fixture with only `project-brief` installed.

- Explicit: "Use project-brief in deep-dive mode. Build a modular human-readable
  architecture and design review pack."
- Natural: "We need a comprehensive understanding of this legacy project before
  planning architecture changes with the team. Explain its design stage by
  stage, limitations, alternatives, historical requirements and unresolved
  choices in navigable human documentation."

Inspect actual output: compact overview first, navigable modules proportional
to complexity, actual data/training/persistence/prediction stages and interfaces,
current versus proposed diagrams, meaningful alternatives and trade-offs,
no invented historical requirements or intent, no unsupported runtime results.
External guidance must remain recommendation input, not repository evidence.
Do not require a fixed file count or judge depth by word count alone.

## R3 — Standalone discussion preparation

Copy `tests/fixtures/review-materials` into scratch, install only
`decision-workshop`, and initially withhold meeting-notes.md from the agent.
Prompt: "Prepare a clear team architecture discussion from architecture.md.
Begin with the whole current system, then alternatives and backbone choices,
then meaningful stages. Save Markdown guide and decision matrix. No slides,
implementation plan, or code."

Check current flow before proposed alternatives, major delivery/contract
choices before retry tuning, consistent stage discussion with plain-language
options/trade-offs, satisfactory validation left alone, linked decision matrix,
no manufactured agreements. Supplied current design is not code-verified.
The external advisory is not evidence of an implemented outbox or worker.
No other skill or prior brief may be used. Snapshot initial outputs.

## R4 — Consolidation with mixed outcomes

Then supply meeting-notes.md and prompt: "Consolidate these meeting notes into
the existing decision register. Preserve IDs, provenance, rejected alternatives,
deferred choices, and unresolved questions; do not infer agreements."

Check supported identifier agreement, delivery mechanism deferred with stated
measurement/budget conditions, in-memory retry option rejected without rejecting
all durable retries, five-second objective unresolved, exponential backoff not
agreed. Preserve IDs, initial rationale and provenance, unrelated documents,
and requirements implied by confirmed decisions without promoting interpretation
to independent approval. Diff against the snapshot.

## R5 — Documentation and packaging

Also exercise two narrow workshop requests with the revised installed skill:

- Focused preparation: "Prepare a focused discussion comparing retry policy
  options for the notification stage. Include only necessary context and
  dependencies; do not reopen identifier or validation decisions or produce a
  whole-system review. Markdown only." Use architecture.md without meeting
  notes. Check local options and dependencies without unrelated stages.
- Consolidation-only: copy the initial decision register into a fresh target
  without its guide. Supply architecture.md and meeting-notes.md and request:
  "Only consolidate M-01 notes into this register. Keep IDs and provenance;
  do not create a meeting guide or rewrite unrelated documents." Check that
  only the register changes and no guide is created.

Run toolkit validation with both actual local creator validators and unit tests
under available Python versions. The unit suite covers discovery, profiles,
standalone skill trees, all installer destinations, dry-run, idempotent update,
source updates, local conflicts/force, preserved outputs, bundled reference and
README/contracts links. Inspect the final diff: no map/audit redesign, installer
changes, runner/configuration, slide engine, or automatic code/planning output.

## R6 — Description routing

Use `review-discussion-triggers.json` as the evaluator's key. Give an independent
classifier only skill names/descriptions and query texts (not expected labels).
Classify as brief/workshop/neither, and overview/deep-dive for brief. Compare
predictions to the key programmatically. This is a description-level intent
check, not measured automatic invocation by Codex, Claude, or another client.

Record executed outputs, assertions, failures/skips and limitations in
[review-discussion-results.md](review-discussion-results.md). Generated documents
need evaluator evidence review; static checks alone are insufficient.
