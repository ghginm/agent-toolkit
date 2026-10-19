<!--
L3 capability/subflow card — .agent/project-map/capabilities/<name>.md.
Write ONLY with a stated trigger: complex dependency web, non-obvious state/
control flow, high change frequency, risky boundary, repeated agent confusion,
important invariants, or a subsystem needing frequent targeted changes.
Delete template comments in the written card.
-->

```
capability: <kebab-id>
module: <parent-L2-module-id>
status: verified-static
verified_revision: <git-sha|none>
verified_at: <YYYY-MM-DD>
sources:
  - <paths across modules that the flow touches>
```

# <Capability name>

## Why this card exists (trigger)
<one line, factual: "3 of the last 5 changes to imputation regressed serving (see commits ...)" / "feature-selection flow spans 4 modules with non-obvious ordering">

## The flow
Step by step with citations:
1. <what enters, where> — `path::symbol`
2. <transform/state transition; ordering or state assumptions>
3. ...
N. <what leaves, to whom>

## Invariants that must hold
- <e.g. "train and serving must consume the same imputation config (`cfg[impute]`) — enforced by shared loader (cite)" >
- <each one cited or labeled inferred>

## Safe-change checklist for this subflow
- [ ] <verify the entry assumption by reading X>
- [ ] <run test Y at path Z>
- [ ] <check the counterpart module (list)>
- [ ] <what to update in the map afterwards>

## Related cards
- Parent: [modules/<parent>.md]; other touchpoints: [<links>]

## Verification
- Source inspected: <flow claims + callers/config consumers>; not inspected: <paths/boundaries>.
- Baseline: <revision + date + dirty paths>. Partial repair: <changed claims + newer baseline; retain older card stamp unless all important claims rechecked>.
- Tests located/read: <paths + assertions inspected, or not read>. Executed: <command + observed result + claims exercised, or not run + reason>.
