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
- each revenue value has traceable official source/table/page or a reproducible extraction record;
- the three known subtotal discrepancies are independently rechecked;
- no silent imputation of structurally unavailable sub-index 6.

Current: **PASS (2026-09-18).**

Evidence:
- `artifacts/qa/DATA-INTEGRITY-01.md`
- `data/metadata/data_lineage.csv`
- `data/metadata/revenue_corrections.csv`
- `src/eureka2026/revenue_corrections.py`

Caveat: exact originating publication/page for the archived 2020–2024 Table 151 extract is not retained; screenshot hashes and the official NSO series provide a reproducible evidence trail, with 2020–2023 additionally cross-checked to the 2024 yearbook.

## G2 — Reproducible pipeline
Pass when:
- no absolute sandbox/user paths;
- environment dependencies are declared;
- raw → clean → model datasets can be regenerated;
- verified revenue corrections are applied by code;
- derived growth/lag variables are regenerated after corrections;
- notebook/script syntax checks pass;
- invariant tests pass;
- canonical processed dataset checksum is recorded.

Current: **OPEN / current gate.**

## G3 — Statistical baseline
Pass when:
- outcome definition is prespecified;
- two-way FE model is reproduced;
- clustered SE are used;
- residual/outlier/sensitivity checks are documented;
- interpretation avoids causal overclaim.
Current: NOT STARTED as final gate; only smoke-tested.

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
- alternative periods, including 2010–2024 without sub-index 6;
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
