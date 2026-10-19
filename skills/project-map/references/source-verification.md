# Source verification for map claims

Apply this checklist in create, update, and validate. Keep the work proportional
by selecting useful claims, not by accepting weaker evidence. No sibling skill
or repository-wide scan is required.

## Check each important current-state claim

- Identify the exact assertion: entrypoint, routing target, responsibility,
  dependency, configuration behavior, contract, invariant, or capability.
  Use existing docs/cards to locate candidates, then open current source and
  read the relevant bodies and branches, not just names, headers, or search hits.
- Trace boundary claims through the actual caller/consumer and producer.
  For config, follow definition/default → loading and overrides → effective
  value at the consumer. A declared option or imported helper does not prove
  it controls the active path. Cite the sites that establish the connection.
- For end-to-end flow, follow the selected entrypoint through dispatch,
  transformations, and output; check alternate/error paths when the claim
  includes them. Distinguish a defined helper from a reachable capability.
- For a missing capability, search plausible names and equivalent mechanisms,
  inspect the likely entrypoints, registrations, config, and consumers, and
  state the paths searched and remaining limits. Write “not found in the
  inspected flow” rather than “the project has no X” from a filename search.
- Attach `path::symbol` or `path:line` to the claim it supports. A `sources:`
  list or one citation somewhere in a card does not establish all its prose.
  Cite evidence of intent as intent only; label unsupported rationale `inferred`.

## Separate evidence without adding statuses

- `verified-static`: the implementation was read and supports the scoped claim.
- A test file's existence is navigation evidence only. Read its assertions,
  setup, mocks, and selected path before saying what it tests; this is still
  `verified-static`, not proof that it passes or that runtime behavior is sound.
- `verified-executed`: record the command, observed result, baseline/date, and
  exact claims exercised. Note skips, failures, missing inputs, and unrun paths;
  a passing smoke test does not execute every contract or invariant.
- Keep indirect conclusions `inferred`, future changes `proposed`, and known
  drift `stale`. Do not use audit-only `unknown` as card metadata; explain
  uninspected or unresolved claims in prose.

## Preserve per-card coverage and baselines

- Record inspected claims/source paths, tests read versus commands run, and
  uninspected boundaries in the card's Verification section. L1 summarizes
  coverage; its own baseline never refreshes the linked cards.
- Before advancing a card's `verified_revision`/`verified_at`, recheck all
  important current-state claims covered by that stamp, including boundary
  callers and effective configuration. On partial repair, retain the older
  card baseline and date; annotate changed claims with their actual newer
  baseline, dirty paths, and scope. Keep unrelated text and metadata unchanged.
- Validation sampling records exactly which claims were checked. Do not stamp
  an entire sampled card from two checked lines or refresh uninspected cards.
  A comment-only change with unchanged useful facts needs no map rewrite.
- Run map_check for structure and report its result separately. Existence of
  cited files, valid metadata, affected-path matches, and a known Git SHA do
  not prove semantics or dependency completeness. Resolve contradictions from
  source, or flag drift and residual uncertainty rather than inventing a pass.