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

Completed:
- Completed **G4 PRED-BENCHMARK-01**:
  - six fixed expanding test years 2019–2024;
  - nested temporal tuning and leakage tests;
  - Elastic Net, RF and XGBoost with/without PCI;
  - negative incremental-PCI result beyond the strongest non-PCI baseline;
  - feature-importance gate failed, so no ranking was produced.
- Completed **G5 ROBUSTNESS-01**:
  - strict pandemic exclusion;
  - contemporaneous and longer-period specifications;
  - winsorization;
  - distributed lag and future-lead placebo;
  - leave-one-year and leave-one-region checks;
  - residual dependence diagnostic.
- Completed **G6 scientific contribution synthesis**:
  - verified literature matrix;
  - integrated G3–G5 narrative;
  - full research-content manuscript draft;
  - number-to-artifact and anonymity checklists.

In progress:
- G7 final Euréka submission package: figures/tables, formatted anonymous manuscript, poster and final audits.

Blocked:
- Causal language remains blocked.
- Feature-importance ranking remains blocked by the negative G4 incremental-value gate.
- Scale-normalized outcome robustness requires new verified denominator/price data and is not required for the current canonical result.

Current next action:
Execute `docs/research/NEXT_EXPERIMENT.md` (SUBMISSION-PACKAGE-01).
