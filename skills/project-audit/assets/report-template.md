# Report Templates

Copy the skeletons below into the audit report. Lead with a short decision summary, then expose evidence and implementation detail progressively. Adapt lightly (merge, shorten, group) — the finding block's field set is required, its formatting is compact by intent. Replace `<...>`; delete template comments (`<!-- -->`) in the written output — `scripts/check_report.py` flags leftovers of both in mode reports. Check the index for leftovers yourself too. Older reports do not need reformatting to remain valid.

## index.md (run manifest — always written; omit cross-mode observations unless 2+ modes ran)

```markdown
# Audit — <project> — <YYYY-MM-DD> — modes: <architecture, ml, exploratory>

- Complexity tier: <tier> (evidence: <one line>)
- Environment: <git rev-parse --short HEAD / "no git">, working tree <clean|dirty>
- Run id: <run-id>

## Executive summary
<3-6 sentences: overall assessment relative to tier; most consequential supported risks; sound areas worth preserving; first priorities; the coverage/evidence limit that most affects the conclusion. Do not turn a sampled audit into a project-wide verdict.>

## Audit at a glance
| Mode / report | Assessment within scope | Leading finding IDs / priority | Evidence basis and limits |
|---|---|---|---|
| [Architecture](architecture.md) | <short assessment, not a score> | <IDs + priority, or no significant findings> | <static / executed / inferred; important unverified area> |
<Use one row per mode that actually ran; replace the example mode and report link as needed.>

## Coverage
Inspected: <areas/paths and depth>. Not inspected (deliberate): <areas + reason>.
Evidence collected: <source sample; commands + actual results, or explicitly not executed and why>. State mode omissions (for example, no ML component) and their reason. Link mode reports for detailed coverage rather than duplicating it.
Verification limits: <claims/flows checked against current source; test files merely located versus assertions read; structural checker result, not semantic proof>.

## Sound areas to preserve
- <verified strength + citation or report-section link; limit the claim to what was checked, or say none established in scope>

## First priorities
1. <finding ID + report link; why first; act after acceptance, experiment first, or await a decision/trigger>
<Use only supported priorities; if none, say no action is justified by this audit. Do not invent findings to fill the table or list.>

## Top findings
| ID / detail | Title | Priority | Confidence | Evidence | Status |
|---|---|---|---|---|---|
| [AUD-ARCH-001](architecture.md#aud-arch-001--concise-title) | <title> | P1 | high | verified-static | draft |
<Include top findings per mode; use actual heading anchors. With none, state that explicitly instead of retaining the example row.>

## Cross-mode observations
<Interactions between findings across audits, referencing IDs. Keep to a few lines.>

## Reports
- [Architecture](architecture.md) · [ML methodology](ml.md) · [Exploratory](exploratory.md)  <include only files that exist>
```

## Per-mode report (architecture.md / ml.md / exploratory.md)

