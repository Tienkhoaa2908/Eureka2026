# RESEARCH OPERATING MODEL

## Goal
Operate the project like an auditable research system, not a one-off notebook.

## Canonical lifecycle

Question → literature gap → data lineage → integrity checks → prespecified baseline → robustness → prediction benchmark → interpretation → application/policy translation → submission artifacts.

## Evidence hierarchy

1. Original official source/data and exact methodological documentation.
2. Reproducible project-generated artifacts from committed code.
3. Peer-reviewed literature or institutional working papers.
4. Secondary summaries only for orientation, never as sole support for a key empirical claim.

## Research separation

### Inference track
- Objective: estimate conditional associations under explicit assumptions.
- Minimum: province FE + year FE; cluster SE by province.
- Prefer lagged institutional variables.
- Discuss endogeneity, reverse causality, measurement error, and omitted variables.
- Causal language requires a stronger identification design than FE alone.

### Prediction track
- Objective: predict future province-year outcomes.
- Evaluation: expanding/rolling temporal validation.
- Models: naive/linear baseline → Elastic Net → RF/XGBoost if they add stable value.
- Feature importance is descriptive of a fitted predictor, not an effect size.

## Reproducibility standard

Every table/figure/result intended for the report must have:
- input data path + provenance;
- script/notebook path;
- deterministic seed where applicable;
- output artifact path;
- validation status;
- date and commit SHA recorded in the experiment log.

## Documentation policy

`PROJECT_STATE.md` = current truth.
`DECISIONS.md` = durable methodological choices.
`EXPERIMENTS.md` = experiment registry.
`PROGRESS.md` = dated diary.
`CHANGELOG.md` = repo evolution.
`docs/research/NEXT_EXPERIMENT.md` = exactly one primary next step.

Duplicated 'current status' files are prohibited because they drift.
