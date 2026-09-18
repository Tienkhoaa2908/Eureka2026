# QUALITY GATES

No downstream result is considered final while an upstream gate is failed.

## G0 — Competition compliance
Pass when official 2026 deadline, field, report structure, anonymization, and formatting requirements are captured and submission checklist exists.
Current: PASS (documentation), final file compliance still pending.

## G1 — Data integrity
Pass when:
- 945 province-year panel keys are unique and complete for 2010–2024;
- 10-subindex panel has expected structural missingness only;
- province naming is canonical and merge coverage is 100%;
- revenue source lineage is documented;
- known subtotal discrepancies are independently rechecked;
- no silent imputation of structurally unavailable CSTP6.

Current: **PASS (2026-09-18).**

Evidence:
- `artifacts/qa/DATA-INTEGRITY-01.md`
- `data/metadata/data_lineage.csv`
- `data/metadata/revenue_corrections.csv`
- `src/eureka2026/revenue_corrections.py`

Caveat: exact originating publication/page for the archived 2020–2024 Table 151 extract is not retained; screenshot hashes and the official NSO series provide a reproducible evidence trail.

## G2 — Reproducible pipeline
Pass when:
- no absolute sandbox/user paths in active source;
- environment dependencies are declared;
- identified source/migration inputs can regenerate the canonical model dataset;
- verified revenue corrections are applied by code;
- derived growth/lag variables are regenerated after corrections;
- province normalization and one-to-one merge checks are explicit;
- invariant tests pass;
- canonical processed dataset checksum is recorded and stable across repeat builds.

Current: **PASS (2026-09-18).**

Evidence:
- `src/eureka2026/pipeline.py`
- `src/eureka2026/xlsx_reader.py`
- `src/eureka2026/province_names.py`
- `tests/test_pipeline.py`
- `tests/test_no_legacy_paths.py`
- `data/metadata/canonical_build_manifest.json`
- `artifacts/qa/REPRO-PIPELINE-01.md`

Canonical output SHA-256:
`a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`

## G3 — Statistical baseline
Pass when:
- outcome definition is prespecified;
- 2014–2024 lagged 10-CSTP sample is exactly 693 rows;
- province FE + year FE model is reproduced from the canonical panel;
- standard errors are clustered by province;
- standardized predictor scaling is reproducible;
- coefficient table includes confidence intervals and multiplicity-aware interpretation;
- residual/influence and COVID-period sensitivity checks are documented;
- interpretation avoids causal overclaim.

Current: **OPEN / current gate.**

## G4 — Predictive benchmark
Pass when:
- time-respecting folds are fixed in advance;
- naive and linear baselines are evaluated;
- RF/XGBoost/Elastic Net are compared on identical folds;
- hyperparameter tuning is nested or confined to training periods;
- feature importance stability is checked.
Current: NOT STARTED.

## G5 — Robustness
Pass when core conclusions are compared across:
- log revenue vs log growth;
- nominal vs deflated/scale-normalized outcome if available;
- contemporaneous vs lagged PCI;
- excluding/isolating COVID years;
- alternative periods, including 2010–2024 without CSTP6;
- influential province checks.
Current: NOT STARTED.

## G6 — Scientific contribution
Pass when the paper clearly states:
- what recent Vietnam literature already establishes;
- what this project adds;
- why the addition is nontrivial;
- what claims are and are not supported by the design.
Current: PARTIAL.

## G7 — Euréka submission
Pass when the anonymous manuscript, poster, citations, figures/tables, and registration package meet the official rules and every reported number maps to a reproducible artifact.
Current: OPEN.
