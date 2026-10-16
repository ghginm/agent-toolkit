# Audit #3 — Exploratory / Open-ended Audit

Purpose: discover important issues, interactions, and opportunities that the structured audits (architecture, ML methodology) are not built to see. It runs its own curiosity — disciplined by evidence.

Two failure modes to avoid in opposite directions:
- **Speculation padding** — generating issues because a section expects content. Zero significant findings is a valid, reportable outcome.
- **Relabeled duplication** — re-filing audit #1/#2 observations under new titles. If a candidate is really a structured-audit finding, cross-reference it instead of rewriting it.

Contents:
1. How to work
2. Probe angles
3. Evidence discipline for novel findings
4. Handoff shape

## 1. How to work

Run *after* the structured audits when they also ran, so you know what is already filed and can look elsewhere. Then investigate sideways: follow threads that the checklists don't connect. Read from an entrypoint once all the way out to an output (or a failure); read the diff history where activity concentrates; read the files nobody opened (smallest, oldest, most-avoided); read docs to *disprove* them. Question assumptions that everyone seems to share — but only where you can name the assumption and where it lives.

Good exploratory findings often sit *between* areas: an interaction, an incentive, a workflow, a contradiction. Typical shapes (not quotas):

- Cross-module assumptions: module A quietly requires something module B is free to change.
- Goals-vs-implementation contradictions: README/product intent vs what the code optimizes for.
- Hidden operational risk: a single-persona path, a fragile manual step, an unguarded destructive command.
- Developer/agent workflow friction: setup that only works on one machine, build/test commands that drifted from reality.
- Unnecessary complexity or a surprising simplification ("these three files are one dict lookup").
- ML×architecture interaction: a methodology risk that exists only because of the structure, or vice versa.
- Non-obvious failure modes: what happens at boundaries — empty input, first run, DST change, schema addition.

## 2. Probe angles

Useful, cheap probes — follow whichever sparks a question:

1. **Docs as claims.** Take the README's promises/instructions; verify each against code and files. Divergence is a finding (docs stale, or aspirational docs written as if implemented — the latter matters for the map/audit lifecycle: proposed ≠ current).
2. **Entry-to-exit trace.** Walk data from the real entrypoint to persisted output; note every implicit contract, transformation nobody owns, and error path that dies silently.
3. **Git archaeology.** `git log --stat` hotspots; reverted fix attempts; the same file touched in every "quick fix" commit — recurrence is evidence-grade signal. Also: was the code written around one dataset/tenant/country that has since grown?
4. **Boundary behaviors.** Read what happens on: empty data, first-ever run, malformed config, dependency absence. Search `except`, `if len(`, `.get(` defaults, and `os.environ` fallbacks — silent defaults that change behavior in production are classic exploratory finds.
5. **Deletion test.** For suspicious indirection, abstraction, or config keys: what actually references it? Unreferenced-but-maintained machinery is a simplification candidate with evidence.
6. **Numbers don't match.** Compare counts/claims across artifacts (config vs code defaults vs docs; metric reported vs metric computed; test count vs test files). Contradictions are findings; verify against code to say which side is wrong.
7. **The human seam.** Where does the project depend on a person's undocumented knowledge? (Paths to personal machines, "ask X", runbooks that don't exist.) Evidence: cite the place the knowledge is needed but absent.
8. **Time and state.** Anything assuming "now", fixed dates, timezone, ordering from filesystem/network, singleton caches, global state across runs.

## 3. Evidence discipline for novel findings

Novelty does not lower the evidence bar — it makes the bar harder to meet fairly, so:

- State the observation (what is seen, cited) separately from the interpretation (why it matters). Interpretation is allowed to be `inferred`; observation must not be.
- If a hypothesis can't be confirmed in scope, file it as a **watch item** with the uncertainty stated and the cheapest check that would confirm/kill it — not as a finding at finding-strength.
- Impact claims that depend on future events say so ("if this repo gains a second pipeline consumer..."), and the recommendation carries the trigger, per the audit's context-sensitivity gate.
- Never pad: if the exploratory pass produced only confirmations of audit #1/#2 work plus two watch items, say exactly that. A short honest exploratory report is a success.

## 4. Handoff shape

Use the report template's common handoff fields and reference each finding's cited observation and Validation rather than repeating them. Add assumptions a coding agent must verify *before implementing* (novel findings often rest on a read of intent — flag it), blast radius including surprising cross-module ties, and any sequencing needed to confirm the diagnosis (e.g., "add the missing-behavior test first; if it passes, the finding was wrong"). Mark explicitly which findings are safe to implement upon acceptance and which need a cheap experiment or a user decision first.
