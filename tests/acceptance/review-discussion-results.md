# Deep review and decision workshop — executed results

Run date: October 16, 2026 (EDT; October 17 UTC). Procedure and prompts:
[review-discussion.md](review-discussion.md). All projects were scratch copies;
canonical fixtures and application code were not modified.

## Implementation checks

| Check | Actual result |
|---|---|
| Toolkit validator | `python tools/validate.py --creators ../skill-creator/skills`: OK, 0 problems, 0 warnings |
| Local Anthropic creator | All six discovered skills PASS via `../skill-creator/skills/skill-creator-anthropic/scripts/quick_validate.py` |
| Local OpenAI creator | All six discovered skills PASS via `../skill-creator/skills/skill-creator-openai/scripts/quick_validate.py` |
| Python 3.14.7 unit suite | `python -m unittest discover -s tests`: 67 tests, OK |
| Python 3.12.3 unit suite | `/usr/bin/python3 -m unittest discover -s tests`: 67 tests, OK |
| Installation mechanics | Standalone discovery/copy, all five destination mappings, dry-run, unchanged reinstall, source update, local conflict/force, both profiles, preserved project artifacts pass in unit suite |
| Scope | Git diff confirms project-map, project-audit, tools, and existing overview template unchanged; `git diff --check` passes |

The initial unit run exposed two profile expectations still listing three
skills. Updated those expected sets/counts deliberately for the fourth profile
member; final suites above pass. No installer changes were needed.

## Actual generated artifacts

Workspace: `/home/ghgin/.hermes/cache/scratch/atk-deep-review-9y6qt3x7`.
Installed only the named skill into each target using the ordinary installer.
Fresh-context worker agents executed the tasks; a separate evaluator read all
15 brief documents, workshop artifacts/snapshot, and underlying fixture sources.
One brief worker processed three separate project copies, so this is not three
independently isolated generation samples or a statistical benchmark.

| Scenario | Observed result | Artifact evidence within workspace |
|---|---|---|
| R1 overview | Compact default, three documents; source-only synthesis without map/audit | `overview/docs/project-brief/{README,pipeline,roadmap}.md`; README 647 whitespace words including Markdown syntax |
| R2 explicit depth | Deep-dive, six linked documents; five actual stages with purpose/contracts, limits, alternatives, and proposed direction | `explicit/docs/project-brief/`; README routes to pipeline, current-state, target-architecture, requirements-register, roadmap |
| R2 natural depth | Comprehensive legacy/architecture-planning request selects deep-dive without a magic phrase; same six-module organization | `natural/docs/project-brief/`; README explicitly explains intent selection |
| R3 preparation | Current system precedes alternatives, backbone questions precede four stage tables, six linked decision IDs; satisfactory validation unchanged | `workshop/discussion/{README,decisions}.md`, initial `workshop-before-consolidation/discussion/` snapshot |
| R4 consolidation | D-002 Agreed; mechanism in D-001 Deferred with measurement/budget conditions; in-memory option specifically Rejected; five-second objective and backoff unapproved | Updated `workshop/discussion/decisions.md`; M-01 provenance, no invented dates/participants; D-003/D-006 and guide preserved |
| Focused preparation | Retry-policy options only, necessary handoff/latency dependencies, no identifier/validation redesign or whole-system review | `focused/discussion/{README,decisions}.md` |
| Consolidation without guide | Existing register alone updated with supported outcomes and stable IDs; no guide created | `consolidate-only/discussion/decisions.md`; README absent |
| R6 final description routing | 20/20 expected classifications, including brief depth | `routing-input-final.json`, `routing-predictions-final.json`, `artifact-checks.json`; evaluator-only key remains in repository |

The brief packs identify the full-data scaling/random split, classifier-only
artifact, and prediction batch refitting from actual fixture source. They do
not claim training, inference, or smoke tests were run; missing CSV/model and
historical requirements are stated as limits. Proposed designs are separate
from current implementation. The workshop works directly from synthetic design
docs: its external advisory informs options but proves no implemented worker,
outbox, monitoring, or duplicate handling. Recommendations do not become votes.

Parent verification reran link/anchor, source-byte, stable-ID, untouched-entry,
standalone-install, no-guide, and target-diagram checks against actual files.
Link checks report no broken targets: overview 48, each deep pack 121, original
workshop 14, focused guide/register 9, consolidation-only register 12.

## Review-driven corrections

Both creator-guided reviewers identified unconditional guide output during
consolidation. Anthropic-guided review also identified focused-scope expansion;
OpenAI-guided review identified overlapping preparation triggers. Clarified
mode-specific output/checks, proportionate scope, and understanding versus
meeting-agenda triggers. Focused/consolidation-only runs used the revised skill;
blinded routing was repeated against final descriptions (20/20).

Independent artifact review passed the substantive checks but found one minor
clarity defect: both proposed target diagrams bypassed the acceptance decision
when feeding scoring, although prose required acceptance. Added a general
proposed-diagram gate consistency check to the deep-dive reference. Parent
corrected both generated example diagrams to show conditional acceptance →
approved bundle → scoring and verified those edges and links. This last narrow
instruction addition was not independently regenerated/re-evaluated; corrected
examples are parent-edited, not pristine generation outputs. The original
independent report retains the finding rather than silently erasing it.

## Limits

These are scoped agent-generation and artifact-review checks on small synthetic
projects, not an empirical human readability study, production evaluation, or
cross-harness activation certification. Description classification is not live
automatic invocation. Three fixture arms share much generated content. Mermaid
edges were inspected as text, not rendered. No ML dependencies, data acquisition,
training/inference, PowerPoint generation, or complete map→audit→brief→workshop
combined run was performed. Scratch artifacts may be pruned; this record and
repository scenarios/fixtures preserve the procedure and scoped outcomes.
