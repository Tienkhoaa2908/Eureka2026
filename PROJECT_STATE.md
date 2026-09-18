# PROJECT STATE — Eureka 2026

Last updated: 2026-09-18 (UTC+7)
Status: bootstrap + scientific audit in progress

## 1. Research objective

Study whether and how the 10 PCI sub-indices are associated with subsequent enterprise outcomes at the province-year level in Vietnam, and test whether nonlinear machine-learning models add out-of-sample predictive value beyond interpretable panel-econometric baselines.

Until a defensible identification strategy is established, use the words association, relationship, predictive signal, or out-of-sample prediction. Do not claim causal impact.

## 2. Data currently available

- Panel PCI + enterprise net revenue: 63 provinces/cities × 2010–2024 = 945 province-year rows.
- Panel of 10 PCI sub-indices: 945 rows. Sub-index 6 (fair competition/policy bias) is structurally unavailable in 2010–2012; full 10-subindex sample begins in 2013.
- Existing panel includes PCI_lag1 and annual enterprise-revenue growth.
- Revenue figures were manually transcribed from GSO/NSO tables/screenshots in the current working materials; this remains the largest reproducibility risk.

## 3. Verified audit findings

- The EDA notebook contains invalid Python in multiple code cells because Vietnamese separator headings are not commented; the standalone .py version does not have this syntax defect.
- Current scripts use environment-specific absolute paths such as /mnt/user-data/uploads and /mnt/user-data/outputs; they are not reproducible after cloning.
- Current EDA computes pooled Pearson correlations and VIF. These are useful diagnostics but do not isolate within-province relationships or establish causality.
- Full 10-subindex VIF values are all below 5 in the current 2013–2024 panel; multicollinearity is therefore not the main immediate blocker, although high pairwise correlations still require interpretation.
- Three published subtotal-vs-province-sum discrepancies are recorded in the existing panel notebook. They must be rechecked against the original GSO/NSO PDFs before being treated as source anomalies.

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

1. Outcome validity: nominal aggregate provincial revenue is heavily driven by province size, inflation, sector mix, and number of firms.
2. Identification: aggregate PCI and aggregate revenue may co-move with omitted province-level economic conditions.
3. Data lineage: revenue transcription is not yet independently reproducible from source tables.
4. Structural missingness: sub-index 6 before 2013 must not be imputed as if it were observed.
5. Methodology drift: PCI indicator composition/weights and administrative definitions may change over time; changes must be documented.
6. Leakage: any random train/test split across province-years will contaminate temporal evaluation.

## 6. Highest-priority next work

See docs/research/NEXT_EXPERIMENT.md. The next gate is DATA-INTEGRITY-01: independently verify the three disputed GSO/NSO cells/subtotals and generate a machine-readable data lineage table. No final model ranking should be accepted before this gate passes.

## 7. Submission state

Euréka 2026 online registration closes 2026-09-25. Submission formatting and anonymization requirements are summarized in docs/competition/EUREKA_2026.md.

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
