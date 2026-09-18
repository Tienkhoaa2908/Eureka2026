# Literature review map — PCI, institutions, and enterprise outcomes

Updated: 2026-09-18

## Core measurement source

PCI/VCCI methodology states that PCI is built from business survey data plus published administrative sources, standardized into ten sub-indices and calibrated into a composite index. This matters because PCI is partly perception-based and its components are correlated measures of a broader institutional environment.

Source: https://www.pcivietnam.vn/en/about/pci-methodology.html
FAQ/weights: https://pcivietnam.vn/en/faqs.html

## Prior evidence the project must position against

### Nguyen, Le & Bryant (2013), Journal of World Business
Sub-national institutions, firm strategies, and firm performance: a multilevel study of private manufacturing firms in Vietnam.
Finding relevant to this project: local institutions interact with firm strategies and outcomes; firm-level and province-level variation should be modeled separately.
DOI: https://doi.org/10.1016/j.jwb.2012.06.008

### Huynh (2022), Asian-Pacific Economic Literature
Spatial effects of institutional quality on firm performance: evidence from Vietnam.
Finding relevant to this project: provincial institutions can have direct and spatial spillover relationships with firm performance, so neighboring-province dependence is a possible robustness issue.
DOI: https://doi.org/10.1111/apel.12362

### Asia-Pacific Journal of Regional Science (2024)
Total factor productivity and institutional quality in Vietnam: which institutions matter most?
Uses firm-level panel data and GMM; reports that not all PCI dimensions matter equally and highlights time costs and labor policy for TFP.
URL: https://link.springer.com/article/10.1007/s41685-024-00343-9

### Nguyen, Phong & Truc (2025)
Impact of Institutional Factors and Tax Revenue on Firm Performance Across Provincial Localities in Vietnam.
Uses 63-province data, 2015–2021, and GMM with additional province-level variables. Relevant because it demonstrates that aggregate province-level outcomes need controls and endogeneity discussion.
DOI: https://doi.org/10.3233/FAIA250083

### Kokko, Nguyen & Nilsson Hakkala (ADB, 2026)
Business Climate, Economic Complexity, and Performance at the Provincial Level in Viet Nam.
Uses 63 provinces and a difference-GMM design; reports that changes in PCI have limited effects on several manufacturing outcomes in many specifications.
URL: https://www.adb.org/publications/business-climate-economic-complexity-performance-provincial-viet-nam

### Thoa & Hung (2026), Hue University Journal of Science
The impact of the provincial competitiveness index on firms' market entry in Vietnam.
Uses 2017–2024 panel regressions with fixed effects and clustered robust standard errors; lagged PCI components are explicitly examined.
DOI: https://doi.org/10.26459/hueunijed.v135i5C.8471

### Linh (2026), Can Tho University Journal of Science
The impact of public governance quality and the business environment on GRDP of provinces and cities in Vietnam.
Uses 63 provinces, 2018–2024, FEM/REM with PAPI and PCI; useful as a current province-level macro outcome comparator.
DOI: https://doi.org/10.22144/ctujos.2026.178

## Research gap we can defensibly claim

Do NOT claim that nobody has studied PCI and performance in Vietnam. That is false.

A defensible gap is narrower:
- recent studies use different outcomes, samples, and econometric designs and do not agree on which institutional dimensions matter;
- many applied studies emphasize in-sample coefficients, while strict time-ordered out-of-sample validation of the same province panel is less commonly foregrounded;
- a transparent comparison of interpretable two-way FE estimates, lagged PCI components, and time-respecting ML prediction on 2010–2024 province-level enterprise revenue can contribute evidence about robustness and predictive usefulness, provided data integrity is established.

## Implications for hypotheses

Use component-specific hypotheses only where theory/literature supports them. Avoid a post-hoc 'winner' hypothesis.
Primary empirical question should be stability: whether a component's signal persists across outcomes, periods, and modeling frameworks.

## Literature-review TODO

Before final manuscript:
1. Build a structured evidence table: sample, level, outcome, PCI measure, estimator, controls, main findings, limitations.
2. Read full methods/results (not only abstracts) for the 5–7 closest studies.
3. Add citations on panel FE, clustered SE, temporal cross-validation, and correlated-feature importance.
4. Add source documentation for GSO/NSO enterprise-revenue definitions and price/nominal units.
