# PROGRESS

## 2026-09-18

Completed:
- Recovered and audited the uploaded project bundle and project description.
- Reframed the research question from unsupported causal ranking to panel inference + out-of-sample prediction.
- Reviewed official Euréka 2026 requirements and recent competition/literature context.
- Bootstrapped GitHub research-OS structure.
- Completed **G1 DATA-INTEGRITY-01**:
  - documented revenue source blocks;
  - corrected three source-backed transcription errors;
  - added machine-readable lineage/correction registries.
- Completed **G2 REPRO-PIPELINE-01**:
  - built one-command repository-relative canonical pipeline;
  - generated stable 945-row output;
  - added explicit province/merge/missingness tests.
- Completed **G3 STAT-BASELINE-01**:
  - implemented two-way FE with province-clustered cluster-t inference;
  - standardized all 10 lagged PCI components reproducibly;
  - added BH FDR multiplicity adjustment;
  - generated full and no-2020/2021 outcome specifications;
  - generated leave-one-province-out sensitivity;
  - found no multiplicity-adjusted component in the log-level outcome;
  - found CSTP5 as the only BH-adjusted association in the log-change outcome, stable in the recorded COVID and province-omission sensitivities;
  - expanded local suite to 15 passing tests before PR.

In progress:
- G4 time-respecting predictive benchmark.
- Literature matrix / integrated manuscript narrative.

Blocked:
- Feature-importance interpretation is blocked until a PCI-added model demonstrates out-of-sample incremental value under G4.
- Causal language remains blocked.

Current next action:
Execute `docs/research/NEXT_EXPERIMENT.md` (PRED-BENCHMARK-01).
