# ENHANCED IDENTIFICATION PLAN

Updated: 2026-09-19

## A. Existing-data deep inference

The original two-way FE result is no longer treated as the endpoint. The following robustness designs are required and have been run in exploratory form in DEEP-INFERENCE-02:

1. province FE + year FE;
2. province FE + region×year FE;
3. province FE + year FE + province-specific linear trends;
4. province FE + region×year FE + province-specific trends;
5. joint PCI-block Wald test and partial R²;
6. institutional-change specification using ΔPCI components;
7. rolling five-year windows;
8. 5,000 province-cluster bootstrap resamples;
9. Driscoll–Kraay-type covariance sensitivity;
10. reverse-temporal placebo;
11. official composite PCI vs component-specific results;
12. quadratic CSTP5 test.

Interpretation must focus on stability and conditional explanatory content, not the number of significant specifications.

## B. Multi-margin confirmatory model

For each prespecified outcome m:

`y^m_it = α_i + λ_t + β_m' PCI_i,t-1 + γ'X_i,t-1 + ε_it`

Primary:
- province FE;
- year FE;
- province-clustered uncertainty;
- BH FDR within the ten-component family;
- joint Wald test for the ten PCI components.

Robustness:
- region×year FE;
- province-specific linear trends where T permits;
- institutional-change (ΔPCI) specification;
- strict COVID-period sensitivity;
- leave-one-region/year influence checks.

## C. Accounting/econometric decomposition

Using matched V05.08/V05.11/V05.23 data:

`g_R = g_F + g_{L/F} + g_{R/L}`.

Run all four regressions on the **same complete-case sample and identical design matrix**.

For each PCI component j verify numerically:

`β^R_j ≈ β^F_j + β^{L/F}_j + β^{R/L}_j`.

Use province-cluster bootstrap to obtain uncertainty for the three channel contributions and for contrasts between margins.

This is the primary mechanism analysis.

## D. Entry validation

Prespecified extensive-margin outcomes:
- log active firms per 1,000 residents;
- change in that density;
- new-registration flow normalized by lagged active firms.

The entry analysis is conceptually separate from the accounting decomposition because new registrations and active firms are not identical enterprise universes.

## E. Profitability validation

Profit rate and pretax-profit outcomes are secondary. They test whether a governance signal that appears in revenue-per-worker also reaches profitability.

Avoid log pretax profit when values can be negative. Use published profit rate or an appropriate signed transformation only if justified before estimation.

## F. Multiple-testing hierarchy

1. outcome-level joint PCI-block test;
2. prespecified component family;
3. BH FDR within each outcome family;
4. distinguish confirmatory hypotheses from exploratory components;
5. never choose the main margin after seeing which p-value is smallest.

## G. Causal boundary

Even with stronger FE and new outcomes, the study remains associational unless a credible exogenous governance shock/instrument is established.

Region×year FE and province trends address important confounding patterns but do not solve all time-varying endogeneity.

## H. Candidate causal extension — only if data support it

The 2026 ADB SEZ work shows that special economic zone coverage changed both local business outcomes and governance. This is scientifically important but makes SEZ exposure a potential confounder/mediator, not an automatic instrument for PCI.

Do not use SEZ exposure as an IV for PCI without an exclusion restriction that can be defended.

## I. Publication decision rule

A stronger paper requires at least one of:

1. a stable, theory-consistent margin-specific association with clear decomposition;
2. a compelling null showing governance moves entry but not intensive performance (or vice versa), supported across measures;
3. a credible mechanism/heterogeneity result that reconciles prior Vietnam studies.

If none materializes, do not oversell the project as a journal-ready causal contribution.
