# Contributing

How to change this toolkit well. The two upstream skill-creators (Anthropic's `skill-creator-anthropic`, OpenAI's `skill-creator-openai`) supply the quality bar summarized below; their directories are NOT runtime dependencies.

## Adding an independent skill

1. Create `skills/<new-name>/SKILL.md` — hyphen-case name ≤64 chars matching the directory; frontmatter limited to spec keys (`name`, `description`, quoted single-line description stating what + when + non-triggers; optional `license`, `metadata`). Optionally add `references/`, `assets/`, `scripts/` — only what the skill actually uses. (OpenAI's `init_skill.py` scaffolds the same shape if you want it; drop `agents/openai.yaml` unless you specifically want Codex UI metadata.)
2. `python tools/validate.py` → `result: OK`.
3. Install-test: `python tools/install.py --target <tmpdir> --skills <new-name> --harness generic --dry-run`, then a real run. No installer/registry/profile edits required for discovery; add a profile entry only if the skill belongs in an existing collection.
4. Behavioral check: have a fresh agent (subagent, or yourself in a clean session) do a realistic task from the skill; verify it triggers, follows, and produces the promised artifacts. Keep evidence under `tests/acceptance/`.
5. README catalog row + docs if meaningful. Commit.

A new skill must not import from `tools/` or reference files outside its own directory at runtime.

## Modifying an existing skill

Same loop: edit → validate → unit tests (`python -m unittest discover -s tests`) → re-run the relevant acceptance scenario → commit. If you changed shared conventions (evidence status names, citation format, `.agent/` paths, finding-ID format, lifecycle states) — sync BOTH skills and `docs/architecture.md`; the contract is intentionally duplicated so each skill installs alone.

## Quality checklist (condensed from both creators)

- **Description does the triggering work**: what + when + realistic-phrasing keywords + explicit non-triggers; no angle brackets; ≤1024 chars but aim < ~600; don't repeat the skill name; avoid marketing adjectives. Undertriggering is the common failure — be specific about tasks, not modest.
- **Every paragraph earns its tokens** (OpenAI: "challenge each piece of information"); delete or move to a reference if it doesn't change behavior.
- **Explain why, don't stack MUSTs** (Anthropic writing style) — except where a hard rule IS the point (evidence honesty, "verify code before implementing"): those stay firm, and the reason is stated once.
- **Degrees of freedom** (OpenAI): deterministic + repeated + testable → script; judgment → prose with reasoning. Never script semantic evaluation; never leave fragile mechanical steps to improvisation.
- **Progressive disclosure**: SKILL.md < 500 lines (target far less); references one level from SKILL.md, each focused, >100-line files get a Contents list; templates in `assets/` referenced by name; SKILL.md says *when* to open each resource.
- **No duplication** between SKILL.md and references beyond pointers + one-line framing; a rule lives in exactly one place.
- **No auxiliary files in the skill dir**: no README/CHANGELOG/dev-notes; user-facing docs belong to the repo root.
- **Portability**: works in plain filesystem terms — no harness tool names in skill bodies, stdlib-only scripts, cross-platform paths (pathlib), git optional everywhere.
- **Scripts are tested by running them** (both creators demand this); fixtures under `tests/` exercise them.
- **Independence**: copy the skill folder to a blank project — everything it promises must still work.

## Validation commands

```bash
python tools/validate.py
python tools/validate.py --creators /path/to/skill-creator/skills   # optional: run upstream quick_validate.py (needs a PyYAML-capable python)
python -m unittest discover -s tests -v
```

Upstream validators check frontmatter basics (name/description/keys/lengths); `tools/validate.py` adds local-reference integrity, directory/name consistency, and skill-shape warnings. Running both is cheap — CI habit: upstream when available, toolkit always.

## Behavioral acceptance

`tests/acceptance/README.md` defines the scenario suite (audit against a flawed ML fixture; map create/route/stale/update/missing/small-large). Unit tests prove the mechanics; acceptance runs prove the *agent behavior* the brief cares about. Re-run affected scenarios on skill edits, record results per the acceptance README.
