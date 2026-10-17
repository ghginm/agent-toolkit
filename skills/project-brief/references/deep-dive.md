# Deep-dive review pack

Build understanding sufficient to discuss the architecture, not a longer audit.
Retain the evidence and refresh discipline from SKILL.md. Use the actual system
boundaries; a library, service, or CLI need not have a sequential pipeline.

## Organize for progressive reading

Start README with purpose, core ideas, current state, an end-to-end current-flow
diagram, important limitations, priorities, and links. Explain unfamiliar terms
once. Keep this entry point readable in 2–3 minutes even when the pack is large.

Choose modules around substantial reader questions, not source-file counts.
Three documents may suffice. For a complex project, consider current-state.md,
target-architecture.md, requirements-register.md, roadmap.md, and selected
steps/<stage>.md pages. These are examples, not required names or a fixed tree.
Respect existing authored structure and the requested destination. Split only
when detail would obscure the entry point; link rather than repeat material.

## Cover the consequential questions

| Topic | Explain | Useful representation |
|---|---|---|
| Core ideas | Purpose, key concepts, architectural principles, terminology, assumptions; distinguish documented rationale from inference | Small concept table |
| Current state | Implemented capabilities, observed working scope, not verified, experimental/incomplete parts, architectural and operational limits | Status/evidence table |
| Architecture | End-to-end data and control flow, external systems, manual steps, important failure paths | Current diagram first; separately labeled proposed diagram with text fallbacks |
| Stages or components | Purpose, inputs/outputs, current behavior and connections, constraints, alternatives, trade-offs, potential improvements | Consistent stage blocks below |
| Cross-cutting concerns | Relevant testing, reliability, maintainability, observability, reproducibility, security, deployment constraints | Concern → local evidence → impact → proportionate improvement |
| Requirements and decisions | Confirmed requirements, proposals, unresolved questions, previous choices and experimental lessons | Source-linked register |
| Direction | Immediate priorities, dependencies, experiments needed, deferrable work and reconsideration triggers | Decision-oriented roadmap |

Use these as coverage guidance, not mandatory headings. Omit irrelevant concerns;
when a consequential area is unknown, state the missing evidence rather than
filling it with generic best practices. If no target design is supported, say
that it remains open instead of inventing one.

## Explain comparable stages consistently

For each substantial stage, adapt this compact block:

- **Purpose and contract:** why it exists; inputs → outputs; preceding/following
  components and stable interface assumptions.
- **Current:** implemented behavior, verification scope, experimental parts,
  limitations, source links.
- **Choices:** meaningful alternatives, including retaining a satisfactory
  implementation; compare benefit, complexity, compatibility, and local cost.
- **Direction:** proposed improvement and reason, or keep as-is; identify the
  measurement or clarification needed where no recommendation is justified.

Prefer tables and diagrams to extended prose. Keep evidence-linked analysis
that explains a decision; omit exhaustive symbol inventories and copied audit
reasoning. External knowledge can suggest a comparison, not establish what the
repository implements or guarantee a proposal's benefit.

## Recover requirements without inventing history

Read selected specifications, decision records, user constraints, and experiment
results. Record each consequential requirement or previous decision with its
source, status, rationale/outcome if documented, and any uncertainty. Preserve
existing IDs. Separate confirmed requirements from proposed changes and open
questions; a past suggestion or accepted audit finding is not proof of team
agreement or implementation. Do not infer a historical requirement from code
alone. If no history was supplied or found in scope, say so.

## Verify depth rather than volume

Check that the reader can explain the real end-to-end flow and the important
stage contracts, distinguish current from target architecture, find the basis
for requirements and lessons, compare meaningful alternatives, and identify
which open questions block next steps. Check navigation and evidence links
from every module. Check that proposed diagram edges preserve the validation
and approval gates stated in the prose, rather than implying automatic adoption.
Keep the roadmap a set of priorities and decision gates,
not an unsolicited implementation plan. Do not equate a large pack with depth.
