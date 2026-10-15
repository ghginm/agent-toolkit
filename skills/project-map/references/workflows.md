# Map Workflows in Detail

Expanded procedures for `create`, `update`, `validate`, and drift recovery; the update-policy table; non-git handling. SKILL.md carries the discipline; this file carries the steps. Read the section you need.

Contents:
1. §create
2. §update
3. §update-policy
4. §validate
5. §drift recovery
6. Non-git and awkward repositories
7. Map ↔ audit interop

### Command setup (any working directory)

Set `PROJECT` to the actual target's absolute root and `MAP_SKILL_DIR` to the absolute parent of the installed `project-map/SKILL.md` supplied in agent context. Never derive the skill location from CWD or toolkit `tools/`. This concrete `.agents/skills/` example assumes those are the actual paths; substitute the real paths, including any user-level, other harness, or manual install location:

```sh
PROJECT="/work/my-project"
MAP_SKILL_DIR="/work/my-project/.agents/skills/project-map"
python "$MAP_SKILL_DIR/scripts/map_check.py" --repo "$PROJECT" --map-dir "$PROJECT/.agent/project-map"
```

Use that validation command for create/validate/finish checks below. Keep both explicit target flags in affected-card commands too.

## 1. §create

1. **Recon with a budget.** Read: manifests, README/docs *as leads*, CI config, test layout, entry scripts. Get the tree 2-3 levels deep. Timebox breadth: the point is enough to partition responsibilities, not full comprehension.
2. **Partition by responsibility.** Sketch modules: "owns X behavior, changes for Y reasons". Folders are hints, not destiny — merge or split when semantics disagree with directory layout. For each sketch, verify by reading that module's main files (code is the ground truth; a module you haven't read does not get a card).
3. **Choose depth proportionally.** Small/calm repo: L1 + 2-4 L2. Medium: L2 per module, L3 only for triggered subflows (triggers list in map-format §5). Large/legacy: still L1 + L2 — breadth is cheap, depth per area is the expensive part; leave unmapped areas listed in L1 coverage.
4. **Write cards from templates** (`assets/`). Citation as you go: a claim you cannot cite gets `inferred` or stays out.
5. **Run `scripts/map_check.py`** against the map; fix every dead path.
6. **Bootstrap pointer.** Show the user the directly pasteable L0 snippet (`assets/bootstrap-snippet.md`) and offer to append it to the project's agent-instructions file (`AGENTS.md`, `CLAUDE.md`, or what the harness actually reads). **This is the canonical home of the permission rule:** append only with explicit permission, only when no equivalent pointer exists, only as an addition — never overwrite or restructure that file; nothing about existing content may be removed. If the harness reads neither file type, print the snippet and ask the user which instructions location it reads. Installing the skill alone does not guarantee routine map consultation: appropriate agent instructions or explicit invocation are needed, with behavior depending on the harness.
7. **Self-check:** routing guide covers the plausible near-term tasks; every card has honest metadata; no L3 without a stated trigger; L1 within budget.

Resume rule: if `.agent/project-map/` already exists, `create` becomes: validate first, then fill gaps/repair — do not regenerate from scratch, that burns effort and hides drift from the diff.

## 2. §update

1. Candidates: use one of the commands below after the absolute-path setup above. Replace `BASELINE` with the actual baseline revision, or replace the example file paths with changed paths relative to `PROJECT`. With no git: ask the user for scope or a file list and use the explicit-files form.

   ```sh
   python "$MAP_SKILL_DIR/scripts/map_check.py" --repo "$PROJECT" --map-dir "$PROJECT/.agent/project-map" --affected --working
   BASELINE="abc1234"
   python "$MAP_SKILL_DIR/scripts/map_check.py" --repo "$PROJECT" --map-dir "$PROJECT/.agent/project-map" --affected --rev "$BASELINE"
   python "$MAP_SKILL_DIR/scripts/map_check.py" --repo "$PROJECT" --map-dir "$PROJECT/.agent/project-map" --affected --files src/example.py tests/test_example.py
   ```
