# agent-toolkit

A general-purpose library of independent skills in the
[Agent Skills format](https://agentskills.io/specification), with stdlib Python
tools for validation and installation.

## Skill catalog

| Skill | Purpose | Scope |
|---|---|---|
| [project-audit](skills/project-audit/SKILL.md) | Project architecture and methodology audits | Software / ML |
| [project-map](skills/project-map/SKILL.md) | Agent-oriented codebase navigation | General |
| [project-brief](skills/project-brief/SKILL.md) | Human onboarding, project overview, status, pipeline, and synthesis | General |
| [agent-efficiency](skills/agent-efficiency/SKILL.md) | Diagnose workflow waste, reuse procedures, review available usage | Development workflows |
| [tidy-dev](skills/tidy-dev/SKILL.md) | Choose worthwhile local structural improvements around a change | Coding / diff review |

Optional [focused-changes policy](policies/focused-changes.md): concise coding
instructions to incorporate manually, not a skill or an automatic hook.

## Quick start

Run these commands from the toolkit checkout. Replace `/absolute/path/to/project`
with your project's absolute path.

```bash
# Generic harness + all skills + all profiles (defaults)
python tools/install.py --target /absolute/path/to/project

# List available skills, profiles, and destination state
python tools/install.py --target /absolute/path/to/project --harness generic --list

# Preview an update; omit --dry-run to apply it
python tools/install.py --target /absolute/path/to/project --skills project-map --harness generic --dry-run
```

| Parameter | Available values | Usage |
|---|---|---|
| `--skills` | `all` (default), `project-audit`, `project-map`, `project-brief`, `agent-efficiency`, `tidy-dev` | All skills or one or more names, comma-separated |
| `--harness` | `generic` (default), `codex`, `claude`, `copilot`, `devin` | Choose one destination convention |
| `--profile` | `all` (default), `software-development`, `ml-development` | Union of all profiles or one named profile; both named profiles select `project-audit`, `project-map`, and `project-brief` |

Without either selector, the defaults are `--skills all --profile all`.
An explicit `--skills` or `--profile` limits installation to that selection;
if both are supplied, their skills are combined without duplicates. Profiles
are skill selections, not separately installed components.
See [all installer options](docs/installation.md#options-and-defaults).

Re-run the original install command after updating this checkout to update an
unmodified installation. Outcomes are `installed`, `up-to-date`, `updated`, or
`skipped-conflict`; `duplicate-warning` identifies another project-level copy.
Conflicts retain local content and return exit code 3. `--force` replaces the
selected skill directory, including locally added files. Other skills, project
artifacts, and instruction files are preserved.

### Installer destinations

These are the installer's path mappings, not a guarantee of discovery or reload
behavior in every harness version. Choose one location per team.

| `--harness` | Project scope (default) | User scope |
|---|---|---|
| `generic` (default) | `.agents/skills/` | `~/.agents/skills/` |
| `codex` | `.agents/skills/` | `~/.agents/skills/` |
| `claude` | `.claude/skills/` | `~/.claude/skills/` |
| `copilot` | `.github/skills/` | `~/.copilot/skills/` |
| `devin` (CLI) | `.devin/skills/` | `~/.config/devin/skills/` |

The `devin` mapping targets Devin CLI, not cloud configuration. For cloud Devin
or an unlisted client, confirm its supported repository path and use the
[manual installation instructions](docs/installation.md#manual-installation).
The installer copies files; it does not activate clients or edit `AGENTS.md` or
`CLAUDE.md`.


## Optional Map → Audit → Brief workflow

Use [project-map](skills/project-map/SKILL.md) for agent navigation,
[project-audit](skills/project-audit/SKILL.md) for evidence-backed diagnosis, and
[project-brief](skills/project-brief/SKILL.md) for human onboarding, overviews,
status, pipeline explanations, and synthesis. This sequence is optional: each
skill works independently from source without requiring the others.

Map cards stay in `.agent/project-map/`, audit evidence in
`.agent/audits/<run-id>/`, and human outputs in `docs/project-brief/`
(`README.md`, `pipeline.md`, `roadmap.md`). Start with the map's L1 index and
read only relevant cards; verify claims against current source rather than
copying a whole map or promoting stale cards to evidence. Keep proposals out of
current-state descriptions. See [the handoff and evidence contract](docs/architecture.md#optional-map--audit--brief-workflow).

## Repository layout

```text
agent-toolkit/
  skills/       # canonical, independently installable skill directories
  tools/        # installer, validator, shared development helpers
  profiles/     # optional JSON collections of skill names
  policies/     # optional project instructions; copied manually, not installed
  tests/        # unit tests, fixtures, existing acceptance evidence
  docs/         # installation, architecture, contributing
```

## Development

```bash
python tools/validate.py
python -m unittest discover -s tests -v
```

The validator and unit suite check metadata, references, and tool mechanics;
they do not establish live behavior for every harness. Optional upstream
creator checks use `python tools/validate.py --creators /path/to/skill-creator/skills`
with a PyYAML-capable interpreter. Creators are not runtime dependencies.

## Further reading

- [Installation and updates](docs/installation.md)
- [Architecture and shared contracts](docs/architecture.md)
- [Contribution checklist](docs/contributing.md)
- [Repository working rules](AGENTS.md)
- [Acceptance procedures](tests/acceptance/README.md) and [recorded evidence](tests/acceptance/results.md); recorded runs are scoped evidence, not cross-harness certification.
