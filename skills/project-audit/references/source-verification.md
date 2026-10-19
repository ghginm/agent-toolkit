# Source verification for audit claims

Use in every mode, including when reusing a map or updating an existing report.
Select claims by consequence, not by how easy they are to cite. Keep this work
within the audit scope; reduce breadth when necessary rather than asserting
uninspected behavior.

## Before accepting a claim

- State the assertion precisely: current behavior, dependency, interface,
  effective config, invariant, missing capability, or sound area. Open the
  current implementation and read relevant bodies and branches. README text,
  comments, old findings, maps, filenames, and search results are leads, not
  proof that the assertion holds. Cite `path::symbol` or `path:line` supporting
  this claim, not merely a nearby file.
- For a boundary or impact claim, inspect the producer and actual callers or
  consumers. Trace an entrypoint through dispatch to the relevant output;
  a helper's definition/import does not establish its use. Follow config
  definition/default → loading and overrides → effective value at the consumer.
  Read competing branches when asserting unconditional behavior. Cite the
  connection; label unresolved reachability or impact `inferred`.
- For “missing X,” search plausible names and equivalent mechanisms; inspect
  likely entrypoints, registries, config, consumers, and relevant tests. Record
  search scope and what was actually read. Say “not found in the inspected
  paths/flow” with those paths, not “the project has no X” after a narrow grep.
  Missing evidence is not evidence of absence; use watch items (`unknown`)
  when the capability cannot be established in scope.
- Keep observed source facts separate from inferred failure consequences,
  documented intent, and proposed remedies. Confirmed rationale cites the
  author's documented rationale, not proof of present implementation.

## Calibrate evidence to what was done

- File existence establishes a location only. To describe test coverage, read
  assertions, fixtures/setup, mocks, skips, and which path is exercised.
  Label this `verified-static`; do not infer a pass or sufficient coverage.
- To use `verified-executed`, record the exact command, environment/baseline,
  observed result, and specific behavior exercised. Preserve failures, skips,
  unavailable inputs, and not-run reasons. A successful checker or smoke test
  does not execute the application's untested branches or verify an entire
  finding; keep static and inferred parts explicit within mixed evidence.
- Use only the existing evidence vocabulary: `verified-static`,
  `verified-executed`, `inferred`, `proposed`, and audit-only `unknown` for watch
  items. Keep finding evidence fields within the template's three choices;
  no new “test-exists” or “partially-verified” status is needed.

## Before publishing or refreshing

- Record inspected claims/flows, paths and depth, uninspected boundaries, tests
  read, and commands/results separately in each mode's coverage. Summary and
  sound-area claims meet the same evidence bar as findings. A revision is a
  baseline, not a correctness certificate; include relevant dirty paths.
- Recheck reused claims against current source before describing them as
  current. If retaining older report material, preserve its original baseline
  and evidence scope; annotate only rechecked claims with the newer baseline.
  Do not silently refresh finding evidence or lifecycle from a config change,
  accepted plan, or unrelated passing test.
- Run check_report for structural consistency, then review claim support and
  contradictions yourself. Existing citation paths and a valid report shape
  cannot prove source meaning, dependency completeness, or semantic truth.