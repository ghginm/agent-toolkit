# Map Card Format

Read before authoring cards. This defines what a card must carry and how claims stay honest. Templates in `assets/` show the shapes; this file explains the semantics.

Contents:
1. The metadata block
2. Claim citation rules
3. L1 index anatomy
4. L2 module card anatomy
5. L3 capability card anatomy
6. Anti-patterns

## 1. The metadata block

A fenced block at the top of every card — flat `key: value`, one-level lists (block or `[a, b]` flow style), inline `#` comments allowed — kept trivially parseable so `scripts/map_check.py` checks it with stdlib code:

```
module: <kebab-case-id>            # unique in map; MUST equal filename for L2/L3
status: verified-static            # one token from the SKILL.md vocabulary
verified_revision: <full-or-short-git-sha | none>
verified_at: <YYYY-MM-DD>          # date of the verification pass, not a promise of depth
sources:                           # repo-relative paths this card's claims rest on
  - src/features/builder.py
  - src/pipelines/train.py
```

Optional additions when they earn their keep: `tests:`, `config:`, `depends-on:`/`depended-on-by:` (card ids; map_check validates them and update fans out through them on interface changes). Index cards (`index.md`) carry `status`/`verified_revision`/`verified_at` but are exempt from `module:`/`sources:`.

Status vocabulary and honesty rules are canonically defined in SKILL.md. Card-authoring specifics on top of them:

- A README is evidence of a documented promise, not implemented behavior. Cite it as such; inspect current implementation before verifying the behavior. Follow the source-verification checklist loaded from SKILL.md for callers, config, absence claims, and partial card baselines.
- `verified-executed` requires the exact command + observed result inline in the card's Verification section (e.g., `pytest tests/features -q → 12 passed, <date>`), and covers only those claims.
- `proposed` as card status is reserved for whole cards about intended future structure; proposed content for an existing module goes in its `Decisions & proposed direction` section instead.
- `stale` cards name at the top what drifted; repair via drift recovery rather than letting them rot.
- Mapping uncommitted work: record the dirty-tree caveat inside the affected card, not just `verified_revision`.

## 2. Claim citation rules

- Format: `path::symbol` or `path:line` (line numbers are hints; symbols are durable).
- Anything a card asserts about behavior, contracts, or dependencies cites inspected source supporting that specific claim. A source list is not blanket evidence for the card. Prose about obvious structure ("src/ contains the library") needs no citation.
- Navigation content ("where to look for X") points at files/symbols — that IS the citation.
- No secrets, tokens, connection strings, or personal paths in cards. For sensitive areas: describe the mechanism's location, not its contents.

## 3. L1 index anatomy

`assets/l1-index-template.md` shows the skeleton; budgets are in the SKILL.md hierarchy table. Sections:

1. **Project** — one-paragraph purpose (cited to README/code only if non-obvious).
2. **Capabilities / major modules** — table linking each L2 card, one-line responsibility.
3. **Entrypoints** — how it actually runs: main scripts, CLI, server, notebook; verified by reading, not folklore.
4. **Build & test** — commands whose existence was verified (config present, script referenced); mark anything not executed as `verified-static`.
5. **Data/control flow** — 3-8 lines or one compact diagram description of how things run end to end.
6. **Task → module routing guide** — the core navigation payload: "change/add X → start in card Y / files Z". 10-25 rows for a mid-size repo, fewer for small. Write rows for tasks a coding agent would plausibly bring.
7. **Coverage & uncertainty** — which parts are mapped (L2/L3 list), which are deliberately unmapped, current `status` distribution. Keep honest: this section is how later agents calibrate trust.

Budget (SKILL.md table): target a few hundred tokens; if L1 swells, it is duplicating L2 — cut content, add links.

## 4. L2 module card anatomy

`assets/l2-module-template.md`. Required sections after metadata:

1. **Responsibility** — 2-4 sentences: what this module owns, what it deliberately does not.
2. **Key entrypoints & symbols** — table: symbol → file::line-ish → what calls it / what it calls. The "where to look for a given change" list goes here or in a dedicated bullet.
3. **Upstream / downstream** — dependencies verified by reading imports/call sites (cite); note whether verified or inferred.
4. **Contracts** — data/API shapes crossing the boundary (keys, types, units, ordering assumptions, schema source). Contracts are where drift hurts most: be specific and cited.
5. **Configuration & tests** — effective config path (defaults/overrides to consumer), test locations and assertions inspected; distinguish test existence, static inspection, and executed results.
6. **Caveats & invariants** — gotchas, assumptions that break, known sharp edges, why-an-obscure-choice-exists (label inferred rationale if undocumented).
7. **Decisions & proposed direction** *(optional)* — accepted audit findings/plans with links; never merged into sections 1-6.
8. **Where to look for X** — 3-8 rows of task → file/symbol.
9. **Verification** — inspected claims/paths and baseline, uninspected boundaries, tests read, commands/results or not run. Partial repairs keep the older card stamp with newer evidence scoped to changed claims.

Do not enumerate every file. A module with 30 files gets the 6 that matter and a one-line description of the rest ("schemas/ holds per-domain table definitions").

## 5. L3 capability card anatomy

`assets/l3-capability-template.md`. Same metadata block. Only write when triggered (complex dependency web, non-obvious state/control flow, high change frequency, risky boundary, repeated agent confusion, important invariants, frequent targeted subsystem changes). Trigger stated in the card ("Created because: two agents broke X by editing Y" / "3 of last 5 changes touched this flow"). Content: the flow step by step with citations, the invariants that must hold, the safe-change checklist for that subflow, and links back to parent L2/L1. Link to L3 from both the L1 routing guide and the parent L2 card — reachability is what makes progressive disclosure work.

## 6. Anti-patterns

- Inventory mapping: card = file listing. The repo already has `ls`.
- Unverifiable prose: "this module is well designed" — no navigation value; cut.
- Aspirational state: proposed refactor described in present tense. Use section 7 separation.
- Mass metadata refresh: touching `verified_revision` on cards whose content didn't change — fakes freshness and pollutes diffs.
- Deep reference chains: L2 linking into L3 which links another L3 as the only route to something; keep links lateral + up/down one level, and the routing guide in L1 as the hub.
- Stale-tolerant routing: L1 routing rows pointing at deleted files. `map_check.py` catches the dead path; you keep the routing honest.
