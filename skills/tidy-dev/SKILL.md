---
name: tidy-dev
description: "Choose and implement worthwhile local structural improvements before, during, or after a code change, or assess a mixed diff. Use when asked whether to tidy first, untangle refactoring from behavior, or simplify structure that materially obstructs the requested change. Not for every coding task, a clear condition change in well-structured code, stylistic cleanup, unrelated refactoring, or a project-wide architecture audit."
license: MIT
metadata:
  author: agent-toolkit
  version: "0.1.0"
---

# Tidy Dev

Choose **tidy first**, **tidy afterward**, or **no tidy** around a concrete coding
task. No tidy is a normal success, not a missed opportunity. Keep the effort
smaller than the problem it removes; do not run a full architecture audit.

## Inspect and choose

1. Establish the requested behavior or assessment scope. Read project
   instructions, relevant source, callers, and tests. If Git is available,
   inspect status and the relevant diff; preserve pre-existing user changes.
   Without Git, compare the inspected source and proposed changes directly.
2. Identify a structural obstacle tied to the task, if any. Consider a focused
   helper extraction, clearer name, simpler conditional, reduced duplication,
   or better responsibility boundary. Cite the affected code and explain the
   concrete benefit, not just a cleanliness preference.
3. Weigh implementation clarity, maintenance benefit, review cost, regression
   risk, and verification coverage against the extra work. Reject speculative
   abstractions, cosmetic churn, unrelated cleanup, and broad rewrites.
4. Choose one outcome:

   | Outcome | Use when | Next step |
   |---|---|---|
   | **Tidy first** | A small, low-risk structural change materially simplifies or de-risks the requested behavior | Make and check that focused improvement, then implement behavior |
   | **Tidy afterward** | The fix is clearer or safer first, or only the finished behavior reveals a useful cleanup | Complete and verify behavior; do optional in-scope cleanup only if still worthwhile |
   | **No tidy** | Structure already supports the change, or benefit does not justify cost/risk | Implement directly, or finish the requested assessment |

A simple condition rarely needs a hierarchy, registry, or configuration layer.
Do not impose line, file, function, or test-count limits: justified complexity
still belongs in the solution. During implementation, reconsider the sequence
only if structure and behavior become materially entangled, not after every edit.

## Distinguish intent from proof

| Change | Intended effect |
|---|---|
| Extract, rename, move, simplify structure, consolidate duplication | Structural: preserve externally observable behavior |
| Add a feature, fix a bug, or change outputs, validation, business rules, or algorithm behavior | Behavioral: deliberately change what the program does |

A structural-looking edit can still change call order, side effects, exceptions,
public interfaces, serialization, or timing-sensitive behavior. Inspect those
contracts rather than classifying from syntax alone. Renaming a public symbol
without preserving consumers is not merely an internal cleanup.

Passing unchanged tests supports preservation only for what they cover; it does
not prove complete equivalence. Adding characterization tests can improve
confidence without turning the intended structural change into a feature.
When baseline tests fail, distinguish pre-existing failures from regressions.

## Act within authorization

- For assessment-only requests, remain read-only: give the decision, scope,
  reasoning, and proposed verification; do not edit code or create reports.
- Within an authorized coding task, make only justified local improvements,
  implement the requested behavior, and respect existing project conventions.
  Propose substantial or unrelated refactoring before doing it.
- Separate structural and behavioral steps where that makes review and
  verification clearer. Favor small, reversible edits. Do not force separate
  branches, commits, handoffs, fresh sessions, or conventional commit formatting.
- Do not rewrite or discard user changes to reconstruct a clean intermediate
  state. If separation would be artificial or unsafe, explain the mixed scope
  briefly and verify it together instead.

## Verify and finish

1. Establish relevant baseline behavior when practical; use existing tests and
   focused checks for the affected contracts. Add characterization coverage
   when a worthwhile tidy needs it, especially around critical behavior.
2. Check a tidy-only step before behavior changes where practical, then test
   the requested behavior and any subsequent cleanup. Use the project's normal
   validation commands; do not skip needed regression checks to save work.
3. If risk is high or coverage inadequate, narrow or defer the tidy, or obtain
   authorization for the needed coverage first. State unavailable checks and
   unverified behavior instead of asserting equivalence.
4. Review the final diff for scope creep, unnecessary abstraction, and accidental
   behavior changes. Report the decision, meaningful changes, executed checks,
   and remaining uncertainty concisely.

Example assessment: **Tidy first:** Isolate parsing in the affected function
before adding the new branch; preserve current error and output contracts with
focused tests. **No tidy needed:** Existing structure supports the change.

Other skills and project maps are optional. Do not invoke them automatically,
regenerate navigation for inconsequential edits, or require a persistent report.
