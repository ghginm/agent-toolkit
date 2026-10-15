## Focused code changes

- Implement the smallest clear solution that fully satisfies the task and its constraints.
- Prefer existing project patterns, interfaces, and utilities over new abstractions.
- Avoid speculative generalization, redundant wrappers, indirection, configuration, and boilerplate.
- Keep changes focused. Refactor unrelated code only when needed for correctness or clearly authorized.
- Prefer straightforward control flow and meaningful names over elaborate architecture.
- Handle realistic failures appropriately; avoid defensive code for impossible or irrelevant scenarios.
- Preserve required error handling, security protections, useful modularity, and project conventions.
- Remove unused code, redundant helpers, placeholders, and unsupported compatibility layers introduced by the change.
- Add tests and documentation where they support correctness and maintenance.
- Implement justified complexity, abstractions, and scalable architecture when necessary; do not force artificial minimalism or numeric code limits.
- Before finishing, review the diff and remove unnecessary complexity without sacrificing correctness or readability.
