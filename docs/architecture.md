# Architecture & Design Decisions

What this toolkit is, what it deliberately is not, and why.

## Goals (from the product brief)

Quality agent behavior — discovery, evidence discipline, proportional depth, incremental maintenance — with the smallest possible technical footprint, portable across harnesses, extensible to unrelated skills without framework work.

## Repository shape

```
skills/     canonical skill implementations (self-contained installable units)
tools/      developer tools only: validate.py, install.py, skillkit.py (helper)
profiles/   JSON skill-lists for convenient installs
tests/      unit tests, fixtures, behavioral acceptance evidence
docs/       this architecture, installation, contributing
```

`skills/` is canonical; there are no per-harness copies. `tools/` is NOT a runtime dependency of any skill: skills that ship scripts (`project-map/scripts/map_check.py`) bundle them, so a lone copied skill still works. This is the load-bearing rule behind every "independent installability" claim.

## Discovery over registry

Adding a skill = creating `skills/new-skill/SKILL.md`. `tools/skillkit.py::discover` scans directories; validator and installer read each skill's own frontmatter. No file elsewhere needs editing. (Verified in tests: `mini-skill` fixture installs through the same code path.)

## Shared conventions are duplicated, not centralized (decision)

`project-audit` and `project-map` use compatible contracts:

- Evidence statuses (shared core): `verified-static`, `verified-executed`, `inferred`, `proposed`. Each skill adds exactly one status for its own object type — `unknown` in audits (a claim that can't be verified in scope), `stale` in maps (a document known to have drifted) — and says so where defined.
- Source citations: `path::symbol` / `path:line`; runtime = command + result.
- Artifact root `.agent/` (`audits/<run-id>/`, `project-map/`).
- Current-state vs proposed-state separation; lifecycle `draft → reviewed → accepted/deferred/rejected → implemented-verified`.
- Finding IDs `AUD-<mode>-NNN` referenced from map cards' *proposed direction* sections when both skills are present.

The brief's two options were a shared contract file or matching embedded conventions. We embed and duplicate (each ~15 lines inside each SKILL.md) because a shared runtime file would create the fragile cross-skill dependency the brief forbids, while duplicated small conventions survive independent installation. Drift risk between the two copies is managed by a sync-check rule in AGENTS.md/contributing. The interlinking that does exist (map helps audits; audits feed map's proposed-direction sections) is opportunistic and degrades silently when the other skill/artifacts are absent.

## Scripts: four total, chosen for determinism (and deliberate non-scripting)

| Script | Why it earns its keep |
|---|---|
| `skills/project-map/scripts/map_check.py` | mechanical path/link/metadata/freshness checking: deterministic, repeated every create/update/validate, cheaper and more reliable than agent eyeballing; stdlib-only; degrades gracefully without git. |
| `skills/project-audit/scripts/check_report.py` | mechanical report-contract checking (cited paths exist, finding IDs/fields complete, report set matches modes, template leftovers absent) — added after creator review flagged the degrees-of-freedom asymmetry: the audit's trust-critical consistency checks were prose-only. |
| `tools/validate.py` | repo developer tool: spec frontmatter + reference integrity across all skills; optionally delegates to upstream creator validators. |
| `tools/install.py` | copy + collision-safe update + lock fingerprint; cross-platform filesystem work agents shouldn't improvise per install. |

Deliberately NOT scripted: audit analysis, map card authoring, dependency judgment, update-policy decisions — semantic work that belongs to the agent (script selection principle §15.4). No git-changes helper as a fourth script: `map_check.py --affected` subsumes change detection with the same stdlib git plumbing calls — splitting them would duplicate a third of each file for no benefit (documented simplification).

## Provenance / update model (intentionally minimal, not a package manager)

The installer keeps one lock file per destination (`agent-toolkit.lock.json`, content sha256 per skill + install timestamp + harness/scope). That's the whole system, enough to distinguish: not installed / unchanged / ours-but-source-updated (silently replaced) / user-modified (skipped + warned; `--force` replaces the entire skill dir and says so). No version resolution, no uninstall dependencies, no registry.

## Harness portability (decision)

- Content: markdown + stdlib python + git-if-available; no tool names, no harness features. `compatibility:` frontmatter intentionally unused (none needed).
- `agents/openai.yaml` (recommended by OpenAI's creator for Codex UI chips) was dropped from shipped skills: it is harness-specific presentation metadata whose generator lives upstream; skills stay neutral and Codex works from spec frontmatter alone. Anyone who wants Codex chips regenerates deterministically: `python /path/to/skill-creator-openai/scripts/generate_openai_yaml.py <skill-dir> --interface ...` at the install destination. This is "harness adaptation as a thin layer", not a skill-content fork.
- Destination map is a plain dict in `install.py` — data, not abstraction. Unknown/new harness → documented manual route (copy the skill dir). Adding one is a one-line dict entry plus a docs row; no adapter framework.
- Windows: copies only (no symlinks), pathlib throughout; live Windows smoke left to users (documented procedure in installation.md) since the dev environment is Linux/WSL.

## What was NOT built (per the brief's anti-goals)

No orchestration, embeddings/vector stores, dependency-graph DB, custom skill runtime, MCP servers, dashboards, background sync, mandatory hooks, AST indexing, approval UI, config sprawl. The one persistence mechanism (lock file) and one artifact convention (`.agent/`) are the entire "infrastructure."

## Creator-guidance reconciliation (Anthropic vs OpenAI skill-creators)

Both creators were used in development (draft → dual critique → revision → validation → behavioral evals). Meaningful differences and how we resolved them — full evaluation outcomes in `tests/acceptance/README.md`:

| Topic | Anthropic creator | OpenAI creator | Resolution |
|---|---|---|---|
| Description tone | "pushy" against undertriggering; all when-to-use in description | same requirement, concise is key | both descriptions state what + when + explicit non-triggers; kept under spec limits; trigger-eval simulated (see acceptance) |
| Extra frontmatter | allows `compatibility` (older fork) | "only name+description; no other fields" (strict reading) | open spec wins: spec-legal keys only, minimal set used |
| `agents/openai.yaml` | n/a | recommended | dropped for harness neutrality (above) |
| Eval machinery | subagent eval loop + benchmark viewer via `claude` CLI | init/validate scripts, qualitative iteration | scripts runnable: both `quick_validate.py` executed; agent-behavior loop run via generic subagents (Claude-CLI-only parts documented as environment limitation, substituted per the brief) |
| Writing style | explain why, few MUSTs | degrees of freedom; challenge token cost | judgment sections argue their why; low-freedom only at evidence/honesty rules (where failure is the point) and in map_check metadata block (parseable-by-design) |
| Duplication | avoid duplication skill-internal | same | SKILL.md = workflow + contracts; references = methodology depth; assets = copy-fill templates; one pointer chain level |
| Extra files in skill dir | (same rule) | explicit ban on README/CHANGELOG etc. | skill dirs contain only SKILL.md + resources; repo docs live at root/docs |

## Extending to an unrelated skill (the test case from §18)

`skills/unity-workflow/SKILL.md` + own resources → `tools/validate.py` → `tools/install.py --skills unity-workflow`. Nothing ML/DS-specific exists outside `project-audit/references/ml-methodology.md`; `tools/`, `profiles/`, `docs/` carry no domain assumptions. The `mini-skill` fixture keeps this claim executable, not aspirational.
