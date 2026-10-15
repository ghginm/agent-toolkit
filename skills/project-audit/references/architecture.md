# Audit #1 — Architecture, MLOps, and Engineering Practices

Evaluate whether the structure supports maintainability, modularity, experimentation, extensibility, and agent-assisted development. ML/DS algorithm choices belong to Audit #2; here the question is whether the *engineering* around them is sound.

Contents:
1. Proportionality tiers (expectations per tier)
2. Inspection areas and probes
3. Applying the context-sensitivity recommendation gate
4. Anti-patterns in recommendations (what not to propose)
5. Handoff shape

## 1. Proportionality tiers

Tier assignment (signals: who runs it, change frequency, external consumption) is defined in SKILL.md §2.4. What follows is what each tier *expects* — calibrate every severity and recommendation to it. A project's behavior outgrowing its tier — or infrastructure massively exceeding it — is itself a finding (both directions are fair game).

| Tier | What "good" means | What is NOT expected |
|---|---|---|
| **Prototype** | runs reproducibly from its inputs; assumptions documented in-place | CI, packaging, abstraction layers |
| **Research / experiment** | experiment isolation, seed/config discipline, results traceable to code+data versions | deployment plumbing, service layers |
| **Reusable pipeline** | module boundaries, interfaces per stage, environment reproducibility, real tests on core logic | microservices, orchestration frameworks |
| **Production platform** | observability, CI/CD, artifact & data lineage, rollback path, error handling under load | — |

## 2. Inspection areas and probes

For each area: what to look at, what counts as a problem *with evidence*, and what does not qualify. Use grep/read breadth-first (structure), then depth-first on suspect spots. Record which areas were covered vs skipped.

**a. Responsibility and coupling.** Largest files, import fan-in/fan-out, functions doing >1 job, shared mutable state, circular imports. Probe: file sizes; grep imports to sketch the dependency direction; read the 3–5 largest modules' headers and main entry functions. A finding needs: the coupling/size demonstrated at a path (`x.py:1-400 mixes ingest+train+report`), plus a concrete harm already visible (test can't cover training without touching network, etc.).

**b. Boundaries and contracts.** Where do modules hand data to each other? Dict-telepathy vs typed/defined interfaces is fine when few and stable; a finding when drift has already occurred or when two consumers assume different keys. Probe: grep for shared dict/frame access patterns (`df["`, `cfg[`, `payload[`), read the data shapes crossing module lines.

**c. Pipeline stage separation (ML projects).** Are ingestion / preprocessing / feature engineering / training / evaluation / inference distinguishable in code, and is preprocessing shared *the same code* between train and inference paths? Divergent preprocessing implementations between the two paths are a P0/P1 class finding — cite both sites.

**d. Configurability and experiment isolation.** Hardcoded paths/params that change per run vs config surface. Probe: grep absolute paths, seeds, dates in code; check output dirs for overwrite collisions (runs writing to the same `model.pkl`). Finding standard: show a place where configuration friction already caused duplication or risk — not "should have a config framework".

**e. Dependencies and environment.** Manifests present, pinned or floating, lockfiles, system-level coupling (CUDA, python version), undocumented installs. Probe: read manifests; try nothing destructive; note reproducibility gaps with exact missing pins.

**f. Tests and CI.** Run the suite if cheap (`pytest -q` or documented equivalent) — record command+result; read a sample of test files to judge what they actually cover vs their names. Check CI config exists AND matches how tests are run locally (a CI file referencing a missing test command is a finding). No suite at all is only a finding relative to tier: expected for reusable pipeline and up; for lower tiers, report as tier-appropriate observation, not violation.

**g. Artifacts, data, and model management (tier ≥ 3).** Where do models/data/checkpoints live; are they versioned or addressable; are large binaries committed; is there any naming/retention scheme. Probe: check `.gitattributes`, committed large files (git count-objects / `du`), output paths in configs.

**h. Deployment and operations (tier 4).** Serving entrypoint, logging structure, error handling at boundaries (grep bare `except`, swallowed errors), health/metrics, secrets handling (do not print secret values; citing a file/line where a secret appears in plaintext is enough).

**i. Duplication and debt hotspots.** Copy-pasted blocks, near-duplicate modules, dead code with no references, TODO clusters around risky areas. Probe: grep repeated function names, read the TODO/FIXME population in the risky subsystem only.

**j. Agent-friendliness of the repo.** Can an agent build/test/run from documented commands? Is there AGENTS.md/CONTRIBUTING with working instructions (verify the commands' existence, not their prose)? Are entrypoints discoverable or folklore-only?

## 3. Applying the context-sensitivity recommendation gate

The six questions are canonically defined in SKILL.md §4 — apply them to every architecture recommendation. Mode-specific notes for answering them here:

- Answer 2 (evidence) is usually an already-cited structure symptom: the coupling that blocks a test, the config friction that produced duplicated run scripts, the two consumers that already disagree about a dict key. Abstract hypothetical pain earns an observation, not a finding.
- Answer 5 (simpler alternative) deserves real effort in this mode: the cheap fixes — rename, extract function, delete indirection, parameterize the one value that changes — are frequently the right answer and are chronically under-recommended.
- Answer 6's trigger should be observable ("when a second pipeline consumer appears"), not vague ("when it grows").

## 4. Anti-patterns in recommendations

Do not propose, absent direct evidence:

- Repositories/services/interfaces/classes where plain functions are working; frameworks (MLflow, Airflow, feature stores) for a single-consumer pipeline.
- Migration to a new architecture just because it is standard.
- Microservice splits, plugin systems, DI containers in small codebases.
- "Add type hints everywhere" / blanket refactors with no named risk.
- CI/CD/registry pipelines for personal prototypes.

Do propose readily when evidence exists:

- **Deletion or inlining** of unused indirection — the cheapest improvement class.
- Making an implicit contract explicit exactly where it already broke or nearly broke.
- Parameterizing exactly the value that changes per run (one argparse flag beats a config framework).
- A regression test pinning behavior you found ambiguous while reading.

## 5. Handoff shape

The audit #1 handoff lists, per actionable finding: touch-point files/symbols; invariants observed (e.g., "`train.py` assumes `features` is already NaN-handled — see build.py:80"); suggested modification order (lowest blast radius first); dependent modules verified by checking importers/callers (list them, or mark `inferred`); test command per area; risks; and decisions reserved for the user (anything changing public interfaces, data formats, or run cost). End with: "Before coding, re-read the listed files — this handoff is a map of where to look, not the territory."
