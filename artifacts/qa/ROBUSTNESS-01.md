# ROBUSTNESS-01 — robustness and falsification checks

Date: 2026-09-18  
Gate: G5 Robustness  
Verdict: **PASS with outcome-data caveat**

## Purpose

Stress-test the G3 result that lagged CSTP5 (Informal Charges / Chi phí không chính thức) is positively associated with subsequent log-revenue change in the 2014–2024 two-way fixed-effects model.

The objective is to identify the boundary of the finding, not to accumulate significant specifications.

## Canonical input

`data/processed/panel.csv`  
SHA-256: `a5b76b667ed0e00a8422eeb4da48f78491824f6529feaf2e6ee9031c365211dd`

Panel regressions retain province and year fixed effects and province-clustered inference. Component-family checks use BH FDR.

## Main robustness findings

### Stricter pandemic window

Exclude outcome years 2020, 2021, **and 2022**, so 2022 log-change cannot inherit 2021 revenue as its baseline.

N=504, years 2014–2019 and 2023–2024.

CSTP5:
- beta = **0.03316**
- p = **0.00672**
- BH q = **0.06720**
- 95% CI [0.00953, 0.05679]

Direction and magnitude remain positive, but the result no longer passes q<0.05. This is a material weakening.

### Contemporaneous 10-component specification

2013–2024, N=756.

CSTP5:
- beta ≈ **-0.00008**
- p = 0.99419
- BH q = 0.99419

The primary signal is specifically lagged, not a generic same-year relationship.

### Longer-period 9-component specification

2011–2024, N=882, omitting CSTP6 because it is structurally unavailable before 2013.

CSTP5:
- beta = **0.01170**
- p = 0.10175
- BH q = 0.31121

The primary result does not generalize to the longer nine-component period.

### Winsorized outcome

1st/99th percentile winsorization, N=693.

CSTP5:
- beta = **0.03416**
- p = **0.000149**
- BH q = **0.001491**
- 95% CI [0.01726, 0.05105]

The G3 association is not driven by a small number of extreme outcome observations.

## Targeted CSTP5 checks

### Single-component lag-1
- beta = **0.01507**
- p = 0.04358
- 95% CI [0.00045, 0.02969]

### Distributed lag, 2015–2024, N=630
- lag 1 beta = **0.02514**, p = **0.00824**
- lag 2 beta = **-0.00480**, p = 0.59695

Signal is concentrated at the one-year lag.

### Future-lead placebo, 2014–2023, N=630
Regress outcome at t on CSTP5 at t+1:
- beta = **0.00704**
- p = 0.47656
- 95% CI [-0.01261, 0.02669]

No detectable future-lead relationship. This is mildly reassuring about temporal ordering but is not causal identification.

## Leave-one-out checks

### Leave one year out
Across 11 omissions:
- beta range = **[0.03191, 0.04924]**
- sign flips = **0/11**

### Leave one macro-region out
Across six omissions:
- beta range = **[0.02907, 0.03990]**
- sign flips = **0/6**

## Residual cross-sectional-dependence diagnostic

Pesaran CD on full log-change residuals:
- N entities = 63
- T = 11
- mean pairwise residual correlation = -0.00945
- CD = -1.3853
- asymptotic p = 0.1660

The diagnostic does not reject cross-sectional independence, but short T limits power. This is not evidence that spatial spillovers are absent.

## Outcome/deflation caveat

Aggregate revenue remains nominal and scale-dependent. A common national deflator would be algebraically absorbed by full year fixed effects in a log-level two-way-FE specification, so it would not create an independent robustness dimension for the FE coefficient. A genuinely different outcome robustness exercise requires verified province-specific prices or scale-normalized outcomes such as revenue per active enterprise/worker.

Those denominator data are not yet part of the verified canonical panel, so they are not silently merged at this stage.

## Interpretation boundary

CSTP5 is **not** a universal or causal “winner.” The defensible result is narrower:

- positive in the prespecified lagged 2014–2024 joint model;
- stable to outlier, year, province and region omission;
- concentrated at lag one and has a null future-lead placebo;
- weakened below BH q<0.05 under the strict pandemic window;
- null in contemporaneous and longer nine-component specifications;
- does not yield incremental future-year predictive value beyond the best non-PCI baseline in G4.

## Reproducibility

Code: `src/eureka2026/robustness.py`

Run:
```bash
python -m src.eureka2026.robustness
```

Evidence:
- `artifacts/results/ROBUSTNESS-01_coefficients.csv`
- `artifacts/results/ROBUSTNESS-01_cstp5_targeted.csv`
- `artifacts/results/ROBUSTNESS-01_year_loo.csv`
- `artifacts/results/ROBUSTNESS-01_region_loo.csv`
- `artifacts/results/ROBUSTNESS-01_metadata.json`

## Gate decision

G5 **passes** for robustness/falsification of the available canonical outcome. Scale-normalized or province-deflated outcomes remain a future extension requiring additional verified data.