```markdown
# Audit <#N — name> — <project> — <date>
Mode: <mode> · Run: <run-id> · Tier: <tier> · Baseline: <git sha or "no-git">

## Executive summary
<3-6 sentences: overall assessment relative to tier, biggest supported issues, sound areas, first priority by ID, and the main evidence/coverage limit. This report should be usable without reading index.md.>

## Findings at a glance
| ID / detail | Problem | Priority | Impact | Recommended action / gate | Evidence |
|---|---|---|---|---|---|
| [AUD-<MODE>-001](#aud-<mode>-001--concise-title) | <title> | <P0-P3> | <who pays and how, briefly> | <concrete action; upon acceptance / experiment / decision / trigger> | <verified-static/verified-executed/inferred> |
<Use actual finding IDs and heading anchors, with metadata matching the detailed blocks. If there are no significant findings, say so and remove the example row; keep coverage, watch items, and the handoff section.>

## Coverage and evidence
Inspected: <mode-specific paths, symbols, flows, tests, and depth>.
Boundary/config coverage: <flows checked; link finding/sound-area traces rather than repeating their evidence>.
Not inspected: <areas + reason; state limits on absence claims>.
Tests located/read: <paths located; assertions/setup/mocks inspected and actual scope, or not read>.
Executed: <command + actual result, or not executed + reason>.
Evidence limits: <what remains inferred or unknown; no fabricated coverage percentages>.

## Sound areas to preserve
- <what was verified and why it matters at this tier; cite source or command + result; no generic praise or inference from missing findings>
<If no sound area was established, say so without implying that none exists.>

## First priorities
1. <ID + brief sequencing reason and prerequisite; refer to the finding for action, trade-offs, and validation>
<Do not repeat the finding's reasoning here; use no action justified when appropriate.>

## Findings

### AUD-<MODE>-001 — <concise title>
status: draft · priority: <P0-P3> · confidence: <high|medium|low — one-line reason> · evidence: <verified-static|verified-executed|inferred>

<!-- The evidence field takes one of those three: it describes how the *observed* claim was established. `proposed` is the role of the whole Proposed action (never of Observed); audit-only `unknown` items go to Watch items below, not into a finding. -->

- **Observed:** <what current code does, cited: path::symbol / path:line / command+result; include producer → consumer or defaults → overrides → use traces when consequential>
- **Evidence scope:** <limits specific to this finding; for absence claims, searched paths/equivalent mechanisms; link shared baseline/commands above and distinguish static from executed parts without repeating traces>
- **Impact/risk:** <who pays and how>
- **Root cause / plausible explanation:** <observed or labeled as inferred>
- **Proposed action:** <concrete; this is a proposal, not current state>
- **Why it helps / trade-offs / simpler alternative:** <compact, one line each; include the context-sensitivity gate answers>
- **Scope:** <approx: XS single function / S one module / M cross-module / L restructure>
- **Validation:** <how to prove the fix works: test, metric, command>

<ml mode uses instead — fields correspond 1:1 to the eight-step chain in references/ml-methodology.md §3 (Observed = step 1, confidence line = step 7, Category = step 8):>
- **Rationale:** <confirmed (cite doc/commit) | inferred (not documented): ...>
- **Assumptions the choice relies on:** ...
- **Failure mechanism:** ...
- **Alternative & how it could hurt:** ...
- **Decisive experiment:** <protocol, baseline, guardrail metric>
- **Category:** justified-now | experiment-first | research-gap

## Watch items / unknowns
<uncertain observations, research gaps: question, why it matters, cheapest resolving check>

## Coding agent handoff
Before coding, re-read the cited files — this handoff points at code, it does not replace reading it. Findings remain proposals until reviewed and accepted; acceptance is not implementation.

### For AUD-<MODE>-001
- Touch points: <path::symbol list>
- Invariants observed: <cited>
- Modification boundary: <what not to break; dependents verified: <list> or inferred>
- Suggested order: ...
- Tests/verification before & after: <reference this finding's Validation or Decisive experiment; add only setup/baseline/after-change details not already recorded>
- Requires user approval: <yes: what | no>

<exploratory mode adds per finding: assumptions to verify before implementing.>
```

Keep diagnosis, rationale, recommendation trade-offs, and experiment protocols in their finding blocks. Use IDs and section links from summaries and handoffs; add implementation-specific boundaries, sequencing, and approval decisions only. Keep mode-specific handoff details from the selected reference. For zero findings, retain **Coding agent handoff** with an explicit statement that no implementation is proposed.

## Lifecycle metadata

Each finding carries a `status:` line, edited by humans/agents over time:
`draft → reviewed → accepted | deferred | rejected → implemented-verified`
- `accepted` means a decision to do it — never rewrite the "Observed" section as if it were done.
- `implemented-verified` requires citing the implementation (path/commit) and the verification (command/test). Add a line to the finding rather than a new file.

## Priorities and IDs

P0 = correctness/data-loss/leakage-class risk active now; P1 = significant pain or risk with evidence; P2 = worthwhile improvement; P3 = hygiene/observation. IDs are stable per run (`AUD-ARCH-001`, `AUD-ML-002`, `AUD-EXP-001`); keep numbering when editing a report so cross-references survive.
