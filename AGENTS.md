# AGENTS.md — working rules for this repository

This repo is a library of Agent Skills plus minimal tooling. It has no build
system, no runtime deps (Python stdlib only), and should stay that way.

## Layout & invariants

- `skills/<name>/SKILL.md` is the canonical source for every skill. Installers
  copy from here; never maintain per-harness duplicate trees.
- A skill must work when copied alone into any project: no reads outside its
  own directory, no imports from `tools/`.
- Frontmatter uses the subset parsed by `tools/skillkit.py`: flat `key: value`
  lines plus a one-level `metadata:` map, with `description` as a quoted single
  line (folded scalars are NOT supported). Keep to spec keys only:
  `name, description, license, compatibility, metadata, allowed-tools`.
- `tools/` scripts: stdlib only, argparse, exit 0 = ok / 1 = problems / 2 = usage.
- `tests/fixtures/skillset/skills/mini-skill` exists to prove discovery
  generalizes; keep it valid or update tests deliberately.
- No new infrastructure (registries, databases, frameworks, hooks) without a
  demonstrated need — check docs/architecture.md first.

## Before committing a change

1. `python tools/validate.py` → `result: OK` (with `--creators
   ../skill-creator/skills` when available and PyYAML reachable).
2. `python -m unittest discover -s tests` → all pass (run under ≥2 Python
   versions if both are available: system 3.12, hermes 3.14).
3. Edited a skill's SKILL.md? Verify every `references/…`, `assets/…`,
   `scripts/…` token still resolves, and the file stays under 500 lines.
4. When modifying shared contracts or conventions (evidence statuses, `.agent/`
   paths, finding-ID format), update all affected skills and references,
   including docs/architecture.md. Do not modify unrelated skills.
5. Skills changed → re-run at least the affected acceptance scenario from
   tests/acceptance/ (procedure in that README).

## Style

Markdown in US English. Imperative instructions in skills; explain *why*
instead of stacking MUSTs. Prefer deleting an instruction over rewording it.
No marketing adjectives in descriptions or docs.
