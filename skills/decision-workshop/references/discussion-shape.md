# Compact discussion shape

Use this guidance for preparation, not as a mandatory output schema. Preserve
existing destinations and decision-register conventions. Prefer the default
guide and register to a new file for every section.

## Repeatable decision block

Use the same short shape for global and local decisions. Let the register row
and guide block share a stable ID. Use headings, a compact table, or short labeled
paragraphs to suit the audience; no fixed number of options or paragraphs is needed.

### D-001 — [Question in plain language]

- **Current / evidence:** [What happens now; supporting citation and its limits.]
- **Why it matters:** [Concrete constraint, consequence, or opportunity here.]

| Option | Benefit here | Cost / risk / constraint |
|---|---|---|
| Keep the current approach, if credible | ... | ... |
| Meaningful alternative | ... | ... |

- **Recommendation:** [Preferred option and reason, conditional on evidence or
  an unresolved dependency; otherwise name the missing evidence. Not approval.]
- **Exact decision:** [The bounded choice the team must confirm, including any
  scope or condition; link prerequisite decision IDs.]

Ask for one primary choice per block. Put clarifications and acceptance criteria
in a short evidence/dependency note rather than appending several decisions to
the exact question. Split only genuinely independent, in-scope choices. State
shared evidence limits once in current context and link back; do not repeat the
same plugin uncertainty or approval disclaimer in every field and the close.
Move secondary evidence lists and extended reasoning out of the main blocks.

Keep the question distinct from the recommendation: a team must be able to
choose another option or defer it. Avoid vague endings such as "discuss scaling."
For example, ask whether to preserve the current boundary or split it, and name
the criterion or evidence that would justify either choice. Do not invent an
implementation, measured threshold, business constraint, or consensus to make
the block look complete. Mark satisfactory components "no decision needed"
briefly rather than forcing a full block.

## Rules without a second decision catalog

Use the separate rules section for general engineering practices, not constraints
specific to a system boundary, compatibility choice, or other architecture decision.
Keep those constraints in that decision's block and link dependent choices there.
For the general practices:

- **Established:** Cite the policy, contract, confirmed decision, or observed
  source convention. Distinguish a documented requirement from enforcement in
  current code; an observed convention alone does not establish team approval.
- **Proposed:** State the rationale and affected choices. Link to its one
  decision block and register ID if approval is needed, rather than presenting
  advice as an established requirement.

## One home, optional depth

Give each comparison one analysis home, normally its guide block. If an existing
document already supplies a usable comparison, link it and add only the meeting
question/context. The opening, stage overview, rule summary, and register point
there instead of becoming parallel versions of the same argument.

Use an appendix, collapsible detail, or an existing source for long evidence.
Presenter notes can carry prompts or explanations, not hidden constraints or
qualifications that would change a decision. Do not invent owners or dates for
next-evidence requests. Keep the analysis in the guide and outcomes in the register.
