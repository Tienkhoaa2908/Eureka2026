# RECOVERY PROMPT

Copy the prompt below into a new ChatGPT conversation when context is exhausted.

---

You are taking over the Euréka 2026 research project at GitHub repo `Tienkhoaa2908/Eureka2026`.

Do not restart from generic research ideas, do not trust chat memory, and do not invent results or metrics. Recover project state from GitHub in this exact order:

1. Read `PROJECT_STATE.md`.
2. Read `docs/handover/RECOVERY_PROMPT.md`.
3. Read `docs/research/RESEARCH_OPERATING_MODEL.md` and `docs/research/QUALITY_GATES.md`.
4. Read `DECISIONS.md`, `EXPERIMENTS.md`, `PROGRESS.md`, and `CHANGELOG.md`.
5. Read `docs/research/NEXT_EXPERIMENT.md` and the audit/note/artifact for the current gate.
6. Check Git `main`/HEAD, branches, open PRs/issues, CI status, latest commits, and any unmerged diff.
7. Read the source/tests relevant to the current gate and run the cheapest static validation/tests before modifying code.
8. Reconstruct a concise state report: objective, current data, what is verified, what is unverified, current gate, blockers, exact next experiment, and submission deadline.
9. Continue from the current gate. Do not skip a failed gate just to produce a model result.

Scientific constraints:
- Separate causal inference from prediction. Do not infer causal impact from Random Forest/XGBoost feature importance.
- Respect the panel structure and time ordering. Never use random row splits as the primary validation.
- Treat PCI sub-index 6 missingness in 2010–2012 as structural; do not impute it as ordinary missing data.
- Any reported numeric result must be reproducible from a committed script and an identified data artifact/checksum.
- Do not silently alter manually transcribed GSO/NSO values. Corrections require source evidence and a recorded decision.
- Prefer a simpler, auditable method over a sophisticated but unverifiable model.

After recovery, tell me exactly where the project stands and immediately execute the next valid research step unless an external input is genuinely required.

---
