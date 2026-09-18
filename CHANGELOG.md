# CHANGELOG

## 2026-09-18

### Added
- Research operating model, quality gates, handover prompts.
- Competition/literature/audit documentation.
- Revenue lineage and correction registry.
- Deterministic canonical panel builder and tests.
- `src/eureka2026/fe_baseline.py`.
- FE utility tests for standardization and BH correction.
- NumPy/statsmodels dependency contract.
- G3 coefficient, influence, scaling, metadata, and QA artifacts.

### Changed
- Research framing separates association/inference from prediction.
- G1 Data integrity: PASS.
- G2 Reproducible pipeline: PASS.
- G3 Statistical baseline: PASS.
- Current gate advanced to G4 PRED-BENCHMARK-01.
- CI now installs declared statistical dependencies before compile/unit tests.

### G3 recorded finding
- No lagged PCI component survives BH FDR in the log-revenue-level FE model.
- CSTP5 is the only BH-adjusted association in the log-revenue-change FE model and remains positive/BH-adjusted after excluding 2020–2021 outcome years.
- The result is explicitly associational and is not labeled causal or “most impactful”.

### Known limitations / open work
- Aggregate nominal revenue has inflation/scale/sector-composition limitations.
- Two-way FE does not eliminate time-varying confounding or reverse causality.
- A stricter COVID-window robustness design remains for G5.
- Spatial dependence remains untested.
- Exact publication/page for the archived 2020–2024 Table 151 extract remains a documented lineage caveat.


### Added — G4/G5/G6 deep validation
- `src/eureka2026/predictive_benchmark.py` and temporal leakage tests.
- `src/eureka2026/robustness.py` and robustness utility tests.
- scikit-learn, XGBoost and SciPy dependency contract.
- fold-level predictive metrics, nested tuning audit, PCI-increment comparison, prediction fingerprints and metadata.
- robustness coefficient, CSTP5 targeted, year-LOO, region-LOO and metadata artifacts.
- `artifacts/qa/PRED-BENCHMARK-01.md`.
- `artifacts/qa/ROBUSTNESS-01.md`.
- `docs/research/LITERATURE_MATRIX.md`.
- `docs/research/INTEGRATED_RESULTS_AND_CONTRIBUTION.md`.
- `docs/submission/MANUSCRIPT_DRAFT.md`.
- `docs/submission/NUMBER_TO_ARTIFACT_MAP.md`.
- `docs/submission/ANONYMITY_CHECKLIST.md`.
- `docs/submission/SUBMISSION_PLAN.md`.

### Changed — evidence state
- G4 Predictive benchmark: PASS with negative incremental-PCI conclusion.
- G5 Robustness: PASS with outcome-data caveat.
- G6 Scientific contribution: PASS.
- Current gate advanced to G7 submission package.
- Working manuscript no longer frames CSTP5 as a universal “most impactful” component.
- XGBoost/Random Forest are retained as benchmark models, not as the source of the paper’s novelty.

### G4/G5 recorded finding
- non-PCI Elastic Net is best on mean MAE for both outcomes;
- no PCI-added model passes the feature-importance gate;
- CSTP5 primary FE signal survives some robustness checks but weakens or disappears in strict-period/alternative-period specifications;
- final interpretation is bounded association + negative predictive increment, not causal ranking.
