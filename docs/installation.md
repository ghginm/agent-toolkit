# Installation

One canonical copy of every skill lives in this repo's `skills/`. Installation is copying selected skill directories into the destination your harness scans, plus (optionally) pasting a bootstrap pointer into your project's agent-instructions file.

## Installer

```bash
python tools/install.py --target /path/to/project --skills project-audit,project-map --harness codex
python tools/install.py --target /path/to/project --profile ml-development --harness claude
python tools/install.py --target /path/to/project --skills project-map --harness generic --dry-run
python tools/install.py --list --harness copilot --target /path/to/project
```

Flags: `--skills` (names) or `--profile` (JSON list under `profiles/`); `--harness claude|codex|copilot|devin|generic`; `--scope project|user`; `--dry-run`; `--force` (replace); `--list`. Exit codes: 0 ok, 2 usage, 3 completed-with-conflict (something was skipped for safety).

The installer validates the selected skills before copying anything, copies each skill directory whole (no symlinks), and records fingerprints in `agent-toolkit.lock.json` inside the destination skills root. That lock file plus content comparison gives the update behavior:

- destination absent → install
- identical to source → "up to date", untouched
- differs, and matches our previous install → treated as a toolkit upgrade, replaced
- differs, and does NOT match our previous install → assumed user-modified: skipped with warning; `--force` replaces the whole directory (deleting locally added files inside it — intentional, blunt, stated)

Nothing else is ever written. `AGENTS.md`/`CLAUDE.md` are never modified (see Bootstrap below).

## Destination conventions

Sources checked October 2026:

| Harness | Project location | User/personal location | Basis |
|---|---|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/` | code.claude.com/docs/en/skills |
| Codex | `.agents/skills/` scanned from CWD up to repo root; repo-root `.agents/skills/` is the shared spot | `~/.agents/skills/` | developers.openai.com/codex/skills |
| GitHub Copilot | `.github/skills/` (also reads `.claude/skills` and `.agents/skills`) | `~/.copilot/skills/` (also `~/.agents/skills/`) | docs.github.com/copilot agent-skills docs |
| Devin | scans `.agents/skills/`, `.devin/skills/`, `.github/skills/`, `.claude/skills/`, `.cognition/skills/`, `.windsurf/skills/` (`.agents/skills/` recommended for cloud Devin; `.devin/skills/` is the CLI convention) | `~/.config/devin/skills/` (CLI; Windows `%APPDATA%\devin\skills`) | docs.devin.ai skills pages |
| generic | `.agents/skills/` — the emerging cross-client convention | `~/.agents/skills/` | agentskills.io client-implementation guide |

Notes the table can't carry:

- **Pick ONE destination per team.** Several harnesses read multiple locations; installing to both `.agents/skills/` and `.claude/skills/` makes those skills visible twice in harnesses that scan both (collision semantics vary). For mixed-harness teams, `--harness generic` (`.agents/skills/`) covers Codex, Copilot, Devin, and other spec-following tools at once.
- **Version drift is real.** Product conventions move; before trusting this table for a new harness/version, confirm against its current docs or installed tool. The manual route below always works.
- Devin distinguishes cloud-repo skills (indexed across connected repos) from CLI disk skills; the installer just places files — activation semantics are the harness's.

## Manual installation (any harness, including unlisted)

1. Copy `skills/<name>/` (the whole directory) to wherever your tool loads skills from — per-project convention directory, or its personal equivalent.
2. Restart the CLI / reload the session if skills don't hot-load.
3. Verify: ask the agent which skills it sees, or trigger something like "create a project map for this repo."

## Bootstrap pointer (L0) — deliberate non-automation

Neither skill edits project instruction files. `project-map`'s create workflow prints a ≤15-line pointer block (`skills/project-map/assets/bootstrap-snippet.md`) for `AGENTS.md`, `CLAUDE.md`, or whatever the harness actually reads, and appends it only with explicit permission when no equivalent exists. Do not assume every harness reads `AGENTS.md` — Claude Code historically used `CLAUDE.md`; use your tool's supported mechanism. The block states: where the map lives, when to consult it, that code verification is mandatory, when to update cards, and the fallback when the map is missing or wrong.

## Upgrades across a team

Commit the installed skill directories (or re-run the installer) — whichever your team prefers; both work. To upgrade: pull this toolkit repo → re-run the same install command → "replace" lines confirm updated skills, user-modified ones surface as conflicts to reconcile manually.

## Windows

Install/copy paths go through `pathlib`; no symlinks are created. Live Windows smoke test (not performed in Linux/WSL development, documented procedure):

1. `python tools\install.py --target C:\path\to\project --skills project-map --harness codex`
2. Confirm files under `C:\path\to\project\.agents\skills\project-map\...`
3. In a Codex session there: run `python .agents\skills\project-map\scripts\map_check.py` — must print the problems/notes summary (git checks skip if unavailable).