2. Expand with judgment: for each changed *interface* (signature, data shape, exported symbol), grep importers/callers and add their cards; for changed config or test files, expand to the modules that read them. A changed-file list is not a dependency analysis.
3. For each candidate card: re-read the cited sources, compare against what changed, and apply §update-policy below.
4. Update `verified_revision`/`verified_at` only for cards you actually re-verified. If the working tree is dirty around a card's sources, add the dirty caveat.
5. New module appears? Create its L2 + an L1 routing row + L1 module table row. Deleted/merged module? Remove card, fix L1 and inbound links (map_check will flag stragglers).
6. Finish: run map_check; report which cards changed and which were left alone deliberately.

## 3. §update-policy

| Change observed | Map action |
|---|---|
| Small internal implementation change; card facts unchanged | Nothing (do NOT refresh metadata) |
| Card's stated behavior/entrypoint/caveat became wrong | Update that card's affected lines; honest metadata bump |
| Interface/contract change | Update owning card + dependent cards' contract sections and `depends-on` |
| New significant module | New L2 + L1 rows (module table + routing) |
| Major refactoring/reorganization | Reassess module partition; restructure affected cards; consider deleting L3s whose trigger died |
| Formatting-only / dependency bumps | Usually nothing; note in L1 if a version floor moved (e.g., python 3.9 → 3.11) |
| New recurring confusion or risky flow discovered while working | Candidate L3 — state the trigger |

Tie-breaker for "is this worth a map edit?": would a *future agent doing a task* be misdirected, or measurably slower, if the card stays as-is? No → don't touch.

## 4. §validate

Layer 1 (mechanical) — `scripts/map_check.py`:

- dead `sources:` paths and broken card links; cards without metadata; unknown status values; `verified_revision` unknown to git or behind HEAD; (with `--working`) cards touching dirty files.
- Mechanical pass says references resolve. It says nothing about claims matching behavior — say exactly that in your report.

Layer 2 (semantic) — agent spot-check:

1. Pick the sample: cards with the oldest baseline, most-changed modules since `verified_revision` (git log --name-only over card sources), and 3-5 rows from the L1 routing guide.
2. For each sampled card: verify 2-4 load-bearing claims against current code (the contract lines, the "where to look" targets, the invariants).
3. Discrepancies → §drift recovery. Report a table: card, claim, code reality, action taken or flagged.
4. Honest scope statement: which cards weren't sampled, so the next agent knows what "validated" covered.

A validate run produces at most: repaired cards (when authorized), flagged cards (`status: stale` + note), and the report. It never produces a bulk metadata refresh.

## 5. §drift recovery

When any workflow finds documentation contradicting code (or being unverifiable):

1. Inspect the relevant code until behavior is established (cite what settled it).
2. Determine the discrepancy's true scope: this line only? whole card? related cards sharing the claim? (grep card links + claims.)
3. Repair when you have write authorization: fix claims, set honest status, bump `verified_revision` for what you actually rechecked. Mark genuinely broken-but-unfixed cards `status: stale` with a one-line note — a stale marker is more useful than silent rot.
4. Report residual uncertainty: what remains unchecked, what could also be wrong by association.
5. Never "fix" by trusting the old doc's narrative (see step 1), and never trust old documentation because it carries a valid SHA.

## 6. Non-git and awkward repositories

- No git / no history: `verified_revision: none`, `verified_at` dated; §update's candidate detection uses user-provided scope or manual judgment; validate's revision checks skip with a note. Everything else unchanged.
- Partial git (repo root elsewhere, subdirectory mapping): keep `PROJECT` set to the actual target root and pass both explicit target flags as above; declare unmapped areas and out-of-scope paths rather than silently relying on CWD.
- Huge monorepo: map the area the team works in, declare coverage limits loudly in L1; a truthful partial map beats a thin full one.
- Read-only checkout: build the map in a writable location and hand the user install instructions; don't force writes.

## 7. Map ↔ audit interop

Optional both ways, never required:

- An existing map (`.agent/project-map/`) is discovery acceleration for `project-audit` — its L1 routing + module cards shorten the audit's reconnaissance, but every claim reused must be re-verified (the map can be stale or wrong).
- Accepted audit findings become map input ONLY as `Decisions & proposed direction` entries (linked by finding ID). The map's current-state sections stay implementation-only.
- When a change implementing an accepted finding lands, update the affected cards from the implementation (code), then mark the finding `implemented-verified` on the audit side.
- Finding IDs (AUD-...) and card metadata statuses use the same vocabulary — the shared conventions are duplicated inside each skill's SKILL.md on purpose, so each skill stays independently installable.
