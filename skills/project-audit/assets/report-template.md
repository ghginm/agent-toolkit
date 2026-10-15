# Report Templates

Copy the skeletons below into the audit report. Adapt lightly (merge, shorten, group) — the finding block's field set is required, its formatting is compact by intent. Replace `<...>`; delete template comments (`<!-- -->`) in the written output — `scripts/check_report.py` flags leftovers of both.

## index.md (run manifest — ALWAYS written; the cross-mode summary section appears only when 2+ modes ran)

```markdown
# Audit — <project> — <YYYY-MM-DD> — modes: <architecture, ml, exploratory>

- Complexity tier: <tier> (evidence: <one line>)
- Environment: <git rev-parse --short HEAD / "no git">, working tree <clean|dirty>
- Run id: <run-id>

## Coverage
Inspected: <areas/paths>. Not inspected (deliberate): <areas + reason>.

## Top findings
| ID | Title | Priority | Confidence | Status |
|---|---|---|---|---|
| AUD-ARCH-001 | <title> | P1 | high | draft |

## Cross-mode observations
<Interactions between findings across audits, referencing IDs. Keep to a few lines.>

## Reports
- [Architecture](architecture.md) · [ML methodology](ml.md) · [Exploratory](exploratory.md)  <include only files that exist>
```

## Per-mode report (architecture.md / ml.md / exploratory.md)

```markdown
# Audit <#N — name> — <project> — <date>
Mode: <mode> · Run: <run-id> · Tier: <tier> · Baseline: <git sha or "no-git">

<Executive summary: 3-6 sentences. Biggest issues, overall health relative to tier, what to do first.>

## Findings

### AUD-<MODE>-001 — <concise title>
status: draft · priority: <P0-P3> · confidence: <high|medium|low — one-line reason> · evidence: <verified-static|verified-executed|inferred>

<!-- The evidence field takes one of those three: it describes how the *observed* claim was established. `proposed` is the role of the whole Proposed action (never of Observed); audit-only `unknown` items go to Watch items below, not into a finding. -->

- **Observed:** <what the code does today, cited: path::symbol / path:line / command+result>
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
### For AUD-<MODE>-001
- Touch points: <path::symbol list>
- Invariants observed: <cited>
- Modification boundary: <what not to break; dependents verified: <list> or inferred>
- Suggested order: ...
- Tests/verification before & after: <commands>
- Requires user approval: <yes: what | no>
- Before coding, re-read these files — this handoff points at code, it does not replace reading it.

<exploratory mode adds per finding: assumptions to verify before implementing.>
```

## Lifecycle metadata

Each finding carries a `status:` line, edited by humans/agents over time:
`draft → reviewed → accepted | deferred | rejected → implemented-verified`
- `accepted` means a decision to do it — never rewrite the "Observed" section as if it were done.
- `implemented-verified` requires citing the implementation (path/commit) and the verification (command/test). Add a line to the finding rather than a new file.

## Priorities and IDs

P0 = correctness/data-loss/leakage-class risk active now; P1 = significant pain or risk with evidence; P2 = worthwhile improvement; P3 = hygiene/observation. IDs are stable per run (`AUD-ARCH-001`, `AUD-ML-002`, `AUD-EXP-001`); keep numbering when editing a report so cross-references survive.
