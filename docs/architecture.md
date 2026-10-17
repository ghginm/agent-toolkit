# Architecture

The toolkit is a general-purpose library of independent Agent Skills, not an
agent runtime. Filesystem conventions and small deterministic tools handle
packaging; agents perform the workflows and semantic judgment.

## Responsibilities

| Location | Responsibility |
|---|---|
| `skills/<name>/` | Canonical installable unit: `SKILL.md` and its own resources |
| `policies/*.md` | Optional project-level instructions, manually incorporated; no runtime enforcement or profile installation |
| `tools/skillkit.py` | Development-only discovery, metadata parsing, fingerprints |
| `tools/validate.py` | Metadata and local-reference validation; optional creator checks |
| `tools/install.py` | Skill selection, validation, copying, update safety, destination reporting |
| `profiles/*.json` | Optional named collections with a `skills` list |
| `tests/` | Unit regressions, fixtures, and existing acceptance evidence |
| `docs/` | Repository usage and contributor contracts, not skill runtime resources |

There is one canonical source tree, not separate content per harness. An
installed skill must not import `tools/`, read sibling skills, or require this
checkout. Bundle deterministic helpers in that skill's own `scripts/`; keep
Python dependencies in the standard library. Project artifacts are outputs,
not toolkit dependencies, and remain in the project when skills are removed.

| Kind | Examples | Persistence / activation |
|---|---|---|
| Independent skill | `project-audit`, `project-map`, `project-brief`, `decision-workshop`, `agent-efficiency`, `tidy-dev` | Installed individually; invoked for relevant tasks, not continuously |
| Optional policy | `policies/focused-changes.md` | User opts into existing project instructions; not a skill |
| Generated project artifact | Audit reports, map cards, authorized reusable commands | Lives in the target project; ordinary efficiency/tidy assessments need no saved report |

