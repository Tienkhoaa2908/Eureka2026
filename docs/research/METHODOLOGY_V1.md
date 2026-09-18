# Methodology v1

Status: proposed; final model results are blocked by G1/G2 quality gates.

## 1. Unit of analysis
Province-year.

## 2. Outcomes

Primary inferential outcome:
`y_it = log(enterprise net revenue_it)`.

Primary change outcome:
`g_it = log(revenue_it) - log(revenue_i,t-1)`.

Robustness outcomes to add if data permit:
- real/deflated revenue;
- revenue per active enterprise;
- revenue per worker or related productivity proxy;
- winsorized growth to limit extreme denominator effects.

## 3. Exposures
Ten PCI sub-indices, standardized for comparability. Primary version uses one-year lags.

## 4. Baseline panel model

`y_it = alpha_i + lambda_t + beta' PCI_i,t-1 + gamma' X_i,t-1 + epsilon_it`

where `alpha_i` is province FE, `lambda_t` is year FE, and `X` contains justified time-varying controls when available.

Standard errors clustered by province. Report standardized coefficient, confidence interval, and substantive scale interpretation.

## 5. Prediction design

Candidate models:
- lagged-outcome naive baseline;
- regularized linear / Elastic Net;
- Random Forest;
- XGBoost.

Validation:
- expanding-window or rolling-origin splits by year;
- all preprocessing fitted on training data only;
- hyperparameter selection inside training periods;
- final comparison on future years not used for tuning.

Metrics:
- MAE and RMSE on log revenue;
- optional MAE on log-growth;
- calibration/scatter diagnostics;
- report fold-by-fold variation, not only one average.

## 6. Interpretation

For linear FE: coefficients are conditional within-province associations after year shocks and controls.
For ML: use permutation/SHAP importance only after predictive value is established; assess rank/sign stability across folds. Do not label importance as causal impact.

## 7. Robustness plan

- contemporaneous vs lagged components;
- 2013–2024 full 10-index vs 2010–2024 nine-index specification;
- exclude 2020–2021;
- region-specific or region×year sensitivity if power permits;
- influential-province leave-one-out or leverage checks;
- spatial dependence diagnostic if residual structure warrants it;
- alternative outcome scaling/deflation.

## 8. Multiplicity

Ten related components create multiple-testing risk. Report confidence intervals and, for confirmatory component tests, consider false-discovery-rate adjustment. Emphasize consistency across specifications over isolated p<0.05 findings.

## 9. Causal claim threshold

Two-way FE alone is not sufficient to claim causal impact. Causal language would require a credible quasi-experiment/instrument/event design plus explicit assumptions and diagnostics. Until then, manuscript title/abstract must use association/prediction language.
