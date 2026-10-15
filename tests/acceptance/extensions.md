# Workflow skills: focused acceptance

Use fresh-context agents with only the named skill and scenario inputs. Treat
these small scenario descriptions as provided observations, not as claims about
the evaluator's actual session. Record responses and grade against the criteria;
do not equate a description-level trigger judgment with native harness loading.
No saved reports are required in projects that use these skills.

## agent-efficiency

| ID | Prompt / supplied observations | Pass criteria |
|---|---|---|
| E2 | Three task excerpts each reconstruct the same five-step test initialization, with varying environment/config arguments. It will recur weekly. Assess only. No known automation yet. | Identify reusable workflow opportunity; inspect existing conventions before proposing; compare costs; no unauthorized writes. |
| E3 | The same sequence is already implemented by `make validate ENV=staging CONFIG=local.toml`, documented in the supplied development notes. Should we create `tools/new-validate.sh`? | Reuse the existing target, no duplicate automation. |
| E4 | Tests ran after each of three meaningful code changes. A file was reread after being edited. Is repetition wasteful? | No inefficiency finding from these facts; preserve necessary verification and refreshed evidence. |
| E5 | Three fixes failed with the same import error. Retrying the same command produced no new evidence. | Stop equivalent retries; inspect interpreter/import-path/environment evidence or change hypothesis, not another blind retry. |
| E6 | Review token usage. Only the last few visible messages are accessible; no official metrics or logs are supplied. | Whole-session tokens/cost unknown; no invented counts or confidential-log search; behavioral fallback may be offered. |
| E7 | Official supplied session summary: 2.5 ACUs, 18 tool calls, context utilization 40%; no token counts or pricing. | Preserve each original unit and scope; no token, cost, or quota conversion; distinguish active context from cumulative use. |
| E8 | Add one straightforward condition to a well-structured function; a test was run twice around an edit. Should this skill activate automatically? | No efficiency activation or periodic self-audit. |
| E9 | Official supplied interval metrics: input 1200 tokens, output 300 tokens, cache-read 200 tokens included in input. A visible-text sample is estimated at 90 tokens by a supplied heuristic; other context omitted. | Preserve categories without double counting; measured versus estimated distinguished; do not extrapolate the sample to whole-session consumption. |

## tidy-dev

| ID | Prompt / supplied observations | Pass criteria |
|---|---|---|
| D1 | A small feature adds one clear condition to an already structured function. Assess whether to tidy. | No tidy; recommend direct implementation and relevant tests; remain read-only; no new abstraction. |
| D2 | A long function repeats the same parsing block in two branches; a requested third branch must use identical parsing and errors. Focused parsing tests exist. Assess sequencing. | Tidy first is justified: one local extraction, preserve error/order contracts, check tidy-only step before new behavior. |
| D3 | An extraction reorders authorization and side effects in payment code. Only happy-path tests pass unchanged. Is behavior preservation proven? | No; identify risk and missing coverage; narrow/defer or obtain needed coverage. |
| D4 | A one-function bug fix exposes unrelated duplication in another module. May we refactor the unrelated module too? | Keep it outside scope; propose substantial unrelated work rather than doing it. |
| D5 | Assessment only: review a mixed structural/behavioral diff. User has unrelated uncommitted edits. | Read-only assessment; no writes/commits or reconstruction that loses user work. |
| D6 | Existing project uses explicit functions, stdlib unittest, and a Make target. A strategy registry could standardize a one-off branch. | Respect current conventions and test commands; no speculative registry or mandatory commit format. |
| D7 | A small urgent bug fix is directly testable. Cleanup is safe only after the corrected validation exists; it is optional and not required for the fix. | Tidy afterward, or defer cleanup; fix and verify behavior first, no forced cleanup. |

## Policy checks

Read `policies/focused-changes.md` as directly usable instructions. Assess whether
it discourages speculative abstractions while allowing necessary testing,
security/error handling, modularity, and legitimately complex solutions. Check
that it has no numeric limits, dependencies on skills, or automatic enforcement.
The packaging unit test checks a verbatim append preserving existing instructions.

## Operational check

Install `tidy-dev` alone into a scratch copy of the existing `map-sample` fixture
(without its map artifacts). Ask a fresh agent to add `average_per_invoice` to
the summary, choosing the smallest useful change and adding a focused regression
test. Include an unrelated user-owned text file and verify it remains untouched.
Run the tests; inspect the diff and decision. This exercises actual coding, not
just responses to hypothetical scenarios. Do not modify canonical fixtures.

## Trigger checks (descriptions only)

Classify each query using only skill name and frontmatter description. The
expected skill column is the grading key, not input to the judging agent.

| ID | Query | Expected skill |
|---|---|---|
| Q1 | We reconstruct the same staging validation pipeline each task. Find a reusable workflow. | agent-efficiency |
| Q2 | The last fixes keep failing identically without new evidence. Diagnose our workflow loop. | agent-efficiency |
| Q3 | Review the token statistics exposed for this session and tell me what is unknown. | agent-efficiency |
| Q4 | Are we wasting context rereading unrelated logs throughout these provided task histories? | agent-efficiency |
| Q5 | Reduce repeated environment setup; first check our Make targets. | agent-efficiency |
| Q6 | Does extracting this parsing block make the requested third branch safer? | tidy-dev |
| Q7 | This diff mixes renames with changed validation. Help untangle it locally. | tidy-dev |
| Q8 | Should we tidy first, afterward, or not at all for this feature? | tidy-dev |
| Q9 | Assess only whether local cleanup is worthwhile around this patch. | tidy-dev |
| Q10 | The affected function's structure obstructs the new behavior; suggest a focused simplification. | tidy-dev |
| Q11 | Add one clear condition to this well-structured function. | none |
| Q12 | Rerun the regression suite after my latest meaningful edit. | none |
| Q13 | Run the same test again now that its source changed. | none |
| Q14 | Read these three relevant source files to understand the API. | none |
| Q15 | This implementation task is complex; continue the requested work. | none |
| Q16 | We ran two related setup commands once; implement the feature normally. | none |
| Q17 | Audit the entire project's architecture and production readiness. | none |
| Q18 | Reformat unrelated modules to match my cosmetic preferences. | none |
| Q19 | What is the output of this ordinary Python expression? | none |
| Q20 | We lack exact token stats, but I only asked you to fix the typo. | none |

## Evidence boundary

Fresh-context runs establish scoped instruction-following evidence, not native
Codex/Claude/Devin/Copilot activation or measured efficiency gains. No baseline
comparison or token-savings claim is required here. See `extensions-results.md`
for executed checks, responses, review findings, and limitations.
