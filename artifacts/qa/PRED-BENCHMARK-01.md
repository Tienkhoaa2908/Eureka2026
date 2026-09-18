# PRED-BENCHMARK-01 — time-respecting predictive benchmark

Date: 2026-09-18  
Gate: G4 Predictive benchmark  
Verdict: **PASS — negative incremental-PCI result**

## Question

Do one-year-lagged PCI sub-indices add genuine future-year predictive value for provincial enterprise-revenue outcomes beyond strong non-PCI baselines, and do nonlinear models improve over a regularized linear predictor?

This is a forecasting/generalization test, not a causal-effect estimator.

## Canonical input

- `data/processed/panel.csv`
- SHA-256: `a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`
- predictive panel: 693 province-year rows, 63 provinces, 2014–2024.

## Leakage control

Fixed outer expanding windows:

1. train 2014–2018 → test 2019;
2. train 2014–2019 → test 2020;
3. train 2014–2020 → test 2021;
4. train 2014–2021 → test 2022;
5. train 2014–2022 → test 2023;
6. train 2014–2023 → test 2024.

Each test year contains all 63 provinces. No random row split is used.

For target year t, features use information available no later than t-1:
- lagged log revenue;
- lagged log-revenue change;
- province identity;
- deterministic time trend;
- PCI-added variants additionally use cstp1_lag1 … cstp10_lag1.

Preprocessing and hyperparameter tuning are fitted inside outer training data only. Inner tuning also uses expanding temporal folds. Seed: `20260918`.

## Models

- naive persistence / zero-change baseline;
- Elastic Net without PCI;
- Elastic Net with PCI;
- Random Forest without PCI;
- Random Forest with PCI;
- XGBoost without PCI;
- XGBoost with PCI.

Primary metric: MAE. Secondary: RMSE.

## Primary outcome — log revenue change

| Model | PCI | Mean MAE | vs naive | folds beating naive |
|---|---:|---:|---:|---:|
| Elastic Net | no | **0.08819** | **+23.21%** | 4/6 |
| Elastic Net | yes | 0.08890 | +22.59% | 4/6 |
| Random Forest | no | 0.10365 | +9.74% | 4/6 |
| Random Forest | yes | 0.09523 | +17.07% | 4/6 |
| XGBoost | no | 0.10172 | +11.43% | 4/6 |
| XGBoost | yes | 0.10321 | +10.13% | 4/6 |
| Naive | no | 0.11484 | 0% | — |

The best mean out-of-sample MAE is the **non-PCI Elastic Net**.

Adding PCI:
- Elastic Net: mean MAE worsens by ~0.80%; beats same-family non-PCI in 1/6 folds.
- Random Forest: improves same-family MAE by ~8.12% and wins 5/6 versus RF without PCI, but remains ~7.98% worse than the stronger non-PCI Elastic Net and beats that benchmark in only 1/6 folds.
- XGBoost: mean MAE worsens by ~1.46%.

## Secondary outcome — log revenue level

| Model | PCI | Mean MAE | vs naive |
|---|---:|---:|---:|
| Elastic Net | no | **0.08859** | **+22.86%** |
| Elastic Net | yes | 0.09045 | +21.24% |
| XGBoost | no | 0.11277 | +1.80% |
| Naive | no | 0.11484 | 0% |
| Random Forest | no | 0.11819 | -2.92% |
| XGBoost | yes | 0.12873 | -12.10% |
| Random Forest | yes | 0.13247 | -15.35% |

Again, non-PCI Elastic Net is best on mean MAE. Adding PCI worsens all three model families for the level outcome.

## Temporal instability

For log revenue change the best model changes by test year:
- 2019: PCI Elastic Net, MAE 0.07285;
- 2020: naive zero-change, 0.06889;
- 2021: non-PCI Elastic Net, 0.08976;
- 2022: non-PCI Elastic Net, 0.09644;
- 2023: naive zero-change, 0.06284;
- 2024: non-PCI Elastic Net, 0.05760 (PCI Elastic Net is effectively tied at recorded precision).

This variation is evidence of regime sensitivity; one pooled average is not a universal ranking.

## Feature-importance gate

Permutation importance/SHAP was preregistered to require a PCI-added model to:
1. beat the non-PCI Elastic Net on mean outer-fold MAE; and
2. beat it in at least 4/6 outer folds.

No PCI-added model passes. Therefore **no PCI feature-importance ranking is generated**.

## Interpretation

G4 produces a defensible negative result: **lagged PCI components do not add stable future-year predictive value beyond a strong non-PCI regularized baseline in this panel.** Nonlinear tree models also do not dominate Elastic Net.

This does not contradict G3. A conditional FE association and incremental future-year forecast value answer different questions.

## Reproducibility

Code: `src/eureka2026/predictive_benchmark.py`

Run:
```bash
python -m src.eureka2026.predictive_benchmark
```

Recorded runtime:
- NumPy 2.3.5
- scikit-learn 1.8.0
- XGBoost 3.1.3

Evidence:
- `artifacts/results/PRED-BENCHMARK-01_metrics.csv`
- `artifacts/results/PRED-BENCHMARK-01_aggregate.csv`
- `artifacts/results/PRED-BENCHMARK-01_pci_increment.csv`
- `artifacts/results/PRED-BENCHMARK-01_tuning.csv`
- `artifacts/results/PRED-BENCHMARK-01_prediction_fingerprints.csv`
- `artifacts/results/PRED-BENCHMARK-01_metadata.json`

Full local prediction artifact SHA-256:
`65714d57fee901ca522fe2b7ea20164c9c1a7f982e212e6bc8a25e21a2922213`.

## Gate decision

G4 **passes**. Passing means the forecasting claim was tested with fixed temporal folds and leakage control; it does not mean ML or PCI improved forecasts.
