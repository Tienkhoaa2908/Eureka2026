# PROJECT STATE — Eureka 2026

Last updated: 2026-09-18 (UTC+7)
Status: **G1 data integrity passed; G2 reproducible pipeline is current gate**

## 1. Research objective

Study whether and how the 10 PCI sub-indices are associated with subsequent enterprise outcomes at the province-year level in Vietnam, and test whether nonlinear machine-learning models add out-of-sample predictive value beyond interpretable panel-econometric baselines.

Until a defensible identification strategy is established, use the words association, relationship, predictive signal, or out-of-sample prediction. Do not claim causal impact.

## 2. Data currently available

- Panel PCI + enterprise net revenue: 63 provinces/cities × 2010–2024 = 945 province-year rows.
- Panel of 10 PCI sub-indices: 945 rows. Sub-index 6 (fair competition/policy bias) is structurally unavailable in 2010–2012; full 10-subindex sample begins in 2013.
- Existing panel includes PCI_lag1 and annual enterprise-revenue growth.
- Revenue source blocks are now documented in `data/metadata/data_lineage.csv`.
- Three verified revenue transcription errors are encoded in `data/metadata/revenue_corrections.csv` and `src/eureka2026/revenue_corrections.py`.

Verified revenue corrections:
- Hòa Bình 2016: 23,040 → **33,040**.
- Gia Lai 2023: 133,195 → **131,195**.
- An Giang 2023: 212,941 → **212,961**.

Annual revenue growth must be regenerated after applying these corrections.

## 3. Verified audit findings

- DATA-INTEGRITY-01 passed. The three previously large regional-subtotal mismatches were caused by transcription errors in the derived province panel, not by large unexplained NSO source anomalies.
- After those three corrections, all 90 region-year subtotal checks are within an absolute residual of 3; regional subtotals are used only as QA, not as model observations.
- The 2020–2024 archived Table 151 extract is fingerprinted and traceable to the official NSO indicator/PX-Web series, but its exact originating publication/page was not retained in the source bundle. This remains a documented lineage caveat, not a silent assumption.
- The EDA notebook contains invalid Python in multiple code cells because Vietnamese separator headings are not commented; the standalone .py version does not have this syntax defect.
- Current legacy scripts use environment-specific absolute paths such as /mnt/user-data/uploads and /mnt/user-data/outputs; they are not reproducible after cloning.
- Current EDA computes pooled Pearson correlations and VIF. These are useful diagnostics but do not isolate within-province relationships or establish causality.
- Full 10-subindex VIF values are all below 5 in the current 2013–2024 panel; multicollinearity is not the main immediate blocker, although correlated-feature interpretation still matters.

## 4. Current scientific design

Primary inferential specification:
- sample: 2014–2024 when using one-year-lagged values for all 10 sub-indices;
- outcome: log enterprise net revenue, plus log revenue growth as a robustness outcome;
- predictors: standardized one-year-lagged PCI sub-indices;
- province fixed effects + year fixed effects;
- standard errors clustered by province;
- report effect size and uncertainty, not only p-values.

Prediction track:
- Elastic Net, Random Forest, and XGBoost;
- expanding/rolling time splits only; random row split is prohibited;
- compare against simple baselines: lagged outcome, year/province effects, and linear/Elastic Net;
- evaluate MAE/RMSE on log scale and optionally MAPE/SMAPE where numerically stable;
- use permutation importance or SHAP only after confirming out-of-sample performance.

## 5. Primary unresolved risks

1. **Reproducibility:** legacy analysis still depends on absolute sandbox paths and manually assembled files; G2 must create one deterministic raw → clean → model build.
2. Outcome validity: nominal aggregate provincial revenue is heavily driven by province size, inflation, sector mix, and number of firms.
3. Identification: aggregate PCI and aggregate revenue may co-move with omitted province-level economic conditions.
4. Structural missingness: sub-index 6 before 2013 must not be imputed as if observed.
5. Methodology drift: PCI indicator composition/weights and administrative definitions may change over time; changes must be documented.
6. Leakage: any random train/test split across province-years will contaminate temporal evaluation.
7. Lineage caveat: exact publication/page for the archived 2020–2024 Table 151 extract remains to be recovered if available.

## 6. Highest-priority next work

See `docs/research/NEXT_EXPERIMENT.md`.

Current gate: **G2 — REPRO-PIPELINE-01**.

Build a deterministic repository-relative pipeline that applies the three source-backed revenue corrections, preserves CSTP6 structural missingness, regenerates growth/lagged fields, validates the 63×15 panel, and emits a canonical processed analysis dataset with checksum.

Do not run final FE or tune XGBoost until G2 passes.

## 7. Submission state

Euréka 2026 online registration closes 2026-09-25. Submission formatting and anonymization requirements are summarized in `docs/competition/EUREKA_2026.md`.

## 8. Recovery protocol

On a new chat or agent session, read files in this order:
1. PROJECT_STATE.md
2. docs/handover/RECOVERY_PROMPT.md
3. docs/research/RESEARCH_OPERATING_MODEL.md
4. docs/research/QUALITY_GATES.md
5. DECISIONS.md
6. EXPERIMENTS.md
7. PROGRESS.md
8. CHANGELOG.md
9. docs/research/NEXT_EXPERIMENT.md
10. the current gate's audit note/artifacts and relevant source/tests.
