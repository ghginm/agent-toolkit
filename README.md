# agent-toolkit

A small, extensible library of **Agent Skills** — markdown-plus-filesystem capability packages that any skill-capable coding agent (Codex, Claude Code, GitHub Copilot, Devin, VS Code, …) can load — plus minimal tooling to validate and install them.

Skills here are built for the [open Agent Skills format](https://agentskills.io/specification): a directory with a `SKILL.md` (YAML frontmatter + instructions) and optional `references/`, `assets/`, `scripts/`. No runtime framework, no registry, no vendor lock-in.

## Available skills

| Skill | What it does |
|---|---|
| [`project-audit`](skills/project-audit/) | Evidence-cited audits of software & ML/DS projects in three selectable modes: **architecture/MLOps**, **ML/DS methodology**, **exploratory** — each ending in a coding-agent handoff. Audits recommend; they never refactor. |
| [`project-map`](skills/project-map/) | Creates, consults, incrementally updates, and validates a hierarchical (L0–L3) map of a repository under `.agent/project-map/` so agents navigate without re-exploring. The map is a navigation aid — code stays the authority. |

**Skills vs. persistent project documents** — an important distinction: *skills* are installable instructions you copy into a harness's skills directory; they teach the agent *how* to work. The *artifacts* skills produce (maps in `.agent/project-map/`, audits in `.agent/audits/`) live in your project, are committed or reviewed like any document, and carry freshness metadata. Deleting the skill does not delete the artifacts, and the artifacts never depend on the toolkit being installed.

## Quick start

```bash
# from this repo — install both skills into a project for your harness
python tools/install.py --target /path/to/project --profile ml-development --harness codex

# one skill, Claude Code, preview first
python tools/install.py --target /path/to/project --skills project-map --harness claude --dry-run

# what's available / already installed?
python tools/install.py --list --harness codex --target /path/to/project
```

Destination conventions verified against product docs (October 2026) — details and manual fallback in [docs/installation.md](docs/installation.md):

| `--harness` | project scope | user scope |
|---|---|---|
| `claude` | `.claude/skills/` | `~/.claude/skills/` |
| `codex` | `.agents/skills/` | `~/.agents/skills/` |
| `copilot` | `.github/skills/` | `~/.copilot/skills/` |
| `devin` | `.devin/skills/` | `~/.config/devin/skills/` |
| `generic` | `.agents/skills/` (cross-client convention) | `~/.agents/skills/` |

The installer copies files only, never symlinks (Windows-safe), never overwrites user-modified installs without `--force`, and never touches your `AGENTS.md`/`CLAUDE.md` — it prints guidance instead.

## Using the skills

After install + restart (or automatic reload), invoke naturally:

- **“Audit this project's architecture and ML methodology, cite evidence, give me findings I can hand to a coding agent.”** → `project-audit` runs `all` modes, writing `.agent/audits/<run-id>/` reports with findings in `status: draft` and per-mode coding-handoff sections.
- **“Create a project map for this repo.”** → `project-map` writes `.agent/project-map/` (L1 index + L2 module cards, L3 only when triggered) and proposes a ≤15-line bootstrap pointer for `AGENTS.md`.
- Later sessions automatically: read L1 → route to module card → **still inspect the actual code** → implement → verify → update touched cards only.
- **“Refresh the map after my changes.”** → `project-map update` uses git to find affected cards; unrelated cards stay untouched.
- **“Is the map still true?”** → `project-map validate` runs mechanical reference checks (`scripts/map_check.py`) plus agent spot-checks of claims against code.

### Example workflows

**New ML project:** install both skills → `project-map create` → skim the routing table → run `project-audit` (modes as needed) → review findings, accept some → coding agent plans work from accepted findings + map, verifies code while implementing → runs tests → `project-map update` for the touched cards.

**Routine coding:** agent reads L1 → locates subsystem → reads real code/tests → changes → verifies → updates affected cards. A full audit never runs uninvited.

**Third unrelated skill (e.g. `research-report`):** create `skills/research-report/SKILL.md` (+ its own resources), run `python tools/validate.py`, install with `--skills research-report`. No toolkit code changes — discovery is a directory scan. See [docs/contributing.md](docs/contributing.md).

## Validating and testing

```bash
python tools/validate.py                 # spec metadata + local reference integrity
python -m unittest discover -s tests -v  # installer / validator / map_check unit tests
```

Behavioral acceptance of the skills (audit/mapping runs against flawed-project fixtures) is documented in [tests/acceptance/](tests/acceptance/). Upstream skill-creator validators (`quick_validate.py` from Anthropic's and OpenAI's skill-creators) can be run via `python tools/validate.py --creators <dir>` when a PyYAML-capable Python is reachable.

## Repository layout

```
agent-toolkit/
  skills/            # canonical skill sources (the deliverables)
  tools/             # repo developer tools: validate.py, install.py (+ skillkit.py helper)
  profiles/          # optional named skill collections (JSON lists)
  tests/             # unit tests + fixtures + acceptance evidence
  docs/              # architecture decisions, installation, contributing
```

## Design posture

Sophisticated in reasoning, lightweight in infrastructure: ordinary filesystem conventions, four stdlib-Python scripts (`tools/validate.py`, `tools/install.py`, `skills/project-map/scripts/map_check.py`, `skills/project-audit/scripts/check_report.py`), and deliberately no plugin framework, registry, database, hooks, or orchestration layer. Rationale and trade-offs: [docs/architecture.md](docs/architecture.md).

## Limitations

- Harness *behavior* differs beyond the spec (auto-triggering, reload semantics, Windows details). Directly tested here: installer conventions + unit tests; live agent behavior was validated via subagent workflow tests (see [tests/acceptance/](tests/acceptance/)). Each harness smoke test should still be done once in your environment — [docs/installation.md](docs/installation.md) lists manual procedures.
- `project-audit` and `project-map` share conventions (evidence statuses, `.agent/` layout) that are intentionally duplicated per-skill so each stays independently installable; drift between the two copies is possible — the contributor checklist includes a sync check.
