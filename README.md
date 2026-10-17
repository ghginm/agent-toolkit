# agent-toolkit

A general-purpose library of independent skills in the
[Agent Skills format](https://agentskills.io/specification), with stdlib Python
tools for validation and installation.

## Skill catalog

| Skill | Purpose | Scope |
|---|---|---|
| [project-audit](skills/project-audit/SKILL.md) | Project architecture and methodology audits | Software / ML |
| [project-map](skills/project-map/SKILL.md) | Agent-oriented codebase navigation | General |
| [project-brief](skills/project-brief/SKILL.md) | Human-readable project overview or modular architecture deep-dive | General |
| [decision-workshop](skills/decision-workshop/SKILL.md) | Architecture discussion guides and decision consolidation | General |
| [agent-efficiency](skills/agent-efficiency/SKILL.md) | Diagnose workflow waste, reuse procedures, review available usage | Development workflows |
| [tidy-dev](skills/tidy-dev/SKILL.md) | Choose worthwhile local structural improvements around a change | Coding / diff review |

Optional [focused-changes policy](policies/focused-changes.md): concise coding
instructions to incorporate manually, not a skill or an automatic hook.

## Example workflows

Want to see how these skills can work together?

**[Recommended contract examples](docs/recommended-contract-examples.md)** —
Copy-paste prompts for practical multi-skill workflows, including technical
review → human review → team discussion.

Each skill also works independently.

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

**Installation notes**

- **Defaults:** Installs all skills unless `--skills` or `--profile` is specified.
- **Selection:** `--skills` selects individual skills; `--profile` selects
  predefined groups. Both can be combined; their skills are merged without duplicates.
- **Updates:** After updating this checkout, re-run the original installation
  command to update unmodified installations.
- **Safety:** Local changes are preserved by default. `--force` replaces the
  selected skill directory, including locally added files.

The installer supports Codex, Claude, Copilot, Devin CLI, and generic Agent Skills
destinations. Choose one location per team; installation does not activate clients.

See [Installation & Updates](docs/installation.md) for complete
[options](docs/installation.md#options-and-defaults), conflict handling, exit codes,
and [destination mappings](docs/installation.md#destination-mappings).

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

## Documentation

**Using the toolkit**

- [Installation & Updates](docs/installation.md) — setup, profiles, destinations, and safe updates.

**Developing the toolkit**

- [Architecture & Contracts](docs/architecture.md) — internal design and invariants.
- [Contributing](docs/contributing.md) — developing and maintaining skills.
- [AGENTS.md](AGENTS.md) — repository instructions for coding agents.
- [Testing & Acceptance](tests/acceptance/README.md) — procedures and
  [recorded evidence](tests/acceptance/results.md), not cross-harness certification.
