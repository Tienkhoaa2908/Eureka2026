# STAT-BASELINE-01 — two-way fixed-effects baseline

Date: 2026-09-18  
Gate: G3 Statistical baseline  
Verdict: **PASS**

## Canonical input

`data/processed/panel.csv`

SHA-256:

`a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`

Primary sample: 2014–2024, 693 province-year observations, 63 province clusters, complete one-year-lagged values for all 10 PCI sub-indices.

## Prespecified model

For each outcome:

`y_it = province_FE_i + year_FE_t + beta' Z(PCI_components_i,t-1) + epsilon_it`

Implementation details:

- all 10 lagged PCI component scores are standardized using the analysis-sample mean and sample standard deviation (ddof=1);
- province fixed effects and year fixed effects are included;
- covariance is clustered by province;
- small-sample correction and t inference with cluster degrees-of-freedom correction are used;
- 95% confidence intervals use the cluster-t inference;
- Benjamini–Hochberg FDR q-values are computed across the 10 PCI-component tests within each specification/outcome;
- full sample design matrix has rank 83/83 and condition number 136.89;
- no-COVID design matrix has rank 81/81 and condition number 138.96.

Outcomes:

1. `log_revenue = ln(Doanh_thu_ty_dong)`.
2. `log_revenue_change = log(revenue_t) - log(revenue_t-1)`.

The models estimate conditional within-province associations after common year shocks. They do **not** identify causal effects.

## Full-sample results

### Log revenue level

No PCI component has BH-adjusted `q < 0.05`.

The three smallest raw p-values are:

| Component | Standardized beta | Cluster p | BH q | 95% CI |
|---|---:|---:|---:|---:|
| CSTP3 — Tính minh bạch | -0.02091 | 0.08579 | 0.35146 | [-0.04485, 0.00303] |
| CSTP6 — Cạnh tranh bình đẳng | 0.02839 | 0.09901 | 0.35146 | [-0.00550, 0.06228] |
| CSTP8 — Dịch vụ hỗ trợ doanh nghiệp | 0.01983 | 0.10544 | 0.35146 | [-0.00430, 0.04395] |

The model R² is 0.9894, but this high value largely reflects province/year fixed effects and persistent level differences. It must not be interpreted as evidence that PCI components explain 98.9% of business performance.

### Log revenue change

CSTP5 — **Chi phí không chính thức** is the only component that survives BH multiplicity adjustment:

- standardized beta = **0.03628**;
- cluster SE = 0.00888;
- t = 4.0845;
- p = **0.000129**;
- BH q = **0.001289**;
- 95% CI = **[0.01852, 0.05404]**;
- `exp(beta)-1` equivalent ≈ **3.69%**.

Interpretation: conditional on province fixed effects, year fixed effects, and the other lagged PCI dimensions, a one-standard-deviation higher prior-year CSTP5 score is associated with about 3.7% higher subsequent revenue ratio / log-revenue change. This is an association, not a causal effect.

CSTP6 has raw `p = 0.0540` but BH `q = 0.2701`; it therefore does not meet the multiplicity-adjusted criterion. No other component has `q < 0.05`.

The log-change model R² is 0.2873.

## COVID sensitivity

Excluding outcome years 2020–2021 leaves 567 observations and 63 province clusters.

For log revenue level, no component survives BH adjustment.

For log revenue change, CSTP5 remains the only BH-adjusted signal:

- standardized beta = **0.03840**;
- cluster SE = 0.01139;
- p = **0.001290**;
- BH q = **0.01290**;
- 95% CI = **[0.01564, 0.06117]**;
- `exp(beta)-1` equivalent ≈ **3.92%**.

The direction and magnitude are close to the full-sample estimate.

Caveat: the no-COVID change model removes 2020 and 2021 as outcome years, but the 2022 log change still uses 2021 revenue as its baseline. A stricter pandemic-window exclusion remains appropriate for the broader G5 robustness stage.

## Leave-one-province-out sensitivity

For the full-sample log-change model, CSTP5 is stable to dropping each province in turn:

- full beta = 0.03628;
- leave-one-province-out beta range = **[0.03403, 0.03947]**;
- maximum absolute coefficient change = 0.00319;
- sign flips = **0 / 63**.

For the log-level model, CSTP5 also keeps a positive sign under all 63 omissions, but the full model itself is not statistically robust after multiplicity adjustment; sign stability must not be mistaken for significance.

## Residual / design diagnostics

Recorded deterministic diagnostics:

| Specification | N | Rank / columns | Condition number | Residual RMSE | Max absolute residual |
|---|---:|---:|---:|---:|---:|
| full — log revenue | 693 | 83 / 83 | 136.89 | 0.14329 | 0.67243 |
| full — log change | 693 | 83 / 83 | 136.89 | 0.10034 | 0.93088 |
| no-COVID — log revenue | 567 | 81 / 81 | 138.96 | 0.14771 | 0.71120 |
| no-COVID — log change | 567 | 81 / 81 | 138.96 | 0.10148 | 0.89364 |

There is no rank-deficiency warning in the fitted design.

## Reproducibility

Code:

`src/eureka2026/fe_baseline.py`

Run:

```bash
python -m src.eureka2026.fe_baseline
```

Runtime versions used for the recorded results:

- NumPy 2.3.5;
- statsmodels 0.14.6.

Result artifact SHA-256:

- coefficients: `7062c90249e350c43fc99147f3dded50a864383ab51e47306cdd14f88ae32495`;
- influence: `077c03fa5be000bcbb4879d5e6ddc3cf2a37bc39b08b031bebc9ab91e1ced1bb`;
- scaling: `960a0b6df763da43676217d739d2c8b940322aa50bbf1857a4f6fe7dbf1c456d`.

Local validation:

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

15/15 tests passed before the PR.

## Gate decision

G3 passes.

The result does **not** justify calling CSTP5 the “most impactful” PCI component. The defensible statement is narrower: **CSTP5 is the only component showing a multiplicity-adjusted association with subsequent log-revenue change under the prespecified G3 full-sample model, and that association remains after excluding 2020–2021 outcome years and after dropping any one province.**

No comparable BH-adjusted signal appears in the log-revenue-level specification.

G4 should now test whether lagged PCI components add genuine out-of-sample predictive value beyond strong temporal baselines.
