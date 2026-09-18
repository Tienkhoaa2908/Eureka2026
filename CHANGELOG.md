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