`agent-efficiency` and `tidy-dev` contain only `SKILL.md`: no detailed reference
catalog or deterministic runtime helper is needed. Both standard profiles select
`project-audit`, `project-map`, `project-brief`, and `decision-workshop` because
architecture review and discussion apply to both software and ML projects.
Efficiency/tidy stay opt-in through explicit selection or an all-skills install.
`tidy-dev` uses the structural/behavioral distinction discussed in Kent Beck's
*Tidy First?* and reviewed in [dtun/tidy-first](https://github.com/dtun/tidy-first).
Its instructions are independently written, not copied upstream text or code;
it omits mandatory handoffs/commit formats and does not treat passing tests as
proof of complete behavioral equivalence. The reviewed upstream material is
MIT-licensed, copyright 2026 Danny Tunney; no upstream runtime files are bundled.

## Discovery and extension

`skillkit.discover` scans `skills/*/SKILL.md`. The installer and validator use
that scan rather than a registry or hard-coded skill catalog. A new skill needs
its own directory and metadata; add a profile entry only when it belongs to a
collection. The `mini-skill` fixture tests discovery beyond the current catalog.

Keep `SKILL.md` focused on workflow and resource routing. Put detailed methods
in `references/`, templates in `assets/`, and repeated mechanical checks in
`scripts/`. A checker can establish structural consistency, not the truth of an
agent's analysis. The current skills bundle map and audit report checkers;
semantic analysis remains agent work.

## Installation and update model

The installer resolves a destination from harness and scope, validates selected
skills, and copies whole directories without symlinks. A destination-local
`agent-toolkit.lock.json` records per-skill content fingerprints and installation
provenance. Fingerprints cover relative file paths and bytes; they are not
semantic versions or dependency constraints.

| Comparison | Outcome |
|---|---|
| Destination absent | `installed` |
| Destination matches current source | `up-to-date` |
| Destination matches recorded install, source differs | `updated` |
| Destination differs without a matching record | `skipped-conflict`; preserve it unless `--force` |

A forced update replaces the whole selected skill directory, including local
additions. Other skills and project artifacts are preserved. Skipped conflicts
return exit 3; they do not prevent safe selected work from completing.
`duplicate-warning` is advisory: it checks other known project-level skill
locations, not user homes, ancestor repositories, arbitrary client settings, or
cloud state. It neither resolves precedence nor removes copies.

The path table is installer data, not a harness adapter layer. In particular,
`devin` selects Devin CLI paths, not cloud setup. Client activation and reload
semantics are outside this tool. The installer never edits project instruction
files; a bootstrap pointer is proposed for manual, explicitly permitted append
without replacing existing instructions. See [installation](installation.md).

## Shared contracts

`project-audit`, `project-map`, `project-brief`, and `decision-workshop` can
cooperate through project artifacts, but none requires the others. Small shared
conventions are duplicated inside each skill so copying one directory alone
preserves its instructions.

| Contract | Meaning |
|---|---|
| Evidence core | `verified-static`, `verified-executed`, `inferred`, `proposed` |
| Skill-specific statuses | Audit `unknown` means unverifiable in scope; map `stale` means known drift. Neither substitutes for the other's metadata status. |
| Citations | Source `path::symbol` or `path:line`; executed evidence records command and result |
| Artifact roots | Agent audit evidence: `.agent/audits/<run-id>/`; agent navigation: `.agent/project-map/`; human brief default: `docs/project-brief/`; discussion default: `discussion/`. Respect user-supplied human output destinations. |
| State separation | Proposals do not describe implemented current state |
| Finding lifecycle | `draft → reviewed → accepted/deferred/rejected → implemented-verified` |
| Finding IDs | `AUD-<mode>-NNN`, optionally linked from map proposed-direction sections |

A git revision is a baseline, not proof of correctness. Mechanical checks do
not justify semantic claims or mass-refreshing untouched cards. If a sibling
artifact is missing, proceed from source rather than requiring its skill.
When changing a shared contract, synchronize all affected skill copies and this table.

## Artifact handoffs and human outputs

| Skill | Audience and purpose | Target-project output |
|---|---|---|
| `project-map` | Agents: navigation and task routing | `.agent/project-map/` |
| `project-audit` | Evidence-backed diagnosis and findings | `.agent/audits/<run-id>/` |
| `project-brief` | Humans: compact overview or architecture deep-dive | Default overview: `docs/project-brief/README.md`, `pipeline.md`, `roadmap.md`; deep-dive: linked modules proportional to the project |
| `decision-workshop` | Teams: discussion preparation or decision consolidation | Default: `discussion/README.md` and `discussion/decisions.md` |

These are artifact boundaries, not an orchestrator, dependency chain, or automatic
post-audit step. Briefs can work directly from source; workshops can work directly
from supplied design documents, proposals, requirements, or decision records.
Installation creates skill directories, not these outputs. Human synthesis is
not another audit and does not silently edit maps, audit findings, source, or
project instructions. See [recommended contract examples](recommended-contract-examples.md)
for one optional combination, not a required workflow.

`project-brief` defaults to compact `overview`; explicit `deep-dive` requests or
natural requests for comprehensive architecture understanding, detailed onboarding,
or design-discussion preparation select a modular review. Ambiguous requests stay
compact. Keep a 2–3-minute README entry point and add only useful modules rather
than a fixed deep-dive file set. No mode configuration or output schema is needed.

Reuse maps selectively: read L1 first, choose relevant L2/L3 cards, then inspect
the cited current implementation. Check revision, working-tree changes, coverage,
and contradictions before reusing claims. A clean checker or recent revision is
not semantic verification. Missing maps permit direct inspection; stale cards
are leads to refresh or recheck, never `verified-*` evidence. Preserve audit
finding IDs and lifecycle when citing findings; recommendations remain proposed
until implementation evidence establishes current state.

Human labels explain the existing evidence vocabulary; they do not replace it:

| Human meaning | Evidence status | Required basis |
|---|---|---|
| Implemented, but not execution-tested in this review | `verified-static` | Current source citation |
| Implemented and execution-verified | `verified-executed` | Command and observed result, scoped to the claim |
| Inferred / uncertain | `inferred` | Explicit inference and supporting evidence |
| Proposed, not implemented | `proposed` | Clearly separate from implemented behavior |
| Unknown / not assessed | `unknown` | State the missing evidence or unresolved contradiction |

Human documents need no metadata frontmatter or new evidence schema; explain the
existing evidence core with human labels in prose or tables. State `unknown`
for unsupported claims in prose; never copy map `stale`
into verified brief evidence. Summaries must preserve evidence limitations,
including static-only checks, failed or unrun commands, and missing coverage.

Workshop decision statuses are `Open`, `Proposed`, `Agreed`, `Deferred`, and
`Rejected`; these describe team decisions, not evidence strength or the audit
finding lifecycle. Preserve stable existing decision IDs and source provenance.
Only supported agreements become `Agreed`: an agent recommendation or silence
is not approval. Consolidation records confirmed choices, rejected alternatives,
deferrals, and unresolved questions without rewriting unrelated documentation.
External knowledge may inform alternatives, never prove repository behavior.
Markdown is primary; slides through available dedicated tools or a slide outline
are optional. Do not generate a full implementation plan or application changes
as an automatic follow-up. No presentation dependency or workflow framework is added.

## Extension invariants

- Preserve independent installation: all runtime resources stay within the
  skill directory; optional sibling artifacts remain optional.
- Use supported flat frontmatter plus a one-level `metadata:` map; keep the
  description quoted on one line. See [contributing](contributing.md).
- Keep tools stdlib-only and explicit about writes, conflicts, and exit codes.
- Add regression coverage for mechanical behavior; do not infer harness runtime
  behavior from copy tests.
- Add a harness destination as path data and documentation, not a content fork.
- Add infrastructure only for a demonstrated need.

[Acceptance procedures](../tests/acceptance/README.md) and
[recorded results](../tests/acceptance/results.md) retain the existing behavioral
evidence. They are separate from unit-test and validator guarantees.
