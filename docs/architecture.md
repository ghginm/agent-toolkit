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
| Independent skill | `project-audit`, `project-map`, `agent-efficiency`, `tidy-dev` | Installed individually; invoked for relevant tasks, not continuously |
| Optional policy | `policies/focused-changes.md` | User opts into existing project instructions; no third skill |
| Generated project artifact | Audit reports, map cards, authorized reusable commands | Lives in the target project; ordinary efficiency/tidy assessments need no saved report |

The new workflow skills contain only `SKILL.md`: no detailed reference catalog
or deterministic runtime helper is needed. Profiles remain audit/map collections.
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

`project-audit` and `project-map` can cooperate through project artifacts, but
neither requires the other. Small shared conventions are duplicated inside
each skill so copying either directory alone preserves its instructions.

| Contract | Meaning |
|---|---|
| Evidence core | `verified-static`, `verified-executed`, `inferred`, `proposed` |
| Skill-specific statuses | Audit `unknown` means unverifiable in scope; map `stale` means known drift. Neither substitutes for the other's metadata status. |
| Citations | Source `path::symbol` or `path:line`; executed evidence records command and result |
| Artifact roots | `.agent/audits/<run-id>/` and `.agent/project-map/` |
| State separation | Proposals do not describe implemented current state |
| Finding lifecycle | `draft → reviewed → accepted/deferred/rejected → implemented-verified` |
| Finding IDs | `AUD-<mode>-NNN`, optionally linked from map proposed-direction sections |

A git revision is a baseline, not proof of correctness. Mechanical checks do
not justify semantic claims or mass-refreshing untouched cards. If a sibling
artifact is missing, proceed from source rather than requiring its skill.
When changing a shared contract, synchronize both skill copies and this table.

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
