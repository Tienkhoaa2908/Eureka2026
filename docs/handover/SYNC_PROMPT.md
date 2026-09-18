# SYNC / HANDOVER PROMPT

Copy the prompt below at the end of a substantial work session.

---

Synchronize everything materially completed in this conversation to GitHub repo `Tienkhoaa2908/Eureka2026` so that a future chat can resume from the repository alone.

Required workflow:

1. Inspect the current default branch, active work branch, open PRs/issues, CI, and latest commits before writing.
2. Identify every new fact, decision, experiment, data-quality finding, code change, result artifact, blocker, and next step from this session.
3. Update `PROJECT_STATE.md` first. It must reflect only the current truth, not a diary.
4. Append durable methodological decisions to `DECISIONS.md`; append experiments (including negative/null results) to `EXPERIMENTS.md`; append dated work to `PROGRESS.md`; summarize repository changes in `CHANGELOG.md`.
5. Update `docs/research/NEXT_EXPERIMENT.md` so it contains exactly one primary next gate/experiment with inputs, procedure, pass/fail criteria, expected artifacts, and what becomes unblocked if it passes.
6. Update any affected method, data-lineage, competition, or audit docs. Update code/tests and run the relevant validation.
7. Remove or archive stale documentation that now contradicts the canonical state. Prefer deletion when a file is purely duplicated/outdated; prefer `docs/archive/` only when preserving historical rationale is useful. Never delete raw evidence, source citations, decision history, or reproducibility artifacts without an explicit replacement.
8. Search the repo for contradictory statements, obsolete paths, duplicate current-state docs, TODOs already completed, and stale dates. Resolve them.
9. Never fabricate metrics. If a value was not reproduced in this session, mark it unverified or omit it.
10. Commit changes on a focused branch and open/update a PR. The PR body must state: what changed, why, validation run, unresolved risks, and exact next step.
11. Re-fetch critical files and inspect the final diff/CI. Do not report 'synced' until GitHub confirms the writes.

End with a compact handover containing: branch/PR, latest commit(s), current gate and status, unresolved blockers, and the one next action a new agent should execute.

---
