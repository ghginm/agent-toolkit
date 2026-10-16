# Documentation workflow acceptance

Use the fresh-context procedure in [README](README.md). Create temporary projects
under the environment's scratch directory (use `tempfile`, honoring `TMPDIR`),
not in canonical fixtures or unrelated repositories. Install named skills using
the ordinary installer; run from installed resources without reading toolkit
files at runtime. Keep generated artifacts for independent inspection. These
checks exercise agent behavior, not native harness activation or a human study.

## D-A — Summary-first audit compatibility

Run A1 on a scratch `leaky-ml` project with the revised `project-audit`; reuse
an M1 map if available. Prompt: "Audit this project — architecture, ML methodology,
and anything open-ended. Cite evidence."

- Read `index.md` first: purpose/scope/tier/baseline, inspected and uninspected
  areas, consequential findings and first actions, sound areas with evidence,
  execution vs static vs inferred vs unknown are visible without detailed reading.
- Each mode report starts with a compact executive summary and findings table
  linking full details. Details retain evidence, lifecycle, confidence, priorities,
  context gate, and the eight-step ML reasoning chain.
- Handoffs reference finding IDs, real touch points, invariants, boundaries,
  sequence, validation, and approvals; they do not repeat full finding reasoning.
- Run installed `check_report.py --project PROJECT --run RUN`; run A1 citation
  scoring and manually review scope/methodological depth/proportionality.
- Existing-format reports still pass the checker (unit regressions); do not
  force new presentation fields on historical valid reports.

## B1 — Reuse technical artifacts for human synthesis

After M1 and D-A, install only `project-brief` into the same scratch project;
other installed skills may be removed, but preserve their output artifacts.
Prompt: "Create a human-readable project guide for a new teammate. Reuse the
existing map and audit selectively; explain the current pipeline, development
status, top problems, and next steps. Write docs/project-brief/."

Record which map cards and findings were read; L1 first, only useful L2/L3,
never the entire map as a prerequisite. Check source when evidence is stale,
contradictory, or insufficient. Missing data is a dependency, not a fabricated
training failure or invented score.

Evaluate the generated overview, pipeline, and roadmap against eight questions:

1. What problem does it solve?
2. How does it work end to end?
3. What has been built?
4. What is not implemented or verified?
5. What are its most consequential current problems (three if supported)?
6. What should the team do next, and why?
7. What is current architecture versus a proposal?
8. Where is deeper technical evidence?

Give an independent reader agent only the generated documents first. Ask it to
answer these questions with section citations, without opening maps or audits.
Then independently check its answers against source and the planted-defect key.
Record concrete answers, gaps, and refinements, not just a readability verdict.
Do not equate this agent-based review with empirical new-teammate testing.

Additional checks: real diagram edges and text fallback; no invented metrics,
progress percentages, author intent, or implementations; traceable substantial
claims; valid relative links and finding anchors; date/revision and stale-source
warnings; proposals separate; overview roughly 400–700 words or shorter when
appropriate; no external Atlas dependency. Preserve a representative generated
example with resolvable evidence links, not a manually invented substitute.

## B2 — Standalone, source-only, proportional refresh

Copy `map-sample` without `.agent/`; install only `project-brief`. Prompt:
"Explain this invoice-reporting project to a new teammate: what it does,
current pipeline, what is built or not verified, and next steps. Put the guide
in docs/project-brief/. No external Atlas is supplied."

Check three output files and the same evidence/presentation rules as B1. Do not
create maps/audits or require their skills. Modify a scratch source comment
without changing useful project facts: a refresh should leave guide bytes
unchanged. Also exercise a meaningful behavior change and request a focused
refresh; change affected capability/pipeline/roadmap sections and dependent
links/edges only, preserving unrelated authored content and older baselines.

## B3 — Stale and mixed-revision sources

In a scratch copy of B1, change a behavior referred to by a map/audit while
leaving those artifacts untouched. Ask to refresh only affected guide sections.
Check actual source wins, old findings are marked superseded/stale where
appropriate, unresolved evidence is labeled uncertain, untouched sections retain
honest older scope, and the skill does not silently update audit/map lifecycle.

## T2 — Description-level routing

Use only skill names and descriptions to classify realistic positive and
near-miss queries: onboarding/overview/status/pipeline/synthesis → brief;
evidence-producing project audit → audit; agent navigation/drift cards → map;
one-function explanation, ordinary test rerun, isolated implementation → none
of these. Record the queries, expected labels, predictions, and limitations.
This does not establish automatic invocation in Codex, Claude, or other clients.

## Recording results

Record date, skill baseline/dirty scope, absolute artifact paths, exact commands
and observed results, checks performed, failures/refinements, and limitations in
`documentation-results.md`. Distinguish unrun scenarios from passes; a small
fixture and agent reader cannot prove human readability or large-project scale.
