# NEXT EXPERIMENT — PRED-BENCHMARK-01

Priority: P0
Gate: G4 Predictive benchmark

## Question

Do one-year-lagged PCI sub-indices add genuine future-year predictive value for provincial enterprise revenue outcomes beyond strong non-PCI baselines, and do nonlinear models improve over regularized linear prediction?

This is a prediction question. It does not estimate causal effects.

## Canonical input

`data/processed/panel.csv`

Expected SHA-256:

`a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`

## Outcomes

Primary:
- one-year `log_revenue_change`.

Secondary:
- `log_revenue`.

Reason: the level target is highly persistent and can make complex models appear strong without demonstrating added PCI information. The change target directly tests whether lagged governance information helps predict movement beyond scale persistence.

## Outer temporal folds

Fix these six expanding-window folds before model fitting:

1. train 2014–2018 → test 2019;
2. train 2014–2019 → test 2020;
3. train 2014–2020 → test 2021;
4. train 2014–2021 → test 2022;
5. train 2014–2022 → test 2023;
6. train 2014–2023 → test 2024.

Each test fold contains the same 63 provinces. No random row split is permitted.

## Information set

For target year `t`, only variables observable by the end of `t-1` may enter features.

Non-PCI baseline features:
- lagged log revenue;
- lagged log-revenue change where available;
- province identity encoded inside the training pipeline;
- deterministic calendar/time-trend feature.

PCI-added feature set:
- all non-PCI baseline features;
- `cstp1_lag1 .. cstp10_lag1`.

Do not include contemporaneous year-t PCI values.

## Models

Mandatory:
1. naive baseline:
   - log revenue: prior-year log revenue;
   - log change: zero-change forecast.
2. Elastic Net on non-PCI baseline features.
3. Elastic Net with PCI-added features.
4. Random Forest with PCI-added features.
5. XGBoost with PCI-added features.

Optional only if time permits: RF/XGBoost non-PCI variants to isolate model-class versus PCI-feature gains more directly.

## Training/tuning rules

- preprocessing is fitted on training years only;
- categorical encoding/scaling is inside the training pipeline;
- hyperparameter tuning uses inner expanding temporal splits within each outer training window;
- no outer test year may affect preprocessing, tuning, early stopping, feature selection, or calibration;
- use a small prespecified grid to limit overfitting to a 63-province panel;
- set and record random seeds.

## Metrics

Primary metric:
- MAE.

Secondary:
- RMSE.

Report:
- metric by outer test year;
- mean and median across the six years;
- mean paired improvement relative to the appropriate naive and Elastic-Net non-PCI baselines;
- number of outer folds in which each model improves on the baseline.

Do not select a model solely from one aggregate average.

## Feature-importance gate

Permutation importance / SHAP may be generated only if a PCI-added model:
- has lower mean outer-fold MAE than the regularized non-PCI baseline; and
- improves MAE in at least 4 of 6 outer folds for that outcome.

If this condition fails, record the negative predictive result and do not manufacture an importance ranking.

## Pass criteria

G4 passes regardless of whether ML wins, provided:

- all six outer folds are reproduced exactly;
- no temporal leakage is detected;
- tuning is training-only;
- mandatory baselines/models run on identical outer folds;
- fold-level predictions and metrics are committed as compact audit artifacts;
- aggregate metrics are reproducible;
- any feature-importance output obeys the feature-importance gate;
- conclusions distinguish predictive performance from causal/inferential claims.

## Expected artifacts

- `src/eureka2026/predictive_benchmark.py`;
- tests for fold construction and leakage prevention;
- dependency update for scikit-learn / XGBoost;
- `artifacts/results/PRED-BENCHMARK-01_metrics.csv`;
- `artifacts/results/PRED-BENCHMARK-01_predictions.csv`;
- compact metadata/parameter artifact;
- `artifacts/qa/PRED-BENCHMARK-01.md`.

## Unlocks

G5 broader robustness work and final integrated result narrative.
