# Recommended contract examples

These are practical examples of combining independent skills, not required
workflows or architectural dependencies. Choose only the steps that serve the
project. No workflow runner, registry, or mandatory metadata schema is needed.

## Project Review → Architecture Discussion

| Step | Skill(s) | Purpose | Output |
|---|---|---|---|
| 1. Technical Review | `project-map` + `project-audit` | Understand implementation and identify evidence-grounded problems | Agent-oriented map and technical audit |
| 2. Human Review | `project-brief` (deep-dive) | Explain architecture and design from technical evidence and optional supplied external knowledge | Human-readable review pack |
| 3. Discussion Preparation | `decision-workshop` | Turn the review into a structured team discussion and decision matrix | Markdown discussion guide |
| Optional: Presentation | Available dedicated slide tools | Present the reviewed discussion structure without hiding open choices | PPTX or slide outline |
| Optional: Consolidation | `decision-workshop` | Record what the team actually decided from meeting notes | Updated decision register |

A workshop can start directly from architecture documents, design proposals,
requirements, or existing decision records; a prior brief is not required.
Likewise, a brief can use source and existing documentation without a map or audit.
Reuse relevant materials selectively, not entire maps or report collections.

Default artifact locations are `.agent/project-map/` for navigation,
`.agent/audits/<run-id>/` for technical evidence, `docs/project-brief/` for human
review, and `discussion/` for discussion materials. Respect user destinations.
The compact brief remains the default: `README.md`, `pipeline.md`, and `roadmap.md`.
Deep-dive uses a short linked README and only the modules the project needs.
The workshop defaults to `discussion/README.md` and `discussion/decisions.md`.

### Contract 1 — Technical Review

```text
Use project-map and project-audit to inspect this repository. Build or update an
agent-oriented map and perform an evidence-grounded technical audit of relevant
architecture, reliability, and methodology concerns. Reuse existing information,
check it against current source, distinguish verified findings from assumptions,
and do not modify application code.
```

### Contract 2 — Human Review

```text
Use project-brief in deep-dive mode. Synthesize the technical review, project
documentation, source, historical requirements, and any supplied external knowledge
into a human-readable review pack. Start with the big picture, then explain the
actual architecture stage by stage. Distinguish current state from target direction;
cover important problems, alternatives, lessons, and unresolved requirements.
Prefer diagrams, tables, and linked evidence; do not invent history or treat
external guidance as proof of repository behavior.
```

### Contract 3 — Discussion Preparation

```text
Use decision-workshop to prepare a team architecture discussion. Begin with current
and proposed high-level architecture. Prioritize structural decisions, then discuss
stages consistently: current implementation, problems, options, trade-offs,
recommendations, and decisions required. Produce a visual-first Markdown guide
and decision matrix. Keep recommendations distinct from agreed choices. Do not
generate slides, an implementation plan, or application changes yet.
```

For consolidation, supply meeting notes or explicit choices. Preserve decision IDs
and provenance, using `Open`, `Proposed`, `Agreed`, `Deferred`, and `Rejected`;
never infer agreement from silence. Record unresolved questions and requirements
implied by confirmed choices without rewriting unrelated documentation.

If slides are requested, review the Markdown structure first and use an available
dedicated capability, or provide a concise outline if none is available. Slides
remain optional and should preserve decision questions and meaningful trade-offs.

See [installation](installation.md) for independent skill selection and
[architecture](architecture.md#artifact-handoffs-and-human-outputs) for evidence
boundaries. These examples add no runtime dependencies to any skill.
