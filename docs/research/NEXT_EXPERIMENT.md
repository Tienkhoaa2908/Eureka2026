# NEXT EXPERIMENT — STAT-BASELINE-01

Priority: P0
Gate: G3 Statistical baseline

## Question

After controlling for time-invariant province characteristics and common year shocks, which one-year-lagged PCI sub-indices show statistically and substantively stable within-province associations with enterprise revenue outcomes in 2014–2024?

This is an association question, not a causal-effect claim.

## Canonical input

`data/processed/panel.csv`

Expected SHA-256:

`a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`

Rebuild first with:

```bash
python -m src.eureka2026.pipeline
```

## Primary sample

- years: 2014–2024;
- 63 provinces × 11 years = 693 rows;
- complete one-year-lagged `cstp1..cstp10`.

## Prespecified outcomes

Primary:
- `log_revenue = ln(Doanh_thu_ty_dong)`.

Robustness:
- `log_revenue_change = log_revenue_it - log_revenue_i,t-1`.

The legacy percent-growth column is not the primary inferential transformation; it is retained as an audit-friendly descriptive field.

## Predictors

`cstp1_lag1 .. cstp10_lag1`.

Standardize each predictor over the analysis sample using committed code and record mean/SD so coefficients are comparable by one-standard-deviation changes.

## Model

Two-way fixed effects:

`y_it = alpha_i + lambda_t + beta' Z(PCI_components_i,t-1) + epsilon_it`

where:
- `alpha_i` = province fixed effects;
- `lambda_t` = year fixed effects;
- standard errors clustered by province.

## Required diagnostics

1. Confirm exact N = 693 and 63 province clusters.
2. Report coefficient, clustered SE, 95% CI, p-value.
3. Report Benjamini–Hochberg FDR-adjusted q-values across the 10 component coefficients for each outcome.
4. Compare coefficient sign/magnitude between log-level and log-change outcomes.
5. Re-estimate excluding 2020–2021 as a prespecified COVID sensitivity.
6. Flag influential observations/provinces using residual/leverage or leave-one-province-out sensitivity feasible for the fitted implementation.
7. Record model rank/conditioning warnings if present.
8. Do not choose a “winner” component from raw p-values alone.

## Pass criteria

- exact canonical input checksum recorded;
- model specification is executable from committed code;
- N/cluster counts match prespecification;
- clustered covariance is used;
- result tables and diagnostics are generated deterministically;
- COVID sensitivity is produced;
- no causal language in automated summaries;
- every reported number maps to a committed output artifact.

## Output artifacts

- `src/eureka2026/fe_baseline.py` or equivalent;
- model dependency declaration;
- `artifacts/results/STAT-BASELINE-01_coefficients.csv` locally;
- `artifacts/qa/STAT-BASELINE-01.md`;
- compact machine-readable model metadata;
- tests for sample construction, standardization, and FDR logic.

## Unlocks

G4 time-respecting predictive benchmark and G5 broader robustness work.
