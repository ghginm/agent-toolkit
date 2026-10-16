# Contributing

Contribute independent Agent Skills or small supporting tools. Read
[AGENTS.md](../AGENTS.md) and [architecture](architecture.md) before changing
shared conventions. No domain-specific workflow or creator checkout is
required to contribute.

## Add or revise a skill

| Phase | Requirements |
|---|---|
| Create | Add or edit canonical `skills/<name>/SKILL.md`; define task, boundaries, outputs, and completion criteria. No per-harness copies. |
| Resources | Bundle only necessary references, assets, and scripts; no imports from `tools/` or reads of sibling skills. |
| Metadata | Match directory name; provide a valid description with concrete triggers and useful non-triggers. |
| Validate | Run the toolkit validator; check resource links and command paths. |
| Test | Run unit tests and focused regressions for mechanical changes; use a focused behavioral check when relevant. |
| Document | Update the [README catalog](../README.md#skill-catalog); profiles are optional collections. |
| Submit | Review the diff and commit a focused change; state executed checks and limitations. |

## Content and resources

| Component | Guidance |
|---|---|
| Description | State what the skill does and when to use it, with concrete triggers and useful non-triggers; no marketing claims |
| `SKILL.md` body | Use imperative technical English; stay under 500 lines and keep only workflow-critical instructions |
| `references/` | Detailed methods, linked directly from `SKILL.md` with when-to-read guidance; give long references a contents list |
| `assets/` | Copy-and-fill templates or other workflow inputs, referenced by name |
| `scripts/` | Deterministic, repeated mechanics; stdlib Python, explicit paths and write scope, focused unit coverage |
| Repository docs | Installation and contributor guidance; avoid README, changelog, or development notes inside a skill |

Keep judgment in prose rather than scripting semantic verdicts. Avoid repeating
rules across a skill's body and references. The deliberate exception is small
cross-skill contracts: duplicate them to preserve standalone use, then keep
all affected copies and [architecture](architecture.md#shared-contracts) synchronized.

## Project navigation, audits, and human briefs

Keep audience boundaries explicit: `project-map` serves agent routing,
`project-audit` diagnoses with evidence, and `project-brief` explains the project
to humans. Preserve their [optional handoff](architecture.md#optional-map--audit--brief-workflow)
without adding cross-skill resource reads or mandatory sequencing. Reuse an
existing map via L1 → selected cards → current source, not a bulk copy.

Keep agent artifacts under `.agent/project-map/` and `.agent/audits/<run-id>/`;
keep human `README.md`, `pipeline.md`, and `roadmap.md` outputs under
`docs/project-brief/`. Maintain the evidence core in frontmatter. Human labels
map to `verified-static`, `verified-executed`, `inferred`, `proposed`, and prose
`unknown`; stale map content requires refresh or reinspection, not a verified
label. Do not promote audit proposals into current-state descriptions.

When changing this integration, check standalone discovery/installation, both
standard profiles, the README catalog/options, and installation examples. Keep
`agent-efficiency` and `tidy-dev` independent and outside those profiles; policy
and instruction-file changes remain manual opt-in, never installer side effects.

## Metadata contract

Use frontmatter delimited by `---`. Required fields are `name` and
`description`; optional spec keys are `license`, `compatibility`, `metadata`,
and `allowed-tools`.

- Match `name` to the directory: lowercase letters, digits, and hyphens; at most
  64 characters, with no leading, trailing, or consecutive hyphens.
- Quote `description` on a single line; keep it nonempty, at most 1024
  characters, and free of angle brackets. Folded YAML scalars are unsupported.
- Use flat `key: value` fields and only a one-level string map for `metadata`.
  Do not add harness-specific presentation keys to the canonical frontmatter.

## Validation and tests

From the repository root:

```bash
python tools/validate.py
python -m unittest discover -s tests -v
```

Run the suite under both available Python versions when practical. Keep the
`mini-skill` discovery fixture valid and add focused tests for installer,
validator, or bundled-checker changes. Verify every edited Markdown link and
skill resource path. Check script examples against their actual argument
parsers: use absolute project and installed-skill directories, explicit
`--repo`/`--map-dir` for map checks, and `--project`/`--run` for audit checks.
See [installation examples](installation.md#running-bundled-checkers).

Optional upstream creator validation:

```bash
python tools/validate.py --creators /path/to/skill-creator/skills
```

Creator validators need a PyYAML-capable interpreter. They supplement the
stdlib toolkit validator; they are neither mandatory tooling nor skill runtime
dependencies.

Each available creator runs independently for every selected skill. Reports
identify the creator and skill: `PASS` means exit 0; `FAIL` means validation
rejection (exit 1); `ERROR` means a Python crash, abnormal exit, launch failure,
or timeout. Missing scripts or a missing PyYAML-capable interpreter are
`SKIPPED`, never `PASS`. Failures and errors make the final exit code 1;
remaining checks still run.

## Clean release archives

No archive-generation tooling is maintained. After reviewing and committing
the intended source changes, package tracked content from that commit:

```bash
git archive --format=tar.gz --prefix=agent-toolkit/ -o ../agent-toolkit.tar.gz HEAD
```

This excludes untracked files and working-tree changes. `.gitignore` keeps
Python caches out of normal staging; `.gitattributes` also excludes cache
paths from `git archive` if accidentally tracked. Never use a recursive archive
of the working directory as a release artifact.

## Review and submission checklist

- [ ] Skill scope and resources work without this checkout or another skill.
- [ ] Metadata, local references, and the under-500-line skill limit hold.
- [ ] Validator and unit-suite results are recorded, including failures or skips.
- [ ] Shared evidence statuses, citations, artifact paths, lifecycle, and IDs are
      synchronized where changed.
- [ ] Catalog, profiles when relevant, and affected commands or links are current.
- [ ] No project instructions are overwritten; bootstrap additions remain
      proposed, manual, and explicitly opt-in.
- [ ] Changes are limited to the intended files; the submission describes what
      changed, why, verification performed, and remaining limitations.

## Existing behavioral evidence

[Acceptance procedures](../tests/acceptance/README.md) describe behavioral
scenarios; [recorded results](../tests/acceptance/results.md) preserve prior
runs. Unit tests establish mechanics, not agent judgment or every client's
runtime behavior. Follow the repository's acceptance policy for behavioral
skill changes unless the task explicitly narrows verification. A documentation
cleanup does not itself require new acceptance runs or installation simulations;
report the checks actually performed.
