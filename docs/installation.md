# Installation

Run installer commands from the toolkit checkout. Installation copies complete
skill directories from `skills/`; no symlinks or runtime services are needed.
Each skill can be installed alone.

## Commands

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
| `--skills` | `all` (default), `project-audit`, `project-map`, `agent-efficiency`, `tidy-dev` | All skills or one or more names, comma-separated |
| `--harness` | `generic` (default), `codex`, `claude`, `copilot`, `devin` | Choose one destination convention |
| `--profile` | `all` (default), `software-development`, `ml-development` | Union of all profiles or one named profile; both named profiles currently select `project-audit` and `project-map` |

Without either selector, the defaults are `--skills all --profile all`.
An explicit `--skills` or `--profile` limits installation to that selection;
if both are supplied, their skills are combined without duplicates. Profiles
are skill selections, not separately installed components. `--profile all`
alone selects the union of all `profiles/*.json` skill lists, whereas
`--skills all` selects every discovered skill, including those outside profiles.
Additional flags are listed under
[Options and defaults](#options-and-defaults).

### Workflow and local tidying skills

Select either independently with `--skills`, or use the all-skills command above.

| Skill | Example invocation |
|---|---|
| `agent-efficiency` | "Analyze the repeated setup in this session; reuse existing commands before proposing automation." |
| `agent-efficiency` | "Review available token usage and distinguish measured values from unknowns." |
| `tidy-dev` | "Would a focused tidy simplify this change? Choose tidy first, afterward, or no tidy." |

Invocation syntax and automatic discovery depend on the client. These skills
do not require each other, telemetry APIs, or the audit/map skills. Existing
profiles still select only audit and map; installation is not continuous review.

## Options and defaults

| Option | Meaning | Default |
|---|---|---|
| `--root ROOT` | Toolkit source containing `skills/` and `profiles/` | Checkout containing the installer |
| `--target TARGET` | Project destination root | Current working directory (`.`) |
| `--skills all\|a,b` | All discovered skills or comma-separated directory names | `all` when neither selector is supplied |
| `--profile all\|NAME` | Union of all profiles or `profiles/NAME.json` with a `skills` list | `all` when neither selector is supplied |
| `--harness NAME` | `generic`, `codex`, `claude`, `copilot`, or `devin` | `generic` |
| `--scope project\|user` | Resolve under target project or current user's home | `project` |
| `--list` | Show available skills, profiles, and installation state | Off; no installation |
| `--dry-run` | Show planned work without writing | Off |
| `--force` | Replace conflicting selected skill directories | Off |
| `--help` | Show command usage | Off |

For user scope, the destination is under the invoking process's home rather
than `--target`. Prefer an absolute `--target` for project scope so the shell's
working directory cannot silently change the installation location.

## Destination mappings

| Harness selection | Project path relative to `--target` | User path |
|---|---|---|
| `generic` | `.agents/skills/` | `~/.agents/skills/` |
| `codex` | `.agents/skills/` | `~/.agents/skills/` |
| `claude` | `.claude/skills/` | `~/.claude/skills/` |
| `copilot` | `.github/skills/` | `~/.copilot/skills/` |
| `devin` (CLI) | `.devin/skills/` | `~/.config/devin/skills/` |

Each destination contains `<name>/SKILL.md` and that skill's resources. This
table describes installer output, not verified runtime compatibility. Confirm
skill discovery, instruction-file support, and reload requirements with the
client version you use. The installer does not start or configure a harness.

The `devin` option is a **Devin CLI** filesystem mapping. It does not configure
cloud Devin, connect repositories, or establish cloud indexing behavior. For
cloud Devin, use its documented repository location and configuration; copy
skills manually when that location differs from the CLI mapping.

### Duplicate locations

Choose one project destination rather than installing the same skill for each
client. Some clients may discover more than one directory. `duplicate-warning`
reports matching skill names in other known project-level skill directories;
it does not merge, remove, or synchronize them. Detection is limited to those
known directories in the selected project: it is not a scan of user homes,
ancestor repositories, arbitrary client configuration, or cloud state. A warning
does not prove which copy a running client will use.

## Updates and preservation

The installer validates selected sources before copying and maintains
`agent-toolkit.lock.json` in the destination skills root. It compares current
source and destination fingerprints with the recorded installation.

| Outcome | Condition | Effect |
|---|---|---|
| `installed` | Destination skill absent | Copy the complete skill directory |
| `up-to-date` | Destination matches source | Leave skill content unchanged |
| `updated` | Destination matches the recorded install, but source changed | Replace with current source |
| `skipped-conflict` | Different destination lacks a matching recorded fingerprint | Preserve destination; reconcile manually or explicitly use `--force` |
| `duplicate-warning` | Another known project-level location contains the selected skill name | Report the other location; leave it untouched |

`--force` permits replacement of a conflicting **whole selected skill
directory**, deleting local edits and locally added files inside it. Review or
back up those changes first. Unselected skill directories, duplicate copies,
project source, `.agent/` artifacts, and `AGENTS.md`/`CLAUDE.md` are not replaced.
The destination lock is installer bookkeeping, not a dependency resolver.

Exit codes: **0** success, **1** validation problems, **2** usage or selection
errors, **3** one or more conflicts skipped. Safe work may complete before a
conflict is reported; exit 3 does not mean every selected skill was skipped.
To update a team installation, update this checkout and repeat the original
command with the same destination and selection. Review the output and commit
installed files and the lock if your team tracks them.

## Project instructions: manual opt-in

Installing a skill does not modify project instructions. For a map bootstrap,
review [the snippet](../skills/project-map/assets/bootstrap-snippet.md) and the
[create workflow](../skills/project-map/references/workflows.md). Propose the
pointer first; append it only with explicit permission and only when no
equivalent exists. Never overwrite existing instructions. Use the instruction
file the actual client supports, rather than assuming every client reads
`AGENTS.md` or `CLAUDE.md`.

Installing the map skill alone does not guarantee routine map consultation.
Use appropriate agent instructions or explicit invocation; behavior varies by
harness.

### Optional focused-changes policy

Review [the policy](../policies/focused-changes.md), then incorporate it into
the instruction file your client actually loads: `AGENTS.md`, `CLAUDE.md`, a
supported Copilot instruction file (for example `.github/copilot-instructions.md`),
or configured Devin/other client instructions. This is plain instruction text,
not a skill; profiles and the installer never apply it. Enforcement varies by client.

For an existing `AGENTS.md`, from the toolkit checkout, after checking that no
equivalent section exists and deciding to opt in:

```bash
PROJECT="/absolute/path/to/project"
{ printf '\n'; cat policies/focused-changes.md; } >> "$PROJECT/AGENTS.md"
```

Choose the correct instruction path before running. This appends, never
overwrites; run once to avoid duplication. For managed or UI-based instructions,
copy the section manually instead. No other skills are required.

## Running bundled checkers

These examples assume a project-scope `generic` or `codex` install. Set each
`*_SKILL_DIR` to the **actual absolute directory containing the installed
`SKILL.md`**, adjusting for another harness or user scope. Replace the project
and audit run paths with real values. The checkers inspect existing artifacts;
they do not create a map or conduct an audit.

```bash
PROJECT="/absolute/path/to/project"
MAP_SKILL_DIR="$PROJECT/.agents/skills/project-map"
AUDIT_SKILL_DIR="$PROJECT/.agents/skills/project-audit"

python "$MAP_SKILL_DIR/scripts/map_check.py" --repo "$PROJECT" --map-dir "$PROJECT/.agent/project-map"
python "$AUDIT_SKILL_DIR/scripts/check_report.py" --project "$PROJECT" --run "$PROJECT/.agent/audits/existing-run-id"
```

A clean mechanical check is not proof that all map claims or audit judgments
are correct. Inspect source and record executed evidence separately.

## Manual installation

1. Confirm the client's supported project or personal skill path.
2. Copy the complete `skills/<name>/` directory there, including its resources.
3. Check that `<destination>/<name>/SKILL.md` exists and confirm discovery using
   the client's supported mechanism. Reload only as required by that client.
4. Keep one maintained copy per intended scope; reconcile updates manually
   unless the installer has a matching provenance record.

A manually copied directory has no installer history. Identical content can be
recognized as up-to-date, but a differing unrecorded copy is a conflict, not an
automatically trusted upgrade.

## Windows and WSL

The installer uses filesystem copies, not symlinks. Native Windows paths and
WSL paths are different namespaces: in WSL, use `/mnt/c/...` for files on `C:`
and run the command with the interpreter and home directory intended for your
client. `--scope user` follows that interpreter's environment; a WSL home is
not a Windows client's personal skill directory.

Use absolute native paths when running native Python, or absolute Linux paths
when running WSL Python. The shell examples above use Bash syntax. No live
Windows or cross-harness activation guarantee is implied by filesystem tests.

See [architecture](architecture.md), [contributing](contributing.md), and the
[existing acceptance procedures](../tests/acceptance/README.md) with
[recorded evidence](../tests/acceptance/results.md).
