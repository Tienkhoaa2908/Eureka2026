# QUALITY GATES

No downstream result is considered final while an upstream gate is failed.

## G0 — Competition compliance
Current: **PASS for documented requirements; final-file compliance belongs to G7.**

## G1 — Data integrity
Current: **PASS (2026-09-18).**

Evidence:
- `artifacts/qa/DATA-INTEGRITY-01.md`
- `data/metadata/data_lineage.csv`
- `data/metadata/revenue_corrections.csv`

## G2 — Reproducible pipeline
Current: **PASS (2026-09-18).**

Canonical SHA-256:
`a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`

Evidence:
- `src/eureka2026/pipeline.py`
- `data/metadata/canonical_build_manifest.json`
- `artifacts/qa/REPRO-PIPELINE-01.md`

## G3 — Statistical baseline
Current: **PASS (2026-09-18).**

Evidence:
- `src/eureka2026/fe_baseline.py`
- `artifacts/results/STAT-BASELINE-01_*.csv/json`
- `artifacts/qa/STAT-BASELINE-01.md`

Key result:
- no BH-adjusted signal in log-revenue level;
- CSTP5 is the only BH-adjusted component in primary log-change specification;
- interpretation is associational.

## G4 — Predictive benchmark
Pass requires:
- fixed temporal outer folds;
- no future information in preprocessing/tuning;
- naive, Elastic Net, RF and XGBoost on identical outer years;
- non-PCI and PCI-added comparisons;
- fold-level MAE/RMSE;
- nested training-only tuning;
- feature importance withheld unless incremental-value gate is passed.

Current: **PASS (2026-09-18) — negative incremental-PCI result.**

Evidence:
- `src/eureka2026/predictive_benchmark.py`
- `tests/test_predictive_benchmark.py`
- `artifacts/results/PRED-BENCHMARK-01_*.csv/json`
- `artifacts/qa/PRED-BENCHMARK-01.md`

Gate finding:
- non-PCI Elastic Net has lowest mean MAE for both outcomes;
- PCI does not add stable predictive value beyond that baseline;
- no feature-importance output is allowed/generated.

## G5 — Robustness
Pass requires boundary testing across period/specification/outliers/influence and residual dependence where warranted.

Current: **PASS (2026-09-18), with outcome-data caveat.**

Evidence:
- `src/eureka2026/robustness.py`
- `tests/test_robustness.py`
- `artifacts/results/ROBUSTNESS-01_*.csv/json`
- `artifacts/qa/ROBUSTNESS-01.md`

Gate finding:
- CSTP5 survives outlier and leave-one-year/region checks;
- result weakens under strict COVID exclusion and is null in contemporaneous/longer-period variants;
- future-lead placebo is null;
- no universal/causal ranking is supported.

Scale-normalized outcome robustness remains outside the current canonical data because verified per-firm/per-worker or province-deflator inputs are unavailable.

## G6 — Scientific contribution
Pass requires:
- recent Vietnam evidence accurately positioned;
- contribution stated without “nobody has studied this” claims;
- inference vs prediction distinction explicit;
- negative evidence retained;
- policy claims bounded.

Current: **PASS (2026-09-18).**

Evidence:
- `docs/research/LITERATURE_MATRIX.md`
- `docs/research/INTEGRATED_RESULTS_AND_CONTRIBUTION.md`
- `docs/submission/MANUSCRIPT_DRAFT.md`

## G7 — Euréka submission
Pass when:
- manuscript and poster are anonymous and format compliant;
- final figures/tables are generated from committed artifacts;
- references are checked;
- every number maps to an artifact;
- final narrative matches G1–G6 evidence.

Current: **OPEN / current gate.**

Evidence/checklists:
- `docs/submission/SUBMISSION_PLAN.md`
- `docs/submission/NUMBER_TO_ARTIFACT_MAP.md`
- `docs/submission/ANONYMITY_CHECKLIST.md`
