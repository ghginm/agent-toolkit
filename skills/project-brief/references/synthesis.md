# Synthesis guidance

## Reconcile sources without starting another audit

Keep a small working claim ledger: claim, source/revision, evidence status,
contradiction, and destination section. It need not become a fourth document.
Group sources by meaningful topic so substantial claims remain traceable without
putting a citation on every sentence. A link to an entire repository is not
adequate support for a specific behavior claim.

Distinguish a documented goal from verified behavior. For example, a README
saying "production-ready" and a static training script showing one metric do
not establish readiness. Explain the observable capability and what remains
unverified; do not silently adopt the label or conduct an unsolicited full audit.

When sources conflict, inspect the smallest relevant implementation slice.
Name unresolved contradictions and their baselines. Reuse an old audit only
where the cited behavior still applies; never rewrite its lifecycle as part of
brief generation. A closed finding may remain useful history but is not a
current blocker without current evidence. Preserve the original finding ID,
priority, confidence, and status when quoting them. A different human-facing
ordering needs a reason based on current goals or dependencies.

Do not infer absence from silence: "No deployment evidence inspected" differs
from "Deployment is not implemented." Record external constraints and missing
inputs as blockers only when supported. Record execution failures only after
observing them; a missing dataset may establish a dependency without proving a
specific command was run and failed.

## Explain the actual system

Start with the user's input and the useful result, then follow entrypoints,
transformations, persistence, consumers, and error paths that connect them.
Libraries may have call flows rather than a single sequential pipeline;
services may branch or loop. Show separate training/inference or build/runtime
flows when they really differ. Name external systems and manual steps instead
of drawing imaginary automation between them.

For each meaningful stage, explain its purpose, inputs, outputs, current
behavior, neighbors, and limitations. Put optional technical depth after the
stage table, not before it. Each diagram edge is a claim about data/control
flow: verify it, including whether a saved artifact contains preprocessing as
well as a model. Label failure paths and unsupported transitions where material.
Provide a text arrow/list fallback immediately beside Mermaid.

Keep current architecture distinct from target design. Identify stable
infrastructure contracts separately from replaceable or experimental strategy
choices. For ML/DS, model families, scoring, features, and evaluation methods
can be experimentable; split discipline, artifact compatibility, and reproducible
inputs are correctness concerns. Do not require these concepts in non-ML work.

## Make recommendations decision-ready

| Bucket | Decision rule | Explain |
|---|---|---|
| Fix now | Supported correctness, reliability, or operational issue | Immediate action, prerequisite, benefit, validation, simpler alternative |
| Experiment first | Superiority depends on data or measured trade-offs | Hypothesis, comparison/baseline, success criterion, cost, decision it unlocks |
| Future considerations | Plausible but not justified now | Why deferred and concrete reconsideration trigger |
| Open questions | Missing requirement or unresolved choice | Who/what can resolve it and what it blocks; do not invent an owner |

Prioritize a few consequential actions, not every audit finding. Explain each
important action's why, dependency, what can happen immediately, and trade-off.
Separate audit priority from roadmap order when prerequisite work must happen
first. Do not invent three problems if fewer are supported. Suggest best
practices only to solve an evidenced local problem, with a simpler alternative
and proportionate complexity. External domain knowledge can enrich a proposal
but cannot verify repository state or prove that a proposed model will win.

Capture documented prior decisions and experiments with their source and
outcome/limits. If none were found in inspected materials, say so rather than
inventing a retrospective rationale. An inferred explanation belongs under
uncertainty, never in confirmed decision history.

## Final editorial pass

Read the overview without following any link. A newcomer should still learn
what the project solves, how it works, what is built/unverified, what matters
most, and what comes next. Links provide depth rather than withholding the
basic answer. Expand confusing terms once. Use status words rather than
unexplained colored icons. Move path inventories and implementation handoffs
back to technical artifacts. Keep detail that resolves a real misunderstanding;
remove repeated audit reasoning and decorative diagrams.
